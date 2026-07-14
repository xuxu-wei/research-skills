#!/usr/bin/env python3
"""Focused fail-closed contracts for the real-only Phase 8 runner."""

from __future__ import annotations

import copy
import inspect
import json
import pickle
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping
from unittest.mock import patch

import yaml

from openai_preview_evidence import (
    EVIDENCE_ENVELOPE_SCHEMA,
    RELEASE_ASSET_INDEX_SCHEMA,
    VERIFIER_REPORT_SCHEMA,
    EvidenceValidationResult,
    PREVIEW_ATTESTED,
    canonical_json_bytes,
    sha256_bytes,
)
import validate_openai_phase8_external_evidence as external_runner
from validate_openai_phase8_external_evidence import (
    PREVIEW_ADAPTER_ID,
    BundleSnapshot,
    JsonArgumentParser,
    Phase8ExternalEvidenceError,
    Slot,
    _assert_slot_independence,
    _assert_subject_identity,
    _reviewer_slots,
    _retrieval_slots,
    _validate_live_result,
    _validate_semantic_result,
    build_parser,
    validate_external_phase8_evidence,
)
import test_openai_phase8_corpus as phase8_corpus


SHA_A = "sha256:" + "a" * 64
SHA_B = "sha256:" + "b" * 64
SHA_C = "sha256:" + "c" * 64
COMMIT = "1" * 40


def identity() -> dict[str, str]:
    return {
        "plugin_version": "0.7.0-preview.1",
        "source_commit": COMMIT,
        "manifest_sha256": SHA_A,
        "registry_sha256": SHA_B,
        "skill_tree_sha256": SHA_C,
    }


def phase8_identity() -> dict[str, str]:
    source = identity()
    return {
        "plugin_version": source["plugin_version"],
        "source_commit": source["source_commit"],
        "manifest_digest": source["manifest_sha256"],
        "registry_digest": source["registry_sha256"],
        "skill_tree_digest": source["skill_tree_sha256"],
    }


def captured_at(days_ago: int = 0) -> str:
    return (
        datetime.now(timezone.utc) - timedelta(days=days_ago, minutes=1)
    ).isoformat().replace("+00:00", "Z")


def reviewer_collection() -> dict:
    data = {
        "schema_version": external_runner.REVIEWER_COLLECTION_SCHEMA,
        "collection_id": "phase8-current-reviewer-receipts",
        "counts_as_runtime_evidence": False,
        "synthetic_test_only": False,
        "evidence_class": "preview_attested_platform_fresh_subagent_receipts",
        **phase8_identity(),
        "cases": [],
    }
    for case_index in range(1, 4):
        runs = []
        for repeat in range(1, 3):
            run_id = f"run-a0{case_index}-{repeat:02d}"
            runs.append(
                {
                    "run_id": run_id,
                    "parent_task_or_thread_id": f"parent-a0{case_index}-{repeat:02d}",
                    "captured_at": captured_at(),
                    "delegated_thread_id": f"thread-a0{case_index}-{repeat:02d}",
                    "normalized_capture_path": f"{run_id}-R.json",
                    "raw_transport_output_path": f"{run_id}-raw.json",
                    "scope_authority": "platform_derived",
                    "review_contract": {
                        "reviewer_instance_id": f"instance-a0{case_index}-{repeat:02d}",
                        "source_edits_performed": False,
                    },
                }
            )
        data["cases"].append({"case_id": f"case-a0{case_index}", "runs": runs})
    return data


def retrieval_collection() -> dict:
    specs = [
        ("search", 3),
        ("deep_research_completed", 2),
        ("deep_research_inactive_control", 1),
    ]
    receipts = []
    serial = 0
    for kind, count in specs:
        for _ in range(count):
            serial += 1
            receipts.append(
                {
                    "receipt_id": f"retrieval-{serial:02d}",
                    "kind": kind,
                    **phase8_identity(),
                    "captured_at": captured_at(),
                    "task_id": f"retrieval-task-{serial:02d}",
                    "normalized_capture_path": f"retrieval-{serial:02d}-R.json",
                    "platform_receipt_or_export_path": f"retrieval-{serial:02d}-export.json",
                }
            )
    return {
        "schema_version": external_runner.RETRIEVAL_COLLECTION_SCHEMA,
        "collection_id": "phase8-current-retrieval-receipts",
        "counts_as_runtime_evidence": False,
        "synthetic_test_only": False,
        "evidence_class": "preview_attested_platform_retrieval_receipts",
        "receipts": receipts,
    }


def expect_error(code: str, function) -> None:
    try:
        function()
    except Phase8ExternalEvidenceError as exc:
        assert exc.code == code, (code, exc.code, str(exc))
    else:
        raise AssertionError(f"expected {code}")


