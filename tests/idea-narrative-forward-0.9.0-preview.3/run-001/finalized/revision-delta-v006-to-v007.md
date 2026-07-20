---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v006-to-v007
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v001
source_artifact:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v007
  version: v007
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/idea-dossier-v007.md
based_on:
  - artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
  - artifact_id: narrative-repair-plan-I01-001-r005
    version: r005
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/narrative-repair-plan-r005.yaml
  - artifact_id: language-assessment-I01-001-r005
    version: r005
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/language-assessment-r005.md
  - artifact_id: protected-content-register-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/protected-content-register-v006.yaml
change_type: editorial_repair_delta
scientific_content_change: false
method_change: false
threshold_change: false
claim_strength_change: false
created_round: 4
frozen: true
---

# v006 至 v007 修订差异

## 修订范围

本轮仅实施局部编辑修复：补充首次出现术语的简释，统一同一科学对象的名称，改写不自然或不明确的表达，拆分负载过高的句子和表格单元格，并将参考文献注释改为可独立理解的自然中文。未重排章节，未新增科学内容，也未改变方法、数值阈值、主张强度、可行性状态或阶段关系。

## 局部修改记录

| 位置 | v007 的编辑处理 | 保持不变的内容 |
|---|---|---|
| Frontmatter | 更新产物标识、版本、轮次和四项逻辑来源引用；未加入 SHA 或摘要值 | workflow、idea identity、identity anchor、change type 与冻结状态 |
| 跨学科概念桥 | 在首次出现处简释“状态占用”“共同生理锚点预测”和“结构符号或滞后”；说明共同观测指标是一般集合，共同生理锚点是其中用于固定潜在状态含义和尺度的指标 | 四类证据的顺序、对象、条件与分别报告边界 |
| 摘要、缺口、研究问题、核心假设、方法、证据链和产物表 | 将“锚点预测”“锚点层预测”和相关泛称统一为“共同生理锚点预测” | 恢复对象、验证对象和核心假设 |
| 缺口、贡献比较和操作后果 | 将生硬的“运输/运输性”改为“跨数据库可迁移性”或“跨数据库外部适用性”，并明确所指主体 | 跨数据库验证设计及其解释范围 |
| 条件性试验分析及停止条件 | 将“新状态分析/端点”直接写为“一维状态摘要分析”或“独立 SOFA 临床状态分析” | 两个分析分支、资格条件、替代路径和停止后果 |
| 结构稳定性阈值 | 将“自助法保留率”解释为预设状态或结构边在全部自助法重复中被保留的比例 | 80% 阈值及其他全部阈值 |
| 观测模型段落 | 明确缺失随机基线与选择模型基线并列，且显式测量过程适用于二者 | 模型类别、敏感性分析和治疗支持度报告 |
| 摘要与证据解释 | 使 Expected result 的两个报告分支及 interpretation 的判定对象在语法上平行 | 计划结果、分析分支和三种支持状态 |
| 被定位的长句和阈值表 | 仅拆句、增加局部换行并统一编号关系 | 所有条件、阈值、后果和先后顺序 |
| 实现职责与证据链 | 将“重放/账本”改为“可复现比较记录/结果与来源记录”等直接表述 | 记录内容、数据隔离和结果释放职责 |
| 参考文献 3、23、25、38 | 删除旧版本依赖；将英文状态词改为自然中文，同时保留来源身份、文件路径、当前核验范围和证据限制 | 未读取材料仍明确写为未读取，有限核验未写成完整核验 |

## 结构与保护内容核对

- H1 与 Title 保持原文。
- 15 个 H2 保持原有顺序；第三个 H2 下的 5 个 H3 保持原有顺序。
- 5 条 Evidence chain 保持原有顺序及 Input、Transformation、Output、Supports 结构。
- 第 14 节仍是 limitations、可行性发现、解释边界、替代方案和停止条件的唯一完整权威位置。
- 研究身份、主要问题、研究对象、证据基础、推断单位、方法、阈值、主张强度、可行性状态和阶段关系均未改变。

## 输入充分性

四项指定输入对本轮全部局部修复均提供了明确定位、目标表达或保护边界，无需猜测科学内容。
