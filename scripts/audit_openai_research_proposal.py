#!/usr/bin/env python3
"""Audit the research-proposal skill package for structural consistency."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "research-skills-openai" / "skills"
PROPOSAL_SKILLS = {
    "proposal-context-brief-builder",
    "proposal-drafter",
    "proposal-evaluator",
    "proposal-orchestrator",
    "proposal-package-assembler",
    "proposal-readiness-triage",
    "proposal-refinement-controller",
    "proposal-review-panel",
    "sap-evaluator",
    "sap-refinement-controller",
    "sap-writer",
}


def skill_files() -> list[Path]:
    return [ROOT / name / "SKILL.md" for name in sorted(PROPOSAL_SKILLS)]


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def frontmatter_errors() -> list[str]:
    errors: list[str] = []
    for path in skill_files():
        data = path.read_bytes()
        text = data.decode("utf-8-sig", errors="replace")
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{rel(path)}: UTF-8 BOM present")
        if not data.startswith(b"---"):
            errors.append(f"{rel(path)}: frontmatter does not start at byte 0")
        match = re.search(r"\n---\s*\n", text[3:])
        if not match:
            errors.append(f"{rel(path)}: missing standard frontmatter closing marker")
            continue
        frontmatter = text[3 : match.start() + 3]
        if not re.search(r"^name:\s*\S+", frontmatter, re.M):
            errors.append(f"{rel(path)}: missing name")
        if not re.search(r"^description:\s*\S+", frontmatter, re.M):
            errors.append(f"{rel(path)}: missing description")
        top_level = re.findall(r"^([A-Za-z0-9_-]+):", frontmatter, re.M)
        if set(top_level) != {"name", "description"} or len(top_level) != 2:
            errors.append(f"{rel(path)}: OpenAI frontmatter must contain only name and description")
        if "metadata:" in frontmatter or "hermes:" in frontmatter:
            errors.append(f"{rel(path)}: Hermes metadata is not allowed in OpenAI profile")
    return errors


def all_files() -> set[str]:
    return {
        p.resolve().relative_to(REPO.resolve()).as_posix()
        for name in PROPOSAL_SKILLS
        for p in (ROOT / name).rglob("*")
        if p.is_file()
    }


def reference_errors() -> list[str]:
    files = all_files()
    errors: list[str] = []
    ref_pattern = re.compile(r"`([^`]+(?:\.md|\.py|\.sh|\.yaml|\.json))`")
    for name in sorted(PROPOSAL_SKILLS):
        for path in sorted((ROOT / name).rglob("*.md")):
            text = read(path)
            for match in ref_pattern.finditer(text):
                target = match.group(1)
                if target.startswith(("references/", "templates/", "scripts/")):
                    candidate = (path.parent / target).resolve()
                    rel_candidate = candidate.relative_to(REPO.resolve()).as_posix()
                elif target.startswith("../"):
                    candidate = (path.parent / target).resolve()
                    if REPO.resolve() not in candidate.parents and candidate != REPO.resolve():
                        continue
                    rel_candidate = candidate.relative_to(REPO.resolve()).as_posix()
                else:
                    continue
                if rel_candidate not in files:
                    errors.append(f"{rel(path)}: unresolved reference `{target}` -> {rel_candidate}")
    return errors


def placeholder_errors() -> list[str]:
    errors: list[str] = []
    delegate = ROOT / "proposal-orchestrator" / "references" / "delegate-brief-templates.md"
    if delegate.exists():
        text = read(delegate)
        if "[Insert " in text:
            errors.append(f"{rel(delegate)}: legacy [Insert ...] placeholder remains")
    return errors


def route_consistency_errors() -> list[str]:
    errors: list[str] = []
    orch = read(ROOT / "proposal-orchestrator" / "SKILL.md")
    panel = read(ROOT / "proposal-review-panel" / "SKILL.md")
    package = read(ROOT / "proposal-package-assembler" / "SKILL.md")
    required_orch_terms = [
        "workflow-state-schema.md",
        "artifact-naming-and-directory-rules.md",
        "10_state/artifact-index.md",
        "04_drafts/proposal-vNNN.md",
        "blind_mock_review",
        "standard_panel",
        "sap-refinement-controller",
        "support_after_major_revision",
        "Submission-Clean Proposal",
    ]
    for term in required_orch_terms:
        if term not in orch:
            errors.append(f"proposal-orchestrator missing route term: {term}")
    if "context_aware_internal_review" not in panel:
        errors.append("proposal-review-panel missing context-aware internal review mode")
    if "must not include context brief" not in panel and "Do not pass individual reviewers" not in panel:
        errors.append("proposal-review-panel missing blind-review forbidden-context rule")
    if "does not rewrite" not in package or "Submission-Clean Boundary" not in package:
        errors.append("proposal-package-assembler missing cleanup boundary")
    naming = read(ROOT / "proposal-orchestrator" / "references" / "artifact-naming-and-directory-rules.md")
    required_naming_terms = [
        "research-proposal-projects/<project-slug>",
        "10_state/workflow-state.yaml",
        "10_state/artifact-index.md",
        "04_drafts/proposal-v001.md",
        "06_revisions/round-001",
        "08_panel/proposal-v003-standard-blind-panel-summary.md",
        "Prior versions must not be overwritten",
    ]
    for term in required_naming_terms:
        if term not in naming:
            errors.append(f"proposal artifact naming rules missing term: {term}")
    schema = read(ROOT / "proposal-orchestrator" / "references" / "workflow-state-schema.md")
    for term in ("project_root", "artifact_index_path", "Artifact Registry", "based_on"):
        if term not in schema:
            errors.append(f"workflow-state-schema missing artifact registry term: {term}")
    return errors


def orphan_support_warnings() -> list[str]:
    warnings: list[str] = []
    for skill_dir in [ROOT / name for name in sorted(PROPOSAL_SKILLS)]:
        skill_text = read(skill_dir / "SKILL.md")
        for sub in ("references", "templates", "scripts"):
            folder = skill_dir / sub
            if not folder.exists():
                continue
            for support in sorted(p for p in folder.rglob("*") if p.is_file()):
                local = support.relative_to(skill_dir).as_posix()
                if local not in skill_text:
                    warnings.append(f"{rel(support)}: not listed in {rel(skill_dir / 'SKILL.md')}")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-orphans", action="store_true", help="treat unlisted support docs as errors")
    args = parser.parse_args()

    errors: list[str] = []
    errors.extend(frontmatter_errors())
    errors.extend(reference_errors())
    errors.extend(placeholder_errors())
    errors.extend(route_consistency_errors())
    warnings = orphan_support_warnings()

    if args.strict_orphans:
        errors.extend(warnings)

    print(f"research-proposal audit root: {rel(ROOT)}")
    print(f"errors: {len(errors)}")
    for item in errors:
        print(f"ERROR: {item}")
    print(f"warnings: {len(warnings)}")
    for item in warnings:
        print(f"WARN: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
