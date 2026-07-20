---
name: article-context-builder
description: "Inventory study materials and normalize authority, reader needs, and constraints."
---
# article-context-builder

## Purpose

After independent readiness triage, normalize the complete material inventory into a downstream context brief, classify study/article type, select reporting standards, and gate the handoff. Do not rejudge readiness, retrieve literature, design architecture, or draft content.

## Core Rules

- Normalize before classifying. Do not classify from raw, unnormalized input.
- Classify study type first, then select article type, then map reporting standard.
- A single study may require multiple reporting standards (e.g., RCT + cost-effectiveness → CONSORT + CHEERS).
- When no exact reporting guideline matches, record `no_exact_guideline_found` — do not force-fit.
- Journal-specific requirements override default reporting standards.
- For hybrid designs, select one primary standard plus auxiliary standards.
- Gate honestly: `clarification_stop` is a valid outcome, not a failure.
- Preserve the user's source-authority declaration separately from the material inventory. A sole semantic authority resolves conflicting meanings or version labels; it does not make compatible results, tables, figures, code, or technical reports disappear.
- Model the intended readers before drafting. Do not assume equal expertise across clinical, statistical, methodological, and domain audiences.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - raw_user_materials (study protocol, results, methods description, tables/figures, references)
    - article_readiness_report
  required_outputs:
    - article_context_brief
  may_read:
    - "00_input/**"
    - "01_readiness/**"
  may_write:
    - "02_context/context-brief.md"
  must_not_read: []
  must_not_write:
    - "04_blueprint/**"
    - "06_drafts/**"
  may_call: []
  must_not_call:
    - article-architect
    - article-drafter
  failure_modes:
    - "study_type cannot be determined → classify as unclear, mark confidence: low, gate as proceed_with_assumptions"
    - "user materials too thin → output clarification_stop with specific questions"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Normalize

Extract and standardize the following fields from raw user materials:

```yaml
context_brief:
  study_identity:
    research_question: ""
    hypothesis: ""                         # if applicable
    primary_objective: ""
    study_design: ""                       # standardized: randomized_controlled_trial | prospective_cohort | retrospective_cohort | case_control | cross_sectional | diagnostic_accuracy | prediction_model | systematic_review_and_meta_analysis | mechanistic_experimental | qualitative | mixed_methods | ai_ml | other
    design_label_from_author: ""           # author's own description, preserved verbatim
  population:
    target_population: ""
    sample_size: ""
    enrollment_period: ""
    key_eligibility: []
  intervention_exposure:
    intervention: ""                       # if interventional
    comparator: ""                         # if interventional
    exposure: ""                           # if observational
    primary_endpoint: ""
    secondary_endpoints: []
  data_summary:
    data_sources: []
    data_completeness: user_provided_sufficient | user_provided_partial | user_provided_minimal
    available_materials: []
    missing_materials: []
    complete_material_inventory: []
    semantic_authority:
      artifact_id: ""
      version: ""
      path: ""
      governs: []
      compatible_assets_retained: []
  reader_context:
    target_reader_profile: []
    reader_prior_knowledge: []
    knowledge_asymmetries: []
    terms_requiring_definition: []
    reader_reasoning_chain: []
    source_intent_coverage: []
    binding_constraints: []
    gap_type: knowledge | evidence | method | implementation | mixed | not_applicable
  source_confidence: high | medium | low   # how reliably fields were extracted
```

### Step 2: Classify

#### 2a. Study Type Classification

Map the study design to one of the standardized types using `references/study-type-taxonomy.md`.

#### 2b. Article Type Recommendation

Based on study type, evidence volume, and material scope:

| Condition | Article Type |
|-----------|-------------|
| Full study, multiple analyses, detailed methods | original_article |
| Single clear finding, simple design | brief_report |
| Preliminary/exploratory, small sample | research_letter |
| Primary contribution is a new method/tool | methods_article |
| Primary contribution is a dataset | data_descriptor |
| Single case or small series | case_report |
| No original data — synthesis of existing literature | review |

#### 2c. Reporting Standard Selection

Map study type to reporting standard using `references/reporting-standard-mapping.md`.

Output:

```yaml
reporting_standard_selection:
  primary_standard: ""                     # e.g., CONSORT, STROBE, PRISMA
  auxiliary_standards: []
  extension: ""                            # e.g., CONSORT-Outcomes 2022
  journal_override: ""                     # if journal imposes different standard
  no_exact_guideline_found: true | false
  rationale: ""
```

### Step 3: Gate

Produce one of three gate outcomes:

- `proceed`: All required fields populated with medium+ confidence.
- `proceed_with_assumptions`: Gaps exist but are non-blocking; assumptions documented.
- `clarification_stop`: Blocking user facts missing; return specific questions.

## Output

Write `02_context/context-brief.md` containing the full context brief YAML plus the gate outcome and any assumptions recorded.

## Stop Conditions

- `clarification_stop`: return the specific questions the user must answer.
- User materials contain no identifiable study design AND no research question → cannot proceed.

## Pitfalls

- Do not classify a study as RCT based on author label alone — verify against design description.
- Do not force a reporting standard when none fits. `no_exact_guideline_found` is honest and useful.
- Do not normalize away important ambiguity. Record it in assumptions.
- Do not skip the gate step. Every context brief must have a gate outcome.
- Do not merge this with readiness triage. Triage judges readiness; this standardizes input.

## Verification

- All `study_identity` fields populated or explicitly marked as unavailable
- Study type matches the design description, not just the author label
- Reporting standard mapping includes rationale
- Gate outcome is explicit with documented assumptions
- Missing materials are listed, not silently ignored
- Every supplied file is either included in `complete_material_inventory` or explicitly excluded with a reason; semantic-authority rules do not exclude compatible evidence assets
- The target-reader profile states expected prior knowledge, expertise asymmetries, term-definition needs, and the reasoning chain the article must support
- Source confidence is assessed

## References

- Read `references/study-type-taxonomy.md` when its named guidance or contract applies: Full study type classification taxonomy with definitions and edge cases.
- Read `references/reporting-standard-mapping.md` when its named guidance or contract applies: Study type → reporting standard mapping rules, multi-standard logic, extension priority, journal override.
- `references/reporting-standards/`: Item libraries for CONSORT, STROBE, PRISMA, TRIPOD, STARD, ARRIVE, COREQ, CHEERS, SQUIRE, CARE.
- Read `references/reporting-standards/README.md` when selecting or locating a reporting-standard item library.
- `article-orchestrator/references/artifact-contracts.md`: Canonical context brief schema.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory and naming conventions.
