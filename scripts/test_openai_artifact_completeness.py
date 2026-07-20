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
    "Title, summary, audience, and positioning",
    "Structured abstract",
    "Background, current state, gap, significance, and rationale",
    "Research question, objectives, and core hypothesis",
    "Research content and work packages",
    "Data, materials, and existing evidence base",
    "Research design and methods",
    "Key techniques and implementation",
    "Evidence chains",
    "Required analyses and evidence",
    "Expected outputs, falsification criteria, and interpretations",
    "Contribution, innovation, impact, application, and closest-work comparison",
    "Title and positioning claim-support table",
    "Feasibility, resources, risks, alternatives, and stop conditions",
    "References",
)
COMPARATIVE_ONLY = re.compile(
    r"^(this|the) (version|revision) (adds|changes|updates)|^compared with (the )?prior",
    re.I,
)
FORBIDDEN_REVIEW_HISTORY = (
    "research-context",
    "evidence-opportunity-map",
    "evidence-map",
    "opportunity-map",
    "methodology-statistics-preflight",
    "reference-ledger",
    "revision-delta",
    "revision_delta",
    "must-fix",
    "must_fix",
    "evaluation-v001",
    "re-evaluation-v001",
    "proposal-v001.md",
    "manuscript-v001.md",
    "idea-dossier-v001.md",
    "idea-snapshot-v001.md",
)
INTERNAL_ID = re.compile(
    r"(?<![A-Za-z0-9])(?:[ACO]\d{1,4}|(?:MF|PF|EL|EV|FM|NG|PS|PANEL)-?[A-Z0-9-]*\d[A-Z0-9-]*)(?![A-Za-z0-9])",
    re.I,
)
CHAIN_FIELDS = (
    "Input",
    "Method / analysis / processing",
    "Output",
    "Supports",
    "Limits and failure conditions",
)
ABSTRACT_FIELDS = (
    "Background and gap",
    "Objective and hypothesis",
    "Approach",
    "Expected result",
    "Contribution and impact",
)
ALLOWED_CONTRIBUTION_FRAMES = {
    "scientific_discovery",
    "method",
    "replication",
    "validation",
    "application",
    "resource",
    "benchmark",
    "practical",
    "translational",
    "integration",
    "editorial_repositioning",
}
IDEA_CHANGE_TYPES = {"create", "revise", "evidence_claim_sync", "editorial_reposition", "editorial_repair"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def idea_dossier(
    plugin_version: str,
    version: int = 1,
    title: str = "External-validation study of dynamic models for clinical research evaluation",
) -> str:
    body = [
        "---",
        "schema_version: research-idea.v3",
        f"plugin_version: {plugin_version}",
        f"artifact_id: idea-I01-001-v{version:03d}",
        "workflow_id: wf-artifact-completeness",
        "idea_id: I01-001",
        f"version_id: v{version:03d}",
        f"change_type: {'create' if version == 1 else 'editorial_reposition'}",
        "parent_idea_ids: []",
        "based_on: []",
        "source_skill: multi-path-idea-generator",
        "created_round: 1",
        "identity_anchor:",
        "  primary_research_question: Does the frozen model transport to a held-out cohort?",
        "  primary_objective: Quantify external validity",
        "  study_object: Frozen dynamic clinical model",
        "  core_data_or_evidence_base: Held-out clinical cohort",
        "  primary_unit_of_inference: Patient episode",
        "frozen: true",
        "---",
        "",
        f"# {title}",
        "",
    ]
    section_content = {
        IDEA_SECTIONS[0]: (
            f"- **Title:** {title}\n"
            "- **One-sentence complete-Idea summary:** Validate a frozen dynamic model in a held-out cohort and quantify transportability for clinical research evaluation.\n"
            "- **Primary audience:** Clinical researchers and model-validation methodologists.\n"
            "- **Positioning and contribution frame:** Validation with evidence-bounded audience repositioning."
        ),
        IDEA_SECTIONS[1]: "\n".join((
            "- **Background and gap:** Dynamic models often lack held-out transportability evidence.",
            "- **Objective and hypothesis:** Quantify external validity and test whether useful calibration is retained.",
            "- **Approach:** Apply the frozen model and prespecified validation analyses to a held-out cohort.",
            "- **Expected result:** Calibration, discrimination, and decision-curve estimates with uncertainty.",
            "- **Contribution and impact:** A reproducible validation package for clinical research use.",
        )),
        IDEA_SECTIONS[8]: "\n".join(
            (
                "### Evidence chain: External validation in a held-out cohort",
                "",
                "- **Input:** Frozen cohort, prespecified outcomes, and documented covariates.",
                "- **Method / analysis / processing:** Fit the prespecified model, calibrate it, and test sensitivity to missingness.",
                "- **Output:** Discrimination, calibration, and decision-curve estimates with uncertainty.",
                "- **Supports:** Objective: Quantify external validity; Core hypothesis: the model remains calibrated; Work package: Held-out validation.",
                "- **Limits and failure conditions:** Stop broad claims if calibration or transportability fails.",
            )
        ),
        IDEA_SECTIONS[3]: "\n".join(
            (
                "### Objective: Quantify external validity",
                "Estimate transportability in a held-out clinical population.",
                "",
                "### Core hypothesis: the model remains calibrated",
                "The prespecified model retains useful calibration after transport.",
            )
        ),
        IDEA_SECTIONS[4]: "### Work package: Held-out validation\nApply the frozen model and quantify transportability.",
        IDEA_SECTIONS[12]: "\n".join(
            (
                "| Title or positioning claim | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or `none` | Support status | Required qualifier |",
                "|---|---|---|---|---|---|---|---|",
                f"| {title} | validation | Research content and work packages > Held-out validation | Discrimination, calibration, and decision-curve estimates with uncertainty. | Smith et al. (2024) and the planned held-out validation | Held-out transportability estimates with uncertainty | supported | |",
            )
        ),
        IDEA_SECTIONS[14]: "Smith J, Lee K. External validation of dynamic clinical models. Journal of Methods. 2024;1:1-10. https://doi.org/10.1000/example.",
    }
    for heading in IDEA_SECTIONS:
        content = section_content.get(heading, f"Complete {heading.lower()} content linked to the current idea.")
        body.extend((f"## {heading}", "", content, ""))
    return "\n".join(body)


def markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        text,
        re.M | re.S,
    )
    return match.group("body").strip() if match else ""


