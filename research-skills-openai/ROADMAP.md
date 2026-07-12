# Research Skills OpenAI Plugin Roadmap

Status: Experimental/Preview  
Planning baseline: 2026-07-12  
Current scope: 45 skills after removal of the standalone OpenAI `pubmed` skill

Completion status: Phase 0 through Phase 6 complete on 2026-07-12. Phase 7
and Phase 8 are in progress with their remaining live/external gates explicit.

Next priority: implement authenticated platform/external-evidence adapters,
finish the current-version runtime/release gates in Phase 7, and complete the
two Deep Research return cycles in Phase 8 before adding new public skills. The
temporary feature freeze remains in effect until both phases pass.

## Priority decision

Maintenance comes before feature expansion.

The current plugin has broad functional coverage: 45 skills, four workflow
state machines, 58 registered edges, 18 independently delegated reviewer
roles, and six public entry points. The limiting factors are operational and
runtime proof rather than missing workflow roles:

- The conservative all-skill description proxy is now 5,882 of 6,400
  characters; the largest all-descriptions-plus-orchestrator proxy is 13,879
  of 14,000. The current Codex task exposed only the six implicit entries in
  its initial catalog; ChatGPT web remains unverified.
- All 16 declared entry modes now have positive deterministic replays and
  mode-specific bypass plus stale/lineage negatives. Current-version live
  happy/control paths remain pending.
- Deterministic replay is strong, but the four live receipts are historical,
  self-attested snapshots; none reached a contract-validated human-signoff gate.
- Search has a self-attested targeted smoke snapshot, not a durable live
  receipt; a complete Deep Research handoff-return-resume cycle has not yet
  been demonstrated.
- The current candidate has a machine-readable release ledger, bundled MIT
  license, and resolved provenance inventory. Commit/CI binding, marketplace
  upgrade/reinstall, rollback, branch-protection evidence, and an authenticated
  external-evidence adapter remain pending.
- The anonymous Phase 8 corpus contains 16 cases. Six delegated reviewer
  responses, three Search runs, and one inactive-Deep-Research control were
  observed in this task, but only self-attested structured snapshots could be
  committed; they are not verified live gate passes. Two complete Deep
  Research handoff-return-resume receipts also remain pending.

Until Phase 8 is complete, do not add a seventh public entry point, restore a
standalone PubMed skill, introduce a new research domain workflow, or add an
Apps SDK/MCP companion. Improvements may add conditionally loaded resources,
fixtures, validators, and private workflow components when they remain within
the context budgets.

## Objective

Turn the current personal development plugin into a context-efficient, auditable research workflow plugin for ChatGPT and Codex. The plugin should provide complete orchestration, explicit task distribution, independent evaluation and revision loops, source-grounded retrieval, and human-review delivery without depending on platform-specific private tool syntax.

## Current baseline

- Four workflow entry points: idea, proposal, article, and perspective.
- Eighteen reviewer-class skills require fresh independent subagents.
- `research-opportunity-mapper` routes broad evidence retrieval and Deep Research handoffs.
- `academic-deep-search` handles narrow questions answerable through 2-5 papers.
- Plugin discovery, manifest, registry, and GitHub marketplace installation are implemented.
- Static and fixture-driven validation cover recursive references, orphan resources, context budgets, workflow edges, discovery, reviewer isolation, revision/package lineage, plugin structure, and four end-to-end workflow scenarios.

## Phase 0 — Reference and registry closure

Status: Complete (2026-07-12)

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
  installation, sharing, discovery, and runtime checks to Phase 11.
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
- Capture current-version fresh-task runs for all four primary workflows: one
  full happy path and one valid stop/block/pending control per workflow.
- Ingest those eight runs through a machine-readable receipt schema with
  exactly one `happy` and one `control` slot for each workflow. Pending slots
  remain explicit placeholders and never count as live evidence.
- Capture complete actor manifests, input and output digests, files read,
  files written, panel dissent, and final state from the runtime artifacts.
- Bind every verified runtime receipt to the current plugin version, registry
  digest, immutable source commit, durable task/platform export, actor
  manifest, and artifact index. Validate the referenced paths and SHA-256
  digests against the actual committed evidence files.
- Pin CI validator dependencies and run the canonical plugin validator in CI,
  not only the repository-specific checks.
- Add a machine-readable release ledger recording version, commit, CI run,
  marketplace source revision, install result, cache path, and fresh-task
  discovery result.
- Test a GitHub upgrade, explicit reinstall, and rollback to a previous plugin
  artifact pinned by an immutable commit or test tag. Treat branch protection
  and required checks as a repository setting to verify, not a claim inferred
  from workflow files.
