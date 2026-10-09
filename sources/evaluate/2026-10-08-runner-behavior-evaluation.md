---
type: Evidence Evaluation
title: Runner policy implementation behavior evaluation
description: This evaluation maps option C's verification requirements to fresh consumer extraction, preserved-input lookup, and explicit behavioral controls.
tags: [governance, presets]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-07T23:57:23-04:00 }
sources:
  - id: behavior
    resource: 2026-10-08-runner-behavior-receipt.json
    title: Exact inputs, authorization, executable capture recipe, and runtime results
  - id: candidate
    resource: 2026-10-07-runner-update-policy-candidate.md
    title: Six evidence requirements and original option comparison
  - id: selection
    resource: ../../bundle/decisions.md#2026-10-07--d015-select-runner-approval-policy-c
    title: Operator selection of C and implementation preparation
  - id: implementation
    resource: ../../presets/github-actions-security.json
    title: Final runner-specific override rule
  - id: runner-source
    resource: https://github.com/renovatebot/renovate/tree/44.145.1/lib/modules/datasource/github-runners
    title: Versioned runner releases and Docker versioning
  - id: hosted-upgrade
    resource: https://github.com/basher83/personal-computing/pull/39
    title: Bot-merged runner and Actions update
---

# Runner policy implementation behavior evaluation

The operator selected **C and implementation preparation** on 2026-10-07 at 23:45:02 EDT. The receipt retains
that exact prompt and answer. Publication approval and operator PR merge acceptance are still pending.[^selection][^behavior]

## Observations that changed the candidate's context

Fresh personal-computing at `ada30901e7d298edb8e6dde761907ed20e32719f` already uses `ubuntu-26.04`.
GitHub records PR #39 as merged by `app/renovate` at 2026-10-07T23:07:17Z. This establishes a bot-merged update
under the previous shared preset; it does not establish a workflow incident or human policy acceptance.
The original 24.04 input remains addressable at `1cb3820ce59c43b4245ecede7c6484b89858ea25`.[^hosted-upgrade][^behavior]

Fresh Zammad-MCP at `f8da4342b2e81cf1c164d7fdd34863726745cee0` supplies repeated Actions-preset inheritance
and actual workflow inputs. Its `ubuntu-latest` values are extracted as `github-runner` but skipped with
`invalid-version`. The floating alias can still change outside Renovate. Expressions and self-hosted labels
produce no eligible runner update in explicit fixtures.[^behavior]

The versioned runner datasource supplies stable Ubuntu 26.04 and defaults to Docker versioning.[^runner-source]

The original four-source inputs are preserved in the
[source capture](2026-10-08-policy-source-capture.json) without newline or prose normalization. Their original
operator-provided files remain in the original checkout; the source evaluation cites the portable capture.

## Method and fidelity

Renovate **44.145.1**, Node **24.11.1**, and the exact selected consumer files are recorded with immutable Git
URLs, blob identities, content, and SHA-256 hashes. The receipt retains the before/after shared preset bytes,
all repository preset inputs, visited built-in/shared preset sets, execution time, source revision, and the
one-off capture recipe. No consumer file, branch, PR, dashboard, or bot setting was changed.[^behavior]

The recipe calls installed Renovate APIs for extraction, preset resolution, `applyPackageRules`,
`lookupUpdates`, `branchifyUpgrades`, and branch approval processing. Repository preset bodies are supplied
from the retained before/after bytes to Renovate's preset cache; built-ins resolve through Renovate itself.
The local platform prevents remote writes. The branch-approval control explicitly supplies a missing branch
and no dashboard check; it is a fixture, not a hosted app observation.

All non-runner returned configurations compare equal after removing only the intentionally differing
`packageRules` list and preset description metadata. Human-readable projections are retained, with unchanged
after projections referring to
their before projection. The executable recipe includes the complete equality assertions. Real runner lookup
updates and hypothetical non-runner update controls are labeled separately; fictitious versions and digests
are not presented as registry results.

