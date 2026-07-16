# Complete Idea Dossier Contract

Load this reference when writing, revising, validating, or reviewing an
`idea-dossier-vNNN.md`. The dossier must stand alone for both an independent
reviewer and the user.

## Required sections

Use these non-empty headings in this order:

1. `## Title, summary, audience, and positioning`
2. `## Structured abstract`
3. `## Background, current state, gap, significance, and rationale`
4. `## Research question, objectives, and core hypothesis`
5. `## Research content and work packages`
6. `## Data, materials, and existing evidence base`
7. `## Research design and methods`
8. `## Key techniques and implementation`
9. `## Evidence chains`
10. `## Required analyses and evidence`
11. `## Expected outputs, falsification criteria, and interpretations`
12. `## Contribution, innovation, impact, application, and closest-work comparison`
13. `## Title and positioning claim-support table`
14. `## Feasibility, resources, risks, alternatives, and stop conditions`
15. `## References`

The one-sentence summary describes the complete current Idea, never merely a
change from an earlier version. Treat expected outputs as predictions, not
observed results. The first section explicitly states title, complete-Idea
summary, audience, and contribution frame; the abstract states background/gap,
objective/hypothesis, approach, expected result, and contribution/impact. Keep
revision history in `revision-delta.md`.

Use one H1 research title and repeat that exact title in the first section's
`Title` field; mismatch is an incomplete dossier.

## Evidence chains

Create at least one chain per major objective or work package:

```markdown
### Evidence chain: <human-readable title>
- **Input:** <data, materials, population, variables, existing evidence, assumptions>
- **Method / analysis / processing:** <design, processing, analysis, comparison, validation, quality control>
- **Output:** <estimate, model, figure, mechanism evidence, validation result, decision evidence>
- **Supports:** <what this output tests or supports>
- **Limits and failure conditions:** <when the chain must be qualified, downgraded, or stopped>
```

Every core objective and hypothesis must connect to an output; every output must
trace back to an input and transformation. Name chain-to-chain links in words,
not opaque IDs. Do not leave undefined inputs, outputs, or circular support.

## Title, audience, and editorial repositioning

Changing title, audience, emphasis, or contribution framing is allowed without
new work when the existing implementation supports the claim. Repositioning
may expand visibility or present the work as validation, replication,
application, translation, integration, resource, benchmark, or method value.

Maintain this in-dossier table:

| Title or positioning claim | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or `none` | Support status | Required qualifier |
|---|---|---|---|---|---|---|---|
| Human-readable claim | scientific_discovery / method / validation / replication / application / resource / benchmark / practical / translational / integration / editorial_repositioning | Dossier section or work package | Full chain and output title | Normal citation or dossier section | Input, transformation, output increment, or `none` | supported / qualified / unsupported | Scope wording |

- A `supported` claim may appear directly. A `qualified` claim must retain its
  qualifier. An `unsupported` claim cannot appear in the title, summary, or
  primary positioning.
- Preserve each mapper status beside its citation in the literature-basis cell.
  Map `weak`, `single-source`, or `access-limited` to at most `qualified`, and
  `conflicting` or `unverified` to `unsupported` unless the dossier documents a
  resolved, independently supported basis. Mapper `supported` still needs an
  implementation/evidence-chain match before dossier status is `supported`.
- Do not inflate association into causation, local evidence into universality,
  or analytical utility into demonstrated clinical effectiveness.
- Similar prior work does not automatically require new work. State an honest
  validation, application, integration, resource, or audience value instead.
  If claiming scientific, data, or method novelty, identify the real increment
  in an input, transformation, or output.

## Citation and marker rules

Use standard author-year or numbered academic citations resolved in the same
dossier. Do not use workflow IDs such as `C24`, `M1`, `A0`, `O001`, or `MF-*`
as prose evidence. The reference ledger is for user navigation and audit; the
dossier must remain understandable without it.
