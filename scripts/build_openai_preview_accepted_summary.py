#!/usr/bin/env python3
"""Build a fail-closed, run-bound summary for protected Preview acceptance."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA = "openai-preview-accepted-run-summary/v2"
WORKFLOW_PATH = ".github/workflows/openai-preview-accepted-evidence.yml"
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
EXPECTED_PHASE7_MATRIX = {
    (workflow, case_kind)
    for workflow in ("idea", "proposal", "article", "perspective", "research_polisher")
    for case_kind in ("happy", "control")
}
EXPECTED_RETRIEVAL_DISTRIBUTION = {
    "search": 3,
    "deep_research_completed": 2,
    "deep_research_inactive_control": 1,
}
PHASE7_COMPLETION_GATE_IDS = frozenset(
    {
        "accepted_platform_capture_adapter",
        "accepted_external_evidence_adapter",
        "five_current_version_live_happy_paths",
        "five_current_version_valid_control_paths",
        "release_source_commit",
        "repository_preview_ci",
        "canonical_plugin_validator_ci",
        "marketplace_resolved_commit",
        "marketplace_upgrade",
        "explicit_reinstall",
        "fresh_task_discovery",
        "immutable_previous_artifact_rollback",
        "main_branch_required_check_protection",
    }
)
EXPECTED_PHASE8_REVIEWER_CASES = {
    "case-a01": "proposal-readiness-triage",
    "case-a02": "article-evaluator",
    "case-a03": "perspective-evaluator",
}
EXPECTED_PHASE8_RETRIEVAL_RECEIPTS = {
    "ph8-search-current-001": "search",
    "ph8-search-exact-001": "search",
    "ph8-search-narrow-academic-001": "search",
    "ph8-deep-research-cycle-001": "deep_research_completed",
    "ph8-deep-research-cycle-002": "deep_research_completed",
    "ph8-deep-research-inactive-001": "deep_research_inactive_control",
}
EXTERNAL_RECORD_PATHS = {
    "repository_preview_ci": ("ci", "repository_preview"),
    "canonical_plugin_validator_ci": ("ci", "canonical_plugin_validator", "ci"),
    "main_branch_protection": ("governance", "main_branch_protection"),
    "marketplace_resolved_commit": ("marketplace_source", "resolved_commit"),
    "marketplace_upgrade": ("receipts", "marketplace_upgrade"),
    "explicit_reinstall": ("receipts", "explicit_reinstall"),
    "fresh_task_discovery": ("receipts", "fresh_task_discovery"),
    "rollback": ("receipts", "rollback"),
}
ACCEPTED_EXTERNAL_STATUSES = {"preview_attested", "provider_verified"}
CHAIN_ASSET_KINDS = {
    "raw_export_asset": {"raw_export", "structured_export", "task_export"},
    "envelope_asset": {"evidence_envelope"},
    "verifier_report_asset": {"verifier_report"},
}


class AcceptedSummaryError(ValueError):
    pass


def fail(message: str) -> None:
    raise AcceptedSummaryError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not readable JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def positive_integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        fail(f"{label} must be a positive integer")
    return value


def safe_name(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or Path(value).name != value
        or "/" in value
        or "\\" in value
    ):
        fail(f"{label} must be one safe filename")
    return value


def sha256_file(path: Path, label: str) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        fail(f"{label} cannot be read: {exc}")


def strict_phase78_snapshot(
    phase7: Mapping[str, Any], phase8: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate the exact Preview-complete state and return compact item results."""

    require(
        isinstance(phase7.get("plugin_version"), str)
        and phase7.get("plugin_version") == phase8.get("plugin_version"),
        "Phase 7 and Phase 8 do not bind one plugin version",
    )
    phase7_summary = phase7.get("summary")
    runtime = phase7.get("runtime_receipts")
    gates = phase7.get("completion_gates")
    require(isinstance(phase7_summary, Mapping), "Phase 7 summary is missing")
    require(isinstance(runtime, Mapping), "Phase 7 runtime receipts are missing")
    require(isinstance(gates, Mapping), "Phase 7 completion gates are missing")
    runtime_results = runtime.get("results")
    require(
        phase7.get("phase_status") == "complete_preview_attested"
        and phase7.get("verification_level") == "preview_attested"
        and phase7.get("counts_as_preview_acceptance") is True
        and phase7.get("provider_verified") is False,
        "Phase 7 is not complete_preview_attested without provider promotion",
    )
    require(
        isinstance(runtime_results, list) and len(runtime_results) == 10,
        "Phase 7 must contain exactly ten runtime results",
    )
    phase7_pairs: set[tuple[Any, Any]] = set()
    receipt_ids: set[str] = set()
    happy = control = 0
    phase7_items: list[dict[str, Any]] = []
    for index, item in enumerate(runtime_results):
        require(isinstance(item, Mapping), f"Phase 7 runtime result {index} is invalid")
        receipt_id = item.get("receipt_id")
        require(
            isinstance(receipt_id, str) and receipt_id and receipt_id not in receipt_ids,
            f"Phase 7 runtime result {index} has a missing or repeated receipt ID",
        )
        receipt_ids.add(receipt_id)
        pair = (item.get("workflow"), item.get("case_kind"))
        phase7_pairs.add(pair)
        require(
            item.get("status") == "verified"
            and item.get("verification_level") == "preview_attested",
            f"Phase 7 runtime result {receipt_id} is not Preview-attested",
        )
        happy += item.get("case_kind") == "happy"
        control += item.get("case_kind") == "control"
        phase7_items.append(dict(item))
    require(
        phase7_pairs == EXPECTED_PHASE7_MATRIX and happy == 5 and control == 5,
        "Phase 7 runtime results do not form the required 5 happy + 5 control matrix",
    )
    require(
        runtime.get("verified_receipt_count") == 10
        and runtime.get("pending_receipt_count") == 0
        and phase7_summary.get("runtime_receipts_verified") == 10
        and phase7_summary.get("runtime_receipts_pending") == 0
        and phase7_summary.get("false_ready_count") == 0,
        "Phase 7 runtime counters are not complete or report false-ready output",
    )
    require(
        set(gates) == PHASE7_COMPLETION_GATE_IDS
        and all(isinstance(value, Mapping) and value.get("status") == "verified" for value in gates.values())
        and phase7.get("pending_gates") == []
        and phase7_summary.get("completion_gates_verified") == 13
        and phase7_summary.get("completion_gates_pending") == 0,
        "Phase 7 does not have all thirteen completion gates verified",
    )

    corpus = phase8.get("corpus")
    live = phase8.get("live_fresh_repeat")
    retrieval = phase8.get("retrieval")
    claims = phase8.get("claims")
    acceptance = phase8.get("acceptance_status")
    provider = phase8.get("provider_trust")
    require(all(isinstance(value, Mapping) for value in (corpus, live, retrieval, claims, acceptance, provider)), "Phase 8 report sections are missing")
    require(
        phase8.get("phase_status") == "complete_preview_attested"
        and acceptance.get("preview_attested") == "complete"
        and acceptance.get("provider_verified") == "pending_strict_provider_evidence"
        and claims.get("preview_gate_complete") is True
        and claims.get("provider_gate_complete") is False
        and claims.get("accepted_verification_level") == "preview_attested",
        "Phase 8 is not complete_preview_attested without provider promotion",
    )
    require(
        corpus.get("metrics", {}).get("false_ready_count") == 0,
        "Phase 8 corpus reports a false-ready result",
    )
    case_results = live.get("case_results")
    review_digests = live.get("review_content_digests")
    require(
        isinstance(case_results, list)
        and len(case_results) == 3
        and isinstance(review_digests, Mapping),
        "Phase 8 reviewer results are incomplete",
    )
    reviewer_items: list[dict[str, Any]] = []
    run_ids: set[str] = set()
    instance_ids: set[str] = set()
    observed_case_skills: dict[str, str] = {}
    for case in case_results:
        require(isinstance(case, Mapping), "Phase 8 reviewer case is invalid")
        case_id = case.get("case_id")
        reviewer_skill = case.get("reviewer_skill")
        case_run_ids = case.get("run_ids")
        case_instance_ids = case.get("reviewer_instance_ids")
        require(
            isinstance(case_id, str)
            and isinstance(reviewer_skill, str)
            and case.get("fresh_runs") == 2
            and isinstance(case_run_ids, list)
            and len(case_run_ids) == 2
            and isinstance(case_instance_ids, list)
            and len(case_instance_ids) == 2,
            f"Phase 8 reviewer case {case.get('case_id')} does not contain two fresh runs",
        )
        observed_case_skills[case_id] = reviewer_skill
        for run_id, instance_id in zip(case_run_ids, case_instance_ids):
            require(
                isinstance(run_id, str)
                and run_id
                and run_id not in run_ids
                and isinstance(instance_id, str)
                and instance_id
                and instance_id not in instance_ids,
                "Phase 8 reviewer run or instance IDs are missing or reused",
            )
            digest = review_digests.get(run_id)
            require(
                isinstance(digest, str)
                and digest.startswith("sha256:")
                and SHA256_RE.fullmatch(digest[7:]) is not None,
                f"Phase 8 reviewer run {run_id} has no bound review digest",
            )
            run_ids.add(run_id)
            instance_ids.add(instance_id)
            reviewer_items.append(
                {
                    "case_id": case.get("case_id"),
                    "run_id": run_id,
                    "reviewer_instance_id": instance_id,
                    "reviewer_skill": case.get("reviewer_skill"),
                    "input_digest": case.get("input_digest"),
                    "review_digest": digest,
                    "review_stage_state": case.get("review_stage_state"),
                    "verification_level": "preview_attested",
                    "provider_verified": False,
                }
            )
    require(
        observed_case_skills == EXPECTED_PHASE8_REVIEWER_CASES
        and len(reviewer_items) == 6
        and live.get("preview_attested_review_count") == 6
        and live.get("provider_verified_live_review_count") == 0
        and live.get("verified_live_review_count") == 0
        and live.get("unique_reviewer_instance_count") == 6
        and live.get("historical_release_mismatch") is False
        and live.get("historical_release_mismatch_snapshot_count") == 0
        and live.get("preview_gate_status") == "completed"
        and live.get("status") == "preview_attested",
        "Phase 8 does not contain six current Preview-attested reviewer runs",
    )
    receipt_results = retrieval.get("receipt_results")
    require(
        isinstance(receipt_results, list) and len(receipt_results) == 6,
        "Phase 8 must contain exactly six retrieval results",
    )
    retrieval_items: list[dict[str, Any]] = []
    retrieval_ids: set[str] = set()
    observed_distribution = {kind: 0 for kind in EXPECTED_RETRIEVAL_DISTRIBUTION}
    for item in receipt_results:
        require(isinstance(item, Mapping), "Phase 8 retrieval result is invalid")
        receipt_id = item.get("receipt_id")
        kind = item.get("kind")
        require(
            isinstance(receipt_id, str)
            and receipt_id
            and receipt_id not in retrieval_ids
            and kind in observed_distribution,
            "Phase 8 retrieval result has a missing/reused ID or invalid kind",
        )
        require(
            item.get("evidence_status") == "preview_attested"
            and item.get("evidence_trust_level") == "preview_attested",
            f"Phase 8 retrieval result {receipt_id} is not Preview-attested",
        )
        retrieval_ids.add(receipt_id)
        observed_distribution[str(kind)] += 1
        retrieval_items.append(dict(item))
    require(
        {
            str(item.get("receipt_id")): str(item.get("kind"))
            for item in retrieval_items
        }
        == EXPECTED_PHASE8_RETRIEVAL_RECEIPTS
        and observed_distribution == EXPECTED_RETRIEVAL_DISTRIBUTION
        and retrieval.get("preview_attested_current_receipts") == 6
        and retrieval.get("preview_attested_current_receipts_by_kind")
        == EXPECTED_RETRIEVAL_DISTRIBUTION
        and retrieval.get("completed_current_receipts") == 0
        and retrieval.get("pending_receipts") == 0
        and retrieval.get("stale_receipts") == 0
        and retrieval.get("historical_release_mismatch_receipts") == 0
        and retrieval.get("observed_unverified_receipts") == 0
        and retrieval.get("preview_gate_status") == "completed"
        and claims.get("preview_attested_retrieval_receipts") == 6
        and claims.get("provider_verified_phase8_complete") is False,
        "Phase 8 retrieval distribution is incomplete, stale, or provider-promoted",
    )
    return {
        "phase7": {
            "phase_status": phase7.get("phase_status"),
            "verification_level": "preview_attested",
            "provider_verified": False,
            "verified_runtime_count": 10,
            "happy_count": 5,
            "control_count": 5,
            "verified_completion_gate_count": 13,
            "pending_gate_count": 0,
            "items": phase7_items,
        },
        "phase8": {
            "phase_status": phase8.get("phase_status"),
            "verification_level": "preview_attested",
            "provider_verified": False,
            "reviewer_items": reviewer_items,
            "retrieval_items": retrieval_items,
            "retrieval_distribution": dict(EXPECTED_RETRIEVAL_DISTRIBUTION),
            "stale_count": 0,
            "false_ready_count": 0,
        },
    }


