#!/usr/bin/env python3
"""Validate all eight release-ledger evidence records with live GitHub re-query.

The CLI consumes one-record mini-bundles that have already been downloaded
from a GitHub Release.  Local files are staging inputs only: the registered
Phase 8 verifier re-queries GitHub and re-downloads every indexed asset before
it can return a gate-eligible result.  This runner accepts no serialized
verifier result, Boolean trust override, or synthetic mode.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import importlib.util
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import yaml

import test_openai_release_ledger as ledger_contract
from generate_openai_release_ledger import (
    MANIFEST_PATH,
    PLUGIN,
    REPO,
    SKILL_TREE_ALGORITHM,
    normalized_file_digest,
    normalized_skill_tree_digest,
)
from openai_preview_evidence import PREVIEW_ATTESTED


DEFAULT_LEDGER = PLUGIN / "reports" / "release-ledger.json"
PHASE8_VERIFIER_PATH = REPO / "tests" / "openai_phase8" / "verify_preview_evidence.py"
ADAPTER_ID = "github_release_asset_preview_v1"
RESULT_SCHEMA = "openai-release-evidence-runner-result/v1"
RUN_SUMMARY_SCHEMA = "openai-preview-live-verifier-summary/v1"
RUN_SUMMARY_JSON_NAME = "openai-preview-live-verifier-summary.json"
RUN_SUMMARY_ARTIFACT_PREFIX = "openai-preview-live-verifier-summary-"
RUN_SUMMARY_ARCHIVE_MAX_BYTES = 1_000_000
RUN_SUMMARY_JSON_MAX_BYTES = 1_000_000
GITHUB_API_HOST = "api.github.com"
EXPECTED_EVIDENCE_TYPES = frozenset(ledger_contract.EXTERNAL_EVIDENCE_TYPES)
ASSET_FIELDS = {
    "envelope_asset": "evidence_envelope",
    "raw_export_asset": None,
    "verifier_report_asset": "verifier_report",
}


class ReleaseEvidenceRunnerError(ValueError):
    """Fail-closed runner error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class _ActionsArtifactRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Allow one GitHub-authorized redirect to documented Actions storage."""

    def __init__(self) -> None:
        super().__init__()
        self.redirect_count = 0

    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: Any,
        code: int,
        message: str,
        headers: Mapping[str, Any],
        new_url: str,
    ) -> urllib.request.Request | None:
        self.redirect_count += 1
        if self.redirect_count != 1 or not _actions_artifact_storage_url(new_url):
            raise urllib.error.URLError("unsafe GitHub Actions artifact redirect")
        return super().redirect_request(
            request, file_pointer, code, message, headers, new_url
        )


def _actions_artifact_storage_url(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    host = (parsed.hostname or "").lower()
    return (
        parsed.scheme == "https"
        and parsed.username is None
        and parsed.password is None
        and not parsed.fragment
        and bool(parsed.path)
        and (
            host == "results-receiver.actions.githubusercontent.com"
            or bool(
                re.fullmatch(
                    r"productionresults[a-z0-9-]*\.blob\.core\.windows\.net",
                    host,
                )
            )
        )
    )


def download_github_actions_artifact(url: str) -> bytes:
    """Download one Actions ZIP without broadening the Phase 8 asset allowlist."""

    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != GITHUB_API_HOST
        or parsed.query
        or parsed.fragment
        or re.fullmatch(
            r"/repos/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/actions/artifacts/"
            r"[1-9][0-9]*/zip",
            parsed.path,
        )
        is None
    ):
        _fail("artifact_download_url_invalid", "Actions artifact API URL is invalid")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        _fail("github_token_missing", "GH_TOKEN or GITHUB_TOKEN is required")
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "research-skills-openai-release-evidence",
        },
    )
    # Authentication is sent only to the initial api.github.com request and is
    # never forwarded to the signed Actions-storage URL.
    request.add_unredirected_header("Authorization", f"Bearer {token}")
    handler = _ActionsArtifactRedirectHandler()
    opener = urllib.request.build_opener(handler)
    try:
        with opener.open(request, timeout=30) as response:
            final_url = response.geturl()
            if handler.redirect_count != 1 or not _actions_artifact_storage_url(
                final_url
            ):
                _fail(
                    "artifact_download_redirect_invalid",
                    "Actions artifact download did not end at trusted storage",
                )
            payload = response.read(RUN_SUMMARY_ARCHIVE_MAX_BYTES + 1)
    except ReleaseEvidenceRunnerError:
        raise
    except (OSError, urllib.error.URLError) as exc:
        _fail("artifact_download_failed", f"Actions artifact download failed: {exc}")
    if not payload or len(payload) > RUN_SUMMARY_ARCHIVE_MAX_BYTES:
        _fail("verifier_summary_invalid", "Actions artifact archive size is invalid")
    return payload


@dataclass(frozen=True)
class MiniBundle:
    root: Path
    asset_index: Path
    envelope: Path
    raw_export: Path
    verifier_report: Path
    locator_key: str
    file_digests: Mapping[str, str]


def _fail(code: str, message: str) -> None:
    raise ReleaseEvidenceRunnerError(code, message)


def _load_json_with_digest(path: Path, label: str) -> tuple[dict[str, Any], str]:
    try:
        payload = path.read_bytes()
        value = json.loads(payload.decode("utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail("invalid_json", f"{label}: {path}: {exc}")
    if not isinstance(value, dict):
        _fail("invalid_json", f"{label} root must be an object: {path}")
    return value, _sha256_hex(payload)


def _load_json(path: Path, label: str) -> dict[str, Any]:
    return _load_json_with_digest(path, label)[0]


def _sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _normalized_hex(value: Any, label: str) -> str:
    text = str(value)
    if text.startswith("sha256:"):
        text = text[7:]
    if ledger_contract.SHA256_RE.fullmatch(text) is None:
        _fail("invalid_digest", f"{label} is not a lowercase SHA-256")
    return text


def _safe_asset_name(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or Path(value).name != value:
        _fail("unsafe_asset_name", f"{label} must be one filename segment")
    return value


def _locator_key(locator: Mapping[str, Any]) -> str:
    return json.dumps(locator, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def external_records(release: Mapping[str, Any]) -> dict[str, Any]:
    ci = release.get("ci", {})
    receipts = release.get("receipts", {})
    governance = release.get("governance", {})
    marketplace = release.get("marketplace_source", {})
    canonical = ci.get("canonical_plugin_validator", {}) if isinstance(ci, Mapping) else {}
    return {
        "repository_preview_ci": ci.get("repository_preview") if isinstance(ci, Mapping) else None,
        "canonical_plugin_validator_ci": canonical.get("ci") if isinstance(canonical, Mapping) else None,
        "main_branch_protection": governance.get("main_branch_protection") if isinstance(governance, Mapping) else None,
        "marketplace_resolved_commit": marketplace.get("resolved_commit") if isinstance(marketplace, Mapping) else None,
        "marketplace_upgrade": receipts.get("marketplace_upgrade") if isinstance(receipts, Mapping) else None,
        "explicit_reinstall": receipts.get("explicit_reinstall") if isinstance(receipts, Mapping) else None,
        "fresh_task_discovery": receipts.get("fresh_task_discovery") if isinstance(receipts, Mapping) else None,
        "rollback": receipts.get("rollback") if isinstance(receipts, Mapping) else None,
    }


def _candidate_directories(root: Path) -> list[Path]:
    resolved = root.resolve(strict=True)
    if not resolved.is_dir():
        _fail("bundle_root_unavailable", f"bundle root is not a directory: {root}")
    candidates = [resolved]
    for child in sorted(resolved.iterdir(), key=lambda item: item.name):
        if not child.is_dir():
            continue
        candidate = child.resolve(strict=True)
        try:
            candidate.relative_to(resolved)
        except ValueError:
            _fail("bundle_root_escape", f"bundle directory escapes root: {child}")
        candidates.append(candidate)
    return candidates


def _indexed_record(
    index: Mapping[str, Any], locator_asset: Mapping[str, Any], expected_kind: str | None
) -> Mapping[str, Any]:
    assets = index.get("assets")
    if not isinstance(assets, list):
        _fail("invalid_asset_index", "asset index assets must be a list")
    asset_id = locator_asset.get("asset_id")
    matches = [
        item
        for item in assets
        if isinstance(item, Mapping) and item.get("asset_id") == asset_id
    ]
    if len(matches) != 1:
        _fail("asset_id_not_unique", f"asset id {asset_id!r} does not occur exactly once")
    record = matches[0]
    if record.get("name") != locator_asset.get("name"):
        _fail("asset_locator_mismatch", f"asset {asset_id} name differs from locator")
    if _normalized_hex(record.get("sha256"), f"asset {asset_id}") != locator_asset.get("sha256"):
        _fail("asset_locator_mismatch", f"asset {asset_id} digest differs from locator")
    if expected_kind is not None and record.get("evidence_kind") != expected_kind:
        _fail("asset_kind_mismatch", f"asset {asset_id} is not {expected_kind}")
    if expected_kind is None and record.get("evidence_kind") not in {
        "raw_export",
        "structured_export",
        "task_export",
    }:
        _fail("asset_kind_mismatch", f"asset {asset_id} is not a capture export")
    return record


def _validate_bundle_candidate(
    directory: Path, locator: Mapping[str, Any]
) -> MiniBundle:
    asset_names = {
        field: _safe_asset_name(locator.get(field, {}).get("name"), field)
        for field in (*ASSET_FIELDS, "release_asset_index_asset")
    }
    paths: dict[str, Path] = {}
    for field, name in asset_names.items():
        candidate = directory / name
        if not candidate.is_file() or candidate.is_symlink():
            _fail("bundle_files_missing", f"mini-bundle is incomplete: {directory}")
        resolved = candidate.resolve(strict=True)
        if resolved.parent != directory.resolve():
            _fail("bundle_root_escape", f"mini-bundle asset escapes: {candidate}")
        paths[field] = resolved
    index_path = paths["release_asset_index_asset"]
    index_bytes = index_path.read_bytes()
    if _sha256_hex(index_bytes) != locator["release_asset_index_asset"]["sha256"]:
        _fail("asset_digest_mismatch", f"Release asset index digest mismatch: {directory}")
    index = _load_json(index_path, "Release asset index")
    release = index.get("github_release", {})
    witness = index.get("github_witness", {})
    if not isinstance(release, Mapping) or not isinstance(witness, Mapping):
        _fail("invalid_asset_index", "GitHub release/witness is missing")
    if (
        release.get("repository") != locator.get("repository")
        or release.get("release_id") != locator.get("release_id")
        or release.get("release_tag") != locator.get("release_tag")
        or witness.get("workflow_run_id") != locator.get("capture_workflow_run_id")
    ):
        _fail("locator_mismatch", f"mini-bundle GitHub witness differs from locator: {directory}")

    for field, kind in ASSET_FIELDS.items():
        locator_asset = locator[field]
        record = _indexed_record(index, locator_asset, kind)
        payload = paths[field].read_bytes()
        if (
            _sha256_hex(payload) != locator_asset["sha256"]
            or len(payload) != record.get("size")
        ):
            _fail("asset_digest_mismatch", f"{field} bytes differ from locator/index")

    return MiniBundle(
        root=directory,
        asset_index=index_path,
        envelope=paths["envelope_asset"],
        raw_export=paths["raw_export_asset"],
        verifier_report=paths["verifier_report_asset"],
        locator_key=_locator_key(locator),
        file_digests={field: _sha256_hex(path.read_bytes()) for field, path in paths.items()},
    )


def _load_phase8_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "openai_phase8_live_verifier", PHASE8_VERIFIER_PATH
    )
    if spec is None or spec.loader is None:
        _fail("live_verifier_unavailable", "Phase 8 verifier could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validate_release_evidence_schema(errors: list[str]) -> None:
    path = ledger_contract.RELEASE_EVIDENCE_SCHEMA_PATH
    ledger_contract.require(path.is_file(), "release evidence schema is missing", errors)
    if not path.is_file():
        return
    try:
        schema = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"release evidence schema cannot be read: {type(exc).__name__}")
        return
    ledger_contract.require(
        isinstance(schema, Mapping), "release evidence schema is not an object", errors
    )
    if not isinstance(schema, Mapping):
        return
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    result_fields = {
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
    ledger_contract.require(
        result_fields <= required,
        "release evidence schema does not require the v3 callback contract",
        errors,
    )
    ledger_contract.require(
        isinstance(properties, Mapping)
        and properties.get("schema_version", {}).get("const") == 3,
        "release evidence schema_version is not 3",
        errors,
    )
    declared_types = (
        set(properties.get("evidence_type", {}).get("enum", []))
        if isinstance(properties, Mapping)
        else set()
    )
    ledger_contract.require(
        declared_types == EXPECTED_EVIDENCE_TYPES,
        "release evidence schema evidence types are stale",
        errors,
    )
    integrity = properties.get("integrity_result", {}) if isinstance(properties, Mapping) else {}
    integrity_properties = integrity.get("properties", {}) if isinstance(integrity, Mapping) else {}
    ledger_contract.require(
        integrity_properties.get("evidence_id", {}).get("minLength") == 1
        and integrity_properties.get(
            "claimed_counts_as_preview_acceptance", {}
        ).get("const")
        is True,
        "release evidence schema lacks required integrity claims",
        errors,
    )
    verifier = properties.get("live_verifier", {}) if isinstance(properties, Mapping) else {}
    verifier_properties = verifier.get("properties", {}) if isinstance(verifier, Mapping) else {}
    ledger_contract.require(
        verifier_properties.get("verified_at", {}).get("format") == "date-time",
        "release evidence schema lacks the verifier timestamp contract",
        errors,
    )
    evidence_contract = schema.get("x-evidence-contract", {})
    ledger_contract.require(
        isinstance(evidence_contract, Mapping)
        and bool(evidence_contract.get("live_requery_policy"))
        and bool(evidence_contract.get("adapter_digest_policy"))
        and bool(evidence_contract.get("integrity_boundary")),
        "release evidence schema lacks live-requery trust boundaries",
        errors,
    )


class _CallbackConstructionCapability:
    __slots__ = ()


_PRODUCTION_CALLBACK_CAPABILITY = _CallbackConstructionCapability()
_TEST_CALLBACK_CAPABILITY = _CallbackConstructionCapability()


class ReleaseEvidenceLiveCallback:
    """Ledger callback backed by one fixed registered live GitHub verifier."""

    adapter_id = ADAPTER_ID

    def __init__(
        self,
        bundle_root: Path,
        *,
        live_verifier: Callable[[Mapping[str, Any]], Mapping[str, Any]],
        github_run_fetcher: Callable[[str], Mapping[str, Any]],
        github_binary_fetcher: Callable[[str], bytes],
        phase8_module: Any,
        _capability: _CallbackConstructionCapability,
    ) -> None:
        if _capability not in {
            _PRODUCTION_CALLBACK_CAPABILITY,
            _TEST_CALLBACK_CAPABILITY,
        }:
            _fail(
                "callback_construction_forbidden",
                "release evidence callbacks must come from the production or test-only factory",
            )
        if isinstance(live_verifier, bool) or not callable(live_verifier):
            _fail("live_verifier_invalid", "live verifier must be the registered callable")
        if getattr(live_verifier, "adapter_id", None) != self.adapter_id:
            _fail("live_verifier_unregistered", "live verifier adapter id is not registered")
        if (
            _capability is _PRODUCTION_CALLBACK_CAPABILITY
            and live_verifier is not getattr(phase8_module, "verify", None)
        ):
            _fail(
                "live_verifier_unregistered",
                "production callback is not bound to the loaded committed Phase 8 verifier",
            )
        if isinstance(github_run_fetcher, bool) or not callable(github_run_fetcher):
            _fail("run_fetcher_invalid", "historical verifier run requires a GitHub API fetcher")
        if isinstance(github_binary_fetcher, bool) or not callable(github_binary_fetcher):
            _fail(
                "binary_fetcher_invalid",
                "historical verifier summary requires a GitHub artifact fetcher",
            )
        self.bundle_root = bundle_root.resolve(strict=True)
        self.candidate_directories = _candidate_directories(self.bundle_root)
        self.live_verifier = live_verifier
        self.github_run_fetcher = github_run_fetcher
        self.github_binary_fetcher = github_binary_fetcher
        self.phase8 = phase8_module
        self._bindings: dict[tuple[str, str], MiniBundle] = {}
        self._binding_scopes: dict[tuple[str, str], str] = {}
        self._used: set[tuple[str, str]] = set()
        self._audit_results: dict[tuple[str, str], dict[str, Any]] = {}
        self._run_summaries: dict[tuple[str, int], Mapping[str, Any]] = {}
        self._bound_locators: set[str] = set()
        self._bound_asset_paths: set[Path] = set()
        self._bound_asset_ids: set[tuple[str, int]] = set()
        self._verified_evidence_ids: set[str] = set()

    def _github_json(self, url: str, label: str) -> Mapping[str, Any]:
        try:
            response = self.github_run_fetcher(url)
        except Exception as exc:
            _fail(
                "github_live_requery_failed",
                f"{label} could not be re-queried: {type(exc).__name__}: {exc}",
            )
        if not isinstance(response, Mapping):
            _fail("github_live_requery_failed", f"{label} response is not an object")
        return response

    def _github_bytes(self, url: str, label: str) -> bytes:
        try:
            response = self.github_binary_fetcher(url)
        except Exception as exc:
            _fail(
                "github_live_requery_failed",
                f"{label} could not be downloaded: {type(exc).__name__}: {exc}",
            )
        if not isinstance(response, bytes):
            _fail("github_live_requery_failed", f"{label} response is not bytes")
        if not response or len(response) > RUN_SUMMARY_ARCHIVE_MAX_BYTES:
            _fail("verifier_summary_invalid", f"{label} archive size is invalid")
        return response

    def _parse_run_summary_archive(self, payload: bytes) -> Mapping[str, Any]:
        try:
            with zipfile.ZipFile(io.BytesIO(payload), "r") as archive:
                members = archive.infolist()
                if archive.comment or len(members) != 1:
                    _fail(
                        "verifier_summary_invalid",
                        "verifier summary ZIP must contain exactly one uncommented member",
                    )
                member = members[0]
                if (
                    member.filename != RUN_SUMMARY_JSON_NAME
                    or member.is_dir()
                    or member.flag_bits & 0x1
                    or member.file_size <= 0
                    or member.file_size > RUN_SUMMARY_JSON_MAX_BYTES
                ):
                    _fail(
                        "verifier_summary_invalid",
                        "verifier summary ZIP member is unsafe or oversized",
                    )
                document_bytes = archive.read(member)
        except ReleaseEvidenceRunnerError:
            raise
        except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
            _fail("verifier_summary_invalid", f"verifier summary ZIP is invalid: {exc}")
        try:
            document = json.loads(document_bytes.decode("utf-8-sig"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            _fail("verifier_summary_invalid", f"verifier summary JSON is invalid: {exc}")
        if not isinstance(document, Mapping):
            _fail("verifier_summary_invalid", "verifier summary root is not an object")
        return document

    def _load_run_summary(self, repository: str, run_id: int) -> Mapping[str, Any]:
        key = (repository, run_id)
        cached = self._run_summaries.get(key)
        if cached is not None:
            return cached
        artifact_name = f"{RUN_SUMMARY_ARTIFACT_PREFIX}{run_id}"
        artifacts_url = (
            f"https://api.github.com/repos/{repository}/actions/runs/{run_id}/artifacts"
        )
        listing = self._github_json(artifacts_url, "historical verifier artifacts")
        artifacts = listing.get("artifacts")
        total_count = listing.get("total_count")
        if (
            not isinstance(artifacts, list)
            or isinstance(total_count, bool)
            or not isinstance(total_count, int)
            or total_count != len(artifacts)
            or total_count > 30
        ):
            _fail(
                "verifier_summary_invalid",
                "historical verifier artifact listing is incomplete or oversized",
            )
        matches = [
            item
            for item in artifacts
            if isinstance(item, Mapping) and item.get("name") == artifact_name
        ]
        if len(matches) != 1:
            _fail(
                "verifier_summary_invalid",
                "historical verifier run has no unique summary artifact",
            )
        artifact = matches[0]
        artifact_id = artifact.get("id")
        artifact_size = artifact.get("size_in_bytes")
        artifact_digest = artifact.get("digest")
        artifact_workflow_run = artifact.get("workflow_run")
        if (
            not isinstance(artifact_id, int)
            or isinstance(artifact_id, bool)
            or artifact_id <= 0
            or not isinstance(artifact_size, int)
            or isinstance(artifact_size, bool)
            or artifact_size <= 0
            or artifact_size > RUN_SUMMARY_ARCHIVE_MAX_BYTES
            or not isinstance(artifact_digest, str)
            or not artifact_digest.startswith("sha256:")
            or ledger_contract.SHA256_RE.fullmatch(
                artifact_digest.removeprefix("sha256:")
            )
            is None
            or artifact.get("expired") is not False
            or not isinstance(artifact_workflow_run, Mapping)
            or artifact_workflow_run.get("id") != run_id
        ):
            _fail(
                "verifier_summary_invalid",
                "historical verifier summary artifact is expired or misbound",
            )
        archive_url = (
            f"https://api.github.com/repos/{repository}/actions/artifacts/{artifact_id}/zip"
        )
        if artifact.get("archive_download_url") != archive_url:
            _fail(
                "verifier_summary_invalid",
                "historical verifier summary archive URL is not canonical",
            )
        archive_payload = self._github_bytes(
            archive_url, "historical verifier summary"
        )
        if "sha256:" + _sha256_hex(archive_payload) != artifact_digest:
            _fail(
                "verifier_summary_invalid",
                "historical verifier summary archive digest differs from GitHub",
            )
        summary = self._parse_run_summary_archive(archive_payload)
        self._run_summaries[key] = summary
        return summary

    def _verify_summary_binding(
        self,
        summary: Mapping[str, Any],
        *,
        repository: str,
        run_id: int,
        evidence_type: str,
        locator: Mapping[str, Any],
        expected_source_identity: Mapping[str, Any],
    ) -> None:
        required = {
            "schema_version",
            "run_id",
            "repository",
            "release_id",
            "release_tag",
            "source_commit",
            "workflow_path",
            "workflow_event",
            "bundles",
        }
        if set(summary) != required or (
            summary.get("schema_version") != RUN_SUMMARY_SCHEMA
            or summary.get("run_id") != run_id
            or summary.get("repository") != repository
            or summary.get("release_id") != locator.get("release_id")
            or summary.get("release_tag") != locator.get("release_tag")
            or summary.get("source_commit")
            != expected_source_identity.get("source_commit")
            or summary.get("workflow_path")
            != ".github/workflows/openai-preview-evidence.yml"
            or summary.get("workflow_event") != "workflow_dispatch"
        ):
            _fail(
                "verifier_summary_mismatch",
                "historical verifier summary does not bind the run and Release",
            )
        bundles = summary.get("bundles")
        if not isinstance(bundles, list) or not bundles or len(bundles) > 1000:
            _fail("verifier_summary_invalid", "verifier summary bundles are invalid")
        asset_fields = {
            "envelope_asset",
            "release_asset_index_asset",
            "raw_export_asset",
            "verifier_report_asset",
        }
        expected_bundle = {
            "evidence_type": evidence_type,
            "verdict": PREVIEW_ATTESTED,
            "provider_verified": False,
            "release_identity": {
                "repository": repository,
                "release_id": locator.get("release_id"),
                "release_tag": locator.get("release_tag"),
            },
            **{
                field: copy.deepcopy(locator[field]) for field in sorted(asset_fields)
            },
        }
        seen_bundle_keys: set[str] = set()
        matches = 0
        for index, bundle_record in enumerate(bundles):
            if not isinstance(bundle_record, Mapping) or set(bundle_record) != {
                "evidence_type",
                "verdict",
                "provider_verified",
                "release_identity",
                *asset_fields,
            }:
                _fail(
                    "verifier_summary_invalid",
                    f"verifier summary bundle {index} has undeclared fields",
                )
            if (
                not isinstance(bundle_record.get("evidence_type"), str)
                or not bundle_record.get("evidence_type")
                or bundle_record.get("verdict") != PREVIEW_ATTESTED
                or bundle_record.get("provider_verified") is not False
            ):
                _fail(
                    "verifier_summary_invalid",
                    f"verifier summary bundle {index} has an invalid verdict",
                )
            release_identity = bundle_record.get("release_identity")
            if (
                not isinstance(release_identity, Mapping)
                or set(release_identity)
                != {"repository", "release_id", "release_tag"}
                or release_identity.get("repository") != summary.get("repository")
                or release_identity.get("release_id") != summary.get("release_id")
                or release_identity.get("release_tag") != summary.get("release_tag")
            ):
                _fail(
                    "verifier_summary_invalid",
                    f"verifier summary bundle {index} has a mismatched Release identity",
                )
            asset_ids: set[int] = set()
            asset_names: set[str] = set()
            for field in asset_fields:
                asset = bundle_record.get(field)
                if not isinstance(asset, Mapping) or set(asset) != {
                    "asset_id",
                    "name",
                    "sha256",
                }:
                    _fail(
                        "verifier_summary_invalid",
                        f"verifier summary bundle {index} {field} is malformed",
                    )
                asset_id = asset.get("asset_id")
                name = asset.get("name")
                digest = asset.get("sha256")
                if (
                    not isinstance(asset_id, int)
                    or isinstance(asset_id, bool)
                    or asset_id <= 0
                    or not isinstance(name, str)
                    or not name
                    or Path(name).name != name
                    or ledger_contract.SHA256_RE.fullmatch(str(digest)) is None
                    or asset_id in asset_ids
                    or name in asset_names
                ):
                    _fail(
                        "verifier_summary_invalid",
                        f"verifier summary bundle {index} assets are invalid or reused",
                    )
                asset_ids.add(asset_id)
                asset_names.add(name)
            bundle_key = json.dumps(
                {field: bundle_record[field] for field in sorted(asset_fields)},
                sort_keys=True,
                separators=(",", ":"),
            )
            if bundle_key in seen_bundle_keys:
                _fail("verifier_summary_invalid", "verifier summary repeats a bundle")
            seen_bundle_keys.add(bundle_key)
            if dict(bundle_record) == expected_bundle:
                matches += 1
        if matches != 1:
            _fail(
                "verifier_summary_mismatch",
                f"historical verifier summary does not uniquely bind {evidence_type}",
            )

    def _verify_current_branch_protection(
        self,
        repository: str,
        record: Mapping[str, Any],
        source_commit: str,
    ) -> None:
        if (
            record.get("branch") != "main"
            or record.get("required_check") != "OpenAI Plugin Preview / validate"
        ):
            _fail(
                "branch_protection_record_invalid",
                "ledger branch-protection observation does not name the required main check",
            )
        url = f"https://api.github.com/repos/{repository}/branches/main/protection"
        protection = self._github_json(url, "current main branch protection")
        required = protection.get("required_status_checks")
        if not isinstance(required, Mapping):
            _fail(
                "branch_protection_not_enforced",
                "main has no required status-check protection",
            )
        contexts = required.get("contexts", [])
        checks = required.get("checks", [])
        if contexts is not None and not isinstance(contexts, list):
            _fail(
                "branch_protection_not_enforced",
                "main branch protection contexts are malformed",
            )
        check_matches = [
            item
            for item in checks
            if isinstance(item, Mapping)
            and item.get("context") == "OpenAI Plugin Preview / validate"
            and isinstance(item.get("app_id"), int)
            and not isinstance(item.get("app_id"), bool)
            and item.get("app_id") > 0
        ] if isinstance(checks, list) else []
        if len(check_matches) != 1:
            _fail(
                "branch_protection_not_enforced",
                "main does not bind the required Preview check to one GitHub App",
            )
        app_id = check_matches[0]["app_id"]
        expected_job_name = str(record["required_check"]).rsplit(" / ", 1)[-1]
        check_runs_url = (
            f"https://api.github.com/repos/{repository}/commits/{source_commit}/check-runs"
        )
        check_run_response = self._github_json(
            check_runs_url, "source-commit Preview check runs"
        )
        check_runs = check_run_response.get("check_runs")
        total_count = check_run_response.get("total_count")
        if (
            not isinstance(check_runs, list)
            or isinstance(total_count, bool)
            or not isinstance(total_count, int)
            or total_count != len(check_runs)
            or total_count > 30
        ):
            _fail(
                "branch_protection_check_run_invalid",
                "source-commit check-run listing is incomplete or oversized",
            )
        successful_matches = []
        for check_run in check_runs:
            app = check_run.get("app") if isinstance(check_run, Mapping) else None
            if (
                isinstance(check_run, Mapping)
                and check_run.get("name") == expected_job_name
                and check_run.get("head_sha") == source_commit
                and check_run.get("status") == "completed"
                and check_run.get("conclusion") == "success"
                and isinstance(app, Mapping)
                and app.get("id") == app_id
                and app.get("slug") == "github-actions"
            ):
                successful_matches.append(check_run)
        if not successful_matches:
            _fail(
                "branch_protection_check_run_invalid",
                "the protected Preview check has no successful GitHub Actions run on the source commit",
            )

    def _bind_record(
        self,
        evidence_type: str,
        record: Mapping[str, Any],
        label: str,
        *,
        release_scope: str,
    ) -> str:
        if record.get("status") != PREVIEW_ATTESTED:
            _fail("external_record_not_preview", f"{label} is not preview_attested")
        locator = record.get("evidence_locator")
        if not isinstance(locator, Mapping):
            _fail("locator_missing", f"{label} locator is missing")
        locator_errors: list[str] = []
        ledger_contract.validate_external_evidence_locator(
            locator, label, locator_errors
        )
        if locator_errors:
            _fail("locator_invalid", "; ".join(locator_errors))
        key = _locator_key(locator)
        if key in self._bound_locators:
            _fail("duplicate_locator", f"locator reused by {label}")
        repository = str(locator.get("repository", ""))
        locator_asset_ids = {
            (repository, int(locator[field]["asset_id"]))
            for field in (
                "envelope_asset",
                "release_asset_index_asset",
                "raw_export_asset",
                "verifier_report_asset",
            )
        }
        if locator_asset_ids & self._bound_asset_ids:
            _fail("duplicate_bundle", f"GitHub evidence assets reused by {label}")

        matches: list[MiniBundle] = []
        candidate_errors: list[str] = []
        index_name = _safe_asset_name(
            locator["release_asset_index_asset"]["name"],
            f"{label}.release_asset_index_asset",
        )
        for directory in self.candidate_directories:
            if not (directory / index_name).is_file():
                continue
            try:
                matches.append(_validate_bundle_candidate(directory, locator))
            except ReleaseEvidenceRunnerError as exc:
                candidate_errors.append(str(exc))
        if not matches:
            detail = f": {'; '.join(candidate_errors)}" if candidate_errors else ""
            _fail("bundle_not_found", f"no mini-bundle matched {label}{detail}")
        if len(matches) != 1:
            _fail("duplicate_bundle", f"multiple mini-bundles matched {label}")
        bundle = matches[0]
        bundle_asset_paths = {
            bundle.asset_index,
            bundle.envelope,
            bundle.raw_export,
            bundle.verifier_report,
        }
        if bundle_asset_paths & self._bound_asset_paths:
            _fail("duplicate_bundle", f"mini-bundle assets reused by {label}")
        self._bound_asset_paths.update(bundle_asset_paths)
        self._bound_asset_ids.update(locator_asset_ids)
        self._bound_locators.add(key)
        binding_key = (evidence_type, key)
        self._bindings[binding_key] = bundle
        self._binding_scopes[binding_key] = release_scope
        return repository

    def prepare_current_release(self, release: Mapping[str, Any]) -> None:
        records = external_records(release)
        if set(records) != EXPECTED_EVIDENCE_TYPES:
            _fail("evidence_type_coverage", "current release does not expose exactly eight types")
        repositories: set[str] = set()
        for evidence_type in sorted(EXPECTED_EVIDENCE_TYPES):
            record = records[evidence_type]
            if not isinstance(record, Mapping):
                _fail("external_record_missing", f"{evidence_type} record is missing")
            repository = self._bind_record(
                evidence_type,
                record,
                evidence_type,
                release_scope="current",
            )
            repositories.add(repository)

        if len(self._bindings) != len(EXPECTED_EVIDENCE_TYPES):
            _fail("evidence_type_coverage", "not all eight evidence types were bound")
        if len(repositories) != 1:
            _fail(
                "locator_repository_mismatch",
                "the eight external records do not bind one repository",
            )
        branch_record = records["main_branch_protection"]
        assert isinstance(branch_record, Mapping)
        source_commit = release.get("source_commit", {})
        source_sha = (
            source_commit.get("sha") if isinstance(source_commit, Mapping) else None
        )
        if not isinstance(source_sha, str) or ledger_contract.COMMIT_SHA_RE.fullmatch(source_sha) is None:
            _fail("branch_protection_record_invalid", "release source commit is invalid")
        self._verify_current_branch_protection(
            next(iter(repositories)), branch_record, source_sha
        )

    def prepare_historical_release(
        self, release: Mapping[str, Any], label: str
    ) -> None:
        for evidence_type, record in sorted(external_records(release).items()):
            if not isinstance(record, Mapping):
                continue
            if record.get("status") in ledger_contract.EXTERNAL_ACCEPTED_STATUS:
                self._bind_record(
                    evidence_type,
                    record,
                    f"{label}.{evidence_type}",
                    release_scope=label,
                )

    def prepare_ledger(self, ledger: Mapping[str, Any]) -> None:
        release = ledger.get("release")
        if not isinstance(release, Mapping):
            _fail("release_missing", "current release is missing")
        self.prepare_current_release(release)
        previous_releases = ledger.get("previous_releases", [])
        if not isinstance(previous_releases, list):
            _fail("previous_releases_invalid", "previous_releases is not a list")
        for index, previous in enumerate(previous_releases):
            if isinstance(previous, Mapping):
                self.prepare_historical_release(
                    previous, f"previous_releases[{index}]"
                )

    def _verify_historical_verifier_run(
        self,
        evidence_type: str,
        locator: Mapping[str, Any],
        expected_source_identity: Mapping[str, Any],
    ) -> None:
        repository = str(locator.get("repository", ""))
        run_id = locator.get("verifier_workflow_run_id")
        workflow_url = (
            f"https://api.github.com/repos/{repository}/actions/workflows/"
            "openai-preview-evidence.yml"
        )
        api_url = f"https://api.github.com/repos/{repository}/actions/runs/{run_id}"
        workflow = self._github_json(workflow_url, "Preview evidence workflow")
        run = self._github_json(api_url, "historical Preview evidence run")
        workflow_id = workflow.get("id")
        if (
            not isinstance(workflow_id, int)
            or isinstance(workflow_id, bool)
            or workflow_id <= 0
            or workflow.get("url")
            != f"https://api.github.com/repos/{repository}/actions/workflows/{workflow_id}"
            or workflow.get("path") != ".github/workflows/openai-preview-evidence.yml"
            or workflow.get("state") != "active"
        ):
            _fail(
                "verifier_run_invalid",
                "GitHub does not expose one active OpenAI Preview evidence workflow",
            )
        workflow_path = str(run.get("path", "")).split("@", 1)[0]
        run_repository = run.get("repository", {})
        if (
            run.get("id") != run_id
            or run.get("url") != api_url
            or run.get("html_url") != locator.get("verifier_run_url")
            or not isinstance(run_repository, Mapping)
            or run_repository.get("full_name") != repository
            or run.get("workflow_id") != workflow_id
            or workflow_path != ".github/workflows/openai-preview-evidence.yml"
            or run.get("event") != "workflow_dispatch"
            or run.get("status") != "completed"
            or run.get("conclusion") != "success"
            or run.get("head_sha") != expected_source_identity.get("source_commit")
        ):
            _fail(
                "verifier_run_witness_mismatch",
                "historical verifier run does not match workflow, repository, source commit, and successful completion",
            )
        summary = self._load_run_summary(repository, int(run_id))
        self._verify_summary_binding(
            summary,
            repository=repository,
            run_id=int(run_id),
            evidence_type=evidence_type,
            locator=locator,
            expected_source_identity=expected_source_identity,
        )

    def _snapshot_unchanged(
        self, bundle: MiniBundle, locator: Mapping[str, Any]
    ) -> dict[str, bytes]:
        paths = {
            "release_asset_index_asset": bundle.asset_index,
            "envelope_asset": bundle.envelope,
            "raw_export_asset": bundle.raw_export,
            "verifier_report_asset": bundle.verifier_report,
        }
        snapshot: dict[str, bytes] = {}
        for field, path in paths.items():
            payload = path.read_bytes()
            actual_digest = _sha256_hex(payload)
            if actual_digest != bundle.file_digests[field]:
                _fail("bundle_changed_after_match", f"{field} changed after preflight")
            if actual_digest != locator[field]["sha256"]:
                _fail("asset_digest_mismatch", f"{field} no longer matches locator")
            snapshot[field] = payload
        return snapshot

    def __call__(
        self,
        *,
        evidence_locator: Mapping[str, Any],
        evidence_type: str,
        expected_source_identity: Mapping[str, Any],
        expected_adapter_id: str,
        expected_verification_level: str,
    ) -> dict[str, Any]:
        if (
            evidence_type not in EXPECTED_EVIDENCE_TYPES
            or expected_adapter_id != self.adapter_id
            or expected_verification_level != PREVIEW_ATTESTED
        ):
            _fail("live_request_mismatch", "ledger callback request is outside Preview scope")
        key = (evidence_type, _locator_key(evidence_locator))
        bundle = self._bindings.get(key)
        if bundle is None:
            _fail("bundle_not_bound", f"no preflight binding for {evidence_type}")
        release_scope = self._binding_scopes.get(key)
        if release_scope is None:
            _fail(
                "audit_scope_missing",
                f"no release scope was recorded for {evidence_type}",
            )
        if key in self._used:
            _fail("bundle_reused", f"live verifier invoked twice for {evidence_type}")
        self._snapshot_unchanged(bundle, evidence_locator)
        self._verify_historical_verifier_run(
            evidence_type, evidence_locator, expected_source_identity
        )

        with tempfile.TemporaryDirectory(prefix="release-evidence-identity-") as temp:
            identity_path = Path(temp) / "source-identity.json"
            identity_path.write_text(
                json.dumps(
                    {"source_identity": dict(expected_source_identity)},
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            request = self.phase8.build_request_from_bundle(
                evidence_root=bundle.root,
                asset_index_path=bundle.asset_index.name,
                envelope_path=bundle.envelope.name,
                expected_source_identity_path=identity_path,
            )
        result = self.live_verifier(request)
        if not isinstance(result, Mapping):
            _fail("live_result_invalid", "live verifier result is not an object")
        if (
            result.get("schema_version") != 3
            or result.get("synthetic_self_test") is not False
            or result.get("gate_eligible") is not True
            or result.get("counts_as_preview_attested") is not True
            or result.get("counts_as_provider_verified") is not False
            or result.get("verification_level") != PREVIEW_ATTESTED
            or result.get("provider_verified") is not False
            or result.get("adapter_id") != self.adapter_id
        ):
            _fail("live_result_not_gate_eligible", "live verifier did not return real Preview v3")
        integrity_result = result.get("integrity_result")
        evidence_id = (
            integrity_result.get("evidence_id")
            if isinstance(integrity_result, Mapping)
            else None
        )
        if (
            not isinstance(evidence_id, str)
            or not evidence_id.strip()
            or evidence_id in self._verified_evidence_ids
        ):
            _fail(
                "live_result_evidence_id_invalid",
                "live verifier evidence_id is missing or reused across bound records",
            )

        result_identity = result.get("source_identity")
        if not isinstance(result_identity, Mapping):
            _fail("live_result_identity_mismatch", "live result source identity is missing")
        for field, expected in expected_source_identity.items():
            actual = result_identity.get(field)
            if field.endswith("_sha256"):
                actual = str(actual).removeprefix("sha256:")
            if actual != expected:
                _fail("live_result_identity_mismatch", f"live result differs at {field}")

        verified_assets = result.get("verified_assets")
        if not isinstance(verified_assets, list):
            _fail("live_result_assets_missing", "live result has no verified asset inventory")
        verified_by_id: dict[int, Mapping[str, Any]] = {}
        for item in verified_assets:
            if not isinstance(item, Mapping):
                _fail("live_result_assets_missing", "verified asset entry is not an object")
            asset_id = item.get("asset_id")
            if not isinstance(asset_id, int) or isinstance(asset_id, bool) or asset_id in verified_by_id:
                _fail("live_result_assets_duplicate", "verified asset IDs are invalid or duplicated")
            verified_by_id[asset_id] = item
        for field in (*ASSET_FIELDS, "release_asset_index_asset"):
            expected_asset = evidence_locator[field]
            actual_asset = verified_by_id.get(expected_asset["asset_id"])
            if (
                actual_asset is None
                or actual_asset.get("name") != expected_asset["name"]
                or _normalized_hex(
                    actual_asset.get("sha256"), f"live result {field}"
                )
                != expected_asset["sha256"]
                or actual_asset.get("state") != "uploaded"
            ):
                _fail("live_result_locator_mismatch", f"live verified {field} differs from locator")

        # The live verifier compared its authenticated downloads with these
        # local staging bytes. Re-check immediately before parsing the raw
        # export so a concurrent local rewrite cannot alter the ledger result.
        verified_snapshot = self._snapshot_unchanged(bundle, evidence_locator)
        with tempfile.TemporaryDirectory(prefix="release-evidence-raw-snapshot-") as temp:
            raw_snapshot = Path(temp) / bundle.raw_export.name
            raw_snapshot.write_bytes(verified_snapshot["raw_export_asset"])
            raw_export = self.phase8.raw_header(raw_snapshot)
        live_verifier_metadata = copy.deepcopy(result.get("live_verifier"))
        if not isinstance(live_verifier_metadata, dict):
            _fail("live_result_invalid", "live verifier metadata is missing")
        # The Phase 8 verifier reports the runner's current Actions execution.
        # The durable ledger locator instead names the completed historical
        # evidence workflow that produced the mini-bundle, independently
        # re-queried above. Preserve that historical witness for ledger binding.
        live_verifier_metadata["verifier_workflow_run_id"] = evidence_locator[
            "verifier_workflow_run_id"
        ]
        live_verifier_metadata["verifier_run_url"] = evidence_locator[
            "verifier_run_url"
        ]
        validated_result = {
            "schema_version": result.get("schema_version"),
            "evidence_type": raw_export.get("evidence_type"),
            "verification_level": result.get("verification_level"),
            "provider_verified": result.get("provider_verified"),
            "observed": copy.deepcopy(raw_export.get("observed")),
            "raw_export": copy.deepcopy(raw_export),
            "source_identity": copy.deepcopy(dict(expected_source_identity)),
            "locator": copy.deepcopy(dict(evidence_locator)),
            "integrity_result": copy.deepcopy(result.get("integrity_result")),
            "live_verifier": live_verifier_metadata,
            "gate_eligibility": copy.deepcopy(result.get("gate_eligibility")),
        }
        result_payload = json.dumps(
            validated_result,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        locator_payload = json.dumps(
            dict(evidence_locator),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self._audit_results[key] = {
            "evidence_type": evidence_type,
            "evidence_id": evidence_id,
            "release_scope": release_scope,
            "verification_level": PREVIEW_ATTESTED,
            "provider_verified": False,
            "source_commit": expected_source_identity.get("source_commit"),
            "locator_sha256": "sha256:" + _sha256_hex(locator_payload),
            "validated_result_sha256": "sha256:" + _sha256_hex(result_payload),
            "verified_asset_ids": sorted(verified_by_id),
            "verifier_workflow_run_id": live_verifier_metadata.get(
                "verifier_workflow_run_id"
            ),
            "verified_at": live_verifier_metadata.get("verified_at"),
        }
        self._verified_evidence_ids.add(evidence_id)
        self._used.add(key)
        return validated_result

    def assert_complete(self) -> None:
        expected = set(self._bindings)
        if self._used != expected:
            missing = sorted(evidence_type for evidence_type, key in expected - self._used)
            _fail("evidence_type_coverage", f"live verifier did not consume: {missing}")

    def audit_results(self) -> list[dict[str, Any]]:
        """Return the current release's eight compact live results.

        Historical accepted records can repeat a current evidence type, so the
        audit ledger is keyed by the complete bound locator and filtered by the
        immutable scope assigned during preflight. This method intentionally
        preserves the eight-item ``live_results`` contract consumed by the
        protected accepted-run summary.
        """

        self.assert_complete()
        if set(self._audit_results) != set(self._bindings):
            _fail(
                "evidence_type_coverage",
                "live verifier audit results do not cover every bound record",
            )
        current_keys = {
            key for key, scope in self._binding_scopes.items() if scope == "current"
        }
        if (
            len(current_keys) != len(EXPECTED_EVIDENCE_TYPES)
            or {evidence_type for evidence_type, _ in current_keys}
            != EXPECTED_EVIDENCE_TYPES
        ):
            _fail(
                "evidence_type_coverage",
                "current live verifier results do not cover exactly eight evidence types",
            )
        ordered_keys = sorted(current_keys, key=lambda item: item[0])
        for key in ordered_keys:
            if self._audit_results[key].get("release_scope") != "current":
                _fail(
                    "audit_scope_mismatch",
                    f"current audit result is misbound for {key[0]}",
                )
        return [
            copy.deepcopy(self._audit_results[key]) for key in ordered_keys
        ]

    def history_audit_results(self) -> list[dict[str, Any]]:
        """Return accepted historical records without replacing current results."""

        self.assert_complete()
        if set(self._audit_results) != set(self._bindings):
            _fail(
                "evidence_type_coverage",
                "live verifier audit results do not cover every bound record",
            )
        history_keys = {
            key for key, scope in self._binding_scopes.items() if scope != "current"
        }
        ordered_keys = sorted(
            history_keys,
            key=lambda item: (self._binding_scopes[item], item[0], item[1]),
        )
        for key in ordered_keys:
            expected_scope = self._binding_scopes[key]
            if self._audit_results[key].get("release_scope") != expected_scope:
                _fail(
                    "audit_scope_mismatch",
                    f"historical audit result is misbound for {key[0]}",
                )
        return [
            copy.deepcopy(self._audit_results[key]) for key in ordered_keys
        ]


def validate_ledger_with_live_bundles(
    ledger: Mapping[str, Any], callback: ReleaseEvidenceLiveCallback
) -> list[str]:
    """Run current/previous release validation and rollback binding with callback."""

    errors: list[str] = []
    if not isinstance(ledger, Mapping):
        return ["ledger is not an object"]
    release = ledger.get("release")
    if not isinstance(release, dict):
        return ["release is not an object"]
    callback.prepare_ledger(ledger)
    ledger_contract.validate_all_sha_fields(dict(ledger), "ledger", errors)
    _validate_release_evidence_schema(errors)

    manifest = _load_json(MANIFEST_PATH, "plugin manifest")
    registry = yaml.safe_load((PLUGIN / "workflow-registry.yaml").read_text(encoding="utf-8-sig"))
    if not isinstance(registry, dict):
        return ["workflow registry is not an object"]
    ledger_contract.require(ledger.get("schema_version") == 1, "ledger schema_version must be 1", errors)
    ledger_contract.require(ledger.get("plugin") == manifest.get("name"), "ledger plugin identity mismatch", errors)
    ledger_contract.require(
        ledger.get("external_evidence_schema")
        == ledger_contract.RELEASE_EVIDENCE_SCHEMA_PATH.relative_to(REPO).as_posix(),
        "ledger external evidence schema path is stale",
        errors,
    )
    ledger_contract.require(release.get("version") == manifest.get("version"), "ledger version differs from manifest", errors)
    ledger_contract.require(registry.get("plugin_version") == manifest.get("version"), "registry version differs from manifest", errors)

    file_count, tree_digest = normalized_skill_tree_digest(PLUGIN / "skills")
    tree = release.get("installable_skill_tree", {})
    ledger_contract.require(tree.get("root") == "skills/", "ledger skill-tree root mismatch", errors)
    ledger_contract.require(tree.get("algorithm") == SKILL_TREE_ALGORITHM, "ledger skill-tree algorithm mismatch", errors)
    ledger_contract.require(tree.get("file_count") == file_count, "ledger skill-tree file count is stale", errors)
    ledger_contract.require(tree.get("sha256") == tree_digest, "ledger skill-tree digest is stale", errors)
    ledger_contract.validate_validation_contract_tree_record(release, errors)

    contracts = release.get("installable_contracts", {})
    for field, path in (
        ("manifest_sha256", MANIFEST_PATH),
        ("registry_sha256", PLUGIN / "workflow-registry.yaml"),
        ("license_sha256", PLUGIN / "LICENSE"),
        ("provenance_sha256", PLUGIN / "PROVENANCE.yaml"),
    ):
        ledger_contract.require(
            contracts.get(field) == normalized_file_digest(path),
            f"ledger {field} is stale",
            errors,
        )
    ledger_contract.require(
        contracts.get("registry_schema_version") == registry.get("schema_version"),
        "ledger registry schema is stale",
        errors,
    )

    marketplace = _load_json(REPO / ".agents" / "plugins" / "marketplace.json", "marketplace")
    marketplace_matches = [
        item
        for item in marketplace.get("plugins", [])
        if isinstance(item, Mapping) and item.get("name") == manifest.get("name")
    ]
    ledger_contract.require(len(marketplace_matches) == 1, "marketplace plugin entry is not unique", errors)
    source = release.get("marketplace_source", {})
    if len(marketplace_matches) == 1 and isinstance(source, Mapping):
        expected_source = {
            "source": source.get("source"),
            "url": source.get("url"),
            "path": source.get("path"),
            "ref": source.get("ref"),
        }
        ledger_contract.require(
            marketplace_matches[0].get("source") == expected_source,
            "ledger marketplace source is stale",
            errors,
        )
        ledger_contract.require(
            source.get("marketplace_name") == marketplace.get("name"),
            "ledger marketplace name mismatch",
            errors,
        )

    public_policy = registry.get("public_entry_policy", {})
    declared_entries = public_policy.get("declared_entries", [])
    implicit_entries = public_policy.get("implicit_active_entries", [])
    ledger_contract.require(
        len(registry.get("skills", [])) == 49,
        "release discovery baseline must contain 49 skills",
        errors,
    )
    ledger_contract.require(
        isinstance(declared_entries, list)
        and len(declared_entries) == 7
        and len(set(declared_entries)) == 7,
        "release discovery baseline must contain 7 unique explicit entries",
        errors,
    )
    ledger_contract.require(
        isinstance(implicit_entries, list)
        and len(implicit_entries) in {6, 7}
        and len(set(implicit_entries)) == len(implicit_entries)
        and set(implicit_entries) <= set(declared_entries),
        "release discovery baseline must contain 6 or 7 valid implicit entries",
        errors,
    )
    ledger_contract.validate_release_evidence(
        release,
        str(release.get("version", "")),
        len(registry.get("skills", [])),
        errors,
        authenticated_external_adapter=(
            ledger_contract.authenticated_external_evidence_adapter_available(release)
        ),
        expected_explicit_entries=declared_entries,
        expected_implicit_entries=implicit_entries,
        live_evidence_verifier=callback,
    )
    ledger_contract.validate_verified_source_commit_tree(release, errors)

    previous_releases = ledger.get("previous_releases", [])
    ledger_contract.require(isinstance(previous_releases, list), "previous_releases is not a list", errors)
    if isinstance(previous_releases, list):
        for index, previous in enumerate(previous_releases):
            label = f"previous_releases[{index}]"
            ledger_contract.require(isinstance(previous, dict), f"{label} is not an object", errors)
            if not isinstance(previous, dict):
                continue
            ledger_contract.validate_release_evidence(
                previous,
                str(previous.get("version", "")),
                None,
                errors,
                prefix=f"{label}.",
                authenticated_external_adapter=(
                    ledger_contract.authenticated_external_evidence_adapter_available(previous)
                ),
                live_evidence_verifier=callback,
            )
            ledger_contract.validate_verified_source_commit_tree(previous, errors, label)
        ledger_contract.validate_rollback_history_binding(release, previous_releases, errors)

    root_license = REPO / "LICENSE"
    plugin_license = PLUGIN / "LICENSE"
    ledger_contract.require(plugin_license.is_file(), "installable plugin LICENSE is missing", errors)
    if plugin_license.is_file() and root_license.is_file():
        ledger_contract.require(plugin_license.read_bytes() == root_license.read_bytes(), "plugin LICENSE differs from repository MIT license", errors)
    ledger_contract.require(manifest.get("license") == "MIT", "manifest license is not MIT", errors)
    ledger_contract.validate_provenance(registry, errors)
    if not errors:
        callback.assert_complete()
    return errors


def create_production_callback(bundle_root: Path) -> ReleaseEvidenceLiveCallback:
    """Construct the only production callback from the committed verifier module."""

    phase8 = _load_phase8_module()
    return ReleaseEvidenceLiveCallback(
        bundle_root,
        live_verifier=phase8.verify,
        github_run_fetcher=lambda url: phase8.github_request(url, binary=False),
        github_binary_fetcher=download_github_actions_artifact,
        phase8_module=phase8,
        _capability=_PRODUCTION_CALLBACK_CAPABILITY,
    )


def _create_test_callback(
    bundle_root: Path,
    *,
    live_verifier: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    github_run_fetcher: Callable[[str], Mapping[str, Any]],
    github_binary_fetcher: Callable[[str], bytes],
    phase8_module: Any,
) -> ReleaseEvidenceLiveCallback:
    """Test-only transport seam; production code must use create_production_callback."""

    return ReleaseEvidenceLiveCallback(
        bundle_root,
        live_verifier=live_verifier,
        github_run_fetcher=github_run_fetcher,
        github_binary_fetcher=github_binary_fetcher,
        phase8_module=phase8_module,
        _capability=_TEST_CALLBACK_CAPABILITY,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Live-verify eight GitHub Release evidence mini-bundles against the current ledger."
    )
    parser.add_argument("--bundle-root", required=True)
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = _build_parser().parse_args(argv)
        ledger_path = Path(args.ledger).resolve(strict=True)
        ledger, ledger_sha256 = _load_json_with_digest(ledger_path, "release ledger")
        callback = create_production_callback(Path(args.bundle_root))
        errors = validate_ledger_with_live_bundles(ledger, callback)
        if errors:
            output = {
                "schema_version": RESULT_SCHEMA,
                "validated": False,
                "live_gate_eligible": False,
                "errors": errors,
            }
            exit_code = 1
        else:
            current_results = callback.audit_results()
            history_results = callback.history_audit_results()
            output = {
                "schema_version": RESULT_SCHEMA,
                "validated": True,
                "live_gate_eligible": True,
                "adapter_id": ADAPTER_ID,
                "evidence_types": sorted(EXPECTED_EVIDENCE_TYPES),
                "verified_record_count": len(current_results),
                "historical_verified_record_count": len(history_results),
                "live_results": current_results,
                "history_results": history_results,
                "ledger": str(ledger_path),
                "ledger_sha256": "sha256:" + ledger_sha256,
            }
            exit_code = 0
    except (OSError, ReleaseEvidenceRunnerError) as exc:
        code = exc.code if isinstance(exc, ReleaseEvidenceRunnerError) else "filesystem_error"
        output = {
            "schema_version": RESULT_SCHEMA,
            "validated": False,
            "live_gate_eligible": False,
            "errors": [{"code": code, "message": str(exc)}],
        }
        exit_code = 1
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
