# Research Skills OpenAI Plugin Roadmap

Status: Experimental/Preview  
Planning baseline: 2026-07-13
Current scope: 49 skills, including the four-skill Research Polisher series

Completion status: Phase 0 through Phase 6 complete on 2026-07-12. Phase 7
and Phase 8 are in progress with their remaining live/external gates explicit.

Next priority: finish the externally witnessed Preview evidence path, complete
the current-version runtime/release gates in Phase 7, and run the two Deep
Research return cycles in Phase 8. Research Polisher is the
owner-approved Phase 9 feature immediately after those gates; its source
implementation does not make the pending live evidence current or verified.

## Priority decision

Maintenance comes before feature expansion.

The current source has broad functional coverage: 49 skills, five workflow
state machines, 20 independently delegated reviewer roles, seven declared
public entry points (six implicit-active and Research Polisher explicit-only),
and 17 declared entry modes. The limiting factors remain operational
and runtime proof:

- The 49-skill, seven-declared-entry `0.7.0-preview.1` source passes the stricter Phase 9
  context limits at 6,086/6,200 description characters and 13,266/13,400 for
  the largest descriptions-plus-orchestrator proxy; ChatGPT web remains
  unverified.
- All 17 current entry modes pass deterministic replay, bypass, and stale/
  lineage guards. All current-version live happy/control paths remain pending.
- Deterministic replay is strong, but all earlier workflow and retrieval
  observations are historical release-mismatch snapshots; none closes a
  current-version Preview gate.
- Search has historical targeted smoke snapshots, not durable current-release
  receipts; a complete Deep Research handoff-return-resume cycle has not yet
  been demonstrated.
- The candidate has a current machine-readable release ledger, bundled MIT
  license, and resolved 49-skill provenance. Commit/CI binding, marketplace
  upgrade/reinstall, rollback, branch-protection evidence, and real externally
  witnessed Preview receipts remain pending.
- The anonymous Phase 8 corpus contains 20 cases and passes deterministic
  quality/isolation gates. Six reviewer and four retrieval observations remain
  historical `0.6.0-preview.1` snapshots; current `0.7.0-preview.1` observed
  and verified counts are zero. Two complete Deep Research cycles remain
  pending.

The owner has approved Research Polisher as the sole seventh public entry and
next feature priority. It is discoverable and explicitly callable, but implicit
routing remains disabled until Phase 8 is complete. Until then, do not mark
Phase 9 complete, claim current-version runtime discovery, add an eighth public entry, restore a
standalone PubMed skill, introduce another research-domain workflow, or add an
Apps SDK/MCP companion.

### Evidence acceptance levels

- `capture_only`: redacted App Server or task export. It is raw material only
  and never advances a gate.
- `preview_attested`: the acceptance target for this personal
  Experimental/Preview release. It requires a source-bound GitHub prerelease,
  Release-asset IDs and digests, a successful Actions witness, and a fresh
  independent executable verifier that re-queries those external objects.
  This level must never be described as OpenAI/provider verified.
- `provider_verified`: a stricter future level requiring a registered,
  authenticated provider adapter. A provider-labelled local file or boolean is
  insufficient.

The offline bundle validator proves only structure, source identity, and byte
integrity. Gate eligibility is produced only by the external verifier. Raw
evidence stays in immutable GitHub Release assets rather than `main`, avoiding
a source-commit/evidence-commit loop.

The operational A/B release sequence, ten Phase 7 live slots, twelve Phase 8
live slots, R -> E -> V -> I evidence DAG, and acceptance matrix are maintained
in [PHASE7-8-RUNBOOK.md](PHASE7-8-RUNBOOK.md). That runbook does not change a
gate: machine-readable reports and live verifier results remain authoritative.

## Objective

Turn the current personal development plugin into a context-efficient, auditable research workflow plugin for ChatGPT and Codex. The plugin should provide complete orchestration, explicit task distribution, independent evaluation and revision loops, source-grounded retrieval, and human-review delivery without depending on platform-specific private tool syntax.

## Current baseline

- Five workflow entry points: idea, proposal, article, perspective, and Research
  Polisher.
- Twenty reviewer-class skills require fresh independent subagents.
- Research Polisher compares three effort tiers through three mutually blind
  strategy-review instances, non-evaluative assembly, and a fresh methodology/
  publishability review.
- `research-opportunity-mapper` routes broad evidence retrieval and Deep Research handoffs.
- `academic-deep-search` handles narrow questions answerable through 2-5 papers.
- Plugin discovery, manifest, registry, and GitHub marketplace installation
  infrastructure are implemented; current-version `0.7.0-preview.1` install and
  discovery evidence remains pending.
- Static and fixture-driven validation covers recursive references, orphan
  resources, context budgets, workflow edges, reviewer isolation, revision/
  package lineage, plugin structure, and all five end-to-end workflows.

## Phase 0 — Reference and registry closure

Status: Complete (2026-07-12)

This completed phase records the 45-skill, six-entry baseline. Its measurements
and routing receipts remain historical and do not establish the 49-skill,
seven-entry `0.7.0-preview.1` source as discovered or runtime-verified.

Deliverables:

- Recursively validate Markdown links, backtick resource paths, templates, scripts, and cross-skill references.
- Replace ambiguous cross-skill `references/foo.md` paths with fully qualified skill-relative references.
- Remove orphaned resources or name them directly from `SKILL.md` with explicit load/run conditions.
- Add tables of contents to references over 100 lines and split references over 300 lines.
- Extend `workflow-registry.yaml` with auditable workflow edges: source, destination, dispatch mode, trigger, input/output contract, and failure route.

