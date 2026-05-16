---
name: article-evaluator
description: Perform a holistic, non-compensatory evaluation of the manuscript across seven dimensions. Integrate language assessment and supplementary audit. Output a structured evaluation report with gated decision: accept | revise | reject | stop_no_gain.
version: 0.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-article, evaluation, quality, non-compensatory, language, supplementary]
    related_skills:
      - article-orchestrator
      - article-claim-auditor
      - article-refinement-controller
      - academic-language-assessor
---

# article-evaluator

## Purpose

Evaluate the complete manuscript against seven quality dimensions with non-compensatory gates on the most critical dimensions. Integrate language assessment and supplementary materials audit into the evaluation.

This skill does NOT rewrite text, audit claims one by one (that is `article-claim-auditor`'s job), audit methods (that is `article-methods-statistics-auditor`'s job), or make revision plans (that is `article-refinement-controller`'s job). It evaluates and decides.

## Core Rules

- Scientific Validity and Evidence-Claim Alignment are non-compensatory: a high score on Clarity cannot offset a fatal scientific flaw.
- Language baseline is non-compensatory via hard gates: systematic grammar/register errors block `accept`.
- Call `academic-language-assessor` for the Language dimension. Do not assess language quality by intuition.
- Perform supplementary audit: check that critical evidence is not buried in supplementary, supplementary content is complete, and journal limits are satisfied.
- Execute as an isolated subagent via `delegate_task`. Do not depend on parent session context.
- The evaluation is a gate. `reject` means stop. `stop_no_gain` means the revision did not improve the manuscript.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - manuscript_draft
    - article_blueprint
    - claim_audit_report
    - article_context_brief
    - methods_audit_report (optional, for context)
    - previous_evaluation_report (in re-evaluation mode)
  required_outputs:
    - evaluation_report (with language_assessment integration and supplementary_audit)
  may_read:
    - "06_drafts/**"
    - "04_blueprint/**"
    - "07_claim-audit/**"
    - "02_context/**"
    - "08_evaluations/**"
  may_write:
    - "08_evaluations/evaluation-v*.md"
  must_not_read:
    - "10_panel/**"
    - "09_revisions/**"
  must_not_write:
    - "06_drafts/**"
    - "04_blueprint/**"
  may_call:
    - academic-language-assessor
  must_not_call:
    - article-drafter
    - article-architect
    - article-claim-auditor
  failure_modes:
    - "academic-language-assessor unavailable → evaluate language dimension inline, mark language_assessment_mode: evaluator_inline_degraded"
    - "claim_audit_report missing → flag scope_limitation, evaluate evidence-claim alignment independently"
  escalation_route: "article-orchestrator"
```

## Seven Dimensions

| Dimension | Compensatory | Assessor |
|-----------|-------------|----------|
| Scientific Validity | **Non-compensatory** | Independent evaluation |
| Evidence-Claim Alignment | **Non-compensatory** | Claim audit report + independent check |
| Reporting Completeness | Compensatory | Reporting checklist mapping |
| Journal Fit | Compensatory | Journal adapter comparison |
| Clarity & Structure | Compensatory | Independent evaluation |
| Language & Academic Register | **Non-compensatory (gates)**; Compensatory (score) | `academic-language-assessor` |
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

### Language Baseline Gates (non-compensatory, from language assessor)

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
| `stop_no_gain` | Re-evaluation finds no improvement | **Stop** |

Decision logic:
- Any `fatal_scientific` gate fail → `reject`
- Any `language_baseline` gate fail → at least `revise`
- Any `genre_rhetoric` gate fail → at least `revise`
- All gates pass + scores adequate → `accept`

Fatal overclaim gate handling:
- Fixable fatal overclaim gate failure routes to `revise` with `claim_downscaling`, removal, or relocation.
- Unfixable fatal overclaim gate failure routes to `reject`.

## Output

Write `08_evaluations/evaluation-vNNN.md` containing dimension scores, gate results, supplementary audit, issue list with revision priorities, and decision.

The report must include `evaluation_id`, `artifact_id`, `draft_ref`, `draft_version`, and `independence_status`. If evaluation is not performed in a true isolated subagent, set `independence_status: inline_degraded`; that result may guide revision but cannot support `ready_for_author_signoff`.

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
- In re-evaluation mode, compare against the prior evaluation to detect `stop_no_gain`.

## Verification

- All seven dimensions scored with explicit severity
- All hard gates assessed, not skipped
- Language assessment integrated (not a separate report)
- Supplementary audit complete with all five checks
- Every issue has a `revision_priority` and `entry_strategy`
- Decision follows gate logic, not overall impression
- Re-evaluation includes comparison with prior evaluation

## References

- `references/evaluation-rubric.md`: Detailed 1–10 scoring anchors for each dimension.
- `references/evaluation-gates.md`: Complete hard gate definitions, thresholds, and consequences.
- `references/supplementary-audit-guide.md`: Criteria for critical evidence burial, completeness, and journal limit compliance.
- `article-orchestrator/references/artifact-contracts.md`: Canonical evaluation report schema.
- `article-orchestrator/references/handoff-validation.md`: Evaluator → refinement controller handoff gates.