def dummy_bundle() -> BundleSnapshot:
    digest = "sha256:" + "d" * 64
    integrity = EvidenceValidationResult(
        evidence_id="evidence-01",
        integrity_valid=True,
        gate_eligible=False,
        verification_level=PREVIEW_ATTESTED,
        claimed_provider_verified=False,
        claimed_counts_as_preview_acceptance=True,
        provider_verified=False,
        counts_as_preview_acceptance=False,
        source_identity_bound=True,
        source_identity=identity(),
        raw_export_asset_id=1,
        raw_export_sha256=digest,
        evidence_envelope_asset_id=2,
        evidence_envelope_sha256=SHA_A,
        verifier_report_asset_id=3,
        verifier_report_sha256=SHA_B,
        release_asset_index_sha256=SHA_C,
    )
    slot = Slot("reviewer", "run-a01-01", "thread-a01-01", captured_at(), "raw.json", {})
    return BundleSnapshot(
        bundle_id="bundle-01",
        slot=slot,
        collection_anchor=False,
        index_path=Path("index.json"),
        index_document={},
        index_bytes=b"{}",
        assets={},
        envelope={},
        envelope_bytes=b"{}",
        integrity=integrity,
        collection_witness=False,
        witnessed_collection_paths={},
        workspace_files=(),
    )


def live_result(bundle: BundleSnapshot) -> dict:
    return {
        "schema_version": 3,
        "verdict": PREVIEW_ATTESTED,
        "adapter_id": PREVIEW_ADAPTER_ID,
        "source_identity": identity(),
        "integrity_valid": True,
        "gate_eligible": True,
        "counts_as_preview_attested": True,
        "counts_as_provider_verified": False,
        "provider_verified": False,
        "synthetic_self_test": False,
        "artifact_digests": {
            "raw_export_sha256": bundle.integrity.raw_export_sha256,
            "evidence_envelope_sha256": bundle.integrity.evidence_envelope_sha256,
            "verifier_report_sha256": bundle.integrity.verifier_report_sha256,
            "release_asset_index_sha256": bundle.integrity.release_asset_index_sha256,
        },
        "verified_assets": [
            {
                "asset_id": 999,
                "name": "index.json",
                "sha256": bundle.integrity.release_asset_index_sha256,
                "size": len(bundle.index_bytes),
                "evidence_kind": "release_asset_index",
                "state": "uploaded",
                "api_url": "https://api.github.com/repos/example/repo/releases/assets/999",
            }
        ],
        "integrity_result": {
            "evidence_id": bundle.integrity.evidence_id,
            "raw_export_asset_id": bundle.integrity.raw_export_asset_id,
            "raw_export_sha256": bundle.integrity.raw_export_sha256,
            "envelope_asset_id": bundle.integrity.evidence_envelope_asset_id,
            "envelope_sha256": bundle.integrity.evidence_envelope_sha256,
            "verifier_report_asset_id": bundle.integrity.verifier_report_asset_id,
            "verifier_report_sha256": bundle.integrity.verifier_report_sha256,
            "release_asset_index_sha256": bundle.integrity.release_asset_index_sha256,
        },
        "live_verifier": {
            "adapter_id": PREVIEW_ADAPTER_ID,
            "live_requery": True,
            "independent": True,
            "verifier_workflow_run_id": 12345,
            "verifier_run_url": "https://github.com/example/repo/actions/runs/12345",
            "verified_at": captured_at(),
        },
        "gate_eligibility": {
            "eligible": True,
            "level": PREVIEW_ATTESTED,
            "determined_by": "registered_live_verifier",
            "provider_authenticated": False,
        },
    }


def semantic_result() -> dict:
    distribution = {
        "deep_research_completed": 2,
        "deep_research_inactive_control": 1,
        "search": 3,
    }
    reviewer = {
        "external_live_capability_present": True,
        "preview_attested_review_count": 6,
        "provider_verified_live_review_count": 0,
        "unique_reviewer_instance_count": 6,
        "preview_gate_status": "completed",
        "verified_live_review_count": 0,
        "status": "preview_attested",
    }
    retrieval = {
        "external_live_capability_present": True,
        "preview_attested_current_receipts": 6,
        "preview_attested_current_receipts_by_kind": distribution,
        "preview_gate_status": "completed",
        "completed_current_receipts": 0,
        "pending_receipts": 0,
        "stale_receipts": 0,
        "observed_unverified_receipts": 0,
        "historical_release_mismatch_receipts": 0,
    }
    return {
        "reviewer": reviewer,
        "retrieval": retrieval,
        "phase8_report": {
            "phase_status": "complete_preview_attested",
            "acceptance_status": {
                "preview_attested": "complete",
                "provider_verified": "pending_strict_provider_evidence",
            },
            "corpus": {"metrics": {"false_ready_count": 0}},
            "live_fresh_repeat": reviewer,
            "retrieval": retrieval,
            "claims": {
                "preview_gate_complete": True,
                "provider_gate_complete": False,
                "accepted_verification_level": "preview_attested",
                "phase8_complete": True,
            },
        },
    }


def json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def asset_record(asset_id: int, name: str, kind: str, payload: bytes) -> dict[str, Any]:
    return {
        "asset_id": asset_id,
        "name": name,
        "evidence_kind": kind,
        "sha256": sha256_bytes(payload),
        "size": len(payload),
        "browser_download_url": (
            "https://github.com/example/research-skills/releases/download/"
            f"v0.7.0-preview.1/{name}"
        ),
    }


