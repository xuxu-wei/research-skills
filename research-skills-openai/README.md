# Research Skills (Personal Preview)

`research-skills-openai` is an owner-operated, experimental ChatGPT/Codex
research workflow plugin. It contains 49 skills for research ideas, proposals,
articles, perspectives, research-impact positioning, evidence retrieval, and
independent review. It is maintained for one owner's research work and is not
presented as a production-stable, supported, shared, or public distribution.

The maintained deterministic suite covers static audits, workflow fixtures,
reviewer isolation, context budgets, registry generation, and plugin packaging.
The `0.9.0-preview.1` Idea-v3 checkpoint passes that suite. The plugin remains
`in_progress_owner_observation`, not `owner_observed_ready`, until its private
current-version runtime slots are completed.

The immediate priorities are deliberately small:

1. bind the already diagnosed current-version install, cache identity, and
   fresh-task discovery to the formal owner-observed distribution receipt;
2. run one owner-observed happy path for each of the five workflows plus two
   cross-workflow controls; and
3. exercise three built-in Search cases, one inactive-Deep-Research control,
   and one complete user-started Deep Research handoff-return-resume cycle.

Research Polisher is already implemented as the seventh declared entry and is
permanently explicit-only under the current personal routing policy. See
[ROADMAP.md](ROADMAP.md) for sequencing and the current acceptance state.
ChatGPT web installation, sharing, and discovery have not been verified and are
not required for the current personal Codex profile.

## Install from GitHub

Register the GitHub repository as the rolling Preview marketplace once, then
install the marketplace-qualified plugin:

```powershell
codex plugin marketplace add xuxu-wei/research-skills --ref main
codex plugin add research-skills-openai@xuxu-research-preview
```

The marketplace uses a `git-subdir` source that tracks the rolling Preview `main`
branch and the `research-skills-openai` subdirectory. A cloned checkout can be
registered instead with `codex plugin marketplace add <repository-root>` for
local marketplace inspection, but that source is not the GitHub update test.

## Update from GitHub

After a new SemVer is pushed to GitHub `main`, refresh the Git marketplace
snapshot, reinstall, and start a new Codex task:

```powershell
codex plugin marketplace upgrade xuxu-research-preview
codex plugin add research-skills-openai@xuxu-research-preview
```

If the standalone CLI is absent, the Codex App bundle can provide the same CLI;
the current executable path is recorded as `CODEX_CLI_PATH` in the App's
`~/.codex/config.toml`. Treat that path as App-managed and do not hard-code its
build-specific directory. If a long-running App process still reports the old
cache path, restart the App and open another new task before judging discovery.

For every installable behavior change, update the plugin SemVer in
`.codex-plugin/plugin.json` and keep `workflow-registry.yaml` synchronized.

After reinstall, restart the Codex App if it still reports the previous cache,
then open a new task. Record the Marketplace revision, installed cache path,
Manifest version, and Registry digest, and confirm 49 skills, seven declared
entries, six implicit entries, and no standalone `pubmed` skill. Only a new task
using one coherent current-version cache completes the personal distribution
slot.

## Personal acceptance

The personal acceptance profile contains 13 owner-observed slots:

| Group | Required observations |
|---|---:|
| Current-version install and fresh-task discovery | 1 |
| Idea, Proposal, Article, Perspective, and Research Polisher happy paths | 5 |
| Reviewer-unavailable and fatal-finding controls | 2 |
| Current, exact, and narrow-academic Search cases | 3 |
| Inactive Deep Research control | 1 |
| Complete Deep Research handoff-return-resume cycle | 1 |

The five workflow happy paths must finish at `human_signoff_required` or, for
Research Polisher, `human_strategy_selection_required`. Reviewer unavailability
must stop at `independent_review_pending`; a fatal or unresolved blocking
finding must never produce a ready state.

Each observed slot records the task ID, plugin version, source identity,
artifact paths and SHA-256 digests, timestamps, reviewer instance IDs when
applicable, Search URLs when applicable, actual outcome, and explicit owner
confirmation.

## Local development cachebuster

GitHub reinstall never reads unpushed working-tree changes. During local
iteration, replace (do not stack) the Codex build-metadata suffix, validate,
copy the maintained plugin into the personal local marketplace, temporarily
disable the GitHub-qualified copy if both are enabled, and open a new task:

