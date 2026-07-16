# Evaluation Output Schema

Require:

- reviewer/workflow/round/instance IDs and `isolation_mode: fresh_subagent`;
- input artifact/version and `files_read` containing exactly one dossier path;
- `prior_scores_visible`, `prior_versions_visible`, `revision_delta_visible`, and
  `source_edits_performed`, all false;
- `reviewed_dossier_digest`, `complete_dossier_confirmed: true`,
  `dossier_only_input_confirmed: true`, current-dossier identity consistency,
  and `historical_identity_drift_assessed: false`;
- per-chain judgments for input sufficiency, transformation validity, output
  relevance, objective/hypothesis traceability, and closure;
- per-row Claim-Support judgments for registration, implementation/output
  support, actual-increment accuracy, qualifier retention, and positioning scope;
- six dimension scores, simple mean, gates, fatal flaws, decision, repairs,
  limitations, and unresolved issues; and
- findings with human-readable `title`, `dossier_locator`, severity, and
  rationale. Never use a naked internal workflow ID as a finding title.

Allowed decisions: `promote`, `revise_then_promote`, `revise`, `reframe`,
`keep_as_backup`, or `reject`. `reframe` cannot change the identity anchor.

`hard_gates` names Feasibility, Relevance, Clarity, and Completion with
`pass | fail` plus a dossier-located rationale. `identity_drift_detected` may
flag an internally inconsistent anchor/body or a repair that would replace an
anchor; it never claims comparison with a hidden prior version.
