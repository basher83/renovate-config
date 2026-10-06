#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Check this bundle's metadata, source joins, indexes, and pinned capture bytes.

Adapted from greenfield's check_bundle.py with this repository's declared scope.
No learning vocabulary, body taxonomy, prose bans, or installed enforcement is
imported. Known snapshots are checked for fidelity; their original metadata and
link context are retained, not treated as newly authored local governance.
The checker cannot authenticate operator approval or establish factual accuracy.
"""

import argparse
import hashlib
import importlib.util
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
import yaml

DEFAULT_BUNDLE = Path(__file__).resolve().parents[2]
FIELDS = {
    "type", "title", "description", "resource", "tags", "status", "sources",
    "usage_window", "generated", "verified", "stale_after",
}
TAGS = {"governance", "enforcement", "formatting", "presets"}
LOG_LABELS = {"Update", "Creation", "Deprecation"}
SOURCE_FIELDS = {"id", "resource", "title", "author", "usage_count", "last_modified", "usage_window"}
ACTOR = re.compile(r"(?:[a-z][a-z0-9_-]*_agent/\S[^\r\n]*|human:\S+|process:\S+)\Z")
SNAPSHOTS = {
    "shared-agent-policy-repository-review.md": ("body", "c33855ebceb837b6f23d30d2bd76a313419718f6a8b7ca3de0c356f3383c8304"),
    "agent-working-policy-draft.md": ("body", "2905371720621dbaa1e95a2d7b928e6fc8bee9136762bcd67f236c1236fa1d8a"),
    "okf-spec.md": ("body", "26aa5da029278939f914e578107242d9607d4f2dc5fe153272b82f9ed1030101"),
    "greenfield-framework.md": ("raw", "7aed48800e0a8c3a7d17f846e9919a46aeb6a1cc817a26a7d3b3d8546298d268"),
    "greenfield-lifecycle-and-revision.md": ("raw", "0d34c130a9f244cf7cc1993a194011ab2b042cf92fa14f4c7db39af83ba19f0c"),
    "greenfield-evidence-boundary.md": ("raw", "af991166fb34531925fd51552055d351b220d3e277030400db389dbdf922c5d4"),
    "upstream-code/check_bundle.py.txt": ("raw", "0b93a347468b5ff2561a742f2b240502f2763ccf742709b47108041f0d19790c"),
    "upstream-code/generate_indexes.py.txt": ("raw", "5a9a1f2dc819413dded3d2220f9ee6e89ebf73ee3b04dc0317d40a3e74d1af43"),
    "upstream-code/ingest_agentsview_insight.py.txt": ("raw", "8d1d535dad6562a8ffe35c09eb724ee6eb36648da3174a66bf6fe7a5f7ca260d"),
    "upstream-code/ingest_subagent_review.py.txt": ("raw", "49052b574b8dc017c51b442a12b0a0e708d04e777b3ffa26d0cd55fadc271bde"),
}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate metadata keys instead of silently keeping the last value."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def document(file: Path) -> tuple[dict, str]:
    text = file.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("missing or unterminated frontmatter")
    fm = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a mapping")
    return fm, text[match.end():]


def timestamp(value, now: datetime) -> datetime:
    result = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timestamp needs an explicit UTC offset")
    if result > now:
        raise ValueError("timestamp is in the future")
    return result


def actor(value) -> None:
    if not isinstance(value, str) or not ACTOR.fullmatch(value):
        raise ValueError(f"actor must identify a harness/model, human, or process: {value!r}")


def window(value, now: datetime) -> None:
    if not isinstance(value, dict) or set(value) - {"from", "to"}:
        raise ValueError("usage_window must use documented from/to fields")
    parsed = {key: timestamp(item, now) for key, item in value.items()}
    if set(parsed) == {"from", "to"} and parsed["from"] > parsed["to"]:
        raise ValueError("usage_window starts after it ends")


def target(bundle: Path, origin: Path, resource: str) -> Path | None:
    url = urlsplit(resource)
    if url.scheme in {"http", "https", "mailto"}:
        if url.scheme != "mailto" and not url.netloc:
            raise ValueError(f"invalid URL: {resource}")
        return None
    if url.scheme or re.search(r"\s", resource):
        raise ValueError(f"source or link is not a followable URL/path: {resource!r}")
    decoded = unquote(url.path)
    if not decoded:
        return origin
    return (bundle / decoded.lstrip("/") if decoded.startswith("/") else origin.parent / decoded).resolve()


def local_target(bundle: Path, file: Path, resource: str) -> Path | None:
    """Resolve local paths within the repository and enforce bundle-absolute references."""
    resolved = target(bundle, file, resource)
    if resolved is not None:
        if not resolved.is_relative_to(bundle.parent) or not resolved.exists():
            raise ValueError(f"local path must resolve inside this repository: {resource}")
        if (file.is_relative_to(bundle) and resolved.is_relative_to(bundle)
                and not urlsplit(resource).path.startswith("/")):
            raise ValueError(f"in-bundle path must be bundle-absolute: {resource}")
    return resolved


def authored_metadata(bundle: Path, file: Path, fm: dict, body: str, now: datetime) -> None:
    if set(fm) - FIELDS:
        raise ValueError(f"undocumented frontmatter fields: {sorted(set(fm) - FIELDS)}")
    for key in ("type", "title", "description", "status"):
        if not isinstance(fm.get(key), str) or not fm[key].strip() or "\n" in fm[key]:
            raise ValueError(f"{key} must be a nonempty single-line string")
    if fm["status"] not in {"draft", "stable", "deprecated"}:
        raise ValueError("unknown lifecycle status")
    tags = fm.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(t, str) and t.strip() for t in tags):
        raise ValueError("tags must be a list of nonempty strings")
    if file.is_relative_to(bundle):
        if set(tags) - TAGS:
            raise ValueError(f"tags outside accepted vocabulary: {sorted(set(tags) - TAGS)}")
        description = fm["description"]
        if not re.fullmatch(r".+[.!?]", description) or re.search(r"[.!?]\s+\S", description):
            raise ValueError("description must have single-sentence punctuation; meaning requires human review")
    if "resource" in fm:
        if not isinstance(fm["resource"], str) or not fm["resource"].strip():
            raise ValueError("resource must be a nonempty URL/path")
        local_target(bundle, file, fm["resource"])
    if "usage_window" in fm:
        window(fm["usage_window"], now)
    generated = fm.get("generated")
    if not isinstance(generated, dict) or set(generated) != {"by", "at"}:
        raise ValueError("generated needs documented by and at fields")
    actor(generated["by"])
    timestamp(generated["at"], now)
    events = fm.get("verified", [])
    events = [events] if isinstance(events, dict) else events
    if not isinstance(events, list):
        raise ValueError("verified must be an event mapping or list")
    for event in events:
        if not isinstance(event, dict) or set(event) != {"by", "at"}:
            raise ValueError("verified events need documented by and at fields")
        actor(event["by"])
        # OKF keeps historical verification independent of the latest generation.
        timestamp(event["at"], now)
    sources = fm.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    ids = set()
    for source in sources:
        if not isinstance(source, dict) or set(source) - SOURCE_FIELDS:
            raise ValueError("source entries must use documented fields")
        for key in ("id", "resource", "title"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                raise ValueError(f"source {key} must be a nonempty string")
        if source["id"] in ids:
            raise ValueError(f"duplicate source ID: {source['id']}")
        ids.add(source["id"])
        if "author" in source:
            actor(source["author"])
        try:
            local_target(bundle, file, source["resource"])
        except ValueError as error:
            raise ValueError(f"source must resolve inside this repository using bundle-absolute paths: {source['resource']}") from error
        if "last_modified" in source:
            timestamp(source["last_modified"], now)
        if "usage_count" in source and (isinstance(source["usage_count"], bool) or
                                         not isinstance(source["usage_count"], int)):
            raise ValueError("source usage_count must be an integer")
        if "usage_window" in source:
            window(source["usage_window"], now)
    clean = re.sub(r"^```.*?^```\s*$", "", body, flags=re.M | re.S)
    definitions = re.findall(r"^\[\^([^\]]+)\]:", clean, re.M)
    uses = set(re.findall(r"\[\^([^\]]+)\](?!:)", clean))
    if len(definitions) != len(set(definitions)):
        raise ValueError("duplicate footnote definition")
    if ids != uses or set(definitions) != uses:
        raise ValueError(f"source/footnote join mismatch: sources={sorted(ids)}, uses={sorted(uses)}")
    for resource in re.findall(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)", clean):
        resolved = local_target(bundle, file, resource)
        fragment = unquote(urlsplit(resource).fragment)
        if resolved is not None and fragment and resolved.suffix == ".md":
            headings = re.findall(r"^#{1,6}\s+(.+)$", resolved.read_text(encoding="utf-8"), re.M)
            anchors = {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-") for heading in headings}
            if fragment not in anchors:
                raise ValueError(f"broken local anchor: {resource}")


def history(file: Path, bundle: Path | None = None) -> None:
    """Validate the reserved OKF log structure without treating it as a concept."""
    text = file.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        raise ValueError("log must not carry concept frontmatter")
    dates = []
    entry_count = 0
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:]
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", heading):
                raise ValueError("log date headings must use YYYY-MM-DD")
            dates.append(datetime.strptime(heading, "%Y-%m-%d").date())
        elif entry := re.match(r"^[*+-] (.+)$", line):
            if not dates:
                raise ValueError("log entry appears before a dated group")
            label = re.match(r"\*\*([^*]+)\*\*", entry[1])
            if not label or label[1] not in LOG_LABELS:
                raise ValueError("log entry must begin with an accepted bold label")
            entry_count += 1
    if not dates:
        raise ValueError("log needs ISO date headings")
    if dates != sorted(set(dates), reverse=True):
        raise ValueError("log dates must be unique and newest first")
    if not entry_count:
        raise ValueError("log needs prose entries")
    if re.search(r"^[ \t]+[*+-] |^\d+\. ", text, re.M):
        raise ValueError("log entries must form a flat list")
    for resource in re.findall(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)", text):
        local_target(bundle or file.parent, file, resource)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("bundle", nargs="?", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--now", help="explicit UTC-offset timestamp for reproducible temporal checks")
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    errors = []
    try:
        now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else datetime.now(timezone.utc)
        if now.tzinfo is None:
            raise ValueError("--now needs an explicit UTC offset")
        if not (bundle / "log.md").is_file():
            errors.append("log.md: missing required root history")
        for name, (mode, expected) in SNAPSHOTS.items():
            file = (bundle / "references" / name if name.startswith("upstream-code/")
                    else bundle.parent / "sources/evaluate" / name)
            raw = file.read_bytes()
            if mode == "body":
                end = raw.find(b"\n---\n", 4)
                if not raw.startswith(b"---\n") or end < 0 or raw[end + 5:end + 6] != b"\n":
                    raise ValueError(f"{name}: malformed capture separator")
                raw = raw[end + 6:]
            if hashlib.sha256(raw).hexdigest() != expected:
                errors.append(f"{file.relative_to(bundle.parent)}: pinned {mode} capture bytes changed")
        for file in sorted(bundle.rglob("*.md")):
            rel = file.relative_to(bundle)
            try:
                if file.name == "index.md":
                    if file.parent == bundle:
                        fm, _ = document(file)
                        if fm != {"okf_version": "0.2"}:
                            raise ValueError("root index carries only okf_version: '0.2'")
                    elif file.read_text(encoding="utf-8").startswith("---\n"):
                        raise ValueError("subdirectory index must not carry frontmatter")
                    continue
                if file.name == "log.md":
                    history(file, bundle)
                    continue
                fm, body = document(file)
                if not isinstance(fm.get("type"), str) or not fm["type"].strip():
                    raise ValueError("type must be nonempty")
                authored_metadata(bundle, file, fm, body, now)
            except (OSError, TypeError, ValueError, yaml.YAMLError) as error:
                errors.append(f"{rel}: {error}")
        pending = bundle.parent / "sources/evaluate"
        if not (pending / "index.md").is_file():
            errors.append("sources/evaluate/index.md: missing pending-evaluation navigation")
        for file in sorted(pending.rglob("*.md")):
            if file.name == "index.md" or file.relative_to(pending).as_posix() in SNAPSHOTS:
                continue
            try:
                fm, body = document(file)
                authored_metadata(bundle, file, fm, body, now)
            except (OSError, TypeError, ValueError, yaml.YAMLError) as error:
                errors.append(f"{file.relative_to(bundle.parent)}: {error}")
        for name in SNAPSHOTS:
            if not name.startswith("upstream-code/") and (bundle / "references" / name).exists():
                errors.append(f"references/{name}: raw capture belongs outside the knowledge bundle")
        spec = importlib.util.spec_from_file_location(
            "bundle_indexes", DEFAULT_BUNDLE / "references/generators/generate_indexes.py")
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        for index, expected in generator.render(bundle).items():
            if not index.exists() or index.read_text(encoding="utf-8") != expected:
                errors.append(f"{index.relative_to(bundle.parent)}: derived index drift")
    except (OSError, TypeError, ValueError, yaml.YAMLError) as error:
        errors.append(str(error))
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print(f"OK: metadata, source joins, local paths, all governed directory indexes, and {len(SNAPSHOTS)} pinned captures")
        print("LIMIT: captured links retain original source context; no factual accuracy or adoption authenticated")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
