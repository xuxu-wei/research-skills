#!/usr/bin/env python3
"""Deterministic tests for the acyclic integrity-only evidence DAG."""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Callable

from openai_preview_evidence import (
    CAPTURE_EXPORT_KINDS,
    EVIDENCE_ENVELOPE_SCHEMA,
    PREVIEW_ATTESTED,
    PROVIDER_VERIFIED,
    RELEASE_ASSET_INDEX_SCHEMA,
    VERIFIER_REPORT_SCHEMA,
    EvidenceValidationError,
    canonical_json_bytes,
    sha256_bytes,
    validate_evidence_bundle,
    validate_release_asset_index,
)


NOW = datetime(2026, 7, 13, 12, 0, 0, tzinfo=timezone.utc)
SOURCE_IDENTITY = {
    "plugin_version": "0.7.0-preview.1",
    "source_commit": "a" * 40,
    "manifest_sha256": "1" * 64,
    "registry_sha256": "2" * 64,
    "skill_tree_sha256": "3" * 64,
}
RAW_EXPORT = b'{"thread_id":"thread-001","items":[{"type":"message"}]}\n'
SCREENSHOT = b"fake-png-fixture"
PROVIDER_RECEIPT = b'{"provider":"openai","receipt_id":"provider-001"}\n'


def asset_record(asset_id: int, name: str, kind: str, payload: bytes) -> dict:
    return {
        "asset_id": asset_id,
        "name": name,
        "evidence_kind": kind,
        "sha256": sha256_bytes(payload),
        "size": len(payload),
    }


def build_envelope(provider: bool = False) -> dict:
    envelope = {
        "schema_version": EVIDENCE_ENVELOPE_SCHEMA,
        "evidence_id": "phase7-idea-happy-001",
        "verification_level": PROVIDER_VERIFIED if provider else PREVIEW_ATTESTED,
        "provider_verified": provider,
        "counts_as_preview_acceptance": True,
        "source_identity": copy.deepcopy(SOURCE_IDENTITY),
        "adapter": {
            "adapter_id": "codex_app_server_preview_v1",
            "adapter_code_sha256": "4" * 64,
        },
        "capture": {
            "surface": "codex_app_server",
            "task_or_thread_id": "thread-001",
            "captured_at": "2026-07-13T10:00:00Z",
            "raw_export_asset_id": 101,
            "raw_export_sha256": sha256_bytes(RAW_EXPORT),
        },
        "github_witness": {
            "repository": "xuxu/research-skills",
            "release_id": 7001,
            "release_tag": "research-skills-openai-v0.7.0-preview.1",
            "workflow_run_id": 9001,
            "actor": "preview-release-bot",
            "source_commit": SOURCE_IDENTITY["source_commit"],
            "raw_export_asset_id": 101,
        },
        "expected_verifier": {
            "verifier_id": "preview_bundle_verifier_v1",
            "verifier_code_sha256": "5" * 64,
            "independent": True,
        },
    }
    if provider:
        envelope["capture"]["provider_receipt_asset_id"] = 103
    return envelope


