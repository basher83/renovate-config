---
type: Research Question
title: What gates Renovate automerge in consumers without required checks
description: This record states the gap, competing hypotheses, and planned research before any research leg runs.
status: draft
tags: [presets]
generated: { by: claude_code/Opus 5.5, at: 2026-10-09T17:39:05Z }
---

# What gates Renovate automerge in consumers without required checks

**Standing: open question; no research leg has run.** This record states the gap and hypotheses before
research, so findings can be judged against what was expected. It establishes no policy.

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

## Exit condition

Each hypothesis is confirmed, rejected, or narrowed, with a cited source, a code reference, or a hosted
observation. Findings return through `sources/evaluate/` and a decision on whether to amend D016 or the
presets. They do not change presets on their own.
