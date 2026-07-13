#!/usr/bin/env python3
"""Fail-closed tests for protected Preview completion and run summary binding."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Callable

from build_openai_preview_accepted_summary import (
    AcceptedSummaryError,
    EXTERNAL_RECORD_PATHS,
    EXPECTED_PHASE8_RETRIEVAL_RECEIPTS,
    EXPECTED_PHASE8_REVIEWER_CASES,
    PHASE7_COMPLETION_GATE_IDS,
    build_summary,
    strict_phase78_snapshot,
)


SOURCE = "a" * 40
REPOSITORY = "owner/repository"
EVIDENCE_TAG = "v0.7.0-preview.1-evidence"
CANDIDATE_TAG = "v0.7.0-preview.1-candidate"
CANDIDATE_NAMES = (
    "accepted-ledger.json",
    "phase7.yaml",
    "phase8-reviewer.yaml",
    "phase8-retrieval.yaml",
)


def dump(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )


def accepted_reports() -> tuple[dict[str, Any], dict[str, Any]]:
    workflows = ("idea", "proposal", "article", "perspective", "research_polisher")
    runtime_results = [
        {
            "receipt_id": f"p7-{workflow}-{kind}",
            "workflow": workflow,
            "case_kind": kind,
            "status": "verified",
            "verification_level": "preview_attested",
        }
        for workflow in workflows
        for kind in ("happy", "control")
    ]
    for offset, item in enumerate(runtime_results):
        item.update(
            external_evidence_id=f"phase7-evidence-{offset}",
            external_live_result_digest="sha256:"
            + hashlib.sha256(f"phase7-live-{offset}".encode()).hexdigest(),
            external_verifier_workflow_run_id=7000 + offset,
            external_verified_at="2026-07-14T00:00:00Z",
        )
    phase7 = {
        "plugin_version": "0.7.0-preview.1",
        "phase_status": "complete_preview_attested",
        "verification_level": "preview_attested",
        "counts_as_preview_acceptance": True,
        "provider_verified": False,
        "pending_gates": [],
        "completion_gates": {
            gate_id: {"status": "verified"}
            for gate_id in PHASE7_COMPLETION_GATE_IDS
        },
        "runtime_receipts": {
            "results": runtime_results,
            "verified_receipt_count": 10,
            "pending_receipt_count": 0,
        },
        "summary": {
            "runtime_receipts_verified": 10,
            "runtime_receipts_pending": 0,
            "completion_gates_verified": 13,
            "completion_gates_pending": 0,
            "false_ready_count": 0,
        },
    }
    cases = []
    review_digests = {}
    for case_index, (case_id, reviewer_skill) in enumerate(
        EXPECTED_PHASE8_REVIEWER_CASES.items()
    ):
        run_ids = [f"run-{case_index}-{run}" for run in range(2)]
        instance_ids = [f"instance-{case_index}-{run}" for run in range(2)]
        for run_id in run_ids:
            review_digests[run_id] = "sha256:" + hashlib.sha256(run_id.encode()).hexdigest()
        cases.append(
            {
                "case_id": case_id,
                "fresh_runs": 2,
                "run_ids": run_ids,
                "reviewer_instance_ids": instance_ids,
                "reviewer_skill": reviewer_skill,
                "input_digest": "sha256:" + hashlib.sha256(f"input-{case_index}".encode()).hexdigest(),
                "review_stage_state": "revision_required",
            }
        )
    receipt_results = [
        {
            "receipt_id": receipt_id,
            "kind": kind,
            "evidence_status": "preview_attested",
            "evidence_trust_level": "preview_attested",
        }
        for receipt_id, kind in EXPECTED_PHASE8_RETRIEVAL_RECEIPTS.items()
    ]
    phase8 = {
        "plugin_version": "0.7.0-preview.1",
        "phase_status": "complete_preview_attested",
        "acceptance_status": {
            "preview_attested": "complete",
            "provider_verified": "pending_strict_provider_evidence",
        },
        "corpus": {"metrics": {"false_ready_count": 0}},
        "live_fresh_repeat": {
            "case_results": cases,
            "review_content_digests": review_digests,
            "preview_attested_review_count": 6,
            "provider_verified_live_review_count": 0,
            "verified_live_review_count": 0,
            "unique_reviewer_instance_count": 6,
            "historical_release_mismatch": False,
            "historical_release_mismatch_snapshot_count": 0,
            "preview_gate_status": "completed",
            "status": "preview_attested",
        },
        "retrieval": {
            "receipt_results": receipt_results,
            "preview_attested_current_receipts": 6,
            "preview_attested_current_receipts_by_kind": {
                "search": 3,
                "deep_research_completed": 2,
                "deep_research_inactive_control": 1,
            },
            "completed_current_receipts": 0,
            "pending_receipts": 0,
            "stale_receipts": 0,
            "historical_release_mismatch_receipts": 0,
            "observed_unverified_receipts": 0,
            "preview_gate_status": "completed",
        },
        "claims": {
            "preview_gate_complete": True,
            "provider_gate_complete": False,
            "accepted_verification_level": "preview_attested",
            "preview_attested_retrieval_receipts": 6,
            "provider_verified_phase8_complete": False,
        },
        "provider_trust": {},
    }
    return phase7, phase8


def fixture(root: Path) -> dict[str, Any]:
    evidence_dir = root / "evidence"
    candidate_dir = root / "candidate"
    evidence_dir.mkdir()
    candidate_dir.mkdir()
    candidate_payloads = {
        CANDIDATE_NAMES[0]: b"placeholder",
        CANDIDATE_NAMES[1]: b"phase7",
        CANDIDATE_NAMES[2]: b"phase8-reviewer",
        CANDIDATE_NAMES[3]: b"phase8-retrieval",
    }
    phase7, phase8 = accepted_reports()
    external_records = {}
    evidence_assets = []
    role_fields = (
        "envelope_asset",
        "release_asset_index_asset",
        "raw_export_asset",
        "verifier_report_asset",
    )
    for type_offset, evidence_type in enumerate((
        "repository_preview_ci",
        "canonical_plugin_validator_ci",
        "main_branch_protection",
        "marketplace_resolved_commit",
        "marketplace_upgrade",
        "explicit_reinstall",
        "fresh_task_discovery",
        "rollback",
    )):
        locator: dict[str, Any] = {
            "repository": REPOSITORY,
            "release_id": 11,
            "release_tag": EVIDENCE_TAG,
        }
        for asset_offset, role in enumerate(role_fields):
            asset_id = 1000 + type_offset * 4 + asset_offset
            name = f"{evidence_type}-{role}.json"
            payload = f"{evidence_type}:{role}".encode()
            (evidence_dir / name).write_bytes(payload)
            bare = hashlib.sha256(payload).hexdigest()
            locator[role] = {"asset_id": asset_id, "name": name, "sha256": bare}
            evidence_assets.append(
                {
                    "id": asset_id,
                    "name": name,
                    "size": len(payload),
                    "state": "uploaded",
                    "digest": "sha256:" + bare,
                }
            )
        external_records[evidence_type] = {
            "status": "preview_attested",
            "evidence_locator": locator,
        }
    release = {
        "version": "0.7.0-preview.1",
        "source_commit": {"sha": SOURCE},
        "ci": {
            "repository_preview": external_records["repository_preview_ci"],
            "canonical_plugin_validator": {
                "ci": external_records["canonical_plugin_validator_ci"]
            },
        },
        "governance": {
            "main_branch_protection": external_records["main_branch_protection"]
        },
        "marketplace_source": {
            "resolved_commit": external_records["marketplace_resolved_commit"]
        },
        "receipts": {
            name: external_records[name]
            for name in (
                "marketplace_upgrade",
                "explicit_reinstall",
                "fresh_task_discovery",
                "rollback",
            )
        },
    }
    previous = copy.deepcopy(release)
    previous["source_commit"] = {"sha": "b" * 40}

    def record_at(container: dict[str, Any], evidence_type: str) -> dict[str, Any]:
        value: Any = container
        for part in EXTERNAL_RECORD_PATHS[evidence_type]:
            value = value[part]
        assert isinstance(value, dict)
        return value

    for historical_type in EXTERNAL_RECORD_PATHS:
        historical_record = record_at(previous, historical_type)
        historical_record.clear()
        historical_record["status"] = "pending"

    history_results: list[dict[str, Any]] = []
    for history_offset, evidence_type in enumerate(
        ("marketplace_resolved_commit", "rollback"), start=1
    ):
        locator: dict[str, Any] = {
            "repository": REPOSITORY,
            "release_id": 20,
            "release_tag": "v0.6.0-preview.1-evidence",
        }
        history_asset_ids: list[int] = []
        for role_offset, role in enumerate(role_fields):
            asset_id = 5000 + history_offset * 10 + role_offset
            history_asset_ids.append(asset_id)
            locator[role] = {
                "asset_id": asset_id,
                "name": f"history-{evidence_type}-{role}.json",
                "sha256": hashlib.sha256(
                    f"history:{evidence_type}:{role}".encode()
                ).hexdigest(),
            }
        record_at(previous, evidence_type).update(
            status="preview_attested", evidence_locator=locator
        )
        locator_digest = "sha256:" + hashlib.sha256(
            json.dumps(locator, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        history_results.append(
            {
                "evidence_type": evidence_type,
                "evidence_id": f"history-evidence-{evidence_type}",
                "release_scope": "previous_releases[0]",
                "verification_level": "preview_attested",
                "provider_verified": False,
                "source_commit": "b" * 40,
                "locator_sha256": locator_digest,
                "validated_result_sha256": "sha256:"
                + hashlib.sha256(f"history-result:{evidence_type}".encode()).hexdigest(),
                "verified_asset_ids": history_asset_ids,
                "verifier_workflow_run_id": 9500 + history_offset,
                "verified_at": "2026-07-14T00:00:00Z",
            }
        )

    ledger = {"release": release, "previous_releases": [previous]}
    dump(candidate_dir / CANDIDATE_NAMES[0], ledger)
    for name, payload in candidate_payloads.items():
        if name != CANDIDATE_NAMES[0]:
            (candidate_dir / name).write_bytes(payload)
    candidate_assets = []
    for index, name in enumerate(CANDIDATE_NAMES, start=201):
        payload = (candidate_dir / name).read_bytes()
        candidate_assets.append(
            {
                "id": index,
                "name": name,
                "size": len(payload),
                "state": "uploaded",
                "digest": "sha256:" + hashlib.sha256(payload).hexdigest(),
            }
        )
    paths = {
        "evidence_release_json": root / "evidence-release.json",
        "candidate_release_json": root / "candidate-release.json",
        "evidence_assets_json": root / "evidence-assets.json",
        "candidate_assets_json": root / "candidate-assets.json",
        "phase7_report_path": root / "phase7-report.json",
        "phase8_report_path": root / "phase8-report.json",
        "phase78_bridge_result_path": root / "phase78-bridge-result.json",
        "release_runner_result_path": root / "release-result.json",
        "candidate_ledger_path": candidate_dir / CANDIDATE_NAMES[0],
        "evidence_asset_dir": evidence_dir,
        "candidate_asset_dir": candidate_dir,
    }
    dump(
        paths["evidence_release_json"],
        {"id": 11, "tag_name": EVIDENCE_TAG, "draft": False, "prerelease": True, "immutable": True},
    )
    dump(
        paths["candidate_release_json"],
        {"id": 12, "tag_name": CANDIDATE_TAG, "draft": False, "prerelease": True, "immutable": True},
    )
    dump(paths["candidate_assets_json"], [candidate_assets, []])
    dump(paths["phase7_report_path"], phase7)
    dump(paths["phase8_report_path"], phase8)

    next_asset_id = 3000

    def live_slot_bundle(
        *, slot_id: str, evidence_id: str, live_digest: str, run_id: int
    ) -> dict[str, Any]:
        nonlocal next_asset_id
        index_name = f"{slot_id}-index.json"
        assets: list[dict[str, Any]] = []
        indexed: list[dict[str, Any]] = []
        for suffix, evidence_kind in (
            ("raw", "raw_export"),
            ("envelope", "evidence_envelope"),
            ("verifier", "verifier_report"),
        ):
            name = f"{slot_id}-{suffix}.json"
            payload = f"{suffix}:{slot_id}".encode()
            asset_id = next_asset_id
            next_asset_id += 1
            (evidence_dir / name).write_bytes(payload)
            bare = hashlib.sha256(payload).hexdigest()
            evidence_assets.append(
                {
                    "id": asset_id,
                    "name": name,
                    "size": len(payload),
                    "state": "uploaded",
                    "digest": "sha256:" + bare,
                }
            )
            asset = {
                "asset_id": asset_id,
                "name": name,
                "size": len(payload),
                "sha256": "sha256:" + bare,
                "evidence_kind": evidence_kind,
            }
            assets.append(asset)
            indexed.append(dict(asset))
        index_payload = json.dumps(
            {"slot_id": slot_id, "assets": indexed},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        index_asset_id = next_asset_id
        next_asset_id += 1
        (evidence_dir / index_name).write_bytes(index_payload)
        index_bare = hashlib.sha256(index_payload).hexdigest()
        evidence_assets.append(
            {
                "id": index_asset_id,
                "name": index_name,
                "size": len(index_payload),
                "state": "uploaded",
                "digest": "sha256:" + index_bare,
            }
        )
        return {
            "evidence_id": evidence_id,
            "live_result_digest": live_digest,
            "verifier_workflow_run_id": run_id,
            "verified_at": "2026-07-14T00:00:00Z",
            "release": {
                "repository": REPOSITORY,
                "release_id": 11,
                "release_tag": EVIDENCE_TAG,
            },
            "asset_index": {
                "name": index_name,
                "size": len(index_payload),
                "sha256": "sha256:" + index_bare,
            },
            "assets": assets,
        }

    phase7_slots = []
    for item in phase7["runtime_receipts"]["results"]:
        phase7_slots.append(
            {
                "receipt_id": item["receipt_id"],
                **live_slot_bundle(
                    slot_id=item["receipt_id"],
                    evidence_id=item["external_evidence_id"],
                    live_digest=item["external_live_result_digest"],
                    run_id=item["external_verifier_workflow_run_id"],
                ),
            }
        )
    normalized = strict_phase78_snapshot(phase7, phase8)
    reviewer_ids = [item["run_id"] for item in normalized["phase8"]["reviewer_items"]]
    retrieval_ids = [
        item["receipt_id"] for item in normalized["phase8"]["retrieval_items"]
    ]
    phase8_slots = []
    for offset, (slot_id, kind) in enumerate(
        [(value, "reviewer") for value in reviewer_ids]
        + [(value, "retrieval") for value in retrieval_ids]
    ):
        phase8_slots.append(
            {
                "slot_id": slot_id,
                "slot_kind": kind,
                "execution_id": f"execution-{offset}",
                "subject_digest": "sha256:"
                + hashlib.sha256(f"subject-{slot_id}".encode()).hexdigest(),
                **live_slot_bundle(
                    slot_id=slot_id,
                    evidence_id=f"phase8-evidence-{offset}",
                    live_digest="sha256:"
                    + hashlib.sha256(f"phase8-live-{offset}".encode()).hexdigest(),
                    run_id=8000 + offset,
                ),
            }
        )
    dump(
        paths["evidence_assets_json"],
        [
            evidence_assets[offset : offset + 100]
            for offset in range(0, len(evidence_assets), 100)
        ]
        + [[]],
    )
    dump(
        paths["phase78_bridge_result_path"],
        {
            "schema_version": "openai-preview-accepted-phase78-run/v1",
            "accepted": True,
            "verification_level": "preview_attested",
            "provider_verified": False,
            "complete_preview_release_validator": "passed_with_fresh_callback",
            "candidate_collection_digests": {
                "phase7_runtime_receipts": "sha256:"
                + hashlib.sha256((candidate_dir / CANDIDATE_NAMES[1]).read_bytes()).hexdigest(),
                "phase8_reviewer_receipts": "sha256:"
                + hashlib.sha256((candidate_dir / CANDIDATE_NAMES[2]).read_bytes()).hexdigest(),
                "phase8_retrieval_receipts": "sha256:"
                + hashlib.sha256((candidate_dir / CANDIDATE_NAMES[3]).read_bytes()).hexdigest(),
            },
            "phase7": {
                "phase_status": "complete_preview_attested",
                "report_sha256": "sha256:"
                + hashlib.sha256(
                    json.dumps(phase7, sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest(),
                "runtime_results": normalized["phase7"]["items"],
                "live_slot_results": phase7_slots,
            },
            "phase8": {
                "phase_status": "complete_preview_attested",
                "report_sha256": "sha256:"
                + hashlib.sha256(
                    json.dumps(phase8, sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest(),
                "live_slot_results": phase8_slots,
                "reviewer_results": normalized["phase8"]["reviewer_items"],
                "retrieval_results": normalized["phase8"]["retrieval_items"],
            },
        },
    )
    dump(
        paths["release_runner_result_path"],
        {
            "schema_version": "openai-release-evidence-runner-result/v1",
            "validated": True,
            "live_gate_eligible": True,
            "adapter_id": "openai-preview-github-live-v1",
            "verified_record_count": 8,
            "historical_verified_record_count": len(history_results),
            "ledger_sha256": "sha256:"
            + hashlib.sha256(paths["candidate_ledger_path"].read_bytes()).hexdigest(),
            "evidence_types": sorted(external_records),
            "history_results": history_results,
            "live_results": [
                {
                    "evidence_type": evidence_type,
                    "evidence_id": f"release-evidence-{evidence_type}",
                    "release_scope": "current",
                    "verification_level": "preview_attested",
                    "provider_verified": False,
                    "source_commit": SOURCE,
                    "locator_sha256": "sha256:"
                    + hashlib.sha256(
                        json.dumps(
                            external_records[evidence_type]["evidence_locator"],
                            sort_keys=True,
                            separators=(",", ":"),
                        ).encode()
                    ).hexdigest(),
                    "validated_result_sha256": "sha256:"
                    + hashlib.sha256(f"result-{evidence_type}".encode()).hexdigest(),
                    "verified_asset_ids": sorted(
                        external_records[evidence_type]["evidence_locator"][role][
                            "asset_id"
                        ]
                        for role in role_fields
                    ),
                    "verifier_workflow_run_id": 9000 + offset,
                    "verified_at": "2026-07-14T00:00:00Z",
                }
                for offset, evidence_type in enumerate(sorted(external_records))
            ],
        },
    )
    paths.update(
        {
            "repository": REPOSITORY,
            "source_commit": SOURCE,
            "evidence_release_tag": EVIDENCE_TAG,
            "candidate_release_tag": CANDIDATE_TAG,
            "evidence_final_commit": SOURCE,
            "candidate_final_commit": SOURCE,
            "run_id": 123,
            "run_attempt": 2,
            "candidate_asset_names": CANDIDATE_NAMES,
        }
    )
    return paths


def rejected(mutator: Callable[[dict[str, Any]], None]) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        values = fixture(Path(temporary))
        mutator(values)
        try:
            build_summary(**values)
        except AcceptedSummaryError:
            return
        raise AssertionError("invalid accepted-run fixture was accepted")


def mutate_json(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    dump(path, value)


def use_alternate_ledger_path(values: dict[str, Any]) -> None:
    source = values["candidate_ledger_path"]
    alternate = source.parent.parent / "alternate-ledger.json"
    alternate.write_bytes(source.read_bytes())
    values["candidate_ledger_path"] = alternate


def swap_ledger_after_runner(values: dict[str, Any]) -> None:
    ledger_path = values["candidate_ledger_path"]
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["post_runner_swap"] = True
    dump(ledger_path, ledger)
    payload = ledger_path.read_bytes()
    pages = json.loads(values["candidate_assets_json"].read_text(encoding="utf-8"))
    ledger_asset = next(
        item for page in pages for item in page if item.get("name") == CANDIDATE_NAMES[0]
    )
    ledger_asset["size"] = len(payload)
    ledger_asset["digest"] = "sha256:" + hashlib.sha256(payload).hexdigest()
    dump(values["candidate_assets_json"], pages)


def duplicate_evidence_id_across_files(values: dict[str, Any]) -> None:
    runner_result = json.loads(
        values["release_runner_result_path"].read_text(encoding="utf-8")
    )
    duplicated = runner_result["live_results"][0]["evidence_id"]
    mutate_json(
        values["phase78_bridge_result_path"],
        lambda bridge: bridge["phase7"]["live_slot_results"][0].__setitem__(
            "evidence_id", duplicated
        ),
    )


def duplicate_chain_bytes_with_new_asset_id(values: dict[str, Any]) -> None:
    bridge = json.loads(
        values["phase78_bridge_result_path"].read_text(encoding="utf-8")
    )
    phase7_raw = next(
        item
        for item in bridge["phase7"]["live_slot_results"][0]["assets"]
        if item["evidence_kind"] == "raw_export"
    )
    phase8_raw = next(
        item
        for item in bridge["phase8"]["live_slot_results"][0]["assets"]
        if item["evidence_kind"] == "raw_export"
    )
    payload = (values["evidence_asset_dir"] / phase7_raw["name"]).read_bytes()
    target = values["evidence_asset_dir"] / phase8_raw["name"]
    target.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    phase8_raw["size"] = len(payload)
    phase8_raw["sha256"] = "sha256:" + digest
    dump(values["phase78_bridge_result_path"], bridge)
    pages = json.loads(values["evidence_assets_json"].read_text(encoding="utf-8"))
    api_asset = next(
        item
        for page in pages
        for item in page
        if item.get("id") == phase8_raw["asset_id"]
    )
    api_asset["size"] = len(payload)
    api_asset["digest"] = "sha256:" + digest
    dump(values["evidence_assets_json"], pages)


def main() -> int:
    phase7, phase8 = accepted_reports()
    snapshot = strict_phase78_snapshot(phase7, phase8)
    assert len(snapshot["phase7"]["items"]) == 10
    assert len(snapshot["phase8"]["reviewer_items"]) == 6
    assert len(snapshot["phase8"]["retrieval_items"]) == 6
    with tempfile.TemporaryDirectory() as temporary:
        summary = build_summary(**fixture(Path(temporary)))
    assert summary["schema_version"] == "openai-preview-accepted-run-summary/v1"
    assert summary["run_attempt"] == 2
    assert len(summary["release_evidence"]["items"]) == 8
    assert len(summary["release_evidence"]["history_items"]) == 2
    assert summary["release_evidence"]["unique_current_chain_count"] == 30
    assert summary["release_evidence"]["unique_current_chain_digest_count"] == 120
    assert summary["final_status"]["accepted"] is True

    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda values: values.__setitem__("candidate_final_commit", "b" * 40),
        lambda values: mutate_json(values["evidence_release_json"], lambda item: item.__setitem__("immutable", False)),
        use_alternate_ledger_path,
        swap_ledger_after_runner,
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: item.__setitem__("validated", False)),
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: (item["history_results"].clear(), item.__setitem__("historical_verified_record_count", 0))),
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: (item["history_results"].pop(), item.__setitem__("historical_verified_record_count", 1))),
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: (item["history_results"].append(copy.deepcopy(item["history_results"][0])), item.__setitem__("historical_verified_record_count", 3))),
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: item["history_results"][0].__setitem__("release_scope", "previous_releases[1]")),
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: item["history_results"][0].__setitem__("locator_sha256", "sha256:" + "0" * 64)),
        lambda values: mutate_json(values["phase7_report_path"], lambda item: item.__setitem__("phase_status", "in_progress_live_and_release_evidence_pending")),
        lambda values: mutate_json(values["phase7_report_path"], lambda item: item["runtime_receipts"].__setitem__("pending_receipt_count", 1)),
        lambda values: mutate_json(values["phase7_report_path"], lambda item: item["completion_gates"][next(iter(item["completion_gates"]))].__setitem__("status", "pending")),
        lambda values: mutate_json(values["phase7_report_path"], lambda item: (item["completion_gates"].pop(next(iter(item["completion_gates"]))), item["completion_gates"].__setitem__("wrong-gate-id", {"status": "verified"}))),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item.__setitem__("phase_status", "in_progress")),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item["live_fresh_repeat"].__setitem__("preview_attested_review_count", 5)),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item["live_fresh_repeat"]["case_results"][0].__setitem__("case_id", "case-wrong")),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item["live_fresh_repeat"]["case_results"][0].__setitem__("reviewer_skill", "wrong-reviewer")),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item["live_fresh_repeat"]["case_results"][1]["reviewer_instance_ids"].__setitem__(0, "instance-0-0")),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item["retrieval"].__setitem__("stale_receipts", 1)),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item["retrieval"]["receipt_results"][0].__setitem__("receipt_id", "retrieval-wrong")),
        lambda values: mutate_json(values["phase8_report_path"], lambda item: item["retrieval"]["receipt_results"][0].__setitem__("evidence_status", "observed_unverified")),
        lambda values: mutate_json(values["candidate_assets_json"], lambda pages: pages[0][0].__setitem__("size", pages[0][0]["size"] + 1)),
        lambda values: mutate_json(values["candidate_assets_json"], lambda pages: pages.pop()),
        lambda values: mutate_json(values["candidate_assets_json"], lambda pages: pages.insert(1, [])),
        lambda values: mutate_json(values["candidate_ledger_path"], lambda item: item["release"]["receipts"]["rollback"].__setitem__("status", "pending")),
        lambda values: mutate_json(values["candidate_ledger_path"], lambda item: item["release"]["receipts"]["rollback"]["evidence_locator"].__setitem__("release_tag", "old-evidence")),
        lambda values: mutate_json(values["candidate_ledger_path"], lambda item: item["release"]["receipts"]["rollback"]["evidence_locator"]["envelope_asset"].__setitem__("asset_id", 999999)),
        lambda values: mutate_json(values["evidence_assets_json"], lambda pages: pages[0][0].__setitem__("digest", "sha256:" + "f" * 64)),
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: item["live_results"][0]["verified_asset_ids"].__setitem__(0, 999999)),
        lambda values: mutate_json(values["release_runner_result_path"], lambda item: item["live_results"][0].__setitem__("release_scope", "previous_releases[0]")),
        duplicate_evidence_id_across_files,
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item["phase7"]["live_slot_results"][1].__setitem__("evidence_id", item["phase7"]["live_slot_results"][0]["evidence_id"])),
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item["phase8"]["live_slot_results"][0].__setitem__("evidence_id", item["phase7"]["live_slot_results"][0]["evidence_id"])),
        duplicate_chain_bytes_with_new_asset_id,
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item.__setitem__("accepted", False)),
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item["phase7"].__setitem__("report_sha256", "sha256:" + "0" * 64)),
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item["phase7"]["live_slot_results"][0].__setitem__("evidence_id", "forged-evidence")),
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item["phase8"]["live_slot_results"][0].__setitem__("slot_id", "wrong-slot")),
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item["candidate_collection_digests"].__setitem__("phase7_runtime_receipts", "sha256:" + "0" * 64)),
        lambda values: mutate_json(values["phase78_bridge_result_path"], lambda item: item["phase8"]["live_slot_results"][0]["release"].__setitem__("release_tag", "old-evidence")),
    ]
    for mutation in mutations:
        rejected(mutation)
    print(f"OpenAI Preview accepted-run summary contracts passed: {len(mutations)} guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
