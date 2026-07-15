# SAP Re-evaluation Policy

Use a fresh isolated evaluator for a revised SAP. Give it only the latest
complete frozen SAP and SHA-256, the stable rubric, necessary proposal/context
and preflight facts, user constraints, and an optional anonymized must-fix list.

Do not provide the prior SAP, revision delta, prior report, score, rationale, or
decision. Record `prior_versions_visible: false` and
`revision_delta_visible: false`. Evaluate the current SAP de novo. The
orchestrator compares sealed rounds and decides improvement or `stop_no_gain`.
