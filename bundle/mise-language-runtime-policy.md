---
type: Policy
title: mise language runtime and tool update policy
description: This policy separates mise language runtimes from allowlisted tools, gates runtime and 0.x tool bumps, and plans a lunar-claude canary after publication.
tags: [presets]
status: draft
generated: { by: claude_agent/Composer 2.5, at: 2026-10-12T22:00:00-04:00 }
sources:
  - id: selection
    resource: /decisions.md#2026-10-13--d017-mise-runtime-tool-split-and-terraform-deptype
    title: Operator-requested preparation for #132 and terraform depType fix
  - id: replay
    resource: ../sources/evaluate/2026-10-13-d017-mise-terraform-receipt.json
    title: Renovate 44.145.1 applyPackageRules replay
  - id: survey
    resource: ../sources/evaluate/2026-10-12-d017-consumer-inventory.json
    title: Authoritative consumer inventory (2026-10-12 ET)
  - id: preset
    resource: ../presets/mise.json
    title: Implementing shared mise preset
---

# mise language runtime and tool update policy

**Standing: preparation for PR #133; publication requires operator merge approval.**[^selection]

## Rule summary

- **Language runtimes** (`python`, `node`, `go`, `ruby`, `java`, `erlang`, `elixir`, `php`, `scala`, `kotlin`,
  `deno`, `bun`, `rust`): grouped as **mise language runtimes**; minor/major require Dependency Dashboard approval
  and do not automerge; patch may automerge after **3 days** `minimumReleaseAge`.
- **Allowlisted tools** (derived from mise pins across extending consumers on 2026-10-12):[^survey] grouped as
  **mise tools**; **1.x+** patch/minor automerge after 3 days; **0.x** minor/major require approval (covers `uv`
  0.12→0.13-style bumps); majors do not automerge.[^preset]
- **Unlisted plugins** (not on the allowlist and not in the language list): **mise plugins (unspecified)** with the
  same approval gate as runtimes for minor/major so nothing silently inherits tool automerge.
- **Vulnerability alerts:** `default.json` sets `vulnerabilityAlerts.minimumReleaseAge: null` so security PRs are
  not delayed by the 3-day tool/runtime patch gate; hosted confirmation remains a canary follow-up.

## Canary plan (mise)

After merge of PR #133:

1. **Primary canary:** **`basher83/lunar-claude`** ([#84](https://github.com/basher83/lunar-claude/pull/84)
   `chore(deps): update mise tools`). It extends only the root preset (inherits global `mise.json`), pins both a
   language runtime (`python`) and a **0.x** tool (`uv`), and already has an open grouped mise PR. It is in blast
   radius; **`personal-computing` is not** (independent Renovate config since leaving the shared preset). Confirm
   split groups, dashboard approval on runtime/`uv` minors, and no silent automerge.
2. **Secondary:** **`Zammad-MCP`** ([#400](https://github.com/basher83/Zammad-MCP/pull/400) `uv` bump) — local caps
   and **uv version pins** grouping atop shared rules (replay covers caps).
3. **Terraform (preset extenders only):** **`Triangulum-Prime`** or **`Supernova-MicroK8s-Infra`** — open provider
   PRs should pick up `required_provider` rules. **`lunar-claude`** has `required_providers` in examples but does
   **not** extend `terraform-tofu.json`; the terraform fix does not apply there.

Record hosted outcomes in `bundle/decisions.md` or a follow-up evidence receipt; do not treat merge alone as proof.

## Evidence limits

The [consumer inventory](../sources/evaluate/2026-10-12-d017-consumer-inventory.json) covers **86** non-archived
`basher83/*` repos (2026-10-12 ET). Issue #132 / **personal-computing#47** remains historical context; replay in
[2026-10-13-d017-mise-terraform-receipt.json](../sources/evaluate/2026-10-13-d017-mise-terraform-receipt.json)
models that bundle but the repo no longer extends this preset. Terraform `provider` depType remains valid for
`provider` blocks; `required_provider` is the common case in `required_providers` blocks.[^replay]

[^selection]: D017 records preparation authority and scope; merge acceptance is separate.
[^survey]: Authoritative inventory captured 2026-10-12 ET; bossjones repos are out of scope for this repository.
[^preset]: Shared mise preset implementing runtime/tool split and allowlist.
[^replay]: Renovate 44.145.1 applyPackageRules replay; #47 fixture is historical regression evidence only.
