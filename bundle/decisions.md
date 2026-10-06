---
type: Decision Record
title: Renovate-config prospective decisions
description: Material decisions with authority, scope, rationale, implementation state, and revisit conditions.
tags: [renovate, governance, decisions]
status: stable
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T07:49:37Z }
sources:
  - id: slice-1-scope
    resource: references/2026-10-06-slice-1-rulings.md
    title: Slice 1 scope and formatting rulings, 2026-10-06
    author: codex_agent/GPT 6.1 Sol
  - id: adoption-rulings
    resource: references/2026-10-06-adoption-rulings.md
    title: Local adoption walkthrough choices
    author: codex_agent/GPT 6.1 Sol
  - id: local-contract
    resource: governance.md
    title: Local operating contract
---

# Renovate-config prospective decisions

**Standing: maintained local decision record, accepted with Slice 1.** D001–D004 preserve the preparation
history; D005 records local adoption. This document does not reconstruct approval for existing preset rules.

For each material decision, record the question and prior position, outcome, authority, effective scope,
rationale, evidence, implementation and verification state, and revisit or supersession conditions.
Keep routine maintenance records proportionate. Preserve prior rationale when superseding an entry.

## 2026-10-06 — D001: Prepare Slice 1; defer adoption

- **Question and prior position:** Slice 1 was a proposal with implementation unapproved. `bundle/` was the
  intended home, migration scope was unresolved, and OKF formatting was deferred. Two separate reviews are
  running: shared working-policy applicability and cross-repository Renovate configuration.
- **Outcome: adapted.** Prepare the full candidate now: local contract and prospective decision log, aligned
  AGENTS/README/preset guidance, and removal marking plus content evaluation for the retained Copilot files.
- **Authority and date:** Operator selections in the Slice 1 decision walkthrough on 2026-10-06: “Full slice,”
  focused move with an OKF caveat, “Bundle documents,” and “Draft now, adopt later.” These selections authorize
  preparation; they do not approve the final contract text or dependency policy.[^slice-1-scope]
- **Effective scope:** This renovate-config worktree only. Create `bundle/governance.md` and
  `bundle/decisions.md`; move `docs/preset-management.md` to `bundle/preset-management.md` and update affected
  guidance and links. Apply OKF v0.2 formatting to those three bundle documents. Leave historical audits and
  upstream reference mirrors in `docs/`. Preserve CLAUDE's symlink to AGENTS and both Copilot files.
- **Rationale and alternatives:** Preparing now allows a concrete diff to be reviewed while research runs.
  The focused move establishes the new local knowledge home without a full historical migration. The OKF
  caveat replaces the earlier formatting deferral for these three files only. The operator selected full
  preparation over contract-only or principles-first work, and adoption later over waiting to draft or
  proceeding to adoption before the governance results.
- **Evidence pointers:** [Candidate contract](governance.md), [preset-management guide](preset-management.md),
  [agent entry point](../AGENTS.md), [human entry point](../README.md), and the Docs vault's
  `renovate-config/slice-1-governance-plan.md`. That saved plan predates this walkthrough's OKF scope adjustment;
  it remains a proposal, not an adoption receipt.
