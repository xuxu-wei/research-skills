# Research Skills OpenAI Plugin Roadmap

Status: Personal Experimental/Preview
Planning baseline: 2026-07-15
Current version: `0.8.0-preview.1`
Current scope: 49 skills, including the four-skill Research Polisher series

## Product position

`research-skills-openai` is an owner-operated research workflow plugin for one
person's ChatGPT/Codex research work. The active roadmap optimizes reliable
personal use, reproducible artifacts, independent evaluation, and practical
installation/update behavior. It does not target production support, team or
public distribution, or automatic submission to an external platform.

The maintained architecture keeps generators, reviewers, and assemblers
separate. Substantive revisions receive fresh independent evaluation; source
artifacts remain immutable; lineage and dissent remain visible; and fatal or
unresolved blocking findings prevent promotion.

The active sequence is:

1. complete the minimal project README and Cover Letter maintenance checkpoint;
2. finish the current-version local install, update, and fresh-task discovery
   check;
3. complete the bounded owner-observed Phase 7 workflow runs;
4. complete the bounded Phase 8 Search and Deep Research runs; and
5. consider Phase 10 only after the current personal workflows are useful in
   real research work.

No additional entry skill is planned while these checks are incomplete.

## Current baseline

- 49 registered skills and 68 workflow edges.
- Five workflow entry points: Idea, Proposal, Article, Perspective, and Research
  Polisher.
- Twenty reviewer-class skills require fresh independent subagents.
- Seven declared entry skills are discoverable. Six permit implicit invocation;
  Research Polisher is permanently explicit-only under the current personal
  routing policy.
- Seventeen declared entry modes pass deterministic replay and their associated
  bypass, stale-input, and lineage guards.
- The 20-case anonymous corpus passes with false-ready zero and 100% compliance
  for fatal/blocking detection, lineage, reviewer isolation, source-edit
  boundaries, and dissent preservation.
- Context proxies remain at 6,086 descriptions and at or below the historical
  13,266 maximum; the current largest orchestrator proxy is 13,171.
- Plugin structure, registry generation, GitHub marketplace metadata, and local
  development installation support are implemented.
- A 2026-07-14 local audit confirmed that `xuxu-research-preview` is registered,
  `research-skills-openai` is enabled, and the coherent installed cache is
  `0.7.0-preview.2`. Installation is implemented; the working-tree
  `0.8.0-preview.1` still requires upgrade/reinstall and fresh-task discovery.
- ChatGPT web installation, sharing, discovery, and runtime behavior remain
  unverified and do not block the personal Codex profile.

## Personal acceptance states

- `deterministic_validated`: maintained static audits, registry/package checks,
  context limits, fixtures, and scenario tests pass.
- `owner_observed`: one real owner-run task is bound to the plugin version, task
  ID, frozen inputs, output artifacts, versions, SHA-256 digests, timestamps,
  reviewer instances where applicable, and explicit owner confirmation.
- `owner_observed_ready`: all required Phase 7 and Phase 8 personal checks have
  valid `owner_observed` records and no unresolved personal blocking finding.
- `in_progress_owner_observation`: deterministic validation passes but one or
  more required owner-observed checks are still missing or unresolved.

An owner-observed record supports only personal readiness. It must not be
described as provider, shared, public, or externally attested evidence.

## Historical completed baseline — Phases 0–6

Phases 0 through 6 were completed on 2026-07-12. Their original skill counts and
receipts are historical snapshots; later Research Polisher expansion increased
the maintained inventory to 49 skills and seven declared entries.

### Phase 0 — Reference and registry closure

Completed outcomes:

- Recursive Markdown, resource, template, script, and cross-skill references
  close without dangling dependencies.
- Every orchestrator-to-reviewer edge is delegated.
- Registry, manifest, and discovered skill inventory agree.

### Phase 1 — Context reduction

Completed outcomes:

- Oversized procedures were split or compressed without removing workflow
  gates.
- Public discovery descriptions and orchestrator context fit the maintained
  context budgets.
- Reviewer isolation, state transitions, and artifact schemas remained intact.

### Phase 2 — Native Search and Deep Research

Completed outcomes:

- Built-in Search is the default for quick, recent, exact, and narrow retrieval.
- Deep Research is used for multi-stage, multi-direction, or multi-source
  synthesis.
- Inactive Deep Research produces a self-contained continuation package and
  pauses at `deep_research_handoff_required`.
