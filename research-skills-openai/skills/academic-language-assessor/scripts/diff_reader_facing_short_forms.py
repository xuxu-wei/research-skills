#!/usr/bin/env python3
"""Advisory diff of reader-facing short-form candidates between two dossiers."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from scan_idea_language_candidates import (
    FIELD_LABEL_RE,
    HEADING_RE,
    INTERNAL_TOKEN_RE,
    _reader_facing_lines,
)


GROUP = "new-reader-facing-short-form"
ABBREVIATION_RE = re.compile(
    r"(?<![A-Za-z0-9])[A-Z][A-Z0-9]{1,9}(?:-[A-Z0-9]{1,8})?(?![A-Za-z0-9])"
)
PARENTHETICAL_RE = re.compile(r"[（(]([^()（）\n]{1,24})[）)]")
QUOTED_RE = re.compile(r"[“「『\"]([^”」』\"\n]{1,18})[”」』\"]")
LABEL_CUE_RE = re.compile(
    r"(?:简称(?:为)?|下称|记为|称为|标记为|label(?:led)?\s+as)\s*[：:]?\s*"
    r"[“「『\"`]?([^，。；;：:\n”」』\"`]{1,18})",
    re.IGNORECASE,
)
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
SPACE_RE = re.compile(r"\s+")
TRIM_CHARS = " \t\r\n`'\"“”「」『』（）()[]{}，,。.;；:："


@dataclass(frozen=True)
class ShortFormCandidate:
    category: str
    form: str
    line_numbers: tuple[int, ...]


def _normalize(form: str) -> str:
    return SPACE_RE.sub(" ", form.strip(TRIM_CHARS)).casefold()


def _is_compact(form: str) -> bool:
    normalized = SPACE_RE.sub(" ", form.strip(TRIM_CHARS))
    if not normalized:
        return False
    if ABBREVIATION_RE.fullmatch(normalized) or INTERNAL_TOKEN_RE.fullmatch(normalized):
        return True
    compact = normalized.replace(" ", "")
    return (
        bool(CJK_RE.search(compact))
        and len(compact) <= 12
        and normalized.count(" ") <= 1
        and not re.search(r"[，。；;：:,]", normalized)
    )


def short_form_candidates(lines: Sequence[str]) -> list[ShortFormCandidate]:
    """Return generic short-form candidates without assigning a language verdict."""

    occurrences: dict[str, tuple[str, str, list[int]]] = {}
    for line_number, raw_text in _reader_facing_lines(lines):
        heading = HEADING_RE.match(raw_text)
        if heading and len(heading.group(1)) >= 2:
            continue
        text = FIELD_LABEL_RE.sub("", raw_text)
        matches: list[tuple[int, str, str]] = []
        matches.extend(
            (match.start(), "abbreviation", match.group(0))
            for match in ABBREVIATION_RE.finditer(text)
        )
        matches.extend(
            (match.start(), "internal-token", match.group(0).strip("`"))
            for match in INTERNAL_TOKEN_RE.finditer(text)
        )
        matches.extend(
            (match.start(1), "parenthetical", match.group(1))
            for match in PARENTHETICAL_RE.finditer(text)
            if _is_compact(match.group(1))
        )
        matches.extend(
            (match.start(1), "quoted-label", match.group(1))
            for match in QUOTED_RE.finditer(text)
            if _is_compact(match.group(1))
        )
        matches.extend(
            (match.start(1), "explicit-label", match.group(1))
            for match in LABEL_CUE_RE.finditer(text)
            if _is_compact(match.group(1))
        )

        seen_on_line: set[str] = set()
        for _, category, raw_form in sorted(matches, key=lambda item: (item[0], item[1])):
            form = raw_form.strip(TRIM_CHARS)
            normalized = _normalize(form)
            if not normalized or normalized in seen_on_line:
                continue
            seen_on_line.add(normalized)
            if normalized not in occurrences:
                occurrences[normalized] = (category, form, [line_number])
            elif occurrences[normalized][2][-1] != line_number:
                occurrences[normalized][2].append(line_number)

    return [
        ShortFormCandidate(category, form, tuple(line_numbers))
        for category, form, line_numbers in occurrences.values()
    ]


def _all_reader_facing_occurrence_lines(
    lines: Sequence[str], form: str
) -> tuple[int, ...]:
    """Locate every literal reader-facing occurrence of a detected form."""

    escaped_parts = [re.escape(part) for part in SPACE_RE.split(form.strip()) if part]
    if not escaped_parts:
        return ()
    pattern_text = r"\s+".join(escaped_parts)
    if form[0].isascii() and (form[0].isalnum() or form[0] == "_"):
        pattern_text = rf"(?<![A-Za-z0-9_]){pattern_text}"
    if form[-1].isascii() and (form[-1].isalnum() or form[-1] == "_"):
        pattern_text = rf"{pattern_text}(?![A-Za-z0-9_])"
    pattern = re.compile(pattern_text, re.IGNORECASE)
    return tuple(
        line_number
        for line_number, raw_text in _reader_facing_lines(lines)
        if pattern.search(FIELD_LABEL_RE.sub("", raw_text))
    )


def diff_short_forms(source_lines: Sequence[str], revised_lines: Sequence[str]) -> list[ShortFormCandidate]:
    """Return revised candidates whose normalized form is absent from the source."""

    source_forms = {_normalize(item.form) for item in short_form_candidates(source_lines)}
    return [
        ShortFormCandidate(
            item.category,
            item.form,
            _all_reader_facing_occurrence_lines(revised_lines, item.form)
            or item.line_numbers,
        )
        for item in short_form_candidates(revised_lines)
        if _normalize(item.form) not in source_forms
    ]


def render_diff(candidates: Sequence[ShortFormCandidate]) -> str:
    output = [f"[{GROUP}]"]
    output.extend(
        f"{item.category}\t{item.form}\t{','.join(map(str, item.line_numbers))}"
        for item in candidates
    )
    return "\n".join(output) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Frozen source dossier")
    parser.add_argument("revised", type=Path, help="Editorially revised dossier")
    parser.add_argument(
        "--fail-on-new",
        action="store_true",
        help=(
            "Developer-only strict switch: return 1 when any new candidate is found; "
            "candidate presence is not a production language verdict"
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        source_text = args.source.read_text(encoding="utf-8-sig")
        revised_text = args.revised.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read dossier: {exc}", file=sys.stderr)
        return 2

    candidates = diff_short_forms(
        source_text.splitlines(keepends=True),
        revised_text.splitlines(keepends=True),
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.write(render_diff(candidates))
    return 1 if args.fail_on_new and candidates else 0


if __name__ == "__main__":
    raise SystemExit(main())
