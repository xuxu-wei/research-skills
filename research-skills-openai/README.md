# Research Skills (Personal Preview)

`research-skills-openai` is an owner-operated, experimental ChatGPT/Codex
research workflow plugin. It contains 51 skills for research ideas, proposals,
articles, perspectives, research-impact positioning, evidence retrieval, and
independent review. It is maintained for one owner's research work and is not
presented as a production-stable, supported, shared, or public distribution.

The maintained deterministic suite covers static audits, workflow fixtures,
reviewer isolation, context budgets, registry generation, and plugin packaging.
The `0.11.0` checkpoint adds one shared narrative assessor and reader-readiness
contracts for Idea, Proposal, Perspective, and Article. Historical Roadmap phases
remain closed records and are not rerun merely because later versions change
their assumptions. Complete Search/Deep Research runtime revalidation is not an
active priority unless the owner explicitly reopens it.

Research Polisher is already implemented as the seventh declared entry and is
permanently explicit-only under the current personal routing policy. See
[ROADMAP.md](ROADMAP.md) for sequencing and the current acceptance state.
ChatGPT web installation, sharing, and discovery have not been verified and are
not required for the current personal Codex profile.

## Install from GitHub

Register the GitHub repository as the rolling Preview marketplace once, then
install the marketplace-qualified plugin:

```powershell
$codexCli = (python scripts/openai_plugin_dev.py status --json | ConvertFrom-Json).codex_cli
& $codexCli plugin marketplace add xuxu-wei/research-skills --ref main
& $codexCli plugin add research-skills-openai@xuxu-research-preview
```

The marketplace uses a `git-subdir` source that tracks the rolling Preview `main`
branch and the `research-skills-openai` subdirectory. A cloned checkout can be
registered instead with `codex plugin marketplace add <repository-root>` for
local marketplace inspection, but that source is not the GitHub update test.

## Update from GitHub

After a new SemVer is pushed to GitHub `main`, refresh the Git marketplace
snapshot, reinstall, and start a new Codex task:

```powershell
$codexCli = (python scripts/openai_plugin_dev.py status --json | ConvertFrom-Json).codex_cli
& $codexCli plugin marketplace upgrade xuxu-research-preview
& $codexCli plugin add research-skills-openai@xuxu-research-preview
```

If the marketplace is no longer registered, restore it first with
`& $codexCli plugin marketplace add xuxu-wei/research-skills --ref main`, then
repeat the upgrade and add commands.

If the standalone CLI is absent, the Codex App bundle can provide the same CLI;
the current executable path is recorded as `CODEX_CLI_PATH` in the App's
`~/.codex/config.toml`. Treat that path as App-managed and do not hard-code its
build-specific directory. If a long-running App process still reports the old
cache path, restart the App and open another new task before judging discovery.

For every installable behavior change, update the plugin SemVer in
`.codex-plugin/plugin.json` and keep `workflow-registry.yaml` synchronized.

After reinstall, restart the Codex App if it still reports the previous cache,
then open a new task. Record the Marketplace revision, installed cache path,
Manifest and Registry versions, and confirm 51 skills, 22 independent reviewer
roles, seven declared entries, six implicit entries, and no standalone `pubmed`
skill. Behavioral validation must run in a new task using one coherent
current-version cache.

## Local development and version debugging

GitHub reinstall never reads unpushed working-tree changes, and an existing
Codex task does not hot-reload changed Skill files. Use Python 3.11 or later and
create an isolated environment once from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8 = "1"
python -m pip install -r requirements-dev.txt
python scripts/openai_plugin_dev.py status
```

Keep `PYTHONUTF8=1` in Windows validation shells so `quick_validate.py` reads
UTF-8 Skill files independently of the system locale.

`install-local` is an update loop and requires the personal marketplace entry
to already point to `./plugins/research-skills-openai`. On a first setup only,
when neither that entry nor the personal Local copy exists, create them through
plugin-creator rather than editing `marketplace.json`:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\create_basic_plugin.py" research-skills-openai --with-marketplace --category Research
```

If `status --json` instead reports an existing but mismatched entry, stop and
repair it through plugin-creator; the update helper intentionally does not
rewrite marketplace configuration.

In the Codex App, temporarily disable the Git-installed
`research-skills-openai` plugin. Then install and verify an isolated Local copy:

```powershell
python scripts/openai_plugin_dev.py install-local
python scripts/openai_plugin_dev.py verify --channel local --expected-version 0.11.0
```

The equivalent CLI switch is
`& $codexCli plugin remove research-skills-openai@xuxu-research-preview --json`.
Removing that installed selector does not remove the Git marketplace itself.
If Windows holds the active Local copy open, close the Codex App before
`install-local`, then reopen it after verification; keep the Local selector as
the only enabled channel during this loop.

The helper validates the existing marketplace entry and tracked source, then
copies the source to the personal Local
plugin directory. It writes `+codex.local-YYYYMMDD-HHMMSS-ffffff` only into that copy;
the worktree remains `0.11.0`. It refuses installation while the Git
channel is enabled, never edits marketplace JSON, and restores the previous
Local copy if installation fails. Do not delete plugin caches.

