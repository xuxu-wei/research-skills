#!/usr/bin/env python3
"""Minimal JSONL App Server fixture for capture-helper tests."""

from __future__ import annotations

import json
import sys


def respond(request_id: int, result: object) -> None:
    print(json.dumps({"id": request_id, "result": result}), flush=True)


for raw_line in sys.stdin:
    document = json.loads(raw_line)
    if "id" not in document:
        continue
    request_id = document["id"]
    method = document.get("method")
    if method == "initialize":
        print(
            "Authorization: Bearer fixture-secret-token email=private@example.test "
            "url=https://example.test/?access_token=fixture-query-secret",
            file=sys.stderr,
            flush=True,
        )
        respond(request_id, {"serverInfo": {"name": "fake-codex", "version": "1.0"}})
    elif method == "skills/list":
        respond(
            request_id,
            {
                "data": [
                    {
                        "cwd": document["params"]["cwds"][0],
                        "skills": [{"name": "research-polisher-orchestrator"}],
                    }
                ]
            },
        )
    elif method == "account/read":
        respond(
            request_id,
            {
                "authMode": "chatgpt",
                "email": "private@example.test",
                "accessToken": "must-not-leak",
                "accountId": "private-account",
            },
        )
    elif method == "plugin/list":
        respond(
            request_id,
            {
                "data": [
                    {
                        "id": "research-skills-openai",
                        "installed": True,
                        "localVersion": "0.7.0-preview.1",
                        "source": {"type": "git", "sha": "a" * 40},
                    }
                ]
            },
        )
    elif method == "thread/read":
        respond(
            request_id,
            {
                "thread": {
                    "id": document["params"]["threadId"],
                    "status": "completed",
                    "turns": [{"id": "turn-1", "items": []}],
                }
            },
        )
    else:
        print(
            json.dumps(
                {"id": request_id, "error": {"code": -32601, "message": method}}
            ),
            flush=True,
        )
