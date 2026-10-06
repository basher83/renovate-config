---
type: Enforcement Contract
title: Repository enforcement
description: This contract defines agent and code ownership, mise interfaces, lifecycle boundaries, and enforcement coverage.
status: draft
tags: [governance, enforcement]
generated: { by: codex_agent/GPT 6.1 Sol, at: 2026-10-06T19:45:48Z }
sources:
  - id: local-contract
    resource: /governance.md
    title: Local purpose, authority, and knowledge boundaries
  - id: local-decisions
    resource: /decisions.md
    title: Recorded implementation decisions
  - id: openwiki
    resource: https://github.com/langchain-ai/openwiki/tree/main/src/okf
    title: OpenWiki OKF implementation examples
  - id: reference-agent
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/tree/main/src/reference_agent
    title: OKF reference agent authoring and finalization examples
---

# Repository enforcement

This candidate defines the enforcement model for the [local operating contract](/governance.md).
Current index controls are implemented; the additional ownership and reconciliation mechanisms below are
proposals awaiting review. No Claims service, metadata repair engine, or PR acceptance projector is installed.
Implementation history belongs in [log.md](/log.md); decisions and their scope live in the decision
owner.[^local-contract]

## Ownership and permitted writes

Agents author authorized inputs. Code owns designated derived outputs and verifies their stored result.
Changing enforcement machinery requires task authority; agents must not weaken checks or bypass finalization
in order to make an unrelated content change pass.

| Surface | Agent responsibility | Code responsibility | Standing |
| --- | --- | --- | --- |
| Bundle concepts | Author scoped content and permitted descriptive metadata | Check current structural rules | Implemented checks; finer write boundary proposed |
| Sources and research | Gather, evaluate, and synthesize within authority; preserve raw evidence | Index intake and compare pinned captures | Implemented limited checks; no acceptance automation |
| Governed indexes | No direct tool calls targeting the files | Derive complete listings from metadata | Implemented generation and drift check |
| `generated` | Proposed: provide attributable run identity through the supported interface | Proposed: reconcile generation from a defined content baseline | No code-owned projection yet; existing authoring rule remains until selected |
| `verified` | Do not invent events; preserve legitimate historical events | Proposed: project only attributable verification evidence, preserving other owners | Shape checks only; authenticity not enforced |
| `status` and promotion | Propose transitions under the governing authority | Proposed: validate transitions against selected acceptance evidence | Vocabulary checks only; transition enforcement absent |
| `sources` | Attribute claims and identify evidence | Proposed: reconcile code-owned evidence joins without replacing independent entries | Current path and footnote checks; no Claims projection |
| Root `log.md` | Record factual scoped events with pointers; never invent acceptance | Validate log structure; proposed lifecycle append mechanism | Structural check; automated event projection absent |
| Machinery and mise tasks | Edit only in an authorized tooling task | Execute declared deterministic operations | Current index workflow implemented |

