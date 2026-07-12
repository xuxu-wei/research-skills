# Research Skills (Preview)

`research-skills-openai` is a personal, experimental ChatGPT/Codex research
workflow plugin. It contains 45 skills for research ideas, proposals, articles,
perspectives, evidence retrieval, and independent review. It is not presented
as production-stable.

Roadmap Phase 0 through Phase 6 are complete. Phase 7 and Phase 8 are in
progress. CI enforces the static, deterministic, fixture, registry, package,
and Preview-release contracts. A historical Codex App cycle verified GitHub
Preview upgrade, reinstall, and fresh-task discovery; that receipt is evidence,
not a continuous or current-version guarantee. ChatGPT web installation,
sharing permission, and discovery remain unverified.

The next Roadmap priority is maintenance and runtime proof, not additional
public skills. Current-version live workflow runs, release/rollback evidence,
and two complete Deep Research return cycles must still pass before bounded
feature expansion. See [ROADMAP.md](ROADMAP.md).

## Install from GitHub Preview

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
`0.6.0-preview.1` to `0.6.0-preview.1+codex.local-YYYYMMDD-HHMMSS`. Never commit
or push a `+codex.local-*` version to the rolling Preview channel.

## Verified surfaces and context loading

The maintained package contains 45 skill contracts, but this Codex task's
initial plugin catalog injected descriptions for only the six entries whose
`agents/openai.yaml` sets `allow_implicit_invocation: true`:

- `academic-deep-search`
- `article-orchestrator`
- `perspective-orchestrator`
- `proposal-orchestrator`
- `research-idea-orchestrator`
- `research-opportunity-mapper`

The other 39 roles set that policy to `false`, were absent from the initial
plugin catalog, and remain available for explicit or orchestrated delegation.
This is a Codex catalog observation and a conservative character measurement,
not model-token accounting or proof that every listed skill body was loaded.
The observed catalog belonged to the task's already-installed
`0.5.0-preview.1` cache; source-candidate `0.6.0-preview.1` policy and isolated
routing are verified locally, while its marketplace install/fresh-task
discovery remain Phase 7 gates. ChatGPT web installation, discovery, sharing,
and runtime behavior remain unverified.

## Public entry quickstarts

Each prompt explicitly names one public entry so it can be pasted into a fresh
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
- Expected output: the requested blueprint, section, draft, or verified human-review package with lineage and review status.
- Stop states: `blocked`, `stopped`, `independent_review_pending`, or `context_handoff_required`.
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
Use $research-idea-orchestrator in [standard | resume_candidates | portfolio_only] mode. Research direction or problem: [topic]. Population/context: [scope]. Available evidence, funding call, data asset, or candidate paths: [summary/path]. Produce an independently evaluated PI-review idea portfolio.
```

- Minimum input: a research direction or practical problem and one usable context, evidence, funding, or data cue.
- Expected output: a ranked PI-review portfolio with candidate lineage, independent evaluations, dissent, and handoff status.
- Stop states: `blocked`, `stopped`, `independent_review_pending`, or `context_handoff_required`.
- Resume: paste the continuation brief and provide the missing context, evidence, frozen candidate set, or reviewer capacity.

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
python scripts/test_openai_release_contract.py
python scripts/sync_openai_fixture_versions.py
python scripts/test_openai_phase6_context.py
python scripts/test_openai_phase2_phase3.py
python scripts/test_openai_phase4_scenarios.py --check-report
python scripts/test_openai_phase7_modes.py --check-report
python scripts/test_openai_phase8_corpus.py --check-report
python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid
python scripts/generate_openai_release_ledger.py --check
python scripts/test_openai_release_ledger.py
python scripts/validate_openai_preview_release.py
python C:\Users\10149\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py research-skills-openai
```

GitHub Actions runs the portable audit, context proxy, fixture, package, release,
and SemVer-bump checks on pull requests and pushes to `main`.

The verified historical GitHub reinstall and fresh-process discovery trace is
in `reports/phase5-upgrade-smoke.md`. The current candidate's commit, CI,
marketplace upgrade/reinstall, fresh-task discovery, and rollback status are
tracked without inference in `reports/release-ledger.json`. A `verified`
external record is accepted only when it binds a repository-relative evidence
file by raw SHA-256, the file's observed payload exactly matches the ledger
record, the release commit's committed plugin and validation-contract trees
match the recorded identity, and an implemented authenticated external-evidence
adapter verifies provider origin. The evidence envelope is defined in
`../tests/openai_phase7/release-evidence.schema.yaml`; no such adapter is
currently implemented, so unobserved or repository-authored records stay
`pending`.

Install, reinstall, discovery, and rollback evidence must also include the
provider-exported cache inventory. The validator recomputes a cache content
identity from the plugin version, immutable source commit, manifest, registry,
complete skill tree, and bundled license. Fresh-task discovery must name and
exactly match one verified N+1 install cache; rollback must bind the selected
current cache and a distinct cache matching the previous release. A cache path
or `cache_mixing_absent` label alone cannot close these gates.

Phase 8 evidence is split deliberately: the anonymous synthetic corpus passes;
three Search runs and one inactive Deep Research pause are recorded only as
self-attested current-task snapshots and do not satisfy verified live gates.
Six earlier review snapshots are retained as explicitly excluded historical
records because their reviewer-visible identifiers disclosed outcome labels;
six fresh replacements using opaque A01-A03 source, case, run, bundle, prompt,
and real instance identifiers now count as current self-attested observations,
but remain 0 verified live receipts. Repository-authored files and recomputed
digests are integrity records, not provider provenance, and can never promote a
receipt by themselves. Promotion requires an executable provider-verifier
adapter plus source-commit/tree identity and current timestamps. Verified
review dispatch must use a source-only sanitized blind bundle whose content
and lineage contain no prior reviewer/evaluator outputs, scores, or decisions.
Validation also reads the bound source file bytes. It requires exactly one
embedded metadata block with the declared field allowlist and accepts only
source/data/context/blueprint/analysis/evidence-class `based_on` artifacts; a
clean bundle cannot mask review instructions, revision briefs, expected-result
oracles, prior conclusions, scores, decisions, or review-artifact lineage in
the source itself. Reviewer-visible identifiers and non-skill resource paths
also reject tokenized outcome labels such as `happy`, `fixable`, `fatal`,
`pending`, `expected`, `oracle`, `accept`, `reject`, `blocked`, or `ready`;
declared skill-resource paths are excluded from this name check.
For Deep Research, every opened source must be primary or authoritative,
identity-verified, and traced to material claims; mapper return and workflow
resume must bind the same real evidence-artifact paths and SHA-256 digests. A
provider-run-completed receipt must bind provider run ID, status, time, and raw
output, with strict `handoff < user start < provider complete < mapper return <
resume` ordering. No real provider adapter is currently installed; synthetic
validator overrides run only in ephemeral temp directories and never count as
runtime evidence. Two complete Deep Research cycles remain pending. See
`reports/phase8-corpus-results.json`.

The workflow stops at a package prepared for human review and signature. It
does not submit material to external journals, funders, or other platforms.
