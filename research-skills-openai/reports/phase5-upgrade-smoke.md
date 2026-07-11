# Phase 5 GitHub Upgrade Smoke

Status: upgrade_verified  
Verification date: 2026-07-12 (Asia/Singapore)  
Marketplace: `xuxu-research-preview`  
Plugin: `research-skills-openai`

## Acceptance chain

1. The previously installed GitHub-marketplace cache was frozen as the baseline:
   - version: `0.1.0`
   - cache: `C:\Users\10149\.codex\plugins\cache\xuxu-research-preview\research-skills-openai\0.1.0`
   - discovered skill directories: `46`
   - `skills/pubmed` present: `true`
   - manifest SHA-256: `62828a41cdde50abe4aabea442f70f1b19c2dac929fbe6027cfa18e5634d092e`
2. GitHub `main` was updated to commit `b3707e71e444b2f26dbd18abbf7ad7eb6cacf12f`, whose plugin manifest declares `0.5.0-preview.1`.
3. GitHub Actions run `29165879809` (`OpenAI Plugin Preview`) completed with conclusion `success` for that commit:
   - <https://github.com/xuxu-wei/research-skills/actions/runs/29165879809>
4. The App-bundled Codex CLI `0.144.0-alpha.4` registered the GitHub marketplace from `xuxu-wei/research-skills@main` and returned:

   ```json
   {
     "marketplaceName": "xuxu-research-preview",
     "installedRoot": "C:\\Users\\10149\\.codex\\.tmp\\marketplaces\\xuxu-research-preview",
     "alreadyAdded": false
   }
   ```

   The installed marketplace snapshot had `refs/heads/main` at `b3707e71e444b2f26dbd18abbf7ad7eb6cacf12f` and origin `https://github.com/xuxu-wei/research-skills.git`.

5. Reinstalling `research-skills-openai@xuxu-research-preview` from that snapshot returned:

   ```json
   {
     "version": "0.5.0-preview.1",
     "installedPath": "C:\\Users\\10149\\.codex\\plugins\\cache\\xuxu-research-preview\\research-skills-openai\\0.5.0-preview.1"
   }
   ```

   A subsequent `plugin marketplace upgrade xuxu-research-preview --json` completed with `errors: []`; because the snapshot already matched `main`, `upgradedRoots` was empty.

6. Direct cache inspection confirmed:
   - manifest version: `0.5.0-preview.1`
   - registry plugin version: `0.5.0-preview.1`
   - registry schema version: `4`
   - discovered skill directories: `45`
   - `skills/pubmed` present: `false`
   - old `0.1.0` cache removed by reinstall
7. A new Codex App task (`019f52be-dcce-7e81-a1c3-6dcf0c4abd10`) read the new cache and reported version `0.5.0-preview.1`, 45 skills, and no `pubmed`. It also reported that the already-running App process first supplied a stale catalog locator, so this task is retained as diagnostic evidence rather than the sole discovery proof.
8. A separate fresh, read-only, ephemeral Codex process (`019f52c2-7705-7921-8a08-6fbb2d049d79`) rebuilt discovery from user configuration. Its catalog directly supplied:

   ```json
   {
     "catalog_skill_path": "C:\\Users\\10149\\.codex\\plugins\\cache\\xuxu-research-preview\\research-skills-openai\\0.5.0-preview.1\\skills\\research-idea-orchestrator\\SKILL.md",
     "plugin_version": "0.5.0-preview.1",
     "registry_version": 4,
     "skill_count": 45,
     "pubmed_present": false,
     "discovery_status": "verified"
   }
   ```

## Release-boundary checks

- The manifest and marketplace still label the distribution `Preview`/`Experimental`.
- The marketplace source remains the rolling GitHub `main` branch; no stable tag/SHA channel is claimed.
- `workflow-registry.yaml` keeps `human_signoff_required` as the final state.
- `automatic_external_submission` remains `false`.

This receipt proves the required GitHub marketplace installation, old-to-new cache replacement, and fresh-process discovery path for Phase 5.
