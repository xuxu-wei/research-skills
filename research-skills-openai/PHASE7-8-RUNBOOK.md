# Phase 7-8 External Evidence Runbook

Status: operational plan; real external evidence is pending
Applies to: personal Experimental/Preview releases only
Current A candidate: `0.7.0-preview.1`

This runbook is the execution checklist for closing Roadmap Phases 7 and 8.
The schemas, validators, generated reports, and release ledger remain the
machine-readable authority. If this document and a validator disagree, stop,
fix the contract or this runbook, regenerate the reports, and do not promote a
release on prose alone.

## Execution work packages and exit criteria

Run the work packages in order. WP2 through WP5 may be scheduled in parallel
only after WP1 freezes one shared A source identity; their accepted evidence
must still bind that exact identity. WP6 is performed for every external
record, not as a one-time batch assertion.

| Work package | Execution | Exit criterion |
| --- | --- | --- |
| WP0 — local preflight | Regenerate the registry, reports, and ledger; run every repository, workflow, context, corpus, evidence, and canonical-plugin validator; complete the structural/protected accepted-state ingestion paths | 49 skills, 7 explicit entries, 6 implicit entries, 20 independent reviewers, 17/17 mode replays, 20/20 corpus cases, zero audit errors/warnings, zero report drift, and accepted reports/ledger replay through production live callbacks without bypassing the full release validator |
| WP1 — freeze A | Commit and push one candidate; wait for Preview CI; publish a non-draft immutable prerelease; verify `main` protection and retain previous N | Version, 40-hex source commit, tag, prerelease, CI run, canonical validator, marketplace resolution, and branch protection all resolve to one source identity |
| WP2 — Phase 7 runtime | Run five workflow happy paths and five input-driven controls in ten fresh tasks; capture actors, file access, lineage, dissent, findings, packages, and source hashes | Exactly 5/5 happy and 5/5 control receipts pass semantic validation; no identity overlap, source edit, hidden dissent/fatal finding, false-ready result, or automatic external submission |
| WP3 — Phase 7 distribution | Upgrade through the marketplace, explicitly reinstall, discover in a fresh task, then roll back to immutable previous N | Upgrade, reinstall, and discovery share one N+1 cache identity at 49/7/6; rollback uses a distinct previous cache/commit with no mixing; all eight release-ledger evidence classes pass live re-query |
| WP4 — Phase 8 reviewers | Dispatch two fresh source-only blind reviews for each of A01, A02, and A03 | 6/6 runs use distinct delegated instances; outcome-oracle exposure and source edits are zero; contract-level state agrees per pair or visible disagreement blocks completion |
| WP5 — Phase 8 retrieval | Run current/exact/narrow built-in Search, two user-started Deep Research handoff-return-resume cycles, and one inactive control | 3/3 Search, 2/2 completed Deep Research, and 1/1 inactive control pass; primary/authoritative source identity and material-claim traceability are 100%; all evidence is current and within clock bounds |
| WP6 — external attestation | Publish every WP1–WP5 R -> E -> V -> I mini-bundle in one immutable evidence Release, run the first verifier, then publish the derived ledger/collections in a distinct immutable candidate Release and run the protected verifier | Every accepted record has unique immutable asset IDs/digests, a successful historical verifier workflow witness, a fresh GitHub API re-query, `preview_attested=true`, and `provider_verified=false`; both Release tags resolve to the same frozen source |
| WP7 — derive A closure | Re-ingest the external collections, regenerate reports/ledger, rerun the complete validation suite, and independently audit the candidate | Phase 7 and Phase 8 are both derived as `complete_preview_attested`; no pending A gate, manual status edit, stale evidence, false-ready path, or uncommitted source delta remains |
| WP8 — policy-only B | Enable Research Polisher implicit invocation, bump the Preview version, regenerate metadata, then rerun CI/install/discovery/routing | Installable diff is restricted to the allowlist; marketplace upgrade/reinstall succeeds; fresh discovery is 49/7/7; all seven public-entry positive and negative routing checks pass |

The local implementation and validators can prepare WP0 and verify downloaded
evidence. WP1, live task execution in WP2/WP4/WP5, marketplace operations, and
user-started Deep Research require the corresponding authenticated GitHub and
ChatGPT/Codex account capabilities. If a capability is absent, record the gate
as pending; do not replace it with a synthetic run.

## Non-negotiable evidence boundary

