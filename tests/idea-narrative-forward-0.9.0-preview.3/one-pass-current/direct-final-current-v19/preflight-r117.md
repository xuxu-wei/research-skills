---
artifact_id: methodology-statistics-preflight-I01-001-r117
version: r117
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/preflight-r117.md
artifact_type: methodology-statistics-preflight-report
input_artifact_ref:
  artifact_id: idea-dossier-I01-001-v053
  version: v053
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/idea-dossier-v053.md
---

# 方法学与统计学预检报告

## 结论

- **decision:** `pass`
- **idea_handoff_decision:** `proceed_with_assumptions`
- **评估范围：** 仅检查连续潜在状态恢复统计量与有前置条件的试验分层标准化概率指数是否唯一可计算、相应工作假设是否满足契约、未获确认时的后果是否保留，以及两项规格是否改变研究身份或主张边界。
- **总体判断：** 两项规格在 Idea 阶段均已达到唯一可计算的要求。两项尚未完成的负责人确认均可作为有明确核验时点的工作假设继续推进；它们不构成结果可见后的方法选择。两项规格均未改变核心问题、研究对象、主要推断单位、阶段 I–II 的主要目标或证据强度。

## 规格一：连续潜在状态恢复统计量

### 可计算性判断

**通过。** 对每次模拟重复 `b`，评估对象、评价格点和计算顺序均已固定：

1. 比较同一预定患者—时间评价格点上的真实连续潜在状态矩阵 `X_b` 与估计后验均值矩阵 `Xhat_b`，并按列中心化；
2. 计算覆盖全部 `d_b` 个真实连续潜在维度、按降序排列的非负典型相关系数；
3. 估计维度不等于 `d_b`、任一矩阵列秩小于 `d_b`，或预先固定的算法无法给出全部 `d_b` 个相关时，令 `r_b=0`；否则令 `r_b` 等于全部典型相关中的最小值，且不取平方；
4. 对情景内 `B` 次重复计算
   \[
   L=\max\{0,\bar r-1.96s_r/\sqrt B\},
   \]
   仅当 `L` 不低于 0.80 时判定连续潜在状态恢复达标。

该定义同时固定了输入、维度处理、异常情形、重复级统计量、情景级汇总、方向和阈值，不留有在看到恢复结果后选择维度、患者、时点、平方相关或汇总函数的余地。正确生成且要求恢复连续状态的情景必须在结果可见前纳入，也阻断了按结果挑选情景。

### 未达到标准或未获确认时的后果

后果完整且可执行：未达到恢复标准时合并或删除维度，或改用线性、多状态或仅预测表征；在首次模拟拟合或查看任何恢复结果前未完成双负责人确认时，复杂候选不得依靠连续恢复晋级；若查看结果后才改变定义，既有连续恢复结论失效，须在结果保持不可见的重新设计中接受新的独立方法学评估。预测性能不得覆盖这一失败。

## 规格二：有前置条件的试验分层标准化概率指数

### 可计算性判断

**通过。** 对每项试验，目标分析集、实际访视有序结局分支、原随机化中心或分层因素 `S`、方向、并列规则和标准化权重均有唯一规则。主要估计目标为

\[
\theta_{\mathrm{PI}}=\sum_s\omega_s\left\{P(Y_1>Y_0\mid S=s)+\tfrac12P(Y_1=Y_0\mid S=s)\right\},
\]

其中 `Y_1` 和 `Y_0` 是同一核验随机化层内独立抽取的试验组与对照组有序访视结局，次序越高越有利；`omega_s` 是预先指定目标分析集中两组汇总后的随机化层样本比例。死亡与死亡、存活出院与存活出院、以及住院者代理值或 SOFA 相同均按并列计半分。数值 0.5、超过 0.5 和低于 0.5 的方向解释也已固定。

观测映射是否成立由治疗标签遮蔽下的准入与忠实度标准决定；不成立而独立分析条件成立时，改用预先定义、与阶段 II 表征无关的 SOFA 有序临床状态端点。两条分支均使用同一概率指数，且选择由结果不可见的资格判定触发，不构成治疗结果驱动的估计目标切换。EXIT-SEP 与 XBJ-SCAP 分别估计，不产生跨试验合并效应；严格胜概率、胜负比或其他量不能替换主要估计目标。

### 未达到标准或未获确认时的后果

后果完整且可执行：原随机化层无法核验，或具名统计负责人未在治疗标签用于任何组间结局计算以及分析计划和代码冻结前确认公式、方向、并列规则、目标分析集、原随机化因素和合并组层权重时，停止相应试验新的访视有序结局主要比较；不得使用事后分层或切换主要估计目标，仅保留原试验终点复现或数据审计。该失败不影响主体阶段 I–II 路线。若实际访视、随机化、中心及死亡、住院或出院语义不能核验，则不开展任何新的访视结局分析。

## 工作假设登记