- `academic-deep-search` is limited to a sufficiently specific question
  answerable from two to five closely read papers.

### Phase 3 — Workflow state-machine closure

Completed outcomes:

- Idea, Proposal, Article, and Perspective workflows close generation,
  independent evaluation, revision, fresh evaluation or panel review, and
  human handoff.
- Assemblers and compositors preserve unresolved findings and do not silently
  repair source content.
- Reviewer unavailability stops at `independent_review_pending` rather than
  falling back to inline self-review.

### Phase 4 — Scenario evals and continuous validation

Completed outcomes:

- All five current workflows pass deterministic end-to-end scenarios.
- The maintained suite passes 63 negative guards, including 24 Research
  Polisher matrix, tier, isolation, assembler, stale-evaluation, and false-ready
  guards.
- Every changed substantive artifact requires a new version and fresh reviewer
  instance before promotion.

### Phase 5 — GitHub marketplace installation and updates

Completed infrastructure and historical observation:

- Plugin-level SemVer, rolling GitHub `main`, marketplace `git-subdir`, CI, and
  explicit upgrade/reinstall procedures are implemented.
- Historical GitHub Actions run `29171766061` succeeded for commit
  `8eb40187df7af45f562ccf39c5b4e3a10167e232`.
- The installed plugin historically upgraded from `0.5.0-preview.1` to
  `0.5.0-preview.2` and was explicitly reinstalled into the new user cache.
- Fresh Codex task `019f5379-15ad-7241-948a-14a5ddc0cebc` discovered that
  historical cache and all six entries then present, with no standalone
  `pubmed` skill.
- Canonical historical evidence remains
  `reports/phase5-upgrade-smoke.md`.

This phase established that installation machinery works; Phase 7 checks the
current source and owner environment.

### Phase 6 — Maintenance headroom and validator portability

Completed outcomes:

- Validators derive versions and inventories instead of embedding the current
  version or skill count.
- Lower, equal, malformed, and local-cachebuster release versions are rejected
  where a release SemVer increase is required.
- Quickstarts, registry, manifest, Preview label, and human-signoff boundaries
  are checked for consistency.
- ChatGPT web behavior is not inferred from Codex evidence.

## Artifact completeness and DOCX delivery hardening

- Priority: P0 blocker before Phase 7–8 resumes
- Type: deterministic source and artifact-contract maintenance
- Status: Complete in source for `0.7.0-preview.3`; awaiting owner confirmation before Phase 7 resumes

### Deliverables

- Adopt `research-idea.v2` complete Markdown snapshots, flat per-Idea nodes,
  logical parent-ID trees, digest-bound reviews, and complete PI portfolios.
- Make Proposal/SAP/Article fresh re-evaluation current-artifact-only; keep old
  versions, deltas, reports, scores, and decisions sealed from reviewers.
- Adopt `research-article.v6` with Markdown authority, preferred DOCX delivery,
  display-asset manifests, native tables/figures, parity checks, and render QA.
- Keep all descriptions and modified default-loaded SKILL bodies within the
  `9f64ad3` regression baselines through conditional references.

### Acceptance

- Delta-only Ideas, comparative-only summaries, partial proposals/manuscripts,
  identity drift, stale digests, or reviewer history access are rejected.
- A synthetic complete Article produces a native-table/embedded-figure DOCX
  whose content, captions, callouts, manifest, and page renders pass QA.
- All deterministic audits and Phase 4/6/7/8 fixtures pass at the new version.
- No local plugin reinstall, live owner-observed task, commit, push, or Phase
  7–8 acceptance credit occurs during this checkpoint.

## Project README and Cover Letter maintenance

- Priority: P0 maintenance before Phase 7–8 resumes
- Type: navigation, editorial handoff, and deterministic contract maintenance
- Status: Complete in source for `0.8.0-preview.1`; awaiting current-version install and owner observation

### Deliverables

- Require all five full-workflow orchestrators to update one minimal project-root
  README before normal delivery, pause, or stop; keep it outside reviewer inputs.
- Support versioned Article and Perspective Cover Letters through the existing
  `article-cover-letter` writer and Perspective final-copy route.
- Keep the Cover Letter quality check mechanical and free of a self-promotion
  decision.
- Add scoped publication-probability estimates only to an existing fresh
  `medical-journal-review` report, with Search-backed benchmarks when available,
  explicit uncertainty, and no extra reviewer round, artifact, state, or gate.

