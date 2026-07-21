#!/usr/bin/env python3
"""Validate a directly transferable Deep Research continuation package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUEST_RE = re.compile(r"deep-research-request-v(?P<version>\d{3})\.md$")
GUIDE_RE = re.compile(r"deep-research-follow-up-guide-v(?P<version>\d{3})\.md$")
REPORT_RE = re.compile(r"deep-research-report-v\d{3}\.md$")

REQUIRED_HEADINGS = (
    "## Research objective and intended use",
    "## Core research question",
    "## Scope and boundaries",
    "## Known background and unresolved issues",
    "## Questions to answer",
    "## Search scope and source requirements",
    "## Analysis and synthesis requirements",
    "## Report structure",
    "## Citation and link requirements",
    "## Completion criteria",
)

REQUIRED_CITATION_CONTRACT_PATTERNS = {
    "one-to-five source limit": r"(?i)\b(?:one\s+to\s+five|1\s*[–-]\s*5)\b",
    "atomic claim unit": r"(?i)\batomic claim\b",
    "clickable claim/source example": r"\(C\d{3};\s*\[R\d{3}\]\(https://",
    "GB/T 7714-2015 reference": r"GB/T\s*7714[—-]2015",
}

BANNED_REQUEST_PATTERNS = {
    "workflow identifier": r"(?i)\bworkflow[ _-]?id\b",
    "round identifier": r"(?i)\bround[ _-]?id\b",
    "pending edge": r"(?i)\bpending[ _-]?edge\b",
    "plugin version": r"(?i)\bplugin[ _-]?version\b",
    "artifact identifier": r"(?i)\bartifact[ _-]?id\b",
    "resume target": r"(?i)\bresume[ _-]?(target|consumer|edge)\b",
    "workflow state": r"deep_research_handoff_required|deep_research_continuation",
    "hash or digest": r"(?i)\bsha-?256\b|\bdigest\b",
    "Windows absolute path": r"(?i)\b[A-Z]:[\\/]",
    "test path": r"(?i)(?:^|[\s`])/?tests/",
}

TEMPLATE_MARKERS = (
    "[concise research topic]",
    "[State what",
    "[Write one",
    "[Briefly summarize",
    "[Primary subquestion]",
    "[Comparison or closest-work question]",
    "[Contrary-evidence or boundary question]",
    "[Name the source classes",
    "[Specify the comparisons",
    "[scope]",
    "[only decision-relevant exclusions]",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(package_dir: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not package_dir.is_dir():
        return {"valid": False, "errors": [f"not a directory: {package_dir}"], "warnings": []}

    files = sorted(path for path in package_dir.iterdir() if path.is_file())
    requests = [path for path in files if REQUEST_RE.fullmatch(path.name)]
    guides = [path for path in files if GUIDE_RE.fullmatch(path.name)]
    unexpected = [
        path.name
        for path in files
        if not REQUEST_RE.fullmatch(path.name)
        and not GUIDE_RE.fullmatch(path.name)
        and not REPORT_RE.fullmatch(path.name)
    ]

    if len(requests) != 1:
        errors.append(f"expected exactly one versioned request, found {len(requests)}")
    if len(guides) != 1:
        errors.append(f"expected exactly one versioned follow-up guide, found {len(guides)}")
    if unexpected:
        errors.append("unexpected files in round directory: " + ", ".join(unexpected))
    if not requests or not guides:
        return {"valid": False, "errors": errors, "warnings": warnings}

    request_path = requests[0]
    guide_path = guides[0]
    request_version = REQUEST_RE.fullmatch(request_path.name).group("version")
    guide_version = GUIDE_RE.fullmatch(guide_path.name).group("version")
    if request_version != guide_version:
        errors.append("request and follow-up guide versions differ")

    request = read(request_path)
    guide = read(guide_path)
    request_length = len(request)
    guide_length = len(guide)

    if request_length > 12_000:
        errors.append(f"request exceeds 12000 characters: {request_length}")
    elif request_length > 8_000:
        warnings.append(f"request exceeds preferred warning threshold: {request_length}")
    if guide_length > 5_000:
        errors.append(f"follow-up guide exceeds 5000 characters: {guide_length}")

    positions = []
    for heading in REQUIRED_HEADINGS:
        position = request.find(heading)
        if position < 0:
            errors.append(f"missing required heading: {heading}")
        positions.append(position)
    if all(position >= 0 for position in positions) and positions != sorted(positions):
        errors.append("required headings are not in the expected order")

    for label, pattern in BANNED_REQUEST_PATTERNS.items():
        if re.search(pattern, request):
            errors.append(f"request contains prohibited {label}")
    for marker in TEMPLATE_MARKERS:
        if marker in request:
            errors.append(f"request contains unresolved template marker: {marker}")
    for label, pattern in REQUIRED_CITATION_CONTRACT_PATTERNS.items():
        if not re.search(pattern, request):
            errors.append(f"request is missing required {label}")

    expected_report = f"deep-research-report-v{request_version}.md"
    if request_path.name not in guide:
        errors.append("follow-up guide does not name the matching request")
    if expected_report not in guide:
        errors.append("follow-up guide does not name the matching returned report")
    if re.search(r"(?i)\bsha-?256\b|\bdigest\b", request + "\n" + guide):
        errors.append("package contains a hash or digest instruction")

    return {
        "valid": not errors,
        "request": request_path.name,
        "guide": guide_path.name,
        "request_characters": request_length,
        "guide_characters": guide_length,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.package_dir.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Deep Research package: " + ("valid" if result["valid"] else "invalid"))
        for message in result["warnings"]:
            print(f"warning: {message}")
        for message in result["errors"]:
            print(f"error: {message}", file=sys.stderr)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
