#!/usr/bin/env python3
"""Validate the owner-operated personal acceptance profile.

This validator keeps deterministic repository checks separate from real task
observations. Pending owner observations are a valid report state; use
``--require-ready`` only when intentionally promoting the personal install.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SCHEMA = REPO / "tests" / "openai_personal" / "owner-observed-receipts.schema.yaml"
RECEIPTS = REPO / "tests" / "openai_personal" / "current-version-owner-observed-receipts.yaml"
REPORT = PLUGIN / "reports" / "personal-readiness.json"

EXPECTED_DECLARED = {
    "academic-deep-search",
    "article-orchestrator",
    "perspective-orchestrator",
    "proposal-orchestrator",
    "research-idea-orchestrator",
    "research-opportunity-mapper",
    "research-polisher-orchestrator",
}
EXPECTED_IMPLICIT = EXPECTED_DECLARED - {"research-polisher-orchestrator"}
EXPECTED_WORKFLOWS = {"idea", "proposal", "article", "perspective", "research_polisher"}
EXPECTED_WORKFLOW_SLOTS = {
    "personal-idea-happy": ("idea", "human_signoff_required"),
    "personal-proposal-happy": ("proposal", "human_signoff_required"),
    "personal-article-happy": ("article", "human_signoff_required"),
    "personal-perspective-happy": ("perspective", "human_signoff_required"),
    "personal-research-polisher-happy": (
        "research_polisher",
        "human_strategy_selection_required",
    ),
}
EXPECTED_CONTROL_SLOTS = {
    "personal-reviewer-unavailable-control": "independent_review_pending",
    "personal-fatal-finding-control": "blocked_without_ready_state",
}
EXPECTED_RETRIEVAL_SLOTS = {
    "personal-search-current": "source_grounded_current_answer",
    "personal-search-exact": "source_grounded_exact_answer",
    "personal-search-narrow-academic": "source_grounded_narrow_academic_answer",
    "personal-deep-research-inactive": (
        "deep_research_handoff_required_with_continuation_package"
    ),
    "personal-deep-research-complete": (
        "handoff_completion_mapper_return_and_single_edge_resume"
    ),
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def file_sha256(path: Path) -> str:
    """Hash tracked text canonically so Windows and Linux agree."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def deterministic_checks() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    schema = load_yaml(SCHEMA)
    if schema.get("$id") != "openai-personal-owner-observed-receipts/v1":
        errors.append("personal owner-observed receipt schema ID is invalid")
    manifest_path = PLUGIN / ".codex-plugin" / "plugin.json"
    registry_path = PLUGIN / "workflow-registry.yaml"
    manifest = load_json(manifest_path)
    registry = load_yaml(registry_path)
    plugin_version = str(manifest.get("version", ""))
    if registry.get("plugin_version") != plugin_version:
        errors.append("manifest and workflow registry versions differ")

    skills = registry.get("skills", [])
    if not isinstance(skills, list) or len(skills) != 49:
        errors.append("registry must contain exactly 49 skills")
        skills = []
    reviewer_count = sum(
        1 for item in skills if isinstance(item, dict) and item.get("requires_independent_subagent") is True
    )
    if reviewer_count != 20:
        errors.append(f"registry must contain 20 independent reviewers, found {reviewer_count}")

    policy = registry.get("public_entry_policy", {})
    declared = set(policy.get("declared_entries", [])) if isinstance(policy, dict) else set()
    implicit = set(policy.get("implicit_active_entries", [])) if isinstance(policy, dict) else set()
    if declared != EXPECTED_DECLARED:
        errors.append("declared entry set differs from the personal profile")
    if implicit != EXPECTED_IMPLICIT:
        errors.append("implicit entry set differs from the fixed personal profile")
    explicit_only = policy.get("explicit_only_entries", {}) if isinstance(policy, dict) else {}
    polisher = explicit_only.get("research-polisher-orchestrator", {}) if isinstance(explicit_only, dict) else {}
    if (
        not isinstance(polisher, dict)
        or polisher.get("status") != "explicit_only_personal_routing_policy"
        or polisher.get("change_authority") != "owner_only"
    ):
        errors.append("Research Polisher is not fixed to the owner-only explicit routing policy")

    edges = registry.get("workflow_edges", [])
    workflows = {
        item.get("workflow")
        for item in edges
        if isinstance(item, dict) and isinstance(item.get("workflow"), str)
    }
    if workflows != EXPECTED_WORKFLOWS:
        errors.append("registry workflow set differs from the five personal workflows")

    phase4 = load_json(PLUGIN / "reports" / "phase4-scenario-results.json")
    phase7 = load_json(PLUGIN / "reports" / "phase7-mode-results.json")
    phase8 = load_json(PLUGIN / "reports" / "phase8-corpus-results.json")
    for label, report in (("phase4", phase4), ("phase7", phase7), ("phase8", phase8)):
        if report.get("plugin_version") != plugin_version:
            errors.append(f"{label} report version differs from the plugin")

    p4 = phase4.get("summary", {})
    if p4.get("workflows_passed") != 5 or p4.get("negative_guards_rejected") != 63:
        errors.append("Phase 4 deterministic baseline must remain 5 workflows and 63 negatives")

    p7 = phase7.get("summary", {})
    if (
        p7.get("declared_entry_modes") != 17
        or p7.get("positive_modes_passed") != 17
        or p7.get("false_ready_count") != 0
        or p7.get("runtime_contract_complete_workflows_verified") != 5
    ):
        errors.append("Phase 7 deterministic baseline must remain 17/17 modes, five workflows, false-ready zero")

    corpus = phase8.get("corpus", {})
    metrics = corpus.get("metrics", {}) if isinstance(corpus, dict) else {}
    required_metrics = (
        "dissent_preservation_percent",
        "fatal_or_blocking_finding_recall_percent",
        "lineage_compliance_percent",
        "major_finding_recall_percent",
        "reviewer_edit_boundary_compliance_percent",
        "reviewer_isolation_compliance_percent",
    )
    if corpus.get("case_count") != 20 or metrics.get("false_ready_count") != 0:
        errors.append("Phase 8 corpus must remain 20 cases with false-ready zero")
    if any(metrics.get(name) != 100.0 for name in required_metrics):
        errors.append("Phase 8 personal quality metrics must remain at 100 percent")

    return (
        {
            "plugin_version": plugin_version,
            "manifest_sha256": file_sha256(manifest_path),
            "registry_sha256": file_sha256(registry_path),
            "receipt_schema_sha256": file_sha256(SCHEMA),
            "skill_count": len(skills),
            "independent_reviewer_count": reviewer_count,
            "declared_entry_count": len(declared),
            "implicit_entry_count": len(implicit),
            "workflow_count": len(workflows),
            "entry_mode_count": p7.get("declared_entry_modes"),
            "phase4_workflows_passed": p4.get("workflows_passed"),
            "phase4_negative_guards_rejected": p4.get("negative_guards_rejected"),
            "phase8_case_count": corpus.get("case_count"),
            "phase8_false_ready_count": metrics.get("false_ready_count"),
        },
        errors,
    )


