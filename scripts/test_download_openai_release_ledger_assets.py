#!/usr/bin/env python3
"""Contract tests for accepted historical release discovery."""

from __future__ import annotations

import copy

from download_openai_release_ledger_assets import DownloadError, accepted_release_pairs


REPOSITORY = "owner/repository"


def record(tag: str, status: str = "preview_attested") -> dict:
    return {
        "status": status,
        "evidence_locator": {"repository": REPOSITORY, "release_tag": tag},
    }


def release(tag: str, status: str = "preview_attested") -> dict:
    return {
        "ci": {
            "repository_preview": record(tag, status),
            "canonical_plugin_validator": {"ci": record(tag, status)},
        },
        "governance": {"main_branch_protection": record(tag, status)},
        "marketplace_source": {"resolved_commit": record(tag, status)},
        "receipts": {
            "marketplace_upgrade": record(tag, status),
            "explicit_reinstall": record(tag, status),
            "fresh_task_discovery": record(tag, status),
            "rollback": record(tag, status),
        },
    }


def rejected(ledger: dict, code: str) -> None:
    try:
        accepted_release_pairs(
            ledger,
            current_repository=REPOSITORY,
            current_release_tag="v2",
        )
    except DownloadError:
        return
    raise AssertionError(f"mutation accepted: {code}")


def main() -> int:
    ledger = {
        "release": release("v2"),
        "previous_releases": [release("v1"), release("v0", "pending")],
    }
    assert accepted_release_pairs(
        ledger,
        current_repository=REPOSITORY,
        current_release_tag="v2",
    ) == [(REPOSITORY, "v1")]
    outside = copy.deepcopy(ledger)
    outside["previous_releases"][0]["ci"]["repository_preview"]["evidence_locator"][
        "repository"
    ] = "other/repository"
    rejected(outside, "cross_repository")
    unsafe = copy.deepcopy(ledger)
    unsafe["previous_releases"][0]["ci"]["repository_preview"]["evidence_locator"][
        "release_tag"
    ] = "../v1"
    rejected(unsafe, "unsafe_tag")
    missing = copy.deepcopy(ledger)
    missing["previous_releases"][0]["ci"]["repository_preview"].pop(
        "evidence_locator"
    )
    rejected(missing, "missing_locator")
    rejected({"release": release("v2"), "previous_releases": {}}, "history_not_list")
    print("Historical release asset discovery contracts passed: 4 guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
