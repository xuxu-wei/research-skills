#!/usr/bin/env python3
"""Independently verify one protected OpenAI Preview accepted-run summary.

This consumer trusts neither the triggering webhook nor the producer's final
Boolean.  It re-queries the exact workflow attempt, protected job, Environment
deployment, run-bound artifact, and the accepted-summary contents before it
can emit a Phase 7-8 closure result.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from build_openai_preview_accepted_summary import (
    EXTERNAL_RECORD_PATHS,
    EXPECTED_PHASE7_MATRIX,
    EXPECTED_PHASE8_RETRIEVAL_RECEIPTS,
    EXPECTED_PHASE8_REVIEWER_CASES,
    EXPECTED_RETRIEVAL_DISTRIBUTION,
    PHASE78_CLOSURE_CONSUMER_SCHEMA,
    PHASE78_CLOSURE_EVIDENCE_TYPE,
    PHASE78_CLOSURE_PRODUCER_SCHEMAS,
)


API_ROOT = "https://api.github.com"
API_VERSION = "2026-03-10"
SOURCE_WORKFLOW_NAME = "OpenAI Preview Accepted Evidence"
SOURCE_WORKFLOW_PATH = ".github/workflows/openai-preview-accepted-evidence.yml"
CONSUMER_WORKFLOW_PATH = (
    ".github/workflows/openai-preview-accepted-summary-consumer.yml"
)
SOURCE_SUMMARY_SCHEMA = "openai-preview-accepted-run-summary/v3"
RESULT_SCHEMA = "openai-preview-accepted-summary-consumer/v1"
ENVIRONMENT_NAME = "openai-preview-governance"
DEFAULT_BRANCH = "main"
PROTECTED_JOB_NAME = "validate-accepted-evidence"
PREFLIGHT_JOB_NAME = "validate-dispatch"
SUMMARY_JSON_NAME = "openai-preview-accepted-summary.json"
SUMMARY_ARTIFACT_PREFIX = "openai-preview-accepted-summary-"
MAX_API_BYTES = 2_000_000
MAX_ARCHIVE_BYTES = 2_000_000
MAX_SUMMARY_BYTES = 1_500_000
MAX_PAGES = 20
PER_PAGE = 100
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")

JsonFetcher = Callable[[str], Any]
BinaryFetcher = Callable[[str], bytes]


class AcceptedSummaryConsumerError(ValueError):
    """Fail-closed consumer error with a stable machine-readable code."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def fail(code: str, message: str) -> None:
    raise AcceptedSummaryConsumerError(code, message)


def require(condition: Any, code: str, message: str) -> None:
    if not condition:
        fail(code, message)


def positive_integer(value: Any, label: str) -> int:
    require(
        isinstance(value, int) and not isinstance(value, bool) and value > 0,
        "identity_invalid",
        f"{label} must be a positive integer",
    )
    return value


def full_commit(value: Any, label: str) -> str:
    require(
        isinstance(value, str) and COMMIT_RE.fullmatch(value) is not None,
        "identity_invalid",
        f"{label} must be a lowercase full commit SHA",
    )
    return value


def bare_digest(value: Any, label: str, *, prefix_optional: bool = False) -> str:
    require(isinstance(value, str), "digest_invalid", f"{label} is missing")
    digest = value[7:] if value.startswith("sha256:") else value
    if not prefix_optional:
        require(
            value.startswith("sha256:"),
            "digest_invalid",
            f"{label} must use the sha256: prefix",
        )
    require(
        SHA256_RE.fullmatch(digest) is not None,
        "digest_invalid",
        f"{label} is not a SHA-256 digest",
    )
    return digest


def parse_time(value: Any, label: str) -> datetime:
    require(isinstance(value, str), "timestamp_invalid", f"{label} is missing")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail("timestamp_invalid", f"{label} is not an ISO-8601 timestamp")
    require(
        parsed.tzinfo is not None,
        "timestamp_invalid",
        f"{label} must include a timezone",
    )
    return parsed.astimezone(timezone.utc)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: Any,
        code: int,
        message: str,
        headers: Mapping[str, Any],
        new_url: str,
    ) -> None:
        raise urllib.error.URLError("redirect is not allowed for GitHub JSON")


def _validate_api_url(url: str) -> urllib.parse.SplitResult:
    parsed = urllib.parse.urlsplit(url)
    require(
        parsed.scheme == "https"
        and (parsed.hostname or "").lower() == "api.github.com"
        and parsed.username is None
        and parsed.password is None
        and not parsed.fragment
        and parsed.path.startswith("/repos/"),
        "github_url_invalid",
        "GitHub API URL is not canonical",
    )
    return parsed


def github_json(url: str) -> Any:
    _validate_api_url(url)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    require(bool(token), "github_token_missing", "GH_TOKEN or GITHUB_TOKEN is required")
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "research-skills-openai-accepted-summary-consumer",
        },
    )
    request.add_unredirected_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.build_opener(_NoRedirect()).open(
            request, timeout=30
        ) as response:
            require(
                response.geturl() == url,
                "github_redirect_rejected",
                "GitHub JSON request was redirected",
            )
            payload = response.read(MAX_API_BYTES + 1)
    except AcceptedSummaryConsumerError:
        raise
    except (OSError, urllib.error.URLError) as exc:
        fail("github_request_failed", f"GitHub JSON request failed: {exc}")
    require(
        0 < len(payload) <= MAX_API_BYTES,
        "github_response_invalid",
        "GitHub JSON response is empty or oversized",
    )
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        fail("github_response_invalid", f"GitHub returned invalid JSON: {exc}")


class _ArtifactRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: Any,
        code: int,
        message: str,
        headers: Mapping[str, Any],
        new_url: str,
    ) -> urllib.request.Request | None:
        self.count += 1
        require(
            self.count == 1 and _trusted_artifact_storage(new_url),
            "artifact_redirect_rejected",
            "Actions artifact redirect target is not trusted",
        )
        redirected = super().redirect_request(
            request, file_pointer, code, message, headers, new_url
        )
        if redirected is not None:
            redirected.remove_header("Authorization")
        return redirected


def _trusted_artifact_storage(url: str) -> bool:
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
            or re.fullmatch(
                r"productionresults[a-z0-9-]*\.blob\.core\.windows\.net", host
            )
            is not None
        )
    )


def github_artifact(url: str) -> bytes:
    parsed = _validate_api_url(url)
    require(
        not parsed.query
        and re.fullmatch(
            r"/repos/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/actions/artifacts/[1-9][0-9]*/zip",
            parsed.path,
        )
        is not None,
        "artifact_url_invalid",
        "Actions artifact URL is not canonical",
    )
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    require(bool(token), "github_token_missing", "GH_TOKEN or GITHUB_TOKEN is required")
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "research-skills-openai-accepted-summary-consumer",
        },
    )
    request.add_unredirected_header("Authorization", f"Bearer {token}")
    handler = _ArtifactRedirect()
    try:
        with urllib.request.build_opener(handler).open(request, timeout=30) as response:
            require(
                handler.count == 1 and _trusted_artifact_storage(response.geturl()),
                "artifact_redirect_rejected",
                "Actions artifact did not resolve to trusted storage",
            )
            payload = response.read(MAX_ARCHIVE_BYTES + 1)
    except AcceptedSummaryConsumerError:
        raise
    except (OSError, urllib.error.URLError) as exc:
        fail("artifact_download_failed", f"Actions artifact download failed: {exc}")
    require(
        0 < len(payload) <= MAX_ARCHIVE_BYTES,
        "artifact_archive_invalid",
        "Actions artifact archive is empty or oversized",
    )
    return payload


def _object(value: Any, label: str) -> Mapping[str, Any]:
    require(isinstance(value, Mapping), "github_response_invalid", f"{label} is not an object")
    return value


def _api(repository: str, suffix: str) -> str:
    return f"{API_ROOT}/repos/{repository}{suffix}"


