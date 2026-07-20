#!/usr/bin/env python3
"""Audit the research-perspective skill package.

Checks:
- each SKILL.md has frontmatter with name and a bounded description
- relative Markdown references in `references/...` and `templates/...` exist
- orchestrator Lite mode includes STEP 2-lite before STEP 3
- orchestrator no longer hard-codes /home/ubuntu paths
- every skill directory has agents/openai.yaml
- review panel documents conditional reviewers

This script intentionally uses only the Python standard library.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "research-skills-openai" / "skills"
PERSPECTIVE_SKILLS = {
    "perspective-argument-architect",
    "perspective-claim-evidence-curator",
    "perspective-drafter",
    "perspective-evaluator",
    "perspective-final-compositor",
    "perspective-input-builder",
    "perspective-orchestrator",
    "perspective-refinement-controller",
    "perspective-review-panel",
}


def skill_files() -> list[Path]:
    return [ROOT / name / "SKILL.md" for name in sorted(PERSPECTIVE_SKILLS)]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fm: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm


def check_frontmatter() -> list[str]:
    issues: list[str] = []
    for skill in skill_files():
        fm = parse_frontmatter(skill)
        rel = skill.relative_to(ROOT).as_posix()
        if not fm.get("name"):
            issues.append(f"{rel}: missing frontmatter name")
        desc = fm.get("description", "").strip("'\"")
        if not desc:
            issues.append(f"{rel}: missing frontmatter description")
        elif len(desc) > 1024:
            issues.append(f"{rel}: description exceeds 1024 characters")
    return issues


def check_markdown_references() -> list[str]:
    issues: list[str] = []
    ref_pattern = re.compile(r"`((?:references|templates)/[^`]+\.md)`")
    for name in sorted(PERSPECTIVE_SKILLS):
        for md in sorted((ROOT / name).rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            for match in ref_pattern.finditer(text):
                target = md.parent / match.group(1)
                if not target.exists():
                    issues.append(
                        f"{md.relative_to(ROOT).as_posix()}: missing {match.group(1)}"
                    )
    return issues


def check_orchestrator_invariants() -> list[str]:
    issues: list[str] = []
    orchestrator = ROOT / "perspective-orchestrator" / "SKILL.md"
    text = orchestrator.read_text(encoding="utf-8")
    if "/home/ubuntu" in text:
        issues.append("perspective-orchestrator/SKILL.md: hard-coded /home/ubuntu path")
    if "provisional claims/evidence" not in text:
        issues.append("perspective-orchestrator/SKILL.md: Lite mode must retain provisional claim/evidence preprocessing")
    if "fresh independent subagents" not in text or "independent_review_pending" not in text:
        issues.append("perspective-orchestrator/SKILL.md: missing fresh delegation and unavailable-reviewer routing")
    for marker in ("`article-cover-letter`", "08_cover-letter/", "publication probability"):
        if marker not in text:
            issues.append(f"perspective-orchestrator/SKILL.md: missing Cover Letter route marker {marker}")
    return issues


def check_cover_letter_contract() -> list[str]:
    issues: list[str] = []
    naming = (ROOT / "perspective-orchestrator/references/artifact-naming-and-directory-rules.md").read_text(encoding="utf-8")
    io_contract = (ROOT / "perspective-orchestrator/references/io-contracts.md").read_text(encoding="utf-8")
    compositor = (ROOT / "perspective-final-compositor/SKILL.md").read_text(encoding="utf-8")
    for marker in (
        "08_cover-letter/cover-letter-v001.md",
        "08_cover-letter/cover-letter-quality-check-v001.md",
        "08_cover-letter/medical-journal-cover-letter-review-v001.md",
        "08_final/cover-letter.md",
    ):
        if marker not in naming:
            issues.append(f"perspective naming contract missing {marker}")
    if "text-identical" not in io_contract:
        issues.append("perspective I/O contract does not require a text-identical final Cover Letter")
    for marker in ("08_final/cover-letter.md", "text-identically", "do not calculate, reinterpret, or adjust"):
        if marker not in compositor:
            issues.append(f"perspective compositor missing Cover Letter/probability marker {marker}")
    return issues


def check_agent_configs() -> list[str]:
    issues: list[str] = []
    for skill in skill_files():
        agent_config = skill.parent / "agents" / "openai.yaml"
        if not agent_config.exists():
            issues.append(f"{skill.parent.relative_to(ROOT).as_posix()}: missing agents/openai.yaml")
    return issues


def check_panel_invariants() -> list[str]:
    issues: list[str] = []
    panel = ROOT / "perspective-review-panel" / "SKILL.md"
    roles = ROOT / "perspective-review-panel" / "references" / "reviewer-role-definitions.md"
    panel_text = panel.read_text(encoding="utf-8")
    roles_text = roles.read_text(encoding="utf-8")
    for term in (
        "Conditional Reviewers",
        "Methodology / Statistics Reviewer",
        "Practicing-Clinician Reviewer",
        "Outlet-Fit Editor Reviewer",
    ):
        if term not in panel_text and term not in roles_text:
            issues.append(f"perspective-review-panel missing conditional reviewer term: {term}")
    return issues


def check_input_builder_execution_contract() -> list[str]:
    issues: list[str] = []
    builder = (ROOT / "perspective-input-builder" / "SKILL.md").read_text(encoding="utf-8")
    briefs = (
        ROOT
        / "perspective-orchestrator"
        / "references"
        / "delegate-brief-templates.md"
    ).read_text(encoding="utf-8")
    required_match = re.search(
        r"(?ms)^Required Outputs:\s*\n(?P<body>(?:\s+-[^\n]*\n)+)", builder
    )
    conditional_match = re.search(
        r"(?ms)^Conditional Output:\s*\n(?P<body>(?:\s+-[^\n]*\n)+)", builder
    )
    expected_required = {
        "01-input-brief.md",
        "target-outlet-profile.md",
        "assumption-log.md",
    }
    if required_match is None:
        issues.append("perspective-input-builder missing Required Outputs block")
    else:
        required_paths = re.findall(r"([\w.-]+\.md)", required_match.group("body"))
        if len(required_paths) != 3 or set(required_paths) != expected_required:
            issues.append(
                "perspective-input-builder Required Outputs must be exactly "
                "01-input-brief.md, target-outlet-profile.md, and assumption-log.md"
            )
    if conditional_match is None:
        issues.append("perspective-input-builder missing Conditional Output block")
    else:
        conditional_paths = re.findall(
            r"([\w.-]+\.md)", conditional_match.group("body")
        )
        if conditional_paths != ["00-perspective-input-template.md"]:
            issues.append(
                "perspective-input-builder Conditional Output must contain only "
                "00-perspective-input-template.md"
            )
        if "仅在现有输入不足、必须交由用户补填时生成" not in conditional_match.group(
            "body"
        ):
            issues.append(
                "perspective-input-builder template output is not bounded to missing user input"
            )
    if "否则立即建立" not in builder or "next_route: clarification_required" not in builder:
        issues.append("perspective-input-builder missing bounded execution route")

    brief_match = re.search(
        r"(?ms)^## Input Builder Brief\s*\n(?P<body>.*?)(?=^---\s*$)", briefs
    )
    if brief_match is None:
        issues.append("perspective delegate templates missing Input Builder Brief section")
    else:
        brief_body = brief_match.group("body")
        expected_brief_paths = {
            "00_input/01-input-brief.md",
            "00_input/target-outlet-profile.md",
            "00_input/assumption-log.md",
            "00_input/00-perspective-input-template.md",
        }
        brief_paths = re.findall(r"00_input/[\w.-]+\.md", brief_body)
        if len(brief_paths) != 4 or set(brief_paths) != expected_brief_paths:
            issues.append(
                "Perspective Input Builder Brief must name exactly three normal outputs "
                "and the one conditional template path"
            )
        for marker in (
            "Create these three files immediately",
            "do not delay the first write",
            "only if",
            "do not create the three normal outputs",
            "next_route: clarification_required",
            "Write nowhere else",
        ):
            if marker not in brief_body:
                issues.append(
                    f"perspective delegate brief missing execution marker: {marker}"
                )
    return issues


def check_argument_architect_execution_contract() -> list[str]:
    issues: list[str] = []
    architect = (
        ROOT / "perspective-argument-architect" / "SKILL.md"
    ).read_text(encoding="utf-8")
    section_match = re.search(
        r"(?ms)^## Execution Order\s*\n(?P<body>.*?)(?=^##\s)", architect
    )
    if section_match is None:
        return ["perspective-argument-architect missing Execution Order section"]
    section = " ".join(section_match.group("body").split())
    for marker in (
        "03_skeletons/02-argument-skeleton.md",
        "在读取完整 matrix 或 evidence bundle 前必须先保存这一检查点",
        "一次只补全一个 argument step",
        "按 Claim ID/Binding ID 的定向读取",
        "不得拆给多个 architect",
    ):
        if marker not in section:
            issues.append(
                f"perspective-argument-architect missing checkpoint marker: {marker}"
            )
    return issues


def check_drafter_execution_contract() -> list[str]:
    issues: list[str] = []
    drafter = (ROOT / "perspective-drafter" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    section_match = re.search(
        r"(?ms)^## Execution Order\s*\n(?P<body>.*?)(?=^###\s)", drafter
    )
    if section_match is None:
        return ["perspective-drafter missing Execution Order section"]
    section = " ".join(section_match.group("body").split())
    for marker in (
        "不要先载入完整 matrix 或 evidence bundle",
        "04_drafts/perspective-v{N}.md",
        "04_drafts/perspective-v{N}-paragraph-map.md",
        "同一 writer 一次只完成一个 section",
        "按 Claim ID/Binding ID 的定向读取",
        "只有两份完整文件可以进入 conformance 或 evaluation",
        "不得拆给多个 writer",
    ):
        if marker not in section:
            issues.append(f"perspective-drafter missing checkpoint marker: {marker}")
    return issues


def main() -> int:
    issues = []
    issues.extend(check_frontmatter())
    issues.extend(check_markdown_references())
    issues.extend(check_orchestrator_invariants())
    issues.extend(check_cover_letter_contract())
    issues.extend(check_agent_configs())
    issues.extend(check_panel_invariants())
    issues.extend(check_input_builder_execution_contract())
    issues.extend(check_argument_architect_execution_contract())
    issues.extend(check_drafter_execution_contract())

    if issues:
        print("research-perspective audit failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("research-perspective audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
