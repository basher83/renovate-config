---
type: Operating Contract
title: Renovate-config operating contract
description: This contract defines the exemplar purpose, authority, knowledge boundaries, and agent and code responsibilities.
tags: [governance]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-07T23:55:09-04:00 }
sources:
  - id: okf-spec
    resource: ../sources/evaluate/okf-spec.md
    title: Consulted opensrc-cached OKF v0.2 specification
  - id: exemplar-intent
    resource: ../sources/evaluate/2026-10-06-exemplar-intent.md
    title: Operator clarification of exemplar purpose and documentation responsibilities
  - id: shared-draft
    resource: ../sources/evaluate/agent-working-policy-draft.md
    title: Agent Working Policy — Draft
  - id: local-scope
    resource: ../sources/evaluate/2026-10-06-slice-1-rulings.md
    title: Slice 1 scope and formatting rulings, 2026-10-06
    author: codex_agent/GPT 6.1 Sol
  - id: review-rulings
    resource: ../sources/evaluate/2026-10-06-adoption-rulings.md
    title: Local adoption walkthrough choices
    author: codex_agent/GPT 6.1 Sol
  - id: review-reconciliation
    resource: ../sources/evaluate/2026-10-06-review-reconciliation.md
    title: Shared-policy review reconciliation
    author: codex_agent/GPT 6.1 Sol
  - id: formatting-rules
    resource: /formatting.md
    title: Bundle document formatting
    author: codex_agent/GPT 6.1 Sol
  - id: intake-placement
    resource: ../sources/evaluate/2026-10-07-policy-evidence-receipt.json
    title: Operator agreement on authored proposal intake and placement
  - id: distribution-ruling
    resource: ../sources/evaluate/2026-10-07-bundle-distribution-ruling.json
    title: Operator ruling on repository-bound bundle references
---

# Renovate-config operating contract

**Standing: documentation candidate extending the adopted local contract.** Existing decisions retain their
recorded scope. This revision captures the operator's clarified intent and proposes the remaining lifecycle
and enforcement model for review. It does not select dependency policy or authorize publication.

## Purpose and completion boundary

Renovate-config is the bounded proving ground for a repository-held process, contract, knowledge boundary,
and authority model. Its small configuration surface makes the model practical to refine; its shared presets
make dependency-policy changes consequential for consumers. The intended end state is a working local exemplar
that other repositories can evaluate and emulate through their own explicit adoption decisions.[^exemplar-intent]

The exemplar must demonstrate that instructions, implementation, persisted output, and acceptance evidence
agree. Documenting a rule or passing one check is not completion. Before proposing reuse elsewhere, identify
owners and authorized write surfaces; exercise finalization and rejection/repair paths; verify persisted results;
record human acceptance of the reviewed revision; and report remaining bypasses and unsupported claims.
These acceptance conditions are a proposed completion model, not evidence that the exemplar is complete.

### Repository boundary and distribution

This bundle is an exemplar to point to as known good within this repository; it is not required to be
distributed independently or used as a template. Other repositories can evaluate and adapt the demonstrated
pattern through their own adoption decisions. This ruling does not establish that the exemplar is complete.
The repository, rather than `bundle/` alone, is the local reference boundary.[^distribution-ruling]

Local source and resource paths may leave `bundle/` but MUST resolve inside this repository. They MUST NOT
refer to another checkout, home directory, or other location on the host filesystem, including through a
symlink escape. Material held in another repository or checkout must be referenced by a followable Git-hosted
URL, preferably identifying a commit and artifact path. Ordinary external primary web sources retain their
URLs. Referencing material does not adopt its policy or grant authority over its repository.

The existing checker enforces resolved local path containment within the repository; it does not authenticate
external URL content, availability, or revision stability. Standalone packaging is not a current requirement.
Revisit this boundary only if the operator selects distribution beyond this repository.

## Governing division of work

Agents author within the task's authorized scope. Repository code owns designated structure and metadata,
reconciles those outputs at defined lifecycle boundaries, and verifies the persisted result. Passing checks
does not grant authority to adopt policy, manufacture verification, commit, or publish.

[Repository enforcement](/enforcement.md) names current and proposed ownership, the mise interface, failure
responses, and evidence. Agents may not directly target code-owned outputs or change their owning machinery
as a workaround. Changing that machinery is a separate authorized task.

## Documentation ownership

- This concept owns purpose, authority, knowledge boundaries, source evaluation, and promotion requirements.
- [Enforcement](/enforcement.md) owns artifact/field ownership, deterministic lifecycle operations, and coverage.
- [Formatting](/formatting.md) owns permitted authoring conventions; it does not assign implementation authority.
- [Decisions](/decisions.md) retains questions, selected outcomes, authority, scope, rationale, and supersession.
- [Preset management](/preset-management.md) applies the contract to authorized dependency changes and consumers.
- Root [log.md](/log.md) carries the chronological change and lifecycle trail under OKF §9. Entries point to
  concepts, decisions, and evidence; concept bodies hold current knowledge rather than a running activity journal.
