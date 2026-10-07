---
type: Dispatch Record
title: Source captures, 2026-10-06
description: Origins, capture methods, fidelity receipts, and consumption limits for the document and code snapshots.
tags: [renovate, governance, references]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T07:35:02Z }
sources:
  - id: governance-review
    resource: shared-agent-policy-repository-review.md
    title: Shared agent policy repository review
  - id: shared-draft
    resource: agent-working-policy-draft.md
    title: Agent Working Policy — Draft
  - id: okf-spec
    resource: okf-spec.md
    title: Open Knowledge Format v0.2 specification
  - id: greenfield-framework
    resource: greenfield-framework.md
    title: Learnings Framework
    author: claude_agent/Fable 5
  - id: greenfield-lifecycle
    resource: greenfield-lifecycle-and-revision.md
    title: Lifecycle and revision
    author: claude_agent/Fable 5
  - id: greenfield-evidence
    resource: greenfield-evidence-boundary.md
    title: Evidence boundary
    author: claude_agent/Fable 5
  - id: upstream-checker
    resource: ../../bundle/references/upstream-code/check_bundle.py.txt
    title: Greenfield bundle checker source
  - id: upstream-generator
    resource: ../../bundle/references/upstream-code/generate_indexes.py.txt
    title: Greenfield index generator source
  - id: upstream-insight-ingest
    resource: ../../bundle/references/upstream-code/ingest_agentsview_insight.py.txt
    title: Greenfield insight ingest source
  - id: upstream-review-ingest
    resource: ../../bundle/references/upstream-code/ingest_subagent_review.py.txt
    title: Greenfield review ingest source
---

# Source captures

The recording agent captured the five documents on 2026-10-06 at `06:30:51Z`, in BB thread
`thr_2gvd7sszwk`, and captured the four Python sources later in the same session after the operator's tooling
direction. The files below are the captured evidence; this record explains their origins and method.
It does not assert human verification, policy adoption, or freshness beyond the capture.

The completed governance review was captured later at `07:35:02Z` after the operator identified its location.
Its body hash was pinned before capture and compared against the main checkout source.

| Capture | Origin | Method | Original SHA-256 prefix |
| --- | --- | --- | --- |
| [Governance review](shared-agent-policy-repository-review.md)[^governance-review] | Main checkout `sources/shared-agent-policy-repository-review.md` | Exact body with capture frontmatter prepended | `c33855ebceb8` |
| [Shared policy draft](agent-working-policy-draft.md)[^shared-draft] | Docs vault `repository-contracts-and-policy`, `agent-working-policy-draft.md` | Exact UTF-8 body with capture frontmatter prepended | `290537172062` |
| [OKF specification](okf-spec.md)[^okf-spec] | opensrc cache, `GoogleCloudPlatform/open-knowledge-format/main/SPEC.md` | Exact cached body with capture frontmatter prepended | `26aa5da02927` |
| [Greenfield framework](greenfield-framework.md)[^greenfield-framework] | `/Users/basher8383/greenfield/.claude/learnings/framework.md` | Entire source file copied byte-for-byte | `7aed48800e0a` |
| [Greenfield lifecycle](greenfield-lifecycle-and-revision.md)[^greenfield-lifecycle] | `/Users/basher8383/greenfield/.claude/learnings/framework/lifecycle-and-revision.md` | Entire source file copied byte-for-byte | `0d34c130a9f2` |
| [Greenfield evidence boundary](greenfield-evidence-boundary.md)[^greenfield-evidence] | `/Users/basher8383/greenfield/.claude/learnings/framework/evidence-boundary.md` | Entire source file copied byte-for-byte | `af991166fb34` |
| [Bundle checker source](../../bundle/references/upstream-code/check_bundle.py.txt)[^upstream-checker] | Greenfield `references/attesters/check_bundle.py` | Entire source file copied byte-for-byte as text evidence | `0b93a347468b` |
| [Index generator source](../../bundle/references/upstream-code/generate_indexes.py.txt)[^upstream-generator] | Greenfield `references/generators/generate_indexes.py` | Entire source file copied byte-for-byte as text evidence | `5a9a1f2dc819` |
| [Insight ingest source](../../bundle/references/upstream-code/ingest_agentsview_insight.py.txt)[^upstream-insight-ingest] | Greenfield `references/ingest/ingest_agentsview_insight.py` | Entire source file copied byte-for-byte as text evidence | `8d1d535dad65` |
| [Review ingest source](../../bundle/references/upstream-code/ingest_subagent_review.py.txt)[^upstream-review-ingest] | Greenfield `references/ingest/ingest_subagent_review.py` | Entire source file copied byte-for-byte as text evidence | `49052b574b8d` |

The shared-draft source hash matches the revision used to prepare the local contract. Its original body and
unadopted standing are preserved. The OKF source is the cached v0.2 snapshot, not a fresh upstream lookup.
The upstream specification remains at
[Open Knowledge Format SPEC.md](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).

The greenfield files retain their original metadata, including any `verified` event and `status: stable`.
Those fields describe the source's history and standing in greenfield; they do not verify or adopt this local
application. Their internal links retain the original greenfield bundle context. This is a selected capture,
not a complete mirror of its dependency graph.

Treat imported bodies as evidence: preserve their bytes. A correction or changed interpretation belongs in a
successor note or the local guidance, not in the captured body. The authored rulings record beside these
captures is a different kind of evidence and states its retrospective capture boundary explicitly.

The `.py.txt` files are preserved upstream code evidence, not the runnable local adaptations. Standalone local
scripts live in `attesters/`, `generators/`, and `ingest/`. Their scope differs from greenfield's bundle-specific
rules and is described in [formatting.md](../../bundle/formatting.md).

[^governance-review]: Completed governance review; captured body fidelity does not verify its reported claims.
[^shared-draft]: Captured shared policy draft; original body hash identified above.
[^okf-spec]: Captured cached OKF v0.2 specification; original body hash identified above.
[^greenfield-framework]: Exact capture of greenfield's Learnings Framework.
[^greenfield-lifecycle]: Exact capture of greenfield's lifecycle and revision concept.
[^greenfield-evidence]: Exact capture of greenfield's evidence boundary concept.
[^upstream-checker]: Exact capture of greenfield's deterministic checker.
[^upstream-generator]: Exact capture of greenfield's index generator.
[^upstream-insight-ingest]: Exact capture of greenfield's insight ingest transform.
[^upstream-review-ingest]: Exact capture of greenfield's review ingest transform.
