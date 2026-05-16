# Portfolio Output Schema

This reference defines the output objects for portfolio assembly.

## Default Output Sections

- executive decision summary;
- research context summary;
- evidence / opportunity map summary;
- ranked candidate ideas;
- score and hard gate table;
- promoted idea packages;
- rejected / merged / backup idea summary;
- lineage summary;
- remaining uncertainties and PI decision points;
- proposal handoff summary.

## Conditional Outputs

- `no_promoted_idea_report`: when no idea reaches portfolio-ready status.
- `portfolio_assembly_failure_report`: when required inputs are missing or evaluation is invalid.

## Formatting Principle

The final output is a PI-review document. It should be readable, concise, and traceable. Do not output a raw machine schema dump unless the user or orchestrator explicitly requests it.
