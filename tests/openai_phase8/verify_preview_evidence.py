#!/usr/bin/env python3
"""Phase 8 semantic verifier for externally witnessed Preview evidence.

The shared ``openai_preview_evidence`` module validates bundle integrity only.
This adapter separately authenticates the GitHub Release and Actions witnesses,
binds them to committed verifier/registry code, and only then permits a Preview
gate result.  Provider verification is deliberately outside this adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import yaml


REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from openai_preview_evidence import (  # noqa: E402
    EvidenceValidationError,
    PREVIEW_ATTESTED,
    normalize_sha256,
    sha256_bytes,
    validate_evidence_bundle,
)
from normalize_openai_preview_capture import (  # noqa: E402
    CAPTURE_ADAPTER_ID as PHASE7_CAPTURE_ADAPTER_ID,
    CaptureNormalizationError,
)
from openai_preview_capture_contracts import (  # noqa: E402
    PHASE8_CAPTURE_ADAPTER_ID,
    validate_normalized_capture,
)


ALLOWED_RAW_SUFFIXES = {".json", ".jsonl"}
API_HOST = "api.github.com"
WEB_HOST = "github.com"
ASSET_REDIRECT_HOSTS = frozenset(
    {
        "release-assets.githubusercontent.com",
        "objects.githubusercontent.com",
    }
)
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REQUEST_SCHEMA_VERSION = 2
PREVIEW_ADAPTER_ID = "github_release_asset_preview_v1"
PROVIDER_REGISTRY_RELATIVE = "tests/openai_phase8/provider-verifier-registry.yaml"
DRAFT_VERIFIER_RELATIVE = "scripts/verify_openai_preview_draft_bundle.py"
DRAFT_VERIFIER_WORKFLOW = ".github/workflows/openai-preview-draft-bundle-verifier.yml"
DRAFT_VERIFIER_ID = "independent-draft-bundle-verifier-v1"
PREVIEW_VERIFIER_WORKFLOW = ".github/workflows/openai-preview-evidence.yml"
PROTECTED_REVALIDATOR_WORKFLOW = ".github/workflows/openai-preview-accepted-evidence.yml"
TRUSTED_CURRENT_VERIFIER_WORKFLOWS = frozenset(
    {PREVIEW_VERIFIER_WORKFLOW, PROTECTED_REVALIDATOR_WORKFLOW}
)
TRUSTED_VERIFIER_BRANCH = "main"
MAX_TAG_DEREFERENCE_DEPTH = 8
RELEASE_ASSETS_PER_PAGE = 100
MAX_RELEASE_ASSET_PAGES = 100


class VerificationError(ValueError):
    pass


def digest(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_digest(payload: bytes) -> str:
    normalized = payload.decode("utf-8-sig").replace("\r\n", "\n").replace(
        "\r", "\n"
    )
    return sha256_bytes(normalized.encode("utf-8"))


def time_digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def inside(root: Path, relative: str, label: str) -> Path:
    resolved_root = root.resolve()
    candidate = (resolved_root / relative).resolve()
    try:
        candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise VerificationError(f"{label} escapes evidence root") from exc
    if not candidate.is_file():
        raise VerificationError(f"{label} is missing")
    return candidate


def repository_path(relative: str, label: str) -> Path:
    candidate = (REPO / relative).resolve()
    try:
        candidate.relative_to(REPO.resolve())
    except ValueError as exc:
        raise VerificationError(f"{label} escapes repository root") from exc
    if not candidate.is_file():
        raise VerificationError(f"{label} is missing")
    return candidate


def read_json(path: Path, label: str) -> dict[str, Any]:
    if path.suffix.lower() != ".json":
        raise VerificationError(f"{label} must be JSON, not YAML or an image")
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"{label} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"{label} root must be an object")
    return value


def raw_header(path: Path) -> dict[str, Any]:
    if path.suffix.lower() not in ALLOWED_RAW_SUFFIXES:
        raise VerificationError("raw export must be JSON/JSONL; screenshots are rejected")
    try:
        if path.suffix.lower() == ".json":
            records = [json.loads(path.read_text(encoding="utf-8-sig"))]
        else:
            records = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8-sig").splitlines()
                if line.strip()
            ]
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError("raw export is not machine-readable JSON/JSONL") from exc
    if not records or not all(isinstance(item, dict) for item in records):
        raise VerificationError("raw export contains no object records")
    return records[0]


def parse_time(value: str, label: str) -> None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise VerificationError(f"{label} is not ISO-8601") from exc
    if parsed.tzinfo is None:
        raise VerificationError(f"{label} has no timezone")


def _validated_url(
    url: str,
    *,
    allowed_hosts: frozenset[str],
    label: str,
    allow_query: bool,
) -> urllib.parse.SplitResult:
    try:
        parsed = urllib.parse.urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise VerificationError(f"{label} is malformed") from exc
    hostname = (parsed.hostname or "").lower()
    if (
        parsed.scheme != "https"
        or hostname not in allowed_hosts
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or not parsed.path.startswith("/")
        or parsed.fragment
        or (parsed.query and not allow_query)
    ):
        raise VerificationError(f"{label} is outside the exact GitHub trust boundary")
    return parsed


def validate_api_url(
    url: str, *, expected: str | None = None, allow_query: bool = False
) -> None:
    _validated_url(
        url,
        allowed_hosts=frozenset({API_HOST}),
        label="GitHub API URL",
        allow_query=allow_query,
    )
    if expected is not None and url != expected:
        raise VerificationError("GitHub API URL does not match the witnessed asset")


def validate_browser_download_url(url: str, repository: str) -> None:
    parsed = _validated_url(
        url,
        allowed_hosts=frozenset({WEB_HOST}),
        label="GitHub browser-download URL",
        allow_query=False,
    )
    expected_prefix = f"/{repository}/releases/download/"
    if not parsed.path.startswith(expected_prefix):
        raise VerificationError("browser-download URL is not for the witnessed repository")


class SafeGitHubRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Permit API asset redirects without forwarding repository credentials."""

    def __init__(self, *, allow_asset_redirects: bool) -> None:
        super().__init__()
        self.allow_asset_redirects = allow_asset_redirects

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        if not self.allow_asset_redirects:
            raise VerificationError("GitHub JSON API request attempted a redirect")
        target = urllib.parse.urljoin(req.full_url, newurl)
        source = _validated_url(
            req.full_url,
            allowed_hosts=frozenset({API_HOST}) | ASSET_REDIRECT_HOSTS,
            label="redirect source URL",
            allow_query=True,
        )
        _validated_url(
            target,
            allowed_hosts=ASSET_REDIRECT_HOSTS,
            label="asset redirect URL",
            allow_query=True,
        )
        if source.hostname not in ({API_HOST} | set(ASSET_REDIRECT_HOSTS)):
            raise VerificationError("asset redirect source is not trusted")
        if code in {301, 302, 303}:
            method = "HEAD" if req.get_method() == "HEAD" else "GET"
            data = None
        elif code in {307, 308}:
            method = req.get_method()
            data = req.data
        else:
            raise VerificationError("unsupported GitHub asset redirect status")
        copied_headers = {
            key: value
            for source_headers in (req.headers, req.unredirected_hdrs)
            for key, value in source_headers.items()
            if key.lower() not in {"authorization", "proxy-authorization", "cookie"}
        }
        return urllib.request.Request(
            target,
            data=data,
            headers=copied_headers,
            origin_req_host=req.origin_req_host,
            unverifiable=True,
            method=method,
        )


