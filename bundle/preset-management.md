---
type: Playbook
title: Preset Management Strategy
description: This guide applies the operating contract to preset changes, consumer evidence, and validation.
tags: [presets]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T19:45:48Z }
sources:
  - id: prior-guide
    resource: "https://github.com/basher83/renovate-config/blob/e06380002719988d6654aad293eee9ee295fc0d2/docs/preset-management.md"
    title: Preset guide before the focused move
  - id: local-contract
    resource: /governance.md
    title: Local operating contract
---

# Preset Management Strategy

**Standing: proposed revision of the maintained technical guide.** Prior acceptance is recorded in the
trail and decisions; this candidate adds the ownership model. This guide implements authorized outcomes;
it does not select dependency policy. Read [AGENTS.md](../AGENTS.md), the [local operating contract](/governance.md),
and the [decision record](/decisions.md). Existing JSON remains operative;
the examples and broad risk categories below do not authorize preset or consumer changes.[^local-contract]
Use [bundle document formatting](/formatting.md) for metadata and provenance style.

This document outlines the standard operating procedures (SOP) for creating and managing Renovate presets
in the shared configuration repository. It adapts the prior guide at the revision identified in
`sources`, preserving technical guidance while making execution conditional on authorization.[^prior-guide]

In addition to what presets exist and where they’re used, this document also captures the mental model
for interpreting Renovate’s automerge behavior in repositories extending the relevant presets.

---

## Core Principle: Global vs. Optional Presets

When investigating a new preset, recommend whether it should be:

1. Globally included – Extended in `default.json` for repositories inheriting the base preset
2. Optionally extended – Repositories explicitly extend it when needed

The operator selects the outcome and affected consumer scope before consequential policy implementation.
The criteria below support a recommendation; “universal” usage requires evidence about actual consumers.

### Decision Criteria

#### Include in `default.json` When

- Universal tool usage: The preset manages tools/technologies used in all or nearly all repositories.
- Low risk: The preset rules are safe to apply globally without negative side effects.
- Consistency benefit: Having consistent behavior across all repos outweighs potential edge cases.

Examples:

- Universal tooling/security behavior that truly applies everywhere
- Very conservative security presets used universally

#### Keep as Optional Preset When

- Selective usage: Only specific repositories or project types need the preset.
- High risk: The preset contains aggressive auto-merge rules or could cause issues if applied broadly.
- Project-specific: The preset is tailored to specific use cases, such as `python-mcp.json` for MCP projects.

Examples:

- `python-mcp.json` – MCP projects with MCP-specific Python caps and MCP major approval.
- `ansible.json` – Ansible projects with an Ansible-specific mise-managed Python cap.
- `terraform-tofu.json` – Infrastructure repos using Terraform/OpenTofu.
- `kubernetes.json` – Kubernetes, Helm, Kustomize, and Talhelper repos.

> Note: `mise.json` is globally included in `default.json` for mise-managed development tool updates.
> Python runtime caps are handled in stack-specific presets (`python-mcp.json`, `ansible.json`).

---

## Apply the ownership and lifecycle contract

Read [repository enforcement](/enforcement.md) before implementation. Agents author authorized preset JSON,
consumer evidence, and permitted concept changes. Repository code owns generated outputs; mise is the
interface for finalization and checks. Record the change trail in root [log.md](/log.md), and record material
policy rationale and authority in [decisions.md](/decisions.md), rather than adding a running history here.

A PR review concerns the concrete dependency-policy result and its consumer consequences. Human acceptance,
structural checks, consumer evidence, merge, and publication retain their separate meanings; operator PR merge is the
human acceptance
event for the reviewed change; it does not automatically verify every claim. Shared behavior changes require
representative consumer
evidence or the explicit exception defined by the operating contract, followed by applicable publication approval.

## Implementation Pattern

Begin this procedure only for an authorized outcome. Identify the adopted decision, affected presets and
consumer classes, allowed repository changes, and verification boundary. All snippets are examples, not
instructions to adopt their policy or representations of a consumer's resolved configuration.

### Step 1: Create the Preset

Create a focused preset file in the `presets/` directory:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Python project preset - auto-merges patches, groups linters and test tools",
  "packageRules": [
    {
      "description": "Auto-merge Python patch updates (PR merge)",
      "matchCategories": ["python"],
      "matchUpdateTypes": ["patch"],
      "automerge": true
    }
  ]
}
```

> Even for “universal” presets, keep them small and focused. It should be obvious what the preset is responsible for.

### Step 2: Add to `default.json` (if global inclusion is authorized)

If the selected outcome includes global inclusion, add the preset to `default.json` within the approved scope:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Base Renovate preset for basher83 repositories",
  "extends": [
    "config:best-practices",
    "workarounds:all",
    "local>basher83/renovate-config//presets/github-actions-security.json"
  ]
  // ... rest of config
}
```