`verify --channel local` compares the complete file inventory and file contents
against the current worktree, allowing only the two local version fields to
differ; it does not save hashes. The cachebuster includes microseconds, so each
rapid reinstall is separately discoverable.

After every Skill change, rerun `install-local` and start a new Codex task. Keep
exactly one channel enabled: Local during iteration, Git after acceptance. Once
tests pass, commit and push the source, disable the Local plugin, enable or
upgrade the Git plugin, verify it, and start another new task:

```powershell
$codexCli = (python scripts/openai_plugin_dev.py status --json | ConvertFrom-Json).codex_cli
& $codexCli plugin remove research-skills-openai@local --json
& $codexCli plugin marketplace upgrade xuxu-research-preview
& $codexCli plugin add research-skills-openai@xuxu-research-preview --json
python scripts/openai_plugin_dev.py verify --channel github --expected-version 0.11.0
```

For a non-mutating discovery smoke test, run a fresh ephemeral task after either
channel verifies. The response must identify the requested installed Skill and
the expected base version; it must not edit the repository:

```powershell
& $codexCli exec --ephemeral --sandbox read-only --cd (Get-Location) `
  'Use $research-narrative-assessor. Report its installed plugin version and its two required assessment outputs; do not edit files.'
```

Never commit or push a `+codex.local-*` version.

## Inventory and invocation policy

The maintained `0.11.0` source contains 51 skill contracts and declares
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
generation, or general literature-search requests. The other 44 private roles
also set the policy to `false` and remain available for explicit or
orchestrated delegation.

A prior current-environment diagnostic confirmed the GitHub marketplace,
enabled-plugin, and fresh-task discovery mechanism. Current workflow artifacts
bind readable logical identity, exact paths, frozen state, a complete index, and
a unique current pointer; new LLM-facing interfaces do not persist hashes.

## Artifact format defaults

- Idea uses `research-idea.v3`: each active node owns a complete versioned
  Markdown Dossier, a concise index, and a human-readable reference ledger.
  The Dossier contains background, methods, expected outputs, references, and
  semi-structured evidence chains expressed as input -> method/analysis/
  processing -> output. It is both the sole project artifact read by the fresh
  Idea evaluator and the Idea delivered to the owner. After scientific and
  methodological revision, fresh narrative and full-dossier language reviewers
  assess the frozen dossier in parallel. The shared
  `research-narrative-assessor` owns argument architecture; the
  `academic-language-assessor` owns language and reader-aware terminology. The orchestrator reconciles their
  included actions into one approved writer brief; the writer does not read the
  two reports or assessor plan. Any editorial repair uses that brief, a
  protected-content register, a new dossier version, independent preservation
  review, and fresh readiness reassessment before evaluation.
- Idea direction routing is adaptive. A clear, supported direction receives
  focused optimization; a vague direction with several supported opportunities
  explores two or at most three directions for one bounded round before remapping
  evidence and opportunity. Titles, audiences, and editorial positioning may be
  changed without mandatory new work when every resulting claim is supported by
  the actual implementation. A novel method, data, or discovery claim still
  requires a real increment.
- Opaque workflow markers do not appear in an Idea Dossier. Historical or
  internal reports resolve them through the node's reference ledger with a
  readable label and source locator. Legacy v1/v2 layouts remain read-only.
- Proposal creates a reader-facing section-content plan before a separate writer
  instance drafts prose. Perspective retains its argument architecture and
  paragraph map. Article inventories every supplied material, records one
  semantic authority while retaining compatible supporting assets, and builds a
  full section-content blueprint before drafting.
- Final Idea, Proposal, Perspective, and Article evaluators receive only the
  complete current reader artifact or contract-defined reader bundle, the stable
  skill rubric, and minimal necessary factual or outlet constraints. Prior
  versions, plans, audits, readiness reports, repair materials, deltas, scores,
  and decisions remain sealed.
- Across all four workflows, one authoritative location contains the complete
  limitation discussion. Other sections omit it unless the limitation itself is
  necessary to advance the immediate reasoning and omission would distort that
  reasoning; pointer-only repetition is not used.
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
  references, closed input-method/output evidence chains, narrative/language
  readiness, logical-reference-bound evaluations, lineage, dissent, and a
  navigation or comparison handoff.
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
python scripts/test_openai_cross_workflow_narrative_contract.py
python scripts/test_openai_article_docx_contract.py
python research-skills-openai/skills/academic-language-assessor/scripts/test_validate_language_assessment.py
python scripts/test_openai_plugin_dev.py
python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" research-skills-openai
```

Run `skill-creator/scripts/quick_validate.py` for every new or modified Skill.
These commands validate the current change only. Completed Roadmap phase suites
are historical and run again only when the owner explicitly reopens them.

GitHub Actions runs the portable audits, context budgets, workflow fixtures,
package checks, and SemVer checks on pull requests and pushes to `main`.

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
