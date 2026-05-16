# Path Selection Rules

本文件管理路径选择与路径建议规则。

## If orchestrator specifies paths

严格按指定 paths 生成，不扩展为其他路径，除非指定路径无法执行并需返回 failure report。

## If orchestrator does not specify paths

本 skill 可提出 recommended paths，并据此生成候选 ideas。路径建议基于：

- opportunity type；
- user goal；
- intended output；
- available data / methods；
- constraints；
- targeted repair direction；
- existing idea pool diversity。

## Opportunity-to-path mapping

- `gap` → `gap_driven`
- `value` → `value_need_driven`
- `method` → `method_driven`
- `data` → `data_opportunity`
- `metric` → `measurement_metric_driven`
- `failure` → `constraint_driven` or `benchmark_evaluation`
- `theory` → `contrarian_assumption_challenge` or `taxonomy_framework`
- `benchmark` → `benchmark_evaluation`
- `taxonomy` → `taxonomy_framework`
- `implementation` → `value_need_driven` or `constraint_driven`

## Repair-target mapping

- novelty weak → `gap_driven`, `contrarian_assumption_challenge`, `method_driven`
- feasibility weak → `constraint_driven`, `data_opportunity`
- impact weak → `value_need_driven`
- clarity weak → `measurement_metric_driven`, `taxonomy_framework`
- completion weak → schema completion plus original path
