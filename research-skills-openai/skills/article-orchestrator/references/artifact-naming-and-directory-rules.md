# Artifact Naming and Directory Rules

## Contents

<!-- toc:start -->
- [Project Directory Layout](#project-directory-layout)
- [Directory Rules](#directory-rules)
- [Cross-Package Version Fields](#cross-package-version-fields)
- [File Naming Conventions](#file-naming-conventions)
  - [Manuscript Drafts](#manuscript-drafts)
  - [Supplementary Materials](#supplementary-materials)
  - [Evaluation Reports](#evaluation-reports)
  - [Revision Records](#revision-records)
  - [Language Assessment Reports](#language-assessment-reports)
  - [Panel Reports](#panel-reports)
  - [Frontmatter](#frontmatter)
  - [Cover Letter](#cover-letter)
  - [Package](#package)
- [Version Rules](#version-rules)
  - [When to Create a New Version](#when-to-create-a-new-version)
  - [Clean Version Rules](#clean-version-rules)
  - [Overwrite Prohibition](#overwrite-prohibition)
- [Artifact Index](#artifact-index)
- [Cross-Skill Loading](#cross-skill-loading)
<!-- toc:end -->

## Project Directory Layout

```
<workspace>/research-article-projects/<project-slug>/
  00_input/                             # User's raw materials
  01_readiness/                         # Readiness Triage Report
  02_context/                           # Article Context Brief
  03_literature/                        # Literature Grounding Report
  04_blueprint/                         # Blueprint + EDP/EPL + display-asset-manifest.yaml
  05_audit/                             # Methods & Statistics Audit Report
  06_drafts/                            # canonical manuscript-vNNN.md + synchronized user-facing DOCX
  07_claim-audit/                       # Claim Audit Reports
  08_evaluations/                       # Evaluation Reports
  09_revisions/                         # Revision rounds
    round-001/
    round-002/
  10_panel/                             # Panel Report + reviewer briefs
  11_frontmatter/                       # Abstract, Key Points, Title, Highlights
  11_cover-letter/                      # Cover letter and cover-letter-only reviews
  12_package/                           # Verified DOCX and human-review package
  13_state/                             # workflow-state.yaml, artifact-index.md
  14_delegates/                         # Isolated subagent briefs (audit trail)
```

## Directory Rules

- Two-digit prefix (`00_`–`14_`) ensures filesystem ordering matches workflow sequence.
- Directory numbers correspond to the step where that artifact type first appears.
- Do not skip numbers even if a step is skipped in a given entry mode.
- `13_state/` is always last among numbered directories.
- `14_delegates/` stores subagent input/output packages for auditability.
- Manuscript drafts live only in `06_drafts/`; reviewer responses, revision plans, revision deltas, and language change logs live only in `09_revisions/round-NNN/`; submission package files live only in `12_package/`.

## Cross-Package Version Fields

Every artifact registered in `13_state/artifact-index.md` should include the shared lineage fields used across research-idea, research-proposal, and research-perspective workflows where applicable:

```text
current_artifact_path
artifact_id
version_id
workflow_id
round_id
plugin_version
revision_round
based_on
change_type
status
source_skill
created_by_instance_id
content_digest
frozen
```

## File Naming Conventions

### Manuscript Drafts

```
06_drafts/manuscript-v001.md
06_drafts/manuscript-v002.md
06_drafts/manuscript-v003.md
06_drafts/manuscript-v003.docx
```

### Supplementary Materials

```
06_drafts/supplementary-v001.md
06_drafts/supplementary-v002.md
```

Supplementary version numbers always match manuscript version numbers.

### Evaluation Reports

```
08_evaluations/evaluation-v001.md
08_evaluations/evaluation-v002.md
```

Evaluation artifact IDs use `eval-001`, `eval-002`, ... and each report records
the evaluated manuscript version in `draft_ref` and `draft_version`.

### Revision Records

```
09_revisions/round-001/revision-plan-r001.md
09_revisions/round-001/response-to-reviewers-r001.md
09_revisions/round-001/revision-delta-r001.md
09_revisions/round-001/language-change-log-r001.md
```

Use `response-to-reviewers-rNNN.md` everywhere. Do not use a singular response filename.

### Language Assessment Reports

```
08_evaluations/language-assessment-v001.md
08_evaluations/language-assessment-v002.md
```

Run `academic-language-assessor` for English, Chinese, or bilingual manuscript text during evaluation and after any language polishing pass. If a changed manuscript is saved after language polishing, create the next manuscript version and record `change_type: language_only`.

### Panel Reports

```
10_panel/panel-report-v001.md
10_panel/reviewer-briefs/
```

### Frontmatter

```
11_frontmatter/abstract.md
11_frontmatter/key-points.md
11_frontmatter/title-options.md
11_frontmatter/running-title.md
11_frontmatter/highlights.md
```

### Cover Letter

```
11_cover-letter/cover-letter-v001.md
11_cover-letter/cover-letter-quality-check-v001.md
11_cover-letter/medical-journal-cover-letter-review-v001.md
```

### Package

```
12_package/submission-package.md
12_package/manuscript-vNNN.docx
12_package/docx-parity-and-render-report.md
12_package/reporting-checklist-mapping.md
12_package/reviewer-risk-matrix.md
12_package/human-signoff-checklist.md
12_package/submission-readiness-summary.md
```

## Version Rules

### When to Create a New Version

| Change Type | New Version? |
|-------------|-------------|
| Substantive content change (claims, evidence, analysis) | Yes |
| Structural reorganization (section reorder) | Yes |
| Language polishing only | Yes if a changed draft is saved; mark `change_type: language_only` |
| Formatting adjustments only | Yes if a changed draft is saved; mark `change_type: formatting_only` |
| Reporting checklist item additions | No |
| Final clean version for submission | Yes (`-clean` suffix) |

### Clean Version Rules

- `manuscript-v003-clean.md` may be created ONLY after `manuscript-v003.md` exists and is recorded in workflow state.
- The clean version strips internal annotations, version markers, and drafting notes.
- The source version (`manuscript-v003.md`) must not be deleted.

### Overwrite Prohibition

- Prior manuscript versions must **never** be overwritten or deleted.
- A DOCX is derived from the same-version canonical Markdown. It never replaces the current Markdown pointer or authorizes source edits.
- `13_state/workflow-state.yaml` is the single authoritative pointer to the current version.
- When a new version is created, the previous version's path is recorded in revision history.

## Artifact Index

`13_state/artifact-index.md` is a human-readable Markdown table:

```markdown
# Artifact Index — {{project_slug}}

| Artifact ID | Role | Version | Path | Source Skill | Created Step | Status |
|------------|------|---------|------|-------------|-------------|--------|
| readiness-001 | Readiness Report | v1 | 01_readiness/readiness-report.md | article-readiness-triage | 1 | final |
| context-001 | Context Brief | v1 | 02_context/context-brief.md | article-context-builder | 2 | final |
| ... | ... | ... | ... | ... | ... | ... |
```

One row per artifact. Status: `final`, `draft`, `superseded`, `blocked`, `missing`.

## Cross-Skill Loading

Other article skills read this file and the sibling orchestrator references directly by path. When an independent subagent cannot access those paths, include the relevant frozen excerpts in its brief.
