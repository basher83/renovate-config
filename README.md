# Renovate Shared Configuration

Centralized Renovate presets for consistent dependency management across all repositories.

## Quick Start

**Basic projects:**

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config"
  ]
}
```

**Python projects:**

```jsonc
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/python.json"
  ]
}
```

**Docker projects:**

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

All presets are in [`presets/`](./presets/):

- **`default.json`** – Base preset (automatically included when extending `local>basher83/renovate-config`)
  - Includes: shared global behavior (e.g., best‑practices, workarounds)
  - Common settings: PR limits, semantic commits, labels, timezone, etc.

- **`python.json`** – Python project defaults (auto-merge patches + dev minor updates, groups tooling)
- **`python-mcp.json`** – MCP projects (Python 3.13 cap, MCP majors require approval, extends `python.json`)
- **`docker.json`** – Docker security (digest pinning, auto-merge digests/patches and non‑critical minors)
- **`github-actions-security.json`** – GitHub Actions security (digest pinning, selective automerge vs. approval)
- **`mise.json`** – mise dev tools (grouped updates, auto-merge; runtimes handled in stack-specific presets)
- **`ansible.json`** – Ansible collections (auto-merge patches, grouped minors)
- **`ansible-python-cap.json`** – Optional Ansible preset to cap Python <3.14.0 when managed via mise
- **`terraform-tofu.json`** – Terraform/OpenTofu providers and modules
- **`infrastructure.json`** – Comprehensive IaC preset
- **`documentation.json`** – Documentation sites (aggressive auto-merge)

> Note: `mise.json` is now included globally in `default.json` for dev tools. Runtime caps (e.g., Python <3.14.0)
> are handled in stack-specific presets like `python-mcp.json` or `ansible-python-cap.json`.

---

## Documentation

- **[Preset Management Strategy](./docs/preset-management.md)** – Guidelines for creating and organizing presets, including the automerge mental model
- **[Official Renovate Docs](./docs/offical-docs/)** – Reference documentation mirrors
- **[Configuration Examples](./examples/)** – Real-world configuration examples

---

## Base Preset Features

The base preset (`default.json`) typically provides:

- **PR Management**:
  - Limit concurrent PRs.
  - Limit creation rate (per hour) to avoid floods.
- **Semantic Commits**:
  - `chore(deps):` style commit messages.
- **Labels & Assignees**:
  - Default `renovate` label (can be extended per repo).
  - Default assignee `basher83` (can be overridden per repo).
- **Timezone**:
  - `America/New_York` for schedules.
- **Global Workarounds / Best Practices**:
  - `config:best-practices` and `workarounds:all` as a baseline.

Specific details may evolve; always check `presets/default.json` for the canonical configuration.

---

## Automerge Mental Model (Important)

Across all presets, automerge is designed to follow a simple mental model:

1. **Safe changes auto‑merge via PR**
   - Examples:
     - Patch updates for most libraries.
     - Dev/test tooling (pytest, linters, type stubs).
     - Docker & Actions digest updates.
     - Non‑critical Docker minors.
   - Configured with `automerge: true` (and usually no `automergeType` override).

2. **Risky changes require attention**
   - Examples:
     - Major library updates.
     - MCP and `zammad-py` majors.
     - Sensitive GitHub Actions minors/majors.
     - Critical Docker image minors/majors.
   - Either:
     - No `automerge` rule (PR stays open), or
     - `dependencyDashboardApproval: true` (requires explicit dashboard approval).

3. **Branch vs PR automerge**
   - `automerge: true` + `automergeType: "branch"`:
     - Updates only the Renovate branch, **does not merge the PR**.
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
**[Preset Management Strategy](./docs/preset-management.md)**.

---

## Preset Philosophy

Presets follow a simple rule:

> If it’s used universally and is safe, include it in `default.json`.  
> Otherwise, make it an **optional preset** and extend it only where needed.

- **Global presets** (in `default.json`): very conservative, universal behavior.
- **Optional presets**: technology‑ or project‑specific behavior (Python, Docker, Actions, Terraform, etc.).

See [Preset Management Strategy](./docs/preset-management.md) for detailed guidelines and the current global vs optional list.
