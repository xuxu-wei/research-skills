#!/usr/bin/env python3
"""Regression tests for the live release-ledger evidence runner."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from unittest.mock import patch

import yaml

import build_openai_preview_verifier_summary as verifier_summary_builder
import generate_openai_release_ledger as ledger_generator
import test_openai_release_ledger as ledger_contract
import validate_openai_release_evidence as runner


REPOSITORY = "xuxu-wei/research-skills"
REQUIRED_CHECK = "OpenAI Plugin Preview / validate"
WORKFLOW_PATH = ".github/workflows/openai-preview-evidence.yml"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def expect_code(callback: Any, code: str, label: str) -> None:
    try:
        callback()
    except runner.ReleaseEvidenceRunnerError as exc:
        require(exc.code == code, f"{label}: expected {code}, got {exc.code}: {exc}")
    else:
        raise AssertionError(f"{label}: expected {code}")


def git_commit(revision: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", revision],
        cwd=runner.REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def json_bytes(document: Mapping[str, Any]) -> bytes:
    return (json.dumps(document, ensure_ascii=False, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_bytes(path: Path, payload: bytes) -> None:
    path.write_bytes(payload)


def set_pending(record: dict[str, Any], reason: str = "historical fixture pending") -> None:
    record["status"] = "pending"
    record["reason"] = reason
    record["evidence_path"] = None
    record["evidence_sha256"] = None
    record["evidence_locator"] = None


def configure_release_identity(
    release: dict[str, Any], *, version: str, source_commit: str
) -> None:
    release["version"] = version
    release["source_commit"] = {"status": "verified", "sha": source_commit}
    release["receipts"]["rollback"]["from_version"] = version


def configure_current_records(
    release: dict[str, Any], previous: dict[str, Any], registry: Mapping[str, Any]
) -> None:
    version = release["version"]
    source_commit = release["source_commit"]["sha"]
    release["external_evidence_trust"] = {
        "adapter_status": "configured",
        "adapter_id": runner.ADAPTER_ID,
        "verification_level": runner.PREVIEW_ATTESTED,
        "provider_authenticated": False,
        "reason": "Live GitHub Release re-query fixture.",
    }
    release["marketplace_source"]["resolved_commit"].update(sha=source_commit)
    release["ci"]["repository_preview"].update(
        run_id="8101",
        run_url=f"https://github.com/{REPOSITORY}/actions/runs/8101",
        commit_sha=source_commit,
        conclusion="success",
    )
    local = release["ci"]["canonical_plugin_validator"]["local"]
    local.update(
        status="verified",
        result="passed",
        verified_on=datetime.now(timezone.utc).date().isoformat(),
    )
    local.pop("reason", None)
    release["ci"]["canonical_plugin_validator"]["ci"].update(
        run_id="8102", commit_sha=source_commit, conclusion="success"
    )
    release["governance"]["main_branch_protection"].update(
        branch="main",
        required_check=REQUIRED_CHECK,
        verified_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )

    upgrade = release["receipts"]["marketplace_upgrade"]
    reinstall = release["receipts"]["explicit_reinstall"]
    upgrade.update(
        installed_version=version,
        source_commit=source_commit,
        cache_path="cache/current-upgrade",
    )
    reinstall.update(
        installed_version=version,
        source_commit=source_commit,
        cache_path="cache/current-reinstall",
    )
    upgrade["cache_artifact"] = ledger_contract.build_cache_artifact(
        release,
        cache_path=upgrade["cache_path"],
        cache_instance_id="current-upgrade-cache",
    )
    reinstall["cache_artifact"] = ledger_contract.build_cache_artifact(
        release,
        cache_path=reinstall["cache_path"],
        cache_instance_id="current-reinstall-cache",
    )
    policy = registry["public_entry_policy"]
    declared = list(policy["declared_entries"])
    implicit = list(policy["implicit_active_entries"])
    discovery = release["receipts"]["fresh_task_discovery"]
    discovery.update(
        plugin_version=version,
        source_commit=source_commit,
        task_id="fresh-task-release-evidence-001",
        installed_skill_count=len(registry["skills"]),
        explicit_callable_entries=len(declared),
        implicit_prompt_entries=len(implicit),
        explicit_callable_entry_skills=declared,
        implicit_prompt_entry_skills=implicit,
        installed_via="explicit_reinstall",
        cache_artifact=copy.deepcopy(reinstall["cache_artifact"]),
    )
    restored_cache = ledger_contract.build_cache_artifact(
        previous,
        cache_path="cache/rollback-restored",
        cache_instance_id="previous-restored-cache",
    )
    rollback = release["receipts"]["rollback"]
    rollback.update(
        from_version=version,
        to_version=previous["version"],
        target_commit=previous["source_commit"]["sha"],
        restored_cache_path=restored_cache["cache_path"],
        candidate_cache_path=reinstall["cache_artifact"]["cache_path"],
        candidate_from_receipt="explicit_reinstall",
        candidate_cache_artifact=copy.deepcopy(reinstall["cache_artifact"]),
        restored_cache_artifact=restored_cache,
        cache_mixing_absent=True,
    )


class FakeGitHub:
    def __init__(self, responses: Mapping[str, Mapping[str, Any]]) -> None:
        self.responses = copy.deepcopy(dict(responses))
        self.calls: list[str] = []
        self.fail_url: str | None = None

    def __call__(self, url: str) -> Mapping[str, Any]:
        self.calls.append(url)
        if url == self.fail_url:
            raise PermissionError("fixture API access denied")
        if url not in self.responses:
            raise KeyError(url)
        return copy.deepcopy(self.responses[url])


class FakeGitHubBinary:
    def __init__(self, responses: Mapping[str, bytes]) -> None:
        self.responses = dict(responses)
        self.calls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.calls.append(url)
        if url not in self.responses:
            raise KeyError(url)
        return self.responses[url]


class FakeArtifactResponse:
    def __init__(self, payload: bytes, final_url: str) -> None:
        self.payload = payload
        self.final_url = final_url

    def __enter__(self) -> "FakeArtifactResponse":
        return self

    def __exit__(self, *_args: Any) -> None:
        return None

    def geturl(self) -> str:
        return self.final_url

    def read(self, limit: int) -> bytes:
        return self.payload[:limit]


class FakeArtifactOpener:
    def __init__(self, handler: Any, payload: bytes, final_url: str) -> None:
        self.handler = handler
        self.payload = payload
        self.final_url = final_url
        self.request: Any = None

    def open(self, request: Any, timeout: int) -> FakeArtifactResponse:
        self.request = request
        require(timeout == 30, "artifact transport timeout")
        self.handler.redirect_count = 1
        return FakeArtifactResponse(self.payload, self.final_url)


def summary_archive(document: Mapping[str, Any], *, extra_member: bool = False) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(runner.RUN_SUMMARY_JSON_NAME, json_bytes(document))
        if extra_member:
            archive.writestr("unexpected.json", b"{}\n")
    return buffer.getvalue()


class FakeLiveVerifier:
    adapter_id = runner.ADAPTER_ID

    def __init__(
        self,
        bundles: Mapping[str, Mapping[str, Any]],
        adapter_code_sha256: str,
    ) -> None:
        self.bundles = {
            (str(Path(str(meta["directory"])).resolve()), str(meta["raw_name"])): meta
            for meta in bundles.values()
        }
        self.adapter_code_sha256 = adapter_code_sha256
        self.calls: list[str] = []
        self.tamper_during_call = False
        self.wrong_verified_asset = False

    def __call__(self, request: Mapping[str, Any]) -> dict[str, Any]:
        root = str(Path(str(request["evidence_root"])).resolve())
        meta = self.bundles[(root, str(request["raw_export_path"]))]
        self.calls.append(str(meta["evidence_type"]))
        if self.tamper_during_call:
            raw_path = Path(root) / str(meta["raw_name"])
            raw_path.write_bytes(raw_path.read_bytes() + b" ")
        verified_assets = []
        for field in (
            "envelope_asset",
            "raw_export_asset",
            "verifier_report_asset",
            "release_asset_index_asset",
        ):
            asset = meta["locator"][field]
            verified_assets.append(
                {
                    "asset_id": asset["asset_id"],
                    "name": asset["name"],
                    "sha256": "sha256:" + asset["sha256"],
                    "state": "uploaded",
                }
            )
        if self.wrong_verified_asset:
            verified_assets[0]["sha256"] = "sha256:" + "0" * 64
        locator = meta["locator"]
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        return {
            "schema_version": 3,
            "verification_level": runner.PREVIEW_ATTESTED,
            "provider_verified": False,
            "adapter_id": runner.ADAPTER_ID,
            "source_identity": copy.deepcopy(request["expected_source_identity"]),
            "verified_assets": verified_assets,
            "integrity_result": {
                "evidence_id": (
                    f"live-{meta['evidence_type']}-"
                    f"{meta['locator']['release_id']}"
                ),
                "integrity_valid": True,
                "gate_eligible": False,
                "claimed_verification_level": runner.PREVIEW_ATTESTED,
                "claimed_provider_verified": False,
                "claimed_counts_as_preview_acceptance": True,
                "source_identity_bound": True,
                "raw_export_asset_id": locator["raw_export_asset"]["asset_id"],
                "raw_export_sha256": "sha256:"
                + locator["raw_export_asset"]["sha256"],
                "envelope_sha256": "sha256:"
                + locator["envelope_asset"]["sha256"],
                "verifier_report_asset_id": locator["verifier_report_asset"][
                    "asset_id"
                ],
                "verifier_report_sha256": "sha256:"
                + locator["verifier_report_asset"]["sha256"],
                "release_asset_index_sha256": "sha256:"
                + locator["release_asset_index_asset"]["sha256"],
            },
            "live_verifier": {
                "adapter_id": runner.ADAPTER_ID,
                "adapter_code_sha256": self.adapter_code_sha256,
                "live_requery": True,
                "live_requery_performed": True,
                "independent": True,
                "requery_source": "github_api",
                "verified_at": now,
                # Deliberately the current Phase 8 execution. The runner must
                # replace this with the separately re-queried historical run.
                "verifier_workflow_run_id": 999999,
                "verifier_run_url": (
                    f"https://github.com/{REPOSITORY}/actions/runs/999999"
                ),
            },
            "gate_eligibility": {
                "eligible": True,
                "level": runner.PREVIEW_ATTESTED,
                "determined_by": "registered_live_verifier",
                "provider_adapter_id": None,
                "provider_authenticated": False,
            },
            "gate_eligible": True,
            "counts_as_preview_attested": True,
            "counts_as_provider_verified": False,
            "synthetic_self_test": False,
        }


def add_bundle(
    root: Path,
    record: dict[str, Any],
    evidence_type: str,
    source_identity: Mapping[str, Any],
    sequence: int,
    *,
    raw_type: str | None = None,
    release_id: int = 70000,
    release_tag: str = "research-skills-openai-live-fixture",
    verifier_run_id: int = 90000,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    directory = root / f"{sequence:02d}-{evidence_type}"
    directory.mkdir(parents=True)
    base_id = 10000 + sequence * 10
    capture_run_id = 80000 + sequence
    names = {
        "raw": f"{evidence_type}-raw.json",
        "envelope": f"{evidence_type}-envelope.json",
        "report": f"{evidence_type}-verifier-report.json",
        "index": f"{evidence_type}-release-asset-index.json",
    }
    captured_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    raw_document: dict[str, Any] = {
        "schema_version": 3,
        "captured_at": captured_at,
        "evidence_type": raw_type or evidence_type,
        "observed": ledger_contract.evidence_payload(record),
    }
    cache_inventory = ledger_contract.cache_inventory_for_evidence(
        record, evidence_type
    )
    if cache_inventory is not None:
        raw_document.update(
            cache_inventory_complete=True,
            cache_inventory=cache_inventory,
        )
    raw_payload = json_bytes(raw_document)
    envelope_payload = json_bytes(
        {
            "schema_version": "openai-preview-evidence-envelope/v1",
            "capture": {
                "captured_at": captured_at,
                "raw_export_asset_id": base_id + 1,
            },
        }
    )
    report_payload = json_bytes(
        {
            "schema_version": "openai-preview-verifier-report/v1",
            "evidence_type": evidence_type,
        }
    )
    write_bytes(directory / names["raw"], raw_payload)
    write_bytes(directory / names["envelope"], envelope_payload)
    write_bytes(directory / names["report"], report_payload)

    def indexed(
        asset_id: int, name: str, kind: str, payload: bytes
    ) -> dict[str, Any]:
        return {
            "asset_id": asset_id,
            "name": name,
            "sha256": "sha256:" + sha256(payload),
            "size": len(payload),
            "evidence_kind": kind,
            "browser_download_url": (
                f"https://github.com/{REPOSITORY}/releases/download/fixture/{name}"
            ),
        }

    assets = [
        indexed(base_id + 1, names["raw"], "structured_export", raw_payload),
        indexed(
            base_id + 2,
            names["envelope"],
            "evidence_envelope",
            envelope_payload,
        ),
        indexed(
            base_id + 3,
            names["report"],
            "verifier_report",
            report_payload,
        ),
    ]
    index_document = {
        "schema_version": "openai-preview-release-asset-index/v1",
        "source_identity": dict(source_identity),
        "github_release": {
            "repository": REPOSITORY,
            "release_id": release_id,
            "release_tag": release_tag,
        },
        # This is the capture/main-push witness carried by I. It is distinct
        # from the later evidence-workflow run persisted only in the locator.
        "github_witness": {
            "workflow_run_id": capture_run_id,
            "workflow_id": 60001,
            "workflow_path": ".github/workflows/openai-plugin-preview.yml",
            "workflow_event": "push",
            "run_head_sha": source_identity["source_commit"],
            "source_commit": source_identity["source_commit"],
            "actor": "fixture-bot",
        },
        "assets": assets,
    }
    index_payload = json_bytes(index_document)
    write_bytes(directory / names["index"], index_payload)
    locator = {
        "repository": REPOSITORY,
        "release_id": release_id,
        "release_tag": release_tag,
        "capture_workflow_run_id": capture_run_id,
        "verifier_workflow_run_id": verifier_run_id,
        "verifier_run_url": (
            f"https://github.com/{REPOSITORY}/actions/runs/{verifier_run_id}"
        ),
        "envelope_asset": {
            "asset_id": base_id + 2,
            "name": names["envelope"],
            "sha256": sha256(envelope_payload),
        },
        "release_asset_index_asset": {
            "asset_id": base_id + 4,
            "name": names["index"],
            "sha256": sha256(index_payload),
        },
        "raw_export_asset": {
            "asset_id": base_id + 1,
            "name": names["raw"],
            "sha256": sha256(raw_payload),
        },
        "verifier_report_asset": {
            "asset_id": base_id + 3,
            "name": names["report"],
            "sha256": sha256(report_payload),
        },
    }
    record["status"] = runner.PREVIEW_ATTESTED
    record.pop("reason", None)
    record["evidence_path"] = None
    record["evidence_sha256"] = None
    record["evidence_locator"] = locator
    meta = {
        "evidence_type": evidence_type,
        "locator": locator,
        "raw_name": names["raw"],
        "directory": directory,
    }
    run_url = f"https://api.github.com/repos/{REPOSITORY}/actions/runs/{verifier_run_id}"
    run = {
        "id": verifier_run_id,
        "url": run_url,
        "html_url": locator["verifier_run_url"],
        "repository": {"full_name": REPOSITORY},
        "workflow_id": 50001,
        "path": WORKFLOW_PATH,
        "event": "workflow_dispatch",
        "status": "completed",
        "conclusion": "success",
        "head_sha": source_identity["source_commit"],
    }
    return meta, {run_url: run}, locator


def build_fixture(
    root: Path,
    base_ledger: Mapping[str, Any],
    registry: Mapping[str, Any],
    *,
    raw_type_overrides: Mapping[str, str] | None = None,
    accepted_previous: bool = False,
) -> dict[str, Any]:
    ledger = copy.deepcopy(dict(base_ledger))
    head = git_commit("HEAD")
    parent = git_commit("HEAD^")
    release = ledger["release"]
    configure_release_identity(
        release, version=str(release["version"]), source_commit=head
    )
    previous = copy.deepcopy(release)
    configure_release_identity(
        previous, version="0.6.0-preview.1", source_commit=parent
    )
    previous["external_evidence_trust"] = {
        "adapter_status": "unavailable",
        "adapter_id": None,
        "verification_level": None,
        "provider_authenticated": False,
        "reason": "Historical fixture has no accepted external records.",
    }
    for record in runner.external_records(previous).values():
        require(isinstance(record, dict), "previous record shape")
        set_pending(record)
    configure_current_records(release, previous, registry)

    bundle_root = root / "bundles"
    bundle_root.mkdir(parents=True)
    source_identity = ledger_contract.release_source_identity(release)
    require(source_identity is not None, "current source identity")
    bundle_meta: dict[str, dict[str, Any]] = {}
    responses: dict[str, Mapping[str, Any]] = {}
    for sequence, evidence_type in enumerate(sorted(runner.EXPECTED_EVIDENCE_TYPES), 1):
        record = runner.external_records(release)[evidence_type]
        require(isinstance(record, dict), f"{evidence_type} record shape")
        # Status is excluded from the raw observation, but the substantive
        # fields must be final before the export is sealed.
        record["status"] = runner.PREVIEW_ATTESTED
        record.pop("reason", None)
        record["evidence_path"] = None
        record["evidence_sha256"] = None
        record["evidence_locator"] = None
        meta, run_response, _ = add_bundle(
            bundle_root,
            record,
            evidence_type,
            source_identity,
            sequence,
            raw_type=(raw_type_overrides or {}).get(evidence_type),
        )
        bundle_meta[str(meta["directory"].resolve())] = meta
        responses.update(run_response)

    verifier_run_id = 90000
    summary_document = {
        "schema_version": runner.RUN_SUMMARY_SCHEMA,
        "run_id": verifier_run_id,
        "repository": REPOSITORY,
        "release_id": 70000,
        "release_tag": "research-skills-openai-live-fixture",
        "source_commit": source_identity["source_commit"],
        "workflow_path": WORKFLOW_PATH,
        "workflow_event": "workflow_dispatch",
        "bundles": [
            {
                "evidence_type": meta["evidence_type"],
                "verdict": runner.PREVIEW_ATTESTED,
                "provider_verified": False,
                "release_identity": {
                    "repository": REPOSITORY,
                    "release_id": meta["locator"]["release_id"],
                    "release_tag": meta["locator"]["release_tag"],
                },
                **{
                    field: copy.deepcopy(meta["locator"][field])
                    for field in (
                        "envelope_asset",
                        "release_asset_index_asset",
                        "raw_export_asset",
                        "verifier_report_asset",
                    )
                },
            }
            for meta in bundle_meta.values()
        ],
    }
    summary_payload = summary_archive(summary_document)
    artifact_id = 99000
    artifact_list_url = (
        f"https://api.github.com/repos/{REPOSITORY}/actions/runs/{verifier_run_id}/artifacts"
    )
    artifact_archive_url = (
        f"https://api.github.com/repos/{REPOSITORY}/actions/artifacts/"
        f"{artifact_id}/zip"
    )
    responses[artifact_list_url] = {
        "total_count": 1,
        "artifacts": [
            {
                "id": artifact_id,
                "name": f"{runner.RUN_SUMMARY_ARTIFACT_PREFIX}{verifier_run_id}",
                "size_in_bytes": len(summary_payload),
                "digest": "sha256:" + sha256(summary_payload),
                "expired": False,
                "archive_download_url": artifact_archive_url,
                "workflow_run": {"id": verifier_run_id},
            }
        ],
    }
    binary_responses = {artifact_archive_url: summary_payload}

    if accepted_previous:
        previous["external_evidence_trust"] = {
            "adapter_status": "configured",
            "adapter_id": runner.ADAPTER_ID,
            "verification_level": runner.PREVIEW_ATTESTED,
            "provider_authenticated": False,
            "reason": "Historical accepted fixture requires live re-query.",
        }
        previous_record = previous["marketplace_source"]["resolved_commit"]
        previous_record["sha"] = previous["source_commit"]["sha"]
        previous_identity = ledger_contract.release_source_identity(previous)
        require(previous_identity is not None, "previous source identity")
        previous_meta, previous_run, _ = add_bundle(
            bundle_root,
            previous_record,
            "marketplace_resolved_commit",
            previous_identity,
            101,
            release_id=71000,
            release_tag="research-skills-openai-previous-live-fixture",
            verifier_run_id=91000,
        )
        bundle_meta[str(previous_meta["directory"].resolve())] = previous_meta
        responses.update(previous_run)
        previous_summary = {
            "schema_version": runner.RUN_SUMMARY_SCHEMA,
            "run_id": 91000,
            "repository": REPOSITORY,
            "release_id": 71000,
            "release_tag": "research-skills-openai-previous-live-fixture",
            "source_commit": previous_identity["source_commit"],
            "workflow_path": WORKFLOW_PATH,
            "workflow_event": "workflow_dispatch",
            "bundles": [
                {
                    "evidence_type": "marketplace_resolved_commit",
                    "verdict": runner.PREVIEW_ATTESTED,
                    "provider_verified": False,
                    "release_identity": {
                        "repository": REPOSITORY,
                        "release_id": previous_meta["locator"]["release_id"],
                        "release_tag": previous_meta["locator"]["release_tag"],
                    },
                    **{
                        field: copy.deepcopy(previous_meta["locator"][field])
                        for field in (
                            "envelope_asset",
                            "release_asset_index_asset",
                            "raw_export_asset",
                            "verifier_report_asset",
                        )
                    },
                }
            ],
        }
        previous_summary_payload = summary_archive(previous_summary)
        previous_artifact_id = 99100
        previous_list_url = (
            f"https://api.github.com/repos/{REPOSITORY}/actions/runs/91000/artifacts"
        )
        previous_archive_url = (
            f"https://api.github.com/repos/{REPOSITORY}/actions/artifacts/"
            f"{previous_artifact_id}/zip"
        )
        responses[previous_list_url] = {
            "total_count": 1,
            "artifacts": [
                {
                    "id": previous_artifact_id,
                    "name": f"{runner.RUN_SUMMARY_ARTIFACT_PREFIX}91000",
                    "size_in_bytes": len(previous_summary_payload),
                    "digest": "sha256:" + sha256(previous_summary_payload),
                    "expired": False,
                    "archive_download_url": previous_archive_url,
                    "workflow_run": {"id": 91000},
                }
            ],
        }
        binary_responses[previous_archive_url] = previous_summary_payload

    workflow_url = (
        f"https://api.github.com/repos/{REPOSITORY}/actions/workflows/"
        "openai-preview-evidence.yml"
    )
    responses[workflow_url] = {
        "id": 50001,
        "url": (
            f"https://api.github.com/repos/{REPOSITORY}/actions/workflows/50001"
        ),
        "path": WORKFLOW_PATH,
        "state": "active",
    }
    responses[
        f"https://api.github.com/repos/{REPOSITORY}/branches/main/protection"
    ] = {
        "required_status_checks": {
            "contexts": [REQUIRED_CHECK],
            "checks": [{"context": REQUIRED_CHECK, "app_id": 15368}],
        }
    }
    responses[
        f"https://api.github.com/repos/{REPOSITORY}/commits/"
        f"{source_identity['source_commit']}/check-runs"
    ] = {
        "total_count": 1,
        "check_runs": [
            {
                "id": 88001,
                # GitHub's Checks API exposes the job name, while branch
                # protection stores the workflow/job context.
                "name": "validate",
                "head_sha": source_identity["source_commit"],
                "status": "completed",
                "conclusion": "success",
                "app": {"id": 15368, "slug": "github-actions"},
            }
        ],
    }
    ledger["previous_releases"] = [previous]
    return {
        "ledger": ledger,
        "release": release,
        "previous": previous,
        "bundle_root": bundle_root,
        "bundles": bundle_meta,
        "responses": responses,
        "binary_responses": binary_responses,
        "summary_document": summary_document,
        "summary_artifact_list_url": artifact_list_url,
        "summary_archive_url": artifact_archive_url,
        "source_identity": source_identity,
    }


def adapter_digest() -> str:
    errors: list[str] = []
    digest = ledger_contract.registered_adapter_verifier_digest(
        runner.ADAPTER_ID, "runner fixture", errors
    )
    require(digest is not None and not errors, f"adapter digest: {errors}")
    return str(digest)


def callback_for(
    fixture: Mapping[str, Any], phase8: Any
) -> tuple[runner.ReleaseEvidenceLiveCallback, FakeLiveVerifier, FakeGitHub]:
    live = FakeLiveVerifier(fixture["bundles"], adapter_digest())
    github = FakeGitHub(fixture["responses"])
    github_binary = FakeGitHubBinary(fixture["binary_responses"])
    callback = runner._create_test_callback(
        fixture["bundle_root"],
        live_verifier=live,
        github_run_fetcher=github,
        github_binary_fetcher=github_binary,
        phase8_module=phase8,
    )
    return callback, live, github


def build_first_pass_summary(
    fixture: Mapping[str, Any], root: Path
) -> dict[str, Any]:
    """Build the durable witness with the real first-pass summary builder."""

    result_dir = root / "builder-results"
    asset_dir = root / "builder-assets"
    result_dir.mkdir()
    asset_dir.mkdir()
    kind_by_field = {
        "raw_export_asset": "structured_export",
        "envelope_asset": "evidence_envelope",
        "verifier_report_asset": "verifier_report",
        "release_asset_index_asset": "release_asset_index",
    }
    integrity_field = {
        "raw_export_asset": "raw_export_asset_id",
        "envelope_asset": "envelope_asset_id",
        "verifier_report_asset": "verifier_report_asset_id",
        "release_asset_index_asset": "release_asset_index_asset_id",
    }
    for offset, meta in enumerate(fixture["bundles"].values()):
        locator = meta["locator"]
        verified_assets: list[dict[str, Any]] = []
        integrity: dict[str, Any] = {}
        for field, evidence_kind in kind_by_field.items():
            asset = locator[field]
            source = Path(meta["directory"]) / asset["name"]
            target = asset_dir / asset["name"]
            target.write_bytes(source.read_bytes())
            verified_assets.append(
                {
                    "asset_id": asset["asset_id"],
                    "name": asset["name"],
                    "sha256": "sha256:" + asset["sha256"],
                    "evidence_kind": evidence_kind,
                }
            )
            integrity[integrity_field[field]] = asset["asset_id"]
        (result_dir / f"{offset:02d}.json").write_bytes(
            json_bytes(
                {
                "schema_version": 3,
                "verdict": runner.PREVIEW_ATTESTED,
                "provider_verified": False,
                "gate_eligible": True,
                "counts_as_preview_attested": True,
                "counts_as_provider_verified": False,
                "source_identity": copy.deepcopy(fixture["source_identity"]),
                "live_verifier": {"verifier_workflow_run_id": 90000},
                "verified_assets": verified_assets,
                "integrity_result": integrity,
                }
            )
        )
    release_path = root / "builder-release.json"
    release_path.write_bytes(
        json_bytes(
            {
            "id": 70000,
            "tag_name": "research-skills-openai-live-fixture",
            "draft": False,
            "prerelease": True,
            "immutable": True,
            }
        )
    )
    return verifier_summary_builder.build_summary(
        result_dir=result_dir,
        asset_dir=asset_dir,
        release_json=release_path,
        source_commit=fixture["source_identity"]["source_commit"],
        repository=REPOSITORY,
        run_id=90000,
    )


def flatten_bundles(fixture: dict[str, Any]) -> None:
    """Match the single flat directory produced by ``gh release download``."""

    root = Path(fixture["bundle_root"])
    for meta in fixture["bundles"].values():
        directory = Path(meta["directory"])
        for source in directory.iterdir():
            shutil.move(str(source), str(root / source.name))
        directory.rmdir()
        meta["directory"] = root


def reseal_summary(
    fixture: dict[str, Any], document: Mapping[str, Any], *, extra_member: bool = False
) -> None:
    payload = summary_archive(document, extra_member=extra_member)
    archive_url = fixture["summary_archive_url"]
    fixture["binary_responses"][archive_url] = payload
    listing = fixture["responses"][fixture["summary_artifact_list_url"]]
    listing["artifacts"][0]["size_in_bytes"] = len(payload)
    listing["artifacts"][0]["digest"] = "sha256:" + sha256(payload)


def callback_request(
    fixture: Mapping[str, Any], evidence_type: str
) -> dict[str, Any]:
    record = runner.external_records(fixture["release"])[evidence_type]
    return {
        "evidence_locator": record["evidence_locator"],
        "evidence_type": evidence_type,
        "expected_source_identity": fixture["source_identity"],
        "expected_adapter_id": runner.ADAPTER_ID,
        "expected_verification_level": runner.PREVIEW_ATTESTED,
    }


def main() -> int:
    phase8 = runner._load_phase8_module()
    base_ledger = ledger_generator.build_ledger()
    registry = yaml.safe_load(
        (runner.PLUGIN / "workflow-registry.yaml").read_text(encoding="utf-8-sig")
    )
    require(isinstance(registry, dict), "registry fixture")

    with tempfile.TemporaryDirectory(prefix="release-runner-success-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        callback, live, github = callback_for(fixture, phase8)
        # The commit-tree validator has its own git-show mutation suite. This
        # fixture uses the dirty working tree so the orchestration test replaces
        # only that already-covered boundary while exercising every other full
        # ledger, prior-release, rollback, provenance, marketplace, and branch
        # protection check in validate_ledger_with_live_bundles.
        with patch.object(
            ledger_contract, "validate_verified_source_commit_tree", lambda *_args: None
        ):
            errors = runner.validate_ledger_with_live_bundles(
                fixture["ledger"], callback
            )
        require(not errors, "full ledger validation: " + "; ".join(errors))
        require(
            set(live.calls) == runner.EXPECTED_EVIDENCE_TYPES
            and len(live.calls) == 8,
            "all eight live evidence types",
        )
        require(
            any("/branches/main/protection" in url for url in github.calls),
            "current branch protection live query",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-history-live-") as temp:
        fixture = build_fixture(
            Path(temp), base_ledger, registry, accepted_previous=True
        )
        callback, live, _ = callback_for(fixture, phase8)
        with patch.object(
            ledger_contract, "validate_verified_source_commit_tree", lambda *_args: None
        ):
            errors = runner.validate_ledger_with_live_bundles(
                fixture["ledger"], callback
            )
        require(
            not errors,
            "accepted previous release live validation: " + "; ".join(errors),
        )
        require(
            len(live.calls) == 9
            and live.calls.count("marketplace_resolved_commit") == 2,
            "accepted previous locator was live re-queried",
        )
        current_results = callback.audit_results()
        history_results = callback.history_audit_results()
        previous_identity = ledger_contract.release_source_identity(
            fixture["previous"]
        )
        require(previous_identity is not None, "previous live source identity")
        current_marketplace = next(
            item
            for item in current_results
            if item["evidence_type"] == "marketplace_resolved_commit"
        )
        require(
            len(current_results) == 8
            and {item["evidence_type"] for item in current_results}
            == runner.EXPECTED_EVIDENCE_TYPES
            and all(item["release_scope"] == "current" for item in current_results)
            and current_marketplace["source_commit"]
            == fixture["source_identity"]["source_commit"],
            "current live results remain the protected eight-record set",
        )
        require(
            len(history_results) == 1
            and history_results[0]["evidence_type"]
            == "marketplace_resolved_commit"
            and history_results[0]["release_scope"] == "previous_releases[0]"
            and history_results[0]["source_commit"]
            == previous_identity["source_commit"],
            "accepted previous result is retained in a separate history set",
        )

        current_key = next(
            key
            for key, scope in callback._binding_scopes.items()
            if scope == "current" and key[0] == "marketplace_resolved_commit"
        )
        history_key = next(
            key
            for key, scope in callback._binding_scopes.items()
            if scope != "current" and key[0] == "marketplace_resolved_commit"
        )
        callback._audit_results[current_key] = copy.deepcopy(
            callback._audit_results[history_key]
        )
        expect_code(
            callback.audit_results,
            "audit_scope_mismatch",
            "historical result cannot overwrite the current audit binding",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-builder-e2e-") as temp:
        root = Path(temp)
        fixture = build_fixture(root, base_ledger, registry)
        built_summary = build_first_pass_summary(fixture, root)
        require(
            len(built_summary["bundles"]) == 8
            and all(
                bundle["release_identity"]
                == {
                    "repository": REPOSITORY,
                    "release_id": 70000,
                    "release_tag": "research-skills-openai-live-fixture",
                }
                for bundle in built_summary["bundles"]
            ),
            "first-pass builder emitted eight Release-bound bundles",
        )
        reseal_summary(fixture, built_summary)
        callback, live, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        for evidence_type in sorted(runner.EXPECTED_EVIDENCE_TYPES):
            callback(**callback_request(fixture, evidence_type))
        callback.assert_complete()
        require(
            len(callback.audit_results()) == 8 and len(live.calls) == 8,
            "builder -> ZIP artifact -> callback round trip",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-adapter-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        adapted = callback(**callback_request(fixture, "repository_preview_ci"))
        locator = runner.external_records(fixture["release"])[
            "repository_preview_ci"
        ]["evidence_locator"]
        require(
            adapted["live_verifier"]["verifier_workflow_run_id"]
            == locator["verifier_workflow_run_id"]
            and adapted["live_verifier"]["verifier_run_url"]
            == locator["verifier_run_url"],
            "historical verifier run replaces current Phase 8 run",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-flat-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        flatten_bundles(fixture)
        callback, live, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        for evidence_type in sorted(runner.EXPECTED_EVIDENCE_TYPES):
            callback(**callback_request(fixture, evidence_type))
        callback.assert_complete()
        require(len(live.calls) == 8, "flat gh release download layout")

    with tempfile.TemporaryDirectory(prefix="release-runner-missing-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        missing = next(iter(fixture["bundles"].values()))["directory"]
        shutil.rmtree(missing)
        callback, _, _ = callback_for(fixture, phase8)
        expect_code(
            lambda: callback.prepare_current_release(fixture["release"]),
            "bundle_not_found",
            "missing bundle",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-type-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        record = runner.external_records(fixture["release"])["rollback"]
        record["status"] = "pending"
        record["reason"] = "missing type"
        callback, _, _ = callback_for(fixture, phase8)
        expect_code(
            lambda: callback.prepare_current_release(fixture["release"]),
            "external_record_not_preview",
            "missing evidence type",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-locator-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        record = runner.external_records(fixture["release"])[
            "repository_preview_ci"
        ]
        record["evidence_locator"]["raw_export_asset"]["asset_id"] += 1000000
        callback, _, _ = callback_for(fixture, phase8)
        expect_code(
            lambda: callback.prepare_current_release(fixture["release"]),
            "bundle_not_found",
            "wrong locator asset id",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-duplicate-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        source = next(iter(fixture["bundles"].values()))["directory"]
        shutil.copytree(source, fixture["bundle_root"] / "duplicate-bundle")
        callback, _, _ = callback_for(fixture, phase8)
        expect_code(
            lambda: callback.prepare_current_release(fixture["release"]),
            "duplicate_bundle",
            "duplicate matching bundle",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-tamper-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        callback, live, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        live.tamper_during_call = True
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "bundle_changed_after_match",
            "TOCTOU rewrite during live verification",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-wrong-raw-") as temp:
        fixture = build_fixture(
            Path(temp),
            base_ledger,
            registry,
            raw_type_overrides={
                "repository_preview_ci": "canonical_plugin_validator_ci"
            },
        )
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        errors: list[str] = []
        ledger_contract.validate_release_evidence(
            fixture["release"],
            fixture["release"]["version"],
            len(registry["skills"]),
            errors,
            expected_explicit_entries=registry["public_entry_policy"][
                "declared_entries"
            ],
            expected_implicit_entries=registry["public_entry_policy"][
                "implicit_active_entries"
            ],
            live_evidence_verifier=callback,
        )
        require(
            any("evidence_type mismatch" in error for error in errors),
            "wrong raw evidence type",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-live-asset-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        callback, live, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        live.wrong_verified_asset = True
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "live_result_locator_mismatch",
            "live result locator mismatch",
        )

    historical_mutations = {
        "workflow path": ("workflow", "path", ".github/workflows/other.yml"),
        "workflow state": ("workflow", "state", "disabled_manually"),
        "workflow id": ("run", "workflow_id", 50002),
        "run event": ("run", "event", "push"),
        "run status": ("run", "status", "in_progress"),
        "run conclusion": ("run", "conclusion", "failure"),
        "run head": ("run", "head_sha", "0" * 40),
        "run repository": ("run_repository", "full_name", "other/repository"),
        "run URL": ("run", "html_url", "https://github.com/other/run/1"),
    }
    for label, (target, field, value) in historical_mutations.items():
        with tempfile.TemporaryDirectory(prefix="release-runner-history-") as temp:
            fixture = build_fixture(Path(temp), base_ledger, registry)
            callback, _, github = callback_for(fixture, phase8)
            workflow_url = (
                f"https://api.github.com/repos/{REPOSITORY}/actions/workflows/"
                "openai-preview-evidence.yml"
            )
            locator = runner.external_records(fixture["release"])[
                "repository_preview_ci"
            ]["evidence_locator"]
            run_url = (
                f"https://api.github.com/repos/{REPOSITORY}/actions/runs/"
                f"{locator['verifier_workflow_run_id']}"
            )
            if target == "workflow":
                github.responses[workflow_url][field] = value
                expected_code = "verifier_run_invalid"
            elif target == "run_repository":
                github.responses[run_url]["repository"][field] = value
                expected_code = "verifier_run_witness_mismatch"
            else:
                github.responses[run_url][field] = value
                expected_code = "verifier_run_witness_mismatch"
            callback.prepare_current_release(fixture["release"])
            expect_code(
                lambda: callback(
                    **callback_request(fixture, "repository_preview_ci")
                ),
                expected_code,
                f"historical {label}",
            )

    with tempfile.TemporaryDirectory(prefix="release-runner-summary-replaced-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        summary = copy.deepcopy(fixture["summary_document"])
        target_bundle = next(
            item
            for item in summary["bundles"]
            if item["evidence_type"] == "repository_preview_ci"
        )
        target_bundle["raw_export_asset"]["sha256"] = "0" * 64
        reseal_summary(fixture, summary)
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "verifier_summary_mismatch",
            "replaced bundle in historical summary",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-summary-duplicate-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        summary = copy.deepcopy(fixture["summary_document"])
        summary["bundles"].append(copy.deepcopy(summary["bundles"][0]))
        reseal_summary(fixture, summary)
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "verifier_summary_invalid",
            "duplicate bundle in historical summary",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-summary-release-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        summary = copy.deepcopy(fixture["summary_document"])
        summary["bundles"][0]["release_identity"]["release_tag"] = "wrong-tag"
        reseal_summary(fixture, summary)
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "verifier_summary_invalid",
            "bundle Release identity differs from its summary and locator",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-artifact-duplicate-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        listing = fixture["responses"][fixture["summary_artifact_list_url"]]
        duplicate = copy.deepcopy(listing["artifacts"][0])
        duplicate["id"] += 1
        listing["artifacts"].append(duplicate)
        listing["total_count"] = 2
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "verifier_summary_invalid",
            "duplicate historical summary artifact",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-summary-zip-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        reseal_summary(
            fixture,
            fixture["summary_document"],
            extra_member=True,
        )
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "verifier_summary_invalid",
            "summary ZIP with an extra member",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-artifact-expired-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        listing = fixture["responses"][fixture["summary_artifact_list_url"]]
        listing["artifacts"][0]["expired"] = True
        callback, _, _ = callback_for(fixture, phase8)
        callback.prepare_current_release(fixture["release"])
        expect_code(
            lambda: callback(**callback_request(fixture, "repository_preview_ci")),
            "verifier_summary_invalid",
            "expired historical summary artifact",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-protection-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        callback, _, github = callback_for(fixture, phase8)
        protection_url = (
            f"https://api.github.com/repos/{REPOSITORY}/branches/main/protection"
        )
        github.responses[protection_url]["required_status_checks"] = {
            "contexts": ["some other check"],
            "checks": [],
        }
        expect_code(
            lambda: callback.prepare_current_release(fixture["release"]),
            "branch_protection_not_enforced",
            "removed current branch protection",
        )
        callback, _, github = callback_for(fixture, phase8)
        github.fail_url = protection_url
        expect_code(
            lambda: callback.prepare_current_release(fixture["release"]),
            "github_live_requery_failed",
            "branch protection permission failure",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-protection-app-") as temp:
        fixture = build_fixture(Path(temp), base_ledger, registry)
        protection_url = (
            f"https://api.github.com/repos/{REPOSITORY}/branches/main/protection"
        )
        fixture["responses"][protection_url]["required_status_checks"]["checks"] = [
            {"context": REQUIRED_CHECK, "app_id": 1}
        ]
        callback, _, _ = callback_for(fixture, phase8)
        expect_code(
            lambda: callback.prepare_current_release(fixture["release"]),
            "branch_protection_check_run_invalid",
            "branch protection bound to the wrong app",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-api-") as temp:
        root = Path(temp)

        def registered(_request: Mapping[str, Any]) -> dict[str, Any]:
            return {}

        registered.adapter_id = runner.ADAPTER_ID  # type: ignore[attr-defined]
        expect_code(
            lambda: runner.ReleaseEvidenceLiveCallback(
                root,
                live_verifier=True,  # type: ignore[arg-type]
                github_run_fetcher=lambda _url: {},
                github_binary_fetcher=lambda _url: b"zip",
                phase8_module=phase8,
                _capability=runner._TEST_CALLBACK_CAPABILITY,
            ),
            "live_verifier_invalid",
            "Boolean live verifier",
        )
        expect_code(
            lambda: runner.ReleaseEvidenceLiveCallback(
                root,
                live_verifier=registered,
                github_run_fetcher=True,  # type: ignore[arg-type]
                github_binary_fetcher=lambda _url: b"zip",
                phase8_module=phase8,
                _capability=runner._TEST_CALLBACK_CAPABILITY,
            ),
            "run_fetcher_invalid",
            "Boolean GitHub verifier",
        )
        expect_code(
            lambda: runner.ReleaseEvidenceLiveCallback(
                root,
                live_verifier=registered,
                github_run_fetcher=lambda _url: {},
                github_binary_fetcher=True,  # type: ignore[arg-type]
                phase8_module=phase8,
                _capability=runner._TEST_CALLBACK_CAPABILITY,
            ),
            "binary_fetcher_invalid",
            "Boolean GitHub artifact fetcher",
        )

    with tempfile.TemporaryDirectory(prefix="release-runner-cli-result-") as temp:
        ledger_path = Path(temp) / "ledger.json"
        ledger_payload = b'{"release":{}}\n'
        ledger_path.write_bytes(ledger_payload)

        class AuditOnlyCallback:
            def audit_results(self) -> list[dict[str, Any]]:
                return [
                    {"evidence_type": evidence_type, "release_scope": "current"}
                    for evidence_type in sorted(runner.EXPECTED_EVIDENCE_TYPES)
                ]

            def history_audit_results(self) -> list[dict[str, Any]]:
                return [
                    {
                        "evidence_type": "marketplace_resolved_commit",
                        "release_scope": "previous_releases[0]",
                    }
                ]

        output_buffer = io.StringIO()
        with patch.object(
            runner, "create_production_callback", return_value=AuditOnlyCallback()
        ), patch.object(
            runner, "validate_ledger_with_live_bundles", return_value=[]
        ), redirect_stdout(output_buffer):
            exit_code = runner.main(
                ["--bundle-root", temp, "--ledger", str(ledger_path)]
            )
        cli_result = json.loads(output_buffer.getvalue())
        require(
            exit_code == 0
            and cli_result["ledger_sha256"]
            == "sha256:" + hashlib.sha256(ledger_payload).hexdigest()
            and cli_result["verified_record_count"] == 8
            and cli_result["historical_verified_record_count"] == 1
            and len(cli_result["live_results"]) == 8
            and len(cli_result["history_results"]) == 1,
            "CLI result binds the exact ledger bytes and separates current/history",
        )

    artifact_api_url = (
        f"https://api.github.com/repos/{REPOSITORY}/actions/artifacts/99000/zip"
    )
    artifact_storage_url = (
        "https://productionresultssa0.blob.core.windows.net/actions-results/"
        "fixture.zip?sig=fixture"
    )
    opener_holder: dict[str, FakeArtifactOpener] = {}

    def build_fake_opener(handler: Any) -> FakeArtifactOpener:
        opener = FakeArtifactOpener(handler, b"fixture-zip", artifact_storage_url)
        opener_holder["opener"] = opener
        return opener

    with patch.dict(os.environ, {"GH_TOKEN": "fixture-token"}, clear=False), patch(
        "validate_openai_release_evidence.urllib.request.build_opener",
        side_effect=build_fake_opener,
    ):
        require(
            runner.download_github_actions_artifact(artifact_api_url)
            == b"fixture-zip",
            "Actions artifact transport",
        )
    transport_request = opener_holder["opener"].request
    require(
        transport_request.unredirected_hdrs.get("Authorization")
        == "Bearer fixture-token"
        and "Authorization" not in transport_request.headers,
        "Actions artifact token must not follow the redirect",
    )
    require(
        runner._actions_artifact_storage_url(artifact_storage_url)
        and not runner._actions_artifact_storage_url(
            "https://example.invalid/fixture.zip?sig=fixture"
        ),
        "Actions artifact redirect allowlist",
    )
    expect_code(
        lambda: runner.download_github_actions_artifact(
            "https://api.github.com/repos/x/y/actions/artifacts/1/zip?unsafe=1"
        ),
        "artifact_download_url_invalid",
        "artifact API query rejected",
    )

    options = {
        option
        for action in runner._build_parser()._actions
        for option in action.option_strings
    }
    require(
        options == {"-h", "--help", "--bundle-root", "--ledger"},
        f"production CLI surface: {sorted(options)}",
    )
    source = Path(runner.__file__).read_text(encoding="utf-8")
    require(
        "live_verifier=phase8.verify" in source
        and "github_binary_fetcher=download_github_actions_artifact" in source
        and "--synthetic" not in options
        and "--verifier-result" not in options,
        "production CLI must hardwire the real Phase 8 verifier",
    )

    print("OpenAI release evidence live-runner tests passed")
    print(
        "coverage: 8/8 records, current branch protection, full ledger/prior/rollback, "
        "historical evidence workflow, wrong/missing/duplicate/tampered bundles, TOCTOU, "
        "wrong raw type/locator/live asset, workflow/run failures, no synthetic CLI"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
