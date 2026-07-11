# Search Routing Rules

The mapper owns retrieval planning and retrieval execution. Orchestrators provide task scope, constraints, existing evidence artifacts, and resource budget; they do not directly call retrieval tools for evidence mapping.

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
