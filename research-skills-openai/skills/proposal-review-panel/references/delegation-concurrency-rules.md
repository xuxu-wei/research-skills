# Panel Reviewer Concurrency Rules

## Independence

Each selected reviewer role runs in a distinct fresh independent subagent or delegated thread. Every reviewer receives only the frozen proposal logical identity, its role brief, review scope, user goal, and allowed verified review scenario. Reviewers share no mutable state and cannot see one another's scores, comments, recommendations, evaluator outputs, editorial/journal-review artifacts, or hidden rationale. Logical identity and index completeness replace digest requirements.

## Concurrent execution

Start the complete reviewer set concurrently using the current ChatGPT/Codex runtime's available subagent delegation capability:

- one task and one reviewer instance per role;
- identical frozen proposal version across tasks;
- role-specific concerns and output path per task;
- no staged disclosure of completed reports;
- wait for every selected reviewer before aggregation.

The default `standard_panel` starts broad-field, domain expert, methodology/statistics, skeptical, and submission-guard reviewer tasks together. Apply the same pattern to the three-role and seven-role tiers.

## Aggregation boundary

Only the panel aggregator may read all completed reports. It may deduplicate overlapping findings, but it must preserve dissent, minority objections, severe concerns, and each finding's source reviewer. It cannot revise the proposal or fabricate consensus.

## Failure handling

If any selected reviewer cannot run independently, do not replace it with inline review. Return `independent_review_pending`, identify missing reviewer reports, include self-contained continuation briefs, and stop without a supportive/final recommendation.

Staged review is allowed only when the user explicitly requests temporal staging; it still must not reveal earlier reviews to later reviewers.