```powershell
python scripts/update_openai_plugin_cachebuster.py
python scripts/audit_openai_research_plugin.py
python scripts/codex_plugin_converter.py --mode codex --install --fail-on-invalid
```

The helper preserves the base version, including any prerelease identifier, and
synchronizes the manifest and workflow registry, for example
`0.9.0-preview.1` to `0.9.0-preview.1+codex.local-YYYYMMDD-HHMMSS`. Never commit
or push a `+codex.local-*` version to the rolling Preview channel.

## Inventory and invocation policy

The maintained `0.9.0-preview.1` source contains 49 skill contracts and declares
seven discoverable entry skills. Six currently set
`allow_implicit_invocation: true`:

- `academic-deep-search`
- `article-orchestrator`
- `perspective-orchestrator`
- `proposal-orchestrator`
- `research-idea-orchestrator`
- `research-opportunity-mapper`

`research-polisher-orchestrator` is the seventh declared entry and has a complete
quickstart. It remains explicit-only as a permanent personal routing boundary;
it must not take over language polishing, ordinary drafting, new-idea
generation, or general literature-search requests. The other 42 private roles
also set the policy to `false` and remain available for explicit or
orchestrated delegation.

A current-environment diagnostic on 2026-07-16 confirmed that the GitHub
marketplace is registered, the plugin is enabled with the coherent
`0.9.0-preview.1` cache, and the current version is discoverable in both Codex
App and a fresh Codex CLI task. The installation mechanism and current-version
loading are therefore diagnostically confirmed. The formal
`personal-distribution-current` slot remains pending until its task/source
identity, artifact digest, timestamps, outcome, and owner confirmation are
captured in the private receipt.

## Artifact format defaults

- Idea uses `research-idea.v3`: each active node owns a complete versioned
  Markdown Dossier, a concise index, and a human-readable reference ledger.
  The Dossier contains background, methods, expected outputs, references, and
  semi-structured evidence chains expressed as input -> method/analysis/
  processing -> output. It is both the sole project artifact read by the fresh
  Idea evaluator and the Idea delivered to the owner.
- Idea direction routing is adaptive. A clear, supported direction receives
  focused optimization; a vague direction with several supported opportunities
  explores two or at most three directions for one bounded round before remapping
  evidence and opportunity. Titles, audiences, and editorial positioning may be
  changed without mandatory new work when every resulting claim is supported by
  the actual implementation. A novel method, data, or discovery claim still
  requires a real increment.
- Opaque workflow markers do not appear in an Idea Dossier. Historical or
  internal reports resolve them through the node's reference ledger with a
  readable label and source locator. When present, the visible v1 run under
  `../tests/idea-to-proposal/.phase7-8-runs/idea/` is an ignored project test
  example, not a migration target; no actual v2 project is currently present.
  v1/v2 layouts remain read-only.
- Proposal and Article re-evaluators receive only the complete current artifact,
  its digest, stable facts/rubric, and an optional anonymous must-fix list. Prior
  versions, deltas, reports, scores, and decisions remain sealed.
- Article uses complete Markdown as the audit source and DOCX as the preferred
  user-facing format when document tooling is available. DOCX packages integrate
  native tables and available figures and must pass content-parity and full-page
  render QA before human sign-off.
- Each full workflow updates one minimal project-root `README.md` before a normal
  handoff, pause, or stop. It links current deliverables, summarizes state and
  unresolved review issues, and supplies the next human action; reviewers never
  use it as evidence.
- Article and Perspective can produce versioned Cover Letters. When the existing
  `medical-journal-review` call can support a publication-probability estimate,
  the scoped interval, confidence, benchmarks, and limitations stay inside that
  same independent review report and are only summarized in the project README.

## Entry-skill quickstarts

Each prompt explicitly names one declared entry so it can be pasted into a fresh
task without asking the router to choose among unrelated workflows.

### `$academic-deep-search`

```text
Use $academic-deep-search to answer this specific academic question by closely reading 2-5 papers: [question]. Population/context: [scope]. Date or source constraints: [constraints or none]. Return cited findings, disagreements, access limits, and a concise answer.
```

