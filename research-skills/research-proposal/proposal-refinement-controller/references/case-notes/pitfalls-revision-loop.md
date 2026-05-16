# Case Note: Revision Loop Pitfalls (Session-Learned)

## Pitfall 1: Skipping Re-evaluation After Revision

**What happened:** In I201 workflow (2026-05-12), v5 revision (MF-FINAL-1~3: text-level vignette fixes, Phase 0 condition expansion, "why system identification" bridge) was completed but the mandatory re-evaluation was skipped. The orchestrator then proceeded to final package assembly with an unevaluated v5.

**Why it matters:** The refinement-controller's Procedure Step 5 states: "修订后必须调用 proposal-evaluator 进行 re-evaluation，并派发给新的隔离、独立 evaluator 子 agent。" Even text-level changes can introduce precision loss or overcorrection. The Skeptical reviewer later confirmed that the v4 Clinical Vignette's "6个百分点" was a specific, unsubstantiated performance claim — this was only caught because the final panel reviewed v4, not because the orchestrator flagged it.

**Rule:** NEVER skip re-evaluation. Even "obviously correct" text-level fixes must pass through an isolated evaluator. Do not self-declare "resolved."

## Pitfall 2: Review Panel on Wrong Version

**What happened:** The final 4-reviewer panel (clinical expert, broad-field, methodology, skeptical) reviewed v4.0. Then v4→v5 revision addressed the panel's 3 MF-FINAL items. But v5 was never re-submitted to the panel — meaning the panel's endorsement technically applies to v4, not v5.

**Why it matters:** The orchestrator's Step 9 (review panel) and Step 7 (revision loop) have ambiguous ordering. If panel→revision, the revision delta is unreviewed. If revision→panel, the panel sees the latest version.

**Recommendation:** Two valid sequences:
1. Revision → Re-evaluation → Review Panel (panel sees final version)
2. Review Panel → Revision → Re-evaluation (panel items only, no need for second panel if scope is limited to panel's own items)

The orchestrator should explicitly track which version the panel reviewed.
