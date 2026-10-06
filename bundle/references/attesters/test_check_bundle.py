#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Regression checks for verification history, source separation, and capture fidelity.

Fixtures live in temporary directories; repository files are never changed.
Run with the same compatible environment as check_bundle.py.
"""

import copy
import importlib.util
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

    def test_log_rejects_unaccepted_labels_and_nested_lists(self):
        with tempfile.TemporaryDirectory(prefix="bundle-history-") as directory:
            log = Path(directory) / "log.md"
            for entry in ("* **Validation**: Change", "* Change", "* **Update**: Change\n  * Nested"):
                with self.subTest(entry=entry):
                    log.write_text("# History\n\n## 2026-10-06\n\n" + entry + "\n")
                    with self.assertRaises(ValueError):
                        checker.history(log)


class CaptureHeaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bundle-check-regression-")
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name) / "repository"
        root.mkdir()
        self.bundle = root / "bundle"
        shutil.copytree(BUNDLE, self.bundle)
        for name in ("AGENTS.md", "README.md"):
            shutil.copyfile(BUNDLE.parent / name, root / name)
        shutil.copytree(BUNDLE.parent / ".github", root / ".github")
        shutil.copytree(BUNDLE.parent / "sources", root / "sources")

    def run_checker(self):
        return subprocess.run([sys.executable, "-B", str(CHECKER), str(self.bundle),
                               "--now", NOW.isoformat()], capture_output=True, text=True)

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

    def test_body_fidelity_is_still_enforced(self):
        file = self.bundle.parent / "sources/evaluate/okf-spec.md"
        file.write_bytes(file.read_bytes() + b"\nChanged imported content.\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("pinned body capture bytes changed", result.stdout)


if __name__ == "__main__":
    unittest.main()
