# Runtime Delegation Compatibility

`research-idea` relies on role isolation, not on a single implementation detail.

## Preferred Runtime

When the runtime supports `delegate_task`, use isolated subagents for:

- methodology/statistics preflight;
- independent idea evaluation;
- any reviewer-like role that must not share generation context.

For multiple independent ideas, dispatch them in one `delegate_task(tasks=[...])` call when supported.

## Required Isolation

The same agent must not both generate or revise an idea and evaluate that idea. Loading `idea-evaluator` inline in the generator/orchestrator context is invalid for final evaluation.

## Fallback Runtime

If no subagent/delegation tool is available:

- generation may run inline;
- context building and portfolio assembly may run inline;
- final independent evaluation must be deferred, marked `evaluation_pending`, or performed in a fresh independent session;
- the portfolio must not mark any idea as promoted unless independent evaluation exists.

## Invalid Delegation Output

Treat a delegated output as invalid when it:

- omits required fields from `artifact-contracts.md`;
- violates the assigned role boundary;
- invents evidence;
- evaluates an idea it generated or revised;
- ignores hard gates;
- cannot be traced to an input brief.

Retry invalid evaluation once with a stricter brief. If it fails again, stop with `evaluation_failure_stop`.
