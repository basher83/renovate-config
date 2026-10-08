---
type: Policy Candidate
title: Explicit approval for GitHub-hosted runner updates
description: This candidate proposes separate grouping and explicit maintainer approval for GitHub-hosted runner updates inherited through the shared preset.
tags: [presets]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-07T23:55:09-04:00 }
sources:
  - id: evaluation
    resource: 2026-10-07-policy-evidence-evaluation.md
    title: Evaluation of the four portfolio sources
  - id: receipt
    resource: 2026-10-07-policy-evidence-receipt.json
    title: Exact input hashes and immutable consumer evidence
  - id: preset
    resource: ../../presets/github-actions-security.json
    title: Operative shared GitHub Actions security preset
  - id: contract
    resource: ../../bundle/governance.md
    title: Local authority, consumer verification, and acceptance contract
  - id: issue
    resource: https://github.com/basher83/renovate-config/issues/122
    title: Runner image and action-input tool policy question
  - id: manager-docs
    resource: https://docs.renovatebot.com/modules/manager/github-actions/
    title: Renovate GitHub Actions dependency types
  - id: runner-docs
    resource: https://docs.renovatebot.com/modules/datasource/github-runners/
    title: Renovate GitHub runners datasource
  - id: approval-docs
    resource: https://docs.renovatebot.com/configuration-options/#dependencydashboardapproval
    title: Renovate Dependency Dashboard approval semantics
  - id: timing
    resource: https://github.com/actions/runner-images/issues/14748
    title: Ubuntu latest alias migration announcement
  - id: retirement
    resource: https://github.blog/changelog/2025-01-15-github-actions-ubuntu-20-runner-image-brownout-dates-and-other-breaking-changes/
    title: GitHub hosted image brownout and retirement example
  - id: review
    resource: 2026-10-07-runner-candidate-review-reconciliation.md
    title: Adversarial review dispositions and authorization reconciliation
---

# Explicit approval for GitHub-hosted runner updates

