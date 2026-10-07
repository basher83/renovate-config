---
type: Framework
title: Bundle document formatting
description: This framework defines local OKF metadata, provenance, navigation, and history conventions.
tags: [governance, formatting]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-07T01:20:34Z }
sources:
  - id: review-verdicts
    resource: https://github.com/basher83/renovate-config/pull/123#issuecomment-6025792492
    title: Operator verdicts on local OKF extensions and locked vocabulary
  - id: okf-spec
    resource: ../sources/evaluate/okf-spec.md
    title: Open Knowledge Format v0.2 specification
  - id: greenfield-framework
    resource: ../sources/evaluate/greenfield-framework.md
    title: Learnings Framework
    author: claude_agent/Fable 5
  - id: greenfield-lifecycle
    resource: ../sources/evaluate/greenfield-lifecycle-and-revision.md
    title: Lifecycle and revision
    author: claude_agent/Fable 5
  - id: greenfield-evidence
    resource: ../sources/evaluate/greenfield-evidence-boundary.md
    title: Evidence boundary
    author: claude_agent/Fable 5
  - id: local-decisions
    resource: /decisions.md
    title: Prospective decisions and formatting direction
    author: codex_agent/GPT 6.1 Sol
  - id: upstream-checker
    resource: /references/upstream-code/check_bundle.py.txt
    title: Greenfield bundle checker source
  - id: upstream-generator
    resource: /references/upstream-code/generate_indexes.py.txt
    title: Greenfield index generator source
  - id: upstream-review-ingest
    resource: /references/upstream-code/ingest_subagent_review.py.txt
    title: Greenfield review ingest source
---

# Bundle document formatting

**Standing: proposed revision of local formatting guidance.** This concept owns authoring conventions.
[Enforcement](/enforcement.md) owns artifact and field responsibilities, mise operations, and coverage.
The [trail](/log.md) and decision record preserve prior acceptance and subsequent changes.[^local-decisions]

## Use documented fields in a consistent order

Ordinary concept documents have YAML frontmatter delimited by `---`, followed by their Markdown body. OKF's
conformance floor requires a nonempty `type`; its other fields are optional. This local style uses `type`,
`title`, `description`, optional `resource`, `tags`, `status`, `generated`, then `sources` when applicable.
A real `verified` entry,
if authorized and supported, follows `generated`.[^okf-spec][^greenfield-framework]

Use a descriptive type appropriate to the document, a short title, a one-sentence description, and a short YAML
list of relevant tags. The description MUST be a single complete sentence summarizing the concept: index
entries copy it verbatim, and search snippets and previews depend on it. Sentence meaning is reviewed by humans;
the checker enforces a single line and sentence punctuation. Keep the existing document bodies and type
distinctions; greenfield's learning-specific
vocabulary and directory rules are not imported by borrowing its frontmatter style.

Use only documented OKF fields. A schema accepting an unknown field does not authorize a new local metadata
convention. Do not add fields such as `sha256`, `authority`, or `source_updated` merely because they validate.
Keep source revisions and abbreviated hash references in the body.[^local-decisions]

The following local extensions implement the operator's PR verdicts; the captured specification remains
unchanged.[^review-verdicts]

## Distinguish resource binding from derivation

A concept bound to an underlying asset MUST identify that asset with top-level `resource`. A concept without
an asset binding omits top-level `resource`; materials it derives from belong in `sources`, whether internal
or external to the bundle. Binding and derivation are separate relationships: a source does not become the
asset merely because the concept cites it. The current contract concepts describe independent rules and
models, so their consulted materials remain derivation sources.[^okf-spec]

## Use the accepted tag vocabulary

Tags MUST add useful distinctions within their owning bundle and connect related concepts across document
types or locations. Do not repeat repository identity, type, or title without a retrieval benefit. Broader
classification belongs to the higher-level bundle that needs it. A concept may omit tags or use an empty list
when none improve local retrieval or grouping.

The locked vocabulary is `governance` for the subject area and `enforcement`, `formatting`, and `presets` for
narrower topics. A new tag requires human approval and merge of a PR that justifies the addition in prose.
The checker enforces this vocabulary for bundle concepts; imported captures retain their original metadata,
and authored pending-evaluation records are not promoted to concepts by validation.

## Use bundle-absolute cross-links

Links between targets within the bundle MUST begin with `/` and resolve from the bundle root, preserving
fragments. This local extension makes OKF §6.1's recommended form required. Path-valued metadata pointing
inside the bundle follows the same convention. The surrounding prose states the relationship asserted by a
link; a link alone does not establish derivation, asset binding, or acceptance.[^okf-spec]

For example, use `[contract](/governance.md)` and `[index rules](/formatting.md#generate-governed-indexes)`.
Targets outside the bundle retain repository-relative paths or external URLs; `/sources/...` would incorrectly
resolve inside the bundle. Imported bodies retain their original link context.

## Record scoped history

A `log.md` MUST exist at the bundle root and MAY appear below it to record that directory's history.
Logs have no concept frontmatter. They contain a flat list of prose entries grouped under ISO `YYYY-MM-DD`
date headings, newest date first. Each entry MUST start with `**Update**`, `**Creation**`, or `**Deprecation**`.
Additional leading labels require human acceptance through a PR. Preserve factual chronology and distinguish
separate validation runs; concept bodies hold current knowledge, and decisions hold material rationale.

## Identify the producing harness and model

Set `generated.at` to the last meaningful content change, preserving historical verification and acceptance
events when correcting generation metadata.

