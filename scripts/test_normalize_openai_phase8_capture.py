#!/usr/bin/env python3
"""Negative-first tests for the profile-aware Phase 8 R v2 normalizer."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from normalize_openai_phase8_capture import (  # noqa: E402
    CaptureNormalizationError,
    SCHEDULER_MANIFEST_PATH,
    StagingRoot,
    normalize_capture,
    validate_normalized_capture,
)
from openai_preview_capture_contracts import validate_normalized_capture as dispatch_capture  # noqa: E402
from openai_preview_evidence import sha256_bytes  # noqa: E402
from validate_openai_phase8_external_evidence import current_checkout_source_identity  # noqa: E402


NOW = datetime.now(timezone.utc).replace(microsecond=0)
STAMP = (NOW - timedelta(minutes=10)).isoformat().replace("+00:00", "Z")


def binding(path: str, payload: bytes, artifact_type: str) -> dict[str, Any]:
    return {
        "artifact_type": artifact_type,
        "path": path,
        "sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
    }


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def pointer_bindings(path: str, names: list[str]) -> dict[str, Any]:
    return {name: {"path": path, "json_pointer": f"/{name}"} for name in names}


def base_task(slot: Mapping[str, Any], input_bytes: bytes, prompt_bytes: bytes) -> dict[str, Any]:
    identity = current_checkout_source_identity()
    return {
        "schema_version": "openai-phase8-task-export/v2",
        "platform": "codex",
        "surface": "codex",
        "evidence_kind": "task_export",
        "export_id": f"export-{slot['execution_id']}",
        "task_id": f"task-{slot['execution_id']}",
        "parent_task_or_thread_id": f"task-{slot['execution_id']}",
        "observable_child_or_delegate_ids": [],
        "captured_at": STAMP,
        "automatic_external_submission": False,
        **identity,
        "slot_id": slot["slot"],
        "profile": slot["capture_profile"],
        "kind": slot["kind"],
        "scheduler_input": {
            "execution_id": slot["execution_id"],
            "input": binding(str(slot["input_path"]), input_bytes, "scheduler_input"),
            "launch_prompt": binding(str(slot["prompt_path"]), prompt_bytes, "scheduler_prompt"),
            "scheduler_manifest_visible": False,
            "scheduler_labels_visible": False,
            "expected_outcomes_visible": False,
        },
        "capability": {"name": "placeholder", "state": "completed", "task_or_tool_run_ids": []},
        "supporting_artifacts": [],
        "platform_id_bindings": {},
        "slot_payload": {},
    }


def reviewer_task(slot: Mapping[str, Any], input_bytes: bytes, prompt_bytes: bytes) -> tuple[dict[str, Any], dict[str, bytes]]:
    task = base_task(slot, input_bytes, prompt_bytes)
    child = f"child-{slot['execution_id']}"
    instance = f"instance-{slot['execution_id']}"
    created = (NOW - timedelta(minutes=11)).isoformat().replace("+00:00", "Z")
    dispatch_bytes = b"schema_version: 1\n"
    platform = {
        "capture_export_id": task["export_id"],
        "task_id": task["task_id"],
        "parent_task_or_thread_id": task["task_id"],
        "parent_delegation_child_id": child,
        "delegated_thread_id": child,
        "captured_child_thread_id": child,
        "reviewer_instance_id": instance,
        "reviewer_instance_created_at": created,
        "platform_receipt_id": f"receipt-{slot['execution_id']}",
        "captured_at": STAMP,
        "files_read": [str(slot["input_path"])],
        "files_written": [f"runtime-artifacts/reviews/{slot['execution_id']}/report.yaml"],
        "input_digest_before": task["scheduler_input"]["input"]["sha256"],
        "input_digest_after": task["scheduler_input"]["input"]["sha256"],
        "source_edits_performed": False,
        "delegated_prompt_sha256": sha256_bytes(dispatch_bytes),
    }
    files = {
        f"runs/{slot['execution_id']}/capture/platform.json": json_bytes(platform),
        f"runs/{slot['execution_id']}/capture/blind.yaml": b"schema_version: 1\n",
        f"runs/{slot['execution_id']}/capture/dispatch.yaml": dispatch_bytes,
        f"runs/{slot['execution_id']}/capture/raw.yaml": b"schema_version: 1\n",
        f"runtime-artifacts/reviews/{slot['execution_id']}/report.yaml": b"schema_version: 1\ndecision: blocked\n",
    }
    types = ["platform_export", "blind_bundle", "dispatch_prompt", "raw_review_output", "reviewer_report"]
    task["supporting_artifacts"] = [binding(path, payload, kind) for (path, payload), kind in zip(files.items(), types)]
    by_path = {item["path"]: item for item in task["supporting_artifacts"]}
    platform_path = next(iter(files))
    task["platform_id_bindings"] = pointer_bindings(platform_path, list(platform))
    task["observable_child_or_delegate_ids"] = [child]
    task["capability"] = {"name": "codex_fresh_subagent", "state": "completed", "task_or_tool_run_ids": [child]}
    task["slot_payload"] = {
        "reviewer_run": {
            "run_id": f"run-{slot['execution_id']}",
            "reviewer_skill": slot["reviewer_skill"],
            "delegated_thread_id": child,
            "reviewer_instance_id": instance,
            "reviewer_instance_created_at": created,
            "platform_receipt_id": platform["platform_receipt_id"],
            "blind_bundle": by_path[f"runs/{slot['execution_id']}/capture/blind.yaml"],
            "dispatch_prompt": by_path[f"runs/{slot['execution_id']}/capture/dispatch.yaml"],
            "raw_transport_output": by_path[f"runs/{slot['execution_id']}/capture/raw.yaml"],
            "report": by_path[f"runtime-artifacts/reviews/{slot['execution_id']}/report.yaml"],
            "scope_authority": "platform_derived",
            "platform_scope": {
                "files_read": platform["files_read"],
                "files_written": platform["files_written"],
                "input_digest_before": platform["input_digest_before"],
                "input_digest_after": platform["input_digest_after"],
                "source_edits_performed": False,
            },
            "isolation_mode": "fresh_subagent",
            "prior_scores_visible": False,
            "peer_outputs_visible": False,
            "target_decision_visible": False,
            "source_edits_performed": False,
        }
    }
    return task, files


def search_task(slot: Mapping[str, Any], input_bytes: bytes, prompt_bytes: bytes) -> tuple[dict[str, Any], dict[str, bytes]]:
    task = base_task(slot, input_bytes, prompt_bytes)
    query = "What is the current official requirement?"
    opened = [
        {"source_id": "src-1", "url": "https://example.org/primary", "primary_or_authoritative": True, "identity_verified": True},
        {"source_id": "src-2", "url": "https://example.edu/authority", "primary_or_authoritative": True, "identity_verified": True},
    ]
    citations = [{"source_id": "src-1", "citation_id": "cite-1"}, {"source_id": "src-2", "citation_id": "cite-2"}]
    claims = [{"claim_id": "claim-1", "material": True, "source_ids": ["src-1", "src-2"]}]
    platform = {
        "capture_export_id": task["export_id"], "task_id": task["task_id"], "captured_at": STAMP,
        "search_tool_id": "builtin-search", "search_tool_run_id": f"search-{slot['execution_id']}",
        "search_query": query, "opened_sources": opened, "citation_metadata": citations,
        "material_claim_trace": claims,
    }
    files = {
        f"runs/{slot['execution_id']}/capture/platform.json": json_bytes(platform),
        f"runs/{slot['execution_id']}/capture/raw-search-output.json": json_bytes({"answer": "bounded"}),
        f"runs/{slot['execution_id']}/capture/citation-export.json": json_bytes(citations),
    }
    task["supporting_artifacts"] = [
        binding(next(iter(files)), files[next(iter(files))], "platform_export"),
        binding(list(files)[1], files[list(files)[1]], "search_output"),
        binding(list(files)[2], files[list(files)[2]], "citation_export"),
    ]
    by_path = {item["path"]: item for item in task["supporting_artifacts"]}
    task["platform_id_bindings"] = pointer_bindings(next(iter(files)), list(platform))
    task["capability"] = {"name": "chatgpt_codex_builtin_search", "state": "active", "task_or_tool_run_ids": [platform["search_tool_id"], platform["search_tool_run_id"]]}
    task["slot_payload"] = {"retrieval": {
        "receipt_id": f"receipt-{slot['execution_id']}", "kind": "search", "question_class": slot["question_class"],
        "query": query, "query_or_request_digest": sha256_bytes(query.encode()),
        "tool_id": platform["search_tool_id"], "tool_run_id": platform["search_tool_run_id"],
        "opened_sources": opened, "citation_metadata": citations, "material_claim_trace": claims,
        "raw_search_output": by_path[list(files)[1]], "citation_export": by_path[list(files)[2]],
        "local_retrieval_fallback": False, "inline_simulation": False,
    }}
    return task, files


def pending_deep_research_task(slot: Mapping[str, Any], input_bytes: bytes, prompt_bytes: bytes) -> tuple[dict[str, Any], dict[str, bytes]]:
    task = base_task(slot, input_bytes, prompt_bytes)
    files = {
        f"runs/{slot['execution_id']}/capture/mapper-handoff.yaml": b"schema_version: 1\nrequest: frozen\n",
        f"runs/{slot['execution_id']}/capture/continuation.yaml": b"schema_version: 1\nnext_action: user_start_deep_research\n",
    }
    task["supporting_artifacts"] = [binding(path, payload, "handoff" if index == 0 else "continuation") for index, (path, payload) in enumerate(files.items())]
    task["capability"] = {"name": "chatgpt_deep_research", "state": "handoff_required", "task_or_tool_run_ids": []}
    task["slot_payload"] = {"retrieval": {
        "kind": "deep_research_completed",
        "completion_projection": {"status": "pending", "reason": "no registered concrete ChatGPT export adapter"},
        "handoff_artifact": task["supporting_artifacts"][0],
        "continuation_artifact": task["supporting_artifacts"][1],
        "pending_edge_id": f"edge-{slot['execution_id']}",
        "workflow_paused": True,
        "inline_simulation": False,
    }}
    return task, files


def inactive_task(slot: Mapping[str, Any], input_bytes: bytes, prompt_bytes: bytes) -> tuple[dict[str, Any], dict[str, bytes]]:
    task = base_task(slot, input_bytes, prompt_bytes)
    observed = (NOW - timedelta(minutes=9)).isoformat().replace("+00:00", "Z")
    platform = {"capture_export_id": task["export_id"], "task_id": task["task_id"], "captured_at": STAMP, "capability_state": "unavailable", "capability_observed_at": observed}
    files = {
        f"runs/{slot['execution_id']}/capture/capability.json": json_bytes(platform),
        f"runs/{slot['execution_id']}/capture/handoff.yaml": b"schema_version: 1\nrequest: frozen\n",
        f"runs/{slot['execution_id']}/capture/continuation.yaml": b"schema_version: 1\nnext_action: activate_deep_research\n",
    }
    task["supporting_artifacts"] = [
        binding(list(files)[0], files[list(files)[0]], "capability_export"),
        binding(list(files)[1], files[list(files)[1]], "handoff"),
        binding(list(files)[2], files[list(files)[2]], "continuation"),
    ]
    task["platform_id_bindings"] = pointer_bindings(list(files)[0], list(platform))
    task["capability"] = {"name": "chatgpt_deep_research", "state": "unavailable", "task_or_tool_run_ids": []}
    task["slot_payload"] = {"retrieval": {
        "kind": "deep_research_inactive_control", "capability_state": "unavailable",
        "capability_observed_at": observed, "capability_state_export": task["supporting_artifacts"][0],
        "handoff_artifact": task["supporting_artifacts"][1], "continuation_artifact": task["supporting_artifacts"][2],
        "pending_edge_id": f"edge-{slot['execution_id']}", "workflow_paused": True,
        "downstream_evidence_map_created": False, "inline_simulation": False,
    }}
    return task, files


def completed_dr_claim_task(slot: Mapping[str, Any], input_bytes: bytes, prompt_bytes: bytes) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Return a deliberately untrusted JSON that self-labels as a provider export."""
    task = base_task(slot, input_bytes, prompt_bytes)
    times = {
        "handoff": (NOW - timedelta(minutes=9)).isoformat().replace("+00:00", "Z"),
        "user_start": (NOW - timedelta(minutes=8)).isoformat().replace("+00:00", "Z"),
        "provider_completed": (NOW - timedelta(minutes=7)).isoformat().replace("+00:00", "Z"),
        "mapper_return": (NOW - timedelta(minutes=6)).isoformat().replace("+00:00", "Z"),
        "resume": (NOW - timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
    }
    opened = [
        {"source_id": "s1", "url": "https://example.org/one", "primary_or_authoritative": True, "identity_verified": True},
        {"source_id": "s2", "url": "https://example.org/two", "primary_or_authoritative": True, "identity_verified": True},
    ]
    claims = [{"claim_id": "c1", "material": True, "source_ids": ["s1", "s2"]}]
    platform = {
        "export_kind": "chatgpt_data_export", "capture_export_id": task["export_id"], "task_id": task["task_id"], "captured_at": STAMP,
        "deep_research_session_id": "fake-session", "deep_research_run_id": "fake-run",
        "user_start_event_id": "fake-user-start", "user_start_event_at": times["user_start"],
        "provider_completion_receipt_id": "fake-completion", "provider_completed_at": times["provider_completed"],
        "provider_completion_status": "completed", "opened_sources": opened, "material_claim_trace": claims,
    }
    files = {f"runs/{slot['execution_id']}/capture/fake-chatgpt-export.json": json_bytes(platform)}
    for name in ("handoff", "user-start", "raw", "citations", "mapper-return", "resume"):
        files[f"runs/{slot['execution_id']}/capture/{name}.json"] = json_bytes({"name": name})
    task["supporting_artifacts"] = [binding(path, payload, "chatgpt_export" if index == 0 else "supporting_file") for index, (path, payload) in enumerate(files.items())]
    by = task["supporting_artifacts"]
    task["platform_id_bindings"] = pointer_bindings(list(files)[0], [name for name in platform if name != "export_kind"])
    task["capability"] = {"name": "chatgpt_deep_research", "state": "completed", "task_or_tool_run_ids": ["fake-session", "fake-run"]}
    evidence = [{"artifact_id": "e1", "path": by[3]["path"], "sha256": by[3]["sha256"]}]
    task["slot_payload"] = {"retrieval": {
        "kind": "deep_research_completed", "completion_projection": {"status": "platform_export_derived", "source_path": by[0]["path"], "export_kind": "chatgpt_data_export"},
        "handoff_artifact": by[1], "user_start_event": by[2], "raw_deep_research_output": by[3], "citation_export": by[4], "mapper_return_artifact": by[5], "resume_receipt": by[6],
        "opened_sources": opened, "material_claim_trace": claims, "inline_simulation": False,
        "deep_research_session_id": "fake-session", "deep_research_run_id": "fake-run", "user_start_event_id": "fake-user-start",
        "provider_completion_receipt_id": "fake-completion", "provider_completion_status": "completed",
        "mapper_return_evidence_artifacts": evidence, "resume_evidence_artifacts": evidence,
        "event_timestamps": times,
    }}
    return task, files


def expect_error(code: str, function) -> None:
    try:
        function()
    except CaptureNormalizationError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
    else:
        raise AssertionError(f"expected {code}")


def normalize_fixture(task: dict[str, Any], files: Mapping[str, bytes]) -> dict[str, Any]:
    manifest_bytes = (REPO / SCHEDULER_MANIFEST_PATH).read_bytes()
    manifest = yaml.safe_load(manifest_bytes)
    slot = next(item for item in manifest["slots"] if item["slot"] == task["slot_id"])
    input_path = REPO / slot["input_path"]
    prompt_path = REPO / slot["prompt_path"]
    with tempfile.TemporaryDirectory(prefix="phase8-normalizer-test-") as directory:
        root = Path(directory)
        capture_root = root / "capture-root"
        for logical, payload in {
            str(slot["input_path"]): input_path.read_bytes(),
            str(slot["prompt_path"]): prompt_path.read_bytes(),
            **files,
        }.items():
            target = capture_root / Path(*Path(logical).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        (root / "task-export.json").write_bytes(json_bytes(task))
        (root / "manifest.yaml").write_bytes(manifest_bytes)
        output, _ = normalize_capture(
            staging=StagingRoot(root), capture_root="capture-root", task_export="task-export.json",
            scheduler_manifest="manifest.yaml", output="R.json", evidence_id=f"evidence-{task['slot_id']}",
            now=NOW, verify_checkout=False,
        )
        return json.loads(output.read_text(encoding="utf-8"))


def main() -> int:
    manifest = yaml.safe_load((REPO / SCHEDULER_MANIFEST_PATH).read_text(encoding="utf-8"))
    slots = {item["execution_id"]: item for item in manifest["slots"]}
    guards: list[str] = []

    def source(slot):
        return (REPO / slot["input_path"]).read_bytes(), (REPO / slot["prompt_path"]).read_bytes()

    rslot = slots["p8-l01"]
    task, files = reviewer_task(rslot, *source(rslot))
    normalized = normalize_fixture(task, files)
    result = validate_normalized_capture(normalized, now=NOW, verify_checkout=False)
    assert result["live_collection_eligible"] is False
    assert result["capture_status"] == "platform_capture_adapter_pending"
    assert dispatch_capture(normalized, now=NOW, verify_checkout=False)["profile"] == "phase8-reviewer-v1"
    guards.append("self_labeled_reviewer_json_non_counting")

    promoted_claim = copy.deepcopy(normalized)
    promoted_claim["live_collection_eligible"] = True
    promoted_claim["capture_status"] = "platform_trace_complete"
    promoted_claim["capture_provenance"]["scope_classification"] = "platform_derived"
    expect_error(
        "normalized_payload_derivation_mismatch",
        lambda: validate_normalized_capture(
            promoted_claim, now=NOW, verify_checkout=False
        ),
    )
    guards.append("self_labeled_reviewer_cannot_flip_live_flag")

    unknown_schema = copy.deepcopy(normalized)
    unknown_schema["normalization_schema"] = "openai-preview-normalized-capture/v999"
    try:
        dispatch_capture(unknown_schema, now=NOW, verify_checkout=False)
    except ValueError as exc:
        assert "unsupported normalized capture schema" in str(exc)
    else:
        raise AssertionError("unknown schema fell back to another normalizer")
    for relative in (
        "scripts/build_openai_preview_mini_bundle.py",
        "scripts/verify_openai_preview_draft_bundle.py",
        "tests/openai_phase8/verify_preview_evidence.py",
    ):
        text = (REPO / relative).read_text(encoding="utf-8")
        assert "from openai_preview_capture_contracts import" in text
    guards.append("explicit_schema_dispatch_without_fallback")

    task_recorded = copy.deepcopy(task)
    task_recorded["slot_payload"]["reviewer_run"]["scope_authority"] = "task_recorded"
    for key in ("files_read", "files_written", "input_digest_before", "input_digest_after", "source_edits_performed"):
        task_recorded["platform_id_bindings"].pop(key)
    pending = normalize_fixture(task_recorded, files)
    assert pending["live_collection_eligible"] is False and pending["capture_status"] == "task_recorded_scope_pending"
    guards.append("task_recorded_scope_non_counting")

    mismatch = copy.deepcopy(task)
    mismatch["slot_payload"]["reviewer_run"]["delegated_thread_id"] = "task-authored-child"
    mismatch["observable_child_or_delegate_ids"] = ["task-authored-child"]
    expect_error("platform_binding_mismatch", lambda: normalize_fixture(mismatch, files))
    guards.append("reviewer_delegation_three_way_mismatch_rejected")

    sslot = slots["p8-l07"]
    search, search_files = search_task(sslot, *source(sslot))
    search_r = normalize_fixture(search, search_files)
    search_result = validate_normalized_capture(search_r, now=NOW, verify_checkout=False)
    assert search_result["live_collection_eligible"] is False
    assert search_result["capture_status"] == "platform_capture_adapter_pending"
    guards.append("self_labeled_search_trace_non_counting")

    final_answer_only = copy.deepcopy(search)
    final_answer_only["platform_id_bindings"].pop("material_claim_trace")
    expect_error("platform_binding_missing", lambda: normalize_fixture(final_answer_only, search_files))
    guards.append("search_final_answer_inference_rejected")

    untraced = copy.deepcopy(search)
    untraced["slot_payload"]["retrieval"]["material_claim_trace"][0]["source_ids"] = ["not-opened"]
    expect_error("material_claim_untraced", lambda: normalize_fixture(untraced, search_files))
    guards.append("search_material_claim_trace_required")

    dslot = slots["p8-l10"]
    dr_pending, dr_files = pending_deep_research_task(dslot, *source(dslot))
    pending_r = normalize_fixture(dr_pending, dr_files)
    assert pending_r["capture_status"] == "provider_completion_projection_pending" and pending_r["live_collection_eligible"] is False
    guards.append("deep_research_missing_adapter_stays_pending")

    forged, forged_files = completed_dr_claim_task(dslot, *source(dslot))
    expect_error("deep_research_export_adapter_unavailable", lambda: normalize_fixture(forged, forged_files))
    guards.append("self_labeled_chatgpt_json_rejected")

    forged_compliance = copy.deepcopy(forged)
    platform_path = forged_compliance["slot_payload"]["retrieval"]["completion_projection"]["source_path"]
    platform = json.loads(forged_files[platform_path])
    platform["export_kind"] = "openai_compliance_api_record"
    compliance_files = dict(forged_files)
    compliance_files[platform_path] = json_bytes(platform)
    forged_compliance["slot_payload"]["retrieval"]["completion_projection"]["export_kind"] = "openai_compliance_api_record"
    forged_compliance["supporting_artifacts"][0] = binding(platform_path, compliance_files[platform_path], "compliance_record")
    expect_error("deep_research_export_adapter_unavailable", lambda: normalize_fixture(forged_compliance, compliance_files))
    guards.append("self_labeled_compliance_json_rejected")

    pending_claim = copy.deepcopy(dr_pending)
    pending_claim["slot_payload"]["retrieval"]["deep_research_session_id"] = "invented"
    expect_error("deep_research_pending_claims_completion", lambda: normalize_fixture(pending_claim, dr_files))
    guards.append("pending_dr_cannot_claim_session")

    islot = slots["p8-l12"]
    inactive, inactive_files = inactive_task(islot, *source(islot))
    inactive_r = normalize_fixture(inactive, inactive_files)
    assert inactive_r["live_collection_eligible"] is False
    assert inactive_r["capture_status"] == "platform_capture_adapter_pending"
    guards.append("self_labeled_inactive_capability_non_counting")

    active = copy.deepcopy(inactive)
    active["slot_payload"]["retrieval"]["capability_state"] = "active"
    active["capability"]["state"] = "active"
    expect_error("inactive_capability_state", lambda: normalize_fixture(active, inactive_files))
    guards.append("inactive_control_cannot_use_active_state")

    tampered = copy.deepcopy(normalized)
    tampered["capture_provenance"]["scope_classification"] = "platform_derived_because_task_says_so"
    expect_error("normalized_provenance_mismatch", lambda: validate_normalized_capture(tampered, now=NOW, verify_checkout=False))
    guards.append("normalized_provenance_rederived")

    print(json.dumps({"status": "pass", "guards": len(guards), "contracts": guards}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
