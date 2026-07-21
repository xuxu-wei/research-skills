---
name: focused-literature-synthesizer
description: "Synthesize one bounded academic question from 2-5 closely read papers; use for narrow method, marker, finding, or figure questions."
---
# Focused Literature Synthesizer

Use this skill for requests such as:

- "What markers do studies on topic X usually measure?"
- "What do results sections in this field usually report?"
- "Show me a typical figure for this disease model or pathway."
- "What experimental methods are commonly used in this literature?"

The goal is not just to find papers. The goal is to read enough of the right papers to give the user a structured, directly useful answer.

## Eligibility Gate

Use this skill only when all conditions hold:

- the question is narrow enough to answer from 2-5 carefully selected papers;
- the requested output is a focused synthesis, not a comprehensive evidence map, novelty landscape, systematic review, or research-gap analysis;
- the source, population/problem, method, marker, result type, or figure type can be stated precisely enough to guide a small search.

If more than five papers, several evidence directions, broad field coverage, or iterative gap mapping are needed, route to `research-landscape-mapper`. Do not broaden this skill into Deep Research.

## Search Capability Routing

- Use ChatGPT/Codex built-in Search for targeted discovery, current literature checks, exact source verification, and opening candidate papers.
- Require live search when recency is material. If only indexed/cached results are available, state the freshness limitation.
- If the question requires multi-stage synthesis across several evidence directions or source classes, stop this skill and route to `research-landscape-mapper`, which owns Deep Research handoffs.
- Do not encode product-internal tool function names. Describe the required capability, source scope, and output contract.

## Two Output Modes

Choose the mode that best matches the user request.

### Body Mode

Use when the user asks about:

- molecules or markers commonly measured
- methods commonly used
- what findings usually appear in Results sections

Organize the answer by experiment type or finding category, not by paper.

### Figure Mode

Use when the user asks for:

- a typical figure in a topic
- how findings are visually presented
- figure captions or representative panels

Organize the answer by figure, with source attribution and caption context.

## Workflow

### 1. Clarify The Research Question

Identify:

- the topic or disease area
- whether the user wants methods, markers, findings, or figures
- whether the user named a specific journal, database, or URL
- whether the topic is biomedical or from another field

If the topic is biomedical, translate the idea into standard English search terms and prefer controlled vocabulary when possible.

### 2. Respect Source Scope First

If the user specifies a source, that scope is binding.

Examples:

- if the user says PubMed, do not mix in Google Scholar
- if the user names specific journals, search only those journals
- if the user gives a URL, read that source directly before searching elsewhere

Do not silently broaden the source list.

### 3. Build Search Terms Carefully

Use English search terms for database queries, even if the conversation is in Chinese.

For biomedical topics:

- prefer MeSH or other standardized vocabulary when available
- generate a few close variants or synonyms
- keep journal names exact when filtering by journal

Detailed query construction tips are in [references/query-guide.md](./references/query-guide.md).

### 4. Search For Candidate Papers

Prefer the best database for the topic:

- biomedical: PubMed or PMC first
- quantitative or engineering topics: field-appropriate databases
- broad discovery: web search only when a better native source is unavailable

Aim to identify 2-5 relevant papers with accessible full text. A few well-read papers are better than many shallow hits. If five papers are insufficient after focused query refinement, stop and route to `research-landscape-mapper` rather than continuing to accumulate sources.

### 5. Verify Source Membership Before Citing

Before you cite a paper as belonging to a target journal or source, verify it.

Check:

- journal field on the abstract page or database result
- exact source metadata in the database
- whether the paper truly matches the user-specified scope

Do not attribute a paper to a journal or database unless you confirmed it.

### 6. Read Full Text Strategically

Abstract-only answers are usually not enough.

Read:

- Methods, Results, and Discussion for Body Mode
- figure captions plus the relevant Results text for Figure Mode

If full text is not available, say that clearly and lower confidence.

### 7. Select And Synthesize

Choose exactly 2 to 5 papers, unless fewer than two relevant papers exist and the sparse result itself is material. The selected papers must be:

- relevant to the question
- compliant with the requested source scope
- diverse enough to avoid overgeneralizing from one paper
- rich enough in methods, results, or figures to support the answer

Then synthesize across papers instead of writing a paper-by-paper summary unless the user asked for that.

## Output Rules

- Answer directly in chat unless the user asks for a file.
- Give every cited source a GB/T 7714—2015 citation and a complete clickable
  link; retain DOI, PMID, PMCID, or ISBN when available.
- Be explicit about what was actually read.
- If evidence is limited, say so plainly.

Use [references/query-guide.md](./references/query-guide.md) for output templates.

## Non-Negotiable Rules

- User-specified source scope overrides your defaults.
- Do not use this skill for a question that requires more than five papers or broad field coverage.
- Do not answer methods or marker questions from abstracts alone if full text is available.
- Do not fabricate source membership or figure details.
- Prefer PubMed and PMC for biomedical literature.
- Translate search intent into English for querying, but answer in the user's language when appropriate.

## If Results Are Sparse

When little is found:

- broaden or narrow terms thoughtfully
- try synonyms or controlled vocabulary
- explain what was searched and why the yield was limited
- suggest the next best search strategy
