#!/usr/bin/env python3
"""Focused tests for trusted Phase 7/8 evidence-root materialization."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Callable

from validate_openai_preview_accepted_phase78 import (
    AcceptedPhase78Error,
    materialize_evidence_subset,
)


def write_bundle(root: Path, prefix: str, asset_name: str | None = None) -> None:
    name = asset_name or f"{prefix}-raw.json"
    (root / name).write_text(f"payload:{prefix}", encoding="utf-8")
    (root / f"{prefix}-index.json").write_text(
        json.dumps({"assets": [{"name": name}]}), encoding="utf-8"
    )


def valid(root: Path) -> None:
    write_bundle(root, "p7-a")
    write_bundle(root, "p7-b")
    (root / "unselected.json").write_text("ignored", encoding="utf-8")


def rejected(mutator: Callable[[Path], tuple[str, int]]) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        source = base / "source"
        source.mkdir()
        valid(source)
        pattern, expected = mutator(source)
        try:
            materialize_evidence_subset(
                source_root=source,
                destination_root=base / "subset",
                asset_index_pattern=pattern,
                expected_index_count=expected,
            )
        except AcceptedPhase78Error:
            return
        raise AssertionError("invalid evidence subset was materialized")


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        source = base / "source"
        source.mkdir()
        valid(source)
        inventory = materialize_evidence_subset(
            source_root=source,
            destination_root=base / "subset",
            asset_index_pattern="p7-*-index.json",
            expected_index_count=2,
        )
        assert set(inventory) == {
            "p7-a-index.json",
            "p7-a-raw.json",
            "p7-b-index.json",
            "p7-b-raw.json",
        }
        assert not (base / "subset" / "unselected.json").exists()

    mutations: list[Callable[[Path], tuple[str, int]]] = [
        lambda _root: ("../*.json", 2),
        lambda _root: ("p7/*.json", 2),
        lambda _root: ("p7-*-index.json", 3),
        lambda root: (
            (root / "p7-a-raw.json").unlink() or "p7-*-index.json",
            2,
        ),
        lambda root: (
            ((root / "p7-a-index.json").write_text("[]", encoding="utf-8"), "p7-*-index.json")[1],
            2,
        ),
        lambda root: (
            (
                (root / "p7-a-index.json").write_text(
                    json.dumps({"assets": [{"name": "../escape.json"}]}),
                    encoding="utf-8",
                ),
                "p7-*-index.json",
            )[1],
            2,
        ),
        lambda root: (
            (
                (root / "p7-b-index.json").write_text(
                    json.dumps({"assets": [{"name": "p7-a-raw.json"}]}),
                    encoding="utf-8",
                ),
                "p7-*-index.json",
            )[1],
            2,
        ),
        lambda root: (
            (
                (root / "p7-a-index.json").write_text(
                    json.dumps({"assets": [{"name": "p7-a-index.json"}]}),
                    encoding="utf-8",
                ),
                "p7-*-index.json",
            )[1],
            2,
        ),
        lambda root: (
            (root / "unexpected-directory").mkdir() or "p7-*-index.json",
            2,
        ),
    ]
    for mutation in mutations:
        rejected(mutation)
    guard_count = len(mutations)
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        source = base / "source"
        source.mkdir()
        valid(source)
        link = source / "linked-asset.json"
        try:
            link.symlink_to(source / "p7-a-raw.json")
        except OSError:
            pass
        else:
            try:
                materialize_evidence_subset(
                    source_root=source,
                    destination_root=base / "subset",
                    asset_index_pattern="p7-*-index.json",
                    expected_index_count=2,
                )
            except AcceptedPhase78Error:
                guard_count += 1
            else:
                raise AssertionError("linked evidence entry was accepted")
    print(f"OpenAI Preview accepted Phase 7/8 subset guards passed: {guard_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
