# Repository knowledge change log

## 2026-10-06

* **Remediation preparation**: Reconciled capture-preserving hook exclusions, added complete authored-document
  lint through mise, and isolated the source-escape regression fixture inside its owned temporary directory.
  [D011](decisions.md#2026-10-06--d011-reconcile-the-complete-pre-commit-boundary) records authority and scope.
* **Validation**: Full hooks passed without bypasses in an isolated staged repository; all ten pinned captures
  matched the starting revision. A concept-title change regenerated navigation and stopped the hook attempt;
  including the output made retry pass, and repeat finalization was idempotent. Nine regressions, authored
  Markdown lint, and strict root/preset validation passed. The
  [validation receipt](../sources/evaluate/2026-10-06-remediation-receipt.json) records scope and limitations.
  No commit, push, PR edit, or acceptance occurred.
* **Preparation**: Drafted the exemplar purpose and [enforcement ownership model](enforcement.md), following
  operator concurrence with the gap review.
  [D010](decisions.md#2026-10-06--d010-capture-exemplar-intent-and-separate-the-trail)
  records scope and the selected operator-merge acceptance event. This is a documentation candidate, not a PR
  acceptance event.
* **Implementation**: Configured mise index finalization at pre-commit; a temporary-repository exercise showed
  regeneration stopping the first attempt and passing after generated output was included. See
  [D009](decisions.md#2026-10-06--d009-finalize-indexes-through-mise-before-commit). No commit or publication occurred.
* **Correction**: Assigned governed indexes to their generator and moved root reference records into pending
  `sources/evaluate/`. [D007](decisions.md#2026-10-06--d007-separate-knowledge-from-sources-pending-evaluation) and
  [D008](decisions.md#2026-10-06--d008-govern-indexes-through-their-generator) retain rationale and scope.
