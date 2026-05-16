# Archival Cleanup (Proposal Pre-Packaging)

## When to use

When a thesis-integrity reviewer report identifies artifacts that must be removed from a proposal before submission — reviewer-response marks, version tags, rhetorical question headings, explanatory reader guides, internal process references. This is the final step between refinement-complete and package-assembly.

The cleanup is **subtractive only**: no new content, no substantive claim changes, no additions. It produces the "submission-clean" version.

## Workflow

### 1. Read the thesis-integrity report

The report provides an itemized list of artifacts organized by category:
- **Reviewer response marks**: "(回应Review Panel MF-1)", "(回应转化评审人)", etc.
- **Version tags**: "V3新增", "V6升级", "V9更新", "V3修正——"
- **Version metadata lines**: "Proposal Version: vX.X | Proposal File: ..."
- **Internal process references**: "已在v6-v7两轮内部Panel测试中验证有效", "8人panel共识" in non-substantive positions
- **Rhetorical question headings**: "**为什么选择TSQN？**" → should be declarative
- **Explanatory reader guides**: "本节阅读指南", "阅读指南：概念翻译表" blocks
- **Terminology dictionaries as standalone body sections**: full tables in §1.2

### 2. Plan patch order: top-to-bottom

Always work from top to bottom of the document to avoid line-number drift confusing later patches. Group patches by section (§1 → §3 → §5 → Unresolved Issues → Appendix).

### 3. Apply patches with verification after each

Use `skill_manage action=patch` for precise find-and-replace. Key rules:
- `old_string` must be unique — include surrounding context (1-2 lines) if needed
- Check diff output after each patch to confirm correctness
- For structural deletions (e.g., removing a 33-line table), replace the entire block with the replacement text in one patch

### 4. Critical: stale cross-reference check

After removing or relocating content, search for references that now point to dead targets:

```
search_files pattern="§1\.2.*概念翻译|概念翻译表.*§1\.2|返回.*§1.2.*概念"
search_files pattern="概念翻译"
```

Common stale references after archival cleanup:
- §3.1.5 referring to "§1.2节开头的概念翻译表" after the table was removed from §1.2
- §2.4 cross-referencing the old appendix title
- Reading guides telling readers to "返回§1.2节开头的概念翻译表"

### 5. Zero-residue verification

After all patches, run exhaustive searches for remaining artifacts:

```
search_files pattern="回应Review|回应.*Panel|回应.*评审人|回应Unresolved"
search_files pattern="v[0-9]新增|V[0-9]升级|V[0-9]更新|V[0-9]修正"
search_files pattern="Proposal Version|Proposal File"
search_files pattern="为什么.*？|本节阅读指南|阅读指南：概念|嵌入论文Table"
```

All counts must be zero for archival cleanup to be complete.

### 6. Produce next version and revision delta

```bash
cp proposal-v{N}.md proposal-v{N+1}.md
```

Changelog format (`06_revisions/round-NNN/revision-delta-rNNN.md`):
- Version header with cleanup source (thesis-integrity report)
- Summary of operations (subtractive only, no substantive changes)
- Category A: reviewer marks removed (count + table of locations/operations)
- Category B: rhetorical question rewrites (before/after table)
- Category C: explanatory section handling (table of operations)
- Line count delta
- Explicit list of items NOT executed (out-of-scope recommendations)

## Pitfalls

- **Stale cross-references**: The most common bug. When you remove §1.2's concept table, §3.1.5's reference to "§1.2节开头的概念翻译表" goes stale. Always run the cross-reference check after removing content.
- **Incomplete search strings**: Use both Chinese and English patterns. "回应Review" catches most but "回应.*8人" catches panel-consensus references.
- **Version metadata reintroduction**: Don't add "Proposal Version: v10.0" back into the cleaned proposal — the filename is the version identifier. The proposal body stays metadata-free.
- **Over-cleaning**: "8人panel共识" in substantive challenge severity descriptions (e.g., `**挑战1（项目级——8人panel共识）**`) is substantive, not just a process reference. Only remove it when it's in a non-substantive position (e.g., "**高（升级为项目级——8人panel共识）**" in the severity column of a risk table, where the parenthetical is pure process metadata).