```yaml
- assumption_id: WA-R117-01
  unconfirmed_detail: 连续潜在状态恢复的固定计算定义及其实现代码尚未取得指定负责人的正式确认。
  working_assumption: >-
    连续分支按 dossier 已固定的唯一定义执行：在同一预定患者—时间评价格点比较真实连续潜在状态矩阵与估计后验均值矩阵；每次重复取覆盖全部真实连续维度的最小非负典型相关；维度不等、秩不足或固定算法无法得到全部相关时该次重复记为 0；以重复均值双侧 95% 正态近似区间下限不低于 0.80 判定情景达标。
  basis_for_planning: >-
    该定义固定了恢复对象、评价格点、维度与秩失败处理、重复级统计量、情景级汇总及阈值；即使复杂候选不能按此晋级，预设的线性、多状态或仅预测路线仍构成最小可行科学路线。
  impact_if_false: >-
    复杂候选不得凭连续状态恢复晋级，只保留预设的线性、多状态或仅预测路线；若结果可见后才改变定义，既有恢复结论失效，并须在结果不可见的重新设计中重新接受独立方法学评估。
  verification_needed: >-
    系统辨识负责人确认计算定义；纵向统计负责人独立复核评价格点、维度与秩处理、重复级和情景级计算代码。
  verification_point: 首次模拟拟合和查看任何恢复结果前，最迟于月 7 模拟方案与代码冻结时。
  affected_design_component: 复杂候选的连续潜在状态恢复判定与模型准入；不影响预设简单表征路线。

- assumption_id: WA-R117-02
  unconfirmed_detail: 每项符合启动条件的试验所用概率指数、目标分析集、原随机化分层与合并组层权重尚未取得具名统计负责人的书面确认及原始资料核对。
  working_assumption: >-
    每项试验唯一采用 dossier 定义的分层标准化概率指数作为新访视有序结局的主要估计目标，并列对两组各计半分；使用经核验的原随机化中心或分层因素以及目标分析集中两组汇总的层样本比例，方向固定为数值越高越有利；其他量仅可预先定义为次要或敏感性分析。
  basis_for_planning: >-
    公式、方向、并列处理、层权重来源、分试验估计和禁止事后替换均已固定；该分析位于主体阶段 I–II 达标后的从属阶段，即使不能实施，阶段 I–II 的最小可行科学路线仍保持完整。
  impact_if_false: >-
    停止相应试验新的访视有序结局主要比较，不得事后改用其他分层或主要估计目标；仅保留原试验终点复现或数据审计，主体阶段 I–II 路线不受影响。
  verification_needed: >-
    具名统计负责人书面确认公式与方向、并列各计半分、目标分析集、原随机化中心或分层因素及合并组层权重，并与原始病例报告表、统计分析计划、随机化资料和数据字典核对。
  verification_point: 每项试验完成核心语义核验后，且在治疗标签用于任何组间结局计算以及分析计划和代码冻结前。
  affected_design_component: 有前置条件的随机试验新访视有序结局主要比较；不影响主体阶段 I–II。
```

两项工作假设均满足继续推进条件：已有不依赖该未确认事项的最小可行科学路线；未确认事项范围有限、可核验且有结果不可见的核验时点；假设不改变核心问题、研究对象、主要测量或推断目标及主张强度；假设不成立时均有不替换主体科学路线的限定后果。它们没有掩盖缺失的核心输入或无效的数据—方法关系。

## 研究身份与主张边界

未发现身份或主张漂移。

- 连续恢复规格只是把既有“可恢复不变量和复杂候选准入”目标操作化；它没有把模拟恢复提升为真实系统识别，也没有用预测性能替代结构恢复。
- 概率指数只用于主体阶段 I–II 达标后的、按试验分开的次要访视结局比较；它不计入或补足阶段 II 成功，也不验证阶段 II 的潜在动力学、转移边或整个模型。
- 研究对象仍是脓毒症中心的纵向重症监护患者系统，主要推断单位仍是患者—时间状态和状态转移；随机试验规格没有把主体目标改成治疗作用、机制、控制或临床决策工具开发。
- 允许解释仍限于相应试验中随机分配与预先定义有序访视结局的差异；跨试验合并效应、共同机制、无条件临床推广和以亚组选择改变主要解释均被排除。

## 方法学交接

- **endpoint_or_metric_status:** 两项新规格均已明确科学功能、计算输入、比较方向、判定时点和失败含义；在负责人按时确认的工作假设下可用于后续方法文件。
- **data_method_fit_status:** 连续恢复仅用于已知模拟真值与同格点后验均值的比较；概率指数仅在随机化、分析集、分层、访视和生存或住院语义核验后使用，二者的数据—方法关系相符。
- **minimal_analysis_route_status:** 已存在。复杂候选不能晋级时保留线性、多状态或仅预测路线；试验新访视比较不能实施时保留主体阶段 I–II，并仅复现原试验终点或报告数据审计。
- **required_repairs:** 无。
- **nonblocking_advice:** 在规定核验时点完成并保存两项负责人确认；确认不得晚于相应结果可见或治疗组比较开始。

## Provenance

```yaml
review_id: methodology-statistics-preflight-I01-001-r117
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id: methodology-statistics-preflight-r117-fresh-01
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r117
input_artifact_ids:
  - idea-dossier-I01-001-v053
input_versions:
  - v053
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/methodology-statistics-preflight/SKILL.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/working-assumption-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/endpoint-metric-checks.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/idea-dossier-v053.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: pass
findings:
  - continuous_latent_state_recovery_statistic_uniquely_computable
  - conditional_trial_probability_index_uniquely_computable
  - working_assumptions_contract_compliant
  - failure_consequences_preserved
  - no_identity_or_claim_drift
unresolved_issues:
  - WA-R117-01 pending confirmation at its specified verification point
  - WA-R117-02 pending confirmation at its specified verification point
```
