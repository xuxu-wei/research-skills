#!/usr/bin/env python3
"""Focused deterministic guards for complete artifacts and blind re-evaluation."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
IDEA_SECTIONS = (
    "One-sentence summary",
    "Research question and objectives",
    "Research content and work packages",
    "Core hypothesis",
    "Scientific significance",
    "Relevance, impact, and innovation",
    "Potential applications",
    "Data, materials, and evidence base",
    "Research methods",
    "Required analyses and evidence",
    "Feasibility, resources, and constraints",
    "Risks, assumptions, uncertainties, and stop conditions",
)
COMPARATIVE_ONLY = re.compile(
    r"^(this|the) (version|revision) (adds|changes|updates)|^compared with (the )?prior",
    re.I,
)
FORBIDDEN_REVIEW_HISTORY = (
    "revision-delta",
    "revision_delta",
    "evaluation-v001",
    "re-evaluation-v001",
    "proposal-v001.md",
    "manuscript-v001.md",
    "idea-snapshot-v001.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def idea_snapshot(plugin_version: str, version: int = 1, summary: str = "A complete current research idea.") -> str:
    body = [
        "---",
        "schema_version: research-idea.v2",
        f"plugin_version: {plugin_version}",
        f"artifact_id: idea-I01-001-v{version:03d}",
        "idea_id: I01-001",
        f"version_id: v{version:03d}",
        "parent_idea_ids: []",
        "based_on: []",
        "source_skill: multi-path-idea-generator",
        "created_round: 1",
        "status: draft",
        "frozen: true",
        "---",
        "",
    ]
    for heading in IDEA_SECTIONS:
        body.extend((f"## {heading}", "", summary if heading == IDEA_SECTIONS[0] else f"Complete {heading.lower()} content.", ""))
    return "\n".join(body)


def validate_snapshot(text: str) -> list[str]:
    errors: list[str] = []
    positions = []
    for heading in IDEA_SECTIONS:
        marker = f"## {heading}"
        if marker not in text:
            errors.append(f"missing:{heading}")
        else:
            positions.append(text.index(marker))
    if positions != sorted(positions):
        errors.append("section_order")
    match = re.search(r"## One-sentence summary\s+([^#\n].*)", text)
    if not match or COMPARATIVE_ONLY.search(match.group(1).strip()):
        errors.append("comparative_or_missing_summary")
    if len(re.findall(r"^## ", text, re.M)) != len(IDEA_SECTIONS):
        errors.append("partial_or_extra_body")
    return errors


def identity_status(before: dict[str, str], after: dict[str, str]) -> str:
    return "preserved" if before == after else "new_idea_required"


def review_history_visible(paths: list[str]) -> bool:
    lowered = "\n".join(paths).lower()
    return any(token in lowered for token in FORBIDDEN_REVIEW_HISTORY)


def manuscript_complete(text: str) -> bool:
    return all(re.search(rf"^## {heading}\s+\S", text, re.M) for heading in ("Introduction", "Methods", "Results", "Discussion"))


def proposal_complete(text: str) -> bool:
    required = ("Problem and gap", "Objectives", "Research plan", "Methods", "Feasibility", "Expected outputs")
    return all(re.search(rf"^## {re.escape(heading)}\s+\S", text, re.M) for heading in required)


def validate_probability(assessment: dict[str, object]) -> list[str]:
    errors: list[str] = []
    scopes = {"cover_letter_only", "full_artifact", "full_submission_package"}
    if assessment.get("assessment_scope") not in scopes:
        errors.append("scope")
    confidence = assessment.get("confidence")
    stages = (
        "editorial_screen_pass_probability",
        "acceptance_given_external_review",
        "eventual_acceptance_probability",
    )
    if confidence == "not_estimable":
        for stage in stages:
            value = assessment.get(stage, {})
            if isinstance(value, dict) and value.get("central_estimate") is not None:
                errors.append(f"not_estimable:{stage}")
        return errors
    values: list[float] = []
    for stage in stages:
        value = assessment.get(stage)
        if not isinstance(value, dict):
            errors.append(f"missing:{stage}")
            continue
        central = value.get("central_estimate")
        interval = value.get("plausible_interval")
        if not isinstance(central, (int, float)) or not 0 <= float(central) <= 1:
            errors.append(f"central:{stage}")
        else:
            values.append(float(central))
        if not isinstance(interval, list) or len(interval) != 2 or not all(isinstance(item, (int, float)) for item in interval):
            errors.append(f"interval:{stage}")
    if len(values) == 3 and abs(values[2] - values[0] * values[1]) > 0.02:
        errors.append("stage_math")
    if assessment.get("assessment_scope") == "cover_letter_only" and confidence == "high":
        errors.append("cover_letter_confidence")
    if assessment.get("benchmark_status") == "verified_public":
        sources = assessment.get("benchmark_sources")
        if not isinstance(sources, list) or not sources:
            errors.append("verified_source_missing")
        elif any(
            not all(source.get(field) for field in ("url", "checked_at", "source_type", "applicable_scope"))
            for source in sources
            if isinstance(source, dict)
        ):
            errors.append("verified_source_metadata")
    return errors


def require(value: bool, label: str) -> None:
    if not value:
        raise AssertionError(label)


def main() -> int:
    plugin_version = str(json.loads(read(PLUGIN / ".codex-plugin/plugin.json"))["version"])
    registry = yaml.safe_load(read(PLUGIN / "workflow-registry.yaml"))
    policy = registry.get("artifact_completeness_policy", {})
    require(policy.get("idea_schema") == "research-idea.v2", "registry idea schema")
    require(policy.get("article_schema") == "research-article.v6", "registry article schema")
    require(
        policy.get("fresh_re_evaluation", {}).get("forbidden")
        == ["prior_artifact", "revision_delta", "prior_report", "prior_score", "prior_decision"],
        "registry blind re-evaluation",
    )

    lifecycle = read(PLUGIN / "skills/research-idea-orchestrator/references/idea-artifact-lifecycle.md")
    docx_contract = read(PLUGIN / "skills/article-orchestrator/references/article-docx-delivery-contract.md")
    for marker in IDEA_SECTIONS:
        require(marker in lifecycle, f"lifecycle section {marker}")
    for marker in ("canonical_markdown_ref", "docx_sync_status", "render_qa_status", "missing_source_asset"):
        require(marker in docx_contract, f"DOCX contract {marker}")

    guards = 0
    with tempfile.TemporaryDirectory() as temp:
        node = Path(temp) / "03_ideas/nodes/I01-001"
        snapshots = node / "snapshots"
        snapshots.mkdir(parents=True)
        first = snapshots / "idea-snapshot-v001.md"
        second = snapshots / "idea-snapshot-v002.md"
        first.write_text(idea_snapshot(plugin_version, 1), encoding="utf-8", newline="\n")
        second.write_text(idea_snapshot(plugin_version, 2, "A complete revised research idea."), encoding="utf-8", newline="\n")
        require(not validate_snapshot(read(first)), "complete initial snapshot")
        require(not validate_snapshot(read(second)), "complete revised snapshot")
        require(digest(first) != digest(second), "version digest changes")
        guards += 3

        partial = "## One-sentence summary\n\nThis version adds one analysis.\n\n## Innovation\n\nChanged only."
        require(bool(validate_snapshot(partial)), "delta-only Idea rejected")
        require("comparative_or_missing_summary" in validate_snapshot(partial), "comparative summary rejected")
        guards += 2

        anchor = {
            "primary_research_question": "Q",
            "primary_objective": "O",
            "study_object": "P",
            "core_data_or_evidence_base": "D",
            "primary_unit_of_inference": "U",
        }
        require(identity_status(anchor, dict(anchor)) == "preserved", "same Idea stays in node")
        changed = dict(anchor, primary_research_question="Different Q")
        require(identity_status(anchor, changed) == "new_idea_required", "identity drift stops revision")
        guards += 2

    current_review_inputs = [
        "03_ideas/nodes/I01-001/snapshots/idea-snapshot-v002.md",
        "01_context/research-context.md",
        "anonymous-must-fix.md",
    ]
    require(not review_history_visible(current_review_inputs), "current-only review allowed")
    require(review_history_visible(current_review_inputs + ["revision-delta-r001.md"]), "delta review rejected")
    require(review_history_visible(current_review_inputs + ["idea-snapshot-v001.md"]), "prior snapshot review rejected")
    guards += 3

    proposal = "\n".join(f"## {h}\nComplete {h}." for h in ("Problem and gap", "Objectives", "Research plan", "Methods", "Feasibility", "Expected outputs"))
    article = "\n".join(f"## {h}\nComplete {h}." for h in ("Introduction", "Methods", "Results", "Discussion"))
    require(proposal_complete(proposal), "complete proposal accepted")
    require(not proposal_complete("## Methods\nOnly a changed method."), "partial proposal rejected")
    require(manuscript_complete(article), "complete article accepted")
    require(not manuscript_complete("## Results\nOnly changed results."), "partial article rejected")
    guards += 4

    portfolio = read(PLUGIN / "skills/idea-portfolio-assembler/templates/research-idea-portfolio.md")
    for marker in ("Complete one-sentence summary", "Scientific significance", "Potential applications", "Required analyses and evidence", "Current snapshot / version / SHA-256"):
        require(marker in portfolio, f"portfolio complete field {marker}")
        guards += 1

    readme_contract = read(PLUGIN / "skills/research-idea-orchestrator/references/project-readme-contract.md")
    for marker in (
        "## Current delivery",
        "## Current artifact",
        "## Status",
        "## Review summary",
        "## Next action",
        "## Publication probability",
        "eventual-acceptance interval",
        "Never give it to a reviewer",
    ):
        require(marker in readme_contract, f"project README contract {marker}")
        guards += 1
    for name in (
        "research-idea-orchestrator",
        "proposal-orchestrator",
        "article-orchestrator",
        "perspective-orchestrator",
        "research-polisher-orchestrator",
    ):
        text = read(PLUGIN / f"skills/{name}/SKILL.md")
        require("project-readme-contract.md" in text, f"{name} routes project README")
        require(
            "finish/pause/stop" in text or "finishing, pausing, or stopping" in text,
            f"{name} updates README on every terminal return",
        )
        guards += 2

    cover_skill = read(PLUGIN / "skills/article-cover-letter/SKILL.md")
    for marker in (
        "workflow_profile: article | perspective",
        "11_cover-letter/cover-letter-vNNN.md",
        "08_cover-letter/cover-letter-vNNN.md",
        "repeats_abstract_mechanically",
        "inputs_sufficient",
    ):
        require(marker in cover_skill, f"Cover Letter contract {marker}")
        guards += 1
    require("recommended_status" not in cover_skill, "Cover Letter check has no self-promotion decision")
    require("may_call: []" in cover_skill, "Cover Letter writer does not invoke its reviewer")
    guards += 2

    medical_skill = read(PLUGIN / "skills/medical-journal-review/SKILL.md")
    probability = read(PLUGIN / "skills/medical-journal-review/references/publication-probability-assessment.md")
    require("publication-probability-assessment.md" in medical_skill, "medical review conditionally loads probability contract")
    require("never create a separate probability artifact" in medical_skill, "probability stays in medical review")
    guards += 2
    for marker in (
        "assessment_scope: cover_letter_only | full_artifact | full_submission_package",
        "benchmark_status: verified_public | user_supplied | heuristic_only | unavailable",
        "eventual_acceptance_probability",
        "confidence: high | moderate | low | not_estimable",
        "built-in Search",
        "mathematically coherent",
        "domain_scope_limitations",
    ):
        require(marker in probability, f"publication probability contract {marker}")
        guards += 1

    fixture_assessments: dict[str, dict[str, object]] = {}
    for fixture_name in ("article", "perspective"):
        fixture = yaml.safe_load(read(REPO / f"tests/openai_phase4/{fixture_name}.yaml"))
        for event in fixture.get("events", []):
            report = event.get("review_report", {})
            assessment = report.get("publication_probability_assessment")
            if isinstance(assessment, dict):
                fixture_assessments[str(assessment.get("assessment_scope"))] = assessment
    require(not validate_probability(fixture_assessments["cover_letter_only"]), "cover-letter-only probability case")
    require(not validate_probability(fixture_assessments["full_artifact"]), "full-artifact probability case")
    guards += 2

    full_package = {
        **fixture_assessments["full_artifact"],
        "assessment_scope": "full_submission_package",
        "benchmark_status": "verified_public",
        "benchmark_sources": [{
            "url": "https://publisher.example/metrics",
            "checked_at": "2026-07-15",
            "source_type": "publisher",
            "applicable_scope": "named outlet and article type",
            "benchmark_value": "reported acceptance range",
        }],
        "confidence": "moderate",
    }
    not_estimable = {
        "assessment_scope": "full_artifact",
        "benchmark_status": "unavailable",
        "benchmark_sources": [],
        "editorial_screen_pass_probability": {"central_estimate": None, "plausible_interval": None},
        "acceptance_given_external_review": {"central_estimate": None, "plausible_interval": None},
        "eventual_acceptance_probability": {"central_estimate": None, "plausible_interval": None},
        "confidence": "not_estimable",
    }
    require(not validate_probability(full_package), "verified full-package probability case")
    require(not validate_probability(not_estimable), "not-estimable probability case")
    guards += 2

    reviewer_skills = {
        entry["name"]
        for entry in registry.get("skills", [])
        if entry.get("requires_independent_subagent") is True
    }
    for name in reviewer_skills:
        require(
            "project-readme-contract.md" not in read(PLUGIN / f"skills/{name}/SKILL.md"),
            f"reviewer {name} cannot receive project README",
        )
        guards += 1

    print(f"OpenAI artifact completeness guards passed: {guards}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