Acceptance:

- Missing, ambiguous, and orphaned resource references: 0.
- Every orchestrator-to-reviewer edge is marked delegated.
- Registry, manifest, and discovered skill set match exactly.

## Phase 1 — Context reduction

Status: Complete (2026-07-12)

Deliverables:

- Convert orchestrators into compact routing kernels containing only phase order, state transitions, delegation rules, stop conditions, and final handoff rules.
- Move long schemas, examples, rubrics, and delegate templates to conditionally loaded references.
- Shorten descriptions and front-load public trigger terms.
- Return concise phase summaries and artifact pointers to orchestrators instead of raw intermediate logs.

Budgets:

- Target per `SKILL.md`: at most 180 lines and 8,000 characters.
- Hard limit per `SKILL.md`: 250 lines and 12,000 characters.
- Skill plus default mandatory references: preferably below 16,000 characters.
- Initial skill-list estimate: no more than 8,000 characters.
- Primary workflow stress baseline: 32K ChatGPT context; degraded/handoff smoke test: 16K.

Acceptance:

- No skill exceeds the hard limits.
- Every long reference has a table of contents or is split.
- The main orchestrator retains at least half of the working context for user artifacts, state, and reasoning in the 32K test profile.

## Phase 2 — Native Search and Deep Research

Status: Complete (2026-07-12)

Deliverables:

- Make `research-opportunity-mapper` the single owner of broad retrieval policy.
- Use built-in Search for quick, current, exact, or targeted retrieval.
- Use Deep Research for multi-stage or multi-source synthesis.
- Emit a self-contained continuation package and pause when Deep Research is required but inactive or unknown.
- Keep local scripts only as explicit reproducibility/batch fallbacks; remove default script-preference language.
- Keep `academic-deep-search` limited to specific questions for which 2-5 carefully read papers are sufficient.

Acceptance:

- One targeted Search smoke snapshot records opened primary/authoritative
  sources. It is a self-attested routing/source-verification observation, not a
  durable Phase 8 live receipt.
- One inactive Deep Research scenario returns `deep_research_handoff_required` and a complete resume package.
- No orchestrator prefers local scripts over native Search or Deep Research.
- No deleted or external retrieval skill remains as a dangling dependency.

## Phase 3 — Workflow state-machine closure

Status: Complete (2026-07-12)

Deliverables:

- Normalize entry-mode gates for Standard, Fast-Track, section-specific, blueprint-only, and submission-only paths.
- Enforce `changed substantive artifact -> new version -> fresh evaluator` across all workflows.
- Preserve panel dissent and fatal findings through final artifact indexes and packages.
- Define explicit stopped, blocked, pending-review, and human-signoff states.
- Permit phase-level delegation for context-heavy builders while preventing concurrent writes to the same source artifact.

Acceptance:

- No entry path bypasses a required independent gate before evaluation, panel review, or packaging.
- No changed final prose reaches a ready status without a fresh evaluator report.
- Fatal findings prevent `accept`, `promoted`, and ready-for-signoff states.
- Reviewer unavailability produces `independent_review_pending`, never inline fallback.

## Phase 4 — Scenario evals and continuous validation

Status: Complete (2026-07-12)

Implement fixture-driven tests for:

1. Idea: generation -> evaluator -> revision -> fresh evaluator -> adversarial panel -> portfolio.
2. Proposal: draft -> evaluator -> revision -> fresh evaluator -> optional SAP evaluator -> panel -> package.
3. Article: methods audit -> draft -> claim audit -> evaluator -> revision -> fresh claim audit/evaluator -> panel -> compositor.
4. Perspective: draft -> evaluator -> revision -> fresh evaluator -> panel patch -> fresh evaluator -> compositor.

Also test unique reviewer instance IDs, reviewer write scopes, prior-score blindness, fatal-flaw blocking, visible dissent, Search routing, Deep Research continuation, and 16K/32K context behavior.

Acceptance:

- All four workflow fixtures complete the independent evaluation/revision loop.
- Every panel role has a distinct reviewer instance ID.
- Reviewer writes remain limited to review/verification report locations.
- Runtime results agree with registry edges and artifact lineage.

Verification:

- Four deterministic workflow fixtures pass the generation/draft, independent evaluation, revision, fresh evaluation, panel, and human-review delivery paths.
- Thirty-nine adversarial mutations are rejected, including stale or missing review inputs, reviewer/writer reuse, understated panel decisions, missing revision plans/deltas, stale SAP binding, incomplete package lineage, and verifier identity mismatches.
- Five finding routes are verified; live output snapshots are raw-hash-bound and report contract-corrected stopped/blocked/pending outcomes separately from their original self-attested states.
- Historical runtime receipts lack captured manifest/registry/schema identity,
  are classified `historical_only_incomplete_identity`, and can never satisfy a
  current-tree gate; 12 identity mutations verify this boundary.
- The canonical evidence is `reports/phase4-scenario-results.json`.

## Phase 5 — Preview release and GitHub updates

Status: Complete (2026-07-12)

Deliverables:

- Use plugin-level SemVer and bump the version for every installable behavior change.
- Keep `main` as the rolling Preview channel while the plugin is experimental.
- Add CI for audits, context budgets, plugin validation, and fixture tests.
- Verify marketplace upgrade/reinstall from GitHub loads the new version in a new task.
- Add a tag/SHA-pinned stable channel only after runtime acceptance is consistently green.

Acceptance:

- Version N installs, GitHub updates to N+1, marketplace refresh/reinstall succeeds, and the new cache version is discovered.
- The plugin remains labeled Preview/Experimental.
- Final workflow status remains human review/sign-off; no automatic external submission is introduced.