def make_external_collections() -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, bytes]]]:
    stamp = captured_at()
    reviewer = {
        "schema_version": external_runner.REVIEWER_COLLECTION_SCHEMA,
        "collection_id": "phase8-current-reviewer-receipts",
        "counts_as_runtime_evidence": False,
        "synthetic_test_only": False,
        "evidence_class": "preview_attested_platform_fresh_subagent_receipts",
        **phase8_identity(),
        "cases": [],
    }
    files: dict[str, dict[str, bytes]] = {}
    reviewer_serial = 0
    for case_index in range(1, 4):
        case_id = f"case-a0{case_index}"
        input_path = f"{case_id}-source.md"
        case_files: dict[str, bytes] = {input_path: f"source {case_id}".encode()}
        runs = []
        for repeat in range(1, 3):
            reviewer_serial += 1
            run_id = f"run-a0{case_index}-{repeat:02d}"
            raw_path = f"b{reviewer_serial:02d}-run-output.json"
            blind = f"b{reviewer_serial:02d}-blind.yaml"
            prompt = f"b{reviewer_serial:02d}-prompt.yaml"
            scope = f"b{reviewer_serial:02d}-scope.yaml"
            runs.append(
                {
                    "run_id": run_id,
                    "parent_task_or_thread_id": f"parent-a0{case_index}-{repeat:02d}",
                    "captured_at": captured_at(),
                    "delegated_thread_id": f"thread-a0{case_index}-{repeat:02d}",
                    "normalized_capture_path": f"b{reviewer_serial:02d}-R.json",
                    "raw_transport_output_path": raw_path,
                    "blind_bundle_path": blind,
                    "dispatch_prompt_path": prompt,
                    "platform_read_scope_export_path": scope,
                    "scope_authority": "platform_derived",
                    "review_contract": {
                        "reviewer_instance_id": f"instance-a0{case_index}-{repeat:02d}",
                        "files_read": [],
                        "files_written": [],
                        "source_edits_performed": False,
                    },
                }
            )
            slot_files = {
                raw_path: json_bytes({"captured_at": stamp, "run_id": run_id}),
                blind: b"schema_version: 1\n",
                prompt: b"schema_version: 1\n",
                scope: b"schema_version: 1\n",
            }
            if repeat == 1:
                slot_files.update(case_files)
            files[run_id] = slot_files
        reviewer["cases"].append(
            {"case_id": case_id, "input_path": input_path, "runs": runs}
        )

    retrieval = {
        "schema_version": external_runner.RETRIEVAL_COLLECTION_SCHEMA,
        "collection_id": "phase8-current-retrieval-receipts",
        "counts_as_runtime_evidence": False,
        "synthetic_test_only": False,
        "evidence_class": "preview_attested_platform_retrieval_receipts",
        "receipts": [],
    }
    kinds = ["search"] * 3 + ["deep_research_completed"] * 2 + ["deep_research_inactive_control"]
    for offset, kind in enumerate(kinds, start=1):
        receipt_id = f"retrieval-{offset:02d}"
        export_path = f"b{offset + 6:02d}-raw.json"
        receipt = {
            "receipt_id": receipt_id,
            "kind": kind,
            **phase8_identity(),
            "captured_at": stamp,
            "task_id": f"retrieval-task-{offset:02d}",
            "normalized_capture_path": f"b{offset + 6:02d}-R.json",
            "platform_receipt_or_export_path": export_path,
            "artifact_paths": [],
            "evidence_artifacts": [],
            "preview_attestation": {},
        }
        slot_files: dict[str, bytes] = {}
        if kind == "search":
            receipt.update(
                {
                    "raw_search_output_path": f"retrieval-{offset:02d}-search.yaml",
                    "citation_export_path": f"retrieval-{offset:02d}-citations.yaml",
                }
            )
            slot_files[receipt["raw_search_output_path"]] = b"schema_version: 1\n"
            slot_files[receipt["citation_export_path"]] = b"schema_version: 1\n"
        elif kind == "deep_research_completed":
            fields = (
                "raw_deep_research_output_path",
                "citation_export_path",
                "handoff_artifact",
                "user_start_event_path",
                "provider_run_completed_path",
                "mapper_return_artifact",
                "resume_receipt_path",
            )
            for field in fields:
                path = f"retrieval-{offset:02d}-{field}.yaml"
                receipt[field] = path
                slot_files[path] = b"schema_version: 1\n"
        else:
            receipt.update(
                {
                    "capability_state_export_path": f"retrieval-{offset:02d}-state.yaml",
                    "continuation_artifact": f"retrieval-{offset:02d}-continuation.yaml",
                }
            )
            slot_files[receipt["capability_state_export_path"]] = b"schema_version: 1\n"
            slot_files[receipt["continuation_artifact"]] = b"schema_version: 1\n"
        retrieval["receipts"].append(receipt)
        files[receipt_id] = slot_files
    return reviewer, retrieval, files


