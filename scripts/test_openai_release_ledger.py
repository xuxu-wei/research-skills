#!/usr/bin/env python3
"""Validate release-ledger and provenance coverage for the OpenAI plugin."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any, Callable

import yaml

from openai_release_utils import compare_semver, parse_semver
from openai_preview_evidence import (
    PREVIEW_ATTESTED,
    PROVIDER_VERIFIED,
    EvidenceValidationError,
    canonical_json_bytes,
    sha256_bytes as evidence_sha256_bytes,
    validate_evidence_bundle,
)

from generate_openai_release_ledger import (
    LEDGER_PATH,
    MANIFEST_PATH,
    MUTABLE_RUNTIME_EVIDENCE_FILES,
    MUTABLE_RUNTIME_EVIDENCE_PREFIXES,
    PLUGIN,
    REPO,
    SKILL_TREE_ALGORITHM,
    VALIDATION_CONTRACT_FILES,
    VALIDATION_TEST_ROOTS,
    VALIDATION_TREE_ALGORITHM,
    normalized_skill_tree_digest,
    normalized_file_digest,
    normalized_validation_contract_digest,
)


COMMIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INTERNAL_VALID_STATUS = {"pending", "verified"}
EXTERNAL_ACCEPTED_STATUS = {PREVIEW_ATTESTED, PROVIDER_VERIFIED}
EXTERNAL_VALID_STATUS = {"pending", *EXTERNAL_ACCEPTED_STATUS}
EVIDENCE_META_FIELDS = {
    "status",
    "reason",
    "evidence_path",
    "evidence_sha256",
    "evidence_locator",
}
CACHE_IDENTITY_ALGORITHM = "sha256_canonical_json_installable_cache_identity_v1"
CACHE_ARTIFACT_FIELDS = {
    "cache_path",
    "cache_instance_id",
    "cache_identity_algorithm",
    "cache_identity_sha256",
    "plugin_version",
    "source_commit",
    "manifest_sha256",
    "registry_sha256",
    "skill_tree_algorithm",
    "skill_tree_file_count",
    "skill_tree_sha256",
    "license_sha256",
}
CACHE_EVIDENCE_TYPES = {
    "marketplace_upgrade",
    "explicit_reinstall",
    "fresh_task_discovery",
    "rollback",
}
RELEASE_EVIDENCE_SCHEMA_PATH = REPO / "tests" / "openai_phase7" / "release-evidence.schema.yaml"
PROVIDER_VERIFIER_REGISTRY_PATH = (
    REPO / "tests" / "openai_phase8" / "provider-verifier-registry.yaml"
)
LIVE_VERIFIER_MAX_FUTURE_SKEW = timedelta(minutes=5)
LIVE_VERIFIER_MAX_AGE = timedelta(days=90)
# Synthetic timestamps use an injected clock so self-tests do not decay as the
# wall clock advances. Production ledger validation continues to use UTC now.
SYNTHETIC_VALIDATION_NOW = datetime(2026, 7, 13, 0, 4, tzinfo=timezone.utc)
EXTERNAL_EVIDENCE_TYPES = {
    "repository_preview_ci",
    "canonical_plugin_validator_ci",
    "main_branch_protection",
    "marketplace_resolved_commit",
    "marketplace_upgrade",
    "explicit_reinstall",
    "fresh_task_discovery",
    "rollback",
}
# Repository-authored envelopes prove integrity but cannot authenticate their
# provider origin. Add an adapter only with a verifier that checks evidence
# outside the record being validated.
SUPPORTED_AUTHENTICATED_EXTERNAL_EVIDENCE_ADAPTERS: frozenset[str] = frozenset()
SUPPORTED_PREVIEW_EXTERNAL_EVIDENCE_ADAPTERS: frozenset[str] = frozenset(
    {"github_release_asset_preview_v1"}
)
LiveEvidenceVerifier = Callable[..., dict[str, Any]]
OPENAI_NATIVE_SKILLS = {
    "research-polisher-methodology-publishability-reviewer",
    "research-polisher-orchestrator",
    "research-polisher-plan-assembler",
    "research-polisher-strategy-reviewer",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def normalized_utc_now(value: datetime | None = None) -> datetime:
    now = datetime.now(timezone.utc) if value is None else value
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("validation clock must be timezone-aware")
    return now.astimezone(timezone.utc)


def parse_aware_iso_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def validate_live_verifier_timestamp(
    value: Any,
    label: str,
    errors: list[str],
    *,
    now: datetime | None = None,
) -> None:
    verified_at = parse_aware_iso_timestamp(value)
    require(
        verified_at is not None,
        f"{label} live verifier verified_at is not a timezone-aware ISO timestamp",
        errors,
    )
    if verified_at is None:
        return
    current = normalized_utc_now(now)
    require(
        verified_at <= current + LIVE_VERIFIER_MAX_FUTURE_SKEW,
        f"{label} live verifier verified_at is more than 5 minutes in the future",
        errors,
    )
    require(
        verified_at >= current - LIVE_VERIFIER_MAX_AGE,
        f"{label} live verifier verified_at is older than 90 days",
        errors,
    )


def registered_adapter_verifier_digest(
    adapter_id: str,
    label: str,
    errors: list[str],
) -> str | None:
    """Read the repository-controlled adapter digest used by the live gate.

    The registry is part of the committed validation-contract tree. The Phase 8
    production verifier first uses the source commit to ``git show`` and bind
    its committed code; this ledger layer then requires its result to repeat the
    verifier digest from the same repository-controlled registry. Runtime output
    cannot choose or override its own accepted code digest.
    """

    try:
        registry = yaml.safe_load(
            PROVIDER_VERIFIER_REGISTRY_PATH.read_text(encoding="utf-8-sig")
        )
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        require(
            False,
            f"{label} committed provider verifier registry cannot be read: {type(exc).__name__}",
            errors,
        )
        return None
    adapters = registry.get("adapters", []) if isinstance(registry, dict) else []
    matches = [
        item
        for item in adapters
        if isinstance(item, dict)
        and item.get("adapter_id") == adapter_id
        and item.get("enabled") is True
    ]
    require(
        len(matches) == 1,
        f"{label} live verifier adapter is not uniquely enabled in the committed provider verifier registry",
        errors,
    )
    if len(matches) != 1:
        return None
    declared = matches[0].get("verifier_digest")
    if not (
        isinstance(declared, str)
        and declared.startswith("sha256:")
        and SHA256_RE.fullmatch(declared.removeprefix("sha256:"))
    ):
        require(
            False,
            f"{label} committed provider verifier registry digest is invalid",
            errors,
        )
        return None
    return declared.removeprefix("sha256:")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_payload(record: dict[str, Any]) -> dict[str, Any]:
    """Return every externally asserted field that a durable export must bind."""

    return {
        key: value
        for key, value in record.items()
        if key not in EVIDENCE_META_FIELDS
    }


def cache_identity_payload(cache_artifact: dict[str, Any]) -> dict[str, Any]:
    """Return the content identity of one installed cache, excluding its location."""

    return {
        key: cache_artifact.get(key)
        for key in (
            "plugin_version",
            "source_commit",
            "manifest_sha256",
            "registry_sha256",
            "skill_tree_algorithm",
            "skill_tree_file_count",
            "skill_tree_sha256",
            "license_sha256",
        )
    }


def cache_identity_sha256(cache_artifact: dict[str, Any]) -> str:
    payload = json.dumps(
        cache_identity_payload(cache_artifact),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_cache_artifact(
    release: dict[str, Any], *, cache_path: str, cache_instance_id: str
) -> dict[str, Any]:
    """Build a synthetic/provider-observed cache inventory from a release identity."""

    contracts = release.get("installable_contracts", {})
    tree = release.get("installable_skill_tree", {})
    source = release.get("source_commit", {})
    artifact = {
        "cache_path": cache_path,
        "cache_instance_id": cache_instance_id,
        "cache_identity_algorithm": CACHE_IDENTITY_ALGORITHM,
        "cache_identity_sha256": None,
        "plugin_version": release.get("version"),
        "source_commit": source.get("sha") if isinstance(source, dict) else None,
        "manifest_sha256": contracts.get("manifest_sha256"),
        "registry_sha256": contracts.get("registry_sha256"),
        "skill_tree_algorithm": tree.get("algorithm"),
        "skill_tree_file_count": tree.get("file_count"),
        "skill_tree_sha256": tree.get("sha256"),
        "license_sha256": contracts.get("license_sha256"),
    }
    artifact["cache_identity_sha256"] = cache_identity_sha256(artifact)
    return artifact


def validate_cache_artifact(
    artifact: Any,
    expected_release: dict[str, Any] | None,
    label: str,
    errors: list[str],
) -> None:
    """Validate one provider-exported cache inventory and optional release binding."""

    require(isinstance(artifact, dict), f"{label} cache artifact is not an object", errors)
    if not isinstance(artifact, dict):
        return
    require(
        set(artifact) == CACHE_ARTIFACT_FIELDS,
        f"{label} cache artifact fields are incomplete or undeclared",
        errors,
    )
    for field in ("cache_path", "cache_instance_id"):
        require(
            isinstance(artifact.get(field), str) and bool(artifact[field].strip()),
            f"{label} {field} is missing",
            errors,
        )
    require(
        artifact.get("cache_identity_algorithm") == CACHE_IDENTITY_ALGORITHM,
        f"{label} cache identity algorithm mismatch",
        errors,
    )
    require(
        artifact.get("cache_identity_sha256") == cache_identity_sha256(artifact),
        f"{label} cache identity digest mismatch",
        errors,
    )
    require(
        isinstance(artifact.get("skill_tree_file_count"), int)
        and artifact["skill_tree_file_count"] > 0,
        f"{label} cache skill-tree file count is invalid",
        errors,
    )
    for field in (
        "source_commit",
        "manifest_sha256",
        "registry_sha256",
        "skill_tree_sha256",
        "license_sha256",
    ):
        pattern = COMMIT_SHA_RE if field == "source_commit" else SHA256_RE
        require(
            bool(pattern.fullmatch(str(artifact.get(field, "")))),
            f"{label} {field} format is invalid",
            errors,
        )
    if expected_release is None:
        return
    expected = build_cache_artifact(
        expected_release,
        cache_path=str(artifact.get("cache_path", "")),
        cache_instance_id=str(artifact.get("cache_instance_id", "")),
    )
    require(
        artifact == expected,
        f"{label} cache content does not match the bound release identity",
        errors,
    )


def cache_inventory_for_evidence(
    record: dict[str, Any], evidence_type: str
) -> list[Any] | None:
    if evidence_type in {"marketplace_upgrade", "explicit_reinstall", "fresh_task_discovery"}:
        return [record.get("cache_artifact")]
    if evidence_type == "rollback":
        return [
            record.get("candidate_cache_artifact"),
            record.get("restored_cache_artifact"),
        ]
    return None


def authenticated_external_evidence_adapter_available(release: Any) -> bool:
    if not isinstance(release, dict):
        return False
    trust = release.get("external_evidence_trust", {})
    if not isinstance(trust, dict):
        return False
    adapter_id = trust.get("adapter_id")
    return (
        trust.get("adapter_status") == "configured"
        and trust.get("verification_level") == PROVIDER_VERIFIED
        and trust.get("provider_authenticated") is True
        and isinstance(adapter_id, str)
        and adapter_id in SUPPORTED_AUTHENTICATED_EXTERNAL_EVIDENCE_ADAPTERS
    )


def preview_external_evidence_adapter_available(release: Any) -> bool:
    if not isinstance(release, dict):
        return False
    trust = release.get("external_evidence_trust", {})
    if not isinstance(trust, dict):
        return False
    adapter_id = trust.get("adapter_id")
    return (
        trust.get("adapter_status") == "configured"
        and trust.get("verification_level") == PREVIEW_ATTESTED
        and trust.get("provider_authenticated") is False
        and isinstance(adapter_id, str)
        and adapter_id in SUPPORTED_PREVIEW_EXTERNAL_EVIDENCE_ADAPTERS
    )


def configured_external_evidence_level(release: Any) -> str | None:
    if authenticated_external_evidence_adapter_available(release):
        return PROVIDER_VERIFIED
    if preview_external_evidence_adapter_available(release):
        return PREVIEW_ATTESTED
    return None


def resolve_repository_evidence_path(value: Any) -> Path | None:
    """Resolve a canonical repository-relative evidence path without escapes."""

    if not isinstance(value, str) or not value.strip() or "\\" in value:
        return None
    relative = PurePosixPath(value)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts or "." in relative.parts:
        return None
    candidate = (REPO / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(REPO.resolve())
    except ValueError:
        return None
    return candidate


def load_structured_evidence(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8-sig")
        if path.suffix.lower() == ".json":
            return json.loads(text)
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(text)
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError):
        return None
    return None


def validate_external_evidence_locator(
    locator: Any, label: str, errors: list[str]
) -> None:
    """Validate an immutable external Release/run/asset locator.

    A locator deliberately contains no local path. Its assets must be fetched
    again by the registered live verifier before an accepted status can count.
    """

    require(isinstance(locator, dict), f"{label} external evidence locator is missing", errors)
    if not isinstance(locator, dict):
        return
    required = {
        "repository",
        "release_id",
        "release_tag",
        "capture_workflow_run_id",
        "verifier_workflow_run_id",
        "verifier_run_url",
        "envelope_asset",
        "release_asset_index_asset",
        "raw_export_asset",
        "verifier_report_asset",
    }
    require(set(locator) == required, f"{label} external evidence locator fields are incomplete or undeclared", errors)
    require(
        bool(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", str(locator.get("repository", "")))),
        f"{label} locator repository is invalid",
        errors,
    )
    for field in ("release_id", "capture_workflow_run_id", "verifier_workflow_run_id"):
        require(
            isinstance(locator.get(field), int)
            and not isinstance(locator.get(field), bool)
            and locator[field] > 0,
            f"{label} locator {field} is invalid",
            errors,
        )
    require(
        isinstance(locator.get("release_tag"), str)
        and bool(locator["release_tag"].strip()),
        f"{label} locator release_tag is invalid",
        errors,
    )
    require(
        isinstance(locator.get("verifier_run_url"), str)
        and locator["verifier_run_url"].startswith("https://"),
        f"{label} locator verifier_run_url is invalid",
        errors,
    )
    asset_fields = {
        "envelope_asset",
        "release_asset_index_asset",
        "raw_export_asset",
        "verifier_report_asset",
    }
    asset_ids: set[int] = set()
    asset_names: set[str] = set()
    for field in sorted(asset_fields):
        asset = locator.get(field)
        require(isinstance(asset, dict), f"{label} locator {field} is missing", errors)
        if not isinstance(asset, dict):
            continue
        require(
            set(asset) == {"asset_id", "name", "sha256"},
            f"{label} locator {field} fields are incomplete or undeclared",
            errors,
        )
        asset_id = asset.get("asset_id")
        name = asset.get("name")
        require(
            isinstance(asset_id, int)
            and not isinstance(asset_id, bool)
            and asset_id > 0,
            f"{label} locator {field} asset_id is invalid",
            errors,
        )
        require(
            isinstance(name, str)
            and bool(name.strip())
            and "/" not in name
            and "\\" not in name,
            f"{label} locator {field} name is invalid",
            errors,
        )
        require(
            bool(SHA256_RE.fullmatch(str(asset.get("sha256", "")))),
            f"{label} locator {field} digest is invalid",
            errors,
        )
        if isinstance(asset_id, int):
            require(asset_id not in asset_ids, f"{label} locator asset ids are not unique", errors)
            asset_ids.add(asset_id)
        if isinstance(name, str):
            require(name not in asset_names, f"{label} locator asset names are not unique", errors)
            asset_names.add(name)


def validate_bound_external_evidence(
    record: Any,
    evidence_type: str,
    label: str,
    errors: list[str],
    *,
    authenticated_external_adapter: bool = False,
    synthetic_external_trust_override: bool = False,
    expected_source_identity: dict[str, Any] | None = None,
    expected_adapter_id: str | None = None,
    live_evidence_verifier: LiveEvidenceVerifier | None = None,
    defer_live_external_requery: bool = False,
    validation_now: datetime | None = None,
) -> None:
    """Bind an accepted record to a shared, externally witnessed evidence bundle."""

    if not isinstance(record, dict) or record.get("status") == "pending":
        return
    require(evidence_type in EXTERNAL_EVIDENCE_TYPES, f"{label} uses unknown evidence type", errors)

    # Preserve old synthetic mutation fixtures without allowing legacy `verified`
    # records to count as Preview or provider evidence.
    if record.get("status") == "verified" and synthetic_external_trust_override:
        evidence_path = resolve_repository_evidence_path(record.get("evidence_path"))
        require(evidence_path is not None, f"{label} verified without a safe evidence_path", errors)
        require(
            bool(SHA256_RE.fullmatch(str(record.get("evidence_sha256", "")))),
            f"{label} verified without a valid evidence_sha256",
            errors,
        )
        if evidence_path is None or not evidence_path.is_file():
            require(False, f"{label} evidence file does not exist", errors)
            return
        require(
            record.get("evidence_sha256")
            == hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
            f"{label} evidence digest does not match the actual file",
            errors,
        )
        document = load_structured_evidence(evidence_path)
        require(isinstance(document, dict), f"{label} evidence file is not JSON/YAML object", errors)
        if not isinstance(document, dict):
            return
        require(document.get("schema_version") == 1, f"{label} evidence schema_version is not 1", errors)
        require(document.get("evidence_type") == evidence_type, f"{label} evidence_type mismatch", errors)
        require(isinstance(document.get("raw_export"), dict), f"{label} raw provider export is missing", errors)
        require(document.get("observed") == evidence_payload(record), f"{label} evidence observed payload does not match the ledger record", errors)
        expected_cache_inventory = cache_inventory_for_evidence(record, evidence_type)
        if expected_cache_inventory is not None:
            raw_export = document.get("raw_export", {})
            require(raw_export.get("cache_inventory_complete") is True, f"{label} provider export does not attest a complete cache inventory", errors)
            require(raw_export.get("cache_inventory") == expected_cache_inventory, f"{label} provider cache inventory does not match the ledger record", errors)
        return

    status = record.get("status")
    require(
        status in EXTERNAL_ACCEPTED_STATUS,
        f"{label} has invalid external evidence status: {status}",
        errors,
    )
    if status not in EXTERNAL_ACCEPTED_STATUS:
        return

    # Provider status is a separate trust tier. A provider-looking Release
    # asset or envelope boolean is never enough; only a registered authenticated
    # provider adapter can enable it. The allowlist is intentionally empty.
    if status == PROVIDER_VERIFIED:
        require(
            authenticated_external_adapter
            and isinstance(expected_adapter_id, str)
            and expected_adapter_id
            in SUPPORTED_AUTHENTICATED_EXTERNAL_EVIDENCE_ADAPTERS,
            f"{label} provider_verified without a registered authenticated provider adapter",
            errors,
        )
        if not authenticated_external_adapter:
            return
    else:
        require(
            isinstance(expected_adapter_id, str)
            and expected_adapter_id in SUPPORTED_PREVIEW_EXTERNAL_EVIDENCE_ADAPTERS,
            f"{label} preview_attested without a registered live-requery verifier",
            errors,
        )

    require(
        expected_source_identity is not None,
        f"{label} accepted without a release source identity",
        errors,
    )
    require(
        record.get("evidence_path") in (None, "")
        and record.get("evidence_sha256") in (None, ""),
        f"{label} repository-relative evidence cannot establish external acceptance",
        errors,
    )
    locator = record.get("evidence_locator")
    validate_external_evidence_locator(locator, label, errors)
    if not isinstance(locator, dict) or expected_source_identity is None:
        return
    expected_adapter_code_sha256 = registered_adapter_verifier_digest(
        expected_adapter_id,
        label,
        errors,
    )
    if expected_adapter_code_sha256 is None:
        return
    if defer_live_external_requery:
        require(
            live_evidence_verifier is None,
            f"{label} structural-only validation cannot ignore a supplied live verifier",
            errors,
        )
        return
    require(
        callable(live_evidence_verifier),
        f"{label} accepted without a live external re-query verifier",
        errors,
    )
    if not callable(live_evidence_verifier):
        return
    require(
        getattr(live_evidence_verifier, "adapter_id", None) == expected_adapter_id,
        f"{label} live verifier is not registered for the configured adapter id",
        errors,
    )
    if getattr(live_evidence_verifier, "adapter_id", None) != expected_adapter_id:
        return
    try:
        result_document = live_evidence_verifier(
            evidence_locator=copy.deepcopy(locator),
            evidence_type=evidence_type,
            expected_source_identity=copy.deepcopy(expected_source_identity),
            expected_adapter_id=expected_adapter_id,
            expected_verification_level=status,
        )
    except Exception as exc:
        require(
            False,
            f"{label} live external re-query failed: {type(exc).__name__}: {exc}",
            errors,
        )
        return
    require(
        isinstance(result_document, dict),
        f"{label} live verifier result is not an object",
        errors,
    )
    if not isinstance(result_document, dict):
        return

    require(
        result_document.get("schema_version") == 3,
        f"{label} live verifier result schema_version is not 3",
        errors,
    )
    require(
        result_document.get("evidence_type") == evidence_type,
        f"{label} live verifier evidence_type mismatch",
        errors,
    )
    require(
        result_document.get("verification_level") == status,
        f"{label} live verifier level differs from record status",
        errors,
    )
    require(
        result_document.get("provider_verified") is (status == PROVIDER_VERIFIED),
        f"{label} live verifier provider flag conflicts with status",
        errors,
    )
    require(
        result_document.get("locator") == locator,
        f"{label} live verifier locator differs from the ledger locator",
        errors,
    )
    require(
        result_document.get("source_identity") == expected_source_identity,
        f"{label} live verifier source identity mismatch",
        errors,
    )
    require(
        result_document.get("observed") == evidence_payload(record),
        f"{label} live verifier observed payload does not match the ledger record",
        errors,
    )

    integrity = result_document.get("integrity_result")
    require(isinstance(integrity, dict), f"{label} integrity result is missing", errors)
    if isinstance(integrity, dict):
        require(
            isinstance(integrity.get("evidence_id"), str)
            and bool(integrity["evidence_id"].strip()),
            f"{label} integrity result evidence_id is empty",
            errors,
        )
        require(integrity.get("integrity_valid") is True, f"{label} bundle integrity was not validated", errors)
        require(
            integrity.get("gate_eligible") is False,
            f"{label} shared integrity validator incorrectly claimed gate eligibility",
            errors,
        )
        require(
            integrity.get("claimed_verification_level") == status,
            f"{label} envelope claimed level differs from status",
            errors,
        )
        require(
            integrity.get("claimed_provider_verified") is (status == PROVIDER_VERIFIED),
            f"{label} envelope provider claim conflicts with status",
            errors,
        )
        require(
            integrity.get("claimed_counts_as_preview_acceptance") is True,
            f"{label} envelope does not claim Preview acceptance",
            errors,
        )
        require(
            integrity.get("source_identity_bound") is True,
            f"{label} shared integrity result did not bind source identity",
            errors,
        )
        require(
            integrity.get("raw_export_asset_id")
            == locator.get("raw_export_asset", {}).get("asset_id"),
            f"{label} raw export asset id differs from the locator",
            errors,
        )
        require(
            str(integrity.get("raw_export_sha256", "")).removeprefix("sha256:")
            == locator.get("raw_export_asset", {}).get("sha256"),
            f"{label} raw export digest differs from the locator",
            errors,
        )
        require(
            str(integrity.get("envelope_sha256", "")).removeprefix("sha256:")
            == locator.get("envelope_asset", {}).get("sha256"),
            f"{label} envelope digest differs from the locator",
            errors,
        )
        require(
            integrity.get("verifier_report_asset_id")
            == locator.get("verifier_report_asset", {}).get("asset_id"),
            f"{label} verifier report asset id differs from the locator",
            errors,
        )
        require(
            str(integrity.get("verifier_report_sha256", "")).removeprefix("sha256:")
            == locator.get("verifier_report_asset", {}).get("sha256"),
            f"{label} verifier report digest differs from the locator",
            errors,
        )
        require(
            str(integrity.get("release_asset_index_sha256", "")).removeprefix("sha256:")
            == locator.get("release_asset_index_asset", {}).get("sha256"),
            f"{label} Release asset index digest differs from the locator",
            errors,
        )

    verifier = result_document.get("live_verifier")
    require(isinstance(verifier, dict), f"{label} live verifier metadata is missing", errors)
    if isinstance(verifier, dict):
        require(verifier.get("adapter_id") == expected_adapter_id, f"{label} live verifier adapter mismatch", errors)
        require(verifier.get("live_requery_performed") is True, f"{label} verifier did not perform a live re-query", errors)
        require(verifier.get("requery_source") == "github_api", f"{label} verifier did not query the GitHub API", errors)
        require(verifier.get("independent") is True, f"{label} live verifier is not independent", errors)
        require(
            verifier.get("verifier_workflow_run_id") == locator.get("verifier_workflow_run_id")
            and verifier.get("verifier_run_url") == locator.get("verifier_run_url"),
            f"{label} verifier workflow witness differs from the locator",
            errors,
        )
        require(
            verifier.get("adapter_code_sha256") == expected_adapter_code_sha256,
            f"{label} verifier code digest differs from the committed provider verifier registry",
            errors,
        )
        validate_live_verifier_timestamp(
            verifier.get("verified_at"),
            label,
            errors,
            now=validation_now,
        )

    gate = result_document.get("gate_eligibility")
    require(isinstance(gate, dict), f"{label} gate eligibility result is missing", errors)
    if isinstance(gate, dict):
        require(gate.get("eligible") is True, f"{label} external verifier did not mark the record eligible", errors)
        require(gate.get("level") == status, f"{label} gate eligibility level differs from status", errors)
        require(
            gate.get("determined_by") == "registered_live_verifier",
            f"{label} gate eligibility was not determined by the registered live verifier",
            errors,
        )
        if status == PREVIEW_ATTESTED:
            require(gate.get("provider_adapter_id") is None, f"{label} Preview evidence claims a provider adapter", errors)
            require(gate.get("provider_authenticated") is False, f"{label} Preview evidence claims provider authentication", errors)
        else:
            require(
                gate.get("provider_authenticated") is True
                and gate.get("provider_adapter_id") in SUPPORTED_AUTHENTICATED_EXTERNAL_EVIDENCE_ADAPTERS,
                f"{label} provider eligibility lacks a registered authenticated adapter",
                errors,
            )

    raw_export = result_document.get("raw_export")
    require(isinstance(raw_export, dict), f"{label} raw export is not machine-readable JSON", errors)
    if not isinstance(raw_export, dict):
        return
    require(raw_export.get("evidence_type") == evidence_type, f"{label} raw export evidence_type mismatch", errors)
    require(raw_export.get("observed") == evidence_payload(record), f"{label} raw export observed payload mismatch", errors)
    expected_cache_inventory = cache_inventory_for_evidence(record, evidence_type)
    if expected_cache_inventory is not None:
        require(raw_export.get("cache_inventory_complete") is True, f"{label} raw export does not attest a complete cache inventory", errors)
        require(raw_export.get("cache_inventory") == expected_cache_inventory, f"{label} raw export cache inventory does not match the ledger record", errors)


def git_bytes(*args: str) -> tuple[int, bytes, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr.decode("utf-8", errors="replace")


def git_blob(commit_sha: str, path: str) -> bytes | None:
    returncode, stdout, _ = git_bytes("show", f"{commit_sha}:{path}")
    return stdout if returncode == 0 else None


def committed_skill_tree_digest(commit_sha: str) -> tuple[int, str] | None:
    prefix = "research-skills-openai/skills/"
    returncode, output, _ = git_bytes(
        "ls-tree", "-r", "--name-only", "-z", commit_sha, "--", prefix
    )
    if returncode != 0:
        return None
    paths = sorted(
        item.decode("utf-8")
        for item in output.split(b"\0")
        if item
    )
    digest = hashlib.sha256()
    for full_path in paths:
        blob = git_blob(commit_sha, full_path)
        if blob is None:
            return None
        relative = full_path.removeprefix(prefix)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(blob.replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return len(paths), digest.hexdigest()


def is_validation_contract_path(path: str) -> bool:
    selected = (
        (path.startswith("scripts/") and path.count("/") == 1 and path.endswith(".py"))
        or any(path == root or path.startswith(f"{root}/") for root in VALIDATION_TEST_ROOTS)
        or path in VALIDATION_CONTRACT_FILES
    )
    return (
        selected
        and path not in MUTABLE_RUNTIME_EVIDENCE_FILES
        and not any(path.startswith(prefix) for prefix in MUTABLE_RUNTIME_EVIDENCE_PREFIXES)
    )


def committed_validation_contract_digest(commit_sha: str) -> tuple[int, str] | None:
    roots = ["scripts", *VALIDATION_TEST_ROOTS, *VALIDATION_CONTRACT_FILES]
    returncode, output, _ = git_bytes(
        "ls-tree", "-r", "--name-only", "-z", commit_sha, "--", *roots
    )
    if returncode != 0:
        return None
    paths = sorted(
        path
        for item in output.split(b"\0")
        if item
        for path in [item.decode("utf-8")]
        if is_validation_contract_path(path)
    )
    digest = hashlib.sha256()
    for path in paths:
        blob = git_blob(commit_sha, path)
        if blob is None:
            return None
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(blob.replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return len(paths), digest.hexdigest()


def validate_verified_source_commit_tree(
    release: Any,
    errors: list[str],
    label: str = "release",
) -> None:
    """Bind a verified release identity to an existing immutable Git commit tree."""

    if not isinstance(release, dict):
        return
    source = release.get("source_commit", {})
    if not isinstance(source, dict) or source.get("status") != "verified":
        return
    commit_sha = source.get("sha")
    if not isinstance(commit_sha, str) or not COMMIT_SHA_RE.fullmatch(commit_sha):
        return
    returncode, _, _ = git_bytes("cat-file", "-e", f"{commit_sha}^{{commit}}")
    require(returncode == 0, f"{label} verified source commit does not exist in local Git history", errors)
    if returncode != 0:
        return

    committed_tree = committed_skill_tree_digest(commit_sha)
    expected_tree = release.get("installable_skill_tree", {})
    require(committed_tree is not None, f"{label} committed skill tree cannot be read", errors)
    if committed_tree is not None:
        require(
            committed_tree == (expected_tree.get("file_count"), expected_tree.get("sha256")),
            f"{label} committed skill tree differs from the ledger identity",
            errors,
        )

    committed_validation = committed_validation_contract_digest(commit_sha)
    expected_validation = release.get("validation_contract_tree", {})
    require(
        committed_validation is not None,
        f"{label} committed validation-contract tree cannot be read",
        errors,
    )
    if committed_validation is not None:
        require(
            committed_validation
            == (
                expected_validation.get("file_count"),
                expected_validation.get("sha256"),
            ),
            f"{label} committed validation-contract tree differs from the ledger identity",
            errors,
        )

    contracts = release.get("installable_contracts", {})
    contract_paths = {
        "manifest_sha256": "research-skills-openai/.codex-plugin/plugin.json",
        "registry_sha256": "research-skills-openai/workflow-registry.yaml",
        "license_sha256": "research-skills-openai/LICENSE",
        "provenance_sha256": "research-skills-openai/PROVENANCE.yaml",
    }
    committed_documents: dict[str, bytes] = {}
    for field, path in contract_paths.items():
        blob = git_blob(commit_sha, path)
        require(blob is not None, f"{label} committed {path} is missing", errors)
        if blob is None:
            continue
        committed_documents[path] = blob
        digest = hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest()
        require(digest == contracts.get(field), f"{label} committed {field} mismatch", errors)

    manifest_path = "research-skills-openai/.codex-plugin/plugin.json"
    registry_path = "research-skills-openai/workflow-registry.yaml"
    try:
        committed_manifest = json.loads(committed_documents[manifest_path].decode("utf-8-sig"))
        committed_registry = yaml.safe_load(committed_documents[registry_path].decode("utf-8-sig"))
    except (KeyError, UnicodeError, json.JSONDecodeError, yaml.YAMLError):
        require(False, f"{label} committed manifest or registry cannot be parsed", errors)
    else:
        require(committed_manifest.get("version") == release.get("version"), f"{label} committed version mismatch", errors)
        require(
            committed_registry.get("plugin_version") == release.get("version"),
            f"{label} committed registry version mismatch",
            errors,
        )
        require(
            committed_registry.get("schema_version") == contracts.get("registry_schema_version"),
            f"{label} committed registry schema mismatch",
            errors,
        )

    marketplace_blob = git_blob(commit_sha, ".agents/plugins/marketplace.json")
    require(marketplace_blob is not None, f"{label} committed marketplace is missing", errors)
    if marketplace_blob is not None:
        try:
            marketplace = json.loads(marketplace_blob.decode("utf-8-sig"))
            matches = [
                item
                for item in marketplace.get("plugins", [])
                if item.get("name") == "research-skills-openai"
            ]
        except (UnicodeError, json.JSONDecodeError):
            matches = []
        require(len(matches) == 1, f"{label} committed marketplace entry is invalid", errors)
        if len(matches) == 1:
            recorded = release.get("marketplace_source", {})
            expected = {
                "source": recorded.get("source"),
                "url": recorded.get("url"),
                "path": recorded.get("path"),
                "ref": recorded.get("ref"),
            }
            require(matches[0].get("source") == expected, f"{label} committed marketplace source mismatch", errors)


def validate_validation_contract_tree_record(
    release: Any, errors: list[str]
) -> None:
    if not isinstance(release, dict):
        require(False, "release is not an object", errors)
        return
    validation_file_count, validation_digest = normalized_validation_contract_digest()
    validation_tree = release.get("validation_contract_tree", {})
    require(
        validation_tree.get("algorithm") == VALIDATION_TREE_ALGORITHM,
        "ledger validation-contract algorithm mismatch",
        errors,
    )
    require(
        validation_tree.get("file_count") == validation_file_count,
        "ledger validation-contract file count is stale",
        errors,
    )
    require(
        validation_tree.get("sha256") == validation_digest,
        "ledger validation-contract digest is stale",
        errors,
    )
    require(
        validation_tree.get("mutable_runtime_evidence_excluded")
        == [
            *sorted(MUTABLE_RUNTIME_EVIDENCE_FILES),
            *sorted(f"{prefix}**" for prefix in MUTABLE_RUNTIME_EVIDENCE_PREFIXES),
        ],
        "ledger validation-contract mutable-evidence exclusions are stale",
        errors,
    )


def validate_status_record(
    record: Any,
    label: str,
    errors: list[str],
    verified_fields: tuple[str, ...] = (),
    *,
    external: bool = False,
    allow_legacy_synthetic_verified: bool = False,
) -> None:
    require(isinstance(record, dict), f"{label} is not an object", errors)
    if not isinstance(record, dict):
        return
    status = record.get("status")
    valid_status = EXTERNAL_VALID_STATUS if external else INTERNAL_VALID_STATUS
    if external and allow_legacy_synthetic_verified:
        valid_status = {*valid_status, "verified"}
    require(status in valid_status, f"{label} has invalid status: {status}", errors)
    if status == "pending":
        require(bool(record.get("reason")), f"{label} pending status lacks a reason", errors)
    elif status in {"verified", *EXTERNAL_ACCEPTED_STATUS}:
        for field in verified_fields:
            require(record.get(field) not in (None, ""), f"{label} accepted without {field}", errors)


def validate_all_sha_fields(value: Any, label: str, errors: list[str]) -> None:
    """Validate every known SHA-bearing scalar, including pending evidence."""
    if isinstance(value, list):
        for index, item in enumerate(value):
            validate_all_sha_fields(item, f"{label}[{index}]", errors)
        return
    if not isinstance(value, dict):
        return
    for key, item in value.items():
        field_label = f"{label}.{key}" if label else key
        if item not in (None, "") and not isinstance(item, (dict, list)):
            if key == "sha256" or key.endswith("_sha256"):
                require(
                    bool(SHA256_RE.fullmatch(str(item))),
                    f"{field_label} is not a lowercase 64-character SHA-256",
                    errors,
                )
            elif key == "sha" or key in {"commit_sha", "source_commit", "target_commit"}:
                require(
                    bool(COMMIT_SHA_RE.fullmatch(str(item))),
                    f"{field_label} is not a lowercase 40-character commit SHA",
                    errors,
                )
        validate_all_sha_fields(item, field_label, errors)


def require_verified_commit_binding(
    record: Any,
    field: str,
    label: str,
    source_commit: Any,
    errors: list[str],
) -> None:
    if not isinstance(record, dict) or record.get("status") == "pending":
        return
    require(
        isinstance(source_commit, dict) and source_commit.get("status") == "verified",
        f"{label} is accepted while source_commit is not verified",
        errors,
    )
    expected = source_commit.get("sha") if isinstance(source_commit, dict) else None
    require(
        record.get(field) == expected,
        f"{label} commit does not match immutable source_commit",
        errors,
    )


def release_source_identity(release: dict[str, Any]) -> dict[str, Any] | None:
    source = release.get("source_commit", {})
    contracts = release.get("installable_contracts", {})
    tree = release.get("installable_skill_tree", {})
    if not (
        isinstance(source, dict)
        and source.get("status") == "verified"
        and COMMIT_SHA_RE.fullmatch(str(source.get("sha", "")))
    ):
        return None
    fields = {
        "plugin_version": release.get("version"),
        "source_commit": source.get("sha"),
        "manifest_sha256": contracts.get("manifest_sha256"),
        "registry_sha256": contracts.get("registry_sha256"),
        "skill_tree_sha256": tree.get("sha256"),
    }
    if not (
        isinstance(fields["plugin_version"], str)
        and parse_semver(fields["plugin_version"]) is not None
        and all(
            SHA256_RE.fullmatch(str(fields[field] or ""))
            for field in (
                "manifest_sha256",
                "registry_sha256",
                "skill_tree_sha256",
            )
        )
    ):
        return None
    return fields


def validate_release_evidence(
    release: dict[str, Any],
    current_version: str,
    expected_skill_count: int | None,
    errors: list[str],
    prefix: str = "",
    *,
    authenticated_external_adapter: bool = False,
    synthetic_external_trust_override: bool = False,
    expected_explicit_entries: list[str] | None = None,
    expected_implicit_entries: list[str] | None = None,
    live_evidence_verifier: LiveEvidenceVerifier | None = None,
    defer_live_external_requery: bool = False,
    validation_now: datetime | None = None,
) -> None:
    def named(label: str) -> str:
        return f"{prefix}{label}"

    def is_external_accepted(record: Any) -> bool:
        return isinstance(record, dict) and (
            record.get("status") in EXTERNAL_ACCEPTED_STATUS
            or (
                synthetic_external_trust_override
                and record.get("status") == "verified"
            )
        )

    trust = release.get("external_evidence_trust", {})
    expected_source_identity = release_source_identity(release)
    expected_adapter_id = trust.get("adapter_id") if isinstance(trust, dict) else None

    def validate_external(record: Any, evidence_type: str, label: str) -> None:
        if isinstance(record, dict) and record.get("status") in EXTERNAL_ACCEPTED_STATUS:
            require(
                record.get("status") == trust.get("verification_level"),
                f"{label} status differs from release verification level",
                errors,
            )
        validate_bound_external_evidence(
            record,
            evidence_type,
            label,
            errors,
            authenticated_external_adapter=authenticated_external_adapter,
            synthetic_external_trust_override=synthetic_external_trust_override,
            expected_source_identity=expected_source_identity,
            expected_adapter_id=expected_adapter_id,
            live_evidence_verifier=live_evidence_verifier,
            defer_live_external_requery=defer_live_external_requery,
            validation_now=validation_now,
        )

    require(isinstance(trust, dict), named("external evidence trust is not an object"), errors)
    if isinstance(trust, dict):
        require(
            trust.get("adapter_status") in {"unavailable", "configured"},
            named("external evidence trust adapter_status is invalid"),
            errors,
        )
        require(
            trust.get("verification_level") in {
                None,
                PREVIEW_ATTESTED,
                PROVIDER_VERIFIED,
            },
            named("external evidence trust verification_level is invalid"),
            errors,
        )
        require(
            isinstance(trust.get("reason"), str) and bool(trust["reason"].strip()),
            named("external evidence trust reason is missing"),
            errors,
        )
        if trust.get("adapter_status") == "unavailable":
            require(trust.get("adapter_id") is None, named("unavailable external adapter has an id"), errors)
            require(trust.get("verification_level") is None, named("unavailable external adapter has a verification level"), errors)
            require(
                trust.get("provider_authenticated") is False,
                named("unavailable external adapter claims provider authentication"),
                errors,
            )
        else:
            require(
                configured_external_evidence_level(release) is not None,
                named("configured external adapter is not supported by the validator"),
                errors,
            )
    if not synthetic_external_trust_override:
        require(
            authenticated_external_adapter
            == authenticated_external_evidence_adapter_available(release),
            named("external adapter validation state was injected rather than derived"),
            errors,
        )

    source_commit = release.get("source_commit")
    validate_status_record(source_commit, named("source_commit"), errors, ("sha",))

    marketplace_source = release.get("marketplace_source", {})
    resolved_commit = marketplace_source.get("resolved_commit") if isinstance(marketplace_source, dict) else None
    validate_status_record(
        resolved_commit,
        named("marketplace_resolved_commit"),
        errors,
        ("sha",),
        external=True,
        allow_legacy_synthetic_verified=synthetic_external_trust_override,
    )
    require_verified_commit_binding(
        resolved_commit,
        "sha",
        named("marketplace_resolved_commit"),
        source_commit,
        errors,
    )
    validate_external(
        resolved_commit,
        "marketplace_resolved_commit",
        named("marketplace_resolved_commit"),
    )

    ci = release.get("ci", {})
    repository_ci = ci.get("repository_preview") if isinstance(ci, dict) else None
    validate_status_record(
        repository_ci,
        named("repository_preview CI"),
        errors,
        ("run_id", "run_url", "commit_sha", "conclusion"),
        external=True,
        allow_legacy_synthetic_verified=synthetic_external_trust_override,
    )
    if is_external_accepted(repository_ci):
        require(repository_ci.get("conclusion") == "success", named("repository CI conclusion is not success"), errors)
    require_verified_commit_binding(
        repository_ci,
        "commit_sha",
        named("repository_preview CI"),
        source_commit,
        errors,
    )
    validate_external(
        repository_ci,
        "repository_preview_ci",
        named("repository_preview CI"),
    )

    canonical = ci.get("canonical_plugin_validator", {}) if isinstance(ci, dict) else {}
    local_canonical = canonical.get("local") if isinstance(canonical, dict) else None
    validate_status_record(
        local_canonical,
        named("local canonical validator"),
        errors,
        ("command", "validator_source", "result", "verified_on"),
    )
    if isinstance(local_canonical, dict) and local_canonical.get("status") == "verified":
        require(local_canonical.get("result") == "passed", named("local canonical validator result is not passed"), errors)
        require(
            bool(DATE_RE.fullmatch(str(local_canonical.get("verified_on", "")))),
            named("local canonical validator date is invalid"),
            errors,
        )
    canonical_ci = canonical.get("ci") if isinstance(canonical, dict) else None
    validate_status_record(
        canonical_ci,
        named("canonical validator CI"),
        errors,
        ("run_id", "commit_sha", "conclusion"),
        external=True,
        allow_legacy_synthetic_verified=synthetic_external_trust_override,
    )
    if is_external_accepted(canonical_ci):
        require(canonical_ci.get("conclusion") == "success", named("canonical validator CI conclusion is not success"), errors)
    require_verified_commit_binding(
        canonical_ci,
        "commit_sha",
        named("canonical validator CI"),
        source_commit,
        errors,
    )
    validate_external(
        canonical_ci,
        "canonical_plugin_validator_ci",
        named("canonical validator CI"),
    )

    governance = release.get("governance", {})
    branch_protection = governance.get("main_branch_protection") if isinstance(governance, dict) else None
    validate_status_record(
        branch_protection,
        named("main branch protection"),
        errors,
        ("branch", "required_check", "verified_at"),
        external=True,
        allow_legacy_synthetic_verified=synthetic_external_trust_override,
    )
    if isinstance(branch_protection, dict):
        require(branch_protection.get("branch") == "main", named("branch protection target is not main"), errors)
        if is_external_accepted(branch_protection):
            require(
                branch_protection.get("required_check") == "OpenAI Plugin Preview / validate",
                named("branch protection required check is invalid"),
                errors,
            )
    validate_external(
        branch_protection,
        "main_branch_protection",
        named("main branch protection"),
    )

    receipts = release.get("receipts", {})
    for receipt_name in ("marketplace_upgrade", "explicit_reinstall"):
        receipt = receipts.get(receipt_name) if isinstance(receipts, dict) else None
        receipt_label = named(receipt_name)
        validate_status_record(
            receipt,
            receipt_label,
            errors,
            ("installed_version", "source_commit", "cache_path", "cache_artifact"),
            external=True,
            allow_legacy_synthetic_verified=synthetic_external_trust_override,
        )
        if is_external_accepted(receipt):
            require(receipt.get("installed_version") == current_version, f"{receipt_label} version mismatch", errors)
            cache_artifact = receipt.get("cache_artifact")
            validate_cache_artifact(cache_artifact, release, receipt_label, errors)
            if isinstance(cache_artifact, dict):
                require(
                    receipt.get("cache_path") == cache_artifact.get("cache_path"),
                    f"{receipt_label} cache_path does not match its cache artifact",
                    errors,
                )
        require_verified_commit_binding(receipt, "source_commit", receipt_label, source_commit, errors)
        validate_external(receipt, receipt_name, receipt_label)

    discovery = receipts.get("fresh_task_discovery") if isinstance(receipts, dict) else None
    discovery_label = named("fresh_task_discovery")
    validate_status_record(
        discovery,
        discovery_label,
        errors,
        (
            "plugin_version",
            "source_commit",
            "task_id",
            "installed_skill_count",
            "explicit_callable_entries",
            "implicit_prompt_entries",
            "explicit_callable_entry_skills",
            "implicit_prompt_entry_skills",
            "installed_via",
            "cache_artifact",
        ),
        external=True,
        allow_legacy_synthetic_verified=synthetic_external_trust_override,
    )
    if is_external_accepted(discovery):
        require(discovery.get("plugin_version") == current_version, f"{discovery_label} version mismatch", errors)
        if expected_skill_count is None:
            require(
                isinstance(discovery.get("installed_skill_count"), int)
                and discovery.get("installed_skill_count") > 0,
                f"{discovery_label} skill count is invalid",
                errors,
            )
        else:
            require(
                discovery.get("installed_skill_count") == expected_skill_count,
                f"{discovery_label} skill count mismatch",
                errors,
            )
        explicit_skills = discovery.get("explicit_callable_entry_skills")
        implicit_skills = discovery.get("implicit_prompt_entry_skills")
        require(
            isinstance(explicit_skills, list)
            and len(explicit_skills) == len(set(explicit_skills))
            and all(isinstance(item, str) and item for item in explicit_skills),
            f"{discovery_label} explicit entry list is invalid",
            errors,
        )
        require(
            isinstance(implicit_skills, list)
            and len(implicit_skills) == len(set(implicit_skills))
            and all(isinstance(item, str) and item for item in implicit_skills),
            f"{discovery_label} implicit entry list is invalid",
            errors,
        )
        if isinstance(explicit_skills, list):
            require(
                discovery.get("explicit_callable_entries") == len(explicit_skills),
                f"{discovery_label} explicit entry count mismatch",
                errors,
            )
        if isinstance(implicit_skills, list):
            require(
                discovery.get("implicit_prompt_entries") == len(implicit_skills),
                f"{discovery_label} implicit entry count mismatch",
                errors,
            )
        if isinstance(explicit_skills, list) and isinstance(implicit_skills, list):
            require(
                set(implicit_skills) <= set(explicit_skills),
                f"{discovery_label} implicit entries are not explicit-callable",
                errors,
            )
        if expected_explicit_entries is not None:
            require(
                set(explicit_skills or []) == set(expected_explicit_entries),
                f"{discovery_label} explicit entry identities mismatch",
                errors,
            )
        if expected_implicit_entries is not None:
            require(
                set(implicit_skills or []) == set(expected_implicit_entries),
                f"{discovery_label} implicit entry identities mismatch",
                errors,
            )
        installed_via = discovery.get("installed_via")
        require(
            installed_via in {"marketplace_upgrade", "explicit_reinstall"},
            f"{discovery_label} installed_via is invalid",
            errors,
        )
        selected_install = (
            receipts.get(installed_via, {})
            if isinstance(receipts, dict) and isinstance(installed_via, str)
            else {}
        )
        require(
            isinstance(selected_install, dict)
            and is_external_accepted(selected_install),
            f"{discovery_label} does not reference an accepted install receipt",
            errors,
        )
        validate_cache_artifact(
            discovery.get("cache_artifact"), release, discovery_label, errors
        )
        require(
            isinstance(selected_install, dict)
            and discovery.get("cache_artifact")
            == selected_install.get("cache_artifact"),
            f"{discovery_label} cache artifact differs from the selected install receipt",
            errors,
        )
    require_verified_commit_binding(discovery, "source_commit", discovery_label, source_commit, errors)
    validate_external(
        discovery,
        "fresh_task_discovery",
        discovery_label,
    )

    rollback = receipts.get("rollback") if isinstance(receipts, dict) else None
    rollback_label = named("rollback")
    validate_status_record(
        rollback,
        rollback_label,
        errors,
        (
            "from_version",
            "to_version",
            "target_commit",
            "restored_cache_path",
            "candidate_cache_path",
            "candidate_from_receipt",
            "candidate_cache_artifact",
            "restored_cache_artifact",
            "cache_mixing_absent",
        ),
        external=True,
        allow_legacy_synthetic_verified=synthetic_external_trust_override,
    )
    if is_external_accepted(rollback):
        require(rollback.get("from_version") == current_version, f"{rollback_label} from_version mismatch", errors)
        require(rollback.get("to_version") != current_version, f"{rollback_label} did not target a previous version", errors)
        require(rollback.get("cache_mixing_absent") is True, f"{rollback_label} cache isolation not proven", errors)
        candidate_from = rollback.get("candidate_from_receipt")
        require(
            candidate_from in {"marketplace_upgrade", "explicit_reinstall"},
            f"{rollback_label} candidate_from_receipt is invalid",
            errors,
        )
        selected_install = (
            receipts.get(candidate_from, {})
            if isinstance(receipts, dict) and isinstance(candidate_from, str)
            else {}
        )
        candidate_cache = rollback.get("candidate_cache_artifact")
        restored_cache = rollback.get("restored_cache_artifact")
        validate_cache_artifact(candidate_cache, release, f"{rollback_label} candidate", errors)
        validate_cache_artifact(restored_cache, None, f"{rollback_label} restored", errors)
        require(
            isinstance(selected_install, dict)
            and is_external_accepted(selected_install)
            and candidate_cache == selected_install.get("cache_artifact"),
            f"{rollback_label} candidate cache does not match an accepted current install",
            errors,
        )
        if isinstance(candidate_cache, dict) and isinstance(restored_cache, dict):
            require(
                rollback.get("candidate_cache_path") == candidate_cache.get("cache_path")
                and rollback.get("restored_cache_path") == restored_cache.get("cache_path"),
                f"{rollback_label} cache paths do not match their inventories",
                errors,
            )
            for field in ("cache_path", "cache_instance_id", "cache_identity_sha256"):
                require(
                    candidate_cache.get(field) != restored_cache.get(field),
                    f"{rollback_label} cache mixing detected in {field}",
                    errors,
                )
            require(
                restored_cache.get("plugin_version") == rollback.get("to_version")
                and restored_cache.get("source_commit") == rollback.get("target_commit"),
                f"{rollback_label} restored cache identity does not match rollback target",
                errors,
            )
    validate_external(rollback, "rollback", rollback_label)


def validate_rollback_history_binding(
    release: dict[str, Any], previous_releases: list[Any], errors: list[str]
) -> None:
    rollback = release.get("receipts", {}).get("rollback", {})
    if not isinstance(rollback, dict) or rollback.get("status") not in {
        "verified",
        *EXTERNAL_ACCEPTED_STATUS,
    }:
        return
    target_version = rollback.get("to_version")
    target_commit = rollback.get("target_commit")
    from_version = rollback.get("from_version")
    if not isinstance(from_version, str) or not isinstance(target_version, str):
        require(False, "accepted rollback versions are invalid", errors)
    elif parse_semver(from_version) is None or parse_semver(target_version) is None:
        require(False, "accepted rollback versions are not strict SemVer", errors)
    else:
        require(
            compare_semver(target_version, from_version) < 0,
            "accepted rollback target version is not strictly older than the current version",
            errors,
        )
    matches = [
        previous
        for previous in previous_releases
        if isinstance(previous, dict) and previous.get("version") == target_version
    ]
    require(
        len(matches) == 1,
        "accepted rollback must target exactly one previous release ledger entry",
        errors,
    )
    if len(matches) != 1:
        return
    previous_source = matches[0].get("source_commit", {})
    require(
        isinstance(previous_source, dict)
        and previous_source.get("status") == "verified",
        "accepted rollback targets a previous release without a verified immutable source commit",
        errors,
    )
    require(
        isinstance(previous_source, dict)
        and previous_source.get("sha") == target_commit,
        "accepted rollback target_commit does not match the previous release source_commit",
        errors,
    )
    validate_cache_artifact(
        rollback.get("restored_cache_artifact"),
        matches[0],
        "accepted rollback restored",
        errors,
    )
    current_source = release.get("source_commit", {})
    current_commit = current_source.get("sha") if isinstance(current_source, dict) else None
    if (
        isinstance(target_commit, str)
        and COMMIT_SHA_RE.fullmatch(target_commit)
        and isinstance(current_commit, str)
        and COMMIT_SHA_RE.fullmatch(current_commit)
    ):
        returncode, _, _ = git_bytes(
            "merge-base", "--is-ancestor", target_commit, current_commit
        )
        require(
            returncode == 0,
            "accepted rollback target commit is not an ancestor of the current release commit",
            errors,
        )


def bind_fixture_evidence(
    record: dict[str, Any], evidence_type: str, path: Path
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw_export: dict[str, Any] = {"synthetic": True}
    cache_inventory = cache_inventory_for_evidence(record, evidence_type)
    if cache_inventory is not None:
        raw_export.update(
            {
                "cache_inventory_complete": True,
                "cache_inventory": cache_inventory,
            }
        )
    document = {
        "schema_version": 1,
        "evidence_type": evidence_type,
        "observed": evidence_payload(record),
        "provider": "synthetic-test-only",
        "raw_export": raw_export,
    }
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    record["evidence_path"] = path.relative_to(REPO).as_posix()
    record["evidence_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()


class SyntheticLiveVerifier:
    """In-memory stand-in for a registered workflow that re-queries GitHub.

    The ledger receives only external locators. This test adapter owns the
    fetched bytes separately, re-runs the shared integrity validator for every
    request, and then makes an independent gate decision. It intentionally does
    not read repository-relative evidence files.
    """

    adapter_id = "github_release_asset_preview_v1"

    def __init__(self) -> None:
        self.bundles: dict[str, dict[str, Any]] = {}
        registry_errors: list[str] = []
        self.adapter_code_sha256 = registered_adapter_verifier_digest(
            self.adapter_id,
            "synthetic live verifier",
            registry_errors,
        )
        if self.adapter_code_sha256 is None:
            raise ValueError("; ".join(registry_errors))

    @staticmethod
    def _key(locator: dict[str, Any]) -> str:
        return json.dumps(locator, sort_keys=True, separators=(",", ":"))

    def bind(
        self,
        record: dict[str, Any],
        evidence_type: str,
        release: dict[str, Any],
        *,
        verification_level: str = PREVIEW_ATTESTED,
        raw_evidence_kind: str = "structured_export",
    ) -> dict[str, Any]:
        identity = release_source_identity(release)
        if identity is None:
            raise ValueError("synthetic release has no complete source identity")
        raw_export: dict[str, Any] = {
            "schema_version": 3,
            "evidence_type": evidence_type,
            "observed": evidence_payload(record),
        }
        cache_inventory = cache_inventory_for_evidence(record, evidence_type)
        if cache_inventory is not None:
            raw_export.update(
                cache_inventory_complete=True,
                cache_inventory=cache_inventory,
            )
        raw_bytes = canonical_json_bytes(raw_export)
        assets: list[dict[str, Any]] = [
            {
                "asset_id": 101,
                "name": "raw-export.json",
                "sha256": evidence_sha256_bytes(raw_bytes),
                "size": len(raw_bytes),
                "evidence_kind": raw_evidence_kind,
            },
        ]
        payloads: dict[int, bytes] = {101: raw_bytes}
        if verification_level == PROVIDER_VERIFIED:
            provider_bytes = canonical_json_bytes({"provider": "synthetic-provider"})
            assets.append(
                {
                    "asset_id": 102,
                    "name": "provider-receipt.json",
                    "sha256": evidence_sha256_bytes(provider_bytes),
                    "size": len(provider_bytes),
                    "evidence_kind": "provider_receipt",
                }
            )
            payloads[102] = provider_bytes
        capture: dict[str, Any] = {
            "surface": "github_release",
            "task_or_thread_id": "release-ledger-self-test",
            "captured_at": "2026-07-13T00:00:00Z",
            "raw_export_asset_id": 101,
            "raw_export_sha256": evidence_sha256_bytes(raw_bytes),
        }
        expected_verifier: dict[str, Any] = {
            "verifier_id": "independent-release-ledger-self-test",
            "verifier_code_sha256": "sha256:" + "8" * 64,
            "independent": True,
        }
        if verification_level == PROVIDER_VERIFIED:
            capture["provider_receipt_asset_id"] = 102
        envelope = {
            "schema_version": "openai-preview-evidence-envelope/v1",
            "evidence_id": f"release-ledger-{verification_level}-self-test",
            "verification_level": verification_level,
            "provider_verified": verification_level == PROVIDER_VERIFIED,
            "counts_as_preview_acceptance": True,
            "source_identity": identity,
            "adapter": {
                "adapter_id": "capture-adapter-self-test",
                "adapter_code_sha256": "sha256:" + "7" * 64,
            },
            "capture": capture,
            "github_witness": {
                "repository": "xuxu-wei/research-skills",
                "release_id": 7101,
                "release_tag": "release-ledger-self-test",
                "workflow_run_id": 7102,
                "actor": "release-ledger-self-test",
                "raw_export_asset_id": 101,
                "source_commit": identity["source_commit"],
            },
            "expected_verifier": expected_verifier,
        }
        envelope_bytes = canonical_json_bytes(envelope)
        verifier_report = {
            "schema_version": "openai-preview-verifier-report/v1",
            "verifier_id": expected_verifier["verifier_id"],
            "verifier_code_sha256": expected_verifier["verifier_code_sha256"],
            "independent": True,
            "verified_at": "2026-07-13T00:02:00Z",
            "source_identity": identity,
            "envelope_asset_id": 104,
            "envelope_sha256": evidence_sha256_bytes(envelope_bytes),
            "raw_export_asset_id": 101,
            "raw_export_sha256": evidence_sha256_bytes(raw_bytes),
            "verdict": "accepted",
        }
        if verification_level == PROVIDER_VERIFIED:
            verifier_report.update(
                provider_receipt_asset_id=102,
                provider_receipt_sha256=evidence_sha256_bytes(payloads[102]),
                provider_attestation_checked=True,
            )
        verifier_report_bytes = canonical_json_bytes(verifier_report)
        assets.extend(
            [
                {
                    "asset_id": 104,
                    "name": "evidence-envelope.json",
                    "sha256": evidence_sha256_bytes(envelope_bytes),
                    "size": len(envelope_bytes),
                    "evidence_kind": "evidence_envelope",
                },
                {
                    "asset_id": 105,
                    "name": "verifier-report.json",
                    "sha256": evidence_sha256_bytes(verifier_report_bytes),
                    "size": len(verifier_report_bytes),
                    "evidence_kind": "verifier_report",
                },
            ]
        )
        payloads[104] = envelope_bytes
        payloads[105] = verifier_report_bytes
        index = {
            "schema_version": "openai-preview-release-asset-index/v1",
            "source_identity": identity,
            "github_release": {
                "repository": "xuxu-wei/research-skills",
                "release_id": 7101,
                "release_tag": "release-ledger-self-test",
            },
            "github_witness": {
                "workflow_run_id": 7102,
                "actor": "release-ledger-self-test",
                "source_commit": identity["source_commit"],
                "witnessed_at": "2026-07-13T00:01:00Z",
            },
            "assets": assets,
        }
        index_bytes = canonical_json_bytes(index)
        locator = {
            "repository": "xuxu-wei/research-skills",
            "release_id": 7101,
            "release_tag": "release-ledger-self-test",
            "capture_workflow_run_id": 7102,
            "verifier_workflow_run_id": 7103,
            "verifier_run_url": "https://github.com/xuxu-wei/research-skills/actions/runs/7103",
            "envelope_asset": {
                "asset_id": 104,
                "name": "evidence-envelope.json",
                "sha256": hashlib.sha256(envelope_bytes).hexdigest(),
            },
            "release_asset_index_asset": {
                "asset_id": 202,
                "name": "release-asset-index.json",
                "sha256": hashlib.sha256(index_bytes).hexdigest(),
            },
            "raw_export_asset": {
                "asset_id": 101,
                "name": "raw-export.json",
                "sha256": hashlib.sha256(raw_bytes).hexdigest(),
            },
            "verifier_report_asset": {
                "asset_id": 105,
                "name": "verifier-report.json",
                "sha256": hashlib.sha256(verifier_report_bytes).hexdigest(),
            },
        }
        record["status"] = verification_level
        record.pop("reason", None)
        record["evidence_path"] = None
        record["evidence_sha256"] = None
        record["evidence_locator"] = locator
        self.bundles[self._key(locator)] = {
            "envelope": envelope,
            "index": index,
            "index_bytes": index_bytes,
            "payloads": payloads,
            "raw_export": raw_export,
            "result_mutator": None,
        }
        return self.bundles[self._key(locator)]

    def reseal(self, record: dict[str, Any], bundle: dict[str, Any]) -> None:
        """Rebuild synthetic external digests after an intentional fixture edit."""

        envelope_bytes = canonical_json_bytes(bundle["envelope"])
        report = json.loads(bundle["payloads"][105].decode("utf-8"))
        report["envelope_sha256"] = evidence_sha256_bytes(envelope_bytes)
        report_bytes = canonical_json_bytes(report)
        bundle["payloads"][104] = envelope_bytes
        bundle["payloads"][105] = report_bytes
        for asset in bundle["index"]["assets"]:
            if asset["asset_id"] in {104, 105}:
                payload = bundle["payloads"][asset["asset_id"]]
                asset["sha256"] = evidence_sha256_bytes(payload)
                asset["size"] = len(payload)
        index_bytes = canonical_json_bytes(bundle["index"])
        bundle["index_bytes"] = index_bytes
        locator = record["evidence_locator"]
        locator["envelope_asset"]["sha256"] = hashlib.sha256(envelope_bytes).hexdigest()
        locator["verifier_report_asset"]["sha256"] = hashlib.sha256(report_bytes).hexdigest()
        locator["release_asset_index_asset"]["sha256"] = hashlib.sha256(index_bytes).hexdigest()
        for key, value in list(self.bundles.items()):
            if value is bundle:
                del self.bundles[key]
        self.bundles[self._key(locator)] = bundle

    def __call__(self, **request: Any) -> dict[str, Any]:
        locator = request["evidence_locator"]
        bundle = self.bundles.get(self._key(locator))
        if bundle is None:
            raise ValueError("external locator was not returned by the live GitHub query")
        envelope = bundle["envelope"]
        index = bundle["index"]
        index_bytes = bundle.get("index_bytes", canonical_json_bytes(index))
        payloads = bundle["payloads"]

        expected_locator_digests = {
            "envelope_asset": hashlib.sha256(payloads[104]).hexdigest(),
            "release_asset_index_asset": hashlib.sha256(index_bytes).hexdigest(),
            "verifier_report_asset": hashlib.sha256(payloads[105]).hexdigest(),
        }
        for field, digest in expected_locator_digests.items():
            if locator[field]["sha256"] != digest:
                raise ValueError(f"live re-query {field} digest mismatch")
        release = index.get("github_release", {})
        witness = index.get("github_witness", {})
        if (
            locator.get("repository") != release.get("repository")
            or locator.get("release_id") != release.get("release_id")
            or locator.get("release_tag") != release.get("release_tag")
            or locator.get("capture_workflow_run_id") != witness.get("workflow_run_id")
        ):
            raise ValueError("live re-query Release or workflow locator mismatch")

        fetched: dict[int, bytes] = {}

        def fetch_asset(asset: dict[str, Any]) -> bytes:
            payload = payloads[int(asset["asset_id"])]
            fetched[int(asset["asset_id"])] = payload
            return payload

        integrity = validate_evidence_bundle(
            envelope,
            index,
            fetch_asset,
            envelope_bytes=payloads[104],
            expected_source_identity=request["expected_source_identity"],
            index_bytes=index_bytes,
            now=SYNTHETIC_VALIDATION_NOW,
        )
        raw_id = integrity.raw_export_asset_id
        raw_bytes = fetched[raw_id]
        if locator["raw_export_asset"]["asset_id"] != raw_id:
            raise ValueError("live re-query raw asset id mismatch")
        if locator["raw_export_asset"]["sha256"] != hashlib.sha256(raw_bytes).hexdigest():
            raise ValueError("live re-query raw asset digest mismatch")
        raw_export = json.loads(raw_bytes.decode("utf-8"))
        claimed_level = getattr(
            integrity,
            "claimed_verification_level",
            getattr(integrity, "verification_level", request["expected_verification_level"]),
        )
        claimed_provider = getattr(
            integrity,
            "claimed_provider_verified",
            getattr(integrity, "provider_verified", False),
        )
        claimed_counts = getattr(
            integrity,
            "claimed_counts_as_preview_acceptance",
            getattr(integrity, "counts_as_preview_acceptance", False),
        )
        result = {
            "schema_version": 3,
            "evidence_type": request["evidence_type"],
            "verification_level": request["expected_verification_level"],
            "provider_verified": request["expected_verification_level"]
            == PROVIDER_VERIFIED,
            "observed": raw_export.get("observed"),
            "raw_export": raw_export,
            "source_identity": request["expected_source_identity"],
            "locator": locator,
            "integrity_result": {
                "evidence_id": integrity.evidence_id,
                "integrity_valid": getattr(integrity, "integrity_valid", True),
                "gate_eligible": getattr(integrity, "gate_eligible", False),
                "claimed_verification_level": claimed_level,
                "claimed_provider_verified": claimed_provider,
                "claimed_counts_as_preview_acceptance": claimed_counts,
                "source_identity_bound": getattr(integrity, "source_identity_bound", True),
                "raw_export_asset_id": integrity.raw_export_asset_id,
                "raw_export_sha256": integrity.raw_export_sha256,
                "envelope_sha256": evidence_sha256_bytes(payloads[104]),
                "verifier_report_asset_id": integrity.verifier_report_asset_id,
                "verifier_report_sha256": integrity.verifier_report_sha256,
                "release_asset_index_sha256": integrity.release_asset_index_sha256,
            },
            "live_verifier": {
                "adapter_id": self.adapter_id,
                "adapter_code_sha256": self.adapter_code_sha256,
                "live_requery_performed": True,
                "requery_source": "github_api",
                "independent": True,
                "verified_at": "2026-07-13T00:03:00Z",
                "verifier_workflow_run_id": locator["verifier_workflow_run_id"],
                "verifier_run_url": locator["verifier_run_url"],
            },
            "gate_eligibility": {
                "eligible": True,
                "level": request["expected_verification_level"],
                "determined_by": "registered_live_verifier",
                "provider_adapter_id": None,
                "provider_authenticated": False,
            },
        }
        mutator = bundle.get("result_mutator")
        if callable(mutator):
            mutator(result)
        return result


def external_records(release: dict[str, Any]) -> dict[str, dict[str, Any]]:
    ci = release["ci"]
    receipts = release["receipts"]
    return {
        "repository_preview_ci": ci["repository_preview"],
        "canonical_plugin_validator_ci": ci["canonical_plugin_validator"]["ci"],
        "main_branch_protection": release["governance"]["main_branch_protection"],
        "marketplace_resolved_commit": release["marketplace_source"]["resolved_commit"],
        "marketplace_upgrade": receipts["marketplace_upgrade"],
        "explicit_reinstall": receipts["explicit_reinstall"],
        "fresh_task_discovery": receipts["fresh_task_discovery"],
        "rollback": receipts["rollback"],
    }


def preview_release_fixture(evidence_dir: Path) -> dict[str, Any]:
    release = verified_release_fixture(evidence_dir, "preview-base")
    release["external_evidence_trust"] = {
        "adapter_status": "configured",
        "adapter_id": SyntheticLiveVerifier.adapter_id,
        "verification_level": PREVIEW_ATTESTED,
        "provider_authenticated": False,
        "reason": "Synthetic registered live-requery verifier for mutation tests.",
    }
    for record in external_records(release).values():
        record["status"] = "pending"
        record["reason"] = "Synthetic evidence has not been bound."
        record["evidence_path"] = None
        record["evidence_sha256"] = None
        record["evidence_locator"] = None
    return release


def verified_release_fixture(evidence_dir: Path, prefix: str = "fixture") -> dict[str, Any]:
    sha = "a" * 40
    fixture = {
        "version": "1.2.0-preview.1",
        "external_evidence_trust": {
            "adapter_status": "unavailable",
            "adapter_id": None,
            "verification_level": None,
            "provider_authenticated": False,
            "reason": "synthetic fixture uses an explicit test-only trust override",
        },
        "source_commit": {"status": "verified", "sha": sha},
        "installable_skill_tree": {
            "root": "skills/",
            "algorithm": SKILL_TREE_ALGORITHM,
            "file_count": 45,
            "sha256": "4" * 64,
        },
        "installable_contracts": {
            "manifest_sha256": "1" * 64,
            "registry_sha256": "2" * 64,
            "registry_schema_version": 5,
            "license_sha256": "3" * 64,
            "provenance_sha256": "5" * 64,
        },
        "marketplace_source": {"resolved_commit": {"status": "verified", "sha": sha}},
        "ci": {
            "repository_preview": {
                "status": "verified",
                "run_id": "1",
                "run_url": "https://example.invalid/run/1",
                "commit_sha": sha,
                "conclusion": "success",
            },
            "canonical_plugin_validator": {
                "local": {
                    "status": "verified",
                    "command": "validate",
                    "validator_source": "fixture",
                    "result": "passed",
                    "verified_on": "2026-07-12",
                },
                "ci": {
                    "status": "verified",
                    "run_id": "2",
                    "commit_sha": sha,
                    "conclusion": "success",
                },
            },
        },
        "governance": {
            "main_branch_protection": {
                "status": "verified",
                "branch": "main",
                "required_check": "OpenAI Plugin Preview / validate",
                "verified_at": "2026-07-12T00:00:00Z",
            }
        },
        "receipts": {
            "marketplace_upgrade": {
                "status": "verified",
                "installed_version": "1.2.0-preview.1",
                "source_commit": sha,
                "cache_path": "cache/upgrade",
                "cache_artifact": None,
            },
            "explicit_reinstall": {
                "status": "verified",
                "installed_version": "1.2.0-preview.1",
                "source_commit": sha,
                "cache_path": "cache/reinstall",
                "cache_artifact": None,
            },
            "fresh_task_discovery": {
                "status": "verified",
                "plugin_version": "1.2.0-preview.1",
                "source_commit": sha,
                "task_id": "task-1",
                "installed_skill_count": 45,
                "explicit_callable_entries": 1,
                "implicit_prompt_entries": 1,
                "explicit_callable_entry_skills": ["article-orchestrator"],
                "implicit_prompt_entry_skills": ["article-orchestrator"],
                "installed_via": "explicit_reinstall",
                "cache_artifact": None,
            },
            "rollback": {
                "status": "pending",
                "from_version": "1.2.0-preview.1",
                "to_version": None,
                "target_commit": None,
                "restored_cache_path": None,
                "candidate_cache_path": None,
                "candidate_from_receipt": None,
                "candidate_cache_artifact": None,
                "restored_cache_artifact": None,
                "cache_mixing_absent": None,
                "reason": "fixture",
            },
        },
    }
    upgrade_cache = build_cache_artifact(
        fixture,
        cache_path="cache/upgrade",
        cache_instance_id=f"{prefix}-upgrade-cache",
    )
    reinstall_cache = build_cache_artifact(
        fixture,
        cache_path="cache/reinstall",
        cache_instance_id=f"{prefix}-reinstall-cache",
    )
    fixture["receipts"]["marketplace_upgrade"]["cache_artifact"] = upgrade_cache
    fixture["receipts"]["explicit_reinstall"]["cache_artifact"] = reinstall_cache
    fixture["receipts"]["fresh_task_discovery"]["cache_artifact"] = copy.deepcopy(
        reinstall_cache
    )
    evidence_records = (
        (fixture["marketplace_source"]["resolved_commit"], "marketplace_resolved_commit"),
        (fixture["ci"]["repository_preview"], "repository_preview_ci"),
        (
            fixture["ci"]["canonical_plugin_validator"]["ci"],
            "canonical_plugin_validator_ci",
        ),
        (fixture["governance"]["main_branch_protection"], "main_branch_protection"),
        (fixture["receipts"]["marketplace_upgrade"], "marketplace_upgrade"),
        (fixture["receipts"]["explicit_reinstall"], "explicit_reinstall"),
        (fixture["receipts"]["fresh_task_discovery"], "fresh_task_discovery"),
    )
    for record, evidence_type in evidence_records:
        bind_fixture_evidence(
            record,
            evidence_type,
            evidence_dir / f"{prefix}-{evidence_type}.json",
        )
    return fixture


def run_live_evidence_mutation_tests(evidence_dir: Path) -> tuple[int, list[str]]:
    """Exercise the externally re-queried Preview tier and its fail-closed edges."""

    failures: list[str] = []
    count = 0

    def validate_case(
        release: dict[str, Any],
        verifier: LiveEvidenceVerifier | None,
        *,
        expected_skill_count: int = 45,
        explicit_entries: list[str] | None = None,
        implicit_entries: list[str] | None = None,
        defer_live_external_requery: bool = False,
    ) -> list[str]:
        case_errors: list[str] = []
        validate_all_sha_fields({"release": release}, "ledger", case_errors)
        validate_release_evidence(
            release,
            release["version"],
            expected_skill_count,
            case_errors,
            expected_explicit_entries=explicit_entries,
            expected_implicit_entries=implicit_entries,
            live_evidence_verifier=verifier,
            defer_live_external_requery=defer_live_external_requery,
            validation_now=SYNTHETIC_VALIDATION_NOW,
        )
        return case_errors

    def preview_repository_case(
        *, raw_evidence_kind: str = "structured_export"
    ) -> tuple[dict[str, Any], SyntheticLiveVerifier, dict[str, Any]]:
        release = preview_release_fixture(evidence_dir)
        verifier = SyntheticLiveVerifier()
        bundle = verifier.bind(
            release["ci"]["repository_preview"],
            "repository_preview_ci",
            release,
            raw_evidence_kind=raw_evidence_kind,
        )
        return release, verifier, bundle

    release, verifier, _ = preview_repository_case()
    errors = validate_case(release, verifier)
    if errors:
        failures.extend(f"live Preview fixture is invalid: {error}" for error in errors)
    count += 1

    errors = validate_case(release, None)
    if not any("without a live external re-query verifier" in error for error in errors):
        failures.append("Preview status without a live re-query verifier was not rejected")
    count += 1

    errors = validate_case(
        release,
        None,
        defer_live_external_requery=True,
    )
    if errors:
        failures.extend(
            f"structural-only accepted-ledger validation failed: {error}"
            for error in errors
        )
    count += 1

    errors = validate_case(
        release,
        verifier,
        defer_live_external_requery=True,
    )
    if not any(
        "structural-only validation cannot ignore a supplied live verifier" in error
        for error in errors
    ):
        failures.append(
            "structural-only validation silently ignored a supplied live verifier"
        )
    count += 1

    malformed_structural = copy.deepcopy(release)
    malformed_structural["ci"]["repository_preview"]["evidence_locator"][
        "raw_export_asset"
    ]["sha256"] = "not-a-digest"
    errors = validate_case(
        malformed_structural,
        None,
        defer_live_external_requery=True,
    )
    if not any("locator raw_export_asset digest is invalid" in error for error in errors):
        failures.append("structural-only validation accepted a malformed locator")
    count += 1

    def unregistered_verifier(**request: Any) -> dict[str, Any]:
        return verifier(**request)

    errors = validate_case(release, unregistered_verifier)
    if not any("live verifier is not registered" in error for error in errors):
        failures.append("unregistered live verifier callback was not rejected")
    count += 1

    result_contract_mutations: tuple[
        tuple[str, Callable[[dict[str, Any]], None], str], ...
    ] = (
        (
            "empty integrity evidence id",
            lambda result: result["integrity_result"].__setitem__("evidence_id", ""),
            "integrity result evidence_id is empty",
        ),
        (
            "false claimed Preview acceptance",
            lambda result: result["integrity_result"].__setitem__(
                "claimed_counts_as_preview_acceptance", False
            ),
            "envelope does not claim Preview acceptance",
        ),
        (
            "unregistered verifier code digest",
            lambda result: result["live_verifier"].__setitem__(
                "adapter_code_sha256", "0" * 64
            ),
            "verifier code digest differs from the committed provider verifier registry",
        ),
        (
            "timezone-naive live verifier timestamp",
            lambda result: result["live_verifier"].__setitem__(
                "verified_at", "2026-07-13T00:03:00"
            ),
            "verified_at is not a timezone-aware ISO timestamp",
        ),
        (
            "future live verifier timestamp",
            lambda result: result["live_verifier"].__setitem__(
                "verified_at", "2026-07-13T00:10:01Z"
            ),
            "verified_at is more than 5 minutes in the future",
        ),
        (
            "stale live verifier timestamp",
            lambda result: result["live_verifier"].__setitem__(
                "verified_at", "2026-04-13T00:03:00Z"
            ),
            "verified_at is older than 90 days",
        ),
    )
    for description, mutation, expected_error in result_contract_mutations:
        contract_release, contract_verifier, contract_bundle = preview_repository_case()
        contract_bundle["result_mutator"] = mutation
        errors = validate_case(contract_release, contract_verifier)
        if not any(expected_error in error for error in errors):
            failures.append(f"{description} was not rejected")
        count += 1

    local_binding_release, local_binding_verifier, _ = preview_repository_case()
    local_record = local_binding_release["ci"]["repository_preview"]
    local_record["evidence_path"] = "tests/openai_phase7/runtime-evidence/self-signed.json"
    local_record["evidence_sha256"] = "0" * 64
    errors = validate_case(local_binding_release, local_binding_verifier)
    if not any("repository-relative evidence cannot establish" in error for error in errors):
        failures.append("repository-relative self-signed evidence was not rejected")
    count += 1

    tampered_release, tampered_verifier, tampered_bundle = preview_repository_case()
    tampered_bundle["payloads"][101] += b"tamper"
    errors = validate_case(tampered_release, tampered_verifier)
    if not any("live external re-query failed" in error for error in errors):
        failures.append("tampered raw Release asset was not rejected")
    count += 1

    for evidence_kind in ("screenshot", "manual_note"):
        non_substantive_release, non_substantive_verifier, _ = preview_repository_case(
            raw_evidence_kind=evidence_kind
        )
        errors = validate_case(non_substantive_release, non_substantive_verifier)
        if not any("non_substantive_evidence_only" in error for error in errors):
            failures.append(f"{evidence_kind}-only Preview evidence was not rejected")
        count += 1

    identity_mutations = (
        ("plugin_version", "9.9.9-preview.1", "version"),
        ("source_commit", "b" * 40, "commit"),
        ("manifest_sha256", "0" * 64, "source identity"),
    )
    for field, value, description in identity_mutations:
        identity_release, identity_verifier, identity_bundle = preview_repository_case()
        identity_bundle["index"]["source_identity"][field] = value
        errors = validate_case(identity_release, identity_verifier)
        if not any("source_identity_mismatch" in error for error in errors):
            failures.append(f"external evidence {description} mismatch was not rejected")
        count += 1

    index_release, index_verifier, index_bundle = preview_repository_case()
    index_bundle["index_bytes"] += b"tamper"
    errors = validate_case(index_release, index_verifier)
    if not any("release_asset_index_asset digest mismatch" in error for error in errors):
        failures.append("tampered Release asset index was not rejected")
    count += 1

    witness_release, witness_verifier, witness_bundle = preview_repository_case()
    witness_bundle["envelope"]["github_witness"]["release_id"] = 9999
    witness_verifier.reseal(
        witness_release["ci"]["repository_preview"], witness_bundle
    )
    errors = validate_case(witness_release, witness_verifier)
    if not any("github_witness_mismatch" in error for error in errors):
        failures.append("mismatched GitHub witness was not rejected")
    count += 1

    downgraded_release, downgraded_verifier, downgraded_bundle = preview_repository_case()

    def forge_provider(result: dict[str, Any]) -> None:
        result["provider_verified"] = True

    downgraded_bundle["result_mutator"] = forge_provider
    errors = validate_case(downgraded_release, downgraded_verifier)
    if not any("provider flag conflicts" in error for error in errors):
        failures.append("Preview-to-provider result downgrade/forgery was not rejected")
    count += 1

    provider_release = preview_release_fixture(evidence_dir)
    provider_release["external_evidence_trust"] = {
        "adapter_status": "configured",
        "adapter_id": SyntheticLiveVerifier.adapter_id,
        "verification_level": PROVIDER_VERIFIED,
        "provider_authenticated": True,
        "reason": "Synthetic provider claim without a registered provider adapter.",
    }
    provider_verifier = SyntheticLiveVerifier()
    provider_verifier.bind(
        provider_release["ci"]["repository_preview"],
        "repository_preview_ci",
        provider_release,
        verification_level=PROVIDER_VERIFIED,
    )
    errors = validate_case(provider_release, provider_verifier)
    if not any("without a registered authenticated provider adapter" in error for error in errors):
        failures.append("provider receipt/boolean without a registered adapter was not rejected")
    count += 1

    explicit = [
        "academic-deep-search",
        "article-orchestrator",
        "perspective-orchestrator",
        "proposal-orchestrator",
        "research-idea-orchestrator",
        "research-opportunity-mapper",
        "research-polisher-orchestrator",
    ]
    implicit_a = explicit[:6]

    def discovery_case(
        *,
        installed_count: int = 49,
        explicit_count: int = 7,
        implicit_count: int = 6,
        explicit_skills: list[str] | None = None,
        implicit_skills: list[str] | None = None,
    ) -> tuple[dict[str, Any], SyntheticLiveVerifier]:
        candidate = preview_release_fixture(evidence_dir)
        discovery = candidate["receipts"]["fresh_task_discovery"]
        discovery["installed_skill_count"] = installed_count
        discovery["explicit_callable_entries"] = explicit_count
        discovery["implicit_prompt_entries"] = implicit_count
        discovery["explicit_callable_entry_skills"] = list(
            explicit if explicit_skills is None else explicit_skills
        )
        discovery["implicit_prompt_entry_skills"] = list(
            implicit_a if implicit_skills is None else implicit_skills
        )
        live = SyntheticLiveVerifier()
        live.bind(
            candidate["receipts"]["explicit_reinstall"],
            "explicit_reinstall",
            candidate,
        )
        live.bind(discovery, "fresh_task_discovery", candidate)
        return candidate, live

    phase_a_release, phase_a_verifier = discovery_case()
    errors = validate_case(
        phase_a_release,
        phase_a_verifier,
        expected_skill_count=49,
        explicit_entries=explicit,
        implicit_entries=implicit_a,
    )
    if errors:
        failures.extend(f"Phase-7A discovery fixture is invalid: {error}" for error in errors)
    count += 1

    phase_b_release, phase_b_verifier = discovery_case(
        implicit_count=7,
        implicit_skills=explicit,
    )
    errors = validate_case(
        phase_b_release,
        phase_b_verifier,
        expected_skill_count=49,
        explicit_entries=explicit,
        implicit_entries=explicit,
    )
    if errors:
        failures.extend(f"Phase-7B discovery fixture is invalid: {error}" for error in errors)
    count += 1

    count_mutations = (
        ({"installed_count": 48}, "skill count mismatch", "installed skill count"),
        ({"explicit_count": 6}, "explicit entry count mismatch", "explicit entry count"),
        ({"implicit_count": 5}, "implicit entry count mismatch", "implicit entry count"),
        (
            {"explicit_skills": [*explicit[:-1], "not-an-entry"]},
            "explicit entry identities mismatch",
            "explicit entry identity list",
        ),
    )
    for arguments, expected_error, description in count_mutations:
        count_release, count_verifier = discovery_case(**arguments)
        errors = validate_case(
            count_release,
            count_verifier,
            expected_skill_count=49,
            explicit_entries=explicit,
            implicit_entries=implicit_a,
        )
        if not any(expected_error in error for error in errors):
            failures.append(f"wrong discovery {description} was not rejected")
        count += 1

    return count, failures


def run_mutation_self_tests() -> tuple[int, list[str]]:
    with tempfile.TemporaryDirectory(prefix=".release-ledger-test-", dir=REPO) as temp_name:
        evidence_dir = Path(temp_name)
        fixture = verified_release_fixture(evidence_dir)
        baseline_errors: list[str] = []
        validate_all_sha_fields({"release": fixture}, "ledger", baseline_errors)
        validate_release_evidence(
            fixture,
            fixture["version"],
            45,
            baseline_errors,
            synthetic_external_trust_override=True,
        )
        failures = [f"verified fixture is invalid: {error}" for error in baseline_errors]

        mismatch_paths = (
            ("source_commit", "sha"),
            ("ci", "repository_preview", "commit_sha"),
            ("marketplace_source", "resolved_commit", "sha"),
            ("receipts", "marketplace_upgrade", "source_commit"),
            ("receipts", "explicit_reinstall", "source_commit"),
            ("receipts", "fresh_task_discovery", "source_commit"),
        )
        count = 0
        for path in mismatch_paths:
            mutated = copy.deepcopy(fixture)
            target: dict[str, Any] = mutated
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = "b" * 40
            mutation_errors: list[str] = []
            validate_all_sha_fields({"release": mutated}, "ledger", mutation_errors)
            validate_release_evidence(
                mutated,
                mutated["version"],
                45,
                mutation_errors,
                synthetic_external_trust_override=True,
            )
            if not any("does not match immutable source_commit" in error for error in mutation_errors):
                failures.append(f"commit mismatch mutation was not rejected: {'.'.join(path)}")
            count += 1

        invalid_sha_mutations = (
            ("ci", "canonical_plugin_validator", "ci", "commit_sha"),
            ("receipts", "rollback", "target_commit"),
        )
        for path in invalid_sha_mutations:
            mutated = copy.deepcopy(fixture)
            target = mutated
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = "not-a-sha"
            mutation_errors = []
            validate_all_sha_fields({"release": mutated}, "ledger", mutation_errors)
            validate_release_evidence(
                mutated,
                mutated["version"],
                45,
                mutation_errors,
                synthetic_external_trust_override=True,
            )
            if not any("commit SHA" in error for error in mutation_errors):
                failures.append(f"invalid SHA mutation was not rejected: {'.'.join(path)}")
            count += 1

        digest_fixture = {"installable_contracts": {"manifest_sha256": "not-a-sha"}}
        mutation_errors = []
        validate_all_sha_fields(digest_fixture, "ledger", mutation_errors)
        if not any("SHA-256" in error for error in mutation_errors):
            failures.append("invalid SHA-256 mutation was not rejected")
        count += 1

        matching_previous = copy.deepcopy(fixture)
        matching_previous["version"] = "1.1.0-preview.1"
        matching_previous["source_commit"] = {
            "status": "verified",
            "sha": "b" * 40,
        }
        restored_cache = build_cache_artifact(
            matching_previous,
            cache_path="cache/rollback",
            cache_instance_id="fixture-restored-cache",
        )
        candidate_cache = copy.deepcopy(
            fixture["receipts"]["explicit_reinstall"]["cache_artifact"]
        )
        rollback_fixture = copy.deepcopy(fixture)
        rollback_fixture["receipts"]["rollback"] = {
            "status": "verified",
            "from_version": rollback_fixture["version"],
            "to_version": "1.1.0-preview.1",
            "target_commit": "b" * 40,
            "restored_cache_path": "cache/rollback",
            "candidate_cache_path": candidate_cache["cache_path"],
            "candidate_from_receipt": "explicit_reinstall",
            "candidate_cache_artifact": candidate_cache,
            "restored_cache_artifact": restored_cache,
            "cache_mixing_absent": True,
        }
        bind_fixture_evidence(
            rollback_fixture["receipts"]["rollback"],
            "rollback",
            evidence_dir / "fixture-rollback.json",
        )
        mutation_errors = []
        validate_rollback_history_binding(rollback_fixture, [], mutation_errors)
        if not any("exactly one previous release" in error for error in mutation_errors):
            failures.append("rollback without a previous release entry was not rejected")
        count += 1

        previous = copy.deepcopy(matching_previous)
        previous["source_commit"] = {"status": "verified", "sha": "c" * 40}
        mutation_errors = []
        validate_rollback_history_binding(rollback_fixture, [previous], mutation_errors)
        if not any("does not match the previous release source_commit" in error for error in mutation_errors):
            failures.append("rollback target_commit mismatch with previous release was not rejected")
        count += 1

        mutation_errors = []
        validate_rollback_history_binding(
            rollback_fixture,
            [matching_previous],
            mutation_errors,
        )
        if not any("not an ancestor" in error for error in mutation_errors):
            failures.append("non-ancestor rollback target commit was not rejected")
        count += 1

        non_older_rollback = copy.deepcopy(rollback_fixture)
        non_older_rollback["receipts"]["rollback"]["to_version"] = (
            non_older_rollback["version"]
        )
        same_version_previous = copy.deepcopy(matching_previous)
        same_version_previous["version"] = non_older_rollback["version"]
        mutation_errors = []
        validate_rollback_history_binding(
            non_older_rollback,
            [same_version_previous],
            mutation_errors,
        )
        if not any("not strictly older" in error for error in mutation_errors):
            failures.append("non-decreasing rollback version was not rejected")
        count += 1

        missing_evidence = copy.deepcopy(fixture)
        missing_record = missing_evidence["marketplace_source"]["resolved_commit"]
        missing_record["evidence_path"] = None
        missing_record["evidence_sha256"] = None
        mutation_errors = []
        validate_release_evidence(
            missing_evidence,
            missing_evidence["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("verified without a safe evidence_path" in error for error in mutation_errors):
            failures.append("verified record without durable evidence was not rejected")
        count += 1

        mutation_errors = []
        validate_release_evidence(
            fixture,
            fixture["version"],
            45,
            mutation_errors,
            authenticated_external_adapter=False,
        )
        if not any(
            "invalid external evidence status" in error
            for error in mutation_errors
        ):
            failures.append(
                "legacy repository-authored verified evidence was not rejected"
            )
        count += 1

        digest_mismatch = copy.deepcopy(fixture)
        digest_mismatch["ci"]["repository_preview"]["evidence_sha256"] = "0" * 64
        mutation_errors = []
        validate_release_evidence(
            digest_mismatch,
            digest_mismatch["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("digest does not match" in error for error in mutation_errors):
            failures.append("external evidence digest mismatch was not rejected")
        count += 1

        content_mismatch = copy.deepcopy(fixture)
        content_record = content_mismatch["ci"]["canonical_plugin_validator"]["ci"]
        mismatched_path = evidence_dir / "mismatched-content.json"
        mismatched_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "evidence_type": "canonical_plugin_validator_ci",
                    "observed": {"run_id": "wrong"},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        content_record["evidence_path"] = mismatched_path.relative_to(REPO).as_posix()
        content_record["evidence_sha256"] = hashlib.sha256(mismatched_path.read_bytes()).hexdigest()
        mutation_errors = []
        validate_release_evidence(
            content_mismatch,
            content_mismatch["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("observed payload does not match" in error for error in mutation_errors):
            failures.append("external evidence content mismatch was not rejected")
        count += 1

        missing_cache_digest = copy.deepcopy(fixture)
        missing_record = missing_cache_digest["receipts"]["marketplace_upgrade"]
        del missing_record["cache_artifact"]["license_sha256"]
        bind_fixture_evidence(
            missing_record,
            "marketplace_upgrade",
            evidence_dir / "missing-cache-digest.json",
        )
        mutation_errors = []
        validate_release_evidence(
            missing_cache_digest,
            missing_cache_digest["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("cache artifact fields are incomplete" in error for error in mutation_errors):
            failures.append("install cache with a missing license digest was not rejected")
        count += 1

        wrong_cache_tree = copy.deepcopy(fixture)
        wrong_record = wrong_cache_tree["receipts"]["explicit_reinstall"]
        wrong_record["cache_artifact"]["skill_tree_sha256"] = "0" * 64
        wrong_record["cache_artifact"]["cache_identity_sha256"] = cache_identity_sha256(
            wrong_record["cache_artifact"]
        )
        bind_fixture_evidence(
            wrong_record,
            "explicit_reinstall",
            evidence_dir / "wrong-cache-tree.json",
        )
        mutation_errors = []
        validate_release_evidence(
            wrong_cache_tree,
            wrong_cache_tree["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("cache content does not match" in error for error in mutation_errors):
            failures.append("install cache with the wrong skill-tree digest was not rejected")
        count += 1

        discovery_cache_mismatch = copy.deepcopy(fixture)
        discovery_record = discovery_cache_mismatch["receipts"]["fresh_task_discovery"]
        discovery_record["cache_artifact"] = copy.deepcopy(
            discovery_cache_mismatch["receipts"]["marketplace_upgrade"]["cache_artifact"]
        )
        bind_fixture_evidence(
            discovery_record,
            "fresh_task_discovery",
            evidence_dir / "discovery-cache-mismatch.json",
        )
        mutation_errors = []
        validate_release_evidence(
            discovery_cache_mismatch,
            discovery_cache_mismatch["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("differs from the selected install receipt" in error for error in mutation_errors):
            failures.append("fresh discovery bound to the wrong cache instance was not rejected")
        count += 1

        raw_cache_inventory_mismatch = copy.deepcopy(fixture)
        raw_record = raw_cache_inventory_mismatch["receipts"]["marketplace_upgrade"]
        raw_path = evidence_dir / "provider-cache-inventory-mismatch.json"
        raw_document = {
            "schema_version": 1,
            "evidence_type": "marketplace_upgrade",
            "observed": evidence_payload(raw_record),
            "provider": "synthetic-test-only",
            "raw_export": {
                "synthetic": True,
                "cache_inventory_complete": True,
                "cache_inventory": [],
            },
        }
        raw_path.write_text(
            json.dumps(raw_document, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        raw_record["evidence_path"] = raw_path.relative_to(REPO).as_posix()
        raw_record["evidence_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
        mutation_errors = []
        validate_release_evidence(
            raw_cache_inventory_mismatch,
            raw_cache_inventory_mismatch["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("provider cache inventory does not match" in error for error in mutation_errors):
            failures.append("provider export with an incomplete cache inventory was not rejected")
        count += 1

        rollback_cache_mixing = copy.deepcopy(rollback_fixture)
        rollback_record = rollback_cache_mixing["receipts"]["rollback"]
        rollback_record["restored_cache_artifact"]["cache_instance_id"] = (
            rollback_record["candidate_cache_artifact"]["cache_instance_id"]
        )
        bind_fixture_evidence(
            rollback_record,
            "rollback",
            evidence_dir / "rollback-cache-mixing.json",
        )
        mutation_errors = []
        validate_release_evidence(
            rollback_cache_mixing,
            rollback_cache_mixing["version"],
            45,
            mutation_errors,
            synthetic_external_trust_override=True,
        )
        if not any("cache mixing detected" in error for error in mutation_errors):
            failures.append("rollback cache-instance mixing was not rejected")
        count += 1

        restored_identity_mismatch = copy.deepcopy(rollback_fixture)
        restored_record = restored_identity_mismatch["receipts"]["rollback"]
        restored_record["restored_cache_artifact"]["license_sha256"] = "9" * 64
        restored_record["restored_cache_artifact"]["cache_identity_sha256"] = (
            cache_identity_sha256(restored_record["restored_cache_artifact"])
        )
        bind_fixture_evidence(
            restored_record,
            "rollback",
            evidence_dir / "rollback-restored-identity-mismatch.json",
        )
        mutation_errors = []
        validate_rollback_history_binding(
            restored_identity_mismatch,
            [matching_previous],
            mutation_errors,
        )
        if not any("cache content does not match" in error for error in mutation_errors):
            failures.append("rollback restored cache differing from the previous release was not rejected")
        count += 1

        fake_commit = copy.deepcopy(fixture)
        fake_commit["source_commit"] = {"status": "verified", "sha": "0" * 40}
        mutation_errors = []
        validate_verified_source_commit_tree(fake_commit, mutation_errors, "fixture")
        if not any("does not exist in local Git history" in error for error in mutation_errors):
            failures.append("nonexistent verified source commit was not rejected")
        count += 1

        validation_count, validation_digest = normalized_validation_contract_digest()
        validation_fixture = {
            "validation_contract_tree": {
                "algorithm": VALIDATION_TREE_ALGORITHM,
                "file_count": validation_count,
                "sha256": validation_digest,
                "mutable_runtime_evidence_excluded": [
                    *sorted(MUTABLE_RUNTIME_EVIDENCE_FILES),
                    *sorted(
                        f"{prefix}**"
                        for prefix in MUTABLE_RUNTIME_EVIDENCE_PREFIXES
                    ),
                ],
            }
        }
        stale_validation_digest = copy.deepcopy(validation_fixture)
        stale_validation_digest["validation_contract_tree"]["sha256"] = "0" * 64
        mutation_errors = []
        validate_validation_contract_tree_record(
            stale_validation_digest,
            mutation_errors,
        )
        if not any("validation-contract digest is stale" in error for error in mutation_errors):
            failures.append("stale validation-contract digest was not rejected")
        count += 1

        stale_exclusions = copy.deepcopy(validation_fixture)
        stale_exclusions["validation_contract_tree"][
            "mutable_runtime_evidence_excluded"
        ] = []
        mutation_errors = []
        validate_validation_contract_tree_record(stale_exclusions, mutation_errors)
        if not any("mutable-evidence exclusions are stale" in error for error in mutation_errors):
            failures.append("stale validation-contract exclusions were not rejected")
        count += 1

        returncode, head_output, _ = git_bytes("rev-parse", "HEAD")
        if returncode == 0:
            committed_mismatch = {
                **validation_fixture,
                "source_commit": {
                    "status": "verified",
                    "sha": head_output.decode("ascii").strip(),
                },
                "installable_skill_tree": {},
                "installable_contracts": {},
                "marketplace_source": {},
                "version": "0.0.0-test",
            }
            committed_mismatch["validation_contract_tree"]["sha256"] = "0" * 64
            mutation_errors = []
            validate_verified_source_commit_tree(
                committed_mismatch,
                mutation_errors,
                "fixture",
            )
            if not any(
                "committed validation-contract tree differs" in error
                for error in mutation_errors
            ):
                failures.append(
                    "committed validation-contract tree mismatch was not rejected"
                )
            count += 1
        live_count, live_failures = run_live_evidence_mutation_tests(evidence_dir)
        count += live_count
        failures.extend(live_failures)
        return count, failures


def validate_provenance(registry: dict[str, Any], errors: list[str]) -> None:
    path = PLUGIN / "PROVENANCE.yaml"
    require(path.is_file(), "PROVENANCE.yaml is missing", errors)
    if not path.is_file():
        return
    provenance = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(provenance.get("schema_version") == 1, "provenance schema_version must be 1", errors)
    require(provenance.get("plugin") == "research-skills-openai", "provenance plugin mismatch", errors)
    license_data = provenance.get("license", {})
    require(license_data.get("spdx_id") == "MIT", "provenance SPDX license is not MIT", errors)
    require(license_data.get("resolution_status") == "resolved", "plugin license is unresolved", errors)
    require(provenance.get("unresolved_resources") == [], "provenance has unresolved resources", errors)
    require(
        provenance.get("authorship", {}).get("per_resource_declared_authors")
        == "unknown_not_declared",
        "unknown per-resource authorship must be explicit",
        errors,
    )

    derivation = provenance.get("skill_resource_derivation", {})
    require(
        derivation.get("plugin_scope_template") == "skills/{name}/**",
        "skill plugin scope template is invalid",
        errors,
    )
    require(
        derivation.get("hermes_source_template") == "../research-skills/{package}/{name}/",
        "Hermes source template is invalid",
        errors,
    )
    require(
        derivation.get("openai_native_package") == "research-polisher",
        "OpenAI-native package declaration is invalid",
        errors,
    )
    declared_native = set(derivation.get("openai_native_skills", []))
    require(
        declared_native == OPENAI_NATIVE_SKILLS,
        "OpenAI-native skill provenance inventory is incomplete",
        errors,
    )
    origin_profiles = derivation.get("origin_profiles", {})
    require(
        origin_profiles.get("hermes_adapted", {}).get("source_template")
        == "../research-skills/{package}/{name}/",
        "Hermes-adapted origin profile is invalid",
        errors,
    )
    require(
        origin_profiles.get("openai_native", {}).get("source_template")
        == "skills/{name}/**",
        "OpenAI-native origin profile is invalid",
        errors,
    )
    require(
        derivation.get("content_origin") == "resolved_by_skill_origin_profile",
        "skill content origin must be resolved by origin profile",
        errors,
    )
    native_group = next(
        (
            group
            for group in provenance.get("resource_groups", [])
            if group.get("name") == "openai_native_research_polisher_skills"
        ),
        {},
    )
    require(
        native_group.get("origin")
        == "maintained_in_this_repository_for_openai_runtime"
        and native_group.get("origin_status") == "resolved",
        "OpenAI-native resource group is unresolved",
        errors,
    )
    require(
        derivation.get("per_resource_declared_authors") == "unknown_not_declared",
        "skill-level unknown authorship must be explicit",
        errors,
    )

    skills = registry.get("skills", [])
    require(bool(skills), "registry contains no skills for provenance", errors)
    registry_native = {
        str(skill.get("name", ""))
        for skill in skills
        if str(skill.get("package", "")) == derivation.get("openai_native_package")
    }
    require(
        registry_native == declared_native,
        "registry and provenance OpenAI-native inventories differ",
        errors,
    )
    for skill in skills:
        name = str(skill.get("name", ""))
        package = str(skill.get("package", ""))
        plugin_dir = PLUGIN / "skills" / name
        require(plugin_dir.is_dir(), f"unresolved plugin resource scope for {name}", errors)
        if name in declared_native:
            require(
                package == derivation.get("openai_native_package"),
                f"OpenAI-native package mismatch for {name}: {package}",
                errors,
            )
            separate_licenses = [
                item
                for item in plugin_dir.rglob("*")
                if item.is_file()
                and item.name.upper().split(".", 1)[0] in {"LICENSE", "NOTICE"}
            ]
            require(
                not separate_licenses,
                f"{name} has a separate license/notice requiring a declared exception",
                errors,
            )
            continue
        source = REPO / "research-skills" / package / name
        require(source.is_dir(), f"unresolved Hermes source for {name}: {source}", errors)
        separate_licenses = [
            item for item in source.rglob("*")
            if item.is_file() and item.name.upper().split(".", 1)[0] in {"LICENSE", "NOTICE"}
        ]
        require(
            not separate_licenses,
            f"{name} has a separate license/notice requiring a declared exception",
            errors,
        )

    expected_top_files = {
        "AGENTS.md",
        "README.md",
        "ROADMAP.md",
        "PHASE7-8-RUNBOOK.md",
        "workflow-registry.yaml",
        "LICENSE",
        "PROVENANCE.yaml",
    }
    actual_top_files = {item.name for item in PLUGIN.iterdir() if item.is_file()}
    require(actual_top_files == expected_top_files, f"unscoped plugin top files: {sorted(actual_top_files ^ expected_top_files)}", errors)


def main() -> int:
    errors: list[str] = []
    mutation_count, mutation_errors = run_mutation_self_tests()
    errors.extend(mutation_errors)
    require(RELEASE_EVIDENCE_SCHEMA_PATH.is_file(), "release evidence schema is missing", errors)
    if RELEASE_EVIDENCE_SCHEMA_PATH.is_file():
        evidence_schema = yaml.safe_load(
            RELEASE_EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8-sig")
        )
        declared_types = set(
            evidence_schema.get("properties", {})
            .get("evidence_type", {})
            .get("enum", [])
        )
        require(
            declared_types == EXTERNAL_EVIDENCE_TYPES,
            "release evidence schema types differ from the validator contract",
            errors,
        )
        require(
            {
                "schema_version",
                "evidence_type",
                "verification_level",
                "provider_verified",
                "observed",
                "raw_export",
                "source_identity",
                "locator",
                "integrity_result",
                "live_verifier",
                "gate_eligibility",
            }
            <= set(evidence_schema.get("required", [])),
            "release evidence schema does not require the live-verifier result contract",
            errors,
        )
        require(
            evidence_schema.get("properties", {})
            .get("schema_version", {})
            .get("const")
            == 3,
            "release evidence schema_version is not 3",
            errors,
        )
        integrity_schema = evidence_schema.get("properties", {}).get(
            "integrity_result", {}
        )
        require(
            integrity_schema.get("properties", {})
            .get("evidence_id", {})
            .get("minLength")
            == 1,
            "release evidence schema does not require a non-empty evidence_id",
            errors,
        )
        require(
            integrity_schema.get("properties", {})
            .get("claimed_counts_as_preview_acceptance", {})
            .get("const")
            is True,
            "release evidence schema does not require the envelope acceptance claim",
            errors,
        )
        live_verifier_schema = evidence_schema.get("properties", {}).get(
            "live_verifier", {}
        )
        require(
            live_verifier_schema.get("properties", {})
            .get("verified_at", {})
            .get("format")
            == "date-time",
            "release evidence schema does not require a date-time verifier timestamp",
            errors,
        )
        cache_schema = evidence_schema.get("$defs", {}).get("cache_artifact", {})
        require(
            set(cache_schema.get("required", [])) == CACHE_ARTIFACT_FIELDS,
            "release evidence cache-artifact schema differs from the validator contract",
            errors,
        )
        require(
            evidence_schema.get("x-evidence-contract", {}).get("cache_inventory_policy"),
            "release evidence schema does not declare the cache inventory policy",
            errors,
        )
        require(
            evidence_schema.get("x-evidence-contract", {}).get("live_requery_policy")
            and evidence_schema.get("x-evidence-contract", {}).get("integrity_boundary")
            and evidence_schema.get("x-evidence-contract", {}).get("persistence_policy"),
            "release evidence schema does not declare external live-requery and integrity boundaries",
            errors,
        )
        require(
            evidence_schema.get("x-evidence-contract", {}).get(
                "adapter_digest_policy"
            ),
            "release evidence schema does not declare adapter digest binding",
            errors,
        )
    require(LEDGER_PATH.is_file(), "release ledger is missing", errors)
    if not LEDGER_PATH.is_file():
        print("OpenAI release-ledger validation failed")
        print("ERROR: release ledger is missing")
        return 1

    manifest = load_json(MANIFEST_PATH)
    registry = yaml.safe_load((PLUGIN / "workflow-registry.yaml").read_text(encoding="utf-8"))
    ledger = load_json(LEDGER_PATH)
    release = ledger.get("release", {})
    validate_all_sha_fields(ledger, "ledger", errors)
    require(ledger.get("schema_version") == 1, "ledger schema_version must be 1", errors)
    require(ledger.get("plugin") == manifest.get("name"), "ledger plugin identity mismatch", errors)
    require(
        ledger.get("external_evidence_schema")
        == RELEASE_EVIDENCE_SCHEMA_PATH.relative_to(REPO).as_posix(),
        "ledger external evidence schema path is stale",
        errors,
    )
    require(release.get("version") == manifest.get("version"), "ledger version differs from manifest", errors)
    require(registry.get("plugin_version") == manifest.get("version"), "registry version differs from manifest", errors)
    public_policy = registry.get("public_entry_policy", {})
    declared_entries = public_policy.get("declared_entries", [])
    implicit_entries = public_policy.get("implicit_active_entries", [])
    require(len(registry.get("skills", [])) == 49, "release discovery baseline must contain 49 skills", errors)
    require(
        isinstance(declared_entries, list)
        and len(declared_entries) == 7
        and len(set(declared_entries)) == 7,
        "release discovery baseline must contain 7 unique explicit entries",
        errors,
    )
    require(
        isinstance(implicit_entries, list)
        and len(implicit_entries) in {6, 7}
        and len(set(implicit_entries)) == len(implicit_entries)
        and set(implicit_entries) <= set(declared_entries),
        "release discovery baseline must contain 6 Phase-7A or 7 Phase-7B implicit entries",
        errors,
    )

    file_count, digest = normalized_skill_tree_digest(PLUGIN / "skills")
    tree = release.get("installable_skill_tree", {})
    require(tree.get("root") == "skills/", "ledger skill-tree root mismatch", errors)
    require(tree.get("algorithm") == SKILL_TREE_ALGORITHM, "ledger skill-tree algorithm mismatch", errors)
    require(tree.get("file_count") == file_count, "ledger skill-tree file count is stale", errors)
    require(tree.get("sha256") == digest, "ledger skill-tree digest is stale", errors)
    require(bool(SHA256_RE.fullmatch(str(tree.get("sha256", "")))), "ledger skill-tree digest format is invalid", errors)

    validate_validation_contract_tree_record(release, errors)

    contracts = release.get("installable_contracts", {})
    require(
        contracts.get("manifest_sha256") == normalized_file_digest(MANIFEST_PATH),
        "ledger manifest digest is stale",
        errors,
    )
    registry_path = PLUGIN / "workflow-registry.yaml"
    require(
        contracts.get("registry_sha256") == normalized_file_digest(registry_path),
        "ledger registry digest is stale",
        errors,
    )
    require(
        contracts.get("registry_schema_version") == registry.get("schema_version"),
        "ledger registry schema is stale",
        errors,
    )
    require(
        contracts.get("license_sha256") == normalized_file_digest(PLUGIN / "LICENSE"),
        "ledger license digest is stale",
        errors,
    )
    require(
        contracts.get("provenance_sha256") == normalized_file_digest(PLUGIN / "PROVENANCE.yaml"),
        "ledger provenance digest is stale",
        errors,
    )

    marketplace = load_json(REPO / ".agents" / "plugins" / "marketplace.json")
    entry = next(item for item in marketplace["plugins"] if item.get("name") == manifest.get("name"))
    source = release.get("marketplace_source", {})
    expected_source = {"source": source.get("source"), "url": source.get("url"), "path": source.get("path"), "ref": source.get("ref")}
    require(expected_source == entry.get("source"), "ledger marketplace source is stale", errors)
    require(source.get("marketplace_name") == marketplace.get("name"), "ledger marketplace name mismatch", errors)
    current_version = str(manifest.get("version"))
    validate_release_evidence(
        release,
        current_version,
        len(registry.get("skills", [])),
        errors,
        authenticated_external_adapter=(
            authenticated_external_evidence_adapter_available(release)
        ),
        expected_explicit_entries=declared_entries,
        expected_implicit_entries=implicit_entries,
        defer_live_external_requery=True,
    )
    validate_verified_source_commit_tree(release, errors)

    previous_releases = ledger.get("previous_releases", [])
    require(isinstance(previous_releases, list), "previous_releases is not a list", errors)
    if isinstance(previous_releases, list):
        for index, previous_release in enumerate(previous_releases):
            label = f"previous_releases[{index}]"
            require(isinstance(previous_release, dict), f"{label} is not an object", errors)
            if isinstance(previous_release, dict):
                validate_release_evidence(
                    previous_release,
                    str(previous_release.get("version", "")),
                    None,
                    errors,
                    prefix=f"{label}.",
                    authenticated_external_adapter=(
                        authenticated_external_evidence_adapter_available(
                            previous_release
                        )
                    ),
                    defer_live_external_requery=True,
                )
                validate_verified_source_commit_tree(previous_release, errors, label)
        validate_rollback_history_binding(release, previous_releases, errors)

    root_license = (REPO / "LICENSE").read_bytes()
    plugin_license = PLUGIN / "LICENSE"
    require(plugin_license.is_file(), "installable plugin LICENSE is missing", errors)
    if plugin_license.is_file():
        require(plugin_license.read_bytes() == root_license, "plugin LICENSE differs from repository MIT license", errors)
    require(manifest.get("license") == "MIT", "manifest license is not MIT", errors)
    validate_provenance(registry, errors)

    if errors:
        print("OpenAI release-ledger validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    pending_count = len(re.findall(r'"status": "pending"', LEDGER_PATH.read_text(encoding="utf-8")))
    print("OpenAI release-ledger structural validation passed")
    print(f"version: {current_version}")
    print(f"skill tree: {file_count} files / {digest}")
    print(
        "external acceptance replay: structural-only in this offline command; "
        "the protected accepted-state workflow must perform the production live re-query"
    )
    print(f"provenance: {len(registry.get('skills', []))} skills resolved / 0 unresolved resources")
    print(f"external evidence still pending: {pending_count}")
    print(f"release-ledger mutation self-tests: {mutation_count} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
