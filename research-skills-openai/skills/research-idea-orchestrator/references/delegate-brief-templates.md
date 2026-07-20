# Delegate Brief Templates

## Contents

Generator/reviser; methodology preflight; dossier-only evaluator; biomedical or
clinical journal review; editorial readiness; repair writer; preservation
reviewer; adversarial role.

Every brief binds workflow/round, artifact IDs, exact paths, and versions,
allowed reads/writes, and failure route. Never rely on parent hidden context.

## Generator or reviser

```text
Role: write complete Ideas; do not evaluate or rank.
Route: <focused_optimization | bounded_exploration>
Active plugin version: <PLUGIN_VERSION>
Frozen reads: <context, maps, route, constraints, current dossier if revising;
for scientific revision after preflight, the current preflight report or a
structured revision plan carrying every approved working_assumption object>
Allowed writes: <assigned dossier and revision-delta paths only>

Read the v3 lifecycle, dossier, routing, and ledger contracts. Write complete
dossiers and separate deltas. Return proposed node/index/ledger metadata plus
pointers; bind new artifacts to the active plugin version rather than a legacy
input's version. Record every `based_on` input with logical artifact ID, version,
and path; path-only lineage is invalid. Only the orchestrator writes metadata. Return
new_idea_required on identity drift. On a `proceed_with_assumptions` route,
copy only the exact preflight-approved assumed value, basis, impact if false,
verification needed, verification point, and affected design component into
the authoritative Assumptions subsection. Never choose or complete an
unprovided value. The preflight report remains unavailable to the evaluator.
```

## Methodology/statistics preflight

```text
Role: independently check endpoint, data-method fit, analysis path, risk, and
feasibility; do not score or rewrite the Idea.
Frozen reads: <current dossier and role-necessary context/evidence>
Allowed writes: <one preflight report>

Pair any internal ID with a readable label and source locator; the orchestrator
updates the ledger. Return findings and routes only. Repair must enter a complete
new dossier before evaluation.
```

## Dossier-only evaluator

```text
Role: fresh idea-evaluator; evaluate only, never edit or generate.
workflow_id: <WORKFLOW_ID>
round_id: <ROUND_ID>
reviewer_instance_id: <INSTANCE_ID>
Current dossier: <artifact ID/version/exact path>
Allowed project reads: exactly the dossier path above
Allowed writes: <one evaluation report>

Do not open context, maps, preflight, ledger, URLs, prior versions, deltas,
must-fix lists, prior reports, scores, or decisions. Skill rubric instructions
are allowed. Check the whole dossier, evidence chains, and Claim-Support table.
Every finding needs a readable title and dossier locator. Return
independent_review_pending if isolation is unavailable.
```

Required fields include:

```yaml
reviewed_dossier_ref: {artifact_id: <ID>, version: <VERSION>, path: <PATH>}
complete_dossier_confirmed: true
dossier_only_input_confirmed: true
identity_drift_detected: false
historical_identity_drift_assessed: false
prior_scores_visible: false
prior_versions_visible: false
revision_delta_visible: false
source_edits_performed: false
files_read: [<exact dossier path>]
```

## Biomedical or clinical Idea journal review

Before delegation, the orchestrator materializes the evaluator's already
separated `research-idea-journal-candidate-brief.v1` payload as one unscored and
unranked frozen artifact. It preserves `matching_source_skill:
idea-evaluator`, sets `materialized_by_skill: research-idea-orchestrator`, and
does not repeat or reinterpret the match. The brief sets
`evaluation_fields_included`, `scoring_present`, `ranking_present`, and
`publication_probability_present` to `false`. It contains no evaluator report
reference, score, finding, decision, repair direction, or limitation.

```text
Role: fresh medical-journal-review using route
`idea_journal_match_editorial_review`; independently confirm, reject, or replace
the score-free candidate matches. Do not run a second Idea evaluation, edit the
dossier, rank candidates by prestige, or select an outlet.
workflow_id: <WORKFLOW_ID>
round_id: <ROUND_ID>
reviewer_instance_id: <INSTANCE_ID>
Current dossier: <artifact ID/version/exact path>
Candidate journal-match brief: <artifact ID/version/exact path>
Allowed project reads: exactly the dossier and candidate brief above
Allowed writes: <one medical journal review report>

Do not open the idea-evaluator report, context, maps, preflight, ledger, prior
versions, deltas, readiness reports, portfolio, scores, decisions, or parent
hidden reasoning. The candidate brief is not evidence that a journal is a good
fit. Check each candidate independently against the dossier and current public
scope/article-type sources. Set `publication_probability_assessment: null`;
this dedicated route never estimates publication probability.
Return independent_review_pending if a fresh reviewer or required sources are
unavailable. Idea references use artifact ID, version, and exact path only; do
not request or persist a SHA or digest.
```

Required Idea-specific fields include:

```yaml
review_route: idea_journal_match_editorial_review
reviewed_idea_ref: {artifact_id: <ID>, version: <VERSION>, path: <PATH>}
candidate_brief_ref: {artifact_id: <ID>, version: <VERSION>, path: <PATH>}
files_read: [<exact dossier path>, <exact candidate brief path>]
isolation_mode: fresh_subagent
evaluator_report_visible: false
evaluator_scores_visible: false
source_edits_performed: false
publication_probability_assessment: null
```

