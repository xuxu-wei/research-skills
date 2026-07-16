# Exploration Strategy Rules

Use this file after choosing the retrieval surface. The strategy controls search
shape; it never changes the Search/Deep Research boundary in `SKILL.md` and
`search-routing-rules.md`.

## Choose one `retrieval_mode`

| Mode | Use when | Retrieval shape | Stop condition |
|---|---|---|---|
| `standard` | The topic is defined, but the evidence landscape or opportunity set still needs mapping. | Verify the core literature, major conflicts, and credible adjacent evidence. | The downstream decision has enough verified evidence and remaining gaps are explicit. |
| `focused` | One bounded question, claim, population, method, or direction needs direct verification. | Prefer directly relevant sources and trace the strongest supporting and opposing evidence. | The bounded question is answered, contradicted, or documented as unresolved. |
| `divergent` | The topic is broad or ambiguous and several evidence directions must be explored. | Search distinct source classes and justified adjacent fields; preserve speculative leads as such. | Additional directions have low expected decision value or the declared breadth limit is reached. |

`retrieval_mode` is independent of `focused_optimization | bounded_exploration`.
Default to `standard` only when neither focused verification nor divergent
exploration is justified. Record the reason; do not infer `divergent` merely
because an Idea workflow may later use bounded exploration.

## Surface and depth

- Use supplied sources when they satisfy the selected mode.
- Use Built-in Search for quick, recent, exact, or targeted retrieval.
- Use Deep Research for multi-stage, multi-direction, multi-source synthesis.
- If required Deep Research is inactive or unknown, emit the continuation
  package, return `deep_research_handoff_required`, and stop.
- Apply `focused-search-routing.md` or `divergent-search-routing.md` only as an
  overlay on `search-routing-rules.md`.

## Output discipline

- Use the same claim `support_status` vocabulary in every mode.
- Keep Evidence and Opportunity Maps separate.
- Do not use target counts as quotas. Return only defensible claims and
  opportunities; an empty or small map is valid.
- In divergent mode, distinguish direct evidence from analogy, transfer
  hypotheses, and emerging signals.
- In focused mode, retain conflicting and negative evidence rather than
  filtering it out.

## Mode changes

Reuse verified material when the scope and freshness still match. Re-run
retrieval only when the question, evidence requirement, source boundary, or
freshness requirement changes. A mode change never upgrades an existing claim's
support status without new verification.

Record the selected mode, rationale, surface, scope bounds, stop condition,
mode changes, and any required follow-up in Handoff Notes.
