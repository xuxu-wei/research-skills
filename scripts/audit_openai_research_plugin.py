#!/usr/bin/env python3
"""Audit the ChatGPT/Codex research preview plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"
REGISTRY = PLUGIN / "workflow-registry.yaml"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE = REPO / ".agents" / "plugins" / "marketplace.json"

EXPECTED_SKILLS = 46
EXPECTED_REVIEWERS = 18

FORBIDDEN_RESIDUES = {
    "delegate_task": re.compile(r"\bdelegate_task\b"),
    "skill_view": re.compile(r"\bskill_view\b"),
    "Gemini": re.compile(r"\bGemini\b", re.I),
    "Hermes runtime path": re.compile(r"(?:/home/ubuntu/\.hermes|~/\.hermes|\\\.hermes\\)", re.I),
    "Hermes timeout": re.compile(r"child_timeout_seconds"),
    "execute_code": re.compile(r"\bexecute_code\b"),
    "inline reviewer fallback": re.compile(r"run reviewers? inline|inline with strict isolation", re.I),
}

REVIEW_FIELDS = {
    "review_id",
    "reviewer_skill",
    "reviewer_instance_id",
    "workflow_id",
    "round_id",
    "input_artifact_ids",
    "input_versions",
    "files_read",
    "isolation_mode",
    "prior_scores_visible",
    "source_edits_performed",
    "decision",
    "findings",
    "unresolved_issues",
}

FINAL_SUBMISSION_SKILLS = {
    "article-submission-compositor",
    "article-cover-letter",
    "article-orchestrator",
    "proposal-package-assembler",
    # These two skills describe a legitimate research topic/contribution type;
    # the wording is not a workflow gate or safety policy.
    "perspective-input-builder",
    "perspective-argument-architect",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---", 4)
    if end < 0:
        return "", text
    return text[4:end], text[end + 4 :]


def top_level_keys(frontmatter: str) -> list[str]:
    return [match.group(1) for match in re.finditer(r"^([A-Za-z0-9_-]+):", frontmatter, re.M)]


def skill_name(path: Path) -> str | None:
    frontmatter, _ = split_frontmatter(read(path))
    match = re.search(r"^name:\s*[\"']?([^\r\n\"']+)", frontmatter, re.M)
    return match.group(1).strip() if match else None


def registry_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for block in re.split(r"(?m)^  - name:\s*", text)[1:]:
        first, *rest = block.splitlines()
        entry: dict[str, str] = {"name": first.strip().strip('"')}
        for line in rest:
            match = re.match(r"^    ([A-Za-z0-9_-]+):\s*(.*)$", line)
            if not match:
                continue
            entry[match.group(1)] = match.group(2).strip()
        entries.append(entry)
    return entries


def registry_related(raw: str) -> list[str]:
    if not raw.startswith("["):
        return []
    return [item.strip().strip('"') for item in raw[1:-1].split(",") if item.strip()]


def referenced_file_errors(skill_md: Path) -> list[str]:
    text = read(skill_md)
    references = set(
        re.findall(
            r"`((?:[A-Za-z0-9_-]+/)?(?:references|templates|scripts)/[^`]+\.(?:md|py|yaml|yml|json))`",
            text,
        )
    )
    references.update(
        re.findall(
            r"\]\((?:\./)?((?:[A-Za-z0-9_-]+/)?(?:references|templates|scripts)/[^)#]+)(?:#[^)]+)?\)",
            text,
        )
    )
    errors: list[str] = []
    for reference in sorted(references):
        first = reference.split("/", 1)[0]
        if first in {"references", "templates", "scripts"}:
            target = skill_md.parent / reference
        elif (SKILLS / first / "SKILL.md").exists():
            target = SKILLS / reference
        else:
            continue
        if not target.exists():
            errors.append(f"{relative(skill_md)}: missing referenced file `{reference}`")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    manifest_version = ""

    if not MANIFEST.exists():
        errors.append("missing plugin manifest")
    else:
        manifest = json.loads(read(MANIFEST))
        if manifest.get("name") != "research-skills-openai":
            errors.append("plugin manifest name must be research-skills-openai")
        manifest_version = str(manifest.get("version", ""))
        if not re.fullmatch(r"0\.1\.0(?:\+codex\.[A-Za-z0-9._-]+)?", manifest_version):
            errors.append("plugin manifest version must be 0.1.0 or a single Codex cachebuster variant")
        if manifest.get("skills") != "./skills/":
            errors.append("plugin manifest skills must be ./skills/")
        if "Preview" not in str(manifest.get("interface", {}).get("displayName", "")):
            errors.append("plugin display name must identify Preview status")

    if not MARKETPLACE.exists():
        errors.append("missing repo marketplace")
    else:
        marketplace = json.loads(read(MARKETPLACE))
        entries = marketplace.get("plugins", [])
        matching = [entry for entry in entries if entry.get("name") == "research-skills-openai"]
        if len(matching) != 1:
            errors.append("marketplace must contain exactly one research-skills-openai entry")
        else:
            source = matching[0].get("source", {})
            if source.get("source") != "git-subdir" or source.get("ref") != "main":
                errors.append("marketplace source must be git-subdir tracking main")

    skill_files = sorted(SKILLS.rglob("SKILL.md"))
    names: dict[str, Path] = {}
    if len(skill_files) != EXPECTED_SKILLS:
        errors.append(f"expected {EXPECTED_SKILLS} skills, found {len(skill_files)}")
    for skill_md in skill_files:
        text = read(skill_md)
        frontmatter, body = split_frontmatter(text)
        name = skill_name(skill_md)
        if not name:
            errors.append(f"{relative(skill_md)}: missing name")
            continue
        if name in names:
            errors.append(f"duplicate skill name {name}")
        names[name] = skill_md
        if name != skill_md.parent.name:
            errors.append(f"{relative(skill_md)}: name does not match parent directory")
        if skill_md.parent.parent != SKILLS:
            errors.append(f"{relative(skill_md)}: plugin skills must be direct children of skills/")
        keys = top_level_keys(frontmatter)
        if set(keys) != {"name", "description"} or len(keys) != 2:
            errors.append(f"{relative(skill_md)}: frontmatter keys must be exactly name and description; got {keys}")
        if "metadata.hermes" in text or re.search(r"(?m)^\s*hermes:\s*$", frontmatter):
            errors.append(f"{relative(skill_md)}: Hermes metadata is forbidden in OpenAI profile")
        openai_yaml = skill_md.parent / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            errors.append(f"{relative(skill_md)}: missing agents/openai.yaml")
        errors.extend(referenced_file_errors(skill_md))
        if name not in FINAL_SUBMISSION_SKILLS and re.search(
            r"\b(?:ethics?|ethical|IRB|privacy|regulatory|informed consent)\b", body, re.I
        ):
            errors.append(f"{relative(skill_md)}: pre-submission ethics/privacy/regulatory gate residue")

    if not REGISTRY.exists():
        errors.append("missing workflow-registry.yaml")
        entries = []
    else:
        registry_text = read(REGISTRY)
        if f'plugin_version: "{manifest_version}"' not in registry_text:
            errors.append("registry plugin version does not match manifest")
        entries = registry_entries(registry_text)
        if len(entries) != EXPECTED_SKILLS:
            errors.append(f"registry expected {EXPECTED_SKILLS} entries, found {len(entries)}")

    registry_names = {entry.get("name", "") for entry in entries}
    if registry_names != set(names):
        errors.append(
            f"registry/skill name mismatch: missing={sorted(set(names)-registry_names)} extra={sorted(registry_names-set(names))}"
        )
    reviewers = [entry for entry in entries if entry.get("requires_independent_subagent") == "true"]
    if len(reviewers) != EXPECTED_REVIEWERS:
        errors.append(f"expected {EXPECTED_REVIEWERS} independent reviewers, found {len(reviewers)}")
    for entry in entries:
        name = entry.get("name", "")
        for related in registry_related(entry.get("related_skills", "")):
            if related not in registry_names:
                errors.append(f"registry {name}: unresolved related skill {related}")
    for entry in reviewers:
        name = entry["name"]
        path = names.get(name)
        if not path:
            continue
        text = read(path)
        if "## Independent Execution Contract" not in text:
            errors.append(f"{relative(path)}: missing Independent Execution Contract")
        if "independent_review_pending" not in text:
            errors.append(f"{relative(path)}: missing independent_review_pending stop route")
        if not re.search(r"read-only", text, re.I):
            errors.append(f"{relative(path)}: reviewer inputs are not explicitly read-only")
        if not re.search(r"do not (?:edit|draft|rewrite|polish|repair)|不得.*(?:修改|起草|重写|润色|修复)", text, re.I):
            errors.append(f"{relative(path)}: reviewer does not explicitly prohibit source edits")
        missing_fields = sorted(field for field in REVIEW_FIELDS if field not in text)
        if missing_fields:
            errors.append(f"{relative(path)}: reviewer report contract missing fields {missing_fields}")
        openai_text = read(path.parent / "agents" / "openai.yaml")
        if "allow_implicit_invocation: false" not in openai_text:
            errors.append(f"{relative(path)}: reviewer must disable implicit invocation")

    for residue_name, pattern in FORBIDDEN_RESIDUES.items():
        for path in sorted(PLUGIN.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".py"}:
                continue
            if pattern.search(read(path)):
                errors.append(f"{relative(path)}: forbidden platform residue `{residue_name}`")

    for skill_md in skill_files:
        lines = len(read(skill_md).splitlines())
        if lines > 500:
            errors.append(f"{relative(skill_md)}: SKILL.md exceeds 500 lines ({lines})")
        elif lines > 300:
            warnings.append(f"{relative(skill_md)}: consider progressive disclosure ({lines} lines)")

    lineage_contracts = [
        SKILLS / "research-idea-orchestrator" / "references" / "artifact-contracts.md",
        SKILLS / "proposal-orchestrator" / "references" / "artifact-naming-and-directory-rules.md",
        SKILLS / "article-orchestrator" / "references" / "artifact-contracts.md",
        SKILLS / "perspective-orchestrator" / "references" / "artifact-naming-and-directory-rules.md",
    ]
    for contract in lineage_contracts:
        contract_text = read(contract)
        if "plugin_version" not in contract_text or "source_skill" not in contract_text:
            errors.append(f"{relative(contract)}: lineage must include plugin_version and source_skill")

    article_evaluator = read(SKILLS / "article-evaluator" / "SKILL.md")
    article_evaluator_fm, _ = split_frontmatter(article_evaluator)
    if "stop_no_gain" in article_evaluator_fm:
        errors.append("article-evaluator: stop_no_gain belongs to the orchestrator, not evaluator metadata")
    for forbidden_input in ("- claim_audit_report", "- methods_audit_report"):
        if forbidden_input in article_evaluator:
            errors.append(f"article-evaluator: must not consume another reviewer report ({forbidden_input[2:]})")
    if "may_call: []" not in article_evaluator:
        errors.append("article-evaluator: reviewer sub-delegation must be empty")
    article_panel = read(SKILLS / "article-review-panel" / "SKILL.md")
    if '"04_blueprint/**"' not in article_panel:
        errors.append("article-review-panel: Submission-Guard cannot read its journal adapter")
    article_briefs = read(
        SKILLS / "article-orchestrator" / "references" / "delegate-brief-templates.md"
    )
    if "04_blueprint/journal-adapter.md (submission_guard only)" not in article_briefs:
        errors.append("article panel brief: Submission-Guard journal adapter is not routed")
    article_contracts = read(
        SKILLS / "article-orchestrator" / "references" / "artifact-contracts.md"
    )
    panel_contract = article_contracts.split("## Panel Report", 1)[1].split("## Cover Letter", 1)[0]
    if 'source_skill: "article-orchestrator"' not in panel_contract or "aggregation_owner" not in panel_contract:
        errors.append("article panel aggregate must be orchestrator-owned")
    if "human_signoff_ref" not in panel_contract:
        errors.append("article panel dissent lacks human-signoff lineage")
    article_compositor = read(SKILLS / "article-submission-compositor" / "SKILL.md")
    if (
        "reviewer_dissent_items" not in article_compositor
        or "fatal_finding_items" not in article_compositor
        or "caps package status at `blocked`" not in article_compositor
    ):
        errors.append("article compositor does not map blocking dissent to human sign-off")
    article_evaluation_gates = read(
        SKILLS / "article-evaluator" / "references" / "evaluation-gates.md"
    )
    article_state = read(
        SKILLS / "article-orchestrator" / "references" / "workflow-state-schema.md"
    )
    if "Inline or degraded evaluation may guide revision" in article_evaluation_gates:
        errors.append("article evaluator retains an inline/degraded fallback")
    if "evaluated inline" in article_state:
        errors.append("article workflow state retains an inline reviewer state")

    proposal_aggregation = read(
        SKILLS / "proposal-review-panel" / "references" / "policy-panel-aggregation-format.md"
    )
    proposal_assembler = read(SKILLS / "proposal-package-assembler" / "SKILL.md")
    if "supportive_recommendation_allowed: false" not in proposal_aggregation:
        errors.append("proposal panel: fatal findings do not disable supportive recommendations")
    if "caps package status at `blocked`" not in proposal_assembler:
        errors.append("proposal assembler: unresolved fatal findings do not cap status at blocked")
    idea_assembler = read(SKILLS / "idea-portfolio-assembler" / "SKILL.md")
    idea_inputs = read(
        SKILLS / "idea-portfolio-assembler" / "references" / "portfolio-input-schema.md"
    )
    if "adversarial panel unresolved blocking finding" not in idea_assembler:
        errors.append("idea assembler: adversarial blocking findings do not cap handoff")
    if "adversarial_panel_reports" not in idea_inputs:
        errors.append("idea assembler: adversarial panel reports are not required inputs")

    perspective_io = read(SKILLS / "perspective-orchestrator" / "references" / "io-contracts.md")
    perspective_naming = read(
        SKILLS / "perspective-orchestrator" / "references" / "artifact-naming-and-directory-rules.md"
    )
    if "06_revisions/06_revisions/" in perspective_io:
        errors.append("perspective: duplicated revision directory in I/O contract")
    if "05_evaluations/evaluation-report-v001.md" not in perspective_naming:
        errors.append("perspective: evaluation naming contract is inconsistent")
    if "07_panel/perspective-vNNN-standard-panel-summary.md" not in perspective_io:
        errors.append("perspective: panel-summary naming contract is inconsistent")
    perspective_layout = perspective_naming
    perspective_drafter = read(SKILLS / "perspective-drafter" / "SKILL.md")
    perspective_refiner = read(SKILLS / "perspective-refinement-controller" / "SKILL.md")
    perspective_orchestrator = read(SKILLS / "perspective-orchestrator" / "SKILL.md")
    if "01_claims/      # claim ledger, claim-evidence matrix" not in perspective_layout:
        errors.append("perspective: claim-evidence matrix directory is inconsistent")
    if "03_skeletons/   # argument skeleton and paragraph maps" in perspective_layout:
        errors.append("perspective: paragraph maps are assigned to two directories")
    if "draft-v{" in perspective_drafter + perspective_refiner + perspective_orchestrator:
        errors.append("perspective: draft naming must use perspective-vNNN")
    if "09_state/workflow-manifest.yaml" not in perspective_orchestrator:
        errors.append("perspective: workflow manifest path is not canonical")
    deep_research_rules = read(
        SKILLS / "research-opportunity-mapper" / "references" / "deep-research-prompt-rules.md"
    )
    deep_research_template = read(
        SKILLS / "research-opportunity-mapper" / "templates" / "deep-research-prompt-template.md"
    )
    if "Single-stage targeted retrieval" in deep_research_rules or "All six sections present" in deep_research_rules:
        errors.append("Deep Research Focused mode conflicts with the global phased contract")
    if "[F] 单阶段 targeted retrieval" in deep_research_template or "[F] 跳过此阶段" in deep_research_template:
        errors.append("Deep Research Focused template skips required phases")
    perspective_architect = read(SKILLS / "perspective-argument-architect" / "SKILL.md")
    perspective_refiner = read(SKILLS / "perspective-refinement-controller" / "SKILL.md")
    if "claim-change-requests/" in perspective_architect + perspective_refiner:
        errors.append("perspective: claim change requests escape 01_claims/change-requests/")
    if "panel-02_evidence/" in perspective_orchestrator:
        errors.append("perspective: malformed panel evidence delegate path")

    plugin_readme = read(PLUGIN / "README.md")
    if "\\`" in plugin_readme:
        errors.append("plugin README contains escaped Markdown code delimiters")

    print("OpenAI research plugin audit")
    print(f"skills: {len(skill_files)}")
    print(f"registry entries: {len(entries)}")
    print(f"independent reviewers: {len(reviewers)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"warnings: {len(warnings)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
