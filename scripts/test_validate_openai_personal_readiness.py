#!/usr/bin/env python3
"""Contract tests for the personal-owner readiness validator."""

from __future__ import annotations

import copy
import tempfile
from pathlib import Path

import validate_openai_personal_readiness as validator


def observed_binding(plugin_version: str, slot_id: str, *, search: bool = False) -> dict:
    return {
        "task_id": f"task-{slot_id}",
        "plugin_version": plugin_version,
        "source_identity": "commit:0123456789abcdef0123456789abcdef01234567",
        "artifact_bindings": [
            {
                "artifact_id": f"artifact-{slot_id}",
                "version": "v001",
                "path": f"artifacts/{slot_id}.json",
                "sha256": "a" * 64,
            }
        ],
        "reviewer_instance_ids": (
            [f"reviewer-{slot_id}"] if "happy" in slot_id else []
        ),
        "source_urls": ["https://example.org/source"] if search else [],
        "started_at": "2026-07-14T00:00:00Z",
        "completed_at": "2026-07-14T00:10:00Z",
        "owner_confirmed": True,
    }


def promote_all(receipts: dict, plugin_version: str) -> dict:
    promoted = copy.deepcopy(receipts)
    items = [promoted["distribution"]]
    for group in ("workflow_runs", "control_runs", "retrieval_runs"):
        items.extend(promoted[group])
    for item in items:
        item["status"] = "owner_observed"
        item["actual_outcome"] = item["expected_outcome"]
        item["binding"] = observed_binding(
            plugin_version,
            item["slot_id"],
            search=item.get("kind") == "search",
        )
    return promoted


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        lf_path = Path(directory) / "lf.txt"
        crlf_path = Path(directory) / "crlf.txt"
        lf_path.write_bytes(b"alpha\nbeta\n")
        crlf_path.write_bytes(b"alpha\r\nbeta\r\n")
        assert validator.file_sha256(lf_path) == validator.file_sha256(crlf_path)

    deterministic, deterministic_errors = validator.deterministic_checks()
    assert not deterministic_errors, deterministic_errors
    plugin_version = deterministic["plugin_version"]
    receipts = validator.load_yaml(validator.RECEIPTS)

    pending, pending_errors = validator.validate_receipts(receipts, plugin_version)
    assert not pending_errors, pending_errors
    assert pending["status"] == "in_progress_owner_observation"
    assert pending["owner_observed_slot_count"] == 0
    assert pending["pending_slot_count"] == 13

    promoted = promote_all(receipts, plugin_version)
    ready, ready_errors = validator.validate_receipts(promoted, plugin_version)
    assert not ready_errors, ready_errors
    assert ready["status"] == "owner_observed_ready"
    assert ready["owner_observed_slot_count"] == 13
    assert ready["pending_slot_count"] == 0

    broken = copy.deepcopy(promoted)
    broken["workflow_runs"][0]["binding"]["reviewer_instance_ids"] = []
    not_ready, broken_errors = validator.validate_receipts(broken, plugin_version)
    assert broken_errors
    assert not_ready["status"] == "in_progress_owner_observation"

    report, report_errors = validator.build_report()
    assert not report_errors, report_errors
    assert report["deterministic_status"] == "deterministic_validated"
    assert report["personal_status"] == "in_progress_owner_observation"
    assert report["claims"]["owner_observed_is_external_attestation"] is False
    assert report["claims"]["owner_observed_is_provider_verified"] is False

    print("Personal readiness validator tests passed: 4 scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