### Acceptance

- Five orchestrators use the same six-part README contract, valid relative links,
  authoritative state, and a next human action; reviewer `files_read` excludes it.
- Article and Perspective letters are versioned and source-bound; a Perspective
  final copy is text-identical, and stale source/outlet changes invalidate old
  letters and reviews.
- Probability cases cover full-artifact, cover-letter-only, heuristic, and
  `not_estimable` scopes; stage and overall estimates are coherent and cannot
  override fatal, blocking, stale-input, or reviewer-isolation gates.
- Counts remain 49 skills, 20 reviewers, seven declared entries, six implicit
  entries, and one explicit-only entry; deterministic audits and scenario suites
  pass without changing existing workflow states.

## Phase 7 — Personal install and workflow readiness

- Priority: P0
- Type: maintenance and owner-observed runtime validation
- Status: Paused until the hardening checkpoint passes and the owner resumes it

### Deliverables

1. Verify the current GitHub marketplace source resolves the intended
   repository, `main` revision, and `research-skills-openai` subdirectory.
2. Upgrade or explicitly reinstall `0.8.0-preview.1`, restart the Codex App when
   necessary, and inspect the resulting user cache.
3. Open a fresh Codex task and confirm discovery of 49 skills, seven declared
   entries, six implicit entries, and the permanent explicit-only Research
   Polisher entry.
4. Run one current-version owner-observed happy path for each workflow:
   - Idea;
   - Proposal;
   - Article;
   - Perspective; and
   - Research Polisher.
5. Run two cross-workflow controls:
   - reviewer delegation is unavailable and the workflow stops at
     `independent_review_pending`; and
   - a fatal or unresolved blocking finding prevents every ready or successful
     handoff state.
6. Record task and artifact bindings without requiring rollback, branch
   protection, immutable Releases, a provider adapter, or an external witness.

### Acceptance

- The GitHub marketplace can be upgraded or reinstalled using the documented
  procedure, and a fresh task loads one coherent current-version cache.
- The installed manifest and registry version agree, and the installed cache
  contains the complete declared skill tree and license.
- Fresh-task discovery reports exactly 49 skills, seven declared entries, and
  six implicit entries; no deleted `pubmed` skill is present.
- Research Polisher is explicitly callable but does not take over language
  polishing, ordinary drafting, new-idea generation, or general literature
  search.
- All five happy paths reach their workflow-declared human handoff:
  `human_signoff_required` or `human_strategy_selection_required`.
- Generator/drafter and reviewer instance identities differ. Reviewers write
  only reports and do not edit the frozen source artifact.
- Artifact lineage, input/output versions and digests, unresolved findings, and
  dissent are complete for every accepted run.
- Both controls reach their expected stop behavior; false-ready is zero.
- Each accepted run is recorded as `owner_observed`, not as external or provider
  verification.

### Verification already available

- Deterministic Phase 7 replay passes all 17 entry modes.
- Mode-specific bypass and stale/lineage mutations are rejected.
- The synthetic closed loop validates workflow-specific writers, panels,
  package boundaries, and continuation routes.
- Plugin provenance and the bundled MIT license have zero unresolved entries.

These deterministic results do not replace the current owner-observed install
and runtime checks.

## Phase 8 — Personal native research loop

- Priority: P0 after the Phase 7 install check
- Type: owner-observed Search and Deep Research validation
- Status: Paused with Phase 7 until the hardening checkpoint passes

### Deliverables

1. Preserve the existing 20-case anonymous regression corpus and its bounded
   fresh-review repeat set.
2. Run three current-version built-in Search cases:
   - a current or recently changed question;
   - an exact fact or source lookup; and
   - a narrow academic question.
3. Run one inactive-Deep-Research control that emits a self-contained
   continuation package and stops at `deep_research_handoff_required`.
4. Run one complete user-started Deep Research cycle:
   handoff, user start, completion, mapper return, and workflow resume.
5. Bind material claims to opened sources and bind mapper return and resume to
   the same evidence artifacts and digests.

### Acceptance

- The corpus remains 20/20 with fatal/blocking detection at 100%, false-ready
  zero, and lineage, isolation, source-edit boundary, and dissent preservation
  at 100%.
- Each Search case records the task, query purpose, opened source URLs or stable
  identifiers, material claim mappings, output artifact, version, digest, and
  owner confirmation.
- Search uses suitable primary or authoritative sources and makes access limits
  and disagreement visible.
