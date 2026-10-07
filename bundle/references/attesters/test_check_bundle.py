#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3", "markdown-it-py==4.0.0", "mdit-py-plugins==0.5.0"]
# ///
"""Regression checks for verification history, source separation, and capture fidelity.

Fixtures live in temporary directories; repository files are never changed.
Run with the same compatible environment as check_bundle.py.
"""

import copy
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.dont_write_bytecode = True
CHECKER = Path(__file__).with_name("check_bundle.py").resolve()
BUNDLE = CHECKER.parents[2]
NOW = datetime.now(timezone.utc)
spec = importlib.util.spec_from_file_location("bundle_checker", CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class VerificationHistoryTests(unittest.TestCase):
    def setUp(self):
        self.file = BUNDLE / "governance.md"
        self.fm, self.body = checker.document(self.file)
        self.fm = copy.deepcopy(self.fm)
        self.fm["generated"]["at"] = (NOW - timedelta(hours=1)).isoformat()

    def test_historical_verification_mapping_is_preserved(self):
        event = {"by": "human:test", "at": (NOW - timedelta(hours=2)).isoformat()}
        self.fm["verified"] = event.copy()
        checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)
        self.assertEqual(self.fm["verified"], event)

    def test_verification_list_can_span_generation(self):
        events = [{"by": "human:test", "at": (NOW - timedelta(hours=2)).isoformat()},
                  {"by": "process:test", "at": (NOW - timedelta(minutes=30)).isoformat()}]
        self.fm["verified"] = copy.deepcopy(events)
        checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)
        self.assertEqual(self.fm["verified"], events)

    def test_future_and_naive_verification_remain_invalid(self):
        for value in ((NOW + timedelta(hours=1)).isoformat(), NOW.replace(tzinfo=None).isoformat()):
            with self.subTest(value=value):
                self.fm["verified"] = {"by": "human:test", "at": value}
                with self.assertRaises(ValueError):
                    checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)

    def test_bundle_vocabulary_rejects_unaccepted_tags_and_allows_no_tags(self):
        self.fm["tags"] = ["renovate"]
        with self.assertRaisesRegex(ValueError, "accepted vocabulary"):
            checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)
        self.fm.pop("tags")
        checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)

    def test_bundle_description_requires_single_sentence_shape(self):
        for description in ("A fragment", "First sentence. Second sentence."):
            with self.subTest(description=description):
                self.fm["description"] = description
                with self.assertRaisesRegex(ValueError, "single-sentence"):
                    checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)

    def test_resource_binding_is_distinct_from_derivation_and_checks_paths(self):
        self.fm["resource"] = "/governance.md"
        checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)
        self.fm["resource"] = "governance.md"
        with self.assertRaisesRegex(ValueError, "bundle-absolute"):
            checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)

    def test_usage_windows_require_complete_ordered_ranges(self):
        past = (NOW - timedelta(hours=2)).isoformat()
        later = (NOW - timedelta(hours=1)).isoformat()
        for window in ({}, {"from": past}, {"to": later}, {"from": later, "to": past}, []):
            for owner in (self.fm, self.fm["sources"][0]):
                with self.subTest(window=window, source=owner is not self.fm):
                    owner["usage_window"] = window
                    with self.assertRaisesRegex(ValueError, "usage_window"):
                        checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)
                    del owner["usage_window"]
        self.fm["usage_window"] = {"from": past, "to": later}
        self.fm["sources"][0]["usage_window"] = {"from": past, "to": later}
        checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)

    def test_usage_count_requires_nonnegative_integer(self):
        source = self.fm["sources"][0]
        for count in (-1, True, 1.5, "1"):
            with self.subTest(count=count):
                source["usage_count"] = count
                with self.assertRaisesRegex(ValueError, "nonnegative integer"):
                    checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)
        for count in (0, 1):
            source["usage_count"] = count
            checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)

    def test_stale_after_requires_offset_and_allows_future_expiration(self):
        for value in ([], {}, None, 1, NOW.replace(tzinfo=None).isoformat(), "invalid"):
            with self.subTest(value=value):
                self.fm["stale_after"] = value
                with self.assertRaises(ValueError):
                    checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)
        for value in (NOW - timedelta(days=1), NOW + timedelta(days=1)):
            self.fm["stale_after"] = value.isoformat()
            checker.authored_metadata(BUNDLE, self.file, self.fm, self.body, NOW)

    def test_metadata_validation_preserves_yaml_round_trip(self):
        self.fm["stale_after"] = (NOW + timedelta(days=1)).isoformat()
        self.fm["usage_window"] = {"from": (NOW - timedelta(days=1)).isoformat(), "to": NOW.isoformat()}
        self.fm["sources"][0]["usage_count"] = 0
        self.fm["verified"] = [{"by": "human:test", "at": (NOW - timedelta(days=2)).isoformat()}]
        original = copy.deepcopy(self.fm)
        restored = checker.yaml.load(checker.yaml.safe_dump(self.fm), Loader=checker.UniqueLoader)
        checker.authored_metadata(BUNDLE, self.file, restored, self.body, NOW)
        self.assertEqual(restored, original)

    def test_markdown_destinations_share_path_and_anchor_validation(self):
        for body, error in (
            ('[policy](governance.md "Policy")', "bundle-absolute"),
            ("[policy](/missing.md 'Policy')", "inside this repository"),
            ('[policy](</missing.md> "Policy")', "inside this repository"),
            ('[policy][ref]\n\n[ref]: governance.md "Policy"', "bundle-absolute"),
            ('[policy][]\n\n[policy]: /missing.md', "inside this repository"),
            ('[policy]\n\n[policy]: /missing.md', "inside this repository"),
            ('[policy](/governance.md#missing "Policy")', "broken local anchor"),
            ('![policy](/missing.md "Policy")', "inside this repository"),
        ):
            with self.subTest(body=body):
                with self.assertRaisesRegex(ValueError, error):
                    checker.markdown_links(BUNDLE, self.file, body)
        for body in (
            '[policy](/governance.md "Policy")',
            '[policy][ref]\n\n[ref]: /governance.md "Policy"',
            '[policy][]\n\n[policy]: /governance.md',
            '[policy]\n\n[policy]: /governance.md',
            '`[example](/missing.md "Title")`',
            '```markdown\n[example](/missing.md "Title")\n```',
            '~~~markdown\n[example](/missing.md)\n~~~',
        ):
            with self.subTest(body=body):
                checker.markdown_links(BUNDLE, self.file, body)


