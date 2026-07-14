# Deferred shared/public Preview evidence capture

Status: retained engineering reference; deferred and not maintained by the
active personal-owner roadmap

Personal acceptance effect: none. This procedure cannot advance
`owner_observed_ready` and is not required for the current personal plugin.

The material below preserves earlier shared/public hardening work. Do not
expand or execute it as a release requirement unless the owner explicitly
reopens that scope.

This procedure converts one real Codex App task into one non-circular
`R -> E -> V -> I` mini-bundle. Every local command is fail-closed and
non-gating. It never invents a GitHub asset ID, platform task ID, delegation
ID, or provider assertion.

## 1. Freeze the scheduler input without exposing its oracle

Use the committed scheduler-only manifest at
`tests/openai_phase7/live-inputs/manifest.yaml`. Keep that manifest outside the
task workspace and never show it to the task or any reviewer. Give the task
only the selected frozen source and its exact canonical launch prompt.

The task must contain exactly one machine-readable user launch message. A
second user message invalidates the capture, even if the second message looks
benign, because it could carry an outcome oracle. The App `thread/read` export
must also contain structured delegation/collaboration items whose real child
IDs exactly match the delegated actor edges. Self-reported child IDs are not a
platform binding.

The workflow-produced `task-export.json` must include:

- the actual parent task/thread ID and all observable delegated child IDs;
- top-level `entry_mode`, plus matching `scheduler_input.execution_id`, public
  entry, and `entry_mode`;
- exact source and launch-prompt repository paths and SHA-256 digests;
- plugin version, registry digest, source commit, observed workflow/case/state;
- bindings for `actor-manifest.json`, `artifact-index.json`, and
  `file-access.json`; and
- lineage, review state, control evidence, and the no-external-submission
  result.

Do not put the scheduler slot, expected state, control driver, manifest path,
or manifest digest in task-visible material.

## 2. Capture and normalize R

Capture the real App Server thread outside the repository:

```powershell
python scripts/capture_openai_codex_app_server.py `
  --cwd <frozen-source-checkout> `
  --codex-home <app-codex-home> `
  --thread-id <real-parent-thread-id> `
  --include-plugins `
  --output-dir <staging-root>/capture
```

Normalize only from the clean frozen checkout and the actual staged inputs:

```powershell
python scripts/normalize_openai_preview_capture.py `
  --staging-root <staging-root> `
  --capture-dir capture `
  --task-export runs/<execution-id>/capture/task-export.json `
  --scheduler-manifest scheduler/manifest.yaml `
  --execution-id <execution-id> `
  --source-file input/<opaque-source-name>.md `
  --prompt-file input/prompt/<opaque-prompt-name>.md `
  --thread-id <real-parent-thread-id> `
  --evidence-id <unique-evidence-id> `
  --output bundle/<evidence-id>-R.json
```

R embeds the byte-exact App capture, transcript, task export, frozen source,
and launch prompt. It records only a digest and the selected non-oracle fields
from the scheduler manifest; it does not embed the manifest. A dirty plugin,
capture adapter, or canonical input pack stops normalization.

## 3. Derive the receipt and ten-slot collection

Build one candidate receipt from R and its digest-bound support files:

```powershell
python scripts/build_openai_phase7_runtime_capture.py receipt `
  --staging-root <staging-root> `
  --raw-export bundle/<evidence-id>-R.json `
  --task-logical-path runs/<execution-id>/capture/task-export.json `
  --actor-manifest bundle/<actor-manifest-asset-name> `
  --artifact-index bundle/<artifact-index-asset-name> `
  --file-access bundle/<file-access-asset-name> `
  --output candidates/<execution-id>-receipt.json
```

This step cross-checks each actor against one registered workflow edge. Only
`dispatch_mode: delegated` actors with `isolation_mode: fresh_subagent` are
required to have structured platform child IDs. Orchestrated and handoff
actors are not child tasks. At least one immutable file-access read must bind
the selected scheduler source bytes, and no write may target that source.

