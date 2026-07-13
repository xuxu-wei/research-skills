# Research Polisher workflow contract

## Dossier manifest

```yaml
research_polisher_dossier:
  artifact_id:
  version:
  plugin_version:
  source_skill: research-polisher-orchestrator
  workflow_id:
  round_id:
  source_artifacts:
    - artifact_id:
      path:
      version:
      sha256:
      summary:
      summary_sha256:
  normalized_context_artifact:
  research_question:
  design:
  methods:
  data:
  existing_results:
  current_claims: []
  current_framing:
  intended_audiences: []
  target_outlets: []
  resource_constraints:
    time:
    people:
    budget:
    data_access:
    technical_capacity:
    maximum_effort_tier:
  evidence_map:
  target_requirements_adapter:
  assumptions: []
  unresolved_inputs: []
```

Do not copy unverified facts into the manifest as confirmed. Bind supplied facts to their source artifact and mark assumptions explicitly.

## Required dispatches

Create one dispatch record per strategist perspective and one for every final evaluation:

```yaml
dispatch:
  dispatch_id:
  workflow_id:
  round_id:
  skill:
  reviewer_instance_id:
  perspective:
  input_artifact_ids: []
  input_versions: []
  input_digests: []
  allowed_files: []
  allowed_write_path:
  peer_outputs_visible: false
  prior_scores_visible: false
```

The three initial strategist dispatches must reference byte-identical dossier and evidence digests. The final reviewer allowlist must omit raw strategy-report and sealed-provenance paths.

## Artifact paths

- `00_input/`: immutable user sources and manifest links.
- `01_context/research_polisher_dossier-vNNN.yaml`: frozen dossier.
- `02_evidence/`: supplied or mapper-produced evidence artifacts.
- `03_strategy/round-NNN/research_polisher_strategy_report-<perspective>.yaml`: sealed strategy reports.
- `04_portfolios/research_polisher_candidate_portfolio-vNNN.md`: anonymous portfolio.
- `04_portfolios/research_polisher_sealed_provenance-vNNN.yaml`: restricted identity mapping.
- `05_evaluations/research_polisher_evaluation_report-vNNN.md`: independent evaluation.
- `05_evaluations/research_polisher_specialist_findings_bundle-vNNN.yaml`: sanitized specialist return, when requested.
- `06_revisions/round-NNN/research_polisher_revision_brief.yaml`: anonymous must-fix brief; keep any delta under the same `research_polisher_*` prefix.
- `07_delivery/research_polisher_selection_dossier.md`: human-selection package.
- `08_state/`: workflow state and artifact index.

## State transitions

```text
initialized -> preprocessing -> artifact_frozen -> pending_review
pending_review -> revision_required -> artifact_frozen -> pending_review
pending_review -> specialist_review_pending -> pending_review
pending_review -> packaging_pending -> human_strategy_selection_required
```

Any active state may move to `clarification_stop`, `deep_research_handoff_required`, `independent_review_pending`, `blocked`, or `stopped` when its declared condition occurs.

## Continuation package

Include plugin/schema version, workflow/round IDs, current state, exactly one pending edge, required skill and perspective, frozen artifact IDs/paths/versions/digests, allowed read/write scope, completed dispatch IDs, unresolved issues, and resume instructions. Do not claim that another task imported or resumed the package unless that event was actually verified.

## Selection handoff

The final dossier must show retained, rejected, and not-assessable options; effort tiers; evaluation findings; dissent; target-verification status; Pareto axes; unresolved issues; source and portfolio lineage; and `selection_status: human_strategy_selection_required`. It must not name an automatic winner.
