# Canonical Evaluation Rubric Pointer

The sole scoring contract for Idea evaluation is:

```text
skills/idea-evaluator/references/evaluation-rubric.md
```

When freezing an evaluation round, bind that canonical resource to the current
plugin version and record its artifact ID/version/path in the delegate brief. Do not copy,
summarize, or redefine scoring rules here.

The evaluator loads the canonical rubric as a skill instruction. It is not a
project artifact and does not appear in the report's project `files_read`.
If the canonical resource cannot be resolved at the frozen plugin version,
return `independent_review_pending` rather than using an inline or reconstructed
rubric.
