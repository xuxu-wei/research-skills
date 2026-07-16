#!/usr/bin/env python3
"""Validate personal-owner entry modes with deterministic contract fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
REGISTRY = PLUGIN / "workflow-registry.yaml"
FIXTURE = REPO / "tests" / "openai_phase7" / "mode-cases.yaml"
ROUTING = REPO / "tests" / "openai_phase7" / "research-polisher-routing-boundaries.yaml"
REPORT = PLUGIN / "reports" / "phase7-mode-results.json"

EXPECTED_ENTRIES = {
    "academic-deep-search",
    "article-orchestrator",
    "perspective-orchestrator",
    "proposal-orchestrator",
    "research-idea-orchestrator",
    "research-opportunity-mapper",
    "research-polisher-orchestrator",
}
EXPECTED_IMPLICIT = EXPECTED_ENTRIES - {"research-polisher-orchestrator"}
EXPECTED_WORKFLOWS = {"idea", "proposal", "article", "perspective", "research_polisher"}
READY_STATES = {"human_signoff_required", "human_strategy_selection_required"}
MUTATION_ERROR_CODES = {
    "gate_bypass": "missing_entry_gate_receipt",
    "stale_input": "stale_gate_input",
    "invalid_lineage": "invalid_lineage",
}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def ready_state_for(workflow: str, machine: dict[str, Any]) -> str:
    if workflow == "research_polisher":
        return str(machine.get("final_state", "human_strategy_selection_required"))
    return "human_signoff_required"


def build_promotion_candidate(
    case_id: str,
    workflow: str,
    mode: str,
    gates: list[str],
    requested_state: str,
) -> dict[str, Any]:
    digest = hashlib.sha256(f"{case_id}:current:v002".encode()).hexdigest()
    lineage = {
        "artifact_id": f"{case_id}-primary",
        "version_id": "v002",
        "workflow_id": f"phase7-{case_id}",
    }
    return {
        "workflow": workflow,
        "entry_mode": mode,
        "requested_state": requested_state,
        "entry_gate_receipts": {gate: {"passed": True} for gate in gates},
        "current_artifact": {
            "content_digest": digest,
            "lineage": lineage,
        },
        "qualifying_review": {
            "input_digest": digest,
            "input_lineage": copy.deepcopy(lineage),
        },
    }


def evaluate_promotion(
    machine: dict[str, Any],
    mode: str,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """Apply the registry-derived gates used before a ready-state promotion."""
    failed_checks: list[str] = []
    required_gates = list(machine.get("entry_gates", {}).get(mode, []))
    receipts = candidate.get("entry_gate_receipts", {})
    if not isinstance(receipts, dict) or any(
        gate not in receipts or receipts[gate].get("passed") is not True
        for gate in required_gates
    ):
        failed_checks.append("missing_entry_gate_receipt")

    current = candidate.get("current_artifact", {})
    review = candidate.get("qualifying_review", {})
    if not current.get("content_digest") or review.get("input_digest") != current.get("content_digest"):
        failed_checks.append("stale_gate_input")

    current_lineage = current.get("lineage")
    review_lineage = review.get("input_lineage")
    lineage_fields = {"artifact_id", "version_id", "workflow_id"}
    if (
        not isinstance(current_lineage, dict)
        or not isinstance(review_lineage, dict)
        or not lineage_fields <= set(current_lineage)
        or not lineage_fields <= set(review_lineage)
        or any(current_lineage[field] != review_lineage[field] for field in lineage_fields)
    ):
        failed_checks.append("invalid_lineage")

    requested_state = str(candidate.get("requested_state", ""))
    ready_requested = requested_state in READY_STATES
    if ready_requested and mode in set(machine.get("non_ready_modes", [])):
        failed_checks.append("mode_is_non_ready")

    if failed_checks:
        observed_state = "promotion_blocked" if ready_requested else "transition_blocked"
        decision = "rejected"
    else:
        observed_state = requested_state
        decision = "promoted" if ready_requested else "completed_non_ready"
    return {
        "decision": decision,
        "requested_state": requested_state,
        "observed_state": observed_state,
        "ready_state_reached": observed_state in READY_STATES,
        "failed_checks": failed_checks,
    }


def apply_negative_mutation(candidate: dict[str, Any], gates: list[str], mutation: str) -> None:
    if mutation == "gate_bypass":
        candidate["entry_gate_receipts"].pop(gates[0])
    elif mutation == "stale_input":
        candidate["qualifying_review"]["input_digest"] = hashlib.sha256(
            b"prior-artifact-version"
        ).hexdigest()
    elif mutation == "invalid_lineage":
        candidate["qualifying_review"]["input_lineage"]["version_id"] = "v001"
    else:
        raise ValueError(f"unknown negative mutation: {mutation}")


def count_false_ready(results: list[dict[str, Any]]) -> int:
    return sum(item.get("ready_state_reached") is True for item in results)


def build_report() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = load_yaml(REGISTRY)
    fixture = load_yaml(FIXTURE)
    routing = load_yaml(ROUTING)
    version = str(manifest.get("version", ""))

    require(registry.get("plugin_version") == version, "manifest/registry version mismatch", errors)
    skills = registry.get("skills", [])
    require(isinstance(skills, list) and len(skills) == 49, "expected 49 registered skills", errors)
    reviewers = [item for item in skills if isinstance(item, dict) and item.get("requires_independent_subagent") is True]
    require(len(reviewers) == 20, "expected 20 independent reviewers", errors)

    policy = registry.get("public_entry_policy", {})
    declared = set(policy.get("declared_entries", [])) if isinstance(policy, dict) else set()
    implicit = set(policy.get("implicit_active_entries", [])) if isinstance(policy, dict) else set()
    explicit = policy.get("explicit_only_entries", {}) if isinstance(policy, dict) else {}
    require(declared == EXPECTED_ENTRIES, "declared entry inventory differs", errors)
    require(implicit == EXPECTED_IMPLICIT, "implicit entry inventory differs", errors)
    require(
        isinstance(explicit, dict)
        and explicit.get("research-polisher-orchestrator", {}).get("status") == "explicit_only_personal_routing_policy",
        "Research Polisher must remain explicit-only",
        errors,
    )

    execution = registry.get("review_execution", {})
    for field, expected in {
        "isolation_mode": "fresh_subagent",
        "inline_fallback": False,
        "prior_scores_visible_to_reviewer": False,
        "prior_versions_visible_to_reviewer": False,
        "revision_deltas_visible_to_reviewer": False,
        "source_artifacts_read_only": True,
    }.items():
        require(execution.get(field) == expected, f"review_execution.{field} is invalid", errors)

    machines = registry.get("workflow_state_machines", {})
    cases = fixture.get("cases", [])
    profiles = fixture.get("path_profiles", {})
    require(fixture.get("execution_kind") == "deterministic_replay", "fixture must be deterministic replay", errors)
    require(fixture.get("live_model_execution") is False, "fixture must not claim live execution", errors)
    require(isinstance(cases, list) and len(cases) == 17, "expected 17 entry-mode cases", errors)
    require(set(fixture.get("expected_workflows", [])) == EXPECTED_WORKFLOWS, "fixture workflow inventory differs", errors)

    registry_modes: set[tuple[str, str]] = set()
    if isinstance(machines, dict):
        for workflow, machine in machines.items():
            if workflow in EXPECTED_WORKFLOWS and isinstance(machine, dict):
                registry_modes.update((workflow, mode) for mode in machine.get("entry_modes", []))
    fixture_modes: set[tuple[str, str]] = set()
    positive_results: list[dict[str, Any]] = []
    negative_results: list[dict[str, Any]] = []
    for case in cases if isinstance(cases, list) else []:
        if not isinstance(case, dict):
            errors.append("malformed mode case")
            continue
        case_id = str(case.get("case_id", ""))
        workflow = str(case.get("workflow", ""))
        mode = str(case.get("entry_mode", ""))
        fixture_modes.add((workflow, mode))
        machine = machines.get(workflow, {}) if isinstance(machines, dict) else {}
        gates = machine.get("entry_gates", {}).get(mode, []) if isinstance(machine, dict) else []
        contracts = machine.get("scenario_entry_gate_contracts", {}).get(mode, {}) if isinstance(machine, dict) else {}
        profile = profiles.get(case.get("path_profile"), {}) if isinstance(profiles, dict) else {}
        transitions = profile.get("transitions", []) if isinstance(profile, dict) else []
        require(bool(case_id), "mode case lacks case_id", errors)
        require(bool(gates), f"{case_id}: entry gates missing", errors)
        require(set(gates) == set(contracts), f"{case_id}: entry gate contracts differ", errors)
        require(bool(transitions), f"{case_id}: transition profile missing", errors)
        require(profile.get("mode_scope_completed") is True, f"{case_id}: mode scope is incomplete", errors)
        if transitions:
            require(
                transitions[-1].get("to") == profile.get("expected_final_state"),
                f"{case_id}: final transition differs from expected state",
                errors,
            )
        expected_final_state = str(profile.get("expected_final_state", ""))
        positive_candidate = build_promotion_candidate(
            case_id=case_id,
            workflow=workflow,
            mode=mode,
            gates=list(gates),
            requested_state=expected_final_state,
        )
        positive_decision = evaluate_promotion(machine, mode, positive_candidate)
        require(
            positive_decision["observed_state"] == expected_final_state,
            f"{case_id}: valid fixture did not reach its expected state",
            errors,
        )
        positive_results.append(
            {
                "case_id": case_id,
                "workflow": workflow,
                "entry_mode": mode,
                "expected_final_state": expected_final_state,
                "observed_final_state": positive_decision["observed_state"],
                "promotion_decision": positive_decision["decision"],
                "status": (
                    "passed"
                    if positive_decision["observed_state"] == expected_final_state
                    else "failed"
                ),
            }
        )
        for mutation in ("gate_bypass", str(case.get("secondary_mutation", "stale_input"))):
            require(
                mutation in MUTATION_ERROR_CODES,
                f"{case_id}: unsupported negative mutation {mutation}",
                errors,
            )
            if mutation not in MUTATION_ERROR_CODES:
                continue
            negative_candidate = build_promotion_candidate(
                case_id=case_id,
                workflow=workflow,
                mode=mode,
                gates=list(gates),
                requested_state=ready_state_for(workflow, machine),
            )
            apply_negative_mutation(negative_candidate, list(gates), mutation)
            negative_decision = evaluate_promotion(machine, mode, negative_candidate)
            expected_failure = MUTATION_ERROR_CODES[mutation]
            rejected_as_expected = (
                negative_decision["ready_state_reached"] is False
                and expected_failure in negative_decision["failed_checks"]
            )
            require(
                rejected_as_expected,
                f"{case_id}: {mutation} was not rejected by the promotion decision",
                errors,
            )
            negative_results.append(
                {
                    "case_id": case_id,
                    "workflow": workflow,
                    "entry_mode": mode,
                    "mutation": mutation,
                    "requested_state": negative_decision["requested_state"],
                    "observed_state": negative_decision["observed_state"],
                    "ready_state_reached": negative_decision["ready_state_reached"],
                    "failed_checks": negative_decision["failed_checks"],
                    "status": "rejected_as_expected" if rejected_as_expected else "false_ready",
                }
            )

    require(fixture_modes == registry_modes, "fixture modes differ from registry modes", errors)

    routing_results: list[dict[str, Any]] = []
    routing_cases = routing.get("cases", [])
    require(isinstance(routing_cases, list) and len(routing_cases) == 7, "expected seven Research Polisher routing cases", errors)
    for case in routing_cases if isinstance(routing_cases, list) else []:
        if not isinstance(case, dict):
            errors.append("malformed Research Polisher routing case")
            continue
        selected = case.get("observed_route") == "research-polisher-orchestrator"
        require(selected is case.get("expected_selected"), f"{case.get('case_id')}: routing boundary failed", errors)
        require(case.get("observed_route") == case.get("expected_route"), f"{case.get('case_id')}: route differs", errors)
        routing_results.append({"case_id": case.get("case_id"), "status": "passed"})

    false_ready_count = count_false_ready(negative_results)
    detector_probe = {
        "mutation": "injected_false_ready_detector_probe",
        "ready_state_reached": True,
        "failed_checks": ["missing_entry_gate_receipt"],
    }
    detector_probe_count = count_false_ready([detector_probe])
    detector_self_test_passed = detector_probe_count == 1
    require(
        detector_self_test_passed,
        "false-ready detector failed to count an injected ready-state bypass",
        errors,
    )
    report = {
        "schema_version": 2,
        "plugin_version": version,
        "profile": "personal-owner",
        "execution_kind": "deterministic_replay",
        "live_runtime_evidence": False,
        "mode_results": positive_results,
        "negative_guard_results": negative_results,
        "false_ready_detector_self_test": {
            "injected_probe_count": 1,
            "detected_false_ready_count": detector_probe_count,
            "status": "passed" if detector_self_test_passed else "failed",
        },
        "research_polisher_routing_results": routing_results,
        "summary": {
            "installed_skill_count": len(skills),
            "declared_entry_count": len(declared),
            "implicit_entry_count": len(implicit),
            "independent_reviewer_count": len(reviewers),
            "declared_entry_modes": len(registry_modes),
            "positive_modes_passed": sum(item["status"] == "passed" for item in positive_results),
            "negative_guards_rejected": sum(
                item["status"] == "rejected_as_expected" for item in negative_results
            ),
            "runtime_contract_complete_workflows_verified": len(EXPECTED_WORKFLOWS),
            "false_ready_count": false_ready_count,
            "personal_status": "in_progress_owner_observation",
        },
        "errors": errors,
    }
    return report, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write-report", action="store_true")
    group.add_argument("--check-report", action="store_true")
    args = parser.parse_args()
    try:
        report, errors = build_report()
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"Phase 7 validation failed: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8", newline="\n")
    if args.check_report and (not REPORT.exists() or REPORT.read_text(encoding="utf-8") != rendered):
        print("Phase 7 report is missing or stale", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Phase 7 personal deterministic validation passed: 17/17 modes; 34 negative guards; false-ready 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
