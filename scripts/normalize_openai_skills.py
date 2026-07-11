#!/usr/bin/env python3
"""Normalize the ChatGPT/Codex plugin skills without touching Hermes sources.

The OpenAI plugin intentionally keeps only ``name`` and ``description`` in
SKILL.md frontmatter. Product-facing metadata and invocation policy live in
``agents/openai.yaml``.
"""

from __future__ import annotations

import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO / "research-skills-openai" / "skills"

IMPLICIT_SKILLS = {
    "research-idea-orchestrator",
    "proposal-orchestrator",
    "article-orchestrator",
    "perspective-orchestrator",
    "research-opportunity-mapper",
    "academic-deep-search",
    "pubmed",
}


def split_frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md does not start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    frontmatter = text[4:end].splitlines()
    body = text[end + 4 :].lstrip("\n")
    return frontmatter, body


def field_block(lines: list[str], field: str) -> list[str]:
    prefix = f"{field}:"
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue
        block = [line]
        value = line[len(prefix) :].strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            for child in lines[index + 1 :]:
                if child.startswith((" ", "\t")) or not child.strip():
                    block.append(child)
                else:
                    break
        return block
    raise ValueError(f"Missing required frontmatter field: {field}")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def description_text(block: list[str]) -> str:
    first = block[0].split(":", 1)[1].strip()
    if first in {"|", ">", "|-", ">-", "|+", ">+"}:
        return " ".join(line.strip() for line in block[1:] if line.strip())
    return unquote(first)


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def display_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def short_description(description: str) -> str:
    compact = re.sub(r"\s+", " ", description).strip()
    first = re.split(r"(?<=[.!?。！？])\s+", compact, maxsplit=1)[0]
    if len(first) <= 100:
        return first
    candidate = first[:97]
    if " " in candidate:
        candidate = candidate.rsplit(" ", 1)[0]
    return candidate.rstrip(" ,.;:-") + "..."


def default_prompt(name: str) -> str:
    return f"Use ${name} for this task and follow its workflow and output contract."


def normalize_skill(skill_md: Path) -> None:
    text = skill_md.read_text(encoding="utf-8-sig")
    frontmatter, body = split_frontmatter(text)
    name_block = field_block(frontmatter, "name")
    description_block = field_block(frontmatter, "description")
    name = unquote(name_block[0].split(":", 1)[1])
    if name != skill_md.parent.name:
        raise ValueError(f"Skill name does not match directory: {name} != {skill_md.parent.name}")

    description = description_text(description_block)
    normalized_frontmatter = [
        "---",
        f"name: {name}",
        f"description: {yaml_quote(description)}",
        "---",
        "",
    ]
    skill_md.write_text("\n".join(normalized_frontmatter) + body.rstrip() + "\n", encoding="utf-8", newline="\n")

    agent_dir = skill_md.parent / "agents"
    agent_dir.mkdir(exist_ok=True)
    openai_yaml = "\n".join(
        [
            "interface:",
            f"  display_name: {yaml_quote(display_name(name))}",
            f"  short_description: {yaml_quote(short_description(description))}",
            f"  default_prompt: {yaml_quote(default_prompt(name))}",
            "policy:",
            f"  allow_implicit_invocation: {'true' if name in IMPLICIT_SKILLS else 'false'}",
            "",
        ]
    )
    (agent_dir / "openai.yaml").write_text(openai_yaml, encoding="utf-8", newline="\n")


def main() -> int:
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if len(skill_files) != 46:
        raise RuntimeError(f"Expected 46 OpenAI skills, found {len(skill_files)}")
    for skill_md in skill_files:
        normalize_skill(skill_md)
    print(f"normalized {len(skill_files)} OpenAI skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