def _validate_observed_binding(receipt: dict[str, Any], plugin_version: str) -> list[str]:
    errors: list[str] = []
    slot_id = receipt.get("slot_id", "<unknown>")
    binding = receipt.get("binding")
    if not isinstance(binding, dict):
        return [f"{slot_id}: binding is missing"]
    for field in ("task_id", "source_identity", "started_at", "completed_at"):
        if not isinstance(binding.get(field), str) or not binding[field].strip():
            errors.append(f"{slot_id}: observed binding lacks {field}")
    if binding.get("plugin_version") != plugin_version:
        errors.append(f"{slot_id}: observed plugin version differs from the collection")
    if binding.get("owner_confirmed") is not True:
        errors.append(f"{slot_id}: owner confirmation is missing")
    artifacts = binding.get("artifact_bindings")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{slot_id}: observed receipt has no artifact binding")
    else:
        for offset, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append(f"{slot_id}: artifact binding {offset} is malformed")
                continue
            for field in ("artifact_id", "version", "path"):
                if not isinstance(artifact.get(field), str) or not artifact[field].strip():
                    errors.append(f"{slot_id}: artifact binding {offset} lacks {field}")
            digest = artifact.get("sha256")
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                errors.append(f"{slot_id}: artifact binding {offset} has no valid SHA-256")
    if receipt.get("kind") == "workflow_happy":
        reviewers = binding.get("reviewer_instance_ids")
        if not isinstance(reviewers, list) or not reviewers:
            errors.append(f"{slot_id}: happy workflow has no reviewer instance ID")
    if receipt.get("kind") == "search":
        urls = binding.get("source_urls")
        if not isinstance(urls, list) or not urls or not all(
            isinstance(url, str) and url.startswith(("https://", "http://")) for url in urls
        ):
            errors.append(f"{slot_id}: Search observation has no valid source URL")
    return errors


