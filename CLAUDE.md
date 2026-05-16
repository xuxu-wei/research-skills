# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a composable research-workflow skill library. Each skill package contains a `SKILL.md` (entry point, trigger conditions, role boundaries, steps), plus `references/`, `templates/`, and sometimes `scripts/`. The design goal is layered decomposition: isolate generation from evaluation, track artifact lineage, and enforce quality gates between workflow stages.

## Skill ownership

- **Xuxu's skills**: `research-idea/`, `research-proposal/`, `research-article/`, `research-perspective/` (all sub-skills), plus `research/` subdirs `academic-language-assessor`, `medical-journal-review`, `methodology-statistics-preflight`, `research-opportunity-mapper`
- **External dependencies** (not Xuxu's; do not modify casually): `research/` subdirs `academic-deep-search`, `arxiv`, `blogwatcher`, `llm-wiki`, `polymarket`, `pubmed`, plus `data-science/`, `office-toolkit/`, `productivity/`

## Commands

```bash
# Audit all 4 research workflows for cross-package consistency
python scripts/audit_research_workflows.py

# Generate flat skills directory (skills-flatten/) for broad agent compatibility
python generate_flatten_skills.py

# Build Codex plugin (skills-openai-plugin/), install to ~/plugins, register in marketplace + config.toml
python install_codex_plugin.py

# Run the converter with specific mode
python scripts/codex_plugin_converter.py --mode flatten
python scripts/codex_plugin_converter.py --mode codex --install
```

## SKILL.md format

Every SKILL.md has YAML frontmatter with required fields:

```yaml
---
name: skill-name            # hyphenated-lowercase, required
description: "..."          # when-to-use description, required
version: X.Y.Z              # SemVer, required
metadata:
  hermes:
    tags: [...]             # required
    related_skills: [...]   # required for research workflow skills
---
```

Body structure varies by role type (see role types below), but every skill states its purpose and what it does NOT do.

## Architecture: the 4 research workflows

Each workflow follows the same loop: **input normalization → evidence/method preprocessing → generate/draft → independent evaluation → targeted revision → re-evaluation or panel → final assembly**.

### research-idea (7 skills)
`orchestrator → context-builder → opportunity-mapper → multi-path-idea-generator → methodology-preflight → idea-evaluator → adversarial-review-panel → portfolio-assembler`

### research-proposal (11 skills)
`orchestrator → context-brief-builder → opportunity-mapper → readiness-triage → proposal-drafter → proposal-evaluator → refinement-controller → review-panel → package-assembler`, with optional SAP branch (`sap-writer → sap-evaluator → sap-refinement-controller`)

### research-article (14 skills)
`orchestrator → readiness-triage → context-builder → literature-grounder → methods-statistics-auditor → architect → drafter → claim-auditor → evaluator → refinement-controller → review-panel → frontmatter-drafter → cover-letter → submission-compositor`

**Critical naming rule**: All article skills use `article-*` prefix (e.g., `article-drafter`), NOT `research-article-*`. Do not rename them.

Entry modes: `standard`, `fast_track_has_draft`, `fast_track_draft_eval`, `blueprint_only`, `section_specific`, `submission_only`. Fast-track modes cannot skip the minimum backfill gate.

### research-perspective (9 skills)
`orchestrator → input-builder → claim-evidence-curator → argument-architect → drafter → evaluator → refinement-controller → review-panel → final-compositor`

Modes: `Lite` (feasibility only), `Standard` (full draft + one revision round), `Full` (pre-submission with panel + compositor).

## Role types and isolation rules

All skills fall into 6 role types. Isolation is mandatory for evaluation roles:

| Role type | Examples | Must NOT do |
|-----------|----------|-------------|
| Orchestrator | `*-orchestrator` | Substitute for evaluator/reviewer scoring |
| Builder/Curator | context-builder, claim-curator, architect | Generate final scores or conclusions |
| Generator/Drafter | idea-generator, proposal-drafter, article-drafter, sap-writer | Evaluate own output |
| Auditor/Evaluator/Triage | readiness-triage, methods-auditor, claim-auditor, `*-evaluator` | Draft, rewrite, or lower standards |
| Review Panel | `*-review-panel`, adversarial-panel | Share output between reviewers; fabricate consensus |
| Assembler/Compositor | portfolio-assembler, package-assembler, submission-compositor | Clean up unresolved issues or hide dissent |

When modifying or creating skills, the audit script enforces these boundaries. Run `python scripts/audit_research_workflows.py` after changes.

## Build system

`scripts/codex_plugin_converter.py` is the core engine (730 lines). Key constants:

- `CORE_PACKAGES`: `["research-idea", "research-proposal", "research-perspective"]` — **note: research-article is missing from this list** (known blind spot; article skills still get included via dependency resolution but are not explicitly enumerated)
- `RESEARCH_DEPENDENCIES`: 8 named skills under `research-skills/research/`
- Source discovery walks `SKILL.md` files; duplicate skill names across packages raise errors
- Custom YAML frontmatter parser — no PyYAML dependency

Output targets:
- `skills-flatten/` — flat directory, one skill per subdir, for broad agent compatibility
- `skills-openai-plugin/` — recursive package layout, installed as a Codex plugin

## Artifact governance

All workflow artifacts must carry lineage fields: `source_skill`, `based_on`, `change_type`, artifact ID, version ID (`vNNN`), round ID (`rNNN`). Substantive changes require revision deltas and response files. Assemblers only aggregate — they do not rewrite or hide unresolved issues.

## Panel tiers

| Tier | Reviewers | Use case |
|------|-----------|----------|
| `lightweight` | 3 | Quick pre-review, early mock review |
| `standard` | 5 | Default for normal proposals/articles |
| `full` | 7 | High-stakes, near-submission |

For medical/clinical proposals, `practicing-clinician reviewer` serves as domain expert by default. `submission-guard reviewer` must always be present; `skeptical reviewer` is enabled by default.

## Stop rules

Workflows must stop (not paper over) when: readiness triage blocks, evaluator finds an unfixable fatal flaw, revision requires inventing endpoints/sample sizes/data/statistical models that don't exist, multiple revision rounds show no gain, or the latest version lacks independent evaluation.
