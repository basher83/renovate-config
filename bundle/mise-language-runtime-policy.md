---
type: Policy
title: mise language runtime and tool update policy
description: This policy separates mise language runtimes from allowlisted tools, gates runtime and 0.x tool bumps, and plans a lunar-claude canary after publication.
tags: [presets]
status: draft
generated: { by: claude_agent/Opus 5.5, at: 2026-10-13T11:51:31-04:00 }
sources:
  - id: selection
    resource: /decisions.md#2026-10-13--d017-mise-runtimetool-split-and-terraform-required_provider-matching
    title: D017 preparation for #132 and the terraform depType fix, pending operator selection
  - id: replay
    resource: ../sources/evaluate/2026-10-13-d017-mise-terraform-receipt.json
    title: Renovate 44.145.1 package-rule and branch-grouping replay
  - id: survey
    resource: ../sources/evaluate/2026-10-12-d017-consumer-inventory.json
    title: Authoritative consumer inventory (2026-10-12 ET)
  - id: preset
    resource: ../presets/mise.json
    title: Implementing shared mise preset
---

# mise language runtime and tool update policy

**Standing: preparation for PR #133; operator merge is the selection and acceptance event.**[^selection]

## Rule summary

- **Language runtimes** (`python`, `node`, `go`, `ruby`, `java`, `erlang`, `elixir`, `php`, `scala`, `kotlin`,
  `deno`, `bun`, `rust`): patches are grouped as **mise language runtimes** and may automerge after a **3 day**
  `minimumReleaseAge`. Minor/major updates require Dependency Dashboard approval, do not automerge, and are
  grouped separately as **mise language runtimes (approval)**.
- **Allowlisted tools** (every tool pinned by an extending consumer on 2026-10-12):[^survey] **1.x+** patch/minor
  updates and **0.x** patches are grouped as **mise tools** and automerge after 3 days. **0.x** minor/major
  updates (such as `uv` 0.12 to 0.13) require approval and are grouped separately as **mise tools (approval)**.
  Majors do not automerge.[^preset]
- **Separate approval groups:** Renovate requires approval for a whole branch when any grouped update needs it,
  and automerges a branch only when every grouped update does. A shared group would therefore hold automergeable
  patches behind one gated update; the replay shows each update keeping its own result after grouping.[^replay]
- **Unlisted plugins** (on neither list): minor/major updates require approval in **mise plugins (unspecified)**.
  Their patches are neither grouped nor automerged, so each opens its own PR for manual merge.
- **Vulnerability alerts:** Renovate's default `vulnerabilityAlerts.minimumReleaseAge` is already `null`;
  `default.json` restates it, so alert PRs bypass the 3-day gate. Hosted confirmation remains a canary follow-up.

## Canary plan (mise)

After merge of PR #133:

1. **Primary canary:** **`basher83/lunar-claude`** ([#84](https://github.com/basher83/lunar-claude/pull/84)
   `chore(deps): update mise tools`). It extends only the root preset (inherits global `mise.json`), pins both a
   language runtime (`python`) and **0.x** tools (`uv`, `ruff`), and already has an open grouped mise PR. It is in
   blast radius; **`personal-computing` is not** (independent Renovate config since leaving the shared preset).
   Confirm separate runtime, tool, and approval branches; dashboard approval on runtime and 0.x tool minors; and
   automerge of the remaining tool updates after three days.
2. **Secondary:** **`Zammad-MCP`** ([#400](https://github.com/basher83/Zammad-MCP/pull/400) `uv` bump): local caps
   and **uv version pins** grouping on top of the shared rules (replay covers caps and the local group).
3. **Terraform (preset extenders only):** **`Triangulum-Prime`** or **`Supernova-MicroK8s-Infra`**: their two open
   provider minors should merge into one Monday `Terraform Providers (Minor)` branch per repository, as replayed.
   **`lunar-claude`** has `required_providers` in examples but does **not** extend `terraform-tofu.json`; the
   terraform fix does not apply there.

Record hosted outcomes in `bundle/decisions.md` or a follow-up evidence receipt; do not treat merge alone as proof.

## Evidence limits

The [consumer inventory](../sources/evaluate/2026-10-12-d017-consumer-inventory.json) covers **86** non-archived
`basher83/*` repos (2026-10-12 ET). Issue #132 / **personal-computing#47** remains historical context; replay in
[2026-10-13-d017-mise-terraform-receipt.json](../sources/evaluate/2026-10-13-d017-mise-terraform-receipt.json)
models that bundle, but the repo no longer extends this preset. Its branch replay uses inventory pins from
`prompting-eval-workbench` and `lunar-claude` with hypothetical update targets; it does not run lookup or the
dashboard. Its Terraform replay uses the open provider PRs on `Triangulum-Prime` and `Supernova-MicroK8s-Infra`
at their inventory revisions; the base-preset run reproduces their live branch names. Terraform `provider` depType
remains valid for `provider` blocks; `required_provider` is the common case in `required_providers` blocks.[^replay]

[^selection]: D017 records preparation scope; operator merge is the selection and acceptance event.
[^survey]: Authoritative inventory captured 2026-10-12 ET; bossjones repos are out of scope for this repository.
[^preset]: Shared mise preset implementing runtime/tool split, approval groups, and allowlist.
[^replay]: Renovate 44.145.1 package-rule and branch-grouping replay; #47 fixture is historical regression evidence only.