def build_external_bundle(
    root: Path,
    *,
    number: int,
    slot: Slot,
    logical_payloads: Mapping[str, bytes],
    anchor: bool,
    witness_collections: Mapping[str, bytes] | None = None,
) -> dict[str, Any]:
    prefix = f"b{number:02d}"
    raw_logical = "b01-raw.json" if anchor else slot.raw_path
    payloads = dict(logical_payloads)
    raw_payload = json_bytes(
        {
            "captured_at": slot.captured_at,
            "capture_format": "codex_json_export",
            "synthetic_test_only": False,
            "slot_id": slot.slot_id,
        }
    )
    payloads[raw_logical] = raw_payload
    if anchor and slot.raw_path not in payloads:
        payloads[slot.raw_path] = json_bytes(
            {"captured_at": slot.captured_at, "run_id": slot.slot_id}
        )
    if witness_collections:
        payloads.update(witness_collections)
    ids: dict[str, int] = {}
    records: list[dict[str, Any]] = []
    file_bindings = []
    for offset, (logical, payload) in enumerate(sorted(payloads.items()), start=1):
        asset_id = number * 1000 + offset
        physical = logical if "/" not in logical else f"{prefix}-file-{offset:02d}.bin"
        if (root / physical).exists():
            physical = f"{prefix}-file-{offset:02d}.bin"
        (root / physical).write_bytes(payload)
        ids[logical] = asset_id
        kind = "task_export" if logical == raw_logical else "supporting_file"
        records.append(asset_record(asset_id, physical, kind, payload))
        file_bindings.append(
            {
                "logical_path": logical,
                "asset_id": asset_id,
                "sha256": sha256_bytes(payload),
                "size": len(payload),
            }
        )
    manifest_id = number * 1000 + 900
    envelope_id = number * 1000 + 901
    report_id = number * 1000 + 902
    manifest = {
        "schema_version": external_runner.WORKSPACE_MANIFEST_SCHEMA,
        "counts_as_runtime_evidence": False,
        "synthetic_test_only": False,
        "bundle_id": f"bundle-{number:02d}",
        "slot_kind": slot.kind,
        "slot_id": slot.slot_id,
        "collection_anchor": anchor,
        "collection_witness": bool(witness_collections),
        "source_identity": identity(),
        "files": file_bindings,
    }
    manifest_bytes = json_bytes(manifest)
    captured = datetime.fromisoformat(slot.captured_at.replace("Z", "+00:00"))
    witnessed = captured + timedelta(seconds=10)
    verified = witnessed + timedelta(seconds=10)
    stamp = lambda value: value.isoformat().replace("+00:00", "Z")
    envelope = {
        "schema_version": EVIDENCE_ENVELOPE_SCHEMA,
        "evidence_id": f"phase8-evidence-{number:02d}",
        "verification_level": PREVIEW_ATTESTED,
        "provider_verified": False,
        "counts_as_preview_acceptance": True,
        "source_identity": identity(),
        "adapter": {
            "adapter_id": "codex-capture-adapter-v1",
            "adapter_code_sha256": "sha256:" + "4" * 64,
        },
        "capture": {
            "surface": "codex",
            "task_or_thread_id": slot.execution_id,
            "captured_at": slot.captured_at,
            "raw_export_asset_id": ids[raw_logical],
            "raw_export_sha256": sha256_bytes(raw_payload),
        },
        "github_witness": {
            "repository": "example/research-skills",
            "release_id": 700,
            "release_tag": "v0.7.0-preview.1",
            "workflow_run_id": 800,
            "actor": "fixture-actor",
            "raw_export_asset_id": ids[raw_logical],
            "source_commit": identity()["source_commit"],
        },
        "expected_verifier": {
            "verifier_id": "independent-preview-verifier-v1",
            "verifier_code_sha256": "sha256:" + "5" * 64,
            "independent": True,
        },
    }
    envelope_bytes = canonical_json_bytes(envelope)
    report = {
        "schema_version": VERIFIER_REPORT_SCHEMA,
        "verifier_id": "independent-preview-verifier-v1",
        "verifier_code_sha256": "sha256:" + "5" * 64,
        "source_identity": identity(),
        "envelope_asset_id": envelope_id,
        "envelope_sha256": sha256_bytes(envelope_bytes),
        "raw_export_asset_id": ids[raw_logical],
        "raw_export_sha256": sha256_bytes(raw_payload),
        "verdict": "accepted",
        "independent": True,
        "verified_at": stamp(verified),
    }
    report_bytes = json_bytes(report)
    named = {
        f"{prefix}-manifest.json": (manifest_id, "supporting_file", manifest_bytes),
        f"{prefix}-envelope.json": (envelope_id, "evidence_envelope", envelope_bytes),
        f"{prefix}-report.json": (report_id, "verifier_report", report_bytes),
    }
    for name, (asset_id, kind, payload) in named.items():
        (root / name).write_bytes(payload)
        records.append(asset_record(asset_id, name, kind, payload))
    index = {
        "schema_version": RELEASE_ASSET_INDEX_SCHEMA,
        "source_identity": identity(),
        "github_release": {
            "repository": "example/research-skills",
            "release_id": 700,
            "release_tag": "v0.7.0-preview.1",
        },
        "github_witness": {
            "workflow_run_id": 800,
            "actor": "fixture-actor",
            "source_commit": identity()["source_commit"],
            "witnessed_at": stamp(witnessed),
        },
        "assets": records,
    }
    index_path = root / f"{prefix}-index.json"
    index_bytes = json_bytes(index)
    index_path.write_bytes(index_bytes)
    return {
        "index_path": index_path.name,
        "index_digest": sha256_bytes(index_bytes),
        "envelope_path": f"{prefix}-envelope.json",
        "envelope_digest": sha256_bytes(envelope_bytes),
        "raw_path": raw_logical,
        "raw_digest": sha256_bytes(raw_payload),
    }


