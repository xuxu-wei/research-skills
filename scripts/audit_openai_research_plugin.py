#!/usr/bin/env python3
"""Audit the ChatGPT/Codex research preview plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

from openai_ui_utils import short_description_error


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"
REGISTRY = PLUGIN / "workflow-registry.yaml"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE = REPO / ".agents" / "plugins" / "marketplace.json"

EXPECTED_REVIEWERS = 22
RESEARCH_POLISHER_ENTRY = "research-polisher-orchestrator"
EXPECTED_PUBLIC_ENTRY_SKILLS = {
    "focused-literature-synthesizer",
    "article-orchestrator",
    "perspective-orchestrator",
    "proposal-orchestrator",
    "research-idea-orchestrator",
    "research-landscape-mapper",
    RESEARCH_POLISHER_ENTRY,
}
EXPECTED_PUBLIC_ENTRIES = len(EXPECTED_PUBLIC_ENTRY_SKILLS)
EXPECTED_IMPLICIT_ACTIVE_ENTRIES = EXPECTED_PUBLIC_ENTRY_SKILLS - {
    RESEARCH_POLISHER_ENTRY
}
EXPECTED_POLISHER_ROUTE = {
    "status": "explicit_only_personal_routing_policy",
    "change_authority": "owner_only",
}
SKILL_LINE_HARD_LIMIT = 250
SKILL_CHAR_HARD_LIMIT = 12_000
SKILL_LINE_TARGET = 180
SKILL_CHAR_TARGET = 8_000
DESCRIPTION_BUDGET = 6_200
INITIAL_LOAD_BUDGET = 13_400
EXPECTED_WORKFLOWS = {
    "idea",
    "proposal",
    "article",
    "perspective",
    "research_polisher",
}
OPENAI_NATIVE_SKILL_PACKAGES = {
    "focused-literature-synthesizer": "research",
    "idea-narrative-assessor": "research-idea",
    "research-landscape-mapper": "research",
    "research-narrative-assessor": "research",
    "research-polisher-methodology-publishability-reviewer": "research-polisher",
    "research-polisher-orchestrator": "research-polisher",
    "research-polisher-plan-assembler": "research-polisher",
    "research-polisher-strategy-reviewer": "research-polisher",
}
DELETED_PERSONAL_PROFILE_ASSETS = {
    "PHASE7-8-RUNBOOK.md",
    "PREVIEW-EVIDENCE-CAPTURE.md",
    "PROVENANCE.yaml",
    "release-ledger.json",
}
DELETED_ASSET_REFERENCE_ALLOWLIST = {
    "scripts/test_openai_release_contract.py": {
        "PHASE7-8-RUNBOOK.md",
        "PREVIEW-EVIDENCE-CAPTURE.md",
        "PROVENANCE.yaml",
    },
}

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

PRE_SUBMISSION_POLICY_SCAN_SKILLS = {
    "academic-language-assessor",
    "research-narrative-assessor",
    "article-claim-auditor",
    "article-context-builder",
    "article-drafter",
    "article-evaluator",
    "article-frontmatter-drafter",
    "article-methods-statistics-auditor",
    "article-readiness-triage",
    "article-review-panel",
    "idea-adversarial-review-panel",
    "idea-evaluator",
    "medical-journal-review",
    "methodology-statistics-preflight",
    "multi-path-idea-generator",
    "perspective-evaluator",
    "perspective-review-panel",
    "proposal-context-brief-builder",
    "proposal-drafter",
    "proposal-evaluator",
    "proposal-readiness-triage",
    "proposal-review-panel",
    "research-context-builder",
    "research-idea-orchestrator",
    "research-polisher-methodology-publishability-reviewer",
    "research-polisher-strategy-reviewer",
    "sap-evaluator",
    "sap-writer",
}
PRE_SUBMISSION_POLICY_RE = re.compile(
    r"\b(?:ethics?|ethical|IRB|privacy|regulatory|informed consent)\b|伦理|隐私|监管|知情同意",
    re.I,
)


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


def resolve_resource_path(source: Path, reference: str) -> Path | None:
    clean = unquote(reference.split("#", 1)[0].split("?", 1)[0]).replace("\\", "/")
    if not clean or clean.startswith(("http://", "https://", "mailto:", "codex://", "app://", "#")):
        return None
    first = clean.split("/", 1)[0]
    if first in {"references", "templates", "scripts", "agents"}:
        for parent in (source.parent, *source.parents):
            if parent.parent == SKILLS:
                return parent / clean
    if (SKILLS / first / "SKILL.md").exists():
        return SKILLS / clean
    return source.parent / clean


def recursive_reference_errors() -> list[str]:
    errors: list[str] = []
    markdown_files = sorted(PLUGIN.rglob("*.md"))
    for source in markdown_files:
        text = read(source)
        visible_text = re.sub(r"```.*?```", "", text, flags=re.S)
        candidates = set(re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", visible_text))
        if any(parent.parent == SKILLS for parent in (source.parent, *source.parents)):
            candidates.update(
                re.findall(
                    r"`((?:[A-Za-z0-9_-]+/)?(?:references|templates|scripts|agents)/[^`]+\.(?:md|py|yaml|yml|json))`",
                    visible_text,
                )
            )
        for raw in sorted(candidates):
            reference = raw.strip().strip("<>").split(maxsplit=1)[0]
            target = resolve_resource_path(source, reference)
            if target is not None and not target.exists():
                errors.append(f"{relative(source)}: missing referenced file `{reference}`")
    return errors


def resource_ownership_errors(skill_md: Path) -> list[str]:
    text = read(skill_md)
    errors: list[str] = []
    resources = [
        path
        for path in skill_md.parent.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix.lower() != ".pyc"
        and any(part in {"references", "templates", "scripts"} for part in path.parts)
    ]
    for resource in sorted(resources):
        resource_path = resource.relative_to(skill_md.parent).as_posix()
        token = f"`{resource_path}`"
        path_mentions = [line for line in text.splitlines() if resource_path in line]
        if not path_mentions:
            errors.append(f"{relative(resource)}: orphaned resource; name it directly from SKILL.md")
            continue
        if not any(re.search(r"\b(?:read|load|use|run|open|when|before|after|only if)\b", line, re.I) for line in path_mentions):
            errors.append(f"{relative(skill_md)}: resource `{resource_path}` lacks an explicit load/run condition")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    manifest_version = ""
    agent_implicit_policies: dict[str, bool] = {}

    if not MANIFEST.exists():
        errors.append("missing plugin manifest")
    else:
        manifest = json.loads(read(MANIFEST))
        if manifest.get("name") != "research-skills-openai":
            errors.append("plugin manifest name must be research-skills-openai")
        manifest_version = str(manifest.get("version", ""))
        if not re.fullmatch(
            r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
            r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
            r"(?:\+codex\.[A-Za-z0-9._-]+)?",
            manifest_version,
        ):
            errors.append("plugin manifest version must be valid SemVer with an optional Codex cachebuster")
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
    description_chars = 0
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
        description_match = re.search(r'^description:\s*"(.*)"\s*$', frontmatter, re.M)
        if description_match:
            description_chars += len(description_match.group(1))
        openai_yaml = skill_md.parent / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            errors.append(f"{relative(skill_md)}: missing agents/openai.yaml")
        else:
            try:
                openai_data = yaml.safe_load(read(openai_yaml)) or {}
            except yaml.YAMLError as exc:
                errors.append(f"{relative(openai_yaml)}: invalid YAML: {exc}")
                openai_data = {}
            interface = openai_data.get("interface", {}) if isinstance(openai_data, dict) else {}
            short_error = short_description_error(interface.get("short_description"))
            if short_error:
                errors.append(f"{relative(openai_yaml)}: {short_error}")
            policy = openai_data.get("policy", {}) if isinstance(openai_data, dict) else {}
            allow_implicit = (
                policy.get("allow_implicit_invocation")
                if isinstance(policy, dict)
                else None
            )
            if not isinstance(allow_implicit, bool):
                errors.append(
                    f"{relative(openai_yaml)}: policy.allow_implicit_invocation must be boolean"
                )
            else:
                agent_implicit_policies[name] = allow_implicit
        errors.extend(resource_ownership_errors(skill_md))
        if name not in FINAL_SUBMISSION_SKILLS and PRE_SUBMISSION_POLICY_RE.search(body):
            errors.append(f"{relative(skill_md)}: pre-submission ethics/privacy/regulatory gate residue")
        if name in PRE_SUBMISSION_POLICY_SCAN_SKILLS:
            for resource_path in sorted(skill_md.parent.rglob("*")):
                if (
                    not resource_path.is_file()
                    or resource_path == skill_md
                    or resource_path.suffix.lower()
                    not in {".md", ".yaml", ".yml", ".json", ".txt"}
                ):
                    continue
                if PRE_SUBMISSION_POLICY_RE.search(read(resource_path)):
                    errors.append(
                        f"{relative(resource_path)}: pre-submission ethics/privacy/regulatory gate residue"
                    )

    if not REGISTRY.exists():
        errors.append("missing workflow-registry.yaml")
        entries = []
    else:
        registry_text = read(REGISTRY)
        if f'plugin_version: "{manifest_version}"' not in registry_text:
            errors.append("registry plugin version does not match manifest")
        registry_data = yaml.safe_load(registry_text) or {}
        entries = registry_data.get("skills", [])
        edges = registry_data.get("workflow_edges", [])
        if registry_data.get("schema_version") != 6:
            errors.append("registry schema_version must be 6 for workflow, scenario-eval, package, revision, context-profile, and cross-workflow editorial-readiness auditability")
        state_policy = registry_data.get("workflow_state_policy", {})
        state_machines = registry_data.get("workflow_state_machines", {})
        scenario_contract = registry_data.get("scenario_eval_contract", {})
        context_policy = registry_data.get("context_profile_policy", {})
        review_execution = registry_data.get("review_execution", {})
        artifact_policy = registry_data.get("artifact_completeness_policy", {})
        editorial_readiness_policy = registry_data.get("cross_workflow_editorial_readiness_policy", {})
        docx_policy = registry_data.get("article_docx_delivery_policy", {})
    if not REGISTRY.exists():
        edges = []
        state_policy = {}
        state_machines = {}
        scenario_contract = {}
        context_policy = {}
        review_execution = {}
        artifact_policy = {}
        editorial_readiness_policy = {}
        docx_policy = {}

    if review_execution.get("prior_versions_visible_to_reviewer") is not False:
        errors.append("registry fresh reviewers must not see prior artifact versions")
    if review_execution.get("revision_deltas_visible_to_reviewer") is not False:
        errors.append("registry fresh reviewers must not see revision deltas")
    if artifact_policy.get("idea_schema") != "research-idea.v3":
        errors.append("registry must use research-idea.v3 complete dossiers")
    if artifact_policy.get("idea_current_artifact") != "complete_markdown_dossier":
        errors.append("registry must make the complete Markdown dossier authoritative for Idea content")
    if artifact_policy.get("idea_legacy_schemas") != ["research-idea.v1", "research-idea.v2"]:
        errors.append("registry must recognize v1/v2 Idea layouts as legacy")
    if artifact_policy.get("idea_legacy_layout_behavior") != "layout_migration_required_read_only_no_automatic_rewrite":
        errors.append("registry must keep legacy Idea layouts read-only without automatic migration")
    idea_chain = artifact_policy.get("idea_evidence_chain_contract", {})
    if idea_chain.get("required_fields") != [
        "input",
        "method_analysis_or_processing",
        "output",
        "supported_objective_or_claim",
    ]:
        errors.append("registry Idea evidence chains must use the complete four-field semi-structured contract")
    editorial = artifact_policy.get("idea_editorial_repositioning_contract", {})
    if not (
        editorial.get("title_audience_and_positioning_changes_allowed") is True
        and editorial.get("added_work_required_for_supported_repositioning") is False
        and editorial.get("all_title_and_positioning_claims_must_be_supported_by_implementation") is True
        and editorial.get("editorial_change_requires_fresh_evaluation") is True
        and editorial.get("claim_support_states") == ["supported", "qualified", "unsupported"]
        and editorial.get("similar_work_does_not_automatically_require_new_work") is True
        and editorial.get("novel_method_data_or_discovery_claim_requires_real_increment") is True
    ):
        errors.append("registry Idea editorial-repositioning and claim-support contract is incomplete")
    marker_policy = artifact_policy.get("idea_internal_marker_policy", {})
    if not (
        marker_policy.get("opaque_workflow_markers_forbidden_in_dossier_prose") is True
        and marker_policy.get("standard_academic_citations_allowed") is True
        and marker_policy.get("user_visible_internal_markers_require_human_label_and_ledger_resolution") is True
    ):
        errors.append("registry Idea internal-marker policy is incomplete")
    dossier_only = artifact_policy.get("idea_evaluator_project_input_contract", {})
    expected_idea_forbidden = {
        "research_context",
        "evidence_map",
        "opportunity_map",
        "preflight_report",
        "reference_ledger",
        "prior_dossier",
        "revision_delta",
        "anonymous_must_fix_list",
        "prior_report",
        "prior_score",
        "prior_decision",
    }
    if not (
        dossier_only.get("allowed_project_artifacts") == ["current_complete_idea_dossier"]
        and dossier_only.get("exact_project_artifact_count") == 1
        and set(dossier_only.get("forbidden_project_artifacts", [])) == expected_idea_forbidden
        and dossier_only.get("logical_binding_fields") == ["artifact_id", "version", "path"]
        and dossier_only.get("content_digest_required") is False
        and dossier_only.get("readiness_reports_visible") is False
    ):
        errors.append("registry Idea evaluator must receive exactly the current complete dossier")
    readiness = artifact_policy.get("idea_editorial_readiness_contract", {})
    if not (
        readiness.get("runs_after_scientific_revision_before_evaluation") is True
        and readiness.get("parallel_reviewers")
        == ["research-narrative-assessor", "academic-language-assessor"]
        and readiness.get("editorially_eligible_narrative_decisions")
        == ["narrative_ready", "minor_narrative_revision"]
        and readiness.get("editorially_eligible_language_decisions")
        == ["submission_ready", "minor_language_revision"]
        and readiness.get("eligibility_requires_no_unresolved_major_narrative_finding") is True
        and readiness.get("eligibility_requires_no_unresolved_critical_or_major_language_finding") is True
        and readiness.get("idea_scope_overrides_global_language_minor_revision_action") is True
        and readiness.get("ordinary_repair_decisions")
        == ["major_narrative_revision", "major_language_revision"]
        and readiness.get("clarification_required_route")
        == "clarification_stop_then_fresh_assessment"
        and readiness.get("needs_professional_editing_route")
        == "editorial_revision_required_external_language_support_then_fresh_assessment"
        and readiness.get("repair_plan_format") == "yaml"
        and readiness.get("repair_requires_protected_content_register") is True
        and readiness.get("repair_requires_fresh_content_preservation_review") is True
        and readiness.get("repair_requires_fresh_narrative_and_language_reassessment") is True
        and readiness.get("evaluator_reads_editorial_artifacts") is False
    ):
        errors.append("registry Idea editorial-readiness contract is incomplete")
    idea_machine = state_machines.get("idea", {})
    if idea_machine.get("primary_artifact_type") != "idea_dossier":
        errors.append("registry Idea primary artifact must be idea_dossier")
    idea_profiles = idea_machine.get("internal_direction_profiles", {})
    focused = idea_profiles.get("focused_optimization", {})
    bounded = idea_profiles.get("bounded_exploration", {})
    if focused.get("current_dossier_count") != 1 or focused.get("final_state") != "human_signoff_required":
        errors.append("registry focused Idea profile must maintain one dossier through human sign-off")
    if not (
        bounded.get("current_dossier_count") == {"minimum": 2, "maximum": 3}
        and bounded.get("optimization_round_limit_per_direction") == 1
        and bounded.get("evidence_and_opportunity_remap_after_optimization") is True
        and bounded.get("fresh_evaluator_per_current_dossier_after_remap") is True
        and bounded.get("structural_change_after_remap") == "revision_required_no_automatic_second_optimization"
        and bounded.get("final_state") == "human_direction_selection_required"
    ):
        errors.append("registry bounded Idea profile must remap, fresh-evaluate, and stop for human selection")
    if artifact_policy.get("article_schema") != "research-article.v7":
        errors.append("registry must use research-article.v7 canonical Markdown")
    if artifact_policy.get("core_identity_drift_behavior") != "new_idea_required_no_automatic_branch":
        errors.append("registry Idea identity drift must stop without automatic branching")
    if docx_policy.get("content_authority") != "canonical_markdown":
        errors.append("registry Article content authority must remain canonical Markdown")
    if docx_policy.get("primary_user_delivery_when_capable") != "docx":
        errors.append("registry Article preferred capable delivery must be DOCX")
    if set(docx_policy.get("fallback_states", [])) != {"docx_generation_pending", "docx_visual_qa_pending"}:
        errors.append("registry Article DOCX fallback states are incomplete")
    if not (
        editorial_readiness_policy.get("workflows") == ["idea", "proposal", "perspective", "article"]
        and editorial_readiness_policy.get("macro_reviewer") == "research-narrative-assessor"
        and editorial_readiness_policy.get("meso_micro_reviewer") == "academic-language-assessor"
        and editorial_readiness_policy.get("reviewers_run_in_parallel_on_same_frozen_reader_artifact_or_bundle") is True
    ):
        errors.append("registry cross-workflow narrative/language role boundary is incomplete")
    repair_interface = editorial_readiness_policy.get("repair_interface", {})
    if not (
        repair_interface.get("raw_assessment_reports_visible_to_writer") is False
        and repair_interface.get("single_writer_brief_format") == "yaml"
        and repair_interface.get("writer_uses_same_owner_for_bounded_section_passes") is True
        and repair_interface.get("multiple_fragment_writers_forbidden") is True
        and repair_interface.get("action_conformance_receipt_required") is True
    ):
        errors.append("registry shared editorial writer interface is incomplete")
    limitation_policy = editorial_readiness_policy.get("limitation_policy", {})
    if not (
        limitation_policy.get("one_complete_authoritative_location_per_document_or_distinct_argument_family") is True
        and limitation_policy.get("omit_elsewhere") is True
        and limitation_policy.get("cross_reference_or_pointer_elsewhere_forbidden") is True
        and limitation_policy.get("narrative_continuity_has_priority_over_defensive_repetition") is True
    ):
        errors.append("registry shared limitation-authority policy is incomplete")
    logical_integrity = editorial_readiness_policy.get("logical_integrity", {})
    if not (
        logical_integrity.get("sha_or_content_digest_forbidden_in_new_llm_facing_artifacts") is True
        and logical_integrity.get("legacy_digest_fields") == "readable_but_ignored"
        and set(logical_integrity.get("required", []))
        == {"artifact_id", "version", "exact_path", "frozen_state", "complete_artifact_index", "unique_current_pointer"}
    ):
        errors.append("registry logical lineage must avoid new LLM-facing hashes while retaining index integrity")
    final_isolation = editorial_readiness_policy.get("final_evaluator_isolation", {})
    if not (
        final_isolation.get("exact_files_read_must_be_reported") is True
        and final_isolation.get("sha_or_content_digest_required") is False
        and final_isolation.get("binding_fields") == ["artifact_id", "version", "exact_path"]
        and "narrative_or_language_report" in final_isolation.get("forbidden", [])
        and "repair_plan_or_writer_brief" in final_isolation.get("forbidden", [])
    ):
        errors.append("registry final evaluator isolation contract is incomplete")
    article_entry = artifact_policy.get("article_entry_material_contract", {})
    if not (
        article_entry.get("complete_inventory_required") is True
        and article_entry.get("semantic_authority_must_be_explicit") is True
        and article_entry.get("compatible_supporting_assets_retained") is True
        and article_entry.get("filename_or_version_whitelist_must_not_hide_supplied_material") is True
    ):
        errors.append("registry Article entry must inventory all supplied materials before readiness")

    registry_names = {entry.get("name", "") for entry in entries}
    if registry_names != set(names):
        errors.append(
            f"registry/skill name mismatch: missing={sorted(set(names)-registry_names)} extra={sorted(registry_names-set(names))}"
        )
    entries_by_name = {entry.get("name", ""): entry for entry in entries}
    for native_name, expected_package in OPENAI_NATIVE_SKILL_PACKAGES.items():
        entry = entries_by_name.get(native_name)
        if entry is None:
            errors.append(f"OpenAI-native skill missing from registry: {native_name}")
        elif entry.get("package") != expected_package:
            errors.append(
                f"OpenAI-native skill {native_name} package differs: "
                f"expected {expected_package}, found {entry.get('package')}"
            )
    plugin_license = PLUGIN / "LICENSE"
    root_license = REPO / "LICENSE"
    if not plugin_license.exists() or not root_license.exists():
        errors.append("plugin and repository LICENSE files must both exist")
    elif plugin_license.read_bytes().replace(b"\r\n", b"\n") != root_license.read_bytes().replace(b"\r\n", b"\n"):
        errors.append("plugin LICENSE differs from the repository MIT license")
    for entry in entries:
        name = entry.get("name", "")
        package = entry.get("package", "")
        if name in OPENAI_NATIVE_SKILL_PACKAGES:
            continue
        source_dir = REPO / "research-skills" / str(package) / str(name)
        if not source_dir.is_dir():
            errors.append(f"{name}: Hermes source directory is missing for package `{package}`")
    if "pubmed" in names or (SKILLS / "pubmed").exists():
        errors.append("standalone OpenAI pubmed skill must remain removed")
    reviewers = [entry for entry in entries if entry.get("requires_independent_subagent") is True]
    if len(reviewers) != EXPECTED_REVIEWERS:
        errors.append(f"expected {EXPECTED_REVIEWERS} independent reviewers, found {len(reviewers)}")
    for entry in entries:
        name = entry.get("name", "")
        for related in entry.get("related_skills", []):
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
        if agent_implicit_policies.get(name) is not False:
            errors.append(f"{relative(path)}: reviewer must disable implicit invocation")

    implicit = [entry for entry in entries if entry.get("invocation_policy") == "implicit"]
    public_entry_policy = registry_data.get("public_entry_policy", {}) if REGISTRY.exists() else {}
    declared_entry_list = public_entry_policy.get("declared_entries", [])
    implicit_active_list = public_entry_policy.get("implicit_active_entries", [])
    declared_entries = set(declared_entry_list) if isinstance(declared_entry_list, list) else set()
    implicit_active_entries = (
        set(implicit_active_list) if isinstance(implicit_active_list, list) else set()
    )
    if (
        not isinstance(declared_entry_list, list)
        or len(declared_entry_list) != EXPECTED_PUBLIC_ENTRIES
        or declared_entries != EXPECTED_PUBLIC_ENTRY_SKILLS
    ):
        errors.append(
            "declared public entries differ from the personal routing profile: "
            f"expected={sorted(EXPECTED_PUBLIC_ENTRY_SKILLS)}, "
            f"actual={sorted(declared_entries)}"
        )
    registry_implicit_entries = {entry.get("name") for entry in implicit}
    source_implicit_entries = {
        name for name, allowed in agent_implicit_policies.items() if allowed
    }
    non_public_implicit = source_implicit_entries - declared_entries
    if non_public_implicit:
        errors.append(
            "non-public skills allow implicit invocation: "
            f"{sorted(non_public_implicit)}"
        )
    if implicit_active_entries != registry_implicit_entries:
        errors.append("public entry policy and skill invocation policies disagree")
    if source_implicit_entries != implicit_active_entries:
        errors.append(
            "agents/openai.yaml and registry implicit policies disagree: "
            f"source_only={sorted(source_implicit_entries - implicit_active_entries)} "
            f"registry_only={sorted(implicit_active_entries - source_implicit_entries)}"
        )
    polisher_route = public_entry_policy.get("explicit_only_entries", {}).get(
        RESEARCH_POLISHER_ENTRY, {}
    )
    polisher_policy = agent_implicit_policies.get(RESEARCH_POLISHER_ENTRY)
    if source_implicit_entries != EXPECTED_IMPLICIT_ACTIVE_ENTRIES:
        errors.append(
            "personal routing requires exactly six implicit entries and keeps "
            f"Research Polisher explicit-only: actual={sorted(source_implicit_entries)}"
        )
    if polisher_policy is not False:
        errors.append("Research Polisher must disable implicit invocation")
    if polisher_route != EXPECTED_POLISHER_ROUTE:
        errors.append(
            "Research Polisher registry route must be the explicit-only personal policy"
        )

    edge_fields = {
        "workflow",
        "source",
        "destination",
        "dispatch_mode",
        "trigger",
        "input_contract",
        "output_contract",
        "failure_route",
    }
    edge_pairs: set[tuple[str, str, str, str]] = set()
    reviewer_names = {entry["name"] for entry in reviewers}
    for index, edge in enumerate(edges, start=1):
        missing = sorted(edge_fields - set(edge))
        if missing:
            errors.append(f"registry edge {index}: missing fields {missing}")
            continue
        source = edge["source"]
        destination = edge["destination"]
        key = (edge["workflow"], source, destination, edge["trigger"])
        if key in edge_pairs:
            errors.append(f"registry edge duplicated: {key}")
        edge_pairs.add(key)
        if source not in registry_names or destination not in registry_names:
            errors.append(f"registry edge references unknown skill: {source} -> {destination}")
        if destination in reviewer_names:
            if edge["dispatch_mode"] != "delegated":
                errors.append(f"reviewer edge must be delegated: {source} -> {destination}")
            if edge["failure_route"] != "independent_review_pending":
                errors.append(f"reviewer edge must stop at independent_review_pending: {source} -> {destination}")

    orchestrators = [name for name in registry_names if name.endswith("orchestrator")]
    edge_lookup = {(edge.get("source"), edge.get("destination")): edge for edge in edges}
    for orchestrator in orchestrators:
        body = read(names[orchestrator])
        initial_load = description_chars + len(body)
        if initial_load > INITIAL_LOAD_BUDGET:
            errors.append(
                f"{orchestrator}: conservative all-skill description plus orchestrator proxy "
                f"exceeds {INITIAL_LOAD_BUDGET} characters ({initial_load})"
            )
        if "phase summary" not in body.lower() or "artifact" not in body.lower():
            errors.append(f"{orchestrator}: missing concise phase-summary/artifact-pointer return contract")
        for reviewer in sorted(reviewer_names):
            if f"`{reviewer}`" not in body:
                continue
            edge = edge_lookup.get((orchestrator, reviewer))
            if not edge:
                errors.append(f"missing orchestrator-to-reviewer edge: {orchestrator} -> {reviewer}")
            elif edge.get("dispatch_mode") != "delegated":
                errors.append(f"orchestrator reviewer edge is not delegated: {orchestrator} -> {reviewer}")

    canonical_states = {
        "pending_review",
        "independent_review_pending",
        "blocked",
        "stopped",
        "human_signoff_required",
    }
    policy_states = set(state_policy.get("active_states", [])) | set(state_policy.get("pause_states", [])) | set(
        state_policy.get("terminal_states", [])
    )
    active_states = set(state_policy.get("active_states", []))
    pause_states = set(state_policy.get("pause_states", []))
    terminal_states = set(state_policy.get("terminal_states", []))
    if active_states & pause_states or active_states & terminal_states or pause_states & terminal_states:
        errors.append("registry workflow state classes must be pairwise disjoint")
    if not canonical_states <= policy_states:
        errors.append(f"registry canonical states missing: {sorted(canonical_states - policy_states)}")
    if state_policy.get("review_unavailable_state") != "independent_review_pending":
        errors.append("registry reviewer-unavailability route must be independent_review_pending")
    if state_policy.get("fatal_finding_state") != "blocked":
        errors.append("registry fatal finding route must be blocked")
    if state_policy.get("final_handoff_state") != "human_signoff_required":
        errors.append("registry final handoff must be human_signoff_required")
    if "human_strategy_selection_required" not in terminal_states:
        errors.append("registry lacks the Research Polisher human-selection terminal state")
    for state in (
        "specialist_review_pending",
        "clarification_stop",
        "deep_research_handoff_required",
        "no_defensible_option",
        "additional_work_required",
    ):
        if state not in policy_states:
            errors.append(f"registry lacks Research Polisher state `{state}`")
    if state_policy.get("wildcard_transition_scope") != "nonterminal_states_only":
        errors.append("registry wildcard transitions must exclude terminal states")
    if state_policy.get("resume_policy", {}).get("independent_review_pending") != "pending_review":
        errors.append("registry independent-review pause lacks a resume policy")
    lifecycle_triples = {
        (item.get("from"), item.get("to"), item.get("trigger"))
        for item in state_policy.get("lifecycle_transitions", [])
        if isinstance(item, dict)
    }
    for transition in (
        (
            "pending_review",
            "specialist_review_pending",
            "specialist_review_requested",
        ),
        (
            "specialist_review_pending",
            "pending_review",
            "sanitized_specialist_findings_ready",
        ),
        (
            "human_strategy_selection_required",
            "additional_work_required",
            "human_selected_extension_option",
        ),
    ):
        if transition not in lifecycle_triples:
            errors.append(f"registry Research Polisher transition missing: {transition}")
    version_gate = state_policy.get("version_gate", {})
    for field in (
        "changed_artifact_requires_new_version",
        "evaluator_instance_must_be_fresh",
        "evaluated_version_must_equal_current_version",
    ):
        if version_gate.get(field) is not True:
            errors.append(f"registry version gate disabled: {field}")
    concurrency = state_policy.get("concurrency_policy", {})
    if concurrency.get("phase_level_delegation_allowed") is not True:
        errors.append("registry must permit phase-level delegation")
    if concurrency.get("single_writer_per_source_artifact") is not True:
        errors.append("registry must enforce one writer per source artifact")
    if concurrency.get("concurrent_writes_to_same_source_artifact") is not False:
        errors.append("registry must forbid concurrent writes to the same source artifact")
    if set(state_machines) != EXPECTED_WORKFLOWS:
        errors.append(
            "registry workflow state machines differ from the five-workflow contract: "
            f"missing={sorted(EXPECTED_WORKFLOWS - set(state_machines))} "
            f"extra={sorted(set(state_machines) - EXPECTED_WORKFLOWS)}"
        )
    for workflow, machine in state_machines.items():
        if machine.get("post_evaluation_panel_required") is False:
            if machine.get("workflow_profile") != "reviewer_matrix_assemble_evaluate":
                errors.append(f"{workflow} state machine: panel-free profile is not declared")
            for gate in (
                "three_strategy_roles_complete",
                "nine_matrix_cells_accounted",
                "dissent_and_conflicts_indexed",
            ):
                if gate not in machine.get("before_strategy_assembly", []):
                    errors.append(f"{workflow} state machine: strategy assembly gate missing {gate}")
            if "candidate_portfolio_versioned" not in machine.get("before_evaluation", []):
                errors.append(f"{workflow} state machine: evaluation lacks a versioned portfolio gate")
        elif workflow == "perspective":
            if "current_perspective_scientific_evaluation_complete" not in machine.get("before_panel", []):
                errors.append("perspective state machine: panel lacks scientific current-version evaluation gate")
            stage_contract = machine.get("evaluation_stage_contract", {})
            if stage_contract.get("scientific", {}).get("dispatch_before") != "panel":
                errors.append("perspective state machine: scientific evaluation must precede panel")
        elif "latest_version_independently_evaluated" not in machine.get("before_panel", []):
            errors.append(f"{workflow} state machine: panel lacks current-version evaluation gate")
        if workflow == "perspective":
            if "final_perspective_evaluation_complete" not in machine.get("before_packaging", []):
                errors.append("perspective state machine: packaging lacks final current-version evaluation gate")
        elif "latest_version_independently_evaluated" not in machine.get("before_packaging", []):
            errors.append(f"{workflow} state machine: packaging lacks current-version evaluation gate")
        if "dissent_and_fatal_findings_indexed" not in machine.get("before_packaging", []):
            errors.append(f"{workflow} state machine: packaging does not preserve dissent/fatal findings")

    canonical_lineage = {
        "artifact_id",
        "version_id",
        "workflow_id",
        "round_id",
        "plugin_version",
        "source_skill",
        "created_by_instance_id",
        "based_on",
        "change_type",
        "path",
        "status",
        "frozen",
    }
    if set(scenario_contract.get("required_workflows", [])) != EXPECTED_WORKFLOWS:
        errors.append("scenario eval contract must cover exactly five workflows")
    if set(scenario_contract.get("required_lineage_fields", [])) != canonical_lineage:
        errors.append("scenario eval contract canonical lineage fields are incomplete")
    if scenario_contract.get("legacy_optional_lineage_fields") != ["content_digest"]:
        errors.append("scenario eval contract must read but not require the legacy content digest")
    required_dispatch = set(scenario_contract.get("required_dispatch_fields", []))
    for field in ("actor_instance_id", "allowed_read_paths", "allowed_write_paths", "input_artifact_ids", "input_versions"):
        if field not in required_dispatch:
            errors.append(f"scenario eval contract dispatch field missing: {field}")
    required_review = set(scenario_contract.get("required_review_fields", []))
    for field in ("reviewer_instance_id", "reviewer_role", "review_scope", "files_read", "prior_scores_visible", "source_edits_performed"):
        if field not in required_review:
            errors.append(f"scenario eval contract review field missing: {field}")
    write_policy = scenario_contract.get("write_scope_policy", {})
    for field in ("allowed_writes_are_exact_event_paths", "actual_writes_must_be_subset_of_allowed_writes", "input_artifacts_must_remain_hash_identical"):
        if write_policy.get(field) is not True:
            errors.append(f"scenario eval write-scope policy disabled: {field}")
    if scenario_contract.get("automatic_external_submission") is not False:
        errors.append("scenario eval contract must prohibit automatic external submission")
    if (
        state_machines.get("research_polisher", {}).get("final_state")
        != "human_strategy_selection_required"
        or scenario_contract.get("workflow_final_states", {}).get("research_polisher")
        != "human_strategy_selection_required"
    ):
        errors.append("Research Polisher final state must require human strategy selection")
    polisher_group = scenario_contract.get("review_group_contracts", {}).get(
        "research_polisher", {}
    )
    if polisher_group.get("skill") != "research-polisher-strategy-reviewer":
        errors.append("Research Polisher strategy review-group skill is incorrect")
    if polisher_group.get("roles") != [
        "scientific_significance",
        "practical_value",
        "dissemination_editorial",
    ]:
        errors.append("Research Polisher must declare the three strategy reviewer roles")
    if polisher_group.get("effort_tiers") != [
        "reposition_only",
        "small_extension",
        "moderate_extension",
    ]:
        errors.append("Research Polisher must declare the three effort tiers")
    for field, expected in (
        ("required_instance_count", 3),
        ("required_matrix_cell_count", 9),
        ("instances_must_be_distinct", True),
        ("peer_outputs_visible", False),
        ("raw_reports_visible_to_final_evaluator", False),
    ):
        if polisher_group.get(field) != expected:
            errors.append(f"Research Polisher review-group contract is invalid: {field}")
    specialist_return = state_machines.get("research_polisher", {}).get(
        "specialist_review_return_contract", {}
    )
    if specialist_return != {
        "state": "specialist_review_pending",
        "sanitizer_skill": "research-polisher-plan-assembler",
        "sanitized_artifact_type": "research_polisher_specialist_findings_bundle",
        "raw_specialist_reports_visible_to_final_reviewer": False,
        "requires_fresh_final_reviewer": True,
        "counts_as_evaluator_round": True,
    }:
        errors.append("Research Polisher specialist-review return contract is incomplete")
    polisher_decisions = scenario_contract.get("review_decision_contracts", {})
    if polisher_decisions.get("research-polisher-strategy-reviewer", {}) != {
        "allowed": [
            "matrix_complete",
            "matrix_complete_with_no_defensible_option",
            "clarification_required",
            "independent_review_pending",
        ],
        "pass": ["matrix_complete", "matrix_complete_with_no_defensible_option"],
        "revise": ["clarification_required"],
        "stop": ["independent_review_pending"],
    }:
        errors.append("Research Polisher strategy-review decision routing is invalid")
    if polisher_decisions.get(
        "research-polisher-methodology-publishability-reviewer", {}
    ) != {
        "allowed": [
            "ready_for_human_selection",
            "revision_required",
            "specialist_review_required",
            "no_defensible_option",
            "not_assessable",
            "independent_review_pending",
        ],
        "pass": ["ready_for_human_selection"],
        "revise": ["revision_required", "specialist_review_required"],
        "stop": [
            "no_defensible_option",
            "not_assessable",
            "independent_review_pending",
        ],
    }:
        errors.append("Research Polisher final-review decision routing is invalid")
    polisher_package = scenario_contract.get("package_input_contracts", {}).get(
        "research_polisher", {}
    )
    polisher_allowed_roles = set(polisher_package.get("allowed_roles", []))
    if "research_polisher_strategy_report" in polisher_allowed_roles:
        errors.append("Research Polisher final package must not expose raw strategy reports")
    if not {
        "research_polisher_dossier",
        "research_polisher_sealed_provenance",
        "research_polisher_candidate_portfolio",
        "research_polisher_evaluation_report",
        "research_polisher_review_finding_index",
    } <= polisher_allowed_roles:
        errors.append("Research Polisher final package contract lacks required artifact roles")
    polisher_final_entry = next(
        (
            item
            for item in entries
            if item.get("name")
            == "research-polisher-methodology-publishability-reviewer"
        ),
        {},
    )
    final_inputs = str(polisher_final_entry.get("allowed_input_artifacts", ""))
    for marker in (
        "dossier",
        "evidence",
        "candidate_portfolio",
        "verified_target_adapter",
        "sanitized_specialist_findings_bundle",
    ):
        if marker not in final_inputs:
            errors.append(f"Research Polisher final-review registry inputs omit `{marker}`")
    polisher_assembler_entry = next(
        (
            item
            for item in entries
            if item.get("name") == "research-polisher-plan-assembler"
        ),
        {},
    )
    assembler_io = " ".join(
        str(polisher_assembler_entry.get(field, ""))
        for field in ("allowed_input_artifacts", "output_artifact_type")
    )
    for marker in ("sealed_provenance", "revision_brief", "specialist_findings_bundle"):
        if marker not in assembler_io:
            errors.append(f"Research Polisher assembler registry I/O omits `{marker}`")
    for compositor in ("article-submission-compositor", "perspective-final-compositor"):
        entry = next((item for item in entries if item.get("name") == compositor), {})
        if entry.get("output_artifact_type") != "verification_report_and_final_handoff_package":
            errors.append(f"{compositor}: registry output type does not include verification and package artifacts")

    if context_policy.get("measurement_unit") != "characters":
        errors.append("context profile must state its measurement unit")
    if "not_model_token_accounting" not in context_policy.get("interpretation", ""):
        errors.append("context profile must not misrepresent character proxy as token accounting")
    profiles = context_policy.get("profiles", {})
    if set(profiles) != {"standard_32k", "degraded_16k"}:
        errors.append("context profile policy must define standard_32k and degraded_16k")
    elif profiles["standard_32k"].get("total_character_budget") != 32000 or profiles["degraded_16k"].get("total_character_budget") != 16000:
        errors.append("context profile character budgets are incorrect")

    errors.extend(recursive_reference_errors())

    for residue_name, pattern in FORBIDDEN_RESIDUES.items():
        for path in sorted(PLUGIN.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".py"}:
                continue
            if pattern.search(read(path)):
                errors.append(f"{relative(path)}: forbidden platform residue `{residue_name}`")

    if description_chars > DESCRIPTION_BUDGET:
        errors.append(f"skill descriptions exceed {DESCRIPTION_BUDGET} characters ({description_chars})")

    for skill_md in skill_files:
        text = read(skill_md)
        lines = len(text.splitlines())
        chars = len(text)
        if lines > SKILL_LINE_HARD_LIMIT or chars > SKILL_CHAR_HARD_LIMIT:
            errors.append(
                f"{relative(skill_md)}: SKILL.md exceeds hard context budget "
                f"({lines}/{SKILL_LINE_HARD_LIMIT} lines, {chars}/{SKILL_CHAR_HARD_LIMIT} chars)"
            )
        elif lines > SKILL_LINE_TARGET or chars > SKILL_CHAR_TARGET:
            warnings.append(
                f"{relative(skill_md)}: exceeds target context budget "
                f"({lines}/{SKILL_LINE_TARGET} lines, {chars}/{SKILL_CHAR_TARGET} chars)"
            )

    for reference in sorted(SKILLS.glob("*/references/**/*.md")):
        text = read(reference)
        lines = len(text.splitlines())
        if lines > 300:
            errors.append(f"{relative(reference)}: reference exceeds 300 lines ({lines})")
        if lines > 100 and not re.search(r"(?m)^## (?:Contents|Table of Contents)\s*$", text):
            errors.append(f"{relative(reference)}: long reference lacks a table of contents ({lines} lines)")

    lineage_contracts = [
        SKILLS / "research-idea-orchestrator" / "references" / "artifact-contracts.md",
        SKILLS / "proposal-orchestrator" / "references" / "artifact-naming-and-directory-rules.md",
        SKILLS / "article-orchestrator" / "references" / "artifact-contracts.md",
        SKILLS / "perspective-orchestrator" / "references" / "artifact-naming-and-directory-rules.md",
        SKILLS / "research-polisher-orchestrator" / "references" / "workflow-contract.md",
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
        SKILLS / "article-orchestrator" / "references" / "artifact-review-and-submission-contracts.md"
    )
    panel_contract = article_contracts.split("## Panel Report", 1)[1].split("## Cover Letter", 1)[0]
    if 'source_skill: "article-orchestrator"' not in panel_contract or "aggregation_owner" not in panel_contract:
        errors.append("article panel aggregate must be orchestrator-owned")
    if "human_signoff_ref" not in panel_contract:
        errors.append("article panel dissent lacks human-signoff lineage")
    cover_letter_skill = read(SKILLS / "article-cover-letter" / "SKILL.md")
    for marker in (
        "workflow_profile: article | perspective",
        "11_cover-letter/cover-letter-vNNN.md",
        "08_cover-letter/cover-letter-vNNN.md",
        "may_call: []",
    ):
        if marker not in cover_letter_skill:
            errors.append(f"article-cover-letter lacks dual-workflow contract marker `{marker}`")
    if "recommended_status" in cover_letter_skill:
        errors.append("article-cover-letter mechanical check must not promote itself")
    medical_review_skill = read(SKILLS / "medical-journal-review" / "SKILL.md")
    probability_contract = read(
        SKILLS
        / "medical-journal-review"
        / "references"
        / "publication-probability-assessment.md"
    )
    if "publication-probability-assessment.md" not in medical_review_skill:
        errors.append("medical-journal-review does not conditionally own probability estimation")
    for forbidden in (
        "without converting the score into publication probability",
        "Do not turn a structured score into a publication probability",
    ):
        if forbidden in medical_review_skill:
            errors.append("medical-journal-review retains the obsolete probability prohibition")
    for marker in (
        "assessment_scope: cover_letter_only | full_artifact | full_submission_package",
        "benchmark_status: verified_public | user_supplied | heuristic_only | unavailable",
        "eventual_acceptance_probability",
        "confidence: high | moderate | low | not_estimable",
        "built-in Search",
        "mathematically coherent",
        "do not create another artifact, reviewer, round, stage, state, or promotion rule",
    ):
        if marker not in probability_contract:
            errors.append(f"publication-probability contract lacks `{marker}`")
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

    idea_dossier_contract = read(
        SKILLS / "research-idea-orchestrator" / "references" / "idea-dossier-contract.md"
    )
    for marker in (
        "## Title, summary, audience, and positioning",
        "## Evidence chains",
        "## Title and positioning claim-support table",
        "## References",
        "**Input:**",
        "**Method / analysis / processing:**",
        "**Output:**",
        "**Supports:**",
        "Section 14 is the sole global authority",
        "supported / qualified / unsupported",
        "Similar prior work does not automatically require new work",
    ):
        if marker not in idea_dossier_contract:
            errors.append(f"Idea dossier contract lacks `{marker}`")
    idea_routing = read(
        SKILLS / "research-idea-orchestrator" / "references" / "adaptive-direction-routing.md"
    )
    for marker in (
        "focused_optimization",
        "bounded_exploration",
        "at most three",
        "invent a weak candidate to fill a quota",
        "exactly one bounded optimization",
        "human_direction_selection_required",
        "automatic optimization round",
    ):
        if marker not in idea_routing:
            errors.append(f"Idea adaptive routing contract lacks `{marker}`")
    idea_ledger = read(
        SKILLS / "research-idea-orchestrator" / "references" / "reference-ledger-contract.md"
    )
    for marker in (
        "references/reference-ledger.md",
        "Human-readable label",
        "Definition artifact",
        "Original source",
        "idea-evaluator` must not",
    ):
        if marker not in idea_ledger:
            errors.append(f"Idea reference-ledger contract lacks `{marker}`")
    idea_evaluator = read(SKILLS / "idea-evaluator" / "SKILL.md")
    for marker in (
        "reviewed_dossier_ref",
        "complete_dossier_confirmed",
        "dossier_only_input_confirmed",
        "dossier_locator",
        "current complete `idea-dossier-vNNN.md`",
    ):
        if marker not in idea_evaluator:
            errors.append(f"idea-evaluator lacks dossier-only marker `{marker}`")

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
    if not (
        "09_state/" in perspective_orchestrator
        and "references/workflow-manifest-schema.md" in perspective_orchestrator
    ):
        errors.append("perspective: workflow manifest location or schema route is missing")
    deep_research_rules = read(
        SKILLS / "research-landscape-mapper" / "references" / "deep-research-prompt-rules.md"
    )
    deep_research_template = read(
        SKILLS / "research-landscape-mapper" / "templates" / "deep-research-request.md"
    )
    deep_research_follow_up = read(
        SKILLS / "research-landscape-mapper" / "templates" / "deep-research-follow-up-guide.md"
    )
    if "Single-stage targeted retrieval" in deep_research_rules or "All six sections present" in deep_research_rules:
        errors.append("Deep Research Focused mode conflicts with the global phased contract")
    if "[F] 单阶段 targeted retrieval" in deep_research_template or "[F] 跳过此阶段" in deep_research_template:
        errors.append("Deep Research Focused template skips required phases")
    if "deep-research-report-vNNN.md" not in deep_research_template + deep_research_follow_up:
        errors.append("Deep Research continuation package lacks the versioned return report contract")
    academic_deep_search = read(SKILLS / "focused-literature-synthesizer" / "SKILL.md")
    if (
        "2-5" not in academic_deep_search
        or "route to `research-landscape-mapper`" not in academic_deep_search
        or "Do not broaden this skill into Deep Research" not in academic_deep_search
    ):
        errors.append("focused-literature-synthesizer must remain limited to narrow questions answerable from 2-5 papers")
    opportunity_mapper = read(SKILLS / "research-landscape-mapper" / "SKILL.md")
    if (
        "single owner of broad retrieval policy" not in opportunity_mapper
        or "Built-in Search" not in opportunity_mapper
        or "deep_research_handoff_required" not in opportunity_mapper
        or "Local scripts are never the default" not in opportunity_mapper
    ):
        errors.append("research-landscape-mapper does not exclusively own native Search/Deep Research routing")
    if "evidence_change_assessment" not in read(
        SKILLS / "research-landscape-mapper" / "references" / "search-routing-rules.md"
    ):
        errors.append("research-landscape-mapper lacks the evidence-change routing contract")
    for orchestrator_name in orchestrators:
        orchestrator_text = read(names[orchestrator_name])
        for residue in ("built-in Search", "Deep Research", "evidence_search.py", "local retrieval script"):
            if residue in orchestrator_text:
                errors.append(f"{orchestrator_name}: direct retrieval-policy residue `{residue}`")
        machine = next(
            (
                value
                for value in state_machines.values()
                if value.get("orchestrator") == orchestrator_name
            ),
            {},
        )
        required_states = set(canonical_states)
        if machine.get("workflow_profile") == "reviewer_matrix_assemble_evaluate":
            required_states.discard("human_signoff_required")
            required_states.add("human_strategy_selection_required")
        for state in required_states:
            if state not in orchestrator_text:
                errors.append(f"{orchestrator_name}: canonical workflow state missing `{state}`")
        if not re.search(r"\b(?:one|single) writer\b", orchestrator_text, re.I) or not re.search(
            r"\bconcurrent(?: source)? writes\b", orchestrator_text, re.I
        ):
            errors.append(f"{orchestrator_name}: single-writer/concurrency contract missing")
    article_orchestrator = read(SKILLS / "article-orchestrator" / "SKILL.md")
    if (
        "`fast_track_draft`" not in article_orchestrator
        or re.search(
            r"`fast_track_draft`[^\n]*readiness triage",
            article_orchestrator,
            re.I,
        )
        is None
    ):
        errors.append("article fast-track draft path must run independent readiness triage")
    perspective_minor_patch = perspective_orchestrator.split("### STEP 8.5: Panel Minor Revision Patch", 1)[1].split(
        "### STEP 9: Final Compositor", 1
    )[0]
    if (
        re.search(r"fresh[^\n]*evaluator", perspective_minor_patch, re.I) is None
        or not (
            "no changed draft goes directly to the compositor" in perspective_minor_patch.lower()
            or "never route a panel minor patch directly to the final compositor"
            in perspective_minor_patch.lower()
        )
    ):
        errors.append("perspective panel minor patch must receive fresh re-evaluation before final composition")
    perspective_architect = read(SKILLS / "perspective-argument-architect" / "SKILL.md")
    perspective_refiner = read(SKILLS / "perspective-refinement-controller" / "SKILL.md")
    if "claim-change-requests/" in perspective_architect + perspective_refiner:
        errors.append("perspective: claim change requests escape 01_claims/change-requests/")
    if "panel-02_evidence/" in perspective_orchestrator:
        errors.append("perspective: malformed panel evidence delegate path")
    perspective_compositor = read(SKILLS / "perspective-final-compositor" / "SKILL.md")
    if "text-identical" not in perspective_compositor or "Do not edit" not in perspective_compositor:
        errors.append("perspective compositor may change final prose after evaluation")
    if not all(
        marker in perspective_orchestrator
        for marker in ("`article-cover-letter`", "08_cover-letter/", "publication probability")
    ):
        errors.append("perspective workflow lacks the Cover Letter or probability route")
    if not all(
        marker in perspective_compositor
        for marker in ("08_final/cover-letter.md", "text-identically", "do not calculate, reinterpret, or adjust")
    ):
        errors.append("perspective compositor does not faithfully carry the Cover Letter or probability")

    readme_contract = read(
        SKILLS
        / "research-idea-orchestrator"
        / "references"
        / "project-readme-contract.md"
    )
    for marker in (
        "## Current delivery",
        "## Current artifact",
        "## Status",
        "## Review summary",
        "## Next action",
        "## Publication probability",
        "Never give it to a reviewer",
    ):
        if marker not in readme_contract:
            errors.append(f"project README contract lacks `{marker}`")
    for orchestrator_name in orchestrators:
        if "project-readme-contract.md" not in read(names[orchestrator_name]):
            errors.append(f"{orchestrator_name}: project README terminal-update route missing")
    for reviewer_name in reviewer_names:
        if "project-readme-contract.md" in read(names[reviewer_name]):
            errors.append(f"{reviewer_name}: reviewer must not read the project README")

    reviewer_input_allowance = re.compile(
        r"(?:allowed inputs?|allowed files?|may read|frozen reads|隔离包文件)[^\n]*README\.md",
        re.I,
    )
    for reviewer_name in reviewer_names:
        if reviewer_input_allowance.search(read(names[reviewer_name])):
            errors.append(f"{reviewer_name}: project README is listed as an allowed reviewer input")

    perspective_panel = read(SKILLS / "perspective-review-panel" / "SKILL.md")
    idea_panel = read(SKILLS / "idea-adversarial-review-panel" / "SKILL.md")
    proposal_briefs = read(
        SKILLS / "proposal-orchestrator" / "references" / "delegate-brief-templates.md"
    )
    perspective_briefs = read(
        SKILLS / "perspective-orchestrator" / "references" / "delegate-brief-templates.md"
    )
    language_assessor = read(SKILLS / "academic-language-assessor" / "SKILL.md")
    language_template = read(
        SKILLS / "academic-language-assessor" / "templates" / "language-assessment-report.md"
    )
    if "preflight if available" in perspective_panel or "evidence limits, preflight" in idea_panel:
        errors.append("review panels must receive anonymous methods facts, not preflight reports")
    if "readiness_report_path_or_text" in proposal_briefs or "preflight_report_path_or_text" in proposal_briefs:
        errors.append("proposal evaluator briefs expose another reviewer report")
    if "list and revision delta" in language_assessor.lower() or "| Metric | Previous | Current |" in language_template:
        errors.append("language reassessment exposes revision history or prior scores")
    if "list and revision delta" in perspective_briefs.lower():
        errors.append("Perspective re-evaluation brief exposes the revision delta")
    if "methodology-statistics-preflight.md if available" in perspective_briefs:
        errors.append("Perspective methodology reviewer brief exposes a preflight report")
    proposal_refiner = read(SKILLS / "proposal-refinement-controller" / "SKILL.md")
    proposal_rules = read(
        SKILLS / "proposal-orchestrator" / "references" / "delegation-rules-pattern.md"
    )
    if "must-fix list plus delta" in proposal_refiner.lower():
        errors.append("proposal re-evaluation brief exposes the revision delta")
    if "proposal/context, preflight," in proposal_rules.lower():
        errors.append("SAP evaluator routing exposes a preflight reviewer report")
    evaluator_contract_files = (
        SKILLS / "proposal-evaluator" / "references" / "schema-proposal-evaluation-report.md",
        SKILLS / "proposal-evaluator" / "templates" / "template-proposal-evaluation-report.md",
        SKILLS / "sap-evaluator" / "references" / "schema-sap-evaluation-report.md",
        SKILLS / "sap-evaluator" / "templates" / "template-sap-evaluation-report.md",
    )
    for contract_path in evaluator_contract_files:
        if "stop_no_gain" in read(contract_path):
            errors.append(
                f"{relative(contract_path)}: evaluator must not derive cross-round stop_no_gain"
            )
    sap_controller = read(SKILLS / "sap-refinement-controller" / "SKILL.md")
    if "It must exclude the previous SAP, SAP delta, preflight report" not in sap_controller:
        errors.append("SAP re-evaluation brief does not seal history and preflight review")
    proposal_panel_independence = read(
        SKILLS / "proposal-review-panel" / "references" / "policy-reviewer-independence.md"
    )
    if "proposal evaluation report, if provided" in proposal_panel_independence.lower():
        errors.append("proposal panel independence policy exposes an evaluator report")

    polisher_orchestrator = read(
        SKILLS / "research-polisher-orchestrator" / "SKILL.md"
    )
    for marker in (
        "scientific_significance",
        "practical_value",
        "dissemination_editorial",
        "reposition_only",
        "small_extension",
        "moderate_extension",
        "human_strategy_selection_required",
    ):
        if marker not in polisher_orchestrator:
            errors.append(f"research-polisher-orchestrator lacks required contract marker `{marker}`")
    if not all(
        marker in polisher_orchestrator.lower()
        for marker in ("language polishing", "drafting", "idea generation", "general literature search")
    ):
        errors.append("Research Polisher public route does not exclude ordinary writing/search tasks")

    polisher_strategy = read(
        SKILLS / "research-polisher-strategy-reviewer" / "SKILL.md"
    )
    for marker in (
        "no_defensible_option",
        "added work",
        "peer strategist reports",
        "reposition_only",
    ):
        if marker.lower() not in polisher_strategy.lower():
            errors.append(f"Research Polisher strategy reviewer lacks `{marker}` contract")

    polisher_assembler = read(
        SKILLS / "research-polisher-plan-assembler" / "SKILL.md"
    )
    if not all(
        marker in polisher_assembler.lower()
        for marker in ("do not score", "do not invent", "dissent", "automatic winner")
    ):
        errors.append("Research Polisher assembler may judge, invent, or hide strategy options")

    polisher_final_reviewer = read(
        SKILLS
        / "research-polisher-methodology-publishability-reviewer"
        / "SKILL.md"
    )
    if not all(
        marker in polisher_final_reviewer.lower()
        for marker in (
            "raw strategist reports",
            "acceptance probability",
            "target_requirements_unverified",
            "not_assessable",
        )
    ):
        errors.append("Research Polisher final reviewer lacks blindness or publication-boundary controls")

    for report_name in ("phase2-targeted-search-smoke.md", "phase2-deep-research-handoff-smoke.md"):
        if not (PLUGIN / "reports" / report_name).exists():
            errors.append(f"missing Phase 2 smoke artifact: reports/{report_name}")

    plugin_readme = read(PLUGIN / "README.md")
    if "\\`" in plugin_readme:
        errors.append("plugin README contains escaped Markdown code delimiters")
    documentation_contracts = {
        REPO / "AGENTS.md",
        PLUGIN / "AGENTS.md",
        PLUGIN / "README.md",
        PLUGIN / "ROADMAP.md",
        REPO / ".github" / "workflows" / "openai-plugin-preview.yml",
        REPO / "scripts" / "openai_release_utils.py",
        REPO / "scripts" / "test_openai_release_contract.py",
    }
    for path in documentation_contracts:
        if not path.exists():
            errors.append(f"missing maintained personal-profile file: {relative(path)}")
            continue
        text = read(path)
        allowed_deleted_references = DELETED_ASSET_REFERENCE_ALLOWLIST.get(relative(path), set())
        for deleted in DELETED_PERSONAL_PROFILE_ASSETS:
            if deleted in text and deleted not in allowed_deleted_references:
                errors.append(f"{relative(path)}: references deleted asset `{deleted}`")

    print("OpenAI research plugin audit")
    print(f"skills: {len(skill_files)}")
    print(f"registry entries: {len(entries)}")
    print(f"workflow edges: {len(edges)}")
    print(f"independent reviewers: {len(reviewers)}")
    print("routing profile: personal-owner (7 declared / 6 implicit)")
    print(f"description characters: {description_chars}/{DESCRIPTION_BUDGET}")
    if orchestrators:
        max_initial = max(description_chars + len(read(names[name])) for name in orchestrators)
        print(
            "max conservative all-skill description+orchestrator proxy: "
            f"{max_initial}/{INITIAL_LOAD_BUDGET}"
        )
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"warnings: {len(warnings)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
