# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Renovate Shared Configuration

This repository provides centralized Renovate presets for consistent dependency management across all projects.

### Preset Architecture

**Base Preset (`default.json`)**:

- Referenced as `local>basher83/renovate-config`
- Provides common settings: PR limits (3 concurrent, 2 hourly), semantic commits, security alerts with auto-merge
- Standard labels: dependencies, renovate
- Assignee: basher83
- Timezone: America/New_York (EST)
- Includes workarounds:all for known package issues

**Specialized Presets**:

1. **`docker.json`** - Docker/container workflows
   - Pin Docker digests and GitHub Actions
   - Auto-merge Docker patches and digest updates
   - Detect abandoned packages
   - Reference: `local>basher83/renovate-config:docker`

2. **`infrastructure.json`** - Terraform/Ansible/IaC projects
   - Auto-merge: Terraform patches, Ansible patches/minor, GitHub Actions patches/minor
   - Custom managers for mise, Packer, Ansible Galaxy
   - Group related dependencies (Ansible collections, GitHub Actions)
   - Monday early morning schedule
   - Reference: `local>basher83/renovate-config:infrastructure`

3. **`python.json`** - Python projects
   - Group pytest packages and linters (black, ruff, mypy)
   - Auto-merge: Production patches, dev dependency patches/minor
   - Custom commit prefix for dev deps: `chore(dev-deps):`
   - Reference: `local>basher83/renovate-config:python`

4. **`python-mcp.json`** - Python MCP projects
   - Extends python.json with Python 3.14 blocking (MCP SDK incompatibility)
   - Approval required for major MCP/zammad-py updates
   - Pin GitHub Actions digests
   - Reference: `local>basher83/renovate-config:python-mcp`

5. **`documentation.json`** - Documentation sites (MkDocs, Docusaurus, Sphinx)
   - Aggressive auto-merge: patches, minor, security
   - Platform automerge enabled
   - Higher PR limit (5 concurrent)
   - Monday before 6am schedule
   - Reference: `local>basher83/renovate-config:documentation`
   - Note: Custom commit emoji (like ⬆️) should be set at repo level

6. **`github-actions-security.json`** - GitHub Actions hardening
   - Pin Actions to commit SHA
   - Auto-merge: digest updates, patches, minor
   - Group all Actions together
   - Reference: `local>basher83/renovate-config:github-actions-security`

### Usage Examples

**Basic projects:**

```json
{
  "extends": ["local>basher83/renovate-config"]
}
```

**Docker projects:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config:docker"
  ]
}
```

**Infrastructure projects:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config:infrastructure"
  ]
}
```

**Python projects:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config:python"
  ]
}
```

**Python MCP projects:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config:python-mcp",
    "local>basher83/renovate-config:github-actions-security"
  ]
}
```

**Multi-stack projects:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config:infrastructure",
    "local>basher83/renovate-config:python",
    "local>basher83/renovate-config:github-actions-security"
  ],
  "packageRules": [
    // Repository-specific overrides
  ]
}
```

### Validation

```bash
# Validate all preset files in this repository
for file in *.json; do
  echo "Validating $file"
  npx --yes --package renovate -- renovate-config-validator "$file"
done

# Validate a consumer's renovate.json that uses these presets
npx --yes --package renovate -- renovate-config-validator renovate.json
```