def embedded_attestation(metadata: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "adapter_id": PREVIEW_ADAPTER_ID,
        "envelope_path": metadata["envelope_path"],
        "envelope_digest": metadata["envelope_digest"],
        "release_asset_index_path": metadata["index_path"],
        "release_asset_index_digest": metadata["index_digest"],
        "raw_export_path": metadata["raw_path"],
        "raw_export_digest": metadata["raw_digest"],
        "synthetic_test_only": False,
    }


def complete_live_result(bundle: BundleSnapshot) -> dict[str, Any]:
    result = live_result(bundle)
    result["verified_assets"] = [
        {
            "asset_id": asset.asset_id,
            "name": asset.name,
            "sha256": asset.digest,
            "size": asset.size,
            "evidence_kind": asset.evidence_kind,
            "state": "uploaded",
            "api_url": f"https://api.github.com/repos/example/research-skills/releases/assets/{asset.asset_id}",
        }
        for asset in bundle.assets.values()
    ] + [
        {
            "asset_id": 900000 + int(bundle.bundle_id.rsplit("-", 1)[1]),
            "name": bundle.index_path.name,
            "sha256": bundle.integrity.release_asset_index_sha256,
            "size": len(bundle.index_bytes),
            "evidence_kind": "release_asset_index",
            "state": "uploaded",
            "api_url": "https://api.github.com/repos/example/research-skills/releases/assets/999999",
        }
    ]
    return result


class IntegrationLiveVerifier:
    adapter_id = PREVIEW_ADAPTER_ID

    def __call__(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return complete_live_result(request["bundle"])


def integration_contract() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="phase8-external-integration-") as directory:
        base = Path(directory)
        root = base / "evidence"
        control = base / "control"
        root.mkdir()
        control.mkdir()
        reviewer, retrieval, files = make_external_collections()
        reviewer_slots = _reviewer_slots(reviewer, identity())
        retrieval_slots = _retrieval_slots(retrieval, identity())
        ordered_reviewers = list(reviewer_slots.values())
        witness_slot = ordered_reviewers[-1]
        anchor_metadata: dict[str, Any] | None = None
        for number, slot in enumerate(ordered_reviewers[:-1], start=1):
            metadata = build_external_bundle(
                root,
                number=number,
                slot=slot,
                logical_payloads=files[slot.slot_id],
                anchor=number == 1,
            )
            if number == 1:
                anchor_metadata = metadata
        assert anchor_metadata is not None
        reviewer["preview_attestation"] = embedded_attestation(anchor_metadata)
        for number, slot in enumerate(retrieval_slots.values(), start=7):
            metadata = build_external_bundle(
                root,
                number=number,
                slot=slot,
                logical_payloads=files[slot.slot_id],
                anchor=False,
            )
            slot.subject["preview_attestation"] = embedded_attestation(metadata)
        reviewer_bytes = yaml.safe_dump(reviewer, sort_keys=False).encode()
        retrieval_bytes = yaml.safe_dump(retrieval, sort_keys=False).encode()
        build_external_bundle(
            root,
            number=6,
            slot=witness_slot,
            logical_payloads=files[witness_slot.slot_id],
            anchor=False,
            witness_collections={
                "phase8-reviewer-receipts.yaml": reviewer_bytes,
                "phase8-retrieval-receipts.yaml": retrieval_bytes,
            },
        )
        reviewer_path = control / "reviewer.yaml"
        retrieval_path = control / "retrieval.yaml"
        identity_path = control / "identity.json"
        reviewer_path.write_bytes(reviewer_bytes)
        retrieval_path.write_bytes(retrieval_bytes)
        identity_path.write_bytes(json_bytes(identity()))

        def semantic_validator(**kwargs):
            assert kwargs["reviewer_receipts_path"].is_file()
            assert kwargs["retrieval_receipts_path"].is_file()
            assert kwargs["source_identity"] == identity()
            records = kwargs["validated_live_records"]
            assert (
                len(records) == 12
                and len({item.slot_id for item in records}) == 12
                and len({item.execution_id for item in records}) == 12
                and sum(item.slot_kind == "reviewer" for item in records) == 6
                and sum(item.slot_kind == "retrieval" for item in records) == 6
            )
            return semantic_result()

        with patch.object(external_runner, "current_checkout_source_identity", lambda: identity()), patch.object(external_runner, "_assert_committed_source_identity", lambda _identity: None):
            try:
                validate_external_phase8_evidence(
                    evidence_root=root,
                    reviewer_receipts_path=reviewer_path,
                    retrieval_receipts_path=retrieval_path,
                    expected_source_identity_path=identity_path,
                    asset_index_pattern="b*-index.json",
                    live_verifier=IntegrationLiveVerifier(),
                    request_builder=lambda *, bundle, identity: {"bundle": bundle, "identity": identity},
                    semantic_validator=semantic_validator,
                )
            except Phase8ExternalEvidenceError as exc:
                assert exc.code in {
                    "slot_raw_export_binding",
                    "phase8_capture_invalid",
                    "phase8_live_capture_required",
                }, (exc.code, str(exc))
                return {"legacy_non_v2_bundle_rejected": True, "code": exc.code}
            raise AssertionError("legacy non-v2 Phase 8 bundle was accepted")


