# Phase 7 canonical live-input pack

This directory contains the scheduler-owned inputs for the ten Phase 7 live
workflow tasks. It is an execution aid, not runtime evidence, a task export, or
a receipt collection. Passing its local validator does not close a Phase 7
gate.

## Separation boundary

- `manifest.yaml` is scheduler-only. It maps each required slot to an opaque
  execution ID and records the expected terminal state used after the task is
  exported. Never attach this file to a task or expose it to a writer,
  evaluator, panel member, strategist, assembler, or final verifier.
- `sources/*.md` are frozen source artifacts. A task may give an independent
  reviewer only the source files and versioned workflow artifacts allowed by
  that reviewer's contract.
- `prompts/*.md` are launch instructions for the orchestrator. They contain no
  expected decision or terminal state. Reviewer briefs must be rebuilt from
  the frozen artifact contract rather than forwarding a launch prompt.
- The source and prompt filenames are opaque. Preserve them when staging and
  exporting a run.

## Operator procedure

1. Freeze one plugin A source commit and one installed cache identity as
   required by `research-skills-openai/PHASE7-8-RUNBOOK.md`.
2. Create a new task workspace outside the repository checkout. Copy exactly
   one source file into that workspace without changing its bytes. Keep
   `manifest.yaml` outside the workspace.
3. Open a fresh Codex or ChatGPT task, attach the copied source, and send the
   matching prompt verbatim. Do not add an expected result, score, or suggested
   finding.
4. Allow the public orchestrator to route only from the supplied facts. Every
   required reviewer or panel role must use a fresh delegated instance and the
   source must remain read-only.
5. Capture the real task export and all files named by the capture profile.
   Raw captures stay in external staging and remain non-gating until the full
   immutable Release and live-verifier chain succeeds.
6. Compare the observed terminal state with the scheduler-only manifest only
   after the task export is frozen.

For a web task without a writable filesystem, retain downloadable artifacts
with the same logical POSIX paths and capture the durable export offered by the
surface. A copied transcript or screenshot alone is supplementary.

## Capture-support files produced by the task

Each task must write actual UTF-8 JSON files under its `runs/<execution-id>/capture/`
directory. They support later normalization but remain self-reported and
non-gating until bound to the real platform export and external verifier.

- `task-export.json` uses `schema_version: 1` and records the actual platform,
  parent task/thread ID, all observable child task/thread/run or reviewer
  instance IDs, plugin version, registry digest, source commit, workflow,
  observed case classification and terminal state, the external-submission
  boundary, and path/digest bindings for the three files below.
- `actor-manifest.json` uses `schema_version: 1`. Every actor records its real
  instance ID, skill, registry role, allowed read roots, and allowed write
  roots. Panel actors also record panel tier and role; strategy reviewers
  record strategy role. Do not invent a missing platform identifier.
- `artifact-index.json` uses `schema_version: 1`. Every artifact records
  artifact ID, version ID, role, canonical logical path, SHA-256, source skill,
  creating instance, parents, change type, and status.
- `file-access.json` uses `schema_version: 1` and records complete `reads` and
  `writes` entries with actor instance ID, canonical logical path, and SHA-256,
  plus the frozen source's before/after digest comparison.

The task export is not a substitute for the App/task export. If the platform
does not expose a required ID, record the missing capability explicitly and
leave the runtime gate pending.

## Local integrity check

Run from the repository root:

```powershell
python scripts/test_openai_phase7_live_inputs.py
```

The check verifies the exact ten-slot inventory, workflow/case distribution,
opaque filenames, source and prompt SHA-256 digests, source freeze headers,
launch routing, control-driver facts, capture profile, and absence of outcome
oracles in task-visible files.