Deterministic replays, synthetic corpus cases, mutation tests, locally authored
receipts, screenshots, and historical observations are preflight evidence.
They can demonstrate that a validator rejects or accepts a shape, but they do
not complete a live slot. In particular:

- the current 17/17 Phase 7 mode replay is not one of the ten live runs;
- the current 20/20 anonymous Phase 8 corpus is not one of the twelve live
  reviewer/retrieval slots;
- historical `0.5.0-preview.1` or `0.6.0-preview.1` observations cannot be
  relabelled as current `0.7.0-preview.1` evidence;
- an App Server smoke capture remains `capture_only` until the full external
  evidence chain passes; and
- a locally consistent evidence bundle remains non-gating until the executable
  live verifier re-queries GitHub.

Never edit a status field from `pending` to an accepted state by hand. Phase
status must be derived by the validators from accepted receipts and the release
ledger.

## A and B release contract

### Release A: prove the frozen workflow set

Release A is the full Phase 7-8 evidence candidate. Freeze it with all of these
properties:

| Property | A requirement |
| --- | --- |
| Plugin version | `0.7.0-preview.1`, unless a later version is deliberately substituted before evidence collection |
| Installed skills | 49 |
| Explicit-callable public entries | 7 |
| Implicit prompt entries | 6 |
| Research Polisher | discoverable and explicitly callable; `allow_implicit_invocation: false` |
| Source | one immutable 40-hex commit, pushed to `main` and tagged by a published GitHub prerelease |
| Required CI witness | successful `push` run of `.github/workflows/openai-plugin-preview.yml` on that exact source commit |

Do not collect accepted evidence across multiple source commits. If the plugin
manifest, registry, skill tree, validation contracts, or other installable
behavior changes after collection begins, abandon the incomplete candidate,
bump the Preview version as required, freeze a new source identity, and rerun
the affected evidence. Never overwrite assets on the old evidence release to
make them look current.

### Release B: unlock only the seventh implicit entry

Release B is expected to be `0.7.0-preview.2`. It may be created only after A
has completed both Phase 7 and Phase 8 at least at `preview_attested`. Its only
installable behavior change is the allowlisted Research Polisher entry-policy
delta:

- change `research-polisher-orchestrator/agents/openai.yaml` so
  `allow_implicit_invocation` becomes `true`;
- update the plugin version in `.codex-plugin/plugin.json`;
- update the identical plugin version and Research Polisher invocation policy
  in `workflow-registry.yaml`; and
- regenerate derived package/ledger metadata required by those changes.

Release notes and evidence records may describe the delta, but no skill body,
resource, workflow edge, reviewer contract, dependency, or other installable
behavior may change in B. Any additional installable delta invalidates the
short B path and requires the full Phase 7-8 evidence program to be rerun.

For a valid B, rerun the Preview CI, marketplace upgrade, explicit reinstall,
fresh-task discovery, and routing checks. The expected discovery contract is
49 installed skills, seven explicit-callable public entries, and seven implicit
prompt entries. Confirm that each of the seven intended entries routes only its
declared request class, including Research Polisher's negative boundaries for
copyediting, new-idea generation, and ordinary literature retrieval.

## Evidence levels

| Level | What establishes it | Gate effect | Required wording |
| --- | --- | --- | --- |
| `capture_only` | A redacted App Server/task/tool export or other raw capture | None | Raw captured material; not accepted evidence |
| `preview_attested` | The complete immutable GitHub Release bundle plus a successful independent executable live re-query | Sufficient for this personal Experimental/Preview release | GitHub-witnessed Preview evidence; never OpenAI/provider verified |
| `provider_verified` | All Preview requirements plus a separately registered authenticated provider adapter and bound provider receipt | Optional stricter future completion state | Provider verified only after the registered adapter passes |

The offline validator proves structure, identity, chronology, and byte
integrity only. Its successful result must still report `gate_eligible: false`
and `accepted: false`. No authenticated provider adapter is currently
registered, so the planned release target is `preview_attested`, not
`provider_verified`.

## The R -> E -> V -> I evidence DAG

Create every accepted evidence bundle in this order. Each node is a distinct
GitHub Release asset with its own immutable asset ID, byte size, and SHA-256.

```text
R: redacted raw export
  -> E: externally witnessed evidence envelope
       -> V: independent verifier report
            -> I: final Release asset index
```

