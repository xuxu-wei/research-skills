# Portfolio Output Schema

This reference defines the output objects for portfolio assembly.

## Default Output Sections

- executive decision summary;
- research context summary;
- evidence / opportunity map summary;
- ranked candidate ideas with complete snapshot-derived content and digest binding;
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

The final output is a self-contained PI-review document. Keep scores, lineage changes, and revision history subordinate to the complete current Idea. Do not output a raw machine schema dump unless explicitly requested.