After all ten real receipts exist, build the collection:

```powershell
python scripts/build_openai_phase7_runtime_capture.py collection `
  --staging-root <staging-root> `
  --plan candidates/receipt-plan.json `
  --scheduler-manifest scheduler/manifest.yaml `
  --output bundle/phase7-runtime-receipts.json
```

The builder requires exact ten-slot coverage and rejects reused slot,
execution, parent, child, task, support-file, source, or prompt bindings.
Each receipt and its task-export binding must repeat the scheduler slot's exact
`entry_mode`; a mismatch at any of the three layers is rejected.

## 4. Obtain GitHub IDs, then build E, V, workspace manifests, and I

Create one draft evidence prerelease at the frozen commit. Upload R first and
save the real GitHub API JSON for the draft Release, R asset, and successful
`main` push run of `.github/workflows/openai-plugin-preview.yml`. Build E only
from those saved API objects:

```powershell
python scripts/build_openai_preview_mini_bundle.py envelope `
  --staging-root <staging-root> `
  --raw-export bundle/<evidence-id>-R.json `
  --release-snapshot api/release.json `
  --workflow-run-snapshot api/source-ci.json `
  --raw-asset-snapshot api/raw-asset.json `
  --output bundle/<evidence-id>-E.json
```

Upload E without replacement. Dispatch
`.github/workflows/openai-preview-draft-bundle-verifier.yml` from `main` with
the exact frozen commit, draft Release ID, source-CI run ID, and R/E/V names.
That separate workflow downloads R and E by their API asset IDs, executes the
committed independent verifier, uploads V once without clobbering, and retains
V plus its post-upload API object.

After every referenced task file and the receipt collection has a real draft
Release asset API object, run `workspace-manifest`. It must cover every logical
path referenced by the selected receipt; no local sidecar satisfies coverage.

Finally prepare a mini-bundle plan containing exactly one R, E, and V plus all
supporting assets, then build I:

```powershell
python scripts/build_openai_preview_mini_bundle.py index `
  --staging-root <staging-root> `
  --plan api/mini-bundle-plan.json `
  --release-snapshot api/release-after-support.json `
  --workflow-run-snapshot api/source-ci.json `
  --output bundle/<evidence-id>-I.json
```

I intentionally does not index itself. Upload I once, verify the complete
asset inventory, and only then publish the draft as an immutable prerelease.
The later live verifier downloads I through its own GitHub API asset object,
re-queries the successful dedicated V workflow run recorded in V, and rejects
a failed, missing, reused, or mismatched run. It also API-requeries the Actions
run currently executing the live verifier and binds its repository, workflow
path and ID, event, source SHA/ref, run attempt, actor, and in-progress state.
The source-CI, draft-V, and current verifier run IDs must be pairwise distinct.
The protected revalidator later re-queries that current run and requires
`completed` plus `success` before acceptance.

## 5. Stop conditions

Leave the slot pending if any required machine-readable export, exact prompt,
structured platform child ID, source read, clean source identity, GitHub API
object, successful source-CI run, dedicated V run, or immutable Release object
is unavailable. Screenshots, handwritten receipts, synthetic fixtures, and
locally chosen IDs remain supplementary or test-only evidence.

## 6. Phase 8 adapter stop

The current Phase 8 normalizer has no registered platform-origin adapter for
reviewer scope, built-in Search traces, inactive Deep Research capability
state, or completed Deep Research. Do not use the Phase 7 App Server procedure
or a locally authored `platform_export`, `chatgpt_export`, or
`capability_export` JSON as a substitute. Those documents may exercise the
mechanical schema, but all twelve production slots remain pending and
non-counting.

A future positive adapter must be repository-defined and bind an exact capture
endpoint and response schema, parser ID, composite code digest, and mutation
tests. Recapture the affected slot after that adapter lands; GitHub R/E/V/I
witnessing alone cannot establish the missing platform origin.
