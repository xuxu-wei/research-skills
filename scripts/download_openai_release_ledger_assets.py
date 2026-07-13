#!/usr/bin/env python3
"""Download accepted historical ledger releases into isolated bundle directories."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence


ACCEPTED = {"preview_attested", "provider_verified"}
REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
TAG_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


class DownloadError(ValueError):
    pass


def external_records(release: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    ci = release.get("ci", {})
    governance = release.get("governance", {})
    marketplace = release.get("marketplace_source", {})
    receipts = release.get("receipts", {})
    values = [
        ci.get("repository_preview") if isinstance(ci, Mapping) else None,
        (
            ci.get("canonical_plugin_validator", {}).get("ci")
            if isinstance(ci, Mapping)
            and isinstance(ci.get("canonical_plugin_validator"), Mapping)
            else None
        ),
        governance.get("main_branch_protection") if isinstance(governance, Mapping) else None,
        marketplace.get("resolved_commit") if isinstance(marketplace, Mapping) else None,
        receipts.get("marketplace_upgrade") if isinstance(receipts, Mapping) else None,
        receipts.get("explicit_reinstall") if isinstance(receipts, Mapping) else None,
        receipts.get("fresh_task_discovery") if isinstance(receipts, Mapping) else None,
        receipts.get("rollback") if isinstance(receipts, Mapping) else None,
    ]
    return [value for value in values if isinstance(value, Mapping)]


def accepted_release_pairs(
    ledger: Mapping[str, Any], *, current_repository: str, current_release_tag: str
) -> list[tuple[str, str]]:
    if REPOSITORY_RE.fullmatch(current_repository) is None:
        raise DownloadError("current repository must be owner/name")
    if TAG_RE.fullmatch(current_release_tag) is None or ".." in current_release_tag:
        raise DownloadError("current release tag is unsafe")
    releases: list[Mapping[str, Any]] = []
    current = ledger.get("release")
    if isinstance(current, Mapping):
        releases.append(current)
    previous = ledger.get("previous_releases", [])
    if not isinstance(previous, list):
        raise DownloadError("previous_releases must be a list")
    releases.extend(value for value in previous if isinstance(value, Mapping))

    pairs: set[tuple[str, str]] = set()
    for release in releases:
        for record in external_records(release):
            if record.get("status") not in ACCEPTED:
                continue
            locator = record.get("evidence_locator")
            if not isinstance(locator, Mapping):
                raise DownloadError("accepted record has no evidence locator")
            repository = locator.get("repository")
            tag = locator.get("release_tag")
            if repository != current_repository:
                raise DownloadError("accepted history points outside the current repository")
            if not isinstance(tag, str) or TAG_RE.fullmatch(tag) is None or ".." in tag:
                raise DownloadError("accepted history contains an unsafe release tag")
            pairs.add((repository, tag))
    pairs.discard((current_repository, current_release_tag))
    return sorted(pairs)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise DownloadError(f"ledger is not readable JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise DownloadError("ledger must be an object")
    return value


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--ledger", required=True)
    value.add_argument("--bundle-root", required=True)
    value.add_argument("--current-repository", required=True)
    value.add_argument("--current-release-tag", required=True)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        if not os.environ.get("GH_TOKEN"):
            raise DownloadError("GH_TOKEN is required")
        ledger = load(Path(args.ledger))
        root = Path(args.bundle_root).resolve(strict=True)
        pairs = accepted_release_pairs(
            ledger,
            current_repository=args.current_repository,
            current_release_tag=args.current_release_tag,
        )
        downloaded = []
        for offset, (repository, tag) in enumerate(pairs, start=1):
            target = root / f"accepted-history-{offset:03d}"
            target.mkdir()
            subprocess.run(
                [
                    "gh",
                    "release",
                    "download",
                    tag,
                    "--repo",
                    repository,
                    "--dir",
                    str(target),
                ],
                check=True,
            )
            if not any(path.is_file() for path in target.iterdir()):
                raise DownloadError(f"historical release {tag} downloaded no assets")
            downloaded.append({"repository": repository, "release_tag": tag, "directory": target.name})
        print(json.dumps({"downloaded": downloaded}, sort_keys=True))
    except (DownloadError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Historical release asset download failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
