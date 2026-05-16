# Loop Control and Stop Rules

Revision loop limits, targeted repair rules, and stop conditions for `article-refinement-controller`.

## Revision Round Limits

- **Default maximum**: 2 substantive revision rounds.
- **Language polishing**: Does not consume a revision round.
- **Reporting completion** (checklist item additions): Does not consume a revision round.
- **Evidence relinking** (updating provenance ledger without text changes): Does not consume a revision round.
- If a 3rd round is needed: orchestrator records `major_revision_required` and stops the automated loop. Manual author intervention is required.

## Targeted Repair Rules

### When Evaluator Returns `revise`

1. `article-refinement-controller` classifies the revision mode (see `references/artifact-contracts.md` revision_plan schema).
2. For revision modes `analysis_required` or `study_redesign_required`: **stop immediately**, do not attempt text-based fixes.
3. For all other modes: generate a revision plan with entry strategy per item (`enter_manuscript` / `response_only` / `decline`).
4. Dispatch `article-drafter` in revision mode.
5. Generate three files per round in `09_revisions/round-NNN/`.
6. Dispatch fresh isolated `article-evaluator` for re-evaluation.

### When Claim Auditor Returns `downscale_and_proceed`

1. Route directly to refinement with primary mode = `claim_downscaling`.
2. Downscaled claims require **author confirmation** before the manuscript advances.

### When Language Hard Gates Fail

1. Route to refinement with primary mode = `language_polishing`.
2. Call `academic-language-assessor` in standalone-preflight mode.
3. `article-drafter` fixes only language issues; substance must not change.
4. Generate `language_change_log`.
5. Call `academic-language-assessor` for re-assessment.

## Stop Conditions

Stop the workflow and report to user when:

| Condition | Trigger | Action |
|-----------|---------|--------|
| Readiness blocked | `readiness_status = not_ready` | Return blocking gaps; suggest required actions |
| Methods blocked | `audit_status ∈ {requires_reanalysis, methodologically_blocked}` | Return audit report; suggest reanalysis or study redesign |
| Fatal overclaims | `claim_audit.recommendation = blocked` | Return claim audit; must fix before proceeding |
| Fatal flaws | `evaluation.decision = reject` | Return evaluation; document unfixable flaws |
| No gain | `evaluation.decision = stop_no_gain` | Return delta report with evidence of no improvement |
| Max rounds reached | `revision.round > max_rounds` | Stop; mark `major_revision_required` |
| Panel rejects | `aggregated_recommendation = reject_or_redesign` | Stop; suggest return to study design |

## Re-evaluation Rules

After each revision round:
1. Use a **fresh** isolated subagent for re-evaluation — never reuse the previous evaluator's context.
2. Evaluator must compare versions (Thesis Integrity check).
3. If `thesis_integrity ≤ 2` (core claim became less clear): decision must be `revise`, direction = **减法** (remove caveat layers).
4. If revision produced no substantive improvement: decision should be `stop_no_gain`.
5. Re-evaluation must use a fresh isolated evaluator. Inline re-evaluation is recorded as `inline_degraded` and caps final package status at `ready_for_author_check`.

## Delta Report Quality Gate

Before routing to re-evaluation, the orchestrator (or refinement-controller) checks:
- Delta report must not be empty or contain only "polished expression" / "improved clarity".
- Every evaluator concern must have an explicit status: addressed / partially_addressed / not_addressed_with_reason.
- If the delta is insufficient, return it to refinement-controller for completion.
