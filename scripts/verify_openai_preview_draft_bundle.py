#!/usr/bin/env python3
"""Independently verify uploaded R/E draft assets and emit the pre-index V.

This command is intentionally separate from the mini-bundle builder.  It runs
only in the dedicated GitHub Actions workflow, validates GitHub API snapshots
for an uploaded R and E against their actual bytes, reparses the normalized App
Server capture, and emits ``openai-preview-verifier-report/v1``.  It cannot
build I or promote a Preview gate.  The later live verifier re-queries this
workflow run before trusting V.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from normalize_openai_preview_capture import (
    CaptureNormalizationError,
    StagingRoot,
    _identifier,
    _mapping,
    _strict_json,
    _timestamp,
    canonical_json_bytes,
    frozen_source_identity,
    require_distinct_paths,
)
from openai_preview_capture_contracts import validate_normalized_capture
from openai_preview_evidence import (
    EVIDENCE_ENVELOPE_SCHEMA,
    PREVIEW_ATTESTED,
    VERIFIER_REPORT_SCHEMA,
    EvidenceValidationError,
    normalize_sha256,
    sha256_bytes,
)


REPO = Path(__file__).resolve().parents[1]
VERIFIER_ID = "independent-draft-bundle-verifier-v1"
WORKFLOW_PATH = ".github/workflows/openai-preview-draft-bundle-verifier.yml"
SOURCE_CI_PATH = ".github/workflows/openai-plugin-preview.yml"
RESULT_SCHEMA = "openai-preview-draft-bundle-verification-result/v1"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class DraftVerificationError(ValueError):
    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


def _fail(code: str, path: str, message: str) -> None:
    raise DraftVerificationError(code, path, message)


def _positive_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail("invalid_positive_integer", path, repr(value))
    return value


def _read_json(path: Path, label: str) -> tuple[Mapping[str, Any], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        _fail("file_read_failed", label, str(exc))
    try:
        return _mapping(_strict_json(payload, label), label), payload
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    except ValueError as exc:
        _fail("unsupported_normalized_capture", "R", str(exc))


def _normalized_digest(value: Any, path: str) -> str:
    try:
        return normalize_sha256(value, path)
    except EvidenceValidationError as exc:
        _fail(exc.code, exc.path, exc.message)


def _github_api_path(value: Any, path: str) -> str:
    if not isinstance(value, str):
        _fail("invalid_github_api_url", path, repr(value))
    try:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
    except ValueError:
        _fail("invalid_github_api_url", path, value)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "api.github.com"
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or parsed.query
        or parsed.fragment
    ):
        _fail("invalid_github_api_url", path, value)
    return parsed.path


def _release(document: Mapping[str, Any], *, now: datetime) -> dict[str, Any]:
    release_id = _positive_int(document.get("id"), "github_release.id")
    api_path = _github_api_path(document.get("url"), "github_release.url")
    match = re.fullmatch(r"/repos/([^/]+/[^/]+)/releases/(\d+)", api_path)
    if match is None or int(match.group(2)) != release_id:
        _fail("github_release_url_mismatch", "github_release.url", api_path)
    repository = match.group(1)
    if REPOSITORY_RE.fullmatch(repository) is None:
        _fail("invalid_repository", "github_release.url", repository)
    if document.get("draft") is not True or document.get("prerelease") is not True:
        _fail("release_not_draft_prerelease", "github_release", "draft prerelease required before I")
    tag = _identifier(document.get("tag_name"), "github_release.tag_name")
    _timestamp(document.get("created_at"), "github_release.created_at", now=now)
    assets = document.get("assets")
    if not isinstance(assets, list):
        _fail("release_assets_missing", "github_release.assets", "expected array")
    return {"repository": repository, "release_id": release_id, "release_tag": tag, "assets": assets}


def _source_ci(
    document: Mapping[str, Any],
    *,
    repository: str,
    source_commit: str,
    now: datetime,
) -> dict[str, Any]:
    run_id = _positive_int(document.get("id"), "source_ci.id")
    workflow_id = _positive_int(document.get("workflow_id"), "source_ci.workflow_id")
    if _github_api_path(document.get("url"), "source_ci.url") != f"/repos/{repository}/actions/runs/{run_id}":
        _fail("source_ci_url_mismatch", "source_ci.url", str(run_id))
    repo = _mapping(document.get("repository"), "source_ci.repository")
    actor = _mapping(document.get("actor"), "source_ci.actor")
    if repo.get("full_name") != repository:
        _fail("source_ci_repository_mismatch", "source_ci.repository.full_name", repr(repo.get("full_name")))
    if (
        document.get("head_sha") != source_commit
        or document.get("head_branch") != "main"
        or document.get("status") != "completed"
        or document.get("conclusion") != "success"
        or document.get("event") != "push"
        or document.get("path") != SOURCE_CI_PATH
    ):
        _fail("source_ci_contract_mismatch", "source_ci", str(run_id))
    witnessed_at = _timestamp(document.get("updated_at"), "source_ci.updated_at", now=now)
    return {
        "workflow_run_id": run_id,
        "workflow_id": workflow_id,
        "workflow_path": SOURCE_CI_PATH,
        "workflow_event": "push",
        "workflow_witness_role": "source_commit_main_ci",
        "actor": _identifier(actor.get("login"), "source_ci.actor.login"),
        "source_commit": source_commit,
        "run_head_sha": source_commit,
        "witnessed_at": witnessed_at,
    }


def _asset(
    document: Mapping[str, Any],
    *,
    payload: bytes,
    local_name: str,
    repository: str,
    release_assets: list[Any],
    now: datetime,
    label: str,
) -> dict[str, Any]:
    asset_id = _positive_int(document.get("id"), f"{label}.id")
    name = document.get("name")
    if not isinstance(name, str) or Path(name).name != name or name != local_name:
        _fail("asset_name_mismatch", f"{label}.name", repr(name))
    size = _positive_int(document.get("size"), f"{label}.size")
    digest = _normalized_digest(document.get("digest"), f"{label}.digest")
    if size != len(payload) or digest != sha256_bytes(payload) or document.get("state") != "uploaded":
        _fail("asset_payload_mismatch", label, name)
    if _github_api_path(document.get("url"), f"{label}.url") != f"/repos/{repository}/releases/assets/{asset_id}":
        _fail("asset_url_mismatch", f"{label}.url", str(asset_id))
    browser = document.get("browser_download_url")
    try:
        parsed = urllib.parse.urlsplit(str(browser))
    except ValueError:
        _fail("asset_browser_url_mismatch", f"{label}.browser_download_url", repr(browser))
    if parsed.scheme != "https" or parsed.hostname != "github.com" or not parsed.path.startswith(f"/{repository}/releases/download/") or parsed.query or parsed.fragment:
        _fail("asset_browser_url_mismatch", f"{label}.browser_download_url", repr(browser))
    _timestamp(document.get("updated_at"), f"{label}.updated_at", now=now)
    matches = [item for item in release_assets if isinstance(item, Mapping) and item.get("id") == asset_id]
    if len(matches) != 1:
        _fail("asset_not_in_release_inventory", label, str(asset_id))
    inventory = matches[0]
    for field in ("name", "size", "digest", "state", "url", "browser_download_url"):
        if inventory.get(field) != document.get(field):
            _fail("release_inventory_asset_mismatch", f"{label}.{field}", str(asset_id))
    return {"asset_id": asset_id, "name": name, "sha256": digest, "size": size}


def _code_digest() -> str:
    normalized = Path(__file__).read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(normalized.encode("utf-8"))


def _execution_context(repository: str, source_commit: str, source_ci_run_id: int) -> dict[str, Any]:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        _fail("github_actions_required", "execution", "dedicated GitHub Actions run required")
    run_id_text = os.environ.get("GITHUB_RUN_ID", "")
    attempt_text = os.environ.get("GITHUB_RUN_ATTEMPT", "")
    if not run_id_text.isdigit() or int(run_id_text) <= 0 or int(run_id_text) == source_ci_run_id:
        _fail("independent_run_identity", "execution.GITHUB_RUN_ID", run_id_text)
    if not attempt_text.isdigit() or int(attempt_text) <= 0:
        _fail("independent_run_identity", "execution.GITHUB_RUN_ATTEMPT", attempt_text)
    expected_ref = f"{repository}/{WORKFLOW_PATH}@refs/heads/main"
    if (
        os.environ.get("GITHUB_REPOSITORY") != repository
        or os.environ.get("GITHUB_SHA") != source_commit
        or os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch"
        or os.environ.get("GITHUB_REF_NAME") != "main"
        or os.environ.get("GITHUB_WORKFLOW_REF") != expected_ref
    ):
        _fail("independent_run_context_mismatch", "execution", "repository/ref/workflow/source mismatch")
    return {
        "repository": repository,
        "workflow_run_id": int(run_id_text),
        "workflow_path": WORKFLOW_PATH,
        "workflow_event": "workflow_dispatch",
        "run_head_sha": source_commit,
        "run_attempt": int(attempt_text),
        "actor": _identifier(os.environ.get("GITHUB_ACTOR"), "execution.GITHUB_ACTOR"),
    }


def verify_draft(
    *,
    staging: StagingRoot,
    raw_export: str,
    envelope_path_value: str,
    release_snapshot: str,
    source_ci_run_snapshot: str,
    raw_asset_snapshot: str,
    envelope_asset_snapshot: str,
    output: str,
    now: datetime,
) -> tuple[Path, Mapping[str, Any]]:
    paths = {
        "R": staging.input_file(raw_export, "cli.raw_export"),
        "E": staging.input_file(envelope_path_value, "cli.envelope"),
        "release": staging.input_file(release_snapshot, "cli.release_snapshot"),
        "source_ci": staging.input_file(source_ci_run_snapshot, "cli.source_ci_run_snapshot"),
        "R_asset": staging.input_file(raw_asset_snapshot, "cli.raw_asset_snapshot"),
        "E_asset": staging.input_file(envelope_asset_snapshot, "cli.envelope_asset_snapshot"),
    }
    output_path = staging.output_file(output, "cli.output")
    require_distinct_paths([*paths.values(), output_path], "draft_verifier_inputs_and_output")
    raw_document, raw_bytes = _read_json(paths["R"], "R")
    try:
        normalized = validate_normalized_capture(raw_document, now=now, verify_checkout=True)
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    identity = _mapping(normalized.get("source_identity"), "R.source_identity")
    if dict(identity) != frozen_source_identity():
        _fail("source_identity_mismatch", "R.source_identity", normalized["evidence_id"])
    envelope, envelope_bytes = _read_json(paths["E"], "E")
    release_document, _ = _read_json(paths["release"], "github_release")
    release = _release(release_document, now=now)
    source_ci_document, _ = _read_json(paths["source_ci"], "source_ci")
    source_ci = _source_ci(
        source_ci_document,
        repository=release["repository"],
        source_commit=str(identity["source_commit"]),
        now=now,
    )
    if datetime.fromisoformat(source_ci["witnessed_at"].replace("Z", "+00:00")) > datetime.fromisoformat(normalized["captured_at"].replace("Z", "+00:00")):
        _fail("invalid_timestamp_order", "source_ci.updated_at", "source CI follows capture")
    raw_asset_document, _ = _read_json(paths["R_asset"], "github_raw_asset")
    raw_asset = _asset(
        raw_asset_document,
        payload=raw_bytes,
        local_name=paths["R"].name,
        repository=release["repository"],
        release_assets=release["assets"],
        now=now,
        label="github_raw_asset",
    )
    envelope_asset_document, _ = _read_json(paths["E_asset"], "github_envelope_asset")
    envelope_asset = _asset(
        envelope_asset_document,
        payload=envelope_bytes,
        local_name=paths["E"].name,
        repository=release["repository"],
        release_assets=release["assets"],
        now=now,
        label="github_envelope_asset",
    )
    expected_capture = {
        "surface": normalized["capture"]["surface"],
        "task_or_thread_id": normalized["capture"]["task_or_thread_id"],
        "captured_at": normalized["captured_at"],
        "raw_export_asset_id": raw_asset["asset_id"],
        "raw_export_sha256": raw_asset["sha256"],
    }
    expected_witness = {
        "repository": release["repository"],
        "release_id": release["release_id"],
        "release_tag": release["release_tag"],
        **source_ci,
        "raw_export_asset_id": raw_asset["asset_id"],
    }
    expected_verifier = {
        "verifier_id": VERIFIER_ID,
        "verifier_code_sha256": _code_digest(),
        "independent": True,
    }
    if (
        envelope.get("schema_version") != EVIDENCE_ENVELOPE_SCHEMA
        or envelope.get("evidence_id") != normalized["evidence_id"]
        or envelope.get("verification_level") != PREVIEW_ATTESTED
        or envelope.get("provider_verified") is not False
        or envelope.get("counts_as_preview_acceptance") is not True
        or envelope.get("source_identity") != identity
        or envelope.get("adapter") != normalized["adapter"]
        or envelope.get("capture") != expected_capture
        or envelope.get("github_witness") != expected_witness
        or envelope.get("expected_verifier") != expected_verifier
        or "verifier" in envelope
    ):
        _fail("envelope_binding_mismatch", "E", normalized["evidence_id"])
    execution = _execution_context(
        release["repository"], str(identity["source_commit"]), source_ci["workflow_run_id"]
    )
    report = {
        "schema_version": VERIFIER_REPORT_SCHEMA,
        "evidence_id": normalized["evidence_id"],
        "verifier_id": VERIFIER_ID,
        "verifier_code_sha256": _code_digest(),
        "independent": True,
        "verified_at": now.isoformat().replace("+00:00", "Z"),
        "verdict": "accepted",
        "source_identity": dict(identity),
        "envelope_asset_id": envelope_asset["asset_id"],
        "envelope_sha256": envelope_asset["sha256"],
        "raw_export_asset_id": raw_asset["asset_id"],
        "raw_export_sha256": raw_asset["sha256"],
        "execution": execution,
    }
    output_path.write_bytes(canonical_json_bytes(report))
    return output_path, report


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        _fail("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("--staging-root", type=Path, required=True)
    parser.add_argument("--raw-export", required=True)
    parser.add_argument("--envelope", required=True)
    parser.add_argument("--release-snapshot", required=True)
    parser.add_argument("--source-ci-run-snapshot", required=True)
    parser.add_argument("--raw-asset-snapshot", required=True)
    parser.add_argument("--envelope-asset-snapshot", required=True)
    parser.add_argument("--output", required=True)
    return parser


def _failure(exc: DraftVerificationError) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA,
        "verified": False,
        "gate_eligible": False,
        "accepted": False,
        "error": {"code": exc.code, "path": exc.path, "message": exc.message},
    }


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        output, report = verify_draft(
            staging=StagingRoot(args.staging_root),
            raw_export=args.raw_export,
            envelope_path_value=args.envelope,
            release_snapshot=args.release_snapshot,
            source_ci_run_snapshot=args.source_ci_run_snapshot,
            raw_asset_snapshot=args.raw_asset_snapshot,
            envelope_asset_snapshot=args.envelope_asset_snapshot,
            output=args.output,
            now=datetime.now(timezone.utc),
        )
        result = {
            "schema_version": RESULT_SCHEMA,
            "verified": True,
            "gate_eligible": False,
            "accepted": False,
            "evidence_id": report["evidence_id"],
            "output": str(output),
            "sha256": sha256_bytes(output.read_bytes()),
            "next_required_external_step": "upload_V_then_build_I",
        }
    except CaptureNormalizationError as exc:
        result = _failure(DraftVerificationError(exc.code, exc.path, exc.message))
        return_code = 2 if exc.code == "invalid_cli_arguments" else 1
    except DraftVerificationError as exc:
        result = _failure(exc)
        return_code = 2 if exc.code == "invalid_cli_arguments" else 1
    except Exception as exc:
        result = _failure(DraftVerificationError("internal_error", "cli", f"{type(exc).__name__}: {exc}"))
        return_code = 3
    else:
        return_code = 0
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
