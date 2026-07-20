# ChatGPT Deep Research Continuation Package

## State binding

- Handoff status: `deep_research_handoff_required`
- Workflow ID / round ID / pending edge ID:
- Plugin version:
- Frozen input logical refs (`artifact_id`, `version`, `path`):
- Resume target:
- Expected returned artifact path or type:

Resume only the pending edge named above. Do not reuse this return for another
workflow edge.

## Research objective

- Core question or landscape objective:
- Downstream decision this evidence informs:
- Why the question matters:
- Required sufficiency criterion:

Retrieve and synthesize evidence. Do not generate or rank research Ideas, draft
a proposal/protocol, or make an evaluator decision.

## Route profile

- Mode: `standard | focused | divergent`
- Domain:
- Date/freshness boundary:
- Languages and geographies:
- Required and preferred source classes:
- Excluded source classes and reasons:
- Search budget or breadth boundary:
- Stop condition:

Mode adjustment:

- `standard`: cover the direct landscape, major conflicts, and decision-relevant
  adjacent evidence.
- `focused`: freeze one bounded question; verify the strongest for/against
  evidence and perform a short targeted gap check.
- `divergent`: use distinct direct, contrary, alternative-method, emerging, and
  justified adjacent-field lanes; record each transfer rationale.

## Current evidence and unresolved claims

- Verified facts with source locators:
- Claims requiring verification:
- Known conflicts:
- Searches already completed:
- Inaccessible sources or known coverage limits:

Do not describe planned retrieval as completed evidence.

## Search plan

1. **Landscape:** questions and terminology; priority sources and queries;
   expected evidence.
2. **Verification:** material claims and source chains; supporting and opposing
   evidence; identity and version checks.
3. **Gap resolution:** missing source classes or conflicts; negative searches;
   final sufficiency check.

For a narrowly approved focused task, omit unnecessary stages but retain source
verification, a sufficiency check, and limitations.

## Required extraction

For each material source, capture as applicable: full citation and direct URL or
stable identifier; source type and version/date; design/method; population,
sample, dataset, or setting; intervention/exposure/comparator; outcome or metric;
key findings and estimates; limitations; conflicts; and the exact supporting
locator.

For each material claim, record:

| Claim label | Claim | Sources and locators | Support status | Evidence confidence | Conflicts and limitations |
|---|---|---|---|---|---|

Use only `supported | weak | conflicting | single-source | unverified |
access-limited` for support status.

## Required return

1. Search-plan completion summary.
2. Verified source table with direct links or stable identifiers.
3. Claim table using the required support-status vocabulary.
4. Conflicts and plausible explanations without forced consensus.
5. Negative searches, inaccessible sources, and coverage limits.
6. Remaining evidence gaps and whether the sufficiency criterion was met.
7. Concise synthesis that distinguishes source statements from report-level
   inference.

Save or return the report as the named artifact, include its completion time,
and preserve the workflow, round, pending-edge, returned-artifact ID, version,
and path for single-edge resume.
