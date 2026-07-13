#!/usr/bin/env python3
"""Validate local evidence-bundle integrity without network access.

This CLI does not authenticate a provider and never promotes evidence into a
Preview or release gate.  Gate-oriented callers must add an authenticated
outer adapter and bind the complete expected source identity.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from openai_preview_evidence import (
    PREVIEW_ATTESTED,
    PROVIDER_VERIFIED,
    EvidenceValidationError,
    validate_evidence_envelope,
    validate_release_asset_index,
)


RESULT_SCHEMA = "openai-preview-evidence-validation-result/v1"
DIRECT_IDENTITY_ARGUMENTS = {
    "plugin_version": "expected_plugin_version",
    "source_commit": "expected_source_commit",
    "manifest_sha256": "expected_manifest_sha256",
    "registry_sha256": "expected_registry_sha256",
    "skill_tree_sha256": "expected_skill_tree_sha256",
}


class JsonArgumentParser(argparse.ArgumentParser):
    """Convert argparse failures into the CLI's machine-readable error shape."""

    def error(self, message: str) -> None:
        raise EvidenceValidationError("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(
        description=(
            "Validate structural, digest, identity, and chronology integrity for "
            "locally materialized evidence assets. This command is not a gate."
        )
    )
    parser.add_argument("--asset-index", required=True, help="Local JSON/YAML Release asset index")
    parser.add_argument(
        "--envelope",
        action="append",
        required=True,
        help="Evidence envelope; repeat for multiple envelopes",
    )
    parser.add_argument("--asset-dir", required=True, help="Directory containing fetched Release assets")
    parser.add_argument(
        "--asset-key",
        choices=("auto", "name", "asset_id"),
        default="auto",
        help="Resolve assets by index name, numeric asset ID, or either",
    )
    parser.add_argument(
        "--expected-source-identity",
        help="JSON/YAML source identity mapping (or document with source_identity)",
    )
    parser.add_argument("--expected-plugin-version")
    parser.add_argument("--expected-source-commit")
    parser.add_argument("--expected-manifest-sha256")
    parser.add_argument("--expected-registry-sha256")
    parser.add_argument("--expected-skill-tree-sha256")
    parser.add_argument(
        "--now",
        help="ISO-8601 verification clock for deterministic replay/testing; defaults to current UTC",
    )
    return parser


