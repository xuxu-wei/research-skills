# Proposal Hard Gates

The proposal must pass all hard gates before the evaluator may return `accept`.

## Minimum Gates

- Clarity >= 3.5
- Feasibility >= 3.0
- Completion >= 3.5
- Genre Fit: pass/fail（无阈值，任何体裁违规即 fail）
- No unresolved fatal flaw

### Gate Interpretation

### Clarity Gate
The proposal must state a reviewable research question or objective, define the research object, and align aims, methods, and expected outputs.

### Feasibility Gate
The proposal must describe a plausible execution path given available or required data, methods, resources, timeline, and ethical constraints.

### Completion Gate
The proposal must contain enough content for evaluator and reviewer assessment. Missing sections may fail this gate if they block reviewability.

### Genre Fit Gate
The proposal must not contain any of the following: (a) narrative clinical scenes ("一位医生在查房时…"), (b) tutorial-style rhetorical questions ("为什么是X？因为…"), (c) review-response residue ("vX新增""回应Review Panel"等 version markers), (d) explanatory paragraphs added for comprehension rather than argument (terminology glossaries, concept translation tables as standalone body sections). Any single violation → FAIL. Evaluator must record the specific location of each violation.

## Gate Failure Handling

- If a gate fails but the issue is repairable, decision should normally be `revise`.
- If a gate fails due to an unrecoverable contradiction or missing foundation, decision should be `reject`.
- If re-evaluation shows no substantive progress on a failed gate, decision may be `stop_no_gain`.
- Genre Fit gate failures are always repairable (textual fixes) and should route to `revise` with specific location annotations.
