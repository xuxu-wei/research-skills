# Proposal Editorial and Journal Routing

## Editorial eligibility

Start editorial assessment only when the current complete proposal has no pending scientific or methodology repair. Freeze:

- a reader handoff containing only `target_reader_profile`, `reader_prior_knowledge`, `terms_requiring_definition`, `reader_reasoning_chain`, `gap_type`, and binding constraints; and
- a protected-content register covering the research question, significance and gap, aims, methods, assumptions, feasibility, risks, novelty/impact claim strength, deliverables, and required source intent.

Use `../templates/template-proposal-reader-handoff.yaml` for the reader artifact. It is a stable projection of context, not a review report or drafting rationale.

Run fresh `research-narrative-assessor` and `academic-language-assessor` instances in parallel. They receive the current proposal and reader handoff only. They do not see evaluator/readiness/method reports, prior drafts, deltas, workflow state, repair history, or one another's outputs.

## One normalized editorial repair brief

Create `06_revisions/round-NNN/editorial-repair-brief-rNNN.yaml` from included actions only. Every action must have a stable ID, source finding ID and assessor type, target locator, operation, intended reader effect, protected content, dependencies, and observable acceptance criterion. Record excluded or conflicting actions outside the writer brief.

The writer receives only:

1. the normalized editorial repair brief;
2. the current complete proposal; and
3. the protected-content register.

Do not provide raw assessor reports, scientific evaluations, readiness reports, prior versions, deltas, scores, or hidden rationale. Use one writer instance and one complete target. Bounded section passes are sequential work within that target, not independent partial drafts.

Before freezing the repaired proposal, validate that every included action is executed or explicitly blocked, dependencies are satisfied, and the complete target remains readable. Then run a fresh content-preservation check and fresh narrative/language reassessments. A scientific change, identity drift, or preservation failure returns to scientific review; editorial findings return to a new editorial round.

## Final evaluator isolation

The final evaluator may read only:

- the current revised complete proposal;
- the stable proposal rubric and gates; and
- minimal call requirements or factual inputs needed to judge alignment.

It must never read old drafts, context/readiness reports, repair briefs, action reports, deltas, preservation/editorial reports, prior evaluations, scores, findings, rationale, or decisions.

## Score-free journal route

Only after `final_scientific` acceptance, create `08_panel/journal-candidate-brief-vNNN.yaml` from the final proposal and verified current journal facts. The brief contains no numeric fit score, evaluator score, evaluator finding, readiness decision, or repair history. It records each concrete journal, article type, audience/scope fit, verified requirements, source URL, verification date, mismatch, and unresolved fact.

Dispatch a fresh `medical-journal-review` with only the final proposal and journal-candidate brief. Every allowed verified journal fact must already be recorded in the brief. The reviewer must not see proposal evaluator outputs, readiness reports, editorial reports, repair history, panel reports, or hidden expected conclusions. Journal findings cannot retroactively change evaluator scores.
