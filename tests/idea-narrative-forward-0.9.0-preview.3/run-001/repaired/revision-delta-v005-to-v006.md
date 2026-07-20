---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v005-to-v006
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v001
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v005
  version: v005
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
based_on:
  - artifact_id: idea-dossier-I01-001-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
  - artifact_id: narrative-repair-plan-I01-001-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/narrative-repair-plan-r003.yaml
  - artifact_id: language-assessment-I01-001-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/language-assessment-r003.md
  - artifact_id: protected-content-register-I01-001-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/protected-content-register-v005.yaml
scientific_change: false
method_change: false
threshold_change: false
claim_strength_change: false
frozen: true
---

# v005 到 v006 的编辑修订差异

本次变更仅修复叙事分工、术语可及性、中文表达和信息归属；研究身份、数据条件、方法、估计目标、阶段顺序、数值阈值、失败后果、科学证伪标准、参考文献证据状态与主张强度均未改变。

| 修订区域 | v006 的编辑处理 | 保持不变的内容 |
|---|---|---|
| 标题与开篇 | 将“计划性”改为“预先设定的”，缩短入口句，并增加不含公式或阈值的概念桥 | 全病程研究对象、24 个月阶段 I–II、条件性阶段 III 和候选模型定位 |
| 核心术语 | 区分跨时间验证、按未参与开发医院开展的验证与跨数据库外部验证；首次直释一维状态摘要；统一使用“观测映射”；把宽泛的“状态量/结构量/模型量”展开为具体评价对象；将非固定标题中的 `dated gates`、`Conjunctive` 和 `Frozen` 改为直接描述里程碑、全部必要证据和预先设定映射的用语 | 验证轴、映射来源、数值方向、评价对象及其科学含义；固定 H2、条件、阈值和方法均未改变 |
| 六个强制功能 H2 | 分别限定为完整科学设计、独有实现职责、五条审计映射、验收与记录要求、计划产物与科学证伪标准、有界贡献与最接近工作；逐主张表继续承担合同审计 | 15 个 H2 的名称和顺序、第三节五个 H3、五条证据链对应的目标及全部独有信息 |
| 限制与停止条件 | 删除其他章节中的完整重复，将全部限制、可行性发现、解释边界、替代方案和停止后果集中在第 14 节 | 原有边界、触发条件、数值阈值、替代方案和停止后果 |
| 阈值呈现 | 在第 14 节按评价对象换行或编号，并补全比例分母、随机种子计数和评价量 | 所有比较方向与数值 |
| 支持状态与来源 | 为 `supported`、`qualified`、`none` 增加一次中文图例；参考文献的版本、来源和证据状态原样保留 | 各主张的支持状态与文献记录 |

未新增数据、方法、证据、结果或外部来源；未把计划工作写成已完成，也未改变任何可行性状态。