def bold_field(section: str, label: str) -> str:
    match = re.search(rf"^- \*\*{re.escape(label)}:\*\*\s*(.+)$", section, re.M)
    return match.group(1).strip() if match else ""


def validate_dossier(text: str) -> list[str]:
    errors: list[str] = []
    frontmatter_match = re.match(r"^---\s*\n(?P<body>.*?)\n---\s*\n", text, re.S)
    try:
        frontmatter = yaml.safe_load(frontmatter_match.group("body")) if frontmatter_match else {}
    except yaml.YAMLError:
        frontmatter = {}
    if not isinstance(frontmatter, dict) or frontmatter.get("change_type") not in IDEA_CHANGE_TYPES:
        errors.append("invalid_change_type")
    if isinstance(frontmatter, dict) and "status" in frontmatter:
        errors.append("mutable_status_forbidden")
    h1_titles = re.findall(r"^# (?!#)(.+)$", text, re.M)
    if len(h1_titles) != 1:
        errors.append("unique_h1_required")
    h1_title = h1_titles[0].strip() if len(h1_titles) == 1 else ""
    positions = []
    for heading in IDEA_SECTIONS:
        marker = f"## {heading}"
        if marker not in text:
            errors.append(f"missing:{heading}")
        else:
            positions.append(text.index(marker))
    if positions != sorted(positions):
        errors.append("section_order")
    summary_body = markdown_section(text, IDEA_SECTIONS[0])
    title_field = bold_field(summary_body, "Title")
    complete_summary = bold_field(summary_body, "One-sentence complete-Idea summary")
    audience = bold_field(summary_body, "Primary audience")
    positioning = bold_field(summary_body, "Positioning and contribution frame")
    if not h1_title or not title_field or title_field != h1_title:
        errors.append("title_field_h1_mismatch")
    if not complete_summary or COMPARATIVE_ONLY.search(complete_summary):
        errors.append("comparative_or_missing_summary")
    if not audience:
        errors.append("primary_audience_missing")
    if not positioning:
        errors.append("positioning_missing")
    abstract = markdown_section(text, IDEA_SECTIONS[1])
    for field in ABSTRACT_FIELDS:
        if not bold_field(abstract, field):
            errors.append(f"structured_abstract_missing_{field.lower().replace(' ', '_')}")
    if len(re.findall(r"^## ", text, re.M)) != len(IDEA_SECTIONS):
        errors.append("partial_or_extra_body")
    for heading in IDEA_SECTIONS:
        body = markdown_section(text, heading)
        if not body or re.fullmatch(r"(?:TBD|TODO|N/?A|placeholder)[.!]?", body, re.I):
            errors.append(f"empty_or_placeholder:{heading}")
    if INTERNAL_ID.search("\n".join(line for line in text.splitlines() if not line.startswith("artifact_id:"))):
        errors.append("internal_workflow_reference")
    errors.extend(validate_evidence_chains(markdown_section(text, "Evidence chains")))
    errors.extend(validate_evidence_chain_coverage(text))
    errors.extend(validate_dossier_claim_table(text))
    errors.extend(validate_standard_references(text))
    return errors


def validate_evidence_chains(section: str) -> list[str]:
    errors: list[str] = []
    chains = list(re.finditer(r"^### (?P<title>.+?)\s*$\n(?P<body>.*?)(?=^### |\Z)", section, re.M | re.S))
    if not chains:
        return ["evidence_chain_missing"]
    for index, chain in enumerate(chains, 1):
        title = chain.group("title").removeprefix("Evidence chain:").strip()
        if not chain.group("title").strip().startswith("Evidence chain:"):
            errors.append(f"evidence_chain_heading:{index}")
        if re.fullmatch(r"[A-Z]{1,5}-?\d+", title, re.I):
            errors.append(f"evidence_chain_opaque_title:{index}")
        body = chain.group("body")
        for field in CHAIN_FIELDS:
            match = re.search(rf"^- \*\*{re.escape(field)}:\*\*\s*(.+)$", body, re.M)
            if not match or not match.group(1).strip():
                errors.append(f"evidence_chain_missing_{field.lower().replace(' ', '_')}:{index}")
    return errors


