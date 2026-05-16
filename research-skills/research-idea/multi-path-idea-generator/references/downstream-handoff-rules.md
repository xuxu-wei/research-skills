# Downstream Handoff Rules

本文件定义生成结果交付给下游技能的要求。

## To methodology-statistics-preflight

标记需要 preflight 的情况：

- endpoint/metric 不够清楚；
- data source 与 research question 的匹配需要检查；
- idea 涉及临床、观察性研究、预测模型、因果推断或统计分析；
- minimal analysis route 可能不成立。

## To isolated idea-evaluator

所有生成的 idea 都必须经 orchestrator 派发给隔离、独立 evaluator。交付内容包括：

- generated idea set；
- supporting opportunity IDs；
- evidence limitations；
- novelty uncertainty；
- risks / reviewer objections；
- lineage notes。

## To idea-portfolio-assembler

仅在 evaluator 和 orchestrator 决策后使用。本 skill 不直接向 portfolio assembler 推送 promoted idea。
