---
type: Framework
title: Lifecycle and revision
description: Lifecycle statuses, the trust posture for agent drafts, and the revision-with-trajectory rule that replaces delete-if-wrong.
tags: [learnings, governance, framework, lifecycle, revision]
status: stable
generated: { by: claude_agent/Fable 5, at: 2026-08-24T03:45:24Z }
verified: { by: human:basher83, at: 2026-08-24T03:51:26Z }
---

# Trajectory

This concept decomposes [framework.md](/framework.md)'s maintenance and
lifecycle rules and currently replaces the delete-if-wrong maintenance
clause with the revision-with-trajectory rule below. Revision history lives
in the framework [log.md](log.md).

# Lifecycle

Concepts carry the OKF statuses `draft`, `stable`, and `deprecated`
(OKF §5.4). Agent-drafted concepts are created with `status: draft` and no
`verified:` key, placing them in OKF's unverified trust tier. Only the
operator verifies: a `verified:` entry by the operator and the flip to
`status: stable` are the operator's moves alone. A reviewer agent's sign-off
is a process gate — it may be required before a draft is presented for
acceptance — but it is never written as a `verified:` entry and never changes
the trust tier.

# Revision with trajectory

A material revision must identify the prior formulation it revises and state
whether it narrows, corrects, or replaces it. Silent replacement is
prohibited: a reader of the successor must be able to find what it
superseded and see the direction of the change.

Content adjudicated wrong or superseded is not deleted. It is deprecated —
`status: deprecated`, with a supersession note pointing to its successor —
and retained so the trajectory from rejected formulation to accepted one
stays inspectable. Deletion destroys exactly the comparison a revision is
judged by.

The log records every transition: creation, revision, deprecation, and
verification each get a `log.md` entry in the same change.
