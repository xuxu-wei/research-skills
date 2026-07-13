#!/usr/bin/env python3
"""Portable release validation for the OpenAI Preview plugin and marketplace."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Mapping, Sequence

import yaml

from openai_release_utils import compare_semver, parse_semver
from build_openai_preview_accepted_summary import (
    AcceptedSummaryError,
    PHASE7_COMPLETION_GATE_IDS,
    strict_phase78_snapshot,
)
from test_openai_release_ledger import (
    authenticated_external_evidence_adapter_available,
    configured_external_evidence_level,
    validate_release_evidence,
    validate_rollback_history_binding,
    validate_verified_source_commit_tree,
)
from test_openai_phase7_modes import release_gate_statuses, run_all as build_phase7_report
from test_openai_phase8_corpus import run_all as build_phase8_report
from validate_openai_release_evidence import (
    ReleaseEvidenceRunnerError,
    create_production_callback,
)


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the complete OpenAI Preview release contract."
    )
    parser.add_argument(
        "--bundle-root",
        help=(
            "Directory containing downloaded current and accepted-history evidence "
            "bundles. When supplied, accepted external records are re-queried through "
            "the fixed production GitHub verifier in this process."
        ),
    )
    parser.add_argument(
        "--require-phase78-complete-preview",
        action="store_true",
        help=(
            "Protected accepted-state mode: require the live-bridge reports to be "
            "complete_preview_attested for all Phase 7 and Phase 8 slots. This mode "
            "requires --bundle-root and is not an ordinary structural replay."
        ),
    )
    return parser


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
    historical_count_match = re.search(r'"skill_count"\s*:\s*(\d+)', upgrade)
    required_upgrade_evidence = (
        "Status: upgrade_verified",
        upgraded_version,
        '"discovery_status": "verified"',
        '"pubmed_present": false',
        "human_signoff_required",
    )
    for marker in required_upgrade_evidence:
        if marker not in upgrade:
            errors.append(f"Phase 5 upgrade receipt missing evidence: {marker}")
    if not historical_count_match or int(historical_count_match.group(1)) <= 0:
        errors.append("Phase 5 upgrade receipt lacks its historical discovered skill count")

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


def main(
    argv: Sequence[str] | None = None,
    *,
    _accepted_phase78_reports: tuple[Mapping[str, object], Mapping[str, object]]
    | None = None,
) -> int:
    args = _build_parser().parse_args(argv)
    errors: list[str] = []
    if args.require_phase78_complete_preview and not args.bundle_root:
        errors.append(
            "--require-phase78-complete-preview requires --bundle-root and the "
            "protected live-evidence workflow"
        )
    if args.require_phase78_complete_preview and _accepted_phase78_reports is None:
        errors.append(
            "protected Phase 7-8 completion requires the same-process live-bridge "
            "reports; serialized report files cannot enable this CLI mode"
        )
    if _accepted_phase78_reports is not None and not args.require_phase78_complete_preview:
        errors.append(
            "same-process Phase 7-8 reports are valid only with the protected "
            "completion gate"
        )
    live_evidence_verifier = None
    phase7_gate_evidence_verifier = None
    if args.bundle_root:
        try:
            live_evidence_verifier = create_production_callback(
                Path(args.bundle_root)
            )
            if args.require_phase78_complete_preview:
                phase7_gate_evidence_verifier = create_production_callback(
                    Path(args.bundle_root)
                )
        except (OSError, ReleaseEvidenceRunnerError) as exc:
            errors.append(
                "production live evidence callback could not be initialized: "
                f"{type(exc).__name__}: {exc}"
            )
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
    public_entry_names = set(
        registry.get("public_entry_policy", {}).get("declared_entries", [])
    )
    if len(public_entry_names) != 7 or len(implicit_entry_names) != 6:
        errors.append(
            "release requires seven declared public entries with six implicit-active "
            "until the Research Polisher Phase 7-8 gate passes"
        )
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
            summary.get("workflows_passed")
            != len(registry.get("workflow_state_machines", {}))
            or summary.get("negative_guards_rejected", 0) < 53
            or summary.get("research_polisher_component_guards_rejected", 0) < 12
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

    phase7: dict[str, object] | None = None
    phase7_path = PLUGIN / "reports" / "phase7-mode-results.json"
    if not phase7_path.is_file():
        errors.append("Phase 7 mode report is missing")
    else:
        recorded_phase7 = json.loads(phase7_path.read_text(encoding="utf-8"))
        if args.require_phase78_complete_preview:
            # The accepted report is produced and retained by the protected live
            # bridge in this process. A capability-free replay is intentionally
            # pending and serialized files alone may not enable this branch.
            phase7 = (
                dict(_accepted_phase78_reports[0])
                if _accepted_phase78_reports is not None
                else recorded_phase7
            )
            if _accepted_phase78_reports is not None and recorded_phase7 != phase7:
                errors.append(
                    "Phase 7 report file differs from the same-process live report"
                )
        else:
            phase7 = build_phase7_report()
            if recorded_phase7 != phase7:
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
        strategy_group_modes = sum(
            bool(result.get("synthetic_strategy_reviewer_receipt_ids"))
            for result in positive_results
            if isinstance(result, dict)
        )
        strategy_receipt_total = sum(
            len(result.get("synthetic_strategy_reviewer_receipt_ids", []))
            for result in positive_results
            if isinstance(result, dict)
        )
        polisher_results = [
            result
            for result in positive_results
            if isinstance(result, dict)
            and result.get("workflow") == "research_polisher"
        ]
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
                "missing_strategy_reviewer_receipt",
                "stale_strategy_reviewer_receipt",
                "duplicate_strategy_reviewer_instance",
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
        expected_completion_gate_ids = PHASE7_COMPLETION_GATE_IDS
        derived_pending_gates = [
            gate_id
            for gate_id, gate in completion_gates.items()
            if not isinstance(gate, dict) or gate.get("status") != "verified"
        ]
        phase7_verification_level = phase7.get("verification_level")
        if derived_pending_gates:
            expected_phase7_status = "in_progress_live_and_release_evidence_pending"
        elif phase7_verification_level == "preview_attested":
            expected_phase7_status = "complete_preview_attested"
        elif phase7_verification_level == "provider_verified":
            expected_phase7_status = "complete_provider_verified"
        else:
            expected_phase7_status = None
        reachability = runtime_receipts.get("completion_reachability_self_test", {})
        phase7_platform_trust = runtime_receipts.get("platform_trust", {})
        phase7_discovery = phase7.get("discovery_contract", {})
        expected_phase7_evidence_class = (
            "synthetic_contract_and_external_runtime_evidence"
            if args.require_phase78_complete_preview
            else "synthetic_contract_evidence_only"
        )
        expected_phase7_execution_kind = (
            "deterministic_replay_with_external_runtime_evidence"
            if args.require_phase78_complete_preview
            else "deterministic_replay"
        )
        if phase7.get("plugin_version") != version:
            errors.append("Phase 7 mode report version differs from the plugin")
        if phase7.get("phase_status") not in {
            "in_progress_live_and_release_evidence_pending",
            "complete_preview_attested",
            "complete_provider_verified",
        }:
            errors.append("Phase 7 report has no valid phase status")
        if (
            phase7_summary.get("declared_entry_modes") != declared_modes
            or phase7_discovery
            != {
                "installed_skill_count": 49,
                "explicit_callable_entries": 7,
                "implicit_prompt_entries": 6,
                "release_stage": "A",
            }
            or phase7_summary.get("installed_skill_count") != 49
            or phase7_summary.get("explicit_callable_entries") != 7
            or phase7_summary.get("implicit_prompt_entries") != 6
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
            or reviewer_mutation_counts["missing_strategy_reviewer_receipt"]
            != strategy_group_modes
            or reviewer_mutation_counts["stale_strategy_reviewer_receipt"]
            != strategy_group_modes
            or reviewer_mutation_counts["duplicate_strategy_reviewer_instance"]
            != strategy_group_modes
            or phase7_summary.get("missing_evaluator_receipts_rejected")
            != evaluator_modes
            or phase7_summary.get("stale_evaluator_receipts_rejected")
            != evaluator_modes
            or phase7_summary.get("missing_panel_receipts_rejected") != panel_modes
            or phase7_summary.get("stale_panel_receipts_rejected") != panel_modes
            or phase7_summary.get("strategy_reviewer_group_mutations_rejected")
            != 3 * strategy_group_modes
            or reviewer_negative_count
            != 2 * (evaluator_modes + panel_modes) + 3 * strategy_group_modes
            or len(polisher_results) != 1
            or polisher_results[0].get("final_state")
            != "human_strategy_selection_required"
            or polisher_results[0].get("writer_skill") is not None
            or polisher_results[0].get("panel_skill") is not None
            or polisher_results[0].get("synthetic_panel_receipt_ids") != []
            or len(
                polisher_results[0].get(
                    "synthetic_strategy_reviewer_receipt_ids", []
                )
            )
            != 3
            or phase7_summary.get(
                "synthetic_strategy_reviewer_receipts_validated"
            )
            != strategy_receipt_total
            or phase7_summary.get(
                "human_strategy_selection_required_modes"
            )
            != 1
            or phase7_summary.get(
                "research_polisher_routing_boundaries_verified"
            )
            != 7
            or phase7_summary.get(
                "research_polisher_takeover_mutations_rejected"
            )
            != 6
            or phase7_summary.get("negative_guards_rejected")
            != len(negative_results)
            or len(negative_results) != entry_negative_count + reviewer_negative_count
            or phase7_summary.get("false_ready_count") != 0
            or phase7_summary.get("automatic_external_submission") is not False
            or phase7_summary.get("live_model_runs_claimed") != runtime_verified
            or phase7.get("evidence_class") != expected_phase7_evidence_class
            or phase7.get("execution_kind") != expected_phase7_execution_kind
            or phase7.get("live_model_execution")
            is not args.require_phase78_complete_preview
            or phase7.get("state_advance_order")
            != "validate_qualifying_receipt_then_validate_registry_prerequisites_then_commit_derived_state_then_execute_transition"
        ):
            errors.append("Phase 7 mode and runtime evidence coverage is incomplete")
        if (
            not isinstance(runtime_results, list)
            or len(runtime_results) != 10
            or expected_runtime_pairs != actual_runtime_pairs
            or runtime_verified + runtime_pending != 10
            or runtime_receipts.get("expected_receipt_count") != 10
            or runtime_receipts.get("verified_receipt_count") != runtime_verified
            or runtime_receipts.get("pending_receipt_count") != runtime_pending
            or runtime_receipts.get("live_evidence_claimed") is not (runtime_verified > 0)
            or phase7_summary.get("runtime_receipts_expected") != 10
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
                "integrity_only_result_promoted_without_attestation",
                "single_screenshot_without_raw_export",
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
                "accepted_platform_capture_adapter", {}
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
                phase7_platform_trust.get(
                    "supported_preview_attestation_adapter_ids"
                ),
                list,
            )
            or not isinstance(
                phase7_platform_trust.get("supported_authenticated_adapter_ids"),
                list,
            )
            or completion_gates.get(
                "five_current_version_live_happy_paths", {}
            ).get("status")
            != ("verified" if runtime_happy_verified == 5 else "pending")
            or completion_gates.get(
                "five_current_version_valid_control_paths", {}
            ).get("status")
            != ("verified" if runtime_control_verified == 5 else "pending")
            or not isinstance(phase7.get("pending_gates"), list)
            or len(phase7.get("pending_gates", [])) != len(derived_pending_gates)
            or set(phase7.get("pending_gates", [])) != set(derived_pending_gates)
            or phase7_summary.get("completion_gates_verified")
            != len(completion_gates) - len(derived_pending_gates)
            or phase7_summary.get("completion_gates_pending")
            != len(derived_pending_gates)
            or phase7.get("phase_status") != expected_phase7_status
            or phase7_verification_level
            not in {None, "preview_attested", "provider_verified"}
            or phase7.get("provider_verified")
            is not (phase7_verification_level == "provider_verified")
            or phase7.get("counts_as_preview_acceptance")
            is not (
                not derived_pending_gates
                and phase7_verification_level
                in {"preview_attested", "provider_verified"}
            )
            or phase7_platform_trust.get("accepted_verification_level")
            != phase7_verification_level
            or any(
                isinstance(result, dict)
                and result.get("status") == "verified"
                and result.get("verification_level")
                != phase7_verification_level
                for result in runtime_results
            )
            or (
                phase7.get("phase_status")
                in {"complete_preview_attested", "complete_provider_verified"}
                and runtime_verified != 10
            )
            or reachability.get("status") != "passed"
            or reachability.get("evidence_kind")
            != "synthetic_gate_logic_self_test_only"
            or reachability.get("counts_as_runtime_evidence") is not False
            or reachability.get("verification_levels", {})
            .get("preview_attested", {})
            .get("derived_phase_status")
            != "complete_preview_attested"
            or reachability.get("verification_levels", {})
            .get("preview_attested", {})
            .get("provider_verified")
            is not False
            or reachability.get("verification_levels", {})
            .get("preview_attested", {})
            .get("counts_as_runtime_evidence")
            is not False
            or reachability.get("verification_levels", {})
            .get("preview_attested", {})
            .get("verified_gate_count")
            != len(completion_gates)
            or reachability.get("verification_levels", {})
            .get("provider_verified", {})
            .get("derived_phase_status")
            != "complete_provider_verified"
            or reachability.get("verification_levels", {})
            .get("provider_verified", {})
            .get("provider_verified")
            is not True
            or reachability.get("verification_levels", {})
            .get("provider_verified", {})
            .get("counts_as_runtime_evidence")
            is not False
            or reachability.get("verification_levels", {})
            .get("provider_verified", {})
            .get("verified_gate_count")
            != len(completion_gates)
            or {
                "bare_boolean_gate_override",
                "forged_attestation_capability",
            }
            - {
                guard.get("mutation")
                for guard in reachability.get("capability_negative_guards", [])
                if isinstance(guard, dict)
                and guard.get("status") == "rejected_as_expected"
            }
        ):
            errors.append("Phase 7 runtime receipt or completion-gate accounting is invalid")

    phase8: dict[str, object] | None = None
    phase8_path = PLUGIN / "reports" / "phase8-corpus-results.json"
    if not phase8_path.is_file():
        errors.append("Phase 8 corpus report is missing")
    else:
        recorded_phase8 = json.loads(phase8_path.read_text(encoding="utf-8"))
        if args.require_phase78_complete_preview:
            # See the Phase 7 note above: accepted state comes from the protected
            # same-process live bridge, never from a serialized replay capability.
            phase8 = (
                dict(_accepted_phase78_reports[1])
                if _accepted_phase78_reports is not None
                else recorded_phase8
            )
            if _accepted_phase78_reports is not None and recorded_phase8 != phase8:
                errors.append(
                    "Phase 8 report file differs from the same-process live report"
                )
        else:
            phase8 = build_phase8_report()
            if recorded_phase8 != phase8:
                errors.append("Phase 8 report differs from a fresh validator replay")
        corpus = phase8.get("corpus", {})
        live_repeat = phase8.get("live_fresh_repeat", {})
        retrieval = phase8.get("retrieval", {})
        claims = phase8.get("claims", {})
        acceptance_status = phase8.get("acceptance_status", {})
        provider_trust = phase8.get("provider_trust", {})
        validator_self_tests = phase8.get("validator_self_tests", {})
        preview_adapter_count = provider_trust.get("preview_adapter_count", 0)
        provider_adapter_count = provider_trust.get("real_adapter_count", 0)
        phase8_status = phase8.get("phase_status")
        required_distribution = {
            "search": 3,
            "deep_research_completed": 2,
            "deep_research_inactive_control": 1,
        }
        required_receipts = sum(required_distribution.values())
        provider_by_kind = retrieval.get("completed_current_receipts_by_kind", {})
        preview_by_kind = retrieval.get(
            "preview_attested_current_receipts_by_kind", {}
        )
        observed_by_kind = retrieval.get("observed_unverified_receipts_by_kind", {})
        durable_retrieval_guards = retrieval.get(
            "durable_provenance_negative_guards", []
        )
        durable_live_guards = live_repeat.get(
            "durable_binding_negative_guards", []
        )
        provider_receipts = retrieval.get("completed_current_receipts", 0)
        preview_receipts = retrieval.get("preview_attested_current_receipts", 0)
        observed_receipts = retrieval.get("observed_unverified_receipts", 0)
        historical_receipts = retrieval.get(
            "historical_release_mismatch_receipts", 0
        )
        pending_receipts = retrieval.get("pending_receipts", 0)
        stale_receipts = retrieval.get("stale_receipts", 0)
        provider_reviews = live_repeat.get(
            "provider_verified_live_review_count", 0
        )
        preview_reviews = live_repeat.get("preview_attested_review_count", 0)
        preview_or_provider_reviews = preview_reviews + provider_reviews
        expected_live_status = (
            "provider_verified"
            if provider_reviews == 6
            else "preview_attested"
            if preview_reviews == 6
            else "historical_release_mismatch"
            if live_repeat.get("historical_release_mismatch") is True
            else "observed_unverified"
        )
        provider_live_gate_complete = (
            provider_reviews == 6
            and live_repeat.get("verified_live_gate_status") == "completed"
            and live_repeat.get("status") == "provider_verified"
        )
        preview_live_gate_complete = (
            preview_or_provider_reviews == 6
            and live_repeat.get("preview_gate_status") == "completed"
            and live_repeat.get("status")
            in {"preview_attested", "provider_verified"}
        )
        provider_retrieval_gate_complete = (
            provider_by_kind == required_distribution
            and provider_receipts == required_receipts
            and retrieval.get("status") == "completed"
        )
        combined_retrieval_by_kind = {
            kind: provider_by_kind.get(kind, 0) + preview_by_kind.get(kind, 0)
            for kind in required_distribution
        }
        preview_retrieval_gate_complete = (
            combined_retrieval_by_kind == required_distribution
            and provider_receipts + preview_receipts == required_receipts
            and retrieval.get("preview_gate_status") == "completed"
        )
        provider_acceptance_complete = (
            provider_live_gate_complete and provider_retrieval_gate_complete
        )
        preview_acceptance_complete = (
            preview_live_gate_complete and preview_retrieval_gate_complete
        )
        expected_phase8_status = (
            "complete_provider_verified"
            if provider_acceptance_complete
            else "complete_preview_attested"
            if preview_acceptance_complete
            else "in_progress"
        )
        accepted_verification_level = (
            "provider_verified"
            if provider_acceptance_complete
            else "preview_attested"
            if preview_acceptance_complete
            else None
        )
        if phase8.get("plugin_version") != version:
            errors.append("Phase 8 report version differs from the plugin")
        if phase8_status not in {
            "in_progress",
            "complete_preview_attested",
            "complete_provider_verified",
        }:
            errors.append("Phase 8 report has no valid phase status")
        if (
            corpus.get("case_count", 0)
            < 4 * len(registry.get("workflow_state_machines", {}))
            or corpus.get("research_polisher_domain_coverage")
            != {
                "basic_experimental": 1,
                "clinical_or_observational": 1,
                "computational_or_engineering": 1,
                "qualitative_or_mixed_methods": 1,
            }
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
            or live_repeat.get("observed_review_snapshot_count") not in {0, 6}
            or (
                live_repeat.get("historical_release_mismatch") is True
                and live_repeat.get("historical_release_mismatch_snapshot_count") != 6
            )
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
            or provider_reviews not in {0, 6}
            or preview_reviews not in {0, 6}
            or preview_or_provider_reviews not in {0, 6}
            or live_repeat.get("verified_live_review_count") != provider_reviews
            or live_repeat.get("provider_verified_slots_pending")
            != 6 - provider_reviews
            or live_repeat.get("preview_verifier_adapter_count")
            != preview_adapter_count
            or live_repeat.get("provider_verifier_adapter_count")
            != provider_adapter_count
            or live_repeat.get("status") != expected_live_status
            or live_repeat.get("preview_gate_status")
            != (
                "completed"
                if preview_or_provider_reviews == 6
                else "pending_preview_attested_execution_evidence"
            )
            or live_repeat.get("verified_live_gate_status")
            != (
                "completed"
                if provider_reviews == 6
                else "pending_provider_verified_execution_evidence"
            )
            or (
                preview_or_provider_reviews == 0
                and (
                    live_repeat.get("status")
                    not in {"observed_unverified", "historical_release_mismatch"}
                    or live_repeat.get("preview_gate_status")
                    != "pending_preview_attested_execution_evidence"
                )
            )
            or (
                provider_reviews == 0
                and live_repeat.get("verified_live_gate_status")
                != "pending_provider_verified_execution_evidence"
            )
            or (provider_reviews == 6 and not provider_live_gate_complete)
            or (
                preview_or_provider_reviews == 6
                and not preview_live_gate_complete
            )
            or retrieval.get("required_distribution") != required_distribution
            or retrieval.get("required_receipt_count") != required_receipts
            or provider_receipts != sum(provider_by_kind.values())
            or preview_receipts != sum(preview_by_kind.values())
            or observed_receipts != sum(observed_by_kind.values())
            or provider_receipts
            + preview_receipts
            + observed_receipts
            + historical_receipts
            + pending_receipts
            + stale_receipts
            != required_receipts
            or retrieval.get("provider_verified_slots_pending")
            != required_receipts - provider_receipts
            or retrieval.get("preview_verifier_adapter_count")
            != preview_adapter_count
            or retrieval.get("provider_verifier_adapter_count")
            != provider_adapter_count
            or retrieval.get("durable_provenance_negative_guard_count") != 44
            or len(durable_retrieval_guards) != 44
            or any(not isinstance(guard, dict) for guard in durable_retrieval_guards)
            or any(
                guard.get("status") != "rejected"
                or guard.get("error_code")
                not in {
                    "retrieval_durable_provenance",
                    "retrieval_durable_query_binding",
                    "retrieval_durable_binding",
                    "retrieval_verified_evidence_class",
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
            or sum(
                guard.get("error_code") == "retrieval_verified_evidence_class"
                for guard in durable_retrieval_guards
                if isinstance(guard, dict)
            )
            != 3
            or retrieval.get("status")
            != (
                "completed"
                if provider_receipts == required_receipts and stale_receipts == 0
                else "pending_provider_verified_evidence"
            )
            or retrieval.get("preview_gate_status")
            != (
                "completed"
                if provider_receipts + preview_receipts == required_receipts
                and stale_receipts == 0
                else "pending_preview_attested_evidence"
            )
            or claims.get("live_fresh_evaluator_repeats_counted_as_pass")
            != provider_reviews
            or claims.get("preview_attested_reviewer_receipts")
            != preview_reviews
            or claims.get("provider_verified_reviewer_slots_pending")
            != 6 - provider_reviews
            or claims.get("live_search_receipts_counted_as_pass")
            != provider_by_kind.get("search", 0)
            or claims.get("preview_attested_retrieval_receipts")
            != preview_receipts
            or claims.get("provider_verified_retrieval_slots_pending")
            != required_receipts - provider_receipts
            or claims.get("deep_research_cycles_claimed_without_receipts") != 0
            or claims.get("repository_authored_files_counted_as_verified")
            is not False
            or claims.get("synthetic_preview_contract_counts_as_real_evidence")
            is not False
            or not isinstance(preview_adapter_count, int)
            or preview_adapter_count < 1
            or not isinstance(provider_adapter_count, int)
            or provider_adapter_count < 0
            or (provider_acceptance_complete and provider_adapter_count < 1)
            or provider_trust.get("repository_authored_files_are_trust_anchors")
            is not False
            or provider_trust.get("synthetic_override_counts_as_runtime_evidence")
            is not False
            or validator_self_tests.get("counts_as_runtime_evidence") is not False
            or validator_self_tests.get("naked_boolean_override_rejected") is not True
            or validator_self_tests.get("arbitrary_external_root_rejected") is not True
            or validator_self_tests.get("expired_capability_rejected") is not True
            or validator_self_tests.get("phase8_acceptance_state_machine", {})
            .get("states")
            != {
                "none": "in_progress",
                "preview": "complete_preview_attested",
                "provider": "complete_provider_verified",
            }
            or validator_self_tests.get("phase8_acceptance_state_machine", {})
            .get("inconsistent_promotion_rejected")
            is not True
        ):
            errors.append("Phase 8 corpus or evidence accounting is incomplete")
        if (
            phase8_status != expected_phase8_status
            or claims.get("preview_gate_complete")
            is not preview_acceptance_complete
            or claims.get("provider_gate_complete")
            is not provider_acceptance_complete
            or claims.get("preview_phase8_acceptance_complete")
            is not preview_acceptance_complete
            or claims.get("preview_attested_phase8_complete")
            is not (
                preview_acceptance_complete and not provider_acceptance_complete
            )
            or claims.get("provider_verified_phase8_complete")
            is not provider_acceptance_complete
            or claims.get("accepted_verification_level")
            != accepted_verification_level
            or claims.get("phase8_complete")
            is not (phase8_status != "in_progress")
            or acceptance_status.get("preview_attested")
            != (
                "complete"
                if preview_acceptance_complete
                else "pending_real_preview_attested_slots"
            )
            or acceptance_status.get("provider_verified")
            != (
                "complete"
                if provider_acceptance_complete
                else "pending_strict_provider_evidence"
            )
        ):
            errors.append("Phase 8 pending status is inconsistent with its evidence gates")

    if args.require_phase78_complete_preview:
        if phase7 is None or phase8 is None:
            errors.append(
                "protected Preview completion requires both Phase 7 and Phase 8 reports"
            )
        else:
            try:
                strict_phase78_snapshot(phase7, phase8)
            except AcceptedSummaryError as exc:
                errors.append(f"protected Phase 7-8 completion gate failed: {exc}")

    ledger_path = PLUGIN / "reports" / "release-ledger.json"
    if not ledger_path.is_file():
        errors.append("machine-readable release ledger is missing")
    else:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        release = ledger.get("release", {})
        if release.get("version") != version:
            errors.append("release ledger version differs from the plugin")
        ledger_evidence_errors: list[str] = []
        if live_evidence_verifier is not None:
            try:
                live_evidence_verifier.prepare_ledger(ledger)
            except (OSError, ReleaseEvidenceRunnerError) as exc:
                ledger_evidence_errors.append(
                    "production live evidence preparation failed: "
                    f"{type(exc).__name__}: {exc}"
                )
        validate_release_evidence(
            release,
            version,
            expected_skill_count,
            ledger_evidence_errors,
            authenticated_external_adapter=(
                authenticated_external_evidence_adapter_available(release)
            ),
            expected_explicit_entries=sorted(public_entry_names),
            expected_implicit_entries=sorted(implicit_entry_names),
            live_evidence_verifier=live_evidence_verifier,
            defer_live_external_requery=(live_evidence_verifier is None),
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
                    live_evidence_verifier=live_evidence_verifier,
                    defer_live_external_requery=(live_evidence_verifier is None),
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
        if live_evidence_verifier is not None and not ledger_evidence_errors:
            try:
                live_evidence_verifier.assert_complete()
            except ReleaseEvidenceRunnerError as exc:
                ledger_evidence_errors.append(
                    "production live evidence coverage failed: "
                    f"{type(exc).__name__}: {exc}"
                )
        errors.extend(
            f"release ledger evidence invalid: {error}"
            for error in ledger_evidence_errors
        )
        if phase7_path.is_file():
            if args.require_phase78_complete_preview:
                try:
                    if phase7_gate_evidence_verifier is None:
                        raise ReleaseEvidenceRunnerError(
                            "live_verifier_missing",
                            "strict Phase 7 release gates require a fresh production callback",
                        )
                    phase7_gate_evidence_verifier.prepare_ledger(ledger)
                    expected_release_gates = release_gate_statuses(
                        ledger,
                        registry,
                        live_evidence_verifier=phase7_gate_evidence_verifier,
                    )
                    phase7_gate_evidence_verifier.assert_complete()
                except (OSError, ReleaseEvidenceRunnerError, ValueError) as exc:
                    errors.append(
                        "strict Phase 7 release-gate live re-query failed: "
                        f"{type(exc).__name__}: {exc}"
                    )
                    expected_release_gates = {}
            else:
                expected_release_gates = release_gate_statuses(ledger, registry)
            reported_release_gates = {
                gate_id: phase7.get("completion_gates", {}).get(gate_id)
                for gate_id in expected_release_gates
            }
            if reported_release_gates != expected_release_gates:
                errors.append(
                    "Phase 7 release completion gates differ from durable ledger evidence"
                )
        if phase7_path.is_file() and phase7.get("phase_status") in {
            "complete_preview_attested",
            "complete_provider_verified",
        }:
            canonical = release.get("ci", {}).get("canonical_plugin_validator", {})
            phase7_internal_records = (
                release.get("source_commit", {}),
                canonical.get("local", {}),
            )
            phase7_external_records = (
                release.get("ci", {}).get("repository_preview", {}),
                canonical.get("ci", {}),
                release.get("governance", {}).get("main_branch_protection", {}),
                release.get("marketplace_source", {}).get("resolved_commit", {}),
                release.get("receipts", {}).get("marketplace_upgrade", {}),
                release.get("receipts", {}).get("explicit_reinstall", {}),
                release.get("receipts", {}).get("fresh_task_discovery", {}),
                release.get("receipts", {}).get("rollback", {}),
            )
            phase7_external_level = phase7.get("verification_level")
            if phase7.get("pending_gates") or any(
                record.get("status") != "verified"
                for record in phase7_internal_records
                if isinstance(record, dict)
            ) or any(
                record.get("status") != phase7_external_level
                for record in phase7_external_records
                if isinstance(record, dict)
            ) or configured_external_evidence_level(release) != phase7_external_level:
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
        for marker, label in (
            (
                "4ebc61c0f8df9852e709ff4b477b750fc816a69b",
                "pinned OpenAI Codex validator source commit",
            ),
            (
                "4e84c911479e4d158d723ed8ccc881d3499e580fbf5650e60d379a1a25ac3186",
                "canonical validator source digest",
            ),
            ("sha256sum --check --strict", "canonical validator digest check"),
            (
                'python "$OPENAI_CODEX_VALIDATOR_PATH" research-skills-openai',
                "canonical OpenAI plugin validator execution",
            ),
        ):
            if marker not in workflow:
                errors.append(f"CI workflow missing {label}")
        for command in (
            "audit_openai_research_plugin.py",
            "test_openai_release_contract.py",
            "sync_openai_fixture_versions.py",
            "test_openai_phase2_phase3.py",
            "test_openai_phase4_scenarios.py --check-report",
            "test_openai_phase6_context.py",
            "test_openai_phase7_modes.py --check-report",
            "test_openai_phase8_corpus.py --check-report",
            "test_openai_preview_evidence.py",
            "test_build_openai_preview_verifier_summary.py",
            "test_download_openai_release_ledger_assets.py",
            "test_validate_openai_preview_evidence_bundle.py",
            "test_openai_app_server_capture.py",
            "test_validate_openai_phase7_runtime_evidence.py",
            "test_validate_openai_phase8_external_evidence.py",
            "test_validate_openai_release_evidence.py",
            "test_openai_phase8_preview_verifier.py",
            "test_openai_preview_workflows.py",
            "codex_plugin_converter.py --mode codex --fail-on-invalid",
            "generate_openai_release_ledger.py --check",
            "test_openai_release_ledger.py",
            "validate_openai_preview_release.py",
            "check_openai_version_bump.py",
        ):
            if command not in workflow:
                errors.append(f"CI workflow missing command: {command}")

    evidence_workflow_path = (
        REPO / ".github" / "workflows" / "openai-preview-evidence.yml"
    )
    if not evidence_workflow_path.is_file():
        errors.append("GitHub Actions Preview evidence workflow is missing")
    else:
        evidence_workflow = evidence_workflow_path.read_text(encoding="utf-8")
        evidence_action_refs = re.findall(
            r"^[ \t]*(?:-[ \t]+)?uses:[ \t]+([^@\s]+)@([^\s#]+)",
            evidence_workflow,
            re.MULTILINE,
        )
        if not evidence_action_refs:
            errors.append("Preview evidence workflow contains no pinned actions")
        elif any(
            not re.fullmatch(r"[0-9a-f]{40}", ref)
            for _, ref in evidence_action_refs
        ):
            errors.append(
                "Preview evidence workflow action dependencies are not pinned to immutable commits"
            )
        for marker, label in (
            ("workflow_dispatch:", "manual immutable-asset trigger"),
            ("fetch-depth: 0", "full source history checkout"),
            ("fetch-tags: true", "immutable release tag checkout"),
            ("persist-credentials: false", "credential-minimized checkout"),
            (
                "generate_openai_release_ledger.py --check",
                "source-identity ledger check",
            ),
            (
                "validate_openai_preview_evidence_bundle.py",
                "offline integrity-only validator",
            ),
            (
                "tests/openai_phase8/verify_preview_evidence.py",
                "live GitHub Preview verifier",
            ),
            (
                "validate_openai_phase8_external_evidence.py",
                "Phase 8 twelve-slot external semantic runner",
            ),
            (
                "build_openai_preview_verifier_summary.py",
                "historical live-verifier run-summary builder",
            ),
            (
                "openai-preview-live-verifier-summary-${{ github.run_id }}",
                "run-bound verifier summary artifact",
            ),
            ("gate_eligible\") is False", "offline non-promotion assertion"),
            (
                "counts_as_preview_attested\") is True",
                "Preview-attested acceptance assertion",
            ),
            (
                "counts_as_provider_verified\") is True",
                "provider-promotion rejection assertion",
            ),
            ("provider==0", "zero provider-verification assertion"),
        ):
            if marker not in evidence_workflow:
                errors.append(
                    f"Preview evidence workflow missing {label}: {marker}"
                )

    accepted_workflow_path = (
        REPO / ".github" / "workflows" / "openai-preview-accepted-evidence.yml"
    )
    if not accepted_workflow_path.is_file():
        errors.append("GitHub Actions protected accepted-state workflow is missing")
    else:
        accepted_workflow = accepted_workflow_path.read_text(encoding="utf-8")
        accepted_action_refs = re.findall(
            r"^[ \t]*(?:-[ \t]+)?uses:[ \t]+([^@\s]+)@([^\s#]+)",
            accepted_workflow,
            re.MULTILINE,
        )
        if not accepted_action_refs:
            errors.append("protected accepted-state workflow contains no pinned actions")
        elif any(
            not re.fullmatch(r"[0-9a-f]{40}", ref)
            for _, ref in accepted_action_refs
        ):
            errors.append(
                "protected accepted-state workflow action dependencies are not pinned"
            )
        for marker, label in (
            ("workflow_dispatch:", "manual accepted-state trigger"),
            ("evidence_release_tag:", "separate immutable evidence release"),
            ("candidate_release_tag:", "separate immutable candidate release"),
            ("name: openai-preview-governance", "protected governance environment"),
            (
                "secrets.OPENAI_PREVIEW_GOVERNANCE_TOKEN",
                "protected governance credential",
            ),
            (
                "download_openai_release_ledger_assets.py",
                "accepted historical-release bundle downloader",
            ),
            (
                "validate_openai_release_evidence.py",
                "standalone production live release verifier",
            ),
            (
                "validate_openai_preview_accepted_phase78.py",
                "same-process Phase 7/8 and complete release validator bridge",
            ),
            (
                "--phase7-asset-index-pattern",
                "separate ten-slot Phase 7 evidence selection",
            ),
            (
                "--phase8-asset-index-pattern",
                "separate twelve-slot Phase 8 evidence selection",
            ),
            (
                "build_openai_preview_accepted_summary.py",
                "run-bound accepted-state summary builder",
            ),
            (
                "openai-preview-accepted-summary-${{ github.run_id }}-${{ github.run_attempt }}",
                "non-overwriting accepted-state summary artifact",
            ),
            ("git clone --no-hardlinks", "isolated trusted workspace"),
            ("data.get(\"immutable\") is True", "immutable Release API check"),
            (
                "candidate asset directory must remain outside the evidence bundle root",
                "candidate/evidence bundle separation",
            ),
        ):
            if marker not in accepted_workflow:
                errors.append(
                    f"protected accepted-state workflow missing {label}: {marker}"
                )

    readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
    roadmap = (PLUGIN / "ROADMAP.md").read_text(encoding="utf-8")
    if f"contains {expected_skill_count} skills" not in readme:
        errors.append("README skill-count claim differs from registry discovery")
    quickstart_names = set(re.findall(r"^### `\$([^`]+)`[ \t]*$", readme, re.MULTILINE))
    if quickstart_names != public_entry_names:
        errors.append(
            "README quickstart/public-entry mismatch: "
            f"missing={sorted(public_entry_names - quickstart_names)} "
            f"extra={sorted(quickstart_names - public_entry_names)}"
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
    print(
        "OpenAI Preview release validation passed"
        if live_evidence_verifier is not None
        else "OpenAI Preview release structural validation passed"
    )
    print(f"version: {version}")
    print(f"skills: {expected_skill_count}")
    print("channel: GitHub main Preview")
    print(
        "external evidence: "
        + (
            "production live re-query"
            if live_evidence_verifier is not None
            else "pending/offline validation path"
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
