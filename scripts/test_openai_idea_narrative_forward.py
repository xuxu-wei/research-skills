#!/usr/bin/env python3
"""Deterministic forward checks for Idea narrative and editorial readiness."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
FIXTURE = REPO / "tests" / "idea-narrative-forward-0.9.0-preview.3"
NEW_FIXTURE = REPO / "tests" / "脓毒症复杂系统模型"
BASELINE_CURRENT = FIXTURE / "one-pass-current" / "baseline-current"
FINAL_PREVIOUS = FIXTURE / "one-pass-current" / "direct-final-current-v22"
FINAL = FIXTURE / "one-pass-current" / "direct-final-current-v23"

BASELINE_DOSSIER = (
    REPO
    / "tests"
    / "idea-test-0.9.0-preview.1"
    / "0.9.0-preview.1"
    / "03_ideas"
    / "nodes"
    / "I01-001"
    / "dossiers"
    / "idea-dossier-v003.md"
)
OLD_EVALUATION = FIXTURE / "run-001" / "blind-evaluation-v003-r001.md"
FINAL_DOSSIER = FINAL / "idea-dossier-v057.md"
FINAL_DELTA = FINAL / "revision-delta-v056-to-v057.md"
FINAL_PRESERVATION = FINAL / "content-preservation-r131.md"
FINAL_NARRATIVE = FINAL / "narrative-assessment-r132.md"
FINAL_NARRATIVE_PLAN = FINAL / "narrative-repair-plan-r132.yaml"
FINAL_LANGUAGE = FINAL / "language-assessment-r132.md"
FINAL_EVALUATION = FINAL / "blind-evaluation-v057-r001.md"
ERROR_REPORT = FIXTURE / "error-localization-report-r001.md"
READINESS_CONTRACT = (
    PLUGIN
    / "skills"
    / "research-idea-orchestrator"
    / "references"
    / "editorial-readiness-and-preservation.md"
)

BLOCKING_SEVERITIES = {"critical", "major"}
IDENTITY_ANCHOR_FIELDS = {
    "primary_research_question",
    "primary_objective",
    "study_object",
    "core_data_or_evidence_base",
    "primary_unit_of_inference",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def read_text(path: Path) -> str:
    require(path.is_file(), f"missing fixture artifact: {path}")
    return path.read_text(encoding="utf-8-sig")


def frontmatter(path: Path) -> dict[str, Any]:
    raw = read_text(path)
    require(raw.startswith("---"), f"missing YAML frontmatter: {path}")
    parts = raw.split("---", 2)
    require(len(parts) == 3, f"unterminated YAML frontmatter: {path}")
    payload = yaml.safe_load(parts[1])
    require(isinstance(payload, dict), f"frontmatter is not an object: {path}")
    return payload


def markdown_body(path: Path) -> str:
    raw = read_text(path)
    require(raw.startswith("---"), f"missing YAML frontmatter: {path}")
    parts = raw.split("---", 2)
    require(len(parts) == 3, f"unterminated YAML frontmatter: {path}")
    return parts[2]


def yaml_file(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(read_text(path))
    require(isinstance(payload, dict), f"YAML is not an object: {path}")
    return payload


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def load_linter() -> Any:
    return load_module(
        "idea_dossier_linter",
        PLUGIN
        / "skills"
        / "multi-path-idea-generator"
        / "scripts"
        / "lint_idea_dossier.py",
    )


def load_narrative_validator() -> Any:
    return load_module(
        "idea_narrative_output_validator",
        PLUGIN
        / "skills"
        / "idea-narrative-assessor"
        / "scripts"
        / "validate_narrative_outputs.py",
    )


def load_language_validator() -> Any:
    return load_module(
        "language_assessment_validator",
        PLUGIN
        / "skills"
        / "academic-language-assessor"
        / "scripts"
        / "validate_language_assessment.py",
    )


def load_writer_brief_validator() -> Any:
    return load_module(
        "editorial_writer_brief_validator",
        PLUGIN
        / "skills"
        / "research-idea-orchestrator"
        / "scripts"
        / "validate_editorial_repair_writer_brief.py",
    )


def ref_version(ref: dict[str, Any]) -> str:
    value = ref.get("version", ref.get("version_id"))
    require(isinstance(value, str) and bool(value), f"logical reference lacks version: {ref}")
    return value


def ref_pair(ref: dict[str, Any]) -> tuple[str, str]:
    artifact_id = ref.get("artifact_id")
    require(
        isinstance(artifact_id, str) and bool(artifact_id),
        f"logical reference lacks artifact_id: {ref}",
    )
    return artifact_id, ref_version(ref)


def ref_triple(ref: dict[str, Any]) -> tuple[str, str, str]:
    path = ref.get("path")
    require(isinstance(path, str) and bool(path), f"logical reference lacks path: {ref}")
    artifact_id, version = ref_pair(ref)
    return artifact_id, version, path


def refs(value: Any, label: str) -> list[dict[str, Any]]:
    require(isinstance(value, list), f"{label}: expected logical-reference list")
    require(all(isinstance(item, dict) for item in value), f"{label}: invalid reference")
    return value


def h2_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (.+?)\s*$", text, re.MULTILINE))
    return {
        match.group(1): text[
            match.end() : matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        ]
        for index, match in enumerate(matches)
    }


def score_value(value: Any) -> float:
    if isinstance(value, dict):
        value = value.get("score")
    require(isinstance(value, (int, float)), f"invalid evaluation score: {value}")
    return float(value)


def evaluation_scores(path: Path, metadata: dict[str, Any]) -> dict[str, float]:
    dimensions = ("Novelty", "Feasibility", "Impact", "Relevance", "Clarity", "Completion")
    structured = metadata.get("dimension_scores")
    if isinstance(structured, dict):
        result = {
            dimension: score_value(structured[dimension])
            for dimension in dimensions
            if dimension in structured
        }
    else:
        result = {
            match.group(1): float(match.group(2))
            for match in re.finditer(
                r"^\|\s*(Novelty|Feasibility|Impact|Relevance|Clarity|Completion)\s*"
                r"\|\s*([1-5](?:\.\d+)?)\s*\|",
                markdown_body(path),
                re.MULTILINE,
            )
        }
    require(set(result) == set(dimensions), f"incomplete evaluation scores: {path}")
    return result


def evaluation_decision(path: Path, metadata: dict[str, Any]) -> str:
    decision = metadata.get("decision")
    if isinstance(decision, str) and decision:
        return decision
    match = re.search(r"\*\*Decision:\*\*\s*`([^`]+)`", markdown_body(path))
    require(match is not None, f"missing evaluation decision: {path}")
    return match.group(1)


def require_fresh_review(metadata: dict[str, Any], label: str) -> None:
    require(metadata.get("isolation_mode") == "fresh_subagent", f"{label}: not fresh")
    require(metadata.get("prior_scores_visible") is False, f"{label}: prior scores visible")
    require(
        metadata.get("source_edits_performed") is False,
        f"{label}: reviewer edited source",
    )


def validate_baseline(
    narrative_validator: Any,
    language_validator: Any,
) -> None:
    dossier = read_text(BASELINE_DOSSIER)
    summary_line = next(
        line for line in dossier.splitlines() if "One-sentence complete-Idea summary" in line
    )
    summary = summary_line.partition("summary:** ")[2]
    require(len(summary) == 303, "baseline summary must remain the 303-character fixture")
    require(dossier.count("门") == 65, "baseline gate-term count")
    require(dossier.count("观测投影") == 8, "baseline observation-projection count")
    require(dossier.count("投影可观测") == 12, "baseline projection-observable count")

    assessment_path = BASELINE_CURRENT / "narrative-assessment-r079.md"
    plan_path = BASELINE_CURRENT / "narrative-repair-plan-r079.yaml"
    assessment = frontmatter(assessment_path)
    plan = yaml_file(plan_path)
    findings = narrative_validator.validate_assessment(assessment)
    narrative_validator.validate_plan(plan, findings)
    require_fresh_review(assessment, "baseline narrative assessment")
    require(assessment.get("decision") == "major_narrative_revision", "baseline narrative")
    major = [item for item in assessment.get("findings", []) if item.get("severity") == "major"]
    require(
        {
            "reader_reasoning_chain",
            "progressive_disclosure_and_reader_baseline",
            "conditional_extension_prominence",
            "caveat_saturation_and_repetition",
        }
        <= {item.get("category") for item in major},
        "baseline narrative major-finding coverage",
    )
    assessment_text = read_text(assessment_path)
    for signal in ("Gap", "Significance", "提前使用", "回读", "限制", "重复"):
        require(signal in assessment_text, f"baseline narrative missed {signal}")
    major_ids = {str(item["finding_id"]) for item in major}
    addressed = {
        str(finding_id)
        for action in plan.get("actions", [])
        for finding_id in action.get("addresses_findings", [])
    }
    require(major_ids <= addressed, "baseline repair plan does not cover every major finding")
    require(plan.get("actions"), "baseline repair plan has no executable actions")
    require(
        any(action.get("operation") in {"split", "consolidate"} for action in plan["actions"]),
        "baseline repair plan lacks structural operations",
    )

    language_path = BASELINE_CURRENT / "language-assessment-r105.md"
    language = frontmatter(language_path)
    language_validator.validate_report(language)
    require_fresh_review(language, "baseline language assessment")
    require(language.get("decision") == "major_language_revision", "baseline language")
    require(
        BASELINE_DOSSIER.relative_to(REPO).as_posix() in language.get("files_read", []),
        "baseline language assessment did not read v003",
    )
    coverage = language.get("coverage_receipt", {})
    require(
        set(coverage)
        == {"reader_entry", "core_scientific_role", "terminology_concordance", "local_language"}
        and all(item.get("status") == "completed" for item in coverage.values()),
        "baseline language four-pass coverage",
    )


def validate_simple_and_terminology(narrative_validator: Any) -> None:
    assessment_path = FIXTURE / "simple-study" / "outputs" / "narrative-assessment-r001.md"
    plan_path = FIXTURE / "simple-study" / "outputs" / "narrative-repair-plan-r001.yaml"
    assessment = frontmatter(assessment_path)
    plan = yaml_file(plan_path)
    findings = narrative_validator.validate_assessment(assessment)
    narrative_validator.validate_plan(plan, findings)
    require(assessment.get("decision") == "narrative_ready", "simple study false positive")
    require(assessment.get("findings") == [], "simple study has narrative findings")
    require(
        plan.get("decision") == "narrative_ready" and plan.get("actions") == [],
        "simple study repair plan",
    )

    result_path = FIXTURE / "terminology" / "output" / "language-terminology-results-r001.yaml"
    results = yaml_file(result_path).get("results", [])
    require(isinstance(results, list), "terminology results are not a list")
    actual = {
        item["case_id"]: (item["decision"], item["term_status"])
        for item in results
    }
    expected = {
        "TERM-FWD-001": ("pass", "domain_standard"),
        "TERM-FWD-002": ("repair", "nonstandard_or_misleading"),
        "TERM-FWD-003": ("repair", "cross_disciplinary_standard"),
        "TERM-FWD-004": ("repair", "nonstandard_or_misleading"),
        "TERM-FWD-005": ("pass", "necessary_coined_term"),
        "TERM-FWD-006": ("verification_required", "unverified_or_disputed"),
    }
    require(actual == expected, f"six terminology outcomes differ: {actual}")


def validate_v057(
    linter: Any,
    narrative_validator: Any,
    language_validator: Any,
    writer_validator: Any,
) -> None:
    final_text = read_text(FINAL_DOSSIER)
    final_meta = frontmatter(FINAL_DOSSIER)
    require(not linter.lint_text(final_text, "0.10.0"), "v057 dossier lint")
    require(final_meta.get("version_id") == "v057", "final dossier version")
    require(final_meta.get("frozen") is True, "v057 is not frozen")
    require(final_meta.get("change_type") == "editorial_repair", "v057 change type")
    require(len(re.findall(r"^## ", final_text, re.MULTILINE)) == 15, "v057 H2 count")
    sections = h2_sections(final_text)
    reasoning = sections.get("Background, current state, gap, significance, and rationale", "")
    require(
        re.findall(
            r"^### (Background|Current state|Gap|Significance|Rationale)\s*$",
            reasoning,
            re.MULTILINE,
        )
        == ["Background", "Current state", "Gap", "Significance", "Rationale"],
        "v057 five-part reader reasoning chain",
    )

    previous_dossier = FINAL_PREVIOUS / "idea-dossier-v056.md"
    register_path = FINAL_PREVIOUS / "protected-content-register-v008.yaml"
    narrative_path = FINAL_PREVIOUS / "narrative-assessment-r129.md"
    narrative_plan_path = FINAL_PREVIOUS / "narrative-repair-plan-r129.yaml"
    language_path = FINAL_PREVIOUS / "language-assessment-r129.md"
    brief_path = FINAL_PREVIOUS / "editorial-repair-writer-brief-r130.yaml"
    previous_meta = frontmatter(previous_dossier)
    register = yaml_file(register_path)
    narrative = frontmatter(narrative_path)
    narrative_plan = yaml_file(narrative_plan_path)
    language = frontmatter(language_path)
    brief = yaml_file(brief_path)

    narrative_findings = narrative_validator.validate_assessment(narrative)
    narrative_validator.validate_plan(narrative_plan, narrative_findings)
    language_validator.validate_report(language)
    narrative_validator.validate_register(register)
    writer_validator.validate_source_coverage(
        brief,
        narrative,
        narrative_plan,
        language,
        narrative_assessment_path=narrative_path,
        narrative_plan_path=narrative_plan_path,
        language_assessment_path=language_path,
        brief_path=brief_path,
    )
    writer_validator.validate_register_binding(brief, register, register_path)

    source_findings = [*narrative.get("findings", []), *language.get("findings", [])]
    major_ids = {
        str(item["finding_id"])
        for item in source_findings
        if item.get("severity") in BLOCKING_SEVERITIES
    }
    included_ids = set(brief.get("included_repair_item_ids", []))
    nonblocking_ids = {
        str(item["finding_id"])
        for item in source_findings
        if item.get("severity") not in BLOCKING_SEVERITIES
    }
    omitted_ids = {
        str(item["finding_id"])
        for item in brief.get("omitted_reported_nonblocking_findings", [])
    }
    require(len(major_ids) == 2, "r130 source does not contain exactly two major repairs")
    require(included_ids == major_ids, "r130 does not include exactly the two major repairs")
    require(not included_ids & nonblocking_ids, "r130 includes a nonblocking finding")
    require(nonblocking_ids <= omitted_ids, "r130 does not visibly omit every nonblocking finding")

    protected_items = register.get("protected_items", [])
    protected_ids = {str(item["protected_id"]) for item in protected_items}
    require(len(protected_items) == len(protected_ids) == 64, "v008 register is not 64/64")
    anchor = register.get("identity_anchor")
    require(isinstance(anchor, dict) and set(anchor) == IDENTITY_ANCHOR_FIELDS, "identity anchor")
    require(previous_meta.get("identity_anchor") == anchor, "v056 identity-anchor mismatch")
    require(final_meta.get("identity_anchor") == anchor, "v057 identity drift")

    final_based_on = {ref_pair(item) for item in refs(final_meta.get("based_on"), "v057 based_on")}
    require(
        final_based_on
        == {
            (previous_meta["artifact_id"], previous_meta["version_id"]),
            (brief["brief_id"], brief["round_id"]),
            (register["register_id"], register["register_version"]),
        },
        "v057 repair lineage",
    )

    delta_meta = frontmatter(FINAL_DELTA)
    delta_text = read_text(FINAL_DELTA)
    delta_pairs = {ref_pair(item) for item in refs(delta_meta.get("based_on"), "v057 delta")}
    require(
        {
            (previous_meta["artifact_id"], previous_meta["version_id"]),
            (final_meta["artifact_id"], final_meta["version_id"]),
            (brief["brief_id"], brief["round_id"]),
            (register["register_id"], register["register_version"]),
        }
        <= delta_pairs,
        "v056-to-v057 delta lineage",
    )
    for repair_id in included_ids:
        require(repair_id in delta_text, f"delta lacks included repair {repair_id}")
    for protected_id in protected_ids:
        require(protected_id in delta_text, f"delta lacks protected item {protected_id}")

    preservation = frontmatter(FINAL_PRESERVATION)
    narrative_validator.validate_preservation(preservation, register, register_path)
    checks = preservation.get("protected_item_checks", [])
    require(preservation.get("decision") == "scientific_content_preserved", "r131 decision")
    require(
        {str(item.get("protected_id")) for item in checks} == protected_ids
        and len(checks) == 64
        and all(item.get("semantic_status") == "preserved" for item in checks),
        "r131 is not a preserved 64/64 review",
    )

    final_narrative = frontmatter(FINAL_NARRATIVE)
    final_plan = yaml_file(FINAL_NARRATIVE_PLAN)
    final_findings = narrative_validator.validate_assessment(final_narrative)
    narrative_validator.validate_plan(final_plan, final_findings)
    require(
        final_narrative.get("decision") == "narrative_ready"
        and final_narrative.get("findings") == []
        and final_plan.get("actions") == [],
        "r132 narrative readiness",
    )
    final_language = frontmatter(FINAL_LANGUAGE)
    language_validator.validate_report(final_language)
    require(
        final_language.get("decision")
        not in {"major_language_revision", "needs_professional_editing"},
        "r132 language decision is blocking",
    )
    require(
        not any(
            item.get("severity") in BLOCKING_SEVERITIES
            for item in final_language.get("findings", [])
        ),
        "r132 contains a blocking language finding",
    )


def validate_v057_evaluation() -> None:
    old_meta = frontmatter(OLD_EVALUATION)
    final_meta = frontmatter(FINAL_EVALUATION)
    baseline_path = BASELINE_DOSSIER.relative_to(REPO).as_posix()
    final_path = FINAL_DOSSIER.relative_to(REPO).as_posix()
    require(old_meta.get("files_read") == [baseline_path], "v003 evaluator input isolation")
    require(old_meta.get("input_versions") == ["v003"], "v003 evaluator version")
    require(final_meta.get("files_read") == [final_path], "v057 evaluator input isolation")
    require(final_meta.get("input_artifact_ids") == ["idea-dossier-I01-001-v057"], "v057 evaluator artifact")
    require(final_meta.get("input_versions") == ["v057"], "v057 evaluator version")
    require(
        final_meta.get("reviewed_dossier_ref")
        == {
            "artifact_id": "idea-dossier-I01-001-v057",
            "version": "v057",
            "path": final_path,
        },
        "v057 evaluator reviewed-dossier binding",
    )
    for label, metadata in (("v003 evaluator", old_meta), ("v057 evaluator", final_meta)):
        require_fresh_review(metadata, label)
        require(metadata.get("dossier_only_input_confirmed") is True, f"{label}: not dossier-only")
        require(metadata.get("prior_versions_visible") is False, f"{label}: prior version visible")
        require(metadata.get("revision_delta_visible") is False, f"{label}: delta visible")

    old_scores = evaluation_scores(OLD_EVALUATION, old_meta)
    final_scores = evaluation_scores(FINAL_EVALUATION, final_meta)
    require(
        final_scores
        == {
            "Novelty": 4.0,
            "Feasibility": 3.0,
            "Impact": 4.0,
            "Relevance": 4.0,
            "Clarity": 4.0,
            "Completion": 4.0,
        },
        f"unexpected v057 blind scores: {final_scores}",
    )
    require(final_scores["Clarity"] >= old_scores["Clarity"], "editorial repair reduced clarity")
    for dimension in ("Novelty", "Feasibility", "Impact"):
        require(
            final_scores[dimension] <= old_scores[dimension],
            f"editorial-only repair improved {dimension}",
        )
    decision = evaluation_decision(FINAL_EVALUATION, final_meta)
    require(decision == "revise_then_promote", f"unexpected v057 decision: {decision}")
    require(decision != "promote", "editorial-only repair auto-promoted the Idea")
    require(
        final_meta.get("evaluation_frozen_before_journal_search") is True
        and final_meta.get("evaluation_changed_after_journal_search") is False,
        "v057 evaluation was not frozen before journal matching",
    )


def no_blocking_findings(metadata: dict[str, Any], label: str) -> None:
    require(
        not any(
            item.get("severity") in BLOCKING_SEVERITIES
            for item in metadata.get("findings", [])
        ),
        f"{label}: blocking finding remains",
    )


def validate_new_workflow(
    narrative_validator: Any,
    language_validator: Any,
) -> None:
    prompt = NEW_FIXTURE / "00_input" / "user-idea-v001.md"
    context = NEW_FIXTURE / "01_context" / "research-context-brief-v001.md"
    evidence = NEW_FIXTURE / "02_evidence" / "evidence-map-v001.md"
    opportunity = NEW_FIXTURE / "02_evidence" / "opportunity-map-v001.md"
    for path in (prompt, context, evidence, opportunity):
        read_text(path)

    dossier_dir = NEW_FIXTURE / "03_ideas" / "nodes" / "I01-001" / "dossiers"
    dossiers = {
        version: frontmatter(dossier_dir / f"idea-dossier-{version}.md")
        for version in ("v001", "v002", "v003", "v004", "v005", "v006")
    }
    for version, metadata in dossiers.items():
        require(metadata.get("version_id") == version, f"new workflow {version} identity")
        require(metadata.get("frozen") is True, f"new workflow {version} not frozen")
    require(
        {ref_triple(item) for item in refs(dossiers["v001"].get("based_on"), "v001 based_on")}
        == {
            ("user-idea-v001", "v001", "00_input/user-idea-v001.md"),
            ("research-context-brief-v001", "v001", "01_context/research-context-brief-v001.md"),
            ("evidence-map-v001", "v001", "02_evidence/evidence-map-v001.md"),
            ("opportunity-map-v001", "v001", "02_evidence/opportunity-map-v001.md"),
        },
        "new workflow initial prompt/context/evidence lineage",
    )
    versions = ("v001", "v002", "v003", "v004", "v005", "v006")
    for previous, current in zip(versions, versions[1:]):
        require(
            (dossiers[previous]["artifact_id"], previous)
            in {ref_pair(item) for item in refs(dossiers[current].get("based_on"), f"{current} based_on")},
            f"new workflow lineage break: {previous} to {current}",
        )

    review_dir = NEW_FIXTURE / "03_ideas" / "nodes" / "I01-001" / "reviews"
    preflight_r004 = frontmatter(review_dir / "preflight-r004.md")
    preflight_r005 = frontmatter(review_dir / "preflight-r005.md")
    require_fresh_review(preflight_r004, "new workflow preflight r004")
    require_fresh_review(preflight_r005, "new workflow preflight r005")
    require(
        preflight_r004.get("decision") == "revise_endpoint_or_metric"
        and preflight_r004.get("preflight_decision") == "revise_endpoint_or_metric",
        "r004 did not route a scientific repair",
    )
    require(
        dossiers["v005"].get("change_type") == "scientific_revision"
        and ("methodology-statistics-preflight-I01-001-r004", "r004")
        in {ref_pair(item) for item in dossiers["v005"]["based_on"]},
        "r004 scientific route did not produce v005",
    )
    require(preflight_r005.get("decision") == "pass", "r005 preflight did not pass")
    require(
        dossiers["v006"].get("change_type") == "editorial_repair"
        and dossiers["v006"].get("identity_anchor") == dossiers["v005"].get("identity_anchor"),
        "v006 editorial repair changed scientific identity",
    )

    register = yaml_file(NEW_FIXTURE / "05_state" / "protected-content-register-v002.yaml")
    narrative_validator.validate_register(register)
    preservation = frontmatter(review_dir / "content-preservation-r007.md")
    require_fresh_review(preservation, "new workflow preservation r007")
    no_blocking_findings(preservation, "new workflow preservation r007")
    protected_ids = {str(item["protected_id"]) for item in register.get("protected_items", [])}
    preservation_checks = preservation.get("protected_item_checks", [])
    require(
        preservation.get("decision") == "scientific_content_preserved"
        and {str(item.get("protected_id")) for item in preservation_checks} == protected_ids
        and all(item.get("semantic_status") == "preserved" for item in preservation_checks),
        "new workflow r007 preservation coverage",
    )

    narrative_path = review_dir / "narrative-assessment-r007.md"
    narrative_plan_path = review_dir / "narrative-repair-plan-r007.yaml"
    narrative = frontmatter(narrative_path)
    narrative_plan = yaml_file(narrative_plan_path)
    narrative_findings = narrative_validator.validate_assessment(narrative)
    narrative_validator.validate_plan(narrative_plan, narrative_findings)
    require_fresh_review(narrative, "new workflow narrative r007")
    no_blocking_findings(narrative, "new workflow narrative r007")
    require(narrative.get("decision") != "major_narrative_revision", "r007 narrative major")

    language = frontmatter(review_dir / "language-assessment-r007.md")
    language_validator.validate_report(language)
    require_fresh_review(language, "new workflow language r007")
    no_blocking_findings(language, "new workflow language r007")
    require(
        language.get("decision") not in {"major_language_revision", "needs_professional_editing"},
        "r007 language major",
    )

    evaluation_path = review_dir / "evaluation-r008.md"
    evaluation = frontmatter(evaluation_path)
    workflow_prefix = NEW_FIXTURE.relative_to(REPO).as_posix()
    full_dossier_path = f"{workflow_prefix}/03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md"
    require_fresh_review(evaluation, "new workflow evaluator r008")
    require(evaluation.get("files_read") == [full_dossier_path], "r008 evaluator input isolation")
    require(evaluation.get("input_artifact_ids") == ["idea-dossier-I01-001-v006"], "r008 input artifact")
    require(evaluation.get("input_versions") == ["v006"], "r008 input version")
    require(evaluation.get("dossier_only_input_confirmed") is True, "r008 not dossier-only")
    require(evaluation.get("prior_versions_visible") is False, "r008 prior version visible")
    require(evaluation.get("revision_delta_visible") is False, "r008 delta visible")
    require(
        evaluation_scores(evaluation_path, evaluation)
        == {
            "Novelty": 4.0,
            "Feasibility": 3.0,
            "Impact": 4.0,
            "Relevance": 4.0,
            "Clarity": 4.0,
            "Completion": 4.0,
        },
        "r008 frozen scores",
    )
    require(evaluation_decision(evaluation_path, evaluation) == "revise_then_promote", "r008 decision")
    require(
        evaluation.get("evaluation_frozen_before_journal_search") is True
        and evaluation.get("evaluation_changed_after_journal_search") is False,
        "r008 evaluation/journal ordering",
    )

    candidate_path = review_dir / "candidate-journal-match-r008.yaml"
    candidate = yaml_file(candidate_path)
    embedded = evaluation.get("journal_matching", {}).get("candidate_brief")
    require(isinstance(embedded, dict), "r008 embedded candidate brief")
    materialization_fields = {
        "artifact_id",
        "version",
        "workflow_id",
        "round_id",
        "materialized_by_skill",
        "frozen",
    }
    require(
        set(candidate) - set(embedded) == materialization_fields,
        "candidate brief has non-materialization fields",
    )
    require(
        {key: value for key, value in candidate.items() if key not in materialization_fields}
        == embedded,
        "candidate brief is not an exact materialization of evaluator payload",
    )
    for key in (
        "evaluation_fields_included",
        "scoring_present",
        "ranking_present",
        "publication_probability_present",
    ):
        require(candidate.get(key) is False, f"candidate brief exposes {key}")

    medical = frontmatter(review_dir / "medical-journal-review-r008.md")
    full_candidate_path = f"{workflow_prefix}/03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml"
    require(
        medical.get("files_read") == [full_dossier_path, full_candidate_path],
        "medical reviewer did not use exactly two project files",
    )
    require(
        medical.get("isolation_mode") == "fresh_subagent"
        and medical.get("evaluator_report_visible") is False
        and medical.get("evaluator_scores_visible") is False
        and medical.get("source_edits_performed") is False,
        "medical reviewer isolation",
    )
    require(medical.get("decision") == "journal_candidates_confirmed", "medical review decision")
    require(
        medical.get("candidate_brief_ref")
        == {
            "artifact_id": candidate["artifact_id"],
            "version": candidate["version"],
            "path": "03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml",
        },
        "medical reviewer candidate binding",
    )

    portfolio = frontmatter(NEW_FIXTURE / "04_portfolio" / "research-idea-portfolio-v001.md")
    state = yaml_file(NEW_FIXTURE / "05_state" / "workflow-state.yaml")
    require(portfolio.get("status") == "revision_required", "portfolio status")
    require(state.get("workflow_status") == "revision_required", "workflow state status")
    require(
        state.get("current_artifact_version") == "v006"
        and state.get("latest_evaluated_version") == "v006",
        "workflow state dossier pointers",
    )


def flatten_artifact_refs(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        if "artifact_id" in value and "path" in value and (
            "version" in value or "version_id" in value
        ):
            return [value]
        flattened: list[dict[str, Any]] = []
        for child in value.values():
            flattened.extend(flatten_artifact_refs(child))
        return flattened
    if isinstance(value, list):
        flattened = []
        for child in value:
            flattened.extend(flatten_artifact_refs(child))
        return flattened
    return []


def validate_artifact_completeness() -> None:
    index = frontmatter(NEW_FIXTURE / "05_state" / "artifact-index.md")
    state = yaml_file(NEW_FIXTURE / "05_state" / "workflow-state.yaml")
    manifest = frontmatter(NEW_FIXTURE / "05_state" / "round-001-manifest.md")
    index_entries = refs(index.get("artifacts"), "artifact index")
    state_entries = flatten_artifact_refs(state.get("artifacts"))
    manifest_entries = flatten_artifact_refs(manifest.get("artifacts"))
    actual_paths = {
        path.relative_to(NEW_FIXTURE).as_posix()
        for path in NEW_FIXTURE.rglob("*")
        if path.is_file()
    }
    require(len(actual_paths) == 56, "new workflow does not contain exactly 56 files")
    require(index.get("expected_standard_artifact_count") == 56, "artifact-index expected count")

    registry_sets: list[set[tuple[str, str, str]]] = []
    for label, entries in (
        ("artifact-index", index_entries),
        ("workflow-state", state_entries),
        ("round manifest", manifest_entries),
    ):
        triples = [ref_triple(item) for item in entries]
        pairs = [ref_pair(item) for item in entries]
        paths = [item[2] for item in triples]
        require(len(entries) == 56, f"{label} does not cover 56/56 files")
        require(len(set(pairs)) == 56, f"{label} has duplicate logical pairs")
        require(len(set(paths)) == 56, f"{label} has duplicate paths")
        require(set(paths) == actual_paths, f"{label} does not match actual files")
        registry_sets.append(set(triples))
    require(
        registry_sets[0] == registry_sets[1] == registry_sets[2],
        "artifact registries disagree",
    )

    catalog = {ref_pair(item): ref_triple(item) for item in index_entries}

    def require_resolved(reference: dict[str, Any], label: str) -> None:
        pair = ref_pair(reference)
        require(pair in catalog, f"{label}: unresolved logical reference {pair}")
        path = reference.get("path")
        if path is not None:
            require(ref_triple(reference) == catalog[pair], f"{label}: path mismatch for {pair}")

    for entry in index_entries:
        based_on = entry.get("based_on", [])
        require(isinstance(based_on, list), f"artifact-index based_on: {ref_pair(entry)}")
        for reference in based_on:
            require(isinstance(reference, dict), "artifact-index based_on reference")
            require_resolved(reference, f"artifact-index {ref_pair(entry)} based_on")
    for label, document in (("workflow-state", state), ("round manifest", manifest)):
        for reference in refs(document.get("based_on"), f"{label} based_on"):
            require_resolved(reference, f"{label} based_on")

    current_pointers = state.get("current_pointers")
    require(isinstance(current_pointers, dict), "workflow-state current pointers")
    for name, reference in current_pointers.items():
        require(isinstance(reference, dict), f"current pointer {name}")
        require_resolved(reference, f"current pointer {name}")
    require(
        ref_pair(current_pointers["current_dossier"])
        == ("idea-dossier-I01-001-v006", "v006")
        and ref_pair(current_pointers["qualifying_evaluation"])
        == ("evaluation-I01-001-r008", "r008")
        and ref_pair(current_pointers["candidate_journal_match"])
        == ("candidate-journal-match-I01-001-r008", "r008")
        and ref_pair(current_pointers["medical_journal_review"])
        == ("medical-journal-review-I01-001-r008", "r008")
        and ref_pair(current_pointers["portfolio"])
        == ("research-idea-portfolio-v001", "v001"),
        "workflow-state current artifact pointers",
    )


def validate_no_persisted_digests() -> None:
    forbidden_key = re.compile(r"(?:^|_)(?:sha(?:256)?|hash|digest)(?:_|$)", re.IGNORECASE)
    hex_digest = re.compile(r"\b[0-9a-f]{64}\b", re.IGNORECASE)

    def check_payload(value: Any, source: Path) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                require(not forbidden_key.search(str(key)), f"digest field: {source}:{key}")
                check_payload(child, source)
        elif isinstance(value, list):
            for child in value:
                check_payload(child, source)

    for tree in (FIXTURE, NEW_FIXTURE):
        for path in tree.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml"}:
                continue
            raw = read_text(path)
            require(not hex_digest.search(raw), f"persisted 64-hex digest: {path}")
            if path.suffix.lower() in {".yaml", ".yml"}:
                check_payload(yaml.safe_load(raw), path)
            elif raw.startswith("---"):
                check_payload(frontmatter(path), path)


def validate_record_only_policy() -> None:
    report = read_text(ERROR_REPORT)
    contract = read_text(READINESS_CONTRACT)
    contract_normalized = re.sub(r"\s+", " ", contract)
    report_paths = list(FIXTURE.rglob("error-localization-report*.md"))
    require(report_paths == [ERROR_REPORT], "low-impact observations are not in one maintained report")
    require(
        "| 插件版本 | 问题现象 | 推测诊断 | 拟议的解决方案 |" in report,
        "unified report lacks the four required fields",
    )
    require(
        "record_only_owner_prioritization_pending" in report
        and "只记录，不为其启动新的修订、复现或专项测试" in report,
        "unified report does not state the record-only policy",
    )
    for phrase in (
        ERROR_REPORT.relative_to(REPO).as_posix(),
        "plugin version",
        "observed symptom",
        "suspected diagnosis",
        "Do not create a case-specific minor-issue report",
        "regression-test requirement",
    ):
        require(
            phrase in contract_normalized,
            f"readiness contract lacks record-only rule: {phrase}",
        )
    require(
        "proposed solution" in contract_normalized,
        "readiness contract lacks the proposed-solution field",
    )


def main() -> int:
    linter = load_linter()
    narrative_validator = load_narrative_validator()
    language_validator = load_language_validator()
    writer_validator = load_writer_brief_validator()
    validate_baseline(narrative_validator, language_validator)
    validate_simple_and_terminology(narrative_validator)
    validate_v057(linter, narrative_validator, language_validator, writer_validator)
    validate_v057_evaluation()
    validate_new_workflow(narrative_validator, language_validator)
    validate_artifact_completeness()
    validate_no_persisted_digests()
    validate_record_only_policy()
    print("OpenAI Idea narrative forward tests passed")
    print("v003 baseline, v057 editorial repair, and the sepsis workflow are internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
