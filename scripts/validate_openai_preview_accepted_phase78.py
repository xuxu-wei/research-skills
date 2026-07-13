#!/usr/bin/env python3
"""Protected same-process bridge for complete Preview Phase 7 and Phase 8 reports."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from build_openai_preview_accepted_summary import strict_phase78_snapshot
from validate_openai_phase7_runtime_evidence import build_attested_phase7_result
import validate_openai_phase8_external_evidence as phase8_external
import validate_openai_preview_release as preview_release
from validate_openai_release_evidence import create_production_callback


SCHEMA = "openai-preview-accepted-phase78-run/v1"
SAFE_PATTERN_RE = re.compile(r"[A-Za-z0-9*?_.-]+")


class AcceptedPhase78Error(ValueError):
    pass


def load_identity(path: Path) -> dict[str, str]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AcceptedPhase78Error(f"expected source identity is not readable JSON: {exc}") from exc
    source = value.get("source_identity") if isinstance(value, Mapping) else None
    if not isinstance(source, Mapping):
        raise AcceptedPhase78Error("expected source identity has no source_identity object")
    return phase8_external._normalized_identity(source)


def digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def write_report(path: Path, report: Mapping[str, Any]) -> None:
    target = path.resolve()
    if not target.parent.is_dir() or target.parent.is_symlink():
        raise AcceptedPhase78Error(f"report output parent is invalid: {target.parent}")
    rendered = json.dumps(
        dict(report), ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    with tempfile.TemporaryDirectory(prefix="accepted-phase78-", dir=target.parent) as directory:
        temporary = Path(directory) / target.name
        temporary.write_text(rendered, encoding="utf-8", newline="\n")
        temporary.replace(target)


def _is_link_or_junction(path: Path) -> bool:
    try:
        is_junction = getattr(path, "is_junction", None)
        return path.is_symlink() or (
            callable(is_junction) and bool(is_junction())
        )
    except OSError as exc:
        raise AcceptedPhase78Error(f"cannot inspect evidence entry {path}: {exc}") from exc


def _flat_file_inventory(root: Path, label: str) -> dict[str, str]:
    """Hash one Release-asset directory and reject every non-plain entry."""

    if _is_link_or_junction(root):
        raise AcceptedPhase78Error(f"{label} must not be a link or junction")
    try:
        resolved = root.resolve(strict=True)
    except OSError as exc:
        raise AcceptedPhase78Error(f"{label} is unavailable: {exc}") from exc
    if not resolved.is_dir():
        raise AcceptedPhase78Error(f"{label} is not a directory")
    inventory: dict[str, str] = {}
    casefolded: set[str] = set()
    try:
        entries = sorted(resolved.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        raise AcceptedPhase78Error(f"{label} cannot be enumerated: {exc}") from exc
    for entry in entries:
        key = entry.name.casefold()
        if key in casefolded:
            raise AcceptedPhase78Error(f"{label} contains a case-colliding name")
        casefolded.add(key)
        if _is_link_or_junction(entry) or not entry.is_file():
            raise AcceptedPhase78Error(
                f"{label} contains a linked or non-file entry: {entry.name}"
            )
        try:
            payload = entry.read_bytes()
        except OSError as exc:
            raise AcceptedPhase78Error(
                f"{label} entry is unreadable: {entry.name}: {exc}"
            ) from exc
        inventory[entry.name] = "sha256:" + hashlib.sha256(payload).hexdigest()
    return inventory


def materialize_evidence_subset(
    *,
    source_root: Path,
    destination_root: Path,
    asset_index_pattern: str,
    expected_index_count: int,
) -> dict[str, str]:
    """Copy only selected indexes and their declared assets into one clean root."""

    if _is_link_or_junction(source_root):
        raise AcceptedPhase78Error("evidence subset source is linked")
    source = source_root.resolve(strict=True)
    destination = destination_root.resolve()
    if (
        not source.is_dir()
        or destination.exists()
        or not isinstance(asset_index_pattern, str)
        or SAFE_PATTERN_RE.fullmatch(asset_index_pattern) is None
        or ".." in asset_index_pattern
    ):
        raise AcceptedPhase78Error("evidence subset source, destination, or pattern is unsafe")
    source_inventory = _flat_file_inventory(source, "evidence subset source")
    indexes = sorted(
        path
        for path in source.glob(asset_index_pattern)
        if path.is_file() and not path.is_symlink() and path.parent == source
    )
    if len(indexes) != expected_index_count:
        raise AcceptedPhase78Error(
            f"evidence subset expected {expected_index_count} indexes, found {len(indexes)}"
        )
    selected: dict[str, str] = {}
    referenced_by: dict[str, str] = {}
    for index_path in indexes:
        try:
            document = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise AcceptedPhase78Error(
                f"asset index is not readable JSON: {index_path.name}: {exc}"
            ) from exc
        assets = document.get("assets") if isinstance(document, Mapping) else None
        if not isinstance(assets, list) or not assets:
            raise AcceptedPhase78Error(f"asset index has no assets: {index_path.name}")
        index_digest = source_inventory[index_path.name]
        if index_path.name in selected:
            raise AcceptedPhase78Error(f"asset index name is repeated: {index_path.name}")
        selected[index_path.name] = index_digest
        for offset, asset in enumerate(assets):
            name = asset.get("name") if isinstance(asset, Mapping) else None
            if (
                not isinstance(name, str)
                or not name
                or Path(name).name != name
                or "/" in name
                or "\\" in name
                or name == index_path.name
            ):
                raise AcceptedPhase78Error(
                    f"asset index contains an unsafe asset name: {index_path.name}[{offset}]"
                )
            if name in referenced_by:
                raise AcceptedPhase78Error(
                    f"physical evidence asset is reused by two indexes: {name}"
                )
            asset_path = source / name
            if not asset_path.is_file() or asset_path.is_symlink():
                raise AcceptedPhase78Error(
                    f"asset index references a missing or linked asset: {name}"
                )
            referenced_by[name] = index_path.name
            selected[name] = source_inventory[name]
    destination.mkdir(parents=False, exist_ok=False)
    for name, expected_digest in selected.items():
        payload = (source / name).read_bytes()
        if "sha256:" + hashlib.sha256(payload).hexdigest() != expected_digest:
            raise AcceptedPhase78Error(f"source evidence changed during subset copy: {name}")
        target = destination / name
        target.write_bytes(payload)
    copied = _flat_file_inventory(destination, "materialized evidence subset")
    if copied != selected:
        raise AcceptedPhase78Error("materialized evidence subset inventory differs from selection")
    return selected


def run(
    *,
    bundle_root: Path,
    evidence_root: Path,
    runtime_receipts: Path,
    reviewer_receipts: Path,
    retrieval_receipts: Path,
    expected_source_identity: Path,
    phase7_asset_index_pattern: str,
    phase8_asset_index_pattern: str,
    phase7_report_output: Path,
    phase8_report_output: Path,
) -> dict[str, Any]:
    collection_paths = {
        "phase7_runtime_receipts": runtime_receipts,
        "phase8_reviewer_receipts": reviewer_receipts,
        "phase8_retrieval_receipts": retrieval_receipts,
    }
    collection_digests = {
        role: "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        for role, path in collection_paths.items()
    }
    source_snapshot = _flat_file_inventory(
        evidence_root, "downloaded evidence root"
    )
    with tempfile.TemporaryDirectory(prefix="accepted-phase78-evidence-") as directory:
        temporary_root = Path(directory)
        phase7_root = temporary_root / "phase7"
        phase8_root = temporary_root / "phase8"
        phase7_subset = materialize_evidence_subset(
            source_root=evidence_root,
            destination_root=phase7_root,
            asset_index_pattern=phase7_asset_index_pattern,
            expected_index_count=10,
        )
        phase8_subset = materialize_evidence_subset(
            source_root=evidence_root,
            destination_root=phase8_root,
            asset_index_pattern=phase8_asset_index_pattern,
            expected_index_count=12,
        )
        overlap = set(phase7_subset) & set(phase8_subset)
        if overlap:
            raise AcceptedPhase78Error(
                f"Phase 7 and Phase 8 evidence subsets reuse physical assets: {sorted(overlap)}"
            )

        release_callback = create_production_callback(bundle_root)
        phase7_result = build_attested_phase7_result(
            evidence_root=phase7_root,
            runtime_receipts_path=runtime_receipts,
            expected_source_identity_path=expected_source_identity,
            asset_index_pattern=phase7_asset_index_pattern,
            live_release_evidence_verifier=release_callback,
        )
        phase7 = phase7_result.get("phase7_report")
        phase7_live_slots = phase7_result.get("live_slot_results")
        if not isinstance(phase7, Mapping) or not isinstance(
            phase7_live_slots, list
        ) or len(phase7_live_slots) != 10:
            raise AcceptedPhase78Error(
                "Phase 7 live bridge returned no complete in-session result"
            )

        verifier = phase8_external._load_phase8_verifier()
        identity = load_identity(expected_source_identity)
        phase8_result = phase8_external.validate_external_phase8_evidence(
            evidence_root=phase8_root,
            reviewer_receipts_path=reviewer_receipts,
            retrieval_receipts_path=retrieval_receipts,
            expected_source_identity_path=expected_source_identity,
            asset_index_pattern=phase8_asset_index_pattern,
            live_verifier=verifier.verify,
            request_builder=lambda *, bundle, identity: phase8_external._request_for_bundle(
                verifier, bundle, identity
            ),
            semantic_validator=phase8_external._default_semantic_validator,
        )
        for subset_root, expected in (
            (phase7_root, phase7_subset),
            (phase8_root, phase8_subset),
        ):
            after = _flat_file_inventory(
                subset_root, "materialized evidence subset after validation"
            )
            if after != expected:
                raise AcceptedPhase78Error("a materialized evidence subset changed during validation")
    source_after = _flat_file_inventory(
        evidence_root, "downloaded evidence root after validation"
    )
    if source_after != source_snapshot:
        raise AcceptedPhase78Error("the downloaded evidence root changed during validation")
    for role, path in collection_paths.items():
        if "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest() != collection_digests[role]:
            raise AcceptedPhase78Error(
                f"candidate receipt collection changed during live validation: {role}"
            )
    phase8 = phase8_result.get("phase8_report")
    if not isinstance(phase8, Mapping):
        raise AcceptedPhase78Error("Phase 8 live bridge returned no in-session report")
    strict = strict_phase78_snapshot(phase7, phase8)
    write_report(phase7_report_output, phase7)
    write_report(phase8_report_output, phase8)
    release_validation_output = io.StringIO()
    with contextlib.redirect_stdout(release_validation_output):
        release_validation_code = preview_release.main(
            [
                "--bundle-root",
                str(bundle_root),
                "--require-phase78-complete-preview",
            ],
            _accepted_phase78_reports=(phase7, phase8),
        )
    if release_validation_code != 0:
        raise AcceptedPhase78Error(
            "complete Preview validator rejected the same-process live reports"
        )
    live_slots = phase8_result.get("live_slot_results")
    if not isinstance(live_slots, list) or len(live_slots) != 12:
        raise AcceptedPhase78Error("Phase 8 live bridge did not bind twelve slot results")
    return {
        "schema_version": SCHEMA,
        "accepted": True,
        "verification_level": "preview_attested",
        "provider_verified": False,
        "candidate_collection_digests": collection_digests,
        "complete_preview_release_validator": "passed_with_fresh_callback",
        "complete_preview_release_validator_output_sha256": "sha256:"
        + hashlib.sha256(
            release_validation_output.getvalue().encode("utf-8")
        ).hexdigest(),
        "phase7": {
            "phase_status": strict["phase7"]["phase_status"],
            "report_sha256": digest(phase7),
            "runtime_results": strict["phase7"]["items"],
            "live_slot_results": phase7_live_slots,
            "completion_gate_count": 13,
        },
        "phase8": {
            "phase_status": strict["phase8"]["phase_status"],
            "report_sha256": digest(phase8),
            "live_slot_results": live_slots,
            "reviewer_results": strict["phase8"]["reviewer_items"],
            "retrieval_results": strict["phase8"]["retrieval_items"],
        },
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--bundle-root", required=True)
    value.add_argument("--evidence-root", required=True)
    value.add_argument("--runtime-receipts", required=True)
    value.add_argument("--reviewer-receipts", required=True)
    value.add_argument("--retrieval-receipts", required=True)
    value.add_argument("--expected-source-identity", required=True)
    value.add_argument("--phase7-asset-index-pattern", required=True)
    value.add_argument("--phase8-asset-index-pattern", required=True)
    value.add_argument("--phase7-report-output", required=True)
    value.add_argument("--phase8-report-output", required=True)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        output = run(
            bundle_root=Path(args.bundle_root),
            evidence_root=Path(args.evidence_root),
            runtime_receipts=Path(args.runtime_receipts),
            reviewer_receipts=Path(args.reviewer_receipts),
            retrieval_receipts=Path(args.retrieval_receipts),
            expected_source_identity=Path(args.expected_source_identity),
            phase7_asset_index_pattern=args.phase7_asset_index_pattern,
            phase8_asset_index_pattern=args.phase8_asset_index_pattern,
            phase7_report_output=Path(args.phase7_report_output),
            phase8_report_output=Path(args.phase8_report_output),
        )
        code = 0
    except Exception as exc:
        output = {
            "schema_version": SCHEMA,
            "accepted": False,
            "error": {
                "code": "accepted_phase78_failed",
                "message": f"{type(exc).__name__}: {exc}",
            },
        }
        code = 1
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
