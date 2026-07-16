#!/usr/bin/env python3
"""Validate the fixed Chinese ROADMAP structure and run mutation self-tests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
ROADMAP = PLUGIN / "ROADMAP.md"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
REGISTRY = PLUGIN / "workflow-registry.yaml"
READINESS = PLUGIN / "reports" / "personal-readiness.json"

EXPECTED_HEADINGS = [
    "文档元数据",
    "产品定位",
    "当前状态",
    "阶段总览",
    "Phase 0：引用与 Registry 闭合",
    "Phase 1：Context 精简",
    "Phase 2：Search 与 Deep Research 路由",
    "Phase 3：工作流状态机闭合",
    "Phase 4：场景评估与持续验证",
    "Phase 5：GitHub Marketplace 安装与更新",
    "Phase 6：维护性与当前版本强化",
    "Phase 7：个人安装与工作流就绪",
    "Phase 8：个人原生研究闭环",
    "当前完成判定",
    "非目标",
]
PHASE_MARKERS = ["- 状态：", "- 优先级：", "- 目标：", "### 已完成", "### 待完成", "### 完成条件"]
ALLOWED_STATUSES = {"已完成", "进行中", "候选"}
FORBIDDEN_TERMS = (
    "Phase 9",
    "Phase 10",
    "阶段 9",
    "阶段 10",
    "Resume packages",
    "resume package",
    "workspace doctor",
    "PHASE7-8-RUNBOOK.md",
    "PREVIEW-EVIDENCE-CAPTURE.md",
    "PROVENANCE.yaml",
    "release-ledger.json",
)
MOJIBAKE_MARKERS = ("\ufffd", "鈥", "銆", "锟", "浼︾", "闅愮")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return value


def validate(text: str, *, version: str, registry: dict[str, Any], readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not text.startswith("# Research Skills OpenAI 路线图\n"):
        errors.append("一级标题必须是固定中文标题")
    headings = re.findall(r"^## (.+)$", text, re.M)
    if headings != EXPECTED_HEADINGS:
        errors.append("二级标题或 Phase 顺序发生漂移")
    phase_numbers = [int(value) for value in re.findall(r"^## Phase (\d+)：", text, re.M)]
    if phase_numbers != list(range(9)):
        errors.append("Phase 编号必须唯一且连续为 0–8")
    for term in FORBIDDEN_TERMS:
        if term.lower() in text.lower():
            errors.append(f"ROADMAP 包含已删除内容：{term}")
    for marker in MOJIBAKE_MARKERS:
        if marker in text:
            errors.append(f"ROADMAP 包含乱码标记：{marker}")

    blocks = re.split(r"(?=^## Phase \d+：)", text, flags=re.M)[1:]
    if len(blocks) != 9:
        errors.append("ROADMAP 必须包含九个 Phase 区块")
    for block in blocks:
        heading = block.splitlines()[0] if block else "<missing>"
        positions = [block.find(marker) for marker in PHASE_MARKERS]
        if any(position < 0 for position in positions):
            errors.append(f"{heading} 缺少统一字段")
        elif positions != sorted(positions):
            errors.append(f"{heading} 字段顺序错误")
        match = re.search(r"^- 状态：`([^`]+)`$", block, re.M)
        if not match or match.group(1) not in ALLOWED_STATUSES:
            errors.append(f"{heading} 使用了无效状态")

    skills = registry.get("skills", [])
    policy = registry.get("public_entry_policy", {})
    reviewer_count = sum(
        1 for item in skills if isinstance(item, dict) and item.get("requires_independent_subagent") is True
    )
    declared_count = len(policy.get("declared_entries", [])) if isinstance(policy, dict) else 0
    implicit_count = len(policy.get("implicit_active_entries", [])) if isinstance(policy, dict) else 0
    observation = readiness.get("owner_observation", {})
    expected_slots = observation.get("expected_slot_count")
    observed_slots = observation.get("owner_observed_slot_count")
    expected_metadata = (
        f"| 当前插件版本 | `{version}` |",
        f"| 当前范围 | {len(skills)} 个 Skill、{reviewer_count} 个独立 Reviewer、5 个完整工作流 |",
        f"| 发现面 | {declared_count} 个声明入口、{implicit_count} 个隐式入口、1 个 explicit-only 入口 |",
        f"| 当前验收状态 | `{readiness.get('personal_status')}`，`{observed_slots}/{expected_slots}` 个 owner-observed 槽位完成 |",
    )
    for line in expected_metadata:
        if line not in text:
            errors.append(f"元数据与机器状态不一致：{line}")

    phase7 = next((block for block in blocks if block.startswith("## Phase 7：")), "")
    if "personal-research-polisher-happy" not in phase7:
        errors.append("Research Polisher 的 owner-observed 槽位必须整合在 Phase 7")
    if "方法学/可发表性 Reviewer" not in phase7 or "explicit-only" not in phase7:
        errors.append("Phase 7 缺少 Research Polisher 的实现与路由边界")
    return errors


def main() -> int:
    try:
        raw = ROADMAP.read_bytes()
        text = raw.decode("utf-8")
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        registry = load_yaml(REGISTRY)
        readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"ROADMAP contract validation failed: {exc}", file=sys.stderr)
        return 1

    version = str(manifest.get("version", ""))
    errors = validate(text, version=version, registry=registry, readiness=readiness)
    mutations = {
        "missing-field": text.replace("- 状态：`已完成`", "", 1),
        "field-order": text.replace("### 已完成", "### __TMP__", 1)
        .replace("### 待完成", "### 已完成", 1)
        .replace("### __TMP__", "### 待完成", 1),
        "duplicate-phase": text + "\n## Phase 8：重复\n",
        "skipped-phase": text.replace("## Phase 4：", "## Phase 5：", 1),
        "removed-phase": text + "\n## Phase 10：不应存在\n",
        "version-drift": text.replace(f"`{version}`", "`0.0.0-invalid`", 1),
        "mojibake": text + "\n\ufffd\n",
    }
    for name, mutated in mutations.items():
        if not validate(mutated, version=version, registry=registry, readiness=readiness):
            errors.append(f"负向自测未拒绝：{name}")
    if errors:
        print("ROADMAP contract validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("ROADMAP contract passed: UTF-8; fixed Chinese structure; Phase 0-8; seven mutation guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