Verification:

- GitHub Actions run `29171766061` succeeded for implementation commit `8eb40187df7af45f562ccf39c5b4e3a10167e232`.
- The installed GitHub Marketplace plugin upgraded from `0.5.0-preview.1` to `0.5.0-preview.2`, then completed an explicit reinstall into the `.2` user cache.
- Fresh Codex task `019f5379-15ad-7241-948a-14a5ddc0cebc` discovered the `.2` catalog path, all six public entry skills, and no `pubmed` skill.
- The distribution remains Experimental/Preview on rolling `main`; the stable tag/SHA channel remains deferred.
- The canonical evidence is `reports/phase5-upgrade-smoke.md`.

## Phase 6 — Maintenance headroom and validator portability

Status: Complete (2026-07-12)

- Priority: P0
- Type: maintenance

Deliverables:

- Measure or tightly bound the effective discovery catalog and initial skill
  context in Codex. Keep ChatGPT web explicitly unverified and defer its
  installation, sharing, discovery, and runtime checks to Phase 12.
- Reduce catalog and orchestrator load while preserving the six public trigger
  boundaries and all 45 skill contracts.
- Remove current-version literals and fixed skill-count assumptions from test
  implementation. Historical receipts may retain their original versions.
- Separate immutable historical receipts from current-release evidence and
  determine compatibility from manifest, registry, schema, and normalized
  skill-tree digests.
- Make SemVer validation require a strictly increasing version for installable
  behavior changes and cover every installable behavior path.
- Add documentation consistency checks for README, Roadmap, manifest, registry,
  public entry count, Preview status, and submission boundary.
- Add copy-paste quickstarts for all six public entry skills, including minimum
  input, expected output, stop states, and resume instructions.
- Keep the README explicit about which surfaces are verified. Do not describe
  ChatGPT web as verified until a web receipt exists.

Acceptance:

- The effective Codex catalog/injection set is documented, including whether
  non-implicit skills contribute to initial context. No ChatGPT web behavior is
  inferred from Codex evidence.
- The conservative all-skill description proxy is at most 6,400 characters.
- Every conservative all-skill-descriptions-plus-orchestrator proxy is at most
  14,000 characters; the existing 16K degraded-profile behavior still passes.
- All 45 skills, 58 edges, and 18 independent reviewers pass the full audit with
  zero errors and zero warnings.
- Validator implementation contains no literal for the current plugin version
  or current skill count; historical fixture and report data are exempt.
- A temporary next prerelease can regenerate and validate evidence without
  editing validator logic.
- A lower, equal, malformed, or local-cachebuster release version is rejected.
- README, Roadmap, manifest, registry, discovery, Preview labeling, and final
  human-signoff claims agree in CI.
- All six quickstarts pass a fresh-task routing smoke test without loading an
  unrelated public skill.

Verification:

- Codex catalog observation: six implicit entries and zero non-implicit roles
  in the initial catalog; ChatGPT web is explicitly unverified.
- Context proxies: 5,882/6,400 all-skill descriptions and 13,879/14,000 for
  the largest description-plus-orchestrator proxy.
- Six of six copy-paste quickstarts passed isolated fresh-subagent routing;
  each child read only the selected public entry and no unrelated entry.
- Strict SemVer transition tests reject equal, lower, malformed, and local
  cachebuster release versions; validators derive the release version and
  skill inventory rather than embedding current literals.
- Canonical evidence: `reports/phase6-context-measurement.md` and
  `../tests/openai_phase6/quickstart-routing-receipts.yaml`.

## Phase 7 — Entry-mode, runtime, and release hardening

Status: In Progress (2026-07-12)

- Priority: P0
- Type: maintenance and runtime proof

Deliverables:

- Add positive end-to-end replay for every declared workflow entry mode, not
  only the four primary modes.
- Add at least one bypass, stale-input, or invalid-lineage mutation per mode.
- Capture current-version fresh-task runs for all five primary workflows: one
  full happy path and one valid stop/block/pending control per workflow.
- Ingest those ten runs through a machine-readable receipt schema with
  exactly one `happy` and one `control` slot for each workflow. Pending slots
  remain explicit placeholders and never count as live evidence.
- Capture complete actor manifests, input and output digests, files read,
  files written, panel dissent, and final state from the runtime artifacts.
- Bind every accepted runtime receipt to the current plugin version, registry
  digest, immutable source commit, durable task/platform export, actor
  manifest, and artifact index. Keep raw evidence in immutable GitHub Release
  assets; validate asset IDs, external witness data, and SHA-256 digests rather
  than copying mutable evidence into the source commit.
- Pin CI validator dependencies and run the canonical plugin validator in CI,
  not only the repository-specific checks.
- Add a machine-readable release ledger recording version, commit, CI run,
  marketplace source revision, install result, cache path, and fresh-task
  discovery result.
- Test a GitHub upgrade, explicit reinstall, and rollback to a previous plugin
  artifact pinned by an immutable commit or test tag. Treat branch protection
  and required checks as a repository setting to verify, not a claim inferred
  from workflow files.
- Maintain the accepted-state CI path that downloads locator-bound evidence and
  candidate Releases, runs the production live release-evidence verifier, and
  feeds that in-process result to complete release/report validation. The
  ordinary path remains structural-only and cannot claim a repeated external
  re-query; a serialized boolean or locally authored verifier result is not a
  substitute.
- Run the accepted-state path as trusted default-branch code in a protected
  GitHub Environment. Keep the single-repository Administration(read),
  Actions(read), and Contents(read) credential in that environment only; never
  pass it to code checked out from a caller-selected source commit.