def capability_records() -> list[Any]:
    records = []
    for offset in range(12):
        kind = "reviewer" if offset < 6 else "retrieval"
        records.append(
            phase8_corpus.make_validated_phase8_live_slot(
                slot_id=f"slot-{offset:02d}",
                slot_kind=kind,
                execution_id=f"execution-{offset:02d}",
                subject={"slot": offset, "kind": kind},
                live_result={"verdict": "preview_attested", "slot": offset},
                evidence_id=f"evidence-{offset:02d}",
                verifier_workflow_run_id=1000 + offset,
                verified_at=captured_at(),
                issuer_capability=(
                    external_runner._PHASE8_EXTERNAL_VALIDATOR_ISSUER_CAPABILITY
                ),
            )
        )
    return records


def capability_lifecycle_contract() -> None:
    with tempfile.TemporaryDirectory(prefix="phase8-capability-") as directory:
        root = Path(directory)
        reviewer_path = root / "reviewer.yaml"
        retrieval_path = root / "retrieval.yaml"
        reviewer_path.write_text("schema_version: 1\n", encoding="utf-8")
        retrieval_path.write_text("schema_version: 1\n", encoding="utf-8")
        factory_arguments = {
            "slot_id": "forged-slot",
            "slot_kind": "reviewer",
            "execution_id": "forged-execution",
            "subject": {"slot": "forged"},
            "live_result": {"verdict": "preview_attested"},
            "evidence_id": "forged-evidence",
            "verifier_workflow_run_id": 999,
            "verified_at": captured_at(),
        }
        for issuer in (None, object()):
            try:
                phase8_corpus.make_validated_phase8_live_slot(
                    **factory_arguments,
                    issuer_capability=issuer,
                )
            except phase8_corpus.CorpusViolation as exc:
                assert exc.code == "phase8_external_live_record"
            else:
                raise AssertionError("public factory accepted a forged issuer")
        for operation in (pickle.dumps, copy.copy, copy.deepcopy):
            try:
                operation(
                    external_runner._PHASE8_EXTERNAL_VALIDATOR_ISSUER_CAPABILITY
                )
            except TypeError:
                pass
            else:
                raise AssertionError("external validator issuer was cloneable")
        try:
            phase8_corpus.ValidatedPhase8LiveSlot()
        except TypeError:
            pass
        else:
            raise AssertionError("manual live-slot construction was accepted")

        records = capability_records()
        for operation in (pickle.dumps, copy.copy, copy.deepcopy):
            try:
                operation(records[0])
            except TypeError:
                pass
            else:
                raise AssertionError("validated live slot was copyable/serializable")

        forged_record = object.__new__(phase8_corpus.ValidatedPhase8LiveSlot)
        for field, value in vars(records[0]).items():
            object.__setattr__(forged_record, field, value)
        object.__setattr__(forged_record, "_issuer_identity", object())
        forged_records = [forged_record, *records[1:]]
        try:
            with phase8_corpus.phase8_external_preview_session(
                workspace_root=root,
                reviewer_receipts_path=reviewer_path,
                retrieval_receipts_path=retrieval_path,
                source_identity=phase8_identity(),
                records=forged_records,
                issuer_capability=(
                    external_runner._PHASE8_EXTERNAL_VALIDATOR_ISSUER_CAPABILITY
                ),
            ):
                pass
        except phase8_corpus.CorpusViolation as exc:
            assert exc.code == "phase8_external_live_capability"
        else:
            raise AssertionError("manually forged live-slot record was accepted")

        with phase8_corpus.phase8_external_preview_session(
            workspace_root=root,
            reviewer_receipts_path=reviewer_path,
            retrieval_receipts_path=retrieval_path,
            source_identity=phase8_identity(),
            records=capability_records(),
            issuer_capability=(
                external_runner._PHASE8_EXTERNAL_VALIDATOR_ISSUER_CAPABILITY
            ),
        ) as capability:
            for operation in (pickle.dumps, copy.copy, copy.deepcopy):
                try:
                    operation(capability)
                except TypeError:
                    pass
                else:
                    raise AssertionError(
                        "external Preview capability was copyable/serializable"
                    )
            reviewer_records = phase8_corpus._external_preview_records(
                capability,
                root=root,
                data_path=reviewer_path,
                slot_kind="reviewer",
            )
            assert len(reviewer_records) == 6
            try:
                phase8_corpus._external_preview_records(
                    {"nonce": capability.nonce},  # type: ignore[arg-type]
                    root=root,
                    data_path=reviewer_path,
                    slot_kind="reviewer",
                )
            except phase8_corpus.CorpusViolation as exc:
                assert exc.code == "phase8_external_live_capability"
            else:
                raise AssertionError("serialized capability was accepted")
            reviewer_path.write_text("schema_version: 2\n", encoding="utf-8")
            try:
                phase8_corpus._external_preview_records(
                    capability,
                    root=root,
                    data_path=reviewer_path,
                    slot_kind="reviewer",
                )
            except phase8_corpus.CorpusViolation as exc:
                assert exc.code == "phase8_external_live_capability"
            else:
                raise AssertionError("collection mutation was accepted")

        try:
            phase8_corpus._external_preview_records(
                capability,
                root=root,
                data_path=reviewer_path,
                slot_kind="reviewer",
            )
        except phase8_corpus.CorpusViolation as exc:
            assert exc.code == "phase8_external_live_capability"
        else:
            raise AssertionError("inactive capability was accepted")


