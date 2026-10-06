#!/usr/bin/env python3
"""Copy or compare a source without summarizing it; refuse existing outputs.

Adapted from greenfield's ingest pattern. Raw mode compares entire files.
Body mode compares the payload after prepended capture frontmatter; creating
a body-mode capture requires an explicit frontmatter file. --check never writes.
This proves byte fidelity, not factual accuracy or operator verification.
"""

import argparse
import hashlib
import re
from pathlib import Path


def payload(data: bytes) -> bytes:
    if not data.startswith(b"---\n"):
        raise ValueError("capture has no prepended frontmatter")
    end = data.find(b"\n---\n", 4)
    if end < 0:
        raise ValueError("capture frontmatter is unterminated")
    body = data[end + 5:]
    if not body.startswith(b"\n"):
        raise ValueError("expected the capture separator's single blank line")
    return body[1:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("--mode", choices=("raw", "body"), default="raw")
    parser.add_argument("--sha256", help="optional full expected source digest, checked before writing")
    parser.add_argument("--frontmatter", type=Path, help="capture header for body-mode creation")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", type=Path, help="compare an existing capture without writing")
    mode.add_argument("--out", type=Path, help="create a new capture; never overwrite")
    args = parser.parse_args()
    try:
        source = args.source.read_bytes()
        digest = hashlib.sha256(source).hexdigest()
        if args.sha256 and (not re.fullmatch(r"[0-9a-f]{64}", args.sha256) or args.sha256 != digest):
            raise ValueError("source digest does not match the expected SHA-256")
        if args.check:
            if args.frontmatter:
                raise ValueError("--frontmatter is only used when creating a capture")
            captured = args.check.read_bytes()
            actual = payload(captured) if args.mode == "body" else captured
            if actual != source:
                raise ValueError(f"{args.check}: captured bytes differ from the source")
            print(f"OK {args.mode} fidelity; source SHA-256 prefix {digest[:12]}")
            return 0
        if args.mode == "body":
            if not args.frontmatter:
                raise ValueError("body-mode creation requires --frontmatter")
            header = args.frontmatter.read_bytes()
            if payload(header) != b"":
                raise ValueError("frontmatter input must contain only its block and separator")
            output = header + source
        else:
            if args.frontmatter:
                raise ValueError("raw mode does not accept --frontmatter")
            output = source
        with args.out.open("xb") as destination:
            destination.write(output)
        print(f"CREATED {args.out}; source SHA-256 prefix {digest[:12]}")
        return 0
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