- Require the live verifier to re-resolve the tag to the frozen source commit,
  require the GitHub Release API to report the prerelease as immutable, and
  enumerate the dedicated Release-assets endpoint with pagination to
  exhaustion before completeness or uniqueness is accepted.
- Use two different immutable tags at the same frozen source: an evidence
  Release containing R/E/V/I before the first verifier run, followed by a
  candidate Release containing the derived ledger and three accepted receipt
  collections. Candidate files must remain outside the evidence bundle root.
- Bundle the applicable license with the installable plugin and maintain a
  zero-unknown provenance/license inventory for migrated or third-party content.

Acceptance:

- All 17 declared entry modes complete deterministic end-to-end replay.
- All 17 mode-specific invalid gate-bypass cases are rejected.
- Five of five current-version live happy paths reach their workflow-declared
  human handoff (`human_signoff_required` or
  `human_strategy_selection_required`); five of five controls stop at their
  expected valid state.
- A status label without durable bindings, or a receipt missing any
  required version/commit/export/manifest/index binding, is rejected and
  cannot advance the phase status.
- False-ready, automatic external submission, writer/reviewer identity overlap,
  reviewer out-of-scope writes, and hidden fatal findings are all zero.
- Artifact lineage, current-version digests, and preserved dissent are complete
  in 100% of runtime receipts.
- CI dependencies are version-pinned, and both the canonical plugin validator
  and repository validators pass.
- Upgrade, reinstall, and fresh-task discovery receipts are bound to the same
  N+1 release and source commit. The rollback receipt is separately bound to
  the previous N artifact and immutable source commit, with no cache mixing.
- The installable cache contains the declared license, and the provenance
  inventory has zero unresolved entries.
- `main` is protected by the required Preview CI check and cannot be presented
  as release-ready when that check is absent or failing.
- Phase status and pending gates are derived from the ten runtime receipts and
  release ledger. `complete_preview_attested` is the personal Preview
  acceptance state and is reachable only when all ten receipts and every
  release, CI, marketplace, install, discovery, rollback, and branch-protection
  gate pass the live GitHub-witnessed Preview adapter.
  `complete_provider_verified` is a separate stricter state and requires an
  authenticated provider adapter; it is not required to ship the personal
  Experimental/Preview build.
- Freeze A at 49 installed skills, seven explicit-callable entries, and six
  implicit prompt entries. After all A gates pass, publish B with only the
  allowlisted policy/version/registry delta that enables Research Polisher as
  the seventh implicit entry; rerun install, discovery, and routing evidence.
  Any other installable delta requires a full Phase 7-8 rerun.
- The committed accepted-state reports and ledger replay in CI against the
  downloaded immutable evidence. An accepted ledger must not make the ordinary
  no-callback validator fail merely because CI omitted its live-evidence path,
  and CI must not bypass the rest of the Preview release validator.
- The governance credential is visible only to a protected-environment job
  running trusted default-branch code; input-commit-controlled code never
  receives it.
- Both accepted Releases report `immutable: true` and their distinct tags still
  resolve to the ledger source commit. A fully paginated evidence-asset
  enumeration contains each indexed object exactly once with no duplicate name
  or ID, while candidate files remain physically outside the evidence bundle.

Verification to date:

- The `0.7.0-preview.1` deterministic suite passes 17/17 modes and rejects 17
  gate-bypass, 17 stale/lineage, and 55 evaluator/panel/strategy-reviewer
  receipt mutations with zero false-ready outcomes.
- The synthetic closed loop validates 17 generation/version receipts, three
  mutually isolated strategist receipts, 44 role-isolated panel receipts, 13 final packages
  created by each workflow's declared final skill, and four gate/finding/route/
  continuation control receipts. Durable validation enforces workflow-specific
  writers, complete panel roles, package input contracts, finalizer boundaries,
  and canonical POSIX repository-relative paths.
- CI dependencies are pinned. The candidate bundles the repository MIT license
  and resolves all 45 migrated plus four OpenAI-native skill origins with zero
  unresolved resources.
- `reports/release-ledger.json` records derived version/tree/source data and
  keeps every unobserved external receipt explicitly pending. An accepted
  Preview claim must bind an immutable GitHub prerelease, Actions run, Release
  asset index, raw export, independent verifier result, and exact source-tree
  identity. The integrity contract is
  `../tests/openai_phase7/release-evidence.schema.yaml`; the live verifier is a
  separate trust boundary.
- An accepted release commit must exist in local Git history and its committed
  plugin manifest, registry/schema, license, provenance, complete skill tree,
  marketplace source, and validation-contract tree must match the
  ledger identity. Mutable runtime evidence is separately digest-bound and
  excluded from that source-tree identity to avoid a capture/commit cycle.
  Fifty-six mutation
  self-tests reject commit mismatches, malformed identities, missing or altered
  evidence, missing provider trust, rollback/history/ancestry mismatches, and a
  nonexistent source commit. Install, reinstall, discovery, and rollback
  receipts also bind a provider-exported cache inventory: source commit,
  manifest, registry, complete skill tree, license, cache instance, and a
  recomputed content identity. Discovery must match one verified N+1 install;
  rollback must match the current install and one previous-release cache with
  distinct paths, instances, and content identities.
- The runtime schema now defines five workflows x two cases. All ten slots are
  explicitly `pending_live_evidence` with 0/10 verified; no historical slot is
  relabelled as current-version evidence.
