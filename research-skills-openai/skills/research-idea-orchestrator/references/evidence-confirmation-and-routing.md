# Evidence Confirmation and Routing

本文件管理进入 workflow 前的 evidence 确认、用户材料 routing、自动检索要求和 clinical evidence 规则。

## 1. Initial User Check

进入 workflow 前，orchestrator 应询问：

```text
是否已有相关文献调研结果、支撑文献、权威综述、指南、科学共识、前沿研究或 research articles？如果有，请提供；如果没有，我会基于当前 idea 自动检索最新相关权威资料来构建 evidence / opportunity map。
```

若用户已经明确提供了材料，不重复询问。

## 2. Accepted Evidence Materials

可作为 evidence map 依据：

- 权威综述；
- 系统综述或 meta-analysis；
- 临床/技术指南；
- 科学共识或 position statement；
- 高质量前沿研究；
- research article 中提取并经验证的研究线索；
- 用户已有文献调研结果；
- 数据库、注册库、benchmark、标准或政策文件；
- funding call 或 priority statement。

## 3. User Provides Review / Guideline / Consensus / Frontier Studies

Routing：

- 将材料作为 primary evidence sources 传递给 `research-opportunity-mapper`。
- 要求 mapper 提取主流方向、争议、空白、方法学瓶颈、评价缺陷和数据机会。
- 标注 evidence confidence。
- 标注文献是否仍需人工核查。

## 4. User Provides Research Article

Research article 不应直接等同于领域证据结论。Routing：

- 将 article 原文或用户提供内容传递给 `research-opportunity-mapper`。
- 要求从原文中抽取研究线索，优先检查 Introduction，也可参考 Discussion、Limitations 和 Future Work。
- 将 article 中的研究线索作为 hypothesis-generating clues。
- 必须用更广泛证据验证线索，包括 review、guideline、consensus、recent studies 或数据库。
- 未验证前，相关 opportunity 的 evidence confidence 不得高于 `low`，novelty risk 应标为 `unverified` 或 `high`。

## 5. User Provides No Materials

如果用户不提供材料：

- 调用 `research-opportunity-mapper` 自动检索最新相关权威综述、指南、科学共识和前沿研究。
- 优先检索高可信来源，再补充近年前沿研究。
- 形成 evidence summary 和 opportunity map。
- 若无法完成检索，必须将 evidence_status 标为 `not_verified`。

## 6. Clinical Idea Evidence Rule

临床相关 idea 必须满足以下任一条件：

- 已联网检索相关 evidence；
- 用户提供了可引用 evidence materials。

若二者均不满足：

- novelty 只能标为 `unverified`；
- guideline alignment 只能标为 `unverified`；
- 不得声称该 idea 与最新指南一致；
- 不得声称该 idea 尚未被研究；
- portfolio 中必须列为 unresolved evidence risk。

## 7. Evidence Confidence Labels

- `high`：多项高质量来源直接支持。
- `moderate`：有直接支持，但来源数量或一致性有限。
- `low`：证据间接、单一或仍需验证。
- `speculative`：主要基于推断或 hypothesis-generating clues。
- `not_verified`：尚未检索或无法确认。
