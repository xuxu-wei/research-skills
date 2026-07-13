#!/usr/bin/env python3
"""Focused fail-closed tests for the Preview workflow run summary."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Callable

from build_openai_preview_verifier_summary import SummaryError, build_summary


SOURCE = "a" * 40
REPOSITORY = "owner/repository"
RUN_ID = 12345


def dump(path: Path, value: Any) -> bytes:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    path.write_bytes(payload)
    return payload


def fixture(root: Path) -> tuple[Path, Path, Path, dict[str, Any]]:
    assets = root / "assets"
    results = root / "results"
    assets.mkdir()
    results.mkdir()
    payloads = {
        "raw.json": json.dumps(
            {"evidence_type": "repository_preview_ci", "observed": {}},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8"),
        "envelope.json": b"envelope",
        "verifier.json": b"verifier",
        "index.json": json.dumps(
            {
                "github_release": {
                    "repository": REPOSITORY,
                    "release_id": 77,
                    "release_tag": "v0.7.0-preview.1",
                }
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8"),
    }
    kinds = {
        "raw.json": "raw_export",
        "envelope.json": "evidence_envelope",
        "verifier.json": "verifier_report",
        "index.json": "release_asset_index",
    }
    verified_assets = []
    for offset, (name, payload) in enumerate(payloads.items(), start=101):
        (assets / name).write_bytes(payload)
        verified_assets.append(
            {
                "asset_id": offset,
                "name": name,
                "sha256": "sha256:" + hashlib.sha256(payload).hexdigest(),
                "evidence_kind": kinds[name],
            }
        )
    result = {
        "schema_version": 3,
        "verdict": "preview_attested",
        "provider_verified": False,
        "gate_eligible": True,
        "counts_as_preview_attested": True,
        "counts_as_provider_verified": False,
        "source_identity": {"source_commit": SOURCE},
        "live_verifier": {"verifier_workflow_run_id": RUN_ID},
        "verified_assets": verified_assets,
        "integrity_result": {
            "raw_export_asset_id": 101,
            "envelope_asset_id": 102,
            "verifier_report_asset_id": 103,
            "release_asset_index_asset_id": 104,
        },
    }
    dump(results / "1.json", result)
    release = root / "release.json"
    dump(
        release,
        {"id": 77, "tag_name": "v0.7.0-preview.1", "draft": False, "prerelease": True, "immutable": True},
    )
    return results, assets, release, result


def build(root: Path) -> dict[str, Any]:
    results, assets, release, _ = fixture(root)
    return build_summary(
        result_dir=results,
        asset_dir=assets,
        release_json=release,
        source_commit=SOURCE,
        repository=REPOSITORY,
        run_id=RUN_ID,
    )


def rejected(mutator: Callable[[Path, Path, Path, dict[str, Any]], None]) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        results, assets, release, result = fixture(root)
        mutator(results, assets, release, result)
        try:
            build_summary(
                result_dir=results,
                asset_dir=assets,
                release_json=release,
                source_commit=SOURCE,
                repository=REPOSITORY,
                run_id=RUN_ID,
            )
        except SummaryError:
            return
        raise AssertionError("mutation was accepted")


def rewrite_result(results: Path, result: dict[str, Any]) -> None:
    dump(results / "1.json", result)


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        summary = build(Path(temporary))
    assert summary["schema_version"] == "openai-preview-live-verifier-summary/v1"
    assert summary["run_id"] == RUN_ID
    assert summary["source_commit"] == SOURCE
    assert len(summary["bundles"]) == 1
    assert summary["bundles"][0]["evidence_type"] == "repository_preview_ci"
    assert set(summary["bundles"][0]) == {
        "evidence_type",
        "verdict",
        "provider_verified",
        "release_identity",
        "envelope_asset",
        "release_asset_index_asset",
        "raw_export_asset",
        "verifier_report_asset",
    }

    mutations: list[Callable[[Path, Path, Path, dict[str, Any]], None]] = [
        lambda results, _assets, _release, _result: (results / "1.json").unlink(),
        lambda results, _assets, _release, result: (
            result.__setitem__("provider_verified", True),
            rewrite_result(results, result),
        ),
        lambda results, _assets, _release, result: (
            result["live_verifier"].__setitem__("verifier_workflow_run_id", RUN_ID + 1),
            rewrite_result(results, result),
        ),
        lambda results, _assets, _release, result: (
            result["source_identity"].__setitem__("source_commit", "b" * 40),
            rewrite_result(results, result),
        ),
        lambda results, _assets, _release, result: (
            result["verified_assets"][1].__setitem__("evidence_kind", "raw_export"),
            rewrite_result(results, result),
        ),
        lambda results, _assets, _release, result: (
            result["verified_assets"].pop(),
            rewrite_result(results, result),
        ),
        lambda _results, assets, _release, _result: (assets / "raw.json").write_text(
            json.dumps({"observed": {}}), encoding="utf-8"
        ),
        lambda _results, assets, _release, _result: (assets / "index.json").write_bytes(
            b"tampered"
        ),
        lambda results, assets, _release, result: (
            (assets / "index.json").write_bytes(
                json.dumps(
                    {
                        "github_release": {
                            "repository": REPOSITORY,
                            "release_id": 999,
                            "release_tag": "old-release",
                        }
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ),
            result["verified_assets"][3].__setitem__(
                "sha256",
                "sha256:"
                + hashlib.sha256((assets / "index.json").read_bytes()).hexdigest(),
            ),
            rewrite_result(results, result),
        ),
        lambda results, _assets, _release, result: dump(
            results / "2.json", copy.deepcopy(result)
        ),
        lambda _results, _assets, release, _result: dump(
            release,
            {"id": 77, "tag_name": "v0.7.0-preview.1", "draft": True, "prerelease": True, "immutable": True},
        ),
    ]
    for mutation in mutations:
        rejected(mutation)
    print(f"OpenAI Preview verifier summary contracts passed: {len(mutations)} guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
