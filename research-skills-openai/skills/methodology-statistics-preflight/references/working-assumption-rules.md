# Working Assumption Rules for Idea Handoff

Use a `working_assumption` only when all of the following are true:

- at least one minimally viable scientific route already exists;
- the unresolved detail is bounded, plausible, and verifiable at a named point;
- writing under the assumption does not change the core question, objective,
  study object, scope, irreplaceable input, primary measurement or inference
  target, or claim strength; and
- if the assumption is false, a bounded adjustment remains possible without
  replacing the scientific route.

The assumed value or route—not merely the fact that a detail is unresolved—must
be explicitly and conditionally accepted in the current methodology/statistics
preflight report. A protected-content register or delegation brief may only carry
that approved assumption verbatim; neither can create or approve one. A downstream
writer must not select among statistical, measurement, or design specifications
merely to resolve a narrative or language ambiguity. If the current preflight has
not accepted a specific assumption, state the bounded specification as pending at
its named verification point or route the choice for clarification.

Otherwise classify the issue as `required_repair` or return
`clarification_stop`. Never use an assumption to conceal a missing core input,
an invalid data-method relation, or a route whose viability depends entirely on
the unknown detail.

Each working assumption requires:

```yaml
assumption_id:
unconfirmed_detail:
working_assumption:
basis_for_planning:
impact_if_false:
verification_needed:
verification_point:
affected_design_component:
```

The downstream scientific writer may complete the plan as if the stated
assumption holds, while recording it once in the dossier's authoritative
assumptions section as a research risk. The writer must not repeat it across
the summary, background, methods, or contribution sections and must not phrase
it as verified evidence.
