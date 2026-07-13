#!/usr/bin/env python3
"""CLI fixture tests for the acyclic local evidence integrity validator."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from openai_preview_evidence import (
    EVIDENCE_ENVELOPE_SCHEMA,
    RELEASE_ASSET_INDEX_SCHEMA,
    VERIFIER_REPORT_SCHEMA,
    sha256_bytes,
)


SCRIPT_DIR = Path(__file__).resolve().parent
CLI = SCRIPT_DIR / "validate_openai_preview_evidence_bundle.py"
NOW_TEXT = "2026-07-13T12:00:00Z"
SOURCE_IDENTITY = {
    "plugin_version": "0.7.0-preview.1",
    "source_commit": "a" * 40,
    "manifest_sha256": "1" * 64,
    "registry_sha256": "2" * 64,
    "skill_tree_sha256": "3" * 64,
}
RAW_EXPORT = b'{"thread_id":"thread-001","items":[{"type":"message"}]}\n'
PROVIDER_RECEIPT = b'{"provider":"openai","receipt_id":"receipt-001"}\n'


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def write_json(path: Path, document: dict) -> bytes:
    payload = (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(payload)
    return payload


def asset_record(asset_id: int, name: str, kind: str, payload: bytes) -> dict:
    return {
        "asset_id": asset_id,
        "name": name,
        "evidence_kind": kind,
        "sha256": sha256_bytes(payload),
        "size": len(payload),
    }


def build_fixture(
    root: Path, *, provider: bool = False, asset_key: str = "name"
) -> dict[str, Path]:
    assets = root / "assets"
    assets.mkdir()
    envelope = {
        "schema_version": EVIDENCE_ENVELOPE_SCHEMA,
        "evidence_id": "phase8-provider-001" if provider else "phase7-idea-happy-001",
        "verification_level": "provider_verified" if provider else "preview_attested",
        "provider_verified": provider,
        "counts_as_preview_acceptance": True,
        "source_identity": SOURCE_IDENTITY,
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
    envelope_path = root / "evidence-envelope.json"
    envelope_bytes = write_json(envelope_path, envelope)

    report = {
        "schema_version": VERIFIER_REPORT_SCHEMA,
        "verifier_id": "preview_bundle_verifier_v1",
        "verifier_code_sha256": "5" * 64,
        "independent": True,
        "verified_at": "2026-07-13T10:02:00Z",
        "verdict": "accepted",
        "source_identity": SOURCE_IDENTITY,
        "envelope_asset_id": 104,
        "envelope_sha256": sha256_bytes(envelope_bytes),
        "raw_export_asset_id": 101,
        "raw_export_sha256": sha256_bytes(RAW_EXPORT),
    }
    if provider:
        report.update(
            {
                "provider_receipt_asset_id": 103,
                "provider_receipt_sha256": sha256_bytes(PROVIDER_RECEIPT),
                "provider_attestation_checked": True,
            }
        )
    report_path = root / "verifier-report.json"
    report_bytes = write_json(report_path, report)

    payloads = [
        (101, "task-export.jsonl", "raw_export", RAW_EXPORT),
        (104, "evidence-envelope.json", "evidence_envelope", envelope_bytes),
        (105, "verifier-report.json", "verifier_report", report_bytes),
    ]
    if provider:
        payloads.insert(
            1, (103, "provider-receipt.json", "provider_receipt", PROVIDER_RECEIPT)
        )
    for asset_id, name, _kind, payload in payloads:
        (assets / (name if asset_key == "name" else str(asset_id))).write_bytes(payload)

    index = {
        "schema_version": RELEASE_ASSET_INDEX_SCHEMA,
        "source_identity": SOURCE_IDENTITY,
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
        "assets": [asset_record(*item) for item in payloads],
    }
    index_path = root / "asset-index.json"
    write_json(index_path, index)

    capture_only = dict(envelope)
    capture_only["verification_level"] = "capture_only"
    capture_only_path = root / "capture-only-envelope.json"
    write_json(capture_only_path, capture_only)
    identity_path = root / "expected-identity.json"
    write_json(identity_path, {"source_identity": SOURCE_IDENTITY})
    wrong_identity_path = root / "wrong-identity.json"
    wrong_identity = dict(SOURCE_IDENTITY)
    wrong_identity["source_commit"] = "b" * 40
    write_json(wrong_identity_path, wrong_identity)
    return {
        "assets": assets,
        "index": index_path,
        "envelope": envelope_path,
        "capture_only": capture_only_path,
        "identity": identity_path,
        "wrong_identity": wrong_identity_path,
        "report": assets / ("verifier-report.json" if asset_key == "name" else "105"),
    }


def run_cli(*args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(CLI), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    require(not completed.stderr, f"unexpected stderr: {completed.stderr}")
    try:
        output = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"CLI did not emit JSON: {completed.stdout!r}") from exc
    return completed.returncode, output


def base_args(paths: dict[str, Path], *, asset_key: str = "name") -> list[str]:
    return [
        "--asset-index",
        str(paths["index"]),
        "--asset-dir",
        str(paths["assets"]),
        "--asset-key",
        asset_key,
        "--now",
        NOW_TEXT,
    ]


def require_integrity_only(output: dict, label: str) -> None:
    require(output["integrity_valid"], f"{label}: integrity valid")
    require(not output["gate_eligible"], f"{label}: not gate eligible")
    require(not output["accepted"], f"{label}: not accepted")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="preview-evidence-cli-") as temp:
        paths = build_fixture(Path(temp))
        code, output = run_cli(
            *base_args(paths),
            "--envelope",
            str(paths["envelope"]),
            "--expected-source-identity",
            str(paths["identity"]),
        )
        require(code == 0, "fixture integrity-valid")
        require_integrity_only(output, "fixture")
        require(output["identity_binding"] == "bound_to_expected_source", "identity bound")
        require(output["summary"]["claimed_preview_attested"] == 1, "claim counted")
        require(output["envelopes"][0]["evidence_envelope_asset_id"] == 104, "E located")
        require(output["envelopes"][0]["verifier_report_asset_id"] == 105, "V located")

        direct_identity_args = [
            "--expected-plugin-version",
            SOURCE_IDENTITY["plugin_version"],
            "--expected-source-commit",
            SOURCE_IDENTITY["source_commit"],
            "--expected-manifest-sha256",
            SOURCE_IDENTITY["manifest_sha256"],
            "--expected-registry-sha256",
            SOURCE_IDENTITY["registry_sha256"],
            "--expected-skill-tree-sha256",
            SOURCE_IDENTITY["skill_tree_sha256"],
        ]
        code, output = run_cli(
            *base_args(paths),
            "--envelope",
            str(paths["envelope"]),
            *direct_identity_args,
        )
        require(code == 0, "direct identity")
        require_integrity_only(output, "direct identity")

        code, output = run_cli(
            *base_args(paths), "--envelope", str(paths["envelope"])
        )
        require(code == 0, "unbound integrity succeeds")
        require_integrity_only(output, "unbound")
        require(output["identity_binding"] == "identity_unbound", "unbound explicit")

        code, output = run_cli(
            *base_args(paths), "--envelope", str(paths["capture_only"])
        )
        require(code == 1 and output["error"]["code"] == "invalid_verification_level", "capture")

        code, output = run_cli(
            *base_args(paths),
            "--envelope",
            str(paths["envelope"]),
            "--expected-source-identity",
            str(paths["wrong_identity"]),
        )
        require(code == 1 and output["error"]["code"] == "source_identity_mismatch", "identity")

        envelope_doc = json.loads(paths["envelope"].read_text(encoding="utf-8"))
        envelope_doc["evidence_id"] = "locally-rewritten"
        write_json(paths["envelope"], envelope_doc)
        code, output = run_cli(
            *base_args(paths), "--envelope", str(paths["envelope"])
        )
        require(code == 1 and output["error"]["code"] == "asset_digest_mismatch", "E rewrite")

    with tempfile.TemporaryDirectory(prefix="preview-provider-cli-") as temp:
        provider_paths = build_fixture(Path(temp), provider=True)
        code, output = run_cli(
            *base_args(provider_paths),
            "--envelope",
            str(provider_paths["envelope"]),
        )
        require(code == 0, "provider fixture integrity-valid")
        require_integrity_only(output, "provider")
        require(output["summary"]["claimed_provider_verified"] == 1, "provider claim")
        require(not output["envelopes"][0]["provider_verified"], "not authenticated")
        provider_paths["report"].write_bytes(provider_paths["report"].read_bytes() + b" ")
        code, output = run_cli(
            *base_args(provider_paths),
            "--envelope",
            str(provider_paths["envelope"]),
        )
        require(code == 1 and output["error"]["code"] == "asset_size_mismatch", "V tamper")

    with tempfile.TemporaryDirectory(prefix="preview-id-cli-") as temp:
        id_paths = build_fixture(Path(temp), asset_key="asset_id")
        code, output = run_cli(
            *base_args(id_paths, asset_key="asset_id"),
            "--envelope",
            str(id_paths["envelope"]),
        )
        require(code == 0, "asset ID lookup")
        require_integrity_only(output, "asset ID lookup")

    source = CLI.read_text(encoding="utf-8")
    for forbidden in ("requests", "urllib", "http.client", "socket"):
        require(forbidden not in source, f"network dependency forbidden: {forbidden}")

    code, output = run_cli("--asset-index", "missing.json")
    require(code == 2 and not output["integrity_valid"], "argument error JSON")
    require(output["error"]["code"] == "invalid_cli_arguments", "argument code")

    print("OpenAI Preview evidence DAG integrity CLI tests passed")
    print(
        "fixtures: real E/V assets, actual envelope bytes, claimed/provider separation, "
        "identity bound/unbound, local E/V tamper, name/asset-id lookup, no network imports"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
