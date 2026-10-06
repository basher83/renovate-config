---
type: Framework
title: Bundle document formatting
description: Local OKF frontmatter style, provenance pointers, and verification boundaries for bundle documents.
tags: [renovate, governance, formatting]
status: stable
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T07:49:37Z }
sources:
  - id: okf-spec
    resource: references/okf-spec.md
    title: Open Knowledge Format v0.2 specification
  - id: greenfield-framework
    resource: references/greenfield-framework.md
    title: Learnings Framework
    author: claude_agent/Fable 5
  - id: greenfield-lifecycle
    resource: references/greenfield-lifecycle-and-revision.md
    title: Lifecycle and revision
    author: claude_agent/Fable 5
  - id: greenfield-evidence
    resource: references/greenfield-evidence-boundary.md
    title: Evidence boundary
    author: claude_agent/Fable 5
  - id: local-decisions
    resource: decisions.md
    title: Prospective decisions and formatting direction
    author: codex_agent/GPT 6.1 Sol
  - id: upstream-checker
    resource: references/upstream-code/check_bundle.py.txt
    title: Greenfield bundle checker source
  - id: upstream-generator
    resource: references/upstream-code/generate_indexes.py.txt
    title: Greenfield index generator source
  - id: upstream-review-ingest
    resource: references/upstream-code/ingest_subagent_review.py.txt
    title: Greenfield review ingest source
---

# Bundle document formatting

**Standing: maintained local formatting guidance, accepted with Slice 1.** This document owns formatting
for the local bundle. The operator accepted it alongside the [operating contract](governance.md), without
claiming a human content-verification event. It changes no dependency policy and installs no enforcement.
The decision record identifies the acceptance and its scope.[^local-decisions]

## Use documented fields in a consistent order

Ordinary concept documents have YAML frontmatter delimited by `---`, followed by their Markdown body. OKF's
conformance floor requires a nonempty `type`; its other fields are optional. This local style uses `type`,
`title`, `description`, `tags`, `status`, `generated`, then `sources` when applicable. A real `verified` entry,
if authorized and supported, follows `generated`.[^okf-spec][^greenfield-framework]

Use a descriptive type appropriate to the document, a short title, a one-sentence description, and a short YAML
list of relevant tags. Keep the existing document bodies and type distinctions; greenfield's learning-specific
vocabulary and directory rules are not imported by borrowing its frontmatter style.

Use only documented OKF fields. A schema accepting an unknown field does not authorize a new local metadata
convention. Do not add fields such as `sha256`, `authority`, or `source_updated` merely because they validate.
Keep source revisions and abbreviated hash references in the body.[^local-decisions]

## Identify the producing harness and model

Write `generated` as an inline mapping, using the house actor form `<harness_agent>/<Model Name>` and an ISO
8601 datetime with an explicit UTC offset. The actor for this preparation is `codex_agent/GPT 6.1 Sol`, based
on this thread's recorded `gpt-6.1-sol` model selection. A CLI version or document revision does not substitute
for that model attribution. Update `generated.at` when the content meaningfully changes.[^greenfield-framework]

```yaml
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T05:56:55Z }
```

## Keep draft lifecycle separate from verification

Agent-created candidates start with `status: draft` and no `verified` entry. Absence of `verified` means
unverified. Passing lint, schema checks, or agent review does not supply a human verification event or adopt
policy. Record an actual operator verification only when it occurred; do not infer it from agreement with a
formatting choice. Generation, verification, and adoption remain separate claims. Historical verification events may predate
the latest generation; they do not claim that a later revision was reverified.[^greenfield-lifecycle][^okf-spec]

## Point to evidence and attribute claims

Order each source entry as `id`, `resource`, `title`, then `author` when the producing actor is known. Keep
source IDs stable, and use matching body footnotes for claims attributed to those sources. Omit unknown authors
rather than invent them.[^greenfield-framework][^okf-spec]

`resource` must point to a followable artifact: an absolute URL or a resolving document path. A scope descriptor
is appropriate for a population that cannot genuinely be followed, not as a substitute for a particular record.
Session-only evidence needs an addressable capture before it is cited as evidence.[^greenfield-evidence]