- Minimum input: one bounded academic question plus any scope constraints.
- Expected output: a source-grounded answer based on 2-5 carefully read papers.
- Stop states: the question needs broad synthesis, required papers are inaccessible, or available evidence cannot answer it.
- Resume: narrow the question, provide missing papers, or confirm a broader retrieval handoff using the returned brief.

### `$article-orchestrator`

```text
Use $article-orchestrator in [standard | fast_track_draft | fast_track_draft_and_evaluation | blueprint_only | section_specific | submission_only] mode. Study summary: [summary]. Available artifact paths: [paths]. Article type or target journal: [target or unknown]. Build the requested workflow output, use fresh independent reviewers, and stop at human review.
```

- Minimum input: an entry mode, study summary, and paths to available study or manuscript artifacts.
- Expected output: the requested blueprint/section or a complete canonical manuscript plus synchronized DOCX and integrated table/figure package when document tooling is available.
- Stop states: `blocked`, `stopped`, `independent_review_pending`, `docx_generation_pending`, `docx_visual_qa_pending`, or `context_handoff_required`.
- Resume: paste the continuation brief and provide the requested artifact, reviewer availability, or current frozen version.

### `$perspective-orchestrator`

```text
Use $perspective-orchestrator in [lite | standard | full] mode. Thesis: [contestable thesis]. Audience/outlet: [target or unknown]. Evidence paths or citations: [sources]. Produce the requested Perspective workflow output with fresh independent review and stop at human review.
```

- Minimum input: a contestable thesis, mode, intended audience, and available evidence.
- Expected output: a versioned Perspective workflow package appropriate to the selected mode, with visible findings and dissent.
- Stop states: `blocked`, `stopped`, `independent_review_pending`, or `context_handoff_required`.
- Resume: paste the continuation brief with missing evidence, clarified thesis/outlet, or current frozen artifact version.

### `$proposal-orchestrator`

```text
Use $proposal-orchestrator in [standard | existing_draft | draft_and_external_review | package_only] mode. Objective: [objective]. Funding call or constraints: [summary/path]. Available idea, draft, data, and evidence paths: [paths]. Optional SAP request: [request or none]. Produce a versioned proposal workflow package with fresh independent review and stop at human review.
```

- Minimum input: an entry mode, proposal objective, applicable constraints, and available source artifacts.
- Expected output: the selected proposal, revision, or SAP package with evaluation, lineage, dissent, and unresolved issues.
- Stop states: `blocked`, `stopped`, `independent_review_pending`, or `context_handoff_required`.
- Resume: paste the continuation brief and supply the requested clarification, frozen draft, review capacity, or missing evidence.

### `$research-idea-orchestrator`

```text
Use $research-idea-orchestrator in [standard | resume_candidates | portfolio_only] mode. Research direction or problem: [topic]. Population/context: [scope]. Available evidence, funding call, data asset, or candidate paths: [summary/path]. Build one focused direction or explore at most three evidence-supported directions, and deliver independently evaluated complete Idea Dossiers.
```

- Minimum input: a research direction or practical problem and one usable context, evidence, funding, or data cue.
- Expected output: one to three self-contained Idea Dossiers with readable
  references, closed input-method/output evidence chains, digest-bound
  evaluations, lineage, dissent, and a navigation or comparison handoff.
- Stop states: `blocked`, `stopped`, `new_idea_required`, `no_defensible_direction`,
  `direction_route_confirmation_required`, `layout_migration_required`,
  `independent_review_pending`, or `context_handoff_required`. Bounded exploration
  ends at `human_direction_selection_required`.
- Resume: paste the continuation brief and provide the missing context, evidence,
  current Dossier/index, routing choice, or reviewer capacity.

### `$research-polisher-orchestrator`

```text
Use $research-polisher-orchestrator in standard mode for this completed or substantially completed research work. Research question, design, methods, existing data and results: [summary and artifact paths]. Current claims, story, audience, and outlet: [summary or unknown]. Available resources, time, data access, and maximum added-work tier: [constraints]. Produce reposition-only, small-extension, and moderate-extension strategies through mutually blind reviewers, independent methodology and publishability review, and a Pareto selection dossier; do not perform language copyediting or invent a new study.
```