- Bundle the applicable license with the installable plugin and maintain a
  zero-unknown provenance/license inventory for migrated or third-party content.

Acceptance:

- All 16 declared entry modes complete deterministic end-to-end replay.
- All 16 mode-specific invalid gate-bypass cases are rejected.
- Four of four current-version live happy paths reach
  `human_signoff_required`; four of four controls stop at their expected valid
  state.
- A `verified` label without durable bindings, or a receipt missing any
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
- Phase status and pending gates are derived from the eight runtime receipts
  and release ledger. `complete` is reachable only when all eight receipts and
  every release, CI, marketplace, install, discovery, rollback, and branch
  protection gate are verified through implemented authenticated platform and
  external-evidence adapters.

Verification to date:

- 16/16 declared modes and all 52 registry-derived entry-gate contracts pass
  deterministic end-to-end replay. The suite rejects 32 entry-gate mutations
  (one bypass plus one stale-input or invalid-lineage case per mode) and 50
  missing/stale evaluator or panel-receipt mutations, for 82/82 exact-error
  negative guards with zero false-ready outcomes.
- The synthetic closed loop now validates 16 generation/version receipts, 44
  role-isolated panel receipts across registry default tiers, 12 final packages
  created by each workflow's declared final skill, and four gate/finding/route/
  continuation control receipts. Durable validation enforces workflow-specific
  writers, complete panel roles, package input contracts, finalizer boundaries,
  and canonical POSIX repository-relative paths.
- CI dependencies are pinned. The installable plugin now bundles the repository
  MIT license; provenance resolves all 45 registered skill source mappings
  with zero unresolved resources.
- `reports/release-ledger.json` records derived version/tree/source data and
  keeps every unobserved external receipt explicitly pending. A verified
  external claim must now bind a repository-relative JSON/YAML envelope whose
  raw SHA-256 and exact observed payload match the ledger record; the envelope
  contract is `../tests/openai_phase7/release-evidence.schema.yaml`.
- A verified release commit must exist in local Git history and its committed
  plugin manifest, registry/schema, license, provenance, complete skill tree,
  marketplace source, and 48-file validation-contract tree must match the
  ledger identity. Mutable runtime evidence is separately digest-bound and
  excluded from that source-tree identity to avoid a capture/commit cycle.
  Twenty-seven mutation
  self-tests reject commit mismatches, malformed identities, missing or altered
  evidence, missing provider trust, rollback/history/ancestry mismatches, and a
  nonexistent source commit. Install, reinstall, discovery, and rollback
  receipts also bind a provider-exported cache inventory: source commit,
  manifest, registry, complete skill tree, license, cache instance, and a
  recomputed content identity. Discovery must match one verified N+1 install;
  rollback must match the current install and one previous-release cache with
  distinct paths, instances, and content identities.
- `../tests/openai_phase7/runtime-receipts.schema.yaml` and
  `../tests/openai_phase7/current-version-runtime-receipts.yaml` define the
  4-workflow x 2-case runtime evidence intake. All eight slots are currently
  `pending_live_evidence`; verified live receipt count remains 0/8.
- Runtime ingestion rejects 37 targeted mutations, including label-only
  promotion, missing bindings, wrong-workflow writers, incomplete/peer-visible
  panels, invalid package inputs or creators, source edits by finalizers,
  malformed or self-relabelled controls, noncanonical paths, evaluator access
  to prior scores/reports, unknown or mismatched actor roles, and repository-
  authored exports with no platform trust adapter. The report derives 13
  pending completion gates; none is silently promoted from a status label or
  self-authored evidence file.
- Repository files and hashes prove integrity, not provider origin. No
  authenticated Codex/ChatGPT capture adapter or GitHub/Codex external-evidence
  adapter is implemented, so both trust gates remain pending even if a local
  envelope is internally self-consistent.
- A synthetic gate-logic self-test proves the completion state is reachable
  when all eight runtime slots and all release-ledger gates are verified; this
  self-test is explicitly excluded from runtime evidence counts.
- Repository contract/report identities use CRLF-to-LF-normalized SHA-256 so
  Windows and Ubuntu checkouts produce the same Phase 7 report. Runtime task,
  actor, artifact, and file-access bindings retain raw-byte SHA-256.
- Still required: four live happy paths, four live controls, a release commit
  and successful CI binding, a verified canonical-validator CI entry, current
  marketplace upgrade/reinstall/fresh discovery, immutable rollback, and
  branch-protection verification. This also requires real authenticated capture
  adapters for platform and external-provider origin. Each external verification
  needs its durable evidence envelope; changing a status string or authoring a
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
  9 later generalizes it into a portable cross-state continuation package.
- Timestamp live research receipts and bind them to plugin version, task ID,
  opened sources, and artifact digests.