Frontmatter points; the body explains what the source supports and its limits. State whether a reference is a
cached snapshot, mutable upstream material, historical evidence, or a local adaptation. Keep short revision or
hash references beside the corresponding body reference, not in invented frontmatter fields.[^greenfield-evidence]

The OKF source above is a local capture of the opensrc-cached v0.2 specification, SHA-256 prefix
`26aa5da02927`; upstream was not refreshed for this check.[^okf-spec] The greenfield sources are also captured
locally. [References](references/index.md) provides navigation, and the
[capture record](references/2026-10-06-source-captures.md) identifies their origins, preservation method,
and historical scope. The operator directions have an authored session record; it is not a verbatim transcript.

References contain evidence, while this document owns the local formatting rules. Preserve imported bodies
verbatim; put corrections or local interpretations in a successor note or the consuming guidance.
Source metadata retained in a capture describes its original context, not local policy adoption.

## Verify the edited documents without overstating the result

Check parseable YAML, documented field names and shapes, actor attribution, timestamps, source paths, and keyed
footnotes. Lint the actual edited files using the scoped invocation in [AGENTS.md](../AGENTS.md). Schema
acceptance alone does not establish provenance accuracy, operator verification, or policy adoption.

## Use standalone deterministic checks

The operator accepted standalone scripts with Slice 1, expanding the earlier documentation-only scope.
They implement three bounded patterns: metadata and source joins, derived index equality, and byte-faithful
capture comparison. Greenfield's type taxonomy, prose bans, complete directory tree, and installed enforcement
are not imported.[^local-decisions][^upstream-checker][^upstream-generator][^upstream-review-ingest]

Run from the repository root; each tool also accepts an explicit path and resolves its default bundle from
its own location:

```bash
uv run --script bundle/references/generators/generate_indexes.py --check
uv run --script bundle/references/attesters/check_bundle.py
```

Both commands are read-only by default. Use the generator's explicit `--write` to update only the two scoped
indexes. Their entries derive titles and descriptions from frontmatter and preserve the existing entry order.
The checker validates the declared metadata, source and footnote joins, local links, derived indexes, and the
ten pinned captures. Body-mode captures have locally authored headers, which receive metadata validation;
their imported bodies retain the original source joins and link context. Raw captures preserve original
metadata as part of their pinned bytes rather than reinterpret its historical scope.

The two YAML-reading scripts declare Python 3.11+ and PyYAML 6.0.3. Dependency resolution is separate from
the checks; use an existing compatible environment or resolve the declared script dependency when authorized.
Focused regression checks use temporary fixtures and preserve verification history, reject invalid authored
capture headers, and retain imported-body fidelity. Run them in the same compatible environment:

```bash
uv run --script bundle/references/attesters/test_check_bundle.py
```

The source-capture tool uses Python's standard library:

```bash
python3 bundle/references/ingest/capture_source.py SOURCE --mode raw --check CAPTURE
python3 bundle/references/ingest/capture_source.py SOURCE --mode body --check CAPTURE
```

Raw mode compares whole files. Body mode compares the exact source payload after prepended capture metadata.
Creation requires `--out`; body-mode creation also requires `--frontmatter`. Existing outputs are never
overwritten. An optional `--sha256` pins the input before creation or comparison. These checks prove fidelity
to an identified source, not that its claims are true or that policy was accepted.

The bundle and references indexes provide navigation. No linter configuration, hook, CI rule, or mise task is
changed. These are standalone tools; an automated blocking gate has not been installed.

[^local-decisions]: Operator formatting direction and local adoption recorded in the decision log, D002 and D005.
[^okf-spec]: Captured OKF v0.2 specification, §§4–7 and 11; original body hash identified above.
[^greenfield-framework]: Captured greenfield Learnings Framework, construction rules and actor house style.
[^greenfield-lifecycle]: Captured greenfield lifecycle and revision, draft and operator-verification boundary.
[^greenfield-evidence]: Captured greenfield evidence boundary, containment and source addressability.
[^upstream-checker]: Captured greenfield checker, adapted for this bundle's metadata and capture boundaries.
[^upstream-generator]: Captured greenfield generator, adapted for the two declared indexes.
[^upstream-review-ingest]: Captured greenfield ingest transform, preserving bytes and refusing existing outputs.