1. **R -- raw export.** Capture the real task, thread, Search, Deep Research,
   install, discovery, or rollback event. Redact credentials and account data.
   Preserve real task/run/instance IDs, timestamps, prompts, outputs, file
   access, tool/source traces, and artifact digests required by the applicable
   schema. Upload R first and record its GitHub Release asset ID, size, and
   digest.
2. **E -- evidence envelope.** Bind R's actual asset ID and digest to the frozen
   plugin version, source commit, manifest digest, registry digest, complete
   skill-tree digest, capture adapter, task/thread identity, GitHub release,
   and expected independent verifier. Upload E after R. E must not contain its
   own digest or a forward reference to V or I.
3. **V -- verifier report.** Run the declared independent verifier against the
   actual bytes of R and E. V binds the uploaded E asset ID and digest, R asset
   ID and digest, source identity, verifier ID, committed verifier-code digest,
   verdict, and verification timestamp. Upload V after E. V must not digest I.
   A provider-level V must additionally bind and check a distinct provider
   receipt; that path is unavailable until an authenticated adapter exists.
4. **I -- final asset index.** After R, E, and V have final GitHub asset IDs,
   create exactly one mini-bundle index for that single evidence record. The
   index identifies the immutable prerelease, GitHub witness run, source
   identity, and every evidence asset's ID, kind, size, and digest. Upload I
   last. Each I must locate exactly one E and one V; do not reuse one index for
   multiple envelopes or create a circular or substituted payload.

If an asset must be corrected, do not replace it under the same evidence claim.
Create a new evidence release/tag or other immutable bundle identity and repeat
the DAG.

The indexed V asset is the non-gating bundle-integrity verifier report. It is
distinct from the later GitHub Actions live-verifier run. Upload R/E/V/I first,
dispatch the live-verifier workflow second, and record that successful run ID
only in the release-ledger evidence locator afterward. The run ID is not an
input to R/E/V/I, so this ordering has no self-reference or upload race.

## Freeze and release prerequisites

Complete these steps before counting any runtime slot:

1. Confirm GitHub authentication can read Actions, repository settings, tags,
   releases, and Release assets and can publish the intended prerelease. If
   authentication fails, leave all external gates pending.
   Use `.github/workflows/openai-preview-accepted-evidence.yml`, which runs
   trusted default-branch code inside a protected GitHub Environment. Configure
   that environment before Freeze A and store
   `OPENAI_PREVIEW_GOVERNANCE_TOKEN` only in that environment, backed by a
   single-repository fine-grained PAT or GitHub App token with
   Administration(read), Actions(read), and Contents(read). Never expose this
   credential to an arbitrary `source_commit` checkout. The default
   `github.token` cannot read `/branches/main/protection`; a missing,
   under-scoped, or unapproved governance job must fail closed.
2. Confirm the selected ChatGPT/Codex surface can actually access the frozen A
   plugin and the capabilities required by the planned slot. If ChatGPT web
   installation, sharing, discovery, Search, or Deep Research is unavailable,
   record the missing capability and do not substitute a local transcript.
3. Run the full validation list in `AGENTS.md` and ensure generated reports and
   the release ledger are current.
4. Commit the A source, push it to `main`, and record the full 40-hex commit.
5. Wait for a successful `push` run of `OpenAI Plugin Preview` on exactly that
   commit. Confirm that the canonical plugin validator ran in that workflow.
6. Verify through the GitHub API that `main` requires the designated Preview CI
   check. A workflow file in the repository is not branch-protection evidence.
7. Create the evidence Release as a draft at the frozen commit, upload every
   R/E/V/I asset, then publish it as an immutable non-draft GitHub prerelease.
   The live verifier must confirm both that its tag still resolves to the
   frozen commit and that the Release API reports it as immutable. Keep the
   previous N release available for rollback.
8. Enumerate Release assets through the dedicated paginated assets endpoint
   until exhaustion. Reject duplicate IDs or names, truncated enumeration, or
   any indexed asset absent from the complete listing.
9. Generate or check `reports/release-ledger.json`. The source identity must
   match the committed manifest, registry, skill tree, license, marketplace,
   and validation-contract identities. External evidence records persist only
   immutable GitHub locators and digests; raw exports stay out of `main`.

## Phase 7: ten live runtime slots

