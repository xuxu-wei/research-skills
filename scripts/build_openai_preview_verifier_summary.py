#!/usr/bin/env python3
"""Build the immutable per-run summary for a live Preview verifier workflow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA = "openai-preview-live-verifier-summary/v1"
WORKFLOW_PATH = ".github/workflows/openai-preview-evidence.yml"
SHA256_RE = re.compile(r"[0-9a-f]{64}")
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
RAW_KINDS = {"raw_export", "structured_export", "task_export"}
ROLES = {
    "envelope_asset": ("envelope_asset_id", {"evidence_envelope"}),
    "release_asset_index_asset": (
        "release_asset_index_asset_id",
        {"release_asset_index"},
    ),
    "raw_export_asset": ("raw_export_asset_id", RAW_KINDS),
    "verifier_report_asset": ("verifier_report_asset_id", {"verifier_report"}),
}


class SummaryError(ValueError):
    pass


def fail(message: str) -> None:
    raise SummaryError(message)


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"{label} is not readable JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
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


def bare_digest(value: Any, label: str) -> str:
    if not isinstance(value, str):
        fail(f"{label} is not a digest")
    digest = value.removeprefix("sha256:")
    if SHA256_RE.fullmatch(digest) is None:
        fail(f"{label} is not a lowercase SHA-256")
    return digest


def positive_id(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        fail(f"{label} must be a positive integer")
    return value


def asset_locator(value: Mapping[str, Any], label: str) -> dict[str, Any]:
    return {
        "asset_id": positive_id(value.get("asset_id"), f"{label}.asset_id"),
        "name": safe_name(value.get("name"), f"{label}.name"),
        "sha256": bare_digest(value.get("sha256"), f"{label}.sha256"),
    }


def build_summary(
    *,
    result_dir: Path,
    asset_dir: Path,
    release_json: Path,
    source_commit: str,
    repository: str,
    run_id: int,
) -> dict[str, Any]:
    if COMMIT_RE.fullmatch(source_commit) is None:
        fail("source_commit must be a full lowercase commit")
    if REPOSITORY_RE.fullmatch(repository) is None:
        fail("repository must be owner/name")
    positive_id(run_id, "run_id")
    release = load_object(release_json, "release")
    release_id = positive_id(release.get("id"), "release.id")
    release_tag = release.get("tag_name")
    if not isinstance(release_tag, str) or not release_tag:
        fail("release.tag_name is missing")
    if (
        release.get("draft") is not False
        or release.get("prerelease") is not True
        or release.get("immutable") is not True
    ):
        fail("release must be a published immutable prerelease")

    paths = sorted(path for path in result_dir.glob("*.json") if path.is_file())
    if not paths:
        fail("the verifier produced no result files")
    bundles: list[dict[str, Any]] = []
    used_assets: set[int] = set()
    for path in paths:
        result = load_object(path, f"result {path.name}")
        live = result.get("live_verifier")
        source = result.get("source_identity")
        if (
            result.get("schema_version") != 3
            or result.get("verdict") != "preview_attested"
            or result.get("provider_verified") is not False
            or result.get("gate_eligible") is not True
            or result.get("counts_as_preview_attested") is not True
            or result.get("counts_as_provider_verified") is not False
            or not isinstance(live, Mapping)
            or live.get("verifier_workflow_run_id") != run_id
            or not isinstance(source, Mapping)
            or source.get("source_commit") != source_commit
        ):
            fail(f"result {path.name} is not a live Preview result for this run/source")
        assets = result.get("verified_assets")
        integrity = result.get("integrity_result")
        if not isinstance(assets, list) or not isinstance(integrity, Mapping):
            fail(f"result {path.name} has no verified_assets/integrity_result")
        if len(assets) != 4:
            fail(f"result {path.name} must bind exactly four Preview assets")
        by_id: dict[int, tuple[dict[str, Any], str]] = {}
        for offset, value in enumerate(assets):
            if not isinstance(value, Mapping):
                fail(f"result {path.name} asset {offset} is not an object")
            kind = value.get("evidence_kind")
            locator = asset_locator(value, f"result {path.name}.{kind}")
            if locator["asset_id"] in by_id:
                fail(f"result {path.name} repeats an asset ID")
            if locator["asset_id"] in used_assets:
                fail("an evidence asset is reused across verifier results")
            local_asset = asset_dir / locator["name"]
            try:
                local_digest = hashlib.sha256(local_asset.read_bytes()).hexdigest()
            except OSError as exc:
                fail(f"verified asset {locator['name']} cannot be snapshotted: {exc}")
            if local_digest != locator["sha256"]:
                fail(f"verified asset {locator['name']} changed after live verification")
            used_assets.add(locator["asset_id"])
            by_id[locator["asset_id"]] = (locator, str(kind))

        by_role: dict[str, dict[str, Any]] = {}
        for role, (id_field, allowed_kinds) in ROLES.items():
            asset_id = positive_id(integrity.get(id_field), f"integrity_result.{id_field}")
            matched = by_id.get(asset_id)
            if matched is None or matched[1] not in allowed_kinds:
                fail(f"result {path.name} does not bind {role} to its declared asset/kind")
            by_role[role] = matched[0]
        if len({item["asset_id"] for item in by_role.values()}) != 4:
            fail(f"result {path.name} reuses one asset across R/E/V/I roles")

        raw_locator = by_role["raw_export_asset"]
        raw_path = asset_dir / raw_locator["name"]
        raw = load_object(raw_path, f"raw export {raw_locator['name']}")
        evidence_type = raw.get("evidence_type")
        if not isinstance(evidence_type, str) or not evidence_type:
            fail(f"raw export {raw_locator['name']} has no evidence_type")
        index_locator = by_role["release_asset_index_asset"]
        index_document = load_object(
            asset_dir / index_locator["name"],
            f"release asset index {index_locator['name']}",
        )
        release_identity = index_document.get("github_release")
        if (
            not isinstance(release_identity, Mapping)
            or release_identity.get("repository") != repository
            or release_identity.get("release_id") != release_id
            or release_identity.get("release_tag") != release_tag
        ):
            fail(
                f"release asset index {index_locator['name']} does not bind the requested Release"
            )
        bundle: dict[str, Any] = {
            "evidence_type": evidence_type,
            "verdict": "preview_attested",
            "provider_verified": False,
            "release_identity": dict(release_identity),
        }
        for role in ROLES:
            bundle[role] = by_role[role]
        bundles.append(bundle)

    bundles.sort(
        key=lambda item: (
            item["evidence_type"],
            item["release_asset_index_asset"]["asset_id"],
        )
    )
    return {
        "schema_version": SCHEMA,
        "run_id": run_id,
        "repository": repository,
        "release_id": release_id,
        "release_tag": release_tag,
        "source_commit": source_commit,
        "workflow_path": WORKFLOW_PATH,
        "workflow_event": "workflow_dispatch",
        "bundles": bundles,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--result-dir", required=True)
    value.add_argument("--asset-dir", required=True)
    value.add_argument("--release-json", required=True)
    value.add_argument("--source-commit", required=True)
    value.add_argument("--repository", required=True)
    value.add_argument("--run-id", required=True, type=int)
    value.add_argument("--output", required=True)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        summary = build_summary(
            result_dir=Path(args.result_dir),
            asset_dir=Path(args.asset_dir),
            release_json=Path(args.release_json),
            source_commit=args.source_commit,
            repository=args.repository,
            run_id=args.run_id,
        )
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except (OSError, SummaryError) as exc:
        print(f"OpenAI Preview verifier summary failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
