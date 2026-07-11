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
| `proposal-evaluator` | `proposal-orchestrator` or `proposal-refinement-controller` | proposal version, context, evidence, goal, constraints; for re-evaluation, previous version plus anonymized issue list and delta | drafting, revising, SAP writing, panel review |
| `sap-evaluator` | `proposal-orchestrator` or `sap-refinement-controller` | SAP version, proposal/context, preflight, endpoint/metric definitions, data description; for re-evaluation, previous version plus anonymized issue list and delta | SAP writing, proposal drafting/evaluation, panel review |
| `proposal-review-panel` | `proposal-orchestrator` | frozen proposal version, mode, tier, review scenario | drafting, revising, source cleanup |

## Re-evaluation isolation

- Start a new evaluator instance after every revision.
- Do not expose the prior score, overall rationale, or decision.
- Provide only the current and previous frozen versions, a stable rubric, necessary factual materials, an anonymized must-fix issue list, and the revision delta.
- The orchestrator compares completed reports and decides whether the workflow improved, reached a gate, or should stop.

## Panel concurrency

- Create one fresh independent subagent or delegated thread per reviewer role.
- Start all selected reviewers concurrently with the same frozen proposal version and role-specific briefs.
- Do not share reviewer outputs before all individual reports are complete.
- Wait for every selected reviewer, then aggregate while preserving dissent, minority objections, and fatal flaws.

## Audit checklist

- No reviewer or evaluator runs inline.
- No reviewer modifies the assessed source.
- No re-evaluator sees a prior score or decision.
- Every panel reviewer has a distinct independent instance.
- No passing or final-ready state is emitted when independent review is pending.
