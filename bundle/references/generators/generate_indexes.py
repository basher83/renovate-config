#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Generate every governed directory index; default to a read-only drift check.

Adapted from greenfield's generate_indexes.py: titles and descriptions come
from frontmatter, entry order is sorted by filename, and --write is explicit.
This version owns every bundle directory index and the repository
intake sources/evaluate/index.md; it imports no learning types or enforcement.
"""

import argparse
import ast
import difflib
import re
from pathlib import Path

import yaml

DEFAULT_BUNDLE = Path(__file__).resolve().parents[2]
TOOLING = {
    "attesters": "Deterministic bundle checks",
    "generators": "Derived index generation and drift checks",
    "ingest": "Source capture and byte-fidelity comparison",
}


def entries(directory: Path, bundle: Path | None = None) -> dict[str, str]:
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
        link = "/" + file.relative_to(bundle).as_posix() if bundle else file.name
        result[file.name] = f"* [{fm['title']}]({link}) - {fm['description']}"
    return result


def directories(bundle: Path) -> list[Path]:
    """Discover the hierarchy while excluding Python's transient bytecode cache."""
    return [bundle, *sorted(path for path in bundle.rglob("*")
                           if path.is_dir() and "__pycache__" not in path.relative_to(bundle).parts)]


def render(bundle: Path) -> dict[Path, str]:
    if not (bundle / "formatting.md").is_file():
        raise ValueError(f"{bundle}: expected this repository's formatting.md")
    outputs = {}
    for directory in directories(bundle):
        heading = "Repository knowledge" if directory == bundle else directory.name.replace("-", " ").title()
        text = '---\nokf_version: "0.2"\n---\n\n' if directory == bundle else ""
        text += f"# {heading}\n\n"
        concepts = entries(directory, bundle)
        if concepts:
            text += "## Concepts\n\n" + "\n".join(concepts[name] for name in sorted(concepts)) + "\n\n"
        children = [child for child in sorted(directory.iterdir())
                    if child.is_dir() and child.name != "__pycache__"]
        if children:
            text += "## Directories\n\n"
            for child in children:
                link = "/" + (child / "index.md").relative_to(bundle).as_posix()
                description = TOOLING.get(child.name, "Generated navigation for this directory")
                text += f"* [{child.name.replace('-', ' ').title()}]({link}) - {description}.\n"
            text += "\n"
        artifacts = [file for file in sorted(directory.iterdir()) if file.is_file() and file.suffix != ".md"]
        if artifacts:
            text += "## Supporting artifacts\n\n"
            for file in artifacts:
                if file.suffix == ".py":
                    doc = ast.get_docstring(ast.parse(file.read_text(encoding="utf-8")))
                    description = doc.splitlines()[0] if doc else "Supporting Python tool."
                else:
                    description = "Preserved source capture." if file.name.endswith(".py.txt") else "Supporting artifact."
                link = "/" + file.relative_to(bundle).as_posix()
                text += f"* [{file.name}]({link}) - {description}\n"
            text += "\n"
        if (directory / "log.md").is_file():
            link = "/" + (directory / "log.md").relative_to(bundle).as_posix()
            text += f"## History\n\n* [Change log]({link}) - Chronological changes to this scope.\n\n"
        if not concepts and not children and not artifacts and not (directory / "log.md").is_file():
            text += "## Contents\n\nNo concepts or supporting artifacts are present.\n"
        outputs[directory / "index.md"] = text.rstrip() + "\n"
    intake = bundle.parent / "sources/evaluate"
    if not intake.is_dir():
        raise ValueError(f"{intake}: expected pending-evaluation directory")
    items = entries(intake)
    outputs[intake / "index.md"] = ("# Sources to evaluate\n\n## Pending records\n\n" +
                                     "\n".join(items[name] for name in sorted(items)) + "\n")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("bundle", nargs="?", type=Path, default=DEFAULT_BUNDLE)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="check without writing (default)")
    mode.add_argument("--write", action="store_true", help="write the complete governed index scope")
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