def validate_evidence_chain_coverage(text: str) -> list[str]:
    errors: list[str] = []
    targets: list[tuple[str, str]] = []
    for section_name, prefixes in (
        ("Research question, objectives, and core hypothesis", ("Objective", "Core hypothesis")),
        ("Research content and work packages", ("Work package",)),
    ):
        section = markdown_section(text, section_name)
        for prefix in prefixes:
            for match in re.finditer(rf"^### {re.escape(prefix)}:\s*(.+)$", section, re.M):
                targets.append((prefix, match.group(1).strip()))
    if not targets:
        return ["evidence_chain_targets_missing"]
    chain_section = markdown_section(text, "Evidence chains").lower()
    for prefix, title in targets:
        if f"{prefix}: {title}".lower() not in chain_section:
            errors.append(f"evidence_chain_unlinked_{prefix.lower().replace(' ', '_')}:{title}")
    return errors


def parse_claim_support_table(text: str) -> list[dict[str, object]]:
    section = markdown_section(text, "Title and positioning claim-support table")
    rows = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        return []
    headers = [cell.strip().lower() for cell in rows[0].strip("|").split("|")]
    expected = [
        "title or positioning claim",
        "contribution frame / claim type",
        "existing implementation that supports it",
        "supporting evidence-chain output",
        "literature or existing-result basis",
        "actual increment, or `none`",
        "support status",
        "required qualifier",
    ]
    if headers != expected:
        return []
    parsed: list[dict[str, object]] = []
    for row in rows[2:]:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) != len(expected):
            continue
        parsed.append(
            {
                "claim": cells[0],
                "claim_type": cells[1],
                "implementation": cells[2],
                "evidence_chain_output": cells[3],
                "basis": cells[4],
                "actual_increment": cells[5],
                "status": cells[6],
                "required_qualifier": cells[7],
                "contribution_frame": cells[1],
            }
        )
    return parsed


def evidence_chain_outputs(text: str) -> set[str]:
    section = markdown_section(text, "Evidence chains")
    return {
        match.group(1).strip()
        for match in re.finditer(r"^- \*\*Output:\*\*\s*(.+)$", section, re.M)
        if match.group(1).strip()
    }


def validate_dossier_claim_table(text: str) -> list[str]:
    entries = parse_claim_support_table(text)
    if not entries:
        return ["claim_support_table_invalid_or_empty"]
    title_matches = re.findall(r"^# (?!#)(.+)$", text, re.M)
    if len(title_matches) != 1:
        return ["title_claim_missing"]
    title = title_matches[0].strip()
    if not any(str(entry.get("claim", "")).strip().lower() == title.lower() for entry in entries):
        return ["visible_title_claim_missing_support_row"]
    return validate_claim_support(entries, [title], evidence_chain_outputs(text))


def validate_standard_references(text: str) -> list[str]:
    errors: list[str] = []
    references = markdown_section(text, "References")
    body = text[: text.find("## References")] if "## References" in text else text
    citations = set(re.findall(r"\b([A-Z][A-Za-z'-]+)(?: et al\.)? \((\d{4}[a-z]?)\)", body))
    for author, year in citations:
        if not re.search(rf"(?mi)^.*\b{re.escape(author)}\b.*\b{re.escape(year)}\b", references):
            errors.append(f"unresolved_standard_reference:{author}-{year}")
    numbered = {int(number) for number in re.findall(r"(?<!\[)\[(\d{1,3})\](?!\])", body)}
    for number in numbered:
        if not re.search(rf"(?m)^\s*(?:\[{number}\]|{number}\.)\s+", references):
            errors.append(f"unresolved_standard_reference:{number}")
    if not citations and not numbered:
        errors.append("standard_reference_citation_missing")
    return errors


def validate_claim_support(
    entries: list[dict[str, object]],
    visible_claims: list[str],
    available_chain_outputs: set[str],
    *,
    similar_study_exists: bool = False,
) -> list[str]:
    errors: list[str] = []
    visible = " ".join(visible_claims).lower()
    if not entries:
        return ["claim_support_missing"]
    for entry in entries:
        claim = str(entry.get("claim", "")).strip()
        status = str(entry.get("status", "")).strip()
        output = str(entry.get("evidence_chain_output", "")).strip()
        implementation = str(entry.get("implementation", "")).strip()
        basis = str(entry.get("basis", "")).strip()
        qualifier = str(entry.get("required_qualifier", "")).strip()
        frame = str(entry.get("contribution_frame", "")).strip()
        actual_increment = str(entry.get("actual_increment", "")).strip()
        if actual_increment.lower() == "none":
            actual_increment = ""
        if not claim or status not in {"supported", "qualified", "unsupported"}:
            errors.append("claim_support_invalid_entry")
            continue
        if output not in available_chain_outputs:
            errors.append(f"claim_support_unknown_output:{claim}")
        if not implementation:
            errors.append(f"claim_support_missing_implementation:{claim}")
        if not basis:
            errors.append(f"claim_support_missing_basis:{claim}")
        claim_visible = claim.lower() in visible
        if claim_visible and status == "unsupported":
            errors.append(f"unsupported_visible_claim:{claim}")
        if claim_visible and status == "qualified" and (not qualifier or qualifier.lower() not in visible):
            errors.append(f"required_qualifier_missing:{claim}")
        if frame not in ALLOWED_CONTRIBUTION_FRAMES:
            errors.append(f"unsupported_contribution_frame:{claim}")
        novelty_claimed = bool(re.search(r"\b(?:first|novel|new|unprecedented)\b", claim, re.I)) or frame == "scientific_discovery"
        if similar_study_exists and novelty_claimed and not actual_increment:
            errors.append(f"false_novelty:{claim}")
    return errors


