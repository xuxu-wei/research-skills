# AGENTS.md

These instructions apply to the `research-skills-openai/` plugin subtree.

## Product status and scope

- Treat this plugin as an owner-operated Personal Experimental/Preview distribution for the owner's research work in ChatGPT Work and Codex.
- Keep it skills-only unless a real MCP server, app mapping, or hook is implemented and tested.
- Do not claim public support, production stability, automatic updates, or automatic external submission.
- Use the `personal-owner` acceptance profile as the default development and release boundary. Shared/public attestation and provider verification are out of the active roadmap unless the owner explicitly reopens them.
- Preserve plugin-level SemVer in `.codex-plugin/plugin.json` and keep `workflow-registry.yaml` on the identical version.
- Whenever the plugin version changes, update README, ROADMAP, generated registries/manifests, fixtures, validation expectations, and every other document that states the current version in the same change; preserve intentionally historical version records.

## Skill authoring workflow

1. Read the target `SKILL.md`, its directly required references, `workflow-registry.yaml`, and every orchestrator that invokes it.
2. Use `skill-creator` before creating or substantially rewriting a skill.
3. Keep SKILL frontmatter limited to `name` and `description`. Store UI metadata and invocation policy in `agents/openai.yaml`.
4. Keep descriptions concise, front-load trigger terms, and state both the job and activation boundary. Keep `agents/openai.yaml` `short_description` values between 25 and 64 characters.
5. Keep core procedures in `SKILL.md`; move schemas, long rubrics, examples, and variant guidance to directly linked references with explicit load conditions.
6. Update the registry, generator/normalizer lists, README/Roadmap claims, and validation expectations in the same change.
7. Run `python scripts/normalize_openai_references.py` after adding or renaming bundled resources, then validate locally before commit or plugin reinstall.

## Discovery and context budget

- Keep the seven declared/discoverable entries limited to the five orchestrators (including `research-polisher-orchestrator`), `research-opportunity-mapper`, and `academic-deep-search` unless another deliberate product decision changes the set. Keep Research Polisher explicit-only as a permanent personal routing boundary; only a new owner decision may change it. The other six may be implicit.
- For new or substantially rewritten skills, target no more than 180 lines and 8,000 characters and do not exceed 250 lines or 12,000 characters. Existing oversized skills are Roadmap debt: do not increase them, and reduce them when touched.
- Keep a skill plus its default mandatory references below 16,000 characters where practical.
- New or substantially rewritten references longer than 100 lines require a table of contents; split references longer than 300 lines. Existing exceptions are Roadmap debt and must not grow.
- Every bundled reference, template, or script must be named directly from `SKILL.md` with a condition explaining when to load or run it.
- Use phase artifacts and concise handoff summaries instead of returning raw search logs, full traces, or unrelated intermediate output to the orchestrator.

## Workflow architecture

All full workflows must close this loop:

```text
input normalization
  -> evidence/method preprocessing
  -> generation or drafting
  -> fresh independent evaluation
  -> targeted revision
  -> fresh re-evaluation and/or independent panel
  -> final human-review package
```

- Orchestrators own routing, state, stop decisions, and aggregate comparisons; they do not score artifacts.
- Generators and drafters do not evaluate their own work.
- Controllers plan revisions and route writing to the owning drafter; they do not impersonate evaluators.
- Assemblers and compositors aggregate and verify existing artifacts; they do not silently repair source content or hide dissent.
- Every substantive artifact change creates a new version and requires a new evaluator instance before `accept`, `promoted`, or a ready-for-signoff package state.
- Fast-track modes may narrow scope but may not bypass an independent gate required for evaluation, panel review, or final packaging.

## Reviewer isolation

- Keep the registry reviewer set synchronized with the standardized `Independent Execution Contract` in each reviewer skill.
- Invoke reviewer roles explicitly in fresh subagents or delegated threads against frozen artifact IDs, paths, and versions.
- Reviewer inputs are read-only; reviewers may write only their review or verification reports.
- Reviewers do not read parent hidden reasoning, prior scores/decisions, or other reviewer outputs unless a final verifier explicitly needs sealed reports to preserve findings.
- Run each panel role in a different instance, wait for every required reviewer, and preserve conflicts, minority opinions, and dissent.
- If fresh delegation is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop. Never review inline.

## Search and Deep Research

- Use ChatGPT/Codex built-in Search for quick, recent, exact, or narrowly scoped retrieval.
- Use ChatGPT Deep Research for multi-stage, multi-direction, or multi-source synthesis.
- When Deep Research is required but inactive or unknown, emit a self-contained continuation package, return `deep_research_handoff_required`, and pause.
- Do not encode private product tool-function names in skills.
- `research-opportunity-mapper` owns broad retrieval planning and evidence/opportunity mapping.
- `academic-deep-search` is only for sufficiently specific questions answerable from a carefully read set of 2-5 papers; broader questions route to `research-opportunity-mapper`.
- Local retrieval scripts are optional Codex fallbacks for explicit reproducibility or batch-output needs, never the default ChatGPT route.

## Artifact governance and submission boundary

- Record `plugin_version`, `source_skill`, artifact ID, version ID, round ID, `based_on`, and `change_type` in workflow lineage.
- Keep source artifacts immutable; revisions write new files.
- Keep reviewer responses and revision deltas separate from final prose.
- A fatal or unresolved blocking finding prevents promotion or ready status.
- Final states stop at a package prepared for human review and signature. Do not submit to journals, funders, repositories, or other external platforms.

## Personal acceptance boundary

- Keep deterministic fixtures distinct from owner-observed runs. Passing fixtures establishes `deterministic_validated`; it does not establish that a current plugin cache completed a real task.
- Record a real task only as `owner_observed` when it binds the plugin version, task ID, source identity, artifact IDs/paths/versions, SHA-256 digests, timestamps, reviewer instance IDs where applicable, relevant source URLs, final state, and owner confirmation.
- Derive `owner_observed_ready` only after the personal runbook's installation/discovery, five workflow happy paths, two controls, three Search cases, inactive Deep Research control, and one completed Deep Research return cycle all pass.
- Until then, report `in_progress_owner_observation`. Never relabel owner-authored receipts as externally attested or provider verified.
- Source immutability, reviewer isolation, complete lineage, visible dissent, and the fatal-finding stop gate remain mandatory for the personal profile.

## Deferred evidence assets

- Existing Preview capture, immutable-release, external re-query, and provider-adapter assets are retained as historical/deferred engineering work. They are not required validation for the personal-owner profile and should not be expanded unless the owner reopens shared/public distribution work.
- Treat App Server exports and task-authored capture files as `capture_only`; redact credentials and account data before retaining them.
- A pending deferred Preview report is not a personal-profile failure and cannot block `owner_observed_ready`.

## Required validation

```powershell
python scripts/audit_openai_research_plugin.py
python scripts/audit_openai_research_proposal.py
python scripts/audit_openai_research_perspective.py
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
python C:\Users\10149\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py research-skills-openai
```

Run the deferred Preview/Release test suites only when changing their retained implementation. A structurally valid but externally pending result is acceptable for the personal-owner profile.

Also run `python scripts/audit_research_workflows.py` when shared Hermes workflow contracts or sources were changed.
