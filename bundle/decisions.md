---
type: Decision Record
title: Renovate-config prospective decisions
description: This record preserves material decisions, their authority, rationale, scope, and revisit conditions.
tags: [governance]
status: stable
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-07T23:32:20-04:00 }
sources:
  - id: review-verdicts
    resource: https://github.com/basher83/renovate-config/pull/123#issuecomment-6025792492
    title: Operator verdicts on local OKF extensions and locked vocabulary
  - id: exemplar-intent
    resource: ../sources/evaluate/2026-10-06-exemplar-intent.md
    title: Operator clarification of exemplar purpose and acceptance
  - id: slice-1-scope
    resource: ../sources/evaluate/2026-10-06-slice-1-rulings.md
    title: Slice 1 scope and formatting rulings, 2026-10-06
    author: codex_agent/GPT 6.1 Sol
  - id: adoption-rulings
    resource: ../sources/evaluate/2026-10-06-adoption-rulings.md
    title: Local adoption walkthrough choices
    author: codex_agent/GPT 6.1 Sol
  - id: local-contract
    resource: /governance.md
    title: Local operating contract
  - id: distribution-ruling
    resource: ../sources/evaluate/2026-10-07-bundle-distribution-ruling.json
    title: Exact operator ruling on distribution and repository path containment
---

# Renovate-config prospective decisions

**Standing: maintained decision rationale.** Root [log.md](/log.md) owns the chronological trail.
This record preserves material choices, authority, scope, and supersession; it does not reconstruct
approval for existing preset rules or turn a journal entry into an acceptance receipt.

For each material decision, record the question and prior position, outcome, authority, effective scope,
rationale, evidence, implementation and verification state, and revisit or supersession conditions.
Keep routine maintenance records proportionate. Preserve prior rationale when superseding an entry.

## 2026-10-07 — D014: Bound local references to this repository

- **Question and prior position:** OKF permits external derivation sources; standalone distribution had not
  been selected. The operator narrowed the question to whether this bundle needs distribution beyond its repo.
- **Outcome: operator-selected boundary.** No standalone distribution requirement. Local paths may leave
  `bundle/` but must resolve within this repository. Material in another checkout uses Git-hosted artifact
  URLs rather than filesystem pointers.
- **Authority and date:** Direct operator ruling on 2026-10-07 in session
  `01a1181a-7f5f-7153-b479-cf8c12409702`; exact messages are preserved in the
  [ruling receipt](../sources/evaluate/2026-10-07-bundle-distribution-ruling.json).[^distribution-ruling]
- **Scope and rationale:** Local governance, reference guidance, and agent entry point. An exemplar is a
  known-good reference, not necessarily a distributed template. Host filesystem dependencies would merely
  move the portability failure outside the bundle; repository containment provides the intended boundary.
- **Implementation and verification state:** Guidance is updated locally. Existing resolved-path validation
  already enforces repository containment, including symlink escapes; no machinery change is needed.
  Scoped checks verify guidance and the existing boundary, not external URL availability or human verification.
- **Remaining authority and revisit conditions:** The ruling selects this local boundary; PR preparation is
  separately authorized. Human acceptance occurs through operator merge of the reviewed PR. Runner-policy
  selection, consumer edits, and adoption elsewhere remain separate. Revisit if distribution beyond this
  repository is explicitly selected.

## 2026-10-06 — D012: Apply reviewed local OKF extensions

- **Question and prior position:** Root concepts used repository-identity tags, fragment descriptions, and
  document-relative in-bundle links; four tool directories lacked generated indexes.
- **Outcome: authorized correction.** Apply the operator's PR rules in the owning formatting concept,
  update current documents, and extend deterministic generation and validation to the complete hierarchy.
