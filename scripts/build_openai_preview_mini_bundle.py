#!/usr/bin/env python3
"""Build E and I for one draft-Release R -> E -> V -> I mini-bundle.

The builder never allocates GitHub IDs.  Every Release, workflow-run, and asset
identity must come from a saved JSON response produced by the GitHub API.  The
``envelope`` command runs only after R has been uploaded.  The ``index``
command runs only after an independent verifier has produced V and R/E/V plus
all supporting files have been uploaded.

The builder does not create V and its output is never gate-eligible by itself.
I deliberately does not index itself, avoiding a digest self-reference; the
later live verifier binds I through its separately uploaded GitHub asset.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from normalize_openai_preview_capture import (
    CaptureNormalizationError,
    StagingRoot,
    _identifier,
    _mapping,
    _strict_json,
    _timestamp,
    canonical_json_bytes,
    frozen_source_identity,
    parse_clock,
    require_distinct_paths,
)
from openai_preview_capture_contracts import validate_normalized_capture
from openai_preview_evidence import (
    EVIDENCE_ENVELOPE_SCHEMA,
    PREVIEW_ATTESTED,
    RELEASE_ASSET_INDEX_SCHEMA,
    VERIFIER_REPORT_SCHEMA,
    EvidenceValidationError,
    normalize_sha256,
    sha256_bytes,
    validate_evidence_bundle,
)


REPO = Path(__file__).resolve().parents[1]
PROVIDER_REGISTRY_PATH = REPO / "tests" / "openai_phase8" / "provider-verifier-registry.yaml"
LIVE_VERIFIER_PATH = REPO / "tests" / "openai_phase8" / "verify_preview_evidence.py"
DRAFT_VERIFIER_PATH = REPO / "scripts" / "verify_openai_preview_draft_bundle.py"
VERIFIER_ID = "independent-draft-bundle-verifier-v1"
PLAN_SCHEMA = "openai-preview-mini-bundle-plan/v1"
RESULT_SCHEMA = "openai-preview-mini-bundle-build-result/v1"
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
WORKFLOW_PATH_RE = re.compile(r"^\.github/workflows/[A-Za-z0-9._/-]+\.ya?ml$")
ROLE_KINDS = {
    "R": "task_export",
    "E": "evidence_envelope",
    "V": "verifier_report",
}
SUPPORTING_KINDS = frozenset({"supporting_file", "screenshot"})


class MiniBundleError(ValueError):
    """Stable fail-closed mini-bundle construction error."""

    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


def _fail(code: str, path: str, message: str) -> None:
    raise MiniBundleError(code, path, message)


def _positive_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail("invalid_positive_integer", path, repr(value))
    return value


def _strict_bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        _fail("invalid_boolean", path, repr(value))
    return value


def _read_json(path: Path, label: str) -> tuple[Mapping[str, Any], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        _fail("file_read_failed", label, f"{type(exc).__name__}: {exc}")
    try:
        return _mapping(_strict_json(payload, label), label), payload
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    except ValueError as exc:
        _fail("unsupported_normalized_capture", "raw_export", str(exc))


def _normalized_digest(value: Any, path: str) -> str:
    try:
        return normalize_sha256(value, path)
    except EvidenceValidationError as exc:
        _fail(exc.code, exc.path, exc.message)


def _api_url(value: Any, path: str) -> urllib.parse.SplitResult:
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
    return parsed


def _browser_download_url(value: Any, repository: str, path: str) -> str:
    if not isinstance(value, str):
        _fail("invalid_browser_download_url", path, repr(value))
    try:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
    except ValueError:
        _fail("invalid_browser_download_url", path, value)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or parsed.query
        or parsed.fragment
        or not parsed.path.startswith(f"/{repository}/releases/download/")
    ):
        _fail("invalid_browser_download_url", path, value)
    return value


def _safe_asset_name(value: Any, path: str) -> str:
    name = _identifier(value, path)
    if Path(name).name != name or "/" in name or "\\" in name or name in {".", ".."}:
        _fail("unsafe_asset_name", path, name)
    return name


def _release_snapshot(document: Mapping[str, Any], *, now: datetime) -> dict[str, Any]:
    release_id = _positive_int(document.get("id"), "github_release.id")
    parsed = _api_url(document.get("url"), "github_release.url")
    match = re.fullmatch(r"/repos/([^/]+/[^/]+)/releases/(\d+)", parsed.path)
    if match is None or int(match.group(2)) != release_id:
        _fail("github_release_url_mismatch", "github_release.url", parsed.path)
    repository = match.group(1)
    if REPOSITORY_RE.fullmatch(repository) is None:
        _fail("invalid_repository", "github_release.url", repository)
    release_tag = _identifier(document.get("tag_name"), "github_release.tag_name")
    _strict_bool(document.get("draft"), "github_release.draft")
    if _strict_bool(document.get("prerelease"), "github_release.prerelease") is not True:
        _fail("release_not_prerelease", "github_release.prerelease", repr(document.get("prerelease")))
    _timestamp(document.get("created_at"), "github_release.created_at", now=now)
    assets = document.get("assets")
    if not isinstance(assets, list):
        _fail("release_assets_missing", "github_release.assets", "expected an API asset array")
    return {
        "repository": repository,
        "release_id": release_id,
        "release_tag": release_tag,
        "draft": document["draft"],
        "assets": assets,
    }


def _workflow_snapshot(
    document: Mapping[str, Any],
    *,
    repository: str,
    source_commit: str,
    workflow_contract: Mapping[str, Any],
    now: datetime,
) -> dict[str, Any]:
    run_id = _positive_int(document.get("id"), "github_workflow_run.id")
    workflow_id = _positive_int(document.get("workflow_id"), "github_workflow_run.workflow_id")
    parsed = _api_url(document.get("url"), "github_workflow_run.url")
    expected_path = f"/repos/{repository}/actions/runs/{run_id}"
    if parsed.path != expected_path:
        _fail("github_workflow_url_mismatch", "github_workflow_run.url", parsed.path)
    html_url = document.get("html_url")
    if html_url != f"https://github.com/{repository}/actions/runs/{run_id}":
        _fail("github_workflow_url_mismatch", "github_workflow_run.html_url", repr(html_url))
    repo_record = _mapping(document.get("repository"), "github_workflow_run.repository")
    if repo_record.get("full_name") != repository:
        _fail("github_workflow_repository_mismatch", "github_workflow_run.repository.full_name", repr(repo_record.get("full_name")))
    head_sha = document.get("head_sha")
    if head_sha != source_commit or not isinstance(head_sha, str) or COMMIT_RE.fullmatch(head_sha) is None:
        _fail("github_workflow_source_mismatch", "github_workflow_run.head_sha", repr(head_sha))
    if document.get("status") != "completed" or document.get("conclusion") != "success":
        _fail("github_workflow_not_successful", "github_workflow_run", "completed/success required")
    actor = _mapping(document.get("actor"), "github_workflow_run.actor")
    actor_login = _identifier(actor.get("login"), "github_workflow_run.actor.login")
    event = document.get("event")
    if event != workflow_contract.get("workflow_event"):
        _fail("unsupported_workflow_event", "github_workflow_run.event", repr(event))
    workflow_path = document.get("path")
    if (
        not isinstance(workflow_path, str)
        or WORKFLOW_PATH_RE.fullmatch(workflow_path) is None
        or ".." in Path(workflow_path).parts
        or workflow_path != workflow_contract.get("workflow_path")
    ):
        _fail("invalid_workflow_path", "github_workflow_run.path", repr(workflow_path))
    if document.get("head_branch") != "main":
        _fail("github_workflow_branch_mismatch", "github_workflow_run.head_branch", repr(document.get("head_branch")))
    witnessed_at = _timestamp(document.get("updated_at"), "github_workflow_run.updated_at", now=now)
    _positive_int(document.get("run_attempt"), "github_workflow_run.run_attempt")
    return {
        "workflow_run_id": run_id,
        "workflow_id": workflow_id,
        "workflow_path": workflow_path,
        "workflow_event": event,
        "workflow_witness_role": workflow_contract["workflow_witness_role"],
        "actor": actor_login,
        "source_commit": source_commit,
        "run_head_sha": source_commit,
        "witnessed_at": witnessed_at,
    }


def _asset_snapshot(
    document: Mapping[str, Any],
    *,
    local_payload: bytes,
    local_name: str,
    repository: str,
    release_assets: list[Any],
    now: datetime,
    label: str,
) -> dict[str, Any]:
    asset_id = _positive_int(document.get("id"), f"{label}.id")
    name = _safe_asset_name(document.get("name"), f"{label}.name")
    if name != local_name:
        _fail("asset_local_name_mismatch", f"{label}.name", f"API={name!r} local={local_name!r}")
    size = _positive_int(document.get("size"), f"{label}.size")
    digest = _normalized_digest(document.get("digest"), f"{label}.digest")
    if size != len(local_payload) or digest != sha256_bytes(local_payload):
        _fail("asset_payload_mismatch", label, name)
    if document.get("state") != "uploaded":
        _fail("asset_not_uploaded", f"{label}.state", repr(document.get("state")))
    parsed = _api_url(document.get("url"), f"{label}.url")
    if parsed.path != f"/repos/{repository}/releases/assets/{asset_id}":
        _fail("asset_api_url_mismatch", f"{label}.url", parsed.path)
    browser_download_url = _browser_download_url(
        document.get("browser_download_url"), repository, f"{label}.browser_download_url"
    )
    _timestamp(document.get("updated_at"), f"{label}.updated_at", now=now)
    matches = [item for item in release_assets if isinstance(item, Mapping) and item.get("id") == asset_id]
    if len(matches) != 1:
        _fail("asset_not_in_release_inventory", label, str(asset_id))
    inventory = matches[0]
    for field, expected in (
        ("name", name),
        ("size", size),
        ("digest", digest),
        ("state", "uploaded"),
        ("url", document.get("url")),
        ("browser_download_url", browser_download_url),
    ):
        if inventory.get(field) != expected:
            _fail("release_inventory_asset_mismatch", f"{label}.{field}", str(asset_id))
    return {
        "asset_id": asset_id,
        "name": name,
        "sha256": digest,
        "size": size,
        "browser_download_url": browser_download_url,
    }


def _normalized_code_digest(path: Path) -> str:
    normalized = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(normalized.encode("utf-8"))


def _preview_adapter_contract() -> Mapping[str, Any]:
    try:
        registry = yaml.safe_load(PROVIDER_REGISTRY_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("provider_registry_invalid", "provider_registry", str(exc))
    adapters = registry.get("adapters", []) if isinstance(registry, Mapping) else []
    adapter = next(
        (
            item
            for item in adapters
            if isinstance(item, Mapping)
            and item.get("adapter_id") == "github_release_asset_preview_v1"
            and item.get("enabled") is True
        ),
        None,
    )
    if not isinstance(adapter, Mapping):
        _fail("provider_adapter_unavailable", "provider_registry.adapters", "Preview adapter is not enabled")
    expected = {
        "workflow_witness_role": "source_commit_main_ci",
        "workflow_path": ".github/workflows/openai-plugin-preview.yml",
        "workflow_event": "push",
    }
    for field, value in expected.items():
        if adapter.get(field) != value:
            _fail("provider_adapter_contract_mismatch", f"provider_registry.{field}", repr(adapter.get(field)))
    if adapter.get("verifier_path") != LIVE_VERIFIER_PATH.relative_to(REPO).as_posix() or adapter.get("verifier_digest") != _normalized_code_digest(LIVE_VERIFIER_PATH):
        _fail("provider_adapter_digest_mismatch", "provider_registry.verifier_digest", repr(adapter.get("verifier_digest")))
    return expected


def _verifier_code_digest() -> str:
    return _normalized_code_digest(DRAFT_VERIFIER_PATH)


def _assert_frozen_identity(identity: Mapping[str, Any]) -> dict[str, str]:
    current = frozen_source_identity()
    if dict(identity) != current:
        mismatches = sorted(key for key in current if identity.get(key) != current.get(key))
        _fail("source_identity_mismatch", "source_identity", str(mismatches))
    return current


def build_envelope(
    *,
    staging: StagingRoot,
    raw_export: str,
    release_snapshot: str,
    workflow_run_snapshot: str,
    raw_asset_snapshot: str,
    output: str,
    now: datetime,
) -> tuple[Path, Mapping[str, Any]]:
    raw_path = staging.input_file(raw_export, "cli.raw_export")
    release_path = staging.input_file(release_snapshot, "cli.release_snapshot")
    workflow_path = staging.input_file(workflow_run_snapshot, "cli.workflow_run_snapshot")
    asset_path = staging.input_file(raw_asset_snapshot, "cli.raw_asset_snapshot")
    output_path = staging.output_file(output, "cli.output")
    require_distinct_paths(
        [raw_path, release_path, workflow_path, asset_path, output_path],
        "envelope_inputs_and_output",
    )
    raw_document, raw_bytes = _read_json(raw_path, "raw_export")
    try:
        normalized = validate_normalized_capture(raw_document, now=now, verify_checkout=True)
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    except ValueError as exc:
        _fail("unsupported_normalized_capture", "R", str(exc))
    identity = _assert_frozen_identity(_mapping(normalized["source_identity"], "raw_export.source_identity"))
    release_document, _ = _read_json(release_path, "github_release")
    release = _release_snapshot(release_document, now=now)
    workflow_document, _ = _read_json(workflow_path, "github_workflow_run")
    workflow = _workflow_snapshot(
        workflow_document,
        repository=release["repository"],
        source_commit=identity["source_commit"],
        workflow_contract=_preview_adapter_contract(),
        now=now,
    )
    if datetime.fromisoformat(workflow["witnessed_at"].replace("Z", "+00:00")) > datetime.fromisoformat(normalized["captured_at"].replace("Z", "+00:00")):
        _fail("invalid_timestamp_order", "github_workflow_run.updated_at", "source CI witness follows capture")
    asset_document, _ = _read_json(asset_path, "github_raw_asset")
    raw_asset = _asset_snapshot(
        asset_document,
        local_payload=raw_bytes,
        local_name=raw_path.name,
        repository=release["repository"],
        release_assets=release["assets"],
        now=now,
        label="github_raw_asset",
    )
    adapter = _mapping(normalized["adapter"], "raw_export.capture_adapter")
    if adapter.get("adapter_id") == VERIFIER_ID:
        _fail("verifier_not_independent", "raw_export.capture_adapter", VERIFIER_ID)
    envelope = {
        "schema_version": EVIDENCE_ENVELOPE_SCHEMA,
        "evidence_id": normalized["evidence_id"],
        "verification_level": PREVIEW_ATTESTED,
        "provider_verified": False,
        "counts_as_preview_acceptance": True,
        "source_identity": identity,
        "adapter": adapter,
        "capture": {
            "surface": normalized["capture"]["surface"],
            "task_or_thread_id": normalized["capture"]["task_or_thread_id"],
            "captured_at": normalized["captured_at"],
            "raw_export_asset_id": raw_asset["asset_id"],
            "raw_export_sha256": raw_asset["sha256"],
        },
        "github_witness": {
            "repository": release["repository"],
            "release_id": release["release_id"],
            "release_tag": release["release_tag"],
            **workflow,
            "raw_export_asset_id": raw_asset["asset_id"],
        },
        "expected_verifier": {
            "verifier_id": VERIFIER_ID,
            "verifier_code_sha256": _verifier_code_digest(),
            "independent": True,
        },
    }
    output_path.write_bytes(canonical_json_bytes(envelope))
    return output_path, envelope


def _plan_assets(
    plan: Mapping[str, Any], *, staging: StagingRoot, output_path: Path
) -> list[dict[str, Any]]:
    if plan.get("schema_version") != PLAN_SCHEMA:
        _fail("unsupported_schema", "plan.schema_version", repr(plan.get("schema_version")))
    values = plan.get("assets")
    if not isinstance(values, list):
        _fail("invalid_type", "plan.assets", "expected an array")
    records: list[dict[str, Any]] = []
    roles: list[str] = []
    paths: list[Path] = [output_path]
    logical_keys: set[str] = set()
    for offset, value in enumerate(values):
        label = f"plan.assets[{offset}]"
        record = _mapping(value, label)
        role = record.get("role")
        expected_fields = {"role", "path", "github_asset_snapshot"}
        if role == "supporting":
            expected_fields.add("evidence_kind")
        if set(record) != expected_fields:
            _fail("plan_asset_fields", label, f"expected {sorted(expected_fields)}")
        if role not in {*ROLE_KINDS, "supporting"}:
            _fail("invalid_asset_role", f"{label}.role", repr(role))
        path_value = record.get("path")
        snapshot_value = record.get("github_asset_snapshot")
        if not isinstance(path_value, str) or not isinstance(snapshot_value, str):
            _fail("invalid_path", label, "asset and snapshot paths must be strings")
        key = path_value.casefold()
        snapshot_key = snapshot_value.casefold()
        if key in logical_keys or snapshot_key in logical_keys or key == snapshot_key:
            _fail("path_reused", label, f"{path_value!r} / {snapshot_value!r}")
        logical_keys.update({key, snapshot_key})
        asset_path = staging.input_file(path_value, f"{label}.path")
        snapshot_path = staging.input_file(snapshot_value, f"{label}.github_asset_snapshot")
        if asset_path.parent != output_path.parent:
            _fail("asset_not_colocated_with_index", f"{label}.path", path_value)
        paths.extend((asset_path, snapshot_path))
        kind = ROLE_KINDS.get(str(role))
        if role == "supporting":
            kind = record.get("evidence_kind")
            if kind not in SUPPORTING_KINDS:
                _fail("unsupported_supporting_kind", f"{label}.evidence_kind", repr(kind))
        records.append(
            {
                "role": role,
                "evidence_kind": kind,
                "path": asset_path,
                "snapshot_path": snapshot_path,
            }
        )
        roles.append(str(role))
    for role in ROLE_KINDS:
        if roles.count(role) != 1:
            _fail("required_role_count", "plan.assets", f"{role}={roles.count(role)}")
    require_distinct_paths(paths, "plan_asset_paths")
    return records


def build_index(
    *,
    staging: StagingRoot,
    plan_path_value: str,
    release_snapshot: str,
    workflow_run_snapshot: str,
    output: str,
    now: datetime,
) -> tuple[Path, Mapping[str, Any], Any]:
    plan_path = staging.input_file(plan_path_value, "cli.plan")
    release_path = staging.input_file(release_snapshot, "cli.release_snapshot")
    workflow_path = staging.input_file(workflow_run_snapshot, "cli.workflow_run_snapshot")
    output_path = staging.output_file(output, "cli.output")
    require_distinct_paths([plan_path, release_path, workflow_path, output_path], "index_control_paths")
    plan, _ = _read_json(plan_path, "plan")
    records = _plan_assets(plan, staging=staging, output_path=output_path)
    control_paths = [plan_path, release_path, workflow_path, output_path]
    data_paths = [path for record in records for path in (record["path"], record["snapshot_path"])]
    require_distinct_paths([*control_paths, *data_paths], "index_inputs_and_output")

    raw_record = next(record for record in records if record["role"] == "R")
    raw_document, raw_bytes = _read_json(raw_record["path"], "R")
    try:
        normalized = validate_normalized_capture(raw_document, now=now, verify_checkout=True)
    except CaptureNormalizationError as exc:
        _fail(exc.code, exc.path, exc.message)
    identity = _assert_frozen_identity(_mapping(normalized["source_identity"], "R.source_identity"))
    if normalized["capture"].get("evidence_kind") != "task_export":
        _fail("raw_evidence_kind_mismatch", "R.capture.evidence_kind", repr(normalized["capture"].get("evidence_kind")))

    release_document, _ = _read_json(release_path, "github_release")
    release = _release_snapshot(release_document, now=now)
    workflow_document, _ = _read_json(workflow_path, "github_workflow_run")
    workflow = _workflow_snapshot(
        workflow_document,
        repository=release["repository"],
        source_commit=identity["source_commit"],
        workflow_contract=_preview_adapter_contract(),
        now=now,
    )
    asset_records: list[dict[str, Any]] = []
    payloads: dict[int, bytes] = {}
    role_assets: dict[str, dict[str, Any]] = {}
    seen_ids: set[int] = set()
    seen_names: set[str] = set()
    for offset, record in enumerate(records):
        payload = record["path"].read_bytes()
        snapshot, _ = _read_json(record["snapshot_path"], f"github_assets[{offset}]")
        asset = _asset_snapshot(
            snapshot,
            local_payload=payload,
            local_name=record["path"].name,
            repository=release["repository"],
            release_assets=release["assets"],
            now=now,
            label=f"github_assets[{offset}]",
        )
        name_key = asset["name"].casefold()
        if asset["asset_id"] in seen_ids:
            _fail("asset_id_reused", f"github_assets[{offset}].id", str(asset["asset_id"]))
        if name_key in seen_names:
            _fail("asset_name_reused", f"github_assets[{offset}].name", asset["name"])
        seen_ids.add(asset["asset_id"])
        seen_names.add(name_key)
        indexed = {**asset, "evidence_kind": record["evidence_kind"]}
        asset_records.append(indexed)
        payloads[asset["asset_id"]] = payload
        if record["role"] in ROLE_KINDS:
            role_assets[record["role"]] = indexed

    envelope_record = next(record for record in records if record["role"] == "E")
    envelope, envelope_bytes = _read_json(envelope_record["path"], "E")
    if envelope.get("schema_version") != EVIDENCE_ENVELOPE_SCHEMA:
        _fail("unsupported_schema", "E.schema_version", repr(envelope.get("schema_version")))
    expected_capture = {
        "surface": normalized["capture"]["surface"],
        "task_or_thread_id": normalized["capture"]["task_or_thread_id"],
        "captured_at": normalized["captured_at"],
        "raw_export_asset_id": role_assets["R"]["asset_id"],
        "raw_export_sha256": role_assets["R"]["sha256"],
    }
    if (
        envelope.get("evidence_id") != normalized["evidence_id"]
        or envelope.get("source_identity") != identity
        or envelope.get("adapter") != normalized["adapter"]
        or envelope.get("capture") != expected_capture
    ):
        _fail("envelope_raw_binding_mismatch", "E", normalized["evidence_id"])
    expected_verifier = envelope.get("expected_verifier")
    if expected_verifier != {
        "verifier_id": VERIFIER_ID,
        "verifier_code_sha256": _verifier_code_digest(),
        "independent": True,
    }:
        _fail("expected_verifier_mismatch", "E.expected_verifier", repr(expected_verifier))
    expected_witness = {
        "repository": release["repository"],
        "release_id": release["release_id"],
        "release_tag": release["release_tag"],
        **workflow,
        "raw_export_asset_id": role_assets["R"]["asset_id"],
    }
    if envelope.get("github_witness") != expected_witness:
        _fail("envelope_witness_mismatch", "E.github_witness", normalized["evidence_id"])

    report_record = next(record for record in records if record["role"] == "V")
    report, _ = _read_json(report_record["path"], "V")
    if report.get("schema_version") != VERIFIER_REPORT_SCHEMA:
        _fail("unsupported_schema", "V.schema_version", repr(report.get("schema_version")))

    index = {
        "schema_version": RELEASE_ASSET_INDEX_SCHEMA,
        "source_identity": identity,
        "github_release": {
            "repository": release["repository"],
            "release_id": release["release_id"],
            "release_tag": release["release_tag"],
        },
        "github_witness": workflow,
        "assets": asset_records,
    }
    index_bytes = canonical_json_bytes(index)

    def fetch_asset(record: Mapping[str, Any]) -> bytes:
        asset_id = record.get("asset_id")
        if isinstance(asset_id, bool) or not isinstance(asset_id, int) or asset_id not in payloads:
            _fail("asset_fetch_unindexed", "asset_index.assets", repr(asset_id))
        return payloads[asset_id]

    try:
        integrity = validate_evidence_bundle(
            envelope,
            index,
            fetch_asset,
            envelope_bytes=envelope_bytes,
            expected_source_identity=identity,
            index_bytes=index_bytes,
            now=now,
        )
    except EvidenceValidationError as exc:
        _fail(exc.code, exc.path, exc.message)
    if integrity.gate_eligible or integrity.counts_as_preview_acceptance or integrity.provider_verified:
        _fail("local_builder_overclaim", "I", normalized["evidence_id"])
    if role_assets["E"]["sha256"] != sha256_bytes(envelope_bytes):
        _fail("envelope_asset_digest_mismatch", "E", normalized["evidence_id"])
    if role_assets["V"]["sha256"] != sha256_bytes(report_record["path"].read_bytes()):
        _fail("verifier_asset_digest_mismatch", "V", normalized["evidence_id"])
    output_path.write_bytes(index_bytes)
    return output_path, index, integrity


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        _fail("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="command", required=True, parser_class=JsonArgumentParser
    )
    envelope = subparsers.add_parser("envelope")
    envelope.add_argument("--staging-root", type=Path, required=True)
    envelope.add_argument("--raw-export", required=True)
    envelope.add_argument("--release-snapshot", required=True)
    envelope.add_argument("--workflow-run-snapshot", required=True)
    envelope.add_argument("--raw-asset-snapshot", required=True)
    envelope.add_argument("--output", required=True)
    envelope.add_argument("--now")
    index = subparsers.add_parser("index")
    index.add_argument("--staging-root", type=Path, required=True)
    index.add_argument("--plan", required=True)
    index.add_argument("--release-snapshot", required=True)
    index.add_argument("--workflow-run-snapshot", required=True)
    index.add_argument("--output", required=True)
    index.add_argument("--now")
    return parser


def _failure(exc: MiniBundleError) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA,
        "built": False,
        "gate_eligible": False,
        "accepted": False,
        "error": {"code": exc.code, "path": exc.path, "message": exc.message},
    }


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        staging = StagingRoot(args.staging_root)
        now = parse_clock(args.now)
        if args.command == "envelope":
            output, envelope = build_envelope(
                staging=staging,
                raw_export=args.raw_export,
                release_snapshot=args.release_snapshot,
                workflow_run_snapshot=args.workflow_run_snapshot,
                raw_asset_snapshot=args.raw_asset_snapshot,
                output=args.output,
                now=now,
            )
            result = {
                "schema_version": RESULT_SCHEMA,
                "built": True,
                "node": "E",
                "gate_eligible": False,
                "accepted": False,
                "evidence_id": envelope["evidence_id"],
                "output": str(output),
                "sha256": sha256_bytes(output.read_bytes()),
                "next_required_external_node": "independent_verifier_report_V",
            }
        else:
            output, _index, integrity = build_index(
                staging=staging,
                plan_path_value=args.plan,
                release_snapshot=args.release_snapshot,
                workflow_run_snapshot=args.workflow_run_snapshot,
                output=args.output,
                now=now,
            )
            result = {
                "schema_version": RESULT_SCHEMA,
                "built": True,
                "node": "I",
                "gate_eligible": False,
                "accepted": False,
                "evidence_id": integrity.evidence_id,
                "output": str(output),
                "sha256": sha256_bytes(output.read_bytes()),
                "index_self_referenced": False,
                "next_required_external_step": "upload_I_publish_immutable_and_live_requery",
            }
    except CaptureNormalizationError as exc:
        result = _failure(MiniBundleError(exc.code, exc.path, exc.message))
        return_code = 2 if exc.code == "invalid_cli_arguments" else 1
    except MiniBundleError as exc:
        result = _failure(exc)
        return_code = 2 if exc.code == "invalid_cli_arguments" else 1
    except Exception as exc:
        result = _failure(MiniBundleError("internal_error", "cli", f"{type(exc).__name__}: {exc}"))
        return_code = 3
    else:
        return_code = 0
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
