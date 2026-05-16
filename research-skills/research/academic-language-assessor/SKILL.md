---
name: academic-language-assessor
description: Assess academic language quality for English, Chinese, or bilingual manuscripts and workflow deliverables. Checks grammar/syntax, academic register, terminology consistency, tense/voice conventions, conciseness, redundancy, readability, Chinese academic clarity, Chinese-English mixed formatting, and defensive or decorative wording. Produces a structured Language Assessment Report with hard gates, specific issues, and revision priorities. Does not rewrite or polish text; rewriting is the responsibility of the calling drafter or refinement controller.
version: 0.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research, language, academic-writing, assessment, editing, quality-gate]
    category: research
    related_skills:
      - article-orchestrator
      - article-evaluator
      - article-refinement-controller
      - article-drafter
      - proposal-evaluator
      - proposal-refinement-controller
      - proposal-drafter
      - perspective-evaluator
      - perspective-refinement-controller
      - perspective-drafter
---

# academic-language-assessor

## Purpose

Use this skill when an academic manuscript, proposal, perspective, portfolio, handoff package, or other academic text needs systematic English, Chinese, or bilingual language quality assessment before submission, during evaluation, or as a preflight before language polishing.

This skill only answers: **does the language meet the baseline academic standard? If not, what specific issues must be fixed?**

It does not rewrite, polish, or edit text. It does not evaluate scientific content, argument quality, or journal fit. Those are the responsibility of evaluators.

## Core Rules

- Assess only language quality, not scientific content.
- Output specific, locatable issues — not vague impressions.
- Hard gates on grammar density, academic register, terminology coherence, and tense conventions.
- Discipline-aware: apply the tense, voice, and register conventions of the target discipline.
- Language-aware: use English rules for English text, Chinese academic clarity rules for Chinese text, and mixed-format rules for bilingual text.
- For Chinese polishing guidance, prioritize concise, clear, explicit prose. Flag unnecessary metaphors, decorative modifiers, redundant defensive caveats, empty setup phrases, and vague self-protective wording for deletion.
- Do not rewrite text. Suggested corrections are directional only.
- When in doubt about a convention, mark it and note the uncertainty — do not enforce a guessed rule.
- Assessment must be reproducible: any issue reported must be locatable by section, paragraph, and sentence.

## Inputs

Usually supplied by an orchestrator, evaluator, or refinement controller:

- `manuscript_text`: full text or specified sections
- `target_language`: English | Chinese | bilingual; default `English`
- `discipline`: biomedical_clinical | cs_ai_engineering | mathematics_theory | social_sciences | humanities | general_science
- `target_journal`: optional, for journal-specific preferences
- `scope`: full_manuscript | specified_sections
- `prior_assessment_report`: if this is a re-assessment after language polishing

If minimum inputs are missing (no text, unknown discipline), return clarification needs — do not fabricate assessments.

## Language-Specific Conventions

### English

Use the six English-oriented dimensions below and consult `references/english-academic-language-conventions.md`, `references/discipline-language-conventions.md`, and `references/common-l1-interference-patterns.md`.

### Chinese

For Chinese academic text, assess whether the prose is:

- **Concise**: remove redundant setup phrases, repeated qualifiers, stacked modifiers, filler transitions, and empty formulas such as "值得注意的是" when they add no information.
- **Clear**: keep sentence subjects, actions, objects, and logical links visible; flag overlong sentences, excessive parentheticals, and abrupt logical jumps.
- **Explicit**: make terms, populations, comparisons, time frames, causal boundaries, and evidence status unambiguous.
- **Non-metaphorical**: remove unnecessary metaphors, literary imagery, emotional phrasing, and decorative language that obscures the claim.
- **Not over-defensive**: remove redundant caveats, repeated self-limitation, and defensive hedging unless needed for scientific accuracy.
- **Not promotional**: flag unsupported phrases such as "显著提升", "重要突破", "深刻揭示", or "填补空白" when evidence does not justify them.
- **Mixed-format compliant**: check Chinese-English spacing, punctuation, abbreviations, units, numerals, and term consistency.
- **Academic but direct**: preserve Chinese academic register without allowing verbosity, ornament, or evasive phrasing.

See `references/chinese-academic-language-conventions.md` for detailed rules.

### Bilingual

