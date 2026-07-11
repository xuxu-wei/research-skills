# Divergent Search Routing

当 Exploration Level 为 Divergent 时，替代 `references/search-routing-rules.md` 使用。此文件仅覆盖与 Standard 不同的部分；未覆盖的规则仍沿用 `search-routing-rules.md`。

## Core Principle

Divergent 模式的检索目标不是「验证一个已知方向」，而是「发现尽可能多的潜在方向」。检索应刻意超出直接相关范围，纳入相邻领域、不同方法角度、类比问题和趋势信号。

## Routing by Domain

### Clinical / Medical / Life Science

Standard 规则基础上追加：

- 纳入基础科学和 mechanistic studies，即使未到达临床阶段
- 纳入不同疾病领域中相似机制或相似干预范式的研究
- 纳入不同人群/地域的 evidence（即使不直接适用于目标人群）
- 对于中医药方向：纳入植物药、天然产物、系统生物学、代谢组学等相关领域的研究

### AI / ML / Engineering

Standard 规则基础上追加：

- 纳入相邻 sub-field 中使用类似方法或处理类似数据结构的论文（如 NLP 中的序列建模方法用于临床时间序列）
- 纳入不同应用领域的 benchmark 和 evaluation protocol
- 纳入 negative results 和 failure reports

### Cross-Domain Exploration

允许且鼓励合理跨领域检索，但需满足关联性标准：

- 方法可迁移：方法结构相似，可移植到当前领域
- 数据可类比：数据形态/规模/噪声特征相似
- 问题同构：核心科学问题在形式上是同构的
- 概念可映射：核心概念可以从一个领域映射到另一个领域

不因为「同属某大类」就无条件探索。关联性判断需写入 routing log。

### Broad Topic

在 Standard 三阶段基础上：

- Phase 1（广度扫描）：范围扩大 2-3 倍，包括相邻学科和交叉领域
- Phase 2（深度追踪）：选择 5-8 条最有趣的线索深挖，而非聚焦 2-3 条
- Phase 3（缺口补全）：专门增加一轮「意外发现」检索——用不同关键词组合、不同数据库、不同视角重新扫一遍

## Retrieval Depth

- `targeted_retrieval`：不适用于 Divergent 模式
- `expanded_retrieval`：默认。覆盖更多来源、更长时间窗口、更多语言
- `stop_with_evidence_limitation`：同 Standard

## Source Priority Adjustments

Standard 的优先级规则仍适用，但额外增加：

- Review articles 和 position papers：用于发现跨领域连接线索，而非作为 evidence
- Preprints 和 conference abstracts：纳入 early signals，标为 `low-confidence`
- Non-English literature：主动纳入（非仅中文），标出语言限制
- Adjacent-field top journals：扫描其近期热点方向和可用方法

## Routing Log

Divergent 模式下的 routing log 需额外记录：
- 每条跨领域路由的关联性判断依据
- 哪些 adjacent fields 被探索、为何被排除
- 意外发现的来源
