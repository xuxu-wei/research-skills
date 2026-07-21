# Deep Research Prompt and Return Rules

## Contents

- [When to use Deep Research](#when-to-use-deep-research)
- [Continuation package](#continuation-package)
- [Direct-send request](#direct-send-request)
- [Length and compression](#length-and-compression)
- [Search and synthesis requirements](#search-and-synthesis-requirements)
- [Return assessment](#return-assessment)
- [Continuation state](#continuation-state)

## When to use Deep Research

Use Deep Research for a major multi-stage, multi-direction, or multi-source
landscape whose result changes a core claim, novelty position, evidence
landscape, or material conflict. Do not chain focused syntheses to imitate it.

If Deep Research is inactive or unknown, create the continuation package,
return `deep_research_handoff_required`, and stop. Do not use ordinary chat or
Built-in Search as a substitute for the returned report.

## Continuation package

Create exactly two outgoing files:

```text
deep-research/round-NNN/
├── deep-research-request-vNNN.md
└── deep-research-follow-up-guide-vNNN.md
```

Save the returned report as `deep-research-report-vNNN.md` in the same round.
The request is the only file sent to Deep Research. The follow-up guide is for
the researcher who transfers the request and returns the report.

Run `scripts/validate_deep_research_package.py` before returning the package.

## Direct-send request

Everything from the first heading through the end of
`deep-research-request-vNNN.md` is the exact prompt. It must be understandable
without local workflow knowledge and contain these sections in order:

1. Research objective and intended use
2. Core research question
3. Scope and boundaries
4. Known background and unresolved issues
5. Questions to answer
6. Search scope and source requirements
7. Analysis and synthesis requirements
8. Report structure
9. Citation and link requirements
10. Completion criteria

Do not include workflow IDs, round or edge IDs, plugin versions, artifact IDs,
local paths, state names, resume instructions, SHA/digests, or other local
orchestration language. Name an attachment only when it is genuinely supplied;
the prompt must still explain the task without requiring the attachment merely
to discover the core question.

## Length and compression

- Keep the empty template at or below 4,000 Unicode characters, including the
  compact citation examples.
- Prefer 2,500–6,000 characters for a rendered request.
- Treat more than 8,000 characters as a warning.
- Never exceed 12,000 characters.
- Do not pad a short but complete request.

If a request is too long, compress in this order:

1. remove internal instructions and repeated boundaries;
2. summarize known evidence, conflicts, and key sources;
3. merge questions that lead to the same decision;
4. move long source lists or background material to named attachments.

Never truncate the core question, decision-changing scope, required comparison,
contrary-evidence search, report structure, or citation requirements.

## Search and synthesis requirements

- Establish the direct field, closest relevant work, and material contrary
  evidence. Add adjacent fields only when their relevance is explained.
- Verify primary or authoritative sources behind material claims; do not rely on
  snippets or search-result summaries.
- Distinguish source findings from report-level inference.
- Record negative, inaccessible, conflicting, and access-limited evidence.
- Adapt extraction fields to the domain rather than forcing irrelevant fields.
- Do not generate or rank research Ideas, draft a proposal or protocol, or make
  a downstream evaluator decision.

For clinical questions, capture design, population, setting,
intervention/exposure, comparator, outcomes, estimates, and applicable guidance.
For computational or engineering questions, capture task, dataset, split,
baseline, metric, evaluation protocol, and reproducibility facts. For
qualitative work, capture sampling, setting, analysis, reported reflexivity or
triangulation, themes, and transfer limits.

Every formal reference must have a GB/T 7714—2015 citation and complete
canonical link. When a user supplied only a citation clue, apply the shared
citation-record contract and label the identification and verification status.
Treat each atomic claim as the citation unit: bind one to five direct-support
works, place each clickable reference group next to the clause it supports, and
split a sentence into several claim IDs when its clauses need different
sources. Keep the compact format examples in the direct-send request.

## Return assessment

Preserve the raw report. The mapper verifies material source identities and
locators, integrates accepted findings into a new Evidence Map and any
profile-required Opportunity Map, and records:

```yaml
deep_research_return:
  report_ref: {artifact_id: "", version: "", exact_path: ""}
  decision: accepted | revision_required | supplemental_search_required
  main_question_coverage: sufficient | partial | insufficient
  subquestion_coverage: sufficient | partial | insufficient
  claim_source_traceability: passed | failed
  citation_and_link_completeness: passed | failed
  closest_work_coverage: sufficient | partial | insufficient | not_applicable
  contrary_evidence_coverage: sufficient | partial | insufficient
  applicability_bounds_explicit: true | false
  novelty_evidence_usable: true | false
  unresolved_items: []
repairability_assessment:
  core_scientific_answer: usable | partially_usable | unusable
  evidence_landscape: recoverable | materially_incomplete | invalid
  source_identity_recoverability: high | moderate | low
  selected_route: deterministic_normalization | built_in_search_and_agent_repair | focused_literature_synthesis | second_deep_research
  severe_conditions_met: []
  prior_lower_cost_repairs_attempted: []
  route_reason: ""
  owner_approval_required: false
```

An accepted report is direct evidence for novelty assessment and has no lower
standing than a formal novelty search. Acceptance still depends on the fields
above. `revision_required` describes the report; it does not select the next
retrieval route.

## Post-return repair ladder

Use the least costly route that can recover the scientific evidence:

1. split compound statements into atomic claims and restore stable claim/source
   bindings;
2. deterministically normalize links, tracking parameters, duplicate works,
   and reference records while preserving the raw return;
3. use Built-in Search and agent reasoning to verify identities, metadata,
   locators, corrections, closest work, and contrary evidence;
4. rebuild the Evidence Map and obtain a fresh review;
5. request one focused synthesis only when the remaining question is bounded to
   two to five papers;
6. recommend a second Deep Research run only after the lower-cost repairs were
   actually attempted and a fresh reviewer still finds the core scientific
   answer or evidence landscape unusable.

Citation formatting, tracking parameters, aggregator links, missing locators,
an unclosed reference table, recoverable compound-claim bindings, recoverable
DOI or journal errors, access limits, or partial noncritical subquestions never
justify a second Deep Research run by themselves. The number of citation errors
is not decisive when the underlying works remain recoverable.

A second run requires at least one severe scientific condition: the report
answers the wrong core question or scope; the core answer is unusable and cannot
be reconstructed; a decision-changing evidence direction such as closest or
contrary work is wholly absent; central evidence is fabricated, unrecoverable,
or materially opposite to the cited source; or the landscape is materially
one-sided or invalid. Set `owner_approval_required: true`, obtain explicit owner
approval, and only then create a new continuation package. Do not prepare a
second-round package speculatively.

## Continuation state

Keep local binding outside the sendable request:

```yaml
deep_research_continuation:
  round: 1
  request_ref: {artifact_id: "", version: "", exact_path: ""}
  follow_up_guide_ref: {artifact_id: "", version: "", exact_path: ""}
  expected_report_path: ""
  originating_evidence_route: ""
  resume_consumer: ""
  status: prepared | report_received | accepted | revision_required | supplemental_search_required
```

Use logical references and exact paths. Do not store hashes or digests.
