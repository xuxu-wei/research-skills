# Delegate Brief Templates

Every brief binds workflow/round, artifact IDs, exact paths, versions, digests,
allowed reads/writes, and failure route. Never rely on parent hidden context.

## Generator or reviser

```text
Role: write complete Ideas; do not evaluate or rank.
Route: <focused_optimization | bounded_exploration>
Frozen reads: <context, maps, route, constraints, current dossier if revising>
Allowed writes: <assigned dossier and revision-delta paths only>

Read the v3 lifecycle, dossier, routing, and ledger contracts. Write complete
dossiers and separate deltas. Return proposed node/index/ledger metadata plus
pointers and digests; only the orchestrator writes metadata. Return
new_idea_required on identity drift.
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
Current dossier: <artifact ID/version/exact path/SHA-256>
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
reviewed_dossier_digest: "sha256:"
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
