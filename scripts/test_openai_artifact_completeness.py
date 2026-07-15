#!/usr/bin/env python3
"""Focused deterministic guards for complete artifacts and blind re-evaluation."""

from __future__ import annotations

import hashlib
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


def idea_snapshot(version: int = 1, summary: str = "A complete current research idea.") -> str:
    body = [
        "---",
        "schema_version: research-idea.v2",
        "plugin_version: 0.7.0-preview.3",
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


def require(value: bool, label: str) -> None:
    if not value:
        raise AssertionError(label)


def main() -> int:
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
        first.write_text(idea_snapshot(1), encoding="utf-8", newline="\n")
        second.write_text(idea_snapshot(2, "A complete revised research idea."), encoding="utf-8", newline="\n")
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

    print(f"OpenAI artifact completeness guards passed: {guards}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
