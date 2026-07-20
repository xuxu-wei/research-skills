# Narrative-readiness rubric

Apply this rubric to reader-facing function and sequence. Do not score scientific
quality or terminology standardity.

## Reader reasoning chain

The dossier must let its stated readers follow, without reconstructing hidden steps:

1. **Background** establishes the problem and the minimum context needed to care.
2. **Current state** explains what is presently known, done, or available.
3. **Gap** states what knowledge or evidence remains unable to answer.
4. **Significance** explains why resolving that gap matters to the stated readers.
5. **Rationale** connects that gap to the proposed design and explains why the design
   is a suitable way to make progress.

Each function must be present, nonempty, and distinct. A list of nearby facts is not a
chain. A novelty comparison is not a scientific gap. A method description is not a
rationale unless the connection is made explicit. Missing significance or a broken
gap-to-rationale connection is a major finding.

## Section-function fit

- A section should perform the function promised by its heading before adding detail.
- Titles, summary, abstract, question, objectives, and contribution claims must name
  compatible core elements and lead the reader toward the same study.
- Technical validation detail belongs after the reader-facing core unless it is
  necessary to understand the question itself.
- Internal workflow language must not substitute for a scientific explanation.

## Progressive disclosure and reader baseline

- Introduce the problem before specialized constructs used to solve it.
- Define an unfamiliar necessary concept at first use in language suitable for the
  declared reader profile.
- Do not require a reader to search later sections to interpret an earlier central
  claim.
- Distinguish genuinely necessary technical density from density created by ordering,
  unexplained labels, or premature contingencies.
- Judge burden relative to the supplied reader handoff, not to the assessor's own
  expertise.

## Narrative balance

Lead with what the study asks, why it matters, and what it can contribute. Boundaries
may qualify the relevant claim, but should not displace the positive argument.

Keep narrative prominence proportional to declared scope, timing, and
conditionality. A contingent downstream component may appear in the core
question and outputs, but its full eligibility, operation, alternative, and
interpretation logic belongs in one technical authority location. Other
required sections retain only the minimum statement needed for their own
question, objective, evidence-chain, output, or claim-audit function.

Maintain one authoritative limitations location. Elsewhere, remove a limitation
entirely unless it directly enables the reader to understand the immediately linked
design choice and removing it would distort that reasoning. Never leave a pointer or
cross-reference to the authoritative section; a necessary local boundary must be
self-contained.

## Repetition and navigation

Flag repetition when it adds no new reader function, especially repeated cautions,
definitions, workflow conditions, or contribution claims. Consolidation must retain
the complete authoritative statement. Flag avoidable backtracking when definitions or
premises arrive after claims that depend on them.

Required sections can be concise, but their distinct contract functions are not
repetition merely because they trace the same study. Before recommending deletion or
consolidation, distinguish method specification, evidence-chain traceability,
required-analysis acceptance criteria, planned outputs, contribution interpretation,
and Claim-Support audit. Remove duplicated content within or across those functions;
do not erase a required function or collapse all functions into a single substitute.
An implementation section must name implementation objects, records, or interfaces;
repeating the preceding method specification is not a distinct implementation
function.

## Decisions

- `narrative_ready`: no repair action is needed for the assessed scope.
- `minor_narrative_revision`: localized changes can resolve all findings without
  restructuring the reader's main route.
- `major_narrative_revision`: a missing/broken reasoning function, pervasive ordering
  or repetition problem, core-element misalignment, or substantial restructuring is
  required.
- `clarification_required`: an absent or conflicting reader handoff or intended core
  relationship prevents a reliable editorial target from being specified.

Decision severity follows the effect on reader reasoning, not the number of findings,
paragraph length, occurrence count, or presence of particular words.
