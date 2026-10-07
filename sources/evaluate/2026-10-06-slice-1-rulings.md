---
type: Dispatch Record
title: Slice 1 scope and formatting rulings, 2026-10-06
description: Participant-authored capture of the operator's preparation, formatting, and evidence directions.
tags: [renovate, governance, rulings]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T06:41:43Z }
---

# Slice 1 scope and formatting rulings

This is a participant-authored record of selected operator directions witnessed in BB thread
`thr_2gvd7sszwk` on 2026-10-06. It was written after the exchanges, during preparation of the references tier.
It is not a verbatim transcript or a human verification receipt. The quoted selections below reproduce the
answers and corrections present in this session; surrounding explanation is the recording agent's prose.

## Prepare the full slice, then reconcile governance before adoption

The operator selected **“Full slice (Recommended)”**: prepare the local operating contract and decision log,
align the entry points, and mark and evaluate the retained Copilot files. #122 and dependency-policy changes
remain excluded.

For the knowledge path, the operator answered:

> 1 with caveat. OKF formatting see /Users/basher8383/3I/lab/personal-computing/.ok/okf/*

Option 1 was the focused move: create the local contract and decision log in `bundle/`, move the
preset-management guide there, and leave historical audits and upstream mirrors in `docs/`.
The operator then selected **“Bundle documents (Recommended)”** for OKF formatting and
**“Draft now, adopt later (Recommended)”** for timing. These selections authorize candidate preparation;
the shared-policy review and an explicit operator decision precede local governance adoption.
Commit and publication actions remain separate.

## Use documented fields and short body references

The operator directed a check against the opensrc-cached OKF `SPEC.md`. After the agent disclosed that it had
added an undocumented `sha256` field to a source entry, the operator stated:

> yeah same. do not invent fileds simply because the schema allows it. That is a boundry right there.
> ref in the body and use the short form

The resulting direction is to use documented OKF metadata and keep abbreviated revision or hash references
in the body. Schema tolerance does not grant authority to invent a metadata convention.

## Follow the house style and give formatting its own owner

The operator pointed to `greenfield/.claude/learnings/index.md`, asked the agent to follow its governance
trail, and said the Markdown body was fine while frontmatter formatting remained the friction.
The inspected framework identifies the compact harness/model actor style, draft lifecycle, and evidence
addressability boundary. The recording agent checked the thread's model selection as `gpt-6.1-sol` before
using `codex_agent/GPT 6.1 Sol`.

After the agent identified the particular-record source descriptors as an unresolved gap, the operator said:

> agreed and these formatting rules also need thier own doc

The next direction pointed to `greenfield/.claude/learnings/references/index.md`. Following that index
showed the authored-record and verbatim-capture pattern used for session observations and external evidence.
The resulting implementation captures the particular sources locally and keeps references separate from
the guidance that consumes them.

## Boundaries retained

These directions do not adopt the complete local operating contract, resolve #122, adopt greenfield's entire
framework, or authorize installed enforcement and publication. The references capture makes sources inspectable;
it does not authenticate operator approval merely through an agent-written marker.

## Prepare standalone deterministic tools

The operator clarified that the reference index also pointed toward its deterministic Python scripts.
After inspection, the operator selected **“Standalone scripts (Recommended)”**: include narrowly adapted
index generation/checks, metadata and source validation, and capture-fidelity checks in the draft.
CI, hooks, mise tasks, and installed enforcement remain unchanged. This selection expands the earlier
documentation-only preparation scope to include standalone tooling; it does not adopt governance.
