#!/usr/bin/env python3
"""Generate the machine-auditable registry for the OpenAI research plugin."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"
HERMES_SKILLS = REPO / "research-skills"

REVIEWERS = {
    "academic-language-assessor",
    "medical-journal-review",
    "methodology-statistics-preflight",
    "idea-evaluator",
    "idea-adversarial-review-panel",
    "proposal-readiness-triage",
    "proposal-evaluator",
    "proposal-review-panel",
    "sap-evaluator",
    "article-readiness-triage",
    "article-methods-statistics-auditor",
    "article-claim-auditor",
    "article-evaluator",
    "article-review-panel",
    "article-submission-compositor",
    "perspective-evaluator",
    "perspective-review-panel",
    "perspective-final-compositor",
}

IMPLICIT = {
    "research-idea-orchestrator",
    "proposal-orchestrator",
    "article-orchestrator",
    "perspective-orchestrator",
    "research-opportunity-mapper",
    "academic-deep-search",
    "pubmed",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def skill_name(path: Path) -> str:
    match = re.search(r"^name:\s*[\"']?([^\r\n\"']+)", read(path), re.M)
    if not match:
        raise ValueError(f"Missing skill name: {path}")
    return match.group(1).strip()


def related_skills(source_skill: Path, installed: set[str]) -> list[str]:
    if not source_skill.exists():
        return []
    text = read(source_skill)
    frontmatter_end = text.find("\n---", 4)
    frontmatter = text[4:frontmatter_end] if frontmatter_end >= 0 else ""
    match = re.search(
        r"^\s*related_skills:\s*(?:\[([^\]]*)\]|\n((?:\s+-[^\n]*\n?)+))",
        frontmatter,
        re.M,
    )
    if not match:
        return []
    if match.group(1) is not None:
        values = [item.strip().strip("'\"") for item in match.group(1).split(",")]
    else:
        values = re.findall(r"^\s+-\s+([A-Za-z0-9_-]+)\s*$", match.group(2), re.M)
    return sorted({value for value in values if value in installed})


def role_for(name: str) -> str:
    if name in REVIEWERS:
        return "reviewer"
    if name.endswith("orchestrator"):
        return "orchestrator"
    if "assembler" in name:
        return "assembler"
    if "refinement-controller" in name:
        return "controller"
    if "drafter" in name or name.endswith("writer"):
        return "drafter"
    if "generator" in name:
        return "generator"
    if name in {"research-opportunity-mapper", "academic-deep-search", "pubmed"}:
        return "retrieval"
    if any(token in name for token in ("builder", "curator", "architect", "grounder", "cover-letter")):
        return "builder"
    return "utility"


def io_contract(role: str) -> tuple[str, str]:
    contracts = {
        "reviewer": ("frozen_artifacts_and_review_brief", "review_or_verification_report"),
        "orchestrator": ("user_inputs_and_existing_workflow_artifacts", "workflow_state_and_final_handoff"),
        "assembler": ("evaluated_artifacts_and_workflow_state", "final_handoff_package"),
        "controller": ("evaluation_findings_and_current_artifact", "revision_plan_delta_and_routing"),
        "drafter": ("approved_context_evidence_and_revision_plan", "versioned_draft_artifact"),
        "generator": ("context_and_opportunity_artifacts", "candidate_artifact_set"),
        "retrieval": ("research_question_source_scope_and_existing_evidence", "source_grounded_retrieval_artifact"),
        "builder": ("approved_upstream_artifacts", "structured_builder_artifact"),
        "utility": ("task_specific_inputs", "task_specific_artifact"),
    }
    return contracts[role]


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> int:
    skill_files = sorted(SKILLS.rglob("SKILL.md"))
    names = {skill_name(path) for path in skill_files}
    if len(skill_files) != 46 or len(names) != 46:
        raise RuntimeError(f"Expected 46 unique skills, found {len(skill_files)} files and {len(names)} names")
    if not REVIEWERS <= names:
        raise RuntimeError(f"Reviewer registry references missing skills: {sorted(REVIEWERS - names)}")
    hermes_by_name = {
        skill_name(path): path
        for path in HERMES_SKILLS.rglob("SKILL.md")
        if skill_name(path) in names
    }
    missing_sources = names - set(hermes_by_name)
    if missing_sources:
        raise RuntimeError(f"Missing Hermes lineage sources: {sorted(missing_sources)}")
    manifest = json.loads(read(PLUGIN / ".codex-plugin" / "plugin.json"))
    plugin_version = str(manifest["version"])

    lines = [
        "schema_version: 1",
        f"plugin_version: {quote(plugin_version)}",
        "review_execution:",
        "  isolation_mode: fresh_subagent",
        "  inline_fallback: false",
        "  prior_scores_visible_to_reviewer: false",
        "  source_artifacts_read_only: true",
        "skills:",
    ]
    for skill_md in skill_files:
        name = skill_name(skill_md)
        source_skill = hermes_by_name[name]
        source_relative = source_skill.parent.relative_to(HERMES_SKILLS)
        package = source_relative.parts[0]
        role = role_for(name)
        allowed_inputs, output = io_contract(role)
        related = related_skills(source_skill, names)
        lines.extend(
            [
                f"  - name: {quote(name)}",
                f"    package: {quote(package)}",
                f"    role: {quote(role)}",
                f"    related_skills: [{', '.join(quote(item) for item in related)}]",
                f"    invocation_policy: {quote('implicit' if name in IMPLICIT else 'explicit_or_orchestrated')}",
                f"    requires_independent_subagent: {'true' if name in REVIEWERS else 'false'}",
                f"    allowed_input_artifacts: {quote(allowed_inputs)}",
                f"    output_artifact_type: {quote(output)}",
            ]
        )

    (PLUGIN / "workflow-registry.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote registry for {len(skill_files)} skills and {len(REVIEWERS)} reviewers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