- Runtime ingestion rejects targeted mutations, including label-only
  promotion, missing bindings, wrong-workflow writers, incomplete/peer-visible
  panels, invalid package inputs or creators, source edits by finalizers,
  malformed or self-relabelled controls, noncanonical paths, evaluator access
  to prior scores/reports, unknown or mismatched actor roles, and repository-
  authored exports with no platform trust adapter. The report derives 13
  pending completion gates; none is silently promoted from a status label or
  self-authored evidence file.
- Repository files and hashes prove integrity, not external origin. The App
  Server capture helper, ten-slot runtime runner, live Preview verifier,
  run-bound workflow summary, eight-record release-ledger runner,
  accepted-history downloader, and protected accepted-state workflow now
  exist. The live verifier requires `immutable: true`, resolves lightweight or
  annotated tags through the Git API, and paginates the dedicated Release-assets
  endpoint to exhaustion; its transport suite contains 46 guards. The protected
  workflow uses distinct evidence/candidate Releases, an isolated trusted
  workspace, and two production callback passes. Its accepted summary binds
  the exact candidate ledger bytes to both the candidate Release inventory and
  the independent runner result, validates accepted history separately, and
  enforces global uniqueness across the current eight release/distribution,
  ten Phase 7, and twelve Phase 8 evidence chains. Exact `refs/tags/...`
  resolution handles lightweight and annotated tags without branch/tag
  ambiguity. All three validation workspaces receive a final immutability or
  allowlist proof before the non-overwriting summary is uploaded as the final
  step. The accepted-summary suite contains 41 guards; workflow invariants
  contain 26 mutation guards, and a real first-pass-summary-to-ZIP-to-callback
  round trip passes locally. The current first-pass
  workflow intentionally receives no governance secret. The protected GitHub
  Environment and credential are not yet configured or exercised, and no real
  current-release bundle has completed either pass; all live gates remain
  pending. No authenticated provider adapter exists.
- Synthetic gate-logic self-tests prove both `complete_preview_attested` and
  `complete_provider_verified` are structurally reachable; they are explicitly
  excluded from runtime evidence counts.
- Repository contract/report identities use CRLF-to-LF-normalized SHA-256 so
  Windows and Ubuntu checkouts produce the same Phase 7 report. Runtime task,
  actor, artifact, and file-access bindings retain raw-byte SHA-256.
- Still required: configure and approve the protected environment/credential;
  run five live happy paths and five live controls; freeze the release commit
  and successful CI binding; verify the canonical-validator CI entry; publish
  and verify the two immutable Releases; capture current marketplace upgrade,
  reinstall, fresh discovery, immutable rollback, and branch protection. Each
  Preview verification needs a real App Server capture, immutable Release
  assets, and live GitHub re-query; changing a status string or authoring a
  matching local file cannot close a completion gate.
- Canonical deterministic evidence: `reports/phase7-mode-results.json`.

## Phase 8 — Field corpus and native research closed loop

Status: In Progress (2026-07-12)

- Priority: P1
- Type: maintenance and quality evaluation

Deliverables:

- Build a reusable anonymized regression corpus from real or realistic research
  workflow failures. Never commit identifying source material.
- For each workflow, include happy, fixable, fatal-or-pending, and
  revision-no-gain cases with expected route, state, required outputs,
  forbidden outputs, and critical findings.
- Repeat three risk-stratified corpus cases with fresh evaluator instances by
  default. Expand to four or five only when the first three expose a route/state
  disagreement or a missed critical finding; do not exceed five repeated cases
  without an explicit owner decision.
- Add live Search cases for current, exact, and narrow academic questions.
- Demonstrate two complete Deep Research cycles: handoff, user-started Deep
  Research, provider-run completion, mapper-specific contract return, durable
  evidence-artifact binding, and workflow resume. Mapper return and resume
  must bind the same evidence-artifact IDs, repository-relative paths, and
  SHA-256 digests. This phase tests the existing mapper return contract; Phase
  10 later generalizes it into a portable cross-state continuation package.
- Timestamp live research receipts and bind them to plugin version, task ID,
  opened sources, and artifact digests.
- Treat repository-authored files and hashes as integrity bindings, not as a
  trust anchor. Preview promotion requires the executable GitHub-witness
  verifier; provider promotion additionally requires an authenticated provider
  adapter.
- Bind accepted evidence to an immutable source commit plus current manifest,
  registry, and complete skill-tree identities. Reject future timestamps and
  evidence older than 90 days.
- For repeated reviewer runs, dispatch a source-only sanitized blind bundle
  containing the frozen source and declared reviewer resources only. Its
  content and lineage must exclude all prior reviewer/evaluator outputs,
  scores, decisions, expected findings, and review references. Preserve the
  exact declared read closure, delegated-thread identity, files written, and
  frozen-input before/after digests. Read and scan the actual bound source
  bytes and embedded metadata rather than trusting blind-bundle metadata alone.
  The embedded block uses an exact field allowlist, and every `based_on` item
  must identify a source/data/context/blueprint/analysis/evidence-class artifact
  rather than a revision, review, expected-result, or oracle artifact.
- Use opaque reviewer-visible source, case, run, bundle, prompt, thread, and
  instance identifiers. Reject tokenized outcome labels in those identifiers
  and in non-skill resource paths; do not apply this check to declared reviewer
  skill resources, whose legitimate filenames may describe readiness or flaws.

Acceptance:

- The corpus contains at least 20 workflow cases: four per workflow and all four
  outcome classes above. It also contains exactly defined minimum retrieval
  coverage: three Search cases, two completed Deep Research cycles, and one
  inactive-Deep-Research control.
- Critical fatal or blocking findings are detected in 100% of labeled cases;
  recall for other labeled major findings is at least 90%.
