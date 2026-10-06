#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Regression checks for verification history and authored capture headers.

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


class CaptureHeaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bundle-check-regression-")
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.bundle = root / "bundle"
        shutil.copytree(BUNDLE, self.bundle)
        for name in ("AGENTS.md", "README.md"):
            shutil.copyfile(BUNDLE.parent / name, root / name)
        shutil.copytree(BUNDLE.parent / ".github", root / ".github")

    def run_checker(self):
        return subprocess.run([sys.executable, "-B", str(CHECKER), str(self.bundle),
                               "--now", NOW.isoformat()], capture_output=True, text=True)

    def test_original_headers_and_raw_snapshots_pass(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_authored_headers_are_rejected_without_changing_body(self):
        mutations = (
            ("type: Reference\n", "type: Reference\nsha256: invented-field\n", "undocumented"),
            ("by: codex_agent/GPT 6.1 Sol", "by: fictional-author", "actor must"),
            ("status: draft", "status: invented-standing", "lifecycle"),
            ("status: draft", "status: draft\nstatus: stable", "duplicate YAML key"),
        )
        for name, (mode, _) in checker.SNAPSHOTS.items():
            if mode != "body":
                continue
            file = self.bundle / "references" / name
            original = file.read_bytes()
            original_body = original[original.find(b"\n---\n", 4) + 6:]
            for before, after, message in mutations:
                with self.subTest(capture=name, mutation=message):
                    changed = original.replace(before.encode(), after.encode(), 1)
                    self.assertNotEqual(changed, original)
                    self.assertEqual(changed[changed.find(b"\n---\n", 4) + 6:], original_body)
                    file.write_bytes(changed)
                    result = self.run_checker()
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(f"references/{name}:", result.stdout)
                    self.assertIn(message, result.stdout)
                    file.write_bytes(original)

    def test_body_fidelity_is_still_enforced(self):
        file = self.bundle / "references" / "okf-spec.md"
        file.write_bytes(file.read_bytes() + b"\nChanged imported content.\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("pinned body capture bytes changed", result.stdout)


if __name__ == "__main__":
    unittest.main()
