#!/usr/bin/env python3
"""Validate the current cross-workflow reader-readiness architecture.

This suite is intentionally independent of historical Roadmap phase fixtures.
It checks only source contracts introduced or relied upon by the current change.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def ordered(text: str, *markers: str) -> bool:
    cursor = -1
    for marker in markers:
        cursor = text.find(marker, cursor + 1)
        if cursor < 0:
            return False
    return True


def main() -> int:
    manifest = json.loads(read(PLUGIN / ".codex-plugin" / "plugin.json"))
    registry = yaml.safe_load(read(PLUGIN / "workflow-registry.yaml"))
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    reviewers = [item for item in registry["skills"] if item.get("requires_independent_subagent")]

    require(manifest["version"] == "0.11.0", "manifest version")
    require(registry["plugin_version"] == "0.11.0", "registry version")
    require(registry["schema_version"] == 6, "registry schema")
    require(len(skill_files) == 51, "skill count")
    require(len(reviewers) == 22, "reviewer count")

    perspective_machine = registry["workflow_state_machines"]["perspective"]
    require(
        perspective_machine["before_panel"]
        == ["current_perspective_scientific_evaluation_complete", "no_unresolved_fatal_finding"],
        "Perspective scientific evaluation precedes panel",
    )
    require(
        "final_perspective_evaluation_complete" in perspective_machine["before_packaging"],
        "Perspective final evaluation precedes packaging",
    )
    stage_contract = perspective_machine["evaluation_stage_contract"]
    require(stage_contract["scientific"]["dispatch_before"] == "panel", "Perspective scientific evaluator stage")
    require(
        stage_contract["final"]["dispatch_after"]
        == ["applicable_panel_route_closed", "editorial_readiness_complete", "content_preservation_complete"],
        "Perspective final evaluator stage",
    )
    perspective_edges = [edge for edge in registry["workflow_edges"] if edge["workflow"] == "perspective"]
    panel_edge = next(edge for edge in perspective_edges if edge["destination"] == "perspective-review-panel")
    require("scientific_perspective_evaluation_passed" in panel_edge["trigger"], "Perspective panel trigger")

    shared = registry["cross_workflow_editorial_readiness_policy"]
    require(shared["workflows"] == ["idea", "proposal", "perspective", "article"], "workflow scope")
    require(shared["macro_reviewer"] == "research-narrative-assessor", "macro reviewer")
    require(shared["meso_micro_reviewer"] == "academic-language-assessor", "language reviewer")
    require(shared["reviewers_run_in_parallel_on_same_frozen_reader_artifact_or_bundle"], "parallel readiness")
    require(shared["repair_interface"]["single_writer_brief_format"] == "yaml", "YAML writer brief")
    require(shared["repair_interface"]["raw_assessment_reports_visible_to_writer"] is False, "raw reports sealed")
    require(shared["repair_interface"]["writer_uses_same_owner_for_bounded_section_passes"], "same writer bounded passes")
    require(shared["repair_interface"]["multiple_fragment_writers_forbidden"], "no fragmented writers")
    require(shared["preservation"]["fresh_independent_preservation_review_required_after_repair"], "fresh preservation review")
    require(shared["fresh_readiness"]["fresh_narrative_and_language_reassessment_required_after_repair"], "fresh readiness reassessment")
    require(shared["logical_integrity"]["sha_or_content_digest_forbidden_in_new_llm_facing_artifacts"], "no LLM-facing hashes")
    require(shared["logical_integrity"]["legacy_digest_fields"] == "readable_but_ignored", "legacy digest compatibility")

    limitation = shared["limitation_policy"]
    require(limitation["omit_elsewhere"], "limitations omitted outside authority")
    require(limitation["cross_reference_or_pointer_elsewhere_forbidden"], "no limitation pointers")
    require("advance_the_immediate_reasoning" in limitation["exception"], "narrow limitation exception")

    terminology = shared["terminology_policy"]
    require(terminology["reviewer"] == "academic-language-assessor", "language owns terminology")
    require(terminology["separate_terminology_skill_or_artifact_forbidden"], "no separate terminology interface")
    require(terminology["single_paper_is_insufficient_to_establish_standard_usage"], "standardity evidence threshold")
    require(
        set(terminology["core_term_roles"])
        == {"title", "summary_or_abstract", "question", "objective", "contribution", "study_object", "measurement", "inference", "design", "interpretation"},
        "core-term definition",
    )

    narrative = read(SKILLS / "research-narrative-assessor" / "SKILL.md")
    profiles_text = read(SKILLS / "research-narrative-assessor" / "references" / "profiles.md")
    for profile in ("Idea", "Proposal", "Perspective", "Article"):
        require(profile in profiles_text, f"narrative profile {profile}")
    for decision in (
        "narrative_ready",
        "minor_narrative_revision",
        "major_narrative_revision",
        "clarification_required",
        "independent_review_pending",
    ):
        require(decision in narrative, f"narrative decision {decision}")
    require("narrative-repair-plan-rNNN.yaml" in narrative, "YAML repair output")
    require("content-preservation" in narrative.lower(), "preservation mode")
    shared_source = "\n".join(
        read(path)
        for path in (SKILLS / "research-narrative-assessor").rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".py"}
    )
    require("tests/" not in shared_source and "tests\\" not in shared_source, "shared assessor embeds a fixture path")
    progressive_examples = read(
        SKILLS / "research-narrative-assessor" / "references" / "progressive-error-examples.md"
    )
    normalized_examples = " ".join(progressive_examples.split())
    for generalization_guard in (
        "Do not match literal phrases",
        "Positive boundary:",
        "Error boundary:",
        "no simpler faithful route exists",
    ):
        require(
            generalization_guard in normalized_examples,
            f"shared assessor example generalization guard: {generalization_guard}",
        )

    perspective_examples = "\n".join(
        read(path)
        for path in (
            SKILLS / "perspective-input-builder" / "SKILL.md",
            SKILLS / "perspective-input-builder" / "templates" / "perspective-input-template.md",
            SKILLS / "perspective-argument-architect" / "references" / "contestability-constraints.md",
            SKILLS / "perspective-claim-evidence-curator" / "references" / "evidence-grading.md",
        )
    )
    for leaked_example in ("AI 辅助", "中药复方", "多中心 RCT", "降低了 30%", "某些传染病", "Nature Medicine", "Lancet Digital Health"):
        require(leaked_example not in perspective_examples, f"Perspective example specialization: {leaked_example}")

    language = read(SKILLS / "academic-language-assessor" / "SKILL.md")
    terminology_ref = read(SKILLS / "academic-language-assessor" / "references" / "terminology-review.md")
    require("exact recommended" in (language + terminology_ref).lower(), "terminology replacement is executable")
    require("first-use" in (language + terminology_ref).lower(), "first-use guidance")
    require("one paper" in terminology_ref.lower(), "single-paper safeguard")
    require("term-register" not in (language + terminology_ref), "no term-register artifact")

    orchestrators = {
        "idea": (SKILLS / "research-idea-orchestrator" / "SKILL.md", "Establish editorial readiness", "**Evaluate.**"),
        "proposal": (SKILLS / "proposal-orchestrator" / "SKILL.md", "**Assess and normalize.**", "**Run blind final evaluation.**"),
        "perspective": (SKILLS / "perspective-orchestrator" / "SKILL.md", "STEP 9: Editorial Quality Cycle", "STEP 10: Final Evaluator"),
        "article": (SKILLS / "article-orchestrator" / "SKILL.md", "**Assess readiness.**", "**Evaluate the delivery object.**"),
    }
    for workflow, (path, readiness_marker, final_marker) in orchestrators.items():
        text = read(path)
        require("research-narrative-assessor" in text, f"{workflow} narrative route")
        require("academic-language-assessor" in text, f"{workflow} language route")
        require(ordered(text, readiness_marker, final_marker), f"{workflow} readiness precedes final evaluator")
        require("medical-journal-review" in text, f"{workflow} journal review route")

    proposal_drafter = read(SKILLS / "proposal-drafter" / "SKILL.md")
    require("proposal-content-plan" in proposal_drafter, "proposal content plan")
    require("fresh" in proposal_drafter.lower() and "writer" in proposal_drafter.lower(), "separate proposal planner/writer")

    perspective_architect = read(SKILLS / "perspective-argument-architect" / "SKILL.md")
    require("paragraph" in perspective_architect.lower() and "reader" in perspective_architect.lower(), "perspective reader-facing architecture")

    article_context = read(SKILLS / "article-context-builder" / "SKILL.md")
    article_readiness = read(SKILLS / "article-readiness-triage" / "SKILL.md")
    for marker in ("complete material inventory", "semantic authority"):
        require(marker in (article_context + article_readiness).lower(), f"article input discovery: {marker}")
    require("every supplied file" in article_context.lower(), "article intake cannot hide supplied material")

    evaluator_markers = {
        "idea": ("only project artifact", "other reviewer output", "prior versions", "deltas", "prior scores/decisions"),
        "proposal": ("final proposal", "context/readiness report", "repair brief", "delta", "prior evaluation"),
        "perspective": ("final perspective alone", "narrative/language report", "repair brief", "revision delta", "previous draft"),
        "article": ("final manuscript", "narrative and language assessors", "repair briefs", "deltas", "prior evaluations"),
    }
    for workflow, evaluator_name in (
        ("idea", "idea-evaluator"),
        ("proposal", "proposal-evaluator"),
        ("perspective", "perspective-evaluator"),
        ("article", "article-evaluator"),
    ):
        text = " ".join(read(SKILLS / evaluator_name / "SKILL.md").lower().split())
        require("files_read" in text, f"{workflow} evaluator files_read")
        require("current" in text and "complete" in text, f"{workflow} final current artifact")
        require(all(term in text for term in evaluator_markers[workflow]), f"{workflow} evaluator forbidden history")

    # New interfaces use readable logical identity. Legacy compatibility prose may
    # mention digests, but no newly produced field may serialize one.
    interface_roots = [
        SKILLS / "research-narrative-assessor",
        SKILLS / "proposal-orchestrator",
        SKILLS / "perspective-orchestrator",
        SKILLS / "article-orchestrator",
    ]
    serialized_field = re.compile(r"(?im)^\s*[a-z0-9_-]*(?:sha256|content_digest|source_digest|file_digest)\s*:")
    for root in interface_roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}:
                require(not serialized_field.search(read(path)), f"new persisted digest field: {path.relative_to(REPO)}")

    print("cross-workflow narrative contract: 51 skills, 22 reviewers, all guards passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