def build_bundle(
    *,
    provider: bool = False,
    screenshot_only: bool = False,
    mutate_envelope: Callable[[dict], None] | None = None,
    mutate_report: Callable[[dict], None] | None = None,
    duplicate_envelope: bool = False,
    duplicate_report: bool = False,
) -> dict:
    payloads: dict[int, bytes] = {
        101: RAW_EXPORT,
        102: SCREENSHOT,
        103: PROVIDER_RECEIPT,
    }
    envelope = build_envelope(provider)
    if mutate_envelope is not None:
        mutate_envelope(envelope)
    envelope_bytes = canonical_json_bytes(envelope)
    payloads[104] = envelope_bytes

    expected = envelope.get("expected_verifier", {})
    capture = envelope.get("capture", {})
    raw_id = capture.get("raw_export_asset_id", 101)
    raw_payload = payloads.get(raw_id, RAW_EXPORT)
    report = {
        "schema_version": VERIFIER_REPORT_SCHEMA,
        "verifier_id": expected.get("verifier_id", "preview_bundle_verifier_v1"),
        "verifier_code_sha256": expected.get("verifier_code_sha256", "5" * 64),
        "independent": True,
        "verified_at": "2026-07-13T10:02:00Z",
        "verdict": "accepted",
        "source_identity": copy.deepcopy(envelope.get("source_identity", SOURCE_IDENTITY)),
        "envelope_asset_id": 104,
        "envelope_sha256": sha256_bytes(envelope_bytes),
        "raw_export_asset_id": raw_id,
        "raw_export_sha256": sha256_bytes(raw_payload),
    }
    if provider:
        receipt_id = capture.get("provider_receipt_asset_id", 103)
        receipt_payload = payloads.get(receipt_id, PROVIDER_RECEIPT)
        report.update(
            {
                "provider_receipt_asset_id": receipt_id,
                "provider_receipt_sha256": sha256_bytes(receipt_payload),
                "provider_attestation_checked": True,
            }
        )
    if mutate_report is not None:
        mutate_report(report)
    report_bytes = canonical_json_bytes(report)
    payloads[105] = report_bytes

    if screenshot_only:
        assets = [asset_record(102, "screen.png", "screenshot", SCREENSHOT)]
    else:
        assets = [asset_record(101, "task-export.jsonl", "raw_export", RAW_EXPORT)]
        assets.append(asset_record(102, "screen.png", "screenshot", SCREENSHOT))
    if provider:
        assets.append(
            asset_record(103, "provider-receipt.json", "provider_receipt", PROVIDER_RECEIPT)
        )
    assets.extend(
        [
            asset_record(104, "evidence-envelope.json", "evidence_envelope", envelope_bytes),
            asset_record(105, "verifier-report.json", "verifier_report", report_bytes),
        ]
    )
    if duplicate_envelope:
        payloads[106] = envelope_bytes
        assets.append(
            asset_record(106, "duplicate-envelope.json", "evidence_envelope", envelope_bytes)
        )
    if duplicate_report:
        payloads[107] = report_bytes
        assets.append(asset_record(107, "duplicate-report.json", "verifier_report", report_bytes))

    index = {
        "schema_version": RELEASE_ASSET_INDEX_SCHEMA,
        "source_identity": copy.deepcopy(SOURCE_IDENTITY),
        "github_release": {
            "repository": "xuxu/research-skills",
            "release_id": 7001,
            "release_tag": "research-skills-openai-v0.7.0-preview.1",
        },
        "github_witness": {
            "workflow_run_id": 9001,
            "actor": "preview-release-bot",
            "source_commit": SOURCE_IDENTITY["source_commit"],
            "witnessed_at": "2026-07-13T10:01:00Z",
        },
        "assets": assets,
    }
    return {
        "envelope": envelope,
        "envelope_bytes": envelope_bytes,
        "report": report,
        "report_bytes": report_bytes,
        "index": index,
        "store": payloads,
    }


def fetcher(store: dict[int, bytes]):
    def fetch(record: dict) -> bytes:
        return store[record["asset_id"]]

    return fetch


def validate(bundle: dict, expected_identity: dict | None = SOURCE_IDENTITY):
    return validate_evidence_bundle(
        bundle["envelope"],
        bundle["index"],
        fetcher(bundle["store"]),
        envelope_bytes=bundle["envelope_bytes"],
        expected_source_identity=expected_identity,
        now=NOW,
    )


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def expect_error(code: str, call, label: str) -> None:
    try:
        call()
    except EvidenceValidationError as exc:
        require(exc.code == code, f"{label}: expected {code}, got {exc.code}: {exc}")
    else:
        raise AssertionError(f"{label}: expected {code}")


def replace_indexed_asset(bundle: dict, asset_id: int, payload: bytes) -> None:
    bundle["store"][asset_id] = payload
    record = next(item for item in bundle["index"]["assets"] if item["asset_id"] == asset_id)
    record["sha256"] = sha256_bytes(payload)
    record["size"] = len(payload)


