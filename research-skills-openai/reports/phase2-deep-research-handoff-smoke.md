# Phase 2 Inactive Deep Research Handoff Smoke Test

The scenario requires multi-direction, multi-source synthesis, while Deep
Research is inactive or unknown in the current task. The mapper therefore
pauses instead of imitating Deep Research.

```yaml
workflow_id: phase2-smoke-consort-extensions
round_id: retrieval-round-001
handoff_status: deep_research_handoff_required
research_question: >-
  How should a research-article workflow apply CONSORT 2025 across general
  randomized trials and relevant cluster, non-inferiority, harms, outcomes,
  routinely collected data, and AI extensions, and what changed from CONSORT
  2010 that affects authoring and verification?
downstream_decision: >-
  Update reporting-standard selection and final checklist verification without
  applying irrelevant extensions.
exploration_mode: standard
scope:
  include:
    - CONSORT 2025 statement and explanation/elaboration
    - CONSORT 2010 comparison
    - named extensions relevant to design, intervention, outcome, and AI use
  exclude:
    - non-randomized study reporting guidelines
    - generic commentary without guideline authority or primary support
date_window: "2010-01-01 through 2026-07-12"
languages: [English]
geographies: [global]
required_source_classes:
  - official guideline-developer pages and checklists
  - primary statement and explanation/elaboration papers
  - authoritative reporting-guideline registry records
preferred_domains:
  - consort-spirit.org
  - equator-network.org
  - bmj.com
  - jama.com
  - thelancet.com
  - nature.com
  - journals.plos.org
excluded_sources:
  - unsourced summaries
  - search snippets used without opening the source
queries:
  - CONSORT 2025 statement checklist explanation elaboration changes from 2010
  - CONSORT 2025 cluster non-inferiority harms outcomes extensions applicability
  - CONSORT AI extension relationship to CONSORT 2025
claims_to_verify:
  - current checklist size and structure
  - exact changes from the 2010 statement
  - extension selection rules by randomized-trial design and reporting need
  - whether older extensions remain applicable with CONSORT 2025
evidence_table_fields:
  - claim_id
  - source_title
  - source_class
  - DOI_or_stable_URL
  - publication_or_update_date
  - supporting_passage_or_item
  - applicability
  - conflict_or_limitation
citation_requirements:
  - direct links or DOI/PMID for every material claim
  - distinguish opened full source from registry metadata
  - cite primary or official sources preferentially
current_evidence_summary:
  - EQUATOR and the official SPIRIT-CONSORT site identify CONSORT 2025 as current.
  - The official site describes a 30-item checklist and flow diagram.
  - The statement was published in five journals; extension synthesis remains incomplete.
included_artifact_ids:
  - phase2-targeted-search-smoke-v001
known_limitations:
  - no systematic comparison of the 2010 and 2025 item-level checklists yet
  - extension compatibility and supersession have not been synthesized
  - some journal pages may be access-limited
return_contract:
  required_sections:
    - search plan and executed queries
    - cited findings by evidence direction
    - item-level change table
    - extension applicability matrix
    - conflicts and inaccessible sources
    - negative searches and remaining gaps
    - source list with stable identifiers or direct links
  handback_statuses:
    - deep_research_complete
    - deep_research_partial
    - deep_research_blocked
```

Status: `deep_research_handoff_required`
Execution: paused pending a ChatGPT Deep Research task.
