#!/usr/bin/env python3
"""Read-only structural lint for research-idea.v3 dossiers."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


REQUIRED_H2 = [
    "Title, summary, audience, and positioning",
    "Structured abstract",
    "Background, current state, gap, significance, and rationale",
    "Research question, objectives, and core hypothesis",
    "Research content and work packages",
    "Data, materials, and existing evidence base",
    "Research design and methods",
    "Key techniques and implementation",
    "Evidence chains",
    "Required analyses and evidence",
    "Expected outputs, falsification criteria, and interpretations",
    "Contribution, innovation, impact, application, and closest-work comparison",
    "Title and positioning claim-support table",
    "Feasibility, resources, risks, alternatives, and stop conditions",
    "References",
]

REQUIRED_REASONING_H3 = [
    "Background",
    "Current state",
    "Gap",
    "Significance",
    "Rationale",
]

NONCONTENT = re.compile(
    r"^(?:[-*]\s*)?(?:<[^>]*>|tbd|todo|not specified|n/?a)\.?$", re.IGNORECASE
)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIMITATION_POINTER = re.compile(
    r"(?:见|参见|详见|另见)\s*(?:第\s*14\s*节|(?:限制|局限|风险|停止条件)(?:部分|章节|一节))"
    r"|(?:see|refer to|as (?:described|discussed) in)\s+(?:section\s*14|the\s+"
    r"(?:limitations?|risks?|stop conditions?)\s+section)"
    r"|(?:limitations?|risks?|stop conditions?)\s+(?:are\s+)?"
    r"(?:described|discussed|listed|reported)\s+in\s+section\s*14",
    re.IGNORECASE,
)
READER_STRUCTURAL_CANDIDATE = re.compile(
    r"(?<![A-Za-z0-9])(?:"
    r"[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+"
    r"|[a-z][a-z0-9]*(?:-[a-z0-9]+){2,}"
    r"|[vr]\d{3,}"
    r")(?![A-Za-z0-9])"
    r"|[（(][A-Z][A-Z0-9]{1,9}(?:-[A-Z0-9]{1,8})?[）)]"
    r"|(?:简称(?:为)?|下称|记为|称为|标记为|label(?:led)?\s+as)\s*[：:]?\s*"
    r"[“「『\"`]?[^，。；;：:\n”」』\"`]{1,18}",
    re.IGNORECASE,
)


def _headings(lines: list[str]) -> list[tuple[int, str, int]]:
    result: list[tuple[int, str, int]] = []
    fenced = False
    for number, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = HEADING.match(line)
        if match:
            result.append((len(match.group(1)), match.group(2).strip(), number))
    return result


def _substantive(lines: list[str]) -> bool:
    for raw in lines:
        value = raw.strip()
        if not value or value.startswith("<!--"):
            continue
        if HEADING.match(value):
            continue
        if not NONCONTENT.fullmatch(value):
            return True
    return False


def _content_after(
    lines: list[str], headings: list[tuple[int, str, int]], heading_index: int
) -> list[str]:
    level, _, start = headings[heading_index]
    stop = len(lines)
    for later_level, _, later_start in headings[heading_index + 1 :]:
        if later_level <= level:
            stop = later_start
            break
    return lines[start + 1 : stop]


def _frontmatter(text: str) -> dict[str, object] | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) != 3:
        return None
    try:
        payload = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return payload if isinstance(payload, dict) else None


def lint_text(text: str, expected_plugin_version: str | None = None) -> list[str]:
    lines = text.splitlines()
    headings = _headings(lines)
    errors: list[str] = []

    if expected_plugin_version is not None:
        metadata = _frontmatter(text)
        if metadata is None:
            errors.append("dossier must contain valid YAML frontmatter")
        elif metadata.get("plugin_version") != expected_plugin_version:
            errors.append(
                "plugin_version must match the active plugin version: "
                f"{expected_plugin_version}"
            )
        if metadata is not None:
            for field in ("artifact_id", "version_id", "path"):
                if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                    errors.append(f"frontmatter field '{field}' must be nonempty")
            based_on = metadata.get("based_on")
            if not isinstance(based_on, list):
                errors.append("frontmatter based_on must be a list")
            else:
                seen: set[tuple[str, str, str]] = set()
                for index, item in enumerate(based_on):
                    if not isinstance(item, dict) or any(
                        not isinstance(item.get(field), str) or not item[field].strip()
                        for field in ("artifact_id", "version", "path")
                    ):
                        errors.append(
                            "each based_on entry must contain artifact_id, version, and path: "
                            f"index {index}"
                        )
                        continue
                    identity = (item["artifact_id"], item["version"], item["path"])
                    if identity in seen:
                        errors.append(f"duplicate based_on logical reference: index {index}")
                    seen.add(identity)
                if metadata.get("change_type") == "editorial_repair" and not based_on:
                    errors.append("editorial_repair requires at least one based_on input")

    h1 = [(title, line) for level, title, line in headings if level == 1]
    if len(h1) != 1 or (len(h1) == 1 and not _substantive([h1[0][0]])):
        errors.append("dossier must contain exactly one substantive H1 title")

    h2_indexes = [index for index, item in enumerate(headings) if item[0] == 2]
    h2_titles = [headings[index][1] for index in h2_indexes]
    if h2_titles != REQUIRED_H2:
        errors.append("H2 headings must match the 15-section contract in order")
    else:
        for index in h2_indexes:
            if not _substantive(_content_after(lines, headings, index)):
                errors.append(f"section '{headings[index][1]}' is empty")

    if len(h2_indexes) >= 3 and h2_titles[:3] == REQUIRED_H2[:3]:
        section_index = h2_indexes[2]
        _, _, section_start = headings[section_index]
        section_stop = len(lines)
        for next_index in h2_indexes[3:4]:
            section_stop = headings[next_index][2]
        reasoning_indexes = [
            index
            for index, (level, _, line) in enumerate(headings)
            if level == 3 and section_start < line < section_stop
        ]
        reasoning_titles = [headings[index][1] for index in reasoning_indexes]
        if reasoning_titles != REQUIRED_REASONING_H3:
            errors.append(
                "section 3 must contain exactly Background, Current state, Gap, "
                "Significance, and Rationale H3 headings in order"
            )
        else:
            for index in reasoning_indexes:
                if not _substantive(_content_after(lines, headings, index)):
                    errors.append(f"reasoning function '{headings[index][1]}' is empty")

    h1_title = h1[0][0].strip() if len(h1) == 1 else None
    title_fields = re.findall(r"^\s*-\s+\*\*Title:\*\*\s*(.+?)\s*$", text, re.MULTILINE)
    if len(title_fields) != 1 or not _substantive(title_fields):
        errors.append("section 1 must contain one substantive Title field")
    elif h1_title is not None and title_fields[0].strip() != h1_title:
        errors.append("H1 and section-1 Title field must match exactly")

    summaries = re.findall(
        r"^\s*-\s+\*\*One-sentence complete-Idea summary:\*\*\s*(.+?)\s*$",
        text,
        re.MULTILINE,
    )
    if len(summaries) != 1 or not _substantive(summaries):
        errors.append("section 1 must contain one substantive complete-Idea summary")

    if re.search(r"\*\*Limits and failure conditions:\*\*", text, re.IGNORECASE):
        errors.append("evidence chains must not contain the deprecated limits field")
    if re.search(r"\|[^\n]*Required qualifier[^\n]*\|", text, re.IGNORECASE):
        errors.append("claim-support tables must not contain a qualifier column")

    section_14_start = None
    section_14_stop = len(lines)
    if h2_titles == REQUIRED_H2:
        section_14_start = headings[h2_indexes[13]][2]
        section_14_stop = headings[h2_indexes[14]][2]
    authority_heading = re.compile(
        r"^(?:Working assumptions|Limitations(?: and boundary conditions)?|"
        r"Risks, alternatives, and stop conditions)(?:\s*\([^)]*\))?$",
        re.IGNORECASE,
    )
    for level, title, line in headings:
        if level >= 3 and authority_heading.fullmatch(title):
            if section_14_start is None or not (section_14_start < line < section_14_stop):
                errors.append(
                    f"authority heading '{title}' must occur only inside section 14"
                )

    if section_14_start is not None:
        outside_authority = "\n".join(
            lines[:section_14_start] + lines[section_14_stop:]
        )
        if LIMITATION_POINTER.search(outside_authority):
            errors.append(
                "reader-facing sections must not point to section 14 or another "
                "limitations location"
            )

    return errors


def reader_language_advisories(text: str) -> list[str]:
    """Return review candidates, not universal language errors."""
    lines = text.splitlines()
    headings = _headings(lines)
    references_start = len(lines)
    for level, title, line in headings:
        if level == 2 and title == "References":
            references_start = line
            break
    advisories: list[str] = []
    fenced = False
    frontmatter = text.startswith("---")
    frontmatter_delimiters = 0
    for number, line in enumerate(lines[:references_start], start=1):
        if frontmatter and line.strip() == "---":
            frontmatter_delimiters += 1
            if frontmatter_delimiters <= 2:
                continue
        if frontmatter and frontmatter_delimiters < 2:
            continue
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = HEADING.match(line)
        if heading and heading.group(2).strip() in {*REQUIRED_H2, *REQUIRED_REASONING_H3}:
            continue
        matches = sorted({match.group(0) for match in READER_STRUCTURAL_CANDIDATE.finditer(line)})
        if matches:
            advisories.append(
                f"line {number}: review possible internal implementation vocabulary: "
                + ", ".join(matches)
            )
    return advisories


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path)
    parser.add_argument("--expected-plugin-version")
    args = parser.parse_args()
    try:
        text = args.dossier.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {args.dossier}: {exc}", file=sys.stderr)
        return 2

    errors = lint_text(text, args.expected_plugin_version)
    advisories = reader_language_advisories(text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for advisory in advisories:
        print(f"ADVISORY: {advisory}")
    print(f"OK: {args.dossier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
