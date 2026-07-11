---
name: article-evaluator
description: "Use when a frozen manuscript needs a holistic, non-compensatory independent evaluation across seven dimensions and a gated decision of accept, revise, or reject."
---
# article-evaluator

## Purpose

Evaluate the complete manuscript against seven quality dimensions with non-compensatory gates on the most critical dimensions. Apply the stable rubric directly to the frozen manuscript and perform a supplementary materials audit.

This skill does NOT rewrite text, audit claims one by one (that is `article-claim-auditor`'s job), audit methods (that is `article-methods-statistics-auditor`'s job), or make revision plans (that is `article-refinement-controller`'s job). It evaluates and decides.

## Core Rules

- Scientific Validity and Evidence-Claim Alignment are non-compensatory: a high score on Clarity cannot offset a fatal scientific flaw.
- Language baseline is non-compensatory via hard gates: systematic grammar/register errors block `accept`.
- Apply the stable language rubric directly to the frozen manuscript without reading `academic-language-assessor` output. The orchestrator separately delegates that specialist review and compares sealed reports only after both return.
- Perform supplementary audit: check that critical evidence is not buried in supplementary, supplementary content is complete, and journal limits are satisfied.
- The evaluation is a gate. `reject` means stop. The orchestrator, not the evaluator, compares sealed evaluation reports to determine `stop_no_gain`.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread. Never perform this review in the generator, drafter, revision, or orchestrator context.
- Receive frozen artifact IDs, file paths, and versions. Treat every source artifact as read-only.
- Write only the evaluation report. Do not edit, rewrite, polish, or fix any source artifact.
- Do not access parent hidden reasoning, expected answers, prior evaluation scores or decisions, or outputs from other reviewers.
- Report `files_read` and `review_scope` in the review report, together with the standard review identity and isolation fields.
- If a fresh independent subagent or delegated thread cannot be established, return `independent_review_pending` plus a self-contained continuation brief and stop. Never review inline.

```yaml
review_id:
reviewer_skill: article-evaluator
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
    - manuscript_draft
    - article_blueprint
    - article_context_brief
  required_outputs:
    - evaluation_report (with independent language rubric and supplementary_audit)
  may_read:
    - "06_drafts/**"
    - "04_blueprint/**"
    - "02_context/**"
  may_write:
    - "08_evaluations/evaluation-v*.md"
  must_not_read:
    - "08_evaluations/**"
    - "10_panel/**"
    - "09_revisions/**"
  must_not_write:
    - "06_drafts/**"
    - "04_blueprint/**"
  may_call: []
  must_not_call:
    - article-drafter
    - article-architect
    - article-claim-auditor
  failure_modes:
    - "required frozen manuscript or blueprint missing → return an evaluation failure report without a decision"
  escalation_route: "article-orchestrator"
```

## Seven Dimensions

| Dimension | Compensatory | Assessor |
|-----------|-------------|----------|
| Scientific Validity | **Non-compensatory** | Independent evaluation |
| Evidence-Claim Alignment | **Non-compensatory** | Independent evaluation |
| Reporting Completeness | Compensatory | Reporting checklist mapping |
| Journal Fit | Compensatory | Journal adapter comparison |
| Clarity & Structure | Compensatory | Independent evaluation |
| Language & Academic Register | **Non-compensatory (gates)**; Compensatory (score) | Independent rubric application; specialist report remains sealed from this evaluator |
| Contribution Significance | Compensatory | Blueprint + independent evaluation |

Each dimension scored 1–10 with a severity: `pass | borderline | fail`.

## Hard Gates

### Scientific Validity Gates (non-compensatory)

```yaml
scientific_validity_gates:
  - methods_support_primary_claim: pass | fail
  - primary_evidence_exists: pass | fail
  - no_fatal_scientific_flaw: pass | fail
```

### Evidence-Claim Gates (non-compensatory)

```yaml
evidence_claim_gates:
  - no_fatal_overclaim: pass | fail
  - primary_claim_has_evidence: pass | fail
```

### Genre/Rhetoric Gates

```yaml
genre_rhetoric_gates:
  - observational_causal_language: pass | fail
  - narrative_clinical_vignette_in_results: pass | fail
  - didactic_rhetorical_questions_in_discussion: pass | fail
  - promotional_overclaim: pass | fail
  - tone_mismatch_with_journal: pass | fail
  - informal_colloquial_register: pass | fail
  - non_standard_abbreviation_undefined: pass | fail
```

### Language Baseline Gates (non-compensatory, independently applied)

```yaml
language_baseline_gates:
  - grammar_error_density: pass | fail
  - terminology_consistency: pass | fail
  - tense_systematic_violation: pass | fail
  - academic_register_pervasive: pass | fail
```

## Supplementary Audit

```yaml
supplementary_audit:
  critical_evidence_buried: []            # primary claims supported only by supplementary evidence
  missing_supplementary_content: []       # main text references missing supplementary items
  orphan_supplementary_content: []        # supplementary items not referenced in main text
  overstuffed_supplementary: []           # excessive supplementary volume approaching duplicate publication
  journal_limit_compliance: pass | fail
  data_code_availability_compliance: pass | fail | partial
```

## Decision

| Decision | Conditions | Route |
|----------|-----------|-------|
| `accept` | All non-compensatory gates pass, overall adequate | Review panel or frontmatter |
| `revise` | Addressable issues found | Refinement controller |
| `reject` | Fatal flaw, cannot be fixed by writing | **Stop** |

Decision logic:
- Any `fatal_scientific` gate fail → `reject`
- Any `language_baseline` gate fail → at least `revise`
- Any `genre_rhetoric` gate fail → at least `revise`
- All gates pass + scores adequate → `accept`

Fatal overclaim gate handling:
- Fixable fatal overclaim gate failure routes to `revise` with `claim_downscaling`, removal, or relocation.
- Unfixable fatal overclaim gate failure routes to `reject`.

## Output

Write `08_evaluations/evaluation-vNNN.md` containing dimension scores, gate results, supplementary audit, issue list with revision priorities, and decision. In re-evaluation mode, evaluate the frozen latest draft from scratch with the stable rubric. Do not read the prior report, score, or decision. The orchestrator compares sealed reports after this evaluator finishes.

The report must include:

```yaml
review_id:
reviewer_skill: article-evaluator
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
review_scope: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: accept | revise | reject
findings: []
unresolved_issues: []
```

Each issue must include:

```yaml
- issue_id: "E001-C003"
  dimension: ""
  severity: critical | major | minor
  description: ""
  location: ""
  revision_priority: must_fix | should_fix | optional
  entry_strategy: enter_manuscript | response_only | decline   # for refinement controller
```

## Pitfalls

- Do not compensate a fatal scientific flaw with high Clarity or Language scores.
- Do not skip the supplementary audit. Critical evidence buried in supplementary is a common failure mode.
- Do not gate language at native-speaker perfection. Gate at functional academic communication.
- Do not evaluate claims one by one (that is the claim auditor's job). Evaluate patterns and overall alignment.
- Do not compare against a prior evaluation in re-evaluation mode. The orchestrator performs the cross-round comparison after receiving sealed reports.

## Verification

- All seven dimensions scored with explicit severity
- All hard gates assessed, not skipped
- Language assessment integrated (not a separate report)
- Supplementary audit complete with all five checks
- Every issue has a `revision_priority` and `entry_strategy`
- Decision follows gate logic, not overall impression
- Re-evaluation used a fresh evaluator instance with `prior_scores_visible: false`

## References

- `references/evaluation-rubric.md`: Detailed 1–10 scoring anchors for each dimension.
- `references/evaluation-gates.md`: Complete hard gate definitions, thresholds, and consequences.
- `references/supplementary-audit-guide.md`: Criteria for critical evidence burial, completeness, and journal limit compliance.
- `article-orchestrator/references/artifact-contracts.md`: Canonical evaluation report schema.
- `article-orchestrator/references/handoff-validation.md`: Evaluator → refinement controller handoff gates.
