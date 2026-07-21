# Search Routing Rules

## Contents

- [Evidence-change decision](#evidence-change-decision)
- [Routing by domain](#routing-by-domain)
- [Reuse before retrieval](#reuse-before-retrieval)
- [Retrieval depth](#retrieval-depth)
- [Routing output](#routing-output)

## Evidence-change decision

Record this decision before new retrieval during an iteration:

```yaml
evidence_change_assessment:
  materiality: none | bounded | major
  change_type:
    - citation_identity
    - single_claim_support
    - core_claim
    - novelty_position
    - evidence_landscape
    - material_conflict
  selected_route: reuse_existing_evidence | built_in_search | focused_literature_synthesizer | research_landscape_mapper
  route_reason: ""
```

The mapper request also records:

```yaml
consumer_workflow: idea | proposal | perspective | article | research_polisher
output_profile: evidence_only | evidence_and_opportunity | idea_landscape
retrieval_mode: auto | built_in_web_search | deep_research
exploration_mode: standard | focused | divergent
```

Use `auto` in production unless the researcher explicitly selects a search
mode. A test fixture may force one mode. A forced Built-in Search run must not
silently switch to Deep Research; report remaining coverage limits instead. A
forced Deep Research run must not use ordinary Search as a substitute for the
returned report.

- `none`: reuse verified evidence whose scope and freshness still match.
- `bounded`: use Built-in Search for an exact source or claim; use
  `focused-literature-synthesizer` only when 2-5 papers require close full-text
  synthesis.
- `major`: use `research-landscape-mapper`, which chooses broad Built-in Search
  or Deep Research.

Do not route editorial or language-only changes to retrieval. Do not chain
multiple focused syntheses to approximate field-level Deep Research.

The mapper owns broad retrieval planning and execution. Orchestrators classify
materiality and provide task scope, constraints, existing evidence artifacts,
resource budget, consumer workflow, and output profile. Within an orchestrated
workflow, the mapper returns one bounded focused-synthesis request to the parent
orchestrator rather than creating a hidden nested chain.

Use ChatGPT/Codex built-in Search for quick, recent, or targeted retrieval. Use ChatGPT Deep Research for multi-stage, multi-direction, multi-source synthesis. If Deep Research is needed but the current task is not running in that mode, save a self-contained continuation package, return `deep_research_handoff_required`, and pause.

## Routing by Domain

### Clinical / Medical / Life Science

Use targeted retrieval first. Recommended sources:
- PubMed
- clinical guidelines
- consensus statements
- systematic reviews
- major professional society documents

Use this route when guideline alignment, clinical relevance, safety, or diagnostic/therapeutic claims matter.

### AI / ML / Engineering / Statistics

Use targeted retrieval first. Recommended sources:
- arXiv
- Semantic Scholar
- OpenAlex or CrossRef when DOI or metadata verification is needed
- conference or venue pages when relevant

### Chinese Literature

Use `chinese-literature-access-rules.md`. If access is blocked or CAPTCHA/manual access is required, record the limitation and do not infer absence of evidence.

### Broad Topic

Use iterative literature search:
1. breadth search;
2. depth tracing;
3. targeted gap filling.

## Reuse Before Retrieval

If an Evidence Map is provided, decide first whether it can be reused.

Reuse only when:

- the scope matches the current task;
- source records are present;
- key claims are not stale for the domain;
- there are no unresolved conflicts that affect the current task;
- the downstream task does not require stronger evidence than the existing map provides.

If reuse is valid, emit `reuse_existing_evidence` and do not repeat retrieval.

## Retrieval Depth

- `targeted_retrieval`: default for most tasks; use a small number of high-priority queries or source lookups.
- `deep_research`: use when the topic is broad, evidence conflicts, novelty/gap claims are central, or multiple search directions must be synthesized.
- `stop_with_evidence_limitation`: use when required retrieval cannot be performed or would exceed the available budget.

## Routing Output

For each route, include route name, reason, expected evidence type, priority, queries or lookup targets, tool/source used, status, limitations, and whether follow-up retrieval is optional or required.
