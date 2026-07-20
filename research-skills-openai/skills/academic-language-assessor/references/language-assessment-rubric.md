# Language Assessment Rubric

## Contents

Grammar and syntax; academic register and tone; terminology; tense and voice;
concision; readability and flow; complete-Idea coverage; severity calibration;
scoring rules.

Scoring anchors for the six assessment dimensions. Each dimension scored 1–10.

---

## 1. Grammar & Syntax

| Score | Anchor |
|-------|--------|
| 9–10 | Near-native; ≤ 1 minor error per 1000 words; no error affects comprehension |
| 7–8 | Occasional minor errors (article, preposition); ≤ 2 errors per 500 words; readability unaffected |
| 5–6 | Noticeable but not pervasive errors; ≤ 3 errors per 500 words; occasional re-reading needed |
| 3–4 | Frequent errors; > 3 per 500 words; sentence structure sometimes unclear; reader effort required |
| 1–2 | Pervasive errors; meaning frequently obscured; ungrammatical constructions throughout |

**Hard gate**: > 3 clear grammatical errors per 500 words → `fail`

---

## 2. Academic Register & Tone

| Score | Anchor |
|-------|--------|
| 9–10 | Consistently formal academic register; no colloquialisms; appropriate disciplinary tone |
| 7–8 | Mostly formal; isolated informal words (≤ 2 per 2000 words); tone appropriate |
| 5–6 | Noticeable informal expressions in ≥ 2 sections; some promotional language; mildly conversational |
| 3–4 | Systematic informal register in ≥ 2 sections; colloquial vocabulary, contractions, or rhetorical questions in formal sections |
| 1–2 | Pervasive informal register throughout; reads as conversational rather than academic; inappropriate for any scholarly venue |

**Hard gate**: systematic informal register in ≥ 2 sections → `fail`

---

## 3. Terminology Consistency

For Idea dossiers, this dimension also covers whether core terms are standard
or natural in the relevant domain, comprehensible at the stated reader
baseline, defined at first use, and stable across languages. Consistency alone
does not rescue a consistently nonstandard or misleading term. Do not require a
long terminology inventory when no problem is present. Assess a composite
phrase by its semantic head and any genuinely ambiguous component, not by
whether the exact complete phrase occurs in a source. Required machine
frontmatter and contract-fixed labels are outside this score unless their
language is copied into ordinary prose or a free-form reader label. Their mere
appearance as the required research-idea.v3 headings, section/abstract fields,
evidence-chain fields, or Claim-Support schema headers is never a language
finding and must not be used to require localization or schema renaming.

| Score | Anchor |
|-------|--------|
| 9–10 | All key terms used consistently; abbreviations defined once and used uniformly; no ambiguity |
| 7–8 | One or two minor inconsistencies; all abbreviations properly defined |
| 5–6 | 3–4 term variations for the same concept; one undefined abbreviation; mild confusion possible |
| 3–4 | ≥ 3 core concepts inconsistently named; multiple undefined abbreviations; reader must guess referents |
| 1–2 | Pervasive terminological chaos; same concept named 5+ different ways; abbreviations undefined or contradictory |

**Hard gate**: ≥ 3 core concepts with inconsistent terminology → `fail`

---

## 4. Tense & Voice Conventions

| Score | Anchor |
|-------|--------|
| 9–10 | Tense and voice follow discipline conventions perfectly across all sections |
| 7–8 | One or two tense shifts that do not confuse meaning; voice generally appropriate |
| 5–6 | Multiple tense errors but not systematic; e.g., occasional present tense in Methods |
| 3–4 | Systematic tense misuse in one section (e.g., Methods consistently in present tense); reader notices |
| 1–2 | Tense chaos across all sections; no apparent awareness of conventions |

**Hard gate**: systematic tense misuse in Methods or Results → `fail`

---

## 5. Conciseness & Redundancy

| Score | Anchor |
|-------|--------|
| 9–10 | Tight, efficient prose; no filler phrases; every word earns its place |
| 7–8 | Mostly concise; occasional "It is worth noting that..." or nominalization |
| 5–6 | Noticeable filler phrases, redundancies, or over-nominalization in ≥ 3 locations |
| 3–4 | Pervasive wordiness across sections; duplicate content between Results and Discussion |
| 1–2 | Extremely verbose; substantial duplicate content; difficult to extract key information |

No hard gate on conciseness — this dimension is compensatory. Overly terse prose that sacrifices clarity is also penalized.

---

Count lexical duplication and qualifier stacking, but do not infer that a
scientifically distinct condition is dispensable merely because related
conditions occur elsewhere. Cross-section rhetorical necessity is assessed by
the narrative role.

## 6. Readability & Flow