def _query(base: str, values: Sequence[tuple[str, Any]]) -> str:
    return base + "?" + urllib.parse.urlencode(values)


def _paginate_wrapped(
    fetch: JsonFetcher, base: str, key: str, *, label: str
) -> list[Mapping[str, Any]]:
    collected: list[Mapping[str, Any]] = []
    declared_total: int | None = None
    seen_ids: set[int] = set()
    for page in range(1, MAX_PAGES + 1):
        document = _object(
            fetch(_query(base, (("per_page", PER_PAGE), ("page", page)))), label
        )
        values = document.get(key)
        total = document.get("total_count")
        require(
            isinstance(values, list)
            and isinstance(total, int)
            and not isinstance(total, bool)
            and total >= 0
            and all(isinstance(item, Mapping) for item in values),
            "pagination_invalid",
            f"{label} page is malformed",
        )
        if declared_total is None:
            declared_total = total
        require(total == declared_total, "pagination_invalid", f"{label} total changed")
        for item in values:
            item_id = positive_integer(item.get("id"), f"{label}.id")
            require(item_id not in seen_ids, "pagination_invalid", f"{label} repeats an ID")
            seen_ids.add(item_id)
            collected.append(item)
        if len(values) < PER_PAGE:
            require(
                len(collected) == declared_total,
                "pagination_invalid",
                f"{label} pagination is incomplete",
            )
            return collected
    fail("pagination_invalid", f"{label} exceeds the page limit")


def _paginate_list(fetch: JsonFetcher, base: str, *, label: str) -> list[Mapping[str, Any]]:
    collected: list[Mapping[str, Any]] = []
    seen_ids: set[int] = set()
    for page in range(1, MAX_PAGES + 1):
        values = fetch(_query(base, (("per_page", PER_PAGE), ("page", page))))
        require(
            isinstance(values, list) and all(isinstance(item, Mapping) for item in values),
            "pagination_invalid",
            f"{label} page is malformed",
        )
        for item in values:
            item_id = positive_integer(item.get("id"), f"{label}.id")
            require(item_id not in seen_ids, "pagination_invalid", f"{label} repeats an ID")
            seen_ids.add(item_id)
            collected.append(item)
        if len(values) < PER_PAGE:
            return collected
    fail("pagination_invalid", f"{label} exceeds the page limit")


