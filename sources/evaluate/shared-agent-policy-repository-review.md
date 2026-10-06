---
type: Reference
title: Shared agent policy repository review
description: Verbatim capture of the cross-repository governance review used to reconcile the local candidate.
tags: [renovate, governance, review]
status: draft
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T07:35:02Z }
---

# Shared Agent Policy: Repository Review for basher83

Review date: 2026-10-06. Scope: the 92 repositories under the `basher83` GitHub account that the connected token can list (34 public, 58 private), and the local workspace containing the attached `sources` directory (`~/3I/lab/renovate-config/sources`). Read-only: nothing was modified on GitHub or on the Mac.

Each claim is labelled Observed (seen directly in a file, API response, or history) or Inferred (my reasoning from observations). The per-repository inventory is in the companion file `basher83-repo-inventory.csv`.

## Method and coverage limits

| Surface | What was done | Limit |
|---|---|---|
| Repository list and metadata | `gh repo list`, contributors, every PR and issue (up to 500 PRs and 300 issues per repo), branch rules | No GitHub organizations; one collaborator repo (`EdBHall/claude-sharedrive`) is out of scope |
| Repository content | Full file trees for all 92; shallow clones (50 commits per branch) of 87; text search across them | History deeper than 50 commits was read only through the API (last non-bot commit on `main`) |
| Local workspace | Read `~/3I/lab/AGENTS.md`, `~/3I/DOMAINS.md`, `~/3I/lab/LAB.md`, `QUEUE.md`, the global `~/.claude/CLAUDE.md` and `~/.pi/agent/AGENTS.md`, and git remotes of the lab checkouts | Forge, workshop, and research domain files were listed, not read |
| Not accessible | Scalr workspace settings, Argo CD live state, Infisical, the content of Entire checkpoints beyond confirming their structure, Renovate's hosted app settings | Claims about these are stated as gaps |

Access anomaly (observed): four local checkouts point to `basher83` remotes that return 404 to the connected token: `Hercules-Vault-Infra`, `dockervm-traefik`, `mothership-compose`, `triangulum-observe`. Each has a tracking `origin/main`, so the repositories existed at some point. I cannot tell whether they were deleted, renamed, or are outside the token's scope. They are excluded from the inventory.

