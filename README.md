# Research Skills

Composable research-workflow skills for turning research questions, evidence, ideas, proposals, study artifacts, and drafts into reviewable deliverables.

## Repository profiles

This repository maintains two related but distinct distributions:

- `research-skills/`: Hermes-oriented source skills. These retain Hermes metadata and per-skill versions.
- `research-skills-openai/`: a personal Experimental/Preview plugin optimized for ChatGPT Work and Codex. It uses plugin-level versioning, `agents/openai.yaml`, and `workflow-registry.yaml`.

Do not treat one profile as generated output of the other. Shared concepts may be ported deliberately, but each profile owns its platform-specific instructions and validation rules.

## Workflow families

Four workflow families use the same production loop:

```text
normalize input
  -> retrieve evidence / check methods
  -> generate or draft
  -> independent evaluation
  -> targeted revision
  -> fresh re-evaluation or independent panel
  -> final human-review package
```

| Workflow | Entry point | Primary deliverable |
| --- | --- | --- |
| Research idea | `research-idea-orchestrator` | Research Idea Portfolio |
| Proposal | `proposal-orchestrator` | Proposal, optional SAP, final package |
| Article | `article-orchestrator` | Manuscript and submission-review package |
| Perspective | `perspective-orchestrator` | Perspective/Viewpoint/Commentary package |

Common research services include evidence and opportunity mapping, focused academic search, methodology/statistics preflight, academic-language assessment, and medical-journal review.

## Design model

- Orchestrators route work and maintain state; they do not replace evaluators.
- Builders, generators, and drafters create artifacts; they do not score their own work.
- Reviewer roles run in fresh independent subagents or delegated threads against frozen inputs.
- Controllers translate findings into bounded revision plans.
- Assemblers and compositors package existing artifacts without hiding unresolved issues or dissent.
- Every artifact records lineage, including source skill, artifact/version/round identity, basis, and change type.
- Final workflow states stop at human review and sign-off; the repository does not automate external submission.

## Repository layout

```text
research-skills/                  Hermes profile
research-skills-openai/           ChatGPT/Codex plugin profile
  .codex-plugin/plugin.json
  skills/
  workflow-registry.yaml
  AGENTS.md
  ROADMAP.md
scripts/                          audits, converters, and registry helpers
.agents/plugins/marketplace.json  repository plugin marketplace
```

## Ownership and third-party material

The research idea, proposal, article, and perspective workflow packages and their shared reviewer/mapping skills are maintained in this repository. Other utility packages may be external dependencies and should not be modified casually.

`research-skills/obsidian-skills/` contains skills derived from [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills), authored by Steph Ango and licensed under MIT. See `research-skills/obsidian-skills/NOTICE.md`.

## Validation

Run the checks relevant to the profile being changed:

```powershell
python scripts/audit_research_workflows.py
python scripts/audit_openai_research_plugin.py
python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid
```

For plugin installation and GitHub update instructions, see `research-skills-openai/README.md`.