def default_semantic_bridge_contract() -> None:
    with tempfile.TemporaryDirectory(prefix="phase8-default-bridge-") as directory:
        root = Path(directory)
        reviewer_path = root / "reviewer.yaml"
        retrieval_path = root / "retrieval.yaml"
        reviewer_path.write_text("schema_version: 1\n", encoding="utf-8")
        retrieval_path.write_text("schema_version: 1\n", encoding="utf-8")
        expected_report = semantic_result()["phase8_report"]

        def fake_run_all(**kwargs):
            capability = kwargs["external_preview_capability"]
            assert len(
                phase8_corpus._external_preview_records(
                    capability,
                    root=root,
                    data_path=reviewer_path,
                    slot_kind="reviewer",
                )
            ) == 6
            assert len(
                phase8_corpus._external_preview_records(
                    capability,
                    root=root,
                    data_path=retrieval_path,
                    slot_kind="retrieval",
                )
            ) == 6
            return expected_report

        with patch.object(phase8_corpus, "run_all", fake_run_all):
            semantic = external_runner._default_semantic_validator(
                workspace_root=root,
                reviewer_receipts_path=reviewer_path,
                retrieval_receipts_path=retrieval_path,
                source_identity=identity(),
                validated_live_records=capability_records(),
            )
        assert semantic["phase8_report"] == expected_report


