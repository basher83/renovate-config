---
type: Research Question
title: What gates Renovate automerge in consumers without required checks
description: This record states the gap, competing hypotheses, and planned research before any research leg runs.
status: draft
tags: [presets]
generated: { by: claude_code/Opus 5.5, at: 2026-10-09T17:39:05Z }
---

# What gates Renovate automerge in consumers without required checks

**Standing: research and proof legs complete; findings await operator decision.**
The hypotheses below were recorded before research ran
and are kept unchanged so the findings can be judged against them. Findings follow. This record establishes no policy.

## Gap

Every automerge rule in the shared presets assumes Renovate merges only after a consumer's CI passes. That
assumption has not been checked against how consumers are actually configured.

A survey on 2026-10-09 checked default-branch protection and rulesets for the 24 repositories that extend
this preset and contain workflows. 23 have no required status checks. Only Zammad-MCP has a ruleset that
requires `test-and-coverage` and `security-scan`. Most consumers have CI workflows, but nothing on the
GitHub side forces Renovate to wait for them.

The question came up while reviewing PR #125. D016 in that PR states that "consumers without required checks
merge on approval." That statement was written without verification, and it may be wrong.

## Why it matters

The answer decides whether automerge across the portfolio is gated by CI or effectively ungated. It covers
digest, patch, and minor automerge for Actions, mise, Python, Docker, and other presets, not just runners.
If automerge is ungated, the presets' risk classifications are the only safeguard. If it is gated by any
checks that run, branch protection is unnecessary for automerge safety, and the D016 statement needs correcting.

## Hypotheses

**H1: Renovate waits for every check that reports on the branch, regardless of branch protection.**
Merge proceeds only when all reported statuses and check runs succeed. Required checks matter to GitHub's
merge button, not to Renovate's decision. Confidence: high. The local mirror of the automerge documentation
(`docs/official-docs/key-concepts/automerge.md`, "Absence of tests") states: "By default, Renovate will not
automerge until it sees passing status checks / check runs for the branch."

**H2: A branch with no checks at all never automerges unless `ignoreTests: true` is set.** The same section
says repositories without tests need `ignoreTests: true` to automerge. Then D016's statement is backwards:
a consumer with no CI would leave an approved runner PR open instead of merging it. Confidence: medium-high.
The mirror text supports it, but the mirror was last updated on 2026-06-27 and has not been checked against
current documentation or Renovate 44.145.1 source.

**H3: Renovate counts only some checks (for example, it ignores pending or skipped checks, or workflows that
do not run on Renovate branches).** If so, a consumer whose CI does not trigger on Renovate branches behaves
like H2, and a consumer with path-filtered workflows may merge without its relevant checks. Confidence:
unknown. This is the case most likely to differ from the documentation's simple wording.

Rejected framing: "Branch protection is what makes automerge safe." It is plausible under the GitHub merge
model but contradicts the documented Renovate behavior; it is kept only as the null result of H1.

## Planned research leg

1. Compare `docs/official-docs/key-concepts/automerge.md` and the `ignoreTests` option against current
   upstream documentation. Record whether the mirror is stale.
2. Read Renovate 44.145.1 source for the GitHub branch-status calculation and the automerge decision. Record
   how no checks, pending checks, skipped checks, and failing non-required checks are treated.
3. Observe one hosted run: a canary workflow in Zammad-MCP pinned to `runs-on: ubuntu-24.04`, after PR #125
   merges, with dashboard approval and an observed merge or wait. This also closes D016's unobserved hosted
   automerge limit. Adding the canary is a consumer edit and needs separate operator approval.
4. Classify the 24 workflow-bearing consumers by whether their CI runs on Renovate branches.

## Affected assertions

- D016 evidence entry in PR #125: "Consumers without required checks merge on approval."
- PR #125 description, "Verification and rollback" section: the same claim.
- Any future preset decision that treats automerge as CI-gated.

## Findings from the research leg

The leg ran on 2026-10-09 against Renovate 44.145.1 source (the version pinned in the existing receipts),
upstream documentation on the `main` branch, and consumer workflows on their default branches.

**H1 is confirmed for Renovate's own automerge.** `resolveBranchStatus` in
`workers/repository/update/branch/status-checks.js` asks the platform for branch status, and the GitHub
`getBranchStatus` in `modules/platform/github/index.js` combines every commit status and every check run on the
branch head. It ignores branch protection entirely. Any failure returns red. The branch is green only when the
combined status is success, or there are no statuses, and every check run concluded `success`, `neutral`, or
`skipped`. Anything still running returns yellow, and the PR automerge path refuses to merge unless the status is
green. Successful `renovate/*` statuses do not count, so Renovate cannot satisfy its own gate.

**H2 is confirmed.** With no check runs, the result depends only on the combined commit status. GitHub reports
`pending` when a commit has no statuses, which maps to yellow, so Renovate never merges a branch that has no
checks. `ignoreTests: true` bypasses this by returning green before checking anything. No preset in this
repository sets `ignoreTests` or `internalChecksAsSuccess`. D016's original wording, "consumers without required
checks merge on approval," was wrong: a consumer with no checks leaves the PR open.

**H3 is narrowed, not confirmed.** Checks that never start are invisible to Renovate. If only some workflows
trigger, Renovate gates on those alone. Skipped and neutral check runs count as passing. Classifying the
24 workflow-bearing consumers by trigger gave:

- 18 have at least one workflow that runs on pull requests to `main` without path filters, so a Renovate PR
  always gets checks.
- `docs`, `forgeflare`, `forgeflare-hooks`, and `tailnet-microservices` rely only on path-filtered workflows.
  The filters cover the files Renovate usually edits (YAML, JSON, TOML, `mise.toml`, `k8s/**`). The forgeflare
  pair and `tailnet-microservices` exclude `renovate.json`, so a Renovate change touching only that file gets no
  checks from them.
- `.github` and `Proxmox-OpenAPI` have no workflow that runs on pull requests; Proxmox-OpenAPI's workflows run on
  tags, schedules, and manual dispatch. Under H2, Renovate never automerges in either unless another app reports
  a status.

This classification parses `on:` triggers only. It does not account for third-party apps such as CodeRabbit that
post their own statuses or check runs. Those count toward Renovate's gate and could turn a check-less branch green.

**New finding, not anticipated by the hypotheses: GitHub-native auto-merge runs in parallel.** `platformAutomerge`
defaults to `true`. When a repository allows auto-merge (`allow_auto_merge` is true for Zammad-MCP, the-range,
personal-computing, and lunar-claude), Renovate enables GitHub's auto-merge when it creates the PR. GitHub then
merges once branch protection requirements are met, and only required checks count there. In Zammad-MCP, GitHub
could merge after `test-and-coverage` and `security-scan` pass while other checks are still running. In the
23 consumers without required checks, it is not known from source whether GitHub accepts the auto-merge request or
merges immediately. GitHub generally refuses auto-merge on a PR that can already merge, and Renovate logs the
error at debug level and falls back to its own gate. That expectation is unverified.

**The local documentation mirror is current on this point.** Upstream `docs/usage/key-concepts/automerge.md`
keeps the "Absence of tests" wording unchanged. The mirror is missing newer merge-queue and GitLab merge-train
sections, which do not affect this question.

## What the proof leg must observe

The Zammad-MCP canary should answer two questions. First, whether GitHub-native auto-merge merges the approved
runner PR when the two required checks pass, before other checks finish. Second, whether Renovate's own gate holds
the PR while any check is still running. A second observation in a consumer without required checks, such as
`the-range`, would settle whether GitHub-native auto-merge merges immediately there. Both are consumer edits that
need operator approval.

## Proof leg observations

**First canary run (Zammad-MCP #394, 2026-10-09).** After dashboard approval, Renovate created the runner PR at
18:04:49 UTC and enabled GitHub-native auto-merge (squash) at 18:04:52. Every check passed between 18:04:56 and
18:06:46. The last was the required `test-and-coverage`, and the PR merged at 18:07:33 with `renovate[bot]` as the
actor. This run confirms three things in hosted operation: dashboard approval holds the PR, an approved runner PR
automerges, and Renovate enables GitHub-native auto-merge. It does not settle which path merged, because a
required check finished last and GitHub credits an auto-merge to the account that enabled it. Zammad-MCP #395 makes
the canary wait five minutes on Renovate branches, so a later automerge PR can separate the two paths. The
timeline is in [Zammad-MCP #392](https://github.com/basher83/Zammad-MCP/issues/392#issuecomment-6086628395).

**Second canary run settles the merge path (Zammad-MCP #396, 2026-10-09).** With the canary delayed five minutes on
Renovate branches, a Docker digest PR was created at 18:22:00 UTC and GitHub-native auto-merge was enabled at 18:22:03.
The required `security-scan` and `test-and-coverage` checks passed at 18:22:35 and 18:23:52, and the PR merged at
18:24:03 while the non-required `runner-canary` was still running. Renovate's own gate waits for every check run,
so GitHub-native auto-merge made this merge. In a consumer with required checks and "Allow auto-merge" enabled,
merges are gated by required checks only. Non-required checks can still be running, or can fail, after the merge.
This supersedes the H1 framing for such consumers: H1 describes Renovate's gate, but GitHub's gate acts first.
The observation is in [Zammad-MCP #392](https://github.com/basher83/Zammad-MCP/issues/392).

**Third-party apps supply the checks that H2 assumed were missing.** The operator confirmed CodeRabbit is installed
on every repository. On Renovate PRs it posts a `success` commit status to say it skipped a bot PR. GitGuardian
posts a check run, and Codacy and CodeQL default setup do the same where enabled. Renovate's gate counts all of these.
The last eight merged Renovate PRs in each consumer without pull-request workflows show the effect:

- `.github` #91 to #98 automerged with only `GitGuardian Security Checks` and the CodeRabbit status. These were
  mise tool, uv, prek, Action version, and digest updates.
- `Proxmox-OpenAPI` #112 to #125 automerged reusable-workflow digest updates with only GitGuardian, Codacy,
  CodeQL, and the CodeRabbit status.

So H2 holds in Renovate's code but not in practice for these consumers. A branch is never check-less, and these
repositories automerge with no functional CI. Every automerge rule in the presets is effectively ungated there.
Each merge came hours after PR creation, not seconds. That fits Renovate merging on a later scheduled run rather
than GitHub-native auto-merge, which would merge almost at once in a repository with no branch protection. It does
not establish that GitHub refused the auto-merge request.

## Exit condition

Each hypothesis is confirmed, rejected, or narrowed, with a cited source, a code reference, or a hosted
observation. Findings return through `sources/evaluate/` and a decision on whether to amend D016 or the
presets. They do not change presets on their own.