def _release(value: Mapping[str, Any], expected_tag: str, label: str) -> dict[str, Any]:
    require(
        value.get("tag_name") == expected_tag
        and value.get("draft") is False
        and value.get("prerelease") is True
        and value.get("immutable") is True,
        f"{label} is not the requested published immutable prerelease",
    )
    return {
        "release_id": positive_integer(value.get("id"), f"{label}.id"),
        "tag": expected_tag,
        "immutable": True,
    }


def _flatten_asset_pages(path: Path, label: str) -> list[Mapping[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not readable JSON: {exc}")
    if (
        not isinstance(value, list)
        or len(value) < 2
        or not all(isinstance(page, list) for page in value)
        or value[-1] != []
        or any(not page for page in value[:-1])
        or any(len(page) != 100 for page in value[:-2])
        or not 1 <= len(value[-2]) <= 100
    ):
        fail(
            f"{label} must contain full 100-item pages, one final data page, "
            "and an explicitly queried terminal empty page"
        )
    values = [item for page in value[:-1] for item in page]
    require(all(isinstance(item, Mapping) for item in values), f"{label} contains a malformed asset")
    return values


def _asset_inventory(path: Path, asset_dir: Path, label: str) -> list[dict[str, Any]]:
    values = _flatten_asset_pages(path, label)
    require(values, f"{label} is empty")
    seen_ids: set[int] = set()
    seen_names: set[str] = set()
    inventory: list[dict[str, Any]] = []
    for offset, value in enumerate(values):
        asset_id = positive_integer(value.get("id"), f"{label}[{offset}].id")
        name = safe_name(value.get("name"), f"{label}[{offset}].name")
        size = value.get("size")
        require(
            asset_id not in seen_ids
            and name not in seen_names
            and isinstance(size, int)
            and not isinstance(size, bool)
            and size >= 0
            and value.get("state") == "uploaded",
            f"{label}[{offset}] is duplicated, malformed, or not uploaded",
        )
        local = asset_dir / name
        require(local.is_file() and not local.is_symlink(), f"{label} local asset is missing: {name}")
        local_size = local.stat().st_size
        digest = sha256_file(local, f"{label} local asset {name}")
        require(local_size == size, f"{label} asset size differs from GitHub: {name}")
        api_digest = value.get("digest")
        if api_digest is not None:
            require(api_digest == f"sha256:{digest}", f"{label} asset digest differs from GitHub: {name}")
        seen_ids.add(asset_id)
        seen_names.add(name)
        inventory.append(
            {
                "asset_id": asset_id,
                "name": name,
                "size": size,
                "sha256": digest,
            }
        )
    local_names = {item.name for item in asset_dir.iterdir() if item.is_file()}
    require(local_names == seen_names, f"{label} API/local asset inventories differ")
    return sorted(inventory, key=lambda item: (item["name"], item["asset_id"]))


def _nested(root: Mapping[str, Any], path: tuple[str, ...], label: str) -> Mapping[str, Any]:
    value: Any = root
    for part in path:
        if not isinstance(value, Mapping):
            fail(f"{label} is missing")
        value = value.get(part)
    if not isinstance(value, Mapping):
        fail(f"{label} is missing")
    return value


def _document_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _locator_digest(locator: Mapping[str, Any]) -> str:
    payload = json.dumps(
        dict(locator), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _locator_chain(
    locator: Mapping[str, Any], *, label: str, repository: str
) -> tuple[set[int], set[str]]:
    require(
        locator.get("repository") == repository
        and positive_integer(locator.get("release_id"), f"{label}.release_id") > 0
        and isinstance(locator.get("release_tag"), str)
        and bool(str(locator.get("release_tag")).strip()),
        f"{label} does not bind a valid Release",
    )
    asset_ids: set[int] = set()
    digests: set[str] = set()
    for field in (
        "envelope_asset",
        "release_asset_index_asset",
        "raw_export_asset",
        "verifier_report_asset",
    ):
        asset = locator.get(field)
        require(isinstance(asset, Mapping), f"{label}.{field} is missing")
        asset_id = positive_integer(asset.get("asset_id"), f"{label}.{field}.asset_id")
        safe_name(asset.get("name"), f"{label}.{field}.name")
        digest = str(asset.get("sha256", "")).removeprefix("sha256:")
        require(
            SHA256_RE.fullmatch(digest) is not None
            and asset_id not in asset_ids
            and digest not in digests,
            f"{label} reuses an asset ID or R/E/V/I digest",
        )
        asset_ids.add(asset_id)
        digests.add(digest)
    return asset_ids, digests


def _historical_expectations(
    ledger: Mapping[str, Any], *, repository: str
) -> dict[tuple[str, str, str], dict[str, Any]]:
    previous_releases = ledger.get("previous_releases", [])
    require(isinstance(previous_releases, list), "candidate ledger previous_releases is invalid")
    expectations: dict[tuple[str, str, str], dict[str, Any]] = {}
    for index, previous in enumerate(previous_releases):
        scope = f"previous_releases[{index}]"
        require(isinstance(previous, Mapping), f"{scope} is not an object")
        source = previous.get("source_commit")
        source_commit = source.get("sha") if isinstance(source, Mapping) else None
        accepted_records: list[tuple[str, Mapping[str, Any]]] = []
        for evidence_type, path in EXTERNAL_RECORD_PATHS.items():
            record = _nested(previous, path, f"{scope}.{evidence_type}")
            if record.get("status") in ACCEPTED_EXTERNAL_STATUSES:
                accepted_records.append((evidence_type, record))
        if accepted_records:
            require(
                isinstance(source_commit, str)
                and COMMIT_RE.fullmatch(source_commit) is not None,
                f"{scope} accepted records have no full source commit",
            )
        for evidence_type, record in accepted_records:
            locator = record.get("evidence_locator")
            require(
                isinstance(locator, Mapping),
                f"{scope}.{evidence_type} accepted record has no locator",
            )
            asset_ids, chain_digests = _locator_chain(
                locator,
                label=f"{scope}.{evidence_type}",
                repository=repository,
            )
            locator_sha256 = _locator_digest(locator)
            key = (scope, evidence_type, locator_sha256)
            require(key not in expectations, "candidate ledger repeats a historical locator")
            expectations[key] = {
                "release_scope": scope,
                "evidence_type": evidence_type,
                "source_commit": source_commit,
                "locator_sha256": locator_sha256,
                "asset_ids": asset_ids,
                "chain_digests": chain_digests,
                "evidence_locator": dict(locator),
            }
    return expectations


def _bind_historical_results(
    *,
    results: Any,
    declared_count: Any,
    expectations: Mapping[tuple[str, str, str], Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], set[str], set[str]]:
    require(
        isinstance(results, list)
        and all(isinstance(item, Mapping) for item in results)
        and declared_count == len(results),
        "standalone release-evidence runner has an invalid historical result inventory",
    )
    by_key: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    evidence_ids: set[str] = set()
    chain_digests: set[str] = set()
    for offset, item in enumerate(results):
        scope = item.get("release_scope")
        evidence_type = item.get("evidence_type")
        locator_sha256 = item.get("locator_sha256")
        key = (str(scope), str(evidence_type), str(locator_sha256))
        require(
            isinstance(scope, str)
            and scope.startswith("previous_releases[")
            and isinstance(evidence_type, str)
            and evidence_type in EXTERNAL_RECORD_PATHS
            and isinstance(locator_sha256, str)
            and re.fullmatch(r"sha256:[0-9a-f]{64}", locator_sha256) is not None
            and key not in by_key,
            f"historical live result {offset} is duplicated or has an invalid composite key",
        )
        by_key[key] = item
    require(
        set(by_key) == set(expectations),
        "historical live results do not exactly cover candidate-ledger accepted records",
    )
    normalized: list[dict[str, Any]] = []
    for key in sorted(expectations):
        expected = expectations[key]
        item = by_key[key]
        evidence_id = item.get("evidence_id")
        result_digest = item.get("validated_result_sha256")
        verified_asset_ids = item.get("verified_asset_ids")
        expected_asset_ids = set(expected["asset_ids"])
        expected_chain_digests = set(expected["chain_digests"])
        require(
            isinstance(evidence_id, str)
            and bool(evidence_id.strip())
            and evidence_id not in evidence_ids
            and item.get("release_scope") == expected["release_scope"]
            and item.get("evidence_type") == expected["evidence_type"]
            and item.get("source_commit") == expected["source_commit"]
            and item.get("verification_level") == "preview_attested"
            and item.get("provider_verified") is False
            and isinstance(result_digest, str)
            and re.fullmatch(r"sha256:[0-9a-f]{64}", result_digest) is not None
            and isinstance(verified_asset_ids, list)
            and len(verified_asset_ids) == 4
            and len(set(verified_asset_ids)) == 4
            and all(
                isinstance(value, int) and not isinstance(value, bool) and value > 0
                for value in verified_asset_ids
            )
            and set(verified_asset_ids) == expected_asset_ids
            and positive_integer(
                item.get("verifier_workflow_run_id"),
                f"{expected['release_scope']}.{expected['evidence_type']}.verifier_workflow_run_id",
            )
            > 0
            and isinstance(item.get("verified_at"), str)
            and bool(str(item.get("verified_at")).strip())
            and expected_chain_digests.isdisjoint(chain_digests),
            f"historical live result is incomplete, reused, or misbound: {key}",
        )
        evidence_ids.add(evidence_id)
        chain_digests.update(expected_chain_digests)
        normalized.append(
            {
                "release_scope": expected["release_scope"],
                "evidence_type": expected["evidence_type"],
                "evidence_id": evidence_id,
                "status": "preview_attested",
                "provider_verified": False,
                "source_commit": expected["source_commit"],
                "locator_sha256": expected["locator_sha256"],
                "validated_result_sha256": result_digest,
                "verified_asset_ids": list(verified_asset_ids),
                "verifier_workflow_run_id": item.get("verifier_workflow_run_id"),
                "verified_at": item.get("verified_at"),
                "evidence_locator": dict(expected["evidence_locator"]),
            }
        )
    return normalized, evidence_ids, chain_digests


def _bind_bridge_live_slots(
    *,
    slots: Any,
    id_field: str,
    expected_ids: set[str],
    expected_kinds: Mapping[str, str] | None,
    evidence_release: Mapping[str, Any],
    evidence_release_tag: str,
    repository: str,
    evidence_by_id: Mapping[int, Mapping[str, Any]],
    evidence_by_name: Mapping[str, Mapping[str, Any]],
    used_asset_ids: set[int],
    used_evidence_ids: set[str],
    used_chain_digests: set[str],
    label: str,
) -> list[dict[str, Any]]:
    require(
        isinstance(slots, list)
        and len(slots) == len(expected_ids)
        and all(isinstance(item, Mapping) for item in slots),
        f"{label} live slot inventory is incomplete",
    )
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for offset, slot in enumerate(slots):
        slot_id = slot.get(id_field)
        release = slot.get("release")
        require(
            isinstance(slot_id, str)
            and slot_id in expected_ids
            and slot_id not in seen_ids
            and isinstance(release, Mapping)
            and release.get("repository") == repository
            and release.get("release_id") == evidence_release["release_id"]
            and release.get("release_tag") == evidence_release_tag,
            f"{label} live slot {offset} is duplicated or bound to another Release",
        )
        if expected_kinds is not None:
            require(
                slot.get("slot_kind") == expected_kinds.get(slot_id),
                f"{label} live slot kind differs from its report subject: {slot_id}",
            )
        evidence_id = slot.get("evidence_id")
        live_digest = slot.get("live_result_digest")
        require(
            isinstance(evidence_id, str)
            and evidence_id
            and evidence_id not in used_evidence_ids
            and isinstance(live_digest, str)
            and re.fullmatch(r"sha256:[0-9a-f]{64}", live_digest) is not None
            and positive_integer(
                slot.get("verifier_workflow_run_id"),
                f"{label}.{slot_id}.verifier_workflow_run_id",
            )
            > 0
            and isinstance(slot.get("verified_at"), str)
            and bool(str(slot.get("verified_at")).strip()),
            f"{label} live slot lacks unique evidence or live-verifier metadata: {slot_id}",
        )
        index = slot.get("asset_index")
        require(isinstance(index, Mapping), f"{label} live slot has no asset index: {slot_id}")
        index_name = safe_name(index.get("name"), f"{label}.{slot_id}.asset_index.name")
        index_api = evidence_by_name.get(index_name)
        index_digest = str(index.get("sha256", "")).removeprefix("sha256:")
        require(
            index_api is not None
            and isinstance(index.get("size"), int)
            and not isinstance(index.get("size"), bool)
            and index_api["size"] == index.get("size")
            and SHA256_RE.fullmatch(index_digest) is not None
            and index_api["sha256"] == index_digest
            and index_api["asset_id"] not in used_asset_ids,
            f"{label} live slot index is absent, reused, or misbound: {slot_id}",
        )
        slot_asset_ids = {int(index_api["asset_id"])}
        slot_chain_digests = {index_digest}
        chain_roles: dict[str, str] = {}
        assets = slot.get("assets")
        require(
            isinstance(assets, list)
            and bool(assets)
            and all(isinstance(item, Mapping) for item in assets),
            f"{label} live slot has no indexed assets: {slot_id}",
        )
        for asset_offset, asset in enumerate(assets):
            asset_id = positive_integer(
                asset.get("asset_id"),
                f"{label}.{slot_id}.assets[{asset_offset}].asset_id",
            )
            name = safe_name(
                asset.get("name"), f"{label}.{slot_id}.assets[{asset_offset}].name"
            )
            digest_value = str(asset.get("sha256", "")).removeprefix("sha256:")
            api = evidence_by_id.get(asset_id)
            require(
                api is not None
                and api["name"] == name
                and api["size"] == asset.get("size")
                and SHA256_RE.fullmatch(digest_value) is not None
                and api["sha256"] == digest_value
                and asset_id not in used_asset_ids
                and asset_id not in slot_asset_ids
                and name != index_name,
                f"{label} live slot asset is absent, reused, or misbound: {slot_id}[{asset_offset}]",
            )
            slot_asset_ids.add(asset_id)
            evidence_kind = asset.get("evidence_kind")
            for role, allowed_kinds in CHAIN_ASSET_KINDS.items():
                if evidence_kind in allowed_kinds:
                    require(
                        role not in chain_roles,
                        f"{label} live slot repeats its {role}: {slot_id}",
                    )
                    chain_roles[role] = digest_value
        require(
            set(chain_roles) == set(CHAIN_ASSET_KINDS)
            and len(set(chain_roles.values())) == len(CHAIN_ASSET_KINDS),
            f"{label} live slot does not expose one unique R/E/V chain: {slot_id}",
        )
        slot_chain_digests.update(chain_roles.values())
        require(
            len(slot_chain_digests) == 4
            and slot_chain_digests.isdisjoint(used_chain_digests),
            f"{label} live slot reuses an R/E/V/I digest: {slot_id}",
        )
        used_asset_ids.update(slot_asset_ids)
        used_chain_digests.update(slot_chain_digests)
        used_evidence_ids.add(evidence_id)
        seen_ids.add(slot_id)
        normalized.append(dict(slot))
    require(seen_ids == expected_ids, f"{label} live slots do not match report subjects")
    return sorted(normalized, key=lambda item: str(item[id_field]))


def build_summary(
    *,
    evidence_release_json: Path,
    candidate_release_json: Path,
    evidence_assets_json: Path,
    candidate_assets_json: Path,
    evidence_asset_dir: Path,
    candidate_asset_dir: Path,
    candidate_ledger_path: Path,
    candidate_asset_names: Sequence[str],
    phase7_report_path: Path,
    phase8_report_path: Path,
    phase78_bridge_result_path: Path,
    release_runner_result_path: Path,
    repository: str,
    source_commit: str,
    evidence_release_tag: str,
    candidate_release_tag: str,
    evidence_final_commit: str,
    candidate_final_commit: str,
    run_id: int,
    run_attempt: int,
) -> dict[str, Any]:
    require(REPOSITORY_RE.fullmatch(repository) is not None, "repository must be owner/name")
    require(COMMIT_RE.fullmatch(source_commit) is not None, "source_commit must be a full lowercase SHA")
    require(evidence_release_tag != candidate_release_tag, "evidence and candidate release tags must differ")
    require(
        evidence_final_commit == source_commit and candidate_final_commit == source_commit,
        "both release tags must finally resolve to the trusted source commit",
    )
    positive_integer(run_id, "run_id")
    positive_integer(run_attempt, "run_attempt")
    evidence_release = _release(load_object(evidence_release_json, "evidence release"), evidence_release_tag, "evidence release")
    candidate_release = _release(load_object(candidate_release_json, "candidate release"), candidate_release_tag, "candidate release")
    evidence_release["final_commit"] = evidence_final_commit
    candidate_release["final_commit"] = candidate_final_commit
    evidence_inventory = _asset_inventory(evidence_assets_json, evidence_asset_dir, "evidence assets")
    candidate_inventory = _asset_inventory(candidate_assets_json, candidate_asset_dir, "candidate assets")
    candidate_by_name = {item["name"]: item for item in candidate_inventory}
    evidence_by_id = {item["asset_id"]: item for item in evidence_inventory}
    required_candidate_names = [safe_name(value, "candidate asset name") for value in candidate_asset_names]
    require(
        len(required_candidate_names) == 4
        and len(set(required_candidate_names)) == 4
        and set(candidate_by_name) == set(required_candidate_names),
        "candidate release must contain exactly the ledger and three receipt collections",
    )

    try:
        candidate_root = candidate_asset_dir.resolve(strict=True)
        expected_ledger_path = (
            candidate_root / required_candidate_names[0]
        ).resolve(strict=True)
        actual_ledger_path = candidate_ledger_path.resolve(strict=True)
    except OSError as exc:
        fail(f"candidate ledger path cannot be resolved: {exc}")
    require(
        actual_ledger_path == expected_ledger_path,
        "candidate ledger path is not the declared candidate Release asset",
    )
    candidate_ledger_digest = sha256_file(actual_ledger_path, "candidate ledger")
    require(
        candidate_by_name[required_candidate_names[0]]["sha256"]
        == candidate_ledger_digest,
        "candidate ledger digest differs from the candidate Release inventory",
    )

    ledger = load_object(actual_ledger_path, "candidate ledger")
    release = ledger.get("release")
    require(isinstance(release, Mapping), "candidate ledger release is missing")
    release_source = release.get("source_commit")
    require(
        isinstance(release_source, Mapping)
        and release_source.get("sha") == source_commit,
        "candidate ledger does not bind the trusted source commit",
    )
    runner = load_object(release_runner_result_path, "release-evidence runner result")
    expected_types = set(EXTERNAL_RECORD_PATHS)
    require(
        runner.get("schema_version") == "openai-release-evidence-runner-result/v1"
        and runner.get("validated") is True
        and runner.get("live_gate_eligible") is True
        and runner.get("verified_record_count") == 8
        and runner.get("ledger_sha256") == "sha256:" + candidate_ledger_digest
        and set(runner.get("evidence_types", [])) == expected_types,
        "standalone release-evidence runner did not bind this ledger and live-verify all eight records",
    )
    live_results = runner.get("live_results")
    history_results = runner.get("history_results")
    require(
        isinstance(live_results, list)
        and len(live_results) == 8
        and all(isinstance(item, Mapping) for item in live_results),
        "standalone release-evidence runner has no eight-item live result inventory",
    )
    historical_expectations = _historical_expectations(
        ledger, repository=repository
    )
    history_items, historical_evidence_ids, historical_chain_digests = (
        _bind_historical_results(
            results=history_results,
            declared_count=runner.get("historical_verified_record_count"),
            expectations=historical_expectations,
        )
    )
    live_by_type = {
        str(item.get("evidence_type")): item for item in live_results
    }
    require(
        set(live_by_type) == expected_types and len(live_by_type) == len(live_results),
        "standalone release-evidence live results repeat or omit an evidence type",
    )
    release_results: list[dict[str, Any]] = []
    bound_current_asset_ids: set[int] = set()
    current_evidence_ids: set[str] = set()
    current_chain_digests: set[str] = set()
    for evidence_type, path in sorted(EXTERNAL_RECORD_PATHS.items()):
        record = _nested(release, path, evidence_type)
        locator = record.get("evidence_locator")
        require(
            record.get("status") == "preview_attested" and isinstance(locator, Mapping),
            f"candidate ledger external record is not Preview-attested: {evidence_type}",
        )
        require(
            locator.get("repository") == repository
            and locator.get("release_id") == evidence_release["release_id"]
            and locator.get("release_tag") == evidence_release_tag,
            f"current external record does not bind this evidence Release: {evidence_type}",
        )
        expected_locator_asset_ids, locator_chain_digests = _locator_chain(
            locator,
            label=f"current.{evidence_type}",
            repository=repository,
        )
        require(
            locator_chain_digests.isdisjoint(current_chain_digests)
            and locator_chain_digests.isdisjoint(historical_chain_digests),
            f"current external record reuses an R/E/V/I digest: {evidence_type}",
        )
        locator_asset_ids: set[int] = set()
        for asset_field in (
            "envelope_asset",
            "release_asset_index_asset",
            "raw_export_asset",
            "verifier_report_asset",
        ):
            asset = locator.get(asset_field)
            require(
                isinstance(asset, Mapping),
                f"current external record has no {asset_field}: {evidence_type}",
            )
            asset_id = positive_integer(
                asset.get("asset_id"), f"{evidence_type}.{asset_field}.asset_id"
            )
            name = safe_name(
                asset.get("name"), f"{evidence_type}.{asset_field}.name"
            )
            digest_value = asset.get("sha256")
            require(
                isinstance(digest_value, str),
                f"{evidence_type}.{asset_field}.sha256 is missing",
            )
            bare = digest_value.removeprefix("sha256:")
            inventory_asset = evidence_by_id.get(asset_id)
            require(
                SHA256_RE.fullmatch(bare) is not None
                and inventory_asset is not None
                and inventory_asset["name"] == name
                and inventory_asset["sha256"] == bare
                and asset_id not in locator_asset_ids
                and asset_id not in bound_current_asset_ids,
                f"current external locator asset is absent, reused, or misbound: {evidence_type}.{asset_field}",
            )
            locator_asset_ids.add(asset_id)
        require(
            locator_asset_ids == expected_locator_asset_ids,
            f"current external locator asset set changed during binding: {evidence_type}",
        )
        bound_current_asset_ids.update(locator_asset_ids)
        live_result = live_by_type[evidence_type]
        locator_digest = _locator_digest(locator)
        verified_asset_ids = live_result.get("verified_asset_ids")
        result_digest = live_result.get("validated_result_sha256")
        evidence_id = live_result.get("evidence_id")
        require(
            isinstance(evidence_id, str)
            and bool(evidence_id.strip())
            and evidence_id not in current_evidence_ids
            and evidence_id not in historical_evidence_ids
            and live_result.get("release_scope") == "current"
            and live_result.get("verification_level") == "preview_attested"
            and live_result.get("provider_verified") is False
            and live_result.get("source_commit") == source_commit
            and live_result.get("locator_sha256") == locator_digest
            and isinstance(result_digest, str)
            and result_digest.startswith("sha256:")
            and SHA256_RE.fullmatch(result_digest[7:]) is not None
            and isinstance(verified_asset_ids, list)
            and len(verified_asset_ids) == 4
            and len(set(verified_asset_ids)) == 4
            and all(
                isinstance(value, int) and not isinstance(value, bool) and value > 0
                for value in verified_asset_ids
            )
            and set(verified_asset_ids) == locator_asset_ids
            and positive_integer(
                live_result.get("verifier_workflow_run_id"),
                f"{evidence_type}.verifier_workflow_run_id",
            )
            > 0,
            f"standalone live result is incomplete or misbound: {evidence_type}",
        )
        current_evidence_ids.add(evidence_id)
        current_chain_digests.update(locator_chain_digests)
        release_results.append(
            {
                "evidence_type": evidence_type,
                "evidence_id": evidence_id,
                "status": "preview_attested",
                "provider_verified": False,
                "live_requery_succeeded": True,
                "locator_sha256": locator_digest,
                "validated_result_sha256": result_digest,
                "verified_asset_ids": list(verified_asset_ids),
                "verifier_workflow_run_id": live_result.get(
                    "verifier_workflow_run_id"
                ),
                "verified_at": live_result.get("verified_at"),
                "evidence_locator": dict(locator),
            }
        )
    phase7_document = load_object(phase7_report_path, "Phase 7 report")
    phase8_document = load_object(phase8_report_path, "Phase 8 report")
    require(
        isinstance(release.get("version"), str)
        and phase7_document.get("plugin_version") == release.get("version")
        and phase8_document.get("plugin_version") == release.get("version"),
        "Phase 7/8 reports do not bind the candidate ledger plugin version",
    )
    phase78 = strict_phase78_snapshot(phase7_document, phase8_document)
    bridge = load_object(phase78_bridge_result_path, "Phase 7-8 live bridge result")
    bridge_phase7 = bridge.get("phase7")
    bridge_phase8 = bridge.get("phase8")
    collection_digests = bridge.get("candidate_collection_digests")
    require(
        bridge.get("schema_version") == "openai-preview-accepted-phase78-run/v1"
        and bridge.get("accepted") is True
        and bridge.get("verification_level") == "preview_attested"
        and bridge.get("provider_verified") is False
        and bridge.get("complete_preview_release_validator")
        == "passed_with_fresh_callback"
        and isinstance(bridge_phase7, Mapping)
        and isinstance(bridge_phase8, Mapping)
        and isinstance(collection_digests, Mapping),
        "same-process Phase 7-8 bridge result is missing or not accepted",
    )
    require(
        bridge_phase7.get("report_sha256") == _document_digest(phase7_document)
        and bridge_phase8.get("report_sha256") == _document_digest(phase8_document)
        and bridge_phase7.get("runtime_results") == phase78["phase7"]["items"]
        and bridge_phase8.get("reviewer_results")
        == phase78["phase8"]["reviewer_items"]
        and bridge_phase8.get("retrieval_results")
        == phase78["phase8"]["retrieval_items"],
        "same-process bridge report digests or normalized results differ from the reports",
    )
    collection_name_by_role = {
        "phase7_runtime_receipts": required_candidate_names[1],
        "phase8_reviewer_receipts": required_candidate_names[2],
        "phase8_retrieval_receipts": required_candidate_names[3],
    }
    require(
        set(collection_digests) == set(collection_name_by_role)
        and all(
            collection_digests.get(role)
            == "sha256:" + candidate_by_name[name]["sha256"]
            for role, name in collection_name_by_role.items()
        ),
        "same-process bridge did not bind the three exact candidate receipt collections",
    )

    phase7_report_items = {
        str(item["receipt_id"]): item for item in phase78["phase7"]["items"]
    }
    used_evidence_ids = set(historical_evidence_ids) | set(current_evidence_ids)
    used_chain_digests = set(historical_chain_digests) | set(current_chain_digests)
    phase7_live_slots = _bind_bridge_live_slots(
        slots=bridge_phase7.get("live_slot_results"),
        id_field="receipt_id",
        expected_ids=set(phase7_report_items),
        expected_kinds=None,
        evidence_release=evidence_release,
        evidence_release_tag=evidence_release_tag,
        repository=repository,
        evidence_by_id=evidence_by_id,
        evidence_by_name={item["name"]: item for item in evidence_inventory},
        used_asset_ids=bound_current_asset_ids,
        used_evidence_ids=used_evidence_ids,
        used_chain_digests=used_chain_digests,
        label="Phase 7",
    )
    for slot in phase7_live_slots:
        report_item = phase7_report_items[str(slot["receipt_id"])]
        require(
            report_item.get("external_evidence_id") == slot.get("evidence_id")
            and report_item.get("external_live_result_digest")
            == slot.get("live_result_digest")
            and report_item.get("external_verifier_workflow_run_id")
            == slot.get("verifier_workflow_run_id")
            and report_item.get("external_verified_at") == slot.get("verified_at"),
            f"Phase 7 live slot differs from its report item: {slot.get('receipt_id')}",
        )
    reviewer_ids = {
        str(item["run_id"]) for item in phase78["phase8"]["reviewer_items"]
    }
    retrieval_ids = {
        str(item["receipt_id"]) for item in phase78["phase8"]["retrieval_items"]
    }
    phase8_kinds = {identifier: "reviewer" for identifier in reviewer_ids}
    phase8_kinds.update({identifier: "retrieval" for identifier in retrieval_ids})
    phase8_live_slots = _bind_bridge_live_slots(
        slots=bridge_phase8.get("live_slot_results"),
        id_field="slot_id",
        expected_ids=reviewer_ids | retrieval_ids,
        expected_kinds=phase8_kinds,
        evidence_release=evidence_release,
        evidence_release_tag=evidence_release_tag,
        repository=repository,
        evidence_by_id=evidence_by_id,
        evidence_by_name={item["name"]: item for item in evidence_inventory},
        used_asset_ids=bound_current_asset_ids,
        used_evidence_ids=used_evidence_ids,
        used_chain_digests=used_chain_digests,
        label="Phase 8",
    )
    require(
        len(
            {
                str(slot.get("execution_id"))
                for slot in phase8_live_slots
                if isinstance(slot.get("execution_id"), str)
                and slot.get("execution_id")
            }
        )
        == 12
        and all(
            re.fullmatch(r"sha256:[0-9a-f]{64}", str(slot.get("subject_digest")))
            is not None
            for slot in phase8_live_slots
        ),
        "Phase 8 live slots reuse execution IDs or omit subject digests",
    )
    require(
        bound_current_asset_ids == set(evidence_by_id),
        "evidence Release contains an unbound asset or omits a bound live asset",
    )
    require(
        len(used_evidence_ids) == 30 + len(history_items)
        and len(used_chain_digests) == 120 + 4 * len(history_items),
        "accepted evidence does not contain 30 globally unique current R/E/V/I chains",
    )
    phase78["phase7"]["live_slot_results"] = phase7_live_slots
    phase78["phase8"]["live_slot_results"] = phase8_live_slots
    return {
        "schema_version": SCHEMA,
        "acceptance_scope": "producer_internal",
        "external_consumer_required": True,
        "counts_as_phase78_closure": False,
        "workflow_path": WORKFLOW_PATH,
        "workflow_event": "workflow_dispatch",
        "repository": repository,
        "run_id": run_id,
        "run_attempt": run_attempt,
        "trusted_source_commit": source_commit,
        "releases": {
            "evidence": evidence_release,
            "candidate": candidate_release,
        },
        "candidate_assets": [candidate_by_name[name] for name in required_candidate_names],
        "candidate_ledger_sha256": candidate_ledger_digest,
        "evidence_inventory": evidence_inventory,
        "candidate_release_inventory": candidate_inventory,
        "phase7": phase78["phase7"],
        "phase8": phase78["phase8"],
        "release_evidence": {
            "adapter_id": runner.get("adapter_id"),
            "verified_record_count": 8,
            "historical_verified_record_count": len(history_items),
            "provider_verified": False,
            "items": release_results,
            "history_items": history_items,
            "unique_current_chain_count": 30,
            "unique_current_evidence_id_count": 30,
            "unique_current_chain_digest_count": 120,
        },
        "final_status": {
            "phase7": "complete_preview_attested",
            "phase8": "complete_preview_attested",
            "provider_verified": False,
            "accepted": True,
        },
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    for name in (
        "evidence-release-json",
        "candidate-release-json",
        "evidence-assets-json",
        "candidate-assets-json",
        "evidence-asset-dir",
        "candidate-asset-dir",
        "candidate-ledger",
        "phase7-report",
        "phase8-report",
        "phase78-bridge-result",
        "release-runner-result",
        "repository",
        "source-commit",
        "evidence-release-tag",
        "candidate-release-tag",
        "evidence-final-commit",
        "candidate-final-commit",
        "run-id",
        "run-attempt",
        "output",
    ):
        value.add_argument(f"--{name}", required=True)
    value.add_argument("--candidate-asset-name", action="append", required=True)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        summary = build_summary(
            evidence_release_json=Path(args.evidence_release_json),
            candidate_release_json=Path(args.candidate_release_json),
            evidence_assets_json=Path(args.evidence_assets_json),
            candidate_assets_json=Path(args.candidate_assets_json),
            evidence_asset_dir=Path(args.evidence_asset_dir),
            candidate_asset_dir=Path(args.candidate_asset_dir),
            candidate_ledger_path=Path(args.candidate_ledger),
            candidate_asset_names=args.candidate_asset_name,
            phase7_report_path=Path(args.phase7_report),
            phase8_report_path=Path(args.phase8_report),
            phase78_bridge_result_path=Path(args.phase78_bridge_result),
            release_runner_result_path=Path(args.release_runner_result),
            repository=args.repository,
            source_commit=args.source_commit,
            evidence_release_tag=args.evidence_release_tag,
            candidate_release_tag=args.candidate_release_tag,
            evidence_final_commit=args.evidence_final_commit,
            candidate_final_commit=args.candidate_final_commit,
            run_id=int(args.run_id),
            run_attempt=int(args.run_attempt),
        )
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(summary, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
    except (OSError, ValueError, AcceptedSummaryError) as exc:
        print(f"OpenAI Preview accepted-run summary failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
