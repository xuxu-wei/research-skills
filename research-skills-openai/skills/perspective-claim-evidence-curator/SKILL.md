---
name: perspective-claim-evidence-curator
description: "Build and maintain Perspective claim, evidence, contrary-evidence, citation-risk, and approved-change artifacts before drafting."
---
# perspective-claim-evidence-curator

## Purpose

集中管理 Perspective 文章中每一个核心主张的证据基础。不是"找文献"，而是做 argument-support mapping——确保每条主张都有匹配的证据、已知反证、标注的强度和适用边界。**claim-ledger 的唯一写入者**。

## Core Rules

- claim-ledger.md 和 claim-evidence-matrix.md 是本模块独占写入的文件
- 所有证据评价使用二维体系：evidence strength + evidence directness
- 主动寻找反证——不只收集支持性证据
- 每条 claim 必须标注 allowed claim strength 和 overclaim risk
- Lite Mode：仅做 provisional claim-ledger，不启动检索，缺失证据标注 gap
- 每条 reference 必须记录来源标识（DOI/PMID/URL/用户材料）、支持的 Claim ID、支持句、引用风险；无法验证来源时标注 `unverified`
- 每次来源使用必须有唯一 Binding ID，记录 source intent、允许支撑的具体命题、原文 locator、允许的 claim strength 和禁止外推；同一来源支持不同命题时建立不同 binding
- Input Brief 中的 source intent 只是 provisional intake；只有 curator 可以把它核验为可供 architect/drafter 使用的 binding
- LLM-facing 来源与产物只使用逻辑身份、路径、版本、来源标识和 locator；不得要求或生成 SHA、content hash 或 digest
- 调用外部检索工具时，使用环境中已注册 skill 或 orchestrator 批准的替代路径

## I/O Contract

```
Allowed Inputs:
  - 01-input-brief.md
  - target-outlet-profile.md
  - 用户提供的证据材料

Required Outputs:
  - claim-ledger.md（初始创建）
  - claim-evidence-matrix.md
  - evidence-map.md（如触发检索）
  - evidence-limitations.md
  - citation-risk-log.md
  - contrary-evidence-log.md
  - existing-discourse-baseline.md
  - reference-list.md

May Read:
  - 00_input/ 目录下所有文件
  - 用户提供的证据文件

May Write:
  - 01_claims/ 目录下所有文件（独占写入权）
  - 02_evidence/ 目录下所有文件

Must Not Read:
  - 任何 draft 文件
  - 任何 evaluation 文件

Must Not Write:
  - 00_input/ 目录下文件
  - draft 内容

May Call:
  - focused-literature-synthesizer（精读 2–5 篇论文的有界问题）
  - research-landscape-mapper（A/B 路径，按需——如 skill 在环境中可用）
  - ChatGPT/Codex 内置 Search；多阶段综合任务可由 orchestrator 路由至 Deep Research

Must Not Call:
  - 任何评价型 skill
  - drafter / architect

Failure Modes:
  - 证据不足无法支撑核心 claim → 在 ledger 中标注 claim_strength=speculative，记录 gap
  - 检索返回空 → 记录 evidence-limitations，不做假证据

Escalation Route:
  - 证据缺口阻塞后续 → 上报 orchestrator，附带 gap report
```

## Procedure

### 1. Extract Candidate Claims

从 Input Brief 中抽取所有核心主张，分配给每一主张一个唯一 Claim ID（C1, C2, ...）。

### 2. Create Claim Ledger

在 `01_claims/claim-ledger.md` 创建初始账本。每条 claim 记录：

- Claim text, Claim type (empirical/conceptual/normative/translational/policy), Claim strength (strong/moderate/weak/speculative/preliminary), Supported by, Contrary evidence, Boundary condition, Allowed/Forbidden wording, Status (keep/weaken/delete/move_to_future_agenda), Last modified.

### 3. Match Evidence to Claims

为每条 claim 匹配证据。每条记录须结构化标注：Claim ID, Evidence ID, Binding ID, Source intent, Bound proposition, Original-source locator, Evidence strength, Evidence directness, Allowed claim strength, Forbidden use, Overclaim risk, Citation risk, Contrary evidence, Boundary condition, Verification status.

`source intent` 仅可取：`background_context | direct_claim_support | premise_support | contrary_evidence | boundary_condition | method_example | illustrative_only`。不得把 `background_context`、`method_example` 或 `illustrative_only` 无声升级为核心主张证据。

### 4. Evidence Strength Grading (二维)

**维度 A：Evidence Strength**
- strong: 多项独立研究一致支持
- moderate: 有研究支持但存在局限
- weak: 仅有初步证据或间接推断
- conceptual: 基于理论推导，无直接经验证据
- illustrative: 说明性目的，非证据性支撑

**维度 B：Evidence Directness**
- direct: 证据直接支撑该主张
- adjacent: 证据支撑相近主张
- indirect: 证据支撑前提或部分要素
- analogical: 来自类比领域
- illustrative_only: 纯说明性

### 5. Collect Contrary Evidence

主动寻找反证 → `contrary-evidence-log.md`。记录：反证内容、来源、挑战的 claim、严重程度。

### 6. Citation Risk Assessment

→ `citation-risk-log.md`。检查：过度外推、二手引用、旧文献、引用不支持主张。

### 7. Build Discourse Baseline

→ `existing-discourse-baseline.md`：当前主流叙事、已有类似观点、本文差异、真正新贡献。如未检索标注 `provisional`。

### 8. Build Reference List

→ `reference-list.md`：GB/T 7714—2015 完整引用、可点击的完整链接、来源标识（DOI/PMID/PMCID/ISBN/用户材料）、Binding ID、source intent、用于哪个 claim、允许支持的具体论述、原文 locator、禁止外推、检索/验证日期、风险。

### 9. Trigger Retrieval (Standard/Full Mode)

先记录 `evidence_change_assessment`：已有证据可用时复用；单一引用或主张核对使用内建 Search，需精读 2–5 篇全文时调用 `focused-literature-synthesizer`；只有核心主张、创新定位、证据格局或重大冲突发生实质改变时才调用 `research-landscape-mapper`。Lite Mode 跳过。

## Lite Mode

- 仅做 provisional claim-ledger（strength=preliminary）
- 不启动检索，缺失证据标注 gap
- discourse-baseline 基于已知文献（标注 provisional）

## Pitfalls

- 只找支持性证据：必须主动找反证
- 强证据错配：强 evidence strength + 低 directness = 高危
- claim-ledger 膨大：不是越多越好
- 未标注 directness
- 来源有引用但没有命题绑定，或同一 binding 被改作不同用途

## References

- Read `references/claim-type-taxonomy.md` when its named guidance or contract applies.
- Read `references/evidence-grading.md` when its named guidance or contract applies.
- Read `references/citation-risk-checklist.md` when its named guidance or contract applies.
- Read `references/claim-change-request-template.md` when its named guidance or contract applies.
