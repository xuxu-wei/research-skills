#!/usr/bin/env python3
"""Capture a redacted Codex App Server JSONL evidence bundle.

This helper records official App Server responses without claiming that the
capture is provider-verified or sufficient by itself for a Preview gate.  A
separate evidence envelope must bind this capture to the frozen plugin identity
and an external witness before it can count as ``preview_attested`` evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SENSITIVE_KEYS = {
    "accesstoken",
    "accountid",
    "apikey",
    "authorization",
    "chatgptaccountid",
    "email",
    "idtoken",
    "refreshtoken",
    "token",
}

SENSITIVE_TEXT_PATTERNS = (
    (re.compile(r"(?i)\b(authorization|cookie|set-cookie)\s*:\s*[^\r\n]+"), r"\1: [REDACTED]"),
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]{8,}"), r"\1 [REDACTED]"),
    (re.compile(r"(?i)([?&](?:access_token|token|api_key|key)=)[^&\s]+"), r"\1[REDACTED]"),
    (re.compile(r"\b(?:sk|gh[pousr])_[A-Za-z0-9_-]{12,}\b"), "[REDACTED]"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
)


class CaptureError(RuntimeError):
    """Raised when the App Server cannot provide a complete capture."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def redact(value: Any, home: str | None) -> Any:
    """Remove credentials and normalize the current home path recursively."""

    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            normalized = "".join(character for character in key.lower() if character.isalnum())
            result[key] = "[REDACTED]" if normalized in SENSITIVE_KEYS else redact(item, home)
        return result
    if isinstance(value, list):
        return [redact(item, home) for item in value]
    if isinstance(value, str):
        redacted = value
        if home:
            variants = {home, home.replace("\\", "/")}
            for variant in sorted(variants, key=len, reverse=True):
                if variant:
                    redacted = redacted.replace(variant, "%USERPROFILE%")
        for pattern, replacement in SENSITIVE_TEXT_PATTERNS:
            redacted = pattern.sub(replacement, redacted)
        return redacted
    return value


def executable_identity(path: str) -> dict[str, Any]:
    resolved = Path(path).resolve()
    result: dict[str, Any] = {"path": str(resolved), "sha256": None, "size": None}
    try:
        payload = resolved.read_bytes()
    except OSError:
        return result
    result["sha256"] = sha256_bytes(payload)
    result["size"] = len(payload)
    return result


class JsonlClient:
    def __init__(
        self, command: list[str], timeout: float, *, environment: dict[str, str] | None = None
    ) -> None:
        self.timeout = timeout
        self.messages: list[dict[str, Any]] = []
        self._queue: queue.Queue[tuple[str, str | None]] = queue.Queue()
        self._process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=environment,
        )
        assert self._process.stdout is not None
        assert self._process.stderr is not None
        self._stdout_thread = threading.Thread(
            target=self._pump,
            args=("stdout", self._process.stdout),
            daemon=True,
        )
        self._stderr_thread = threading.Thread(
            target=self._pump,
            args=("stderr", self._process.stderr),
            daemon=True,
        )
        self._stdout_thread.start()
        self._stderr_thread.start()

    def _pump(self, channel: str, stream: Any) -> None:
        for line in stream:
            self._queue.put((channel, line.rstrip("\r\n")))
        self._queue.put((channel, None))

    def send(self, document: dict[str, Any]) -> None:
        if self._process.stdin is None:
            raise CaptureError("App Server stdin is unavailable")
        self._process.stdin.write(json.dumps(document, ensure_ascii=False) + "\n")
        self._process.stdin.flush()

    def request(self, request_id: int, method: str, params: dict[str, Any]) -> Any:
        self.send({"method": method, "id": request_id, "params": params})
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            remaining = max(0.01, deadline - time.monotonic())
            try:
                channel, line = self._queue.get(timeout=remaining)
            except queue.Empty as error:
                raise CaptureError(f"timed out waiting for {method}") from error
            if line is None:
                if self._process.poll() is not None:
                    raise CaptureError(
                        f"App Server exited before responding to {method}: "
                        f"{self._process.returncode}"
                    )
                continue
            if channel == "stderr":
                self.messages.append({"channel": "stderr", "line": line})
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError as error:
                raise CaptureError(f"App Server emitted non-JSON stdout: {line!r}") from error
            self.messages.append({"channel": "stdout", "message": message})
            if message.get("id") != request_id:
                continue
            if "error" in message:
                raise CaptureError(f"{method} failed: {message['error']}")
            return message.get("result")
        raise CaptureError(f"timed out waiting for {method}")

    def close(self) -> None:
        if self._process.stdin is not None:
            self._process.stdin.close()
        try:
            self._process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self._process.terminate()
            try:
                self._process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=3)


