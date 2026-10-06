# Renovate Shared Configuration

Centralized Renovate presets for consistent dependency management in repositories extending these presets.
Shared changes affect those consumers, subject to inheritance and local overrides; this repository does not
establish that every owned repository has been inventoried or extends the base.

The [local operating contract](./bundle/governance.md) and
[prospective decision record](./bundle/decisions.md) define the adopted local authority and verification boundaries.
**Slice 1 is adopted locally.** The operator accepted candidate `33e5e1f29df4` on 2026-10-06;
[decision D005](./bundle/decisions.md#2026-10-06--d005-adopt-slice-1-locally) records its scope. Commit and publication
remain separate. Existing JSON remains operative, shared adoption remains unresolved, and issue #122 stays paused.

## Quick Start

Basic projects:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config"
  ]
}
```

Python projects:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/python.json"
  ]
}
```

Docker projects:

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/docker.json"
  ]
}
```

See [`examples/`](./examples/) for more configuration examples.

---

## Available Presets

The base preset is `default.json`, which is automatically included when extending
`local>basher83/renovate-config`. It provides shared behavior such as best practices,
workarounds, PR limits, semantic commits, labels, timezone, and the global presets.

Global presets included by `default.json`:

- `github-actions-security.json` – GitHub Actions security rules with digest pinning,
  selective automerge, and approval for sensitive updates.
- `mise.json` – mise-managed development tool updates, grouped and automerged.

Optional presets in [`presets/`](./presets/) are extended per project:

- `ansible.json` – Ansible collection and role updates, including the mise-managed Python
  `<3.14.0` cap for Ansible compatibility.
- `docker.json` – Docker security, digest pinning, safe automerge, and approval for
  higher-risk image updates.
- `kubernetes.json` – Kubernetes manifests, Helm charts, Kustomize, and Talhelper updates.
- `python.json` – Python project defaults with patch automerge and grouped tooling updates.
- `python-mcp.json` – MCP projects with Python runtime caps and MCP major approval, extending
  `python.json`.
- `rust.json` – Rust/Cargo crate updates, ecosystem grouping, and approval for critical majors.
- `terraform-tofu.json` – Terraform/OpenTofu provider and module updates.

Python runtime caps are intentionally stack-specific and live in `python-mcp.json` and
`ansible.json`, not in the global `mise.json` preset.

---

## Documentation

- [Repository Knowledge](./bundle/index.md) – Local guidance and captured references
- [Bundle Document Formatting](./bundle/formatting.md) – Local OKF frontmatter and provenance style
- [Preset Management Strategy](./bundle/preset-management.md) – Guidelines for creating and organizing
  presets, including the automerge mental model
- [Official Renovate Docs](./docs/official-docs/) – Reference documentation mirrors
- [Configuration Examples](./examples/) – Real-world configuration examples

---

## Base Preset Features

The base preset (`default.json`) typically provides:

- PR management:
  - Limit concurrent PRs.
  - Limit creation rate (per hour) to avoid floods.
- Semantic commits:
  - `chore(deps):` style commit messages.
- Labels and assignees:
  - Default `renovate` label (can be extended per repo).
  - Default assignee `basher83` (can be overridden per repo).
- Timezone:
  - `America/New_York` for schedules.
- Global workarounds and best practices:
  - `config:best-practices` and `workarounds:all` as a baseline.

Specific details may evolve; always check `default.json` for the canonical configuration.

---

## Automerge Mental Model (Important)

The categories below summarize the guide's automerge model. They are not permission to select a new policy
or proof of safety. Consult matched JSON rules and any applicable decision for the actual dependency and consumer:

1. Safe changes auto‑merge via PR
   - Examples:
     - Patch updates for most libraries.
     - Dev/test tooling (pytest, linters, type stubs).
     - Docker & Actions digest updates.
     - Non‑critical Docker minors.
   - Configured with `automerge: true` (and usually no `automergeType` override).

2. Risky changes require attention
   - Examples:
     - Major library updates.
     - MCP and `zammad-py` majors.
     - Sensitive GitHub Actions minors/majors.
     - Critical Docker image minors/majors.
   - Either:
     - No `automerge` rule (PR stays open), or
     - `dependencyDashboardApproval: true` (requires explicit dashboard approval).

3. Branch vs PR automerge
   - `automerge: true` + `automergeType: "branch"`:
     - Creates a Renovate branch first; if checks pass, Renovate automerges it into the base branch.
     - We avoid this for “invisible” maintenance flows.
   - `automerge: true` with default `automergeType` (PR):
     - PR is merged into the base branch when checks pass.
     - PR closes → ideal for “no visible PR” safe updates.

4. **Branch protection + required checks are the gate**
   - We rely on:
     - Required status checks (e.g. tests + security scans).
     - No required approvals where we want Renovate to auto‑merge.
   - Inspect the consumer's actual requirements; passing checks establish only what those checks verify.
   - Merge conditions do not establish policy approval or that an update is suitable.

For a deeper explanation with examples (e.g., `Zammad-MCP`), see
[Preset Management Strategy](./bundle/preset-management.md).

---

## Preset Philosophy

For a new preset, consider this starting point for an operator-reviewed recommendation:

> Recommend global inclusion when evidence supports broad consumer applicability and acceptable risk.
> Recommend optional inclusion for stack-specific needs. Implement only the authorized outcome.

- Global presets in `default.json`: very conservative, universal behavior.
- Optional presets: technology- or project-specific behavior.

See [Preset Management Strategy](./bundle/preset-management.md) for detailed guidelines and the current global vs optional list.