The [formatting conventions](/formatting.md#use-the-accepted-tag-vocabulary) own the locked tags,
[single-sentence metadata](/formatting.md#use-documented-fields-in-a-consistent-order),
[resource distinction](/formatting.md#distinguish-resource-binding-from-derivation), and
[accepted log labels](/formatting.md#record-scoped-history). Checks enforce vocabulary, sentence shape,
paths, and history structure; human review evaluates sentence meaning and asset binding.

## Mise is the repository interface

Agents invoke governed operations through mise, not individual implementation scripts or output paths.

```bash
mise run bundle:finalize
mise run bundle:check
mise run bundle:test
mise run bundle:lint
```

Finalization regenerates every bundle directory index and `sources/evaluate/index.md`,
then checks concepts, source joins, paths, index drift, and ten capture pins. A separate pre-commit mise task
lints authored documents and generated navigation; exact exclusions preserve imported capture bytes.
The generator's output derives
from metadata with filename ordering; prior index content is not an ordering input.[^local-decisions]

The capture tool is still exposed directly in existing guidance. A mise capture interface is proposed;
its source, mode, destination, and preservation requirements need explicit parameter handling before exposure.
This document records that interface gap rather than claiming it is already resolved.

## Lifecycle boundaries

1. **Preparation:** Establish scope, authority, permitted paths, source roles, and the exact starting revision.
   Proposed metadata reconciliation also needs a content baseline and attributable producer identity.
2. **Authoring:** Agents work on permitted content. They do not author indexes or invent approval/verification.
   Proposed post-write repair operates only on selected code-owned structure and reads back stored bytes.
3. **Finalization:** The configured pre-commit hook invokes mise automatically. Generated changes stop the commit
   for review and inclusion; retrying with included outputs must pass. No automatic staging or commit occurs.
4. **Review and acceptance:** PR acceptance is the intended human boundary. The operator selected merge of the PR by
the operator; machine projection is
   unimplemented. Any receipt must identify the reviewed revision, actor, scope, and subsequent changes.
5. **Publication:** Obtain applicable approval for the concrete result. A future publication check should validate
   the actual revision being sent; checking only a mutable working tree is insufficient to prove that revision.

Both inspected examples put index maintenance after authoring. OpenWiki additionally repairs metadata and
reconciles code-owned provenance and Claims projections. The OKF reference agent can use model synthesis for
some directory descriptions; that mechanism is not used by this repository's deterministic generator.
These are implementation evidence, not authority to import their complete storage or trust
model.[^openwiki][^reference-agent]

## Repair, rejection, and preservation

Proposed repair must be deterministic, limited to selected structure, and preserve authored bodies and
independently owned metadata. Unknown but permitted producer extensions must not be silently lost.
OKF conformance and stricter local authoring rules must be checked and reported separately.

Do not manufacture authority through repair: invalid verification, unproven promotion, or a missing acceptance
receipt must not become an invented human event. Removing an invalid status can imply OKF's default `stable`,
so lifecycle-sensitive failures require an explicit safe response rather than automatic deletion.
Capture bytes remain evidence and must not be repaired as though they were current local concepts.
A failed required persistence/read-back operation prevents claiming successful finalization. Optional operations
need an explicit best-effort rule and a reported gap; they must not silently weaken required acceptance conditions.

## Trail, rationale, and Claims

Root `log.md` records dated changes and lifecycle events, newest first, using ISO date headings and links.
It is reserved history, not an ordinary concept, and has no concept frontmatter. Concept bodies describe the
current model; decisions retain material rationale and supersession. Neither an index nor a log creates authority.

OpenWiki's Claims mechanisms distinguish durable evidence/state from metadata projected onto pages. Evaluate
that separation here before selecting any local ledger or projector. If implemented, projections must own only
their designated entries, preserve other producers' events, and have a recovery path when persistence fails.
PR acceptance, content verification, generation, and publication remain distinct events.[^openwiki]

## Evidence required for the exemplar

- Named ownership and permitted paths for every governed artifact or field.
- Automatic finalization at the selected boundary and verification of stored outputs.
- Negative controls for output tampering, invalid metadata, and unsupported lifecycle transitions.
- Repeatability: unchanged inputs produce no new output or invented lifecycle events.
- Attributable human acceptance of a reviewed revision, plus explicit treatment of later changes.
- Receipts describing implementation, configuration, observed execution, bypasses, and remaining limits.

Current evidence covers index generation/drift, capture fidelity, structural checks, and a temporary-repository
pre-commit exercise. It does not demonstrate metadata repair, verification authenticity, PR projection, hosted
CI bundle coverage, or a check of the outgoing committed revision. See the trail for scoped receipts.

[^local-contract]: Local governance defines purpose and authority; this concept owns enforcement responsibilities.
[^local-decisions]: D007–D009 record the current intake, generator, and mise finalization changes.
[^openwiki]: Inspected opensrc implementation; mutable upstream reference, not a local adoption or pinned Claims
    deployment.
[^reference-agent]: Inspected opensrc authoring tool and runner finalization; source example only.
