#!/usr/bin/env python3
"""Normalize one real Codex App Server capture into a frozen R asset.

The normalizer accepts the three App Server capture files, the workflow's
machine-readable task export, and one scheduler-owned input binding.  It
verifies the exact launch prompt in the platform thread, the frozen source and
prompt bytes against the committed ten-slot manifest, and the current clean
plugin source identity before emitting a self-contained composite R asset.

The output remains ``capture_only``.  This script cannot authenticate OpenAI,
GitHub, a user, or an independent reviewer, and it never promotes a gate.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml

from capture_openai_codex_app_server import redact
from openai_preview_evidence import normalize_sha256, sha256_bytes
from validate_openai_phase7_runtime_evidence import current_checkout_source_identity


REPO = Path(__file__).resolve().parents[1]
CAPTURE_HELPER = REPO / "scripts" / "capture_openai_codex_app_server.py"
NORMALIZED_CAPTURE_SCHEMA = "openai-preview-normalized-capture/v1"
CAPTURE_ADAPTER_ID = "codex_app_server_capture_normalizer_v1"
CAPTURE_SOURCE_FILES = ("capture.json", "transport.jsonl", "sha256sums.json")
SCHEDULER_SOURCE_FILE = "scheduler-frozen-source.md"
SCHEDULER_PROMPT_FILE = "scheduler-launch-prompt.md"
SOURCE_FILES = (
    *CAPTURE_SOURCE_FILES,
    "task-export.json",
    SCHEDULER_SOURCE_FILE,
    SCHEDULER_PROMPT_FILE,
)
SCHEDULER_MANIFEST_REPOSITORY_PATH = "tests/openai_phase7/live-inputs/manifest.yaml"
SCHEDULER_MANIFEST_SCHEMA = "phase7-scheduler-input-pack/v1"
SCHEDULER_INPUT_SCHEMA = "phase7-task-scheduler-input/v1"
SCHEDULER_BINDING_SCHEMA = "phase7-normalized-scheduler-binding/v1"
INSTALLABLE_PATHS = (
    "research-skills-openai/.codex-plugin/plugin.json",
    "research-skills-openai/workflow-registry.yaml",
    "research-skills-openai/skills",
)
FROZEN_CAPTURE_PATHS = (
    *INSTALLABLE_PATHS,
    SCHEDULER_MANIFEST_REPOSITORY_PATH,
    "tests/openai_phase7/live-inputs/sources",
    "tests/openai_phase7/live-inputs/prompts",
    "scripts/capture_openai_codex_app_server.py",
    "scripts/normalize_openai_preview_capture.py",
)
MAX_FUTURE_SKEW = timedelta(minutes=5)
MAX_EVIDENCE_AGE = timedelta(days=90)
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$")
HEX_64_RE = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{number}" for number in range(1, 10)}
    | {f"LPT{number}" for number in range(1, 10)}
)


class CaptureNormalizationError(ValueError):
    """Stable fail-closed normalization error."""

    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message
        super().__init__(f"{code} at {path}: {message}")


def _fail(code: str, path: str, message: str) -> None:
    raise CaptureNormalizationError(code, path, message)


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("invalid_type", path, "expected an object")
    return value


def _sequence(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        _fail("invalid_type", path, "expected an array")
    return value


def _string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("invalid_string", path, "expected a non-empty string")
    return value.strip()


def _identifier(value: Any, path: str) -> str:
    text = _string(value, path)
    if IDENTIFIER_RE.fullmatch(text) is None:
        _fail("invalid_identifier", path, "contains unsupported characters")
    return text


def _strict_json(payload: bytes, path: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _fail("duplicate_json_key", path, key)
            result[key] = value
        return result

    try:
        return json.loads(payload.decode("utf-8-sig"), object_pairs_hook=reject_duplicates)
    except CaptureNormalizationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail("invalid_json", path, str(exc))


def _timestamp(value: Any, path: str, *, now: datetime) -> str:
    text = _string(value, path)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        _fail("invalid_timestamp", path, "expected ISO-8601")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("invalid_timestamp", path, "UTC offset is required")
    parsed = parsed.astimezone(timezone.utc)
    if parsed > now + MAX_FUTURE_SKEW:
        _fail("timestamp_too_far_in_future", path, text)
    if parsed < now - MAX_EVIDENCE_AGE:
        _fail("stale_evidence_timestamp", path, text)
    return text


def parse_clock(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        _fail("invalid_timestamp", "cli.now", "expected ISO-8601")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("invalid_timestamp", "cli.now", "UTC offset is required")
    return parsed.astimezone(timezone.utc)


def canonical_json_bytes(document: Mapping[str, Any]) -> bytes:
    return (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _is_link_or_junction(path: Path) -> bool:
    try:
        is_junction = getattr(path, "is_junction", None)
        return path.is_symlink() or (callable(is_junction) and bool(is_junction()))
    except OSError as exc:
        _fail("path_unreadable", "staging_root", f"{path}: {exc}")


def canonical_relative(value: str, path: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        _fail("unsafe_relative_path", path, repr(value))
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
        or relative.as_posix() != value
    ):
        _fail("unsafe_relative_path", path, value)
    for part in relative.parts:
        stem = part.split(".", 1)[0].upper()
        if (
            part.endswith((" ", "."))
            or any(character in part for character in '<>"|?*')
            or stem in WINDOWS_RESERVED_NAMES
        ):
            _fail("nonportable_relative_path", path, value)
    return relative


class StagingRoot:
    """Resolve canonical, non-link paths beneath one explicit staging root."""

    def __init__(self, root: Path) -> None:
        try:
            resolved = root.resolve(strict=True)
        except OSError as exc:
            _fail("staging_root_unavailable", "cli.staging_root", str(exc))
        if not resolved.is_dir() or _is_link_or_junction(root):
            _fail("staging_root_unavailable", "cli.staging_root", str(root))
        self.root = resolved

    def _candidate(self, relative_value: str, label: str) -> Path:
        relative = canonical_relative(relative_value, label)
        candidate = self.root.joinpath(*relative.parts)
        cursor = self.root
        for part in relative.parts:
            cursor = cursor / part
            if cursor.exists() and _is_link_or_junction(cursor):
                _fail("symlink_rejected", label, relative_value)
        try:
            candidate.resolve(strict=False).relative_to(self.root)
        except (OSError, ValueError):
            _fail("path_escape", label, relative_value)
        return candidate

    def input_file(self, relative_value: str, label: str) -> Path:
        candidate = self._candidate(relative_value, label)
        if not candidate.is_file():
            _fail("file_missing", label, relative_value)
        return candidate.resolve(strict=True)

    def input_directory(self, relative_value: str, label: str) -> Path:
        candidate = self._candidate(relative_value, label)
        if not candidate.is_dir():
            _fail("directory_missing", label, relative_value)
        return candidate.resolve(strict=True)

    def output_file(self, relative_value: str, label: str) -> Path:
        candidate = self._candidate(relative_value, label)
        if candidate.exists():
            _fail("output_exists", label, relative_value)
        candidate.parent.mkdir(parents=True, exist_ok=True)
        self._candidate(relative_value, label)
        return candidate


def require_distinct_paths(paths: Sequence[Path], label: str) -> None:
    resolved: set[Path] = set()
    file_ids: set[tuple[int, int]] = set()
    for path in paths:
        value = path.resolve(strict=path.exists())
        if value in resolved:
            _fail("path_reused", label, str(path))
        resolved.add(value)
        if path.exists():
            stat = path.stat()
            identity = (stat.st_dev, stat.st_ino)
            if stat.st_ino and identity in file_ids:
                _fail("file_reused", label, str(path))
            if stat.st_ino:
                file_ids.add(identity)


def _composite_code_digest() -> str:
    digest = hashlib.sha256()
    for path in (CAPTURE_HELPER, Path(__file__).resolve()):
        digest.update(path.relative_to(REPO).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def frozen_source_identity() -> dict[str, str]:
    """Return current identity only when the installable plugin tree is clean."""

    try:
        diff = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", *FROZEN_CAPTURE_PATHS],
            cwd=REPO,
            check=False,
            capture_output=True,
            timeout=20,
        )
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "--", *FROZEN_CAPTURE_PATHS],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        _fail("git_state_unavailable", "source_identity", f"{type(exc).__name__}: {exc}")
    if diff.returncode not in {0, 1}:
        _fail("git_state_unavailable", "source_identity", "git diff failed")
    if diff.returncode == 1 or untracked.stdout.strip():
        _fail(
            "installable_tree_dirty",
            "source_identity",
            "plugin identity, capture adapter, or scheduler input pack differs from HEAD",
        )
    return current_checkout_source_identity()


def _parse_transport(payload: bytes) -> list[Mapping[str, Any]]:
    records: list[Mapping[str, Any]] = []
    for offset, line in enumerate(payload.decode("utf-8-sig").splitlines()):
        if not line.strip():
            continue
        value = _strict_json(line.encode("utf-8"), f"transport.jsonl[{offset}]")
        records.append(_mapping(value, f"transport.jsonl[{offset}]"))
    if not records:
        _fail("empty_transport", "transport.jsonl", "no JSON object records")
    return records


def _assert_redacted(value: Any, path: str) -> None:
    if redact(value, None) != value:
        _fail("capture_not_redacted", path, "sensitive text remains after capture")


def validate_capture_bundle_bytes(
    capture_bytes: bytes,
    transport_bytes: bytes,
    checksums_bytes: bytes,
    *,
    thread_id: str,
    now: datetime,
) -> tuple[Mapping[str, Any], list[Mapping[str, Any]], Mapping[str, Any]]:
    capture = _mapping(_strict_json(capture_bytes, "capture.json"), "capture.json")
    transport = _parse_transport(transport_bytes)
    checksums = _mapping(_strict_json(checksums_bytes, "sha256sums.json"), "sha256sums.json")
    if set(checksums) != {"capture.json", "transport.jsonl"}:
        _fail("checksum_manifest_fields", "sha256sums.json", "expected exactly two source files")
    for name, payload in (("capture.json", capture_bytes), ("transport.jsonl", transport_bytes)):
        expected = checksums.get(name)
        if not isinstance(expected, str) or HEX_64_RE.fullmatch(expected.lower()) is None:
            _fail("invalid_sha256", f"sha256sums.json.{name}", repr(expected))
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected.lower():
            _fail("source_digest_mismatch", name, f"expected {expected}, found {actual}")

    required_claims = {
        "schema_version": 1,
        "capture_kind": "codex_app_server_preview",
        "verification_level": "capture_only",
        "provider_verified": False,
        "counts_as_preview_acceptance": False,
    }
    for field, expected in required_claims.items():
        if capture.get(field) != expected:
            _fail("capture_contract_mismatch", f"capture.json.{field}", repr(capture.get(field)))
    captured_at = _timestamp(capture.get("captured_at"), "capture.json.captured_at", now=now)
    thread_ids = _sequence(capture.get("thread_ids"), "capture.json.thread_ids")
    normalized_thread_ids = [
        _identifier(value, f"capture.json.thread_ids[{offset}]")
        for offset, value in enumerate(thread_ids)
    ]
    if len(normalized_thread_ids) != len(set(normalized_thread_ids)):
        _fail("duplicate_thread_id", "capture.json.thread_ids", "thread IDs must be unique")
    selected = _identifier(thread_id, "cli.thread_id")
    if selected not in normalized_thread_ids:
        _fail("thread_not_captured", "cli.thread_id", selected)

    results = _mapping(capture.get("results"), "capture.json.results")
    _mapping(results.get("initialize"), "capture.json.results.initialize")
    threads = _mapping(results.get("threads"), "capture.json.results.threads")
    if set(threads) != set(normalized_thread_ids):
        _fail("thread_result_set_mismatch", "capture.json.results.threads", str(sorted(threads)))
    selected_result = _mapping(threads.get(selected), f"capture.json.results.threads.{selected}")
    selected_thread = _mapping(selected_result.get("thread"), f"capture.json.results.threads.{selected}.thread")
    if selected_thread.get("id") != selected:
        _fail("thread_identity_mismatch", f"capture.json.results.threads.{selected}.thread.id", selected)

    embedded_transport = _sequence(
        capture.get("transport_messages"), "capture.json.transport_messages"
    )
    if embedded_transport != transport:
        _fail(
            "transport_capture_mismatch",
            "capture.json.transport_messages",
            "capture and JSONL transcript differ",
        )
    stdout_results = [
        item.get("message", {}).get("result")
        for item in transport
        if item.get("channel") == "stdout"
        and isinstance(item.get("message"), Mapping)
        and "result" in item.get("message", {})
    ]
    for label, value in (
        ("initialize", results["initialize"]),
        (f"threads.{selected}", selected_result),
    ):
        if value not in stdout_results:
            _fail("result_not_in_transport", f"capture.json.results.{label}", selected)

    executable = _mapping(capture.get("codex_executable"), "capture.json.codex_executable")
    try:
        normalize_sha256(executable.get("sha256"), "capture.json.codex_executable.sha256")
    except Exception as exc:
        _fail("invalid_executable_identity", "capture.json.codex_executable.sha256", str(exc))
    size = executable.get("size")
    if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
        _fail("invalid_executable_identity", "capture.json.codex_executable.size", repr(size))

    _assert_redacted(capture, "capture.json")
    _assert_redacted(transport, "transport.jsonl")
    return capture, transport, {
        "captured_at": captured_at,
        "thread_id": selected,
        "thread_result": selected_result,
    }


def _strict_yaml_mapping(payload: bytes, path: str) -> Mapping[str, Any]:
    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                _fail("scheduler_manifest_key", path, repr(key))
            if key in result:
                _fail("duplicate_yaml_key", path, key)
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )
    try:
        document = yaml.load(payload.decode("utf-8-sig"), Loader=UniqueKeyLoader)
    except CaptureNormalizationError:
        raise
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        _fail("invalid_scheduler_manifest", path, str(exc))
    return _mapping(document, path)


def _message_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def _platform_user_messages(thread_result: Mapping[str, Any]) -> list[str]:
    thread = _mapping(thread_result.get("thread"), "platform_thread.thread")
    turns = _sequence(thread.get("turns"), "platform_thread.thread.turns")
    messages: list[str] = []
    for turn_offset, turn_value in enumerate(turns):
        turn = _mapping(turn_value, f"platform_thread.thread.turns[{turn_offset}]")
        items = _sequence(turn.get("items"), f"platform_thread.thread.turns[{turn_offset}].items")
        for item_offset, item_value in enumerate(items):
            item = _mapping(
                item_value,
                f"platform_thread.thread.turns[{turn_offset}].items[{item_offset}]",
            )
            item_type = re.sub(r"[^a-z]", "", str(item.get("type", "")).lower())
            if item_type != "usermessage":
                continue
            text_parts: list[str] = []
            content = item.get("content")
            if isinstance(content, str):
                text_parts.append(content)
            elif isinstance(content, list):
                for part_offset, part_value in enumerate(content):
                    part = _mapping(
                        part_value,
                        f"platform_thread.thread.turns[{turn_offset}].items[{item_offset}].content[{part_offset}]",
                    )
                    part_type = re.sub(r"[^a-z]", "", str(part.get("type", "")).lower())
                    if part_type in {"text", "inputtext"}:
                        text_parts.append(
                            _string(
                                part.get("text"),
                                f"platform_thread.thread.turns[{turn_offset}].items[{item_offset}].content[{part_offset}].text",
                            )
                        )
            elif isinstance(item.get("text"), str):
                text_parts.append(str(item["text"]))
            if not text_parts:
                _fail(
                    "platform_user_message_unreadable",
                    f"platform_thread.thread.turns[{turn_offset}].items[{item_offset}]",
                    "user message has no machine-readable text",
                )
            messages.append("\n".join(text_parts))
    return messages


def _require_prompt_in_thread(thread_result: Mapping[str, Any], prompt_bytes: bytes) -> None:
    try:
        prompt = prompt_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        _fail("scheduler_prompt_not_utf8", "scheduler_prompt", str(exc))
    needle = _message_text(prompt)
    if not needle:
        _fail("scheduler_prompt_empty", "scheduler_prompt", "prompt is empty")
    messages = _platform_user_messages(thread_result)
    if len(messages) != 1:
        _fail(
            "unexpected_platform_user_message_count",
            "capture.json.results.threads.selected.thread.turns",
            f"expected exactly one launch message, found {len(messages)}",
        )
    if _message_text(messages[0]) != needle:
        _fail(
            "launch_prompt_not_in_platform_export",
            "capture.json.results.threads.selected",
            "the sole machine-readable user message is not the exact scheduler prompt",
        )


def _platform_delegation_ids(thread_result: Mapping[str, Any]) -> set[str]:
    thread = _mapping(thread_result.get("thread"), "platform_thread.thread")
    turns = _sequence(thread.get("turns"), "platform_thread.thread.turns")
    identifiers: set[str] = set()
    id_keys = {
        "agentid",
        "childagentid",
        "childtaskid",
        "childthreadid",
        "delegationid",
        "reviewerinstanceid",
        "runid",
        "subagentid",
    }

    def collect(value: Any, path: str) -> None:
        if isinstance(value, Mapping):
            for key, item in value.items():
                normalized_key = re.sub(r"[^a-z]", "", str(key).lower())
                if normalized_key in id_keys and isinstance(item, str):
                    identifiers.add(_identifier(item, f"{path}.{key}"))
                else:
                    collect(item, f"{path}.{key}")
        elif isinstance(value, list):
            for offset, item in enumerate(value):
                collect(item, f"{path}[{offset}]")

    for turn_offset, turn_value in enumerate(turns):
        turn = _mapping(turn_value, f"platform_thread.thread.turns[{turn_offset}]")
        items = _sequence(turn.get("items"), f"platform_thread.thread.turns[{turn_offset}].items")
        for item_offset, item_value in enumerate(items):
            item = _mapping(item_value, f"platform_thread.thread.turns[{turn_offset}].items[{item_offset}]")
            signature = " ".join(
                str(item.get(field, "")).lower()
                for field in ("type", "name", "tool_name", "method", "server")
            )
            if not any(
                token in signature
                for token in ("spawn_agent", "spawnagent", "subagent", "delegat", "collaboration")
            ):
                continue
            collect(item, f"platform_thread.thread.turns[{turn_offset}].items[{item_offset}]")
    return identifiers


def _require_platform_child_binding(
    thread_result: Mapping[str, Any],
    task_document: Mapping[str, Any],
) -> None:
    expected = set(task_document["observable_child_or_delegate_ids"])
    observed = _platform_delegation_ids(thread_result)
    if not observed:
        _fail(
            "platform_child_id_binding_unavailable",
            "capture.json.results.threads.selected.thread.turns",
            "no structured delegation/collaboration IDs were exported",
        )
    if observed != expected:
        _fail(
            "platform_child_id_mismatch",
            "capture.json.results.threads.selected.thread.turns",
            f"task export={sorted(expected)} platform={sorted(observed)}",
        )


def _scheduler_file_binding(value: Any, path: str) -> dict[str, str]:
    record = _mapping(value, path)
    if set(record) != {"path", "sha256"}:
        _fail("scheduler_file_binding_fields", path, "expected path and sha256")
    relative = _string(record.get("path"), f"{path}.path")
    canonical_relative(relative, f"{path}.path")
    try:
        digest = normalize_sha256(record.get("sha256"), f"{path}.sha256")
    except Exception as exc:
        _fail("invalid_sha256", f"{path}.sha256", str(exc))
    return {"path": relative, "sha256": digest}


def _validate_task_scheduler_input(
    task: Mapping[str, Any],
    *,
    slot: Mapping[str, Any],
    source_binding: Mapping[str, str],
    prompt_binding: Mapping[str, str],
) -> Mapping[str, Any]:
    value = _mapping(task.get("scheduler_input"), "task-export.json.scheduler_input")
    required_fields = {
        "schema_version",
        "execution_id",
        "public_entry",
        "entry_mode",
        "source",
        "launch_prompt",
    }
    if set(value) != required_fields or value.get("schema_version") != 1:
        _fail(
            "scheduler_input_contract",
            "task-export.json.scheduler_input",
            f"expected schema 1 and fields {sorted(required_fields)}",
        )
    expected_scalars = {
        "execution_id": slot.get("execution_id"),
        "public_entry": slot.get("public_entry"),
        "entry_mode": slot.get("entry_mode"),
    }
    for field, expected in expected_scalars.items():
        if value.get(field) != expected:
            _fail(
                "scheduler_input_mismatch",
                f"task-export.json.scheduler_input.{field}",
                f"expected {expected!r}, found {value.get(field)!r}",
            )
    if _scheduler_file_binding(value.get("source"), "task-export.json.scheduler_input.source") != dict(source_binding):
        _fail("scheduler_input_mismatch", "task-export.json.scheduler_input.source", "source binding differs")
    if _scheduler_file_binding(
        value.get("launch_prompt"),
        "task-export.json.scheduler_input.launch_prompt",
    ) != dict(prompt_binding):
        _fail("scheduler_input_mismatch", "task-export.json.scheduler_input.launch_prompt", "prompt binding differs")
    forbidden = {
        "expected_final_state",
        "control_driver",
        "scheduler_manifest",
        "scheduler_manifest_sha256",
        "slot",
    }
    leaked = sorted(forbidden.intersection(value))
    if leaked:
        _fail("scheduler_outcome_oracle_exposed", "task-export.json.scheduler_input", leaked[0])
    return value


def _validate_scheduler_manifest(
    manifest_bytes: bytes,
    *,
    execution_id: str,
    source_bytes: bytes,
    prompt_bytes: bytes,
    source_identity: Mapping[str, Any],
    task_document: Mapping[str, Any],
    thread_result: Mapping[str, Any],
) -> dict[str, Any]:
    manifest = _strict_yaml_mapping(manifest_bytes, "scheduler_manifest")
    if (
        manifest.get("schema_version") != 1
        or manifest.get("evidence_kind") != "scheduler_input_pack_only"
        or manifest.get("counts_as_runtime_evidence") is not False
    ):
        _fail("scheduler_manifest_contract", "scheduler_manifest", "non-evidence schema 1 pack required")
    visibility = manifest.get("task_visibility")
    if visibility != {
        "scheduler_manifest_visible_to_task": False,
        "scheduler_manifest_visible_to_reviewers": False,
        "launch_prompt_visible_to_reviewers": False,
        "expected_state_location": "manifest_only",
    }:
        _fail("scheduler_visibility_contract", "scheduler_manifest.task_visibility", repr(visibility))
    plugin = _mapping(manifest.get("plugin_binding"), "scheduler_manifest.plugin_binding")
    if (
        plugin.get("plugin_name") != "research-skills-openai"
        or plugin.get("plugin_version") != source_identity.get("plugin_version")
        or plugin.get("source_commit") not in {
            "set_from_frozen_A_at_execution",
            source_identity.get("source_commit"),
        }
        or plugin.get("registry_sha256") not in {
            "set_from_frozen_A_at_execution",
            source_identity.get("registry_sha256"),
        }
    ):
        _fail("scheduler_plugin_binding_mismatch", "scheduler_manifest.plugin_binding", repr(plugin))
    slots = manifest.get("slots")
    if not isinstance(slots, list) or len(slots) != 10:
        _fail("scheduler_slot_count", "scheduler_manifest.slots", "exactly ten slots are required")
    slot_ids: set[str] = set()
    execution_ids: set[str] = set()
    paths: set[str] = set()
    digests: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    selected: Mapping[str, Any] | None = None
    for offset, value in enumerate(slots):
        slot = _mapping(value, f"scheduler_manifest.slots[{offset}]")
        slot_id = _identifier(slot.get("slot"), f"scheduler_manifest.slots[{offset}].slot")
        execution = _identifier(
            slot.get("execution_id"),
            f"scheduler_manifest.slots[{offset}].execution_id",
        )
        if slot_id in slot_ids or execution in execution_ids:
            _fail("scheduler_slot_reused", f"scheduler_manifest.slots[{offset}]", slot_id)
        slot_ids.add(slot_id)
        execution_ids.add(execution)
        workflow = _string(slot.get("workflow"), f"scheduler_manifest.slots[{offset}].workflow")
        case_kind = _string(slot.get("case_kind"), f"scheduler_manifest.slots[{offset}].case_kind")
        pair = (workflow, case_kind)
        if pair in pairs:
            _fail("scheduler_workflow_case_reused", f"scheduler_manifest.slots[{offset}]", repr(pair))
        pairs.add(pair)
        for field in ("source", "prompt"):
            path_field = "source_path" if field == "source" else "prompt_path"
            digest_field = "source_sha256" if field == "source" else "prompt_sha256"
            relative = _string(slot.get(path_field), f"scheduler_manifest.slots[{offset}].{path_field}")
            canonical_relative(relative, f"scheduler_manifest.slots[{offset}].{path_field}")
            try:
                digest = normalize_sha256(
                    slot.get(digest_field),
                    f"scheduler_manifest.slots[{offset}].{digest_field}",
                )
            except Exception as exc:
                _fail("invalid_sha256", f"scheduler_manifest.slots[{offset}].{digest_field}", str(exc))
            if relative.casefold() in paths or digest in digests:
                _fail("scheduler_visible_input_reused", f"scheduler_manifest.slots[{offset}]", field)
            paths.add(relative.casefold())
            digests.add(digest)
        if execution == execution_id:
            selected = slot
    required_pairs = {
        (workflow, case)
        for workflow in ("idea", "proposal", "article", "perspective", "research_polisher")
        for case in ("happy", "control")
    }
    if pairs != required_pairs:
        _fail("scheduler_workflow_case_coverage", "scheduler_manifest.slots", repr(sorted(pairs)))
    if selected is None:
        _fail("scheduler_execution_not_found", "cli.execution_id", execution_id)
    source_binding = {
        "path": str(selected["source_path"]),
        "sha256": str(selected["source_sha256"]),
    }
    prompt_binding = {
        "path": str(selected["prompt_path"]),
        "sha256": str(selected["prompt_sha256"]),
    }
    if sha256_bytes(source_bytes) != source_binding["sha256"]:
        _fail("scheduler_source_digest_mismatch", "cli.source_file", source_binding["path"])
    if sha256_bytes(prompt_bytes) != prompt_binding["sha256"]:
        _fail("scheduler_prompt_digest_mismatch", "cli.prompt_file", prompt_binding["path"])
    if (
        task_document.get("workflow") != selected.get("workflow")
        or task_document.get("entry_mode") != selected.get("entry_mode")
        or task_document.get("case_kind") != selected.get("case_kind")
    ):
        _fail("scheduler_slot_classification_mismatch", "task-export.json", execution_id)
    _validate_task_scheduler_input(
        task_document,
        slot=selected,
        source_binding=source_binding,
        prompt_binding=prompt_binding,
    )
    _require_prompt_in_thread(thread_result, prompt_bytes)
    _require_platform_child_binding(thread_result, task_document)
    return {
        "schema": SCHEDULER_BINDING_SCHEMA,
        "manifest_schema": SCHEDULER_MANIFEST_SCHEMA,
        "manifest_repository_path": SCHEDULER_MANIFEST_REPOSITORY_PATH,
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "pack_id": _identifier(manifest.get("pack_id"), "scheduler_manifest.pack_id"),
        "slot": _identifier(selected.get("slot"), "scheduler_manifest.selected.slot"),
        "execution_id": execution_id,
        "workflow": str(selected["workflow"]),
        "case_kind": str(selected["case_kind"]),
        "public_entry": _identifier(selected.get("public_entry"), "scheduler_manifest.selected.public_entry"),
        "entry_mode": _identifier(selected.get("entry_mode"), "scheduler_manifest.selected.entry_mode"),
        "capture_profile": _identifier(selected.get("capture_profile"), "scheduler_manifest.selected.capture_profile"),
        "plugin": {
            "name": "research-skills-openai",
            "version": str(source_identity["plugin_version"]),
            "source_commit": str(source_identity["source_commit"]),
            "registry_sha256": str(source_identity["registry_sha256"]),
        },
        "source": source_binding,
        "launch_prompt": prompt_binding,
        "parent_task_or_thread_id": str(task_document["parent_task_or_thread_id"]),
        "observable_child_or_delegate_ids": list(task_document["observable_child_or_delegate_ids"]),
        "platform_child_id_binding": "structured_delegation_items_exact",
        "platform_user_message_binding": "single_exact_launch_prompt",
        "manifest_visible_to_task": False,
        "manifest_visible_to_reviewers": False,
    }


def _validate_file_binding(value: Any, path: str) -> None:
    binding = _mapping(value, path)
    if set(binding) != {"path", "sha256"}:
        _fail("task_export_binding_fields", path, "expected path and sha256")
    relative = binding.get("path")
    if not isinstance(relative, str):
        _fail("task_export_binding_path", f"{path}.path", repr(relative))
    canonical_relative(relative, f"{path}.path")
    try:
        normalize_sha256(binding.get("sha256"), f"{path}.sha256")
    except Exception as exc:
        _fail("invalid_sha256", f"{path}.sha256", str(exc))


def _validate_source_task_export(
    document: Mapping[str, Any],
    *,
    thread_id: str,
    source_identity: Mapping[str, Any],
    path: str,
) -> None:
    required = {
        "schema_version",
        "platform",
        "task_id",
        "plugin_version",
        "registry_sha256",
        "source_commit",
        "workflow",
        "entry_mode",
        "case_kind",
        "final_state",
        "automatic_external_submission",
        "actor_manifest",
        "artifact_index",
        "file_access",
        "parent_task_or_thread_id",
        "observable_child_or_delegate_ids",
        "scheduler_input",
    }
    missing = sorted(required - set(document))
    if missing:
        _fail("task_export_missing_field", f"{path}.{missing[0]}", "required field is absent")
    if document.get("schema_version") != 1 or document.get("platform") != "codex":
        _fail("task_export_contract_mismatch", path, "schema_version=1 and platform=codex required")
    if document.get("task_id") != thread_id:
        _fail("task_export_thread_mismatch", f"{path}.task_id", repr(document.get("task_id")))
    if document.get("parent_task_or_thread_id") != thread_id:
        _fail(
            "task_export_parent_mismatch",
            f"{path}.parent_task_or_thread_id",
            repr(document.get("parent_task_or_thread_id")),
        )
    children = _sequence(
        document.get("observable_child_or_delegate_ids"),
        f"{path}.observable_child_or_delegate_ids",
    )
    child_ids = [
        _identifier(value, f"{path}.observable_child_or_delegate_ids[{offset}]")
        for offset, value in enumerate(children)
    ]
    if not child_ids:
        _fail(
            "task_export_child_ids_missing",
            f"{path}.observable_child_or_delegate_ids",
            "at least one observable delegation ID is required",
        )
    if len(child_ids) != len(set(child_ids)) or thread_id in child_ids:
        _fail(
            "task_export_child_id_reused",
            f"{path}.observable_child_or_delegate_ids",
            "child IDs must be unique and distinct from the parent",
        )
    for field in ("plugin_version", "registry_sha256", "source_commit"):
        if document.get(field) != source_identity.get(field):
            _fail("task_export_source_mismatch", f"{path}.{field}", repr(document.get(field)))
    if document.get("workflow") not in {
        "idea",
        "proposal",
        "article",
        "perspective",
        "research_polisher",
    }:
        _fail("task_export_workflow", f"{path}.workflow", repr(document.get("workflow")))
    _identifier(document.get("entry_mode"), f"{path}.entry_mode")
    if document.get("case_kind") not in {"happy", "control"}:
        _fail("task_export_case_kind", f"{path}.case_kind", repr(document.get("case_kind")))
    _string(document.get("final_state"), f"{path}.final_state")
    if document.get("automatic_external_submission") is not False:
        _fail(
            "task_export_submission_boundary",
            f"{path}.automatic_external_submission",
            repr(document.get("automatic_external_submission")),
        )
    _validate_file_binding(document.get("actor_manifest"), f"{path}.actor_manifest")
    _validate_file_binding(document.get("artifact_index"), f"{path}.artifact_index")
    _validate_file_binding(document.get("file_access"), f"{path}.file_access")
    for forbidden in (
        "expected_final_state",
        "control_driver",
        "scheduler_manifest",
        "scheduler_manifest_sha256",
    ):
        if forbidden in document:
            _fail("scheduler_outcome_oracle_exposed", f"{path}.{forbidden}", "forbidden")


def normalize_capture(
    *,
    staging: StagingRoot,
    capture_dir: str,
    task_export: str,
    scheduler_manifest: str,
    execution_id: str,
    source_file: str,
    prompt_file: str,
    output: str,
    evidence_id: str,
    thread_id: str,
    now: datetime,
) -> tuple[Path, Mapping[str, Any]]:
    directory = staging.input_directory(capture_dir, "cli.capture_dir")
    source_paths = [directory / name for name in CAPTURE_SOURCE_FILES]
    for offset, path in enumerate(source_paths):
        if not path.is_file() or _is_link_or_junction(path):
            _fail("capture_source_missing", f"capture_source[{offset}]", str(path))
    task_export_path = staging.input_file(task_export, "cli.task_export")
    scheduler_manifest_path = staging.input_file(
        scheduler_manifest,
        "cli.scheduler_manifest",
    )
    scheduler_source_path = staging.input_file(source_file, "cli.source_file")
    scheduler_prompt_path = staging.input_file(prompt_file, "cli.prompt_file")
    output_path = staging.output_file(output, "cli.output")
    require_distinct_paths(
        [
            *source_paths,
            task_export_path,
            scheduler_manifest_path,
            scheduler_source_path,
            scheduler_prompt_path,
            output_path,
        ],
        "capture_inputs_and_output",
    )
    payloads = {path.name: path.read_bytes() for path in source_paths}
    payloads["task-export.json"] = task_export_path.read_bytes()
    payloads[SCHEDULER_SOURCE_FILE] = scheduler_source_path.read_bytes()
    payloads[SCHEDULER_PROMPT_FILE] = scheduler_prompt_path.read_bytes()
    capture, transport, selected = validate_capture_bundle_bytes(
        payloads["capture.json"],
        payloads["transport.jsonl"],
        payloads["sha256sums.json"],
        thread_id=thread_id,
        now=now,
    )
    identity = frozen_source_identity()
    repository_manifest_path = REPO / SCHEDULER_MANIFEST_REPOSITORY_PATH
    if (
        not repository_manifest_path.is_file()
        or repository_manifest_path.is_symlink()
        or scheduler_manifest_path.read_bytes() != repository_manifest_path.read_bytes()
    ):
        _fail(
            "scheduler_manifest_not_committed",
            "cli.scheduler_manifest",
            SCHEDULER_MANIFEST_REPOSITORY_PATH,
        )
    task_document = _mapping(
        _strict_json(payloads["task-export.json"], "task-export.json"),
        "task-export.json",
    )
    reserved_fields = {
        "normalization_schema",
        "evidence_id",
        "captured_at",
        "verification_level",
        "provider_verified",
        "counts_as_preview_acceptance",
        "synthetic_test_only",
        "source_identity",
        "capture_adapter",
        "capture_provenance",
        "scheduler_binding",
    }
    collisions = sorted(reserved_fields.intersection(task_document))
    if collisions:
        _fail("task_export_reserved_field", "task-export.json", collisions[0])
    _validate_source_task_export(
        task_document,
        thread_id=selected["thread_id"],
        source_identity=identity,
        path="task-export.json",
    )
    scheduler_binding = _validate_scheduler_manifest(
        scheduler_manifest_path.read_bytes(),
        execution_id=_identifier(execution_id, "cli.execution_id"),
        source_bytes=payloads[SCHEDULER_SOURCE_FILE],
        prompt_bytes=payloads[SCHEDULER_PROMPT_FILE],
        source_identity=identity,
        task_document=task_document,
        thread_result=selected["thread_result"],
    )
    if scheduler_source_path.name != PurePosixPath(scheduler_binding["source"]["path"]).name:
        _fail("scheduler_source_filename_mismatch", "cli.source_file", scheduler_source_path.name)
    if scheduler_prompt_path.name != PurePosixPath(scheduler_binding["launch_prompt"]["path"]).name:
        _fail("scheduler_prompt_filename_mismatch", "cli.prompt_file", scheduler_prompt_path.name)
    normalized = {
        **task_document,
        "normalization_schema": NORMALIZED_CAPTURE_SCHEMA,
        "evidence_id": _identifier(evidence_id, "cli.evidence_id"),
        "captured_at": selected["captured_at"],
        "verification_level": "capture_only",
        "provider_verified": False,
        "counts_as_preview_acceptance": False,
        "synthetic_test_only": False,
        "source_identity": identity,
        "scheduler_binding": scheduler_binding,
        "capture_adapter": {
            "adapter_id": CAPTURE_ADAPTER_ID,
            "adapter_code_sha256": _composite_code_digest(),
        },
        "capture_provenance": {
            "surface": "codex_app_server",
            "task_or_thread_id": selected["thread_id"],
            "capture_kind": capture["capture_kind"],
            "evidence_kind": "task_export",
            "codex_executable": capture["codex_executable"],
            "selected_thread": selected["thread_result"],
        },
        "source_files": {
            name: {
                "sha256": sha256_bytes(payload),
                "size": len(payload),
                "content_base64": base64.b64encode(payload).decode("ascii"),
            }
            for name, payload in payloads.items()
        },
    }
    output_path.write_bytes(canonical_json_bytes(normalized))
    return output_path, normalized


def decode_normalized_source_files(document: Mapping[str, Any]) -> dict[str, bytes]:
    records = _mapping(document.get("source_files"), "normalized_capture.source_files")
    if set(records) != set(SOURCE_FILES):
        _fail("normalized_source_files", "normalized_capture.source_files", "source set mismatch")
    decoded: dict[str, bytes] = {}
    for name in SOURCE_FILES:
        record = _mapping(records.get(name), f"normalized_capture.source_files.{name}")
        if set(record) != {"sha256", "size", "content_base64"}:
            _fail("normalized_source_fields", f"normalized_capture.source_files.{name}", "field set mismatch")
        encoded = record.get("content_base64")
        if not isinstance(encoded, str):
            _fail("invalid_base64", f"normalized_capture.source_files.{name}.content_base64", repr(encoded))
        try:
            payload = base64.b64decode(encoded, validate=True)
        except (ValueError, base64.binascii.Error):
            _fail("invalid_base64", f"normalized_capture.source_files.{name}.content_base64", "decode failed")
        size = record.get("size")
        if isinstance(size, bool) or not isinstance(size, int) or size <= 0 or len(payload) != size:
            _fail("normalized_source_size_mismatch", f"normalized_capture.source_files.{name}", repr(size))
        try:
            expected = normalize_sha256(record.get("sha256"), f"normalized_capture.source_files.{name}.sha256")
        except Exception as exc:
            _fail("invalid_sha256", f"normalized_capture.source_files.{name}.sha256", str(exc))
        if sha256_bytes(payload) != expected:
            _fail("normalized_source_digest_mismatch", f"normalized_capture.source_files.{name}", name)
        decoded[name] = payload
    return decoded


def validate_normalized_capture(
    document: Mapping[str, Any], *, now: datetime, verify_checkout: bool = True
) -> Mapping[str, Any]:
    if document.get("schema_version") != 1 or document.get("normalization_schema") != NORMALIZED_CAPTURE_SCHEMA:
        _fail(
            "unsupported_schema",
            "normalized_capture.normalization_schema",
            repr(document.get("normalization_schema")),
        )
    for field, expected in (
        ("verification_level", "capture_only"),
        ("provider_verified", False),
        ("counts_as_preview_acceptance", False),
        ("synthetic_test_only", False),
    ):
        if document.get(field) != expected:
            _fail("normalized_claim_mismatch", f"normalized_capture.{field}", repr(document.get(field)))
    evidence_id = _identifier(document.get("evidence_id"), "normalized_capture.evidence_id")
    captured_at = _timestamp(document.get("captured_at"), "normalized_capture.captured_at", now=now)
    identity = _mapping(document.get("source_identity"), "normalized_capture.source_identity")
    adapter = _mapping(document.get("capture_adapter"), "normalized_capture.capture_adapter")
    if adapter.get("adapter_id") != CAPTURE_ADAPTER_ID or adapter.get("adapter_code_sha256") != _composite_code_digest():
        _fail("capture_adapter_mismatch", "normalized_capture.capture_adapter", "code identity differs")
    capture = _mapping(document.get("capture_provenance"), "normalized_capture.capture_provenance")
    thread_id = _identifier(capture.get("task_or_thread_id"), "normalized_capture.capture_provenance.task_or_thread_id")
    if capture.get("surface") != "codex_app_server" or capture.get("evidence_kind") != "task_export":
        _fail("normalized_capture_kind", "normalized_capture.capture_provenance", "unsupported surface or kind")
    decoded = decode_normalized_source_files(document)
    source_capture, _transport, selected = validate_capture_bundle_bytes(
        decoded["capture.json"],
        decoded["transport.jsonl"],
        decoded["sha256sums.json"],
        thread_id=thread_id,
        now=now,
    )
    source_task = _mapping(
        _strict_json(decoded["task-export.json"], "normalized_capture.source_task_export"),
        "normalized_capture.source_task_export",
    )
    _validate_source_task_export(
        source_task,
        thread_id=thread_id,
        source_identity=identity,
        path="normalized_capture.source_task_export",
    )
    scheduler_binding = _mapping(
        document.get("scheduler_binding"),
        "normalized_capture.scheduler_binding",
    )
    repository_manifest_path = REPO / SCHEDULER_MANIFEST_REPOSITORY_PATH
    try:
        manifest_bytes = repository_manifest_path.read_bytes()
    except OSError as exc:
        _fail(
            "scheduler_manifest_unavailable",
            "normalized_capture.scheduler_binding.manifest_repository_path",
            str(exc),
        )
    if scheduler_binding.get("manifest_sha256") != sha256_bytes(manifest_bytes):
        _fail(
            "scheduler_manifest_digest_mismatch",
            "normalized_capture.scheduler_binding.manifest_sha256",
            repr(scheduler_binding.get("manifest_sha256")),
        )
    expected_scheduler_binding = _validate_scheduler_manifest(
        manifest_bytes,
        execution_id=_identifier(
            scheduler_binding.get("execution_id"),
            "normalized_capture.scheduler_binding.execution_id",
        ),
        source_bytes=decoded[SCHEDULER_SOURCE_FILE],
        prompt_bytes=decoded[SCHEDULER_PROMPT_FILE],
        source_identity=identity,
        task_document=source_task,
        thread_result=selected["thread_result"],
    )
    if dict(scheduler_binding) != expected_scheduler_binding:
        _fail(
            "normalized_scheduler_binding_mismatch",
            "normalized_capture.scheduler_binding",
            evidence_id,
        )
    for key, value in source_task.items():
        if document.get(key) != value:
            _fail(
                "normalized_task_export_derivation_mismatch",
                f"normalized_capture.{key}",
                evidence_id,
            )
    if (
        selected["captured_at"] != captured_at
        or capture.get("capture_kind") != source_capture.get("capture_kind")
        or capture.get("codex_executable") != source_capture.get("codex_executable")
        or capture.get("selected_thread") != selected["thread_result"]
    ):
        _fail("normalized_capture_derivation_mismatch", "normalized_capture.capture_provenance", evidence_id)
    if verify_checkout and dict(identity) != frozen_source_identity():
        _fail("source_identity_mismatch", "normalized_capture.source_identity", evidence_id)
    return {
        "evidence_id": evidence_id,
        "captured_at": captured_at,
        "source_identity": dict(identity),
        "adapter": dict(adapter),
        "capture": dict(capture),
        "scheduler_binding": expected_scheduler_binding,
    }


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        _fail("invalid_cli_arguments", "cli", message)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("--staging-root", type=Path, required=True)
    parser.add_argument("--capture-dir", required=True, help="Relative directory with the three capture files")
    parser.add_argument("--task-export", required=True, help="Relative workflow-produced task-export JSON")
    parser.add_argument(
        "--scheduler-manifest",
        required=True,
        help="Scheduler-only copy of the committed ten-slot manifest",
    )
    parser.add_argument("--execution-id", required=True, help="Opaque scheduler execution ID")
    parser.add_argument("--source-file", required=True, help="Actual frozen source supplied to the task")
    parser.add_argument("--prompt-file", required=True, help="Exact launch prompt sent to the task")
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--evidence-id", required=True)
    parser.add_argument("--output", required=True, help="New relative R JSON path")
    parser.add_argument("--now", help="ISO-8601 validation clock; defaults to current UTC")
    return parser


def _failure(exc: CaptureNormalizationError) -> dict[str, Any]:
    return {
        "schema_version": "openai-preview-capture-normalization-result/v1",
        "normalized": False,
        "gate_eligible": False,
        "accepted": False,
        "error": {"code": exc.code, "path": exc.path, "message": exc.message},
    }


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        staging = StagingRoot(args.staging_root)
        output, document = normalize_capture(
            staging=staging,
            capture_dir=args.capture_dir,
            task_export=args.task_export,
            scheduler_manifest=args.scheduler_manifest,
            execution_id=args.execution_id,
            source_file=args.source_file,
            prompt_file=args.prompt_file,
            output=args.output,
            evidence_id=args.evidence_id,
            thread_id=args.thread_id,
            now=parse_clock(args.now),
        )
        result = {
            "schema_version": "openai-preview-capture-normalization-result/v1",
            "normalized": True,
            "gate_eligible": False,
            "accepted": False,
            "verification_level": "capture_only",
            "evidence_id": document["evidence_id"],
            "output": str(output),
            "sha256": sha256_bytes(output.read_bytes()),
            "source_identity": document["source_identity"],
        }
    except CaptureNormalizationError as exc:
        result = _failure(exc)
        return_code = 2 if exc.code == "invalid_cli_arguments" else 1
    except Exception as exc:
        result = _failure(CaptureNormalizationError("internal_error", "cli", f"{type(exc).__name__}: {exc}"))
        return_code = 3
    else:
        return_code = 0
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
