# Novelty Claim Rules

Novelty claim 必须受 Evidence Map 限制。

## Allowed levels

- `supported`: 有 evidence map 中的直接或多来源支持。
- `plausible`: 有间接证据，但仍需验证。
- `unverified`: 证据不足或尚未完成外部验证。
- `speculative`: 主要来自推测、单篇文章线索或假设挑战。

## Rules

- 单篇 research article 的 Introduction / Discussion 只能生成 clue，不足以支持 high-confidence novelty。
- 临床相关 idea 若无联网 evidence 或用户提供 evidence，novelty 与 guideline alignment 必须标为 `unverified`。
- 不得使用 “first”, “novel”, “unprecedented”, “never studied” 等强表述，除非 Evidence Map 明确支持。
- 若 evidence limitations 明确存在，idea 必须继承相关 uncertainty。
