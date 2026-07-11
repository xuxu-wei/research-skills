# Focused Search Routing

当 Exploration Level 为 Focused 时，替代 `references/search-routing-rules.md` 使用。此文件仅覆盖与 Standard 不同的部分；未覆盖的规则仍沿用 `search-routing-rules.md`。

## Core Principle

Focused 模式的检索目标是「为已明确的研究方向找到最 solid 的证据」。检索应严格限定在直接相关范围内，排除边缘或关联性弱的来源。

## Routing by Domain

### Clinical / Medical / Life Science

在 Standard 规则基础上收紧：

- 优先 systematic reviews 和 practice guidelines；如不存在，优先 highest-level primary evidence
- 仅纳入直接针对目标 population、intervention、outcome 的证据
- 排除不同疾病领域、不同干预类别的间接证据（除非用户明确要求类比）
- 中医药方向：仅检索针对目标方剂/药材/成分的直接证据，不扩展至同类方剂

### AI / ML / Engineering

在 Standard 规则基础上收紧：

- 仅纳入直接针对 target task / dataset / metric 的论文
- 排除使用不同 evaluation protocol 或不同 benchmark 的工作
- 优先 peer-reviewed published work；preprints 仅在出版版本不可得时使用

### Cross-Domain

Focused 模式下**不进行跨领域检索**。如发现某领域的证据对当前方向至关重要但不可得，记录为 evidence limitation，不尝试从其他领域找替代。

## Retrieval Depth

- `targeted_retrieval`：默认。少量高优先级查询，直接针对核心问题。
- `expanded_retrieval`：仅在 targeted 结果不足或出现冲突时触发。仍不跨领域。
- `stop_with_evidence_limitation`：当 targeted + expanded 均无法覆盖关键 evidence gap 时立即停止。

## Source Priority Adjustments

在 Standard 优先级规则基础上收紧：

- 仅纳入最高质量和最直接相关的来源
- Review articles 仅用于快速定位 primary sources，不作为独立 evidence
- Preprints：除非领域极新且无 peer-reviewed 替代，否则排除
- Non-English literature：除非用户明确要求或领域特性使然，否则排除
- 排除 opinion pieces、editorials、letters（除非包含原始数据）

## Quality Gates

Focused 模式下每条纳入 Evidence Map 的来源需通过：

1. 直接相关性：population / intervention / outcome 与用户方向匹配
2. 时效性：在用户指定时间范围内（默认 5 年）
3. 可验证性：有 DOI 或等价标识符
4. 独立性：非单一来源的衍生引用

未通过的来源不进入 Evidence Map，但可在 Evidence Limitations 中提及。

## Routing Log

Focused 模式下的 routing log 需记录：
- 每条纳入来源通过 quality gates 的情况
- 被排除的高知名度但不符合质量门的来源及排除理由
- Targeted → Expanded 升级的触发条件