- False-ready rate is zero; lineage, reviewer isolation, source-edit boundary,
  and dissent preservation compliance are each 100%.
- The default repeat set is three cases and the maximum automatic repeat set is
  five. Contract-level final state agrees across the fresh runs for every
  repeated case; any remaining disagreement is visible and blocks completion
  rather than triggering additional unbounded runs.
- Each live Search and completed Deep Research case opens only
  identity-verified primary or authoritative sources, with 100% traceability
  from material claims to every opened source. Each of the three live Search
  cases opens at least two such sources.
- Both Deep Research cases return through the declared contract and resume the
  unique pending edge. When Deep Research is inactive, the workflow pauses in
  100% of cases and never simulates it inline.
- Live retrieval evidence older than 90 days is marked stale and cannot satisfy
  the current-release gate; timestamps beyond a five-minute clock-skew allowance
  are rejected.
- A repository-authored export, status label, or recomputed digest can never
  satisfy a live gate without a successful executable external verifier.
  Synthetic reachability tests use an internal temporary capability and always
  report `counts_as_runtime_evidence: false`.
- Every accepted reviewer dispatch is oracle-free and uses a validated
  source-only sanitized blind bundle. Reads are limited to that bundle, its
  frozen source, and declared reviewer-skill resources. Platform access
  evidence binds read and write sets plus identical input before/after digests.
  The actual source content and lineage contain no review instruction, revision
  brief or plan, expected-result oracle, prior audit/evaluator/panel conclusion,
  score, decision, or review artifact. Embedded metadata is allowlisted and
  source lineage uses only approved source-artifact kinds.
- Reviewer-visible identifiers and non-skill paths contain no outcome oracle
  token. Path, blind-bundle-ID, prompt-ID, and case/run-ID mutations are all
  rejected without treating normal reviewer-skill resource names as leakage.
- Each completed Deep Research receipt has unique task, session, run,
  provider-run-completed receipt, mapper-return receipt, resume transaction,
  and pending-edge identities. The provider completion record binds its run
  ID, success status, timestamp, and raw-output digest. Its handoff, user-start,
  provider-complete, mapper-return, and resume events are strictly monotonic.
  Mapper return and resume bind the same real evidence-artifact path/digest set.
- Phase status is three-way: `complete_preview_attested` when all reviewer and
  retrieval slots pass the live GitHub-witnessed Preview adapter;
  `complete_provider_verified` only when the same slots also pass an
  authenticated provider adapter; otherwise it remains in progress. The first
  state is sufficient for this personal Experimental/Preview release.

Verification to date:

- The current corpus contains 20 anonymous synthetic cases: four outcome
  classes for each of five workflows. False-ready is zero; fatal/blocking and
  major-finding recall, lineage, isolation, edit-boundary, and dissent checks
  are each 100%.
- The bounded repeat set remains exactly three cases (maximum automatic five).
  Its sources and repository-assigned identifiers are now opaque A01-A03
  values. Six earlier snapshots with outcome-bearing reviewer-visible names are
  preserved under `historical_oracle_exposed_runs` with their real instance
  IDs, original paths, and original digests; they are excluded from evidence
  rather than relabelled as neutral executions. Six fresh replacements now use
  real opaque instance IDs. They remain bound to `0.6.0-preview.1`, are
  classified `historical_release_mismatch`, and provide zero current observed
  or verified receipts for `0.7.0-preview.1`. The
  A03 replacement exposed two substantive wording/decision-rule defects; each
  source update received new isolated reviews, and the final v005 pair agrees
  on pre-panel eligibility while preserving the stable-setting and annual-
  reassessment dissent.
- Three built-in Search snapshots (current, exact, narrow academic) internally
  bind at least two sources and material claims; the inactive Deep Research
  snapshot binds a continuation package. They remain bound to
  `0.6.0-preview.1`, lack durable provenance, and count as neither observed nor
  verified current-release receipts.
- Repository file/digest bindings are now explicitly insufficient for
  promotion. `../tests/openai_phase8/provider-verifier-registry.yaml` declares
  the Preview verifier contract but no authenticated provider adapter; no real
  current-release Preview asset bundle has passed it. Synthetic reachability
  is restricted to an internal temporary capability and reported as
  non-evidence.
- The real-only Phase 8 external runner now requires twelve isolated
  mini-bundles, performs twelve live v3 re-queries, materializes only indexed
  bytes into a fresh workspace, and replays the six blind-review plus 3/2/1
  retrieval semantics with source and temporary-workspace immutability checks.
  Its 27 contract guards pass locally; no live bundle has yet supplied
  those twelve slots.
- Accepted receipts additionally require the current immutable source commit,
  manifest, registry, and skill-tree identity. Reviewer evidence uses a
  source-only sanitized blind bundle, reviewer-resource/input allowlist,
  delegated-thread creation identity, write-set binding, and frozen-input
  before/after digests. Prior reviewer/evaluator outputs, scores, decisions,
  and review lineage are rejected both in the bundle and in the actual source
  bytes. Five direct source-poisoning negatives separately reject a generic
  review instruction, a revision brief/plan, an expected-result oracle, a
  review artifact in `based_on`, and an undeclared expected-result metadata
  field. Four reviewer-visible-identifier mutations separately reject an
  outcome-bearing source path, blind-bundle ID, prompt ID, and case/run ID.
  Future timestamps are rejected and the 90-day window applies to both reviewer
  and retrieval evidence.