## Parallel editorial readiness reviewers

```text
Role: <fresh idea-narrative-assessor | fresh academic-language-assessor>.
Current dossier: <artifact ID/version/exact path>
Reader handoff: <target-reader profile and prior-knowledge fields>
Allowed project reads: exactly the current dossier and reader handoff
Allowed writes: <one narrative report plus YAML repair plan | one language report>

Do not open preflight, evaluator output, prior reports, prior versions, deltas,
workflow state, portfolio, or parent hidden reasoning. Narrative review does not
judge science or terminology standardity. Language review covers the complete
dossier and may verify only core terminology that triggers focused review under its
terminology-review contract.
```

## Editorial repair writer

```text
Role: perform an editorial-only repair; do not evaluate or change science.
Active plugin version: <PLUGIN_VERSION>
Frozen reads: <current dossier, this approved writer brief,
protected-content register>
Forbidden reads: <narrative/language reports, assessor repair plan, prior
dossiers, deltas, preflight, evaluation, or hidden parent context>
Included repair item IDs: <frozen narrative action IDs and actionable language finding IDs>
Source review binding: <narrative assessment, narrative plan, and language assessment logical refs>
Source finding coverage: <each repair item's source item IDs and addressed finding IDs>
Overlapping-action dispositions: <compatible combined targets or none>
Normalized repair actions: <one complete action per included source ID, using
source ID, locator, operation, current problem, target state, required function
or term replacement, content to preserve, content to delete/move and its
destination, dependencies, and acceptance test>
Allowed writes: <one complete next dossier and one revision delta>

Integrity uses logical ID, version, path, and complete index membership. Do not
compute, request, report, or persist a SHA/content hash for either output.

Execute every applicable action, including deletions and moves. Preserve all
registered content. Declare any scientifically necessary change instead of
hiding it in an editorial revision. Bind both outputs to the active plugin
version, never the prior dossier's legacy version. Use `change_type: editorial_repair` for the
dossier and `change_type: editorial_repair_delta` for the delta.

For a long dossier or repair bundle, edit one complete target dossier in
bounded section groups rather than regenerating the whole text in one pass:
(1) reader core, sections 1--4; (2) research plan and technical authority,
sections 5--11; (3) positioning, claim audit, and the sole limitations
authority, sections 12--14; (4) references and whole-dossier concordance. Use
only the normalized repair actions in this brief; do not open the assessor
reports or plan. These are internal
working passes, not partial artifacts, and different writers must not author
independent fragments. Persist only the final complete dossier and delta.
Do not create or finalize the delta until the whole-dossier scan and
deterministic lint pass and the dossier is frozen. Any later dossier edit
invalidates the delta and requires a new scan and rewritten delta; timestamps
or content hashes do not prove this ordering.

Before handoff, map every frozen included repair item ID in the repair bundle to
its revised locator, operation, and acceptance-test evidence in the delta. Do
not claim completion or hand off to preservation while an included action lacks
text-grounded evidence.

Add a compact reader-facing concordance check to the delta for the central
object, primary question or task, primary outcome, and contribution when those
roles exist. Add any other core scientific role only when it actually occurs and
its naming controls design, analysis, evidence status, or interpretation, or
when an accepted repair action addresses it. For each included role, record its one reader-facing name,
first-use locator, competing forms removed or reclassified, and an
all-occurrence scan result. Changing only the report's example locators or
replacing one opaque label with a new compressed label does not close a finding;
any unresolved critical or major language finding blocks handoff.

For every protected item, reopen each revised locator and compare the dossier's
actual words with every enumerated element in `protected_content`. Do not treat
the section heading, intended topic, or the delta's assertion as evidence. If a
claimed element is not present in the dossier text, repair the complete dossier
before handoff.

Keep the delta compact: one row per narrative action, language finding,
protected ID, and concordance role is sufficient when it names the exact revised
locator and observable result. Do not reproduce the protected text, report
instructions, long dossier excerpts, or a second narrative of the complete
study. Compactness never permits a missing ID or an unsupported completion
claim.

When an editorial action explicitly requires author, methodologist, or data
holder confirmation and no approved answer is present, preserve the source
science and mark the action unresolved in the delta. Do not guess the answer or
turn the missing confirmation into a new assumption, restriction, or method
decision.
```

## Content-preservation reviewer

```text
Role: fresh idea-narrative-assessor in preservation mode; compare only.
Frozen reads: <old dossier, new dossier, protected register, revision delta>
Allowed writes: <one content-preservation report>

Return exactly one preservation decision. Do not assess prose readiness,
methods correctness, novelty, impact, or feasibility; do not edit either file.
```

## Adversarial role

```text
Role: <novelty/gap skeptic | feasibility/method skeptic | PI strategy reviewer>
Run in a fresh instance; do not score, rewrite, or read evaluator findings.
Frozen reads: <dossier and role-necessary context/map/anonymous methods facts/ledger>
Allowed writes: <one role report>

Do not read a preflight report, reviewer identity, score, decision, or route;
the methods bundle may contain source facts only. Attack Proposal handoff readiness. Use readable finding titles and dossier
locators. Display an essential internal reference as `ID: readable label` and
resolve it through the ledger. Return objections, dissent, and route only.
```
