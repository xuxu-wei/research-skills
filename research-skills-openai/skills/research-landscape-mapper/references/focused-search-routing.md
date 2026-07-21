# Focused Search Routing

Apply this overlay when `mode: focused`. Keep the surface decision from
`search-routing-rules.md`: focused work may use supplied sources or Built-in
Search, but still requires Deep Research when the task is multi-stage,
multi-direction, or multi-source synthesis.

## Freeze the question

Record the bounded question, downstream decision, population or system,
intervention/exposure/method, outcome/metric, time window, geography, source
classes, exclusions, and sufficiency criterion. Do not silently broaden them.

## Retrieval sequence

1. Verify supplied identifiers and reusable evidence.
2. Run the smallest set of exact or targeted queries likely to answer the
   bounded question.
3. Open primary or authoritative sources and verify the supporting passage,
   study context, and source identity.
4. Trace the strongest supporting and opposing source chains.
5. Expand only for unresolved conflict, a missing required source class, or a
   failed sufficiency criterion.
6. Stop with an evidence limitation when further retrieval has low expected
   value or the declared budget is exhausted.

## Relevance and source handling

- Include evidence only when it directly addresses the frozen question or is
  necessary to interpret it.
- Use reviews to locate and contextualize primary evidence; cite the source that
  actually supports each material claim.
- Treat preprints, abstracts, editorials, and indirect-domain evidence according
  to their real evidentiary role; do not upgrade them by venue or prominence.
- Do not infer absence from an inaccessible database, failed query, or language
  boundary.
- For clinical questions, match population, exposure/intervention, comparator,
  outcome, design, and care context as relevant.
- For computational or engineering questions, match task, dataset, split,
  metric, baseline, and evaluation protocol as relevant.

## Claim gate

For every material claim, record a readable label, source locator,
`support_status`, evidence confidence, and limitations. Use:

- `supported` only for directly verified, adequately corroborated evidence;
- `single-source` when only one verified source supports the claim;
- `weak` for indirect, limited, or low-quality evidence;
- `conflicting` when credible sources materially disagree;
- `access-limited` when required evidence cannot be inspected; and
- `unverified` when verification has not occurred.

Never discard a credible conflicting result to create a cleaner conclusion.
Record excluded high-salience sources only when their exclusion affects the
downstream decision, with a concise reason.

## Handoff

Report the frozen scope, route, queries or lookup targets, included and excluded
source classes, sufficiency result, claim statuses, conflicts, negative searches,
access limits, and whether further retrieval is required.
