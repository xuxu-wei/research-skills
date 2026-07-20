---
schema_version: research-idea-journal-match-review.v1
review_id: medical-journal-review-I01-001-r008
reviewer_skill: medical-journal-review
reviewer_instance_id: fresh-medical-journal-review-I01-001-r008-20260720T163512+0800
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r008
review_route: idea_journal_match_editorial_review
reviewed_idea_ref:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
candidate_brief_ref:
  artifact_id: candidate-journal-match-I01-001-r008
  version: r008
  path: 03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml
files_read:
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml
instructions_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/medical-journal-review/SKILL.md
  - research-skills-openai/skills/medical-journal-review/references/idea-journal-match-editorial-route.md
  - research-skills-openai/skills/medical-journal-review/templates/idea-journal-match-review.md
external_urls_consulted:
  - source_id: CM-SCOPE-INDEPENDENT-01
    url: https://www.nature.com/commsmed/aims
    publisher_or_journal: Communications Medicine, Nature Portfolio
    page_type: aims_and_scope
    checked_at: 2026-07-20T16:35:12+08:00
    source_status: 当前官方页面；正文未展示或使用影响因子、排名、录用率、审稿速度或引用指标
  - source_id: CM-TYPE-INDEPENDENT-01
    url: https://www.nature.com/commsmed/submit/content-types
    publisher_or_journal: Communications Medicine, Nature Portfolio
    page_type: article_types
    checked_at: 2026-07-20T16:35:12+08:00
    source_status: 当前官方页面；Article 定义可直接核验，正文未展示或使用影响因子、排名、录用率、审稿速度或引用指标
isolation_mode: fresh_subagent
evaluator_report_visible: false
evaluator_scores_visible: false
source_edits_performed: false
publication_probability_assessment: null
decision: journal_candidates_confirmed
candidate_dispositions:
  - candidate_id: CM-ARTICLE-01
    publication_unit:
      unit_id: core_empirical_study_manuscript
      dossier_locator: "Research content and work packages > 4. 敏感性、复现与论文；Expected outputs，第 6 项"
      whole_idea_reason: null
    submitted_journal: Communications Medicine
    submitted_article_type: Article
    disposition: confirmed
    rationale: >-
      该出版单元是完成公开成人重症监护纵向数据库开发、异质数据库外部验证、敏感性分析和独立复现后的原创实证论文。期刊当前官方范围明确覆盖临床与转化研究、医学与计算科学的交叉研究、观察性临床或流行病学研究，以及具有显著临床或转化意义的新方法、技术或资源；本研究以成人重症监护脓毒症病程、临床结局和跨数据库验证为中心，方法学贡献服务于明确的医学问题，因此主题和研究设计与该范围相符。官方内容类型页面将 Article 定义为原创、重要且高质量的研究，可容纳短篇至深入研究，和 dossier 所指的完整核心实证论文一致。
    mismatch_risks:
      - 当前 dossier 描述的是拟开展研究，而期刊要求最终结果具有新颖性、结论证据充分、数据技术可靠，并构成可能影响本领域认识的进展；若两库资格、外部验证或独立复现未达到预定标准，最终稿的适配度会显著下降。
      - 医学与计算科学交叉稿件的核心进展须对医学界有意义；若最终稿主要呈现模型复杂性而未清楚界定脓毒症预测用途、外部迁移失败边界和临床解释，可能被视为临床意义不足。
      - Article 的官方建议篇幅约为 5,000 词；四项任务、跨数据库状态表示诊断、观测过程诊断、敏感性分析和复现结果可能难以全部在正文中充分呈现，需要严格压缩正文并将可复核技术细节置于补充材料。
    official_source_ids:
      - CM-SCOPE-INDEPENDENT-01
      - CM-TYPE-INDEPENDENT-01
replacement_candidates: []
unresolved_issues: []
---

# Idea 期刊候选独立审查

## 范围与隔离

- 审查的 Idea 逻辑引用：`idea-dossier-I01-001-v006`，版本 `v006`，路径 `03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md`
- 候选 brief 逻辑引用：`candidate-journal-match-I01-001-r008`，版本 `r008`，路径 `03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml`
- Evaluator 报告可见：`false`
- Evaluator 分数可见：`false`
- 项目文件读取范围：仅 front matter 中 `files_read` 列出的两个冻结输入
- 审查范围：只判断候选期刊和文章类型与预期论文的编辑适配性；不评价 Idea 分数，不估计发表概率，也不改变源产物

## 查阅的官方来源

| Source ID | 官方期刊或出版商 URL | 页面类型 | 来源状态 | 核验时间 |
|---|---|---|---|---|
| CM-SCOPE-INDEPENDENT-01 | https://www.nature.com/commsmed/aims | Aims & Scope | 当前官方页面；仅使用范围和发表标准正文，未使用任何禁用指标 | 2026-07-20T16:35:12+08:00 |
| CM-TYPE-INDEPENDENT-01 | https://www.nature.com/commsmed/submit/content-types | Article types | 当前官方页面；直接核验 Article 定义，未使用任何禁用指标 | 2026-07-20T16:35:12+08:00 |

## 候选处置

| Candidate ID | 出版单元与 dossier 定位 | 候选期刊与文章类型 | 处置 | 独立适配理由 | 不匹配风险 | 官方来源 IDs |
|---|---|---|---|---|---|---|
| CM-ARTICLE-01 | `core_empirical_study_manuscript`；Research content and work packages > 4. 敏感性、复现与论文；Expected outputs，第 6 项 | Communications Medicine；Article | `confirmed` | 预期产物是成人重症监护脓毒症纵向数据建模及异质数据库外部验证的原创实证论文。官方范围同时覆盖临床研究、观察性研究、医学与计算科学交叉研究及具有临床意义的新方法；Article 用于原创、重要且高质量的研究，和该出版单元一致。 | 最终结果必须形成证据充分且对医学界有意义的进展；以方法复杂性替代临床贡献会削弱适配；约 5,000 词的建议篇幅会限制四项任务及多组诊断的正文展开。 | CM-SCOPE-INDEPENDENT-01；CM-TYPE-INDEPENDENT-01 |

## 替代候选

无。提交候选已获得当前官方范围和文章类型页面的充分支持，没有触发替换检索。

## 决定与未解决事项

- 决定：`journal_candidates_confirmed`
- 未解决事项：无。该确认是对 dossier 所定义预期论文的编辑适配判断；最终稿仍须以实际完成的两库研究、外部验证和独立复现结果满足期刊公开的质量与重要性标准。

