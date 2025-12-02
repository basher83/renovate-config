---
title: Preset Management Strategy
description: Guidelines for creating and organizing Renovate presets in the shared configuration repository
---

# Preset Management Strategy

This document outlines the standard operating procedures (SOP) for creating and managing Renovate presets
in the shared configuration repository.

In addition to *what* presets exist and *where* they’re used, this document also captures the **mental model**
for how we use Renovate’s automerge behavior across all repos.

---

## Core Principle: Global vs. Optional Presets

When creating a new preset, determine whether it should be:

1. **Globally included** – Extended in `default.json` for all repositories
2. **Optionally extended** – Repositories explicitly extend it when needed

### Decision Criteria

#### Include in `default.json` When

- **Universal tool usage**: The preset manages tools/technologies used in **all or nearly all** repositories
- **Low risk**: The preset rules are safe to apply globally without negative side effects
- **Consistency benefit**: Having consistent behavior across all repos outweighs potential edge cases

**Examples:**

- Universal tooling/security behavior that truly applies everywhere
- Very conservative security presets used universally

#### Keep as Optional Preset When

- **Selective usage**: Only specific repositories or project types need the preset
- **High risk**: The preset contains aggressive auto-merge rules or could cause issues if applied broadly
- **Project-specific**: The preset is tailored to specific use cases (e.g., `python-mcp.json` for MCP projects)

**Examples:**

- `python-mcp.json` – Only MCP projects should cap Python to 3.13
- `terraform-tofu.json` – Only infrastructure repos using Terraform/OpenTofu
- `documentation.json` – Only docs sites that can tolerate aggressive auto-merge

> Note: Historically, `mise.json` was treated as a global preset. Renovate now has first-class support for
> updating `mise` directly, so we plan to **remove** this preset from `default.json` and rely on Renovate’s
> built-in behavior instead.

---

## Implementation Pattern

### Step 1: Create the Preset

Create a focused preset file in the `presets/` directory:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Universal mise tooling preset - conservative updates for all tool versions",
  "packageRules": [
    {
      "description": "Auto-update utility tools (patch and minor)",
      "matchManagers": ["mise"],
      "matchUpdateTypes": ["patch", "minor"],
      "automerge": true
    }
  ]
}
```

> Even for “universal” presets, keep them **small and focused**. It should be obvious what the preset is responsible for.

### Step 2: Add to `default.json` (if globally applicable)

If the preset should apply to all repositories, add it to `default.json`:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Base Renovate preset for basher83 repositories",
  "extends": [
    "config:best-practices",
    "workarounds:all",
    "local>basher83/renovate-config//presets/mise.json"
  ]
  // ... rest of config
}
```

### Step 3: Update Repository Configs (if globally included)

Repositories that were previously extending the preset explicitly can now remove it:

**Before:**

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/mise.json",
    "local>basher83/renovate-config//presets/python-mcp.json"
  ]
}
```

**After:**

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

A key part of our strategy is having a clear mental model for **how** Renovate merges changes,
and how that interacts with branch protection and required status checks.

### 1. Branch vs PR Automerge

Renovate supports two main automerge modes:

- `automerge: true` + **`automergeType: "branch"`**:
  - Renovate updates the **dependency branch only** (e.g. `renovate/some-dep`).
  - It will keep pushing new commits to that branch.
  - **It does not merge the PR into the base branch** and the PR typically stays open.
  - Good for:
    - Long‑running branches where you want a “rolling” update branch.
    - Cases where humans always decide when to merge.

- `automerge: true` with **no `automergeType`** (or `automergeType: "pr"`):
  - Renovate will:
    1. Open a PR.
    2. Wait for branch protection / status checks / conditions.
    3. **Merge the PR into the base branch** (usually `main`).
    4. Close the PR.
  - This is what we use for the “no visible PR; updates land in `main` automatically” behavior.

**House rule:**

> If the goal is that safe updates “just land in `main`” and PRs disappear,  
> use `automerge: true` and **do not** set `automergeType` (or set it to `"pr"` explicitly).  
> Avoid `automergeType: "branch"` unless you explicitly want long-lived PRs.

### 2. What “Safe” vs “Risky” Means

Across presets, we follow this general classification:

- **Safe (automerge via PR)**:
  - Version **digests** (e.g. Actions and Docker pinned to commits).
  - **Patch** updates for most libraries.
  - **Minor** updates for dev/test tooling (linters, pytest, type stubs, etc.).
  - Docker image **patch** updates, and **minor** updates for non-critical images.
  - Terraform provider **digest/patch** (optionally off‑hours).

- **Risky (no automerge or require approval)**:
  - **Major** updates to application dependencies (Python libs, MCP SDK, `zammad-py`, etc.).
  - **Minor/Major** updates to security‑sensitive GitHub Actions (e.g. `actions/checkout`, `aws-actions/*`).
  - **Minor/Major** updates to critical Docker images (databases, queues, proxies).
  - Terraform/OpenTofu provider and module **majors**.

We encode this via:

- **`automerge: true`** for safe changes.
- **Omitting `automerge`** or adding **`dependencyDashboardApproval: true`** for risky changes.

### 3. Interaction with Branch Protection

Branch protection determines **when** Renovate is allowed to merge:

- **Required status checks**:
  - We normally require at least:
    - A test workflow (e.g. `test-and-coverage`).
    - Optionally a security workflow (e.g. `security-scan`).
  - Renovate will only automerge when these are green.

- **Required reviews**:
  - For repos where we want Renovate to auto‑merge safe updates:
    - Keep `required_approving_review_count: 0`.
    - Don’t require code owner reviews globally.
  - If we ever require reviews, Renovate automerge will be blocked unless we explicitly allow it to bypass.

**Mental model:**

> Presets describe which changes **could** be merged automatically.  
> Branch protection + required checks describe when they are **actually safe** to merge.  
> Renovate obeys both.

### 4. When a PR Stays Open Despite “Automerge: Enabled”

When Renovate’s PR body says:

> **Automerge**: Enabled.

But the PR does not close automatically, it’s usually because:

- We used `automergeType: "branch"` (branch-only updates, no PR merge), or
- Branch protection/required checks are not satisfied, or
- The dependency falls under a rule with `dependencyDashboardApproval: true`.

When triaging such a case, check:

1. **Which rule matched?**
   - Do we have both a “safe” rule and a “require approval” rule that might apply?
2. **Is the PR using branch‑level automerge?**
   - Look at the matching preset for `automergeType`.
3. **Are required checks all green?**
   - If a required check is failing or pending, Renovate will not merge.
4. **Does the PR need Dashboard approval?**
   - Major bumps for MCP, `zammad-py`, critical Docker images, etc., are intentionally blocked until approved.

---

## Benefits of This Approach

1. **DRY Principle**: Common presets are defined once and inherited automatically.
2. **Consistency**: All repositories get a consistent “safe vs risky” behavior for dependencies.
3. **Clear Expectations**:
   - Safe changes: auto‑merge via PR once tests/security pass.
   - Risky changes: visible PRs that require explicit approval.
4. **Maintainability**:
   - Update preset rules in one place; behavior changes across all repos that extend them.
5. **Flexibility**:
   - Per‑repo configs can:
     - Extend project‑specific presets (`python-mcp.json`, `terraform-tofu.json`, etc.).
     - Add repo‑specific `packageRules` for especially important dependencies.

---

## Current Global Presets

The following presets are included in `default.json`:

- *(Subject to change as Renovate gains more built‑in capabilities, e.g. for `mise`.)*

> TODO: As part of the `mise.json` deprecation, update this section once `mise.json`
> has been removed from `default.json`.

---

## Current Optional Presets

The following presets are available but must be explicitly extended:

- `python.json` – Python project defaults
- `python-mcp.json` – MCP-specific Python rules (Python 3.13 cap, MCP majors require approval)
- `docker.json` – Docker security and digest pinning
- `github-actions-security.json` – GitHub Actions security rules (digest pinning & selective automerge)
- `terraform-tofu.json` – Terraform/OpenTofu provider/module rules
- `ansible.json` – Ansible collection/role updates
- `infrastructure.json` – Infrastructure-as-Code comprehensive preset
- `documentation.json` – Documentation site aggressive auto-merge

---

## Migration Checklist

When promoting a preset from optional to global:

- [ ] Verify the preset is **safe** to apply globally.
- [ ] Confirm all or nearly all repos would benefit.
- [ ] Ensure the automerge behavior (if any) is consistent with our “safe vs risky” model.
- [ ] Add preset to `default.json` `extends` array.
- [ ] Validate `default.json` configuration against the Renovate schema.
- [ ] Update repository configs to remove explicit preset extension (if now redundant).
- [ ] Test in a sample repository to ensure behavior is correct.
- [ ] Document the change in this file and in `README.md`.

---

## Best Practices

1. **Keep presets focused**: Each preset should have a single, clear purpose (e.g., “Python dev tooling”, “Terraform providers”, “Docker security”).
2. **Use descriptive names**: Preset filenames should clearly indicate their purpose.
3. **Document decisions**:
   - Add comments or descriptions explaining why certain rules exist.
   - Especially for `dependencyDashboardApproval` and majors.
4. **Test before globalizing**:
   - Always test preset changes in at least one repo before adding them to `default.json`.
5. **Prefer PR automerge (`automergeType: "pr"`) for safe updates**:
   - Reserve `automergeType: "branch"` for rare cases where you explicitly want a long‑lived PR.
6. **Align with branch protection**:
   - Make sure required status checks match your expectations.
   - Don’t accidentally require reviews if you want Renovate to auto‑merge safe changes.
7. **Review regularly**:
   - Periodically review which presets should be global vs. optional.
   - Revisit “safe vs risky” classifications as projects mature or requirements change.
