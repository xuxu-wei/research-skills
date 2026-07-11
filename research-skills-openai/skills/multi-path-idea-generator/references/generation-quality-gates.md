# Generation Quality Gates

候选 idea 进入 idea pool 前必须满足最低完整性要求。

## Minimum requirements

每个 idea 必须包含：

- research question 或 objective；
- endpoint/metric；
- data source 或 evidence base；
- minimal experiment / analysis / validation route；
- value claim；
- novelty claim with confidence limitation；
- supporting opportunity IDs；
- generation path；
- risks or reviewer objections；
- assumptions and uncertainties。

## Failure handling

若无法满足最低要求：

- 不要用空泛语言补齐；
- 不要生成 proposal；
- 输出 `generation-failure-report.md`；
- 建议返回 `research-context-builder` 或 `research-opportunity-mapper`。
