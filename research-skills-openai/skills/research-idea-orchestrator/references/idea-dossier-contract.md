# Complete Idea Dossier Contract

## Contents

Required sections; evidence chains; title/audience positioning; citation and
marker rules; limitation, assumption, and contingency authority.

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

“Complete” does not mean reproducing a downstream decision tree. The summary
first states the central study object or question, primary research approach or
planned test, and positive planned contribution. Use validation language only
when validation is part of the Idea. A contingent downstream component, when
present, is represented only by
its scientific purpose and conditional status; its eligibility, alternative,
and stopping logic belongs in its technical authority subsection. Do not use a
project-stage or branch label in the summary when understanding it would require
a later definition.

Use one H1 research title and repeat that exact title in the first section's
`Title` field; mismatch is an incomplete dossier.

Within section 3, require these non-empty H3 headings in this exact order:

1. `### Background`
2. `### Current state`
3. `### Gap`
4. `### Significance`
5. `### Rationale`

Each subsection performs its named function. The gap states what current
knowledge or evidence cannot answer; novelty positioning belongs in section 12
and cannot substitute for the gap. Significance explains why closing the gap
matters. Rationale connects that gap and significance to the proposed design.

Sections 1--4 form the reader-understanding core. Introduce the problem and
contribution before specialized technical detail, and explain any concept not
covered by the target reader's prior knowledge at first use. Sections 5--11 and
13--14 provide technical, evidential, and feasibility detail; section 12 returns to the
contribution and closest-work comparison. The title, summary, abstract, and
section 3 must not depend on definitions supplied only in later sections.

## Optional placement pattern for a sequential downstream component

Apply this pattern only when the scientific design explicitly makes a later
component conditional on success of a primary study. It does not govern
parallel, adaptive, iterative, nested, or multiple dependent components; those
require their own design-faithful placement map. A complete Idea does not repeat
every component in every section.

| Dossier function | Typical reader-facing role when this pattern applies |
|---|---|
| Title and one-sentence summary | Conditional scientific purpose only; no named eligibility set, branch, fallback, stopping route, internal stage label, visit/item detail, or deliverable inventory |
| Structured abstract | At most one short purpose-and-sequence statement across the abstract; do not repeat it in approach, expected result, and contribution fields |
| Background-to-rationale chain | Omit unless one short sentence is necessary to explain why the primary design precedes the component |
| Question and objectives | Only the subordinate question/objective content needed to preserve the scientific design; no decision tree or technical label |
| Work plan | The dependent work package(s) needed by the design; do not repeat them in the opening, timeline, success definition, and closing sequence |
| Data/evidence | Availability and evidence status only |
| Scientific methods | The sole complete authority for eligibility, operations, mutually exclusive alternatives, stopping logic, and allowed interpretation |
| Implementation | Objects, records, and interfaces only |
| Evidence chain, required analyses, and outputs | The role-necessary input/transformation/output or evidence item in each applicable section; no re-explanation of the branch tree |
| Contribution and closest work | Omit unless the component itself supports a bounded contribution or closest-work comparison; do not make it a parallel primary contribution by default |
| Claim-Support | A row only for an actual title or primary-positioning claim; do not create rows for technical sub-branches unless they are themselves primary claims |
| Section 14 | Resource status, working assumptions, the complete limitation family, and operational risk trigger/response/consequence in their respective subsections; do not repeat design branches from Methods or append a final prose recap |

Absence from a section is valid when that section has no distinct function for
the component. Traceability comes from the applicable method authority,
evidence chain(s), and any actual title/positioning Claim-Support row, not from
repeated prose or fixed cardinalities.

## Evidence chains

Create at least one chain per major objective or work package:

```markdown
### Evidence chain: <human-readable title>
- **Input:** <data, materials, population, variables, existing evidence>
- **Method / analysis / processing:** <design, processing, analysis, comparison, validation, quality control>
- **Output:** <estimate, model, figure, mechanism evidence, validation result, decision evidence>
- **Supports:** <what this output tests or supports>
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

| Title or positioning claim, written at its supported scope | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or a natural-language no-increment statement | Support status in the dossier language |
|---|---|---|---|---|---|---|
| Human-readable bounded claim | Natural-language contribution frame | Dossier section or work package | Full chain and output title | Normal citation or dossier section | Input, transformation, output increment, or a plain statement that none is claimed | Natural-language supported / qualified / unsupported equivalent |

Render contribution frames, no-increment statements, support states, and mapper
evidence states in the dossier's reader language. Preserve their semantics, but do
not expose machine enum tokens in reader-facing prose or tables when a natural
equivalent exists.

- A `supported` claim may appear directly. A `qualified` claim must be written
  at its supported scope in the claim cell and everywhere it appears; do not
  maintain a separate repeated-qualifier column. An `unsupported` claim cannot
  appear in the title, summary, or primary positioning.
- Preserve each mapper status beside its citation in the literature-basis cell.
  Map `weak`, `single-source`, or `access-limited` to at most `qualified`, and
  `conflicting` or `unverified` to `unsupported` unless the dossier documents a
  resolved, independently supported basis. Mapper `supported` still needs an
  implementation/evidence-chain match before dossier status is `supported`.
- Do not inflate association into causation, local evidence into universality,
  or technical or analytical utility into demonstrated real-world effectiveness
  or impact.
- Similar prior work does not automatically require new work. State an honest
  validation, application, integration, resource, or audience value instead.
  If claiming scientific, data, or method novelty, identify the real increment
  in an input, transformation, or output.

## Citation and marker rules

Use standard author-year or numbered academic citations resolved in the same
dossier. Do not use workflow IDs such as `C24`, `M1`, `A0`, `O001`, or `MF-*`
as prose evidence. The reference ledger is for user navigation and audit; the
dossier must remain understandable without it.

## Limitation, assumption, and contingency authority

Section 14 is the sole global authority for complete limitation statements and
working assumptions. Consolidate each item there once. Within section 14, put
the complete statement of a limitation family only under `Limitations and
boundary conditions`; the feasibility subsection states resource status, the
working-assumptions subsection states pending specifications, and the risk table
states each operational risk trigger, response, and consequence without
repeating the full limitation. Do not add a closing boundary recap. Other
sections do not repeat, summarize, or cross-reference limitations.

Design eligibility, mutually exclusive analysis alternatives, design-specific
stopping logic, and their allowed interpretations belong only in the relevant
Methods authority. Falsification criteria and result-dependent interpretations
belong only in section 11. Section 14 must not restate either decision tree; its
risk table covers operational threats and responses that are not already design
logic.

When a scientific, statistical, measurement, or design specification is
deliberately unresolved, list it once under section 14's `Working assumptions`
subsection. State the exact pending choice, what is already fixed, the decision
point and information allowed at that point, and the consequence of not resolving
it. A feasibility table may report that the item remains pending, but must not
introduce additional unresolved specifications absent from that list. Omit the
subsection when none exist.

The only exception is a minimal local boundary that directly advances the
immediate reasoning: it is necessary to explain the design choice that follows,
and omission would distort that reasoning. This exception is not permission to
front-load methodological defense or repeat a general caveat. Scientific
falsification criteria remain in section 11 because they define what results
would challenge the hypothesis; do not duplicate them as limitations.