Write `generated` as an inline mapping, using the house actor form `<harness_agent>/<Model Name>` and an ISO
8601 datetime with an explicit UTC offset. Use the actual producing harness and model. A CLI version or document
revision does not substitute
for that model attribution. The current workflow still requires authored generation metadata; code-owned
reconciliation is a proposal
in [enforcement](/enforcement.md#ownership-and-permitted-writes), not an implemented stamp
service.[^greenfield-framework]

```yaml
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T05:56:55Z }
```

## Keep draft lifecycle separate from verification

Agent-created candidates start with `status: draft` and no `verified` entry. Absence of `verified` means
unverified. Passing lint, schema checks, or agent review does not supply a human verification event or adopt
policy. Record an actual operator verification only when it occurred; do not infer it from agreement with a
formatting choice. Generation, verification, and adoption remain separate claims. Historical verification events may
predate the latest generation; they do not claim that a later revision was reverified.[^greenfield-lifecycle][^okf-spec]

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
locally. [Sources to evaluate](../sources/evaluate/index.md) provides intake navigation, and the
[capture record](../sources/evaluate/2026-10-06-source-captures.md) identifies their origins, preservation method,
and historical scope. The operator directions have an authored session record; it is not a verbatim transcript.

Raw captures and authored evidence records await evaluation in `sources/evaluate/`; this document owns local
formatting rules. Apply the [knowledge layers and evaluation
criteria](/governance.md#knowledge-layers-and-source-evaluation).
OKF's optional `references/` convention represents material as first-class bundle concepts; it does not require
source ingestion into the bundle. Greenfield's evidence-containment rule is not adopted here. Preserve imported bodies
verbatim; put corrections or local interpretations in a successor note or the consuming guidance.
Source metadata retained in a capture describes its original context, not local policy adoption.

## Verify the edited documents without overstating the result

Check parseable YAML, documented field names and shapes, actor attribution, timestamps, source paths, and keyed
footnotes. Lint the actual edited files using the scoped invocation in [AGENTS.md](../AGENTS.md). Schema
acceptance alone does not establish provenance accuracy, operator verification, or policy adoption.

## Generate governed indexes

Agents must never issue a direct tool call targeting a bundle-governed `index.md`. Agents work on permitted
concepts and source records; deterministic finalization owns indexes. No per-index edit, repair, or regeneration
command is part of the agent interface. The repository interface is mise.

Every directory in the bundle hierarchy MUST contain a generated `index.md`, including tool-only directories.
The generator owns all of those indexes plus `sources/evaluate/index.md`. The bundle-root index MUST carry
`okf_version`; subordinate indexes have no frontmatter. Each body groups entries under headings. Concept
entries MUST include the linked concept's description verbatim; tool and capture entries describe supporting
artifacts without converting them into concepts.
It derives labels and descriptions from document metadata and sorts entries by filename. Prior index content
is not an input to entry ordering. The intake follows the OKF §8 listing convention without promoting its sources.
Generation MUST execute before push; the configured pre-commit finalizer establishes that sequence for the
ordinary commit-and-push workflow. The current configuration has no outgoing-revision guard against hook
bypass; do not claim universal push enforcement.
Governance semantics remain in the operating contract.

```bash
mise run bundle:finalize
mise run bundle:check
mise run bundle:test
```

[Enforcement](/enforcement.md#lifecycle-boundaries) owns the finalization and commit boundary. This concept
specifies index authoring conventions only; agents never repair generated navigation directly.

## Use standalone deterministic checks

The decision record identifies the authorized checker and generator scope.
They implement three bounded patterns: metadata and source joins, derived index equality, and byte-faithful
capture comparison. Greenfield's type taxonomy, prose bans, complete directory tree, and installed enforcement
are not imported.[^local-decisions][^upstream-checker][^upstream-generator][^upstream-review-ingest]

Run from the repository root; each tool also accepts an explicit path and resolves its default bundle from
its own location:

```bash
mise run bundle:check
```

Checking is read-only. Finalization regenerates the complete governed index scope before checking it.
Their entries derive titles and descriptions from frontmatter and use deterministic filename ordering.
The checker validates the declared metadata, source and footnote joins, local links, derived indexes, and the
ten pinned captures. Markdown captures are checked in `sources/evaluate/`, outside concept validation;
code snapshots remain at their existing paths. Fidelity checks preserve evidence during this correction;
they do not decide source admission, retention, or promotion. Source metadata is not validated as current
bundle standing. Imported bodies retain their original source joins and link context.

The two YAML-reading scripts declare Python 3.11+ and PyYAML 6.0.3. Dependency resolution is separate from
the checks; use an existing compatible environment or resolve the declared script dependency when authorized.
Focused regression checks use temporary fixtures and preserve verification history, reject evidence copied
back into the bundle, bound local source paths to the repository, and retain imported-body fidelity.
Run them in the same compatible environment:

```bash
mise run bundle:test
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

See [enforcement](/enforcement.md) for the mise interface, current coverage, and the remaining direct capture-tool gap.

[^local-decisions]: Operator formatting direction and local adoption recorded in the decision log, D002 and D005.
[^okf-spec]: Captured OKF v0.2 specification, §§4–7 and 11; original body hash identified above.
[^greenfield-framework]: Captured greenfield Learnings Framework, construction rules and actor house style.
[^review-verdicts]: Operator PR instructions on descriptions, index coverage, logs, tags, and the linked earlier rules.
[^greenfield-lifecycle]: Captured greenfield lifecycle and revision, draft and operator-verification boundary.
[^greenfield-evidence]: Captured greenfield evidence boundary, containment and source addressability.
[^upstream-checker]: Captured greenfield checker, adapted for this bundle's metadata and capture boundaries.
[^upstream-generator]: Captured greenfield generator, adapted for the declared indexes.
[^upstream-review-ingest]: Captured greenfield ingest transform, preserving bytes and refusing existing outputs.
