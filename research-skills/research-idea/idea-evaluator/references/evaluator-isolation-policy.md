# Evaluator Isolation Policy

## Required Isolation

The evaluator must not be the same agent that generated or revised the idea.

## Invalid Evaluation

Mark evaluation invalid if:

- evaluator generated the idea
- evaluator rewrites the idea during scoring
- evaluator invents evidence
- evaluator ignores hard gates
- evaluator omits scores, gates, recommendation, or repair direction

## Recovery

Invalid evaluation should be returned to the orchestrator for reassignment to a separate evaluator.