- Indexes are derived navigation, owned by the generator. They do not hold policy or acceptance semantics.

The decision record remains a deliberate record of rationale, not a replacement chronological journal.
A log entry does not itself adopt policy or prove a claim. Corrections to history are explicit entries;
prior events and superseded rationale remain discoverable.

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

## Knowledge layers and source evaluation

This repository separates raw evidence, provisional synthesis, and maintained knowledge. The operator clarified
this boundary during review on 2026-10-06. Greenfield supplies examples of frontmatter conventions and deterministic
Python checks; borrowing those mechanisms does not adopt its evidence-containment or directory rules.

- **Sources:** Root `sources/` holds raw material, captures, observations, and records. A citation does not turn
  a source into a concept or require copying it into the bundle.
- **Research:** Root `research/` holds provisional analysis and synthesis across identified sources. Research
  develops findings, alternatives, and uncertainty; it does not establish adopted policy. A bounded
  recommendation submitted for an operator decision belongs in pending evaluation, with its supporting
  analysis and evidence identified separately.
- **Knowledge:** `bundle/` holds maintained, reusable concepts. Knowledge enters through deliberate promotion
  with a recorded outcome, rationale, evidence, and applicable operator authority. Promotion leaves sources intact.
- **References:** Under OKF v0.2 §6.3, `bundle/references/` conventionally holds external material, run instructions,
  or code represented as first-class concepts and supporting executable artifacts. The name is optional. Ordinary
  Markdown files there are concepts, except reserved `index.md` and `log.md` (§3.1). Raw evidence and provisional
  analysis belong outside the bundle; being cited is not an admission criterion. Standalone tools remain supporting
  machinery and do not establish the standing of the material they inspect.