- The inactive control pauses without simulating Deep Research inline and
  produces a sufficient continuation package.
- The completed cycle records the unique pending edge and resumes that edge
  exactly once. Mapper return and resume bind the same evidence artifacts.
- All five retrieval observations are current-version `owner_observed` records.

### Verification already available

- The anonymous synthetic corpus contains four outcome classes for each of the
  five workflows and passes the maintained quality and governance metrics.
- Historical Search, reviewer, and inactive-Deep-Research snapshots remain
  useful regression inputs but do not count as current owner observations.
- The Deep Research contract already defines handoff, completion, mapper-return,
  artifact-binding, and single-edge-resume invariants.

## Phase 9 — Research Polisher

- Priority: included in Phase 7 personal acceptance
- Type: owner-approved personal workflow
- Status: Source implemented; owner-observed happy path pending

Research Polisher is the seventh declared entry and remains permanently
explicit-only. Its trigger is completed or substantially completed research and
excludes copyediting, language polishing, ordinary drafting, new-idea
generation, and general literature-search requests.

Implemented workflow:

1. freeze a `research_polisher_dossier` with source identities, versions,
   digests, design, methods, existing data/results, claims, audience, and
   resource ceilings;
2. dispatch three mutually blind strategy reviewers for scientific
   significance, practical value, and dissemination/editorial positioning;
3. require each reviewer to cover `reposition_only`, `small_extension`, and
   `moderate_extension`, or return `no_defensible_option`;
4. assemble an anonymous 3-by-3 portfolio without scoring, ranking, selecting,
   or inventing a hybrid option;
5. run a fresh methodology/publishability reviewer; and
6. allow at most one targeted strategy revision and fresh re-evaluation before
   producing an unweighted Pareto view for human selection.

Maintained acceptance:

- `reposition_only` contains no new data, experiment, validation, or analysis.
- Extension strategies record assets, dependencies, feasibility basis, risks,
  and stop conditions; unsupported feasibility is rejected.
- Strategist and final-reviewer instances are distinct, source artifacts remain
  unchanged, and the assembler preserves provenance, conflicts, and dissent.
- A source-level fatal finding, stale evaluation, missing reviewer, or changed
  input digest prevents `human_strategy_selection_required`.
- The component suite covers clinical/observational, basic science,
  computational/engineering, and qualitative or mixed-methods cases.

The remaining Phase 9 task is its one current-version owner-observed happy path
inside Phase 7. It is not waiting for a public-release gate and will not become
implicit automatically.

## Phase 10 — Resume packages and workspace doctor

- Priority: P1 candidate after personal runtime validation
- Type: bounded workflow infrastructure
- Status: Candidate; not part of the current implementation

Potential scope:

- one portable continuation-package schema for
  `independent_review_pending`, `deep_research_handoff_required`, and
  `context_handoff_required`;
- exact single-edge resume in a fresh task after plugin/schema and artifact
  digest checks; and
- a read-only workspace doctor for stale evaluations, digest mismatches,
  dangling lineage, hidden dissent, and reviewer write-scope violations.

Phase 10 starts only after Phase 7–8 personal use is satisfactory or real owner
work exposes a repeated continuation problem. It adds no declared entry and is
not implemented in the current documentation change.

## Current completion decision

The plugin remains `in_progress_owner_observation` while any required Phase 7
or Phase 8 record is missing. It becomes `owner_observed_ready` only when all of
the following are complete:

- current-version install/update/reinstall and fresh-task discovery;
- five workflow happy paths;
- two cross-workflow controls;
- three Search cases;
- one inactive-Deep-Research control; and
- one complete Deep Research handoff-return-resume cycle.

No status string or synthetic fixture substitutes for those owner observations.
Conversely, shared/public release infrastructure is not required for this
personal state.

## Outside the active personal roadmap

The following work is intentionally not planned or required now:

- target-journal, target-outlet, or funder-requirements adapters;
- a fixed journal, funder, or outlet catalog;
- shared/public distribution hardening, public plugin-directory submission, or
  a production/stable channel;
- immutable external attestation releases, public-release governance, or a
  provider-authenticated evidence adapter;
- an eighth declared entry or additional implicit router;
- a restored standalone PubMed skill;
- automatic external submission or automatic human-signoff decisions; and
- Apps SDK/MCP work without a concrete personal authenticated-data need.

These items require a new explicit owner decision before they return to the
active roadmap.
