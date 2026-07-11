---
name: article-architect
description: "Design the complete manuscript architecture before drafting: contribution statement, claim-evidence matrix, evidence provenance ledger, evidence display plan, supplementary index, results skeleton, journal adapter, and reviewer risk preview."
---
# article-architect

## Purpose

Design the complete article architecture before any drafting begins. The blueprint constrains the drafter, guides the claim auditor, and provides the evaluator with the intended structure.

This skill does NOT draft manuscript text, audit methods, evaluate quality, or retrieve literature.

## Core Rules

- Architecture before drafting. No blueprint means no manuscript.
- The Contribution Statement is the anchor. Every claim, display item, and section must trace back to it.
- Results organization mode must be explicitly chosen and justified.
- The EDP (Evidence Display Plan) determines where each piece of evidence appears: main text or supplementary.
- The Supplementary Index is a first-class output, not an afterthought.
- The EPL (Evidence Provenance Ledger) is seeded here and refined by drafter and claim-auditor.
- The Reviewer Risk Preview warns the user what a reviewer will likely flag — it is not the evaluation itself.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - article_context_brief
    - literature_grounding_report
    - article_readiness_report
  required_outputs:
    - article_blueprint (contribution_statement, claim_evidence_matrix, EDP, EPL, supplementary_index, results_skeleton, journal_adapter, reviewer_risk_preview)
  may_read:
    - "02_context/**"
    - "03_literature/**"
    - "01_readiness/**"
  may_write:
    - "04_blueprint/article-blueprint.md"
  must_not_read:
    - "06_drafts/**"
    - "08_evaluations/**"
    - "07_claim-audit/**"
  must_not_write:
    - "06_drafts/**"
  may_call: []
  must_not_call:
    - article-drafter
    - article-evaluator
    - article-claim-auditor
  failure_modes:
    - "insufficient evidence for primary claim → flag in reviewer_risk_preview, mark claim_confidence: low"
    - "context_brief missing key variable definitions → request context builder rework via orchestrator"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Contribution Statement

Define the single core contribution:

```yaml
contribution_statement:
  what_is_known: ""
  what_this_study_adds: ""
  primary_contribution_type: evidence | method | data | theory | refutation | replication | synthesis
  contribution_strength: major | moderate | incremental
  one_sentence_takeaway: ""               # ≤30 words
```

### Step 2: Study Type Confirmation + Core Q&A

Confirm or revise the study type from the context brief. Define the core question-answer pair:

```yaml
core_qa:
  question: ""
  answer: ""                              # ≤50 words
  evidence_summary: ""                    # what evidence supports this answer
```

### Step 3: Claim-Evidence Matrix

Map every claim to its supporting evidence:

```yaml
claim_evidence_matrix:
  - claim_id: "C001"
    claim_text: ""
    claim_type: primary | secondary | exploratory | methodological | contextual
    section_placement: Introduction | Methods | Results | Discussion
    supporting_evidence_ids: ["E001", "E002"]
    inference_type: direct_observation | statistical_inference | mechanistic_inference | literature_synthesis | assumption
    wording_strength_target: definitive | strong | moderate | cautious | speculative
    risk_of_overclaim: low | medium | high
```

### Step 4: Evidence Provenance Ledger (seed)

Seed the EPL with all evidence entries referenced by the claim-evidence matrix:

```yaml
evidence_provenance_ledger:
  schema_version: "research-article.v5"
  granularity: claim_level
  entries:
    - evidence_id: "E001"
      claim_ids: ["C001"]
      evidence_type: primary_data | secondary_data | experiment | statistical_result | literature_reference | user_assertion | assumption
      source_description: ""
      verification_status: verified | user_supplied_unverified | inferred | missing
      risk_level: low | medium | high
      notes: ""
```

### Step 5: Evidence Display Plan + Supplementary Index

Plan each display item's carrier and placement:

```yaml
evidence_display_plan:
  results_organization_mode: norm_driven | argument_driven | hybrid | artifact_driven | theory_driven | evidence_synthesis_driven
  mode_rationale: ""
  display_items:
    - display_id: "D001"
      supports_claims: ["C001"]
      carrier: table | figure | flowchart | in_text | supplementary_table | supplementary_figure
      placement: main | supplementary
      supp_id: "S1"                      # if placement = supplementary
      description: ""
      data_source: ""
      status: planned | draft_available | needs_creation

supplementary_index:
  schema_version: "research-article.v5"
  items:
    - supp_id: "S1"
      type: supplementary_table | supplementary_figure | supplementary_methods | supplementary_analysis | supplementary_note | data_deposition | code_repository
      title: ""
      content_summary: ""
      supports_claims: []
      supports_display_items: []
      referenced_from: ""
      required_by_reporting_guideline: true | false
      required_by_journal_policy: true | false
      status: planned
  journal_limits:
    max_supplementary_items: 0
    max_supplementary_files: 0
    supplementary_file_format: ""
    data_availability_policy: ""
    code_availability_policy: ""
  cross_reference_map: []
```

### Step 6: Results Skeleton

Define the Results section structure paragraph by paragraph:

```yaml
results_skeleton:
  - paragraph_id: "R-P01"
    topic: ""
    display_items: ["D001"]
    claims_delivered: ["C001"]
    key_numbers: []
    transition_from: ""
    transition_to: ""
```

### Step 7: Journal Adapter

```yaml
journal_adapter:
  target_journal: ""
  article_types_available: []
  word_limit: 0
  abstract_limit: 0
  display_item_limit: 0
  reference_limit: 0
  supplementary_policy: ""
  structured_abstract_required: true | false
  key_structural_requirements: []
  formatting_checklist: []
```

### Step 8: Reviewer Risk Preview

Anticipate what a reviewer will question:

```yaml
reviewer_risk_preview:
  - risk_id: "R001"
    concern: ""
    severity: likely_fatal | major_concern | minor_concern | stylistic
    section: ""
    related_claim: ""
    preemptive_action: ""                # what the manuscript can do now to mitigate
```

## Output

Write `04_blueprint/article-blueprint.md` containing all eight sections above.

## Pitfalls

- Do not place primary evidence in supplementary materials to save space.
- Do not skip the results organization mode selection — it determines paragraph ordering.
- Do not seed the EPL with fabricated or guessed evidence sources.
- Supplementary Index must be complete; missing items here become missing items at submission.
- The Reviewer Risk Preview is not the evaluation. It flags likely reviewer concerns, not quality judgments.

## Verification

- Contribution statement is specific and ≤30 words for the one-sentence takeaway
- Every claim in the matrix has at least one evidence entry in the EPL
- Every display item has a carrier and placement decision
- Supplementary Index covers all supplementary-bound items with main-text reference locations
- Results organization mode has an explicit rationale
- Journal adapter lists concrete constraints, not generic descriptions
- Reviewer risk preview names specific concerns, not "may have limitations"

## References

- `references/results-organization-modes.md`: Detailed definitions and selection criteria for the six organization modes.
- `references/claim-taxonomy.md`: Claim types, inference types, and wording strength calibration.
- `article-orchestrator/references/artifact-contracts.md`: Canonical blueprint, EDP, EPL, and supplementary index schemas.
- `article-orchestrator/references/evidence-provenance-ledger-schema.md`: EPL granularity tiers and field rules.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory and naming conventions.
- `article-orchestrator/references/handoff-validation.md`: Blueprint → drafter handoff gates.
