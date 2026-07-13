#!/usr/bin/env python3
"""Validate externally attested Phase 7 runtime evidence.

This runner is intentionally a real-evidence path only.  It has no synthetic
or offline promotion switch.  Every receipt is represented by a separate
Release mini-bundle.  The runner snapshots every indexed asset into memory,
checks the complete R->E->V->I integrity graph, asks the registered live
verifier to issue an in-process attestation, and only then materializes the
attested workspace into a fresh temporary directory for the Phase 7 semantic
validator.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping, Sequence

import yaml

from openai_preview_evidence import (
    PREVIEW_ATTESTED,
    EvidenceValidationError,
    EvidenceValidationResult,
    normalize_sha256,
    sha256_bytes,
    validate_evidence_bundle,
)
from generate_openai_release_ledger import (
    normalized_file_digest,
    normalized_skill_tree_digest,
)


REPO = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO / "research-skills-openai" / "workflow-registry.yaml"
RUNTIME_SCHEMA_PATH = REPO / "tests" / "openai_phase7" / "runtime-receipts.schema.yaml"
PHASE8_VERIFIER_PATH = REPO / "tests" / "openai_phase8" / "verify_preview_evidence.py"
PREVIEW_ADAPTER_ID = "github_release_asset_preview_v1"
WORKSPACE_MANIFEST_SCHEMA = "openai-phase7-workspace-manifest/v1"
RESULT_SCHEMA = "openai-phase7-external-runtime-validation/v1"
EXPECTED_RECEIPT_COUNT = 10
IDENTITY_FIELDS = {
    "plugin_version",
    "source_commit",
    "manifest_sha256",
    "registry_sha256",
    "skill_tree_sha256",
}
WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{number}" for number in range(1, 10)}
    | {f"LPT{number}" for number in range(1, 10)}
)


class RuntimeEvidenceError(ValueError):
    """Stable fail-closed error emitted by the external-evidence runner."""

    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


@dataclass(frozen=True)
class SourceSnapshot:
    path: Path
    payload: bytes
    digest: str


@dataclass(frozen=True)
class AssetSnapshot:
    asset_id: int
    name: str
    evidence_kind: str
    digest: str
    size: int
    payload: bytes
    source_path: Path


@dataclass(frozen=True)
class WorkspaceFile:
    logical_path: str
    asset_id: int
    digest: str
    size: int
    payload: bytes


@dataclass(frozen=True)
class BundleSnapshot:
    bundle_id: str
    receipt_id: str
    index_path: Path
    index_document: Mapping[str, Any]
    index_bytes: bytes
    assets: Mapping[int, AssetSnapshot]
    envelope: Mapping[str, Any]
    envelope_bytes: bytes
    workspace_files: tuple[WorkspaceFile, ...]
    integrity_result: EvidenceValidationResult


@dataclass(frozen=True)
class ExternalRuntimeEvidenceRun:
    """Live result plus the opaque same-process report handoff."""

    summary: Mapping[str, Any]
    report_session: Any

    def __reduce__(self) -> Any:
        raise TypeError("external runtime evidence runs are not serializable")

    def __deepcopy__(self, _memo: dict[int, Any]) -> Any:
        raise TypeError("external runtime evidence runs are not copyable")


AttestationIssuer = Callable[..., Any]
RuntimeValidator = Callable[..., list[dict[str, Any]]]
RequestBuilder = Callable[..., Mapping[str, Any]]
RuntimeReportSessionIssuer = Callable[..., Any]


def _fail(code: str, path: str, message: str) -> None:
    raise RuntimeEvidenceError(code, path, message)


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("invalid_document", path, "expected an object")
    return value


def _sequence(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _fail("invalid_document", path, "expected an array")
    return value


def _read_bytes(path: Path, label: str) -> bytes:
    if path.is_symlink():
        _fail("symlink_rejected", label, str(path))
    try:
        if not path.is_file():
            _fail("file_missing", label, str(path))
        return path.read_bytes()
    except OSError as exc:
        _fail("file_read_failed", label, f"{type(exc).__name__}: {exc}")


def _parse_mapping(payload: bytes, path: str) -> Mapping[str, Any]:
    try:
        value = yaml.safe_load(payload)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("invalid_document", path, str(exc))
    return _mapping(value, path)


def _snapshot(path: Path, label: str) -> SourceSnapshot:
    payload = _read_bytes(path, label)
    return SourceSnapshot(path=path, payload=payload, digest=sha256_bytes(payload))


def _resolve_input(path: Path, label: str) -> Path:
    if path.is_symlink():
        _fail("symlink_rejected", label, str(path))
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        _fail("file_missing", label, f"{type(exc).__name__}: {exc}")


def _inside(root: Path, candidate: Path, label: str, *, must_exist: bool = True) -> Path:
    try:
        resolved = candidate.resolve(strict=must_exist)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        _fail("path_escape", label, str(candidate))
    return resolved


def _canonical_logical_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        _fail("logical_path_not_canonical", label, repr(value))
    logical = PurePosixPath(value)
    if (
        logical.is_absolute()
        or not logical.parts
        or any(part in {"", ".", ".."} for part in logical.parts)
        or logical.as_posix() != value
    ):
        _fail("logical_path_not_canonical", label, value)
    for part in logical.parts:
        stem = part.split(".", 1)[0].upper()
        if (
            part.endswith((" ", "."))
            or any(character in part for character in '<>"|?*')
            or stem in WINDOWS_RESERVED_NAMES
        ):
            _fail("logical_path_not_portable", label, value)
    return value


def _normalized_identity(document: Mapping[str, Any]) -> dict[str, Any]:
    candidate = document.get("source_identity", document)
    identity = _mapping(candidate, "expected_source_identity")
    if set(identity) != IDENTITY_FIELDS:
        _fail(
            "expected_identity_fields",
            "expected_source_identity",
            f"expected exactly {sorted(IDENTITY_FIELDS)}",
        )
    source_commit = identity.get("source_commit")
    if not isinstance(source_commit, str) or re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        _fail("expected_identity_invalid", "expected_source_identity.source_commit", str(source_commit))
    normalized = dict(identity)
    for field in IDENTITY_FIELDS - {"plugin_version", "source_commit"}:
        try:
            normalized[field] = normalize_sha256(identity[field], f"expected_source_identity.{field}")
        except EvidenceValidationError as exc:
            _fail(exc.code, exc.path, exc.message)
    if not isinstance(normalized.get("plugin_version"), str) or not normalized["plugin_version"]:
        _fail("expected_identity_invalid", "expected_source_identity.plugin_version", "missing version")
    return normalized


def current_checkout_source_identity() -> dict[str, str]:
    """Derive the only source identity a standalone run may accept."""

    try:
        process = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        _fail("checkout_head_unavailable", "local_checkout", f"{type(exc).__name__}: {exc}")
    head = process.stdout.strip().lower()
    if re.fullmatch(r"[0-9a-f]{40}", head) is None:
        _fail("checkout_head_invalid", "local_checkout", repr(head))
    manifest_path = REPO / "research-skills-openai" / ".codex-plugin" / "plugin.json"
    registry_path = REPO / "research-skills-openai" / "workflow-registry.yaml"
    skills_root = REPO / "research-skills-openai" / "skills"
    manifest = _parse_mapping(_read_bytes(manifest_path, "plugin_manifest"), "plugin_manifest")
    registry = _parse_mapping(_read_bytes(registry_path, "workflow_registry"), "workflow_registry")
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        _fail("plugin_version_unavailable", "plugin_manifest.version", repr(version))
    if registry.get("plugin_version") != version:
        _fail(
            "plugin_version_mismatch",
            "workflow_registry.plugin_version",
            f"manifest={version!r} registry={registry.get('plugin_version')!r}",
        )
    _, skill_digest = normalized_skill_tree_digest(skills_root)
    return {
        "plugin_version": version,
        "source_commit": head,
        "manifest_sha256": f"sha256:{normalized_file_digest(manifest_path)}",
        "registry_sha256": f"sha256:{normalized_file_digest(registry_path)}",
        "skill_tree_sha256": f"sha256:{skill_digest}",
    }


def _assert_current_checkout_identity(expected_identity: Mapping[str, Any]) -> dict[str, str]:
    actual = current_checkout_source_identity()
    if dict(expected_identity) != actual:
        mismatches = sorted(
            field
            for field in IDENTITY_FIELDS
            if expected_identity.get(field) != actual.get(field)
        )
        _fail(
            "local_source_identity_mismatch",
            "expected_source_identity",
            f"does not match current checkout fields: {mismatches}",
        )
    return actual


def _safe_pattern(pattern: str) -> str:
    if (
        not isinstance(pattern, str)
        or not pattern
        or "\\" in pattern
        or "\x00" in pattern
        or Path(pattern).is_absolute()
        or any(part == ".." for part in PurePosixPath(pattern).parts)
    ):
        _fail("unsafe_asset_index_pattern", "asset_index_pattern", repr(pattern))
    return pattern


def _discover_indexes(root: Path, pattern: str) -> list[Path]:
    safe_pattern = _safe_pattern(pattern)
    try:
        candidates = list(root.glob(safe_pattern))
    except (OSError, ValueError) as exc:
        _fail("invalid_asset_index_pattern", "asset_index_pattern", str(exc))
    indexes: list[Path] = []
    seen: set[Path] = set()
    for offset, candidate in enumerate(candidates):
        resolved = _inside(root, candidate, f"asset_indexes[{offset}]")
        if resolved.suffix.lower() != ".json":
            _fail("asset_index_not_json", f"asset_indexes[{offset}]", str(candidate))
        if candidate.is_symlink():
            _fail("symlink_rejected", f"asset_indexes[{offset}]", str(candidate))
        if resolved in seen:
            _fail("duplicate_bundle", f"asset_indexes[{offset}]", str(resolved))
        seen.add(resolved)
        indexes.append(resolved)
    indexes.sort(key=lambda item: item.as_posix().casefold())
    if len(indexes) != EXPECTED_RECEIPT_COUNT:
        _fail(
            "runtime_bundle_count",
            "asset_indexes",
            f"expected {EXPECTED_RECEIPT_COUNT}, found {len(indexes)}",
        )
    return indexes


def _load_asset_snapshots(
    *, root: Path, index_path: Path, index_document: Mapping[str, Any]
) -> dict[int, AssetSnapshot]:
    records = _sequence(index_document.get("assets"), f"{index_path}.assets")
    assets: dict[int, AssetSnapshot] = {}
    for offset, value in enumerate(records):
        record = _mapping(value, f"{index_path}.assets[{offset}]")
        asset_id = record.get("asset_id")
        name = record.get("name")
        if isinstance(asset_id, bool) or not isinstance(asset_id, int) or asset_id <= 0:
            _fail("invalid_asset_id", f"{index_path}.assets[{offset}]", str(asset_id))
        if not isinstance(name, str) or not name or Path(name).name != name or name in {".", ".."}:
            _fail("unsafe_asset_name", f"{index_path}.assets[{offset}]", repr(name))
        unresolved_source = index_path.parent / name
        if unresolved_source.is_symlink():
            _fail("symlink_rejected", f"asset[{asset_id}]", name)
        source = _inside(root, unresolved_source, f"asset[{asset_id}]")
        if source.parent != index_path.parent:
            _fail("asset_path_escape", f"asset[{asset_id}]", name)
        payload = _read_bytes(source, f"asset[{asset_id}]")
        digest = sha256_bytes(payload)
        expected_digest = record.get("sha256")
        expected_size = record.get("size")
        if digest != expected_digest or len(payload) != expected_size:
            _fail("asset_digest_or_size_mismatch", f"asset[{asset_id}]", name)
        if asset_id in assets:
            _fail("duplicate_asset_id", f"asset[{asset_id}]", str(asset_id))
        assets[asset_id] = AssetSnapshot(
            asset_id=asset_id,
            name=name,
            evidence_kind=str(record.get("evidence_kind", "")),
            digest=digest,
            size=len(payload),
            payload=payload,
            source_path=source,
        )
    return assets


def _manifest_asset(
    assets: Mapping[int, AssetSnapshot], *, label: str
) -> tuple[AssetSnapshot, Mapping[str, Any]]:
    candidates: list[tuple[AssetSnapshot, Mapping[str, Any]]] = []
    for asset in assets.values():
        if asset.evidence_kind != "supporting_file":
            continue
        try:
            document = yaml.safe_load(asset.payload)
        except (UnicodeDecodeError, yaml.YAMLError):
            continue
        if isinstance(document, Mapping) and document.get("schema_version") == WORKSPACE_MANIFEST_SCHEMA:
            candidates.append((asset, document))
    if len(candidates) != 1:
        _fail("workspace_manifest_count", label, f"expected 1, found {len(candidates)}")
    return candidates[0]


def _manifest_binding(
    value: Any,
    *,
    assets: Mapping[int, AssetSnapshot],
    label: str,
) -> tuple[str, AssetSnapshot]:
    binding = _mapping(value, label)
    if set(binding) != {"logical_path", "asset_id", "sha256", "size"}:
        _fail("workspace_binding_fields", label, "unexpected or missing fields")
    logical_path = _canonical_logical_path(binding.get("logical_path"), f"{label}.logical_path")
    asset_id = binding.get("asset_id")
    if isinstance(asset_id, bool) or not isinstance(asset_id, int):
        _fail("workspace_asset_id", f"{label}.asset_id", str(asset_id))
    asset = assets.get(asset_id)
    if asset is None:
        _fail("workspace_asset_unindexed", f"{label}.asset_id", str(asset_id))
    if binding.get("sha256") != asset.digest or binding.get("size") != asset.size:
        _fail("workspace_asset_binding_mismatch", label, logical_path)
    return logical_path, asset


def _required_workspace_paths(
    receipt: Mapping[str, Any], artifact_index_payload: bytes
) -> set[str]:
    receipt_id = str(receipt.get("receipt_id"))
    binding = _mapping(receipt.get("binding"), f"receipts.{receipt_id}.binding")
    required: set[str] = set()
    for field in ("task_export", "actor_manifest", "artifact_index"):
        item = _mapping(binding.get(field), f"receipts.{receipt_id}.binding.{field}")
        required.add(_canonical_logical_path(item.get("path"), f"receipts.{receipt_id}.binding.{field}.path"))
    access = _mapping(receipt.get("file_access"), f"receipts.{receipt_id}.file_access")
    for group in ("reads", "writes"):
        for offset, item in enumerate(_sequence(access.get(group), f"receipts.{receipt_id}.file_access.{group}")):
            record = _mapping(item, f"receipts.{receipt_id}.file_access.{group}[{offset}]")
            required.add(_canonical_logical_path(record.get("path"), f"receipts.{receipt_id}.file_access.{group}[{offset}].path"))
    artifact_index = _parse_mapping(artifact_index_payload, f"receipts.{receipt_id}.artifact_index")
    for offset, item in enumerate(_sequence(artifact_index.get("artifacts"), f"receipts.{receipt_id}.artifact_index.artifacts")):
        artifact = _mapping(item, f"receipts.{receipt_id}.artifact_index.artifacts[{offset}]")
        required.add(_canonical_logical_path(artifact.get("path"), f"receipts.{receipt_id}.artifact_index.artifacts[{offset}].path"))
    return required


def _workspace_files(
    *,
    manifest: Mapping[str, Any],
    manifest_asset_id: int,
    assets: Mapping[int, AssetSnapshot],
    receipt: Mapping[str, Any],
    runtime_receipts_bytes: bytes,
    expected_identity: Mapping[str, Any],
    label: str,
) -> tuple[str, str, str, tuple[WorkspaceFile, ...]]:
    allowed_fields = {
        "schema_version",
        "bundle_id",
        "receipt_id",
        "source_identity",
        "runtime_receipts",
        "files",
    }
    if set(manifest) != allowed_fields:
        _fail("workspace_manifest_fields", label, "unexpected or missing fields")
    bundle_id = manifest.get("bundle_id")
    receipt_id = manifest.get("receipt_id")
    if not isinstance(bundle_id, str) or not bundle_id.strip():
        _fail("workspace_bundle_id", f"{label}.bundle_id", repr(bundle_id))
    if receipt_id != receipt.get("receipt_id"):
        _fail("workspace_receipt_mismatch", f"{label}.receipt_id", str(receipt_id))
    if dict(_mapping(manifest.get("source_identity"), f"{label}.source_identity")) != dict(expected_identity):
        _fail("workspace_source_identity_mismatch", f"{label}.source_identity", str(receipt_id))

    collection_logical_path, collection_asset = _manifest_binding(
        manifest.get("runtime_receipts"), assets=assets, label=f"{label}.runtime_receipts"
    )
    if collection_asset.evidence_kind != "supporting_file" or collection_asset.payload != runtime_receipts_bytes:
        _fail("runtime_collection_not_bound", f"{label}.runtime_receipts", str(receipt_id))

    files: list[WorkspaceFile] = []
    seen_paths: set[str] = {collection_logical_path.casefold()}
    seen_ids: set[int] = {manifest_asset_id, collection_asset.asset_id}
    for offset, value in enumerate(_sequence(manifest.get("files"), f"{label}.files")):
        logical_path, asset = _manifest_binding(
            value, assets=assets, label=f"{label}.files[{offset}]"
        )
        path_key = logical_path.casefold()
        if path_key in seen_paths:
            _fail("workspace_path_reused", f"{label}.files[{offset}]", logical_path)
        if asset.asset_id in seen_ids:
            _fail("workspace_asset_reused", f"{label}.files[{offset}]", str(asset.asset_id))
        if asset.evidence_kind in {"evidence_envelope", "verifier_report", "provider_receipt"}:
            _fail("workspace_nonmaterializable_asset", f"{label}.files[{offset}]", asset.evidence_kind)
        seen_paths.add(path_key)
        seen_ids.add(asset.asset_id)
        files.append(
            WorkspaceFile(
                logical_path=logical_path,
                asset_id=asset.asset_id,
                digest=asset.digest,
                size=asset.size,
                payload=asset.payload,
            )
        )

    binding = _mapping(receipt.get("binding"), f"receipts.{receipt_id}.binding")
    artifact_binding = _mapping(binding.get("artifact_index"), f"receipts.{receipt_id}.binding.artifact_index")
    artifact_path = _canonical_logical_path(
        artifact_binding.get("path"), f"receipts.{receipt_id}.binding.artifact_index.path"
    )
    artifact_file = next((item for item in files if item.logical_path == artifact_path), None)
    if artifact_file is None:
        _fail("workspace_artifact_index_missing", label, artifact_path)
    required = _required_workspace_paths(receipt, artifact_file.payload)
    actual = {item.logical_path for item in files}
    if actual != required:
        _fail(
            "workspace_path_coverage",
            label,
            f"missing={sorted(required - actual)} extra={sorted(actual - required)}",
        )

    task_binding = _mapping(binding.get("task_export"), f"receipts.{receipt_id}.binding.task_export")
    task_path = _canonical_logical_path(task_binding.get("path"), f"receipts.{receipt_id}.binding.task_export.path")
    task_file = next(item for item in files if item.logical_path == task_path)
    task_asset = assets[task_file.asset_id]
    if task_asset.evidence_kind != "task_export" or task_binding.get("sha256") != task_file.digest:
        _fail("workspace_task_export_binding", label, task_path)
    reserved_ids = {
        asset.asset_id
        for asset in assets.values()
        if asset.evidence_kind in {"evidence_envelope", "verifier_report"}
    }
    consumed_ids = reserved_ids | seen_ids
    if consumed_ids != set(assets):
        _fail(
            "indexed_asset_not_consumed",
            label,
            f"unreferenced asset ids: {sorted(set(assets) - consumed_ids)}",
        )
    return bundle_id, str(receipt_id), collection_logical_path, tuple(files)


def _is_link_or_junction(path: Path) -> bool:
    try:
        is_junction = getattr(path, "is_junction", None)
        return path.is_symlink() or (
            callable(is_junction) and bool(is_junction())
        )
    except OSError as exc:
        _fail("inventory_entry_unreadable", "inventory", f"{path}: {exc}")


def _tree_inventory(
    root: Path, label: str
) -> dict[str, tuple[str, str | None]]:
    """Snapshot every file and directory while rejecting link-like entries."""

    inventory: dict[str, tuple[str, str | None]] = {}
    casefolded: set[str] = set()
    try:
        paths = sorted(root.rglob("*"), key=lambda item: item.as_posix())
    except OSError as exc:
        _fail("inventory_unreadable", label, f"{type(exc).__name__}: {exc}")
    for path in paths:
        relative = path.relative_to(root).as_posix()
        key = relative.casefold()
        if key in casefolded:
            _fail("inventory_case_collision", label, relative)
        casefolded.add(key)
        if _is_link_or_junction(path):
            _fail("symlink_rejected", label, relative)
        if path.is_file():
            payload = _read_bytes(path, f"{label}.{relative}")
            inventory[relative] = ("file", sha256_bytes(payload))
        elif path.is_dir():
            inventory[relative] = ("directory", None)
        else:
            _fail("inventory_entry_type", label, relative)
    return inventory


def _allowed_tree_entries(root: Path, files: set[Path]) -> set[str]:
    allowed: set[str] = set()
    for path in files:
        relative = path.relative_to(root).as_posix()
        allowed.add(relative)
        parent = PurePosixPath(relative).parent
        while parent.parts and parent.as_posix() != ".":
            allowed.add(parent.as_posix())
            parent = parent.parent
    return allowed


def _assert_inventory_unchanged(
    root: Path,
    expected: Mapping[str, tuple[str, str | None]],
    stage: str,
) -> None:
    current = _tree_inventory(root, f"evidence_root.{stage}")
    if current != dict(expected):
        _fail(
            "source_inventory_changed_during_validation",
            f"evidence_root.{stage}",
            "evidence bytes, paths, or entry types changed",
        )


def _assert_snapshots_unchanged(snapshots: Mapping[Path, SourceSnapshot], stage: str) -> None:
    for source in snapshots.values():
        current = _read_bytes(source.path, f"toctou.{stage}")
        if sha256_bytes(current) != source.digest or current != source.payload:
            _fail("source_changed_during_validation", f"toctou.{stage}", str(source.path))


def _load_phase8_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_openai_phase8_preview_runtime_verifier", PHASE8_VERIFIER_PATH
    )
    if spec is None or spec.loader is None:
        _fail("phase8_verifier_unavailable", "phase8_verifier", str(PHASE8_VERIFIER_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RealPreviewVerifier:
    """One-argument, real-only adapter around the Phase 8 verifier."""

    adapter_id = PREVIEW_ADAPTER_ID

    def __init__(self, module: Any) -> None:
        self._module = module

    def __call__(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        return self._module.verify(request, synthetic_self_test=False)


def _default_request_builder(module: Any, expected_identity: Mapping[str, Any]) -> RequestBuilder:
    def build(*, bundle: BundleSnapshot) -> Mapping[str, Any]:
        with tempfile.TemporaryDirectory(prefix="phase7-runtime-identity-") as directory:
            identity_path = Path(directory) / "source-identity.json"
            identity_path.write_text(
                json.dumps(dict(expected_identity), sort_keys=True), encoding="utf-8", newline="\n"
            )
            return module.build_request_from_bundle(
                evidence_root=bundle.index_path.parent,
                asset_index_path=bundle.index_path.name,
                envelope_path=next(
                    asset.name
                    for asset in bundle.assets.values()
                    if asset.evidence_kind == "evidence_envelope"
                ),
                expected_source_identity_path=identity_path,
            )

    return build


def _load_defaults() -> tuple[
    Mapping[str, Any],
    Mapping[str, Any],
    AttestationIssuer,
    RuntimeValidator,
    Any,
    Any,
]:
    import test_openai_phase7_modes as phase7

    issuer = getattr(phase7, "issue_external_runtime_attestation", None)
    if not callable(issuer):
        _fail(
            "external_attestation_factory_unavailable",
            "phase7.issue_external_runtime_attestation",
            "the Phase 7 in-process attestation factory is not available",
        )
    phase8 = _load_phase8_module()
    verifier = RealPreviewVerifier(phase8)
    registry = _parse_mapping(_read_bytes(REGISTRY_PATH, "registry"), "registry")
    schema = _parse_mapping(_read_bytes(RUNTIME_SCHEMA_PATH, "runtime_schema"), "runtime_schema")
    # The identity-bound builder is created by validate_external_runtime_evidence.
    return (
        registry,
        schema,
        issuer,
        phase7.validate_runtime_collection,
        verifier,
        phase8,
    )


def validate_external_runtime_evidence(
    *,
    evidence_root: Path,
    runtime_receipts_path: Path,
    expected_source_identity_path: Path,
    asset_index_pattern: str,
    registry: Mapping[str, Any],
    schema: Mapping[str, Any],
    attestation_issuer: AttestationIssuer,
    runtime_validator: RuntimeValidator,
    live_verifier: Any,
    request_builder: RequestBuilder,
    report_session_issuer: RuntimeReportSessionIssuer | None = None,
    retain_report_session: bool = False,
) -> dict[str, Any] | ExternalRuntimeEvidenceRun:
    if _is_link_or_junction(evidence_root):
        _fail("symlink_rejected", "evidence_root", str(evidence_root))
    try:
        root = evidence_root.resolve(strict=True)
    except OSError as exc:
        _fail("evidence_root_missing", "evidence_root", f"{type(exc).__name__}: {exc}")
    if not root.is_dir():
        _fail("evidence_root_missing", "evidence_root", str(evidence_root))
    receipts_snapshot = _snapshot(
        _resolve_input(runtime_receipts_path, "runtime_receipts"), "runtime_receipts"
    )
    identity_snapshot = _snapshot(
        _resolve_input(expected_source_identity_path, "expected_source_identity"),
        "expected_source_identity",
    )
    collection = _parse_mapping(receipts_snapshot.payload, "runtime_receipts")
    expected_identity = _normalized_identity(
        _parse_mapping(identity_snapshot.payload, "expected_source_identity")
    )
    _assert_current_checkout_identity(expected_identity)
    receipts = _sequence(collection.get("receipts"), "runtime_receipts.receipts")
    if len(receipts) != EXPECTED_RECEIPT_COUNT:
        _fail("runtime_receipt_count", "runtime_receipts.receipts", str(len(receipts)))
    receipt_map: dict[str, Mapping[str, Any]] = {}
    for offset, value in enumerate(receipts):
        receipt = _mapping(value, f"runtime_receipts.receipts[{offset}]")
        receipt_id = receipt.get("receipt_id")
        if not isinstance(receipt_id, str) or not receipt_id:
            _fail("runtime_receipt_id", f"runtime_receipts.receipts[{offset}]", repr(receipt_id))
        if receipt_id in receipt_map:
            _fail("duplicate_receipt", f"runtime_receipts.receipts[{offset}]", receipt_id)
        if receipt.get("status") != "verified":
            _fail("runtime_receipt_not_verified", f"runtime_receipts.receipts[{offset}]", receipt_id)
        receipt_map[receipt_id] = receipt

    trust = _mapping(collection.get("platform_trust"), "runtime_receipts.platform_trust")
    adapter_id = trust.get("adapter_id")
    if (
        trust.get("adapter_status") != "configured"
        or trust.get("verification_level") != PREVIEW_ATTESTED
        or trust.get("provider_authenticated") is not False
        or adapter_id != PREVIEW_ADAPTER_ID
        or getattr(live_verifier, "adapter_id", None) != adapter_id
    ):
        _fail("preview_adapter_not_configured", "runtime_receipts.platform_trust", str(adapter_id))

    indexes = _discover_indexes(root, asset_index_pattern)
    snapshots: dict[Path, SourceSnapshot] = {
        receipts_snapshot.path: receipts_snapshot,
        identity_snapshot.path: identity_snapshot,
    }
    preloaded: list[tuple[Path, Mapping[str, Any], bytes, dict[int, AssetSnapshot]]] = []
    indexed_source_paths: set[Path] = set()
    for index_path in indexes:
        index_snapshot = _snapshot(index_path, "asset_index")
        if index_path in snapshots:
            _fail("duplicate_input_file", "asset_index", str(index_path))
        snapshots[index_path] = index_snapshot
        index_document = _parse_mapping(index_snapshot.payload, str(index_path))
        assets = _load_asset_snapshots(root=root, index_path=index_path, index_document=index_document)
        for asset in assets.values():
            if asset.source_path in snapshots:
                _fail("indexed_control_file_reused", "asset", str(asset.source_path))
            if asset.source_path in indexed_source_paths:
                _fail("asset_file_reused_across_bundles", "asset", str(asset.source_path))
            indexed_source_paths.add(asset.source_path)
            snapshots[asset.source_path] = SourceSnapshot(
                path=asset.source_path, payload=asset.payload, digest=asset.digest
            )
        preloaded.append((index_path, index_document, index_snapshot.payload, assets))

    allowed_inventory = set(indexes) | indexed_source_paths
    for control_path in (receipts_snapshot.path, identity_snapshot.path):
        try:
            control_path.relative_to(root)
        except ValueError:
            continue
        allowed_inventory.add(control_path)
    source_inventory = _tree_inventory(root, "evidence_root.initial")
    allowed_entries = _allowed_tree_entries(root, allowed_inventory)
    unindexed = sorted(set(source_inventory) - allowed_entries)
    if unindexed:
        _fail("unindexed_evidence_file", "evidence_root", str(unindexed))

    bundles: list[BundleSnapshot] = []
    bundle_ids: set[str] = set()
    bundled_receipts: set[str] = set()
    collection_logical_paths: set[str] = set()
    global_logical_paths: set[str] = set()
    for index_path, index_document, index_bytes, assets in preloaded:
        manifest_asset, manifest = _manifest_asset(assets, label=str(index_path))
        receipt_id = manifest.get("receipt_id")
        receipt = receipt_map.get(str(receipt_id))
        if receipt is None:
            _fail("bundle_receipt_unknown", str(index_path), str(receipt_id))
        (
            bundle_id,
            normalized_receipt_id,
            collection_logical_path,
            workspace_files,
        ) = _workspace_files(
            manifest=manifest,
            manifest_asset_id=manifest_asset.asset_id,
            assets=assets,
            receipt=receipt,
            runtime_receipts_bytes=receipts_snapshot.payload,
            expected_identity=expected_identity,
            label=f"{index_path}.workspace_manifest",
        )
        bundle_key = bundle_id.casefold()
        if bundle_key in bundle_ids:
            _fail("duplicate_bundle", str(index_path), bundle_id)
        if normalized_receipt_id in bundled_receipts:
            _fail("duplicate_receipt_bundle", str(index_path), normalized_receipt_id)
        bundle_ids.add(bundle_key)
        bundled_receipts.add(normalized_receipt_id)
        collection_logical_paths.add(collection_logical_path)
        for item in workspace_files:
            key = item.logical_path.casefold()
            if key in global_logical_paths:
                _fail("workspace_path_reused_across_bundles", str(index_path), item.logical_path)
            global_logical_paths.add(key)

        envelope_assets = [asset for asset in assets.values() if asset.evidence_kind == "evidence_envelope"]
        report_assets = [asset for asset in assets.values() if asset.evidence_kind == "verifier_report"]
        if len(envelope_assets) != 1 or len(report_assets) != 1:
            _fail("envelope_report_count", str(index_path), "each bundle needs exactly one envelope and report")
        envelope_asset = envelope_assets[0]
        envelope = _parse_mapping(envelope_asset.payload, f"{index_path}.envelope")

        def fetch_asset(record: Mapping[str, Any]) -> bytes:
            asset_id = record.get("asset_id")
            if isinstance(asset_id, bool) or not isinstance(asset_id, int) or asset_id not in assets:
                _fail("asset_fetch_unindexed", str(index_path), str(asset_id))
            return assets[asset_id].payload

        try:
            integrity = validate_evidence_bundle(
                envelope,
                index_document,
                fetch_asset,
                envelope_bytes=envelope_asset.payload,
                expected_source_identity=expected_identity,
                index_bytes=index_bytes,
            )
        except EvidenceValidationError as exc:
            _fail(exc.code, f"{index_path}:{exc.path}", exc.message)
        task_path = _mapping(receipt.get("binding"), "receipt.binding").get("task_export", {}).get("path")
        task_file = next((item for item in workspace_files if item.logical_path == task_path), None)
        if task_file is None or integrity.raw_export_sha256 != task_file.digest:
            _fail("bundle_raw_export_receipt_mismatch", str(index_path), normalized_receipt_id)
        bundles.append(
            BundleSnapshot(
                bundle_id=bundle_id,
                receipt_id=normalized_receipt_id,
                index_path=index_path,
                index_document=index_document,
                index_bytes=index_bytes,
                assets=assets,
                envelope=envelope,
                envelope_bytes=envelope_asset.payload,
                workspace_files=workspace_files,
                integrity_result=integrity,
            )
        )

    if bundled_receipts != set(receipt_map):
        _fail(
            "runtime_bundle_slot_coverage",
            "asset_indexes",
            f"missing={sorted(set(receipt_map) - bundled_receipts)} extra={sorted(bundled_receipts - set(receipt_map))}",
        )
    if len(collection_logical_paths) != 1:
        _fail(
            "runtime_collection_logical_path_mismatch",
            "workspace_manifests",
            str(sorted(collection_logical_paths)),
        )
    _assert_current_checkout_identity(expected_identity)
    _assert_snapshots_unchanged(snapshots, "before_live_attestation")
    _assert_inventory_unchanged(root, source_inventory, "before_live_attestation")

    attestations: dict[str, Any] = {}
    for bundle in bundles:
        request = request_builder(bundle=bundle)
        try:
            attestation = attestation_issuer(
                bundle.integrity_result,
                receipt_id=bundle.receipt_id,
                live_verifier=live_verifier,
                live_verifier_request=dict(request),
                expected_adapter_id=str(adapter_id),
            )
        except Exception as exc:
            _assert_snapshots_unchanged(snapshots, "failed_live_attestation")
            _assert_inventory_unchanged(root, source_inventory, "failed_live_attestation")
            _fail("live_attestation_failed", bundle.receipt_id, f"{type(exc).__name__}: {exc}")
        if attestation is None:
            _fail("live_attestation_missing", bundle.receipt_id, "issuer returned no attestation")
        attestations[bundle.receipt_id] = attestation
    _assert_snapshots_unchanged(snapshots, "after_live_attestation")
    _assert_inventory_unchanged(root, source_inventory, "after_live_attestation")

    with tempfile.TemporaryDirectory(prefix="phase7-attested-workspace-") as directory:
        workspace_root = Path(directory).resolve()
        materialized: dict[str, str] = {}
        for bundle in bundles:
            for item in bundle.workspace_files:
                path = workspace_root / Path(*PurePosixPath(item.logical_path).parts)
                resolved = _inside(workspace_root, path, f"workspace.{item.logical_path}", must_exist=False)
                if resolved.exists():
                    _fail("workspace_materialization_collision", item.logical_path, str(resolved))
                resolved.parent.mkdir(parents=True, exist_ok=True)
                resolved.write_bytes(item.payload)
                if sha256_bytes(resolved.read_bytes()) != item.digest:
                    _fail("workspace_materialization_digest", item.logical_path, item.digest)
                materialized[item.logical_path] = item.digest

        before_inventory = _tree_inventory(
            workspace_root, "temporary_workspace.before_runtime_validation"
        )
        before_paths = {
            path: digest
            for path, (kind, digest) in before_inventory.items()
            if kind == "file" and digest is not None
        }
        expected_entries = set(materialized)
        for logical_path in materialized:
            parent = PurePosixPath(logical_path).parent
            while parent.parts and parent.as_posix() != ".":
                expected_entries.add(parent.as_posix())
                parent = parent.parent
        if before_paths != materialized:
            _fail("workspace_materialization_inventory", "temporary_workspace", "unexpected files")
        if set(before_inventory) != expected_entries:
            _fail(
                "workspace_materialization_inventory",
                "temporary_workspace",
                "unexpected directories or entry types",
            )
        try:
            results = runtime_validator(
                dict(collection),
                schema=dict(schema),
                registry=dict(registry),
                expected_source_commit=str(expected_identity["source_commit"]),
                root=workspace_root,
                supported_preview_adapter_ids=frozenset({str(adapter_id)}),
                supported_provider_adapter_ids=frozenset(),
                validated_evidence_results=attestations,
            )
        except Exception as exc:
            after_failure_inventory = _tree_inventory(
                workspace_root, "temporary_workspace.failed_runtime_validation"
            )
            if after_failure_inventory != before_inventory:
                _fail(
                    "temporary_workspace_changed",
                    "runtime_validator",
                    "workspace bytes, paths, or entry types changed",
                )
            _fail("phase7_runtime_validation_failed", "runtime_validator", f"{type(exc).__name__}: {exc}")
        after_inventory = _tree_inventory(
            workspace_root, "temporary_workspace.after_runtime_validation"
        )
        if after_inventory != before_inventory:
            _fail(
                "temporary_workspace_changed",
                "runtime_validator",
                "workspace bytes, paths, or entry types changed",
            )

    _assert_snapshots_unchanged(snapshots, "after_runtime_validation")
    _assert_inventory_unchanged(root, source_inventory, "after_runtime_validation")
    _assert_current_checkout_identity(expected_identity)
    result_ids = [item.get("receipt_id") for item in results]
    if (
        len(results) != EXPECTED_RECEIPT_COUNT
        or any(item.get("status") != "verified" for item in results)
        or len(result_ids) != len(set(result_ids))
        or set(result_ids) != set(receipt_map)
    ):
        _fail("phase7_runtime_result_incomplete", "runtime_validator", str(len(results)))
    live_slot_results: list[dict[str, Any]] = []
    attestation_metadata_available = all(
        all(
            hasattr(attestation, field)
            for field in (
                "evidence_id",
                "adapter_id",
                "live_result_digest",
                "verifier_workflow_run_id",
                "verified_at",
            )
        )
        for attestation in attestations.values()
    )
    if retain_report_session and not attestation_metadata_available:
        _fail(
            "live_slot_summary_incomplete",
            "external_runtime_validation",
            "report retention requires live attestation metadata",
        )
    for bundle in (
        sorted(bundles, key=lambda item: item.receipt_id)
        if attestation_metadata_available
        else ()
    ):
        attestation = attestations[bundle.receipt_id]
        release_identity = _mapping(
            bundle.index_document.get("github_release"),
            f"{bundle.index_path}.github_release",
        )
        live_slot_results.append(
            {
                "receipt_id": bundle.receipt_id,
                "evidence_id": attestation.evidence_id,
                "adapter_id": attestation.adapter_id,
                "live_result_digest": attestation.live_result_digest,
                "verifier_workflow_run_id": (
                    attestation.verifier_workflow_run_id
                ),
                "verified_at": attestation.verified_at,
                "release": dict(release_identity),
                "asset_index": {
                    "name": bundle.index_path.name,
                    "size": len(bundle.index_bytes),
                    "sha256": sha256_bytes(bundle.index_bytes),
                },
                "assets": [
                    {
                        "asset_id": asset.asset_id,
                        "name": asset.name,
                        "size": asset.size,
                        "sha256": asset.digest,
                        "evidence_kind": asset.evidence_kind,
                    }
                    for asset in sorted(
                        bundle.assets.values(), key=lambda item: item.asset_id
                    )
                ],
            }
        )
    summary = {
        "schema_version": RESULT_SCHEMA,
        "accepted": True,
        "verification_level": PREVIEW_ATTESTED,
        "provider_verified": False,
        "adapter_id": adapter_id,
        "source_identity": expected_identity,
        "bundle_count": len(bundles),
        "receipt_count": len(results),
        "receipt_ids": sorted(receipt_map),
        "live_slot_results": live_slot_results,
        "workspace_file_count": len(global_logical_paths),
        "source_immutability_verified": True,
        "temporary_workspace_immutability_verified": True,
    }
    if not retain_report_session:
        if report_session_issuer is not None:
            _fail(
                "report_session_issuer_without_retention",
                "report_session_issuer",
                "a report-session issuer is only valid for same-process retention",
            )
        return summary
    if not callable(report_session_issuer):
        _fail(
            "report_session_issuer_missing",
            "report_session_issuer",
            "same-process report generation requires the opaque session issuer",
        )
    try:
        report_session = report_session_issuer(
            collection=collection,
            runtime_receipts_sha256=receipts_snapshot.digest,
            expected_source_commit=str(expected_identity["source_commit"]),
            expected_adapter_id=str(adapter_id),
            validated_evidence_results=attestations,
            validated_runtime_results=results,
        )
    except Exception as exc:
        _fail(
            "report_session_issue_failed",
            "report_session_issuer",
            f"{type(exc).__name__}: {exc}",
        )
    if report_session is None:
        _fail(
            "report_session_missing",
            "report_session_issuer",
            "issuer returned no report session",
        )
    return ExternalRuntimeEvidenceRun(summary=summary, report_session=report_session)


def validate_external_runtime_evidence_for_report(
    *,
    evidence_root: Path,
    runtime_receipts_path: Path,
    expected_source_identity_path: Path,
    asset_index_pattern: str,
) -> ExternalRuntimeEvidenceRun:
    """Run the production verifier and retain its opaque report session."""

    import test_openai_phase7_modes as phase7

    registry, schema, issuer, validator, verifier, phase8 = _load_defaults()
    expected_identity = _normalized_identity(
        _parse_mapping(
            _read_bytes(expected_source_identity_path, "expected_source_identity"),
            "expected_source_identity",
        )
    )
    result = validate_external_runtime_evidence(
        evidence_root=evidence_root,
        runtime_receipts_path=runtime_receipts_path,
        expected_source_identity_path=expected_source_identity_path,
        asset_index_pattern=asset_index_pattern,
        registry=registry,
        schema=schema,
        attestation_issuer=issuer,
        runtime_validator=validator,
        live_verifier=verifier,
        request_builder=_default_request_builder(phase8, expected_identity),
        report_session_issuer=phase7.issue_external_runtime_validation_session,
        retain_report_session=True,
    )
    if not isinstance(result, ExternalRuntimeEvidenceRun):
        _fail(
            "report_session_missing",
            "external_runtime_validation",
            "production validation did not retain its report session",
        )
    return result


def build_attested_phase7_result(
    *,
    evidence_root: Path,
    runtime_receipts_path: Path,
    expected_source_identity_path: Path,
    asset_index_pattern: str,
    live_release_evidence_verifier: Any,
) -> dict[str, Any]:
    """Return the strict report plus its ten live, Release-bound slot records."""

    import test_openai_phase7_modes as phase7

    run = validate_external_runtime_evidence_for_report(
        evidence_root=evidence_root,
        runtime_receipts_path=runtime_receipts_path,
        expected_source_identity_path=expected_source_identity_path,
        asset_index_pattern=asset_index_pattern,
    )
    report = phase7.build_attested_phase7_report(
        external_runtime_session=run.report_session,
        live_release_evidence_verifier=live_release_evidence_verifier,
    )
    live_slots = run.summary.get("live_slot_results")
    if not isinstance(live_slots, list) or len(live_slots) != EXPECTED_RECEIPT_COUNT:
        _fail(
            "live_slot_summary_incomplete",
            "external_runtime_validation",
            str(len(live_slots) if isinstance(live_slots, list) else None),
        )
    return {
        "phase7_report": report,
        "live_slot_results": live_slots,
    }


def build_attested_phase7_report(
    *,
    evidence_root: Path,
    runtime_receipts_path: Path,
    expected_source_identity_path: Path,
    asset_index_pattern: str,
    live_release_evidence_verifier: Any,
) -> dict[str, Any]:
    """Backward-compatible report-only wrapper over the live result bridge."""

    result = build_attested_phase7_result(
        evidence_root=evidence_root,
        runtime_receipts_path=runtime_receipts_path,
        expected_source_identity_path=expected_source_identity_path,
        asset_index_pattern=asset_index_pattern,
        live_release_evidence_verifier=live_release_evidence_verifier,
    )
    return dict(_mapping(result.get("phase7_report"), "phase7_report"))


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise RuntimeEvidenceError("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description="Validate real Phase 7 runtime evidence bundles")
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--runtime-receipts", required=True)
    parser.add_argument("--expected-source-identity", required=True)
    parser.add_argument("--asset-index-pattern", required=True)
    parser.add_argument(
        "--report-output",
        help="Atomically write a strict complete Preview Phase 7 report.",
    )
    parser.add_argument(
        "--release-evidence-bundle-root",
        help="Eight-record live release-evidence bundle root required by --report-output.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        report_requested = args.report_output is not None
        if report_requested is not (args.release_evidence_bundle_root is not None):
            _fail(
                "invalid_cli_arguments",
                "cli",
                "--report-output and --release-evidence-bundle-root must be supplied together",
            )
        if report_requested:
            import test_openai_phase7_modes as phase7
            from validate_openai_release_evidence import create_production_callback

            report = build_attested_phase7_report(
                evidence_root=Path(args.evidence_root),
                runtime_receipts_path=Path(args.runtime_receipts),
                expected_source_identity_path=Path(args.expected_source_identity),
                asset_index_pattern=args.asset_index_pattern,
                live_release_evidence_verifier=create_production_callback(
                    Path(args.release_evidence_bundle_root)
                ),
            )
            report_path = Path(args.report_output)
            phase7.write_phase7_report(report, output_path=report_path)
            output = {
                "schema_version": RESULT_SCHEMA,
                "accepted": True,
                "verification_level": PREVIEW_ATTESTED,
                "provider_verified": False,
                "phase7_report_written": str(report_path),
                "phase7_status": report["phase_status"],
                "runtime_receipts_verified": report["summary"][
                    "runtime_receipts_verified"
                ],
                "completion_gates_verified": report["summary"][
                    "completion_gates_verified"
                ],
                "pending_gate_count": len(report["pending_gates"]),
            }
        else:
            registry, schema, issuer, validator, verifier, phase8 = _load_defaults()
            identity_document = _parse_mapping(
                _read_bytes(
                    Path(args.expected_source_identity),
                    "expected_source_identity",
                ),
                "expected_source_identity",
            )
            expected_identity = _normalized_identity(identity_document)
            output = validate_external_runtime_evidence(
                evidence_root=Path(args.evidence_root),
                runtime_receipts_path=Path(args.runtime_receipts),
                expected_source_identity_path=Path(args.expected_source_identity),
                asset_index_pattern=args.asset_index_pattern,
                registry=registry,
                schema=schema,
                attestation_issuer=issuer,
                runtime_validator=validator,
                live_verifier=verifier,
                request_builder=_default_request_builder(phase8, expected_identity),
            )
    except RuntimeEvidenceError as exc:
        output = {
            "schema_version": RESULT_SCHEMA,
            "accepted": False,
            "error": {"code": exc.code, "path": exc.path, "message": exc.message},
        }
        code = 2 if exc.code == "invalid_cli_arguments" else 1
    except Exception as exc:
        output = {
            "schema_version": RESULT_SCHEMA,
            "accepted": False,
            "error": {
                "code": "internal_error",
                "path": "cli",
                "message": f"{type(exc).__name__}: {exc}",
            },
        }
        code = 3
    else:
        code = 0
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
