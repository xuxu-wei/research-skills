# Phase 7-8 Personal Acceptance Runbook

Status: active personal-owner procedure

Plugin: `research-skills-openai`

Maintained source version: `0.8.0-preview.1`

This runbook validates the plugin for one owner's research work. It does not
create a public-release, external-attestation, or provider-verification claim.

## 1. Acceptance states

| State | Meaning |
|---|---|
| `deterministic_validated` | Repository audits, fixtures, context budgets, registry, and package checks pass. |
| `owner_observed` | One real task is bound to the current plugin, task, artifacts, digests, timestamps, and owner confirmation. |
| `in_progress_owner_observation` | Deterministic validation passes, but at least one required real observation is missing. |
| `owner_observed_ready` | Every required distribution, workflow, control, Search, and Deep Research slot passes. |

An owner observation is personal evidence only. Do not rename it as external
attestation or provider verification.

## 2. Current installation finding

The GitHub installation mechanism is already implemented and the owner's Codex
configuration currently contains:

- marketplace `xuxu-research-preview`;
- source `https://github.com/xuxu-wei/research-skills.git`, ref `main`;
- plugin `research-skills-openai@xuxu-research-preview`, enabled; and
- installed cache last observed as `0.7.0-preview.2`.

The maintained source is `0.8.0-preview.1`, but that version has not yet been
owner-observed after marketplace upgrade/reinstall. The older cache does not
validate the current source; run the upgrade after this version is pushed.

## 3. Deterministic preflight

Run from the repository root:

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

Required deterministic baseline:

- 49 skills, 20 independent reviewers, 68 workflow edges;
- seven declared entries and six implicit entries;
- Research Polisher fixed to explicit-only personal routing;
- five workflows and 17/17 entry modes;
- Phase 4: 5/5 workflows and 63 negative guards;
- Phase 8: 20/20 cases, false-ready zero, and all maintained quality metrics at 100%; and
- zero plugin-audit errors or warnings.

## 4. Install or update from GitHub

Perform this only after the intended SemVer and source changes are committed and
pushed to `main`:

```powershell
codex plugin marketplace upgrade xuxu-research-preview
codex plugin add research-skills-openai@xuxu-research-preview
```

If `codex` is not on `PATH`, read `CODEX_CLI_PATH` from
`$HOME\.codex\config.toml` and invoke that App-managed executable. Do not
hard-code its build-specific path in repository instructions.

After reinstall:

1. restart the Codex App if it still reports the previous cache;
2. open a new task;
3. record the marketplace revision, installed cache path, manifest version, and
   registry digest; and
4. confirm 49 skills, seven declared entries, six implicit entries, and no
   standalone `pubmed` skill.

The distribution slot passes only when the new task uses one coherent current-
version cache. A repository checkout or old task does not count.

## 5. Owner-observed receipt rules

Use
`../tests/openai_personal/current-version-owner-observed-receipts.yaml` as the
current collection. Each completed slot must change from
`pending_owner_observation` to `owner_observed` and record:

- task ID and plugin version;
- source commit or equivalent source identity;
- artifact ID, path, version, and SHA-256 digest;
- start and completion timestamps;
- reviewer instance IDs where a reviewer ran;
- opened source URLs for Search;
- actual outcome matching the slot contract; and
- explicit owner confirmation.

Do not mark a receipt observed from a prompt, fixture, screenshot, filename, or
repository-authored status alone.

## 6. Phase 7 workflow slots

Run one current-version happy path for each workflow:

| Slot | Expected outcome |
|---|---|
| Idea | `human_signoff_required` |
| Proposal | `human_signoff_required` |
| Article | `human_signoff_required` |
| Perspective | `human_signoff_required` |
| Research Polisher | `human_strategy_selection_required` |

For each accepted happy path:

- the generator/drafter and every reviewer have different instance IDs;
- reviewers read frozen inputs and write only review or verification reports;
- substantive revisions create a new artifact version;
- the final evaluator reviews the current version;
- unresolved findings and dissent remain visible; and
- no external submission occurs.

Run two controls:

| Control | Expected outcome |
|---|---|
| Fresh reviewer/delegation unavailable | `independent_review_pending` plus a self-contained continuation brief |
| Fatal or unresolved blocking finding | `blocked_without_ready_state` |

Any inline self-review, source edit by a reviewer, hidden dissent, stale
evaluation, or false-ready result fails Phase 7.

## 7. Research Polisher routing boundary

Research Polisher is permanently explicit-only for this personal profile. Test
one positive explicit invocation and confirm it does not take over:

- language or grammar polishing;
- ordinary article drafting;
- generation of a new research idea; or
- general literature retrieval.

There is no automatic future activation step. Changing this policy requires a
new owner decision and a new routing review.

## 8. Phase 8 retrieval slots

Run three built-in Search tasks:

| Slot | Purpose |
|---|---|
| `personal-search-current` | A recently changed fact or current source question |
| `personal-search-exact` | One exact fact, document, or identifier lookup |
| `personal-search-narrow-academic` | One narrow academic question with source-grounded synthesis |

For each Search task, retain the query purpose, opened URLs or stable source
identifiers, material claim mappings, output artifact, version, digest, task
ID, timestamps, and owner confirmation.

Run one inactive Deep Research control:

- Deep Research is unavailable or inactive;
- the workflow does not simulate it inline;
- it emits a self-contained continuation package; and
- it stops at `deep_research_handoff_required`.

Run one complete user-started Deep Research cycle:

```text
handoff
  -> user starts Deep Research
  -> Deep Research completes
  -> research-opportunity-mapper returns a bound evidence artifact
  -> the original workflow resumes exactly one pending edge
```

Mapper return and resume must bind the same evidence artifact paths and digests.

## 9. Derive personal readiness

Regenerate and check the report:

```powershell
python scripts/validate_openai_personal_readiness.py --write-report
python scripts/validate_openai_personal_readiness.py --check-report
```

Pending observations are valid while work remains. To assert final personal
readiness, run:

```powershell
python scripts/validate_openai_personal_readiness.py --require-ready
```

`--require-ready` must fail until the distribution slot, five workflow slots,
two controls, three Search slots, inactive Deep Research slot, and complete
Deep Research slot are all owner-observed.

## 10. Stop and escalation rules

Stop rather than promote when:

- the installed cache differs from the intended source version;
- a reviewer cannot run independently;
- a source artifact changes during review;
- a fatal or unresolved blocking finding exists;
- the evaluated version is stale;
- required dissent or lineage is missing; or
- a Deep Research return cannot be bound to the pending workflow edge.

The retained public-release evidence machinery is outside this active runbook.
Its historical operator reference is
[PREVIEW-EVIDENCE-CAPTURE.md](PREVIEW-EVIDENCE-CAPTURE.md); it does not block the
personal-owner profile.