For bilingual documents, assess each language under its own rules and additionally check term mapping, acronym consistency, Chinese-English spacing, punctuation, and whether translated wording changes claim strength.

## Discipline Conventions (selective reference)

See `references/discipline-language-conventions.md` for full conventions. Key rules:

### Biomedical / Clinical

- **Abstract**: past tense for methods/results; present tense for conclusions
- **Introduction**: present tense for established knowledge; past tense for prior studies
- **Methods**: past tense (what was done); passive voice acceptable but not mandatory
- **Results**: past tense (what was found); no interpretation
- **Discussion**: present tense for interpretation; past tense for referencing own results; modal verbs for speculation
- **Abbreviations**: define at first use in abstract and again in main text
- **Numbers**: numerals for measurements; spell out at sentence start

### CS / AI / Engineering

- **System description**: present tense
- **Experiments**: past tense
- **Algorithms**: present tense for description
- **Equations**: present tense ("is defined as")
- **Abbreviations**: define at first use; common CS acronyms (CNN, LSTM, API) may be used without definition if widely recognized

### Mathematics / Theory

- **Theorems, lemmas, proofs**: present tense
- **Definitions**: present tense
- **Notation**: define all non-standard notation; consistent use throughout

### Social Sciences

- **Refer to APA 7th Edition** for tense, voice, and language conventions
- **Past tense** for literature review; **present tense** for results/conclusions
- **Active voice** preferred; passive acceptable in Methods
- **Bias-free language**: per APA guidelines

### Humanities

- **Text analysis**: present tense ("the author argues")
- **Historical narrative**: past tense for events; present tense for interpretation
- **First person**: may be acceptable depending on discipline and journal

### General Science (default when discipline unclear)

- **Methods**: past tense, passive or active
- **Results**: past tense, objective
- **Introduction**: present tense for established facts; past tense for prior work
- **Discussion**: mixed present/past per context
- **All abbreviations defined** at first use in abstract and main text
- **Conservative register**: avoid colloquialisms, contractions, rhetorical questions in Results/Methods

## Assessment Dimensions

### 1. Grammar & Syntax (score 1–10)

Check for:
- Subject-verb agreement errors
- Sentence fragments or run-ons
- Incorrect or missing articles (a/an/the)
- Preposition errors
- Punctuation errors (comma splices, missing commas in restrictive/non-restrictive clauses)
- Dangling or misplaced modifiers
- Parallel structure violations

**Hard gate**: > 3 clear grammatical errors per 500 words → `fail`

### 2. Academic Register & Tone (score 1–10)