- **Authority and date:** Operator verdicts in [PR #123](https://github.com/basher83/renovate-config/pull/123#issuecomment-6025792492)
  and the linked resource, provenance, and cross-link comments on 2026-10-06; requested implementation in this session.[^review-verdicts]
- **Effective scope:** Concept descriptions, tags, derivation joins, in-bundle paths, logs, generator, checker,
  lint coverage, regression fixtures, and agent guidance. Imported captures and dependency JSON stay unchanged.
- **Rationale:** Owning concepts state local extensions; deterministic code implements structural checks.
  Resource binding and sentence meaning require semantic review rather than manufactured metadata assertions.
- **Implementation state:** Prepared for review. Pre-commit remains the configured finalization boundary;
  an outgoing-revision guard is not implemented. New vocabulary or log labels need human acceptance via PR.
- **Revisit condition:** Accepted changes to vocabulary, hierarchy, or lifecycle boundaries require matching tooling.

## 2026-10-06 — D011: Reconcile the complete pre-commit boundary

- **Question and prior position:** The index hook passed alone, but existing fixers could alter pinned capture
  bytes, the shebang hook treated code captures as executable scripts, and Markdown coverage omitted new documents.
- **Outcome: authorized remediation.** Preserve the ten pinned captures with exact per-hook exclusions from
  whitespace and end-of-file rewriting, and exclude the four code captures from executable-shebang enforcement.
  Secret detection, size, merge-conflict, syntax, and other applicable structural checks remain enabled.
- **Authority and date:** The operator approved the fix plan on 2026-10-06. The work covers hook reconciliation,
  a mise lint interface, fixture isolation, validation, and a replacement PR description prepared for review.
- **Rationale:** Imported evidence must retain its recorded bytes; authored documents and generated navigation
  need explicit complete lint coverage. The legacy Markdown hook delegates governed surfaces to `bundle:lint`.
- **Effective scope:** Hook configuration, `bundle:lint`, agent guidance, isolated regression fixtures, and trail.
  Preset behavior, metadata repair, Claims projection, consumer changes, commit, and publication are excluded.
- **Implementation state:** Prepared in the worktree. Full combined hooks and boundary exercises supply the
  validation receipt; earlier green CI applies only to the previously published PR head.
- **Revisit condition:** New capture types or governed Markdown surfaces require coverage and preservation review.

## 2026-10-06 — D010: Capture exemplar intent and separate the trail

- **Question and prior position:** The bundle described local Slice 1 rules and index tooling without stating
  the exemplar purpose or a general artifact/field ownership model.
- **Outcome: agreed documentation direction.** The operator concurred with the gap review and document
  responsibilities, then identified root `log.md` as the chronological trail outside concept bodies.
- **Authority and date:** Operator feedback in this review on 2026-10-06; a
  [participant-authored source record](../sources/evaluate/2026-10-06-exemplar-intent.md) captures the scope.[^exemplar-intent]
- **Purpose:** Demonstrate the model in this small but consequential repository before proposing reuse elsewhere.
- **Effective scope:** Draft purpose and ownership revisions, a dedicated enforcement concept, log conventions,
  and the minimal structural support needed to validate the new reserved log. Metadata repair, Claims deployment,
  PR acceptance projection, and publication controls remain proposals rather than implemented mechanisms.
- **Selected acceptance boundary:** In the follow-up question, the operator selected merge of the PR by the
  operator. Receipts must identify the PR, merged revision, actor, time, and scope. Projector implementation
  and treatment of indirect/automated merges remain open; no human verification is inferred.
- **Implementation state:** Documentation candidate prepared for feedback; no commit or publication authorized.
- **Revisit condition:** Review the proposed ownership matrix and select lifecycle events before implementing them.

## 2026-10-06 — D009: Finalize indexes through mise before commit

- **Question and prior position:** Direct generator commands still left agents responsible for index maintenance.
- **Outcome: adapted.** Mise is the interface. Agents must not issue direct tool calls targeting governed indexes.
  A configured pre-commit hook calls `bundle:finalize` to generate and check all three outputs automatically.
  Entries are sorted from metadata, without preserving order from prior index content.
- **Authority and date:** Operator direction on 2026-10-06 requires the mise interface and automatic index updates
  at a boundary before push, using the OKF reference agent and OpenWiki as implementation examples.
- **Rationale:** Both examples finalize indexes after agent authoring. OpenWiki separates agent page writes from
  deterministic index synchronization. The OKF reference agent renders indexes in code but can synthesize directory
  descriptions with a model; this repository uses no model in generation. Finalizing before commit ensures outputs
  can enter the reviewed commit rather than becoming uncommitted changes during push.
- **Effective scope:** Mise tasks, one local pre-commit configuration entry, generator ordering, and guidance.
  No automatic staging, commit, push, hook replacement, or harness-specific filesystem restriction is introduced.
- **Implementation and verification state:** Configured in the worktree. The existing prek pre-commit shim reads
  repository configuration. Generation changes stop commit for review and inclusion; a bypassed hook is not enforcement.
- **Revisit condition:** Reassess if another authoring workflow needs finalization or a stronger write boundary.

## 2026-10-06 — D008: Govern indexes through their generator

- **Question and prior position:** The correction manually authored the intake index with status prose and
  basename-only entries, bypassing the deterministic generator and the OKF index convention.
- **Outcome: adapted.** Agents must never directly modify a bundle-governed `index.md`. Extend the generator
  to own `sources/evaluate/index.md` alongside the two bundle indexes; derive titles and descriptions from
  metadata and check all three outputs for drift. Governance semantics remain in their owning documents.
- **Authority and date:** Direct operator instruction on 2026-10-06 requires the explicit prohibition for agents,
  following the agreed correction to generate intake navigation.
- **Effective scope:** Agent instructions, bundle guidance, generator, checker, and temporary regression fixtures.
- **Implementation and verification state:** Implemented in the worktree; no commit or publication authorized.
- **Revisit condition:** New governed indexes require an explicit generator scope and documented ownership.

## 2026-10-06 — D007: Separate knowledge from sources pending evaluation

- **Question and prior position:** The Slice 1 agent borrowed Greenfield's evidence-containment layout while
  the operator intended examples of frontmatter conventions and deterministic Python enforcement. No separate
  comparison of `bundle/references/` with root `sources/` established that placement.
- **Outcome: adapted.** Define sources, research, knowledge, and OKF references in the
  [operating contract](/governance.md#knowledge-layers-and-source-evaluation), including evaluation and promotion
  criteria. Move every root Markdown file from `bundle/references/` into `sources/evaluate/`.
- **Authority and date:** Direct operator instruction in this review on 2026-10-06: establish the criteria and
  boundaries first, then move those files to a directory that records sources awaiting evaluation and action.
- **Effective scope:** Guidance, intake navigation, affected pointers, and standalone checker/index adaptations.
  Existing tooling and code-snapshot directories remain in place. No individual source is accepted, rejected,
  promoted, or selected for removal by this move. Preset behavior and installed enforcement remain unchanged.
- **Rationale:** Misplacement does not establish a need for retention. OKF permits external sources and relative
  pointers; its references convention does not require copying cited evidence into the bundle. Prior use and
  preserved source metadata do not resolve pending evaluation.
- **Implementation and verification state:** Applied in the worktree; imported captures retain their bytes.
  Checks establish structural consistency and fidelity, not source suitability. No commit or publication is authorized.
- **Revisit condition:** Evaluate individual records against the contract, record their outcomes, and resolve
  future retention, research, or promotion deliberately. Earlier decisions remain historical records.

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
- **Evidence pointers:** [Candidate contract](/governance.md), [preset-management guide](/preset-management.md),
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
  owner in [formatting.md](/formatting.md), with the other entry points linking to it.
- **Authority and date:** Operator direction on 2026-10-06: do not invent fields because the schema permits
  them; follow the greenfield governance trail for formatting; these rules need their own document.
- **Effective scope:** The Slice 1 bundle documents and their navigation. Keep ordinary Markdown bodies
  intact except for moving duplicated formatting guidance to its owner and correcting producer attribution.
  This does not adopt the operating contract or greenfield's learning-specific type and directory rules.
- **Implementation and verification state:** The formatting reference is a draft, with no human verification
  claimed. Metadata, lint, and pointer checks establish their stated scope only; no enforcement is added.
- **Remaining work and revisit condition:** The particular-record sources are now captured in
  [references](../sources/evaluate/index.md), with origins and fidelity limits recorded separately. Reconcile broader
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
  [rulings record](../sources/evaluate/2026-10-06-adoption-rulings.md).[^adoption-rulings]
- **Effective scope:** Revised local candidate only. Configured bot authority, preset JSON, consumers, CI,
  hooks, and repository machinery remain unchanged. Shared-policy adoption is not included.
- **Rationale and evidence:** The [review reconciliation](../sources/evaluate/2026-10-06-review-reconciliation.md)
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
  `33e5e1f29df4` on 2026-10-06. The [walkthrough record](../sources/evaluate/2026-10-06-adoption-rulings.md)
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

The [local contract](/governance.md) defines the adopted authority and verification boundaries reflected
in this record.[^local-contract] [Formatting guidance](/formatting.md) owns the metadata style.

[^distribution-ruling]: Exact current-session operator ruling on repository containment and no standalone distribution requirement.
[^review-verdicts]: Operator PR instructions on descriptions, index coverage, logs, tags, and the linked earlier rules.
[^exemplar-intent]: Participant-authored summary of operator direction and the selected PR-merge acceptance boundary.
[^slice-1-scope]: Participant-authored capture of the operator's Slice 1 directions, 2026-10-06.
[^adoption-rulings]: Participant-authored operator choices for the revised candidate; including final acceptance.
[^local-contract]: Adopted renovate-config operating contract.
