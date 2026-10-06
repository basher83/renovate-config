#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Generate this bundle's two indexes; default to a read-only drift check.

Adapted from greenfield's generate_indexes.py: titles and descriptions come
from frontmatter, existing entry order is retained, and --write is explicit.
This version owns only the bundle root and references/; it imports no learning
types, directory taxonomy, or repository enforcement.
"""

import argparse
import difflib
import re
from pathlib import Path

import yaml

DEFAULT_BUNDLE = Path(__file__).resolve().parents[2]
ENTRY = re.compile(r"^\* \[[^\]]+\]\(([^)]+)\) - .*$", re.M)
SNAPSHOTS = {
    "agent-working-policy-draft.md", "shared-agent-policy-repository-review.md", "okf-spec.md", "greenfield-framework.md",
    "greenfield-lifecycle-and-revision.md", "greenfield-evidence-boundary.md",
}
TOOLING = {
    "attesters": "Deterministic bundle checks",
    "generators": "Derived index generation and drift checks",
    "ingest": "Source capture and byte-fidelity comparison",
}


def entries(directory: Path) -> dict[str, str]:
    result = {}
    for file in sorted(directory.glob("*.md")):
        if file.name in {"index.md", "log.md"}:
            continue
        text = file.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            raise ValueError(f"{file}: missing frontmatter")
        fm = yaml.safe_load(match[1])
        if not isinstance(fm, dict):
            raise ValueError(f"{file}: frontmatter must be a mapping")
        for key in ("type", "title", "description"):
            if not isinstance(fm.get(key), str) or not fm[key].strip() or "\n" in fm[key]:
                raise ValueError(f"{file}: {key} must be a nonempty single-line string")
        result[file.name] = f"* [{fm['title']}]({file.name}) - {fm['description']}"
    return result


def ordered(index: Path, items: dict[str, str]) -> list[str]:
    prior = ENTRY.findall(index.read_text(encoding="utf-8")) if index.exists() else []
    names = list(dict.fromkeys(name for name in prior if name in items))
    return names + sorted(set(items) - set(names))


def render(bundle: Path) -> dict[Path, str]:
    if not (bundle / "formatting.md").is_file():
        raise ValueError(f"{bundle}: expected this repository's formatting.md")
    for file in bundle.rglob("*.md"):
        if file.parent not in {bundle, bundle / "references"}:
            raise ValueError(f"{file}: concept directory outside the declared index scope")
    root_items = entries(bundle)
    root_index = bundle / "index.md"
    root = '---\nokf_version: "0.2"\n---\n\n# Repository knowledge\n\n'
    root += "\n".join(root_items[name] for name in ordered(root_index, root_items))
    root += ("\n\n## References\n\n* [References](references/index.md) - Captured source documents "
             "and authored session records, with origins and fidelity limits.\n")
    refs = bundle / "references"
    items = entries(refs)
    reference_index = refs / "index.md"
    order = ordered(reference_index, items)
    reference = "# References\n\n## Source snapshots\n\n"
    reference += "\n".join(items[name] for name in order if name in SNAPSHOTS)
    reference += "\n\n## Session records\n\n"
    reference += "\n".join(items[name] for name in order if name not in SNAPSHOTS)
    reference += "\n\n## Tooling\n\n"
    for name, description in TOOLING.items():
        directory = refs / name
        scripts = sorted(p.name for p in directory.glob("*.py"))
        if not scripts:
            raise ValueError(f"{directory}: expected at least one Python script")
        reference += f"* [{name.title()}]({name}/) - {description}: {', '.join(scripts)}.\n"
    originals = sorted(p.name for p in (refs / "upstream-code").glob("*.py.txt"))
    if not originals:
        raise ValueError("expected captured upstream source code")
    reference += ("* [Upstream source code](upstream-code/) - Verbatim Python source snapshots, "
                  f"retained as evidence: {', '.join(originals)}.\n")
    return {root_index: root, reference_index: reference}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("bundle", nargs="?", type=Path, default=DEFAULT_BUNDLE)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="check without writing (default)")
    mode.add_argument("--write", action="store_true", help="write only the two declared indexes")
    args = parser.parse_args()
    try:
        drift = False
        for index, expected in render(args.bundle.resolve()).items():
            current = index.read_text(encoding="utf-8") if index.exists() else ""
            if current == expected:
                print(f"OK {index.name} in {index.parent.name}")
            elif args.write:
                index.write_text(expected, encoding="utf-8")
                print(f"WROTE {index}")
            else:
                drift = True
                print("".join(difflib.unified_diff(current.splitlines(True), expected.splitlines(True),
                                                 fromfile=str(index), tofile="regenerated")), end="")
        return int(drift)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
