# Independent Delegation Pattern

Use this pattern for every evaluator, triage, auditor, assessor, panel reviewer, and final verifier in the proposal workflow.

## Required execution pattern

1. The orchestrator explicitly creates a fresh independent subagent or delegated thread for the named reviewer skill.
2. The brief contains the user goal, task boundary, frozen artifact IDs, file paths and versions, allowed supporting facts, output path/type, and prohibited actions.
3. The reviewer reads sources without modifying them and writes only its review or verification report.
4. The reviewer cannot access the parent task's hidden reasoning, expected answer, or other reviewer outputs.
5. The report records the reviewer instance, files read, scope, isolation mode, and whether prior scores were visible or source edits were performed.
6. If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop. Never evaluate inline or produce a passing/final-ready state.

## Proposal role routing

| Reviewer skill | Explicit caller | Frozen inputs | Prohibited work |
|---|---|---|---|
| `proposal-readiness-triage` | `proposal-orchestrator` | idea/package, context brief, evidence artifacts, goal, constraints, target output | drafting, SAP writing, panel review |
| `proposal-drafter` planning instance | `proposal-orchestrator` | context/reader contract, evidence, source intent, binding constraints, target plan ref | proposal prose, evaluation, continuing as writer |
| `proposal-drafter` full writer | `proposal-orchestrator` | frozen content plan, context/reader contract, evidence/facts, binding constraints, target proposal ref | planning, evaluation, self-certification |
| `proposal-evaluator` | `proposal-orchestrator` | one complete current proposal, stable rubric, minimal call/factual inputs; optional anonymous must-fix list only before final evaluation | old proposal, context/readiness, repair/delta/editorial/prior evaluation artifacts, drafting, revising, panel review |
| `research-narrative-assessor` | `proposal-orchestrator` | current proposal and frozen reader handoff | scientific evaluation, language repair, raw peer-review history, source edits |
| `academic-language-assessor` | `proposal-orchestrator` | current proposal and frozen reader handoff | scientific/narrative evaluation, raw peer-review history, source edits |
| `proposal-drafter` editorial writer | `proposal-refinement-controller` | normalized editorial repair brief, current proposal, protected register | raw assessor/evaluator/readiness reports, old proposals, scientific changes, self-evaluation |
| `medical-journal-review` | `proposal-orchestrator` | final proposal and score-free journal candidate brief containing the verified journal facts | evaluator scores/findings/decision, readiness/repair/editorial/panel history, separate hidden facts, source edits |
| `sap-evaluator` | `proposal-orchestrator` | complete current SAP, proposal/context, anonymous methods facts, endpoint/data facts; optional anonymous must-fix list | preflight report, prior SAP/delta/report, writing, proposal evaluation, panel review |
| `proposal-review-panel` | `proposal-orchestrator` | frozen proposal version, mode, tier, review scenario | drafting, revising, source cleanup |

## Re-evaluation isolation

- Start a new evaluator instance after every revision.
- Do not expose the prior score, overall rationale, or decision.
- Provide only the current complete frozen artifact, stable rubric, necessary facts, and an optional anonymized must-fix list before final evaluation.
- Do not provide a prior version, revision delta, prior report, score, rationale, or decision.
- For final proposal evaluation, also prohibit context/readiness, content plan, repair brief, action execution, preservation, and narrative/language artifacts; do not provide an anonymized must-fix list.
- Use logical artifact identity and complete index records. Do not require or generate digests; tolerate legacy digest fields as inert metadata.
- The orchestrator compares completed reports and decides whether the workflow improved, reached a gate, or should stop.

## Panel concurrency

- Create one fresh independent subagent or delegated thread per reviewer role.
- Start all selected reviewers concurrently with the same frozen proposal version and role-specific briefs.
- Do not share reviewer outputs before all individual reports are complete.
- Wait for every selected reviewer, then aggregate while preserving dissent, minority objections, and fatal flaws.

## Editorial parallelism and repair

- Start narrative and language assessors concurrently on the same frozen proposal and reader handoff.
- Neither assessor sees the other output or scientific review history.
- Normalize included actions only after both return.
- Give one writer only the normalized brief, current proposal, and protected register.
- Validate all included actions before freeze, then use fresh instances for preservation and narrative/language reassessment.

## Journal route

- Create a score-free journal candidate brief only after final scientific evaluation, using the final proposal and verified current journal facts.
- A fresh medical-journal reviewer receives no evaluator, readiness, repair, editorial, or panel outputs.
- Journal findings remain separate from evaluator scoring and cannot upgrade or rewrite it.

## Audit checklist

- No reviewer or evaluator runs inline.
- No reviewer modifies the assessed source.
- No re-evaluator sees a prior score or decision.
- Every panel reviewer has a distinct independent instance.
- No passing or final-ready state is emitted when independent review is pending.