- Minimum input: a completed or substantially completed study with frozen source paths or a sufficiently detailed design, methods, data, results, and resource summary.
- Expected output: a versioned 3-by-3 impact-strategy portfolio, preserved dissent, fresh independent methodology/publishability evaluation, and a human-selection dossier.
- Stop states: `revision_required`, `specialist_review_pending`, `no_defensible_option`, `independent_review_pending`, `deep_research_handoff_required`, `clarification_stop`, `blocked`, or `stopped`; a qualifying package stops at human strategy selection.
- Resume: paste the self-contained continuation brief with the missing frozen artifacts, evidence return, resource constraints, or reviewer availability.

### `$research-opportunity-mapper`

```text
Use $research-opportunity-mapper for this broad evidence question: [question]. Decision the map must support: [decision]. Scope, dates, languages, and preferred/excluded sources: [constraints]. Return an evidence map, opportunity map, conflicts, gaps, and stable citations.
```

- Minimum input: a broad evidence question, downstream decision, and retrieval scope.
- Expected output: an auditable evidence/opportunity map with conflicts, limitations, gaps, and source links or identifiers.
- Stop states: `deep_research_handoff_required` when multi-stage synthesis needs inactive Deep Research, or a documented evidence/access block.
- Resume: activate Deep Research and submit the continuation package, or refine scope and provide inaccessible priority sources.

## Validation

```powershell
python scripts/audit_openai_research_plugin.py
python scripts/audit_openai_research_proposal.py
python scripts/audit_openai_research_perspective.py
python scripts/test_openai_roadmap_contract.py
python scripts/test_openai_release_contract.py
python scripts/sync_openai_fixture_versions.py
python scripts/test_openai_artifact_completeness.py
python scripts/test_openai_article_docx_contract.py
python scripts/test_openai_phase6_context.py
python scripts/test_openai_phase2_phase3.py
python scripts/test_openai_phase4_scenarios.py --check-report
python scripts/test_openai_phase7_modes.py --check-report
python scripts/test_openai_phase8_corpus.py --check-report
python scripts/test_validate_openai_personal_readiness.py
python scripts/validate_openai_personal_readiness.py --check-report
python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" research-skills-openai
```

GitHub Actions runs the portable audits, context budgets, workflow fixtures,
package checks, and SemVer checks on pull requests and pushes to `main`.

The personal runtime evidence level is `owner_observed`. Each accepted
observation binds the plugin version, task ID, frozen input and output artifact
IDs or paths, SHA-256 digests, timestamps, reviewer instances where applicable,
and an explicit owner confirmation. These receipts support only the personal
state `owner_observed_ready`; they do not assert external, provider, shared, or
public attestation.

The tracked
`../tests/openai_personal/current-version-owner-observed-receipts.yaml` is only
an all-pending schema template. Copy it to the ignored local path
`../tests/article/.phase7-8-runs/local-owner-observed-receipts.yaml` and record
task IDs, artifact bindings, timestamps, reviewer IDs, URLs, and confirmations
only in that private copy. Pass it with `--receipts`; never commit it:

```powershell
$privateReceipts = "tests/article/.phase7-8-runs/local-owner-observed-receipts.yaml"
New-Item -ItemType Directory -Force (Split-Path $privateReceipts) | Out-Null
Copy-Item tests/openai_personal/current-version-owner-observed-receipts.yaml $privateReceipts
```

The tracked derived report contains slot status/counts only. Pending observations remain a
valid `in_progress_owner_observation` state and do not fail deterministic CI.

Validate local progress without rewriting the tracked report:

```powershell
python scripts/validate_openai_personal_readiness.py --receipts $privateReceipts
```

Assert final personal readiness only after every slot is observed:

```powershell
python scripts/validate_openai_personal_readiness.py --receipts $privateReceipts --require-ready
```

The core runtime constraints remain unchanged:

- generators and drafters do not review their own work;
- reviewer roles run in fresh delegated instances against frozen inputs and do
  not edit the reviewed artifact;
- substantive revisions create a new version and receive a fresh evaluation;
- artifact lineage and reviewer dissent remain visible; and
- a fatal or unresolved blocking finding prevents promotion or human-handoff
  readiness.

The workflow stops at a package prepared for human review and signature. It
does not submit material to external journals, funders, or other platforms.
