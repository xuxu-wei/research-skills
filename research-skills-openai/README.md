# Research Skills (Preview)

`research-skills-openai` is a personal, experimental ChatGPT/Codex research
workflow plugin. It contains 45 skills for research ideas, proposals, articles,
perspectives, evidence retrieval, and independent review. It is not presented
as production-stable.

Roadmap Phase 0 through Phase 4 are complete: reference closure, compact skills,
native Search/Deep Research routing, auditable state machines, fresh evaluation
gates, filesystem-observed scenario replays, and negative contract tests are enforced.

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
`0.5.0-preview.2` to `0.5.0-preview.2+codex.local-YYYYMMDD-HHMMSS`. Never commit
or push a `+codex.local-*` version to the rolling Preview channel.

## Validation

```powershell
python scripts/audit_openai_research_plugin.py
python scripts/test_openai_phase2_phase3.py
python scripts/test_openai_phase4_scenarios.py --check-report
python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid
python scripts/validate_openai_preview_release.py
python C:\Users\10149\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py research-skills-openai
```

GitHub Actions runs the portable audit, context proxy, fixture, package, release,
and SemVer-bump checks on pull requests and pushes to `main`.

The verified old-to-new GitHub reinstall and fresh-process discovery trace is in
`reports/phase5-upgrade-smoke.md`.

The workflow stops at a package prepared for human review and signature. It
does not submit material to external journals, funders, or other platforms.