- **Implementation and verification state:** Draft files and entry-point changes are prepared for review.
  Preparation is not completion or adoption. Verification receipts accompany the diff; schema, Markdown,
  metadata, links, and consumer behavior must retain distinct claims. No commit or publication is authorized
  by this decision. The separate mise setting correction was already published as
  [e063800](https://github.com/basher83/renovate-config/commit/e06380002719988d6654aad293eee9ee295fc0d2).
- **Revisit conditions:** Reconcile the running shared-policy review before seeking explicit local adoption.
  Revisit wording or scope if its findings warrant changes. The separate Renovate review informs later
  dependency-policy work; it is not a prerequisite for drafting this slice.

## 2026-10-06 — D002: Give formatting guidance its own owner

- **Question and prior position:** Formatting details were embedded in the governance candidate. The first
  pass used an undocumented `sha256` source field, then a CLI-version producer label and expanded mappings.
- **Outcome: adapted.** Use documented OKF fields, keep abbreviated hash references in the body, and apply
  greenfield's compact frontmatter house style with harness/model attribution. Give these rules their own
  owner in [formatting.md](formatting.md), with the other entry points linking to it.
- **Authority and date:** Operator direction on 2026-10-06: do not invent fields because the schema permits
  them; follow the greenfield governance trail for formatting; these rules need their own document.
- **Effective scope:** The Slice 1 bundle documents and their navigation. Keep ordinary Markdown bodies
  intact except for moving duplicated formatting guidance to its owner and correcting producer attribution.
  This does not adopt the operating contract or greenfield's learning-specific type and directory rules.
- **Implementation and verification state:** The formatting reference is a draft, with no human verification
  claimed. Metadata, lint, and pointer checks establish their stated scope only; no enforcement is added.
- **Remaining work and revisit condition:** The particular-record sources are now captured in
  [references](references/index.md), with origins and fidelity limits recorded separately. Reconcile broader
  governance after its review arrives. An inspectable authored record does not itself authenticate approval.

## 2026-10-06 — D003: Include standalone deterministic tooling

- **Question and prior position:** Slice 1 preparation originally covered documentation, with machinery
  changes excluded. One-off lint and metadata receipts did not provide reusable drift and capture checks.
- **Outcome: adapted.** Prepare standalone index generation/checks, bundle validation, and source-capture
  comparison, using the greenfield scripts as evidence for the pattern rather than copying their local rules.
- **Authority and date:** The operator clarified the Python-tooling intent and selected “Standalone scripts
  (Recommended)” on 2026-10-06.[^slice-1-scope]
- **Effective scope:** Scripts under `references/attesters/`, `references/generators/`, and `references/ingest/`,
  local source captures, and their usage documentation. CI, hooks, mise tasks, and installed enforcement remain
  unchanged. This decision explicitly expands the earlier documentation-only candidate scope.
- **Implementation and verification state:** The scripts default to read-only checks or require an explicit
  output option. Snapshot pins protect captured bytes; index checks compare regenerated descriptions and
  coverage; metadata checks reject unsupported fields and unresolved source joins. Receipts describe these
  checks, not factual accuracy or authenticated policy adoption.
- **Revisit condition:** Broader automation, enforcement, or consumer behavior checks require their own scope
  decision. Reconcile the pending governance review before local adoption.

## 2026-10-06 — D004: Revise the full local contract after governance review

- **Question and prior position:** Local adoption awaited the shared-policy review. Its recommendation was a
  minimal cross-repository pilot, while Slice 1 prepared a full local contract.
- **Outcome: adapted.** Carry the full local contract forward; clarify publication consequences and layered
  instructions. Require separate approval before each push, merge, publication, or external change. Require
  representative consumer evidence or an explicit operator exception for shared preset behavior changes.
  Retain both Copilot files for now.
- **Authority and date:** Operator answers in the adoption walkthrough on 2026-10-06, captured in the
  [rulings record](references/2026-10-06-adoption-rulings.md).[^adoption-rulings]
- **Effective scope:** Revised local candidate only. Configured bot authority, preset JSON, consumers, CI,
  hooks, and repository machinery remain unchanged. Shared-policy adoption is not included.
- **Rationale and evidence:** The [review reconciliation](references/2026-10-06-review-reconciliation.md)
  maps the report's recommendations to local dispositions and records unverified and deferred findings.
- **Implementation and verification state:** The revised contract and supporting records are prepared for
  final acceptance. This decision records preparation choices, not adoption or human verification. No commit
  or publication is authorized by these selections.
- **Revisit conditions:** Final text acceptance is still required. Revisit rules if actual use reveals
  friction or gaps, or task-specific consumer evidence changes the consequence assessment. Cross-repository
  rollout and enforcement require separate decisions.

## 2026-10-06 — D005: Adopt Slice 1 locally

- **Question and prior position:** The reconciled candidate remained draft after the preparation choices in
  D004. Final text acceptance, metadata standing, and publication were separate decisions.
- **Outcome: accepted.** The operator selected “Adopt locally (Recommended)” for revised candidate
  `33e5e1f29df4` on 2026-10-06. The [walkthrough record](references/2026-10-06-adoption-rulings.md)
  captures the question and response.[^adoption-rulings]
- **Accepted revision:** The candidate manifest has SHA-256 prefix `33e5e1f29df4`. The full manifest and
  verification receipt were saved in BB thread storage as `slice-1-adoption-review.json`; the exact candidate
  diff is `slice-1-candidate.patch`. Subsequent edits record acceptance and align standing and routing.
- **Canonical owners and scope:** `bundle/governance.md` owns the local contract; `bundle/decisions.md` owns
  material decision history; `bundle/formatting.md` owns local OKF and provenance style; and
  `bundle/preset-management.md` is the maintained technical guide for authorized preset work. All four are
  stable, with no invented human `verified` event. AGENTS is the agent entry point; CLAUDE remains its symlink.
  The accepted scope is renovate-config only, including standalone supporting scripts and retained Copilot files.
- **Selected rules:** Separate approval of the concrete result before each push, merge, publication, or
  external change. Representative consumer evidence or an explicit operator exception for shared preset
  behavior changes. Keep both Copilot files; deletion remains separate.
- **Rationale and evidence:** Retain the full local contract after reconciling the cross-repository review.
  The operator chose local acceptance without adopting a shared policy, installing enforcement, or selecting
  new dependency policy. Source captures retain their original metadata and evidence limits.
- **Implementation and verification state:** Local standing and entry-point alignment are implemented.
  Scoped Markdown, metadata, source joins, paths, derived indexes, and ten pinned captures passed before
  acceptance; checks are repeated for the standing edits. These do not prove factual accuracy, live consumer
  behavior, or human content verification. The accepted candidate and final local state remain separate receipts.
- **Remaining authority:** No commit, push, merge, or publication is authorized by adoption. Preset JSON,
  dogfooding, consumer workflows, CI, hooks, and mise/linter configuration remain unchanged. Issue
  [#122](https://github.com/basher83/renovate-config/issues/122) remains paused and unresolved.
- **Revisit conditions:** Revisit when actual use reveals friction, instruction conflicts, or inadequate
  verification; record adaptations and supersession prospectively. Shared rollout, enforcement, publication,
  and dependency-policy choices require their own decisions.

## 2026-10-06 — D006: Correct the three Slice 1 review findings

- **Question and prior position:** The read-only audit found that the checker rejected historical verification,
  skipped locally authored capture headers, and the guide omitted the accepted consumer-evidence exception.
- **Outcome: accepted remediation.** Preserve verification timestamp independence; validate body-mode capture
  headers while retaining imported bodies; align the guide with evidence or an explicit operator exception.
- **Authority and date:** The operator selected “Fix all three (Recommended)” on 2026-10-06, including focused
  regression checks and scoped validation.[^adoption-rulings]
- **Scope and rationale:** Narrow corrections to the supporting checker and guide, with standalone regression
  checks and usage documentation. These implement the adopted rules rather than select new dependency policy.
  The original accepted candidate remains identified in D005; the review and remediation have separate receipts.
- **Implementation and verification state:** Corrections are implemented. Regression fixtures verify retained
  historical events, invalid authored capture headers, and imported-body pins. Six regression tests pass;
  restoring the original bugs in a temporary fixture makes them fail. Scoped lint and bundle checks pass.
  Captured source bodies remain untouched; no human verification event is added.
- **Remaining authority and revisit conditions:** No commit or publication is included. Further findings or
  actual usage can justify another scoped correction; CI, hooks, consumer settings, and preset JSON stay unchanged.

## Copilot content disposition

Both files are marked **Retained for now; deletion requires a separate reviewed change.** Their bodies are retained,
with routing notes and affected path corrections. The specialist YAML frontmatter is preserved. They remain
present; the note does not disable loading or authorize deletion.

| Retained content | Assessment and canonical owner | Disposition in this candidate |
| --- | --- | --- |
| Repository layout, commands, JSON conventions, and inheritance examples in Copilot instructions | Duplicates [AGENTS.md](../AGENTS.md) and the preset guide | Retain per D004; route to the maintained entry point and correct the moved guide path |
| Upstream documentation pointers in the specialist | Useful primary-source navigation, already available through AGENTS | Retain without making a new copy; verify current upstream claims during the relevant future task |
| Specialist troubleshooting sequence | Useful prompts for logs, detection, overrides, permissions, and merge conditions | Retain as capability guidance; task authority determines which checks and changes are in scope |
| Final configuration assembly and pilot-consumer verification | Useful verification principles | Preserve explicitly in the contract's verification section; qualify schema-only claims in the routing note |
| Organization setup, secrets, GitHub App administration, and self-hosting | Capability descriptions beyond Slice 1's authority | Retain with explicit task-authority boundary; no administrative work is activated |
| Generic response templates and assumed future validation | Not a receipt of executed verification; potentially redundant | Retain pending removal decision; AGENTS and the contract require actual checks or explicit gaps |
| Commands to install tooling and broad automerge guidance | Do not establish task authority or proof of suitability | Retain with an overriding task-scope and verification note; no tooling or dependency-policy change |

This content assessment supports the operator's D004 retention selection. A later reviewed deletion decision can
identify what must be preserved first; this adoption does not delete either file.

The [local contract](governance.md) defines the adopted authority and verification boundaries reflected
in this record.[^local-contract] [Formatting guidance](formatting.md) owns the metadata style.

[^slice-1-scope]: Participant-authored capture of the operator's Slice 1 directions, 2026-10-06.
[^adoption-rulings]: Participant-authored operator choices for the revised candidate; including final acceptance.
[^local-contract]: Adopted renovate-config operating contract.
