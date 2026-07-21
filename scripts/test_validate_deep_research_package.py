#!/usr/bin/env python3
"""Deterministic tests for the Deep Research package validator."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MAPPER_SCRIPTS = REPO / "research-skills-openai" / "skills" / "research-landscape-mapper" / "scripts"
sys.path.insert(0, str(MAPPER_SCRIPTS))

from validate_deep_research_package import REQUIRED_HEADINGS, validate  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def valid_request() -> str:
    sections = ["# Deep Research: Fixture"]
    for index, heading in enumerate(REQUIRED_HEADINGS, start=1):
        content = f"Complete scientific content for section {index}."
        if heading == "## Citation and link requirements":
            content = (
                "Treat each atomic claim as the citation unit and bind one to five works. "
                "Example: (C001; [R001](https://doi.org/example)). "
                "Register the full GB/T 7714—2015 reference."
            )
        sections.extend([heading, "", content])
    return "\n\n".join(sections) + "\n"


def write_package(root: Path, request: str, guide: str | None = None) -> None:
    (root / "deep-research-request-v001.md").write_text(request, encoding="utf-8")
    guide_text = guide or (
        "# Follow-up\n\nSend `deep-research-request-v001.md` and save "
        "`deep-research-report-v001.md`.\n"
    )
    (root / "deep-research-follow-up-guide-v001.md").write_text(guide_text, encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        write_package(root, valid_request())
        require(validate(root)["valid"], "valid package")

        (root / "deep-research-request-v001.md").write_text(
            valid_request() + "\nPlugin version: 0.13.0\n", encoding="utf-8"
        )
        require(not validate(root)["valid"], "internal state must fail")

        (root / "deep-research-request-v001.md").write_text(
            valid_request() + ("x" * 12_001), encoding="utf-8"
        )
        require(not validate(root)["valid"], "hard length cap")

        (root / "deep-research-request-v001.md").write_text(
            valid_request().replace("Complete scientific content for section 1.", "[State what"),
            encoding="utf-8",
        )
        require(not validate(root)["valid"], "unresolved marker")

        (root / "deep-research-request-v001.md").write_text(
            valid_request().replace("one to five", "any number of"), encoding="utf-8"
        )
        require(not validate(root)["valid"], "one-to-five source limit")

    print("deep research package validator tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
