#!/usr/bin/env python3
"""Test the Codex App Server Preview capture helper without a live account."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from capture_openai_codex_app_server import redact, resolve_codex


REPO = Path(__file__).resolve().parents[1]
CAPTURE = REPO / "scripts" / "capture_openai_codex_app_server.py"
FAKE = REPO / "tests" / "openai_phase7" / "fake_app_server.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    sample = {
        "accessToken": "secret",
        "nested": {"account_id": "secret-account", "path": str(Path.home() / "x")},
    }
    redacted = redact(sample, str(Path.home()))
    require(redacted["accessToken"] == "[REDACTED]", "access token was not redacted")
    require(redacted["nested"]["account_id"] == "[REDACTED]", "account ID was not redacted")
    require("%USERPROFILE%" in redacted["nested"]["path"], "home path was not normalized")

    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "bundle"
        result = subprocess.run(
            [
                sys.executable,
                str(CAPTURE),
                "--codex",
                sys.executable,
                "--cwd",
                str(REPO),
                "--thread-id",
                "thread-a01",
                "--include-account",
                "--include-plugins",
                "--timeout",
                "1",
                "--output-dir",
                str(output),
            ],
            env={**dict(__import__("os").environ), "PYTHONPATH": str(REPO / "scripts")},
            capture_output=True,
            text=True,
            check=False,
        )
        # Python needs the fixture path in place of the normal app-server
        # subcommand. Run a tiny wrapper command for the test instead.
        if result.returncode == 0:
            raise AssertionError("capture unexpectedly accepted Python as Codex")

        wrapper = Path(temporary) / ("fake-codex.cmd" if sys.platform == "win32" else "fake-codex")
        if sys.platform == "win32":
            wrapper.write_text(f'@"{sys.executable}" "{FAKE}"\r\n', encoding="utf-8")
        else:
            wrapper.write_text(f'#!{sys.executable}\nexec "{sys.executable}" "{FAKE}"\n', encoding="utf-8")
            wrapper.chmod(0o755)
        config_path = Path(temporary) / "config.toml"
        escaped_wrapper = str(wrapper).replace("\\", "\\\\")
        config_path.write_text(
            f'[mcp_servers.fixture.env]\nCODEX_CLI_PATH = "{escaped_wrapper}"\n',
            encoding="utf-8",
        )
        require(
            Path(resolve_codex(None, config_path)).resolve() == wrapper.resolve(),
            "App-managed CODEX_CLI_PATH was not resolved",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(CAPTURE),
                "--codex",
                str(wrapper),
                "--cwd",
                str(REPO),
                "--thread-id",
                "thread-a01",
                "--include-account",
                "--include-plugins",
                "--timeout",
                "5",
                "--output-dir",
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        require(result.returncode == 0, f"capture fixture failed: {result.stderr}")
        document = json.loads((output / "capture.json").read_text(encoding="utf-8"))
        serialized_capture = json.dumps(document, ensure_ascii=False)
        for secret in (
            "fixture-secret-token",
            "private@example.test",
            "fixture-query-secret",
            "must-not-leak",
            "private-account",
        ):
            require(secret not in serialized_capture, f"sensitive text leaked: {secret}")
        require(document["verification_level"] == "capture_only", "capture overclaimed trust")
        require(document["provider_verified"] is False, "capture overclaimed provider verification")
        require(
            document["counts_as_preview_acceptance"] is False,
            "capture alone counted as Preview acceptance",
        )
        account = document["results"]["account"]
        require(
            document["results"]["plugins"]["data"][0]["id"]
            == "research-skills-openai",
            "plugin/list response was not retained",
        )
        require(
            document["plugin_list_is_experimental_and_not_sufficient_alone"] is True,
            "experimental plugin/list boundary was not recorded",
        )
        require(account["email"] == "[REDACTED]", "email leaked")
        require(account["accessToken"] == "[REDACTED]", "token leaked")
        require(account["accountId"] == "[REDACTED]", "account ID leaked")
        require(
            document["results"]["threads"]["thread-a01"]["thread"]["status"]
            == "completed",
            "thread export was not retained",
        )
        checksums = json.loads((output / "sha256sums.json").read_text(encoding="utf-8"))
        for name, digest in checksums.items():
            require(
                hashlib.sha256((output / name).read_bytes()).hexdigest() == digest,
                f"checksum mismatch for {name}",
            )

    print("Codex App Server Preview capture tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