class HistoryTests(unittest.TestCase):
    def test_log_is_not_a_concept_and_dates_are_newest_first(self):
        with tempfile.TemporaryDirectory(prefix="bundle-history-") as directory:
            log = Path(directory) / "log.md"
            log.write_text("# History\n\n## 2026-10-06\n\n* **Update**: Change\n\n## 2026-10-05\n\n* **Creation**: Prior change\n")
            checker.history(log)
            for text in ("---\ntype: History\n---\n\n## 2026-10-06\n",
                         "# History\n\n## October 6\n", "# History\n\n## 2026-10-05\n\n## 2026-10-06\n"):
                with self.subTest(text=text):
                    log.write_text(text)
                    with self.assertRaises(ValueError):
                        checker.history(log)

    def test_log_rejects_entry_before_first_date_heading(self):
        with tempfile.TemporaryDirectory(prefix="bundle-history-") as directory:
            log = Path(directory) / "log.md"
            log.write_text("# History\n\n* **Update**: Undated change\n\n"
                           "## 2026-10-06\n\n* **Creation**: Dated change\n")
            with self.assertRaisesRegex(ValueError, "before a dated group"):
                checker.history(log)

    def test_log_rejects_unaccepted_labels_and_nested_lists(self):
        with tempfile.TemporaryDirectory(prefix="bundle-history-") as directory:
            log = Path(directory) / "log.md"
            for entry in ("* **Validation**: Change", "* Change", "* **Update**: Change\n  * Nested"):
                with self.subTest(entry=entry):
                    log.write_text("# History\n\n## 2026-10-06\n\n" + entry + "\n")
                    with self.assertRaises(ValueError):
                        checker.history(log)

    def test_all_nested_list_markers_are_rejected_without_blank_line(self):
        with tempfile.TemporaryDirectory(prefix="bundle-history-") as directory:
            log = Path(directory) / "log.md"
            for marker in ("*", "+", "-", "1.", "2.", "1)"):
                with self.subTest(marker=marker):
                    log.write_text("# History\n\n## 2026-10-06\n\n* **Update**: Probe.\n  "
                                   + marker + " Nested event.\n")
                    with self.assertRaisesRegex(ValueError, "flat list"):
                        checker.history(log)

    def test_numbered_log_entries_require_date_and_label(self):
        with tempfile.TemporaryDirectory(prefix="bundle-history-") as directory:
            log = Path(directory) / "log.md"
            for marker in ("1.", "1)"):
                log.write_text("# History\n\n## 2026-10-06\n\n" + marker + " Unlabelled.\n")
                with self.assertRaisesRegex(ValueError, "accepted bold label"):
                    checker.history(log)
                log.write_text("# History\n\n" + marker + " **Update**: Undated.\n\n## 2026-10-06\n")
                with self.assertRaisesRegex(ValueError, "before a dated group"):
                    checker.history(log)
                log.write_text("# History\n\n## 2026-10-06\n\n" + marker + " **Update**: Labelled.\n")
                checker.history(log)

    def test_history_validates_titled_and_reference_links(self):
        with tempfile.TemporaryDirectory(prefix="bundle-history-") as directory:
            log = Path(directory) / "log.md"
            for link in ('[policy](/missing.md "Policy")', '[policy][ref]\n\n[ref]: /missing.md'):
                log.write_text("# History\n\n## 2026-10-06\n\n* **Update**: " + link + "\n")
                with self.assertRaisesRegex(ValueError, "inside this repository"):
                    checker.history(log)


class CaptureHeaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bundle-check-regression-")
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name) / "repository"
        root.mkdir()
        self.bundle = root / "bundle"
        shutil.copytree(BUNDLE, self.bundle)
        for name in ("AGENTS.md", "README.md", "mise.toml", ".rumdl.toml"):
            shutil.copyfile(BUNDLE.parent / name, root / name)
        shutil.copytree(BUNDLE.parent / ".github", root / ".github")
        shutil.copytree(BUNDLE.parent / "sources", root / "sources")
        for name in ("examples", "presets", "docs"):
            shutil.copytree(BUNDLE.parent / name, root / name)

    def run_checker(self):
        return subprocess.run([sys.executable, "-B", str(CHECKER), str(self.bundle),
                               "--now", NOW.isoformat()], capture_output=True, text=True)

    def run_mise(self, task):
        root = self.bundle.parent
        env = os.environ.copy()
        # Trust only the owned fixture for this subprocess; do not persist trust settings.
        env["MISE_TRUSTED_CONFIG_PATHS"] = str(root.resolve())
        return subprocess.run(["mise", "run", task], cwd=root, env=env,
                              capture_output=True, text=True, timeout=60)

    def test_default_mise_rejects_symlinked_bundle_root_without_writes(self):
        root = self.bundle.parent
        other = root.parent / "other-checkout"
        shutil.copytree(root, other)
        original_bundle = root / "original-bundle"
        self.bundle.rename(original_bundle)
        self.bundle.symlink_to(other / "bundle", target_is_directory=True)
        sentinel = other / "bundle/index.md"
        sentinel.write_text("Other checkout's index must remain unchanged.\n")
        before = {file: file.read_bytes() for directory in (original_bundle, root / "sources", other)
                  for file in directory.rglob("*") if file.is_file()}
        for task in ("bundle:generate", "bundle:check", "bundle:finalize"):
            with self.subTest(task=task):
                result = self.run_mise(task)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("symlink in governed scope", result.stdout + result.stderr)
                self.assertNotIn("WROTE", result.stdout + result.stderr)
                for file, raw in before.items():
                    self.assertEqual(file.read_bytes(), raw, str(file))
        for tool in ("attesters/check_bundle.py", "generators/generate_indexes.py"):
            result = subprocess.run([sys.executable, "-B", str(original_bundle / "references" / tool),
                                     str(self.bundle)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("symlink in governed scope", result.stdout)

    def test_default_mise_accepts_links_in_provenance_footnotes(self):
        file = self.bundle / "governance.md"
        original = file.read_text()
        for definition in (
            '[^exemplar-intent]: [record](../sources/evaluate/2026-10-06-exemplar-intent.md)',
            '[^exemplar-intent]: [record](../sources/evaluate/2026-10-06-exemplar-intent.md "Record")',
            '[^exemplar-intent]:\n    [record][evidence]\n\n'
            '[evidence]: ../sources/evaluate/2026-10-06-exemplar-intent.md "Record"',
        ):
            with self.subTest(definition=definition):
                file.write_text(re.sub(r"^\[\^exemplar-intent\]:.*$", definition, original, flags=re.M))
                for task in ("bundle:check", "bundle:finalize", "bundle:lint"):
                    result = self.run_mise(task)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_provenance_footnote_links_still_enforce_paths_and_anchors(self):
        file = self.bundle / "governance.md"
        original = file.read_text()
        for definition, error in (
            ('[^exemplar-intent]: [record](governance.md "Record")', "bundle-absolute"),
            ('[^exemplar-intent]: [record](/missing.md "Record")', "inside this repository"),
            ('[^exemplar-intent]: [record][evidence]\n\n[evidence]: /missing.md', "inside this repository"),
            ('[^exemplar-intent]: [record](/governance.md#missing "Record")', "broken local anchor"),
        ):
            with self.subTest(definition=definition):
                file.write_text(re.sub(r"^\[\^exemplar-intent\]:.*$", definition, original, flags=re.M))
                result = self.run_mise("bundle:check")
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(error, result.stdout)

    def test_original_headers_and_raw_snapshots_pass(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_authored_pending_record_rejects_broken_source_pointer(self):
        file = self.bundle.parent / "sources/evaluate/2026-10-06-review-reconciliation.md"
        file.write_text(file.read_text().replace("resource: shared-agent-policy-repository-review.md",
                                                "resource: missing-review.md"))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("2026-10-06-review-reconciliation.md: source must resolve", result.stdout)
        self.assertNotIn("derived index drift", result.stdout)

    def test_authored_pending_record_rejects_unmatched_footnote(self):
        file = self.bundle.parent / "sources/evaluate/2026-10-06-exemplar-intent.md"
        file.write_text(file.read_text() + "\nUnmatched evidence.[^missing]\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("2026-10-06-exemplar-intent.md: source/footnote join mismatch", result.stdout)
        self.assertNotIn("derived index drift", result.stdout)

    def test_pending_evidence_cannot_return_to_bundle(self):
        shutil.copyfile(self.bundle.parent / "sources/evaluate/okf-spec.md",
                        self.bundle / "references/okf-spec.md")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("raw capture belongs outside", result.stdout)

    def test_source_pointer_cannot_escape_repository(self):
        fm, body = checker.document(self.bundle / "governance.md")
        fm["sources"][0]["resource"] = "../../outside.md"
        (self.bundle.parent.parent / "outside.md").write_text("outside repository")
        with self.assertRaisesRegex(ValueError, "inside this repository"):
            checker.authored_metadata(self.bundle, self.bundle / "governance.md", fm, body, NOW)

    def test_intake_index_drift_is_detected_and_regeneration_repairs_it(self):
        index = self.bundle.parent / "sources/evaluate/index.md"
        original = index.read_bytes()
        index.write_bytes(original + b"\nUnowned status explanation.\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("sources/evaluate/index.md: derived index drift", result.stdout)
        generator = BUNDLE / "references/generators/generate_indexes.py"
        repair = subprocess.run([sys.executable, "-B", str(generator), str(self.bundle), "--write"],
                                capture_output=True, text=True)
        self.assertEqual(repair.returncode, 0, repair.stdout + repair.stderr)
        self.assertEqual(index.read_bytes(), original)
        self.assertEqual(self.run_checker().returncode, 0)

    def test_relative_in_bundle_cross_link_is_rejected(self):
        file = self.bundle / "governance.md"
        file.write_text(file.read_text().replace("](/formatting.md)", "](formatting.md)"))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("in-bundle path must be bundle-absolute", result.stdout)

    def test_root_log_is_required(self):
        (self.bundle / "log.md").unlink()
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("missing required root history", result.stdout)

    def test_new_directory_requires_generated_navigation_and_preserves_description(self):
        directory = self.bundle / "references/nested"
        directory.mkdir()
        fm, _ = checker.document(self.bundle / "governance.md")
        fm["sources"] = []
        concept = directory / "example.md"
        concept.write_text("---\n" + checker.yaml.safe_dump(fm, sort_keys=False) + "---\n\n# Example\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("references/nested/index.md: derived index drift", result.stdout)
        generator = BUNDLE / "references/generators/generate_indexes.py"
        subprocess.run([sys.executable, "-B", str(generator), str(self.bundle), "--write"],
                       capture_output=True, text=True, check=True)
        index = (directory / "index.md").read_text()
        self.assertFalse(index.startswith("---"))
        self.assertIn("(/references/nested/example.md) - " + fm["description"], index)
        self.assertEqual(self.run_checker().returncode, 0)


    def test_generator_rejects_symlinks_before_any_index_writes(self):
        generator = BUNDLE / "references/generators/generate_indexes.py"
        external = self.bundle.parent.parent / "outside"
        external.mkdir()
        sentinel = external / "index.md"
        sentinel.write_text("Owned external bytes.\n")
        root_index = self.bundle / "index.md"
        root_index.write_text("Deliberate drift must survive failed generation.\n")
        before = {file: file.read_bytes() for file in self.bundle.rglob("index.md")}
        intake_index = self.bundle.parent / "sources/evaluate/index.md"
        before[intake_index] = intake_index.read_bytes()
        cases = ((self.bundle / "external", external),
                 (self.bundle / "references/internal", self.bundle / "references/ingest"),
                 (self.bundle / "references/upstream-code/index.md", sentinel),
                 (intake_index, sentinel),
                 (self.bundle / "dangling", external / "missing"))
        for link, destination in cases:
            with self.subTest(link=link):
                saved = link.read_bytes() if link.is_file() else None
                if link.exists():
                    link.unlink()
                link.symlink_to(destination, target_is_directory=destination.is_dir())
                for mode in ("--write", "--check"):
                    result = subprocess.run([sys.executable, "-B", str(generator), str(self.bundle), mode],
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("symlink in governed scope", result.stdout)
                    self.assertNotIn("WROTE", result.stdout)
                    self.assertEqual(sentinel.read_text(), "Owned external bytes.\n")
                    for file, raw in before.items():
                        if file != link:
                            self.assertEqual(file.read_bytes(), raw)
                result = self.run_checker()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("symlink in governed scope", result.stdout)
                link.unlink()
                if saved is not None:
                    link.write_bytes(saved)

    def test_generator_rejects_symlinked_intake_parent(self):
        generator = BUNDLE / "references/generators/generate_indexes.py"
        sources = self.bundle.parent / "sources"
        outside = self.bundle.parent.parent / "moved-sources"
        sources.rename(outside)
        sources.symlink_to(outside, target_is_directory=True)
        before = {file: file.read_bytes() for file in self.bundle.rglob("index.md")}
        result = subprocess.run([sys.executable, "-B", str(generator), str(self.bundle), "--write"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("symlink in governed scope", result.stdout)
        for file, raw in before.items():
            self.assertEqual(file.read_bytes(), raw)

    def test_titled_link_negative_controls_reach_full_checker(self):
        file = self.bundle / "governance.md"
        original = file.read_text()
        for link in ('[policy](governance.md "Policy")', '[policy](/missing.md "Policy")',
                     '[policy][ref]\n\n[ref]: /missing.md "Policy"'):
            with self.subTest(link=link):
                file.write_text(original + "\n" + link + "\n")
                result = self.run_checker()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertNotIn("derived index drift", result.stdout)
    def test_body_fidelity_is_still_enforced(self):
        file = self.bundle.parent / "sources/evaluate/okf-spec.md"
        file.write_bytes(file.read_bytes() + b"\nChanged imported content.\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("pinned body capture bytes changed", result.stdout)


if __name__ == "__main__":
    unittest.main()