## Verification requirements

| Candidate requirement | Retained evidence and result | Limit |
| --- | --- | --- |
| 1. Fresh scoped inputs | Two fresh default-branch revisions plus one immutable pre-upgrade replay; actual configs/workflows, preset revision/order, local rules, runtime versions, and absent Actions lockfiles recorded. | Two consumer classes, not a portfolio census or hosted app configuration capture. |
| 2. Actual extraction | 4 dependencies in each personal-computing input and 26 in Zammad-MCP; preserved Ubuntu 24.04 runner and separate mise input extracted by Renovate. | Latest runner values are skipped; unsupported-label controls are fixtures. |
| 3. Before/after rule results | 204 hypothetical update-type controls over actual extracted dependencies; real 24.04→26.04 lookup is major; separate grouping, approval true, automerge false. Global major options cannot undo C; deliberate later local rules can. | Hypothetical patch/minor/digest/pin/replacement runner cases test matching, not real OS upgrades. |
| 4. Non-runner and mixed-group controls | Full configuration equality for actual non-runners and 40 explicit fixture comparisons covering actions, reusable workflows, uses-with, containers, and services. Mixed-major fixtures show baseline mixing and C isolation for base-only and repeated inheritance. | Fixture update versions/digests are hypothetical; future upstream/consumer changes need rechecking. |
| 5. Lookup and approval disposition | Real runner lookup on preserved 24.04 offers stable 26.04; grouping produces `renovate/major-github-hosted-runners`; actual branch processor returns `needs-approval` under the explicit missing-branch fixture. Branch automerge returns `no automerge`. | Replay against today's releases, not historical registry state or a hosted run of C. Fresh 26.04 has no available update; that alone is not gating evidence. |
| Existing-group reconciliation | Fresh GitHub queries show no open Renovate PR in either sampled consumer; new mixed groups are separated in runtime controls. | No sampled live mixed PR remains to reconcile. Reconciliation in other consumers and a future hosted run remain unobserved. |
| 6. Configuration and review | Strict root/preset validation, bundle checks/lint/regressions, receipt parsing, and applicable hooks passed for the prepared revision; the exact implementation and rollback are reviewable. | Local passing checks do not grant publication or merge acceptance. |

The preserved-input read-only lookup path satisfies item 5's lookup alternative. No evidence exception is
claimed. It demonstrates the rule for an available upgrade even though that upgrade has already merged in
the fresh consumer. The candidate expressly permits retained pre-upgrade replay and distinguishes it from
hosted observation.[^candidate][^behavior]

## Implementation and release consequences

The only behavior change is the final `github-actions` / `github-runner` package rule: override both group
identity fields, require dashboard approval for all emitted runner update types, and disable automerge.
Existing manager-wide labels are deliberately retained. The major branch prefix comes from inherited
`separateMajorMinor`, rather than a second runner policy.[^implementation]

Consumers resolving the mutable shared preset can receive this default on their next run; later local
rules can override it. Each consumer maintainer owns pending approval and image-retirement dates. The current
sample needs no runner migration now. No claim is made that every consumer has resolved the new preset or
that GitHub's hosted app has executed C before publication.

A reviewed revert of this final rule restores the prior grouping and automerge eligibility; it does not undo
runner versions already merged in consumers. After publication, observe the next eligible runner update and
its dashboard/PR state when available. That is follow-up observation, not a reason to manufacture a test PR
or new policy machinery.

[^selection]: D015 records the scoped operator choice and preparation authority.
[^behavior]: Actual runtime output, immutable input captures, explicit controls, and retained one-off recipe.
[^hosted-upgrade]: Fresh GitHub PR metadata identifies the merged revision, timestamp, and bot merge actor.
[^runner-source]: Versioned upstream runner datasource; static release data includes stable Ubuntu 26.04.
[^candidate]: Original proposal's six requirements and allowance for preserved-input replay.
[^implementation]: Shared preset, with the runner-specific rule appended after inherited manager-wide rules.
