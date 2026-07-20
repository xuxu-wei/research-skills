# Delegation Rules Pattern

Standard isolation and delegation pattern for research-article evaluators, auditors, and reviewers.

## Delegation Principle

Build skills (context-builder, architect, drafter, frontmatter-drafter, cover-letter) run **inline** in the orchestrator session.

Evaluate/audit skills (readiness-triage, methods-auditor, claim-auditor, narrative assessor, language assessor, content-preservation checker, evaluator, every review-panel role, medical-journal-review, submission compositor/verifier) run only in fresh independent subagents or delegated threads. Narrative and language readiness run in parallel against the same reader bundle; the orchestrator normalizes their included actions before any writer sees them. The orchestrator creates panel roles directly and aggregates only after all sealed reports return. A journal-fit reviewer receives the final article and a score-free verified candidate brief, never evaluator scores or findings.

## Isolation Requirements

1. **No shared implicit context**: Evaluators and auditors must not receive the orchestrator's internal reasoning, drafting history, or user conversation context.
2. **Explicit brief only**: The delegate brief (from `references/delegate-brief-templates.md`) is the sole source of task instructions.
3. **Frozen artifacts**: Every reviewer receives artifact IDs, paths, and versions. Reviewers treat source artifacts as read-only and must not switch versions mid-review.
4. **Blind separation**: Review panel members in `blind_external_simulation` mode receive only the manuscript and their role description. No context brief, evaluation reports, blueprint, or other reviewer outputs.
5. **Fresh final evaluation**: The evaluator runs only after editorial readiness/preservation. It receives no prior scores, decisions, plans, reports, deltas, audits, or assessor outputs. The orchestrator compares sealed scientific rounds only after the fresh evaluator returns.
6. **No inline fallback**: If a fresh independent context is unavailable, return `independent_review_pending` with a continuation brief and stop.

## Subagent Inputs

Each isolated subagent receives:
- Task brief (required)
- Frozen artifact IDs, versions, and file paths (required)
- User goal and target journal (required)
- Scope limitations (if applicable)
- Stable rubric and necessary factual artifacts (required for evaluation)
- No prior versions, plans, deltas, reports, scores, decisions, expected findings, or writer-facing repair brief in final evaluator inputs

## Subagent Prohibitions

Every delegate brief must explicitly state:
- Do NOT draft, revise, or rewrite text
- Do NOT edit, polish, or fix source artifacts
- Do NOT broaden scope beyond the assigned task
- Do NOT seek information not provided in the brief
- Do NOT call downstream skills (evaluator does not call refinement-controller)
- Do NOT access parent hidden reasoning, expected answers, or other reviewer outputs
- Report files read, review scope, input identities, isolation mode, findings, and unresolved issues

## Concurrent Delegation

For a review panel, create one fresh independent subagent or delegated thread per reviewer role and dispatch all roles concurrently. Wait for all required roles to complete before the coordinator reads their sealed outputs. Preserve dissent and conflicts; do not manufacture consensus.

## When Independent Delegation Is Unavailable

Build skills may continue in the orchestrator context. Reviewer-class work must not. For readiness triage, methods audit, claim audit, narrative/language readiness, content preservation, final evaluation, panel review, journal review, or final compositor/verification:

1. Set the relevant workflow step to `independent_review_pending`.
2. Save a self-contained continuation brief with the frozen input identities, paths, scope, rubric, output path, and prohibited actions.
3. Stop before issuing any quality decision, aggregate recommendation, promotion, or ready package status.
4. Resume only in a fresh independent subagent or delegated thread. Never perform the missing review inline.

## Audit Trail

Subagent input briefs and output reports are saved in `14_delegates/` for auditability:

```
14_delegates/
  readiness-triage-brief.md
  readiness-triage-output.md
  methods-audit-brief.md
  methods-audit-output.md
  claim-audit-brief.md
  claim-audit-output.md
  narrative-assessment-brief.md
  narrative-assessment-output.md
  language-assessment-brief.md
  language-assessment-output.md
  content-preservation-brief.md
  content-preservation-output.md
  evaluation-brief.md
  evaluation-output.md
  submission-compositor-brief.md
  submission-compositor-output.md
  panel-reviewer-domain-brief.md
  panel-reviewer-domain-output.md
  ...
```
