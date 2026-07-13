# Phase 6 Codex Catalog and Context Measurement

Date: 2026-07-13
Surface: source policy and historical Codex desktop observations
ChatGPT web: not tested; no inference is made about its discovery or loading
Status: Complete

## Result

The maintained `0.7.0-preview.1` source contains 49 skill contracts. Registry
policy declares seven public entries; six are implicit-active, while Research
Polisher is explicit-only until the Phase 7-8 external gate passes:

- `academic-deep-search`
- `article-orchestrator`
- `perspective-orchestrator`
- `proposal-orchestrator`
- `research-idea-orchestrator`
- `research-opportunity-mapper`
- `research-polisher-orchestrator`

The only completed Codex catalog observation remains the historical installed
`0.5.0-preview.1` cache, which exposed the six public entries that existed then
and zero private roles. The retained routing snapshot is bound to
`0.6.0-preview.1` and six entries. Neither observation proves that the new
`0.7.0-preview.1` seventh entry has been installed or discovered. Current
marketplace install, fresh-task discovery, and routing receipts remain Phase 7
gates.

## Character proxies

The proxy counts Unicode characters from UTF-8 source. It uses all 49
descriptions even though runtime discovery is pending. Each orchestrator proxy
adds its complete `SKILL.md`, including frontmatter, to the description total.

| Measurement | Result | Limit |
| --- | ---: | ---: |
| Observed public-entry descriptions | 956 | Informational |
| All 49 descriptions | 6,086 | 6,200 |
| Article orchestrator proxy | 13,146 | 13,400 |
| Perspective orchestrator proxy | 12,785 | 13,400 |
| Proposal orchestrator proxy | 13,266 | 13,400 |
| Research-idea orchestrator proxy | 13,088 | 13,400 |
| Research-polisher orchestrator proxy | 12,295 | 13,400 |

The stricter Phase 9 limits pass with 114 description characters and 134
maximum-orchestrator-proxy characters of conservative headroom.

## Reproducible checks

Run:

```powershell
python scripts/test_openai_phase6_context.py
python scripts/audit_openai_research_plugin.py
```

The test derives inventory, entry policy, and orchestrators from
`workflow-registry.yaml`. It validates registry/source agreement, all 49 UI
policies and 25-64-character short descriptions, both context limits, and one
copy-paste quickstart per current public entry.

## Routing snapshot boundary

`tests/openai_phase6/quickstart-routing-receipts.yaml` preserves six isolated
`0.6.0-preview.1` routing observations and their original SHA-256 bindings. They
are historical evidence and are not rewritten to match current source files or
the seventh entry. The current static quickstart set is 7/7; current-version
fresh-subagent routing evidence is 0/7 pending a real rerun.

## Interpretation and limits

- Source package: 49 skills; policy declares seven public entries, six currently implicit-active.
- Runtime catalog observation for `0.7.0-preview.1`: pending.
- Non-implicit source skills: 43 (one gated public entry plus 42 private roles); no claim is made that they load initially.
- This is character-based headroom, not model-token accounting.
- Source presence, hashes, or a repository-authored routing snapshot cannot
  substitute for marketplace installation and fresh-task discovery.
- ChatGPT web installation, sharing, discovery, and runtime remain unverified
  until Phase 12 evidence exists.
