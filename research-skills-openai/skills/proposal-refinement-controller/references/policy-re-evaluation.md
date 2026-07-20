# Re-evaluation Policy

## Purpose

Ensure each revision is assessed by an isolated, independent evaluator.

## Required Inputs

- Updated complete frozen proposal logical identity and path.
- Stable rubric and only the factual materials needed to assess the updated proposal.
- For non-final scientific reassessment only, an optional anonymized must-fix issue list with no scores, overall rationale, or decision. It is prohibited for `final_scientific`.

## Isolation Requirements

The re-evaluator must not be the drafter, refiner, or a self-checking continuation of the drafting context.

The non-final scientific re-evaluator should see only the latest complete frozen proposal, stable rubric, necessary factual materials, and optional anonymized must-fix issue list. It must not see a prior proposal, revision delta, context/readiness report, repair brief, editorial or preservation report, hidden drafting rationale, prior scores, overall rationale, or the prior decision.

The `final_scientific` evaluator receives only the revised final proposal, stable rubric/gates, and minimal call/factual inputs. It receives no anonymous must-fix list, old draft, context/readiness report, repair brief, action-execution report, protected register, delta, preservation report, narrative/language report, or prior evaluation.

Use logical artifact identity (`artifact_id`, `version`, `path`) and complete index records. Do not require or generate SHA/digest fields; tolerate legacy digest metadata without using it for matching.

## Required Current-Artifact Assessment

When an allowed anonymous must-fix list is supplied, a non-final scientific reassessment must state which listed defects remain in the current proposal. Every stage must answer:

- Are there new defects in the current complete proposal?
- Does the current proposal contain a coherent research question, aims, methods, and claims?
- Should the current proposal be accepted, revised again, or rejected?

The orchestrator alone compares sealed rounds and the separate delta for
improvement or `stop_no_gain`.