Check for:
- Contractions (don't, can't, it's)
- Informal vocabulary (big, get, lots, really, very, huge, stuff, thing)
- Colloquial expressions or idioms
- Rhetorical questions in Methods or Results
- Overly promotional language ("remarkably", "strikingly", "extremely", "very significant")
- Narrative storytelling in Results ("a 45-year-old man presented with...")
- Use of "we" or "I" where not appropriate for the discipline
- Sentence-initial "And", "But", "So" in formal academic text
- Use of "etc." where a complete list or "such as" would be more precise

**Hard gate**: systematic informal register in ≥ 2 sections → `fail`

### 3. Terminology Consistency (score 1–10)

Check for:
- Same concept referred to by multiple different terms (e.g., "participants"/"subjects"/"patients"/"individuals" used interchangeably)
- Abbreviations defined but later spelled out, or vice versa
- Abbreviations defined multiple times
- Non-standard abbreviations used without definition
- Brand/proprietary names used without manufacturer/location
- Gene/protein nomenclature inconsistencies (italics, case)

**Hard gate**: ≥ 3 core concepts with inconsistent terminology → `fail`

### 4. Tense & Voice Conventions (score 1–10)

Check for:
- Methods section using present or future tense
- Results section using present tense for findings
- Introduction using future tense to describe the study
- Discussion using past tense for established facts
- Inconsistent tense within a single paragraph describing a single temporal frame
- Voice shifts that confuse agency (active/passive mixing without purpose)

**Hard gate**: systematic tense misuse in Methods or Results → `fail`

### 5. Conciseness & Redundancy (score 1–10)

Check for:
- Redundant word pairs ("each and every", "first and foremost", "various different")
- Nominalization chains (prefer "we analyzed" over "an analysis was performed")
- Unnecessary hedging that undermines clarity without adding precision
- "It is worth noting that...", "It should be pointed out that...", "It is important to mention that..."
- "There is/are" where a stronger verb-subject construction is possible
- Duplicate content between Results and Discussion
- Duplicate content between Abstract and main text (acceptable to overlap, but not verbatim repetition)

### 6. Readability & Flow (score 1–10)

Check for:
- Excessively long sentences (> 35 words in biomedical; > 40 words in CS/engineering)
- Paragraphs of a single sentence
- Paragraphs exceeding ~250 words without a clear topic break
- Abrupt transitions between paragraphs or sections
- Information density too high (multiple distinct findings in one sentence)
- Signposting adequacy (do readers know where they are in the argument?)

## Workflow

### 1. Confirm Scope

Verify that this is a language assessment task, not scientific evaluation, rewriting, or journal selection.

If asked to evaluate scientific content or rewrite, return scope mismatch.

### 2. Read Manuscript and Confirm Discipline

- Read the full manuscript or specified sections
- Confirm or infer discipline from content and vocabulary
- Select applicable conventions from `references/discipline-language-conventions.md`

### 3. Assess Each Dimension

For each of the six dimensions, produce:
- A score (1–10)
- A severity judgment (pass / borderline / fail)
- Specific, locatable issues with original text, issue description, and suggested correction

Use the anchors in `references/language-assessment-rubric.md`.

### 4. Check Hard Gates

Evaluate each hard gate independently:
- Grammar error density
- Academic register pervasiveness
- Terminology incoherence
- Tense systematic violation

A single hard gate failure → `overall_language_readiness ≤ major_language_revision`.

### 5. Determine Overall Language Readiness

| Level | Criteria |
|-------|---------|
| `submission_ready` | All dimension scores ≥ 7; all hard gates pass; ≤ 5 minor issues |
| `minor_language_revision` | All dimension scores ≥ 5; all hard gates pass; minor/major issues present but fixable |
| `major_language_revision` | ≥ 1 dimension score ≤ 4 OR ≥ 1 hard gate borderline; systematic issues |
| `needs_professional_editing` | ≥ 1 hard gate fail; error density high across multiple dimensions; beyond what targeted revision can fix |

### 6. Prioritize Issues

Each issue tagged:
- `critical`: must fix — hard gate violation
- `major`: should fix — degrades quality significantly
- `minor`: consider fixing — improves polish
- `suggestion`: optional — stylistic preference

### 7. Generate Assessment Report

Output the structured assessment report (see Outputs section).

### 8. Re-assessment Mode

If a prior assessment report is provided, evaluate whether:
- Each critical and major issue from the prior report has been addressed
- New issues have been introduced
- Dimension scores have improved or degraded
- Language polishing was substantive or cosmetic only

## Outputs

Output a **Language Assessment Report** with this structure:

```yaml
language_assessment_report:
  schema_version: "research.v1"
  assessment_id: "lang-001"
  source_skill: "academic-language-assessor"
  target_language: English | Chinese | bilingual
  discipline: ""
  target_journal: ""
  scope: full_manuscript | specified_sections
  sections_assessed: []
  dimension_scores:
    grammar_syntax:
      score: 0
      error_density_per_1000_words: 0
      severity: pass | borderline | fail
    academic_register_tone:
      score: 0
      severity: pass | borderline | fail
    terminology_consistency:
      score: 0
      severity: pass | borderline | fail
    tense_voice_conventions:
      score: 0
      severity: pass | borderline | fail
    conciseness_redundancy:
      score: 0
      severity: pass | borderline | fail
    readability_flow:
      score: 0
      severity: pass | borderline | fail
  overall_language_readiness:
    level: submission_ready | minor_language_revision | major_language_revision | needs_professional_editing
  hard_gate_status: pass | fail
  failed_gates: []
  specific_issues:
    - issue_id: "L001"
      dimension: ""
      severity: critical | major | minor | suggestion
      location:
        section: ""
        paragraph_index: 0
        sentence: ""
      original: ""
      issue_description: ""
      suggested_correction: ""
      category: ""                    # e.g., subject_verb_agreement | informal_register | tense_shift | term_variation | redundancy | sentence_length
  strengths: []                       # things done well, worth preserving
  language_revision_priorities:
    - priority: 1
      dimension: ""
      issue_count: 0
      fix_approach: ""
  re_assessment_delta:                # only in re-assessment mode
    previous_level: ""
    current_level: ""
    issues_resolved: 0
    issues_remaining: 0
    new_issues: 0
    improvement: significant | moderate | minimal | none | degraded
  recommendation: accept | polish | revise_language | professional_editing_required
  assessment_notes: ""                # uncertainty, scope limitations, or caveats
```

## Hard Gates

See `references/language-hard-gates.md` for detailed criteria.

| Gate | Threshold | Consequence |
|------|-----------|-------------|
| `grammar_error_density` | > 3 clear errors per 500 words | `fail` → overall ≤ major_language_revision |
| `academic_register_pervasive` | Systematic informal register in ≥ 2 sections | `fail` → overall ≤ needs_professional_editing |
| `terminology_incoherence` | ≥ 3 core concepts with inconsistent terminology | `fail` → overall ≤ major_language_revision |
| `tense_systematic_violation` | Systematic tense misuse in Methods or Results | `fail` → overall ≤ major_language_revision |

A "systematic" violation means the error pattern is dominant or pervasive in the affected section, not isolated to one or two sentences.

## Delegation Rules

This skill should be executed as an **isolated subagent** when called by:
- `article-evaluator` (evaluator-embedded mode)
- `article-refinement-controller` (standalone-preflight mode)
- `proposal-evaluator`
- `proposal-refinement-controller`
- `perspective-evaluator`
- `perspective-refinement-controller`

Can also be used standalone by the user for ad-hoc language checks.

The subagent must receive the full manuscript text, target discipline, target journal (if any), scope, and prior assessment report (if re-assessment). Do not rely on parent session context.

The assessor must not call the drafter, evaluator, or refinement controller of any package — it only assesses and reports.

## Stop Conditions

Stop and report the issue if:
- No manuscript text provided
- Target discipline cannot be inferred and user has not specified
- Asked to rewrite or edit text instead of assess
- Asked to evaluate scientific content instead of language

## Pitfalls

- Do not rewrite or polish text — this is assessment only.
- Do not evaluate scientific validity under the guise of language assessment.
- Do not apply the conventions of one discipline rigidly to another.
- Do not make Chinese academic prose ornate. Prefer concise, clear, explicit wording and flag unnecessary metaphors, decorative modifiers, and redundant defensive caveats.
- Do not flag stylistic preferences as errors without noting they are suggestions.
- Do not mark a dimension as `fail` based on a single minor issue — look for patterns.
- Non-native features (L1 transfer patterns) should be flagged descriptively, not judgmentally.
- Avoid false precision — if you cannot determine whether something is an error, mark it as `uncertain` with a note.
- Do not output a passing assessment for a manuscript with pervasive language problems just because the scientific content appears strong.

## Verification

Before completing, check:
- All six dimensions scored with specific evidence
- Each hard gate explicitly evaluated
- Every reported issue is locatable (section + paragraph + sentence)
- Discipline conventions were referenced, not guessed
- Target-language conventions were applied; Chinese or bilingual text was checked for concision, clarity, explicitness, mixed formatting, and unnecessary defensive or decorative wording
- Strengths identified, not only weaknesses
- Re-assessment mode handled correctly (if applicable)
- Recommendation matches the evidence
- No text was rewritten
- No scientific evaluation was performed

## References

- `references/language-assessment-rubric.md`: Detailed scoring anchors for each of the six dimensions (1–10 scale with examples).
- `references/english-academic-language-conventions.md`: English academic style, register, and language baseline rules.
- `references/chinese-academic-language-conventions.md`: Chinese academic style rules emphasizing concise, clear, explicit prose and removal of unnecessary metaphor, modifier stacking, and redundant defensive phrasing.
- `references/language-hard-gates.md`: Detailed hard gate criteria, thresholds, and failure consequence rules.
- `references/discipline-language-conventions.md`: Tense, voice, register, abbreviation, and formatting conventions by discipline and journal type.
- `references/common-l1-interference-patterns.md`: Common non-native English patterns (Chinese L1, etc.) to recognize and flag descriptively.
- `templates/language-assessment-report.md`: Output template for the Language Assessment Report.
