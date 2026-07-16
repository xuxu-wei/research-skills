# Phase 5 GitHub Upgrade Smoke

Status: upgrade_verified  
Verification date: 2026-07-12 (Asia/Singapore)  
Marketplace: `xuxu-research-preview`  
Plugin: `research-skills-openai`

## Acceptance chain

1. The previously installed GitHub-marketplace cache was frozen as the baseline:
   - version: `0.5.0-preview.1`
   - cache: `$CODEX_HOME\plugins\cache\xuxu-research-preview\research-skills-openai\0.5.0-preview.1`
   - discovered skill directories: `45`
   - `skills/pubmed` present: `false`
2. GitHub `main` was updated to commit `8eb40187df7af45f562ccf39c5b4e3a10167e232`, whose plugin manifest declares `0.5.0-preview.2`.
3. GitHub Actions run `29171766061` (`OpenAI Plugin Preview`) completed with conclusion `success` for that commit:
   - <https://github.com/xuxu-wei/research-skills/actions/runs/29171766061>
4. The App-bundled Codex CLI refreshed the configured Git marketplace and returned:

   ```json
   {
     "selectedMarketplaces": ["xuxu-research-preview"],
     "upgradedRoots": [
       "$CODEX_HOME\\.tmp\\marketplaces\\xuxu-research-preview"
     ],
     "errors": []
   }
   ```

   The marketplace continues to resolve `https://github.com/xuxu-wei/research-skills.git`, subdirectory `research-skills-openai`, ref `main`.

5. Explicit reinstall of `research-skills-openai@xuxu-research-preview` returned:

   ```json
   {
     "pluginId": "research-skills-openai@xuxu-research-preview",
     "name": "research-skills-openai",
     "marketplaceName": "xuxu-research-preview",
     "version": "0.5.0-preview.2",
     "installedPath": "$CODEX_HOME\\plugins\\cache\\xuxu-research-preview\\research-skills-openai\\0.5.0-preview.2",
     "authPolicy": "ON_INSTALL"
   }
   ```

6. Direct cache inspection confirmed:
   - manifest version: `0.5.0-preview.2`
   - registry schema version: `5`
   - discovered skill directories: `45`
   - valid `agents/openai.yaml` files: `45`
   - `skills/pubmed` present: `false`
   - source and installed skills trees: `330` files each
   - normalized source/cache SHA-256: `2409b09f94a51228ce4e58472a744c5ede0e0be9275def825fac81e2f0f2a45e`

7. A new persistent, read-only Codex task (private task ID redacted) rebuilt discovery from user configuration without reading the development repository. Its system-provided catalog returned:

   ```json
   {
     "catalog_skill_path": "$CODEX_HOME/plugins/cache/xuxu-research-preview/research-skills-openai/0.5.0-preview.2/skills/academic-deep-search/SKILL.md",
     "visible_entry_skills": [
       "research-skills-openai:academic-deep-search",
       "research-skills-openai:article-orchestrator",
       "research-skills-openai:perspective-orchestrator",
       "research-skills-openai:proposal-orchestrator",
       "research-skills-openai:research-idea-orchestrator",
       "research-skills-openai:research-opportunity-mapper"
     ],
     "plugin_version": "0.5.0-preview.2",
     "skill_count": 45,
     "pubmed_present": false,
     "discovery_status": "verified"
   }
   ```

## Release-boundary checks

- The manifest and marketplace still label the distribution `Preview`/`Experimental`.
- The marketplace source remains the rolling GitHub `main` branch; no stable tag/SHA channel is claimed.
- `workflow-registry.yaml` keeps `human_signoff_required` as the final state.
- automatic_external_submission: false

This receipt proves the required GitHub marketplace upgrade/reinstall, old-to-new cache replacement, and fresh-task discovery path for Phase 5.