- The Deep Research contract now requires provider session/run identity, an
  explicit user-start event, provider-run-completed receipt, actual evidence
  artifact path/digest bindings, mapper-return receipt, resume transaction,
  five-stage event ordering, and cross-receipt uniqueness. Its sources must be
  primary or authoritative and identity-verified, with complete material-claim
  traceability. Forty-one retrieval and six reviewer binding guards still
  pass, together with seven Deep Research semantic negative guards; their
  synthetic positive baselines use the explicit non-counting override.
- Still required for Preview acceptance: capture externally witnessed
  prompt/output/instance/access evidence for the six review runs; capture live
  tool/citation evidence for all three Search runs and the inactive control;
  and complete two user-started Deep Research handoff-return-resume cycles.
  A provider-authenticated adapter remains a stricter deferred enhancement.
  Phase 8 therefore remains in progress and cannot satisfy the feature-
  expansion gate.
- Canonical evidence: `reports/phase8-corpus-results.json`,
  `../tests/openai_phase8/live-repeat-receipts.yaml`, and
  `../tests/openai_phase8/retrieval-receipts.yaml`; provider trust policy is
  `../tests/openai_phase8/provider-verifier-registry.yaml`.

## Phase 9 — Research Polisher: cross-domain impact strategy

- Priority: P1
- Type: owner-approved public workflow expansion
- Status: In Progress (2026-07-13); live release evidence remains gated on Phases 7–8

Deliverables:

- Add `research-polisher-orchestrator` as the seventh public entry for completed
  or substantially completed research. Its trigger excludes copyediting,
  language polishing, ordinary drafting, new-idea generation, and general
  literature-search requests.
- Add `research-polisher-strategy-reviewer`,
  `research-polisher-plan-assembler`, and
  `research-polisher-methodology-publishability-reviewer` as private workflow
  roles. Both reviewer-class skills use fresh delegated subagents; the
  assembler does not score, rank, choose, or invent strategies.
- Freeze a `research_polisher_dossier` binding source IDs, versions, paths,
  digests, research design, methods, existing data/results, current claims and
  story, intended audience/outlet, and resource/work ceilings.
- Dispatch three mutually blind instances of the strategy reviewer for
  `scientific_significance`, `practical_value`, and
  `dissemination_editorial`. Every instance returns all three effort tiers or
  an explicit `no_defensible_option`.
- Enforce `reposition_only` as no new data, experiment, validation, or analysis;
  `small_extension` as one bounded, certain or well-supported high-feasibility
  work package; and `moderate_extension` as one bounded, high-feasibility
  analysis, validation, mechanism, or translation module that is not a new
  study or core redesign.
- Assemble the sealed 3-by-3 reports into an anonymous, versioned
  `research_polisher_candidate_portfolio`, preserving provenance, conflicts,
  dissent, and `no_defensible_option` cells without creating false consensus.
- Send the frozen anonymous portfolio and necessary source facts to a fresh
  methodology/publishability reviewer that cannot read strategist identities,
  raw reports, prior scores, or sealed provenance. It returns `retain`,
  `revise`, `reject`, or `not_assessable` per option and never a publication
  probability or automatic winner.
- Allow at most one targeted strategy revision and one fresh re-evaluation.
  Produce an unweighted Pareto view and stop at
  `human_strategy_selection_required`; selected extension options remain
  `additional_work_required` until the work exists.
- Use `research-opportunity-mapper` for broad positioning, and
  `academic-deep-search` only for a narrow question answerable from 2–5 papers.
  Route methodology/statistics or medical-journal review only as conditional
  specialist checks. Until Phase 11 supplies a source-verified target adapter,
  specific journal or section fit remains `target_requirements_unverified`.
- Emit self-contained continuation briefs in Phase 9. Portable import and
  single-edge cross-task resume remain Phase 10 work.

Acceptance:

- The maintained source contains exactly 49 registered skills, five workflow
  state machines, 20 independent reviewer-class skills, seven declared public
  entries, and 17 entry modes. Six entries are implicit-active; Research
  Polisher remains explicit-only until the Phase 7-8 external gate passes.
- The all-description proxy is at most 6,200 characters; every
  all-descriptions-plus-orchestrator proxy is at most 13,400 characters.
- Each complete case has three distinct strategist instance IDs, a complete
  3-by-3 matrix, sealed raw reports, an anonymous portfolio, and a final
  reviewer instance distinct from every strategist and artifact writer.
- `reposition_only` has empty `added_work_items`, produces no new result or
  source version, and traces every proposed claim to frozen evidence.
- Every extension records assets, dependencies, feasibility basis, risks, and
  stop conditions; unsupported feasibility and out-of-tier work are rejected.
- The assembler preserves all dissent and provenance, performs no source edit,
  and does not score, rank, select, or synthesize a new hybrid option.
- Every portfolio revision receives a new version and fresh evaluation. A
  source-level fatal finding, stale evaluation, missing reviewer, or changed
  input digest prevents `human_strategy_selection_required`.
- At least 12 component scenarios cover clinical/observational, basic science,
  computational/engineering, and qualitative or mixed-methods work, including
  tier-boundary, isolation, target-verification, and false-ready negatives.
- The Phase 7 contract contains ten current-version runtime slots and the Phase
  8 corpus contains at least 20 cases. Historical 0.5/0.6 receipts do not count
  as `0.7.0-preview.1` marketplace, discovery, workflow, or rollback evidence.

Verification to date:

- Source, registry, manifest, OpenAI-native provenance, and plugin validation
  pass for 49 skills, 20 independent reviewers, seven declared entries (six
  implicit-active and Research Polisher explicit-only), five
  workflows, 67 edges, and 17 modes.
- Context proxies pass at 6,086/6,200 descriptions and 13,266/13,400 maximum
  descriptions-plus-orchestrator load.
