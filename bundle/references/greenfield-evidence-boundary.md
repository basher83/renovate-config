---
type: Framework
title: Evidence boundary
description: The containment rule — front-matter points, the body argues, references/ contains — and the addressability requirement for anything cited as evidence.
tags: [learnings, governance, framework, evidence, provenance]
status: stable
generated: { by: claude_agent/Fable 5, at: 2026-08-24T03:45:24Z }
verified: { by: human:basher83, at: 2026-08-24T03:52:09Z }
---

# Trajectory

This concept is new to the decomposed framework: it narrows
[framework.md](/framework.md)'s citation-form construction rules, which
described how to write `sources` entries but did not bound what may stand
behind them, with the containment and addressability rules below. Revision
history lives in the framework [log.md](log.md).

# The containment rule

Each layer of a concept has one job. Front-matter points: `sources` entries
name where evidence lives. The body argues: it draws conclusions from that
evidence and attributes claims by footnote. `references/` contains: ingested
evidence lives there as first-class files. A concept that blurs these —
evidence living only inside a body paragraph, or a source entry doing the
arguing — is malformed for this bundle even where OKF tolerates it.

# Addressability

Anything the bundle asserts as evidence must be addressable: an absolute
URL, a bundle-relative path, or an artifact ingested into `references/`. A
`sources[].resource` may be a scope descriptor only for a population a
consumer genuinely cannot follow (for example, every dispatch in a session's
history) — never for a specific artifact that could be ingested. A
descriptor that names one particular record is a pointer to nothing; ingest
the record instead.

# Session-witnessed evidence

Evidence witnessed only inside a session — an observation an orchestrator
made, a dispatch it prepared, a state that was later corrected — must be
ingested into `references/` (for example `references/dispatch-records/`)
before any concept cites it. The write-down states what it is, who wrote it,
when, and how it relates to the witnessed moment, so the retrospective gap
is visible rather than hidden.
