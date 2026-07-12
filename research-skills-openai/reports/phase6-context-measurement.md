# Phase 6 Codex Catalog and Context Measurement

Date: 2026-07-12
Surface: Codex desktop task
ChatGPT web: not tested; no inference is made about its discovery or loading
Status: Complete

## Result

The maintained source package still contains 45 skill contracts. Registry and
`agents/openai.yaml` policy expose exactly six as implicit public entries and
keep the other 39 explicit-or-orchestrated. In this Codex task, the
system-supplied initial plugin catalog contained only these six entries:

- `academic-deep-search`
- `article-orchestrator`
- `perspective-orchestrator`
- `proposal-orchestrator`
- `research-idea-orchestrator`
- `research-opportunity-mapper`

No other `research-skills-openai` role appeared in the initial skill catalog.
This proves the catalog boundary observed in this task; it does not expose
private platform token accounting. Skill bodies remain conditional content
read after selection, so this report does not claim that all six bodies were
loaded at startup.

The catalog entries in this already-running task pointed to the installed
`0.5.0-preview.1` user cache. The source candidate under test is
`0.6.0-preview.1`; its registry and all 45 `agents/openai.yaml` policies match
the same six/39 boundary, and its six routing smokes read the source candidate
directly. This observation therefore measures Codex catalog filtering, not a
current-candidate install/discovery receipt. Current-version marketplace and
fresh-task discovery remain Phase 7 gates.

## Character proxies

The proxy counts Unicode characters as read from UTF-8 source. It deliberately
uses all 45 descriptions for the conservative bound even though the observed
Codex catalog exposed only six. For an orchestrator, it adds the complete
`SKILL.md` file, including frontmatter, to that all-description total. This is
more conservative than counting the body alone.

| Measurement | Result | Limit |
| --- | ---: | ---: |
| Observed public-entry descriptions | 944 | Informational |
| All 45 descriptions | 5,882 | 6,400 |
| Article orchestrator proxy | 13,873 | 14,000 |
| Perspective orchestrator proxy | 13,683 | 14,000 |
| Proposal orchestrator proxy | 13,083 | 14,000 |
| Research-idea orchestrator proxy | 13,879 | 14,000 |

The previous Roadmap proxy was 7,710 description characters and 15,704 for the
largest description-plus-orchestrator total. The compact descriptions preserve
the same skill names, roles, implicit-entry set, and skill bodies.

## Reproducible checks

Run:

```powershell
python scripts/test_openai_phase6_context.py
python scripts/audit_openai_research_plugin.py
```

The Phase 6 test derives the skill inventory and public entries from
`workflow-registry.yaml`; it does not hard-code the current plugin version or
the 45-skill count. It verifies registry/source agreement, every
`allow_implicit_invocation` value, both context limits, and one isolated
copy-paste quickstart per public entry. Each quickstart explicitly invokes only
its own public skill. Every routing snapshot now binds both its instantiated
prompt and the current README quickstart template plus the selected source
`SKILL.md` by SHA-256, so source or documentation drift invalidates the receipt.

## Fresh-subagent routing smoke

Six synthetic quickstart prompts were dispatched sequentially to six fresh
subagent instances. Every run selected the requested public entry, judged the
minimum filled input sufficient for routing, read exactly that entry's
`SKILL.md`, read no unrelated public-entry skill, and performed no source edit.
The run contracts and canonical instance IDs are recorded in
`tests/openai_phase6/quickstart-routing-receipts.yaml` and validated by
`scripts/test_openai_phase6_context.py`. These are current-task structured
observations, not a portable platform execution export; current-version
installed discovery remains a Phase 7 gate.

## Interpretation and limits

- Source package: 45 skills.
- Initial Codex plugin catalog observed in this task: six public-entry
  descriptions.
- Non-implicit roles observed in the initial catalog: zero; they remain
  available through explicit or orchestrated invocation.
- This is character-based headroom, not model-token accounting.
- A future Codex build or plugin policy change requires a fresh-task catalog
  observation; the static policy test alone cannot prove runtime exposure.
- ChatGPT web installation, sharing, discovery, and runtime remain explicitly
  unverified until Phase 11 evidence exists.
