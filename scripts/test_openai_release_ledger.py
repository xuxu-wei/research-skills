#!/usr/bin/env python3
"""Validate release-ledger and provenance coverage for the OpenAI plugin."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

import yaml

from openai_release_utils import compare_semver, parse_semver

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
VALID_STATUS = {"pending", "verified"}
EVIDENCE_META_FIELDS = {"status", "reason", "evidence_path", "evidence_sha256"}
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


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


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
        and trust.get("provider_authenticated") is True
        and isinstance(adapter_id, str)
        and adapter_id in SUPPORTED_AUTHENTICATED_EXTERNAL_EVIDENCE_ADAPTERS
    )


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


def validate_bound_external_evidence(
    record: Any,
    evidence_type: str,
    label: str,
    errors: list[str],
    *,
    authenticated_external_adapter: bool = False,
    synthetic_external_trust_override: bool = False,
) -> None:
    """Require a verified external claim to match one durable raw evidence file."""

    if not isinstance(record, dict) or record.get("status") != "verified":
        return
    require(
        authenticated_external_adapter or synthetic_external_trust_override,
        f"{label} cannot be verified without an authenticated external-evidence adapter",
        errors,
    )
    require(evidence_type in EXTERNAL_EVIDENCE_TYPES, f"{label} uses unknown evidence type", errors)
    evidence_path = resolve_repository_evidence_path(record.get("evidence_path"))
    require(evidence_path is not None, f"{label} verified without a safe evidence_path", errors)
    require(
        bool(SHA256_RE.fullmatch(str(record.get("evidence_sha256", "")))),
        f"{label} verified without a valid evidence_sha256",
        errors,
    )
    if evidence_path is None:
        return
    require(evidence_path.is_file(), f"{label} evidence file does not exist", errors)
    if not evidence_path.is_file():
        return
    actual_digest = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    require(
        record.get("evidence_sha256") == actual_digest,
        f"{label} evidence digest does not match the actual file",
        errors,
    )
    document = load_structured_evidence(evidence_path)
    require(isinstance(document, dict), f"{label} evidence file is not JSON/YAML object", errors)
    if not isinstance(document, dict):
        return
    require(document.get("schema_version") == 1, f"{label} evidence schema_version is not 1", errors)
    require(document.get("evidence_type") == evidence_type, f"{label} evidence_type mismatch", errors)
    require(
        isinstance(document.get("provider"), str)
        and bool(document["provider"].strip()),
        f"{label} evidence provider is missing",
        errors,
    )
    require(
        isinstance(document.get("raw_export"), dict),
        f"{label} raw provider export is missing",
        errors,
    )
    require(
        document.get("observed") == evidence_payload(record),
        f"{label} evidence observed payload does not match the ledger record",
        errors,
    )
    expected_cache_inventory = cache_inventory_for_evidence(record, evidence_type)
    if expected_cache_inventory is not None:
        raw_export = document.get("raw_export", {})
        require(
            raw_export.get("cache_inventory_complete") is True,
            f"{label} provider export does not attest a complete cache inventory",
            errors,
        )
        require(
            raw_export.get("cache_inventory") == expected_cache_inventory,
            f"{label} provider cache inventory does not match the ledger record",
            errors,
        )


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
) -> None:
    require(isinstance(record, dict), f"{label} is not an object", errors)
    if not isinstance(record, dict):
        return
    status = record.get("status")
    require(status in VALID_STATUS, f"{label} has invalid status: {status}", errors)
    if status == "pending":
        require(bool(record.get("reason")), f"{label} pending status lacks a reason", errors)
    elif status == "verified":
        for field in verified_fields:
            require(record.get(field) not in (None, ""), f"{label} verified without {field}", errors)


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
    if not isinstance(record, dict) or record.get("status") != "verified":
        return
    require(
        isinstance(source_commit, dict) and source_commit.get("status") == "verified",
        f"{label} is verified while source_commit is not verified",
        errors,
    )
    expected = source_commit.get("sha") if isinstance(source_commit, dict) else None
    require(
        record.get(field) == expected,
        f"{label} commit does not match immutable source_commit",
        errors,
    )


def validate_release_evidence(
    release: dict[str, Any],
    current_version: str,
    expected_skill_count: int | None,
    errors: list[str],
    prefix: str = "",
    *,
    authenticated_external_adapter: bool = False,
    synthetic_external_trust_override: bool = False,
) -> None:
    def named(label: str) -> str:
        return f"{prefix}{label}"

    def validate_external(record: Any, evidence_type: str, label: str) -> None:
        validate_bound_external_evidence(
            record,
            evidence_type,
            label,
            errors,
            authenticated_external_adapter=authenticated_external_adapter,
            synthetic_external_trust_override=synthetic_external_trust_override,
        )

    trust = release.get("external_evidence_trust", {})
    require(isinstance(trust, dict), named("external evidence trust is not an object"), errors)
    if isinstance(trust, dict):
        require(
            trust.get("adapter_status") in {"unavailable", "configured"},
            named("external evidence trust adapter_status is invalid"),
            errors,
        )
        require(
            isinstance(trust.get("reason"), str) and bool(trust["reason"].strip()),
            named("external evidence trust reason is missing"),
            errors,
        )
        if trust.get("adapter_status") == "unavailable":
            require(trust.get("adapter_id") is None, named("unavailable external adapter has an id"), errors)
            require(
                trust.get("provider_authenticated") is False,
                named("unavailable external adapter claims provider authentication"),
                errors,
            )
        else:
            require(
                authenticated_external_evidence_adapter_available(release),
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
    validate_status_record(resolved_commit, named("marketplace_resolved_commit"), errors, ("sha",))
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
    )
    if isinstance(repository_ci, dict) and repository_ci.get("status") == "verified":
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
    )
    if isinstance(canonical_ci, dict) and canonical_ci.get("status") == "verified":
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
    )
    if isinstance(branch_protection, dict):
        require(branch_protection.get("branch") == "main", named("branch protection target is not main"), errors)
        if branch_protection.get("status") == "verified":
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
        )
        if isinstance(receipt, dict) and receipt.get("status") == "verified":
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
            "skill_count",
            "visible_entry_skills",
            "installed_via",
            "cache_artifact",
        ),
    )
    if isinstance(discovery, dict) and discovery.get("status") == "verified":
        require(discovery.get("plugin_version") == current_version, f"{discovery_label} version mismatch", errors)
        if expected_skill_count is None:
            require(
                isinstance(discovery.get("skill_count"), int) and discovery.get("skill_count") > 0,
                f"{discovery_label} skill count is invalid",
                errors,
            )
        else:
            require(
                discovery.get("skill_count") == expected_skill_count,
                f"{discovery_label} skill count mismatch",
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
            and selected_install.get("status") == "verified",
            f"{discovery_label} does not reference a verified install receipt",
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
    )
    if isinstance(rollback, dict) and rollback.get("status") == "verified":
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
            and selected_install.get("status") == "verified"
            and candidate_cache == selected_install.get("cache_artifact"),
            f"{rollback_label} candidate cache does not match a verified current install",
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
    if not isinstance(rollback, dict) or rollback.get("status") != "verified":
        return
    target_version = rollback.get("to_version")
    target_commit = rollback.get("target_commit")
    from_version = rollback.get("from_version")
    if not isinstance(from_version, str) or not isinstance(target_version, str):
        require(False, "verified rollback versions are invalid", errors)
    elif parse_semver(from_version) is None or parse_semver(target_version) is None:
        require(False, "verified rollback versions are not strict SemVer", errors)
    else:
        require(
            compare_semver(target_version, from_version) < 0,
            "verified rollback target version is not strictly older than the current version",
            errors,
        )
    matches = [
        previous
        for previous in previous_releases
        if isinstance(previous, dict) and previous.get("version") == target_version
    ]
    require(
        len(matches) == 1,
        "verified rollback must target exactly one previous release ledger entry",
        errors,
    )
    if len(matches) != 1:
        return
    previous_source = matches[0].get("source_commit", {})
    require(
        isinstance(previous_source, dict)
        and previous_source.get("status") == "verified",
        "verified rollback targets a previous release without a verified immutable source commit",
        errors,
    )
    require(
        isinstance(previous_source, dict)
        and previous_source.get("sha") == target_commit,
        "verified rollback target_commit does not match the previous release source_commit",
        errors,
    )
    validate_cache_artifact(
        rollback.get("restored_cache_artifact"),
        matches[0],
        "verified rollback restored",
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
            "verified rollback target commit is not an ancestor of the current release commit",
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


def verified_release_fixture(evidence_dir: Path, prefix: str = "fixture") -> dict[str, Any]:
    sha = "a" * 40
    fixture = {
        "version": "1.2.0-preview.1",
        "external_evidence_trust": {
            "adapter_status": "unavailable",
            "adapter_id": None,
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
                "skill_count": 45,
                "visible_entry_skills": ["article-orchestrator"],
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
            "without an authenticated external-evidence adapter" in error
            for error in mutation_errors
        ):
            failures.append(
                "repository-authored external evidence without a trust adapter was not rejected"
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
        derivation.get("per_resource_declared_authors") == "unknown_not_declared",
        "skill-level unknown authorship must be explicit",
        errors,
    )

    skills = registry.get("skills", [])
    require(bool(skills), "registry contains no skills for provenance", errors)
    for skill in skills:
        name = str(skill.get("name", ""))
        package = str(skill.get("package", ""))
        source = REPO / "research-skills" / package / name
        plugin_dir = PLUGIN / "skills" / name
        require(source.is_dir(), f"unresolved Hermes source for {name}: {source}", errors)
        require(plugin_dir.is_dir(), f"unresolved plugin resource scope for {name}", errors)
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
        "AGENTS.md", "README.md", "ROADMAP.md", "workflow-registry.yaml", "LICENSE", "PROVENANCE.yaml"
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
            {"schema_version", "evidence_type", "observed", "provider", "raw_export"}
            <= set(evidence_schema.get("required", [])),
            "release evidence schema does not require provider raw export binding",
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
    print("OpenAI release-ledger validation passed")
    print(f"version: {current_version}")
    print(f"skill tree: {file_count} files / {digest}")
    print(f"provenance: {len(registry.get('skills', []))} skills resolved / 0 unresolved resources")
    print(f"external evidence still pending: {pending_count}")
    print(f"release-ledger mutation self-tests: {mutation_count} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
