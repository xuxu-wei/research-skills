# SAP Re-evaluation Policy

SAP re-evaluation must be performed by a new isolated evaluator instance after revision. The evaluator must not see the prior evaluator's scores, overall rationale, or decision.

## Requirements

The evaluator should receive:

- current SAP file path;
- previous SAP version or path;
- anonymized prior must-fix issue list without scores, overall rationale, or decision;
- SAP revision delta report;
- methodology/statistics preflight report;
- relevant proposal or context brief;
- user constraints and target output.

## Evaluation Focus

- Were prior must-fix issues addressed?
- Were prior hard gate failures resolved?
- Were new defects introduced?
- Was the revision substantive, or only stylistic?
- Is another revision likely to add value?

## stop_no_gain

Use `stop_no_gain` when the revision does not materially improve key defects, when critical flaws remain, or when further revision requires missing information rather than writing effort.