def github_request(
    url: str,
    *,
    binary: bool,
    opener: Any | None = None,
    allow_query: bool = False,
    json_array: bool = False,
) -> bytes | dict[str, Any] | list[Any]:
    # Both JSON and asset requests originate at the exact GitHub API host.
    # Binary asset downloads may subsequently follow a credential-stripped
    # redirect to GitHub's dedicated signed-release-asset hosts.
    if binary and json_array:
        raise VerificationError("binary GitHub request cannot require a JSON array")
    validate_api_url(url, allow_query=allow_query)
    headers = {
        "Accept": "application/octet-stream" if binary else "application/vnd.github+json",
        "User-Agent": "research-skills-openai-phase8-preview-verifier",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    client = opener or urllib.request.build_opener(
        SafeGitHubRedirectHandler(allow_asset_redirects=binary)
    )
    try:
        with client.open(
            urllib.request.Request(url, headers=headers), timeout=30
        ) as response:
            final_url = response.geturl() if hasattr(response, "geturl") else url
            if binary:
                _validated_url(
                    final_url,
                    allowed_hosts=frozenset({API_HOST}) | ASSET_REDIRECT_HOSTS,
                    label="asset response URL",
                    allow_query=True,
                )
            else:
                validate_api_url(
                    final_url, expected=url, allow_query=allow_query
                )
            payload = response.read()
    except VerificationError:
        raise
    except (OSError, urllib.error.URLError) as exc:
        raise VerificationError("GitHub witness or asset could not be re-queried") from exc
    if binary:
        return payload
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise VerificationError("GitHub witness response is not JSON") from exc
    expected_type = list if json_array else dict
    if not isinstance(value, expected_type):
        expected_label = "array" if json_array else "object"
        raise VerificationError(
            f"GitHub witness response root is not an {expected_label}"
        )
    return value


def committed_file_digest(source_commit: str, relative: str) -> str:
    if COMMIT_RE.fullmatch(source_commit) is None:
        raise VerificationError("source commit is not a full immutable SHA")
    repository_path(relative, "committed binding file")
    try:
        payload = subprocess.run(
            ["git", "show", f"{source_commit}:{relative}"],
            cwd=REPO,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
        ).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        raise VerificationError("committed binding file could not be read") from exc
    return normalized_digest(payload)


def validate_code_bindings(
    request: Mapping[str, Any], source_commit: str, *, synthetic_self_test: bool
) -> dict[str, Any]:
    bindings = (
        ("verifier_path", "verifier_digest", "verifier"),
        ("provider_registry_path", "provider_registry_digest", "provider registry"),
    )
    for path_field, digest_field, label in bindings:
        relative = str(request.get(path_field, ""))
        expected = str(request.get(digest_field, ""))
        path = repository_path(relative, label)
        if SHA256_RE.fullmatch(expected) is None or normalized_digest(path.read_bytes()) != expected:
            raise VerificationError(f"{label} working-tree digest mismatch")
        if not synthetic_self_test and committed_file_digest(source_commit, relative) != expected:
            raise VerificationError(f"{label} is not bound to the witnessed commit")
    registry_path = repository_path(
        str(request.get("provider_registry_path", "")), "provider registry"
    )
    try:
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8-sig"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise VerificationError("provider registry is invalid") from exc
    adapters = registry.get("adapters", []) if isinstance(registry, dict) else []
    adapter = next(
        (
            item
            for item in adapters
            if isinstance(item, dict)
            and item.get("adapter_id") == request.get("adapter_id")
        ),
        None,
    )
    if not isinstance(adapter, dict):
        raise VerificationError("Preview adapter is not present in the bound registry")
    checks = {
        "enabled": adapter.get("enabled") is True,
        "adapter_type": adapter.get("adapter_type") == "preview_attestation",
        "trust_level": adapter.get("trust_level") == PREVIEW_ATTESTED,
        "verifier_path": adapter.get("verifier_path") == request.get("verifier_path"),
        "verifier_digest": adapter.get("verifier_digest") == request.get("verifier_digest"),
        "verification_request_schema": adapter.get("verification_request_schema") == REQUEST_SCHEMA_VERSION,
        "workflow_witness_role": (
            adapter.get("workflow_witness_role") == "source_commit_main_ci"
            and (
                request.get("workflow_witness_role") == "source_commit_main_ci"
                or (synthetic_self_test and request.get("workflow_witness_role") is None)
            )
        ),
        "workflow_path": adapter.get("workflow_path") == request.get("workflow_path"),
        "workflow_event": adapter.get("workflow_event") == request.get("workflow_event"),
        "api_host": adapter.get("api_host") == API_HOST,
        "asset_redirect_hosts": set(adapter.get("asset_redirect_hosts", [])) == set(ASSET_REDIRECT_HOSTS),
        "github_requery": adapter.get("real_verification_requires_github_requery") is True,
    }
    mismatches = sorted(field for field, valid in checks.items() if not valid)
    if mismatches:
        raise VerificationError(
            "verification request conflicts with the bound adapter: "
            + ",".join(mismatches)
        )
    return adapter


def _relative_file_under_root(root: Path, path_value: str, label: str) -> str:
    resolved_root = root.resolve()
    candidate = Path(path_value)
    if not candidate.is_absolute():
        candidate = resolved_root / candidate
    candidate = candidate.resolve()
    try:
        relative = candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise VerificationError(f"{label} escapes evidence root") from exc
    if not candidate.is_file():
        raise VerificationError(f"{label} is missing")
    return relative.as_posix()


def build_request_from_bundle(
    *,
    evidence_root: Path,
    asset_index_path: str,
    envelope_path: str,
    expected_source_identity_path: Path,
) -> dict[str, Any]:
    """Derive a complete live-verification request from downloaded assets."""
    root = evidence_root.resolve()
    if not root.is_dir():
        raise VerificationError("evidence root is missing")
    index_relative = _relative_file_under_root(root, asset_index_path, "asset index")
    envelope_relative = _relative_file_under_root(root, envelope_path, "envelope")
    index_file = inside(root, index_relative, "asset index")
    envelope_file = inside(root, envelope_relative, "envelope")
    index = read_json(index_file, "asset index")
    envelope = read_json(envelope_file, "envelope")
    identity_document = read_json(
        expected_source_identity_path.resolve(), "expected source identity"
    )
    expected_identity = identity_document.get("source_identity", identity_document)
    if not isinstance(expected_identity, dict):
        raise VerificationError("expected source identity is invalid")
    if set(expected_identity) != {
        "plugin_version",
        "source_commit",
        "manifest_sha256",
        "registry_sha256",
        "skill_tree_sha256",
    }:
        raise VerificationError("expected source identity is incomplete")
    expected_identity = {
        **expected_identity,
        "source_commit": str(expected_identity["source_commit"]).lower(),
        **{
            field: normalize_sha256(expected_identity[field], f"source_identity.{field}")
            for field in (
                "manifest_sha256",
                "registry_sha256",
                "skill_tree_sha256",
            )
        },
    }

    registry_path = repository_path(PROVIDER_REGISTRY_RELATIVE, "provider registry")
    try:
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8-sig"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise VerificationError("provider registry is invalid") from exc
    adapters = registry.get("adapters", []) if isinstance(registry, dict) else []
    adapter = next(
        (
            item
            for item in adapters
            if isinstance(item, dict)
            and item.get("adapter_id") == PREVIEW_ADAPTER_ID
            and item.get("enabled") is True
        ),
        None,
    )
    if not isinstance(adapter, dict):
        raise VerificationError("Preview adapter is not enabled")

    release = index.get("github_release")
    witness = index.get("github_witness")
    assets = index.get("assets")
    capture = envelope.get("capture")
    if not all(
        isinstance(value, Mapping)
        for value in (release, witness, capture)
    ) or not isinstance(assets, list):
        raise VerificationError("bundle release, witness, capture, or assets are invalid")
    raw_asset_id = capture.get("raw_export_asset_id")
    raw_record = next(
        (
            item
            for item in assets
            if isinstance(item, dict) and item.get("asset_id") == raw_asset_id
        ),
        None,
    )
    if not isinstance(raw_record, dict):
        raise VerificationError("raw export asset is not indexed")
    raw_name = str(raw_record.get("name", ""))
    if not raw_name or Path(raw_name).name != raw_name:
        raise VerificationError("raw export asset name is unsafe")
    raw_relative = _relative_file_under_root(root, raw_name, "raw export")
    captured_at = str(capture.get("captured_at", ""))
    parse_time(captured_at, "capture timestamp")
    return {
        "schema_version": REQUEST_SCHEMA_VERSION,
        "evidence_root": str(root),
        "adapter_id": PREVIEW_ADAPTER_ID,
        "envelope_path": envelope_relative,
        "envelope_digest": digest(envelope_file),
        "release_asset_index_path": index_relative,
        "release_asset_index_digest": digest(index_file),
        "release_asset_index_name": index_file.name,
        "release_asset_index_size": index_file.stat().st_size,
        "raw_export_path": raw_relative,
        "raw_export_digest": digest(inside(root, raw_relative, "raw export")),
        "raw_export_reference": raw_record.get("browser_download_url"),
        "capture_timestamp_digest": time_digest(captured_at),
        "verifier_path": adapter.get("verifier_path"),
        "verifier_digest": adapter.get("verifier_digest"),
        "provider_registry_path": PROVIDER_REGISTRY_RELATIVE,
        "provider_registry_digest": normalized_digest(registry_path.read_bytes()),
        "workflow_path": witness.get("workflow_path"),
        "workflow_witness_role": witness.get("workflow_witness_role")
        or adapter.get("workflow_witness_role"),
        "workflow_id": witness.get("workflow_id"),
        "workflow_event": witness.get("workflow_event"),
        "workflow_run_id": witness.get("workflow_run_id"),
        "run_head_sha": witness.get("run_head_sha"),
        "release_asset_ids": [
            item.get("asset_id") for item in assets if isinstance(item, dict)
        ],
        "release_asset_digests": {
            str(item.get("asset_id")): item.get("sha256")
            for item in assets
            if isinstance(item, dict)
        },
        "synthetic_test_only": False,
        "expected_source_identity": expected_identity,
    }


def _git_object_target(
    payload: Mapping[str, Any], repository: str, label: str
) -> tuple[str, str]:
    target = payload.get("object")
    if not isinstance(target, Mapping):
        raise VerificationError(f"{label} has no Git object target")
    object_type = target.get("type")
    object_sha = str(target.get("sha", ""))
    if object_type not in {"commit", "tag"} or COMMIT_RE.fullmatch(object_sha) is None:
        raise VerificationError(f"{label} has an unsupported Git object target")
    collection = "commits" if object_type == "commit" else "tags"
    expected_url = (
        f"https://api.github.com/repos/{repository}/git/{collection}/{object_sha}"
    )
    validate_api_url(str(target.get("url", "")), expected=expected_url)
    return str(object_type), object_sha


def validate_release_tag_target(
    repository: str, release_tag: str, expected_source_commit: str
) -> None:
    """Resolve lightweight or annotated tags to one live immutable commit."""
    if (
        not release_tag
        or release_tag.strip() != release_tag
        or any(ord(character) < 32 for character in release_tag)
        or COMMIT_RE.fullmatch(expected_source_commit) is None
    ):
        raise VerificationError("GitHub Release tag or expected commit is invalid")
    encoded_tag = urllib.parse.quote(release_tag, safe="")
    ref_url = (
        f"https://api.github.com/repos/{repository}/git/ref/tags/{encoded_tag}"
    )
    ref_live = github_request(ref_url, binary=False)
    if not isinstance(ref_live, dict) or ref_live.get("ref") != f"refs/tags/{release_tag}":
        raise VerificationError("GitHub Release tag reference mismatch")
    object_type, object_sha = _git_object_target(
        ref_live, repository, "GitHub Release tag reference"
    )

    seen_tag_objects: set[str] = set()
    dereference_depth = 0
    while object_type == "tag":
        if object_sha in seen_tag_objects:
            raise VerificationError("GitHub annotated tag chain contains a cycle")
        if dereference_depth >= MAX_TAG_DEREFERENCE_DEPTH:
            raise VerificationError("GitHub annotated tag chain exceeds the depth limit")
        seen_tag_objects.add(object_sha)
        dereference_depth += 1
        tag_url = (
            f"https://api.github.com/repos/{repository}/git/tags/{object_sha}"
        )
        tag_live = github_request(tag_url, binary=False)
        if (
            not isinstance(tag_live, dict)
            or tag_live.get("sha") != object_sha
            or tag_live.get("url") != tag_url
        ):
            raise VerificationError("GitHub annotated tag object mismatch")
        object_type, object_sha = _git_object_target(
            tag_live, repository, "GitHub annotated tag object"
        )

    commit_url = (
        f"https://api.github.com/repos/{repository}/git/commits/{object_sha}"
    )
    commit_live = github_request(commit_url, binary=False)
    if (
        not isinstance(commit_live, dict)
        or commit_live.get("sha") != object_sha
        or commit_live.get("url") != commit_url
        or object_sha != expected_source_commit
    ):
        raise VerificationError("GitHub Release tag does not resolve to the source commit")


def fetch_live_release_assets(
    repository: str, release_id: int
) -> list[dict[str, Any]]:
    """Read every dedicated Release-assets page and reject unstable pagination."""
    assets: list[dict[str, Any]] = []
    seen_ids: set[int] = set()
    seen_names: set[str] = set()
    saw_short_page = False
    for page_number in range(1, MAX_RELEASE_ASSET_PAGES + 1):
        page_url = (
            f"https://api.github.com/repos/{repository}/releases/{release_id}/assets"
            f"?per_page={RELEASE_ASSETS_PER_PAGE}&page={page_number}"
        )
        page_assets = github_request(
            page_url,
            binary=False,
            allow_query=True,
            json_array=True,
        )
        if not isinstance(page_assets, list):
            raise VerificationError("GitHub Release asset page root is not an array")
        if len(page_assets) > RELEASE_ASSETS_PER_PAGE:
            raise VerificationError("GitHub Release asset page exceeds the requested size")
        if not page_assets:
            return assets
        if saw_short_page:
            raise VerificationError("GitHub Release asset pagination is inconsistent")
        for item in page_assets:
            if not isinstance(item, dict):
                raise VerificationError("GitHub Release asset page is malformed")
            asset_id = item.get("id")
            asset_name = item.get("name")
            if (
                isinstance(asset_id, bool)
                or not isinstance(asset_id, int)
                or asset_id <= 0
                or not isinstance(asset_name, str)
                or not asset_name
                or asset_name in {".", ".."}
                or Path(asset_name).name != asset_name
            ):
                raise VerificationError("GitHub Release asset identity is invalid")
            if asset_id in seen_ids:
                raise VerificationError("GitHub Release contains a duplicate asset ID")
            if asset_name in seen_names:
                raise VerificationError("GitHub Release contains a duplicate asset name")
            seen_ids.add(asset_id)
            seen_names.add(asset_name)
            assets.append(item)
        saw_short_page = len(page_assets) < RELEASE_ASSETS_PER_PAGE
    raise VerificationError("GitHub Release asset pagination did not reach exhaustion")


def validate_live_github_witness(
    asset_index: Mapping[str, Any], request: Mapping[str, Any]
) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    release = asset_index.get("github_release")
    witness = asset_index.get("github_witness")
    assets = asset_index.get("assets")
    if not isinstance(release, Mapping) or not isinstance(witness, Mapping):
        raise VerificationError("GitHub release or workflow witness is missing")
    if not isinstance(assets, list) or not assets:
        raise VerificationError("Release asset index assets are invalid")
    repository = str(release.get("repository", ""))
    if REPOSITORY_RE.fullmatch(repository) is None:
        raise VerificationError("GitHub repository identity is invalid")
    release_id = release.get("release_id")
    workflow_run_id = witness.get("workflow_run_id")
    workflow_id = witness.get("workflow_id")
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value <= 0
        for value in (release_id, workflow_run_id, workflow_id)
    ):
        raise VerificationError("GitHub release, workflow, or run ID is invalid")
    release_tag = release.get("release_tag")
    if not isinstance(release_tag, str):
        raise VerificationError("GitHub Release tag is invalid")
    source_commit = str(witness.get("source_commit", ""))
    if (
        COMMIT_RE.fullmatch(source_commit) is None
        or witness.get("run_head_sha") != source_commit
    ):
        raise VerificationError("GitHub workflow run is not bound to an immutable commit")
    expected_source_identity = request.get("expected_source_identity")
    if (
        not isinstance(expected_source_identity, Mapping)
        or expected_source_identity.get("source_commit") != source_commit
    ):
        raise VerificationError("verification request does not bind the source commit")
    if (
        request.get("workflow_path") != witness.get("workflow_path")
        or request.get("workflow_witness_role")
        != witness.get("workflow_witness_role")
        or request.get("workflow_id") != workflow_id
        or request.get("workflow_event") != witness.get("workflow_event")
        or request.get("workflow_run_id") != workflow_run_id
        or request.get("run_head_sha") != witness.get("run_head_sha")
    ):
        raise VerificationError("verification request does not bind the GitHub workflow run")

    release_url = f"https://api.github.com/repos/{repository}/releases/{release_id}"
    run_url = f"https://api.github.com/repos/{repository}/actions/runs/{workflow_run_id}"
    release_live = github_request(release_url, binary=False)
    if (
        not isinstance(release_live, dict)
        or release_live.get("id") != release_id
        or release_live.get("tag_name") != release_tag
        or release_live.get("draft") is not False
        or release_live.get("prerelease") is not True
        or release_live.get("immutable") is not True
    ):
        raise VerificationError("GitHub Release witness mismatch")

    validate_release_tag_target(repository, release_tag, source_commit)
    live_asset_list = fetch_live_release_assets(repository, release_id)

    run_live = github_request(run_url, binary=False)
    if not isinstance(run_live, dict):
        raise VerificationError("GitHub Actions witness response is invalid")
    run_actor = run_live.get("actor")
    if (
        run_live.get("id") != workflow_run_id
        or run_live.get("workflow_id") != workflow_id
        or run_live.get("path") != witness.get("workflow_path")
        or run_live.get("event") != witness.get("workflow_event")
        or run_live.get("head_sha") != witness.get("run_head_sha")
        or run_live.get("head_sha") != witness.get("source_commit")
        or not isinstance(run_actor, Mapping)
        or run_actor.get("login") != witness.get("actor")
        or run_live.get("status") != "completed"
        or run_live.get("conclusion") != "success"
    ):
        raise VerificationError("GitHub Actions witness mismatch")

    live_assets = {int(item["id"]): item for item in live_asset_list}
    expected_ids = request.get("release_asset_ids")
    expected_digests = request.get("release_asset_digests")
    if not all(isinstance(record, Mapping) for record in assets):
        raise VerificationError("Release asset record is invalid")
    indexed_ids = [record.get("asset_id") for record in assets]
    indexed_digests = {
        str(record.get("asset_id")): record.get("sha256") for record in assets
    }
    if (
        any(
            isinstance(asset_id, bool)
            or not isinstance(asset_id, int)
            or asset_id <= 0
            for asset_id in indexed_ids
        )
        or len(indexed_ids) != len(set(indexed_ids))
        or any(
            SHA256_RE.fullmatch(str(value)) is None
            for value in indexed_digests.values()
        )
        or expected_ids != indexed_ids
        or expected_digests != indexed_digests
    ):
        raise VerificationError("verification request does not bind all Release assets")

    index_name = request.get("release_asset_index_name")
    index_digest = request.get("release_asset_index_digest")
    index_size = request.get("release_asset_index_size")
    if (
        not isinstance(index_name, str)
        or not index_name
        or Path(index_name).name != index_name
        or SHA256_RE.fullmatch(str(index_digest)) is None
        or isinstance(index_size, bool)
        or not isinstance(index_size, int)
        or index_size <= 0
    ):
        raise VerificationError("verification request does not bind the Release asset index")
    live_index_candidates = [
        item for item in live_asset_list if item.get("name") == index_name
    ]
    if len(live_index_candidates) != 1:
        raise VerificationError("Release asset index does not have one live GitHub asset")
    live_index_asset = live_index_candidates[0]
    index_asset_id = live_index_asset.get("id")
    if (
        isinstance(index_asset_id, bool)
        or not isinstance(index_asset_id, int)
        or index_asset_id <= 0
        or index_asset_id in indexed_ids
    ):
        raise VerificationError("GitHub Release asset-index witness mismatch")
    expected_index_api_url = (
        f"https://api.github.com/repos/{repository}/releases/assets/{index_asset_id}"
    )
    validate_api_url(
        str(live_index_asset.get("url", "")), expected=expected_index_api_url
    )
    validate_browser_download_url(
        str(live_index_asset.get("browser_download_url", "")), repository
    )
    if (
        live_index_asset.get("digest") != index_digest
        or live_index_asset.get("size") != index_size
        or live_index_asset.get("state") != "uploaded"
    ):
        raise VerificationError("GitHub Release asset-index witness mismatch")

    verified: dict[int, dict[str, Any]] = {}
    for record in assets:
        if not isinstance(record, Mapping):
            raise VerificationError("Release asset record is invalid")
        asset_id = record.get("asset_id")
        live_asset = live_assets.get(asset_id)
        expected_api_url = (
            f"https://api.github.com/repos/{repository}/releases/assets/{asset_id}"
        )
        if not isinstance(live_asset, dict):
            raise VerificationError("GitHub Release asset witness mismatch")
        validate_api_url(str(live_asset.get("url", "")), expected=expected_api_url)
        browser_url = str(record.get("browser_download_url", ""))
        validate_browser_download_url(browser_url, repository)
        if (
            live_asset.get("name") != record.get("name")
            or live_asset.get("browser_download_url") != browser_url
            or live_asset.get("digest") != record.get("sha256")
            or live_asset.get("size") != record.get("size")
            or live_asset.get("state") != "uploaded"
        ):
            raise VerificationError("GitHub Release asset witness mismatch")
        verified[int(asset_id)] = live_asset
    return verified, live_index_asset


