# Research Skills OpenAI Plugin Roadmap

Status: Experimental/Preview  
Planning baseline: 2026-07-12  
Current scope: 45 skills after removal of the standalone OpenAI `pubmed` skill

Completion status: Phase 0 through Phase 3 complete on 2026-07-12; Phase 4-5 remain planned.

## Objective

Turn the current personal development plugin into a context-efficient, auditable research workflow plugin for ChatGPT Work and Codex. The plugin should provide complete orchestration, explicit task distribution, independent evaluation and revision loops, source-grounded retrieval, and human-review delivery without depending on platform-specific private tool syntax.

## Current baseline

- Four workflow entry points: idea, proposal, article, and perspective.
- Eighteen reviewer-class skills require fresh independent subagents.
- `research-opportunity-mapper` routes broad evidence retrieval and Deep Research handoffs.
- `academic-deep-search` handles narrow questions answerable through 2-5 papers.
- Plugin discovery, manifest, registry, and GitHub marketplace installation are implemented.
- Static validation now covers recursive references, orphan resources, context budgets, workflow edges, discovery, reviewer isolation, and plugin structure. Scenario-level runtime tests remain a later phase.

## Phase 0 – Reference and registry closure

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

## Phase 1 – Context reduction

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

## Phase 2 – Native Search and Deep Research

Status: Complete (2026-07-12)

Deliverables:

- Make `research-opportunity-mapper` the single owner of broad retrieval policy.
- Use built-in Search for quick, current, exact, or targeted retrieval.
- Use Deep Research for multi-stage or multi-source synthesis.
- Emit a self-contained continuation package and pause when Deep Research is required but inactive or unknown.
- Keep local scripts only as explicit reproducibility/batch fallbacks; remove default script-preference language.
- Keep `academic-deep-search` limited to specific questions for which 2-5 carefully read papers are sufficient.

Acceptance:

- One live targeted Search scenario returns opened, verified primary/authoritative sources.
- One inactive Deep Research scenario returns `deep_research_handoff_required` and a complete resume package.
- No orchestrator prefers local scripts over native Search or Deep Research.
- No deleted or external retrieval skill remains as a dangling dependency.

## Phase 3 – Workflow state-machine closure

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

Implement fixture-driven tests for:

1. Idea: generation -> evaluator -> revision -> fresh evaluator -> adversarial panel -> portfolio.
2. Proposal: draft -> evaluator -> revision -> fresh evaluator -> optional SAP evaluator -> panel -> package.
3. Article: draft -> methods/claim audits -> evaluator -> revision -> fresh evaluator -> panel -> compositor.
4. Perspective: draft -> evaluator -> revision -> fresh evaluator -> panel patch -> fresh evaluator -> compositor.

Also test unique reviewer instance IDs, reviewer write scopes, prior-score blindness, fatal-flaw blocking, visible dissent, Search routing, Deep Research continuation, and 16K/32K context behavior.

Acceptance:

- All four workflow fixtures complete the independent evaluation/revision loop.
- Every panel role has a distinct reviewer instance ID.
- Reviewer writes remain limited to review/verification report locations.
- Runtime results agree with registry edges and artifact lineage.

## Phase 5 — Preview release and GitHub updates

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

## Later development

- Build a reusable anonymized evaluation corpus from real research workflow failures.
- Add journal/funder adapters only as conditionally loaded references or separately versioned modules.
- Evaluate an Apps SDK/MCP companion only when live authenticated data or programmatic handoff becomes necessary.
- Consider public directory submission only after reference, context, workflow, runtime, update, and workspace-sharing gates are all satisfied.
