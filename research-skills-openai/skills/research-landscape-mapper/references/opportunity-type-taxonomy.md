# Opportunity Type Taxonomy

Use these categories when constructing the Opportunity Map. Categories are organized by mode: core types are always available; exploration types are enabled in Divergent mode and may appear opportunistically in Standard mode. They should not appear in Focused mode.

## Core Types (all modes)

- `gap`: a research question or area not adequately addressed.
- `value`: important scientific, clinical, engineering, social, or user need.
- `method`: method limitation or opportunity for improved approach.
- `data`: underused, newly available, missing, or poorly integrated data.
- `metric`: weak endpoint, outcome, benchmark, or evaluation measure.
- `failure`: known implementation, deployment, reproducibility, translation, or adoption failure.
- `theory`: conceptual, mechanistic, or explanatory gap.
- `benchmark`: need for better comparison set, task, dataset, baseline, or stress test.
- `taxonomy`: need for classification, framework, typology, or conceptual ordering.
- `implementation`: opportunity in real-world workflow, delivery, adoption, or operationalization.

## Exploration Types (Divergent mode enabled; Standard mode opportunistic; Focused mode disabled)

These are deliberately speculative and should carry lower confidence labels (`speculative`, `low-confidence`, `unverified`).

- `analogy`: a problem solved in a different domain whose method, data, or conceptual approach could transfer. Key question: "who else has solved something structurally similar?" Requires a stated relevance rationale (not random cross-domain jumps).
- `tension`: two or more findings that conflict, suggesting a deeper unresolved question. Key question: "where does the evidence disagree, and what question would explain the disagreement?"
- `trend`: an emerging direction not yet fully defined — possible entry points before the field consolidates. Key question: "what are people starting to talk about but haven't formalized yet?"
- `reframing`: the same problem redefined from a different perspective (different endpoint, different population, different timescale, different causal model). Key question: "if we changed one core assumption, what would the research question become?"
- `wildcard`: low-probability high-impact speculation; a "what if" that current evidence cannot rule out. Key question: "what's the most interesting possibility that almost no one is talking about?"

`cross-domain` was removed as a standalone type. Cross-domain exploration is a retrieval strategy (see `references/divergent-search-routing.md`), not an opportunity type. Opportunities discovered from cross-domain retrieval should be classified under `analogy`, `method`, `reframing`, or other types based on their nature.

## Classification Rules by Exploration Level

| Exploration Level | Allowed Types | Default Type Mix |
|---|---|---|
| Standard (S) | Core types; exploration types only when evidence naturally supports them | ~80% core, ~20% exploration |
| Divergent (D) | Core + exploration types | ~30% core, ~70% exploration |
| Focused (F) | Core types only | 100% core |

- Assign the most useful primary type. Add secondary types only when they affect generation routing.
- Do not create a full idea here. Each opportunity must link to supporting evidence or be marked `unverified`.
- **Divergent mode**: exploration-type opportunities may outnumber core-type opportunities. This is expected — the evaluator and generator will later filter.
- **Focused mode**: exploration types must not appear.
- Every opportunity must carry an exploration flag: `exploratory` (speculative, breadth-seeking) or `focused` (narrowing, verification-oriented).

## Confidence Rules by Exploration Level

| Exploration Level | Confidence bar for inclusion | Labeling |
|---|---|---|
| Divergent (D) | Loose — "plausible and interesting" is sufficient | Most items marked `speculative`, `low-confidence`, or `unverified` |
| Standard (S) | Medium — at least one supporting source or clear logical chain | Mixed confidence labels |
| Focused (F) | Strict — needs direct evidence support | Most items marked `supported` or `likely` |
