# High-Impact Aspiration Check

Load this advisory check only when the user explicitly asks whether an Idea
could support an `IF > 10` or comparable high-impact aspiration.

The orchestrator adds this stable appendix to the fresh `idea-evaluator` brief;
the evaluator applies it from the same dossier-only input and appends the result
to its review report. The orchestrator never performs the judgment.

Evaluate only what the current complete dossier supports:

- importance and breadth of the research question;
- strength and closure of the proposed evidence chains;
- likely relevance beyond a narrow local setting;
- depth of the contribution relative to closest work;
- consistency between title/positioning claims and the planned implementation;
- feasibility of the work required to sustain those claims.

Append a concise advisory result:

```yaml
high_impact_aspiration:
  alignment: plausible | conditional | not_supported | not_assessable
  rationale: []
  conditions_to_strengthen: []
  unsupported_positioning_claims: []
```

This check does not change the six canonical scores or hard gates and does not
estimate submission or acceptance probability. After freezing the evaluation,
the evaluator still follows the ordinary journal-matching contract. For a final
biomedical or clinical Idea, the orchestrator freezes its unscored, unranked
candidate brief and delegates a fresh `medical-journal-review`.