def route_idea(
    direction_clarity: str,
    current_direction_value: str,
    evidence_confidence: str,
    supported_directions: list[dict[str, object]],
) -> tuple[str, int]:
    credible = [
        item for item in supported_directions
        if item.get("evidence_confidence") in {"high", "moderate"}
    ]
    if evidence_confidence == "low":
        return "direction_route_confirmation_required", 0
    if direction_clarity == "clear" and current_direction_value == "supported":
        return "focused_optimization", 1
    if direction_clarity in {"underdefined", "ambiguous"}:
        if len(credible) >= 2:
            ranks = [item.get("selection_rank") for item in credible]
            if len(credible) > 3 and (None in ranks or len(set(ranks)) != len(ranks)):
                return "direction_route_confirmation_required", 0
            return "bounded_exploration", min(len(credible), 3)
        if len(credible) == 1:
            return "focused_optimization", 1
    if current_direction_value == "unsupported" and not credible:
        return "no_defensible_direction", 0
    return "direction_route_confirmation_required", 0


def validate_exploration_trace(events: list[dict[str, str]], direction_ids: set[str], final_state: str) -> list[str]:
    errors: list[str] = []
    refresh_at: dict[str, int] = {}
    optimizations: dict[str, list[int]] = {direction_id: [] for direction_id in direction_ids}
    evaluators: dict[str, list[int]] = {direction_id: [] for direction_id in direction_ids}
    structural_change_at: int | None = None
    for index, event in enumerate(events):
        direction_id = event.get("direction_id", "")
        if event.get("type") == "idea_optimized":
            optimizations.setdefault(direction_id, []).append(index)
        if event.get("type") == "opportunity_map_refreshed":
            refresh_at[direction_id] = index
        if event.get("type") == "idea_evaluated":
            evaluators.setdefault(direction_id, []).append(index)
        if event.get("type") == "structural_change_requested_after_remap":
            structural_change_at = index
    for direction_id in direction_ids:
        if len(optimizations.get(direction_id, [])) != 1:
            errors.append(f"exploration_optimization_count:{direction_id}")
        if direction_id not in refresh_at:
            errors.append(f"exploration_refresh_missing:{direction_id}")
            continue
        if optimizations.get(direction_id) and optimizations[direction_id][0] > refresh_at[direction_id]:
            errors.append(f"exploration_optimization_after_refresh:{direction_id}")
        if structural_change_at is not None:
            continue
        if len(evaluators.get(direction_id, [])) != 1:
            errors.append(f"exploration_terminal_evaluator_count:{direction_id}")
        elif evaluators[direction_id][0] < refresh_at[direction_id]:
            errors.append(f"exploration_evaluator_before_refresh:{direction_id}")
    if structural_change_at is not None:
        if final_state != "revision_required":
            errors.append("exploration_structural_change_state")
        if any(
            index > structural_change_at and event.get("type") == "idea_optimized"
            for index, event in enumerate(events)
        ):
            errors.append("exploration_automatic_second_optimization")
    elif final_state != "human_direction_selection_required":
        errors.append("exploration_final_state")
    return errors


