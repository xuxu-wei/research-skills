# Adaptive Idea Direction Routing

Load this reference after context and opportunity mapping. The orchestrator
applies these rules mechanically; it does not score research value.

## Routing signals

```yaml
idea_direction_routing:
  direction_clarity: clear | underdefined | ambiguous
  current_direction_value: supported | uncertain | unsupported
  evidence_confidence: high | moderate | low
  distinct_supported_directions:
    - title:
      rationale:
      evidence_confidence: high | moderate | low
      closest_to_current_direction: true | false
  route: focused_optimization | bounded_exploration | direction_route_confirmation_required | no_defensible_direction
  rationale:
```

`research-context-builder` characterizes clarity without judging value.
`research-opportunity-mapper` supplies evidence-grounded value, confidence, and
distinct directions. Conflicting or low-confidence signals require owner input.

## Deterministic route

- Use `focused_optimization` when the current direction is clear and supported,
  or when only one defensible direction exists.
- Use `bounded_exploration` only when the direction is underdefined or
  ambiguous and at least two substantively distinct directions have moderate
  or high evidence confidence.
- Generate two directions when only two qualify; generate at most three. Never
  invent a weak candidate to fill a quota.
- If none is defensible, return `no_defensible_direction`. If signals conflict
  or more than three directions cannot be separated using user priority,
  relevance, evidence confidence, feasibility, and distinctness, return
  `direction_route_confirmation_required`.

## Focused optimization

Maintain one node. Default repair order is: complete analysis and evidence
chains; align evidence and claims; increase scientific/practical value; improve
audience reach or editorial positioning; add analysis, data, or method only
when needed. Keep the existing revision/no-gain limits.

## Bounded exploration

1. Generate two or three complete dossiers.
2. Apply exactly one bounded optimization to each direction, incorporating any
   nonfatal preflight repair rather than creating an extra optimization round.
3. Remap evidence and opportunity separately for every evolved direction.
4. Write a new dossier version that only synchronizes background, citations,
   closest-work comparison, evidence limits, and claim qualifiers.
5. Run one fresh dossier-only `idea-evaluator` per direction.
6. Stop at `human_direction_selection_required`.

Post-remap synchronization may change title, audience, positioning, and
qualifiers, but must synchronize the title, one-sentence summary, structured
abstract, positioning prose, Claim-Support rows, references, and qualifiers as
one content version. It must not add objectives, data, methods, or work packages.
If structural repair is required, return `revision_required`; do not start
another automatic optimization round. Never select a winner or enter Proposal.
