#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3", "markdown-it-py==4.0.0", "mdit-py-plugins==0.5.0"]
# ///
"""Report bundle formatting rules that the governed checker does not enforce.

Usage:
    .agents/skills/bundle-conformance-audit/scripts/audit_unenforced.py
    .agents/skills/bundle-conformance-audit/scripts/audit_unenforced.py --include-intake

Use this after `mise run bundle:check` passes, to find violations of
bundle/formatting.md that the checker accepts: frontmatter field order,
source-entry order, block-style `generated`, and `generated.at` more than an
hour older than the last commit that changed the document body.

Do NOT use this as a replacement for `mise run bundle:check`, as a commit gate,
or as evidence that footnotes support their claims; that last check needs a
reader. It never writes files.

Options:
    --include-intake: Also report authored records in sources/evaluate/. They
        are outside the bundle, so treat those findings as flags, not fixes.

Notes:
    Run from the repository root. Exit status is 1 when findings are printed.
    Authoring precedes its commit, so a stamp within an hour of the commit is
    treated as current.
    A stale `generated.at` finding names the commit to inspect; resolve the
    producing harness from that commit's Entire-Checkpoint trailer before
    editing, and leave the stamp alone when the producer is ambiguous.
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.dont_write_bytecode = True
import yaml

FIELD_ORDER = ["type", "title", "description", "resource", "tags", "status", "generated", "verified", "sources"]
SOURCE_ORDER = ["id", "resource", "title", "author"]
RESERVED = {"index.md", "log.md"}
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
COMMIT_LAG = timedelta(hours=1)


def last_body_change(file: Path) -> tuple[str, datetime] | None:
    """Find the newest commit that changed a document outside its frontmatter.

    Args:
        file: Repository-relative path of the document.

    Returns:
        The abbreviated commit hash and author time, or None when the file has
        no committed body change.

    Raises:
        subprocess.CalledProcessError: If git cannot read the file's history.
    """
    log = subprocess.run(["git", "log", "--format=%h %aI", "--", str(file)],
                         check=True, capture_output=True, text=True).stdout.split("\n")
    for line in filter(None, log):
        commit, when = line.split()
        shown = subprocess.run(["git", "show", f"{commit}^:{file}"], capture_output=True, text=True)
        before = FRONTMATTER.sub("", shown.stdout) if shown.returncode == 0 else ""
        after = subprocess.run(["git", "show", f"{commit}:{file}"],
                               check=True, capture_output=True, text=True).stdout
        if before != FRONTMATTER.sub("", after):
            return commit, datetime.fromisoformat(when)
    return None


def audit(file: Path) -> list[str]:
    """Collect unenforced formatting findings for one document.

    Args:
        file: Repository-relative path of a concept or authored record.

    Returns:
        Finding messages; empty when the document conforms.

    Raises:
        ValueError: If the document has no parseable frontmatter mapping.
    """
    match = FRONTMATTER.match(file.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{file}: missing or unterminated frontmatter")
    fm = yaml.safe_load(match[1])
    if not isinstance(fm, dict):
        raise ValueError(f"{file}: frontmatter must be a mapping")
    findings = []
    known = [key for key in fm if key in FIELD_ORDER]
    if known != sorted(known, key=FIELD_ORDER.index):
        findings.append(f"field order is {known}")
    for source in fm.get("sources") or []:
        keys = [key for key in source if key in SOURCE_ORDER]
        if keys != sorted(keys, key=SOURCE_ORDER.index):
            findings.append(f"source {source.get('id')!r} key order is {keys}")
    if not re.search(r"^generated: \{ by: .+, at: .+ \}$", match[1], re.M):
        findings.append("generated is not an inline mapping")
    generated = fm.get("generated")
    stamp = generated.get("at") if isinstance(generated, dict) else None
    stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00")) if isinstance(stamp, str) else stamp
    change = last_body_change(file)
    if change and isinstance(stamp, datetime) and stamp + COMMIT_LAG < change[1]:
        findings.append(f"generated.at {stamp.isoformat()} predates body change {change[0]} at {change[1].isoformat()}")
    return findings


def main() -> int:
    """Print findings for every audited document.

    Returns:
        1 when any finding is printed, otherwise 0.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--include-intake", action="store_true",
                        help="also report authored records in sources/evaluate/")
    args = parser.parse_args()
    files = sorted(Path("bundle").rglob("*.md"))
    if args.include_intake:
        sys.path.insert(0, "bundle/references/attesters")
        from check_bundle import SNAPSHOTS
        intake = Path("sources/evaluate")
        files += [f for f in sorted(intake.rglob("*.md")) if f.relative_to(intake).as_posix() not in SNAPSHOTS]
    total = 0
    for file in files:
        if file.name in RESERVED:
            continue
        for finding in audit(file):
            print(f"{file}: {finding}")
            total += 1
    print(f"{total} finding(s) in rules the checker does not enforce")
    return int(bool(total))


if __name__ == "__main__":
    raise SystemExit(main())