def legacy_layout_status(schema_version: str, path: str) -> tuple[str, bool]:
    if schema_version in {"research-idea.v1", "research-idea.v2"}:
        return "layout_migration_required", True
    if schema_version == "research-idea.v3" and "/dossiers/idea-dossier-v" in path.replace("\\", "/"):
        return "current", False
    return "invalid_layout", True


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
    require(policy.get("idea_schema") == "research-idea.v3", "registry idea schema")
    require(policy.get("idea_current_artifact") == "complete_markdown_dossier", "registry Idea dossier authority")
    require(set(policy.get("idea_dossier_change_types", [])) == IDEA_CHANGE_TYPES, "registry Idea change-type vocabulary")
    require(policy.get("idea_legacy_schemas") == ["research-idea.v1", "research-idea.v2"], "registry Idea legacy schemas")
    require(
        policy.get("idea_legacy_layout_behavior") == "layout_migration_required_read_only_no_automatic_rewrite",
        "registry Idea legacy read-only behavior",
    )
    chain_policy = policy.get("idea_evidence_chain_contract", {})
    require(
        chain_policy.get("required_fields")
        == [
            "input",
            "method_analysis_or_processing",
            "output",
            "supported_objective_or_claim",
        ],
        "registry semi-structured evidence-chain fields",
    )
    editorial_policy = policy.get("idea_editorial_repositioning_contract", {})
    require(editorial_policy.get("added_work_required_for_supported_repositioning") is False, "registry permits supported no-work repositioning")
    require(editorial_policy.get("editorial_change_requires_fresh_evaluation") is True, "registry title change requires fresh evaluation")
    require(editorial_policy.get("claim_support_states") == ["supported", "qualified", "unsupported"], "registry claim-support states")
    require(set(editorial_policy.get("contribution_frames", [])) == ALLOWED_CONTRIBUTION_FRAMES, "registry contribution-frame vocabulary")
    evaluator_policy = policy.get("idea_evaluator_project_input_contract", {})
    require(evaluator_policy.get("exact_project_artifact_count") == 1, "registry evaluator gets one project artifact")
    require(
        evaluator_policy.get("allowed_project_artifacts") == ["current_complete_idea_dossier"],
        "registry evaluator only receives current dossier",
    )
    require(
        evaluator_policy.get("logical_binding_fields") == ["artifact_id", "version", "path"]
        and evaluator_policy.get("content_digest_required") is False
        and evaluator_policy.get("readiness_reports_visible") is False,
        "registry evaluator uses isolated logical dossier binding",
    )
    expected_forbidden = {
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
    require(set(evaluator_policy.get("forbidden_project_artifacts", [])) == expected_forbidden, "registry evaluator forbidden project inputs")
    idea_machine = registry.get("workflow_state_machines", {}).get("idea", {})
    require(idea_machine.get("primary_artifact_type") == "idea_dossier", "registry Idea primary role")
    profiles = idea_machine.get("internal_direction_profiles", {})
    require(profiles.get("focused_optimization", {}).get("current_dossier_count") == 1, "focused route has one dossier")
    bounded = profiles.get("bounded_exploration", {})
    require(bounded.get("current_dossier_count") == {"minimum": 2, "maximum": 3}, "bounded route has two to three dossiers")
    require(bounded.get("optimization_round_limit_per_direction") == 1, "bounded route has one optimization")
    require(bounded.get("evidence_and_opportunity_remap_after_optimization") is True, "bounded route remaps after optimization")
    require(bounded.get("fresh_evaluator_per_current_dossier_after_remap") is True, "bounded route fresh-evaluates every dossier")
    require(bounded.get("final_state") == "human_direction_selection_required", "bounded route stops for human selection")
    focused_gates = idea_machine.get("before_packaging_by_direction_profile", {}).get("focused_optimization", [])
    require(
        focused_gates == ["adversarial_reports_complete_when_proposal_handoff_candidate"],
        "focused panel is conditional on Proposal handoff",
    )
    scenario = registry.get("scenario_eval_contract", {})
    idea_package_rules = scenario.get("package_input_contracts", {}).get("idea", {}).get("required_inputs", [])
    panel_rule = next(rule for rule in idea_package_rules if rule.get("artifact_role") == "panel_report")
    require(
        panel_rule.get("required_when_condition") == "proposal_handoff_candidate"
        and "required_when_direction_profile" not in panel_rule,
        "Idea package panel rule is conditional, not route-wide",
    )
    idea_decisions = scenario.get("review_decision_contracts", {}).get("idea-evaluator", {})
    require("merge" not in idea_decisions.get("allowed", []), "Idea evaluator uses canonical decisions")
    actor_roles = scenario.get("runtime_artifact_role_contract", {}).get("actor_output_roles_by_skill", {})
    require(
        set(actor_roles.get("multi-path-idea-generator", []))
        == {"idea_dossier", "revision_delta", "proposed_navigation_metadata"},
        "Idea generator only proposes navigation metadata",
    )
    require(
        {"idea_index", "reference_ledger"}
        <= set(actor_roles.get("research-idea-orchestrator", [])),
        "Idea orchestrator owns index and ledger metadata",
    )
    handoff = idea_machine.get("proposal_handoff_contract", {})
    require(
        handoff.get("required_current_evaluation_decision") == "promote"
        and handoff.get("fresh_evaluation_required") is True
        and handoff.get("revise_then_promote_requires_revision_and_fresh_re_evaluation") is True,
        "Proposal handoff requires a fresh promote decision",
    )
    require(policy.get("article_schema") == "research-article.v6", "registry article schema")
    require(
        policy.get("fresh_re_evaluation", {}).get("forbidden")
        == ["prior_artifact", "revision_delta", "prior_report", "prior_score", "prior_decision"],
        "registry blind re-evaluation",
    )

    lifecycle = read(PLUGIN / "skills/research-idea-orchestrator/references/idea-artifact-lifecycle.md")
    dossier_contract = read(PLUGIN / "skills/research-idea-orchestrator/references/idea-dossier-contract.md")
    docx_contract = read(PLUGIN / "skills/article-orchestrator/references/article-docx-delivery-contract.md")
    for marker in IDEA_SECTIONS:
        require(marker in dossier_contract, f"dossier section {marker}")
    for marker in (
        "supported / qualified / unsupported",
        "Similar prior work does not automatically require new work",
        "validation, replication",
        "C24",
        "M1",
        "A0",
    ):
        require(marker in dossier_contract, f"Dossier claim/marker contract {marker}")
    require("idea-dossier-vNNN.md" in lifecycle, "lifecycle routes complete Idea dossiers")
    for marker in ("canonical_markdown_ref", "docx_sync_status", "render_qa_status", "missing_source_asset"):
        require(marker in docx_contract, f"DOCX contract {marker}")

    guards = 0
    with tempfile.TemporaryDirectory() as temp:
        node = Path(temp) / "03_ideas/nodes/I01-001"
        dossiers = node / "dossiers"
        dossiers.mkdir(parents=True)
        first = dossiers / "idea-dossier-v001.md"
        second = dossiers / "idea-dossier-v002.md"
        first.write_text(idea_dossier(plugin_version, 1), encoding="utf-8", newline="\n")
        second.write_text(
            idea_dossier(plugin_version, 2, "Validated dynamic models for research evaluation across clinical audiences"),
            encoding="utf-8",
            newline="\n",
        )
        require(not validate_dossier(read(first)), "complete initial dossier")
        require(not validate_dossier(read(second)), "complete revised dossier")
        require(digest(first) != digest(second), "version digest changes")
        guards += 3

        invalid_change_type = read(first).replace("change_type: create", "change_type: initial")
        require("invalid_change_type" in validate_dossier(invalid_change_type), "legacy dossier change_type rejected")
        mutable_status = read(first).replace("frozen: true", "status: draft\nfrozen: true", 1)
        require("mutable_status_forbidden" in validate_dossier(mutable_status), "mutable dossier status rejected")
        title_mismatch = read(first).replace(
            "- **Title:** External-validation study of dynamic models for clinical research evaluation",
            "- **Title:** A different internal title",
        )
        require("title_field_h1_mismatch" in validate_dossier(title_mismatch), "H1 and Title field mismatch rejected")
        missing_abstract_slot = read(first).replace(
            "- **Expected result:** Calibration, discrimination, and decision-curve estimates with uncertainty.\n",
            "",
        )
        require(
            "structured_abstract_missing_expected_result" in validate_dossier(missing_abstract_slot),
            "incomplete structured abstract rejected",
        )
        duplicate_h1 = read(first).replace(
            "# External-validation study of dynamic models for clinical research evaluation",
            "# External-validation study of dynamic models for clinical research evaluation\n\n# Duplicate title",
            1,
        )
        require("unique_h1_required" in validate_dossier(duplicate_h1), "duplicate H1 rejected")
        guards += 5

        partial = "## Title, summary, audience, and positioning\n\nThis version adds one analysis.\n\n## Contribution\n\nChanged only."
        require(bool(validate_dossier(partial)), "delta-only Idea rejected")
        require("comparative_or_missing_summary" in validate_dossier(partial), "comparative summary rejected")
        guards += 2

        opaque = read(first).replace("Validate a frozen dynamic model", "C24")
        require("internal_workflow_reference" in validate_dossier(opaque), "opaque workflow marker rejected")
        scientific_m1 = read(first).replace("A complete idea", "A complete idea about M1 macrophages")
        require("internal_workflow_reference" not in validate_dossier(scientific_m1), "scientific M1 term is not an internal marker")
        broken_chain = read(first).replace(
            "- **Output:** Discrimination, calibration, and decision-curve estimates with uncertainty.\n",
            "",
        )
        require(
            any(error.startswith("evidence_chain_missing_output") for error in validate_dossier(broken_chain)),
            "broken Input-Method-Output chain rejected",
        )
        unresolved_reference = read(first).replace("Smith J, Lee K.", "Jones R, Lee K.")
        require(
            any(error.startswith("unresolved_standard_reference") for error in validate_dossier(unresolved_reference)),
            "unresolved standard citation rejected",
        )
        unsupported_title = read(first).replace(
            "# External-validation study of dynamic models for clinical research evaluation",
            "# First universal cure for all clinical disease",
        )
        require(
            "visible_title_claim_missing_support_row" in validate_dossier(unsupported_title),
            "unmapped inflated title rejected by dossier validator",
        )
        unknown_output = read(first).replace(
            "| External-validation study of dynamic models for clinical research evaluation | validation | Research content and work packages > Held-out validation | Discrimination, calibration, and decision-curve estimates with uncertainty. |",
            "| External-validation study of dynamic models for clinical research evaluation | validation | Research content and work packages > Held-out validation | Nonexistent universal-effect output |",
        )
        require(
            any(error.startswith("claim_support_unknown_output") for error in validate_dossier(unknown_output)),
            "claim table output must resolve to a real evidence-chain output",
        )
        old_six_column = read(first).replace(
            "| Title or positioning claim | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or `none` | Support status | Required qualifier |",
            "| Title or positioning claim | Claim type | Supporting evidence-chain output | Literature or existing-result basis | Support status | Required qualifier |",
        )
        require(
            "claim_support_table_invalid_or_empty" in validate_dossier(old_six_column),
            "legacy six-column claim table rejected",
        )
        missing_implementation = read(first).replace(
            "| validation | Research content and work packages > Held-out validation |",
            "| validation | |",
        )
        require(
            any(error.startswith("claim_support_missing_implementation") for error in validate_dossier(missing_implementation)),
            "claim row without existing implementation rejected",
        )
        missing_basis = read(first).replace(
            "| Smith et al. (2024) and the planned held-out validation |",
            "| |",
        )
        require(
            any(error.startswith("claim_support_missing_basis") for error in validate_dossier(missing_basis)),
            "claim row without literature or existing-result basis rejected",
        )
        guards += 9

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
        title_only = dict(anchor)
        require(identity_status(anchor, title_only) == "preserved", "title-only repositioning is not identity drift")
        require(digest(first) != digest(second), "title-only repositioning creates a new version")
        title_revision_receipt = {
            "change_type": "editorial_reposition",
            "added_work_items": [],
            "prior_evaluator_instance_id": "idea-evaluator-001",
            "fresh_evaluator_instance_id": "idea-evaluator-002",
        }
        require(title_revision_receipt["added_work_items"] == [], "title repositioning may add no work")
        require(
            title_revision_receipt["prior_evaluator_instance_id"]
            != title_revision_receipt["fresh_evaluator_instance_id"],
            "title-only content version receives a fresh evaluator",
        )
        guards += 6

    current_review_inputs = [
        "03_ideas/nodes/I01-001/dossiers/idea-dossier-v002.md",
    ]
    require(not review_history_visible(current_review_inputs), "current-only review allowed")
    require(len(current_review_inputs) == 1, "Idea evaluator receives exactly one project file")
    for forbidden in (
        "01_context/research-context.md",
        "02_evidence/evidence-opportunity-map.md",
        "methodology-statistics-preflight.md",
        "references/reference-ledger.md",
        "revision-delta-r001.md",
        "anonymous-must-fix.md",
        "reviews/evaluation-v001.md",
    ):
        require(review_history_visible(current_review_inputs + [forbidden]), f"Idea evaluator rejects {forbidden}")
    require(review_history_visible(current_review_inputs + ["revision-delta-r001.md"]), "delta review rejected")
    require(review_history_visible(current_review_inputs + ["idea-dossier-v001.md"]), "prior dossier review rejected")
    guards += 11

    output_name = "Discrimination, calibration, and decision-curve estimates with uncertainty"
    supported_repositioning = [{
        "claim": "useful for a broader clinical research audience",
        "status": "qualified",
        "required_qualifier": "for research evaluation",
        "evidence_chain_output": output_name,
        "implementation": "Research content and work packages > Held-out validation",
        "basis": "Smith et al. (2024) and the frozen work package",
        "contribution_frame": "editorial_repositioning",
        "actual_increment": "",
    }]
    require(
        not validate_claim_support(
            supported_repositioning,
            ["Useful for a broader clinical research audience for research evaluation"],
            {output_name},
            similar_study_exists=True,
        ),
        "supported title/audience repositioning needs no new work",
    )
    guards += 1

    removed_qualifier = validate_claim_support(
        supported_repositioning,
        ["Useful for a broader clinical research audience"],
        {output_name},
        similar_study_exists=True,
    )
    require(any(error.startswith("required_qualifier_missing") for error in removed_qualifier), "removed qualifier rejected")
    unsupported = [{**supported_repositioning[0], "status": "unsupported"}]
    require(
        any(error.startswith("unsupported_visible_claim") for error in validate_claim_support(
            unsupported,
            ["useful for a broader clinical research audience"],
            {output_name},
        )),
        "unsupported title claim rejected",
    )
    false_novelty = [{
        **supported_repositioning[0],
        "claim": "First discovery of a universal clinical mechanism",
        "status": "supported",
        "required_qualifier": "",
        "contribution_frame": "scientific_discovery",
    }]
    require(
        any(error.startswith("false_novelty") for error in validate_claim_support(
            false_novelty,
            ["First discovery of a universal clinical mechanism"],
            {output_name},
            similar_study_exists=True,
        )),
        "false novelty rejected when similar work exists",
    )
    novel_method = [{
        **supported_repositioning[0],
        "claim": "Novel method for universal clinical prediction",
        "status": "supported",
        "required_qualifier": "",
        "contribution_frame": "method",
    }]
    require(
        any(error.startswith("false_novelty") for error in validate_claim_support(
            novel_method,
            ["Novel method for universal clinical prediction"],
            {output_name},
            similar_study_exists=True,
        )),
        "novel method claim without actual increment rejected",
    )
    for frame in ("replication", "validation", "application"):
        framed = [{**supported_repositioning[0], "status": "supported", "required_qualifier": "", "contribution_frame": frame}]
        require(
            not validate_claim_support(
                framed,
                ["useful for a broader clinical research audience"],
                {output_name},
                similar_study_exists=True,
            ),
            f"similar-study {frame} framing allowed",
        )
    unknown_frame = [{**supported_repositioning[0], "contribution_frame": "unknown_frame"}]
    require(
        any(error.startswith("unsupported_contribution_frame") for error in validate_claim_support(
            unknown_frame,
            ["useful for a broader clinical research audience for research evaluation"],
            {output_name},
        )),
        "unknown contribution frame rejected",
    )
    guards += 8

    direction = lambda name, rank, confidence="moderate": {
        "direction_id": name,
        "selection_rank": rank,
        "evidence_confidence": confidence,
    }
    require(route_idea("clear", "supported", "high", []) == ("focused_optimization", 1), "clear direction routes focused")
    require(route_idea("ambiguous", "uncertain", "moderate", [direction("D1", 1), direction("D2", 2)]) == ("bounded_exploration", 2), "two directions remain two")
    require(route_idea("underdefined", "uncertain", "high", [direction("D1", 1), direction("D2", 2), direction("D3", 3), direction("D4", 4)]) == ("bounded_exploration", 3), "exploration capped at three")
    require(route_idea("ambiguous", "uncertain", "moderate", [direction("D1", 1)]) == ("focused_optimization", 1), "single credible opportunity routes focused")
    require(route_idea("ambiguous", "unsupported", "moderate", []) == ("no_defensible_direction", 0), "no credible direction stops")
    require(route_idea("ambiguous", "uncertain", "low", [direction("D1", 1), direction("D2", 2)]) == ("direction_route_confirmation_required", 0), "low-confidence route asks human")
    tied = [direction("D1", 1), direction("D2", 1), direction("D3", 2), direction("D4", 3)]
    require(route_idea("ambiguous", "uncertain", "moderate", tied) == ("direction_route_confirmation_required", 0), "ambiguous top-three asks human")
    guards += 7

    exploration = [
        {"type": "idea_optimized", "direction_id": "D1"},
        {"type": "idea_optimized", "direction_id": "D2"},
        {"type": "opportunity_map_refreshed", "direction_id": "D1"},
        {"type": "opportunity_map_refreshed", "direction_id": "D2"},
        {"type": "idea_evaluated", "direction_id": "D1", "reviewer_instance_id": "eval-D1"},
        {"type": "idea_evaluated", "direction_id": "D2", "reviewer_instance_id": "eval-D2"},
    ]
    require(
        not validate_exploration_trace(exploration, {"D1", "D2"}, "human_direction_selection_required"),
        "bounded exploration refreshes maps before one terminal evaluator per direction",
    )
    early = [
        {"type": "idea_optimized", "direction_id": "D1"},
        {"type": "idea_evaluated", "direction_id": "D1"},
        {"type": "opportunity_map_refreshed", "direction_id": "D1"},
    ]
    require(any("before_refresh" in error for error in validate_exploration_trace(early, {"D1"}, "human_direction_selection_required")), "pre-refresh evaluator rejected")
    require("exploration_final_state" in validate_exploration_trace(exploration, {"D1", "D2"}, "human_signoff_required"), "exploration cannot enter ordinary signoff")
    structural_pause = [
        {"type": "idea_optimized", "direction_id": "D1"},
        {"type": "opportunity_map_refreshed", "direction_id": "D1"},
        {"type": "structural_change_requested_after_remap", "direction_id": "D1"},
    ]
    require(not validate_exploration_trace(structural_pause, {"D1"}, "revision_required"), "post-remap structural change pauses")
    illegal_second_round = structural_pause + [{"type": "idea_optimized", "direction_id": "D1"}]
    require(
        "exploration_automatic_second_optimization"
        in validate_exploration_trace(illegal_second_round, {"D1"}, "revision_required"),
        "post-remap structural change cannot start a second automatic optimization",
    )
    guards += 5

    compatibility = yaml.safe_load(read(REPO / "tests/openai_phase4/idea-layout-compatibility.yaml"))
    with tempfile.TemporaryDirectory() as temp:
        legacy_root = Path(temp)
        for case in compatibility["cases"]:
            legacy_path = legacy_root / Path(case["path"])
            legacy_path.parent.mkdir(parents=True, exist_ok=True)
            legacy_path.write_text(f"schema_version: {case['schema_version']}\n", encoding="utf-8", newline="\n")
        before = {
            path.relative_to(legacy_root).as_posix(): digest(path)
            for path in legacy_root.rglob("*")
            if path.is_file()
        }
        for case in compatibility["cases"]:
            status, read_only = legacy_layout_status(case["schema_version"], case["path"])
            require(status == case["expected_status"], f"legacy compatibility {case['case_id']} status")
            require(read_only is case["read_only"], f"legacy compatibility {case['case_id']} read-only")
            require(case.get("automatic_migration") is False, f"legacy compatibility {case['case_id']} never auto-migrates")
            require(case.get("fixture_kind") == "synthetic_tracked", "compatibility cases never depend on local ignored runs")
            guards += 4
        after = {
            path.relative_to(legacy_root).as_posix(): digest(path)
            for path in legacy_root.rglob("*")
            if path.is_file()
        }
        require(before == after, "legacy layout inspection performs no writes")
        require(not any("idea-dossier" in path for path in after if "snapshots" in path or "candidates" in path), "legacy inspection creates no v3 dossier")
        guards += 2

    proposal = "\n".join(f"## {h}\nComplete {h}." for h in ("Problem and gap", "Objectives", "Research plan", "Methods", "Feasibility", "Expected outputs"))
    article = "\n".join(f"## {h}\nComplete {h}." for h in ("Introduction", "Methods", "Results", "Discussion"))
    require(proposal_complete(proposal), "complete proposal accepted")
    require(not proposal_complete("## Methods\nOnly a changed method."), "partial proposal rejected")
    require(manuscript_complete(article), "complete article accepted")
    require(not manuscript_complete("## Results\nOnly changed results."), "partial article rejected")
    guards += 4

    portfolio = read(PLUGIN / "skills/idea-portfolio-assembler/templates/research-idea-portfolio.md")
    for marker in (
        "Current dossier artifact ID / version / path",
        "Relative dossier link",
        "Evaluation report link",
        "Reference ledger link",
        "Status",
        "Fatal / blocking findings",
        "Dissent",
        "Unresolved issues",
        "Next human action",
        "Do not copy or rewrite dossier prose here.",
    ):
        require(marker in portfolio, f"portfolio navigation field {marker}")
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
