#!/usr/bin/env python3
"""Audit the research-perspective skill package.

Checks:
- each SKILL.md has frontmatter with name and "Use when" description
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


ROOT = Path(__file__).resolve().parents[1]


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
    for skill in sorted(ROOT.glob("*/SKILL.md")):
        fm = parse_frontmatter(skill)
        rel = skill.relative_to(ROOT).as_posix()
        if not fm.get("name"):
            issues.append(f"{rel}: missing frontmatter name")
        desc = fm.get("description", "")
        if not desc:
            issues.append(f"{rel}: missing frontmatter description")
        elif not desc.startswith("Use when"):
            issues.append(f"{rel}: description must start with 'Use when'")
    return issues


def check_markdown_references() -> list[str]:
    issues: list[str] = []
    ref_pattern = re.compile(r"`((?:references|templates)/[^`]+\.md)`")
    for md in sorted(ROOT.rglob("*.md")):
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
    if "STEP 1 → STEP 2-lite → STEP 3" not in text:
        issues.append("perspective-orchestrator/SKILL.md: Lite mode must include STEP 2-lite")
    if "delegation adapter" not in text:
        issues.append("perspective-orchestrator/SKILL.md: missing delegation adapter guidance")
    return issues


def check_agent_configs() -> list[str]:
    issues: list[str] = []
    for skill in sorted(ROOT.glob("*/SKILL.md")):
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


def main() -> int:
    issues = []
    issues.extend(check_frontmatter())
    issues.extend(check_markdown_references())
    issues.extend(check_orchestrator_invariants())
    issues.extend(check_agent_configs())
    issues.extend(check_panel_invariants())

    if issues:
        print("research-perspective audit failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("research-perspective audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
