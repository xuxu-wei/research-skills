---
name: article-frontmatter-drafter
description: "Draft versioned abstract, titles, key points, highlights, and related frontmatter from an evaluated manuscript and blueprint."
---
# article-frontmatter-drafter

## Purpose

Draft manuscript frontmatter except the cover letter: abstract, key points, title options, running title, highlights, and graphical abstract text. These elements must align with the manuscript and target journal requirements.

This skill does NOT modify the manuscript body, introduce new claims not in the manuscript, draft the cover letter (that is `article-cover-letter`'s job), or assemble the submission package (that is `article-submission-compositor`'s job).

## Core Rules

- The contribution statement from the blueprint anchors all frontmatter.
- Abstract must not contain results or claims absent from the manuscript body.
- Title must be accurate, not promotional. Avoid "Novel," "First," and "Unique" unless definitively supported.
- Key points must be standalone; a reader should understand the study's contribution from them.
- Follow journal-specific frontmatter requirements from the journal adapter.
- Do not write or edit `11_cover-letter/**`.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - manuscript_draft
    - article_blueprint (contribution_statement, journal_adapter)
    - evaluation_report (optional, for addressing evaluator frontmatter feedback)
    - panel_report (optional, for addressing reviewer frontmatter feedback)
  required_outputs:
    - abstract
    - key_points
    - title_options
    - running_title
    - highlights
    - graphical_abstract_text (if applicable)
  may_read:
    - "06_drafts/**"
    - "04_blueprint/**"
    - "08_evaluations/**"
    - "10_panel/**"
  may_write:
    - "11_frontmatter/**"
  must_not_write:
    - "06_drafts/**"
    - "04_blueprint/**"
    - "11_cover-letter/**"
  may_call: []
  must_not_call:
    - article-evaluator
    - article-drafter
    - article-cover-letter
  failure_modes:
    - "journal adapter missing structured abstract format -> default to IMRaD structured abstract, flag for author check"
    - "contribution statement too vague for title -> request architect clarification via orchestrator"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Load and Cross-Check

Load the manuscript, blueprint, and journal adapter. Verify contribution statement, article type, journal abstract requirements, and all claims referenced by frontmatter.

### Step 2: Draft Abstract

Follow the journal's abstract format:

```yaml
abstract:
  format: structured | unstructured
  sections:
    introduction: ""
    methods: ""
    results: ""
    discussion: ""
    conclusion: ""
  word_count: 0
  journal_limit: 0
  within_limit: true | false
```

Rules:
- Include numerical results with precision when available.
- Do not cite references unless journal policy permits.
- Define abbreviations on first use.
- Match the manuscript's tense conventions.

### Step 3: Draft Key Points

Produce journal-compliant key points covering what was known, what this study adds, the key methodological or evidence strength, implications, and an important limitation when relevant.

### Step 4: Draft Titles

Produce 2-4 title options:

- Descriptive: design/population/exposure/outcome.
- Declarative: main finding, only when evidence is strong.
- Interrogative: research question, only if journal style allows.

Also draft a running title within journal limits.

### Step 5: Draft Highlights and Graphical Abstract Text

Draft highlights and graphical abstract text only when required or useful for the target journal.

## Output

Write to `11_frontmatter/`:

- `abstract.md`
- `key-points.md`
- `title-options.md`
- `running-title.md`
- `highlights.md`
- `graphical-abstract-text.md` (if applicable)

## Stop Conditions

- Contribution statement is missing or too vague.
- Journal-specific frontmatter requirements are unknown and cannot be safely inferred.

## Pitfalls

- Do not make the abstract sound like a press release.
- Do not declare unsupported novelty.
- Do not introduce claims absent from the manuscript.
- Do not draft or edit the cover letter.
- Title alternatives must be genuinely different, not word-order permutations.

## Verification

- Abstract includes numerical results where available.
- Abstract word count is within journal limit or explicitly flagged.
- Key points are standalone readable.
- Title alternatives represent distinct strategies.
- No claims introduced in frontmatter absent from manuscript.
- Running title and highlights are within journal limits.
- No `11_cover-letter/**` artifact was created or modified.

## References

- Read `references/abstract-writing-guide.md` when its named guidance or contract applies: Structured abstract formats by journal type, word count management, and common pitfalls.
- Read `references/title-strategies.md` when its named guidance or contract applies: Title type selection criteria, journal policy considerations, and examples by study type.
- `article-orchestrator/references/artifact-contracts.md`: Canonical frontmatter artifact schemas.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory and naming conventions.
