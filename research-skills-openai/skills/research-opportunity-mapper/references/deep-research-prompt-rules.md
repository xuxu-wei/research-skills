# ChatGPT Deep Research Rules

Load this file only when the task needs multi-stage, multi-direction, or
multi-source synthesis. If Deep Research is inactive or unknown, create a
self-contained continuation package, return `deep_research_handoff_required`,
and stop. Do not imitate Deep Research with ordinary chat or Built-in Search.

## Required package sections

1. **State binding:** workflow ID, round ID, pending edge ID, plugin version,
   frozen input logical references (`artifact_id`, `version`, `path`), and the
   exact resume target.
2. **Research objective:** one bounded question or landscape objective, why it
   matters to the downstream decision, and what decision the evidence will
   inform.
3. **Route profile:** `standard | focused | divergent`, source priorities,
   dates, languages, geographies, required and excluded source classes, budget,
   and stop condition.
4. **Current evidence:** verified facts, unresolved claims, known conflicts,
   inaccessible sources, and searches already completed. Do not present planned
   searches as completed.
5. **Search plan:** staged retrieval with source verification and citation
   tracing, adapted to the route profile.
6. **Extraction fields:** source identity, design/method, population/sample/data,
   exposure/intervention, outcome/metric, findings, uncertainty, limitations,
   contradictions, and stable locator when relevant.
7. **Output contract:** search summary, source table, claim table, conflicts,
   negative/inaccessible searches, remaining gaps, and limitations.
8. **Return contract:** required local filename or artifact type, source links,
   completion signal, returned artifact logical reference, and instructions to
   resume only the named pending edge.

## Search plan

- **Landscape:** establish terminology, major source classes, established
  findings, and disagreements.
- **Verification:** open and trace the primary or authoritative sources behind
  material claims; distinguish source statements from synthesis.
- **Gap resolution:** target unresolved conflicts and missing required source
  classes, then document negative and access-limited searches.

Do not force all three stages when the approved focused plan is narrower. Do not
stop at snippets or search-result summaries for material claims.

## Mode adjustments

### Standard

Cover the direct field, major contrary evidence, and only those adjacent sources
needed for the downstream decision. Stop at declared decision sufficiency.

### Focused

Freeze one question and prioritize directly relevant sources. Verify the
strongest supporting and opposing evidence, perform a brief targeted gap check,
and stop when the sufficiency criterion is met or an evidence limitation is
established.

### Divergent

Use distinct search lanes for direct, contrary, alternative-method, emerging,
and justified adjacent-field evidence. Record each transfer rationale. Preserve
analogy and emerging signals without upgrading them to direct support.

## Claim contract

Every material claim must include a readable label, source locator,
`support_status: supported | weak | conflicting | single-source | unverified |
access-limited`, evidence confidence, and limitations. Use `single-source` when
only one verified source supports a claim. A Deep Research report is not itself
independent corroboration of the sources it summarizes.

## Domain adaptation

- For clinical or health questions, extract study design, population, setting,
  intervention/exposure, comparator, outcomes, effect estimates, and applicable
  guideline or consensus context.
- For computational, statistical, or engineering questions, extract task,
  dataset, split, baseline, metric, evaluation protocol, reproducibility facts,
  and venue/version identity.
- For qualitative or mixed-methods questions, extract sampling, setting,
  analytic approach, reflexivity/triangulation facts when reported, themes, and
  transfer limits.

Apply only fields relevant to the question. Record language, geography, and
access limits rather than inferring no evidence.

## Scope boundary and return

Retrieve and synthesize evidence only. Do not generate or rank Ideas, draft a
proposal/protocol, or make an evaluator decision. When the report returns, the
mapper verifies source identity and material locators, converts findings into
Evidence and Opportunity Maps, preserves conflicts and access limits, records
the returned artifact's ID, version, and path, and resumes the named pending
edge once.
