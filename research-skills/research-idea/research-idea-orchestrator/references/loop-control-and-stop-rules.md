# Loop Control and Stop Rules

本文件定义 idea round、循环控制、score delta、lineage 记录和 early stop 规则。

## 1. Default Round Limit

默认最多 3 轮 idea rounds，除非用户明确指定更多或更少。

一轮包括：

1. routing；
2. generation 或 targeted repair；
3. optional methodology/statistics preflight；
4. isolated independent evaluation；
5. decision update；
6. lineage update。

## 2. Required Round Log

每轮必须记录：

- round number；
- selected generation or repair paths；
- new ideas；
- revised ideas；
- merged ideas；
- rejected ideas；
- backup ideas；
- score changes；
- main reasons for score changes；
- remaining unresolved issues；
- next decision。

## 3. Stop Conditions

### accept_stop

至少 1 个 idea 达到 promote 标准，且没有 fatal gate failure。

### portfolio_stop

已获得 1-3 个质量足够、互相区分明确的候选 idea。

### no_gain_stop

连续一轮修订后核心评分提升 `< 0.2`，且主要缺陷未解决。

### clarification_stop

缺失的用户决策很可能改变：

- 研究方向；
- endpoint/metric；
- data source；
- intended output。

只有在上述情况下才触发 `clarification_stop`。

### reject_stop

所有 idea 均存在不可修复的 feasibility、relevance、data 或 measurement 问题。

### evaluation_failure_stop

隔离独立 evaluation 已重派一次，仍缺少必要字段或违反 independence 规则。

## 4. Clarification Policy

- 可合理假设的信息：继续推进，并在 portfolio 中标注 assumption。
- 会显著影响 feasibility 或 routing 的信息：最多问 3 个澄清问题。
- 会改变研究方向、endpoint/metric、data source 或 intended output 的信息：触发 `clarification_stop`。

## 5. Repair Routing

- novelty low -> gap_driven / contrarian_assumption_challenge / method_driven
- evidence weak -> research-opportunity-mapper
- feasibility low -> constraint_driven / data_opportunity / methodology-statistics-preflight
- impact low -> value_need_driven / implementation / translational framing
- relevance low -> context re-alignment; ask user only if goal is ambiguous
- clarity low -> measurement_metric_driven / question narrowing / endpoint reconstruction
- completion low -> schema completion / minimal experiment design

## 6. No Random Regeneration

If evaluation identifies a specific defect, the next round must target that defect. Random broad generation is allowed only when:

- the opportunity map is too broad;
- no candidate idea meets minimum quality;
- user explicitly requests divergent brainstorming.
