# Downstream Handoff Rules

## Contents

- [Preflight](#preflight)
- [Editorial readiness and Idea evaluator](#editorial-readiness-and-idea-evaluator)
- [Portfolio](#portfolio)

## Preflight

Pass the current dossier plus role-necessary context/evidence when endpoint,
data-method fit, analysis feasibility, or clinical/statistical design needs
independent checking. Any repair returns to the writer and produces a new
complete dossier.

## Editorial readiness and Idea evaluator

After preflight revision, the orchestrator sends the frozen current dossier to
fresh narrative and language assessors. Any editorial repair produces a new
complete dossier and requires fresh readiness assessment. Persist an editorially
repaired dossier with `change_type: editorial_repair` and its paired delta with
`change_type: editorial_repair_delta`; do not label this route as an ordinary
scientific revision.

Identify both outputs by logical ID, version, path, and index membership. Do not
compute, request, report, or persist a content hash as a repair or completion
check.

For an editorial repair, map every frozen included repair item ID to its revised
locator and acceptance-test evidence in the delta. Re-read the title,
summary, research question, contribution, and core design relations after all
moves and replacements so a required definition is not left after its first
reader-facing use. This writer check does not authorize a readiness decision.

When the bundle is long, maintain one complete target dossier and repair it in
bounded internal passes: reader core (sections 1--4), research plan and technical
authority (5--11), positioning/claim audit/limitations authority (12--14), then
references and a whole-dossier scan. Read only the normalized actions in the
approved writer brief; narrative and language reports and the assessor repair
plan are not writer inputs. Never persist section fragments or split authorship
across writers.

Keep the target as an unfrozen candidate until the orchestrator has checked
every included repair action against the actual text and rerun the named script,
inputs, and arguments. If that check finds an omitted action, false receipt, or
nearby wording regression, correct the same candidate in a bounded pass and
rerun all checks. Freeze only after this conformance check passes; no independent
preservation or readiness review starts earlier.

Do not create or finalize the delta until the final whole-dossier scan and
deterministic lint pass and the complete dossier is frozen. Any later dossier
edit invalidates the delta and requires a new whole-dossier scan and rewritten
delta; do not use timestamps or content hashes as a substitute for this order.
Resolve every lint `ADVISORY` before freezing: replace internal implementation
shorthand with the scientific object, operation, or record it denotes, or give
a legitimate technical term an immediate reader-level definition. Advisories
are review candidates rather than a universal forbidden-word list.

After the revised text is complete, make a temporary role-based list from the
new title, summary, question, study object, contribution, and core design
relations—not only from the assessor's original findings. Include stage or
programme labels and labels that name document organization, evidence
bookkeeping, acceptance, or fallback rather than a domain object or scientific
operation. Also include every abbreviation in the title, summary, abstract,
background, question, or hypothesis and any abbreviation that carries a core
endpoint, exposure, intervention, model, or validation role. Recheck every first
reader-facing occurrence for an identifiable referent and function, unambiguous
modifier attachment, expansion appropriate to the documented reader baseline,
and consistent bilingual form. Do not retain or introduce
a compressed core label merely because its components are familiar; use the
verified replacement from the approved writer brief or direct descriptive wording.
Also reread each title, summary, question, hypothesis, and assumption sentence
for nested qualifiers: every condition must attach to one identifiable action
or conclusion without making the reader search forward. Record locator-level
acceptance evidence in the delta, then discard the
temporary list.

The delta's acceptance evidence must include a compact concordance check for
the central object, primary question or task, primary outcome, and contribution
when those roles exist. Add any other core scientific role only when the dossier
actually contains it and its naming controls design, analysis, evidence status,
or interpretation, or when an accepted repair action addresses it. For each
included role, record the one
reader-facing name, its first-use locator, the competing forms removed or
reclassified, and the result of an all-occurrence scan. A finding is not closed
when only its example locators changed, when a competing form remains elsewhere,
or when the replacement invents another compressed label. Any unresolved
critical or major language finding blocks persistence.

Consistency does not require repeating a definition. After one timely
reader-facing definition, use the stable name alone. Keep the complete
eligibility, operation, alternative, and interpretation logic for a contingent
downstream component in its technical authority subsection; in other mandatory
sections, retain only the input, output, objective, evidence, or claim boundary
needed for that section's distinct contract function. The one-sentence summary
may identify the component's conditional scientific purpose, but never carries
its full entry conditions, alternative branches, stopping branch, or internal
stage/branch labels. A protected register requires semantic traceability, not a
full restatement in every section named by a broad source locator.

Before persistence, make a temporary occurrence check for every limitation
family. Record its sole complete section-14 locator and, for each retained local
boundary, the immediately adjacent estimand, design choice, interpretation, or
audit decision that would become false or ambiguous if the boundary were
removed. Delete any occurrence without such a distinct function; do not retain
it for emphasis, reassurance, symmetry, or completeness. Discard this temporary
check after recording the affected repair action's acceptance evidence in the
delta.

When the design explicitly contains a sequential component that begins only
after a primary study succeeds, apply the dossier contract's optional placement
pattern: omit a section with no distinct role and keep the full eligibility,
alternative, and stopping logic in the scientific-method authority. For
parallel, adaptive, iterative, nested, or multiple dependent components, derive
a design-faithful placement map instead of imposing that sequential pattern or
its cardinalities. Traceability, symmetry, and a mandatory section are not
reasons to restate any component.

If a language or narrative action requires the author, methodologist, or data
holder to confirm a scientific object, value, or route, and the repair bundle
contains no approved answer, do not infer one, relabel the scientific state, or
add a new restriction. Preserve the source science, record that action as
unresolved in the delta, and route it for clarification. A purely editorial
writer cannot convert ambiguity into a new methodological decision.

Reader-facing text states the current scientific status directly. Do not expose
that the current revision lacks preflight approval, that a reviewer requested a
change, or that an earlier version did or did not read a source. Such provenance
belongs in the delta or evidence index, not the dossier.

Treat each protected-register summary as an index to its `source_locator`, not
as an exhaustive substitute for the source passage. Before compressing or
deleting text, compare that complete passage and carry forward every scientific
commitment, numerical or temporal rule, analysis-handling rule, evidence state,
and claim boundary. In the delta, map every `protected_id` to its revised
locator(s) and item-level preservation evidence. If any protected commitment
cannot be retained, declare a scientific change and return it to scientific
review; do not describe the change as editorial.

Before handoff, reopen every cited revised locator and verify that its actual
text contains every enumerated element claimed by the delta. A section topic,
an intended direction, or the delta's own assertion is not preservation
evidence. If even one claimed element is absent from the dossier text, block
handoff and repair the complete dossier first.

Keep the delta as a compact verification index: one locator-level row per
included repair item, protected ID, and concordance role. Do not
repeat full protected-content entries, report instructions, or long dossier
passages. The revised dossier, not a second full narrative in the delta, is the
evidence source.

Only after readiness is established does the orchestrator pass exactly one
frozen current dossier to the evaluator, identified by artifact ID, version,
and path. Do not pass context, maps, evidence limitations, ledger, preflight,
lineage, prior versions, deltas, must-fix lists, or editorial reports. All
necessary facts and citations must already be inside the dossier.

## Portfolio

Do not promote directly. After qualifying evaluation and any required panel,
the assembler receives dossier/report/ledger pointers and sealed decisions.
