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
The proposal must state a reviewable research question or objective, define the research object, and align aims, methods, and expected outputs. The reader must be able to follow problem → current knowledge → gap → significance → design rationale with progressive disclosure and manageable terminology. Missing significance or a broken gap-to-rationale transition is a gate failure.

### Feasibility Gate
The proposal must describe a plausible execution path given available or required data, methods, resources, timeline, and operational constraints.

### Completion Gate
The proposal must contain enough content for evaluator and reviewer assessment, satisfy binding source requirements, and maintain one authoritative `Assumptions, feasibility, and risks` location. Missing required functions may fail this gate when they block reviewability; section labels and counts alone do not establish completion.

### Genre Fit Gate
The proposal must use a persuasive research-proposal genre appropriate to its target reader and binding format. Review-response residue or version-process metadata in the body is a failure. Narrative devices, rhetorical questions, definitions, glossaries, or explanatory material are defects only when they displace decision-relevant argument, obscure section function, or add reader burden without advancing the reasoning chain. Record the location and functional harm; do not fail genre fit from a universal sentence-form rule.

## Gate Failure Handling

- If a gate fails but the issue is repairable, decision should normally be `revise`.
- If a gate fails due to an unrecoverable contradiction or missing foundation, decision should be `reject`.
- The evaluator still returns only `accept`, `revise`, or `reject`. Only the orchestrator may derive `stop_no_gain` after independently comparing sealed round reports; never expose those reports to the evaluator.
- Genre Fit failures route to `revise` when the function can be repaired without changing scientific content; a genre problem that reveals a missing rationale or substantive choice follows the corresponding scientific route.
