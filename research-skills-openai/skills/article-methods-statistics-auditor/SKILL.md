---
name: article-methods-statistics-auditor
description: "Audit study methods and statistical approach BEFORE drafting begins. Determine whether the study design supports the primary inference and whether any methodological flaws block manuscript writing."
---
# article-methods-statistics-auditor

## Purpose

Audit the study's methods and statistical approach before drafting begins. Answer: does the study design support the primary inference? Are there methodological flaws that block manuscript writing?

This skill does NOT evaluate manuscript quality (that is `article-evaluator`'s job), audit claims (that is `article-claim-auditor`'s job), draft text, or provide statistical consulting. It audits readiness from a methods perspective.

## Core Rules

- Audit methods, not manuscript. The manuscript doesn't exist yet.
- Distinguish between what writing CAN fix (incomplete Methods description) and what writing CANNOT fix (confounded design, wrong analysis).
- Call `methodology-statistics-preflight` for quick screening before deep audit when input is voluminous.
- Flag uncertainty rather than forcing a judgment. `uncertain — requires statistician review` is a valid output.
- The audit is pre-drafting: its audience is the orchestrator and architect, not the journal reviewer.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread. Never perform this review in the generator, drafter, revision, or orchestrator context.
- Receive frozen artifact IDs, file paths, and versions. Treat every source artifact as read-only.
- Write only the methods/statistics audit report. Do not edit, rewrite, polish, or fix any source artifact.
- Do not access parent hidden reasoning, expected answers, or outputs from other reviewers.
- Report `files_read` and `review_scope` in the review report, together with the standard review identity and isolation fields.
- Include `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `review_scope`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.
- If a fresh independent subagent or delegated thread cannot be established, return `independent_review_pending` plus a self-contained continuation brief and stop. Never review inline.

```yaml
review_id:
reviewer_skill: article-methods-statistics-auditor
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - article_context_brief
    - protocol_or_SAP (optional)
    - statistical_output (recommended)
    - analysis_plan_description (required if no SAP)
    - tables_figures (optional, for cross-check)
  required_outputs:
    - methods_audit_report
  may_read:
    - "02_context/**"
    - "00_input/**"
  may_write:
    - "05_audit/methods-audit.md"
  must_not_read:
    - "04_blueprint/**"
    - "06_drafts/**"
    - "08_evaluations/**"
  must_not_write:
    - "04_blueprint/**"
    - "06_drafts/**"
  may_call:
    - methodology-statistics-preflight
  must_not_call:
    - article-evaluator
    - article-claim-auditor
    - article-drafter
  failure_modes:
    - "no protocol/SAP and no analysis plan description → audit limited to design-level only, flag scope_limitation"
    - "statistical output format unreadable → request reformatted input, do not guess"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Confirm Audit Scope

Clarify what can and cannot be audited given available inputs:

```yaml
audit_scope:
  design_audit_possible: true | false
  statistical_audit_possible: true | false
  reporting_completeness_audit_possible: true | false
  limitations: []
```

### Step 2: Design Audit

Assess whether the study design supports the primary inference:

| Check | Assessment |
|-------|-----------|
| Design matches research question | pass | concern | fail |
| Primary endpoint defined and appropriate | pass | concern | fail |
| Sample size / power justification | pass | concern | fail | not_applicable |
| Control for confounding (observational) | pass | concern | fail | not_applicable |
| Randomization integrity (RCT) | pass | concern | fail | not_applicable |
| Blinding adequacy | pass | concern | fail | not_applicable |
| Selection bias risk | low | medium | high | unclear |
| Measurement/information bias risk | low | medium | high | unclear |
| Missing data handling | pass | concern | fail | not_reported |

### Step 3: Statistical Audit

Assess the statistical approach (when statistical output is available):

| Check | Assessment |
|-------|-----------|
| Primary analysis method appropriate | pass | concern | fail | cannot_assess |
| Model assumptions checked | pass | concern | fail | not_reported |
| Multiplicity handled | pass | concern | fail | not_applicable |
| Sensitivity analyses performed | pass | concern | fail | not_applicable |
| Subgroup analyses pre-specified | pass | concern | fail | not_applicable |
| Results internally consistent | pass | concern | fail | cannot_assess |

### Step 4: Determine Audit Status

```yaml
audit_status:
  pass                                            # methods defensible, proceed to drafting
  conditionally_pass_with_author_verification     # uncertain items need author confirmation
  requires_methods_clarification                  # Methods description incomplete but not blocking
  requires_reanalysis                             # analysis must be redone, cannot be fixed by writing
  methodologically_blocked                        # study design fundamentally flawed for intended inference
```

### Step 5: Generate Findings

For each concern, specify:

```yaml
findings:
  - finding_id: "M001"
    category: design | statistical | reporting
    severity: critical | major | minor | informational
    description: ""
    can_be_fixed_by_writing: true | false
    manuscript_implication: ""           # what the Methods section must address
    recommended_action: author_clarification | reanalysis | methods_detailing | sensitivity_analysis | limitation_statement | statistician_review
```

## Route Decision

| Audit Status | Route |
|-------------|-------|
| `pass` | Proceed to drafting |
| `conditionally_pass_with_author_verification` | Proceed, flag items for author |
| `requires_methods_clarification` | Proceed, flag Methods section for extra attention |
| `requires_reanalysis` | **Stop**. User must reanalyze before writing. |
| `methodologically_blocked` | **Stop**. Study design cannot support intended inference. |

## Output

Write `05_audit/methods-audit.md` containing the full audit report with audit scope, design audit, statistical audit, audit status, findings, and route decision.

## Stop Conditions

- `requires_reanalysis`: return specific reanalysis requirements.
- `methodologically_blocked`: return the blocking flaw with explanation of why writing cannot fix it.
- No context brief provided → cannot audit without knowing the study design.

## Pitfalls

- Do not audit the manuscript (it doesn't exist yet). Audit the study design and analysis plan.
- Do not require perfection. All studies have methodological limitations. Flag only what blocks or seriously weakens.
- Do not guess when statistical output is missing. Narrow the audit scope and flag the limitation.
- Do not conflate "not reported" with "not done." Mark `not_reported` separately from `fail`.
- Do not replace statistical consultation. When uncertain, say so.

## Verification

- Audit scope explicitly states what was and was not assessed
- Each design and statistical check has an explicit assessment
- Audit status maps to one of the five defined levels
- Each finding has a `can_be_fixed_by_writing` determination
- Route decision follows audit status per the routing table
- Limitations of the audit itself are documented

## References

- `references/methods-audit-checklist.md`: Comprehensive audit checklist organized by study type (RCT, observational, diagnostic, prediction model, systematic review, mechanistic, AI/ML, qualitative).
- `references/statistical-audit-guide.md`: Statistical method assessment criteria by analysis type.
- `article-orchestrator/references/artifact-contracts.md`: Canonical methods audit report schema.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory and naming conventions.
- `article-orchestrator/references/handoff-validation.md`: Methods audit → drafter handoff gates.
