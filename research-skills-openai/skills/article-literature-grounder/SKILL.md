---
name: article-literature-grounder
description: "Build an auditable literature-grounding report for an article, covering search scope, novelty position, competing evidence, coverage limits, and citation risk."
---
# article-literature-grounder

## Purpose

Ground a research study in its literature context before architecture and drafting begin. Answer: what is known, what is the gap, where does this study sit, and what competing evidence exists.

This skill does NOT design the manuscript architecture, draft content, judge readiness, or decide novelty claims. It provides the literature foundation that `article-architect` and `article-drafter` consume.

## Core Rules

- Every search must be auditable: record databases, queries, dates, and inclusion/exclusion logic.
- Cover five dimensions: seminal literature, recent literature, competing/contradictory evidence, prior reviews/guidelines, and citation prerequisites.
- Assess coverage honestly. `partial` coverage on a dimension is better than silent gaps.
- Prioritize guidelines/consensus → landmark studies → systematic reviews → recent original studies → editorials.
- When confidence is low, call `research-opportunity-mapper` for supplementary retrieval.
- Do not fabricate references. If a reference cannot be verified, mark it `verification_status: unverified`.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - article_context_brief
  required_outputs:
    - literature_grounding_report
  may_read:
    - "02_context/**"
    - "01_readiness/**"
  may_write:
    - "03_literature/literature-grounding.md"
  must_not_read:
    - "04_blueprint/**"
    - "06_drafts/**"
    - "08_evaluations/**"
  must_not_write:
    - "04_blueprint/**"
    - "06_drafts/**"
  may_call:
    - research-opportunity-mapper
  must_not_call:
    - article-architect
    - article-drafter
    - article-evaluator
  failure_modes:
    - "no relevant literature found → record empty coverage, flag novelty_claim_risk: high"
    - "search results dominated by low-quality sources → widen search, record quality concern"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Define Search Scope

Extract from the context brief:

- Research question and PICO/PECO elements
- Study type (informs what kind of literature is relevant)
- Target journal (informs citation expectations)
- Known key references from user materials

### Step 2: Execute Structured Search

Search across relevant databases using defined queries.

Record the search protocol:

```yaml
search_protocol:
  databases_searched: []
  search_queries: []
  date_searched: ""
  date_range: ""
  inclusion_logic: ""
  exclusion_logic: ""
  source_priority:
    - guidelines
    - landmark_trials_or_studies
    - systematic_reviews
    - recent_original_studies
    - editorials_or_commentaries
```

### Step 3: Assess Coverage

Evaluate coverage across five dimensions:

```yaml
coverage_assessment:
  seminal_literature_covered: yes | partial | no | unclear
  recent_literature_covered: yes | partial | no | unclear
  conflicting_literature_checked: yes | partial | no
  prior_reviews_guidelines_covered: yes | partial | no | unclear
  citation_prerequisites_met: yes | partial | no
```

### Step 4: Map Novelty Position

Position the study against existing literature:

```yaml
novelty_position:
  gap_type: evidence_gap | methodological_gap | population_gap | replication | extension | confirmation | refutation
  prior_evidence_summary: ""
  what_this_study_adds: ""
  novelty_claim_confidence: high | medium | low
  novelty_claim_risk: high | medium | low    # risk that novelty claim is undermined by existing literature
```

### Step 5: Identify Competing Evidence

```yaml
competing_evidence:
  - study_ref: ""
    finding: ""
    direction: consistent | inconsistent | partially_consistent
    quality_assessment: high | medium | low
    need_to_address: true | false
```

### Step 6: Assess Citation Risk

```yaml
citation_risk:
  missing_seminal_references: []
  missing_competing_evidence_references: []
  self_citation_balance: appropriate | excessive | insufficient
  reference_format_readiness: ready | needs_formatting | incomplete
```

## Output

Write `03_literature/literature-grounding.md` containing the full grounding report with all sections above.

## Stop Conditions

- Context brief lacks a research question → cannot define search scope → stop.
- All five coverage dimensions return `no` or `unclear` after search + mapper call → flag as critical gap.

## Pitfalls

- Do not present a one-sided literature picture. Conflicting evidence must be recorded.
- Do not inflate coverage. `partial` with documentation is more useful than `yes` without.
- Do not treat editorials as equivalent to systematic reviews in source priority.
- Do not assert novelty without checking for prior similar studies.
- Do not fabricate or guess references.

## Verification

- Search protocol is complete and reproducible
- All five coverage dimensions assessed
- Competing evidence explicitly searched for and recorded
- Citation risk assessment includes specific missing references (not just "may be missing")
- Novelty position is grounded in literature, not just user assertion
- `research-opportunity-mapper` was called if coverage is `partial` or `no` on key dimensions

## References

- Read `references/literature-search-protocol.md` when its named guidance or contract applies: Detailed search methodology, database selection guide, query construction rules.
- Read `references/novelty-assessment-guide.md` when its named guidance or contract applies: Gap-type definitions, novelty claim evaluation framework.
- `article-orchestrator/references/artifact-contracts.md`: Canonical literature grounding report schema.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory and naming conventions.
- `article-orchestrator/references/evidence-confirmation-and-routing.md`: Evidence gate and routing rules.