def _load_mapping(path: Path, logical_path: str) -> tuple[Mapping[str, Any], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise EvidenceValidationError(
            "file_read_failed", logical_path, f"{path}: {type(exc).__name__}: {exc}"
        ) from exc
    try:
        loaded = yaml.safe_load(payload)
    except yaml.YAMLError as exc:
        raise EvidenceValidationError(
            "invalid_document", logical_path, f"{path}: {exc}"
        ) from exc
    if not isinstance(loaded, Mapping):
        raise EvidenceValidationError(
            "invalid_document", logical_path, f"{path}: expected a mapping"
        )
    return loaded, payload


def _expected_source_identity(args: argparse.Namespace) -> Mapping[str, Any] | None:
    direct = {
        field: getattr(args, argument)
        for field, argument in DIRECT_IDENTITY_ARGUMENTS.items()
        if getattr(args, argument) is not None
    }
    if args.expected_source_identity and direct:
        raise EvidenceValidationError(
            "expected_identity_conflict",
            "cli.expected_source_identity",
            "use either an identity file or direct expected-identity arguments, not both",
        )
    if args.expected_source_identity:
        document, _ = _load_mapping(
            Path(args.expected_source_identity), "cli.expected_source_identity"
        )
        candidate = document.get("source_identity", document)
        if not isinstance(candidate, Mapping):
            raise EvidenceValidationError(
                "invalid_document",
                "cli.expected_source_identity",
                "source_identity must be a mapping",
            )
        expected = candidate
    else:
        expected = direct or None
    if expected is not None:
        missing = sorted(set(DIRECT_IDENTITY_ARGUMENTS) - set(expected))
        if missing:
            raise EvidenceValidationError(
                "expected_identity_incomplete",
                "cli.expected_source_identity",
                f"missing expected identity fields: {', '.join(missing)}",
            )
    return expected


def _verification_clock(args: argparse.Namespace) -> datetime | None:
    if args.now is None:
        return None
    try:
        parsed = datetime.fromisoformat(args.now.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceValidationError(
            "invalid_timestamp", "cli.now", "expected an ISO-8601 timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise EvidenceValidationError(
            "invalid_timestamp", "cli.now", "timestamp must include a UTC offset"
        )
    return parsed


class LocalAssetFetcher:
    """Resolve indexed assets beneath one directory by safe name and/or ID."""

    def __init__(self, asset_dir: Path, asset_key: str) -> None:
        try:
            self.root = asset_dir.resolve(strict=True)
        except OSError as exc:
            raise EvidenceValidationError(
                "asset_directory_unavailable",
                "cli.asset_dir",
                f"{asset_dir}: {type(exc).__name__}: {exc}",
            ) from exc
        if not self.root.is_dir():
            raise EvidenceValidationError(
                "asset_directory_unavailable", "cli.asset_dir", f"{asset_dir} is not a directory"
            )
        self.asset_key = asset_key

    def _safe_name_path(self, name: Any) -> Path:
        if not isinstance(name, str) or not name or Path(name).name != name:
            raise EvidenceValidationError(
                "unsafe_asset_name",
                "asset.name",
                "asset name must be one path segment",
            )
        candidate = (self.root / name).resolve(strict=False)
        if candidate.parent != self.root:
            raise EvidenceValidationError(
                "unsafe_asset_name", "asset.name", "asset path escapes the asset directory"
            )
        return candidate

    def __call__(self, record: Mapping[str, Any]) -> bytes:
        name_path = self._safe_name_path(record.get("name"))
        asset_id = record.get("asset_id")
        if isinstance(asset_id, bool) or not isinstance(asset_id, int) or asset_id <= 0:
            raise EvidenceValidationError(
                "invalid_positive_integer", "asset.asset_id", "expected a positive integer"
            )
        id_path = self.root / str(asset_id)
        candidates: list[Path]
        if self.asset_key == "name":
            candidates = [name_path]
        elif self.asset_key == "asset_id":
            candidates = [id_path]
        else:
            candidates = [name_path, id_path]
        existing = [path for path in candidates if path.is_file()]
        if not existing:
            raise EvidenceValidationError(
                "local_asset_missing",
                f"asset[{asset_id}]",
                f"no local file matched name={record.get('name')!r} or asset_id={asset_id}",
            )
        payloads: list[bytes] = []
        for path in existing:
            try:
                payloads.append(path.read_bytes())
            except OSError as exc:
                raise EvidenceValidationError(
                    "file_read_failed",
                    f"asset[{asset_id}]",
                    f"{path}: {type(exc).__name__}: {exc}",
                ) from exc
        if any(payload != payloads[0] for payload in payloads[1:]):
            raise EvidenceValidationError(
                "ambiguous_local_asset",
                f"asset[{asset_id}]",
                "name and asset_id files contain different bytes",
            )
        return payloads[0]


def validate_from_args(args: argparse.Namespace) -> dict[str, Any]:
    expected_identity = _expected_source_identity(args)
    verification_clock = _verification_clock(args)
    index_path = Path(args.asset_index)
    index_document, index_bytes = _load_mapping(index_path, "cli.asset_index")
    fetcher = LocalAssetFetcher(Path(args.asset_dir), args.asset_key)
    verified_index = validate_release_asset_index(
        index_document,
        fetcher,
        expected_source_identity=expected_identity,
        index_bytes=index_bytes,
        now=verification_clock,
    )

    envelope_results: list[dict[str, Any]] = []
    for offset, raw_path in enumerate(args.envelope):
        envelope_path = Path(raw_path)
        envelope, envelope_bytes = _load_mapping(
            envelope_path, f"cli.envelopes[{offset}]"
        )
        result = validate_evidence_envelope(
            envelope,
            verified_index,
            envelope_bytes=envelope_bytes,
            expected_source_identity=expected_identity,
            now=verification_clock,
        )
        envelope_results.append(
            {
                "path": str(envelope_path.resolve()),
                "evidence_id": result.evidence_id,
                "integrity_valid": result.integrity_valid,
                "gate_eligible": result.gate_eligible,
                "accepted": False,
                "claimed_verification_level": result.verification_level,
                "claimed_provider_verified": result.claimed_provider_verified,
                "claimed_counts_as_preview_acceptance": (
                    result.claimed_counts_as_preview_acceptance
                ),
                "provider_verified": result.provider_verified,
                "counts_as_preview_acceptance": result.counts_as_preview_acceptance,
                "source_identity_bound": result.source_identity_bound,
                "raw_export_asset_id": result.raw_export_asset_id,
                "raw_export_sha256": result.raw_export_sha256,
                "evidence_envelope_asset_id": result.evidence_envelope_asset_id,
                "evidence_envelope_sha256": result.evidence_envelope_sha256,
                "verifier_report_asset_id": result.verifier_report_asset_id,
                "verifier_report_sha256": result.verifier_report_sha256,
            }
        )

    preview_count = sum(
        item["claimed_verification_level"] == PREVIEW_ATTESTED for item in envelope_results
    )
    provider_count = sum(
        item["claimed_verification_level"] == PROVIDER_VERIFIED for item in envelope_results
    )
    return {
        "schema_version": RESULT_SCHEMA,
        "integrity_valid": True,
        "gate_eligible": False,
        "accepted": False,
        "identity_binding": (
            "bound_to_expected_source" if expected_identity is not None else "identity_unbound"
        ),
        "asset_index": {
            "path": str(index_path.resolve()),
            "sha256": verified_index.index_sha256,
            "repository": verified_index.repository,
            "release_id": verified_index.release_id,
            "release_tag": verified_index.release_tag,
            "source_identity": dict(verified_index.source_identity),
            "verified_asset_count": len(verified_index.assets),
        },
        "summary": {
            "envelope_count": len(envelope_results),
            "claimed_preview_attested": preview_count,
            "claimed_provider_verified": provider_count,
            "capture_only": 0,
        },
        "envelopes": envelope_results,
    }


def _failure(exc: EvidenceValidationError) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA,
        "integrity_valid": False,
        "gate_eligible": False,
        "accepted": False,
        "error": {"code": exc.code, "path": exc.path, "message": exc.message},
    }


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        output = validate_from_args(args)
    except EvidenceValidationError as exc:
        output = _failure(exc)
        exit_code = 2 if exc.code == "invalid_cli_arguments" else 1
    except Exception as exc:  # Keep the CLI parseable without masking an implementation defect.
        output = {
            "schema_version": RESULT_SCHEMA,
            "integrity_valid": False,
            "gate_eligible": False,
            "accepted": False,
            "error": {
                "code": "internal_error",
                "path": "cli",
                "message": f"{type(exc).__name__}: {exc}",
            },
        }
        exit_code = 3
    else:
        exit_code = 0
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