def _parse_summary_archive(payload: bytes) -> tuple[Mapping[str, Any], str]:
    try:
        with zipfile.ZipFile(io.BytesIO(payload), "r") as archive:
            members = archive.infolist()
            require(
                not archive.comment and len(members) == 1,
                "summary_archive_invalid",
                "summary ZIP must contain exactly one uncommented member",
            )
            member = members[0]
            mode = (member.external_attr >> 16) & 0xFFFF
            require(
                member.filename == SUMMARY_JSON_NAME
                and not member.is_dir()
                and not stat.S_ISLNK(mode)
                and not (member.flag_bits & 0x1)
                and 0 < member.file_size <= MAX_SUMMARY_BYTES,
                "summary_archive_invalid",
                "summary ZIP member is unsafe or oversized",
            )
            summary_bytes = archive.read(member)
    except AcceptedSummaryConsumerError:
        raise
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        fail("summary_archive_invalid", f"summary ZIP is invalid: {exc}")
    require(
        len(summary_bytes) <= MAX_SUMMARY_BYTES,
        "summary_archive_invalid",
        "summary JSON exceeds the size limit",
    )
    try:
        document = json.loads(summary_bytes.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        fail("summary_json_invalid", f"summary JSON is invalid: {exc}")
    require(isinstance(document, Mapping), "summary_json_invalid", "summary root is not an object")
    return document, hashlib.sha256(summary_bytes).hexdigest()


def _validate_inventory(
    value: Any, *, expected_count: int, label: str
) -> tuple[dict[int, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    require(
        isinstance(value, list)
        and len(value) == expected_count
        and all(isinstance(item, Mapping) for item in value),
        "summary_inventory_invalid",
        f"{label} must contain exactly {expected_count} assets",
    )
    by_id: dict[int, Mapping[str, Any]] = {}
    by_name: dict[str, Mapping[str, Any]] = {}
    digests: set[str] = set()
    for offset, item in enumerate(value):
        asset_id = positive_integer(item.get("asset_id"), f"{label}[{offset}].asset_id")
        name = item.get("name")
        size = item.get("size")
        digest = bare_digest(item.get("sha256"), f"{label}[{offset}].sha256", prefix_optional=True)
        require(
            isinstance(name, str)
            and bool(name)
            and name == Path(name).name
            and isinstance(size, int)
            and not isinstance(size, bool)
            and size >= 0
            and asset_id not in by_id
            and name not in by_name
            and digest not in digests,
            "summary_inventory_invalid",
            f"{label}[{offset}] is duplicated, unsafe, or malformed",
        )
        by_id[asset_id] = item
        by_name[name] = item
        digests.add(digest)
    return by_id, by_name


def _asset_matches(
    declared: Mapping[str, Any], inventory: Mapping[str, Any], *, prefixed: bool
) -> bool:
    value = declared.get("sha256")
    if not isinstance(value, str):
        return False
    digest = value[7:] if value.startswith("sha256:") else value
    return (
        declared.get("name") == inventory.get("name")
        and declared.get("size", inventory.get("size")) == inventory.get("size")
        and digest == inventory.get("sha256")
        and (not prefixed or value.startswith("sha256:"))
    )


def _slot_assets(
    slot: Mapping[str, Any],
    *,
    inventory_by_id: Mapping[int, Mapping[str, Any]],
    inventory_by_name: Mapping[str, Mapping[str, Any]],
    used_asset_ids: set[int],
    evidence_release: Mapping[str, Any],
    repository: str,
    label: str,
) -> tuple[str, str]:
    release = slot.get("release")
    index = slot.get("asset_index")
    assets = slot.get("assets")
    require(
        isinstance(release, Mapping)
        and release.get("repository") == repository
        and release.get("release_id") == evidence_release.get("release_id")
        and release.get("release_tag") == evidence_release.get("tag")
        and isinstance(index, Mapping)
        and isinstance(assets, list)
        and len(assets) == 3
        and all(isinstance(item, Mapping) for item in assets),
        "summary_lineage_invalid",
        f"{label} has no valid evidence Release bundle",
    )
    index_name = index.get("name")
    index_asset = inventory_by_name.get(index_name) if isinstance(index_name, str) else None
    require(
        index_asset is not None and _asset_matches(index, index_asset, prefixed=True),
        "summary_lineage_invalid",
        f"{label} asset index is absent or misbound",
    )
    index_id = positive_integer(index_asset.get("asset_id"), f"{label}.asset_index.id")
    require(index_id not in used_asset_ids, "summary_lineage_invalid", f"{label} reuses an asset")
    used_asset_ids.add(index_id)
    kinds: set[str] = set()
    for asset in assets:
        asset_id = positive_integer(asset.get("asset_id"), f"{label}.asset.id")
        inventory = inventory_by_id.get(asset_id)
        kind = asset.get("evidence_kind")
        require(
            inventory is not None
            and _asset_matches(asset, inventory, prefixed=True)
            and isinstance(kind, str)
            and kind not in kinds
            and asset_id not in used_asset_ids,
            "summary_lineage_invalid",
            f"{label} contains an absent, repeated, or misbound asset",
        )
        kinds.add(kind)
        used_asset_ids.add(asset_id)
    require(
        kinds == {"raw_export", "evidence_envelope", "verifier_report"},
        "summary_lineage_invalid",
        f"{label} evidence roles are incomplete",
    )
    evidence_id = slot.get("evidence_id")
    digest = slot.get("live_result_digest")
    require(
        isinstance(evidence_id, str)
        and bool(evidence_id)
        and isinstance(digest, str),
        "summary_lineage_invalid",
        f"{label} has no evidence identity",
    )
    bare_digest(digest, f"{label}.live_result_digest")
    positive_integer(slot.get("verifier_workflow_run_id"), f"{label}.verifier_workflow_run_id")
    parse_time(slot.get("verified_at"), f"{label}.verified_at")
    return evidence_id, digest


def _validate_source_summary(
    summary: Mapping[str, Any],
    *,
    repository: str,
    run_id: int,
    run_attempt: int,
    source_commit: str,
) -> dict[str, Any]:
    expected_top = {
        "schema_version",
        "acceptance_scope",
        "external_consumer_required",
        "counts_as_phase78_closure",
        "workflow_path",
        "workflow_event",
        "repository",
        "run_id",
        "run_attempt",
        "trusted_source_commit",
        "releases",
        "candidate_assets",
        "candidate_ledger_sha256",
        "evidence_inventory",
        "candidate_release_inventory",
        "phase7",
        "phase8",
        "release_evidence",
        "final_status",
    }
    require(
        set(summary) == expected_top
        and summary.get("schema_version") == SOURCE_SUMMARY_SCHEMA
        and summary.get("acceptance_scope") == "producer_internal"
        and summary.get("external_consumer_required") is True
        and summary.get("counts_as_phase78_closure") is False
        and summary.get("workflow_path") == SOURCE_WORKFLOW_PATH
        and summary.get("workflow_event") == "workflow_dispatch"
        and summary.get("repository") == repository
        and summary.get("run_id") == run_id
        and summary.get("run_attempt") == run_attempt
        and summary.get("trusted_source_commit") == source_commit,
        "summary_identity_invalid",
        "accepted summary identity or producer scope is invalid",
    )
    releases = summary.get("releases")
    require(
        isinstance(releases, Mapping) and set(releases) == {"evidence", "candidate"},
        "summary_release_invalid",
        "accepted summary has no two-Release identity",
    )
    evidence_release = releases.get("evidence")
    candidate_release = releases.get("candidate")
    require(
        isinstance(evidence_release, Mapping)
        and isinstance(candidate_release, Mapping)
        and evidence_release.get("immutable") is True
        and candidate_release.get("immutable") is True
        and full_commit(
            evidence_release.get("final_commit"), "evidence release final_commit"
        )
        == source_commit
        and full_commit(
            candidate_release.get("final_commit"), "candidate release final_commit"
        )
        == source_commit
        and positive_integer(evidence_release.get("release_id"), "evidence release ID")
        != positive_integer(candidate_release.get("release_id"), "candidate release ID")
        and isinstance(evidence_release.get("tag"), str)
        and isinstance(candidate_release.get("tag"), str)
        and evidence_release.get("tag") != candidate_release.get("tag"),
        "summary_release_invalid",
        "accepted summary Releases are mutable, missing, or aliased",
    )
    evidence_by_id, evidence_by_name = _validate_inventory(
        summary.get("evidence_inventory"), expected_count=120, label="evidence_inventory"
    )
    candidate_by_id, _ = _validate_inventory(
        summary.get("candidate_release_inventory"),
        expected_count=4,
        label="candidate_release_inventory",
    )
    candidate_assets = summary.get("candidate_assets")
    require(
        isinstance(candidate_assets, list)
        and len(candidate_assets) == 4
        and all(isinstance(item, Mapping) for item in candidate_assets)
        and {item.get("asset_id") for item in candidate_assets} == set(candidate_by_id)
        and all(candidate_by_id[item["asset_id"]] == item for item in candidate_assets),
        "summary_inventory_invalid",
        "candidate asset selection does not equal the four-asset Release inventory",
    )
    ledger_digest = bare_digest(
        summary.get("candidate_ledger_sha256"),
        "candidate_ledger_sha256",
        prefix_optional=True,
    )
    require(
        sum(item.get("sha256") == ledger_digest for item in candidate_assets) == 1,
        "summary_lineage_invalid",
        "candidate ledger digest does not bind exactly one candidate asset",
    )

    used_assets: set[int] = set()
    evidence_ids: set[str] = set()
    live_digests: set[str] = set()
    release_evidence = summary.get("release_evidence")
    expected_release_evidence_fields = {
        "adapter_id",
        "release_stage",
        "stage_a_predecessor_scope",
        "stage_a_verified_record_count",
        "stage_a_closure",
        "verified_record_count",
        "historical_verified_record_count",
        "provider_verified",
        "items",
        "history_items",
        "unique_current_chain_count",
        "unique_current_evidence_id_count",
        "unique_current_chain_digest_count",
    }
    require(
        isinstance(release_evidence, Mapping)
        and set(release_evidence) == expected_release_evidence_fields
        and isinstance(release_evidence.get("adapter_id"), str)
        and bool(release_evidence.get("adapter_id"))
        and release_evidence.get("verified_record_count") == 8
        and release_evidence.get("provider_verified") is False
        and release_evidence.get("unique_current_chain_count") == 30
        and release_evidence.get("unique_current_evidence_id_count") == 30
        and release_evidence.get("unique_current_chain_digest_count") == 120,
        "summary_evidence_invalid",
        "release evidence counts or trust level are invalid",
    )
    items = release_evidence.get("items")
    history = release_evidence.get("history_items")
    require(
        isinstance(items, list)
        and len(items) == 8
        and all(isinstance(item, Mapping) for item in items)
        and isinstance(history, list)
        and all(isinstance(item, Mapping) for item in history)
        and release_evidence.get("historical_verified_record_count") == len(history),
        "summary_evidence_invalid",
        "release evidence inventories are malformed",
    )
    release_stage = release_evidence.get("release_stage")
    predecessor_scope = release_evidence.get("stage_a_predecessor_scope")
    predecessor_count = release_evidence.get("stage_a_verified_record_count")
    stage_a_closure = release_evidence.get("stage_a_closure")
    if release_stage == "A":
        require(
            predecessor_scope is None
            and predecessor_count == 0
            and stage_a_closure is None,
            "summary_evidence_invalid",
            "Stage A summary claims a Stage A predecessor binding",
        )
    elif release_stage == "B":
        predecessor_items = [
            item
            for item in history
            if isinstance(item, Mapping)
            and item.get("release_scope") == predecessor_scope
        ]
        expected_predecessor_types = {
            *EXTERNAL_RECORD_PATHS,
            PHASE78_CLOSURE_EVIDENCE_TYPE,
        }
        require(
            isinstance(predecessor_scope, str)
            and re.fullmatch(r"previous_releases\[\d+\]", predecessor_scope) is not None
            and predecessor_count == len(expected_predecessor_types)
            and len(predecessor_items) == len(expected_predecessor_types)
            and {item.get("evidence_type") for item in predecessor_items}
            == expected_predecessor_types,
            "summary_evidence_invalid",
            "Stage B summary lacks a complete live-verified Stage A predecessor",
        )
        closure_history = [
            item
            for item in predecessor_items
            if item.get("evidence_type") == PHASE78_CLOSURE_EVIDENCE_TYPE
        ]
        require(
            isinstance(stage_a_closure, Mapping)
            and set(stage_a_closure)
            == {
                "release_scope",
                "evidence_type",
                "source_commit",
                "release_stage",
                "producer_summary_schema",
                "producer_run_id",
                "producer_run_attempt",
                "producer_summary_sha256",
                "consumer_result_schema",
                "consumer_run_id",
                "consumer_run_attempt",
                "consumer_result_sha256",
                "phase7_verified_runtime_count",
                "phase8_verified_reviewer_count",
                "phase8_verified_retrieval_count",
                "phase8_verified_slot_count",
                "verification_level",
                "provider_verified",
                "counts_as_phase78_closure",
                "accepted",
                "evidence_id",
                "locator_sha256",
                "validated_result_sha256",
                "verifier_workflow_run_id",
                "verified_at",
            }
            and len(closure_history) == 1
            and stage_a_closure.get("release_scope") == predecessor_scope
            and stage_a_closure.get("evidence_type")
            == PHASE78_CLOSURE_EVIDENCE_TYPE
            and stage_a_closure.get("source_commit")
            == closure_history[0].get("source_commit")
            and stage_a_closure.get("release_stage") == "A"
            and stage_a_closure.get("producer_summary_schema")
            in PHASE78_CLOSURE_PRODUCER_SCHEMAS
            and stage_a_closure.get("consumer_result_schema")
            == PHASE78_CLOSURE_CONSUMER_SCHEMA
            and stage_a_closure.get("phase7_verified_runtime_count") == 10
            and stage_a_closure.get("phase8_verified_reviewer_count") == 6
            and stage_a_closure.get("phase8_verified_retrieval_count") == 6
            and stage_a_closure.get("phase8_verified_slot_count") == 12
            and stage_a_closure.get("verification_level") == "preview_attested"
            and stage_a_closure.get("provider_verified") is False
            and stage_a_closure.get("counts_as_phase78_closure") is True
            and stage_a_closure.get("accepted") is True
            and all(
                stage_a_closure.get(field) == closure_history[0].get(field)
                for field in (
                    "evidence_id",
                    "locator_sha256",
                    "validated_result_sha256",
                    "verifier_workflow_run_id",
                    "verified_at",
                )
            ),
            "summary_evidence_invalid",
            "Stage B summary lacks an accepted, live-bound 10+12 Stage A closure",
        )
        positive_integer(
            stage_a_closure.get("producer_run_id"),
            "stage_a_closure.producer_run_id",
        )
        positive_integer(
            stage_a_closure.get("producer_run_attempt"),
            "stage_a_closure.producer_run_attempt",
        )
        positive_integer(
            stage_a_closure.get("consumer_run_id"),
            "stage_a_closure.consumer_run_id",
        )
        positive_integer(
            stage_a_closure.get("consumer_run_attempt"),
            "stage_a_closure.consumer_run_attempt",
        )
        bare_digest(
            stage_a_closure.get("producer_summary_sha256"),
            "stage_a_closure.producer_summary_sha256",
            prefix_optional=True,
        )
        bare_digest(
            stage_a_closure.get("consumer_result_sha256"),
            "stage_a_closure.consumer_result_sha256",
            prefix_optional=True,
        )
    else:
        fail("summary_evidence_invalid", "release stage is neither A nor B")
    require(
        {item.get("evidence_type") for item in items} == set(EXTERNAL_RECORD_PATHS),
        "summary_evidence_invalid",
        "release evidence types are incomplete or duplicated",
    )
    for offset, item in enumerate(items):
        locator = item.get("evidence_locator")
        verified_ids = item.get("verified_asset_ids")
        require(
            item.get("status") == "preview_attested"
            and item.get("provider_verified") is False
            and item.get("live_requery_succeeded") is True
            and isinstance(locator, Mapping)
            and locator.get("repository") == repository
            and locator.get("release_id") == evidence_release.get("release_id")
            and locator.get("release_tag") == evidence_release.get("tag")
            and isinstance(verified_ids, list)
            and len(verified_ids) == 4,
            "summary_evidence_invalid",
            f"release evidence item {offset} is not Preview-attested and bound",
        )
        locator_ids: set[int] = set()
        for field in (
            "envelope_asset",
            "release_asset_index_asset",
            "raw_export_asset",
            "verifier_report_asset",
        ):
            asset = locator.get(field)
            require(isinstance(asset, Mapping), "summary_lineage_invalid", f"{field} is missing")
            asset_id = positive_integer(asset.get("asset_id"), f"release item {offset}.{field}.id")
            inventory = evidence_by_id.get(asset_id)
            require(
                inventory is not None
                and _asset_matches(asset, inventory, prefixed=False)
                and asset_id not in locator_ids
                and asset_id not in used_assets,
                "summary_lineage_invalid",
                f"release item {offset}.{field} is absent, reused, or misbound",
            )
            locator_ids.add(asset_id)
            used_assets.add(asset_id)
        require(
            set(verified_ids) == locator_ids,
            "summary_lineage_invalid",
            f"release item {offset} verified asset IDs do not bind its locator",
        )
        evidence_id = item.get("evidence_id")
        require(
            isinstance(evidence_id, str) and bool(evidence_id) and evidence_id not in evidence_ids,
            "summary_lineage_invalid",
            f"release item {offset} repeats or omits its evidence ID",
        )
        evidence_ids.add(evidence_id)
        for key in ("locator_sha256", "validated_result_sha256"):
            bare_digest(item.get(key), f"release item {offset}.{key}")
        positive_integer(item.get("verifier_workflow_run_id"), f"release item {offset}.run_id")
        parse_time(item.get("verified_at"), f"release item {offset}.verified_at")
    for offset, item in enumerate(history):
        require(
            item.get("status") == "preview_attested"
            and item.get("provider_verified") is False
            and isinstance(item.get("evidence_locator"), Mapping),
            "summary_evidence_invalid",
            f"historical release evidence item {offset} is malformed",
        )
        full_commit(item.get("source_commit"), f"history item {offset}.source_commit")

    phase7 = summary.get("phase7")
    require(
        isinstance(phase7, Mapping)
        and phase7.get("phase_status") == "complete_preview_attested"
        and phase7.get("verification_level") == "preview_attested"
        and phase7.get("provider_verified") is False
        and phase7.get("verified_runtime_count") == 10
        and phase7.get("happy_count") == 5
        and phase7.get("control_count") == 5
        and phase7.get("verified_completion_gate_count") == 13
        and phase7.get("pending_gate_count") == 0,
        "summary_phase7_invalid",
        "Phase 7 completion fields are invalid",
    )
    phase7_items = phase7.get("items")
    phase7_slots = phase7.get("live_slot_results")
    require(
        isinstance(phase7_items, list)
        and len(phase7_items) == 10
        and all(isinstance(item, Mapping) for item in phase7_items)
        and isinstance(phase7_slots, list)
        and len(phase7_slots) == 10
        and all(isinstance(item, Mapping) for item in phase7_slots),
        "summary_phase7_invalid",
        "Phase 7 item or live-slot inventory is incomplete",
    )
    require(
        {(item.get("workflow"), item.get("case_kind")) for item in phase7_items}
        == EXPECTED_PHASE7_MATRIX,
        "summary_phase7_invalid",
        "Phase 7 workflow matrix is incomplete or duplicated",
    )
    phase7_by_receipt: dict[str, Mapping[str, Any]] = {}
    for item in phase7_items:
        receipt_id = item.get("receipt_id")
        require(
            isinstance(receipt_id, str)
            and bool(receipt_id)
            and receipt_id not in phase7_by_receipt
            and item.get("status") == "verified"
            and item.get("verification_level") == "preview_attested",
            "summary_phase7_invalid",
            "Phase 7 runtime item is repeated or not verified",
        )
        phase7_by_receipt[receipt_id] = item
    require(
        {slot.get("receipt_id") for slot in phase7_slots} == set(phase7_by_receipt),
        "summary_phase7_invalid",
        "Phase 7 live slots do not match runtime receipts",
    )
    for slot in phase7_slots:
        receipt_id = str(slot.get("receipt_id"))
        item = phase7_by_receipt[receipt_id]
        evidence_id, live_digest = _slot_assets(
            slot,
            inventory_by_id=evidence_by_id,
            inventory_by_name=evidence_by_name,
            used_asset_ids=used_assets,
            evidence_release=evidence_release,
            repository=repository,
            label=f"phase7.{receipt_id}",
        )
        require(
            item.get("external_evidence_id") == evidence_id
            and item.get("external_live_result_digest") == live_digest
            and item.get("external_verifier_workflow_run_id")
            == slot.get("verifier_workflow_run_id")
            and item.get("external_verified_at") == slot.get("verified_at"),
            "summary_lineage_invalid",
            f"Phase 7 receipt {receipt_id} does not bind its live slot",
        )
        require(
            evidence_id not in evidence_ids and live_digest not in live_digests,
            "summary_lineage_invalid",
            "Phase 7 reuses a live evidence identity",
        )
        evidence_ids.add(evidence_id)
        live_digests.add(live_digest)

    phase8 = summary.get("phase8")
    require(
        isinstance(phase8, Mapping)
        and phase8.get("phase_status") == "complete_preview_attested"
        and phase8.get("verification_level") == "preview_attested"
        and phase8.get("provider_verified") is False
        and phase8.get("retrieval_distribution") == EXPECTED_RETRIEVAL_DISTRIBUTION
        and phase8.get("stale_count") == 0
        and phase8.get("false_ready_count") == 0,
        "summary_phase8_invalid",
        "Phase 8 completion fields are invalid",
    )
    reviewers = phase8.get("reviewer_items")
    retrieval = phase8.get("retrieval_items")
    phase8_slots = phase8.get("live_slot_results")
    require(
        isinstance(reviewers, list)
        and len(reviewers) == 6
        and all(isinstance(item, Mapping) for item in reviewers)
        and isinstance(retrieval, list)
        and len(retrieval) == 6
        and all(isinstance(item, Mapping) for item in retrieval)
        and isinstance(phase8_slots, list)
        and len(phase8_slots) == 12
        and all(isinstance(item, Mapping) for item in phase8_slots),
        "summary_phase8_invalid",
        "Phase 8 reviewer, retrieval, or live-slot inventory is incomplete",
    )
    reviewer_runs: set[str] = set()
    reviewer_instances: set[str] = set()
    case_counts: dict[str, int] = {}
    case_inputs: dict[str, str] = {}
    for item in reviewers:
        case_id = item.get("case_id")
        run_identity = item.get("run_id")
        instance = item.get("reviewer_instance_id")
        input_digest = item.get("input_digest")
        review_digest = item.get("review_digest")
        require(
            isinstance(case_id, str)
            and item.get("reviewer_skill") == EXPECTED_PHASE8_REVIEWER_CASES.get(case_id)
            and isinstance(run_identity, str)
            and bool(run_identity)
            and run_identity not in reviewer_runs
            and isinstance(instance, str)
            and bool(instance)
            and instance not in reviewer_instances
            and item.get("verification_level") == "preview_attested"
            and item.get("provider_verified") is False
            and isinstance(input_digest, str)
            and isinstance(review_digest, str),
            "summary_phase8_invalid",
            "Phase 8 reviewer identity, role, or trust level is invalid",
        )
        bare_digest(input_digest, f"phase8.{case_id}.input_digest")
        bare_digest(review_digest, f"phase8.{case_id}.review_digest")
        reviewer_runs.add(run_identity)
        reviewer_instances.add(instance)
        case_counts[case_id] = case_counts.get(case_id, 0) + 1
        if case_id in case_inputs:
            require(
                case_inputs[case_id] == input_digest,
                "summary_phase8_invalid",
                f"Phase 8 case {case_id} changed frozen input",
            )
        case_inputs[case_id] = input_digest
    require(
        case_counts == {case_id: 2 for case_id in EXPECTED_PHASE8_REVIEWER_CASES},
        "summary_phase8_invalid",
        "Phase 8 fresh-repeat reviewer matrix is incomplete",
    )
    retrieval_map: dict[str, str] = {}
    for item in retrieval:
        receipt_id = item.get("receipt_id")
        kind = item.get("kind")
        require(
            isinstance(receipt_id, str)
            and EXPECTED_PHASE8_RETRIEVAL_RECEIPTS.get(receipt_id) == kind
            and receipt_id not in retrieval_map
            and item.get("evidence_status") == "preview_attested"
            and item.get("evidence_trust_level") == "preview_attested",
            "summary_phase8_invalid",
            "Phase 8 retrieval receipt is duplicated, stale, or misclassified",
        )
        retrieval_map[receipt_id] = str(kind)
    require(
        retrieval_map == EXPECTED_PHASE8_RETRIEVAL_RECEIPTS,
        "summary_phase8_invalid",
        "Phase 8 retrieval receipt set is incomplete",
    )
    expected_slots = {value: "reviewer" for value in reviewer_runs}
    expected_slots.update({value: "retrieval" for value in retrieval_map})
    require(
        {slot.get("slot_id"): slot.get("slot_kind") for slot in phase8_slots}
        == expected_slots,
        "summary_phase8_invalid",
        "Phase 8 live slots do not match reviewer and retrieval identities",
    )
    execution_ids: set[str] = set()
    for slot in phase8_slots:
        slot_id = str(slot.get("slot_id"))
        execution_id = slot.get("execution_id")
        require(
            isinstance(execution_id, str)
            and bool(execution_id)
            and execution_id not in execution_ids,
            "summary_phase8_invalid",
            "Phase 8 live execution identity is missing or reused",
        )
        execution_ids.add(execution_id)
        bare_digest(slot.get("subject_digest"), f"phase8.{slot_id}.subject_digest")
        evidence_id, live_digest = _slot_assets(
            slot,
            inventory_by_id=evidence_by_id,
            inventory_by_name=evidence_by_name,
            used_asset_ids=used_assets,
            evidence_release=evidence_release,
            repository=repository,
            label=f"phase8.{slot_id}",
        )
        require(
            evidence_id not in evidence_ids and live_digest not in live_digests,
            "summary_lineage_invalid",
            "Phase 8 reuses a live evidence identity",
        )
        evidence_ids.add(evidence_id)
        live_digests.add(live_digest)
    require(
        used_assets == set(evidence_by_id)
        and len(evidence_ids) == 30
        and len(live_digests) == 22,
        "summary_lineage_invalid",
        "current R/E/V/I assets or live evidence identities are not globally unique and complete",
    )
    final = summary.get("final_status")
    require(
        final
        == {
            "phase7": "complete_preview_attested",
            "phase8": "complete_preview_attested",
            "provider_verified": False,
            "accepted": True,
        },
        "summary_final_status_invalid",
        "producer internal final status is not exactly accepted Preview evidence",
    )
    return {
        "schema_version": summary.get("schema_version"),
        "release_stage": release_stage,
        "stage_a_predecessor_scope": predecessor_scope,
        "stage_a_verified_record_count": predecessor_count,
        "stage_a_closure_consumer_result_sha256": (
            stage_a_closure.get("consumer_result_sha256")
            if isinstance(stage_a_closure, Mapping)
            else None
        ),
        "evidence_release_id": evidence_release.get("release_id"),
        "evidence_release_tag": evidence_release.get("tag"),
        "candidate_release_id": candidate_release.get("release_id"),
        "candidate_release_tag": candidate_release.get("tag"),
        "candidate_ledger_sha256": ledger_digest,
        "phase7_live_slot_count": 10,
        "phase8_reviewer_count": 6,
        "phase8_retrieval_count": 6,
        "current_evidence_id_count": 30,
        "current_asset_count": 120,
    }


def _same_job_identity(value: Mapping[str, Any], expected: Mapping[str, Any]) -> bool:
    fields = (
        "id",
        "run_id",
        "run_attempt",
        "head_sha",
        "head_branch",
        "name",
        "status",
        "conclusion",
        "html_url",
        "started_at",
        "completed_at",
    )
    return all(value.get(field) == expected.get(field) for field in fields)


def _environment_policy_snapshot(
    environment: Mapping[str, Any], branch_policies: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    rules = environment.get("protection_rules")
    require(
        isinstance(rules, list) and all(isinstance(rule, Mapping) for rule in rules),
        "environment_policy_invalid",
        "Environment protection rules are malformed",
    )
    canonical = lambda value: json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return {
        "id": environment.get("id"),
        "name": environment.get("name"),
        "url": environment.get("url"),
        "updated_at": environment.get("updated_at"),
        "deployment_branch_policy": canonical(
            environment.get("deployment_branch_policy")
        ),
        "protection_rules": sorted(canonical(rule) for rule in rules),
        "branch_policies": sorted(canonical(policy) for policy in branch_policies),
    }


def _validate_status_history(
    statuses: Sequence[Mapping[str, Any]],
    *,
    success_status: Mapping[str, Any],
    protected_job_url: str,
) -> None:
    timed_statuses = [
        (
            parse_time(item.get("created_at"), "deployment status.created_at"),
            item,
        )
        for item in statuses
    ]
    ordered = [item for _, item in sorted(timed_statuses, key=lambda pair: pair[0])]
    matching_successes = [
        item
        for item in ordered
        if item.get("state") == "success"
        and item.get("log_url") == protected_job_url
    ]
    noninactive = [
        (created_at, item)
        for created_at, item in timed_statuses
        if item.get("state") != "inactive"
    ]
    maximum_noninactive_time = max(
        (created_at for created_at, _ in noninactive), default=None
    )
    terminal_noninactive = [
        item
        for created_at, item in noninactive
        if created_at == maximum_noninactive_time
    ]
    success_time = parse_time(success_status.get("created_at"), "success status.created_at")
    require(
        len(matching_successes) == 1
        and matching_successes[0].get("id") == success_status.get("id")
        and len(terminal_noninactive) == 1
        and terminal_noninactive[0].get("state") == "success"
        and terminal_noninactive[0].get("id") == success_status.get("id")
        and terminal_noninactive[0].get("log_url") == protected_job_url
        and not any(
            item.get("state") in {"failure", "error"}
            and parse_time(item.get("created_at"), "deployment status.created_at")
            > success_time
            for item in ordered
        ),
        "deployment_binding_invalid",
        "deployment has no unique final success for the protected job",
    )


def verify(
    *,
    repository: str,
    run_id: int,
    run_attempt: int,
    source_commit: str,
    consumer_commit: str,
    consumer_run_id: int,
    consumer_run_attempt: int,
    json_fetcher: JsonFetcher = github_json,
    binary_fetcher: BinaryFetcher = github_artifact,
    now: datetime | None = None,
) -> dict[str, Any]:
    require(
        REPOSITORY_RE.fullmatch(repository) is not None,
        "identity_invalid",
        "repository must be owner/name",
    )
    positive_integer(run_id, "run_id")
    positive_integer(run_attempt, "run_attempt")
    positive_integer(consumer_run_id, "consumer_run_id")
    positive_integer(consumer_run_attempt, "consumer_run_attempt")
    full_commit(source_commit, "source_commit")
    full_commit(consumer_commit, "consumer_commit")
    require(
        consumer_commit == source_commit,
        "consumer_source_drift",
        "default branch advanced; re-dispatch accepted evidence on the current commit",
    )

    repository_api = _object(json_fetcher(_api(repository, "")), "repository")
    repository_id = positive_integer(repository_api.get("id"), "repository.id")
    require(
        repository_api.get("full_name") == repository
        and repository_api.get("default_branch") == DEFAULT_BRANCH,
        "repository_identity_invalid",
        "repository identity or default branch is unexpected",
    )
    latest_run = _object(
        json_fetcher(_api(repository, f"/actions/runs/{run_id}")), "latest workflow run"
    )
    exact_run = _object(
        json_fetcher(
            _api(repository, f"/actions/runs/{run_id}/attempts/{run_attempt}")
        ),
        "exact workflow attempt",
    )
    workflow_id = positive_integer(exact_run.get("workflow_id"), "workflow_id")
    run_repository = exact_run.get("repository")
    head_repository = exact_run.get("head_repository")
    expected_run_url = f"https://github.com/{repository}/actions/runs/{run_id}"
    require(
        latest_run.get("id") == run_id
        and latest_run.get("run_attempt") == run_attempt
        and latest_run.get("head_sha") == source_commit
        and exact_run.get("id") == run_id
        and exact_run.get("run_attempt") == run_attempt
        and exact_run.get("event") == "workflow_dispatch"
        and exact_run.get("path") == SOURCE_WORKFLOW_PATH
        and exact_run.get("name") == SOURCE_WORKFLOW_NAME
        and exact_run.get("head_branch") == DEFAULT_BRANCH
        and exact_run.get("head_sha") == source_commit
        and exact_run.get("status") == "completed"
        and exact_run.get("conclusion") == "success"
        and exact_run.get("html_url") == expected_run_url
        and isinstance(run_repository, Mapping)
        and run_repository.get("id") == repository_id
        and run_repository.get("full_name") == repository
        and isinstance(head_repository, Mapping)
        and head_repository.get("id") == repository_id
        and head_repository.get("full_name") == repository,
        "workflow_attempt_invalid",
        "exact successful source attempt is not the latest trusted main run",
    )
    workflow = _object(
        json_fetcher(_api(repository, f"/actions/workflows/{workflow_id}")),
        "source workflow",
    )
    require(
        workflow.get("id") == workflow_id
        and workflow.get("name") == SOURCE_WORKFLOW_NAME
        and workflow.get("path") == SOURCE_WORKFLOW_PATH
        and workflow.get("state") == "active",
        "workflow_identity_invalid",
        "source workflow identity or active state is invalid",
    )

    jobs = _paginate_wrapped(
        json_fetcher,
        _api(repository, f"/actions/runs/{run_id}/attempts/{run_attempt}/jobs"),
        "jobs",
        label="exact-attempt jobs",
    )
    protected_matches = [job for job in jobs if job.get("name") == PROTECTED_JOB_NAME]
    preflight_matches = [job for job in jobs if job.get("name") == PREFLIGHT_JOB_NAME]
    require(
        len(protected_matches) == 1 and len(preflight_matches) == 1,
        "protected_job_invalid",
        "exact attempt has no unique preflight and protected validation jobs",
    )
    protected_job = protected_matches[0]
    preflight_job = preflight_matches[0]
    protected_job_id = positive_integer(protected_job.get("id"), "protected job ID")
    protected_job_url = (
        f"https://github.com/{repository}/actions/runs/{run_id}/job/{protected_job_id}"
    )
    for label, job in (("preflight", preflight_job), ("protected", protected_job)):
        require(
            job.get("run_id") == run_id
            and job.get("run_attempt") == run_attempt
            and job.get("head_sha") == source_commit
            and job.get("head_branch") == DEFAULT_BRANCH
            and job.get("status") == "completed"
            and job.get("conclusion") == "success",
            "protected_job_invalid",
            f"{label} job is failed, incomplete, or misbound",
        )
    require(
        protected_job.get("html_url") == protected_job_url,
        "protected_job_invalid",
        "protected job HTML URL is not canonical",
    )
    direct_job = _object(
        json_fetcher(_api(repository, f"/actions/jobs/{protected_job_id}")),
        "direct protected job",
    )
    require(
        _same_job_identity(direct_job, protected_job),
        "protected_job_invalid",
        "direct protected job differs from exact-attempt job listing",
    )
    job_started = parse_time(protected_job.get("started_at"), "protected job started_at")
    job_completed = parse_time(protected_job.get("completed_at"), "protected job completed_at")
    require(job_started <= job_completed, "timestamp_invalid", "protected job timestamps are reversed")

    environment_url = _api(repository, f"/environments/{ENVIRONMENT_NAME}")
    environment = _object(json_fetcher(environment_url), "governance environment")
    environment_id = positive_integer(environment.get("id"), "environment.id")
    rules = environment.get("protection_rules")
    branch_config = environment.get("deployment_branch_policy")
    require(
        environment.get("name") == ENVIRONMENT_NAME
        and environment.get("url") == environment_url
        and isinstance(rules, list)
        and all(isinstance(rule, Mapping) for rule in rules)
        and isinstance(branch_config, Mapping)
        and branch_config.get("protected_branches") is False
        and branch_config.get("custom_branch_policies") is True,
        "environment_policy_invalid",
        "governance Environment identity or branch mode is invalid",
    )
    reviewer_rules = [rule for rule in rules if rule.get("type") == "required_reviewers"]
    branch_rules = [rule for rule in rules if rule.get("type") == "branch_policy"]
    require(
        len(reviewer_rules) == 1 and len(branch_rules) == 1,
        "environment_policy_invalid",
        "governance Environment has no unique reviewer and branch rules",
    )
    reviewers = reviewer_rules[0].get("reviewers")
    require(
        isinstance(reviewers, list) and reviewers,
        "environment_policy_invalid",
        "governance Environment has no required reviewers",
    )
    required_users: set[str] = set()
    for reviewer in reviewers:
        require(isinstance(reviewer, Mapping), "environment_policy_invalid", "reviewer is malformed")
        identity = reviewer.get("reviewer")
        if reviewer.get("type") == "User" and isinstance(identity, Mapping):
            login = identity.get("login")
            if isinstance(login, str) and login:
                required_users.add(login)
    require(required_users, "environment_policy_invalid", "no auditable User reviewer is configured")
    rule_ids = sorted(positive_integer(rule.get("id"), "environment rule ID") for rule in rules)
    branch_policies = _paginate_wrapped(
        json_fetcher,
        environment_url + "/deployment-branch-policies",
        "branch_policies",
        label="deployment branch policies",
    )
    require(
        len(branch_policies) == 1
        and branch_policies[0].get("name") == DEFAULT_BRANCH
        and branch_policies[0].get("type") == "branch",
        "environment_policy_invalid",
        "governance Environment must allow exactly the main branch",
    )
    branch_policy_id = positive_integer(branch_policies[0].get("id"), "branch policy ID")
    initial_environment_policy = _environment_policy_snapshot(
        environment, branch_policies
    )
    approvals = json_fetcher(_api(repository, f"/actions/runs/{run_id}/approvals"))
    require(
        isinstance(approvals, list) and all(isinstance(item, Mapping) for item in approvals),
        "environment_approval_invalid",
        "workflow review history is malformed",
    )
    applicable_approvals: list[dict[str, Any]] = []
    for approval in approvals:
        environments = approval.get("environments")
        if not isinstance(environments, list):
            continue
        applies = any(
            isinstance(value, Mapping)
            and value.get("id") == environment_id
            and value.get("name") == ENVIRONMENT_NAME
            for value in environments
        )
        if not applies:
            continue
        state_value = approval.get("state")
        user = approval.get("user")
        login = user.get("login") if isinstance(user, Mapping) else None
        require(
            state_value != "rejected",
            "environment_approval_invalid",
            "workflow review history contains a governance rejection",
        )
        if state_value == "approved" and login in required_users:
            applicable_approvals.append({"state": state_value, "reviewer": login})
    require(
        applicable_approvals,
        "environment_approval_invalid",
        "no configured reviewer approved the governance Environment",
    )
    pending = json_fetcher(_api(repository, f"/actions/runs/{run_id}/pending_deployments"))
    require(
        pending == [],
        "environment_approval_invalid",
        "source run still has pending deployments",
    )

    deployments_base = _query(
        _api(repository, "/deployments"),
        (("sha", source_commit), ("ref", DEFAULT_BRANCH), ("environment", ENVIRONMENT_NAME)),
    )
    # Append pagination to an already-query-bearing URL without permitting caller input.
    deployments: list[Mapping[str, Any]] = []
    seen_deployments: set[int] = set()
    for page in range(1, MAX_PAGES + 1):
        values = json_fetcher(deployments_base + f"&per_page={PER_PAGE}&page={page}")
        require(
            isinstance(values, list) and all(isinstance(item, Mapping) for item in values),
            "pagination_invalid",
            "deployment page is malformed",
        )
        for deployment in values:
            deployment_id = positive_integer(deployment.get("id"), "deployment.id")
            require(deployment_id not in seen_deployments, "pagination_invalid", "deployment ID repeats")
            seen_deployments.add(deployment_id)
            deployments.append(deployment)
        if len(values) < PER_PAGE:
            break
    else:
        fail("pagination_invalid", "deployments exceed the page limit")
    bound_deployments: list[tuple[Mapping[str, Any], Mapping[str, Any], list[Mapping[str, Any]]]] = []
    for deployment in deployments:
        deployment_id = positive_integer(deployment.get("id"), "deployment.id")
        deployment_url = _api(repository, f"/deployments/{deployment_id}")
        statuses_url = deployment_url + "/statuses"
        if not (
            deployment.get("sha") == source_commit
            and deployment.get("ref") == DEFAULT_BRANCH
            and deployment.get("task") == "deploy"
            and deployment.get("environment") == ENVIRONMENT_NAME
            and deployment.get("url") == deployment_url
            and deployment.get("statuses_url") == statuses_url
            and deployment.get("repository_url") == _api(repository, "")
        ):
            continue
        statuses = _paginate_list(
            json_fetcher,
            statuses_url,
            label=f"deployment {deployment_id} statuses",
        )
        relevant = [status_value for status_value in statuses if status_value.get("log_url") == protected_job_url]
        successes = [status_value for status_value in relevant if status_value.get("state") == "success"]
        if len(successes) == 1:
            bound_deployments.append((deployment, successes[0], statuses))
    require(
        len(bound_deployments) == 1,
        "deployment_binding_invalid",
        "no unique governance deployment success binds the exact protected job",
    )
    deployment, success_status, deployment_statuses = bound_deployments[0]
    deployment_id = positive_integer(deployment.get("id"), "bound deployment.id")
    direct_deployment = _object(
        json_fetcher(_api(repository, f"/deployments/{deployment_id}")),
        "direct deployment",
    )
    require(
        all(
            direct_deployment.get(field) == deployment.get(field)
            for field in (
                "id",
                "sha",
                "ref",
                "task",
                "environment",
                "created_at",
                "url",
                "statuses_url",
                "repository_url",
            )
        ),
        "deployment_binding_invalid",
        "direct deployment differs from the filtered deployment listing",
    )
    deployment_created = parse_time(deployment.get("created_at"), "deployment.created_at")
    environment_updated = parse_time(environment.get("updated_at"), "environment.updated_at")
    require(
        environment_updated <= deployment_created <= job_completed,
        "deployment_binding_invalid",
        "Environment was changed after deployment or deployment timing is invalid",
    )
    _validate_status_history(
        deployment_statuses,
        success_status=success_status,
        protected_job_url=protected_job_url,
    )
    success_status_id = positive_integer(success_status.get("id"), "success status.id")
    success_time = parse_time(success_status.get("created_at"), "success status.created_at")
    require(
        success_status.get("deployment_url") == _api(repository, f"/deployments/{deployment_id}")
        and success_status.get("repository_url") == _api(repository, "")
        and success_status.get("environment") == ENVIRONMENT_NAME
        and job_started <= success_time <= job_completed + timedelta(minutes=5),
        "deployment_binding_invalid",
        "successful deployment status is not canonically bound or timely",
    )

    artifacts = _paginate_wrapped(
        json_fetcher,
        _api(repository, f"/actions/runs/{run_id}/artifacts"),
        "artifacts",
        label="source run artifacts",
    )
    expected_artifact_name = f"{SUMMARY_ARTIFACT_PREFIX}{run_id}-{run_attempt}"
    artifact_matches = [item for item in artifacts if item.get("name") == expected_artifact_name]
    require(
        len(artifact_matches) == 1,
        "summary_artifact_invalid",
        "source run has no unique attempt-bound accepted summary artifact",
    )
    artifact = artifact_matches[0]
    artifact_id = positive_integer(artifact.get("id"), "artifact.id")
    direct_artifact = _object(
        json_fetcher(_api(repository, f"/actions/artifacts/{artifact_id}")),
        "direct artifact",
    )
    require(
        all(
            direct_artifact.get(field) == artifact.get(field)
            for field in (
                "id",
                "name",
                "size_in_bytes",
                "archive_download_url",
                "digest",
                "expired",
                "created_at",
                "expires_at",
            )
        ),
        "summary_artifact_invalid",
        "direct artifact differs from the run artifact listing",
    )
    artifact_size = artifact.get("size_in_bytes")
    artifact_digest = artifact.get("digest")
    archive_url = _api(repository, f"/actions/artifacts/{artifact_id}/zip")
    workflow_run = artifact.get("workflow_run")
    require(
        isinstance(artifact_size, int)
        and not isinstance(artifact_size, bool)
        and 0 < artifact_size <= MAX_ARCHIVE_BYTES
        and artifact.get("expired") is False
        and artifact.get("archive_download_url") == archive_url
        and isinstance(workflow_run, Mapping)
        and workflow_run.get("id") == run_id
        and workflow_run.get("head_sha") == source_commit
        and workflow_run.get("head_branch") == DEFAULT_BRANCH,
        "summary_artifact_invalid",
        "accepted summary artifact is expired, oversized, or misbound",
    )
    api_archive_digest = bare_digest(artifact_digest, "artifact.digest")
    artifact_created = parse_time(artifact.get("created_at"), "artifact.created_at")
    parse_time(artifact.get("expires_at"), "artifact.expires_at")
    require(
        job_started <= artifact_created <= job_completed + timedelta(minutes=5),
        "summary_artifact_invalid",
        "accepted summary artifact was not created by the protected job window",
    )
    archive = binary_fetcher(archive_url)
    require(
        isinstance(archive, bytes)
        and len(archive) == artifact_size
        and hashlib.sha256(archive).hexdigest() == api_archive_digest,
        "summary_artifact_invalid",
        "accepted summary ZIP size or GitHub digest does not match",
    )
    summary, summary_digest = _parse_summary_archive(archive)
    summary_binding = _validate_source_summary(
        summary,
        repository=repository,
        run_id=run_id,
        run_attempt=run_attempt,
        source_commit=source_commit,
    )

    # Re-read mutable GitHub state immediately before promotion.  These reads
    # narrow the TOCTOU window and ensure the result does not rely on a policy,
    # status, artifact, or latest-attempt snapshot that changed during ZIP and
    # summary validation.
    final_environment = _object(
        json_fetcher(environment_url), "final governance environment"
    )
    final_branch_policies = _paginate_wrapped(
        json_fetcher,
        environment_url + "/deployment-branch-policies",
        "branch_policies",
        label="final deployment branch policies",
    )
    require(
        _environment_policy_snapshot(final_environment, final_branch_policies)
        == initial_environment_policy,
        "environment_policy_changed",
        "governance Environment policy changed during verification",
    )
    final_statuses = _paginate_list(
        json_fetcher,
        _api(repository, f"/deployments/{deployment_id}/statuses"),
        label=f"final deployment {deployment_id} statuses",
    )
    _validate_status_history(
        final_statuses,
        success_status=success_status,
        protected_job_url=protected_job_url,
    )
    final_artifact = _object(
        json_fetcher(_api(repository, f"/actions/artifacts/{artifact_id}")),
        "final direct artifact",
    )
    require(
        final_artifact.get("expired") is False
        and all(
            final_artifact.get(field) == direct_artifact.get(field)
            for field in (
                "id",
                "name",
                "size_in_bytes",
                "archive_download_url",
                "digest",
                "created_at",
                "expires_at",
            )
        ),
        "summary_artifact_changed",
        "accepted summary artifact changed or expired during verification",
    )
    final_latest_run = _object(
        json_fetcher(_api(repository, f"/actions/runs/{run_id}")),
        "final latest workflow run",
    )
    require(
        final_latest_run.get("id") == run_id
        and final_latest_run.get("run_attempt") == run_attempt
        and final_latest_run.get("head_sha") == source_commit
        and final_latest_run.get("head_branch") == DEFAULT_BRANCH
        and final_latest_run.get("status") == "completed"
        and final_latest_run.get("conclusion") == "success",
        "workflow_attempt_changed",
        "source run attempt changed during verification",
    )
    verified_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return {
        "schema_version": RESULT_SCHEMA,
        "repository": {
            "id": repository_id,
            "full_name": repository,
            "default_branch": DEFAULT_BRANCH,
        },
        "consumer": {
            "workflow_path": CONSUMER_WORKFLOW_PATH,
            "run_id": consumer_run_id,
            "run_attempt": consumer_run_attempt,
            "source_commit": consumer_commit,
        },
        "target_run": {
            "workflow_id": workflow_id,
            "workflow_path": SOURCE_WORKFLOW_PATH,
            "run_id": run_id,
            "run_attempt": run_attempt,
            "head_sha": source_commit,
            "head_branch": DEFAULT_BRANCH,
            "status": "completed",
            "conclusion": "success",
        },
        "protected_job": {
            "job_id": protected_job_id,
            "name": PROTECTED_JOB_NAME,
            "html_url": protected_job_url,
            "started_at": protected_job.get("started_at"),
            "completed_at": protected_job.get("completed_at"),
        },
        "environment": {
            "id": environment_id,
            "name": ENVIRONMENT_NAME,
            "configuration_observed_at": verified_at.isoformat().replace("+00:00", "Z"),
            "updated_at": environment.get("updated_at"),
            "protection_rule_ids": rule_ids,
            "branch_policy_ids": [branch_policy_id],
            "required_user_reviewers": sorted(required_users),
            "approval_records": applicable_approvals,
            "approval_scope": "workflow_run",
        },
        "deployment": {
            "deployment_id": deployment_id,
            "sha": source_commit,
            "ref": DEFAULT_BRANCH,
            "environment": ENVIRONMENT_NAME,
            "status_id": success_status_id,
            "state": "success",
            "log_url": protected_job_url,
            "created_at": deployment.get("created_at"),
            "status_created_at": success_status.get("created_at"),
        },
        "artifact": {
            "artifact_id": artifact_id,
            "name": expected_artifact_name,
            "size_in_bytes": artifact_size,
            "archive_sha256": api_archive_digest,
            "api_digest": artifact_digest,
            "summary_sha256": summary_digest,
            "expires_at": artifact.get("expires_at"),
        },
        "accepted_summary_binding": summary_binding,
        "decision": {
            "verification_level": "preview_attested",
            "provider_verified": False,
            "counts_as_phase78_closure": True,
            "accepted": True,
        },
        "verified_at": verified_at.isoformat().replace("+00:00", "Z"),
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--repository", required=True)
    value.add_argument("--run-id", type=int, required=True)
    value.add_argument("--run-attempt", type=int, required=True)
    value.add_argument("--source-commit", required=True)
    value.add_argument("--consumer-commit", required=True)
    value.add_argument("--consumer-run-id", type=int, required=True)
    value.add_argument("--consumer-run-attempt", type=int, required=True)
    value.add_argument("--output", type=Path, required=True)
    return value


def write_result(path: Path, result: Mapping[str, Any]) -> None:
    """Write one result exactly once; an existing path is always a hard failure."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(dict(result), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = verify(
            repository=args.repository,
            run_id=args.run_id,
            run_attempt=args.run_attempt,
            source_commit=args.source_commit,
            consumer_commit=args.consumer_commit,
            consumer_run_id=args.consumer_run_id,
            consumer_run_attempt=args.consumer_run_attempt,
        )
        write_result(args.output, result)
    except (AcceptedSummaryConsumerError, FileExistsError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        "OpenAI Preview accepted-summary consumer passed: "
        f"source_run={args.run_id} attempt={args.run_attempt}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
