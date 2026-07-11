# No-Gain Stop Policy

## Purpose

Prevent repeated revision loops that consume context without improving proposal quality.

## Trigger Conditions

Trigger `stop_no_gain` when one or more apply:

- A revision round fails to resolve the main must-fix issues.
- The proposal is clearer but not more feasible, defensible, or complete.
- The same hard gate failure remains after targeted revision.
- The revision introduces a new major inconsistency.
- Further progress requires user input, new evidence, or method redesign.
- Maximum revision rounds have been reached without accept.

## Required Output

When stopping for no gain, report:

- unresolved core issues;
- why further autonomous revision is unlikely to help;
- what user input or external review is required;
- whether the proposal should be rejected, redesigned, or held for human review.