Run every row in a new task against the same installed A cache. The generator
or drafter, each evaluator, each panel member, and the finalizer must have the
role separation required by the workflow. Capture actor manifests, complete
read/write sets, frozen source before/after hashes, versioned lineage, dissent,
fatal findings, final state, artifact index, and absence of automatic external
submission.

| Slot | Workflow | Required result |
| --- | --- | --- |
| `phase7-idea-happy` | Idea | `human_signoff_required` |
| `phase7-idea-control` | Idea | `stopped` after independently reviewed no incremental gain or explicit stop |
| `phase7-proposal-happy` | Proposal | `human_signoff_required` |
| `phase7-proposal-control` | Proposal | `blocked` for a fatal data-availability constraint |
| `phase7-article-happy` | Article | `human_signoff_required` |
| `phase7-article-control` | Article | `blocked` for a source-level fatal finding |
| `phase7-perspective-happy` | Perspective | `human_signoff_required` |
| `phase7-perspective-control` | Perspective | `stopped` after independently reviewed no incremental gain or explicit stop |
| `phase7-research-polisher-happy` | Research Polisher | `human_strategy_selection_required` |
| `phase7-research-polisher-control` | Research Polisher | `no_defensible_option` after every bounded option fails |

The controls are input-driven workflow outcomes. Reviewer unavailability is a
separate fault-injection test and must not replace any of the five live control
slots.

For each run:

1. freeze the input artifact IDs, versions, paths, and digests;
2. open a new ChatGPT/Codex task and invoke the intended public entry;
3. require fresh delegated reviewer instances and retain their real opaque
   instance IDs;
4. finish at exactly the declared human-handoff or valid control state;
5. export the task and artifacts into an external staging directory, never the
   source tree;
6. create and upload its R -> E -> V -> I bundle; and
7. ingest only the live-verifier result into the runtime receipt collection.

Each of the ten Phase 7 mini-bundles must also index one workspace manifest,
the identical frozen ten-receipt collection, the task export, actor manifest,
artifact index, and every file referenced by the receipt's read/write sets or
artifact index. The workspace manifest maps canonical POSIX logical paths to
the corresponding Release asset ID, size, and digest. Use unique Release asset
names per mini-bundle; no local sidecar or unindexed file may satisfy a path.
The runtime evidence runner snapshots all indexed bytes in memory, performs the
live GitHub re-query, materializes only those bytes into a fresh temporary
workspace, runs the semantic receipt validator, and re-hashes both source and
temporary files before accepting all ten slots.

The Codex App capture helper can produce the redacted R material:

```powershell
python scripts/capture_openai_codex_app_server.py `
  --cwd <repository-root> `
  --codex-home <app-codex-home> `
  --thread-id <real-thread-id> `
  --include-plugins `
  --output-dir <external-staging-directory>
```

The helper may also capture `skills/list`; experimental `plugin/list` is only
supplementary. Neither call alone proves marketplace installation, fresh-task
discovery, or an accepted workflow run.

For ChatGPT web, use only the account/workspace surface that actually exposes
the installed or shared A plugin. In a new chat, record the visible plugin
identity and version, entry discovery, exact user prompt, returned artifacts,
and real task/run identifiers through the export mechanism available on that
surface. Redact account and sharing details that are not required by the
schema. A browser screenshot or copied conversation is supplementary only; if
the surface provides no durable export or the plugin is not discoverable, the
slot remains pending.

## Phase 7: distribution and repository gates

Complete the runtime slots and all distribution gates against the identical A
source identity:

- immutable source commit exists in GitHub;
- successful repository Preview CI is bound to that commit;
- the canonical plugin validator is present and successful in that CI run;
- the marketplace resolves the A source commit;
- marketplace upgrade succeeds;
- explicit reinstall succeeds;
- a new task discovers exactly 49 installed skills, seven explicit-callable
  entries, and six implicit entries;
- install, reinstall, and discovery bind the same N+1 cache content identity;
- rollback selects a distinct previous N cache, source commit, instance ID,
  path, and content identity without cache mixing; and
- GitHub API evidence confirms the required Preview check protects `main`.

Install, reinstall, discovery, and rollback R assets must include a complete
provider-exported cache inventory. A path string, version label, or
`cache_mixing_absent` boolean is insufficient.

## Phase 8: twelve live slots

Phase 8 has six independent-review slots and six retrieval slots. All use the
same current A source identity and the same evidence DAG.

### Six independent-review runs

Run two fresh, mutually isolated reviewer instances for each opaque case:

| Case | Domain/route | Required runs |
| --- | --- | --- |
| A01 | Proposal fatal/readiness route | two fresh delegated instances |
| A02 | Article fixable/evaluation route | two fresh delegated instances |
| A03 | Perspective eligible-with-visible-dissent route | two fresh delegated instances |

Each dispatch must use the validated source-only blind bundle. Reviewer-visible
case, source, prompt, bundle, thread, run, and instance identifiers must be
opaque and contain no outcome oracle. Reviewers may read only the frozen source,
blind bundle, and declared reviewer resources; they may write only their review
report. They cannot see prior scores, decisions, reviewer outputs, expected
findings, revision instructions, or outcome-bearing paths. Preserve all
disagreement and block completion if contract-level final states disagree.

### Three built-in Search runs

Capture one current, one exact, and one narrow-academic Search case. Each case
must use ChatGPT/Codex built-in Search, open at least two identity-verified
primary or authoritative sources, and map every material claim to the opened
sources. Record the real task/run identity, tool trace, queries, opened URLs or
source IDs, timestamps, citations, outputs, and artifact digests.

### Two completed Deep Research cycles

For each cycle, capture the complete chain:

```text
mapper handoff
  < explicit user start
  < provider run completed
  < mapper-contract return
  < unique pending-edge resume
