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
README = PLUGIN / "README.md"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
REGISTRY = PLUGIN / "workflow-registry.yaml"
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
    "Phase 9：跨工作流人类可读性",
    "当前完成判定",
    "非目标",
]
PHASE_MARKERS = ["- 状态：", "- 优先级：", "- 目标：", "### 已完成", "### 完成条件"]
ALLOWED_STATUSES = {"已完成", "进行中", "候选"}
FORBIDDEN_TERMS = (
    "Phase 10",
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


def validate(text: str, *, version: str, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not text.startswith("# Research Skills OpenAI 路线图\n"):
        errors.append("一级标题必须是固定中文标题")
    headings = re.findall(r"^## (.+)$", text, re.M)
    if headings != EXPECTED_HEADINGS:
        errors.append("二级标题或 Phase 顺序发生漂移")
    phase_numbers = [int(value) for value in re.findall(r"^## Phase (\d+)：", text, re.M)]
    if phase_numbers != list(range(10)):
        errors.append("Phase 编号必须唯一且连续为 0–9")
    for term in FORBIDDEN_TERMS:
        if term.lower() in text.lower():
            errors.append(f"ROADMAP 包含已删除内容：{term}")
    for marker in MOJIBAKE_MARKERS:
        if marker in text:
            errors.append(f"ROADMAP 包含乱码标记：{marker}")

    blocks = re.split(r"(?=^## Phase \d+：)", text, flags=re.M)[1:]
    if len(blocks) != 10:
        errors.append("ROADMAP 必须包含十个 Phase 区块")
    for block in blocks:
        heading = block.splitlines()[0] if block else "<missing>"
        pending_marker = "### 可选复验" if heading.startswith(("## Phase 7：", "## Phase 8：")) else "### 待完成"
        markers = [*PHASE_MARKERS[:-1], pending_marker, PHASE_MARKERS[-1]]
        positions = [block.find(marker) for marker in markers]
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
    expected_metadata = (
        f"| 当前插件版本 | `{version}` |",
        f"| 当前范围 | {len(skills)} 个 Skill、{reviewer_count} 个独立 Reviewer、5 个完整工作流 |",
        f"| 发现面 | {declared_count} 个声明入口、{implicit_count} 个隐式入口、1 个 explicit-only 入口 |",
        "| 当前路线图状态 | Phase 0–9 均已完成；已完成 Phase 只作为历史记录，不自动复验 |",
    )
    for line in expected_metadata:
        if line not in text:
            errors.append(f"元数据与机器状态不一致：{line}")

    phase7 = next((block for block in blocks if block.startswith("## Phase 7：")), "")
    phase8 = next((block for block in blocks if block.startswith("## Phase 8：")), "")
    phase9 = next((block for block in blocks if block.startswith("## Phase 9：")), "")
    if "personal-research-polisher-happy" not in phase7:
        errors.append("Research Polisher 的 owner-observed 槽位必须整合在 Phase 7")
    if "方法学/可发表性 Reviewer" not in phase7 or "explicit-only" not in phase7:
        errors.append("Phase 7 缺少 Research Polisher 的实现与路由边界")
    if "- 状态：`已完成`" not in phase7 or "- 优先级：`P0 已关闭`" not in phase7:
        errors.append("Phase 7 必须按所有者决定标记为已完成并关闭 P0")
    if "### 可选复验" not in phase7:
        errors.append("Phase 7 必须把严格运行档案标记为可选复验")
    if "- 状态：`已完成`" not in phase8 or "- 优先级：`按需复验`" not in phase8:
        errors.append("Phase 8 必须标记为已完成且仅按需复验")
    if "### 可选复验" not in phase8:
        errors.append("Phase 8 必须把严格原生闭环标记为可选复验")
    if "不得自动恢复" not in phase8 or "仅在所有者明确要求时" not in phase8:
        errors.append("Phase 8 必须禁止自动恢复并要求所有者显式重开")
    for marker in (
        "research-narrative-assessor",
        "academic-language-assessor",
        "一个 YAML writer brief",
        "不把 SHA/Digest 写入 LLM-facing 合同",
        "#### Proposal",
        "#### Perspective",
        "#### Article",
        "install-local",
        "tests/0.10.0-{workflow}/",
        "tests/0.11.0-{workflow}/",
        "Hermes",
    ):
        if marker not in phase9 and marker != "Hermes":
            errors.append(f"Phase 9 缺少当前验收合同：{marker}")
    if "- 状态：`已完成`" not in phase9 or "- 优先级：`P0 已关闭`" not in phase9:
        errors.append("Phase 9 必须在当前 forward tests 通过后标记为已完成并关闭 P0")
    edge_count = len(registry.get("workflow_edges", []))
    if f"{edge_count} 条工作流边" not in text:
        errors.append("ROADMAP 工作流边计数与 Registry 不一致")
    priorities = (
        "`P1`：规范 Deep Research 接续包",
        "deep-research-request-vNNN.md",
        "deep-research-follow-up-guide-vNNN.md",
        "`P2`：仅在 OpenAI 插件",
        "同步到 Hermes",
    )
    for phrase in priorities:
        if phrase not in text:
            errors.append(f"ROADMAP 缺少后续优先事项：{phrase}")
    return errors


def validate_readme(text: str, *, version: str, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    normalized = " ".join(text.split())
    forbidden = (
        "The immediate priorities are deliberately small:",
        "part of the pending Phase 7 distribution slot",
    )
    for phrase in forbidden:
        if phrase in normalized:
            errors.append(f"README 仍声明已关闭的 Phase 7–8 优先任务：{phrase}")
    required = (
        "Historical Roadmap phases remain closed records",
        "unless the owner explicitly reopens it",
        "research-narrative-assessor",
        "new LLM-facing interfaces do not persist hashes",
        "Completed Roadmap phase suites are historical",
    )
    for phrase in required:
        if phrase not in normalized:
            errors.append(f"README 缺少所有者接受或按需复验声明：{phrase}")
    skills = registry.get("skills", [])
    declared = registry.get("public_entry_policy", {}).get("declared_entries", [])
    private_count = len(skills) - len(declared)
    inventory = (
        f"contains {len(skills)} skills",
        f"The maintained `{version}` source contains {len(skills)} skill contracts",
        f"The other {private_count} private roles",
    )
    for phrase in inventory:
        if phrase not in normalized:
            errors.append(f"README 库存与 Registry 不一致：{phrase}")
    development = (
        "python -m venv .venv",
        "python scripts/openai_plugin_dev.py install-local",
        f"verify --channel local --expected-version {version}",
        f"verify --channel github --expected-version {version}",
        "After every Skill change, rerun `install-local` and start a new Codex task.",
        "Keep exactly one channel enabled",
        "Never commit or push a `+codex.local-*` version.",
    )
    for phrase in development:
        if phrase not in normalized:
            errors.append(f"README 缺少开发调试闭环：{phrase}")
    if "python scripts/update_openai_plugin_cachebuster.py" in normalized:
        errors.append("README 不得再指导修改源码 cachebuster")
    return errors


def main() -> int:
    try:
        raw = ROADMAP.read_bytes()
        text = raw.decode("utf-8")
        readme_text = README.read_text(encoding="utf-8")
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        registry = load_yaml(REGISTRY)
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"ROADMAP contract validation failed: {exc}", file=sys.stderr)
        return 1

    version = str(manifest.get("version", ""))
    errors = validate(text, version=version, registry=registry)
    errors.extend(validate_readme(readme_text, version=version, registry=registry))
    mutations = {
        "missing-field": text.replace("- 状态：`已完成`", "", 1),
        "field-order": text.replace("### 已完成", "### __TMP__", 1)
        .replace("### 待完成", "### 已完成", 1)
        .replace("### __TMP__", "### 待完成", 1),
        "duplicate-phase": text + "\n## Phase 9：重复\n",
        "skipped-phase": text.replace("## Phase 4：", "## Phase 5：", 1),
        "removed-phase": text + "\n## Phase 10：不应存在\n",
        "version-drift": text.replace(f"`{version}`", "`0.0.0-invalid`", 1),
        "mojibake": text + "\n\ufffd\n",
    }
    for name, mutated in mutations.items():
        if not validate(mutated, version=version, registry=registry):
            errors.append(f"负向自测未拒绝：{name}")
    if errors:
        print("ROADMAP contract validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("ROADMAP contract passed: UTF-8; fixed Chinese structure; Phase 0-9; seven mutation guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