def validate_draft_verifier_execution(
    *,
    report_payload: bytes,
    repository: str,
    source_commit: str,
    source_ci_run_id: int,
) -> int:
    """Re-query the distinct pre-index GitHub Actions run recorded by V."""

    try:
        report = json.loads(report_payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError("draft verifier report is not valid JSON") from exc
    if not isinstance(report, Mapping):
        raise VerificationError("draft verifier report is not an object")
    verifier_path = repository_path(DRAFT_VERIFIER_RELATIVE, "draft verifier")
    expected_digest = normalized_digest(verifier_path.read_bytes())
    if (
        report.get("verifier_id") != DRAFT_VERIFIER_ID
        or report.get("verifier_code_sha256") != expected_digest
        or report.get("independent") is not True
        or report.get("verdict") != "accepted"
    ):
        raise VerificationError("draft verifier code or verdict binding mismatch")
    execution = report.get("execution")
    if not isinstance(execution, Mapping):
        raise VerificationError("draft verifier execution witness is missing")
    run_id = execution.get("workflow_run_id")
    run_attempt = execution.get("run_attempt")
    actor = execution.get("actor")
    if (
        isinstance(run_id, bool)
        or not isinstance(run_id, int)
        or run_id <= 0
        or run_id == source_ci_run_id
        or isinstance(run_attempt, bool)
        or not isinstance(run_attempt, int)
        or run_attempt <= 0
        or execution.get("repository") != repository
        or execution.get("workflow_path") != DRAFT_VERIFIER_WORKFLOW
        or execution.get("workflow_event") != "workflow_dispatch"
        or execution.get("run_head_sha") != source_commit
        or not isinstance(actor, str)
        or not actor
    ):
        raise VerificationError("draft verifier execution identity is invalid")
    live = github_request(
        f"https://api.github.com/repos/{repository}/actions/runs/{run_id}",
        binary=False,
    )
    if not isinstance(live, Mapping):
        raise VerificationError("draft verifier workflow response is invalid")
    live_repo = live.get("repository")
    live_actor = live.get("actor")
    if (
        live.get("id") != run_id
        or live.get("run_attempt") != run_attempt
        or live.get("path") != DRAFT_VERIFIER_WORKFLOW
        or live.get("event") != "workflow_dispatch"
        or live.get("head_sha") != source_commit
        or live.get("head_branch") != "main"
        or live.get("status") != "completed"
        or live.get("conclusion") != "success"
        or not isinstance(live_repo, Mapping)
        or live_repo.get("full_name") != repository
        or not isinstance(live_actor, Mapping)
        or live_actor.get("login") != actor
    ):
        raise VerificationError("draft verifier workflow witness mismatch")
    try:
        verified_at = datetime.fromisoformat(
            str(report.get("verified_at", "")).replace("Z", "+00:00")
        )
        started_at = datetime.fromisoformat(
            str(live.get("run_started_at", "")).replace("Z", "+00:00")
        )
        completed_at = datetime.fromisoformat(
            str(live.get("updated_at", "")).replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise VerificationError("draft verifier chronology is invalid") from exc
    if any(value.tzinfo is None for value in (verified_at, started_at, completed_at)):
        raise VerificationError("draft verifier chronology lacks timezone")
    if not (started_at <= verified_at <= completed_at + timedelta(minutes=5)):
        raise VerificationError("draft verifier timestamp is outside its workflow run")
    return int(run_id)


def validate_current_verifier_execution(
    *,
    repository: str,
    source_commit: str,
    source_ci_run_id: int,
    draft_verifier_run_id: int,
) -> dict[str, Any]:
    """Re-query and bind the Actions run executing this live verification."""

    run_id_text = os.environ.get("GITHUB_RUN_ID", "")
    run_attempt_text = os.environ.get("GITHUB_RUN_ATTEMPT", "")
    actor = os.environ.get("GITHUB_ACTOR", "")
    workflow_ref = os.environ.get("GITHUB_WORKFLOW_REF", "")
    workflow_prefix = f"{repository}/"
    workflow_suffix = f"@refs/heads/{TRUSTED_VERIFIER_BRANCH}"
    if (
        os.environ.get("GITHUB_ACTIONS") != "true"
        or not run_id_text.isdigit()
        or int(run_id_text) <= 0
        or not run_attempt_text.isdigit()
        or int(run_attempt_text) <= 0
        or os.environ.get("GITHUB_REPOSITORY") != repository
        or os.environ.get("GITHUB_EVENT_NAME") != "workflow_dispatch"
        or os.environ.get("GITHUB_SHA") != source_commit
        or os.environ.get("GITHUB_WORKFLOW_SHA") != source_commit
        or os.environ.get("GITHUB_REF")
        != f"refs/heads/{TRUSTED_VERIFIER_BRANCH}"
        or os.environ.get("GITHUB_REF_NAME") != TRUSTED_VERIFIER_BRANCH
        or not workflow_ref.startswith(workflow_prefix)
        or not workflow_ref.endswith(workflow_suffix)
        or not actor
    ):
        raise VerificationError(
            "live Preview promotion requires a bound GitHub Actions execution"
        )
    workflow_path = workflow_ref[
        len(workflow_prefix) : len(workflow_ref) - len(workflow_suffix)
    ]
    if workflow_path not in TRUSTED_CURRENT_VERIFIER_WORKFLOWS:
        raise VerificationError("current verifier workflow is not registered")

    run_id = int(run_id_text)
    run_attempt = int(run_attempt_text)
    if len({source_ci_run_id, draft_verifier_run_id, run_id}) != 3:
        raise VerificationError(
            "source, draft, and current verifier runs must be distinct"
        )

    workflow_name = Path(workflow_path).name
    workflow_api_url = (
        f"https://api.github.com/repos/{repository}/actions/workflows/{workflow_name}"
    )
    workflow = github_request(workflow_api_url, binary=False)
    if not isinstance(workflow, Mapping):
        raise VerificationError("current verifier workflow response is invalid")
    workflow_id = workflow.get("id")
    if (
        isinstance(workflow_id, bool)
        or not isinstance(workflow_id, int)
        or workflow_id <= 0
        or workflow.get("url")
        != f"https://api.github.com/repos/{repository}/actions/workflows/{workflow_id}"
        or workflow.get("path") != workflow_path
        or workflow.get("state") != "active"
    ):
        raise VerificationError("current verifier workflow identity is invalid")

    run_api_url = f"https://api.github.com/repos/{repository}/actions/runs/{run_id}"
    run = github_request(run_api_url, binary=False)
    if not isinstance(run, Mapping):
        raise VerificationError("current verifier run response is invalid")
    run_repository = run.get("repository")
    run_actor = run.get("actor")
    run_path = str(run.get("path", "")).split("@", 1)[0]
    run_url = f"https://github.com/{repository}/actions/runs/{run_id}"
    if (
        run.get("id") != run_id
        or run.get("run_attempt") != run_attempt
        or run.get("url") != run_api_url
        or run.get("html_url") != run_url
        or run.get("workflow_id") != workflow_id
        or run_path != workflow_path
        or run.get("event") != "workflow_dispatch"
        or run.get("head_sha") != source_commit
        or run.get("head_branch") != TRUSTED_VERIFIER_BRANCH
        or run.get("status") != "in_progress"
        or run.get("conclusion") is not None
        or not isinstance(run_repository, Mapping)
        or run_repository.get("full_name") != repository
        or not isinstance(run_actor, Mapping)
        or run_actor.get("login") != actor
    ):
        raise VerificationError("current verifier workflow run witness mismatch")
    return {
        "workflow_id": workflow_id,
        "workflow_run_id": run_id,
        "run_attempt": run_attempt,
        "workflow_path": workflow_path,
        "workflow_event": "workflow_dispatch",
        "run_head_sha": source_commit,
        "run_head_ref": f"refs/heads/{TRUSTED_VERIFIER_BRANCH}",
        "actor": actor,
        "run_url": run_url,
    }


def _verify(
    request: Mapping[str, Any],
    *,
    synthetic_self_test: bool,
    require_current_execution: bool,
) -> dict[str, Any]:
    if request.get("schema_version") != REQUEST_SCHEMA_VERSION:
        raise VerificationError("unsupported request schema")
    if request.get("adapter_id") != PREVIEW_ADAPTER_ID:
        raise VerificationError("verification request uses an unregistered adapter")
    expected_source_identity = request.get("expected_source_identity")
    if not isinstance(expected_source_identity, Mapping) or set(
        expected_source_identity
    ) != {
        "plugin_version",
        "source_commit",
        "manifest_sha256",
        "registry_sha256",
        "skill_tree_sha256",
    }:
        raise VerificationError("verification request lacks a complete source identity")
    root = Path(str(request.get("evidence_root", ""))).resolve()
    if not root.is_dir():
        raise VerificationError("evidence root is missing")
    envelope_path = inside(root, str(request.get("envelope_path", "")), "envelope")
    index_path = inside(
        root, str(request.get("release_asset_index_path", "")), "Release asset index"
    )
    raw_path = inside(root, str(request.get("raw_export_path", "")), "raw export")
    for path, expected, label in (
        (envelope_path, request.get("envelope_digest"), "envelope"),
        (index_path, request.get("release_asset_index_digest"), "Release asset index"),
        (raw_path, request.get("raw_export_digest"), "raw export"),
    ):
        if digest(path) != expected:
            raise VerificationError(f"{label} digest mismatch")

    envelope = read_json(envelope_path, "envelope")
    asset_index = read_json(index_path, "Release asset index")
    assets = asset_index.get("assets", [])
    if not isinstance(assets, list):
        raise VerificationError("Release asset index assets are invalid")
    source_commit = str(asset_index.get("source_identity", {}).get("source_commit", ""))
    validate_code_bindings(request, source_commit, synthetic_self_test=synthetic_self_test)

    if synthetic_self_test:
        live_assets: dict[int, dict[str, Any]] = {}
        live_index_asset: dict[str, Any] | None = None
    else:
        if request.get("synthetic_test_only"):
            raise VerificationError("synthetic Preview evidence cannot be promoted")
        # The live API object is authenticated and checked before any indexed
        # asset bytes are downloaded.  Repository-authored URLs are never used
        # as download authority.
        live_assets, live_index_asset = validate_live_github_witness(
            asset_index, request
        )
        live_index_payload = github_request(
            str(live_index_asset["url"]), binary=True
        )
        if (
            not isinstance(live_index_payload, bytes)
            or live_index_payload != index_path.read_bytes()
        ):
            raise VerificationError(
                "downloaded Release asset index differs from the live GitHub asset"
            )

    fetched_asset_payloads: dict[int, bytes] = {}

    def fetch_asset(record: Mapping[str, Any]) -> bytes:
        if synthetic_self_test:
            fixture = inside(root, str(record.get("fixture_path", "")), "indexed asset")
            payload = fixture.read_bytes()
        else:
            asset_id = record.get("asset_id")
            live_asset = live_assets.get(asset_id)
            if not isinstance(live_asset, dict):
                raise VerificationError("asset was not authenticated before download")
            payload = github_request(str(live_asset["url"]), binary=True)
            assert isinstance(payload, bytes)
        fetched_asset_payloads[int(record["asset_id"])] = payload
        return payload

    result = validate_evidence_bundle(
        envelope,
        asset_index,
        fetch_asset,
        envelope_bytes=envelope_path.read_bytes(),
        expected_source_identity=expected_source_identity,
        index_bytes=index_path.read_bytes(),
    )
    if (
        not result.integrity_valid
        or result.gate_eligible
        or result.provider_verified
        or result.counts_as_preview_acceptance
        or result.verification_level != PREVIEW_ATTESTED
        or result.claimed_provider_verified
        or not result.claimed_counts_as_preview_acceptance
        or not result.source_identity_bound
    ):
        raise VerificationError("shared integrity layer returned an invalid Preview contract")

    draft_verifier_run_id: int | None = None
    if not synthetic_self_test:
        report_payload = fetched_asset_payloads.get(result.verifier_report_asset_id)
        release_record = asset_index.get("github_release", {})
        witness_record = asset_index.get("github_witness", {})
        if not isinstance(report_payload, bytes):
            raise VerificationError("draft verifier report asset was not fetched")
        draft_verifier_run_id = validate_draft_verifier_execution(
            report_payload=report_payload,
            repository=str(release_record.get("repository", "")),
            source_commit=source_commit,
            source_ci_run_id=int(witness_record.get("workflow_run_id", 0)),
        )

    raw_asset = next(
        (item for item in assets if item.get("asset_id") == result.raw_export_asset_id),
        None,
    )
    if not isinstance(raw_asset, dict):
        raise VerificationError("raw export asset record is missing")
    if synthetic_self_test:
        if raw_asset.get("fixture_path") != request.get("raw_export_path"):
            raise VerificationError("raw export path does not match the indexed fixture")
    elif raw_asset.get("name") != request.get("raw_export_path"):
        raise VerificationError("raw export path does not match the indexed Release asset")
    if raw_asset.get("browser_download_url") != request.get("raw_export_reference"):
        raise VerificationError("raw export reference does not match the GitHub asset")
    repository = str(asset_index.get("github_release", {}).get("repository", ""))
    validate_browser_download_url(str(request.get("raw_export_reference", "")), repository)

    fetched_raw = fetched_asset_payloads.get(result.raw_export_asset_id)
    if fetched_raw is None or fetched_raw != raw_path.read_bytes():
        raise VerificationError(
            "local raw export differs from the authenticated Release asset"
        )
    header = raw_header(raw_path)
    captured_at = str(envelope.get("capture", {}).get("captured_at", ""))
    parse_time(captured_at, "capture timestamp")
    if header.get("captured_at") != captured_at:
        raise VerificationError("raw export capture timestamp mismatch")
    if time_digest(captured_at) != request.get("capture_timestamp_digest"):
        raise VerificationError("capture timestamp digest mismatch")

    envelope_adapter = envelope.get("adapter", {})
    if (
        isinstance(envelope_adapter, Mapping)
        and envelope_adapter.get("adapter_id")
        in {PHASE7_CAPTURE_ADAPTER_ID, PHASE8_CAPTURE_ADAPTER_ID}
    ):
        try:
            normalized_capture = validate_normalized_capture(
                header,
                now=datetime.now(timezone.utc),
                verify_checkout=True,
            )
        except CaptureNormalizationError as exc:
            raise VerificationError(
                f"normalized App Server capture is invalid: {exc.code} at {exc.path}"
            ) from exc
        except ValueError as exc:
            raise VerificationError(
                f"normalized capture schema is unsupported: {exc}"
            ) from exc
        normalized_capture_fields = normalized_capture.get("capture", {})
        if (
            normalized_capture.get("source_identity") != expected_source_identity
            or normalized_capture.get("captured_at") != captured_at
            or normalized_capture_fields.get("task_or_thread_id")
            != envelope.get("capture", {}).get("task_or_thread_id")
        ):
            raise VerificationError(
                "normalized App Server capture is not bound to the envelope and source"
            )

    if synthetic_self_test:
        if request.get("synthetic_test_only") is not True or header.get(
            "synthetic_test_only"
        ) is not True:
            raise VerificationError("offline mode is restricted to synthetic self-tests")
    elif header.get("synthetic_test_only"):
        raise VerificationError("synthetic Preview evidence cannot be promoted")

    verified_assets: list[dict[str, Any]] = []
    for record in assets:
        if not isinstance(record, Mapping):
            raise VerificationError("Release asset record is invalid")
        asset_id = record.get("asset_id")
        live_asset = live_assets.get(asset_id, {})
        verified_assets.append(
            {
                "asset_id": asset_id,
                "name": record.get("name"),
                "sha256": record.get("sha256"),
                "size": record.get("size"),
                "evidence_kind": record.get("evidence_kind"),
                "state": live_asset.get("state") if live_asset else "synthetic_fixture",
                "api_url": live_asset.get("url") if live_asset else None,
                "browser_download_url": (
                    live_asset.get("browser_download_url")
                    if live_asset
                    else record.get("browser_download_url")
                ),
            }
        )
    if live_index_asset is not None:
        verified_assets.append(
            {
                "asset_id": live_index_asset.get("id"),
                "name": live_index_asset.get("name"),
                "sha256": live_index_asset.get("digest"),
                "size": live_index_asset.get("size"),
                "evidence_kind": "release_asset_index",
                "state": live_index_asset.get("state"),
                "api_url": live_index_asset.get("url"),
                "browser_download_url": live_index_asset.get(
                    "browser_download_url"
                ),
            }
        )
    verified_assets.sort(key=lambda item: int(item["asset_id"]))

    verified_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    live_requery = not synthetic_self_test
    gate_eligible = live_requery and require_current_execution
    source_ci_run_id = asset_index.get("github_witness", {}).get("workflow_run_id")
    current_execution: dict[str, Any] | None = None
    if gate_eligible:
        if (
            isinstance(source_ci_run_id, bool)
            or not isinstance(source_ci_run_id, int)
            or source_ci_run_id <= 0
            or draft_verifier_run_id is None
        ):
            raise VerificationError("live Preview execution lineage is incomplete")
        current_execution = validate_current_verifier_execution(
            repository=repository,
            source_commit=source_commit,
            source_ci_run_id=source_ci_run_id,
            draft_verifier_run_id=draft_verifier_run_id,
        )
    artifact_digests = {
        "raw_export_sha256": result.raw_export_sha256,
        "evidence_envelope_sha256": result.evidence_envelope_sha256,
        "verifier_report_sha256": result.verifier_report_sha256,
        "release_asset_index_sha256": result.release_asset_index_sha256,
    }
    integrity_result = {
        "evidence_id": result.evidence_id,
        "integrity_valid": result.integrity_valid,
        "gate_eligible": result.gate_eligible,
        "claimed_verification_level": result.verification_level,
        "claimed_provider_verified": result.claimed_provider_verified,
        "claimed_counts_as_preview_acceptance": (
            result.claimed_counts_as_preview_acceptance
        ),
        "source_identity_bound": result.source_identity_bound,
        "raw_export_asset_id": result.raw_export_asset_id,
        "raw_export_sha256": result.raw_export_sha256,
        "envelope_asset_id": result.evidence_envelope_asset_id,
        "envelope_sha256": result.evidence_envelope_sha256,
        # Descriptive aliases are retained for direct consumers of this v3 result.
        "evidence_envelope_asset_id": result.evidence_envelope_asset_id,
        "evidence_envelope_sha256": result.evidence_envelope_sha256,
        "verifier_report_asset_id": result.verifier_report_asset_id,
        "verifier_report_sha256": result.verifier_report_sha256,
        "release_asset_index_asset_id": (
            live_index_asset.get("id") if live_index_asset is not None else None
        ),
        "release_asset_index_sha256": result.release_asset_index_sha256,
    }
    live_verifier = {
        "adapter_id": PREVIEW_ADAPTER_ID,
        "adapter_code_sha256": str(request.get("verifier_digest", "")).removeprefix(
            "sha256:"
        ),
        "live_requery": live_requery,
        # Legacy spelling retained for the release-ledger validator.
        "live_requery_performed": live_requery,
        "independent": gate_eligible,
        "requery_source": "github_api" if live_requery else "synthetic_fixture",
        "verified_at": verified_at,
        "source_ci_workflow_run_id": source_ci_run_id if gate_eligible else None,
        "draft_verifier_workflow_run_id": (
            draft_verifier_run_id if gate_eligible else None
        ),
        "verifier_workflow_id": (
            current_execution["workflow_id"] if current_execution else None
        ),
        "verifier_workflow_run_id": (
            current_execution["workflow_run_id"] if current_execution else None
        ),
        "verifier_run_attempt": (
            current_execution["run_attempt"] if current_execution else None
        ),
        "verifier_workflow_path": (
            current_execution["workflow_path"] if current_execution else None
        ),
        "verifier_workflow_event": (
            current_execution["workflow_event"] if current_execution else None
        ),
        "verifier_run_head_sha": (
            current_execution["run_head_sha"] if current_execution else None
        ),
        "verifier_run_head_ref": (
            current_execution["run_head_ref"] if current_execution else None
        ),
        "verifier_actor": current_execution["actor"] if current_execution else None,
        "verifier_run_url": (
            current_execution["run_url"] if current_execution else None
        ),
    }
    gate_eligibility = {
        "eligible": gate_eligible,
        "level": PREVIEW_ATTESTED,
        "determined_by": (
            "registered_live_verifier" if gate_eligible else "synthetic_self_test"
        ),
        "provider_adapter_id": None,
        "provider_authenticated": False,
    }
    return {
        "schema_version": 3,
        "verdict": (
            PREVIEW_ATTESTED
            if gate_eligible
            else (
                "external_integrity_requeried"
                if live_requery
                else "synthetic_contract_valid"
            )
        ),
        "evidence_id": result.evidence_id,
        "verification_level": PREVIEW_ATTESTED,
        "adapter_id": PREVIEW_ADAPTER_ID,
        "provider_verified": False,
        "source_identity": dict(expected_source_identity),
        "artifact_digests": artifact_digests,
        "verified_assets": verified_assets,
        "integrity_result": integrity_result,
        "live_verifier": live_verifier,
        "gate_eligibility": gate_eligibility,
        # Legacy booleans remain stable while callers migrate to v3 fields.
        "integrity_valid": True,
        "gate_eligible": gate_eligible,
        "counts_as_preview_attested": gate_eligible,
        "counts_as_provider_verified": False,
        "synthetic_self_test": synthetic_self_test,
    }


def verify(
    request: Mapping[str, Any], *, synthetic_self_test: bool = False
) -> dict[str, Any]:
    """Run the registered Preview verifier and bind its current trusted run."""

    return _verify(
        request,
        synthetic_self_test=synthetic_self_test,
        require_current_execution=not synthetic_self_test,
    )


# The release-ledger dispatcher checks this attribute before invoking a live
# verifier, preventing an arbitrary callable from impersonating this adapter.
verify.adapter_id = PREVIEW_ADAPTER_ID  # type: ignore[attr-defined]


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--request")
    mode.add_argument("--asset-index")
    parser.add_argument("--evidence-root")
    parser.add_argument("--envelope")
    parser.add_argument("--expected-source-identity")
    parser.add_argument("--synthetic-self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.request:
            if any(
                value is not None
                for value in (
                    args.evidence_root,
                    args.envelope,
                    args.expected_source_identity,
                )
            ):
                raise VerificationError("request mode cannot include bundle arguments")
            request = read_json(Path(args.request), "verification request")
        else:
            if args.synthetic_self_test:
                raise VerificationError("bundle mode is reserved for live verification")
            if not all(
                (args.evidence_root, args.envelope, args.expected_source_identity)
            ):
                raise VerificationError("bundle mode requires root, envelope, and identity")
            request = build_request_from_bundle(
                evidence_root=Path(args.evidence_root),
                asset_index_path=str(args.asset_index),
                envelope_path=str(args.envelope),
                expected_source_identity_path=Path(args.expected_source_identity),
            )
        result = verify(request, synthetic_self_test=args.synthetic_self_test)
    except (VerificationError, EvidenceValidationError) as exc:
        print(json.dumps({"verdict": "reject", "reason": str(exc)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
