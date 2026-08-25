#!/usr/bin/env python3
"""Audit the research-proposal skill package for structural consistency."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


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
        "existing_draft",
        "draft_and_external_review",
        "package_only",
        "sap-refinement-controller",
        "pending_review",
        "independent_review_pending",
        "human_signoff_required",
    ]
    for term in required_orch_terms:
        if term not in orch:
            errors.append(f"proposal-orchestrator missing route term: {term}")
    if "context_aware_internal_review" not in panel:
        errors.append("proposal-review-panel missing context-aware internal review mode")
    if "Do not read context brief" not in panel and "must not include context brief" not in panel and "Do not pass individual reviewers" not in panel:
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


def background_argumentation_contract_errors() -> list[str]:
    errors: list[str] = []
    drafter = read(ROOT / "proposal-drafter" / "SKILL.md")
    orchestrator = read(ROOT / "proposal-orchestrator" / "SKILL.md")
    evaluator = read(ROOT / "proposal-evaluator" / "SKILL.md")
    background_workflow = read(ROOT / "proposal-orchestrator" / "references" / "proposal-background-path-workflow.md")
    state = read(ROOT / "proposal-orchestrator" / "references" / "workflow-state-schema.md")
    naming = read(ROOT / "proposal-orchestrator" / "references" / "artifact-naming-and-directory-rules.md")
    delegate = "\n".join(
        (
            read(ROOT / "proposal-orchestrator" / "references" / "delegate-background-path-options-brief.md"),
            read(ROOT / "proposal-orchestrator" / "references" / "delegate-brief-templates.md"),
        )
    )

    options_path = ROOT / "proposal-drafter" / "templates" / "template-proposal-background-path-options.yaml"
    selection_path = ROOT / "proposal-orchestrator" / "templates" / "template-proposal-background-path-selection.yaml"
    plan_path = ROOT / "proposal-drafter" / "templates" / "template-proposal-content-plan.yaml"
    options = yaml.safe_load(read(options_path))
    selection = yaml.safe_load(read(selection_path))
    plan = yaml.safe_load(read(plan_path))

    if options.get("schema") != "proposal-background-path-options.v1":
        errors.append("background options schema must be proposal-background-path-options.v1")
    if options.get("recommendation", "missing") is not None or options.get("ranking", "missing") is not None:
        errors.append("background options must keep recommendation and ranking null")
    if options.get("selection_status") != "human_background_path_selection_required":
        errors.append("background options missing human selection stop")
    if options.get("option_count") not in (2, 3):
        errors.append("background options template must demonstrate a 2-3 option count")
    required_option_fields = {
        "option_id", "primary_mode", "organizing_axis", "one_sentence_argument_logic",
        "opening", "current_status_units", "mappings", "synthesis",
        "evidence_requirements", "strengths", "tradeoffs", "loss_of_focus_risks",
    }
    sample_option = (options.get("options") or [{}])[0]
    if not required_option_fields <= set(sample_option):
        errors.append("background options sample is missing required per-option fields")

    if selection.get("schema") != "proposal-background-path-selection.v1":
        errors.append("background selection schema must be proposal-background-path-selection.v1")
    for key in ("selection_mode", "user_authorization_text", "selected_option_id", "accepted_sole_path", "user_requested_local_modifications", "rejected_option_ids", "selection_source", "options_ref"):
        if key not in selection:
            errors.append(f"background selection template missing {key}")
    if selection.get("selection_source") != "user":
        errors.append("background selection source must be user")
    for key in ("selection_mode", "selected_option_id", "accepted_sole_path", "options_ref"):
        if selection.get(key) is not None:
            errors.append(f"background selection template must leave {key} null until user authorization")

    if plan.get("schema") != "proposal-content-plan.v2":
        errors.append("new proposal content plan must use proposal-content-plan.v2")
    background = plan.get("background_argumentation") or {}
    for key in ("selection_source", "selection_mode", "user_authorization_text", "selected_path_ref", "primary_mode", "opening", "argument_units", "synthesis"):
        if key not in background:
            errors.append(f"v2 content plan background_argumentation missing {key}")

    combined_planning = "\n".join((drafter, orchestrator, background_workflow, delegate)).lower()
    for term in (
        "background_path_options", "two or three", "recommendation: null", "ranking: null",
        "only one", "sole_path_acceptance", "user_explicit", "binding_constraint", "hybrid", "pairwise distinct",
        "proposal-content-plan.v2", "human_background_path_selection_required",
    ):
        if term not in combined_planning:
            errors.append(f"background planning contract missing term: {term}")
    for term in ("rejects all", "local modifications", "new candidate round"):
        if term not in (orchestrator + background_workflow).lower():
            errors.append(f"proposal orchestrator recovery contract missing term: {term}")

    for term in (
        "background_path_options_visible: false",
        "background_path_selection_visible: false",
        "content_plan_visible: false",
        "systematic background",
        "progressive background",
        "literal word `综上`",
    ):
        if term not in evaluator:
            errors.append(f"proposal evaluator background/isolation contract missing term: {term}")

    for term in (
        "proposal_background_path_options", "proposal_background_path_selection",
        "human_background_path_selection_required", "clarification_stop", "proposal-content-plan.v2",
    ):
        if term not in state:
            errors.append(f"workflow state missing background contract term: {term}")
    for term in (
        "proposal-background-path-options-v001.yaml",
        "proposal-background-path-selection-v001.yaml",
        "must never be sent to the full writer or blind final evaluator",
    ):
        if term not in naming:
            errors.append(f"artifact naming/isolation rules missing term: {term}")
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
    errors.extend(background_argumentation_contract_errors())
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