```

The provider completion record must bind its session/run ID, success status,
completion time, and raw-output digest. The mapper return and resumed workflow
must bind the same evidence-artifact IDs, paths, and SHA-256 digests. Each cycle
uses unique task, session, run, return, resume, and pending-edge identities and
opens only identity-verified primary or authoritative sources with full
material-claim traceability.

### One inactive-Deep-Research control

Run one case while Deep Research is inactive or unavailable. The workflow must
return `deep_research_handoff_required`, emit a self-contained continuation
package, and stop without simulating Deep Research inline. Capture the real
task/capability state and continuation artifact.

All accepted Phase 8 evidence must be no more than 90 days old and no timestamp
may exceed the verification clock by more than five minutes.

## Package, verify, and record the evidence

After uploading the immutable R -> E -> V -> I assets, first run the offline
integrity check. Success here is necessary but deliberately non-gating:

```powershell
python scripts/validate_openai_preview_evidence_bundle.py `
  --asset-index <downloaded-index> `
  --asset-dir <downloaded-asset-directory> `
  --expected-source-identity <source-identity-file> `
  --envelope <downloaded-envelope>
```

Then dispatch `.github/workflows/openai-preview-evidence.yml` with the immutable
prerelease tag, full source commit, and `asset_index_pattern` matching all
one-record asset indexes that the first pass should witness. The workflow
resolves the unique indexed envelope inside each mini-bundle; callers do not
supply a separate envelope pattern. For the ten-slot Phase 7 semantic batch,
set both `phase7_runtime_receipts_name` and a Phase-7-only
`phase7_asset_index_pattern`; supplying only one is an error. For the
twelve-slot Phase 8 semantic batch, set both receipt collection names and a
Phase-8-only `phase8_asset_index_pattern`; supplying an incomplete group is an
error. The two dedicated patterns must differ, select exactly 10 and 12
indexes respectively, and must not share indexes or physical assets. Leaving
both semantic input groups empty runs only the per-bundle integrity and live
Preview checks. It does not validate or promote an accepted release ledger;
that operation belongs to the separate protected accepted-state path.
That workflow must:

1. check out the exact source commit and confirm the tag resolves to it;
2. re-query the published non-draft GitHub prerelease;
3. download the real Release assets;
4. reproduce the committed source identity;
5. run the offline integrity validator without promoting its result; and
6. run `tests/openai_phase8/verify_preview_evidence.py`, which independently
   re-queries the GitHub Release, successful main-push CI witness, committed
   verifier, index, and assets before returning `preview_attested`; and
7. when the Phase 7 receipt input is present, run
   `scripts/validate_openai_phase7_runtime_evidence.py` and require 10/10
   semantically valid, source-immutable Preview receipts;
8. when both Phase 8 collection inputs are present, run
   `scripts/validate_openai_phase8_external_evidence.py` and require six blind
   reviewer runs plus the 3/2/1 Search, completed-Deep-Research, and inactive
   control distribution; and
9. publish exactly one run-bound, non-overwriting Actions artifact named
   `openai-preview-live-verifier-summary-<run-id>`. Its single JSON member binds
   that historical workflow run to the repository, source commit, prerelease,
   and every verified R/E/V/I asset locator.

Only a successful non-synthetic live result with `gate_eligible: true`,
`counts_as_preview_attested: true`, and
`counts_as_provider_verified: false` closes a Preview slot. Persist its
immutable Release/run/asset locators and digests in the ledger; do not commit
the raw exports. Re-query GitHub once more when validating the ledger, including
the successful historical workflow run, its unexpired single-file summary
artifact, current branch protection, the prerelease, and every indexed asset.
A deleted, replaced, failed, mismatched, or stale object cannot survive as a
cached acceptance claim. The run-summary artifact binds the historical run to
its actual release/tag/assets because the GitHub run API does not expose
workflow-dispatch inputs.

Release-ledger promotion therefore requires two verifier passes and two
immutable Releases. The implemented first pass validates the R/E/V/I bundles
from the immutable **evidence Release** and publishes the run-bound summary
artifact without receiving any governance secret. After it succeeds, populate
each ledger locator with that historical run and the exact evidence-Release
assets. Create a different tag at the same frozen commit, upload the candidate
ledger plus the accepted Phase 7 and Phase 8 collections to a draft
**candidate Release**, and publish that second Release as immutable. This split
is mandatory because an immutable evidence Release cannot accept a ledger that
is created only after the first verifier run.

Dispatch `.github/workflows/openai-preview-accepted-evidence.yml` from the
default branch with both distinct tags and the four candidate filenames. The
workflow re-queries both Releases and resolves each exact `refs/tags/...`
binding, including bounded annotated-tag peeling, rather than using an
ambiguous branch/tag commit endpoint. It keeps candidate
assets outside the evidence bundle root, stages only the ledger and three
collections in an isolated copy of the trusted checkout, regenerates the Phase
7 and Phase 8 reports, downloads accepted history into separate directories,
runs `scripts/validate_openai_release_evidence.py` through its production live
callback, and then reruns the complete Preview release validator with a fresh
production callback. Only those two validation steps receive the protected
governance credential. The locator must continue to reference the first pass;
it must not be rewritten to trust the second pass that is currently consuming
it. The final summary independently binds the candidate ledger path and digest
to the candidate Release inventory and standalone runner, validates accepted
history as a separate scope, and rejects any repeated evidence ID or R/E/V/I
content digest across the current 8 + 10 + 12 chains. Before upload, the
workflow re-proves the trusted checkout and both isolated validation workspaces;
the non-overwriting artifact upload is the last step. Consumers must still
re-query the exact run attempt and protected-Environment deployment and accept
the artifact only when the run conclusion is successful.

The ordinary Preview CI performs fail-closed structural validation and never
claims that it repeated the external re-query. An accepted ledger is releasable
only when the protected accepted-state workflow and the complete repository
validator both succeed for the same immutable source identity. A serialized
success flag or locally authored verifier result cannot bridge the two paths.

When the ledger contains an accepted previous release, the second pass first
runs `scripts/download_openai_release_ledger_assets.py`. It downloads each
distinct historical locator tag from the same repository into an isolated
child directory. This is required for B and later histories: assets from the
current `release_tag` alone cannot validate accepted A evidence, and flattened
same-name assets from different releases must never be mixed.

ChatGPT web evidence must retain the real task, Search, or Deep Research export
available from that surface. GitHub witnessing can raise a valid capture to the
personal `preview_attested` level, but it does not establish that OpenAI signed
or authenticated the capture. Until a registered provider adapter exists, keep
`provider_verified: false` in every accepted record.

## Acceptance matrix

| Gate | A Preview acceptance | Provider-complete acceptance | Current state |
| --- | --- | --- | --- |
| Phase 7 deterministic replay | 17/17 positive modes and all declared negatives pass | Same | Passes locally; non-live |
| Phase 7 workflow runtime | 5/5 happy plus 5/5 controls pass the live GitHub verifier | The same ten also pass an authenticated provider adapter | 0/10 accepted |
| Phase 7 safety/governance | zero false-ready, identity overlap, out-of-scope reviewer writes, hidden fatal findings, or automatic submission; 100% lineage/dissent/source immutability | Same | Synthetic guards pass; live receipts pending |
| A discovery | 49 installed, 7 explicit-callable, 6 implicit, one source/cache identity | Same plus provider verification where required | Pending |
| A release/distribution | source, CI, canonical validator, marketplace, upgrade, reinstall, discovery, rollback, and branch protection all pass live re-query | Same plus authenticated provider adapter where applicable | 13 Phase 7 completion gates pending in the generated report |
| Phase 8 corpus | 20/20 deterministic cases, fatal/blocking recall 100%, other major-finding recall at least 90%, false-ready zero, and isolation/lineage/edit-boundary/dissent each 100% | Same | Passes locally; non-live |
| Phase 8 reviewers | 6/6 accepted fresh isolated runs | The same 6/6 provider verified | 0/6 accepted current-version runs |
| Phase 8 Search | 3/3 accepted current, exact, and narrow cases | The same 3/3 provider verified | 0/3 accepted current-version runs |
| Phase 8 Deep Research | 2/2 complete user-started handoff-return-resume cycles | The same 2/2 provider verified | 0/2 accepted cycles |
| Phase 8 inactive control | 1/1 pauses with a continuation package | The same 1/1 provider verified | 0/1 accepted current-version control |
| Evidence integrity | every accepted slot has a unique, acyclic R -> E -> V -> I chain and passes live GitHub re-query | Same plus bound authenticated provider receipt | Tooling and synthetic reachability pass; no current live bundle accepted |
| B policy-only release | A phases complete at `preview_attested`; allowed delta only; CI, upgrade, reinstall, discovery, and routing rerun at 49/7/7 | A phases complete at `provider_verified`, if that stronger claim is desired | Not eligible while A gates are pending |

Completion states are derived as follows:

- if any required live or distribution gate is pending, Phase 7 remains
  `in_progress_live_and_release_evidence_pending` and Phase 8 remains
  `in_progress`;
- if every required A slot and distribution gate passes the live GitHub
  verifier, each phase may become `complete_preview_attested`;
- `complete_provider_verified` is reachable only when all of the same evidence
  also passes a registered authenticated provider adapter; and
- Research Polisher remains explicit-only until both Phase 7 and Phase 8 reach
  an accepted completion state and the policy-only B release passes its own
  install/discovery/routing checks.

## Current pending baseline

At the time this runbook was added, generated reports still state:

- Phase 7 deterministic replay passes 17/17 modes, but all ten current-version
  runtime receipts are `pending_live_evidence`, 0/10 are accepted, and all 13
  completion gates are pending;
- Phase 8 deterministic corpus evaluation passes 20/20 cases, but 0/6 live
  reviewer runs, 0/3 Search runs, 0/2 Deep Research cycles, and 0/1 inactive
  control are accepted for the current version;
- no current-release R -> E -> V -> I bundle has passed the live GitHub
  verifier; and
- no authenticated provider adapter is registered.

Accordingly, neither phase is complete, Release B is not yet eligible, and no
synthetic or historical evidence should be presented as live acceptance.

## Final execution checklist

- [ ] Freeze and push A; record its exact source identity.
- [x] Implement the protected accepted-state workflow, production callback,
      immutable tag/Release re-query, and paginated asset validation.
- [ ] Configure the protected environment and its single-repository read-only
      governance credential, then exercise both structural and accepted-state
      paths without exposing the credential to caller-selected code.
- [ ] Pass the main-push Preview CI and verify branch protection through GitHub.
- [ ] Publish the immutable A evidence Release, run the first verifier, publish
      the separate immutable candidate Release, verify both tag-to-commit
      bindings, enumerate evidence assets with pagination, and retain immutable
      previous N.
- [ ] Complete and attest all ten Phase 7 live runtime slots.
- [ ] Complete marketplace upgrade, reinstall, fresh discovery, rollback, and
      cache-inventory evidence.
- [ ] Complete and attest six Phase 8 independent-review runs.
- [ ] Complete and attest three built-in Search runs.
- [ ] Complete and attest two user-started Deep Research cycles.
- [ ] Complete and attest one inactive-Deep-Research control.
- [ ] Regenerate reports/ledger and pass every validator with no pending A gate.
- [ ] Confirm both phases derive `complete_preview_attested` (or the stricter
      `complete_provider_verified`) without manual status edits.
- [ ] Create B with only the allowlisted policy/version/registry delta.
- [ ] Pass B CI, upgrade, reinstall, fresh discovery, and seven-entry routing.
- [ ] Keep the plugin labelled personal Experimental/Preview.
