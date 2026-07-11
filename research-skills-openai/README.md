# Research Skills (Preview)

`research-skills-openai` is a personal, experimental ChatGPT/Codex research
workflow plugin. It contains 45 skills for research ideas, proposals, articles,
perspectives, evidence retrieval, and independent review. It is not presented
as production-stable.

Roadmap Phase 0 through Phase 3 are complete: reference closure, compact skills,
native Search/Deep Research routing, auditable state machines, version/fresh-
evaluation gates, canonical stop states, and single-writer rules are enforced.

## Install from the repository marketplace

The repository marketplace is `.agents/plugins/marketplace.json`. After cloning
the repository, register that non-default marketplace once and install the
plugin by its marketplace-qualified name:

```powershell
codex plugin marketplace add <repository-root>
codex plugin add research-skills-openai@xuxu-research-preview
```

The marketplace uses a `git-subdir` source pinned to the repository `main`
branch and the `research-skills-openai` subdirectory.

## Update from GitHub

Pull the latest `main` revision, then reinstall the marketplace entry and start
a new Codex task so skill discovery uses the updated plugin:

```powershell
git pull
codex plugin add research-skills-openai@xuxu-research-preview
```

For every installable behavior change, update the plugin SemVer in
`.codex-plugin/plugin.json` and keep `workflow-registry.yaml` synchronized.

## Local development cachebuster

During local iteration, replace (do not stack) the Codex build-metadata suffix,
validate, reinstall, and open a new task:

```powershell
python scripts/update_openai_plugin_cachebuster.py
python scripts/audit_openai_research_plugin.py
codex plugin add research-skills-openai@xuxu-research-preview
```

The helper preserves the base version, including any prerelease identifier, and
synchronizes the manifest and workflow registry, for example
`0.4.0-preview.1` to `0.4.0-preview.1+codex.local-YYYYMMDD-HHMMSS`.

## Validation

```powershell
python scripts/audit_openai_research_plugin.py
python scripts/test_openai_phase2_phase3.py
python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid
python C:\Users\10149\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py research-skills-openai
```

The workflow stops at a package prepared for human review and signature. It
does not submit material to external journals, funders, or other platforms.
