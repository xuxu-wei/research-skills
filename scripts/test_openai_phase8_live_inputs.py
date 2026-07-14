#!/usr/bin/env python3
"""Validate the scheduler-only Phase 8 canonical live-input pack.

This test proves input integrity and visibility boundaries only. It never runs
a reviewer, Search, or Deep Research task and cannot produce live evidence.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "tests" / "openai_phase8" / "live-inputs"
MANIFEST = PACK / "manifest.yaml"
REGISTRY = REPO / "research-skills-openai" / "workflow-registry.yaml"
PLUGIN_MANIFEST = REPO / "research-skills-openai" / ".codex-plugin" / "plugin.json"

EXPECTED_SLOTS = {
    "phase8-reviewer-a01-r1": ("p8-l01", "reviewer", "a01", "independent_review", "phase8-reviewer-v1", "proposal-readiness-triage"),
    "phase8-reviewer-a01-r2": ("p8-l02", "reviewer", "a01", "independent_review", "phase8-reviewer-v1", "proposal-readiness-triage"),
    "phase8-reviewer-a02-r1": ("p8-l03", "reviewer", "a02", "independent_review", "phase8-reviewer-v1", "article-evaluator"),
    "phase8-reviewer-a02-r2": ("p8-l04", "reviewer", "a02", "independent_review", "phase8-reviewer-v1", "article-evaluator"),
    "phase8-reviewer-a03-r1": ("p8-l05", "reviewer", "a03", "independent_review", "phase8-reviewer-v1", "perspective-evaluator"),
    "phase8-reviewer-a03-r2": ("p8-l06", "reviewer", "a03", "independent_review", "phase8-reviewer-v1", "perspective-evaluator"),
    "phase8-search-current": ("p8-l07", "search", "s01", "current", "phase8-search-v1", None),
    "phase8-search-exact": ("p8-l08", "search", "s02", "exact", "phase8-search-v1", None),
    "phase8-search-narrow-academic": ("p8-l09", "search", "s03", "narrow_academic", "phase8-search-v1", None),
    "phase8-deep-research-cycle-1": ("p8-l10", "deep_research_completed", "d01", "multi_stage_evidence_map", "phase8-deep-research-v1", None),
    "phase8-deep-research-cycle-2": ("p8-l11", "deep_research_completed", "d02", "multi_direction_synthesis", "phase8-deep-research-v1", None),
    "phase8-deep-research-inactive-control": ("p8-l12", "deep_research_inactive_control", "d03", "inactive_capability_control", "phase8-deep-research-inactive-v1", None),
}

EXPECTED_DISTRIBUTION = {
    "reviewer": 6,
    "search": 3,
    "deep_research_completed": 2,
    "deep_research_inactive_control": 1,
}

REVIEWER_EXPECTATIONS = {
    "a01": ("blocked", ["data_access_impossible"], []),
    "a02": ("revision_required", ["prespecified_sensitivity_result_omitted"], []),
    "a03": ("pre_panel_eligible", [], ["annual_reassessment_frequency"]),
}

REVIEWER_ORIGINS = {
    "a01": "tests/openai_phase8/live-repeat-inputs/source-a01.md",
    "a02": "tests/openai_phase8/live-repeat-inputs/source-a02.md",
    "a03": "tests/openai_phase8/live-repeat-inputs/source-a03.md",
}

CAPTURE_PROFILES = {
    "phase8-reviewer-v1": {
        "current_source_identity",
        "unique_parent_task_id",
        "unique_delegated_thread_id",
        "reviewer_instance_id_and_created_at",
        "platform_receipt_id",
        "frozen_source_path_digest_before_after",
        "source_only_blind_bundle_path_digest",
        "exact_dispatch_prompt_path_digest",
        "declared_resource_closure",
        "actual_files_read_and_written",
        "raw_transport_output_path_digest",
        "platform_read_write_scope_export_path_digest",
        "reviewer_report_only_write_scope",
        "isolation_mode_fresh_subagent",
        "prior_scores_peer_outputs_and_target_decision_invisible",
        "source_edits_performed_false",
        "reviewer_contract_decision_findings_unresolved_and_dissent",
        "automatic_external_submission_false",
    },
    "phase8-search-v1": {
        "current_source_identity",
        "unique_platform_task_tool_and_run_ids",
        "captured_at_with_timezone",
        "builtin_search_capability",
        "exact_query_and_request_digests",
        "raw_search_output_path_digest",
        "citation_export_path_digest",
        "at_least_two_primary_or_authoritative_sources",
        "opened_source_identity_and_canonical_locator",
        "complete_material_claim_trace",
        "artifact_path_size_and_digest_bindings",
        "local_retrieval_fallback_false",
        "automatic_external_submission_false",
    },
    "phase8-deep-research-v1": {
        "current_source_identity",
        "unique_task_session_and_run_ids",
        "mapper_handoff_path_digest",
        "explicit_user_start_event_path_digest",
        "provider_completed_receipt_id_path_digest_and_status",
        "raw_deep_research_output_path_digest",
        "citation_export_path_digest",
        "mapper_return_receipt_id_and_artifact_path_digest",
        "resume_transaction_id_path_digest",
        "unique_pending_edge_id",
        "identical_evidence_artifact_bindings_on_return_and_resume",
        "strictly_monotonic_five_stage_timestamps",
        "primary_or_authoritative_opened_source_identity",
        "complete_material_claim_trace",
        "inline_simulation_false",
        "automatic_external_submission_false",
    },
    "phase8-deep-research-inactive-v1": {
        "current_source_identity",
        "unique_platform_task_id",
        "capability_state_export_path_digest",
        "mapper_handoff_path_digest",
        "self_contained_continuation_path_digest",
        "unique_pending_edge_id",
        "workflow_paused_true",
        "downstream_evidence_map_created_false",
        "inline_simulation_false",
        "automatic_external_submission_false",
    },
}

TASK_VISIBLE_ORACLES = (
    "expected_review_stage_state",
    "required_critical_finding_labels",
    "required_dissent_labels",
    "expected_completion_status",
    "expected_capability_active",
    "expected_workflow_paused",
    "expected_downstream_evidence_map_created",
    "data_access_impossible",
    "prespecified_sensitivity_result_omitted",
    "annual_reassessment_frequency",
    "search_verified",
    "deep_research_cycle_completed",
    "deep_research_handoff_required",
    "phase8-reviewer-a01-r1",
    "phase8-reviewer-a01-r2",
    "phase8-reviewer-a02-r1",
    "phase8-reviewer-a02-r2",
    "phase8-reviewer-a03-r1",
    "phase8-reviewer-a03-r2",
    "manifest.yaml",
    "corpus.yaml",
    "live-repeat-receipts.yaml",
    "retrieval-receipts.yaml",
)

REVIEWER_CAPTURE_FILES = {
    "capture/task-export.json",
    "capture/source-only-blind-bundle.yaml",
    "capture/dispatch-prompt.yaml",
    "capture/raw-review-output.yaml",
    "capture/read-scope.json",
    "capture/reviewer-run.json",
}

SEARCH_CAPTURE_FILES = {
    "task-export.json",
    "raw-search-output.json",
    "citation-export.json",
    "retrieval-receipt.json",
}

DEEP_RESEARCH_CAPTURE_FILES = {
    "task-export.json",
    "mapper-handoff.yaml",
    "user-start-event.json",
    "provider-completed.json",
    "raw-deep-research-output.json",
    "citation-export.json",
    "mapper-return.yaml",
    "resume-receipt.json",
    "evidence-artifact-index.json",
    "retrieval-receipt.json",
    "continuation-package.yaml",
}

INACTIVE_CAPTURE_FILES = {
    "task-export.json",
    "capability-state-export.json",
    "mapper-handoff.yaml",
    "continuation-package.yaml",
    "retrieval-receipt.json",
}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: expected YAML mapping")
    return value


def digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def resolve_pack_file(value: Any, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value or Path(value).is_absolute():
        errors.append(f"{label}: path must be a canonical repository-relative POSIX path")
        return None
    candidate = (REPO / value).resolve()
    try:
        candidate.relative_to(PACK.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes live-input pack")
        return None
    if not candidate.is_file() or candidate.is_symlink():
        errors.append(f"{label}: missing regular non-symlink file {value}")
        return None
    return candidate


def task_visible_oracle(text: str) -> str | None:
    lowered = text.lower()
    for marker in TASK_VISIBLE_ORACLES:
        if marker.lower() in lowered:
            return marker
    return None


def contains_all(text: str, values: set[str]) -> bool:
    return all(value in text for value in values)


def main() -> int:
    errors: list[str] = []
    manifest = load_yaml(MANIFEST)
    registry = load_yaml(REGISTRY)
    plugin = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))

    require(manifest.get("schema_version") == 1, "manifest schema_version must be 1", errors)
    require(
        manifest.get("evidence_kind") == "scheduler_input_pack_only"
        and manifest.get("counts_as_runtime_evidence") is False,
        "pack must remain explicit scheduler-only non-evidence",
        errors,
    )
    binding = manifest.get("plugin_binding", {})
    require(
        binding.get("plugin_name") == "research-skills-openai"
        and binding.get("plugin_version") == plugin.get("version") == registry.get("plugin_version"),
        "manifest, plugin, and registry versions must agree",
        errors,
    )
    require(
        binding.get("source_commit") == "set_from_frozen_A_at_execution"
        and binding.get("registry_sha256") == "set_from_frozen_A_at_execution"
        and binding.get("skill_tree_sha256") == "set_from_frozen_A_at_execution",
        "frozen-A source identity placeholders are incomplete",
        errors,
    )
    require(
        manifest.get("task_visibility")
        == {
            "scheduler_manifest_visible_to_any_execution": False,
            "scheduler_labels_visible_to_any_execution": False,
            "expected_outcomes_visible_to_any_execution": False,
            "reviewer_launch_prompt_visible_to_delegate": False,
            "reviewer_peer_outputs_visible": False,
            "expected_fields_location": "manifest_only",
        },
        "task/reviewer visibility boundary is incomplete",
        errors,
    )
    profiles = manifest.get("capture_profiles", {})
    require(set(profiles) == set(CAPTURE_PROFILES), "capture profile inventory differs", errors)
    for name, expected_fields in CAPTURE_PROFILES.items():
        actual = profiles.get(name, [])
        require(
            isinstance(actual, list) and len(actual) == len(set(actual)) and set(actual) == expected_fields,
            f"{name}: capture profile fields differ",
            errors,
        )

    slots = manifest.get("slots")
    if not isinstance(slots, list):
        errors.append("manifest slots must be a list")
        slots = []
    by_slot = {
        item.get("slot"): item
        for item in slots
        if isinstance(item, dict) and isinstance(item.get("slot"), str)
    }
    require(len(slots) == 12 and len(by_slot) == 12, "pack must contain 12 unique slots", errors)
    require(set(by_slot) == set(EXPECTED_SLOTS), "slot inventory differs from Phase 8 contract", errors)
    require(
        Counter(str(item.get("kind")) for item in slots if isinstance(item, dict)) == EXPECTED_DISTRIBUTION,
        "slot kind distribution must be reviewer/Search/Deep Research 6/3/2/1",
        errors,
    )

    seen_execution_ids: set[str] = set()
    seen_paths: set[str] = set()
    seen_path_digest_bindings: set[tuple[str, str]] = set()
    prompt_digests: set[str] = set()
    retrieval_input_digests: set[str] = set()
    reviewer_inputs: dict[str, list[bytes]] = defaultdict(list)

    for slot_id, expected in EXPECTED_SLOTS.items():
        slot = by_slot.get(slot_id)
        if not isinstance(slot, dict):
            continue
        execution_id, kind, case_id, question_class, profile, reviewer_skill = expected
        require(
            (
                slot.get("execution_id"),
                slot.get("kind"),
                slot.get("case_id"),
                slot.get("question_class"),
                slot.get("capture_profile"),
                slot.get("reviewer_skill"),
            )
            == expected,
            f"{slot_id}: scheduling contract mismatch",
            errors,
        )
        require(execution_id not in seen_execution_ids, f"{slot_id}: duplicate execution ID", errors)
        require(re.fullmatch(r"p8-l(?:0[1-9]|1[0-2])", execution_id) is not None, f"{slot_id}: execution ID is not opaque", errors)
        seen_execution_ids.add(execution_id)

        input_file = resolve_pack_file(slot.get("input_path"), f"{slot_id}.input_path", errors)
        prompt_file = resolve_pack_file(slot.get("prompt_path"), f"{slot_id}.prompt_path", errors)
        for value in (slot.get("input_path"), slot.get("prompt_path")):
            if isinstance(value, str):
                require(value not in seen_paths, f"{slot_id}: task-visible file path reused", errors)
                seen_paths.add(value)
        if input_file is None or prompt_file is None:
            continue
        require(input_file.name == f"{execution_id}.md", f"{slot_id}: input filename must equal opaque execution ID", errors)
        require(prompt_file.name == f"{execution_id}.md", f"{slot_id}: prompt filename must equal opaque execution ID", errors)

        input_digest = digest(input_file)
        prompt_digest = digest(prompt_file)
        require(slot.get("input_sha256") == input_digest, f"{slot_id}: input SHA-256 drift", errors)
        require(slot.get("prompt_sha256") == prompt_digest, f"{slot_id}: prompt SHA-256 drift", errors)
        for path_value, digest_value in (
            (slot.get("input_path"), input_digest),
            (slot.get("prompt_path"), prompt_digest),
        ):
            binding_pair = (str(path_value), digest_value)
            require(
                binding_pair not in seen_path_digest_bindings,
                f"{slot_id}: task-visible path/digest binding reused",
                errors,
            )
            seen_path_digest_bindings.add(binding_pair)
        require(prompt_digest not in prompt_digests, f"{slot_id}: prompt bytes reused", errors)
        prompt_digests.add(prompt_digest)

        input_text = input_file.read_text(encoding="utf-8")
        prompt_text = prompt_file.read_text(encoding="utf-8")
        for label, text in (("input", input_text), ("prompt", prompt_text)):
            oracle = task_visible_oracle(text)
            require(oracle is None, f"{slot_id}: {label} leaks scheduler oracle {oracle}", errors)
        require(
            700 <= len(prompt_text) <= 2600 and 8 <= len(prompt_text.splitlines()) <= 35,
            f"{slot_id}: prompt exceeds the 700-2600 character / 8-35 line boundary",
            errors,
        )
        normalized_prompt = " ".join(prompt_text.lower().split())
        require(
            "machine-readable" in normalized_prompt
            and "schema_version: 1" in normalized_prompt
            and "never invent" in normalized_prompt
            and "external submission" in normalized_prompt,
            f"{slot_id}: capture or submission boundary missing",
            errors,
        )

        if kind == "reviewer":
            expected_state, critical_labels, dissent_labels = REVIEWER_EXPECTATIONS[case_id]
            require(
                slot.get("repeat_index") in {1, 2}
                and slot.get("expected_review_stage_state") == expected_state
                and slot.get("required_critical_finding_labels") == critical_labels
                and slot.get("required_dissent_labels") == dissent_labels,
                f"{slot_id}: scheduler-only reviewer labels differ",
                errors,
            )
            origin_value = REVIEWER_ORIGINS[case_id]
            origin = (REPO / origin_value).resolve()
            require(slot.get("source_origin_path") == origin_value and origin.is_file(), f"{slot_id}: source origin mismatch", errors)
            if origin.is_file():
                require(input_file.read_bytes() == origin.read_bytes(), f"{slot_id}: reviewer source is not an exact safe copy", errors)
            reviewer_inputs[case_id].append(input_file.read_bytes())
            require(
                slot.get("required_materials") == ["frozen_source", "installed_frozen_A_plugin"],
                f"{slot_id}: reviewer materials differ",
                errors,
            )
            require(
                f"research-skills-openai:{reviewer_skill}" in prompt_text
                and f"`{input_file.name}`" in prompt_text
                and "exactly one fresh delegated reviewer instance" in normalized_prompt
                and "source-only sanitized blind bundle" in normalized_prompt
                and "must not perform the assessment inline" in normalized_prompt
                and "source is read-only" in normalized_prompt
                and "prior scores" in normalized_prompt
                and "other reviewer output" in normalized_prompt,
                f"{slot_id}: source-only fresh-delegation boundary missing",
                errors,
            )
            require(
                contains_all(prompt_text, REVIEWER_CAPTURE_FILES)
                and f"runtime-artifacts/reviews/{execution_id}/report.yaml" in prompt_text,
                f"{slot_id}: reviewer capture artifacts or write boundary incomplete",
                errors,
            )
        else:
            require(input_digest not in retrieval_input_digests, f"{slot_id}: retrieval input bytes reused", errors)
            retrieval_input_digests.add(input_digest)
            require(slot.get("reviewer_skill") is None, f"{slot_id}: retrieval slot declares reviewer", errors)

        if kind == "search":
            require(
                slot.get("capability") == "chatgpt_codex_builtin_search"
                and slot.get("expected_completion_status") == "search_verified"
                and slot.get("expected_minimum_opened_sources") == 2
                and slot.get("required_source_flags") == ["primary_or_authoritative", "identity_verified"],
                f"{slot_id}: Search scheduling contract differs",
                errors,
            )
            require(
                slot.get("required_materials") == ["frozen_request", "installed_frozen_A_plugin", "builtin_search_active"],
                f"{slot_id}: Search materials differ",
                errors,
            )
            require(
                "chatgpt/codex built-in search" in normalized_prompt
                and "do not substitute a local retrieval script" in normalized_prompt
                and "at least two identity-verified primary or authoritative sources" in normalized_prompt
                and "map every material claim" in normalized_prompt
                and "actual tool trace" in normalized_prompt
                and contains_all(prompt_text, SEARCH_CAPTURE_FILES),
                f"{slot_id}: native Search or source-traceability boundary missing",
                errors,
            )

        if kind == "deep_research_completed":
            require(
                slot.get("public_entry") == "research-opportunity-mapper"
                and slot.get("capability") == "chatgpt_deep_research"
                and slot.get("expected_completion_status") == "deep_research_cycle_completed"
                and slot.get("expected_minimum_opened_sources") == 2
                and slot.get("required_source_flags") == ["primary_or_authoritative", "identity_verified"],
                f"{slot_id}: completed Deep Research scheduling contract differs",
                errors,
            )
            require(
                slot.get("required_materials") == ["frozen_request", "installed_frozen_A_plugin", "user_started_deep_research"],
                f"{slot_id}: Deep Research materials differ",
                errors,
            )
            require(
                "research-skills-openai:research-opportunity-mapper" in prompt_text
                and "the user must explicitly start deep research" in normalized_prompt
                and "do not perform, imitate, or summarize the multi-stage research inline" in normalized_prompt
                and "provider run has completed" in normalized_prompt
                and "resume exactly the recorded edge once" in normalized_prompt
                and "strictly ordered" in normalized_prompt
                and contains_all(prompt_text, DEEP_RESEARCH_CAPTURE_FILES),
                f"{slot_id}: real handoff-completion-return-resume boundary missing",
                errors,
            )
            require(
                normalized_prompt.index("the user must explicitly start deep research")
                < normalized_prompt.index("provider run has completed")
                < normalized_prompt.index("resume exactly the recorded edge once"),
                f"{slot_id}: Deep Research event instructions are out of order",
                errors,
            )

        if kind == "deep_research_inactive_control":
            require(
                slot.get("public_entry") == "research-opportunity-mapper"
                and slot.get("capability") == "chatgpt_deep_research"
                and slot.get("expected_completion_status") == "deep_research_handoff_required"
                and slot.get("expected_capability_active") is False
                and slot.get("expected_workflow_paused") is True
                and slot.get("expected_downstream_evidence_map_created") is False,
                f"{slot_id}: inactive scheduling contract differs",
                errors,
            )
            require(
                slot.get("required_materials") == ["frozen_request", "installed_frozen_A_plugin", "deep_research_inactive_or_unavailable"],
                f"{slot_id}: inactive materials differ",
                errors,
            )
            require(
                "inspect the actual deep research capability state" in normalized_prompt
                and "inactive, unavailable, or cannot be started" in normalized_prompt
                and "continuation package" in normalized_prompt
                and "pause" in normalized_prompt
                and "do not perform, imitate, or summarize deep research inline" in normalized_prompt
                and "do not create a downstream evidence map" in normalized_prompt
                and contains_all(prompt_text, INACTIVE_CAPTURE_FILES),
                f"{slot_id}: inactive capability stop boundary missing",
                errors,
            )

    require(len(seen_execution_ids) == 12 and len(seen_paths) == 24, "execution IDs or task-visible paths are not unique", errors)
    require(len(seen_path_digest_bindings) == 24, "task-visible path/digest bindings are not unique", errors)
    require(len(prompt_digests) == 12, "all 12 launch prompts must have unique bytes", errors)
    require(len(retrieval_input_digests) == 6, "all six retrieval inputs must have unique bytes", errors)
    for case_id in ("a01", "a02", "a03"):
        copies = reviewer_inputs.get(case_id, [])
        require(len(copies) == 2 and copies[0] == copies[1], f"{case_id}: repeat source bytes must be identical", errors)
    require(
        len({hashlib.sha256(reviewer_inputs[case_id][0]).hexdigest() for case_id in ("a01", "a02", "a03") if reviewer_inputs.get(case_id)}) == 3,
        "A01-A03 canonical source digests must remain distinct",
        errors,
    )

    expected_files = {f"p8-l{number:02d}.md" for number in range(1, 13)}
    actual_inputs = {path.name for path in (PACK / "inputs").glob("*.md")}
    actual_prompts = {path.name for path in (PACK / "prompts").glob("*.md")}
    require(actual_inputs == expected_files, "input directory must contain exactly 12 opaque files", errors)
    require(actual_prompts == expected_files, "prompt directory must contain exactly 12 opaque files", errors)

    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "valid": True,
                "pack_id": manifest.get("pack_id"),
                "plugin_version": binding.get("plugin_version"),
                "slots": len(slots),
                "distribution": EXPECTED_DISTRIBUTION,
                "unique_task_visible_paths": len(seen_paths),
                "unique_path_digest_bindings": len(seen_path_digest_bindings),
                "unique_prompt_digests": len(prompt_digests),
                "unique_retrieval_input_digests": len(retrieval_input_digests),
                "reviewer_repeat_source_pairs": 3,
                "capture_profiles": len(CAPTURE_PROFILES),
                "runtime_evidence": False,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