`pushedAt` does not indicate activity here. Renovate pushes to about 40 repositories almost daily. For example, [Triangulum-Prime](https://github.com/basher83/Triangulum-Prime) was pushed on 2026-10-06, but its last human commit on `main` was 2026-04-30. Status in the inventory is therefore based on the last non-bot commit on `main`. That under-counts work that lives only on branches.

## Review A: Inventory

### Repository classes

| Class (count) | Status mix | Representative repositories | Traits relevant to a policy |
|---|---|---|---|
| Shared config and guidance hubs (8) | 2 active, 4 recent, 2 dormant | [renovate-config](https://github.com/basher83/renovate-config), [.github](https://github.com/basher83/.github), [pi-dev-config](https://github.com/basher83/pi-dev-config), [lunar-claude](https://github.com/basher83/lunar-claude), [domain-chassis](https://github.com/basher83/domain-chassis), [3I-commons](https://github.com/basher83/3I-commons) | Their outputs are consumed by other repositories, so a change here reaches many places |
| Live infrastructure and deployment (20) | 5 active, 5 recent, 9 dormant, 1 archived | [Triangulum-Prime](https://github.com/basher83/Triangulum-Prime), [Virgo-Core](https://github.com/basher83/Virgo-Core), [Omni-Scale](https://github.com/basher83/Omni-Scale), [mothership-gitops](https://github.com/basher83/mothership-gitops), [omni-infra-provider-proxmox](https://github.com/basher83/omni-infra-provider-proxmox) (fork, deployed), [tailnet-microservices](https://github.com/basher83/tailnet-microservices), [linux-hosts](https://github.com/basher83/linux-hosts) | A merge can change running systems; mostly older guidance written as CLAUDE.md only |
| Coordination, knowledge, registry (9) | 6 active, 3 recent | [lab-operations](https://github.com/basher83/lab-operations), [workshop-wiki](https://github.com/basher83/workshop-wiki), [personal-computing](https://github.com/basher83/personal-computing), [TheMothership](https://github.com/basher83/TheMothership), [personal-learning](https://github.com/basher83/personal-learning) | Heavy, explicit decision and standing vocabulary; personal and sensitive data |
| Published software with external users (7) | 2 active, 1 recent, 3 dormant, 1 archived | [Zammad-MCP](https://github.com/basher83/Zammad-MCP) (17 external contributor identities), [Proxmox-OpenAPI](https://github.com/basher83/Proxmox-OpenAPI), [radiant-filament](https://github.com/basher83/radiant-filament) | External contributors, a public reputation, and GHCR images |
| Agent tooling, harnesses, evals (27) | 6 active, 19 recent | [prompting-eval-workbench](https://github.com/basher83/prompting-eval-workbench), [the-range](https://github.com/basher83/the-range), [llm-observability-stack](https://github.com/basher83/llm-observability-stack), forge and nanny families | Many short-lived experiments; skills and plugins consumed by harnesses |
| Research and autonomous loops (13) | 2 active, 9 recent | [rr-prose-backpressure](https://github.com/basher83/rr-prose-backpressure), [research-ralph-template](https://github.com/basher83/research-ralph-template), [forge-pi](https://github.com/basher83/forge-pi) | Unattended agents commit, and a host loop pushes |
| Personal, profile, other forks (8) | mostly dormant | [dotfiles](https://github.com/basher83/dotfiles), [ssh-config](https://github.com/basher83/ssh-config), [claw-code](https://github.com/basher83/claw-code) | Little policy need beyond keeping secrets out |

Ownership (observed): every non-fork repository has `basher83` as its only human committer, with one exception. [Zammad-MCP](https://github.com/basher83/Zammad-MCP) has 17 other non-bot contributor identities, and its [PR ledger](https://github.com/basher83/Zammad-MCP/blob/main/docs/maintainer/PR_LEDGER.md) lists 41 open PRs at one point. Most PRs across the account were opened by bots (Renovate, Dependabot, Copilot, Devin). Most human work goes straight to `main`.

### Relationships and blast radius

| Producer | Consumed by (observed) | Where a small change spreads |
|---|---|---|
| [renovate-config `default.json`](https://github.com/basher83/renovate-config/blob/main/default.json) and presets | 37 repos extend it; 11 others use standalone `config:recommended` | Automerge rules decide what reaches `main` without review in every consumer, including deploy-on-merge repos (see the GitOps chain below) |
| [.github](https://github.com/basher83/.github) reusable workflows | `sync-labels.yml` is called by 8 repos (2 at `@main`, 6 pinned to six different SHAs); `python-mise-fast-pr-gate.yml` by radiant-filament | Repos at `@main` pick up changes immediately. The [Hercules-Power-Templates caller](https://github.com/basher83/Hercules-Power-Templates/blob/main/.github/use-sync-labels.yml) sits outside `.github/workflows/`, so GitHub never runs it |
| [pi-dev-config `core/`](https://github.com/basher83/pi-dev-config/blob/main/modes/README.md) | `core/global/AGENTS.md` is installed as `~/.pi/agent/AGENTS.md` (hashes match); `modes/tdd-python` is composed into [Zammad-MCP/AGENTS.md](https://github.com/basher83/Zammad-MCP/blob/main/AGENTS.md) | A shared agent-guidance mechanism already exists for Pi |
| [lunar-claude](https://github.com/basher83/lunar-claude/blob/main/.claude-plugin/marketplace.json) marketplace (15 plugins), [domain-chassis](https://github.com/basher83/domain-chassis/blob/main/AGENTS.md) plugin | Claude Code installations; domain-chassis says it is "consumed by every 3I domain" | Plugin changes reach every session that loads them. Consumers are not declared in any repo |
| Omni-Scale (substrate) → mothership-gitops (workloads) | [mothership-gitops AGENTS.md §1](https://github.com/basher83/mothership-gitops/blob/main/AGENTS.md) defers substrate ownership to Omni-Scale | Cross-repo fixes must stop at the boundary |
| tailnet-microservices → mothership-gitops | `anthropic-oauth-proxy` tracks another repo's `main`; automated sync is disabled as a "cross-repo promotion step" ([AGENTS.md §4](https://github.com/basher83/mothership-gitops/blob/main/AGENTS.md)) | Promotion is a manual gate |
| Triangulum-Prime modules | Referenced as `github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=vm/1.0.1` ([CLAUDE.md](https://github.com/basher83/Triangulum-Prime/blob/main/CLAUDE.md)) | Tagged refs limit drift |
| lab-operations | Coordinates work across Virgo-Core, mothership-gitops, linux-hosts, and Omni-Scale through linked PRs ([lab-operations#1](https://github.com/basher83/lab-operations/pull/1)) | Coordination records claim no authority over owner repos ([README](https://github.com/basher83/lab-operations/blob/main/README.md)) |

The highest-consequence chain is Renovate → GitOps → production (observed for each link; the end-to-end effect is inferred):

1. The [kubernetes preset](https://github.com/basher83/renovate-config/blob/main/presets/kubernetes.json) automerges Helm patch updates.
2. [mothership-gitops#42](https://github.com/basher83/mothership-gitops/pull/42) (a Phoenix chart bump) was merged by Renovate with zero reviews. The only checks were Fast Gate and GitGuardian.
3. `main` has no branch protection and no rulesets.
4. [apps/phoenix/application.yaml](https://github.com/basher83/mothership-gitops/blob/main/apps/phoenix/application.yaml) sets automated sync with prune and self-heal.

So an edit in renovate-config can roll a chart into `talos-prod-01` with no human step. This may be intended. The finding is that no single document states the end-to-end path.

### Where instructions and decisions live

Agent guidance comes in seven layers. Only some are version-controlled:

| Layer | Versioned | Observed content |
|---|---|---|
| `~/.claude/CLAUDE.md` (113 lines, global) | No. No repo contains it | Interaction and orchestration preferences |
| `~/.pi/agent/AGENTS.md` | Yes, installed from [pi-dev-config/core/global](https://github.com/basher83/pi-dev-config/blob/main/core/global/AGENTS.md) | Research, writing, and tool conventions |
| `~/.codex/AGENTS.md` | n/a | Empty file |
| `~/3I/lab/AGENTS.md`, `~/3I/DOMAINS.md`, `LAB.md`, `QUEUE.md`, `gates/` | No. The workspace root "is not git-tracked" | Lab invariants (remote state, no plaintext secrets, destroy and recreate), cluster roles, the gate lifecycle |
| Domain-wide methodology: [domain-chassis](https://github.com/basher83/domain-chassis) (last human commit 2026-07-18), [3I-commons ADRs](https://github.com/basher83/3I-commons/tree/main/architecture-decisions) (2026-07-08) | Yes | Gates, prime, review; commons ADR-001 to ADR-005 |
| Newer governance homes: [lab-operations](https://github.com/basher83/lab-operations) (treats prior structures as "evidence to assess, not structures to inherit"), [workshop-wiki](https://github.com/basher83/workshop-wiki/blob/main/concepts/governance-promotion.md) (promotion mechanism "unresolved") | Yes | Standing, approval, and promotion vocabulary |
| Repo root | Yes | 38 of 87 non-fork repos have `AGENTS.md` (27 of them with `CLAUDE.md` as a symlink to it); 20 have `CLAUDE.md` only, mostly 2025-era infrastructure; 29 have neither at root |

Decision records exist in 17 repos (ADR-style directories), plus PLAN/LOG pairs and frontmatter decision logs. Formats differ: [mothership-gitops ADRs](https://github.com/basher83/mothership-gitops/blob/main/docs/adrs/README.md) have Proposed, Accepted, Superseded, and Rejected statuses with supersession links. [personal-computing](https://github.com/basher83/personal-computing/blob/main/AGENTS.md) uses a `# Decision Log` per concept. [lab-operations](https://github.com/basher83/lab-operations/blob/main/PLAN.md) records dispositions in prose in PLAN.md and LOG.md.

Duplication and conflicts (observed):

- `~/3I/lab/AGENTS.md` requires remote state for all Tofu with "no local state files". [Triangulum-Prime CLAUDE.md](https://github.com/basher83/Triangulum-Prime/blob/main/CLAUDE.md) (line 205) instructs "Test locally with local backend" and lists `tofu apply` in its local workflow. Both load in the same session for Claude Code and Pi, which read ancestor files.
- `~/3I/lab/AGENTS.md` points agents to `omni-infra-provider-proxmox/PATCH.md` to explain a patched image that is currently deployed. That file is untracked in the local checkout, so the record of deployed divergence exists only on one disk.
- The [.github README](https://github.com/basher83/.github/blob/main/README.md) quick-start calls `python-quality.yml`, which does not exist. Four workflows exist, but the badge says five.
- The renovate-config [audit report](https://github.com/basher83/renovate-config/blob/main/docs/audits/AUDIT_REPORT_2026-04-28.md) found 13 false claims across six of its own docs, including AGENTS/CLAUDE drift. A later commit made AGENTS.md "canonical single source".
- [Zammad-MCP AGENTS.md](https://github.com/basher83/Zammad-MCP/blob/main/AGENTS.md) inherits a block requiring "a matching minimal GitHub Agentic Workflow" before any production test. The repo has no such workflow (it has `tests.yml`, `security-scan.yml`, `docker-publish.yml`). The 200-line file limit is met through a dated exemption list (`server.py` is 3,872 lines).

### Differences that matter for a shared policy

| Dimension | Range observed |
|---|---|
| Effect of merging to `main` | Nothing (research and wiki repos); a Scalr run with `auto_apply: false` defaults (Triangulum-Prime, per its YAML; live Scalr settings not verified); Argo auto-sync to production (mothership-gitops); a GHCR image push (Zammad-MCP, tailnet-microservices) |
| Push authority | "never push without approval" (personal-computing); "Ask before you push" (Zammad-MCP); "pushing remains his decision" (lab-operations PLAN); the host loop driver pushes between iterations (rr-prose-backpressure); unstated (renovate-config, Triangulum-Prime) |
| Sensitive data | Device registry and process arguments (personal-computing); Infisical-wired secrets (mothership-gitops); session transcripts (Entire, 27 repos) |
| Contributors | Solo in 86 non-fork repos; external contributors in Zammad-MCP |
| Generated content | Composed AGENTS.md (pi-dev-config modes); copied upstream docs (`renovate-config/docs/official-docs`); vendored corpora (rr-prose-backpressure, 7,412 files); agent-written wiki pages marked `generated: by: codex/gpt-6` (workshop-wiki) |
| Branch rules | Rulesets require PRs only in Zammad-MCP and Proxmox-OpenAPI; 17 repos block only deletion and force-push; 69 have none (the account is on GitHub Pro, so private repos could use rules) |

Session transcripts in public repositories (observed): 27 repos have an `entire/checkpoints/v1` branch, where Entire stores session data. In [renovate-config](https://github.com/basher83/renovate-config/tree/entire/checkpoints/v1), a public repo, that branch holds `full.jsonl`, `transcript.jsonl`, and `prompt.txt`. The first record includes creator user and account IDs, a session ID, and local filesystem paths. Eight of the 27 repos are public (Omni-Scale, domain-chassis, forgeflare, forgeflare-hooks, lunar-claude, renovate-config, tailnet-microservices, the-agent-toolshed). In four repos, including the public [the-agent-toolshed](https://github.com/basher83/the-agent-toolshed), the default branch is `entire/checkpoints/v1` rather than `main`. I did not audit transcript content for secrets. Whether Entire redacts before pushing is not established here.

## Review B: Representative sample

### Selection

| Repo | Represents | Guidance quality |
|---|---|---|
| [renovate-config](https://github.com/basher83/renovate-config) | Shared hub with the widest blast radius; also holds the attached `sources/` | Strong on format, silent on approval |
| [mothership-gitops](https://github.com/basher83/mothership-gitops) | Deploy-on-merge production | Strong, directive |
| [Triangulum-Prime](https://github.com/basher83/Triangulum-Prime) | 2025-era IaC hub with CLAUDE.md only, no CI, dormant human activity | Weak; conflicts with the workspace layer |
| [Zammad-MCP](https://github.com/basher83/Zammad-MCP) | Published software with external contributors | Very long (601 lines), composed from shared blocks |
| [lab-operations](https://github.com/basher83/lab-operations) | Cross-repo coordination and decision records | Very strong; high ceremony |
| [rr-prose-backpressure](https://github.com/basher83/rr-prose-backpressure) | Autonomous research loop | Strong, loop-specific |
| [personal-computing](https://github.com/basher83/personal-computing) | Sensitive personal data, layered knowledge | Strong |
| [workshop-wiki](https://github.com/basher83/workshop-wiki) (light) | Newest governance home with no root agent file | None at root |

Not covered: the 2025 Ansible and Docker hosts (hello-komodo, docker, Supernova), the forge software family, eval harnesses (prompting-eval-workbench, the-range), the plugin marketplaces as products, forks, and dormant personal repos. Plugin and skill distribution (lunar-claude, domain-chassis) is the most consequential gap, because those packages carry guidance into sessions in every repository.

### Who can decide and do what

- Observed: approval is explicit where the repository's risk is personal or live. [personal-computing](https://github.com/basher83/personal-computing/blob/main/AGENTS.md) lists six approval-required action classes. lab-operations grants authority per work slice and records it in PLAN ("Brent authorized coherent local commits as work progresses; pushing remains his decision"; "Brent approved one synthetic request").
- Observed: mothership-gitops states technical prohibitions (no prune on Longhorn, no auto-sync on `argocd-ha`) but no rule about agent merge, push, or `kubectl` authority beyond "break-glass procedures".
- Observed: renovate-config's AGENTS.md has no authority section at all, even though it is the account's widest-reaching file. Its one open decision ([#122](https://github.com/basher83/renovate-config/issues/122)) is filed as "Proposed solution for maintainer evaluation", so the convention lives in practice rather than in the instructions.
- Ambiguous: Triangulum-Prime documents `tofu apply` with no approval statement. The safeguard is Scalr's `auto_apply: false`, which the agent cannot see.
- Ambiguous: Zammad-MCP has a rule for pushing but none for commenting on, labelling, or closing external contributors' PRs. Those actions are public, and the [PR ledger](https://github.com/basher83/Zammad-MCP/blob/main/docs/maintainer/PR_LEDGER.md) plans them ("Comment routing: PRs — 11 Yes / 16 No / 14 Conditional").

### How a proposal becomes a decision

- Observed, strongest: lab-operations labels the standing of every artifact ("proposal, not blanket implementation authority"; "Accepted by Brent … on 2026-08-15"). Its [PHASE-3-REVIEW](https://github.com/basher83/lab-operations/blob/main/PHASE-3-REVIEW.md) is a tracked disposition record.
- Observed: mothership-gitops separates `specs/` (proposed), `docs/superpowers/plans/` (plans), `docs/adrs/` (decided), and `docs/incidents/` (history).
- Observed: personal-computing separates `sources/`, `research/` (always `status: draft`), and `bundles/`, with promotion as the only way in. [PR #30](https://github.com/basher83/personal-computing/pull/30) shows a promotion carried out under that rule.
- Weak: Triangulum-Prime and renovate-config have no place for decisions. renovate-config's rationale lives in issues and PR bodies ([#120](https://github.com/basher83/renovate-config/issues/120), [#121](https://github.com/basher83/renovate-config/pull/121)).
- Inferred: approval is almost always recorded as the author's own prose ("Brent accepted…"). GitHub review state is not used, since solo maintainers cannot approve their own PRs. The Zammad ledger notes this explicitly.

### How work is bounded

- Observed: a PR-body convention recurs across four repositories without any shared instruction requiring it. It names scope or standing, lists validation with explicit limits, links related cross-repo PRs, and states a merge or sync boundary.
  - [mothership-gitops#49](https://github.com/basher83/mothership-gitops/pull/49): "Do not merge or sync yet … merging can activate scheduled backups."
  - [lab-operations#1](https://github.com/basher83/lab-operations/pull/1): "Operational PR review is not merge/deployment approval."
  - [renovate-config#121](https://github.com/basher83/renovate-config/pull/121) and [personal-computing#30](https://github.com/basher83/personal-computing/pull/30) follow the same shape.
- Observed: discovered work goes to different places. rr-prose-backpressure has `TODO.md` with a three-iteration rule. lab-operations has PLAN plus `inbox.md`. renovate-config files issues. The workspace uses `TRIAGE.md`, which is unversioned.
- Observed: cross-repo change rules exist only pairwise (mothership-gitops → Omni-Scale "stop and say so"; lab-operations "discover legitimate owners rather than inferring them from file placement").

### Can rationale be recovered

- Observed: mothership-gitops ADR-001 → ADR-002 is a clean supersession, with the revisit trigger named in advance.
- Observed: agent attribution is inconsistent. Older repos use `Co-Authored-By` trailers (171 of 325 commits in the fetched window for Virgo-Core). Newer repos use `Entire-Checkpoint` trailers (79 of 101 for personal-computing). lab-operations, mothership-gitops, renovate-config, Triangulum-Prime, and workshop-wiki carry no AI co-author trailers in the window. forge-pi commits under dozens of ad hoc identities ("pi-spec-loop", "reverse-ralph", "Claude (cco)").
  - Inferred: a later reader cannot reliably tell agent work from operator work or connect a commit to its session, except where Entire is present. lab-operations has an open evaluation on exactly this question ([EVAL-001](https://github.com/basher83/lab-operations/blob/main/EVAL-001-ATTRIBUTION-RECOVERY.md)).
- Observed: lab-operations' rewritable PLAN.md has single paragraphs of about 300 words that mix current state with history ("Prior offline-only authority descriptions below apply to their original slices"). Inferred: telling current from superseded state takes close reading.

### What is actually verified

| Repo | Stated | Evidence |
|---|---|---|
| renovate-config | `renovate-config-validator --strict` is "the quality gate" | CI runs only that. [#120](https://github.com/basher83/renovate-config/issues/120) shows the Python caps were schema-valid but never matched, letting through a 3.14 proposal to Zammad-MCP. The fix PR verified with a real Renovate extraction run; CI still does not |
| mothership-gitops | pre-commit, hygiene, `validate:gitops` | Static checks only. "Full Helm/schema gate not run locally" ([#49](https://github.com/basher83/mothership-gitops/pull/49)). Runtime effects are verified manually |
| Triangulum-Prime | "validate manually with `tofu plan`" | No workflows; 207 Renovate PRs merged with GitGuardian as the only check |
| Zammad-MCP | Local and GitHub parity, TDD, an 86% coverage floor | Tests, security, and publish workflows exist; the required agentic workflow does not |
| personal-computing | `mise run ci`; `check:local` for secrets | AGENTS.md itself notes "A green gate does not prove factual accuracy, live-state currency, or secret-free transcripts" |
| rr-prose-backpressure | Verification blocks per finding | 16 `verify_*.py` scripts and a PreToolUse hook blocking `git add -A`; no CI |

### Shared versus local, and where friction would arise

These points are covered in the synthesis below.

## Synthesis

### Recurring needs a shared policy would address

1. **A consequence map.** Agents need to know whether merging, pushing, or running a command here changes a running system, publishes something, or affects other repos. The evidence is the Renovate → Argo chain, the GHCR publish-on-push workflows, Scalr triggers, and the public transcript branches. Today this knowledge is scattered across files in different repos, or held in tools the agent cannot see.
2. **One vocabulary for standing.** Agents and readers need to tell observation, proposal, approved plan, and implemented behavior apart. Four mature repos invented compatible but differently named versions (standing labels, `status: draft`, ADR statuses, `generated:` frontmatter).
3. **Authority defaults for irreversible or public actions.** Push, merge, apply, sync, posting to external contributors, and publishing need defaults. These are explicit in three repos, unstated in the hub and IaC repos, and different in the loop repos.
4. **Attribution.** Readers need to know which agent or session produced a change, with one mechanism used consistently.
5. **Honest verification statements.** Every strong PR already says what was and was not validated. Gates in renovate-config and Triangulum-Prime cover less than their instructions imply.
6. **One reconciled guidance stack.** The global, workspace, domain, and repo layers conflict (Tofu state), refer to records that exist only locally (PATCH.md), and include unversioned files.

### Expectations suitable across repositories, with evidence

| Expectation | Evidence it recurs or is needed in different repo types |
|---|---|
| State the merge and push consequence of the repo, and default to asking before push, merge, or publish unless the repo declares otherwise | Explicit in personal-computing, Zammad-MCP, and lab-operations; missing in renovate-config and Triangulum-Prime, where consequences are highest |
| PR and issue bodies state scope or standing, validation with its limits, related cross-repo changes, and the merge or deploy boundary | Arose independently in 4 repos ([#49](https://github.com/basher83/mothership-gitops/pull/49), [#1](https://github.com/basher83/lab-operations/pull/1), [#121](https://github.com/basher83/renovate-config/pull/121), [#30](https://github.com/basher83/personal-computing/pull/30)) |
| Keep observed and inferred claims apart; label proposals as proposals | Global Pi AGENTS.md, personal-computing, lab-operations, renovate-config#122 ("Not yet observed: …") |
| Changes in another repo go through that repo's owner process; do not work around another repo's limits locally | mothership-gitops §1, lab-operations AGENTS.md |
| No plaintext secrets; scan the outgoing range before publishing | Workspace invariant; Infisical scans reported in #49 and lab-operations#1 |
| One attribution mechanism for agent commits | The current four-way inconsistency described above |

### Responsibilities that need local ownership

- What counts as a consequential action and which gate applies: Argo sync policy exceptions (mothership-gitops), Scalr apply (Triangulum-Prime), GHCR publication (Zammad-MCP), live-machine reads (personal-computing).
- Decision-record format and location. ADRs, decision logs, and PLAN/LOG each fit their repo's purpose.
- Verification commands and what they prove.
- Repository-type contracts: TDD and code-size limits (Zammad-MCP, personal-computing), research commandments (loops), OKF layering (personal-computing).
- Handling of external contributors (Zammad-MCP only).

### Counterexamples to broad rules

- **"Stop and ask before continuing."** This contradicts rr-prose-backpressure's Commandment X, "Complete all autonomous work before reporting", and its host-side push. A universal stop rule would break the loop's design.
- **"Never push without approval."** This conflicts with Renovate's model and with the loop driver. It would need an explicit carve-out for automation identities.
- **"Every repo needs ADRs or PLAN/LOG."** 23 repos are dormant and several are empty or one-file stubs (crucible, searchmark, nanny-rs-via-pi-goal). lab-operations' level of ceremony is itself under evaluation (its [verification-friction work](https://github.com/basher83/lab-operations/blob/main/VERIFICATION-CONTRACT-PROPOSAL.md)).
- **"Require PRs and reviews on `main`."** Solo maintainers cannot approve their own PRs on GitHub, and the Zammad ledger records self-approval failing. In practice this adds a click without adding review.
- **Imported strict code rules.** Zammad-MCP needed a dated exemption list to coexist with the 200-line limit, and it does not meet the agentic-workflow requirement at all. Shared blocks that state preconditions a repo has not met produce rules that cannot be followed.
- **"AGENTS.md is the single source."** Claude Code and Pi also load ancestor and global files. A repo-only policy leaves the unversioned `~/3I` and `~/.claude` layers ungoverned.

## Prioritized questions and decisions

| # | Decision or question | Why it ranks here | Information needed |
|---|---|---|---|
| 1 | Should Entire checkpoints be pushed from public repos, and should the four default branches be reset to `main`? | Observed public exposure of transcripts, IDs, and paths; possibly irreversible | Entire's push and redaction configuration; a scan of the 8 public checkpoint branches; whether forks or clones already exist |
| 2 | Which layer holds the shared policy (repo-tracked, `~/3I` workspace, pi-dev-config global, domain-chassis plugin, or workshop-wiki), and do unversioned layers get a versioned source? | Determines where every later rule lives; current layers conflict | Which harnesses load which files (Claude Code, Pi, Codex ancestor-walk behavior); whether `~/3I` should become a repo |
| 3 | Is Renovate automerge into deploy-on-merge repos intended to reach production with no human step? | Observed end-to-end path, not documented anywhere | Argo CD notification and rollback setup; history of Renovate-caused incidents (the Phoenix timeout incident is a candidate to check); appetite for repo-level `automerge: false` overrides |
| 4 | Default authority model: ask before push, merge, apply, or publish unless the repo declares otherwise, with named carve-outs for bots and loops | Recurs in 3 repos, absent in hubs | Your list of actions that are acceptable without asking, per repo class; whether loop repos are trusted to self-push |
| 5 | Attribution standard: Entire trailers, `Co-Authored-By`, a dedicated bot identity, or a combination | Four mechanisms in use now; lab-operations EVAL-001 is designing the test | EVAL-001 results; whether Entire stays given decision #1 |
| 6 | Shared standing vocabulary: adopt one minimal set (observation, proposal, accepted, implemented, superseded) or map local vocabularies to it | Compatible local versions exist; workshop-wiki left promotion unresolved | Whether workshop-wiki or lab-operations owns the definition; whether a mapping is enough |
| 7 | Hub change policy: should renovate-config and .github changes require a dry run, or a consumer test, before merge? | #120 shows schema validation is not semantic verification; `@main` callers update instantly | Cost of a Renovate dry run in CI; whether to pin all `.github` callers to SHAs |
| 8 | Scope of the shared policy: all 92 repos, or only active and recent ones | 23 dormant, 2 archived, and 2 empty repos would add noise | Your intent for the 2025 infra repos (retire, archive, or revive); the status of the 4 repos that return 404 |
| 9 | How the policy treats publication of shared blocks (pi-dev-config modes) that impose preconditions on consumers | Zammad-MCP shows unmet inherited rules | Whether modes should declare their preconditions and consumers |

## Recommended next step

Pilot a minimal "consequence and authority" header plus the recurring PR-body shape in four repositories, for four weeks. Do not write a full policy yet.

Scope:

- Pilot repositories: [renovate-config](https://github.com/basher83/renovate-config) (shared hub), [mothership-gitops](https://github.com/basher83/mothership-gitops) (deploy-on-merge), [Triangulum-Prime](https://github.com/basher83/Triangulum-Prime) (weak guidance, conflicting layers), and [rr-prose-backpressure](https://github.com/basher83/rr-prose-backpressure) or [research-ralph-template](https://github.com/basher83/research-ralph-template) (autonomous loop, as the counterexample check). Zammad-MCP is a candidate second wave once the external-communication rule is drafted.
- Content of the shared part:
  - What merging, pushing, or running commands here changes, including other repos and live systems.
  - Which actions need approval, with carve-outs for bot and loop identities.
  - Where decisions and discovered work go.
  - What the gates prove and what they do not.
  - The PR-body fields (standing, validation and its limits, related changes, merge or deploy boundary).
- Content of the local part: everything in "Responsibilities that need local ownership" above.
- Out of scope: Entire remediation (decide #1 first, separately), branch rulesets, ADR adoption, and dormant repos.
- Before starting: decide #1 and #2, and resolve the Tofu local-state conflict between `~/3I/lab/AGENTS.md` and Triangulum-Prime.

Success criteria (each checkable from repository history or session records):

1. In cold-start sessions, the agent correctly states the merge and push consequence of the repo and the cross-repo effects of a proposed change. Target: at least 4 of 5 trials per repo. Use lab-operations' replay method from its 2026-09-15 concept-recovery test, and record trace and model this time, since that test lacked them.
2. No unapproved push, merge, apply, or sync occurs in the pilot repos. Loop repos keep their self-push carve-out without being blocked.
3. Every agent-authored PR in the pilot carries the four PR-body fields, with validation limits stated.
4. No new instruction conflicts between layers. Check with a grep-based or agent-run audit at start and end.
5. Friction: approval prompts per session, and time to a first useful commit, do not rise relative to the 4 weeks before the pilot. If they rise without a prevented error, drop the rule that caused them.
6. For hubs, a renovate-config preset change ships with evidence of its effect on at least one consumer (a dry run or extraction), not only schema validity.

Evidence that would change this assessment:

- Entire's redaction behavior.
- Live Scalr and Argo settings.
- The content of the four repositories that return 404.
- The forge, workshop, and research domain AGENTS.md files.
- Any incident history attributing an outage to an automerged update.