def main() -> int:
    guards: list[str] = []

    reviewers = _reviewer_slots(reviewer_collection(), identity())
    retrieval = _retrieval_slots(retrieval_collection(), identity())
    assert len(reviewers) == 6 and len(retrieval) == 6
    guards.append("exact_6_plus_6_distribution")

    missing = reviewer_collection()
    missing["cases"][0]["runs"].pop()
    expect_error("reviewer_repeat_count", lambda: _reviewer_slots(missing, identity()))
    guards.append("missing_reviewer_run_rejected")

    duplicate = reviewer_collection()
    duplicate["cases"][0]["runs"][1]["run_id"] = duplicate["cases"][0]["runs"][0]["run_id"]
    expect_error("duplicate_slot", lambda: _reviewer_slots(duplicate, identity()))
    guards.append("duplicate_reviewer_run_rejected")

    oracle = reviewer_collection()
    oracle["cases"][0]["runs"][0]["run_id"] = "fatal-oracle-run"
    expect_error("reviewer_outcome_oracle", lambda: _reviewer_slots(oracle, identity()))
    guards.append("outcome_oracle_identifier_rejected")

    mixed = reviewer_collection()
    mixed["source_commit"] = "2" * 40
    expect_error("mixed_release_evidence", lambda: _reviewer_slots(mixed, identity()))
    guards.append("mixed_source_identity_rejected")

    stale = reviewer_collection()
    stale["cases"][0]["runs"][0]["captured_at"] = captured_at(91)
    expect_error("stale_evidence", lambda: _reviewer_slots(stale, identity()))
    guards.append("stale_reviewer_run_rejected")

    shared_timestamp = reviewer_collection()
    shared_timestamp["captured_at"] = captured_at()
    expect_error(
        "reviewer_collection_shared_timestamp",
        lambda: _reviewer_slots(shared_timestamp, identity()),
    )
    guards.append("shared_reviewer_collection_timestamp_rejected")

    wrong_distribution = retrieval_collection()
    wrong_distribution["receipts"][0]["kind"] = "deep_research_completed"
    expect_error("retrieval_distribution", lambda: _retrieval_slots(wrong_distribution, identity()))
    guards.append("retrieval_distribution_rejected")

    all_slots = {**reviewers, **retrieval}
    _assert_slot_independence(all_slots)
    reused = dict(all_slots)
    key = next(iter(retrieval))
    reused[key] = Slot(
        reused[key].kind,
        reused[key].slot_id,
        next(iter(reviewers.values())).execution_id,
        reused[key].captured_at,
        reused[key].raw_path,
        reused[key].subject,
    )
    expect_error("execution_id_reused", lambda: _assert_slot_independence(reused))
    guards.append("execution_identity_reuse_rejected")

    subject = phase8_identity()
    subject["plugin_version"] = "0.7.0-preview.2"
    expect_error("mixed_release_evidence", lambda: _assert_subject_identity(subject, identity(), "subject"))
    guards.append("mixed_plugin_version_rejected")

    bundle = dummy_bundle()
    _validate_live_result(bundle, live_result(bundle), identity())
    forged = live_result(bundle)
    forged["live_verifier"]["live_requery"] = False
    expect_error("live_preview_verification_failed", lambda: _validate_live_result(bundle, forged, identity()))
    guards.append("offline_or_forged_live_result_rejected")

    distribution = _validate_semantic_result(semantic_result())
    assert distribution["search"] == 3
    false_ready = semantic_result()
    false_ready["reviewer"]["preview_attested_review_count"] = 5
    expect_error("phase8_semantic_result_incomplete", lambda: _validate_semantic_result(false_ready))
    guards.append("partial_semantic_result_rejected")

    parser = build_parser()
    required = [
        "--evidence-root", "root",
        "--reviewer-receipts", "reviewer.yaml",
        "--retrieval-receipts", "retrieval.yaml",
        "--expected-source-identity", "identity.json",
        "--asset-index-pattern", "*.json",
        "--synthetic",
    ]
    expect_error("invalid_cli_arguments", lambda: parser.parse_args(required))
    assert isinstance(parser, JsonArgumentParser)
    guards.append("no_synthetic_cli_switch")
    report_args = parser.parse_args(
        [
            "--evidence-root",
            "root",
            "--reviewer-receipts",
            "reviewer.yaml",
            "--retrieval-receipts",
            "retrieval.yaml",
            "--expected-source-identity",
            "identity.json",
            "--asset-index-pattern",
            "*.json",
            "--report-output",
            "phase8-report.json",
        ]
    )
    assert report_args.report_output == "phase8-report.json"
    guards.append("same_process_report_output_cli_supported")

    live_signature = inspect.signature(phase8_corpus.validate_live_fresh_repeats)
    retrieval_signature = inspect.signature(phase8_corpus.validate_retrieval_receipts)
    assert {"data_path", "root"} <= set(live_signature.parameters)
    assert {"data_path", "root"} <= set(retrieval_signature.parameters)
    guards.append("phase8_validators_accept_fresh_workspace")

    capability_lifecycle_contract()
    guards.extend(
        [
            "public_factory_forged_issuer_rejected",
            "external_validator_issuer_clone_rejected",
            "manual_live_slot_construction_rejected",
            "live_slot_pickle_copy_deepcopy_rejected",
            "manual_record_issuer_identity_rejected",
            "serialized_live_capability_rejected",
            "capability_pickle_copy_deepcopy_rejected",
            "mutated_collection_capability_rejected",
            "inactive_live_capability_rejected",
        ]
    )

    default_semantic_bridge_contract()
    guards.append("default_semantic_bridge_uses_active_live_session")

    ordinary_report = phase8_corpus.run_all()
    assert (
        ordinary_report["phase_status"] == "in_progress"
        and ordinary_report["live_fresh_repeat"][
            "external_live_capability_present"
        ]
        is False
        and ordinary_report["retrieval"]["external_live_capability_present"]
        is False
    )
    forged_report = copy.deepcopy(ordinary_report)
    forged_report["phase_status"] = "complete_preview_attested"
    forged_report["acceptance_status"]["preview_attested"] = "complete"
    forged_report["claims"].update(
        {
            "preview_gate_complete": True,
            "provider_gate_complete": False,
            "accepted_verification_level": "preview_attested",
            "phase8_complete": True,
        }
    )
    try:
        phase8_corpus.require_complete_preview_attested(forged_report)
    except phase8_corpus.CorpusViolation as exc:
        assert exc.code == "phase8_complete_preview_attested_required"
    else:
        raise AssertionError("serialized completion booleans advanced Phase 8")
    guards.extend(
        [
            "ordinary_cli_report_remains_pending_without_live_session",
            "serialized_completion_booleans_rejected",
        ]
    )

    integrated = integration_contract()
    assert integrated["legacy_non_v2_bundle_rejected"] is True
    guards.append("legacy_non_v2_twelve_bundle_path_rejected")

    print(f"Phase 8 external runner contracts passed: {len(guards)} guards")
    print(", ".join(guards))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