### Step 3: Update Repository Configs (if consumer migration is authorized)

For an identified consumer, resolve inheritance and local overrides before proposing removal of an explicit
extension. Preset publication does not itself authorize consumer edits. The following is a hypothetical
example if Docker has been deliberately included in the base; it does not describe the current base preset.

Before:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/docker.json",
    "local>basher83/renovate-config//presets/python-mcp.json"
  ]
}
```

After:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/python-mcp.json"
  ]
}
```

---

## Mental Model for Automerge

A key part of our strategy is having a clear mental model for how Renovate merges changes,
and how that interacts with branch protection and required status checks.

### 1. Branch vs PR Automerge

Renovate supports two main automerge modes:

- `automerge: true` + `automergeType: "branch"`:
  - Renovate creates and updates the dependency branch without opening a PR first.
  - If checks pass and the branch is up to date, Renovate automerges it into the base branch.
  - If checks fail or stay pending too long, Renovate opens a PR as a fallback.
  - Good for:
    - Low-noise update flows where passing updates can land without PR notification noise.
    - Repos where branch protection allows Renovate to merge passing update branches.

- `automerge: true` with no `automergeType` (or `automergeType: "pr"`):
  - Renovate will:
    1. Open a PR.
    2. Wait for branch protection / status checks / conditions.
    3. Merge the PR into the base branch (usually `main`).
    4. Close the PR.
  - This produces a PR that may merge automatically when the applicable conditions are met.

Implementation convention, conditional on the selected policy:

> If the goal is PR-based automerge, use `automerge: true` and do not set `automergeType`
> (or set it to `"pr"` explicitly). Use `automergeType: "branch"` only when the repo is
> configured for branch automerge and the reduced PR noise is intentional.

### 2. What “Safe” vs “Risky” Means

The guide uses the following broad risk classification. It is a starting point for discussion, not proof
that an update is safe or authority to change shared behavior. Check the actual matched JSON rules and any
approved decision for the dependency and consumer in question.

- Safe, automerge via PR:
  - Version digests, such as Actions and Docker pinned to commits.
  - Patch updates for most libraries.
  - Minor updates for dev/test tooling, such as linters, pytest, and type stubs.
  - Docker image patch updates, and minor updates for non-critical images.
  - Terraform provider digest and patch updates, optionally off-hours.

- Risky, no automerge or require approval:
  - Major updates to application dependencies, such as Python libs, MCP SDK, and `zammad-py`.
  - Minor and major updates to security-sensitive GitHub Actions, such as `actions/checkout` and `aws-actions/*`.
  - Minor and major updates to critical Docker images, such as databases, queues, and proxies.
  - Terraform/OpenTofu provider and module majors.

An authorized policy may be encoded via:

- `automerge: true` for safe changes.
- Omitting `automerge` or adding `dependencyDashboardApproval: true` for risky changes.

### 3. Interaction with Branch Protection

Branch protection determines **when** Renovate is allowed to merge:

Inspect the identified consumer's actual protection and checks rather than infer its settings from this
guide. The examples below describe possible merge conditions; changing those settings requires task authority.

- Required status checks:
  - We normally require at least:
    - A test workflow (e.g. `test-and-coverage`).
    - Optionally a security workflow (e.g. `security-scan`).
  - Renovate will only automerge when these are green.

- Required reviews:
  - For repos where we want Renovate to auto‑merge safe updates:
    - Keep `required_approving_review_count: 0`.
    - Don’t require code owner reviews globally.
  - If we ever require reviews, Renovate automerge will be blocked unless we explicitly allow it to bypass.

Mental model:

> Presets describe which changes could be merged automatically.
> Branch protection + required checks constrain when merging is allowed; passing checks do not prove suitability.
> Renovate obeys both.

### 4. When a PR Stays Open Despite “Automerge: Enabled”

When Renovate’s PR body says:

> Automerge: Enabled.

But the PR does not close automatically, it’s usually because:

- We used `automergeType: "branch"` and expected PR-based automerge, or
- Branch protection/required checks are not satisfied, or
- The dependency falls under a rule with `dependencyDashboardApproval: true`.

When triaging such a case, check:

1. Which rule matched?
   - Do we have both a “safe” rule and a “require approval” rule that might apply?
2. Is the PR using branch-level automerge?
   - Look at the matching preset for `automergeType`.
