# Renovate Shared Configuration

Centralized Renovate presets for consistent dependency management across all repositories.

## Quick Start

**Basic projects:**

```json
{
  "extends": ["local>basher83/renovate-config"]
}
```

**Python projects:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/python.json"
  ]
}
```

**Docker projects:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/docker.json"
  ]
}
```

See [`examples/`](./examples/) for more configuration examples.

## Available Presets

All presets are in [`presets/`](./presets/):

- **`default.json`** - Base preset (automatically included when extending `local>basher83/renovate-config`)
  - Includes: `mise.json` for universal tool management
  - Common settings: PR limits, semantic commits, security alerts, labels

- **`python.json`** - Python project defaults (auto-merge patches + dev minor updates)
- **`python-mcp.json`** - MCP projects (Python 3.13 cap, extends `python.json`)
- **`docker.json`** - Docker security (digest pinning, auto-merge patches/minors)
- **`github-actions-security.json`** - GitHub Actions security (digest pinning, auto-merge)
- **`ansible.json`** - Ansible collections (auto-merge patches, grouped minors)
- **`terraform-tofu.json`** - Terraform/OpenTofu providers and modules
- **`infrastructure.json`** - Comprehensive IaC preset
- **`documentation.json`** - Documentation sites (aggressive auto-merge)

## Documentation

- **[Preset Management Strategy](./docs/preset-management.md)** - Guidelines for creating and organizing presets
- **[Official Renovate Docs](./docs/offical-docs/)** - Reference documentation
- **[Configuration Examples](./examples/)** - Real-world configuration examples

## Base Preset Features

The base preset (`default.json`) provides:

- **PR Management**: 3 concurrent, 2 hourly, not-pending creation
- **Semantic Commits**: Enabled by default
- **Security Alerts**: Auto-merge enabled with security label
- **Labels**: `renovate` (can be extended per-repo)
- **Assignees**: `basher83` (can be overridden per-repo)
- **Timezone**: `America/New_York`
- **Universal Tools**: `mise.json` included for tool version management

## Preset Philosophy

Presets follow a simple rule: **if it's used universally, include it in `default.json`; otherwise, make it optional**.

- **Global presets** (in `default.json`): `mise.json`
- **Optional presets**: Everything else - extend only when needed

See [Preset Management Strategy](./docs/preset-management.md) for detailed guidelines.
