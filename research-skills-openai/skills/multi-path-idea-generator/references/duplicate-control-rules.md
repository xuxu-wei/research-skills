# Duplicate Control Rules

本文件管理候选 idea 与 existing idea pool 的重复控制。

## Near-duplicate indicators

- research question 实质相同；
- data source、endpoint 和 method 基本相同；
- 仅改标题、对象措辞或价值表述；
- generation path 不同但实际研究设计相同。

## Actions

- `keep`: 实质不同，可保留。
- `merge`: 与已有 idea 互补，合并并记录 parent IDs。
- `reframe`: 角度不同但设计过近，应重构。
- `discard`: 无实质增量，应丢弃并记录原因。

## Required notes

每个 merge、reframe 或 discard 都应记录：

- affected idea IDs；
- reason；
- retained distinction or lost distinction；
- lineage update。