The format authority is the [OKF
specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
Its `sources` field permits internal or external derivation material (§5.1), and path-valued fields permit URLs
and relative paths (§6.2). It does not require a locally captured copy of every cited source.[^okf-spec]

Local extensions for [resource binding](/formatting.md#distinguish-resource-binding-from-derivation),
[tags](/formatting.md#use-the-accepted-tag-vocabulary), [cross-links](/formatting.md#use-bundle-absolute-cross-links),
and [history](/formatting.md#record-scoped-history) belong to the formatting concept.

### Index ownership

Agents must never issue direct tool calls targeting an `index.md` governed by this bundle. The
[formatting guidance](/formatting.md#generate-governed-indexes) names the owning generator and its explicit
outputs, including the intake index outside the bundle. Agents author permitted inputs; repository code
finalizes indexes through mise at the pre-commit boundary, then checks for drift. Indexes provide navigation; this
contract owns layer definitions and evaluation criteria.

### Pending evaluation

[`sources/evaluate/`](../sources/evaluate/index.md) is intake for sources, authored evaluation records, and
authored proposals awaiting an operator decision. Source evaluation determines an artifact's evidentiary role;
proposal evaluation determines whether to select its recommendation. These are distinct decisions even when
their records share the intake directory. This clarification follows the operator's placement agreement
recorded in [D013](/decisions.md#2026-10-07--d013-place-decision-proposals-in-pending-evaluation).[^intake-placement]
Placement records pending evaluation only. It does not establish truth, necessity, acceptance, or promotion.
Preserved frontmatter describes the source's original context, even when it says `stable` or records verification;
that metadata does not grant local standing. Prior citations record historical use, not a completed evaluation.

An authored proposal identifies its type, draft standing, decision requested, supporting evidence, and
acceptance conditions. It is not raw evidence or adopted knowledge. Exploratory analysis can remain in
`research/`; the proposal links to it. A selected proposal receives a scoped decision record and any accepted
knowledge is promoted into its owning bundle concept under the existing PR acceptance boundary. Source
evaluation, policy selection, implementation authorization, and promotion remain separate events.

Evaluate each item before deciding its retained role or using it to support a new bundle assertion:

1. Identify the local question or claim it could support, and whether it contributes relevant evidence.
2. Establish origin, version or capture date, fidelity, credibility, and limits. Distinguish observations,
   operator directions, agent interpretations, and proposals; do not infer authority from an authored record.
3. Decide whether the assertion needs this particular artifact. Determine whether a direct upstream citation,
   an existing source, or a retained local snapshot best supports it. Misplacement alone does not justify retention.
4. Assess reusable value, duplication, freshness, and consistency with the local boundary and adopted decisions.
   A source's conventions do not become local policy through citation or copying.
5. Record the outcome and rationale: retain as a source with a named role and destination; investigate or synthesize
   in `research/`; propose an augmentation or new concept through promotion; reject; or defer with a revisit condition.
   Identify affected assertions and pointers. Removal or changes to adopted policy require applicable authority.

Promotion is a separate decision from source retention. A retained source need not become knowledge, and a concept
can cite an external source without a local mirror. Evaluation and structural checks do not authenticate operator
approval or factual accuracy. These are governing instructions; no automated evaluation or promotion gate is installed.

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

Record material decisions prospectively in [decisions.md](/decisions.md): the question and prior position,
accepted/adapted/deferred/rejected outcome, authority, date, effective scope, rationale, evidence pointers,
implementation and verification state, and revisit or supersession conditions.

Routine maintenance needs proportionate rationale. Do not reconstruct approval for every existing preset.
Preserve superseded rationale when decisions change. Git records the edit; a concise decision entry explains
its meaning without requiring reconstruction of the full conversation.

Historical adoption and subsequent adaptations are linked from [log.md](/log.md) and recorded with their
scope in [decisions.md](/decisions.md). Issue #122 and dependency-policy selection remain separate workstreams.

The operator subsequently selected separate runner grouping, dashboard approval for every extracted runner
update, and no automerge, and authorized implementation preparation under
[D015](/decisions.md#2026-10-07--d015-select-runner-approval-policy-c).
[D016](/decisions.md#2026-10-09--d016-replace-runner-manual-merge-with-automerge) later replaced manual merge with
automerge after approval. That scoped resumption does not select
action-input policy or authorize publication; the earlier #122 pause remains historical.

### Human acceptance at the PR boundary

Human acceptance is **merge of the PR by the operator** for the reviewed governance or knowledge change.
Record the PR URL, merged revision, merge actor, timestamp, and accepted scope. Checks and agent-authored
markers cannot substitute for that attributable event. Unmerged work remains a candidate; later changes
are outside the prior merge's acceptance until accepted in their own scope.

Root [log.md](/log.md) records the acceptance event and links to its evidence. Material policy choices retain
rationale in [decisions.md](/decisions.md). The merge is also a publication event on its target branch;
applicable approval must precede that action. It does not authorize consumer edits or adoption elsewhere.

PR acceptance does not implicitly verify every claim, accept unevaluated sources, or create a human `verified`
event. Those statements require their own evidence and scope. Automated or indirect merges must not be
reported as operator acceptance without a separately selected authority rule. A future projector may consume
merge evidence, but no PR/Claims projection is implemented here.[^exemplar-intent]

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

## 7. Enforcement and current coverage

The contract defines required behavior; [enforcement.md](/enforcement.md) distinguishes implemented controls
from proposed ones. Index finalization and structural validation are configured through mise at pre-commit.
Metadata reconciliation, promotion/acceptance projection, and stronger publication checks remain proposals.
No installed hook prevents every bypass or proves factual accuracy. Coverage claims require receipts for the
specific revision and environment; documented commands do not establish execution.

## Source revision and formatting

This contract applies the [captured Agent Working Policy — Draft](../sources/evaluate/agent-working-policy-draft.md),
read from the Repository Contracts and Policy Docs vault on 2026-10-06, SHA-256 prefix
`290537172062`.[^shared-draft] The [capture record](../sources/evaluate/2026-10-06-source-captures.md) identifies the
origin and exact-body comparison.

The shared source remains unadopted. This contract states the local application in full; its local capture
makes provenance inspectable without requiring access to the vault.

The operator selected OKF v0.2 formatting for the Slice 1 bundle documents.[^local-scope]
[Bundle document formatting](/formatting.md) owns the field ordering, actor style, source attribution, draft
standing, and verification guidance. It identifies the cached specification and local house-style references,
including their provenance limits. Current enforcement coverage is recorded separately.[^formatting-rules]

[^exemplar-intent]: Participant-authored record of operator clarification in this review; operator selected PR merge
    as acceptance; machine projection remains unimplemented.
[^distribution-ruling]: Exact current-session operator ruling on repository containment and no standalone distribution requirement.
[^okf-spec]: Consulted cached specification, preserved in pending evaluation; the upstream link identifies its origin.
[^intake-placement]: Current-session operator agreement on authored proposal intake, preserved in the evidence receipt.
[^review-rulings]: Participant-authored adoption walkthrough record, including the operator's final acceptance.
[^review-reconciliation]: Reconciliation of the completed review, including reported-evidence limits and deferred work.
[^shared-draft]: Captured Agent Working Policy — Draft, with original body hash identified above.
[^local-scope]: Participant-authored capture of the operator's Slice 1 directions, 2026-10-06.
[^formatting-rules]: Adopted local bundle document formatting reference.
