# Renovate Shared Configuration

Centralized Renovate presets for consistent dependency management across all repositories.

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

- [Preset Management Strategy](./docs/preset-management.md) – Guidelines for creating and organizing
  presets, including the automerge mental model
- [Official Renovate Docs](./docs/offical-docs/) – Reference documentation mirrors
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

Across all presets, automerge is designed to follow a simple mental model:

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
   - Renovate only automerges when these conditions are met.

For a deeper explanation with examples (e.g., `Zammad-MCP`), see
[Preset Management Strategy](./docs/preset-management.md).

---

## Preset Philosophy

Presets follow a simple rule:

> If it’s used universally and is safe, include it in `default.json`.
> Otherwise, make it an optional preset and extend it only where needed.

- Global presets in `default.json`: very conservative, universal behavior.
- Optional presets: technology- or project-specific behavior.

See [Preset Management Strategy](./docs/preset-management.md) for detailed guidelines and the current global vs optional list.
