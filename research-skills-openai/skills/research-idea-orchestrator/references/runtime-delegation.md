# Runtime Delegation Compatibility

`research-idea` relies on role isolation, not on a single implementation detail.

## Required Delegation

Use ChatGPT/Codex subagent or delegated-thread capabilities to create fresh independent instances for:

- methodology/statistics preflight;
- independent idea evaluation;
- any reviewer-like role that must not share generation context.

For multiple independent ideas or panel roles, dispatch one task per reviewer concurrently. Each reviewer must have a distinct instance ID and frozen input set.

## Required Isolation

The same agent must not both generate or revise an idea and evaluate that idea. Loading `idea-evaluator` inline in the generator/orchestrator context is invalid for final evaluation.

## Unavailable Delegation

If no subagent/delegation tool is available:

- generation may run inline;
- context building and portfolio assembly may run inline;
- every reviewer-class task must return `independent_review_pending` plus a self-contained continuation brief and stop;
- do not perform inline evaluation, soft-isolated review, or same-context self-review;
- the portfolio must not mark any idea as promoted, ready, or conditional unless all required independent reviews exist.

The continuation brief must name the reviewer skill and role, frozen artifact IDs/paths/versions, allowed files, prohibited files, review scope, output path, and required report schema.

## Invalid Delegation Output

Treat a delegated output as invalid when it:

- omits required fields from `artifact-contracts.md`;
- violates the assigned role boundary;
- invents evidence;
- evaluates an idea it generated or revised;
- ignores hard gates;
- cannot be traced to an input brief.

Retry invalid evaluation once in a new fresh subagent with a stricter brief. If
it fails again, stop with workflow state `blocked` and failure route
`evaluation_failure_stop`.
