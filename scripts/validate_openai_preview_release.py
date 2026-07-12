#!/usr/bin/env python3
"""Portable release validation for the OpenAI Preview plugin and marketplace."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from openai_release_utils import compare_semver, parse_semver
from test_openai_release_ledger import (
    authenticated_external_evidence_adapter_available,
    validate_release_evidence,
    validate_rollback_history_binding,
    validate_verified_source_commit_tree,
)
from test_openai_phase7_modes import release_gate_statuses, run_all as build_phase7_report
from test_openai_phase8_corpus import run_all as build_phase8_report


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
def markdown_h2_section(markdown: str, title: str) -> str | None:
    heading = re.search(rf"^##[ \t]+{re.escape(title)}(?:[ \t]+.*)?$", markdown, re.MULTILINE)
    if not heading:
        return None
    next_heading = re.search(r"^##[ \t]+", markdown[heading.end() :], re.MULTILINE)
    end = heading.end() + next_heading.start() if next_heading else len(markdown)
    return markdown[heading.start() : end]


def section_status(section: str) -> str | None:
    status_pattern = re.compile(
        r"^Status:[ \t]*(?P<status>[A-Za-z][0-9A-Za-z_-]*)"
        r"(?:[ \t]+\([^\r\n)]*\))?[ \t]*$"
    )
    for line in section.splitlines()[1:]:
        if not line.strip():
            continue
        match = status_pattern.fullmatch(line)
        return match.group("status").lower() if match else None
    return None


def validate_phase5_upgrade_receipt(upgrade: str, current_version: str, expected_skill_count: int) -> list[str]:
    errors: list[str] = []
    upgrade_match = re.search(
        r"^2\.[ \t]+GitHub `main` was updated to commit `[0-9a-f]{40}`[^\r\n]*"
        r"declares `([^`]+)`\.[ \t]*$",
        upgrade,
        re.MULTILINE,
    )
    upgraded_version = upgrade_match.group(1) if upgrade_match else ""
    required_upgrade_evidence = (
        "Status: upgrade_verified",
        upgraded_version,
        '"discovery_status": "verified"',
        f'"skill_count": {expected_skill_count}',
        '"pubmed_present": false',
        "human_signoff_required",
    )
    for marker in required_upgrade_evidence:
        if marker not in upgrade:
            errors.append(f"Phase 5 upgrade receipt missing evidence: {marker}")

    automatic_submission_false = any(
        re.search(pattern, upgrade, re.MULTILINE)
        for pattern in (
            r'^[ \t]*(?:[-*][ \t]+)?["`]?automatic_external_submission["`]?[ \t]*:[ \t]*false[ \t]*[,.]?[ \t]*$',
            r"^[ \t]*-[ \t]+`automatic_external_submission`[ \t]+remains[ \t]+`false`\.[ \t]*$",
        )
    )
    if not automatic_submission_false:
        errors.append("Phase 5 upgrade receipt does not prove automatic_external_submission: false")

    baseline_match = re.search(
        r"^1\.[ \t]+The previously installed[^\r\n]*:[ \t]*\r?\n"
        r"[ \t]*-[ \t]+version:[ \t]+`([^`]+)`[ \t]*$",
        upgrade,
        re.MULTILINE,
    )
    if not baseline_match:
        errors.append("Phase 5 upgrade receipt lacks an installed baseline version")
    elif not upgrade_match:
        errors.append("Phase 5 upgrade receipt lacks the upgraded manifest version")
    else:
        baseline_version = baseline_match.group(1)
        if parse_semver(baseline_version) is None:
            errors.append(f"Phase 5 upgrade receipt baseline is not SemVer: {baseline_version}")
        elif parse_semver(upgraded_version) is None:
            errors.append(f"Phase 5 upgrade receipt target is not SemVer: {upgraded_version}")
        elif compare_semver(baseline_version, upgraded_version) >= 0:
            errors.append(
                "Phase 5 upgrade receipt baseline must be strictly older than "
                f"the recorded upgrade: {baseline_version} !< {upgraded_version}"
            )
        elif parse_semver(current_version) is not None and compare_semver(upgraded_version, current_version) > 0:
            errors.append(
                "Phase 5 historical upgrade cannot be newer than the current plugin: "
                f"{upgraded_version} > {current_version}"
            )

    actions_chain = re.search(
        r"^2\.[ \t]+GitHub `main` was updated to commit `(?P<commit>[0-9a-f]{40})`[^\r\n]*\r?\n"
        r"3\.[ \t]+GitHub Actions run `[0-9]+`[^\r\n]*conclusion `success` for "
        r"(?:that commit|commit `(?P=commit)`):[ \t]*$",
        upgrade,
        re.MULTILINE,
    )
    if not actions_chain:
        errors.append(
            "Phase 5 upgrade receipt does not bind a successful GitHub Actions run "
            "to the same full commit SHA"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    registry = yaml.safe_load((PLUGIN / "workflow-registry.yaml").read_text(encoding="utf-8"))
    marketplace = json.loads((REPO / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    version = str(manifest.get("version", ""))
    registry_skill_names = {
        str(entry.get("name", "")) for entry in registry.get("skills", []) if entry.get("name")
    }
    discovered_skill_names = {
        path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")
    }
    expected_skill_count = len(registry_skill_names)
    implicit_entry_names = {
        str(entry.get("name"))
        for entry in registry.get("skills", [])
        if entry.get("invocation_policy") == "implicit"
    }
    if not registry_skill_names or discovered_skill_names != registry_skill_names:
        errors.append(
            "release skill discovery differs from registry: "
            f"missing={sorted(registry_skill_names - discovered_skill_names)} "
            f"extra={sorted(discovered_skill_names - registry_skill_names)}"
        )

    if parse_semver(version) is None:
        errors.append(f"manifest version is not release SemVer without build metadata: {version}")
    if "+codex." in version:
        errors.append("main Preview manifest contains a local cachebuster")
    if registry.get("plugin_version") != version:
        errors.append("manifest and registry versions differ")
    if registry.get("schema_version") != 5:
        errors.append("release requires registry schema 5")
    if manifest.get("name") != "research-skills-openai" or manifest.get("skills") != "./skills/":
        errors.append("plugin manifest identity or skills path is invalid")

    product_text = " ".join(
        [
            str(manifest.get("description", "")),
            str(manifest.get("interface", {}).get("displayName", "")),
            str(manifest.get("interface", {}).get("longDescription", "")),
        ]
    ).lower()
    if "preview" not in product_text or "experimental" not in product_text:
        errors.append("plugin is not clearly labeled Preview/Experimental")
    if registry.get("workflow_state_policy", {}).get("final_handoff_state") != "human_signoff_required":
        errors.append("final workflow state is not human_signoff_required")
    if registry.get("scenario_eval_contract", {}).get("automatic_external_submission") is not False:
        errors.append("release contract does not prohibit automatic external submission")

    entries = [item for item in marketplace.get("plugins", []) if item.get("name") == "research-skills-openai"]
    if len(entries) != 1:
        errors.append(f"marketplace must contain exactly one plugin entry, found {len(entries)}")
    else:
        entry = entries[0]
        expected_source = {
            "source": "git-subdir",
            "url": "https://github.com/xuxu-wei/research-skills.git",
            "path": "./research-skills-openai",
            "ref": "main",
        }
        if entry.get("source") != expected_source:
            errors.append("marketplace must track the GitHub main git-subdir source")
        if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            errors.append("marketplace policy is invalid")
        if entry.get("category") != "Research":
            errors.append("marketplace category is invalid")

    phase4_path = PLUGIN / "reports" / "phase4-scenario-results.json"
    if not phase4_path.is_file():
        errors.append("Phase 4 scenario report is missing")
    else:
        phase4 = json.loads(phase4_path.read_text(encoding="utf-8"))
        if phase4.get("plugin_version") != version:
            errors.append("Phase 4 report version differs from the plugin")
        summary = phase4.get("summary", {})
        if (
            summary.get("workflows_passed") != 4
            or summary.get("negative_guards_rejected", 0) < 39
            or summary.get("finding_routes_verified") != 5
            or summary.get("live_workflows_receipts_audited") != 4
            or summary.get("live_workflows_reached_human_signoff_gate") != 0
            or summary.get("live_workflows_stopped_at_valid_gate") != 2
            or summary.get("live_workflows_blocked_at_valid_gate") != 1
            or summary.get("live_workflows_independent_review_pending") != 1
            or summary.get("live_raw_state_claims_corrected") != 2
        ):
            errors.append("Phase 4 scenario or negative-guard coverage is incomplete")
        if summary.get("live_receipt_applicability") not in {
            "current_tree_compatible",
            "historical_only_digest_mismatch",
            "historical_only_incomplete_identity",
        }:
            errors.append("Phase 4 live-receipt applicability is missing or invalid")
        if (
            summary.get("live_receipt_applicability")
            == "historical_only_incomplete_identity"
            and (
                summary.get("live_receipt_identity_complete") is not False
                or summary.get("live_current_identity_compatible_receipts") != 0
                or summary.get("live_identity_negative_guards_rejected", 0) < 12
            )
        ):
            errors.append("Phase 4 incomplete historical identity is not safely bounded")
        if summary.get("automatic_external_submission") is not False:
            errors.append("Phase 4 report permits automatic external submission")

    validation_path = PLUGIN / "reports" / "validation.json"
    if not validation_path.is_file():
        errors.append("portable plugin validation report is missing")
    else:
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if (
            validation.get("plugin_version") != version
            or validation.get("registry_schema_version") != registry.get("schema_version")
            or validation.get("expected_skill_count") != expected_skill_count
            or validation.get("ok") is not True
        ):
            errors.append("portable plugin validation report is stale or invalid")

    phase6_path = PLUGIN / "reports" / "phase6-context-measurement.md"
    if not phase6_path.is_file():
        errors.append("Phase 6 context measurement is missing")

    phase7_path = PLUGIN / "reports" / "phase7-mode-results.json"
    if not phase7_path.is_file():
        errors.append("Phase 7 mode report is missing")
    else:
        phase7 = json.loads(phase7_path.read_text(encoding="utf-8"))
        if phase7 != build_phase7_report():
            errors.append("Phase 7 report differs from a fresh validator replay")
        phase7_summary = phase7.get("summary", {})
        declared_modes = sum(
            len(machine.get("entry_modes", []))
            for machine in registry.get("workflow_state_machines", {}).values()
            if isinstance(machine, dict)
        )
        declared_gate_contracts = sum(
            len(gates)
            for machine in registry.get("workflow_state_machines", {}).values()
            if isinstance(machine, dict)
            for gates in machine.get("scenario_entry_gate_contracts", {}).values()
            if isinstance(gates, dict)
        )
        positive_results = phase7.get("positive_mode_results", [])
        negative_results = phase7.get("negative_guard_results", [])
        evaluator_modes = sum(
            bool(result.get("synthetic_evaluator_receipt_ids"))
            for result in positive_results
            if isinstance(result, dict)
        )
        panel_modes = sum(
            bool(result.get("synthetic_panel_receipt_ids"))
            for result in positive_results
            if isinstance(result, dict)
        )
        entry_negative_count = sum(
            result.get("guard_scope") == "entry_gate_receipt_or_artifact_lineage"
            for result in negative_results
            if isinstance(result, dict)
        )
        reviewer_negative_count = sum(
            result.get("guard_scope") == "lifecycle_qualifying_reviewer_receipt"
            for result in negative_results
            if isinstance(result, dict)
        )
        reviewer_mutation_counts = {
            mutation: sum(
                result.get("mutation") == mutation
                for result in negative_results
                if isinstance(result, dict)
            )
            for mutation in (
                "missing_evaluator_receipt",
                "stale_evaluator_receipt",
                "missing_panel_receipt",
                "stale_panel_receipt",
            )
        }
        runtime_receipts = phase7.get("runtime_receipts", {})
        runtime_results = runtime_receipts.get("results", [])
        runtime_guards = runtime_receipts.get("validator_negative_guards", [])
        runtime_verified = sum(
            isinstance(result, dict) and result.get("status") == "verified"
            for result in runtime_results
        )
        runtime_pending = sum(
            isinstance(result, dict)
            and result.get("status") == "pending_live_evidence"
            for result in runtime_results
        )
        runtime_happy_verified = sum(
            isinstance(result, dict)
            and result.get("status") == "verified"
            and result.get("case_kind") == "happy"
            for result in runtime_results
        )
        runtime_control_verified = sum(
            isinstance(result, dict)
            and result.get("status") == "verified"
            and result.get("case_kind") == "control"
            for result in runtime_results
        )
        expected_runtime_pairs = {
            (workflow, case_kind)
            for workflow in registry.get("workflow_state_machines", {})
            for case_kind in ("happy", "control")
        }
        actual_runtime_pairs = {
            (result.get("workflow"), result.get("case_kind"))
            for result in runtime_results
            if isinstance(result, dict)
        }
        completion_gates = phase7.get("completion_gates", {})
        expected_completion_gate_ids = {
            "authenticated_platform_capture_adapter",
            "authenticated_external_evidence_adapter",
            "four_current_version_live_happy_paths",
            "four_current_version_valid_control_paths",
            "release_source_commit",
            "repository_preview_ci",
            "canonical_plugin_validator_ci",
            "marketplace_resolved_commit",
            "marketplace_upgrade",
            "explicit_reinstall",
            "fresh_task_discovery",
            "immutable_previous_artifact_rollback",
            "main_branch_required_check_protection",
        }
        derived_pending_gates = [
            gate_id
            for gate_id, gate in completion_gates.items()
            if not isinstance(gate, dict) or gate.get("status") != "verified"
        ]
        expected_phase7_status = (
            "complete"
            if not derived_pending_gates
            else "in_progress_live_and_release_evidence_pending"
        )
        reachability = runtime_receipts.get("completion_reachability_self_test", {})
        phase7_platform_trust = runtime_receipts.get("platform_trust", {})
        if phase7.get("plugin_version") != version:
            errors.append("Phase 7 mode report version differs from the plugin")
        if phase7.get("phase_status") not in {
            "in_progress_live_and_release_evidence_pending",
            "complete",
        }:
            errors.append("Phase 7 report has no valid phase status")
        if (
            phase7_summary.get("declared_entry_modes") != declared_modes
            or phase7_summary.get("positive_modes_passed") != declared_modes
            or len(positive_results) != declared_modes
            or phase7_summary.get("registry_entry_mode_contracts_verified")
            != declared_modes
            or phase7_summary.get("registry_entry_gate_contracts_verified")
            != declared_gate_contracts
            or phase7_summary.get("mode_specific_gate_bypasses_rejected") != declared_modes
            or phase7_summary.get("additional_stale_or_lineage_guards_rejected") != declared_modes
            or phase7_summary.get("entry_gate_negative_guards_rejected")
            != entry_negative_count
            or entry_negative_count != declared_modes * 2
            or phase7_summary.get("qualifying_reviewer_receipt_negatives_rejected")
            != reviewer_negative_count
            or reviewer_mutation_counts["missing_evaluator_receipt"]
            != evaluator_modes
            or reviewer_mutation_counts["stale_evaluator_receipt"]
            != evaluator_modes
            or reviewer_mutation_counts["missing_panel_receipt"] != panel_modes
            or reviewer_mutation_counts["stale_panel_receipt"] != panel_modes
            or phase7_summary.get("missing_evaluator_receipts_rejected")
            != evaluator_modes
            or phase7_summary.get("stale_evaluator_receipts_rejected")
            != evaluator_modes
            or phase7_summary.get("missing_panel_receipts_rejected") != panel_modes
            or phase7_summary.get("stale_panel_receipts_rejected") != panel_modes
            or reviewer_negative_count != 2 * (evaluator_modes + panel_modes)
            or phase7_summary.get("negative_guards_rejected")
            != len(negative_results)
            or len(negative_results) != entry_negative_count + reviewer_negative_count
            or phase7_summary.get("false_ready_count") != 0
            or phase7_summary.get("automatic_external_submission") is not False
            or phase7_summary.get("live_model_runs_claimed") != runtime_verified
            or phase7.get("evidence_class") != "synthetic_contract_evidence_only"
            or phase7.get("execution_kind") != "deterministic_replay"
            or phase7.get("live_model_execution") is not False
            or phase7.get("state_advance_order")
            != "validate_qualifying_receipt_then_validate_registry_prerequisites_then_commit_derived_state_then_execute_transition"
        ):
            errors.append("Phase 7 deterministic mode coverage is incomplete")
        if (
            not isinstance(runtime_results, list)
            or len(runtime_results) != 8
            or expected_runtime_pairs != actual_runtime_pairs
            or runtime_verified + runtime_pending != 8
            or runtime_receipts.get("expected_receipt_count") != 8
            or runtime_receipts.get("verified_receipt_count") != runtime_verified
            or runtime_receipts.get("pending_receipt_count") != runtime_pending
            or runtime_receipts.get("live_evidence_claimed") is not (runtime_verified > 0)
            or phase7_summary.get("runtime_receipts_expected") != 8
            or phase7_summary.get("runtime_receipts_verified") != runtime_verified
            or phase7_summary.get("runtime_receipts_pending") != runtime_pending
            or len(runtime_guards) < 9
            or phase7_summary.get("runtime_validator_negative_guards_rejected")
            != len(runtime_guards)
            or any(
                not isinstance(guard, dict)
                or guard.get("status") != "rejected_as_expected"
                for guard in runtime_guards
            )
            or {
                "label_only_verified_status",
                "missing_durable_actor_manifest_binding",
                "task_export_digest_mismatch",
                "task_export_content_identity_mismatch",
                "review_artifact_dissent_hidden",
                "review_artifact_fatal_hidden_false_ready",
                "panel_writes_primary_input",
                "unregistered_evaluator_actor_skill",
                "repository_authored_export_without_platform_trust_adapter",
            }
            - {
                guard.get("mutation")
                for guard in runtime_guards
                if isinstance(guard, dict)
            }
            or set(completion_gates) != expected_completion_gate_ids
            or any(
                not isinstance(gate, dict)
                or gate.get("status") not in {"verified", "pending"}
                for gate in completion_gates.values()
            )
            or completion_gates.get(
                "authenticated_platform_capture_adapter", {}
            ).get("status")
            != (
                "verified"
                if phase7_platform_trust.get("completion_gate_verified") is True
                else "pending"
            )
            or phase7_platform_trust.get(
                "repository_files_alone_count_as_platform_authenticity"
            )
            is not False
            or not isinstance(
                phase7_platform_trust.get("supported_authenticated_adapter_ids"),
                list,
            )
            or completion_gates.get(
                "four_current_version_live_happy_paths", {}
            ).get("status")
            != ("verified" if runtime_happy_verified == 4 else "pending")
            or completion_gates.get(
                "four_current_version_valid_control_paths", {}
            ).get("status")
            != ("verified" if runtime_control_verified == 4 else "pending")
            or not isinstance(phase7.get("pending_gates"), list)
            or len(phase7.get("pending_gates", [])) != len(derived_pending_gates)
            or set(phase7.get("pending_gates", [])) != set(derived_pending_gates)
            or phase7_summary.get("completion_gates_verified")
            != len(completion_gates) - len(derived_pending_gates)
            or phase7_summary.get("completion_gates_pending")
            != len(derived_pending_gates)
            or phase7.get("phase_status") != expected_phase7_status
            or (
                phase7.get("phase_status") == "complete"
                and runtime_verified != 8
            )
            or reachability.get("status") != "passed"
            or reachability.get("evidence_kind")
            != "synthetic_gate_logic_self_test_only"
            or reachability.get("counts_as_runtime_evidence") is not False
            or reachability.get("derived_phase_status") != "complete"
            or reachability.get("verified_gate_count") != len(completion_gates)
        ):
            errors.append("Phase 7 runtime receipt or completion-gate accounting is invalid")

    phase8_path = PLUGIN / "reports" / "phase8-corpus-results.json"
    if not phase8_path.is_file():
        errors.append("Phase 8 corpus report is missing")
    else:
        phase8 = json.loads(phase8_path.read_text(encoding="utf-8"))
        if phase8 != build_phase8_report():
            errors.append("Phase 8 report differs from a fresh validator replay")
        corpus = phase8.get("corpus", {})
        live_repeat = phase8.get("live_fresh_repeat", {})
        retrieval = phase8.get("retrieval", {})
        claims = phase8.get("claims", {})
        phase8_status = phase8.get("phase_status")
        required_distribution = {
            "search": 3,
            "deep_research_completed": 2,
            "deep_research_inactive_control": 1,
        }
        completed_by_kind = retrieval.get("completed_current_receipts_by_kind", {})
        observed_by_kind = retrieval.get("observed_unverified_receipts_by_kind", {})
        durable_retrieval_guards = retrieval.get(
            "durable_provenance_negative_guards", []
        )
        durable_live_guards = live_repeat.get(
            "durable_binding_negative_guards", []
        )
        completed_receipts = retrieval.get("completed_current_receipts", 0)
        observed_receipts = retrieval.get("observed_unverified_receipts", 0)
        pending_receipts = retrieval.get("pending_receipts", 0)
        stale_receipts = retrieval.get("stale_receipts", 0)
        verified_reviews = live_repeat.get("verified_live_review_count", 0)
        live_gate_complete = (
            verified_reviews == 6
            and live_repeat.get("status") == "completed"
            and live_repeat.get("verified_live_gate_status") == "completed"
        )
        retrieval_gate_complete = (
            completed_by_kind == required_distribution
            and completed_receipts == sum(required_distribution.values())
            and observed_receipts == 0
            and pending_receipts == 0
            and stale_receipts == 0
            and retrieval.get("status") == "completed"
        )
        if phase8.get("plugin_version") != version:
            errors.append("Phase 8 report version differs from the plugin")
        if phase8_status not in {
            "in_progress_live_runtime_evidence_pending",
            "complete",
        }:
            errors.append("Phase 8 report has no valid phase status")
        if (
            corpus.get("case_count", 0)
            < 4 * len(registry.get("workflow_state_machines", {}))
            or corpus.get("metrics", {}).get("false_ready_count") != 0
            or corpus.get("metrics", {}).get("fatal_or_blocking_finding_recall_percent")
            != 100.0
            or corpus.get("metrics", {}).get("major_finding_recall_percent", 0)
            < 90.0
            or any(
                corpus.get("metrics", {}).get(metric) != 100.0
                for metric in (
                    "lineage_compliance_percent",
                    "reviewer_isolation_compliance_percent",
                    "reviewer_edit_boundary_compliance_percent",
                    "dissent_preservation_percent",
                )
            )
            or live_repeat.get("case_count") != 3
            or live_repeat.get("observed_review_snapshot_count") != 6
            or live_repeat.get("unique_reviewer_instance_count") != 6
            or live_repeat.get("snapshot_contract_state_agreement_percent") != 100.0
            or live_repeat.get("durable_binding_negative_guard_count") != 6
            or len(durable_live_guards) != 6
            or any(
                not isinstance(guard, dict)
                or guard.get("status") != "rejected"
                or guard.get("error_code") != "live_repeat_durable_binding"
                for guard in durable_live_guards
            )
            or verified_reviews not in {0, 6}
            or (
                verified_reviews == 0
                and (
                    live_repeat.get("status") != "observed_unverified"
                    or live_repeat.get("verified_live_gate_status")
                    != "pending_durable_execution_evidence"
                )
            )
            or (verified_reviews == 6 and not live_gate_complete)
            or retrieval.get("required_distribution") != required_distribution
            or retrieval.get("required_receipt_count")
            != sum(required_distribution.values())
            or completed_receipts != sum(completed_by_kind.values())
            or observed_receipts != sum(observed_by_kind.values())
            or completed_receipts + observed_receipts + pending_receipts + stale_receipts
            != sum(required_distribution.values())
            or retrieval.get("durable_provenance_negative_guard_count") != 41
            or len(durable_retrieval_guards) != 41
            or any(not isinstance(guard, dict) for guard in durable_retrieval_guards)
            or any(
                guard.get("status") != "rejected"
                or guard.get("error_code")
                not in {
                    "retrieval_durable_provenance",
                    "retrieval_durable_query_binding",
                    "retrieval_durable_binding",
                }
                for guard in durable_retrieval_guards
                if isinstance(guard, dict)
            )
            or sum(
                guard.get("error_code") == "retrieval_durable_query_binding"
                for guard in durable_retrieval_guards
                if isinstance(guard, dict)
            )
            != 3
            or sum(
                guard.get("error_code") == "retrieval_durable_binding"
                for guard in durable_retrieval_guards
                if isinstance(guard, dict)
            )
            != 10
            or claims.get("live_fresh_evaluator_repeats_counted_as_pass")
            != verified_reviews
            or claims.get("live_search_receipts_counted_as_pass")
            != completed_by_kind.get("search", 0)
            or claims.get("deep_research_cycles_claimed_without_receipts") != 0
        ):
            errors.append("Phase 8 corpus or evidence accounting is incomplete")
        if phase8_status == "complete":
            if (
                not live_gate_complete
                or not retrieval_gate_complete
                or claims.get("phase8_complete") is not True
            ):
                errors.append("Phase 8 is marked complete without all durable live gates")
        elif (
            live_gate_complete
            and retrieval_gate_complete
            or claims.get("phase8_complete") is not False
            or retrieval.get("status") not in {"pending_live_evidence", "completed"}
        ):
            errors.append("Phase 8 pending status is inconsistent with its evidence gates")

    ledger_path = PLUGIN / "reports" / "release-ledger.json"
    if not ledger_path.is_file():
        errors.append("machine-readable release ledger is missing")
    else:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        release = ledger.get("release", {})
        if release.get("version") != version:
            errors.append("release ledger version differs from the plugin")
        ledger_evidence_errors: list[str] = []
        validate_release_evidence(
            release,
            version,
            expected_skill_count,
            ledger_evidence_errors,
            authenticated_external_adapter=(
                authenticated_external_evidence_adapter_available(release)
            ),
        )
        validate_verified_source_commit_tree(release, ledger_evidence_errors)
        previous_releases = ledger.get("previous_releases", [])
        if isinstance(previous_releases, list):
            for index, previous in enumerate(previous_releases):
                if not isinstance(previous, dict):
                    ledger_evidence_errors.append(
                        f"previous_releases[{index}] is not an object"
                    )
                    continue
                validate_release_evidence(
                    previous,
                    str(previous.get("version", "")),
                    None,
                    ledger_evidence_errors,
                    prefix=f"previous_releases[{index}].",
                    authenticated_external_adapter=(
                        authenticated_external_evidence_adapter_available(previous)
                    ),
                )
                validate_verified_source_commit_tree(
                    previous,
                    ledger_evidence_errors,
                    f"previous_releases[{index}]",
                )
            validate_rollback_history_binding(
                release,
                previous_releases,
                ledger_evidence_errors,
            )
        else:
            ledger_evidence_errors.append("previous_releases is not a list")
        errors.extend(
            f"release ledger evidence invalid: {error}"
            for error in ledger_evidence_errors
        )
        if phase7_path.is_file():
            expected_release_gates = release_gate_statuses(ledger, registry)
            reported_release_gates = {
                gate_id: phase7.get("completion_gates", {}).get(gate_id)
                for gate_id in expected_release_gates
            }
            if reported_release_gates != expected_release_gates:
                errors.append(
                    "Phase 7 release completion gates differ from durable ledger evidence"
                )
        if phase7_path.is_file() and phase7.get("phase_status") == "complete":
            canonical = release.get("ci", {}).get("canonical_plugin_validator", {})
            phase7_release_records = (
                release.get("source_commit", {}),
                release.get("ci", {}).get("repository_preview", {}),
                canonical.get("local", {}),
                canonical.get("ci", {}),
                release.get("governance", {}).get("main_branch_protection", {}),
                release.get("marketplace_source", {}).get("resolved_commit", {}),
                release.get("receipts", {}).get("marketplace_upgrade", {}),
                release.get("receipts", {}).get("explicit_reinstall", {}),
                release.get("receipts", {}).get("fresh_task_discovery", {}),
                release.get("receipts", {}).get("rollback", {}),
            )
            if phase7.get("pending_gates") or any(
                record.get("status") != "verified"
                for record in phase7_release_records
                if isinstance(record, dict)
            ):
                errors.append(
                    "Phase 7 is marked complete without all runtime, release, rollback, and governance gates"
                )

    workflow_path = REPO / ".github" / "workflows" / "openai-plugin-preview.yml"
    if not workflow_path.is_file():
        errors.append("GitHub Actions Preview validation workflow is missing")
    else:
        workflow = workflow_path.read_text(encoding="utf-8")
        action_refs = re.findall(
            r"^[ \t]*-[ \t]+uses:[ \t]+([^@\s]+)@([^\s#]+)",
            workflow,
            re.MULTILINE,
        )
        if not action_refs:
            errors.append("CI workflow contains no externally pinned actions")
        elif any(not re.fullmatch(r"[0-9a-f]{40}", ref) for _, ref in action_refs):
            errors.append("CI workflow action dependencies are not pinned to immutable commits")
        if "fetch-depth: 0" not in workflow:
            errors.append("CI workflow cannot validate immutable source commits without full history")
        if not re.search(
            r"python -m pip install PyYAML==[0-9]+\.[0-9]+\.[0-9]+",
            workflow,
        ):
            errors.append("CI Python validator dependency is not exactly version-pinned")
        for command in (
            "audit_openai_research_plugin.py",
            "test_openai_release_contract.py",
            "sync_openai_fixture_versions.py",
            "test_openai_phase2_phase3.py",
            "test_openai_phase4_scenarios.py --check-report",
            "test_openai_phase6_context.py",
            "test_openai_phase7_modes.py --check-report",
            "test_openai_phase8_corpus.py --check-report",
            "codex_plugin_converter.py --mode codex --fail-on-invalid",
            "generate_openai_release_ledger.py --check",
            "test_openai_release_ledger.py",
            "validate_openai_preview_release.py",
            "check_openai_version_bump.py",
        ):
            if command not in workflow:
                errors.append(f"CI workflow missing command: {command}")

    readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
    roadmap = (PLUGIN / "ROADMAP.md").read_text(encoding="utf-8")
    if f"contains {expected_skill_count} skills" not in readme:
        errors.append("README skill-count claim differs from registry discovery")
    quickstart_names = set(re.findall(r"^### `\$([^`]+)`[ \t]*$", readme, re.MULTILINE))
    if quickstart_names != implicit_entry_names:
        errors.append(
            "README quickstart/public-entry mismatch: "
            f"missing={sorted(implicit_entry_names - quickstart_names)} "
            f"extra={sorted(quickstart_names - implicit_entry_names)}"
        )
    scope_match = re.search(r"^Current scope:[ \t]*(\d+)[ \t]+skills\b", roadmap, re.MULTILINE)
    if not scope_match or int(scope_match.group(1)) != expected_skill_count:
        errors.append("Roadmap current-scope skill count differs from registry discovery")
    documentation_text = f"{readme}\n{roadmap}".lower()
    for marker, label in (
        ("experimental/preview", "Preview status"),
        ("chatgpt web", "ChatGPT web verification boundary"),
        ("human review", "human-review boundary"),
    ):
        if marker not in documentation_text:
            errors.append(f"README/Roadmap missing {label}")
    if "does not submit" not in readme.lower():
        errors.append("README does not state the no-external-submission boundary")
    phase5_section = markdown_h2_section(roadmap, "Phase 5")
    if phase5_section is None:
        errors.append("Roadmap Phase 5 section is missing")
    elif section_status(phase5_section) == "complete":
        upgrade_path = PLUGIN / "reports" / "phase5-upgrade-smoke.md"
        if not upgrade_path.is_file():
            errors.append("Phase 5 is marked complete without a verified upgrade receipt")
        else:
            upgrade = upgrade_path.read_text(encoding="utf-8")
            errors.extend(validate_phase5_upgrade_receipt(upgrade, version, expected_skill_count))

    if errors:
        print("OpenAI Preview release validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OpenAI Preview release validation passed")
    print(f"version: {version}")
    print(f"skills: {expected_skill_count}")
    print("channel: GitHub main Preview")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