- Treat repository-authored files and hashes as integrity bindings, not as a
  provider trust anchor. Promotion requires an executable, platform/provider
  verifier adapter implemented in validator code; no such adapter is currently
  available.
- Bind verified evidence to an immutable source commit plus current manifest,
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

- The corpus contains at least 16 workflow cases: four per workflow and all four
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
  satisfy a live gate without a successful executable provider-verifier
  adapter. Ephemeral synthetic overrides are validator self-tests only and
  always report `counts_as_runtime_evidence: false`.
- Every verified reviewer dispatch is oracle-free and uses a validated
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

Verification to date:

- 16 anonymous synthetic cases cover four workflows and all four outcome
  classes. False-ready is zero; labeled fatal/blocking and other major finding
  recall are 100%; lineage, isolation, edit-boundary, and dissent checks are
  each 100%.
- The bounded repeat set remains exactly three cases (maximum automatic five).
  Its sources and repository-assigned identifiers are now opaque A01-A03
  values. Six earlier snapshots with outcome-bearing reviewer-visible names are
  preserved under `historical_oracle_exposed_runs` with their real instance
  IDs, original paths, and original digests; they are excluded from evidence
  rather than relabelled as neutral executions. Six fresh replacements now use
  real opaque instance IDs and restore the self-attested observation count;
  they still provide 0 verified live receipts without a platform adapter. The
  A03 replacement exposed two substantive wording/decision-rule defects; each
  source update received new isolated reviews, and the final v005 pair agrees
  on pre-panel eligibility while preserving the stable-setting and annual-
  reassessment dissent.
- Three built-in Search snapshots (current, exact, narrow academic) internally
  bind at least two sources, material claims, and current-version artifacts;
  the inactive Deep Research snapshot binds a continuation package. They lack
  durable Search/tool provenance and are not counted as verified live receipts.
- Repository file/digest bindings are now explicitly insufficient for
  promotion. `../tests/openai_phase8/provider-verifier-registry.yaml` contains
  zero real adapters, so all repository-authored evidence remains pending or
  observed-unverified. The only synthetic override is restricted to ephemeral
  validator temp roots and is reported as non-evidence.
- Verified receipts additionally require the current immutable source commit,
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
- Still required: implement and validate a real provider-verifier adapter;
  capture its authenticated prompt/output/instance/access evidence for the six
  review runs; capture provider-verified tool/citation evidence for all three
  Search runs and the inactive control; and complete two provider-verified,
  user-started Deep Research handoff-return-resume cycles. Phase 8 therefore
  remains in progress and cannot satisfy the feature-expansion gate.
- Canonical evidence: `reports/phase8-corpus-results.json`,
  `../tests/openai_phase8/live-repeat-receipts.yaml`, and
  `../tests/openai_phase8/retrieval-receipts.yaml`; provider trust policy is
  `../tests/openai_phase8/provider-verifier-registry.yaml`.

## Phase 9 — Resume packages and workspace doctor

- Priority: P2
- Type: first feature expansion
- Status: Gated on Phases 6–8

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

- Twelve resume fixtures pass: four workflows multiplied by the three pause
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
- Public entry count and Phase 6 context budgets do not increase.

## Phase 10 — Source-verified target requirements

- Priority: P2
- Type: bounded feature expansion
- Status: Gated on Phase 9 and demonstrated user demand

Deliverables:

- Add one shared target-requirements contract for journal article types, funder
  calls, and Perspective/Viewpoint outlets.
- Extract requirements from user-supplied documents or native Search at run
  time; do not ship a fixed catalog of journal or funder rules.
- Record field-level source URL or document pointer, `checked_at`, verification
  status, conflicts, and unknown values.
- Route the verified adapter into the existing article, proposal, and
  perspective workflows as a conditional component, not a new implicit public
  entry.
- Keep approval, consent, disclosure, and submission-form checks limited to the
  final target-specific package stage.

Acceptance:

- At least 12 frozen adapter fixtures pass: four journal, four funder, and four
  outlet cases.
- Every populated requirement field has a source and timestamp; missing facts
  remain `unknown`, and conflicting requirements remain visible.
- Unverified or stale critical fields cap package status and cannot be converted
  into invented defaults.
- All three consuming workflows bind the identical adapter ID, version, and
  digest through their final artifact indexes.
- Existing audit, runtime, isolation, and context-headroom gates remain green;
  no new public skill is added.

## Phase 11 — Reference integrity, integrations, and release decision

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
- A seventh public router or additional implicit entry points.
- A restored standalone PubMed skill or a fixed journal/funder catalog.
- Automatic external submission or automatic human-signoff decisions.
- Apps SDK/MCP work without a verified authenticated-data requirement.
