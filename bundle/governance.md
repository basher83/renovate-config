---
type: Operating Contract
title: Renovate-config operating contract
description: Adopted local rules for authority, bounded work, decisions, evidence, and verification.
tags: [renovate, governance]
status: stable
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T07:38:55Z }
sources:
  - id: shared-draft
    resource: references/agent-working-policy-draft.md
    title: Agent Working Policy — Draft
  - id: local-scope
    resource: references/2026-10-06-slice-1-rulings.md
    title: Slice 1 scope and formatting rulings, 2026-10-06
    author: codex_agent/GPT 6.1 Sol
  - id: review-rulings
    resource: references/2026-10-06-adoption-rulings.md
    title: Local adoption walkthrough choices
    author: codex_agent/GPT 6.1 Sol
  - id: review-reconciliation
    resource: references/2026-10-06-review-reconciliation.md
    title: Shared-policy review reconciliation
    author: codex_agent/GPT 6.1 Sol
  - id: formatting-rules
    resource: formatting.md
    title: Bundle document formatting
    author: codex_agent/GPT 6.1 Sol
---

# Renovate-config operating contract

**Standing: adopted local operating contract.** On 2026-10-06, the operator accepted revised Slice 1
candidate `33e5e1f29df4` for renovate-config. The [adoption decision](decisions.md#2026-10-06--d005-adopt-slice-1-locally)
records scope, authority, and remaining publication work.[^review-rulings]

This is the canonical local contract. It is readable without the Docs vault and applies only to renovate-config.
The shared policy and other repositories retain their own standing. The completed shared-policy review is
reconciled in the [review record](references/2026-10-06-review-reconciliation.md).[^review-reconciliation]
The operator's preparation directions established the local bundle and its boundaries.[^local-scope]
Adoption does not authorize a commit, publication, or dependency-policy change. Existing JSON remains operative.

## Repository responsibilities

This repository provides shared Renovate configuration to repositories extending its presets:

- `default.json` and `presets/*.json` implement shared dependency-update behavior.
- `renovate.json` configures this repository's own dependency updates.
- `examples/` illustrates consumer configurations; examples do not establish current consumer state.
- `sources/` holds discovery and source material, with the limitations recorded alongside it.
- `docs/audits/` holds dated observations; `docs/official-docs/` holds upstream reference mirrors.
- `bundle/` holds local operating guidance, prospective decisions, and the preset-management reference.
- Tasks, workflows, hooks, linter configuration, and agent entry points support repository work.

Location does not establish authority, truth, freshness, or adoption. Moving a guide to `bundle/` does not
approve its recommendations. Existing JSON is operative configuration; missing decision provenance is a gap
to report, not permission to invent historical approval or alter behavior.

## 1. Authority and intent

The operator decides goals, risk tolerance, and dependency policy. Agents investigate, recommend, and perform
authorized work. Relevant primary sources and direct observations establish empirical behavior. A preference
does not establish an external fact; a fact or successful check does not select policy.

Read the task and relevant discussion before acting. Distinguish investigation, policy deliberation,
implementation of a selected outcome, and repository maintenance. Suggested code in an issue remains a
candidate until the task or an explicit decision authorizes implementation. Tool access and technical
capability do not confer authority to change presets, consumers, secrets, or organization settings.

Use existing authorization for investigation, preparation, and commits without repeated approval requests.
Before each push, merge, publication, or external change, obtain separate operator approval of the concrete
result and its consequences. Preparation alone does not authorize a commit. State unresolved consequential
choices and their effects. This agent contract does not revoke configured authority for Renovate or other
existing automation identities.[^review-rulings]

Global, ancestor, domain, repository, and task instructions can all affect a session. Follow the harness
instruction priority; this local contract does not make AGENTS the sole loaded source or override higher
priority instructions. Surface material conflicts before dependent work when they cannot be resolved from
that priority or existing operator direction. A local contract does not authorize changing another guidance
layer or another repository.[^review-reconciliation]

## 2. Standing of material

Keep observations and source material distinct from provisional conclusions, accepted decisions, executable
configuration, and repository machinery. Research may end with a recommendation and uncertainty without
changing policy or JSON. Describe which statements are observed, source-backed, inferred, or still unknown.

OKF metadata describes document type, provenance, and lifecycle. A `status` value or `verified` field does
not itself authenticate a policy decision. Record actual adoption authority in the decision log. Generation,
content verification, policy acceptance, implementation, and publication are separate events.

## 3. Bounded work and consumers

For material work, identify the purpose, work type, authorized outcome, affected surfaces and consumer classes,
exclusions, and completion condition. Name the evidence or operator direction that would justify revisiting
scope. Scale this explanation to the ambiguity and impact of the task.

A change to a shared preset affects repositories extending that preset, including through inheritance.
Establish the affected consumer classes from evidence; do not infer universal use from ownership or a repository
inventory. Local editing authority does not automatically authorize changes in consuming repositories.

Publishing a change to the shared presets makes it available to consumers that resolve the changed revision.
The effect depends on their preset references, Renovate execution, local overrides, and merge settings;
publishing here does not itself prove adoption or a successful update in every consumer. A consumer merge
can trigger deployment or artifact publication according to that consumer's own configuration. The review
reports a Renovate-to-Argo deployment chain; its live state has not been independently verified here.
For a proposed behavior change, identify the relevant consumer and publication consequences before approval,
using task-specific evidence rather than treating the inventory as a complete consequence map.[^review-reconciliation]

New findings can justify another workstream, but do not silently expand the current task into a migration,
dependency-policy selection, consumer rollout, or enforcement project.

## 4. Adoption and decision history

Record material decisions prospectively in [decisions.md](decisions.md): the question and prior position,
accepted/adapted/deferred/rejected outcome, authority, date, effective scope, rationale, evidence pointers,
implementation and verification state, and revisit or supersession conditions.

Routine maintenance needs proportionate rationale. Do not reconstruct approval for every existing preset.
Preserve superseded rationale when decisions change. Git records the edit; a concise decision entry explains
its meaning without requiring reconstruction of the full conversation.

The operator accepted the full local Slice 1 after review reconciliation, rather than adopting a minimal
pilot. This acceptance applies to this repository's operating guidance and standalone supporting tools;
shared adoption and enforcement remain separate decisions.[^review-rulings] The separate cross-repository
Renovate review informs later dependency decisions. Issue
[#122](https://github.com/basher83/renovate-config/issues/122) remains paused and unresolved; this adoption
does not select its runner or tool-update policy.

## 5. Change discipline and publication

Preserve operator edits and unrelated work. Keep responsibility boundaries reviewable and avoid opportunistic
rewrites. Separate investigation, policy selection, implementation, and publication when their authority or
completion conditions differ. Follow [AGENTS.md](../AGENTS.md) for configuration conventions and commands.

Do not commit as an incidental consequence of drafting or verification; commits require task authorization.
Before each push, merge, publication, or external change, present the concrete result and obtain separate
operator approval, even when earlier task direction named that action. Approval applies to the stated action,
result, and scope; a changed result or a different action needs its own approval. Consumer edits and external
settings remain under their owners' processes. Keep the previously published mise setting correction separate
from this governance adoption.[^review-rulings]

## 6. Verification and its limits

Match each claim to a check that can establish it:

| Claim | Relevant evidence | Limits |
| --- | --- | --- |
| Configuration accepted by Renovate | Strict validator output for the complete relevant files, with version and scope | Does not prove extraction, matching, consumer results, or policy suitability |
| Dependency extracted and rule matched | Manager output and rule diagnostics for representative dependencies | Does not establish every consumer's inherited behavior |
| Effective inherited configuration | Resolved configuration, preset order, and local overrides for an identified consumer | Does not establish a successful update or merge |
| Observed consumer behavior | Identified consumer logs, update results, checks, and merge conditions | Applies to the observed revision, environment, and time |
| Policy or prose accepted | Explicit operator decision with scope | Cannot be inferred from lint, metadata, or an agent-written approval marker |
| Edited documentation checked | Scoped Markdown lint, complete-body review, and local link checks | Does not establish factual accuracy or external link availability |

For a shared preset behavior change, require strict validation and relevant extraction, rule-matching, or
resolved-configuration evidence from an identified representative consumer before accepting the change for
publication. Identify its revision, environment, tested dependencies, and limits. If that evidence cannot be
obtained, state the gap and obtain an explicit operator exception; ordinary publication approval does not
imply that exception. One consumer does not prove all consumers or a successful deployment. For other
authorized configuration changes, assemble and check the relevant complete configuration against the claims.
Branch protection and passing checks are merge conditions, not proof that an update is suitable.[^review-rulings]

For documentation-only work, inspect actual linter coverage. The current umbrella task does not explicitly
cover `bundle/` or AGENTS and excludes `.github`. Use a supported scoped invocation before claiming that edited
entry points were checked. Do not install tools or broaden machinery merely to turn an unavailable check green.

## 7. Enforcement limits

This contract is guidance, not a verified blocking mechanism. Standalone documentation and capture checks are
accepted supporting tools, but no CI, hooks, branch rules, or automated blocking mechanism is installed.
Distinguish written instructions, reporting signals, blocking checks, and verified installations.
Future enforcement needs an adopted requirement and an observed repository need; evaluate it separately after use.

## Source revision and formatting

This contract applies the [captured Agent Working Policy — Draft](references/agent-working-policy-draft.md),
read from the Repository Contracts and Policy Docs vault on 2026-10-06, SHA-256 prefix
`290537172062`.[^shared-draft] The [capture record](references/2026-10-06-source-captures.md) identifies the
origin and exact-body comparison.

The shared source remains unadopted. This contract states the local application in full; its local capture
makes provenance inspectable without requiring access to the vault.

The operator selected OKF v0.2 formatting for the Slice 1 bundle documents.[^local-scope]
[Bundle document formatting](formatting.md) owns the field ordering, actor style, source attribution, draft
standing, and verification guidance. It identifies the cached specification and local house-style references,
including their provenance limits. No OKF runtime or enforcement has been installed here.[^formatting-rules]

[^review-rulings]: Participant-authored adoption walkthrough record, including the operator's final acceptance.
[^review-reconciliation]: Reconciliation of the completed review, including reported-evidence limits and deferred work.
[^local-scope]: Participant-authored capture of the operator's Slice 1 directions, 2026-10-06.
[^shared-draft]: Captured Agent Working Policy — Draft, with original body hash identified above.
[^formatting-rules]: Adopted local bundle document formatting reference.