3. Are required checks all green?
   - If a required check is failing or pending, Renovate will not merge.
4. Does the PR need Dashboard approval?
   - Major bumps for MCP, `zammad-py`, critical Docker images, etc., are intentionally blocked until approved.

---

## Benefits of This Approach

1. DRY principle: Common presets are defined once and inherited automatically.
2. Consistency: Repositories extending the relevant presets inherit shared rules, subject to local overrides.
3. Clear expectations:
   - Safe changes: auto‑merge via PR once tests/security pass.
   - Risky changes: visible PRs that require explicit approval.
4. Maintainability:
   - Update preset rules in one place; behavior can change across repositories that extend them.
5. Flexibility:
   - Per‑repo configs can:
     - Extend project‑specific presets (`python-mcp.json`, `terraform-tofu.json`, etc.).
     - Add repo‑specific `packageRules` for especially important dependencies.

---

## Current Global Presets

The following presets are included in `default.json`:

- `github-actions-security.json` – GitHub Actions security rules with digest pinning, selective automerge,
  and approval for sensitive updates.
- `mise.json` – mise-managed development tool updates, grouped and automerged.

---

## Current Optional Presets

The following presets are available but must be explicitly extended:

- `python.json` – Python project defaults
- `python-mcp.json` – MCP-specific Python rules (Python 3.13 cap including mise, MCP majors require approval)
- `docker.json` – Docker security and digest pinning
- `kubernetes.json` – Kubernetes manifests, Helm charts, Kustomize, and Talhelper updates
- `rust.json` – Rust/Cargo crate updates (ecosystem grouping, auto-merge patches, approval for critical majors)
- `terraform-tofu.json` – Terraform/OpenTofu provider/module rules
- `ansible.json` – Ansible collection/role updates (includes Python <3.14.0 cap for mise)

---

## Migration Checklist

When implementing an authorized promotion from optional to global:

- [ ] Identify the operator decision, selected policy, affected consumers, and authorized rollout scope.
- [ ] Gather evidence about consumer needs and risks; retain unverified coverage explicitly.
- [ ] Confirm that the proposed automerge behavior implements the selected outcome.
- [ ] Add preset to `default.json` `extends` array.
- [ ] Validate `default.json` configuration against the Renovate schema.
- [ ] Diagnose extraction, matching, and resolved inheritance for the behavior being claimed.
- [ ] Update identified consumer configs only where migration is authorized and redundancy is verified.
- [ ] Obtain relevant evidence from an identified representative consumer, or record an explicit operator
  exception when that evidence is unavailable; identify the gap and remaining consumer limits.
- [ ] Document the change in this file and in `README.md`.
- [ ] Record the material decision, implementation state, and actual verification limits in `decisions.md`.

Schema acceptance, matching diagnostics, and a pilot result establish different claims. See the
[contract's verification guidance](/governance.md#6-verification-and-its-limits). Publication remains a separate
action requiring approval of the concrete result.

---

## Best Practices

1. Keep presets focused: Each preset should have a single, clear purpose
   (e.g., "Python dev tooling", "Terraform providers", "Docker security").
2. Use descriptive names: Preset filenames should clearly indicate their purpose.
3. Document decisions:
   - Use JSON descriptions to explain a rule; keep material authority and rationale in the decision record.
   - Do not invent historical approval for existing `dependencyDashboardApproval` or major-update rules.
4. Gather consumer evidence before publication:
   - For shared preset behavior changes, obtain relevant extraction, matching, or resolved-configuration
     evidence from an identified representative consumer, or an explicit operator exception when unavailable.
   - Record the evidence limits or exception; publication approval does not itself supply that exception.
5. Prefer PR automerge (`automergeType: "pr"`) for safe updates:
   - Use branch automerge only when that flow is selected and the consumer's merge conditions allow it.
6. Align with branch protection:
   - Make sure required status checks match your expectations.
   - Report conflicting review requirements; do not change branch protection without authorization.
7. Review regularly:
   - Periodically review which presets should be global vs. optional.
   - Revisit “safe vs risky” classifications as projects mature or requirements change.

[^local-contract]: Adopted renovate-config operating contract; separate publication approval remains required.
[^prior-guide]: Preset-management guide at renovate-config revision e06380002719988d6654aad293eee9ee295fc0d2.

Apply the [accepted tags](/formatting.md#use-the-accepted-tag-vocabulary),
[bundle cross-links](/formatting.md#use-bundle-absolute-cross-links), and
[history conventions](/formatting.md#record-scoped-history) when documenting a preset change.
