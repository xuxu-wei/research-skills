#!/usr/bin/env python3
"""Validation primitives for externally witnessed Preview evidence bundles.

The module is deliberately transport-neutral. Callers inject an asset fetcher;
this file never performs network I/O and never treats repository-authored status
text as proof of an external run.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Mapping, Sequence

import yaml

from openai_release_utils import parse_semver


EVIDENCE_ENVELOPE_SCHEMA = "openai-preview-evidence-envelope/v1"
RELEASE_ASSET_INDEX_SCHEMA = "openai-preview-release-asset-index/v1"
VERIFIER_REPORT_SCHEMA = "openai-preview-verifier-report/v1"
PREVIEW_ATTESTED = "preview_attested"
PROVIDER_VERIFIED = "provider_verified"
VERIFICATION_LEVELS = frozenset({PREVIEW_ATTESTED, PROVIDER_VERIFIED})

CAPTURE_EXPORT_KINDS = frozenset({"raw_export", "structured_export", "task_export"})
# Backwards-compatible alias for callers that imported the old constant.  A
# provider receipt is deliberately excluded: it attests provenance but is not
# itself a captured task/export.
RAW_EVIDENCE_KINDS = CAPTURE_EXPORT_KINDS
NON_SUBSTANTIVE_EVIDENCE_KINDS = frozenset(
    {"screenshot", "manual_note", "manual_status"}
)
ALL_EVIDENCE_KINDS = RAW_EVIDENCE_KINDS | NON_SUBSTANTIVE_EVIDENCE_KINDS | {
    "supporting_file",
    "provider_receipt",
    "evidence_envelope",
    "verifier_report",
}

MAX_FUTURE_SKEW = timedelta(minutes=5)
MAX_EVIDENCE_AGE = timedelta(days=90)

_HEX_40_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_HEX_64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$")
_REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class EvidenceValidationError(ValueError):
    """A stable, machine-inspectable Preview evidence validation failure."""

    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


@dataclass(frozen=True)
class VerifiedAsset:
    asset_id: int
    name: str
    sha256: str
    size: int
    evidence_kind: str


@dataclass(frozen=True)
class VerifiedReleaseAssetIndex:
    repository: str
    release_id: int
    release_tag: str
    source_identity: Mapping[str, str]
    workflow_run_id: int
    actor: str
    witnessed_at: datetime
    index_sha256: str
    assets: Mapping[int, VerifiedAsset]
    asset_payloads: Mapping[int, bytes]


@dataclass(frozen=True)
class EvidenceValidationResult:
    evidence_id: str
    integrity_valid: bool
    gate_eligible: bool
    verification_level: str
    claimed_provider_verified: bool
    claimed_counts_as_preview_acceptance: bool
    provider_verified: bool
    counts_as_preview_acceptance: bool
    source_identity_bound: bool
    source_identity: Mapping[str, str]
    raw_export_asset_id: int
    raw_export_sha256: str
    evidence_envelope_asset_id: int
    evidence_envelope_sha256: str
    verifier_report_asset_id: int
    verifier_report_sha256: str
    release_asset_index_sha256: str


AssetFetcher = Callable[[Mapping[str, Any]], bytes]


def _fail(code: str, path: str, message: str) -> None:
    raise EvidenceValidationError(code, path, message)


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("invalid_type", path, "expected a mapping")
    return value


def _sequence(value: Any, path: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        _fail("invalid_type", path, "expected a sequence")
    return value


def _required(mapping: Mapping[str, Any], key: str, path: str) -> Any:
    if key not in mapping:
        _fail("missing_field", f"{path}.{key}", "required field is absent")
    return mapping[key]


def _nonempty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("invalid_string", path, "expected a non-empty string")
    return value.strip()


def _identifier(value: Any, path: str) -> str:
    text = _nonempty_string(value, path)
    if not _IDENTIFIER_RE.fullmatch(text):
        _fail("invalid_identifier", path, "contains unsupported characters")
    return text


def _positive_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail("invalid_positive_integer", path, "expected a positive integer")
    return value


def _strict_bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        _fail("invalid_boolean", path, "expected a boolean")
    return value


def normalize_sha256(value: Any, path: str = "sha256") -> str:
    """Return a lowercase ``sha256:<hex>`` digest or raise a stable error."""

    text = _nonempty_string(value, path)
    raw = text.removeprefix("sha256:")
    if not _HEX_64_RE.fullmatch(raw):
        _fail("invalid_sha256", path, "expected 64 hexadecimal characters")
    return f"sha256:{raw.lower()}"


def sha256_bytes(payload: bytes) -> str:
    """Return a normalized SHA-256 digest for raw bytes."""

    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def canonical_json_bytes(document: Mapping[str, Any]) -> bytes:
    """Serialize a mapping deterministically for fixture and binding digests."""

    return json.dumps(
        document,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _normalize_now(now: datetime | None) -> datetime:
    current = now if now is not None else datetime.now(timezone.utc)
    if current.tzinfo is None or current.utcoffset() is None:
        _fail("invalid_timestamp", "now", "timestamp must include a UTC offset")
    return current.astimezone(timezone.utc)


def _timestamp(value: Any, path: str) -> datetime:
    text = _nonempty_string(value, path)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        _fail("invalid_timestamp", path, "expected an ISO-8601 timestamp")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("invalid_timestamp", path, "timestamp must include a UTC offset")
    return parsed.astimezone(timezone.utc)


def _validate_timestamp_window(value: datetime, path: str, now: datetime) -> None:
    if value > now + MAX_FUTURE_SKEW:
        _fail(
            "timestamp_too_far_in_future",
            path,
            "timestamp is more than five minutes ahead of the verification clock",
        )
    if value < now - MAX_EVIDENCE_AGE:
        _fail(
            "stale_evidence_timestamp",
            path,
            "timestamp is more than 90 days older than the verification clock",
        )


def _assert_document_matches_bytes(
    document: Mapping[str, Any], payload: bytes, path: str
) -> None:
    if not isinstance(payload, bytes):
        _fail("invalid_asset_payload", path, "document bytes must be bytes")
    try:
        loaded = yaml.safe_load(payload)
    except yaml.YAMLError as exc:
        _fail("invalid_document", path, f"raw bytes are not valid JSON/YAML: {exc}")
    if not isinstance(loaded, Mapping):
        _fail("invalid_document", path, "raw bytes must decode to a mapping")
    if dict(loaded) != dict(document):
        _fail(
            "envelope_document_mismatch",
            path,
            "parsed envelope document does not match the supplied raw envelope bytes",
        )


def _parse_verifier_report(payload: bytes, path: str) -> Mapping[str, Any]:
    try:
        loaded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail("invalid_verifier_report", path, f"expected UTF-8 JSON: {exc}")
    if not isinstance(loaded, Mapping):
        _fail("invalid_verifier_report", path, "expected a JSON object")
    if _required(loaded, "schema_version", path) != VERIFIER_REPORT_SCHEMA:
        _fail("unsupported_schema", f"{path}.schema_version", VERIFIER_REPORT_SCHEMA)
    return loaded


def _source_identity(value: Any, path: str) -> dict[str, str]:
    identity = _mapping(value, path)
    plugin_version = _nonempty_string(
        _required(identity, "plugin_version", path), f"{path}.plugin_version"
    )
    if parse_semver(plugin_version) is None:
        _fail("invalid_plugin_version", f"{path}.plugin_version", "expected strict SemVer")
    source_commit = _nonempty_string(
        _required(identity, "source_commit", path), f"{path}.source_commit"
    ).lower()
    if not _HEX_40_RE.fullmatch(source_commit):
        _fail("invalid_source_commit", f"{path}.source_commit", "expected a full 40-hex commit")
    return {
        "plugin_version": plugin_version,
        "source_commit": source_commit,
        "manifest_sha256": normalize_sha256(
            _required(identity, "manifest_sha256", path), f"{path}.manifest_sha256"
        ),
        "registry_sha256": normalize_sha256(
            _required(identity, "registry_sha256", path), f"{path}.registry_sha256"
        ),
        "skill_tree_sha256": normalize_sha256(
            _required(identity, "skill_tree_sha256", path), f"{path}.skill_tree_sha256"
        ),
    }


def _assert_expected_identity(
    actual: Mapping[str, str], expected: Mapping[str, Any] | None, path: str
) -> None:
    if expected is None:
        return
    for key, expected_value in expected.items():
        if key not in actual:
            _fail("unknown_identity_field", f"{path}.{key}", "field is not comparable")
        if key.endswith("_sha256"):
            normalized = normalize_sha256(expected_value, f"expected_source_identity.{key}")
        elif key == "source_commit":
            normalized = _nonempty_string(
                expected_value, f"expected_source_identity.{key}"
            ).lower()
        else:
            normalized = _nonempty_string(expected_value, f"expected_source_identity.{key}")
        if actual[key] != normalized:
            _fail(
                "source_identity_mismatch",
                f"{path}.{key}",
                f"expected {normalized!r}, found {actual[key]!r}",
            )


def validate_release_asset_index(
    document: Mapping[str, Any],
    fetch_asset: AssetFetcher,
    *,
    expected_source_identity: Mapping[str, Any] | None = None,
    index_bytes: bytes | None = None,
    now: datetime | None = None,
) -> VerifiedReleaseAssetIndex:
    """Fetch and digest-check every indexed GitHub Release asset.

    ``fetch_asset`` receives the asset record and must return its raw bytes. It
    can read local fixtures, a cache, or a caller-owned network client. This
    function itself never opens files or makes a network request.
    """

    verification_clock = _normalize_now(now)
    index = _mapping(document, "asset_index")
    if _required(index, "schema_version", "asset_index") != RELEASE_ASSET_INDEX_SCHEMA:
        _fail("unsupported_schema", "asset_index.schema_version", RELEASE_ASSET_INDEX_SCHEMA)

    source_identity = _source_identity(
        _required(index, "source_identity", "asset_index"), "asset_index.source_identity"
    )
    _assert_expected_identity(source_identity, expected_source_identity, "asset_index.source_identity")

    release = _mapping(_required(index, "github_release", "asset_index"), "asset_index.github_release")
    repository = _nonempty_string(
        _required(release, "repository", "asset_index.github_release"),
        "asset_index.github_release.repository",
    )
    if not _REPOSITORY_RE.fullmatch(repository):
        _fail("invalid_repository", "asset_index.github_release.repository", "expected owner/repository")
    release_id = _positive_int(
        _required(release, "release_id", "asset_index.github_release"),
        "asset_index.github_release.release_id",
    )
    release_tag = _nonempty_string(
        _required(release, "release_tag", "asset_index.github_release"),
        "asset_index.github_release.release_tag",
    )

    witness = _mapping(
        _required(index, "github_witness", "asset_index"), "asset_index.github_witness"
    )
    workflow_run_id = _positive_int(
        _required(witness, "workflow_run_id", "asset_index.github_witness"),
        "asset_index.github_witness.workflow_run_id",
    )
    actor = _identifier(
        _required(witness, "actor", "asset_index.github_witness"),
        "asset_index.github_witness.actor",
    )
    witness_commit = _nonempty_string(
        _required(witness, "source_commit", "asset_index.github_witness"),
        "asset_index.github_witness.source_commit",
    ).lower()
    if witness_commit != source_identity["source_commit"]:
        _fail(
            "source_identity_mismatch",
            "asset_index.github_witness.source_commit",
            "GitHub witness commit does not match the indexed source commit",
        )
    witnessed_at = _timestamp(
        _required(witness, "witnessed_at", "asset_index.github_witness"),
        "asset_index.github_witness.witnessed_at",
    )
    _validate_timestamp_window(
        witnessed_at, "asset_index.github_witness.witnessed_at", verification_clock
    )

    records = _sequence(_required(index, "assets", "asset_index"), "asset_index.assets")
    if not records:
        _fail("missing_assets", "asset_index.assets", "at least one asset is required")
    verified: dict[int, VerifiedAsset] = {}
    verified_payloads: dict[int, bytes] = {}
    names: set[str] = set()
    for offset, raw_record in enumerate(records):
        path = f"asset_index.assets[{offset}]"
        record = _mapping(raw_record, path)
        asset_id = _positive_int(_required(record, "asset_id", path), f"{path}.asset_id")
        name = _nonempty_string(_required(record, "name", path), f"{path}.name")
        if asset_id in verified:
            _fail("duplicate_asset_id", f"{path}.asset_id", str(asset_id))
        if name in names:
            _fail("duplicate_asset_name", f"{path}.name", name)
        evidence_kind = _nonempty_string(
            _required(record, "evidence_kind", path), f"{path}.evidence_kind"
        )
        if evidence_kind not in ALL_EVIDENCE_KINDS:
            _fail("unsupported_evidence_kind", f"{path}.evidence_kind", evidence_kind)
        expected_digest = normalize_sha256(_required(record, "sha256", path), f"{path}.sha256")
        expected_size = _positive_int(_required(record, "size", path), f"{path}.size")
        try:
            payload = fetch_asset(record)
        except Exception as exc:  # Boundary adapter errors become stable validation failures.
            _fail("asset_fetch_failed", path, f"{type(exc).__name__}: {exc}")
        if not isinstance(payload, bytes):
            _fail("invalid_asset_payload", path, "fetch_asset must return bytes")
        if len(payload) != expected_size:
            _fail(
                "asset_size_mismatch",
                f"{path}.size",
                f"expected {expected_size}, fetched {len(payload)}",
            )
        actual_digest = sha256_bytes(payload)
        if actual_digest != expected_digest:
            _fail(
                "asset_digest_mismatch",
                f"{path}.sha256",
                f"expected {expected_digest}, fetched {actual_digest}",
            )
        verified[asset_id] = VerifiedAsset(
            asset_id=asset_id,
            name=name,
            sha256=actual_digest,
            size=len(payload),
            evidence_kind=evidence_kind,
        )
        verified_payloads[asset_id] = payload
        names.add(name)

    if not any(asset.evidence_kind in CAPTURE_EXPORT_KINDS for asset in verified.values()):
        _fail(
            "non_substantive_evidence_only",
            "asset_index.assets",
            "at least one raw_export, structured_export, or task_export is required",
        )
    envelope_assets = [
        asset for asset in verified.values() if asset.evidence_kind == "evidence_envelope"
    ]
    if not envelope_assets:
        _fail(
            "missing_witness_envelope_asset",
            "asset_index.assets",
            "the externally witnessed evidence envelope must be indexed and digested",
        )
    if len(envelope_assets) != 1:
        _fail(
            "ambiguous_witness_envelope_asset",
            "asset_index.assets",
            "an integrity bundle must index exactly one evidence_envelope asset",
        )
    report_assets = [
        asset for asset in verified.values() if asset.evidence_kind == "verifier_report"
    ]
    if not report_assets:
        _fail(
            "missing_verifier_report_asset",
            "asset_index.assets",
            "the independent verifier report must be indexed and digested",
        )
    if len(report_assets) != 1:
        _fail(
            "ambiguous_verifier_report_asset",
            "asset_index.assets",
            "an integrity bundle must index exactly one verifier_report asset",
        )

    serialized = index_bytes if index_bytes is not None else canonical_json_bytes(index)
    if not isinstance(serialized, bytes):
        _fail("invalid_asset_payload", "asset_index", "index_bytes must be bytes")
    return VerifiedReleaseAssetIndex(
        repository=repository,
        release_id=release_id,
        release_tag=release_tag,
        source_identity=source_identity,
        workflow_run_id=workflow_run_id,
        actor=actor,
        witnessed_at=witnessed_at,
        index_sha256=sha256_bytes(serialized),
        assets=verified,
        asset_payloads=verified_payloads,
    )


def validate_evidence_envelope(
    document: Mapping[str, Any],
    verified_index: VerifiedReleaseAssetIndex,
    *,
    envelope_bytes: bytes,
    expected_source_identity: Mapping[str, Any] | None = None,
    now: datetime | None = None,
) -> EvidenceValidationResult:
    """Validate envelope integrity against digest-checked Release assets.

    This function validates only structure, cryptographic bindings, identity
    claims, and chronology.  It cannot authenticate the provider or make the
    evidence eligible for a Preview/release gate; an outer authenticated
    adapter must perform that promotion.
    """

    verification_clock = _normalize_now(now)
    envelope = _mapping(document, "envelope")
    _assert_document_matches_bytes(envelope, envelope_bytes, "envelope")
    if _required(envelope, "schema_version", "envelope") != EVIDENCE_ENVELOPE_SCHEMA:
        _fail("unsupported_schema", "envelope.schema_version", EVIDENCE_ENVELOPE_SCHEMA)
    evidence_id = _identifier(_required(envelope, "evidence_id", "envelope"), "envelope.evidence_id")
    level = _nonempty_string(
        _required(envelope, "verification_level", "envelope"),
        "envelope.verification_level",
    )
    if level not in VERIFICATION_LEVELS:
        _fail("invalid_verification_level", "envelope.verification_level", level)
    claimed_provider_verified = _strict_bool(
        _required(envelope, "provider_verified", "envelope"), "envelope.provider_verified"
    )
    claimed_counts_as_preview = _strict_bool(
        _required(envelope, "counts_as_preview_acceptance", "envelope"),
        "envelope.counts_as_preview_acceptance",
    )
    expected_provider_flag = level == PROVIDER_VERIFIED
    if claimed_provider_verified != expected_provider_flag:
        _fail(
            "verification_level_conflict",
            "envelope.provider_verified",
            f"{level} requires provider_verified={expected_provider_flag}",
        )

    source_identity = _source_identity(
        _required(envelope, "source_identity", "envelope"), "envelope.source_identity"
    )
    _assert_expected_identity(source_identity, expected_source_identity, "envelope.source_identity")
    if source_identity != dict(verified_index.source_identity):
        _fail(
            "source_identity_mismatch",
            "envelope.source_identity",
            "envelope and Release asset index identify different source trees",
        )

    adapter = _mapping(_required(envelope, "adapter", "envelope"), "envelope.adapter")
    adapter_id = _identifier(
        _required(adapter, "adapter_id", "envelope.adapter"), "envelope.adapter.adapter_id"
    )
    normalize_sha256(
        _required(adapter, "adapter_code_sha256", "envelope.adapter"),
        "envelope.adapter.adapter_code_sha256",
    )

    capture = _mapping(_required(envelope, "capture", "envelope"), "envelope.capture")
    _identifier(_required(capture, "surface", "envelope.capture"), "envelope.capture.surface")
    _identifier(
        _required(capture, "task_or_thread_id", "envelope.capture"),
        "envelope.capture.task_or_thread_id",
    )
    captured_at = _timestamp(
        _required(capture, "captured_at", "envelope.capture"), "envelope.capture.captured_at"
    )
    _validate_timestamp_window(captured_at, "envelope.capture.captured_at", verification_clock)
    raw_asset_id = _positive_int(
        _required(capture, "raw_export_asset_id", "envelope.capture"),
        "envelope.capture.raw_export_asset_id",
    )
    raw_digest = normalize_sha256(
        _required(capture, "raw_export_sha256", "envelope.capture"),
        "envelope.capture.raw_export_sha256",
    )
    raw_asset = verified_index.assets.get(raw_asset_id)
    if raw_asset is None:
        _fail(
            "unindexed_raw_export",
            "envelope.capture.raw_export_asset_id",
            "raw export is not present in the verified Release asset index",
        )
    if raw_asset.evidence_kind not in CAPTURE_EXPORT_KINDS:
        _fail(
            "non_substantive_raw_export",
            "envelope.capture.raw_export_asset_id",
            f"asset kind {raw_asset.evidence_kind!r} cannot prove a run",
        )
    if raw_asset.sha256 != raw_digest:
        _fail(
            "asset_digest_mismatch",
            "envelope.capture.raw_export_sha256",
            "envelope digest does not match the fetched Release asset",
        )

    witness = _mapping(
        _required(envelope, "github_witness", "envelope"), "envelope.github_witness"
    )
    witness_repository = _nonempty_string(
        _required(witness, "repository", "envelope.github_witness"),
        "envelope.github_witness.repository",
    )
    witness_release_id = _positive_int(
        _required(witness, "release_id", "envelope.github_witness"),
        "envelope.github_witness.release_id",
    )
    witness_tag = _nonempty_string(
        _required(witness, "release_tag", "envelope.github_witness"),
        "envelope.github_witness.release_tag",
    )
    witness_run_id = _positive_int(
        _required(witness, "workflow_run_id", "envelope.github_witness"),
        "envelope.github_witness.workflow_run_id",
    )
    witness_actor = _identifier(
        _required(witness, "actor", "envelope.github_witness"),
        "envelope.github_witness.actor",
    )
    for forbidden_field in (
        "asset_index_sha256",
        "envelope_asset_id",
        "envelope_sha256",
    ):
        if forbidden_field in witness:
            _fail(
                "circular_digest_binding",
                f"envelope.github_witness.{forbidden_field}",
                "the envelope must not reference the later index or its own indexed identity",
            )
    witness_asset_id = _positive_int(
        _required(witness, "raw_export_asset_id", "envelope.github_witness"),
        "envelope.github_witness.raw_export_asset_id",
    )
    witness_envelope_asset = next(
        asset
        for asset in verified_index.assets.values()
        if asset.evidence_kind == "evidence_envelope"
    )
    witness_envelope_asset_id = witness_envelope_asset.asset_id
    actual_envelope_digest = sha256_bytes(envelope_bytes)
    if witness_envelope_asset.sha256 != actual_envelope_digest:
        _fail(
            "asset_digest_mismatch",
            "envelope",
            "actual envelope bytes do not match the indexed evidence_envelope digest",
        )
    indexed_envelope_payload = verified_index.asset_payloads.get(witness_envelope_asset_id)
    if indexed_envelope_payload != envelope_bytes:
        _fail(
            "envelope_asset_mismatch",
            "envelope",
            "actual envelope bytes differ from the fetched evidence_envelope asset",
        )
    if witness_envelope_asset_id == raw_asset_id:
        _fail(
            "witness_envelope_not_distinct",
            "asset_index.assets",
            "witness envelope and captured export must use different asset IDs",
        )
    witness_commit = _nonempty_string(
        _required(witness, "source_commit", "envelope.github_witness"),
        "envelope.github_witness.source_commit",
    ).lower()
    if (
        witness_repository != verified_index.repository
        or witness_release_id != verified_index.release_id
        or witness_tag != verified_index.release_tag
        or witness_run_id != verified_index.workflow_run_id
        or witness_actor != verified_index.actor
        or witness_asset_id != raw_asset_id
        or witness_commit != source_identity["source_commit"]
    ):
        _fail(
            "github_witness_mismatch",
            "envelope.github_witness",
            "witness does not bind the envelope to the verified Release, raw asset, and source commit",
        )

    if "verifier" in envelope:
        _fail(
            "forward_reference_in_envelope",
            "envelope.verifier",
            "verifier results belong in the later indexed verifier_report asset",
        )
    expected_verifier = _mapping(
        _required(envelope, "expected_verifier", "envelope"),
        "envelope.expected_verifier",
    )
    verifier_id = _identifier(
        _required(expected_verifier, "verifier_id", "envelope.expected_verifier"),
        "envelope.expected_verifier.verifier_id",
    )
    if verifier_id == adapter_id:
        _fail(
            "verifier_not_independent",
            "envelope.expected_verifier.verifier_id",
            "capture adapter and verifier must have different identities",
        )
    verifier_code_digest = normalize_sha256(
        _required(
            expected_verifier,
            "verifier_code_sha256",
            "envelope.expected_verifier",
        ),
        "envelope.expected_verifier.verifier_code_sha256",
    )
    if not _strict_bool(
        _required(expected_verifier, "independent", "envelope.expected_verifier"),
        "envelope.expected_verifier.independent",
    ):
        _fail(
            "verifier_not_independent",
            "envelope.expected_verifier.independent",
            "must be true",
        )
    forbidden_verifier_result_fields = {
        "asset_index_sha256",
        "verifier_report_asset_id",
        "verifier_report_sha256",
        "verified_at",
        "verdict",
        "raw_export_asset_id",
        "raw_export_sha256",
        "provider_attestation_checked",
    }
    leaked_result_fields = sorted(
        forbidden_verifier_result_fields.intersection(expected_verifier)
    )
    if leaked_result_fields:
        _fail(
            "forward_reference_in_envelope",
            f"envelope.expected_verifier.{leaked_result_fields[0]}",
            "the capture envelope may name expected verifier code, but cannot contain later verifier results",
        )

    witness_role = witness.get("workflow_witness_role")
    if witness_role is None:
        # Legacy envelopes used a post-capture packaging witness.
        if captured_at > verified_index.witnessed_at:
            _fail(
                "invalid_timestamp_order",
                "envelope.capture.captured_at",
                "captured_at must be earlier than or equal to witnessed_at",
            )
    elif witness_role == "source_commit_main_ci":
        # The production Preview adapter binds the already-frozen successful
        # main-push CI run, which necessarily precedes live task capture.
        if verified_index.witnessed_at > captured_at:
            _fail(
                "invalid_timestamp_order",
                "envelope.capture.captured_at",
                "source-commit CI witnessed_at must precede captured_at",
            )
    else:
        _fail(
            "unsupported_workflow_witness_role",
            "envelope.github_witness.workflow_witness_role",
            str(witness_role),
        )

    verifier_report_asset = next(
        asset
        for asset in verified_index.assets.values()
        if asset.evidence_kind == "verifier_report"
    )
    verifier_report_asset_id = verifier_report_asset.asset_id
    if verifier_report_asset_id in {raw_asset_id, witness_envelope_asset_id}:
        _fail(
            "verifier_report_not_distinct",
            "asset_index.assets",
            "verifier report, witness envelope, and captured export require distinct asset IDs",
        )

    verifier_report = _parse_verifier_report(
        verified_index.asset_payloads[verifier_report_asset_id], "verifier_report"
    )
    if "asset_index_sha256" in verifier_report:
        _fail(
            "circular_digest_binding",
            "verifier_report.asset_index_sha256",
            "a verifier report indexed by the asset index must not digest that index",
        )
    report_verifier_id = _identifier(
        _required(verifier_report, "verifier_id", "verifier_report"),
        "verifier_report.verifier_id",
    )
    report_verifier_code_digest = normalize_sha256(
        _required(verifier_report, "verifier_code_sha256", "verifier_report"),
        "verifier_report.verifier_code_sha256",
    )
    report_source_identity = _source_identity(
        _required(verifier_report, "source_identity", "verifier_report"),
        "verifier_report.source_identity",
    )
    report_envelope_asset_id = _positive_int(
        _required(verifier_report, "envelope_asset_id", "verifier_report"),
        "verifier_report.envelope_asset_id",
    )
    report_envelope_digest = normalize_sha256(
        _required(verifier_report, "envelope_sha256", "verifier_report"),
        "verifier_report.envelope_sha256",
    )
    report_raw_asset_id = _positive_int(
        _required(verifier_report, "raw_export_asset_id", "verifier_report"),
        "verifier_report.raw_export_asset_id",
    )
    report_raw_digest = normalize_sha256(
        _required(verifier_report, "raw_export_sha256", "verifier_report"),
        "verifier_report.raw_export_sha256",
    )
    report_verdict = _nonempty_string(
        _required(verifier_report, "verdict", "verifier_report"),
        "verifier_report.verdict",
    )
    report_independent = _strict_bool(
        _required(verifier_report, "independent", "verifier_report"),
        "verifier_report.independent",
    )
    verified_at = _timestamp(
        _required(verifier_report, "verified_at", "verifier_report"),
        "verifier_report.verified_at",
    )
    _validate_timestamp_window(verified_at, "verifier_report.verified_at", verification_clock)
    if verified_index.witnessed_at > verified_at:
        _fail(
            "invalid_timestamp_order",
            "verifier_report.verified_at",
            "verified_at must be later than or equal to witnessed_at",
        )
    if (
        report_verifier_id != verifier_id
        or report_verifier_code_digest != verifier_code_digest
        or report_source_identity != source_identity
        or report_envelope_asset_id != witness_envelope_asset_id
        or report_envelope_digest != actual_envelope_digest
        or report_raw_asset_id != raw_asset_id
        or report_raw_digest != raw_asset.sha256
        or report_verdict != "accepted"
        or not report_independent
    ):
        _fail(
            "verifier_report_binding_mismatch",
            "verifier_report",
            "report does not bind the actual envelope, raw export, source identity, verifier code, and accepted verdict",
        )

    if level == PROVIDER_VERIFIED:
        provider_receipt_id = _positive_int(
            _required(capture, "provider_receipt_asset_id", "envelope.capture"),
            "envelope.capture.provider_receipt_asset_id",
        )
        if provider_receipt_id in {
            raw_asset_id,
            witness_envelope_asset_id,
            verifier_report_asset_id,
        }:
            _fail(
                "provider_receipt_not_distinct",
                "envelope.capture.provider_receipt_asset_id",
                "provider receipt must use an asset ID distinct from the captured export and reports",
            )
        provider_receipt = verified_index.assets.get(provider_receipt_id)
        if provider_receipt is None or provider_receipt.evidence_kind != "provider_receipt":
            _fail(
                "missing_provider_receipt",
                "envelope.capture.provider_receipt_asset_id",
                "provider_verified requires an indexed provider_receipt asset",
            )
        report_provider_receipt_id = _positive_int(
            _required(verifier_report, "provider_receipt_asset_id", "verifier_report"),
            "verifier_report.provider_receipt_asset_id",
        )
        report_provider_receipt_digest = normalize_sha256(
            _required(verifier_report, "provider_receipt_sha256", "verifier_report"),
            "verifier_report.provider_receipt_sha256",
        )
        provider_attestation_checked = _strict_bool(
            _required(verifier_report, "provider_attestation_checked", "verifier_report"),
            "verifier_report.provider_attestation_checked",
        )
        if (
            not provider_attestation_checked
            or report_provider_receipt_id != provider_receipt_id
            or report_provider_receipt_digest != provider_receipt.sha256
        ):
            _fail(
                "provider_attestation_unchecked",
                "verifier_report.provider_attestation_checked",
                "verifier report must bind and independently check the indexed provider receipt",
            )

    return EvidenceValidationResult(
        evidence_id=evidence_id,
        integrity_valid=True,
        gate_eligible=False,
        verification_level=level,
        claimed_provider_verified=claimed_provider_verified,
        claimed_counts_as_preview_acceptance=claimed_counts_as_preview,
        provider_verified=False,
        counts_as_preview_acceptance=False,
        source_identity_bound=expected_source_identity is not None,
        source_identity=source_identity,
        raw_export_asset_id=raw_asset_id,
        raw_export_sha256=raw_asset.sha256,
        evidence_envelope_asset_id=witness_envelope_asset_id,
        evidence_envelope_sha256=witness_envelope_asset.sha256,
        verifier_report_asset_id=verifier_report_asset_id,
        verifier_report_sha256=verifier_report_asset.sha256,
        release_asset_index_sha256=verified_index.index_sha256,
    )


def validate_evidence_bundle(
    envelope: Mapping[str, Any],
    asset_index: Mapping[str, Any],
    fetch_asset: AssetFetcher,
    *,
    envelope_bytes: bytes,
    expected_source_identity: Mapping[str, Any] | None = None,
    index_bytes: bytes | None = None,
    now: datetime | None = None,
) -> EvidenceValidationResult:
    """Validate bundle integrity using a caller-injected asset fetcher."""

    verified_index = validate_release_asset_index(
        asset_index,
        fetch_asset,
        expected_source_identity=expected_source_identity,
        index_bytes=index_bytes,
        now=now,
    )
    return validate_evidence_envelope(
        envelope,
        verified_index,
        envelope_bytes=envelope_bytes,
        expected_source_identity=expected_source_identity,
        now=now,
    )