**Option C selected; implementation prepared for review.** The operator selected C and preparation on 2026-10-07.
[D015](../../bundle/decisions.md#2026-10-07--d015-select-runner-approval-policy-c) records that authority; the
[behavior evaluation](2026-10-08-runner-behavior-evaluation.md) supplies the subsequent evidence. This original
proposal retains its deliberation context; publication and operator PR merge acceptance remain pending.[^receipt]

## Decision requested

**Choose the runner policy and the evidence path.** Recommend **C**: runner-only grouping, dashboard approval
before branch/PR creation, and `automerge: false` for every extracted `github-runner` update. Dashboard approval
permits creation; subsequent merge remains a separate maintainer action.[^approval-docs]

### Timing and decision paths

GitHub schedules the `ubuntu-latest` alias migration to Ubuntu 26.04 from **October 19 to November 19, 2026**,
and describes 26.04 as already generally available. October 19 is twelve calendar days after this memo's date.
It is not a deadline for updating pinned `ubuntu-24.04`, nor a verified Renovate PR arrival date. A candidate
update may be offered earlier; the original draft had not checked current hosted eligibility and PR state.
The subsequent behavior
evaluation
records bot-merged personal-computing PR #39 and a preserved-input replay.[^timing][^receipt]

| Path to select | Consequence |
| --- | --- |
| Read-only dry run first — recommended next evidence work | Refresh personal-computing, extract its actual dependencies, and compare the proposed rule through lookup/grouping without waiting for a hosted PR. Keep current automerge exposure explicit while this runs. |
| Select C with a bounded evidence exception | After baseline extraction, rule comparisons, and strict validation, explicitly identify any unexercised item 4 controls and item 5 hosted observation being deferred, an owner, and a follow-up trigger. Publication still requires approval of the concrete result. |
| Retain current behavior while deferring | A runner update may automerge if offered and passing applicable conditions. This accepts continued exposure; it cannot promise that only one update will merge. |

A consumer-local hold is another possible containment measure, but requires separate, explicit authority for
that consumer. None is applied or authorized by this memo. Do not wait until October 19 to investigate
eligibility; the announced alias migration is a useful planning signal, not the gate's start date.

This memo takes only the runner slice of #122 and the dependency review's larger depType-splitting proposal.
Action-input policy, action/workflow grouping, and sensitive-action coupling remain separate, visible
decision leads. D015 subsequently resumes preparation of this runner subset; action-input implementation remains paused.
No evidence exception has been granted.[^issue][^evaluation][^review]

## Evidence and reasoning

**Observed locally:** the base extends `github-actions-security.json`. That preset gives all `github-actions`
dependencies the same group and enables digest, patch, minor, and major automerge through manager-wide rules,
with package-name exceptions. There is no runner-specific exception. The preset is unchanged from review
revision `e063800` through evaluated HEAD `e24fc5e`.[^preset][^receipt]

**Source-backed:** current Renovate manager documentation lists `github-runner` for hosted runner versions
in `runs-on:` and distinguishes it from `action`, `workflow`, and `uses-with`. The runner datasource defaults
to Docker versioning. Those facts identify an appropriate matching boundary; they do not establish the update
classification assigned by the hosted app to a particular Ubuntu upgrade.[^manager-docs][^runner-docs]

**Direct consumer evidence:** one base-only consumer workflow is captured: `personal-computing` at `1cb3820`
selects `ubuntu-24.04` and independently pins mise through an action input. Zammad-MCP supplies only a config
inheritance/override control; its runner usage was not captured. This is one verified literal runner input,
not broad runner coverage across consumer classes.[^receipt]

**Reported historical behavior:** the dependency review reports runner matching and dashboard evidence, but
its raw extraction/evaluation outputs are absent here. The evaluation records that limit and the conflicting
portfolio consumer counts. This draft does not claim a portfolio-wide behavioral rerun.[^evaluation]

**Policy judgment:** selecting a different runner version changes the CI environment. Passing the exercised
checks does not establish compatibility for every workflow assumption. Explicit review makes that selection
visible to the maintainer. It adds human work; it is not evidence that existing automerge caused an incident.

## Options

| Option | Benefit | Cost or limitation |
| --- | --- | --- |
| A: retain manager-wide behavior | Least maintenance and fastest runner adoption | Runner changes can remain eligible for automerge; mixed groups obscure the environment decision. |
| B: runner-only grouping with major/minor approval and no automerge for those types | Uses #122's type boundary plus the same isolation proposed for C | May gate exactly the same ordinary OS upgrades as C; actual classification remains unmeasured. Other emitted types retain inherited behavior. |
| C: runner-only grouping with approval and no automerge for all extracted runner updates | Same practical gate if real updates are all major/minor, plus protection against classification surprises | Adds maintainer approval/manual merge work relative to A, with no demonstrated extra burden over B. Unattended gates can become failing CI at image brownout or retirement deadlines. |

Recommend **C** for operator review. Docker versioning makes major classification plausible for normal OS
version jumps, but no run here establishes equivalence between B and C. Group isolation is the principal
change beyond #122's example; both gated options can include it. C adds a simple classification-independent
boundary, rather than a demonstrated large increase in approval scope.[^runner-docs]

### Maintenance responsibility and retirement risk

Approval trades unattended runner selection for a deadline the consumer maintainer must watch. GitHub's
Ubuntu 20.04 retirement included scheduled brownouts that deliberately failed CI before removal. That is
a historical example, not a retirement date for Ubuntu 24.04.[^retirement]

If C is adopted, the maintainer of each affected consumer owns pending runner approvals and relevant image
deprecation notices. A pending approval approaching its image's first announced brownout or removal date
requires a migration decision or an explicit alternative before that date. No new reminder machinery is
required, but accepting C must include accepting this maintenance responsibility.

## Scope and expected behavior

The proposed home is a runner-specific rule in `presets/github-actions-security.json`, already inherited
through the base. It is a shared default for consumers resolving that preset, subject to later local rules.
It is not a requirement imposed on every owned repository or on independent Renovate configs.[^preset][^evaluation]

| Case | Intended result if C is accepted and implemented |
| --- | --- |
| Extracted `github-runner` update | Runner-only group; approval pending before branch/PR creation; automerge disabled afterward. |
| Runner and ordinary action updates available together | No branch/group mixing between runners and non-runners; action processing remains independent. |
| `jdx/mise-action` input (`uses-with`) | Existing behavior retained; its approval policy remains a separate decision in #122. |
| Action digest, sensitive action, reusable workflow, job container/service | Existing non-runner configuration retained, including current approval and pinning rules. |
| Floating `ubuntu-latest`, unsupported expressions, self-hosted labels | No claim of freezing the environment: `latest` is extracted but skipped as an invalid version; unsupported inputs produce no eligible runner update. |
| Explicit later consumer override | Report the resulting behavior and owner; the shared default does not override local authority. |
| Existing manager-wide labels | Deliberately retain `github-actions` and `security` for this first slice; `security` remains inherited categorization, not a claim that every runner bump fixes a vulnerability. Label cleanup is deferred. |

Implementation would need to override both inherited group identity fields and automerge behavior after
the manager-wide rules. The specific rule order, group name/slug, and behavior of repeated extensions must
be verified against Renovate, rather than inferred from this table. No executable configuration is supplied
as an adopted implementation in this draft.

## Consumers and publication consequences

The dependency map reports 34 personal base consumers; the other inventory reports 37. The evaluation names
the three classification disagreements. Three external `bossjones` consumers are reported but not directly
rechecked. These figures describe source coverage, not an exact current rollout census.[^evaluation]

The historical report's 88 runner records in 28 repos cannot be divided into eligible literal-version updates
from the attached CSVs: the raw per-dependency outputs are missing. The number affected is unknown. A future
refresh must distinguish supported literal labels, moving aliases, unsupported expressions, and self-hosted
labels. One captured input is enough to motivate this candidate, not to certify portfolio coverage.

At the recorded revisions, personal-computing exercises the base-only runner case and Zammad-MCP exercises
base plus optional/repeated inheritance. Both use mutable preset references. A shared preset publication can
affect consumers on their next resolution/run; it does not migrate an already pinned consumer to a new ref,
prove app installation, or merge an update everywhere. Refresh selected consumer revisions and references
before any implementation publication.[^receipt]

No consumer file edits, bot changes, branch protection changes, runtime caps, mise grouping changes, global
major-automerge rewrite, or preset-versioning migration belong to this candidate. Already open grouped PRs
may need reconciliation when Renovate next runs; new grouping alone is not proof they have been cleared.

## Evidence required for implementation acceptance

The policy recommendation is ready for deliberation. Implementation acceptance for publication requires
the following evidence, or an explicit operator exception identifying the unverified boundary.[^contract]

1. **Fresh scoped inputs:** record consumer SHAs, workflow paths, preset revision/order, local rules,
   Renovate version, and environment. Start with the single captured personal-computing runner case;
   Zammad-MCP is initially only an inheritance/override control. Name further coverage as it is obtained.
2. **Actual extraction:** retain Renovate's extracted literal runner and action-input records. Include the
   concrete `ubuntu-24.04` input; do not substitute only hand-authored dependency objects.
3. **Before/after rule results:** demonstrate runner-only grouping, approval enabled, and automerge disabled.
   Exercise emitted update types and hypothetical controls without presenting the latter as real upgrades.
   Verify repeated preset inheritance and local overrides, including any applicable global update options.
4. **Non-runner and mixed-group controls:** compare action digests, sensitive actions, reusable workflows,
   action-input tool/runtime versions, and containers/services actually present or explicitly fixture-based.
   Confirm no unintended field changes or mixed branches; retain the comparison, not only a pass marker.
5. **Lookup or hosted behavior:** retain a read-only run with real runner lookup results, grouping, and approval
   disposition, or hosted dashboard/job evidence. Do not wait for an uncontrolled automerge to collect it.
   An unavailable update is an explicitly bounded observation gap, not proof of gating. Preserved pre-upgrade
   revisions remain usable for replay if a runner PR has already merged; the first update does not consume
   that input evidence. Such replay is not a historical hosted observation. Verify existing-group
   reconciliation without creating test PRs as a side effect.
6. **Configuration and review:** run strict root/preset validation and applicable hooks. Present the exact
   change, consumer effects, unresolved evidence, and bounded rollback before publication approval.

Use existing tools and retained receipts. This candidate does not require new CI, metadata services, Claims
projection, or policy-enforcement machinery.

## Acceptance, rollback, and revisit

After operator policy selection, record the selected option and rationale separately from implementation
authorization. Drafting authority alone does not lift #122's implementation pause;
D015 records the later narrow resumption. If an evidence exception is
selected, record its exact missing observations, rationale, owner, follow-up trigger, and effective scope;
ordinary publication approval is not an evidence exception.
An eventual acceptance receipt should identify the policy document revision, implementing preset revision,
PR URL, operator merge actor/time, accepted scope, and behavioral evidence. Acceptance of this draft as
research is not acceptance of its recommendation, and accepting runner policy does not settle action inputs.
The chronological trail and material decision record retain their established responsibilities.[^contract]

For an implemented change, propose a reviewed revert of the runner-specific rule if it blocks necessary
maintenance or changes non-runner behavior. Reverting restores the prior automation risk; it does not revert
runner versions already merged in consumers. Consumer remediation remains with their owners.

Revisit the policy if classification evidence favors a narrower gate, a consumer needs an explicit exception,
approvals cause measurable maintenance backlog, a pending approval approaches an announced image brownout or
retirement date, grouping affects unrelated updates, or Renovate changes its runner extraction. Those
observations should drive any later refinement and reusable workflow extraction.

[^receipt]: [Evidence receipt](2026-10-07-policy-evidence-receipt.json), immutable inputs and read-only captures.
[^approval-docs]: [Dashboard approval](https://docs.renovatebot.com/configuration-options/#dependencydashboardapproval), consulted 2026-10-07.
[^timing]: [GitHub migration announcement](https://github.com/actions/runner-images/issues/14748), checked 2026-10-07.
[^issue]: [Issue #122](https://github.com/basher83/renovate-config/issues/122), an open question with two policy subjects.
[^evaluation]: [Four-source evaluation](2026-10-07-policy-evidence-evaluation.md), dispositions and limits.
[^review]: [Review reconciliation](2026-10-07-runner-candidate-review-reconciliation.md), findings and task scope.
[^preset]: [Current shared preset](../../presets/github-actions-security.json), evaluated at `e24fc5e`.
[^manager-docs]: [Manager documentation](https://docs.renovatebot.com/modules/manager/github-actions/), consulted 2026-10-07.
[^runner-docs]: [Runner datasource](https://docs.renovatebot.com/modules/datasource/github-runners/), consulted 2026-10-07.
[^retirement]: [GitHub brownout announcement](https://github.blog/changelog/2025-01-15-github-actions-ubuntu-20-runner-image-brownout-dates-and-other-breaking-changes/), checked 2026-10-07.
[^contract]: [Local contract](../../bundle/governance.md), authority, representative evidence, and operator merge acceptance.
