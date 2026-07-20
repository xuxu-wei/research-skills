#!/usr/bin/env python3
"""Print deterministic, read-only language-review candidates from an Idea dossier."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


GROUP_READER_ENTRY = "reader-entry"
GROUP_COMPACT_LABEL = "compact-reader-label"
GROUP_TOKEN = "mixed-language-version-internal-token"
GROUP_ORDER = (GROUP_READER_ENTRY, GROUP_COMPACT_LABEL, GROUP_TOKEN)
READER_PREFIX_CHARS = 180

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN_TOKEN_RE = re.compile(r"(?<![A-Za-z])[A-Za-z][A-Za-z0-9_-]+")
VERSION_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:[vr]\d{3,}|[vr]\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.-]+)?|\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?)(?![A-Za-z0-9])",
    re.IGNORECASE,
)
INTERNAL_TOKEN_RE = re.compile(
    r"(?:"
    r"(?<![A-Za-z0-9])[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+(?![A-Za-z0-9])"
    r"|(?<![A-Za-z0-9])[a-z][a-z0-9]*(?:-[a-z0-9]+){2,}(?![A-Za-z0-9])"
    r"|@sha256:"
    r"|`[A-Za-z][A-Za-z0-9_.-]*`"
    r")"
)
ABBREVIATION_RE = re.compile(
    r"(?<![A-Za-z0-9])[A-Z][A-Z0-9]{1,9}(?:-[A-Z0-9]{1,8})?(?![A-Za-z0-9])"
)
PARENTHETICAL_RE = re.compile(r"[（(]([^()（）\n]{1,24})[）)]")
QUOTED_RE = re.compile(r"[“「『\"]([^”」』\"\n]{1,18})[”」』\"]")
LABEL_CUE_RE = re.compile(
    r"(?:简称(?:为)?|下称|记为|称为|标记为|label(?:led)?\s+as)\s*[：:]?\s*[（(]?\s*"
    r"[“「『\"`]?([^，。；;：:\n”」』\"`]{1,18})",
    re.IGNORECASE,
)
TOKEN_STOPLIST = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "of",
    "on", "or", "the", "to", "with", "ii", "iii",
}
FIELD_LABEL_RE = re.compile(r"^\s*-\s*\*\*[^*]+:\*\*\s*")


@dataclass(frozen=True)
class LineCandidate:
    line_number: int
    excerpt: str


@dataclass(frozen=True)
class TokenCandidate:
    token: str
    line_numbers: tuple[int, ...]


def _normalized_heading(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def _is_structured_abstract(title: str) -> bool:
    normalized = _normalized_heading(title)
    return normalized == "structured abstract" or "结构式摘要" in title


def _is_primary_question(title: str) -> bool:
    normalized = _normalized_heading(title)
    return normalized in {"primary research question", "primary question"} or "主要研究问题" in title


def _is_core_hypothesis(title: str) -> bool:
    normalized = _normalized_heading(title)
    return normalized.startswith("core hypothesis") or "核心假设" in title


def _reader_facing_lines(lines: Sequence[str]) -> list[tuple[int, str]]:
    """Exclude initial YAML frontmatter and fenced code from prose scanning."""

    start = 0
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                start = index + 1
                break

    visible: list[tuple[int, str]] = []
    in_fence = False
    for index in range(start, len(lines)):
        text = lines[index].rstrip("\r\n")
        if re.match(r"^\s*(```|~~~)", text):
            in_fence = not in_fence
            continue
        if in_fence or not text.strip() or re.match(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$", text):
            continue
        visible.append((index + 1, text))
    return visible


def _reader_entry_line_numbers(visible: Sequence[tuple[int, str]]) -> set[int]:
    """Locate the H1, first H2, structured abstract, and core question/hypothesis."""

    selected: set[int] = set()
    first_h2_seen = False
    selected_h2 = False
    selected_h3 = False

    for line_number, text in visible:
        match = HEADING_RE.match(text)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            if level == 1:
                selected.add(line_number)
            if level == 2:
                selected_h3 = False
                if not first_h2_seen:
                    first_h2_seen = True
                    selected_h2 = True
                else:
                    selected_h2 = _is_structured_abstract(title)
            elif level == 3:
                selected_h3 = _is_primary_question(title) or _is_core_hypothesis(title)
            elif level < 3:
                selected_h3 = False

        # Fixed H2/H3 scaffold headings are locators, not language candidates.
        if match and len(match.group(1)) in {2, 3}:
            continue
        if selected_h2 or selected_h3:
            selected.add(line_number)

    return selected


def _candidate_tokens(text: str) -> list[str]:
    """Return unique candidate tokens in their first source-column order."""

    matches: list[tuple[int, str]] = []
    if CJK_RE.search(text):
        matches.extend((match.start(), match.group(0)) for match in LATIN_TOKEN_RE.finditer(text))
    matches.extend((match.start(), match.group(0)) for match in VERSION_RE.finditer(text))
    matches.extend(
        (match.start(), match.group(0).strip("`")) for match in INTERNAL_TOKEN_RE.finditer(text)
    )

    tokens: list[str] = []
    seen: set[str] = set()
    for _, token in sorted(matches, key=lambda item: item[0]):
        if token and token not in seen:
            tokens.append(token)
            seen.add(token)
    return tokens


def _is_compact(form: str) -> bool:
    normalized = re.sub(r"\s+", " ", form.strip(" \t\r\n`'\"“”「」『』（）()[]{}：:；;，,"))
    if not normalized:
        return False
    if ABBREVIATION_RE.fullmatch(normalized) or INTERNAL_TOKEN_RE.fullmatch(normalized):
        return True
    compact = normalized.replace(" ", "")
    return (
        bool(CJK_RE.search(compact))
        and 2 <= len(compact) <= 12
        and normalized.count(" ") <= 1
        and not re.search(r"[，。；;：:,]", normalized)
    )


def _compact_labels(text: str, *, include_incidental: bool) -> list[str]:
    """Return structurally marked compact forms without assigning a verdict."""

    matches: list[tuple[int, str]] = [
        (match.start(1), match.group(1))
        for match in LABEL_CUE_RE.finditer(text)
        if _is_compact(match.group(1))
    ]
    if include_incidental:
        matches.extend((match.start(), match.group(0)) for match in ABBREVIATION_RE.finditer(text))
        matches.extend(
            (match.start(1), match.group(1))
            for pattern in (PARENTHETICAL_RE, QUOTED_RE)
            for match in pattern.finditer(text)
            if _is_compact(match.group(1))
        )

    labels: list[str] = []
    seen: set[str] = set()
    for _, raw_label in sorted(matches, key=lambda item: item[0]):
        label = raw_label.strip(" \t\r\n`'\"“”「」『』（）()[]{}：:；;，,")
        normalized = label.casefold()
        if not normalized or normalized in seen:
            continue
        labels.append(label)
        seen.add(normalized)
    return labels


def _bounded_excerpt(text: str) -> str:
    return text[:READER_PREFIX_CHARS] + ("…" if len(text) > READER_PREFIX_CHARS else "")


def scan_candidates(
    lines: Sequence[str],
) -> dict[str, list[LineCandidate] | list[TokenCandidate]]:
    """Return candidates in source order, without assigning a language verdict."""

    visible = _reader_facing_lines(lines)
    reader_entries = _reader_entry_line_numbers(visible)
    reader_candidates: list[LineCandidate] = []
    compact_label_lines: dict[str, list[int]] = {}
    token_lines: dict[str, list[int]] = {}
    priority_tokens: set[str] = set()

    for line_number, text in visible:
        if line_number in reader_entries:
            reader_candidates.append(LineCandidate(line_number, _bounded_excerpt(text)))
        for label in _compact_labels(
            text,
            include_incidental=line_number in reader_entries,
        ):
            line_numbers = compact_label_lines.setdefault(label, [])
            if not line_numbers or line_numbers[-1] != line_number:
                line_numbers.append(line_number)
        token_text = text
        heading = HEADING_RE.match(text)
        if heading and len(heading.group(1)) >= 2:
            token_text = ""
        else:
            token_text = FIELD_LABEL_RE.sub("", token_text)
        for token in _candidate_tokens(token_text):
            if token.casefold() in TOKEN_STOPLIST:
                continue
            line_numbers = token_lines.setdefault(token, [])
            if not line_numbers or line_numbers[-1] != line_number:
                line_numbers.append(line_number)
            if line_number in reader_entries:
                priority_tokens.add(token)

    return {
        GROUP_READER_ENTRY: reader_candidates,
        GROUP_COMPACT_LABEL: [
            TokenCandidate(label, tuple(line_numbers))
            for label, line_numbers in compact_label_lines.items()
        ],
        GROUP_TOKEN: [
            TokenCandidate(token, tuple(line_numbers))
            for token, line_numbers in token_lines.items()
            if token in priority_tokens
            or VERSION_RE.fullmatch(token)
            or "_" in token
            or token.count("-") >= 2
            or token == "@sha256:"
        ],
    }


def render_candidates(
    candidates: dict[str, list[LineCandidate] | list[TokenCandidate]],
) -> str:
    """Render stable, grep-friendly grouped output."""

    output: list[str] = []
    output.append(f"[{GROUP_READER_ENTRY}]")
    for candidate in candidates[GROUP_READER_ENTRY]:
        assert isinstance(candidate, LineCandidate)
        output.append(f"{candidate.line_number}\t{candidate.excerpt}")

    output.append(f"[{GROUP_COMPACT_LABEL}]")
    for candidate in candidates[GROUP_COMPACT_LABEL]:
        assert isinstance(candidate, TokenCandidate)
        output.append(f"{candidate.token}\t{','.join(map(str, candidate.line_numbers))}")

    output.append(f"[{GROUP_TOKEN}]")
    for candidate in candidates[GROUP_TOKEN]:
        assert isinstance(candidate, TokenCandidate)
        output.append(f"{candidate.token}\t{','.join(map(str, candidate.line_numbers))}")

    return "\n".join(output) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print candidate Idea-dossier lines for focused academic-language review."
    )
    parser.add_argument("dossier", type=Path, help="Path to a Markdown Idea dossier")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        text = args.dossier.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read {args.dossier}: {exc}", file=sys.stderr)
        return 2

    lines = text.splitlines(keepends=True)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.write(render_candidates(scan_candidates(lines)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
