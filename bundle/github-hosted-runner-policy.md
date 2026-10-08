---
type: Policy
title: GitHub-hosted runner update policy
description: This policy requires separate grouping, dashboard approval, and manual merge for extracted GitHub-hosted runner updates.
tags: [presets]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-07T23:55:09-04:00 }
sources:
  - id: selection
    resource: /decisions.md#2026-10-07--d015-select-runner-approval-policy-c
    title: Operator selection and implementation preparation authority
  - id: behavior
    resource: ../sources/evaluate/2026-10-08-runner-behavior-receipt.json
    title: Extracted inputs, resolved rules, real lookups, and explicit controls
  - id: proposal
    resource: ../sources/evaluate/2026-10-07-runner-update-policy-candidate.md
    title: Original policy alternatives and reviewed rationale
  - id: preset
    resource: ../presets/github-actions-security.json
    title: Implementing shared preset
---

# GitHub-hosted runner update policy

**Standing: option C selected; implementation candidate awaiting publication approval and operator PR merge.**
[D015](/decisions.md#2026-10-07--d015-select-runner-approval-policy-c) records the operator's scope.[^selection]

## Rule and maintenance responsibility

Every dependency extracted as `github-runner` by the `github-actions` manager receives the
`GitHub-hosted runners` group (`github-hosted-runners`), `dependencyDashboardApproval: true`, and
`automerge: false`. The final runner-specific rule overrides the inherited group and automerge rules.
Renovate's inherited major separation may prefix the generated group and branch with `major-`.[^preset][^behavior]

Dashboard approval permits creation of a new runner branch/PR. Merge remains a separate maintainer action.
The maintainer of each affected consumer owns pending approvals and image-deprecation notices. An approval
approaching the image's first announced brownout or removal requires a migration decision or explicit
alternative before that deadline. This policy trades unattended environment changes for deliberate maintenance.

## Coverage and consumer effects

The default preset already extends this Actions preset. Consumers resolving the mutable shared reference
receive the new default on their next Renovate resolution, subject to later local rules. Deliberate consumer
rules can override it; they remain the consumer owner's responsibility. No consumer edit is part of this change.

Only eligible extracted runner versions can produce updates. `ubuntu-latest` is extracted but skipped as an
invalid version in the exercised Renovate release; its environment can still change through GitHub's alias.
Expressions and self-hosted labels produce no eligible runner update in the explicit controls. This rule
cannot freeze floating aliases or unsupported runner selectors.[^behavior]

Action digest pinning, ordinary and sensitive action rules, reusable workflows, action-input versions,
containers/services, inherited labels, and mise rules retain their prior behavior. Runner PRs deliberately
retain the inherited `github-actions` and `security` labels; categorization is not a vulnerability claim.
Action-input policy and sensitive-action coupling remain separate questions in #122.[^proposal]

## Evidence and remaining limits

Renovate 44.145.1 extraction, preset resolution, rule processing, lookup, grouping, and branch approval
processing were exercised. Personal-computing's preserved 24.04 workflow produces a real major 26.04 lookup;
the proposed runner branch returns `needs-approval` under an explicit missing-branch/no-approval fixture and
has no automerge. Non-runner behavioral configuration compares equal, apart from descriptive metadata. Repeated inheritance,
mixed major groups, global update options, and later local overrides have explicit controls.[^behavior]

Fresh personal-computing is already on 26.04, following bot-merged PR #39. Fresh Zammad-MCP uses skipped
`ubuntu-latest` values. Neither had an open Renovate PR when queried. The preserved replay does not establish
hosted execution of this policy, workflow compatibility after a future upgrade, or portfolio-wide coverage.
There is no outstanding sampled mixed PR to reconcile; consumers outside this sample remain unobserved.

The [behavior evaluation](../sources/evaluate/2026-10-08-runner-behavior-evaluation.md) maps the six verification
requirements to retained evidence and distinguishes actual observations from hypothetical/fixture controls.
Publication, consumer rollout, and operator merge acceptance require their respective evidence and authority.

## Rollback and revisit

A reviewed revert of the final runner-specific rule restores prior grouping and automerge eligibility. It
cannot undo runner versions already merged in consumers. Consumer remediation remains with their owners.
Revisit this policy if approvals approach retirement dates, backlog impedes maintenance, grouping affects
non-runners, a consumer needs an exception, or Renovate changes extraction/versioning behavior.

[^selection]: D015 records exact operator selection; it does not substitute for PR merge acceptance.
[^preset]: Shared Actions preset with the runner-specific rule placed last.
[^behavior]: Versioned runtime evidence and immutable consumer inputs, with replay and fixture limits retained.
[^proposal]: Original runner policy recommendation, alternatives, and external review reconciliation.
