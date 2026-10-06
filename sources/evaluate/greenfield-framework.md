---
type: Framework
title: Learnings Framework
description: Normative contract and interpretation rules for the learnings bundle
tags: [learnings, governance, greenfield]
status: stable
generated: { by: claude_agent/Fable 5, at: 2026-08-19T07:22:22Z }
verified: { by: human:basher83, at: 2026-08-25T06:19:15Z }
---

# Purpose and scope

This bundle is a conformant OKF v0.2 knowledge bundle that records learnings
from greenfield analysis work: orchestrated reverse-engineering and
spec-analysis sessions run with the greenfield plugin in this repository. Each
learning is a reusable conclusion extracted from evidence — primarily the
session-analysis transcripts kept in [insight-analysis-transcripts](/references/insight-analysis-transcripts/index.md) and written so a future session can apply it without rediscovering it.

The operator's longer-term intent frames what belongs here: fork the
greenfield plugin and conform it to the work the operator does most. Learnings
recorded in this bundle are feedstock for that fork. A recommendation that
"belongs in the greenfield skill" is therefore still recorded here as a
learning; this bundle is where such feedback accumulates until the fork
exists to receive it.

## Governing rule

The bundle's governing rule, stated verbatim:

> Record corrections and confirmed approaches alike, including why they
> mattered. Don't save what the repo or chat history already records; update
> an existing note rather than creating a duplicate; revision with trajectory for
> notes that turn out to be wrong.

Operator's gloss: the "don't save what's already recorded" clause is a nudge
to record the learning rather than only relay it in chat. It is not an excuse
to skip recording. When a learning surfaces in conversation, the failure mode
to avoid is leaving it stranded in chat history; the clause only excuses
duplicating something a durable artifact already captures in full.

## Construction rules

[Type Vocabulary](/framework/type-vocabulary.md) - Kind vocabulary and number allocation

### Required front-matter

Every learning concept carries:

- `type`: see [Type Vocabulary](/framework/type-vocabulary.md)
- `title`: a short display name for the learning.
- `description`: a one-line summary, used by the index and previews.
- `tags`: a YAML list of short cross-cutting labels.
- `status: draft` at creation (see the lifecycle section below).
- `generated: { by: <actor>, at: <ISO 8601 datetime> }` using the OKF §7
  actor convention. The house style in this repo for agent actors is
  `<harness_agent>/<Model Name>` — for example `claude_agent/Fable 5` or
  `codex_agent/GPT 5.6 Sol`, `pi_agent/GPT 5.6 Sol` for CLI harnesses, `perplexity_agent/GPT 5.6 Sol`. Human actors are `human:<id>`, for example
  `human:basher83`.
- `sources`: a list of the evidence the learning derives from. Each entry
  carries a stable `id` and a `resource`. Paths to evidence outside this
  bundle are written as relative paths; the insight transcripts live in the
  bundle's `references/` subdirectory and are cited as
  `references/insight-analysis-transcripts/<file>.md`.

Each `sources` entry:

- `resource`: Names either a concrete artifact a
  consumer can follow (an absolute URL, a bundle-relative path, or a path
  into a `references/` subdirectory) see [Evidence Boundary](/framework/evidence-boundary.md).
- `id`: A stable key used to attribute individual claims (see
  below).
- `title`: Human-readable label for the source.
- `author` Who or what produced the source, in the actor convention

### Sources and per-claim attribution

Claims in the body are attributed to specific sources with markdown footnotes
whose labels are `sources[].id` values, per OKF §5.1:

```markdown
The session spent $104.78 with no budget gate between layers.[^insight-0817]

[^insight-0817]: 2026-08-17 agent analysis insight
```

The footnote label is the join key into `sources`; keep `id`s stable when
editing so attribution survives reordering.

### Writing Style

Writing follows Gutes Deutsch nach Wolf Schneider (or Plain English according to Strunk & White).

Additionally:
- Technical terms stay in English (LLM, Prompt, Token, Spec, etc.)
- Address the reader directly, use first person sparingly but deliberately
- Use analogies to human thinking to explain technical concepts
- One thought per paragraph (5-8 sentences is fine)
- Section headings are statements, not topic announcements
- First sentence says what the paragraph is about
- Show code and prompts, don't just claim things work
- Conclusions make a clear statement — never end with 'it remains exciting'


