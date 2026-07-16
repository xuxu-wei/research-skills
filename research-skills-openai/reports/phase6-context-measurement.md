# Phase 6 Codex Catalog and Context Measurement

Date: 2026-07-17
Surface: source policy and Codex desktop installation observations
ChatGPT web: not tested; no inference is made about its discovery or loading
Status: Complete

## Result

The maintained `0.9.0-preview.2` source contains 49 skill contracts. Registry
policy declares seven discoverable entries; six are implicit-active, while
Research Polisher is permanently explicit-only under the personal routing
policy:

- `academic-deep-search`
- `article-orchestrator`
- `perspective-orchestrator`
- `proposal-orchestrator`
- `research-idea-orchestrator`
- `research-opportunity-mapper`
- `research-polisher-orchestrator`

A prior current-environment diagnostic confirmed that marketplace
`xuxu-research-preview` is registered and that enabled-plugin discovery works
in Codex App and a fresh Codex CLI task. The `0.9.0-preview.2` cache refresh and
formal `personal-distribution-current` observation remain pending until their
task/source identity, artifact digests, timestamps, outcome, and owner
confirmation are captured. The retained historical routing snapshot remains
bound to `0.6.0-preview.1` and six entries.

## Character proxies

The proxy counts Unicode characters from UTF-8 source. It uses all 49
descriptions even though runtime discovery is pending. Each orchestrator proxy
adds its complete `SKILL.md`, including frontmatter, to the description total.

| Measurement | Result | Limit |
| --- | ---: | ---: |
| Declared-entry descriptions | 956 | Informational |
| All 49 descriptions | 6,029 | 6,200 |
| Article orchestrator proxy | 12,833 | 13,400 |
| Perspective orchestrator proxy | 12,728 | 13,400 |
| Proposal orchestrator proxy | 13,146 | 13,400 |
| Research-idea orchestrator proxy | 12,937 | 13,400 |
| Research-polisher orchestrator proxy | 12,195 | 13,400 |

The regression limits pass with 171 description characters and 254
maximum-orchestrator-proxy characters of conservative headroom. The 14 touched
skill bodies total 68,852 characters against the 73,043 baseline.

## Reproducible checks

Run:

```powershell
python scripts/test_openai_phase6_context.py
python scripts/audit_openai_research_plugin.py
```

The test derives inventory, entry policy, and orchestrators from
`workflow-registry.yaml`. It validates registry/source agreement, all 49 UI
policies and 25-64-character short descriptions, both context limits, and one
copy-paste quickstart per current declared entry.

## Routing snapshot boundary

`tests/openai_phase6/quickstart-routing-receipts.yaml` preserves six isolated
`0.6.0-preview.1` routing observations and their original SHA-256 bindings. They
are historical evidence and are not rewritten to match current source files or
the seventh entry. The current static quickstart set is 7/7. The current App/CLI
diagnostic is recorded separately from this retained snapshot and does not
replace the still-pending formal distribution receipt.

## Interpretation and limits

- Source package: 49 skills; policy declares seven entries, six currently implicit-active.
- Runtime catalog loading for `0.9.0-preview.2`: refresh and formal owner-observed binding pending in Phase 7.
- Non-implicit source skills: 43 (the explicit-only Research Polisher entry plus 42 private roles); no claim is made that they load initially.
- This is character-based headroom, not model-token accounting.
- Source presence, hashes, or a repository-authored routing snapshot cannot
  substitute for marketplace installation and fresh-task discovery.
- ChatGPT web installation, sharing, discovery, and runtime remain unverified
  and do not block the personal Codex profile.
