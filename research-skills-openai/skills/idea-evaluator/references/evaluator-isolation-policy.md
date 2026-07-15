# Evaluator Isolation Policy

## Required Isolation

The evaluator must run in a fresh independent subagent/delegated thread and must not be the same agent or context that generated or revised the idea. It reads only frozen, versioned artifacts and may write only evaluation artifacts.

## Invalid Evaluation

Mark evaluation invalid if:

- evaluator generated the idea
- evaluator rewrites the idea during scoring
- evaluator invents evidence
- evaluator ignores hard gates
- evaluator omits scores, gates, recommendation, or repair direction
- evaluator reads parent hidden reasoning, a prior snapshot, revision delta, prior score/decision, or another reviewer output
- evaluator evaluates a partial/delta-only Idea or cannot bind the current digest
- evaluator edits any source artifact

## Recovery

Invalid evaluation should be returned to the orchestrator for reassignment to a new fresh evaluator. If independent delegation is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop; never use inline self-review.