## Maintenance, Lifecycle and Revision

[Lifecycle](/framework/lifecycle-and-revision.md) - Lifecycle statuses, the trust posture for agent drafts, and the revision-with-trajectory rule

- Before writing a new learning, check the existing ones. If an existing
  learning already covers the substance, update it (and its `generated`
  attribution) rather than creating a duplicate.
- `index.md` is a derived navigation view. It lists what exists with each
  concept's front-matter description, and it never owns status; if the index
  and a concept disagree, the concept controls and the mismatch is drift to
  repair. Its only front-matter is `okf_version: "0.2"`.
- `log.md` records changes per OKF §9: date-grouped entries, newest first,
  ISO 8601 `YYYY-MM-DD` headings.
- Keep index and log current in the same change that adds, updates, or
  deprecates a learning.
### Rulings inbox (pilot)

[inbox.md](/inbox.md) at the bundle root is a capture projection for
operator rulings made in session: entries land there in the same turn with
no verification ceremony, carry body dispositions (unresolved,
deferred, applied, rejected), and own no state — when an entry conflicts
with a canonical artifact, the canonical artifact controls and the entry is
stale. An entry becomes durable only when applied to the artifact that owns
it and committed, at which point it flips to applied with a destination
pointer. The surface is never verified. This is a bounded pilot borrowing
the projection shape from the operator's personal-learning estate; it lives
here under this file's decompose discipline and graduates into `framework/`
when exercised enough to need independent lifecycle.

## Relationship to global CLAUDE.md and the greenfield skill

The operator's global CLAUDE.md is authoritative until a conflict with it is
logged here with evidence, and the operator (`human:basher83`) decides whether
and how anything propagates into CLAUDE.md. When a learning's substance also
appears in CLAUDE.md, this bundle records the learning in full and is its
canonical home — the evidence, the why, and the how-to-apply live here —
while CLAUDE.md holds only the operative rule.

The same holds for the greenfield skill: recommendations that would change
the plugin's skills or agents are recorded here as learnings, because they
are feedback for the planned fork, not edits to make upstream.

## Framework, interpretation, and index separation

### Working interpretation

Three functions are becoming visible:

| Surface | Primary function | What it should not silently become |
|---|---|---|
| Framework | Defines the bundles normative contract: purpose, construction rules, lifecycle, standing, required relationships, and safe consumption | An index of every artifact or an unmarked point-in-time opinion |
| Interpretation | Explains why a structure is understood a particular way, what evidence supports that reading, and what remains uncertain | Binding governance merely because it is persuasive or colocated |
| Index | Provides concise navigation and, where declared, a derived view of current status | The hidden owner of lifecycle and standing semantics |
| Content artifact | Carries the actual decision, learning, evidence, interpretation, task, or other domain object | The implicit definition of its surrounding collection |

The responsibilities should be separated conceptually. That does not require a separate file for every responsibility in every bundle.

### Governance and interpretation

The distinction is:

```text
Governance asks:
  What rules currently apply, who may change them, and what do they permit?

Interpretation asks:
  Why do we understand this structure this way, from which evidence,
  for what use, and with what uncertainty?
```

A `framework.md` may initially contain both when the explanatory material is
short, stable, and necessary to apply the rules correctly. Combining them can
reduce unsafe partial consumption and avoid forcing a cold consumer to assemble
one contract from several files.

Separate files become preferable when governance and interpretation have
materially different:

- standing or acceptance authorities;
- authors or intended consumers;
- evidence requirements;
- revision cadences or wake conditions;
- scopes or named uses;
- competing interpretations;
- or trajectory requirements.

The working rule is therefore:

> Separate governance from interpretation as responsibilities. Split them into
> separate artifacts when either must be trusted, revised, replaced, compared,
> or consumed independently.

### Index boundary

An index should answer some bounded version of:

- What exists?
- Where is it?
- What kind of artifact is it?
- Which item should I inspect for a named need?
- If status is intentionally projected here, what source owns that status?

An index may expose status as a derived view, but it should not independently
define or own that status. If the index and source artifact disagree, the
declared source of truth controls and the mismatch is drift to repair.
