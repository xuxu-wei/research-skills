# Language Hard Gates

Non-compensatory gates for language assessment. A single gate failure constrains the `overall_language_readiness` level regardless of other dimension scores.

---

## Gate 1: Grammar Error Density

**Threshold**: > 3 clear, unambiguous grammatical errors per 500 words (averaged across assessed sections)

**What counts as a "clear" error**:
- Subject-verb disagreement ("the data shows" in biomedical — acceptable in some social science contexts)
- Verb tense error (not a convention preference — an actual wrong tense)
- Missing or incorrect article where it changes meaning
- Sentence fragment lacking a main clause
- Dangling modifier that creates ambiguity

**What does NOT count**:
- Stylistic preferences (active vs passive)
- Discipline-debated usage ("data is" vs "data are")
- Variant punctuation conventions (Oxford comma)

**Failure consequence**: `overall_language_readiness ≤ major_language_revision`

**Rationale**: Error density at this level reliably indicates that the manuscript was not proofread. Reviewers and editors consistently flag grammar as a reason for negative first impressions.

---

## Gate 2: Academic Register — Pervasive Informal Register

**Threshold**: Systematic use of informal/colloquial register in ≥ 2 manuscript sections

**What constitutes "systematic"**:
- ≥ 5 clear informal features per section in ≥ 2 sections
OR
- ≥ 1 section where the dominant register is conversational rather than academic

**Informal features checklist**:
- Contractions (don't, can't, won't, it's for "it is")
- Informal vocabulary: "big", "get", "lots", "really", "very", "huge", "stuff", "thing", "a lot", "kind of", "sort of"
- Sentence-initial "And", "But", "So" used as discourse markers (acceptable in humanities in some contexts)
- Rhetorical questions in Methods or Results ("But is this really the case?")
- Direct address to reader ("you can see that...", "notice how...")
- Exclamation marks
- Em-dashes used excessively as informal punctuation (> 3 per page)

**Exception**: Direct quotes from participants (qualitative research), patient-reported text, or interview transcripts are exempt.

**Failure consequence**: `overall_language_readiness ≤ needs_professional_editing`

**Rationale**: Pervasive informal register is very difficult to fix through targeted revision — it usually requires systematic rewriting by someone with strong academic English command. It is also one of the most common reasons for immediate negative reviewer impressions.

---

## Gate 3: Terminology Incoherence

**Threshold**: ≥ 3 core concepts referred to by ≥ 2 different terms each, with no apparent reason (not stylistic variation, but inconsistent naming)

**What counts as a "core concept"**:
- The primary exposure, intervention, or independent variable
- The primary outcome or dependent variable
- The study population or sample descriptor
- The main method or technique name
- The key construct being measured

**What does NOT count**:
- Intentional synonym variation for readability
- Full term vs. defined abbreviation (acceptable if abbreviation consistently used after definition)
- Disciplinary synonyms where both are standard (e.g., "covariate" / "confounder" used precisely with distinct meanings)

**Failure consequence**: `overall_language_readiness ≤ major_language_revision`

**Rationale**: Terminology inconsistency creates genuine ambiguity about whether the author is referring to the same concept or a different one. In biomedical and technical writing, this can affect reproducibility and regulatory compliance.

---

## Gate 4: Tense Systematic Violation

**Threshold**: Systematic tense misuse in Methods or Results sections, judged against the conventions of the target discipline

**What constitutes "systematic"**:
- The dominant tense in Methods is present or future (should be past for empirical research)
- The dominant tense in Results is present for reporting findings (should be past for most disciplines)
- Method descriptions consistently using future tense ("we will recruit", "participants will be randomized")

**What does NOT count**:
- Isolated tense shifts for valid reasons (referring to a table, describing a figure)
- Present tense for established facts or definitions within Methods
- Discipline-appropriate deviations (present tense in CS system description; present tense in mathematics proofs)

**Failure consequence**: `overall_language_readiness ≤ major_language_revision`

**Rationale**: Systematic tense errors suggest the author does not know the reporting conventions of their field. This is a correctable but significant problem.

---

## Gate Interaction

- A single gate failure is sufficient to constrain the overall level
- Multiple gate failures compound: 2+ gate failures → `overall_language_readiness = needs_professional_editing`
- Gate failures are independent of dimension scores: even if all six dimensions score ≥ 7, a gate failure still constrains the overall level

## Gate Re-assessment

After language polishing:
- A previously failed gate that now passes → level constraint is lifted
- A previously passed gate that now fails → new issues were introduced during polishing; overall level may degrade
