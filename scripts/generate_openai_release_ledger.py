#!/usr/bin/env python3
"""Generate the derived fields of the OpenAI plugin release ledger.

External receipts are deliberately never inferred. They are preserved only
while the full installable identity remains unchanged: version, manifest,
registry/schema, license, provenance, skill tree, and marketplace source.
Otherwise they reset to explicit pending records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
LEDGER_PATH = PLUGIN / "reports" / "release-ledger.json"
MANIFEST_PATH = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = REPO / ".agents" / "plugins" / "marketplace.json"
SKILL_TREE_ALGORITHM = "sha256_sorted_posix_relative_path_nul_crlf_normalized_bytes_nul"
VALIDATION_TREE_ALGORITHM = (
    "sha256_sorted_repository_relative_path_nul_crlf_normalized_bytes_nul"
)
VALIDATION_TEST_ROOTS = (
    "tests/openai_phase4",
    "tests/openai_phase6",
    "tests/openai_phase7",
    "tests/openai_phase8",
)
VALIDATION_CONTRACT_FILES = (
    ".gitattributes",
    ".gitignore",
    ".github/workflows/openai-plugin-preview.yml",
    ".github/workflows/openai-preview-accepted-evidence.yml",
    ".github/workflows/openai-preview-accepted-summary-consumer.yml",
    ".github/workflows/openai-preview-evidence.yml",
    "codex-plugin-validation.json",
)
MUTABLE_RUNTIME_EVIDENCE_FILES = {
    "tests/openai_phase7/current-version-runtime-receipts.yaml",
    "tests/openai_phase8/live-repeat-receipts.yaml",
    "tests/openai_phase8/retrieval-receipts.yaml",
}
MUTABLE_RUNTIME_EVIDENCE_PREFIXES = (
    "tests/openai_phase7/runtime-evidence/",
    "tests/openai_phase8/retrieval-artifacts/",
    "tests/openai_phase8/runtime-evidence/",
)
VALIDATION_RUNTIME_CACHE_DIRS = {"__pycache__"}
VALIDATION_RUNTIME_CACHE_SUFFIXES = {".pyc", ".pyd", ".pyo"}


def is_validation_runtime_cache(path: Path, repository: Path = REPO) -> bool:
    relative = path.relative_to(repository)
    return (
        any(part in VALIDATION_RUNTIME_CACHE_DIRS for part in relative.parts)
        or path.suffix.lower() in VALIDATION_RUNTIME_CACHE_SUFFIXES
    )


def _git_file_listing(repository: Path, *arguments: str) -> list[bytes]:
    process = subprocess.run(
        ["git", "ls-files", *arguments],
        cwd=repository,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"cannot enumerate release-ledger sources: {detail}")
    return [item for item in process.stdout.split(b"\0") if item]


def _has_symlink_component(path: Path, repository: Path) -> bool:
    current = repository
    for part in path.relative_to(repository).parts:
        current /= part
        if current.is_symlink():
            return True
    return False


def _decode_tracked_record(record: bytes) -> tuple[bytes, bytes, str]:
    metadata, separator, raw_path = record.partition(b"\t")
    fields = metadata.split()
    if not separator or len(fields) != 3:
        raise RuntimeError("malformed tracked release-ledger source record")
    mode, _, stage = fields
    return mode, stage, raw_path.decode("utf-8")


def _require_regular_tracked_record(mode: bytes, stage: bytes, relative: str) -> None:
    if mode not in {b"100644", b"100755"}:
        raise RuntimeError(
            f"tracked non-regular release-ledger source is forbidden: {relative}"
        )
    if stage != b"0":
        raise RuntimeError(f"unmerged release-ledger source is forbidden: {relative}")


def _validate_worktree_file(
    path: Path,
    declared_root: Path,
    repository: Path,
    relative: str,
) -> Path:
    if _has_symlink_component(path, repository):
        raise RuntimeError(f"symlink release-ledger source is forbidden: {relative}")
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(declared_root)
    except (FileNotFoundError, ValueError) as exc:
        raise RuntimeError(
            f"release-ledger source escapes its declared root: {relative}"
        ) from exc
    if not path.is_file():
        raise RuntimeError(f"non-file release-ledger source is forbidden: {relative}")
    return path


def tracked_repository_file(
    path: Path,
    repository: Path = REPO,
    declared_root: Path | None = None,
) -> Path:
    """Return one tracked regular file without following repository symlinks."""

    repository = repository.resolve(strict=True)
    path = path.absolute()
    declared_root = (declared_root or repository).absolute()
    try:
        relative = path.relative_to(repository).as_posix()
        root_relative = declared_root.relative_to(repository)
    except ValueError as exc:
        raise RuntimeError(f"release-ledger file escapes repository: {path}") from exc
    if _has_symlink_component(declared_root, repository):
        raise RuntimeError(f"symlink release-ledger root is forbidden: {root_relative.as_posix()}")
    try:
        resolved_root = declared_root.resolve(strict=True)
        resolved_root.relative_to(repository)
    except (FileNotFoundError, ValueError) as exc:
        raise RuntimeError(
            f"release-ledger root escapes repository: {declared_root}"
        ) from exc
    records = _git_file_listing(
        repository,
        "--cached",
        "--stage",
        "-z",
        "--",
        relative,
    )
    if len(records) != 1:
        raise RuntimeError(f"release-ledger source is not uniquely tracked: {relative}")
    mode, stage, tracked_relative = _decode_tracked_record(records[0])
    if tracked_relative != relative:
        raise RuntimeError(f"Git returned an out-of-scope source: {tracked_relative}")
    _require_regular_tracked_record(mode, stage, relative)
    if is_validation_runtime_cache(path, repository):
        raise RuntimeError(
            f"tracked runtime cache is forbidden in release identity: {relative}"
        )
    return _validate_worktree_file(
        path,
        resolved_root,
        repository,
        relative,
    )


def repository_candidate_files(
    root: Path,
    repository: Path = REPO,
) -> list[Path]:
    """Return tracked and non-ignored new files under a repository root."""

    root = root.absolute()
    repository = repository.resolve(strict=True)
    try:
        root_relative = root.relative_to(repository).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"release-ledger root escapes repository: {root}") from exc
    if _has_symlink_component(root, repository):
        raise RuntimeError(f"symlink release-ledger root is forbidden: {root_relative}")
    try:
        resolved_root = root.resolve(strict=True)
        resolved_root.relative_to(repository)
    except (FileNotFoundError, ValueError) as exc:
        raise RuntimeError(f"release-ledger root escapes repository: {root}") from exc
    if not root.is_dir():
        raise RuntimeError(f"release-ledger root is not a directory: {root_relative}")
    tracked_records = _git_file_listing(
        repository,
        "--cached",
        "--stage",
        "-z",
        "--",
        root_relative,
    )
    untracked_records = _git_file_listing(
        repository,
        "--others",
        "--exclude-per-directory=.gitignore",
        "-z",
        "--",
        root_relative,
    )
    prefix = f"{root_relative}/"
    candidates: dict[str, tuple[Path, bool]] = {}
    for record in tracked_records:
        mode, stage, relative = _decode_tracked_record(record)
        _require_regular_tracked_record(mode, stage, relative)
        if relative != root_relative and not relative.startswith(prefix):
            raise RuntimeError(f"Git returned an out-of-scope source: {relative}")
        path = repository / Path(relative)
        if is_validation_runtime_cache(path, repository):
            raise RuntimeError(
                f"tracked runtime cache is forbidden in release identity: {relative}"
            )
        candidates[relative] = (path, True)
    for record in untracked_records:
        relative = record.decode("utf-8")
        if relative != root_relative and not relative.startswith(prefix):
            raise RuntimeError(f"Git returned an out-of-scope source: {relative}")
        path = repository / Path(relative)
        if not is_validation_runtime_cache(path, repository):
            candidates.setdefault(relative, (path, False))

    paths: list[Path] = []
    for relative, (path, tracked) in sorted(candidates.items()):
        if not path.exists():
            if tracked:
                continue
            raise RuntimeError(f"untracked release-ledger source disappeared: {relative}")
        paths.append(
            _validate_worktree_file(
                path,
                resolved_root,
                repository,
                relative,
            )
        )
    return paths


def normalized_skill_tree_digest(root: Path) -> tuple[int, str]:
    root = root.absolute()
    digest = hashlib.sha256()
    files = repository_candidate_files(root)
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return len(files), digest.hexdigest()


def normalized_file_digest(path: Path) -> str:
    path = tracked_repository_file(path)
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validation_contract_paths() -> list[Path]:
    scripts_root = REPO / "scripts"
    paths = [
        path
        for path in repository_candidate_files(scripts_root)
        if path.parent == scripts_root and path.suffix == ".py"
    ]
    for root in VALIDATION_TEST_ROOTS:
        paths.extend(repository_candidate_files(REPO / root))
    paths.extend(
        tracked_repository_file(REPO / path)
        for path in VALIDATION_CONTRACT_FILES
    )
    return sorted(
        (
            path
            for path in set(paths)
            if (
                path.relative_to(REPO).as_posix()
                not in MUTABLE_RUNTIME_EVIDENCE_FILES
                and not any(
                    path.relative_to(REPO).as_posix().startswith(prefix)
                    for prefix in MUTABLE_RUNTIME_EVIDENCE_PREFIXES
                )
            )
        ),
        key=lambda path: path.relative_to(REPO).as_posix(),
    )


def normalized_validation_contract_digest() -> tuple[int, str]:
    digest = hashlib.sha256()
    paths = validation_contract_paths()
    for path in paths:
        digest.update(path.relative_to(REPO).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return len(paths), digest.hexdigest()


def pending(reason: str, **fields: Any) -> dict[str, Any]:
    return {"status": "pending", **fields, "reason": reason}


def merge_evidence_defaults(default: Any, existing: Any) -> Any:
    """Preserve recorded evidence while adding newly introduced schema fields."""
    if not isinstance(default, dict) or not isinstance(existing, dict):
        return existing
    merged = dict(default)
    for key, value in existing.items():
        merged[key] = (
            merge_evidence_defaults(default.get(key), value)
            if key in default
            else value
        )
    return merged


def default_external_evidence(version: str) -> dict[str, Any]:
    release_reason = "The candidate has not yet been bound to an immutable pushed commit."
    receipt_reason = "A current-version external receipt has not yet been captured."
    return {
        "external_evidence_trust": {
            "adapter_status": "unavailable",
            "adapter_id": None,
            "verification_level": None,
            "provider_authenticated": False,
            "reason": (
                "No registered live external verifier has re-queried a GitHub "
                "Release evidence bundle for this release. Repository files, "
                "status text, screenshots, and manual notes do not establish "
                "Preview acceptance."
            ),
        },
        "source_commit": pending(release_reason, sha=None),
        "ci": {
            "repository_preview": pending(
                "A successful GitHub Actions run bound to the release commit is not yet recorded.",
                workflow_file=".github/workflows/openai-plugin-preview.yml",
                run_id=None,
                run_url=None,
                commit_sha=None,
                conclusion=None,
                evidence_locator=None,
            ),
            "canonical_plugin_validator": {
                "local": pending(
                    "The bundled canonical validator has not yet been recorded for this tree.",
                    command=(
                        "python C:/Users/10149/.codex/skills/.system/plugin-creator/"
                        "scripts/validate_plugin.py research-skills-openai"
                    ),
                    validator_source="Codex bundled plugin-creator skill",
                    result=None,
                    verified_on=None,
                ),
                "ci": pending(
                    "No stable public canonical-validator CI entry point is available; "
                    "the bundled system validator is not vendored into this repository.",
                    run_id=None,
                    commit_sha=None,
                    conclusion=None,
                    evidence_locator=None,
                ),
            },
        },
        "governance": {
            "main_branch_protection": pending(
                "Repository branch protection and the required Preview check have not been verified through an authenticated repository API.",
                branch="main",
                required_check="OpenAI Plugin Preview / validate",
                verified_at=None,
                evidence_locator=None,
            ),
        },
        "marketplace_resolved_commit": pending(
            "The rolling marketplace ref has not yet been resolved and bound to this release.",
            sha=None,
            evidence_locator=None,
        ),
        "receipts": {
            "marketplace_upgrade": pending(
                receipt_reason,
                installed_version=None,
                source_commit=None,
                cache_path=None,
                cache_artifact=None,
                evidence_locator=None,
            ),
            "explicit_reinstall": pending(
                receipt_reason,
                installed_version=None,
                source_commit=None,
                cache_path=None,
                cache_artifact=None,
                evidence_locator=None,
            ),
            "fresh_task_discovery": pending(
                receipt_reason,
                plugin_version=None,
                source_commit=None,
                task_id=None,
                installed_skill_count=None,
                explicit_callable_entries=None,
                implicit_prompt_entries=None,
                explicit_callable_entry_skills=None,
                implicit_prompt_entry_skills=None,
                installed_via=None,
                cache_artifact=None,
                evidence_locator=None,
            ),
            "rollback": pending(
                "Rollback evidence must be captured against the previous artifact and an immutable commit.",
                from_version=version,
                to_version=None,
                target_commit=None,
                restored_cache_path=None,
                candidate_cache_path=None,
                candidate_from_receipt=None,
                candidate_cache_artifact=None,
                restored_cache_artifact=None,
                cache_mixing_absent=None,
                evidence_locator=None,
            ),
        },
    }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def marketplace_source() -> dict[str, Any]:
    marketplace = read_json(MARKETPLACE_PATH)
    matches = [
        item for item in marketplace.get("plugins", [])
        if item.get("name") == "research-skills-openai"
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one research-skills-openai marketplace entry, found {len(matches)}")
    source = matches[0].get("source")
    if not isinstance(source, dict):
        raise ValueError("marketplace entry has no source mapping")
    return {
        "marketplace_name": marketplace.get("name"),
        "source": source.get("source"),
        "url": source.get("url"),
        "path": source.get("path"),
        "ref": source.get("ref"),
    }


def evidence_identity(release: dict[str, Any]) -> tuple[Any, ...]:
    tree = release.get("installable_skill_tree", {})
    contracts = release.get("installable_contracts", {})
    validation = release.get("validation_contract_tree", {})
    source = release.get("marketplace_source", {})
    return (
        release.get("version"),
        tree.get("sha256"),
        contracts.get("manifest_sha256"),
        contracts.get("registry_sha256"),
        contracts.get("registry_schema_version"),
        contracts.get("license_sha256"),
        contracts.get("provenance_sha256"),
        validation.get("algorithm"),
        validation.get("file_count"),
        validation.get("sha256"),
        source.get("marketplace_name"),
        source.get("source"),
        source.get("url"),
        source.get("path"),
        source.get("ref"),
    )


def build_ledger(existing: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest = read_json(MANIFEST_PATH)
    registry_path = PLUGIN / "workflow-registry.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    version = str(manifest.get("version", ""))
    file_count, digest = normalized_skill_tree_digest(PLUGIN / "skills")
    validation_file_count, validation_digest = normalized_validation_contract_digest()
    external = default_external_evidence(version)
    derived_release: dict[str, Any] = {
        "version": version,
        "external_evidence_trust": external["external_evidence_trust"],
        "source_commit": external["source_commit"],
        "installable_skill_tree": {
            "root": "skills/",
            "algorithm": SKILL_TREE_ALGORITHM,
            "file_count": file_count,
            "sha256": digest,
        },
        "installable_contracts": {
            "manifest_sha256": normalized_file_digest(MANIFEST_PATH),
            "registry_sha256": normalized_file_digest(registry_path),
            "registry_schema_version": registry.get("schema_version"),
            "license_sha256": normalized_file_digest(PLUGIN / "LICENSE"),
            "provenance_sha256": normalized_file_digest(PLUGIN / "PROVENANCE.yaml"),
        },
        "validation_contract_tree": {
            "algorithm": VALIDATION_TREE_ALGORITHM,
            "file_count": validation_file_count,
            "sha256": validation_digest,
            "mutable_runtime_evidence_excluded": [
                *sorted(MUTABLE_RUNTIME_EVIDENCE_FILES),
                *sorted(f"{prefix}**" for prefix in MUTABLE_RUNTIME_EVIDENCE_PREFIXES),
            ],
        },
        "ci": external["ci"],
        "governance": external["governance"],
        "marketplace_source": {
            **marketplace_source(),
            "resolved_commit": external["marketplace_resolved_commit"],
        },
        "receipts": external["receipts"],
    }

    previous_releases: list[dict[str, Any]] = []
    if isinstance(existing, dict):
        prior_history = existing.get("previous_releases", [])
        if isinstance(prior_history, list):
            previous_releases = prior_history
        prior_release = existing.get("release")
        if isinstance(prior_release, dict):
            if evidence_identity(prior_release) == evidence_identity(derived_release):
                for key in (
                    "external_evidence_trust",
                    "source_commit",
                    "ci",
                    "governance",
                    "receipts",
                ):
                    if key in prior_release:
                        derived_release[key] = merge_evidence_defaults(
                            derived_release[key], prior_release[key]
                        )
                resolved = prior_release.get("marketplace_source", {}).get("resolved_commit")
                if isinstance(resolved, dict):
                    derived_release["marketplace_source"]["resolved_commit"] = (
                        merge_evidence_defaults(
                            derived_release["marketplace_source"]["resolved_commit"],
                            resolved,
                        )
                    )
            elif prior_release.get("source_commit", {}).get("status") == "verified":
                old_identity = evidence_identity(prior_release)
                history_identities = {evidence_identity(item) for item in previous_releases}
                if old_identity not in history_identities:
                    previous_releases = [*previous_releases, prior_release]

    return {
        "schema_version": 1,
        "plugin": "research-skills-openai",
        "external_evidence_schema": "tests/openai_phase7/release-evidence.schema.yaml",
        "evidence_policy": (
            "Derived fields come from the current tree. External evidence is preserved only "
            "for an unchanged version, manifest, registry/schema, license, provenance, "
            "skill-tree digest, validation-contract tree, and marketplace source. Accepted "
            "external records store only immutable GitHub Release/run/asset locators and "
            "digests, and require a registered verifier to live re-query those external assets. "
            "Shared bundle validation proves integrity only and never determines gate eligibility. "
            "preview_attested is explicitly not verified or provider_verified. provider_verified "
            "is unavailable until a separately registered authenticated provider adapter exists. "
            "Repository files, status text, screenshots, and manual notes never suffice. "
            "Unobserved evidence remains pending."
        ),
        "release": derived_release,
        "previous_releases": previous_releases,
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed ledger is stale")
    args = parser.parse_args()
    existing = read_json(LEDGER_PATH) if LEDGER_PATH.is_file() else None
    expected = build_ledger(existing)
    expected_text = render(expected)
    if args.check:
        if not LEDGER_PATH.is_file() or LEDGER_PATH.read_text(encoding="utf-8") != expected_text:
            print("OpenAI release ledger is stale; run scripts/generate_openai_release_ledger.py")
            return 1
        print("OpenAI release ledger is current")
        return 0
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(expected_text, encoding="utf-8", newline="\n")
    print(f"Wrote {LEDGER_PATH.relative_to(REPO).as_posix()}")
    print(f"version: {expected['release']['version']}")
    print(f"skill tree: {file_count_label(expected['release'])}")
    return 0


def file_count_label(release: dict[str, Any]) -> str:
    tree = release["installable_skill_tree"]
    return f"{tree['file_count']} files / {tree['sha256']}"


if __name__ == "__main__":
    raise SystemExit(main())