- Phase 4 passes five workflows and 63 negative guards, including 24 dedicated
  Research Polisher matrix, tier, isolation, assembler, target, and stale-
  evaluation guards.
- Phase 7 passes 17/17 deterministic modes plus seven Research Polisher routing
  boundaries; six forced false-takeover mutations are rejected. Phase 8 passes
  20/20 synthetic cases, including one case in each required Research Polisher
  domain, with zero false-ready and 100% lineage, isolation, edit-boundary, and
  dissent compliance.
- An explicitly delegated fresh-child probe followed Research Polisher and stopped
  at `clarification_stop` because no frozen source paths/digests were supplied;
  it read only the public orchestrator and modified no file. This self-attested
  probe is not marketplace or full-workflow evidence.
- Still required: current-version marketplace install/fresh-task discovery,
  seven-entry routing receipts, one durable Polisher happy path, one durable
  reviewer-unavailable control, and the remaining Phase 7/8 external gates.

## Phase 10 — Resume packages and workspace doctor

- Priority: P2
- Type: bounded workflow infrastructure expansion
- Status: Gated on Phases 7–9

Deliverables:

- Define one portable continuation-package schema for
  `independent_review_pending`, `deep_research_handoff_required`, and
  `context_handoff_required`.
- Let each orchestrator import a package in a fresh ChatGPT or Codex task,
  verify plugin/schema compatibility and artifact digests, and resume exactly
  one pending edge without replaying completed work.
- Add a read-only workspace doctor that applies runtime invariants to real user
  workspaces and reports stale evaluations, digest mismatches, dangling
  lineage, hidden dissent, and reviewer write-scope violations.
- Support both path-based Codex packages and uploaded portable packages that do
  not assume the original local path exists.

Acceptance:

- Fifteen resume fixtures pass: five workflows multiplied by the three pause
  types.
- Every valid package resumes exactly one expected pending edge without
  duplicate artifact writes, reviewer reuse, or premature promotion.
- Schema, plugin-version, or digest incompatibility returns `migration_required`
  or `blocked`; it never silently continues.
- The workspace doctor has zero false positives on clean fixtures and rejects
  every existing Phase 4 lineage, stale-review, dissent, and write-scope
  mutation.
- A fresh task can resume one real Codex path package and one uploaded portable
  package using only the package contents and declared source artifacts.
- Public entry count does not increase beyond the Phase 9 baseline, and the
  stricter Phase 9 context budgets remain green.

## Phase 11 — Source-verified target requirements

- Priority: P2
- Type: bounded feature expansion
- Status: Gated on Phase 10 and demonstrated user demand

Deliverables:

- Add one shared target-requirements contract for journal article types, funder
  calls, and Perspective/Viewpoint outlets.
- Extract requirements from user-supplied documents or native Search at run
  time; do not ship a fixed catalog of journal or funder rules.
- Record field-level source URL or document pointer, `checked_at`, verification
  status, conflicts, and unknown values.
- Route the verified adapter into the article, proposal, perspective, and
  Research Polisher workflows as a conditional component, not a new implicit
  public entry.
- Keep approval, consent, disclosure, and submission-form checks limited to the
  final target-specific package stage.

Acceptance:

- At least 12 frozen adapter fixtures pass: four journal, four funder, and four
  outlet cases.
- Every populated requirement field has a source and timestamp; missing facts
  remain `unknown`, and conflicting requirements remain visible.
- Unverified or stale critical fields cap package status and cannot be converted
  into invented defaults.
- All four consuming workflows bind the identical adapter ID, version, and
  digest through their final artifact indexes.
- Existing audit, runtime, isolation, and context-headroom gates remain green;
  no new public skill is added.

## Phase 12 — Reference integrity, integrations, and release decision

- Priority: P3
- Type: conditional expansion and release governance
- Status: Deferred until field evidence identifies a need

Candidate work, in order:

1. Add a private canonical reference-integrity ledger for DOI, PMID, URL,
   preprint-to-version mapping, deduplication, and metadata conflicts.
2. Evaluate a read-only Apps SDK/MCP companion only when an authenticated data
   source or programmatic handoff has a documented use case that skills, file
   uploads, native Search, and Deep Research cannot satisfy.
3. Evaluate DOCX/PDF delivery through available document runtimes only after
   users demonstrate that Markdown packages are insufficient.
4. Consider a tag/SHA-pinned stable channel after at least three consecutive
   Preview versions pass current runtime, corpus, upgrade, and rollback gates.
5. Consider ChatGPT plugin-directory submission only after web installation,
   sharing permission, workspace-policy, and fresh-task discovery are verified.

Acceptance before a stable or public claim:

- Three consecutive Preview versions pass all current CI and runtime gates.
- A clean profile can install the pinned release, discover all intended public
  entries, complete a representative workflow, upgrade, and roll back.
- ChatGPT web and Codex verification are reported separately; an unavailable or
  entitlement-blocked surface is never counted as passing.
- There are no open P0/P1 defects in the anonymized regression corpus.
- The release has a changelog, machine-readable ledger entry, immutable source
  tag/SHA, documented compatibility range, and human-reviewed rollback notes.
- The plugin remains personal Experimental/Preview until the owner explicitly
  approves a stable-channel or public-directory transition.

## Explicitly deferred scope

- A systematic-review or meta-analysis workflow.
- An eighth public router or additional implicit entry points.
- A restored standalone PubMed skill or a fixed journal/funder catalog.
- Automatic external submission or automatic human-signoff decisions.
- Apps SDK/MCP work without a verified authenticated-data requirement.
