# Delegation Rules Pattern

Standard isolation and delegation pattern for research-article evaluators, auditors, and reviewers.

## Delegation Principle

Build skills (context-builder, architect, drafter, frontmatter-drafter, cover-letter) run **inline** in the orchestrator session.

Evaluate/audit skills (readiness-triage, methods-auditor, claim-auditor, evaluator, review-panel reviewers) run via **`delegate_task`** as isolated subagents. Biomedical cover-letter-only review is a narrow delegate task to `medical-journal-review`; the delegate receives only the cover letter and returns the apparent article tier from that letter alone.

## Isolation Requirements

1. **No shared implicit context**: Evaluators and auditors must not receive the orchestrator's internal reasoning, drafting history, or user conversation context.
2. **Explicit brief only**: The delegate brief (from `references/delegate-brief-templates.md`) is the sole source of task instructions.
3. **Frozen artifacts**: Evaluators evaluate the artifact version specified in the brief. They must not request newer versions mid-evaluation.
4. **Blind separation**: Review panel members in `blind_external_simulation` mode receive only the manuscript and their role description. No context brief, evaluation reports, blueprint, or other reviewer outputs.

## Subagent Inputs

Each isolated subagent receives:
- Task brief (required)
- File paths to relevant artifacts (required)
- User goal and target journal (required)
- Scope limitations (if applicable)
- Prior assessment report (for re-evaluation only)

## Subagent Prohibitions

Every delegate brief must explicitly state:
- Do NOT draft, revise, or rewrite text
- Do NOT broaden scope beyond the assigned task
- Do NOT seek information not provided in the brief
- Do NOT call downstream skills (evaluator does not call refinement-controller)

## Concurrent Delegation

For review panel: use `delegate_task(tasks=[...])` to dispatch all reviewers in a single call. Reviewers run concurrently and independently.

## Fallback When delegate_task Unavailable

If the runtime does not support `delegate_task`:
1. Build skills (context-builder, architect, drafter) continue to run inline.
2. Readiness triage, methods auditor, claim auditor must **defer** to a fresh independent session or mark the evaluation as `independence_status: fallback_pending`.
3. Final independent evaluation MUST be performed in an isolated context. If unavailable, mark `draft_status: evaluated_inline_degraded` and record `scope_limitation: isolation_unavailable`.
4. No manuscript may receive `ready_for_author_signoff` status without at least one truly isolated evaluation.
5. If evaluator or reviewer work is performed inline, record `independence_status: inline_degraded`; the highest downstream package status is `ready_for_author_check`.

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
  evaluation-brief.md
  evaluation-output.md
  panel-reviewer-domain-brief.md
  panel-reviewer-domain-output.md
  ...
```
