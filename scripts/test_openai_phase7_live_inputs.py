#!/usr/bin/env python3
"""Validate the scheduler-only Phase 7 canonical live-input pack.

This is a static input-integrity test. It does not execute a workflow, attest a
platform task, or produce a runtime receipt.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "tests" / "openai_phase7" / "live-inputs"
MANIFEST = PACK / "manifest.yaml"
REGISTRY = REPO / "research-skills-openai" / "workflow-registry.yaml"
PLUGIN_MANIFEST = REPO / "research-skills-openai" / ".codex-plugin" / "plugin.json"

EXPECTED_SLOTS = {
    "phase7-idea-happy": (
        "p7-l01",
        "idea",
        "happy",
        "research-idea-orchestrator",
        "standard",
        "human_signoff_required",
        None,
    ),
    "phase7-idea-control": (
        "p7-l02",
        "idea",
        "control",
        "research-idea-orchestrator",
        "standard",
        "stopped",
        "independent_review_no_incremental_gain",
    ),
    "phase7-proposal-happy": (
        "p7-l03",
        "proposal",
        "happy",
        "proposal-orchestrator",
        "standard",
        "human_signoff_required",
        None,
    ),
    "phase7-proposal-control": (
        "p7-l04",
        "proposal",
        "control",
        "proposal-orchestrator",
        "existing_draft",
        "blocked",
        "fatal_data_availability_constraint",
    ),
    "phase7-article-happy": (
        "p7-l05",
        "article",
        "happy",
        "article-orchestrator",
        "standard",
        "human_signoff_required",
        None,
    ),
    "phase7-article-control": (
        "p7-l06",
        "article",
        "control",
        "article-orchestrator",
        "fast_track_draft",
        "blocked",
        "source_level_fatal_finding",
    ),
    "phase7-perspective-happy": (
        "p7-l07",
        "perspective",
        "happy",
        "perspective-orchestrator",
        "full",
        "human_signoff_required",
        None,
    ),
    "phase7-perspective-control": (
        "p7-l08",
        "perspective",
        "control",
        "perspective-orchestrator",
        "standard",
        "stopped",
        "independent_review_no_incremental_gain",
    ),
    "phase7-research-polisher-happy": (
        "p7-l09",
        "research_polisher",
        "happy",
        "research-polisher-orchestrator",
        "standard",
        "human_strategy_selection_required",
        None,
    ),
    "phase7-research-polisher-control": (
        "p7-l10",
        "research_polisher",
        "control",
        "research-polisher-orchestrator",
        "standard",
        "no_defensible_option",
        "all_options_no_defensible_option",
    ),
}

CONTROL_FACT_MARKERS = {
    "p7-l02": "Only the already published primary contrast may be proposed",
    "p7-l04": "The custodian decision is final",
    "p7-l06": "feature selection read the held-out outcome labels",
    "p7-l08": "Permitted changes are limited to",
    "p7-l10": "The exact source work has already been published",
}

CAPTURE_PROFILE_ITEMS = {
    "visible_plugin_identity_and_version",
    "unique_platform_task_id_and_durable_task_export",
    "parent_task_or_thread_id_and_all_child_task_thread_run_ids",
    "exact_launch_prompt_and_frozen_source_digest",
    "actor_manifest_with_unique_instance_ids_and_role_scopes",
    "complete_actor_read_and_write_sets",
    "source_hashes_before_and_after",
    "versioned_artifact_index_with_complete_lineage",
    "evaluator_and_panel_isolation_fields",
    "dissent_conflicts_and_fatal_findings_with_visibility",
    "observed_terminal_state_and_continuation_when_applicable",
    "final_handoff_or_valid_nonready_artifact_index",
    "automatic_external_submission_false",
}

TASK_VISIBLE_ORACLES = (
    "human_signoff_required",
    "human_strategy_selection_required",
    "independent_review_pending",
    "no_defensible_option",
    "expected_final_state",
    "control_driver",
    "case_kind",
    "manifest.yaml",
    "current-version-runtime-receipts",
)

CAPTURE_FILES = (
    "capture/task-export.json",
    "capture/actor-manifest.json",
    "capture/artifact-index.json",
    "capture/file-access.json",
)


def digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def load_yaml(path: Path) -> dict[str, Any]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise AssertionError(f"{path}: expected a YAML mapping")
    return document


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def resolve_pack_file(relative_value: Any, label: str, errors: list[str]) -> Path | None:
    if not isinstance(relative_value, str) or not relative_value:
        errors.append(f"{label}: expected non-empty repository-relative path")
        return None
    if "\\" in relative_value or Path(relative_value).is_absolute():
        errors.append(f"{label}: path must be canonical repository-relative POSIX")
        return None
    candidate = (REPO / relative_value).resolve()
    try:
        candidate.relative_to(PACK.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes live-input pack")
        return None
    if not candidate.is_file() or candidate.is_symlink():
        errors.append(f"{label}: missing regular non-symlink file {relative_value}")
        return None
    return candidate


def task_visible_has_oracle(text: str) -> str | None:
    lowered = text.lower()
    for token in TASK_VISIBLE_ORACLES:
        if token.lower() in lowered:
            return token
    if re.search(r"\b(?:happy|control|blocked|stopped)\b", lowered):
        return "outcome-class word"
    if re.search(r"phase7-(?:idea|proposal|article|perspective|research-polisher)-", lowered):
        return "scheduler slot ID"
    return None


def main() -> int:
    errors: list[str] = []
    manifest = load_yaml(MANIFEST)
    registry = load_yaml(REGISTRY)
    plugin = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))

    require(manifest.get("schema_version") == 1, "manifest schema_version must be 1", errors)
    require(
        manifest.get("evidence_kind") == "scheduler_input_pack_only"
        and manifest.get("counts_as_runtime_evidence") is False,
        "pack must remain explicit non-evidence",
        errors,
    )
    binding = manifest.get("plugin_binding", {})
    require(
        binding.get("plugin_version") == plugin.get("version") == registry.get("plugin_version"),
        "manifest, plugin, and registry versions must agree",
        errors,
    )
    visibility = manifest.get("task_visibility", {})
    require(
        visibility
        == {
            "scheduler_manifest_visible_to_task": False,
            "scheduler_manifest_visible_to_reviewers": False,
            "launch_prompt_visible_to_reviewers": False,
            "expected_state_location": "manifest_only",
        },
        "task visibility boundary is incomplete",
        errors,
    )
    profiles = manifest.get("capture_profiles", {})
    require(
        set(profiles.get("phase7-runtime-v1", [])) == CAPTURE_PROFILE_ITEMS,
        "capture profile does not cover the required Phase 7 export fields",
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
    require(len(slots) == 10 and len(by_slot) == 10, "pack must contain 10 unique slots", errors)
    require(set(by_slot) == set(EXPECTED_SLOTS), "slot inventory differs from Phase 7 contract", errors)

    state_machines = registry.get("workflow_state_machines", {})
    seen_execution_ids: set[str] = set()
    seen_paths: set[str] = set()
    seen_digests: set[str] = set()
    for slot_id, expected in EXPECTED_SLOTS.items():
        slot = by_slot.get(slot_id)
        if not isinstance(slot, dict):
            continue
        execution_id, workflow, case_kind, entry, mode, final_state, driver = expected
        actual_tuple = (
            slot.get("execution_id"),
            slot.get("workflow"),
            slot.get("case_kind"),
            slot.get("public_entry"),
            slot.get("entry_mode"),
            slot.get("expected_final_state"),
            slot.get("control_driver"),
        )
        require(actual_tuple == expected, f"{slot_id}: scheduling contract mismatch", errors)
        require(execution_id not in seen_execution_ids, f"{slot_id}: duplicate execution ID", errors)
        seen_execution_ids.add(execution_id)

        machine = state_machines.get(workflow, {})
        require(machine.get("orchestrator") == entry, f"{slot_id}: registry orchestrator mismatch", errors)
        require(mode in machine.get("entry_modes", []), f"{slot_id}: registry mode missing", errors)
        require(
            slot.get("required_materials") == ["frozen_source", "installed_frozen_A_plugin"],
            f"{slot_id}: required materials incomplete",
            errors,
        )
        require(
            set(slot.get("resource_boundaries", []))
            == {
                "source_declared_assets_only",
                "source_declared_time_compute_and_access_limits",
                "no_external_submission",
            },
            f"{slot_id}: resource boundaries incomplete",
            errors,
        )
        require(slot.get("capture_profile") == "phase7-runtime-v1", f"{slot_id}: capture profile mismatch", errors)

        source = resolve_pack_file(slot.get("source_path"), f"{slot_id}.source_path", errors)
        prompt = resolve_pack_file(slot.get("prompt_path"), f"{slot_id}.prompt_path", errors)
        for path_value in (slot.get("source_path"), slot.get("prompt_path")):
            if isinstance(path_value, str):
                require(path_value not in seen_paths, f"{slot_id}: reused visible file path", errors)
                seen_paths.add(path_value)
        if source is None or prompt is None:
            continue
        require(source.name == f"{execution_id}.md", f"{slot_id}: source filename is not opaque ID", errors)
        require(prompt.name == f"{execution_id}.md", f"{slot_id}: prompt filename is not opaque ID", errors)
        source_digest = digest(source)
        prompt_digest = digest(prompt)
        require(slot.get("source_sha256") == source_digest, f"{slot_id}: source SHA-256 drift", errors)
        require(slot.get("prompt_sha256") == prompt_digest, f"{slot_id}: prompt SHA-256 drift", errors)
        for value in (source_digest, prompt_digest):
            require(value not in seen_digests, f"{slot_id}: duplicate task-visible bytes", errors)
            seen_digests.add(value)

        source_text = source.read_text(encoding="utf-8")
        prompt_text = prompt.read_text(encoding="utf-8")
        require(
            re.search(rf"(?m)^artifact_id: {re.escape(execution_id)}-source$", source_text) is not None
            and re.search(r"(?m)^version_id: v001$", source_text) is not None
            and re.search(r"(?m)^status: frozen$", source_text) is not None,
            f"{slot_id}: frozen source header incomplete",
            errors,
        )
        require(len(source_text.split()) >= 120, f"{slot_id}: source is not self-contained enough", errors)
        require(
            re.search(r"(?im)^## .*(?:resource|limit|boundary|scope|available additional work)", source_text)
            is not None,
            f"{slot_id}: source has no explicit resource/scope boundary",
            errors,
        )
        source_oracle = task_visible_has_oracle(source_text)
        prompt_oracle = task_visible_has_oracle(prompt_text)
        require(source_oracle is None, f"{slot_id}: source leaks {source_oracle}", errors)
        require(prompt_oracle is None, f"{slot_id}: prompt leaks {prompt_oracle}", errors)
        require(
            f"research-skills-openai:{entry}" in prompt_text
            and f"`{mode}` mode" in prompt_text
            and f"`{source.name}`" in prompt_text,
            f"{slot_id}: prompt does not bind entry, mode, and source",
            errors,
        )
        require(
            all(name in prompt_text for name in CAPTURE_FILES)
            and "`schema_version: 1`" in prompt_text
            and "parent task/thread ID" in prompt_text
            and "child task/thread/run or reviewer instance ID" in prompt_text,
            f"{slot_id}: prompt does not require complete schema-v1 capture files",
            errors,
        )
        normalized_prompt = " ".join(prompt_text.lower().split())
        require(
            "fresh" in normalized_prompt
            and "external submission" in normalized_prompt
            and "verification receipts" in normalized_prompt,
            f"{slot_id}: isolation, submission, or evidence boundary missing",
            errors,
        )

        if case_kind == "control":
            marker = CONTROL_FACT_MARKERS[execution_id]
            require(marker.lower() in source_text.lower(), f"{slot_id}: control-driving source fact missing", errors)
            require(
                "reviewer unavailable" not in source_text.lower()
                and "delegation unavailable" not in source_text.lower(),
                f"{slot_id}: reviewer-unavailability must not drive a live control",
                errors,
            )

    actual_sources = {path.name for path in (PACK / "sources").glob("*.md")}
    actual_prompts = {path.name for path in (PACK / "prompts").glob("*.md")}
    expected_files = {f"p7-l{number:02d}.md" for number in range(1, 11)}
    require(actual_sources == expected_files, "source directory must contain exactly 10 opaque inputs", errors)
    require(actual_prompts == expected_files, "prompt directory must contain exactly 10 opaque launch prompts", errors)
    require(
        "statistical analysis plan appendix" in (PACK / "sources" / "p7-l03.md").read_text(encoding="utf-8").lower()
        and "independently reviewed analytical attachments"
        in (PACK / "prompts" / "p7-l03.md").read_text(encoding="utf-8").lower(),
        "proposal positive case must naturally require independent SAP production and review",
        errors,
    )

    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "valid": True,
                "pack_id": manifest.get("pack_id"),
                "slots": len(slots),
                "sources": len(actual_sources),
                "prompts": len(actual_prompts),
                "digests_verified": len(seen_digests),
                "runtime_evidence": False,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