def validate_receipts(receipts: dict[str, Any], plugin_version: str) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if receipts.get("schema_version") != 1:
        errors.append("personal receipt schema version must be 1")
    if receipts.get("profile") != "personal-owner":
        errors.append("personal receipt profile must be personal-owner")
    if receipts.get("evidence_level") != "owner_observed":
        errors.append("personal receipt evidence level must be owner_observed")
    if receipts.get("plugin_version") != plugin_version:
        errors.append("personal receipt version differs from the plugin")

    expected_groups: list[tuple[str, dict[str, Any]]] = [
        ("workflow_runs", EXPECTED_WORKFLOW_SLOTS),
        ("control_runs", EXPECTED_CONTROL_SLOTS),
        ("retrieval_runs", EXPECTED_RETRIEVAL_SLOTS),
    ]
    all_receipts: list[dict[str, Any]] = []
    for group_name, expected in expected_groups:
        values = receipts.get(group_name)
        if not isinstance(values, list):
            errors.append(f"{group_name} must be a list")
            continue
        indexed = {
            item.get("slot_id"): item
            for item in values
            if isinstance(item, dict) and isinstance(item.get("slot_id"), str)
        }
        if set(indexed) != set(expected):
            errors.append(f"{group_name} slot inventory differs from the personal contract")
        for slot_id, expectation in expected.items():
            item = indexed.get(slot_id)
            if not isinstance(item, dict):
                continue
            all_receipts.append(item)
            if group_name == "workflow_runs":
                workflow, outcome = expectation
                if item.get("workflow") != workflow:
                    errors.append(f"{slot_id}: workflow differs from the contract")
            else:
                outcome = expectation
            if item.get("expected_outcome") != outcome:
                errors.append(f"{slot_id}: expected outcome differs from the contract")

    distribution = receipts.get("distribution")
    if not isinstance(distribution, dict) or distribution.get("slot_id") != "personal-distribution-current":
        errors.append("current-version distribution slot is missing")
    else:
        all_receipts.insert(0, distribution)

    allowed_statuses = {"pending_owner_observation", "owner_observed"}
    observed_ids: list[str] = []
    pending_ids: list[str] = []
    for item in all_receipts:
        slot_id = str(item.get("slot_id"))
        status = item.get("status")
        if status not in allowed_statuses:
            errors.append(f"{slot_id}: invalid personal observation status")
            continue
        if status == "pending_owner_observation":
            pending_ids.append(slot_id)
            continue
        observed_ids.append(slot_id)
        if item.get("actual_outcome") != item.get("expected_outcome"):
            errors.append(f"{slot_id}: observed outcome does not match the accepted outcome")
        errors.extend(_validate_observed_binding(item, plugin_version))

    expected_total = 1 + len(EXPECTED_WORKFLOW_SLOTS) + len(EXPECTED_CONTROL_SLOTS) + len(EXPECTED_RETRIEVAL_SLOTS)
    if len(all_receipts) != expected_total:
        errors.append(f"personal receipt count must be {expected_total}")
    ready = len(observed_ids) == expected_total and not pending_ids and not errors
    return (
        {
            "expected_slot_count": expected_total,
            "owner_observed_slot_count": len(observed_ids),
            "pending_slot_count": len(pending_ids),
            "owner_observed_slots": sorted(observed_ids),
            "pending_slots": sorted(pending_ids),
            "status": "owner_observed_ready" if ready else "in_progress_owner_observation",
        },
        errors,
    )


def build_report(receipts_path: Path = RECEIPTS) -> tuple[dict[str, Any], list[str]]:
    deterministic, errors = deterministic_checks()
    receipts = load_yaml(receipts_path)
    observation, receipt_errors = validate_receipts(receipts, deterministic["plugin_version"])
    errors.extend(receipt_errors)
    deterministic_status = "deterministic_validated" if not errors else "deterministic_validation_failed"
    if deterministic_status != "deterministic_validated":
        observation["status"] = "in_progress_owner_observation"
    report = {
        "schema_version": 1,
        "profile": "personal-owner",
        "plugin_version": deterministic["plugin_version"],
        "deterministic_status": deterministic_status,
        "personal_status": observation["status"],
        "deterministic_baseline": deterministic,
        "owner_observation": observation,
        "deferred_profiles": {
            "preview_attested": "out_of_scope_nonblocking",
            "provider_verified": "out_of_scope_nonblocking",
        },
        "claims": {
            "owner_observed_is_external_attestation": False,
            "owner_observed_is_provider_verified": False,
            "automatic_external_submission": False,
        },
        "errors": errors,
    }
    return report, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipts", type=Path, default=RECEIPTS)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check-report", action="store_true")
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args(argv)

    try:
        report, errors = build_report(args.receipts)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"Personal readiness validation failed: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8")
    if args.check_report:
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != rendered:
            print("Personal readiness report is missing or stale", file=sys.stderr)
            return 1
    if errors:
        print("Personal readiness validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.require_ready and report["personal_status"] != "owner_observed_ready":
        print("Personal readiness remains in_progress_owner_observation", file=sys.stderr)
        return 1
    print(
        "Personal readiness validation passed: "
        f"{report['deterministic_status']}; {report['personal_status']}; "
        f"observed={report['owner_observation']['owner_observed_slot_count']}/"
        f"{report['owner_observation']['expected_slot_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
