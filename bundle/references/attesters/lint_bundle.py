#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Lint authored knowledge and generated navigation without rewriting captures."""

import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from check_bundle import SNAPSHOTS


def lint(root: Path) -> int:
    indexes = {path.relative_to(root) for path in (root / "bundle").rglob("index.md")}
    indexes.add(Path("sources/evaluate/index.md"))
    captures = {Path("sources/evaluate") / name for name in SNAPSHOTS if name.endswith(".md")}
    authored = {Path("AGENTS.md"), Path("README.md")}
    for directory in ("bundle", "sources/evaluate", ".github"):
        authored.update(path.relative_to(root) for path in (root / directory).rglob("*.md"))
    authored -= indexes | captures
    groups = ((authored, 'MD025.front-matter-title = ""'), (indexes, "MD013.line-length = 240"))
    for paths, override in groups:
        names = sorted(path.as_posix() for path in paths)
        result = subprocess.run(["rumdl", "check", "--no-cache", "--no-exclude",
                                 "--deny-config-warnings", "--config", override,
                                 "--include", ",".join(names), *names], cwd=root, check=False)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(lint(Path(__file__).resolve().parents[3]))
