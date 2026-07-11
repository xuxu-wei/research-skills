# Exploration Strategy Rules

总控文件。定义三种 Exploration Level 的参数差异。SKILL.md 的 Route Selection 完成后，按此处规则加载对应策略。

## Level Overview

| Level | 简写 | 适用意图 |
|-------|------|---------|
| Standard | S | 方向已有轮廓，需要证据验证和机会识别。用户说"自主决定"/"默认"/"你来定"时自动选此。 |
| Divergent | D | 方向模糊、希望探索更多可能性、寻找被忽视的角度。 |
| Focused | F | 方向明确、需要严格验证、为 proposal/evaluation 准备 solid evidence。 |

## Per-Level Parameter Override

### Retrieval Routing

| Level | 路由规则文件 |
|-------|------------|
| Standard | `references/search-routing-rules.md`（当前行为，不变） |
| Divergent | `references/divergent-search-routing.md` |
| Focused | `references/focused-search-routing.md` |

### Opportunity Type Preference

| Level | 允许的类型 |
|-------|----------|
| Standard | 全部 core types；exploration types 仅在证据自然支持时出现 |
| Divergent | core types + exploration types（analogy, cross-domain, tension, trend, reframing, wildcard） |
| Focused | 仅 core types；exploration types 不出现在 Opportunity Map 中 |

详细分类见 `references/opportunity-type-taxonomy.md`。

### Confidence Threshold

| Level | 纳入标准 | 标注倾向 |
|-------|---------|---------|
| Standard | 至少一个来源或清晰逻辑链 | 混合 |
| Divergent | "plausible and interesting" 即可 | 多数标 `speculative` 或 `low-confidence` |
| Focused | 需要直接证据支撑 | 多数标 `supported` 或 `likely` |

### Deep Research Continuation Adjustment (Path B)

| Level | 调整 |
|-------|------|
| Standard | 使用 `templates/deep-research-prompt-template.md` 默认版本 |
| Divergent | Phase 1 拓宽检索范围、增加相邻领域来源、降低时效性限制 |
| Focused | 缩减至单阶段 targeted retrieval、提高时效性要求、增加验证性要求 |

详细规则见 `references/deep-research-prompt-rules.md` 的 Level-specific adjustments 章节。

### Opportunity Count Expectation

| Level | 预期输出 |
|-------|---------|
| Standard | 6-12 条 |
| Divergent | 12-25 条（以 speculative 标注为主） |
| Focused | 3-8 条（以 supported 标注为主） |

这只是预期参考，不设硬性上限。机会质量优先于数量。

## Mode Transition

在一次 session 内，如用户对输出不满意，允许切换模式：

- 用户："太窄了，换个更发散的模式" → 切换到 Divergent，基于已有 Evidence Map 扩大 opportunity 提取范围，不重新检索
- 用户："太多了，帮我聚焦" → 切换到 Focused，过滤已有 opportunities 至 core types + 收紧置信度

切换时不重新执行完整的 intake → retrieve 流程。但如果用户要求重新检索，则完整重跑。

## Decision Log

Handoff Notes 中记录：
- 选择的 Exploration Level（S / D / F）
- 如用户指定了"自主决定"，记录为 `Standard (auto)`
