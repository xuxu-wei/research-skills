# Evaluation Policy

Use `evaluation-rubric.md` as the only source for dimensions, thresholds, hard
gates, fatal flaws, and decision anchors. This file adds execution rules only.

- Score solely from the frozen dossier. While scoring, do not browse or
  reconstruct missing facts; mark unsupported or insufficiently documented
  judgments unverified.
- `promote` and `revise_then_promote` require every hard gate to pass and no
  fatal flaw. A failed gate permits only `revise`, identity-preserving `reframe`,
  `keep_as_backup`, or `reject`.
- Fatal flaws override the mean. Examples include unusable core input,
  method-question mismatch, irreparable evidence-chain break, unsupported
  primary title/positioning, or no relevance to the stated goal.
- `reframe` cannot replace an identity anchor. If the only repair would do so,
  flag `identity_drift_detected`; the orchestrator decides `new_idea_required`.
- Never choose `merge`: another Idea is not an allowed input.
- Freeze every evaluation field before journal search. The later official-scope
  search is not evidence for Novelty, Feasibility, Impact, Relevance, Clarity,
  Completion, a gate, fatal flaw, or decision, and cannot change any of them.

Return bounded repair directions, not replacement prose.