def capture(
    *,
    codex: str,
    cwd: str,
    thread_ids: list[str],
    include_account: bool,
    include_skills: bool,
    include_plugins: bool,
    codex_home: str | None,
    timeout: float,
) -> dict[str, Any]:
    command = [codex, "app-server", "--listen", "stdio://"]
    environment = dict(os.environ)
    if codex_home:
        environment["CODEX_HOME"] = str(Path(codex_home).resolve())
    client = JsonlClient(command, timeout, environment=environment)
    results: dict[str, Any] = {}
    try:
        results["initialize"] = client.request(
            1,
            "initialize",
            {
                "clientInfo": {
                    "name": "research_skills_preview_evidence",
                    "title": "Research Skills Preview Evidence Capture",
                    "version": "1.0.0",
                },
                "capabilities": {"experimentalApi": True},
            },
        )
        client.send({"method": "initialized", "params": {}})
        request_id = 2
        if include_skills:
            results["skills"] = client.request(
                request_id,
                "skills/list",
                {"cwds": [str(Path(cwd).resolve())], "forceReload": True},
            )
            request_id += 1
        if include_plugins:
            results["plugins"] = client.request(request_id, "plugin/list", {})
            request_id += 1
        if include_account:
            results["account"] = client.request(request_id, "account/read", {})
            request_id += 1
        results["threads"] = {}
        for thread_id in thread_ids:
            results["threads"][thread_id] = client.request(
                request_id,
                "thread/read",
                {"threadId": thread_id, "includeTurns": True},
            )
            request_id += 1
    finally:
        client.close()

    home = str(Path.home())
    redacted_results = redact(results, home)
    redacted_messages = redact(client.messages, home)
    return {
        "schema_version": 1,
        "capture_kind": "codex_app_server_preview",
        "verification_level": "capture_only",
        "provider_verified": False,
        "counts_as_preview_acceptance": False,
        "plugin_list_is_experimental_and_not_sufficient_alone": include_plugins,
        "captured_at": utc_now(),
        "cwd": redact(str(Path(cwd).resolve()), home),
        "codex_home": redact(
            str(Path(codex_home).resolve()) if codex_home else None, home
        ),
        "thread_ids": thread_ids,
        "codex_executable": redact(executable_identity(codex), home),
        "results": redacted_results,
        "transport_messages": redacted_messages,
    }


def write_bundle(document: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    capture_bytes = (
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    transcript_bytes = b"".join(
        (json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        for item in document.get("transport_messages", [])
    )
    capture_path = output_dir / "capture.json"
    transcript_path = output_dir / "transport.jsonl"
    capture_path.write_bytes(capture_bytes)
    transcript_path.write_bytes(transcript_bytes)
    checksums = {
        "capture.json": sha256_bytes(capture_bytes),
        "transport.jsonl": sha256_bytes(transcript_bytes),
    }
    checksum_path = output_dir / "sha256sums.json"
    checksum_path.write_text(
        json.dumps(checksums, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return checksums


def configured_codex_path(config_path: Path | None = None) -> str | None:
    """Read the App-managed CLI path without requiring a standalone install."""

    path = config_path or (Path.home() / ".codex" / "config.toml")
    try:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return None
    queue_: list[dict[str, Any]] = [document]
    while queue_:
        mapping = queue_.pop(0)
        for key, value in mapping.items():
            if key.upper() == "CODEX_CLI_PATH" and isinstance(value, str):
                if Path(value).is_file():
                    return value
            elif isinstance(value, dict):
                queue_.append(value)
    return None


def resolve_codex(value: str | None, config_path: Path | None = None) -> str:
    configured = configured_codex_path(config_path)
    candidate = value or (
        configured
        if config_path is not None
        else os.environ.get("CODEX_CLI_PATH") or configured or shutil.which("codex")
    )
    if not candidate or not Path(candidate).is_file():
        raise CaptureError(
            "Codex executable was not found; pass --codex or use the App-managed "
            "CODEX_CLI_PATH in ~/.codex/config.toml"
        )
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", help="Path to the Codex executable")
    parser.add_argument(
        "--codex-config",
        type=Path,
        help="Optional config.toml used to locate the App-managed Codex executable",
    )
    parser.add_argument("--cwd", default=str(Path.cwd()), help="Workspace for skills/list")
    parser.add_argument(
        "--codex-home",
        default=str(Path.home() / ".codex"),
        help="Codex home containing the App's marketplaces and plugin state",
    )
    parser.add_argument("--thread-id", action="append", default=[], help="Thread to export")
    parser.add_argument("--include-account", action="store_true", help="Capture redacted account/read")
    parser.add_argument(
        "--include-plugins",
        action="store_true",
        help="Capture experimental plugin/list state as supplementary evidence",
    )
    parser.add_argument("--no-skills", action="store_true", help="Skip skills/list")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        codex = resolve_codex(args.codex, args.codex_config)
        document = capture(
            codex=codex,
            cwd=args.cwd,
            thread_ids=args.thread_id,
            include_account=args.include_account,
            include_skills=not args.no_skills,
            include_plugins=args.include_plugins,
            codex_home=args.codex_home,
            timeout=args.timeout,
        )
        checksums = write_bundle(document, args.output_dir)
    except (CaptureError, OSError) as error:
        print(f"capture failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"output_dir": str(args.output_dir), "sha256": checksums}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
