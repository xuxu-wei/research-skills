---
schema_version: research-idea.v3
plugin_version: "0.10.0"
artifact_id: reference-ledger-I01-001-v001
version_id: v001
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: round-001
idea_id: I01-001
path: 03_ideas/nodes/I01-001/references/reference-ledger.md
source_skill: research-idea-orchestrator
created_by_instance_id: fresh-idea-portfolio-assembler-v001
based_on:
  - artifact_id: evidence-map-v001
    version: v001
    path: 02_evidence/evidence-map-v001.md
  - artifact_id: opportunity-map-v001
    version: v001
    path: 02_evidence/opportunity-map-v001.md
  - artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
  - artifact_id: narrative-assessment-I01-001-r007
    version: r007
    path: 03_ideas/nodes/I01-001/reviews/narrative-assessment-r007.md
  - artifact_id: language-assessment-I01-001-r007
    version: r007
    path: 03_ideas/nodes/I01-001/reviews/language-assessment-r007.md
change_type: create
status: current
frozen: false
---

# I01-001 参考标识登记表

当前 Idea：`I01-001`（受约束的脓毒症全病程动态状态模型：在一个数据库中开发并在异质数据库中外部验证）。本表只提供标识、可读名称与定位，不把内部标识当作科学证据。

| Internal ID | Type | Human-readable label | Definition artifact | Original source | Locator | Version/status |
|---|---|---|---|---|---|---|
| I01-001 | Idea | 受约束的脓毒症全病程动态状态模型：在一个数据库中开发并在异质数据库中外部验证 | [current dossier](../dossiers/idea-dossier-v006.md) | current complete dossier | H1 与 Title 字段 | v006/current; revision required |
| C1 | claim | 成人脓毒症的临床定义与筛查边界 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | Sepsis-3 与 2026 成人指南 | Key Claims, C1 | v001/current |
| C2 | claim | 存在互补的公开成人 ICU 纵向数据 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 数据库官方资料 | Key Claims, C2 | v001/current |
| C3 | claim | 单库内部随机划分不能代替外部验证 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 数据库比较与外部验证研究 | Key Claims, C3 | v001/current |
| C4 | claim | 中国感染 ICU 数据可作地域外部样本但规模与完整性有限 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | PhysioNet 与数据描述论文 | Key Claims, C4 | v001/current |
| C5 | claim | 脓毒症起点与标签细节会改变模型性能 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 标签实现研究与公开代码 | Key Claims, C5 | v001/current |
| C6 | claim | ICU 缺失模式携带照护信息且填补值不是真实生理状态 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 缺失模式研究与 GRU-D | Key Claims, C6 | v001/current |
| C7 | claim | 脓毒症静态亚型、轨迹与多状态病程已有研究 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 代表性表型与轨迹研究 | Key Claims, C7 | v001/current |
| C8 | claim | ICU 与脓毒症已有状态空间、动态网络、强化学习和数字孪生原型 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 代表性方法研究 | Key Claims, C8 | v001/current |
| C9 | claim | 电子病历时间关联或网络权重不能自动解释为干预因果作用 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 因果方法与动态网络研究 | Key Claims, C9 | v001/current |
| C10 | claim | 原设想四类成功标准属于不同估计任务 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | TRIPOD+AI 与 PROBAST+AI | Key Claims, C10 | v001/current |
| C11 | claim | ICU 预测模型外部迁移后常有性能与校准下降 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 外部验证综述与实例 | Key Claims, C11 | v001/current |
| C12 | claim | EXIT-SEP 是中国多中心安慰剂对照随机试验 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | EXIT-SEP 主报告 | Key Claims, C12 | v001/current |
| C13 | claim | XBJ-SCAP 的疾病范围不同于一般脓毒症队列 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | XBJ-SCAP 主报告 | Key Claims, C13 | v001/current |
| C14 | claim | EXIT-SEP 已有 SENECA 四表型事后异质性分析 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | EXIT-SEP 表型事后分析 | Key Claims, C14 | v001/current |
| C15 | claim | 随机分配不自动识别中介网络且亚组差异需交互检验 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | AGReMA 与 CONSORT 2025 | Key Claims, C15 | v001/current |
| C16 | claim | 2026 成人脓毒症指南对血必净持审慎立场 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 2026 成人指南 | Key Claims, C16 | v001/current |
| C17 | claim | 动物验证应遵循脓毒症模型和动物报告规范且转化证据冲突 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | MQTiPSS、ARRIVE 2.0 与冲突研究 | Key Claims, C17 | v001/current |
| C18 | claim | “首个完整系统”主张目前未核实 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 有界检索与最近邻来源 | Key Claims, C18 | v001/current; unverified |
| C19 | claim | 试验原始数据与公共数据库项目级可用性尚未核实 | [evidence map](../../../../02_evidence/evidence-map-v001.md) | 用户资源陈述与数据库条件 | Key Claims, C19 | v001/current; unverified |
| O1 | opportunity | 把四类目标拆成可复核的纵向任务基准 | [opportunity map](../../../../02_evidence/opportunity-map-v001.md) | evidence map | Opportunities, O1 | v001/current |
| O2 | opportunity | 构建受约束且可辨识性明确的动态状态表示 | [opportunity map](../../../../02_evidence/opportunity-map-v001.md) | evidence map | Opportunities, O2 | v001/current |
| O3 | opportunity | 把跨数据库可迁移性设为主要贡献之一 | [opportunity map](../../../../02_evidence/opportunity-map-v001.md) | evidence map | Opportunities, O3 | v001/current |
| O4 | opportunity | 把缺失值填补与潜在状态估计分开评价 | [opportunity map](../../../../02_evidence/opportunity-map-v001.md) | evidence map | Opportunities, O4 | v001/current |
| O5 | opportunity | 把既有动态表型作为比较基准和稳定性压力测试 | [opportunity map](../../../../02_evidence/opportunity-map-v001.md) | evidence map | Opportunities, O5 | v001/current |
| O6 | opportunity | 冻结公开数据模型后再开展条件性随机试验二次分析 | [opportunity map](../../../../02_evidence/opportunity-map-v001.md) | evidence map | Opportunities, O6 | v001/current; conditional |
| O7 | opportunity | 只为一个预定机制假设设计可选动物桥接研究 | [opportunity map](../../../../02_evidence/opportunity-map-v001.md) | evidence map | Opportunities, O7 | v001/current; conditional |
| WA-01 | working assumption | 核心实证研究可独立形成论文，后续研究可另文或后续整合 | [current dossier](../dossiers/idea-dossier-v006.md) | current dossier | Working assumptions, WA-01 | v006/open until month 3 |
| WA-02 | working assumption | 第三数据库仅在两库结果锁定且资源允许时作压力测试 | [current dossier](../dossiers/idea-dossier-v006.md) | current dossier | Working assumptions, WA-02 | v006/open until month 12 |
| NAR-001 | narrative finding | Background 提前承担 Rationale 的方案选择功能 | [narrative assessment](../reviews/narrative-assessment-r007.md) | fresh narrative review | Findings, NAR-001 | r007/open minor |
| NAR-002 | narrative finding | “持续恢复”的技术含义晚于多次核心使用 | [narrative assessment](../reviews/narrative-assessment-r007.md) | fresh narrative review | Findings, NAR-002 | r007/open minor |
| NAR-003 | narrative finding | 开篇定义段混合读者入口与方法细节 | [narrative assessment](../reviews/narrative-assessment-r007.md) | fresh narrative review | Findings, NAR-003 | r007/open minor |
| NAR-004 | narrative finding | Working assumptions 中任务三说明重复且不符合小节功能 | [narrative assessment](../reviews/narrative-assessment-r007.md) | fresh narrative review | Findings, NAR-004 | r007/open minor |
| LANG-001 | language finding | 外部状态表示相关术语的修饰对象与“占用”含义不够直接 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-001 | r007/open minor |
| LANG-002 | language finding | 任务三预测目标的限定语叠加且角色形式不一致 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-002 | r007/open minor |
| LANG-003 | language finding | 参数和潜在状态恢复诊断的并列范围有歧义 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-003 | r007/open minor |
| LANG-004 | language finding | “人体开放复杂巨系统”标签不透明且装饰性较强 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-004 | r007/open minor |
| LANG-005 | language finding | 单句完整构想摘要的从句链负担过重 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-005 | r007/open minor |
| LANG-006 | language finding | 任务三说明泄露对话来源，不符合自足学术语域 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-006 | r007/open minor |
| LANG-007 | language finding | 条件性后续研究独立性的表达含连续否定与分支隐喻 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-007 | r007/open minor |
| LANG-008 | language finding | MQTiPSS 与 ARRIVE 2.0 首次使用缺少用途说明 | [language assessment](../reviews/language-assessment-r007.md) | fresh language review | findings, LANG-008 | r007/open minor |
| CM-ARTICLE-01 | journal candidate | Communications Medicine — Article；核心实证研究论文 | [candidate brief](../reviews/candidate-journal-match-r008.yaml) | official scope and article-type sources | candidates, CM-ARTICLE-01 | r008/confirmed by independent medical review |

## Current logical references

| Role | Artifact ID | Version | Path |
|---|---|---|---|
| Current dossier | idea-dossier-I01-001-v006 | v006 | `03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md` |
| Qualifying evaluation | evaluation-I01-001-r008 | r008 | `03_ideas/nodes/I01-001/reviews/evaluation-r008.md` |
| Candidate journal match | candidate-journal-match-I01-001-r008 | r008 | `03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml` |
| Medical journal review | medical-journal-review-I01-001-r008 | r008 | `03_ideas/nodes/I01-001/reviews/medical-journal-review-r008.md` |