def main() -> int:
    require(
        CAPTURE_EXPORT_KINDS == {"raw_export", "structured_export", "task_export"},
        "capture exports exclude provider receipts",
    )

    bundle = build_bundle()
    result = validate(bundle)
    require(result.integrity_valid and not result.gate_eligible, "integrity-only result")
    require(result.verification_level == PREVIEW_ATTESTED, "claimed level preserved")
    require(not result.provider_verified, "provider authentication is outside core")
    require(not result.counts_as_preview_acceptance, "core never counts acceptance")
    require(result.claimed_counts_as_preview_acceptance, "claimed acceptance preserved")
    require(result.source_identity_bound, "expected identity bound")
    require(result.evidence_envelope_asset_id == 104, "actual envelope asset located")
    require(result.evidence_envelope_sha256 == sha256_bytes(bundle["envelope_bytes"]), "E digest")
    require(result.verifier_report_asset_id == 105, "verifier report located")
    require(result.verifier_report_sha256 == sha256_bytes(bundle["report_bytes"]), "V digest")

    unbound = validate(bundle, None)
    require(not unbound.source_identity_bound and not unbound.gate_eligible, "identity unbound")

    provider_bundle = build_bundle(provider=True)
    provider_result = validate(provider_bundle)
    require(provider_result.verification_level == PROVIDER_VERIFIED, "provider claim level")
    require(provider_result.claimed_provider_verified, "provider claim preserved")
    require(not provider_result.provider_verified, "provider claim never promoted locally")

    provider_as_raw = build_bundle(
        provider=True,
        mutate_envelope=lambda item: (
            item["capture"].update(
                raw_export_asset_id=103,
                raw_export_sha256=sha256_bytes(PROVIDER_RECEIPT),
            ),
            item["github_witness"].update(raw_export_asset_id=103),
        ),
    )
    expect_error(
        "non_substantive_raw_export",
        lambda: validate(provider_as_raw),
        "provider receipt is not a capture export",
    )

    same_provider_id = build_bundle(
        provider=True,
        mutate_envelope=lambda item: item["capture"].update(provider_receipt_asset_id=101),
    )
    expect_error(
        "provider_receipt_not_distinct",
        lambda: validate(same_provider_id),
        "provider receipt and raw export IDs differ",
    )

    modified_document = copy.deepcopy(bundle["envelope"])
    modified_document["evidence_id"] = "locally-rewritten-envelope"
    modified_bytes = canonical_json_bytes(modified_document)
    rewritten = dict(bundle)
    rewritten["envelope"] = modified_document
    rewritten["envelope_bytes"] = modified_bytes
    expect_error(
        "asset_digest_mismatch",
        lambda: validate(rewritten),
        "local envelope rewrite differs from indexed bytes",
    )
    mismatched_mapping = dict(bundle)
    mismatched_mapping["envelope"] = modified_document
    expect_error(
        "envelope_document_mismatch",
        lambda: validate(mismatched_mapping),
        "mapping cannot differ from raw envelope bytes",
    )

    rewritten_index = copy.deepcopy(bundle)
    rewritten_index["envelope"] = modified_document
    rewritten_index["envelope_bytes"] = modified_bytes
    rewritten_index["index"] = copy.deepcopy(bundle["index"])
    rewritten_index["store"] = dict(bundle["store"])
    replace_indexed_asset(rewritten_index, 104, modified_bytes)
    expect_error(
        "verifier_report_binding_mismatch",
        lambda: validate(rewritten_index),
        "report detects envelope rewrite even when local index is rewritten",
    )

    report_tamper = copy.deepcopy(bundle)
    report_tamper["store"] = dict(bundle["store"])
    report_tamper["store"][105] = bundle["report_bytes"] + b" "
    expect_error(
        "asset_size_mismatch",
        lambda: validate(report_tamper),
        "verifier report content tamper",
    )

    bad_report_binding = copy.deepcopy(bundle)
    bad_report_binding["index"] = copy.deepcopy(bundle["index"])
    bad_report_binding["store"] = dict(bundle["store"])
    bad_report = copy.deepcopy(bundle["report"])
    bad_report["raw_export_sha256"] = "0" * 64
    bad_report_bytes = canonical_json_bytes(bad_report)
    replace_indexed_asset(bad_report_binding, 105, bad_report_bytes)
    expect_error(
        "verifier_report_binding_mismatch",
        lambda: validate(bad_report_binding),
        "indexed report with rewritten binding",
    )

    report_index_cycle = copy.deepcopy(bundle)
    report_index_cycle["index"] = copy.deepcopy(bundle["index"])
    report_index_cycle["store"] = dict(bundle["store"])
    cyclic_report = copy.deepcopy(bundle["report"])
    cyclic_report["asset_index_sha256"] = "6" * 64
    replace_indexed_asset(report_index_cycle, 105, canonical_json_bytes(cyclic_report))
    expect_error(
        "circular_digest_binding",
        lambda: validate(report_index_cycle),
        "report cannot digest its later index",
    )

    forward_result = build_bundle(
        mutate_envelope=lambda item: item.update(
            verifier={"verdict": "accepted", "verifier_report_sha256": "6" * 64}
        )
    )
    expect_error(
        "forward_reference_in_envelope",
        lambda: validate(forward_result),
        "E cannot include later V result",
    )
    index_cycle = build_bundle(
        mutate_envelope=lambda item: item["github_witness"].update(
            asset_index_sha256="6" * 64
        )
    )
    expect_error(
        "circular_digest_binding",
        lambda: validate(index_cycle),
        "E cannot digest later I",
    )

    duplicate_e = build_bundle(duplicate_envelope=True)
    expect_error(
        "ambiguous_witness_envelope_asset",
        lambda: validate(duplicate_e),
        "I must identify one E",
    )
    duplicate_v = build_bundle(duplicate_report=True)
    expect_error(
        "ambiguous_verifier_report_asset",
        lambda: validate(duplicate_v),
        "I must identify one V",
    )

    tampered_raw = copy.deepcopy(bundle)
    tampered_raw["store"] = dict(bundle["store"])
    tampered_raw["store"][101] = RAW_EXPORT + b"tampered"
    expect_error("asset_size_mismatch", lambda: validate(tampered_raw), "raw tamper")

    digest_mismatch = copy.deepcopy(bundle)
    digest_mismatch["index"] = copy.deepcopy(bundle["index"])
    digest_mismatch["index"]["assets"][0]["sha256"] = "0" * 64
    expect_error("asset_digest_mismatch", lambda: validate(digest_mismatch), "index digest")

    screenshot_bundle = build_bundle(screenshot_only=True)
    expect_error(
        "non_substantive_evidence_only",
        lambda: validate_release_asset_index(
            screenshot_bundle["index"], fetcher(screenshot_bundle["store"]), now=NOW
        ),
        "screenshot-only index",
    )

    no_envelope = copy.deepcopy(bundle)
    no_envelope["index"] = copy.deepcopy(bundle["index"])
    no_envelope["index"]["assets"] = [
        item for item in no_envelope["index"]["assets"] if item["evidence_kind"] != "evidence_envelope"
    ]
    expect_error("missing_witness_envelope_asset", lambda: validate(no_envelope), "missing E")
    no_report = copy.deepcopy(bundle)
    no_report["index"] = copy.deepcopy(bundle["index"])
    no_report["index"]["assets"] = [
        item for item in no_report["index"]["assets"] if item["evidence_kind"] != "verifier_report"
    ]
    expect_error("missing_verifier_report_asset", lambda: validate(no_report), "missing V")

    wrong_version = dict(SOURCE_IDENTITY)
    wrong_version["plugin_version"] = "0.7.0-preview.2"
    expect_error(
        "source_identity_mismatch",
        lambda: validate(bundle, wrong_version),
        "wrong expected version",
    )
    wrong_commit = dict(SOURCE_IDENTITY)
    wrong_commit["source_commit"] = "b" * 40
    expect_error(
        "source_identity_mismatch",
        lambda: validate(bundle, wrong_commit),
        "wrong expected commit",
    )

    conflicting_level = build_bundle(
        mutate_envelope=lambda item: item.update(provider_verified=True)
    )
    expect_error(
        "verification_level_conflict",
        lambda: validate(conflicting_level),
        "verification claim conflict",
    )
    missing_receipt = build_bundle(
        provider=True,
        mutate_envelope=lambda item: item["capture"].update(provider_receipt_asset_id=999),
    )
    expect_error("missing_provider_receipt", lambda: validate(missing_receipt), "missing receipt")

    witness_mismatch = build_bundle(
        mutate_envelope=lambda item: item["github_witness"].update(release_id=7002)
    )
    expect_error("github_witness_mismatch", lambda: validate(witness_mismatch), "wrong witness")
    verifier_reuse = build_bundle(
        mutate_envelope=lambda item: item["expected_verifier"].update(
            verifier_id=item["adapter"]["adapter_id"]
        )
    )
    expect_error(
        "verifier_not_independent", lambda: validate(verifier_reuse), "verifier identity reuse"
    )

    capture_after_witness = build_bundle(
        mutate_envelope=lambda item: item["capture"].update(
            captured_at="2026-07-13T10:01:01Z"
        )
    )
    expect_error(
        "invalid_timestamp_order",
        lambda: validate(capture_after_witness),
        "capture precedes witness",
    )
    verify_before_witness = build_bundle(
        mutate_report=lambda item: item.update(verified_at="2026-07-13T10:00:59Z")
    )
    expect_error(
        "invalid_timestamp_order",
        lambda: validate(verify_before_witness),
        "verification follows witness",
    )
    future_capture = build_bundle(
        mutate_envelope=lambda item: item["capture"].update(
            captured_at="2026-07-13T12:05:01Z"
        )
    )
    expect_error(
        "timestamp_too_far_in_future", lambda: validate(future_capture), "future timestamp"
    )
    stale_index = copy.deepcopy(bundle)
    stale_index["index"] = copy.deepcopy(bundle["index"])
    stale_index["index"]["github_witness"]["witnessed_at"] = "2026-04-13T11:59:59Z"
    expect_error("stale_evidence_timestamp", lambda: validate(stale_index), "stale timestamp")

    print("OpenAI Preview evidence DAG integrity tests passed")
    print(
        "coverage: constructible R->E->V->I DAG, actual envelope bytes, report bindings, "
        "no cycles, integrity-only semantics, identity, kinds, tamper, chronology, freshness"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
