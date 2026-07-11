#!/usr/bin/env python3
"""Add deterministic contents lists to long OpenAI plugin references."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
REFERENCES = REPO / "research-skills-openai" / "skills"
TOC_START = "<!-- toc:start -->"
TOC_END = "<!-- toc:end -->"


def slugify(title: str) -> str:
    value = unicodedata.normalize("NFKC", title).strip().lower()
    value = re.sub(r"[`*_~]", "", value)
    value = re.sub(r"[^\w\-\s]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_]+", "-", value).strip("-")
    return value or "section"


def headings(lines: list[str]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{2,3})\s+(.+?)\s*#*\s*$", line)
        if match and match.group(2) not in {"Contents", "Table of Contents"}:
            found.append((len(match.group(1)), match.group(2)))
    return found


def toc_lines(items: list[tuple[int, str]]) -> list[str]:
    seen: Counter[str] = Counter()
    result = ["## Contents", "", TOC_START]
    for level, title in items:
        base = slugify(title)
        suffix = seen[base]
        seen[base] += 1
        anchor = base if suffix == 0 else f"{base}-{suffix}"
        indent = "  " if level == 3 else ""
        result.append(f"{indent}- [{title}](#{anchor})")
    result.extend([TOC_END, ""])
    return result


def normalize(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    original = text.splitlines()
    if len(original) <= 100:
        return
    items = headings(original)
    if not items:
        raise RuntimeError(f"Long reference has no section headings: {path}")

    if TOC_START in original and TOC_END in original:
        start = original.index(TOC_START)
        end = original.index(TOC_END)
        heading = start - 2 if start >= 2 and original[start - 2] == "## Contents" else start
        tail = end + 1
        while tail < len(original) and not original[tail].strip():
            tail += 1
        updated = original[:heading] + toc_lines(items) + original[tail:]
    elif any(line in {"## Contents", "## Table of Contents"} for line in original):
        return
    else:
        h1 = next((index for index, line in enumerate(original) if line.startswith("# ")), None)
        if h1 is None:
            raise RuntimeError(f"Long reference has no H1: {path}")
        insert_at = h1 + 1
        if insert_at < len(original) and original[insert_at] == "":
            insert_at += 1
        updated = original[:insert_at] + toc_lines(items) + original[insert_at:]

    if len(updated) > 300:
        raise RuntimeError(f"Reference remains over 300 lines after contents generation: {path} ({len(updated)})")
    path.write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8", newline="\n")


def normalize_skill_routes(skill_md: Path) -> None:
    lines = skill_md.read_text(encoding="utf-8-sig").splitlines()
    resources = [
        path
        for path in skill_md.parent.rglob("*")
        if path.is_file() and any(part in {"references", "templates", "scripts"} for part in path.parts)
    ]
    changed = False
    for resource in sorted(resources):
        relative_path = resource.relative_to(skill_md.parent).as_posix()
        token = f"`{relative_path}`"
        matches = [index for index, line in enumerate(lines) if token in line]
        if not matches:
            continue
        if any(re.search(r"\b(?:read|load|use|run|open|when|before|after|only if)\b", lines[index], re.I) for index in matches):
            continue
        index = matches[-1]
        line = lines[index]
        action = "Run" if relative_path.startswith("scripts/") else "Use" if relative_path.startswith("templates/") else "Read"
        condition = (
            "when reproducible local execution is explicitly required"
            if action == "Run"
            else "when producing its named artifact"
            if action == "Use"
            else "when its named guidance or contract applies"
        )
        if line.lstrip().startswith("-"):
            indent = line[: len(line) - len(line.lstrip())]
            tail = line.lstrip()[1:].strip()
            tail = tail[len(token) :].lstrip(" :") if tail.startswith(token) else tail
            suffix = f": {tail}" if tail else "."
            lines[index] = f"{indent}- {action} {token} {condition}{suffix}"
        else:
            lines[index] = f"{line} {action} this resource only {condition}."
        changed = True
    if changed:
        skill_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    paths = sorted(REFERENCES.glob("*/references/**/*.md"))
    for path in paths:
        normalize(path)
    skills = sorted(REFERENCES.glob("*/SKILL.md"))
    for skill_md in skills:
        normalize_skill_routes(skill_md)
    print(f"normalized {len(paths)} OpenAI reference files and {len(skills)} resource routers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
