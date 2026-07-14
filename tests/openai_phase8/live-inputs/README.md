# Phase 8 canonical live-input pack

This directory is a scheduler-only, non-evidence input pack for the twelve
current-release Phase 8 executions. `manifest.yaml` contains the scheduling
classes, expected states, finding labels, and control condition. It must never
be attached to a task, delegated reviewer, Search run, or Deep Research run.

The six reviewer inputs are exact byte copies of the frozen A01-A03 source
artifacts: each pair receives identical source bytes through different opaque
paths and different launch prompts. Reviewers receive only a generated
source-only blind bundle, the frozen input, and the declared resources of their
reviewer skill. The launch task dispatches exactly one fresh reviewer and does
not assess the source inline.

The three Search prompts require the native ChatGPT/Codex Search capability,
two or more identity-verified primary or authoritative sources, and complete
claim-to-source traceability. The two Deep Research prompts require the real
user-start event and target the full handoff-to-resume chain. No concrete
platform-origin adapter is currently registered for reviewer scope, Search
tool traces, the inactive capability control, or completed Deep Research.
Therefore all twelve slots remain pending/non-counting. Structured JSON and
exact JSON pointers are checked only as mechanical capture claims; a filename,
`artifact_type`, or internally consistent self-labelled document cannot make
them platform-derived. Markdown, Word, PDF, screenshots, or self-labelled JSON
also cannot establish provider completion.

All generated files are capture inputs only. Repository hashes, task-authored
exports, and this manifest do not attest a run. Promotion requires both a
registered concrete platform capture adapter and the immutable GitHub R/E/V/I
chain with an independent executable verifier.

## Production normalizer input contract

The future Phase 8 production normalizer should require these exact
`capture/task-export.json` fields for every slot:

- `schema_version`, `platform`, `surface`, `evidence_kind`, `export_id`,
  `task_id`, `parent_task_or_thread_id`, `observable_child_or_delegate_ids`,
  `captured_at`, and `automatic_external_submission`;
- `plugin_version`, `source_commit`, `manifest_sha256`, `registry_sha256`, and
  `skill_tree_sha256`;
- `scheduler_input.execution_id`, `scheduler_input.input.path`,
  `scheduler_input.input.sha256`, `scheduler_input.launch_prompt.path`,
  `scheduler_input.launch_prompt.sha256`, and the three false visibility flags
  for scheduler manifest, scheduler labels, and expected outcomes;
- `capability.name`, `capability.state`, `capability.task_or_tool_run_ids`,
  `supporting_artifacts`, and `slot_payload`. Every supporting-artifact binding
  has exactly `artifact_type`, `path`, `sha256`, and `size_bytes`.

Reviewer exports additionally need `reviewer_run.run_id`, `reviewer_skill`,
`delegated_thread_id`, `reviewer_instance_id`, `reviewer_instance_created_at`,
`platform_receipt_id`, and bindings for the blind bundle, exact delegated
prompt, raw transport output, read/write-scope export, and report inside
`slot_payload.reviewer_run`. The scope export contains actual `files_read`,
`files_written`, `input_digest_before`, `input_digest_after`, and
`source_edits_performed`.

Search exports additionally need `slot_payload.retrieval.receipt_id`, `kind`,
`question_class`, `query`, `query_or_request_digest`, `opened_sources`,
`material_claim_trace`, and bindings for raw Search output and citation export.

Until a concrete exact-schema Deep Research adapter is implemented, those two
exports use `completion_projection.status: pending`, bind a handoff and a
self-contained continuation package, retain one pending edge, and stop. They
must not claim session/run/completion IDs. A future adapter may project the
user-start event, session/run IDs, provider completion, raw output, citations,
mapper return, resume transaction, identical returned/resumed artifact set, and
strictly ordered timestamps only from the adapter's registered machine-readable
export schema.

The inactive control additionally needs, under `slot_payload.retrieval`, the
capability-state export, self-contained handoff and continuation bindings,
`workflow_paused: true`, `downstream_evidence_map_created: false`, and
`inline_simulation: false`.
