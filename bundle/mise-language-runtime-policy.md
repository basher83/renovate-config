---
type: Policy
title: mise language runtime and tool update policy
description: This policy separates mise language runtimes from allowlisted tools, gates runtime and 0.x tool bumps, and plans a personal-computing canary after publication.
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
    resource: ../sources/evaluate/2026-10-13-d017-consumer-survey.json
    title: Live default-branch consumer survey
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
- **Allowlisted tools** (derived from mise pins across extending consumers on 2026-10-13):[^survey] grouped as
  **mise tools**; **1.x+** patch/minor automerge after 3 days; **0.x** minor/major require approval (covers `uv`
  0.12→0.13-style bumps); majors do not automerge.[^preset]
- **Unlisted plugins** (not on the allowlist and not in the language list): **mise plugins (unspecified)** with the
  same approval gate as runtimes for minor/major so nothing silently inherits tool automerge.
- **Vulnerability alerts:** `default.json` sets `vulnerabilityAlerts.minimumReleaseAge: null` so security PRs are
  not delayed by the 3-day tool/runtime patch gate; hosted confirmation remains a canary follow-up.

## Canary plan (mise)

After merge of PR #133:

1. **Primary canary:** `personal-computing` (issue #132 repro). Confirm the next combined runtime/tool bump splits
   into separate groups and that Python/Node minors wait for dashboard approval while allowlisted tools follow 0.x
   vs 1.x rules.
2. **Secondary:** `Zammad-MCP` — confirm local `allowedVersions` / `uv version pins` grouping still applies atop
   shared rules (replay covers caps; hosted PR titles are the receipt).
3. **Terraform:** `Triangulum-Prime` or `Supernova-MicroK8s-Infra` — confirm open provider PRs pick up digest/patch
   automerge and Monday minor grouping once `required_provider` matches (replay only; hosted PR #111/#113 unobserved).

Record hosted outcomes in `bundle/decisions.md` or a follow-up evidence receipt; do not treat merge alone as proof.

## Evidence limits

The [consumer survey](../sources/evaluate/2026-10-13-d017-consumer-survey.json) reflects repositories visible to
the cloud-agent GitHub token (27 active). Private repos such as `personal-computing` rely on issue #132 and the
D017 replay fixture for #47. Terraform `provider` depType remains valid for `provider` blocks; `required_provider`
is the common case in `required_providers` blocks.[^replay]

[^selection]: D017 records preparation authority and scope; merge acceptance is separate.
[^survey]: Live default-branch survey captured in the evaluate receipt on 2026-10-13.
[^preset]: Shared mise preset implementing runtime/tool split and allowlist.
[^replay]: Renovate 44.145.1 applyPackageRules replay receipt for #47 and terraform depTypes.