For an Idea dossier, score sentence structure, paragraph focus, and local
transitions here. The five-part reasoning chain, section order, section
function, and cross-section disclosure sequence belong to narrative assessment.

| Score | Anchor |
|-------|--------|
| 9–10 | Effortless reading; logical paragraph structure; clear transitions; appropriate sentence length variety |
| 7–8 | Good flow; occasional overlong sentence or abrupt transition |
| 5–6 | Multiple overlong sentences (> 35 words biomedical; > 40 words CS); some paragraphs lack topic sentences; transitions occasionally missing |
| 3–4 | Frequent readability obstacles; many paragraphs lack clear focus; transitions absent or confusing |
| 1–2 | Extremely difficult to follow; no apparent paragraph logic; sentences consistently too long or fragmented |

No hard gate on readability — this dimension is compensatory.

---

## Complete-Idea coverage and finding level

A completed Idea assessment records four coverage passes with
`status: completed`. They confirm review completion, not that the prose passed
its language criteria:

- `reader_entry`: inspect every bounded title, summary, question, hypothesis,
  and contribution entry unit without closing a sentence after its first issue;
- `core_scientific_role`: identify every scientific role actually present and
  check each reader-facing name; do not impose absent roles. Always compare the
  central study object's head noun and role across title, summary, question,
  and contribution, and keep the study object, fitted model, representation
  output, and structural relation distinct when those roles are present;
- `terminology_concordance`: for every triggered concept cluster, inspect all
  competing forms and locators across the dossier; zero triggered clusters may
  pass with a count of zero. When validation is present, check that each label
  distinguishes the partition dimension (for example time, site, or database)
  from model recalibration, updating, adaptation, or refitting, without implying
  a different clinical setting;
- `local_language`: assess every in-scope reader-facing unit for grammar,
  register, tense, local clarity, and local redundancy.

Record only counts and a concise basis in `coverage_receipt`; never persist the
temporary role list or a complete term inventory. Classify language findings as
`meso` when one concept cluster spans multiple reader-facing occurrences or
roles, and `micro` when one localized expression can be repaired independently.
Route macro argument, section-function, or disclosure-order problems to the
narrative assessor instead of encoding them as language findings.

Build each readable finding `fingerprint` as
`finding_level|scientific_role|normalized_locator|failure_mode`, using lowercase
kebab-case components. This key stabilizes writer handoff across renumbered
finding IDs; it is not a content digest.

---

## Finding severity and bounded reporting

Calibrate severity by the stated reader's ability to identify the scientific
role and meaning, not by how technical, frequent, or improvable a phrase is.

- `critical`: language repeatedly obscures or reverses the artifact's study
  status, primary question, main inference, or central result, so a reliable
  editorial repair cannot proceed without clarification or professional editing.
- `major`: the current wording materially prevents the stated reader from
  identifying a central study object, primary task or outcome, main method,
  principal measurement, or interpretation boundary, or a qualifying hard gate
  fails as an overall pattern. The report must state what materially wrong
  reading remains possible. A major finding blocks readiness.
- `minor`: the referent and scientific role remain recoverable from nearby text,
  but a localized ambiguity, delayed definition, secondary-role inconsistency,
  translation, abbreviation, or sentence construction creates avoidable effort.
  Minor findings remain visible but do not by themselves trigger another repair
  cycle.
- `suggestion`: a defensible optional preference with no material reader cost.

A supporting diagnostic, implementation label, secondary outcome, or later
technical detail is not automatically central merely because it recurs. A term
defined later is minor when the first use still identifies its referent and
function; it is major only when the earlier wording supports a materially wrong
reading of a central role. Do not promote a finding because a more elegant or
more explicit expression is available.

Complete coverage does not require exhaustive issue production. Report the
smallest non-overlapping set that represents every evidenced actionable pattern;
group one scientific role's competing forms into one finding, and do not split
minor local edits solely to increase coverage counts. Finding count is never a
quality target.

Severity describes reader impact; it does not authorize the assessor to choose
scientific content. If a repair can only be completed by selecting between
different estimands, metrics, model definitions, scientific roles, or claim
strengths, use `clarification_required` and name the unresolved alternatives.
Do not present one alternative as a language replacement. If the intended
scientific meaning is recoverable and only its wording is nonstandard or
ambiguous, an ordinary language finding with a concrete repair remains valid.

---

## Scoring Rules

- Score based on the **overall pattern**, not a single worst instance
- A single excellent paragraph does not rescue a section full of errors
- A single bad sentence does not tank a dimension unless it's emblematic of a broader pattern
- When uncertain between two scores, choose the lower one and note the uncertainty
- Non-native features (L1 interference) are assessed the same way as any other error on Grammar, Register, and Readability — their origin does not change their impact on the reader
