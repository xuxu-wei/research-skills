#!/usr/bin/env python3
"""Test Phase 8 collection assembly without upgrading pending captures."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from collections import Counter
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from build_openai_phase8_live_collections import (  # noqa: E402
    ASSET_BINDINGS_SCHEMA,
    PLAN_SCHEMA,
    assemble_collections,
    build_workspace_manifests,
    CollectionBuildError,
    build_collections,
    load_captures,
    pending_inventory,
    validate_asset_bindings,
)
from openai_preview_evidence import sha256_bytes  # noqa: E402
from normalize_openai_preview_capture import canonical_json_bytes  # noqa: E402
from test_normalize_openai_phase8_capture import (  # noqa: E402
    NOW,
    completed_dr_claim_task,
    inactive_task,
    normalize_fixture,
    pending_deep_research_task,
    reviewer_task,
    search_task,
)


def retime(task: dict, files: dict[str, bytes], minutes: int) -> tuple[dict, dict[str, bytes]]:
    task = copy.deepcopy(task)
    files = dict(files)
    stamp = (NOW - timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")
    task["captured_at"] = stamp
    platform_binding = task.get("platform_id_bindings", {}).get("captured_at")
    if isinstance(platform_binding, dict):
        path = platform_binding["path"]
        platform = json.loads(files[path])
        platform["captured_at"] = stamp
        reviewer_run = task.get("slot_payload", {}).get("reviewer_run")
        if isinstance(reviewer_run, dict):
            created = (NOW - timedelta(minutes=minutes + 1)).isoformat().replace("+00:00", "Z")
            reviewer_run["reviewer_instance_created_at"] = created
            platform["reviewer_instance_created_at"] = created
        files[path] = (json.dumps(platform, sort_keys=True) + "\n").encode()
        for offset, item in enumerate(task["supporting_artifacts"]):
            if item["path"] == path:
                task["supporting_artifacts"][offset] = {
                    **item,
                    "sha256": sha256_bytes(files[path]),
                    "size_bytes": len(files[path]),
                }
                break
    return task, files


def expect_error(code: str, function) -> None:
    try:
        function()
    except CollectionBuildError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
    else:
        raise AssertionError(f"expected {code}")


def main() -> int:
    manifest = yaml.safe_load((REPO / "tests/openai_phase8/live-inputs/manifest.yaml").read_text(encoding="utf-8"))
    slots = {item["execution_id"]: item for item in manifest["slots"]}
    with tempfile.TemporaryDirectory(prefix="phase8-collection-test-") as directory:
        root = Path(directory).resolve()
        captures_dir = root / "captures"
        captures_dir.mkdir()
        plan = {"schema_version": PLAN_SCHEMA, "captures": []}
        for serial in range(1, 13):
            execution = f"p8-l{serial:02d}"
            slot = slots[execution]
            input_bytes = (REPO / slot["input_path"]).read_bytes()
            prompt_bytes = (REPO / slot["prompt_path"]).read_bytes()
            if serial <= 6:
                task, files = reviewer_task(slot, input_bytes, prompt_bytes)
                task, files = retime(task, files, 30 - serial)
            elif serial <= 9:
                task, files = search_task(slot, input_bytes, prompt_bytes)
            elif serial <= 11:
                task, files = pending_deep_research_task(slot, input_bytes, prompt_bytes)
            else:
                task, files = inactive_task(slot, input_bytes, prompt_bytes)
            normalized = normalize_fixture(task, files)
            path = captures_dir / f"{execution}.json"
            path.write_text(json.dumps(normalized, sort_keys=True), encoding="utf-8")
            plan["captures"].append({"slot_id": slot["slot"], "path": f"captures/{execution}.json"})

        captures = load_captures(root=root, plan=plan, now=NOW, verify_checkout=False)
        state = pending_inventory(captures)
        assert state["eligible_slot_count"] == 0
        assert len(state["pending_slots"]) == 12
        assert Counter(item["reason"] for item in state["pending_slots"]) == {
            "no_registered_platform_capture_adapter": 10,
            "no_concrete_deep_research_export_adapter": 2,
        }
        assert state["next_required_action"] == "register_concrete_platform_capture_adapter_then_recapture"

        expect_error("phase8_capture_pending", lambda: build_collections(captures, {}))

        # Exercise the pure assembler in memory.  This is deliberately not a
        # CLI/live-verifier input and every emitted document stays explicitly
        # synthetic and non-counting.  The two future DR records model only
        # the mechanical schema surface; they do not pass the R v2 normalizer.
        mechanical_captures = []
        for capture in captures:
            if capture.kind != "deep_research_completed":
                mechanical_captures.append(capture)
                continue
            document = copy.deepcopy(capture.document)
            validated = copy.deepcopy(capture.validated)
            task = copy.deepcopy(validated["task_export"])
            prefix = f"synthetic-unit/{capture.slot_id}"
            platform_path = f"{prefix}/provider-export.json"
            source_paths = {
                "raw_deep_research_output": f"{prefix}/raw.json",
                "citation_export": f"{prefix}/citations.json",
                "handoff_artifact": f"{prefix}/handoff.json",
                "user_start_event": f"{prefix}/user-start.json",
                "mapper_return_artifact": f"{prefix}/mapper-return.json",
                "resume_receipt": f"{prefix}/resume.json",
            }
            task["slot_payload"] = {"retrieval": {
                "kind": "deep_research_completed",
                "deep_research_session_id": f"synthetic-session-{capture.slot_id}",
                "deep_research_run_id": f"synthetic-run-{capture.slot_id}",
                "provider_completion_receipt_id": f"synthetic-receipt-{capture.slot_id}",
                "provider_completion_status": "completed",
                "pending_edge_id": f"synthetic-edge-{capture.slot_id}",
                **{name: {"path": path} for name, path in source_paths.items()},
                "opened_sources": [],
                "material_claim_trace": [],
                "mapper_return_evidence_artifacts": [],
                "event_timestamps": {},
                "inline_simulation": False,
            }}
            validated["task_export"] = task
            validated["live_collection_eligible"] = True
            decoded = dict(validated["decoded_source_files"])
            decoded.update({path: b"synthetic-unit-only" for path in [platform_path, *source_paths.values()]})
            validated["decoded_source_files"] = decoded
            document["capture_provenance"] = {
                "id_bindings": {
                    "synthetic_unit_only": {
                        "source_path": platform_path,
                        "json_pointer": "/not-used-by-mechanical-assembler",
                        "value_sha256": "sha256:" + "0" * 64,
                    }
                },
                "scope_classification": "non_counting_pending",
            }
            mechanical_captures.append(replace(capture, document=document, validated=validated))

        next_asset_id = 1000
        slot_assets = {}
        for capture in mechanical_captures:
            normalized_path = f"synthetic-unit/{capture.slot_id}/R.json"
            normalized = {
                "logical_path": normalized_path,
                "asset_id": next_asset_id,
                "sha256": sha256_bytes(capture.payload),
                "size": len(capture.payload),
            }
            next_asset_id += 1
            sources = {}
            for logical, payload in capture.validated["decoded_source_files"].items():
                sources[logical] = {
                    "logical_path": f"synthetic-unit/{capture.slot_id}/sources/{logical}",
                    "asset_id": next_asset_id,
                    "sha256": sha256_bytes(payload),
                    "size": len(payload),
                }
                next_asset_id += 1
            slot_assets[capture.slot_id] = {
                "bundle_id": f"synthetic-bundle-{capture.slot_id}",
                "normalized": normalized,
                "sources": sources,
                "attestation": {
                    "adapter_id": "synthetic-unit-not-a-live-adapter",
                    "envelope_path": f"synthetic-unit/{capture.slot_id}/E.json",
                    "envelope_digest": "sha256:" + "1" * 64,
                    "release_asset_index_path": f"synthetic-unit/{capture.slot_id}/I.json",
                    "release_asset_index_digest": "sha256:" + "2" * 64,
                    "raw_export_path": normalized_path,
                    "raw_export_digest": normalized["sha256"],
                    "synthetic_test_only": True,
                },
            }
        mechanical_assets = {
            "slots": slot_assets,
            "anchor": mechanical_captures[0].slot_id,
            "witness": mechanical_captures[1].slot_id,
            "collections": {},
        }
        reviewer_doc, retrieval_doc = assemble_collections(
            mechanical_captures,
            mechanical_assets,
            synthetic_test_only=True,
        )
        reviewer_bytes = canonical_json_bytes(reviewer_doc)
        retrieval_bytes = canonical_json_bytes(retrieval_doc)
        mechanical_assets["collections"] = {
            "reviewer": {
                "logical_path": "synthetic-unit/collections/reviewer.json",
                "asset_id": next_asset_id,
                "sha256": sha256_bytes(reviewer_bytes),
                "size": len(reviewer_bytes),
            },
            "retrieval": {
                "logical_path": "synthetic-unit/collections/retrieval.json",
                "asset_id": next_asset_id + 1,
                "sha256": sha256_bytes(retrieval_bytes),
                "size": len(retrieval_bytes),
            },
        }
        manifests = build_workspace_manifests(
            mechanical_captures,
            mechanical_assets,
            reviewer_bytes,
            retrieval_bytes,
            synthetic_test_only=True,
        )
        assert reviewer_doc["counts_as_runtime_evidence"] is False and reviewer_doc["synthetic_test_only"] is True
        assert retrieval_doc["counts_as_runtime_evidence"] is False and retrieval_doc["synthetic_test_only"] is True
        assert sum(len(case["runs"]) for case in reviewer_doc["cases"]) == 6
        assert Counter(item["kind"] for item in retrieval_doc["receipts"]) == {
            "search": 3,
            "deep_research_completed": 2,
            "deep_research_inactive_control": 1,
        }
        assert len(manifests) == 12
        assert all(item["counts_as_runtime_evidence"] is False and item["synthetic_test_only"] is True for item in manifests.values())
        assert sum(item["collection_anchor"] is True for item in manifests.values()) == 1
        assert sum(item["collection_witness"] is True for item in manifests.values()) == 1

        # Even a fully populated self-labelled JSON cannot replace the absent
        # concrete Deep Research export adapter.
        forged_slot = slots["p8-l10"]
        forged, forged_files = completed_dr_claim_task(
            forged_slot,
            (REPO / forged_slot["input_path"]).read_bytes(),
            (REPO / forged_slot["prompt_path"]).read_bytes(),
        )
        try:
            normalize_fixture(forged, forged_files)
        except Exception as exc:
            assert getattr(exc, "code", None) == "deep_research_export_adapter_unavailable"
        else:
            raise AssertionError("self-labelled Deep Research JSON became live-eligible")

        fake_bindings = {
            "schema_version": ASSET_BINDINGS_SCHEMA,
            "synthetic_test_only": True,
            "source_identity": dict(captures[0].identity),
            "slots": {},
            "collections": {},
            "collection_anchor_slot": captures[0].slot_id,
            "collection_witness_slot": captures[1].slot_id,
        }
        expect_error("asset_bindings_schema", lambda: validate_asset_bindings(captures, fake_bindings))

        duplicate_plan = copy.deepcopy(plan)
        duplicate_plan["captures"][1]["slot_id"] = duplicate_plan["captures"][0]["slot_id"]
        expect_error("capture_slot_reused_or_unknown", lambda: load_captures(root=root, plan=duplicate_plan, now=NOW, verify_checkout=False))

        duplicate_parent_doc = json.loads((captures_dir / "p8-l02.json").read_text(encoding="utf-8"))
        duplicate_parent_doc["parent_task_or_thread_id"] = captures[0].document["parent_task_or_thread_id"]
        # The validator re-derives the parent from embedded source bytes, so a
        # top-level-only edit is rejected before collection independence.
        (captures_dir / "p8-l02.json").write_text(json.dumps(duplicate_parent_doc, sort_keys=True), encoding="utf-8")
        expect_error("normalized_capture_derivation_mismatch", lambda: load_captures(root=root, plan=plan, now=NOW, verify_checkout=False))

    print(json.dumps({
        "status": "pass",
        "captures": 12,
        "eligible": 0,
        "pending_platform_capture_adapter": 10,
        "pending_completed_deep_research": 2,
        "synthetic_asset_bindings_accepted": False,
        "self_labeled_provider_json_accepted": False,
        "mechanical_assembly_unit_collections": 2,
        "mechanical_assembly_unit_manifests": 12,
        "mechanical_assembly_counts_as_runtime_evidence": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
