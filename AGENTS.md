# AGENTS.md

This repository is a composable research-workflow skill library. Each skill is a self-contained directory with `SKILL.md` as entry point, plus optional `references/`, `templates/`, and `scripts/`.

## Skill specification compliance

Skills follow the [Agent Skills spec](https://agentskills.io/specification). Apply the profile rules below; do not mix Hermes metadata into the OpenAI plugin skills.

### Required frontmatter (per spec)

```yaml
---
name: skill-name           # max 64 chars, lowercase + hyphens, must match parent dir
description: "..."         # max 1024 chars, describes what AND when to use
---
```

### Hermes extensions (under `metadata.hermes`)

This extension applies only to skills under `research-skills/`.

```yaml
metadata:
  hermes:
    version: X.Y.Z         # SemVer, required for all Hermes skills
    tags: [...]            # required
    related_skills: [...]  # required for workflow skills; must resolve to installed skill names
```

### OpenAI plugin profile

Skills under `research-skills-openai/skills/` keep only `name` and `description` in SKILL.md frontmatter. Store ChatGPT/Codex UI metadata and invocation policy in `agents/openai.yaml`. Store role, dependency, and independent-review requirements in `research-skills-openai/workflow-registry.yaml`. Do not add `metadata.hermes` to the OpenAI plugin profile.

### Body structure

State the skill's purpose and what it does NOT do. For workflow skills, follow the role-type template below. Keep `SKILL.md` under 500 lines; move detailed reference material to `references/`.

## Creating and modifying skills

When creating a new skill or substantially rewriting an existing one, invoke the `skill-creator` skill first. It guides the full cycle: capture intent -> research -> draft -> test with evals -> iterate -> package.

## Skill design principles

- **Single responsibility**: one skill does one thing. Split when a skill accumulates unrelated responsibilities.
- **Isolation**: generators never evaluate their own output; evaluators never draft or rewrite. Use separate subagent context for evaluation roles.
- **Progressive disclosure**: metadata -> body -> references. The agent loads only what it needs.
- **Artifact lineage**: every workflow artifact tracks `source_skill`, `based_on`, `change_type`, artifact ID, version ID, round ID. Assemblers aggregate; they do not rewrite or hide dissent.

## Version management

- Bump major: behavioral contract change (removed step, changed handoff protocol).
- Bump minor: new section, new reference file, expanded guidance.
- Bump patch: clarifications, typo fixes, wording improvements with no behavioral change.
- Update `metadata.hermes.version` in Hermes SKILL.md files before committing changes.
- Version the OpenAI distribution as one plugin through `research-skills-openai/.codex-plugin/plugin.json`; keep `workflow-registry.yaml` on the same plugin version.

## Package structure and ownership

A **package** is a directory under `research-skills/` containing related skills that share a workflow.

**Xuxu's packages** (modify freely): `research-idea/`, `research-proposal/`, `research-article/`, `research-perspective/`, plus `research/` subdirs `academic-language-assessor`, `medical-journal-review`, `methodology-statistics-preflight`, `research-opportunity-mapper`.

**External dependencies** (do not modify casually): `research/` subdirs `academic-deep-search`, `arxiv`, `blogwatcher`, `llm-wiki`, `polymarket`, `pubmed`; plus `data-science/`, `office-toolkit/`, `productivity/`.

## Reference integrity

- Every entry in `metadata.hermes.related_skills` must resolve to an installed skill name (enforced by audit).
- Every backtick-quoted `.md` reference in `SKILL.md` (e.g., `` `references/foo.md` ``) must point to an existing file.
- Cross-package skill references use the skill name, not the filesystem path.

## Workflow architecture

Four research workflows share a common loop: **input normalization -> evidence/method preprocessing -> generate/draft -> independent evaluation -> targeted revision -> re-evaluation or panel -> final assembly**.

| Workflow | Skills | Entry point |
|----------|--------|-------------|
| research-idea | 7 | `research-idea-orchestrator` |
| research-proposal | 11 (+ 3 SAP) | `proposal-orchestrator` |
| research-article | 14 | `article-orchestrator` |
| research-perspective | 9 | `perspective-orchestrator` |

**Naming rule**: article skills use `article-*` prefix, not `research-article-*`. Do not rename.

## Role types and isolation

| Role | Must NOT do |
|------|-------------|
| Orchestrator | Substitute for evaluator/reviewer scoring |
| Builder/Curator | Generate final scores or conclusions |
| Generator/Drafter | Evaluate own output |
| Auditor/Evaluator/Triage | Draft, rewrite, or lower standards |
| Review Panel | Share output between reviewers; fabricate consensus |
| Assembler/Compositor | Clean up unresolved issues or hide dissent |

Evaluation roles must include explicit isolation language in their SKILL.md (e.g., "use isolated subagent", "do not evaluate own output"). In the OpenAI plugin, every registry entry with `requires_independent_subagent: true` must contain the standardized `Independent Execution Contract`, disable implicit invocation, operate on frozen read-only artifacts, and stop with `independent_review_pending` rather than reviewing inline when delegation is unavailable.

## Stop rules

Workflows must stop, not paper over, when: readiness triage blocks, evaluator finds an unfixable fatal flaw, revision would require inventing data or models that don't exist, multiple rounds show no gain, or the latest version lacks independent evaluation.

## Validation

```bash
python scripts/audit_research_workflows.py
python scripts/audit_openai_research_plugin.py
python scripts/codex_plugin_converter.py --mode flatten
python scripts/codex_plugin_converter.py --mode codex --install
```

Run the audit after creating or modifying any skill. Fix all errors before committing.
