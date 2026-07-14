#!/usr/bin/env python3
"""End-to-end and mutation tests for real-capture R/E/V/I preparation."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from openai_preview_evidence import sha256_bytes


REPO = Path(__file__).resolve().parents[1]
NORMALIZER = REPO / "scripts" / "normalize_openai_preview_capture.py"
BUILDER = REPO / "scripts" / "build_openai_preview_mini_bundle.py"
RUNTIME_BUILDER = REPO / "scripts" / "build_openai_phase7_runtime_capture.py"
DRAFT_VERIFIER = REPO / "scripts" / "verify_openai_preview_draft_bundle.py"
OFFLINE_VALIDATOR = REPO / "scripts" / "validate_openai_preview_evidence_bundle.py"
WORKFLOW = REPO / ".github" / "workflows" / "openai-preview-draft-bundle-verifier.yml"
REPOSITORY = "xuxu-wei/research-skills"
THREAD_ID = "thread-live-001"
EVIDENCE_ID = "phase7-idea-happy-live-001"
EXECUTION_ID = "p7-l01"
SCHEDULER_MANIFEST = REPO / "tests" / "openai_phase7" / "live-inputs" / "manifest.yaml"
SCHEDULER_SOURCE = REPO / "tests" / "openai_phase7" / "live-inputs" / "sources" / f"{EXECUTION_ID}.md"
SCHEDULER_PROMPT = REPO / "tests" / "openai_phase7" / "live-inputs" / "prompts" / f"{EXECUTION_ID}.md"
ISOLATED_GIT_ENV: dict[str, str] = {}
PLUGIN_VERSION = json.loads(
    (REPO / "research-skills-openai" / ".codex-plugin" / "plugin.json").read_text(
        encoding="utf-8"
    )
)["version"]


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def write_json(path: Path, document: object) -> bytes:
    payload = (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return payload


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(script: Path, *arguments: str, env: dict[str, str] | None = None) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(script), *arguments],
        cwd=REPO,
        env={**os.environ, **ISOLATED_GIT_ENV, **(env or {})},
        check=False,
        capture_output=True,
        text=True,
    )
    require(not completed.stderr, f"{script.name} stderr: {completed.stderr}")
    try:
        output = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{script.name} returned non-JSON: {completed.stdout!r}") from exc
    return completed.returncode, output


def initialize_isolated_clean_git(git_dir: Path) -> dict[str, str]:
    """Commit the current bytes into a disposable Git database for production checks."""

    environment = {
        **os.environ,
        "GIT_DIR": str(git_dir),
        "GIT_WORK_TREE": str(REPO),
    }
    snapshot_paths = (
        ".github/workflows/openai-preview-draft-bundle-verifier.yml",
        "research-skills-openai/.codex-plugin/plugin.json",
        "research-skills-openai/workflow-registry.yaml",
        "research-skills-openai/skills",
        "scripts/build_openai_phase7_runtime_capture.py",
        "scripts/build_openai_preview_mini_bundle.py",
        "scripts/capture_openai_codex_app_server.py",
        "scripts/normalize_openai_preview_capture.py",
        "scripts/openai_preview_evidence.py",
        "scripts/verify_openai_preview_draft_bundle.py",
        "tests/openai_phase7/live-inputs",
        "tests/openai_phase7/runtime-receipts.schema.yaml",
        "tests/openai_phase8/provider-verifier-registry.yaml",
        "tests/openai_phase8/verify_preview_evidence.py",
    )
    commands = (
        ["git", "init"],
        ["git", "config", "core.autocrlf", "false"],
        ["git", "config", "user.name", "Preview Evidence Test"],
        ["git", "config", "user.email", "preview-evidence-test@example.invalid"],
        ["git", "add", "--", *snapshot_paths],
        ["git", "commit", "-m", "isolated production identity fixture"],
    )
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=REPO,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        require(completed.returncode == 0, f"isolated git failed: {command}: {completed.stderr}")
    return {"GIT_DIR": str(git_dir), "GIT_WORK_TREE": str(REPO)}


def production_identity() -> dict[str, str]:
    script = (
        "import json,sys; "
        f"sys.path.insert(0,{str(REPO / 'scripts')!r}); "
        "from normalize_openai_preview_capture import frozen_source_identity; "
        "print(json.dumps(frozen_source_identity(),sort_keys=True))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO,
        env={**os.environ, **ISOLATED_GIT_ENV},
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode == 0, f"production identity failed: {completed.stderr}")
    return json.loads(completed.stdout)


def stage_scheduler_inputs(root: Path) -> dict[str, Path]:
    paths = {
        "manifest": root / "scheduler" / "manifest.yaml",
        "source": root / "input" / SCHEDULER_SOURCE.name,
        "prompt": root / "input" / "prompt" / SCHEDULER_PROMPT.name,
    }
    for label, source in (
        ("manifest", SCHEDULER_MANIFEST),
        ("source", SCHEDULER_SOURCE),
        ("prompt", SCHEDULER_PROMPT),
    ):
        paths[label].parent.mkdir(parents=True, exist_ok=True)
        paths[label].write_bytes(source.read_bytes())
    return paths


def write_capture(
    root: Path,
    *,
    now: datetime,
    prompt_text: str,
    mutation: str | None = None,
) -> None:
    capture_dir = root / "capture"
    capture_dir.mkdir(parents=True)
    initialize = {"serverInfo": {"name": "codex-app-server", "version": "1.0"}}
    thread_result = {
        "thread": {
            "id": THREAD_ID,
            "status": "completed",
            "turns": [
                {
                    "id": "turn-1",
                    "items": [
                        {
                            "type": "user_message",
                            "content": [{"type": "input_text", "text": prompt_text}],
                        },
                        {
                            "type": "collaboration_tool_call",
                            "name": "collaboration.spawn_agent",
                            "result": {"agent_id": "child-evaluator-001"},
                        },
                        {"type": "agent_message", "text": "observed result"},
                    ],
                }
            ],
        }
    }
    if mutation == "extra_user_message":
        thread_result["thread"]["turns"].append(
            {
                "id": "turn-2",
                "items": [
                    {
                        "type": "user_message",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "Expected state: human_signoff_required.",
                            }
                        ],
                    }
                ],
            }
        )
    elif mutation == "missing_child_binding":
        thread_result["thread"]["turns"][0]["items"] = [
            item
            for item in thread_result["thread"]["turns"][0]["items"]
            if item.get("type") != "collaboration_tool_call"
        ]
    elif mutation == "extra_orchestrated_child":
        thread_result["thread"]["turns"][0]["items"].insert(
            2,
            {
                "type": "collaboration_tool_call",
                "name": "collaboration.spawn_agent",
                "result": {"agent_id": "writer-orchestrated-001"},
            },
        )
    transport = [
        {"channel": "stdout", "message": {"id": 1, "result": initialize}},
        {"channel": "stdout", "message": {"id": 2, "result": thread_result}},
    ]
    capture = {
        "schema_version": 1,
        "capture_kind": "codex_app_server_preview",
        "verification_level": "capture_only",
        "provider_verified": False,
        "counts_as_preview_acceptance": False,
        "captured_at": timestamp(now - timedelta(minutes=8)),
        "thread_ids": [THREAD_ID],
        "codex_executable": {
            "path": "C:/Program Files/OpenAI/Codex/codex.exe",
            "sha256": "a" * 64,
            "size": 12345,
        },
        "results": {"initialize": initialize, "threads": {THREAD_ID: thread_result}},
        "transport_messages": transport,
    }
    if mutation == "forged_claim":
        capture["provider_verified"] = True
    elif mutation == "missing_field":
        del capture["transport_messages"]
    capture_bytes = write_json(capture_dir / "capture.json", capture)
    transport_bytes = b"".join(
        (json.dumps(record, sort_keys=True) + "\n").encode("utf-8") for record in transport
    )
    (capture_dir / "transport.jsonl").write_bytes(transport_bytes)
    checksums = {
        "capture.json": hashlib.sha256(capture_bytes).hexdigest(),
        "transport.jsonl": hashlib.sha256(transport_bytes).hexdigest(),
    }
    write_json(capture_dir / "sha256sums.json", checksums)
    if mutation == "digest_mismatch":
        (capture_dir / "capture.json").write_bytes(capture_bytes + b" ")


def write_task_export(
    root: Path,
    identity: dict[str, str],
    *,
    scheduler_paths: dict[str, Path],
    mutation: str | None = None,
) -> dict[str, Path]:
    manifest = yaml.safe_load(scheduler_paths["manifest"].read_text(encoding="utf-8"))
    slot = next(item for item in manifest["slots"] if item["execution_id"] == EXECUTION_ID)
    logical = {
        "actor": f"runs/{EXECUTION_ID}/capture/actor-manifest.json",
        "artifact": f"runs/{EXECUTION_ID}/capture/artifact-index.json",
        "access": f"runs/{EXECUTION_ID}/capture/file-access.json",
        "source": f"runs/{EXECUTION_ID}/input/{scheduler_paths['source'].name}",
        "task": f"runs/{EXECUTION_ID}/capture/task-export.json",
    }
    support = {
        "actor": root / "bundle" / f"{EVIDENCE_ID}-actor-manifest.json",
        "artifact": root / "bundle" / f"{EVIDENCE_ID}-artifact-index.json",
        "access": root / "bundle" / f"{EVIDENCE_ID}-file-access.json",
    }
    actor = {
        "schema_version": 1,
        "task_id": THREAD_ID,
        "plugin_version": identity["plugin_version"],
        "registry_sha256": identity["registry_sha256"],
        "source_commit": identity["source_commit"],
        "workflow": "idea",
        "actors": [
            {
                "instance_id": "child-evaluator-001",
                "skill": "idea-evaluator",
                "role": "evaluator",
                "dispatch_source": "research-idea-orchestrator",
                "dispatch_mode": "delegated",
                "dispatch_trigger": "candidate_set_frozen_or_revised",
                "isolation_mode": "fresh_subagent",
                "allowed_read_roots": [f"runs/{EXECUTION_ID}"],
                "allowed_write_roots": [f"runs/{EXECUTION_ID}/reviews"],
            },
            {
                "instance_id": "writer-orchestrated-001",
                "skill": "multi-path-idea-generator",
                "role": "writer",
                "dispatch_source": "research-idea-orchestrator",
                "dispatch_mode": "orchestrated",
                "dispatch_trigger": "context_and_opportunity_map_ready_or_revision_authorized",
                "allowed_read_roots": [f"runs/{EXECUTION_ID}"],
                "allowed_write_roots": [f"runs/{EXECUTION_ID}/artifacts"],
            },
        ],
    }
    artifact = {
        "schema_version": 1,
        "task_id": THREAD_ID,
        "plugin_version": identity["plugin_version"],
        "registry_sha256": identity["registry_sha256"],
        "source_commit": identity["source_commit"],
        "workflow": "idea",
        "artifacts": [],
    }
    source_digest = sha256_bytes(scheduler_paths["source"].read_bytes())
    access = {
        "schema_version": 1,
        "task_id": THREAD_ID,
        "plugin_version": identity["plugin_version"],
        "registry_sha256": identity["registry_sha256"],
        "source_commit": identity["source_commit"],
        "workflow": "idea",
        "reads": [
            {
                "actor_instance_id": "child-evaluator-001",
                "path": logical["source"],
                "sha256": source_digest,
                "sha256_before": source_digest,
                "sha256_after": source_digest,
            }
        ],
        "writes": [],
        "source_artifact_hashes_unchanged": True,
    }
    if mutation == "actor_child_mismatch":
        actor["actors"][0]["instance_id"] = "child-evaluator-999"
    elif mutation == "missing_delegated_child":
        actor["actors"].append(
            {
                "instance_id": "child-evaluator-002",
                "skill": "idea-evaluator",
                "role": "evaluator",
                "dispatch_source": "research-idea-orchestrator",
                "dispatch_mode": "delegated",
                "dispatch_trigger": "candidate_set_frozen_or_revised",
                "isolation_mode": "fresh_subagent",
                "allowed_read_roots": [f"runs/{EXECUTION_ID}"],
                "allowed_write_roots": [f"runs/{EXECUTION_ID}/reviews"],
            }
        )
    elif mutation == "source_not_read":
        access["reads"][0].update(
            sha256="sha256:" + "0" * 64,
            sha256_before="sha256:" + "0" * 64,
            sha256_after="sha256:" + "0" * 64,
        )
    elif mutation == "source_write":
        access["writes"].append(
            {
                "actor_instance_id": "child-evaluator-001",
                "path": logical["source"],
                "sha256": source_digest,
            }
        )
    actor_bytes = write_json(support["actor"], actor)
    artifact_bytes = write_json(support["artifact"], artifact)
    access_bytes = write_json(support["access"], access)
    document = {
        "schema_version": 1,
        "platform": "codex",
        "task_id": THREAD_ID,
        "parent_task_or_thread_id": THREAD_ID,
        "observable_child_or_delegate_ids": ["child-evaluator-001"],
        "plugin_version": identity["plugin_version"],
        "registry_sha256": identity["registry_sha256"],
        "source_commit": identity["source_commit"],
        "workflow": "idea",
        "entry_mode": slot["entry_mode"],
        "case_kind": "happy",
        "final_state": "human_signoff_required",
        "automatic_external_submission": False,
        "actor_manifest": {"path": logical["actor"], "sha256": sha256_bytes(actor_bytes)},
        "artifact_index": {"path": logical["artifact"], "sha256": sha256_bytes(artifact_bytes)},
        "file_access": {"path": logical["access"], "sha256": sha256_bytes(access_bytes)},
        "scheduler_input": {
            "schema_version": 1,
            "execution_id": EXECUTION_ID,
            "public_entry": slot["public_entry"],
            "entry_mode": slot["entry_mode"],
            "source": {"path": slot["source_path"], "sha256": slot["source_sha256"]},
            "launch_prompt": {"path": slot["prompt_path"], "sha256": slot["prompt_sha256"]},
        },
        "lineage": {
            "complete": True,
            "current_artifact_ref": "primary@v001",
            "evaluated_artifact_ref": "primary@v001",
        },
        "review_state": {
            "dissent_ids": [],
            "preserved_dissent_ids": [],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
            "fatal_findings_visible": True,
        },
        "control_evidence": {
            "input_condition": None,
            "gate": None,
            "finding": None,
            "route": None,
            "continuation_artifact_ref": None,
        },
    }
    if mutation == "missing_field":
        del document["actor_manifest"]
    elif mutation == "missing_file_access":
        del document["file_access"]
    elif mutation == "wrong_source":
        document["source_commit"] = "b" * 40
    elif mutation == "wrong_entry_mode":
        document["entry_mode"] = "existing_draft"
    elif mutation == "wrong_scheduler_entry_mode":
        document["scheduler_input"]["entry_mode"] = "existing_draft"
    elif mutation == "child_id_mismatch":
        document["observable_child_or_delegate_ids"] = ["child-evaluator-999"]
    elif mutation == "outcome_oracle":
        document["expected_final_state"] = "human_signoff_required"
    elif mutation == "extra_orchestrated_child":
        document["observable_child_or_delegate_ids"].append("writer-orchestrated-001")
    support["task"] = root / "input" / "task-export.json"
    write_json(support["task"], document)
    support["source"] = scheduler_paths["source"]
    support["prompt"] = scheduler_paths["prompt"]
    support["manifest"] = scheduler_paths["manifest"]
    support["task_logical_path"] = Path(logical["task"])
    return support


def normalize(root: Path, now: datetime) -> tuple[int, dict]:
    return run(
        NORMALIZER,
        "--staging-root",
        str(root),
        "--capture-dir",
        "capture",
        "--task-export",
        "input/task-export.json",
        "--scheduler-manifest",
        "scheduler/manifest.yaml",
        "--execution-id",
        EXECUTION_ID,
        "--source-file",
        f"input/{SCHEDULER_SOURCE.name}",
        "--prompt-file",
        f"input/prompt/{SCHEDULER_PROMPT.name}",
        "--thread-id",
        THREAD_ID,
        "--evidence-id",
        EVIDENCE_ID,
        "--output",
        f"bundle/{EVIDENCE_ID}-R.json",
        "--now",
        timestamp(now),
    )


def api_asset(
    *,
    asset_id: int,
    name: str,
    payload: bytes,
    tag: str,
    updated_at: str,
) -> dict:
    return {
        "id": asset_id,
        "name": name,
        "size": len(payload),
        "digest": sha256_bytes(payload),
        "state": "uploaded",
        "url": f"https://api.github.com/repos/{REPOSITORY}/releases/assets/{asset_id}",
        "browser_download_url": f"https://github.com/{REPOSITORY}/releases/download/{tag}/{name}",
        "updated_at": updated_at,
    }


def source_ci(identity: dict[str, str], now: datetime) -> dict:
    return {
        "id": 9001,
        "workflow_id": 5001,
        "run_attempt": 1,
        "url": f"https://api.github.com/repos/{REPOSITORY}/actions/runs/9001",
        "html_url": f"https://github.com/{REPOSITORY}/actions/runs/9001",
        "repository": {"full_name": REPOSITORY},
        "actor": {"login": "preview-ci-bot"},
        "head_sha": identity["source_commit"],
        "head_branch": "main",
        "status": "completed",
        "conclusion": "success",
        "event": "push",
        "path": ".github/workflows/openai-plugin-preview.yml",
        "updated_at": timestamp(now - timedelta(minutes=12)),
    }


def release_document(tag: str, now: datetime, assets: list[dict]) -> dict:
    return {
        "id": 7001,
        "url": f"https://api.github.com/repos/{REPOSITORY}/releases/7001",
        "tag_name": tag,
        "draft": True,
        "prerelease": True,
        "created_at": timestamp(now - timedelta(minutes=20)),
        "assets": copy.deepcopy(assets),
    }


def expected_state(workflow: str, case_kind: str) -> str:
    if case_kind == "happy":
        return (
            "human_strategy_selection_required"
            if workflow == "research_polisher"
            else "human_signoff_required"
        )
    return {
        "idea": "stopped",
        "proposal": "blocked",
        "article": "blocked",
        "perspective": "stopped",
        "research_polisher": "no_defensible_option",
    }[workflow]


def build_ten_slot_collection(
    root: Path,
    *,
    first_receipt: dict,
    identity: dict[str, str],
) -> Path:
    manifest = yaml.safe_load((root / "scheduler" / "manifest.yaml").read_text(encoding="utf-8"))
    receipt_paths: list[str] = []
    for offset, slot in enumerate(manifest["slots"]):
        execution = slot["execution_id"]
        if execution == EXECUTION_ID:
            receipt = copy.deepcopy(first_receipt)
        else:
            receipt = copy.deepcopy(first_receipt)
            receipt["receipt_id"] = f"synthetic-non-gating-{execution}"
            receipt["workflow"] = slot["workflow"]
            receipt["entry_mode"] = slot["entry_mode"]
            receipt["case_kind"] = slot["case_kind"]
            state = expected_state(slot["workflow"], slot["case_kind"])
            receipt["expected_final_state"] = state
            receipt["final_state"] = state
            parent = f"thread-{execution}"
            child = f"child-{execution}"
            task_digest = "sha256:" + hashlib.sha256(f"task:{execution}".encode()).hexdigest()
            receipt["binding"]["task_export"] = {
                "platform": "codex",
                "task_id": parent,
                "entry_mode": slot["entry_mode"],
                "path": f"runs/{execution}/capture/task-export.json",
                "sha256": task_digest,
            }
            for field, stem in (
                ("actor_manifest", "actor"),
                ("artifact_index", "artifact"),
                ("file_access", "access"),
            ):
                receipt["binding"][field] = {
                    "path": f"runs/{execution}/capture/{stem}.json",
                    "sha256": "sha256:"
                    + hashlib.sha256(f"{field}:{execution}".encode()).hexdigest(),
                }
            scheduler = receipt["binding"]["scheduler_input"]
            scheduler.update(
                slot=slot["slot"],
                execution_id=execution,
                workflow=slot["workflow"],
                case_kind=slot["case_kind"],
                public_entry=slot["public_entry"],
                entry_mode=slot["entry_mode"],
                capture_profile=slot["capture_profile"],
                source={"path": slot["source_path"], "sha256": slot["source_sha256"]},
                launch_prompt={"path": slot["prompt_path"], "sha256": slot["prompt_sha256"]},
                parent_task_or_thread_id=parent,
                observable_child_or_delegate_ids=[child],
                plugin={
                    "name": "research-skills-openai",
                    "version": identity["plugin_version"],
                    "source_commit": identity["source_commit"],
                    "registry_sha256": identity["registry_sha256"],
                },
            )
        path = root / "candidates" / f"{execution}-receipt.json"
        write_json(path, receipt)
        receipt_paths.append(str(path.relative_to(root)).replace("\\", "/"))
    write_json(
        root / "candidates" / "receipt-plan.json",
        {
            "schema_version": "openai-phase7-receipt-plan/v1",
            "receipts": receipt_paths,
        },
    )
    output = root / "bundle" / "phase7-runtime-receipts.json"
    code, result = run(
        RUNTIME_BUILDER,
        "collection",
        "--staging-root",
        str(root),
        "--plan",
        "candidates/receipt-plan.json",
        "--scheduler-manifest",
        "scheduler/manifest.yaml",
        "--output",
        str(output.relative_to(root)).replace("\\", "/"),
    )
    require(code == 0 and result["built"] is True, f"ten-slot collection: {result}")
    collection = read_json(output)
    require(len(collection["receipts"]) == 10, "ten scheduler slots collected")
    require(
        {item["binding"]["scheduler_input"]["entry_mode"] for item in collection["receipts"]}
        >= {"standard", "existing_draft", "fast_track_draft", "full"},
        "entry modes preserved",
    )
    return output


def build_happy_fixture(root: Path, now: datetime) -> dict[str, object]:
    identity = production_identity()
    scheduler_paths = stage_scheduler_inputs(root)
    prompt_text = scheduler_paths["prompt"].read_text(encoding="utf-8")
    write_capture(root, now=now, prompt_text=prompt_text)
    support = write_task_export(root, identity, scheduler_paths=scheduler_paths)
    code, normalized = normalize(root, now)
    require(code == 0 and normalized["normalized"] is True, f"normalizer happy: {normalized}")
    require(normalized["gate_eligible"] is False and normalized["accepted"] is False, "R non-gating")
    raw_path = root / "bundle" / f"{EVIDENCE_ID}-R.json"
    raw_document = read_json(raw_path)
    require(raw_document["schema_version"] == 1, "R remains runtime task-export schema v1")
    require(raw_document["task_id"] == THREAD_ID, "R task identity")
    require("capture_provenance" in raw_document and "source_files" in raw_document, "R embeds capture")
    require(raw_document["scheduler_binding"]["execution_id"] == EXECUTION_ID, "R scheduler execution")
    require(raw_document["scheduler_binding"]["entry_mode"] == "standard", "R scheduler entry mode")
    require(raw_document["scheduler_binding"]["manifest_visible_to_task"] is False, "manifest hidden")

    receipt_name = f"{EVIDENCE_ID}-receipt.json"
    code, receipt_result = run(
        RUNTIME_BUILDER,
        "receipt",
        "--staging-root",
        str(root),
        "--raw-export",
        f"bundle/{raw_path.name}",
        "--task-logical-path",
        str(support["task_logical_path"]).replace("\\", "/"),
        "--actor-manifest",
        str(support["actor"].relative_to(root)).replace("\\", "/"),
        "--artifact-index",
        str(support["artifact"].relative_to(root)).replace("\\", "/"),
        "--file-access",
        str(support["access"].relative_to(root)).replace("\\", "/"),
        "--output",
        f"bundle/{receipt_name}",
        "--now",
        timestamp(now),
    )
    require(code == 0 and receipt_result["built"] is True, f"receipt build: {receipt_result}")
    receipt = read_json(root / "bundle" / receipt_name)
    require(receipt["binding"]["scheduler_input"]["entry_mode"] == "standard", "receipt entry mode")
    collection_path = build_ten_slot_collection(
        root,
        first_receipt=receipt,
        identity=identity,
    )

    tag = f"research-skills-openai-v{PLUGIN_VERSION}-evidence"
    raw_asset = api_asset(
        asset_id=101,
        name=raw_path.name,
        payload=raw_path.read_bytes(),
        tag=tag,
        updated_at=timestamp(now - timedelta(minutes=5)),
    )
    api = root / "api"
    write_json(api / "raw-asset.json", raw_asset)
    write_json(api / "source-ci.json", source_ci(identity, now))
    write_json(api / "release.json", release_document(tag, now, [raw_asset]))
    envelope_name = f"{EVIDENCE_ID}-E.json"
    code, envelope_result = run(
        BUILDER,
        "envelope",
        "--staging-root",
        str(root),
        "--raw-export",
        f"bundle/{raw_path.name}",
        "--release-snapshot",
        "api/release.json",
        "--workflow-run-snapshot",
        "api/source-ci.json",
        "--raw-asset-snapshot",
        "api/raw-asset.json",
        "--output",
        f"bundle/{envelope_name}",
        "--now",
        timestamp(now),
    )
    require(code == 0 and envelope_result["built"] is True, f"E build: {envelope_result}")
    require(envelope_result["node"] == "E" and not envelope_result["accepted"], "E non-gating")

    envelope_path = root / "bundle" / envelope_name
    envelope_asset = api_asset(
        asset_id=102,
        name=envelope_name,
        payload=envelope_path.read_bytes(),
        tag=tag,
        updated_at=timestamp(now - timedelta(minutes=3)),
    )
    write_json(api / "envelope-asset.json", envelope_asset)
    write_json(api / "release.json", release_document(tag, now, [raw_asset, envelope_asset]))
    verifier_name = f"{EVIDENCE_ID}-V.json"
    verifier_env = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_REPOSITORY": REPOSITORY,
        "GITHUB_SHA": identity["source_commit"],
        "GITHUB_EVENT_NAME": "workflow_dispatch",
        "GITHUB_REF_NAME": "main",
        "GITHUB_WORKFLOW_REF": f"{REPOSITORY}/.github/workflows/openai-preview-draft-bundle-verifier.yml@refs/heads/main",
        "GITHUB_RUN_ID": "9101",
        "GITHUB_RUN_ATTEMPT": "1",
        "GITHUB_ACTOR": "draft-verifier-bot",
    }
    code, verifier_result = run(
        DRAFT_VERIFIER,
        "--staging-root",
        str(root),
        "--raw-export",
        f"bundle/{raw_path.name}",
        "--envelope",
        f"bundle/{envelope_name}",
        "--release-snapshot",
        "api/release.json",
        "--source-ci-run-snapshot",
        "api/source-ci.json",
        "--raw-asset-snapshot",
        "api/raw-asset.json",
        "--envelope-asset-snapshot",
        "api/envelope-asset.json",
        "--output",
        f"bundle/{verifier_name}",
        env=verifier_env,
    )
    require(code == 0 and verifier_result["verified"] is True, f"V build: {verifier_result}")
    require(not verifier_result["gate_eligible"] and not verifier_result["accepted"], "V non-gating")

    verifier_path = root / "bundle" / verifier_name
    verifier_asset = api_asset(
        asset_id=103,
        name=verifier_name,
        payload=verifier_path.read_bytes(),
        tag=tag,
        updated_at=timestamp(now - timedelta(minutes=1)),
    )
    write_json(api / "v-asset.json", verifier_asset)
    source_asset_path = root / "bundle" / f"{EVIDENCE_ID}-frozen-source.md"
    source_asset_path.write_bytes(support["source"].read_bytes())
    supporting_paths = {
        "actor": support["actor"],
        "artifact": support["artifact"],
        "access": support["access"],
        "source": source_asset_path,
        "collection": collection_path,
    }
    support_assets: dict[str, dict] = {}
    for asset_id, (label, path) in enumerate(supporting_paths.items(), start=104):
        asset = api_asset(
            asset_id=asset_id,
            name=path.name,
            payload=path.read_bytes(),
            tag=tag,
            updated_at=timestamp(now - timedelta(seconds=45 - asset_id + 104)),
        )
        support_assets[label] = asset
        write_json(api / f"{label}-asset.json", asset)
    pre_workspace_assets = [raw_asset, envelope_asset, verifier_asset, *support_assets.values()]
    write_json(api / "release.json", release_document(tag, now, pre_workspace_assets))
    workspace_map = {
        "schema_version": "openai-phase7-workspace-asset-map/v1",
        "bundle_id": "phase7-p7-l01-workspace",
        "runtime_receipts": {
            "logical_path": "phase7/runtime-receipts.json",
            "path": str(collection_path.relative_to(root)).replace("\\", "/"),
            "github_asset_snapshot": "api/collection-asset.json",
        },
        "files": [
            {
                "logical_path": str(support["task_logical_path"]).replace("\\", "/"),
                "path": f"bundle/{raw_path.name}",
                "github_asset_snapshot": "api/raw-asset.json",
            },
            {
                "logical_path": raw_document["actor_manifest"]["path"],
                "path": str(support["actor"].relative_to(root)).replace("\\", "/"),
                "github_asset_snapshot": "api/actor-asset.json",
            },
            {
                "logical_path": raw_document["artifact_index"]["path"],
                "path": str(support["artifact"].relative_to(root)).replace("\\", "/"),
                "github_asset_snapshot": "api/artifact-asset.json",
            },
            {
                "logical_path": raw_document["file_access"]["path"],
                "path": str(support["access"].relative_to(root)).replace("\\", "/"),
                "github_asset_snapshot": "api/access-asset.json",
            },
            {
                "logical_path": f"runs/{EXECUTION_ID}/input/{SCHEDULER_SOURCE.name}",
                "path": str(source_asset_path.relative_to(root)).replace("\\", "/"),
                "github_asset_snapshot": "api/source-asset.json",
            },
        ],
    }
    write_json(api / "workspace-map.json", workspace_map)
    workspace_name = f"{EVIDENCE_ID}-workspace-manifest.json"
    code, workspace_result = run(
        RUNTIME_BUILDER,
        "workspace-manifest",
        "--staging-root",
        str(root),
        "--collection",
        str(collection_path.relative_to(root)).replace("\\", "/"),
        "--receipt-id",
        EVIDENCE_ID,
        "--asset-map",
        "api/workspace-map.json",
        "--release-snapshot",
        "api/release.json",
        "--output",
        f"bundle/{workspace_name}",
        "--now",
        timestamp(now),
    )
    require(code == 0 and workspace_result["built"] is True, f"workspace manifest: {workspace_result}")
    workspace_path = root / "bundle" / workspace_name
    workspace_asset = api_asset(
        asset_id=109,
        name=workspace_name,
        payload=workspace_path.read_bytes(),
        tag=tag,
        updated_at=timestamp(now - timedelta(seconds=20)),
    )
    write_json(api / "workspace-asset.json", workspace_asset)
    final_assets = [*pre_workspace_assets, workspace_asset]
    write_json(api / "release.json", release_document(tag, now, final_assets))
    plan = {
        "schema_version": "openai-preview-mini-bundle-plan/v1",
        "assets": [
            {"role": "R", "path": f"bundle/{raw_path.name}", "github_asset_snapshot": "api/raw-asset.json"},
            {"role": "E", "path": f"bundle/{envelope_name}", "github_asset_snapshot": "api/envelope-asset.json"},
            {"role": "V", "path": f"bundle/{verifier_name}", "github_asset_snapshot": "api/v-asset.json"},
            *[
                {
                    "role": "supporting",
                    "evidence_kind": "supporting_file",
                    "path": str(path.relative_to(root)).replace("\\", "/"),
                    "github_asset_snapshot": f"api/{label}-asset.json",
                }
                for label, path in supporting_paths.items()
            ],
            {
                "role": "supporting",
                "evidence_kind": "supporting_file",
                "path": f"bundle/{workspace_name}",
                "github_asset_snapshot": "api/workspace-asset.json",
            },
        ],
    }
    write_json(api / "plan.json", plan)
    index_name = f"{EVIDENCE_ID}-I.json"
    code, index_result = run(
        BUILDER,
        "index",
        "--staging-root",
        str(root),
        "--plan",
        "api/plan.json",
        "--release-snapshot",
        "api/release.json",
        "--workflow-run-snapshot",
        "api/source-ci.json",
        "--output",
        f"bundle/{index_name}",
        "--now",
        timestamp(now),
    )
    require(code == 0 and index_result["node"] == "I", f"I build: {index_result}")
    require(index_result["index_self_referenced"] is False, "I self-reference absent")
    index = read_json(root / "bundle" / index_name)
    require(index_name not in {item["name"] for item in index["assets"]}, "I is not indexed by itself")
    require(index["github_witness"]["workflow_event"] == "push", "source CI push witness")
    require(index["github_witness"]["workflow_witness_role"] == "source_commit_main_ci", "source CI role")
    write_json(api / "expected-identity.json", {"source_identity": identity})
    code, offline = run(
        OFFLINE_VALIDATOR,
        "--asset-index",
        str(root / "bundle" / index_name),
        "--asset-dir",
        str(root / "bundle"),
        "--envelope",
        str(envelope_path),
        "--expected-source-identity",
        str(api / "expected-identity.json"),
        "--now",
        timestamp(now),
    )
    require(code == 0 and offline["integrity_valid"] is True, f"offline integrity: {offline}")
    require(not offline["gate_eligible"] and not offline["accepted"], "offline remains non-gating")
    return {"identity": identity, "plan": plan, "index_name": index_name}


def expect_failure(code: int, output: dict, expected: set[str], label: str) -> None:
    actual = output.get("error", {}).get("code")
    require(code != 0 and actual in expected, f"{label}: {actual}, output={output}")
    require(output.get("gate_eligible") is False and output.get("accepted") is False, f"{label}: fail closed")


def normalization_mutations(identity: dict[str, str], now: datetime) -> list[str]:
    guards: list[str] = []
    for mutation, expected in (
        ("forged_claim", {"capture_contract_mismatch"}),
        ("missing_field", {"invalid_type"}),
        ("digest_mismatch", {"source_digest_mismatch"}),
        ("extra_user_message", {"unexpected_platform_user_message_count"}),
        ("missing_child_binding", {"platform_child_id_binding_unavailable"}),
    ):
        with tempfile.TemporaryDirectory(prefix=f"capture-{mutation}-") as temp:
            root = Path(temp)
            scheduler = stage_scheduler_inputs(root)
            write_capture(
                root,
                now=now,
                prompt_text=scheduler["prompt"].read_text(encoding="utf-8"),
                mutation=mutation,
            )
            write_task_export(root, identity, scheduler_paths=scheduler)
            expect_failure(*normalize(root, now), expected, mutation)
            guards.append(mutation)
    for mutation, expected in (
        ("missing_field", {"task_export_missing_field"}),
        ("missing_file_access", {"task_export_missing_field"}),
        ("wrong_source", {"task_export_source_mismatch"}),
        ("wrong_entry_mode", {"scheduler_slot_classification_mismatch"}),
        ("wrong_scheduler_entry_mode", {"scheduler_input_mismatch"}),
        ("child_id_mismatch", {"platform_child_id_mismatch"}),
        ("outcome_oracle", {"scheduler_outcome_oracle_exposed"}),
    ):
        with tempfile.TemporaryDirectory(prefix=f"task-{mutation}-") as temp:
            root = Path(temp)
            scheduler = stage_scheduler_inputs(root)
            write_capture(
                root,
                now=now,
                prompt_text=scheduler["prompt"].read_text(encoding="utf-8"),
            )
            write_task_export(root, identity, scheduler_paths=scheduler, mutation=mutation)
            expect_failure(*normalize(root, now), expected, f"task {mutation}")
            guards.append(f"task_{mutation}")
    with tempfile.TemporaryDirectory(prefix="scheduler-source-drift-") as temp:
        root = Path(temp)
        scheduler = stage_scheduler_inputs(root)
        write_capture(root, now=now, prompt_text=scheduler["prompt"].read_text(encoding="utf-8"))
        write_task_export(root, identity, scheduler_paths=scheduler)
        scheduler["source"].write_bytes(scheduler["source"].read_bytes() + b"\nunauthorized drift\n")
        expect_failure(*normalize(root, now), {"scheduler_source_digest_mismatch"}, "source drift")
        guards.append("scheduler_source_drift")
    with tempfile.TemporaryDirectory(prefix="scheduler-manifest-drift-") as temp:
        root = Path(temp)
        scheduler = stage_scheduler_inputs(root)
        write_capture(root, now=now, prompt_text=scheduler["prompt"].read_text(encoding="utf-8"))
        write_task_export(root, identity, scheduler_paths=scheduler)
        scheduler["manifest"].write_bytes(scheduler["manifest"].read_bytes() + b"\n")
        expect_failure(*normalize(root, now), {"scheduler_manifest_not_committed"}, "manifest drift")
        guards.append("scheduler_manifest_drift")
    with tempfile.TemporaryDirectory(prefix="capture-path-escape-") as temp:
        root = Path(temp)
        scheduler = stage_scheduler_inputs(root)
        write_capture(root, now=now, prompt_text=scheduler["prompt"].read_text(encoding="utf-8"))
        write_task_export(root, identity, scheduler_paths=scheduler)
        code, output = run(
            NORMALIZER,
            "--staging-root",
            str(root),
            "--capture-dir",
            "capture",
            "--task-export",
            "../task-export.json",
            "--scheduler-manifest",
            "scheduler/manifest.yaml",
            "--execution-id",
            EXECUTION_ID,
            "--source-file",
            f"input/{SCHEDULER_SOURCE.name}",
            "--prompt-file",
            f"input/prompt/{SCHEDULER_PROMPT.name}",
            "--thread-id",
            THREAD_ID,
            "--evidence-id",
            EVIDENCE_ID,
            "--output",
            "bundle/R.json",
            "--now",
            timestamp(now),
        )
        expect_failure(code, output, {"unsafe_relative_path"}, "path escape")
        guards.append("path_escape")
    with tempfile.TemporaryDirectory(prefix="capture-path-reuse-") as temp:
        root = Path(temp)
        scheduler = stage_scheduler_inputs(root)
        write_capture(root, now=now, prompt_text=scheduler["prompt"].read_text(encoding="utf-8"))
        code, output = run(
            NORMALIZER,
            "--staging-root",
            str(root),
            "--capture-dir",
            "capture",
            "--task-export",
            "capture/capture.json",
            "--scheduler-manifest",
            "scheduler/manifest.yaml",
            "--execution-id",
            EXECUTION_ID,
            "--source-file",
            f"input/{SCHEDULER_SOURCE.name}",
            "--prompt-file",
            f"input/prompt/{SCHEDULER_PROMPT.name}",
            "--thread-id",
            THREAD_ID,
            "--evidence-id",
            EVIDENCE_ID,
            "--output",
            "bundle/R.json",
            "--now",
            timestamp(now),
        )
        expect_failure(code, output, {"path_reused", "file_reused"}, "path reuse")
        guards.append("path_reuse")
    return guards


def receipt_mutations(identity: dict[str, str], now: datetime) -> list[str]:
    guards: list[str] = []
    for mutation, expected in (
        ("actor_child_mismatch", {"observable_child_actor_mismatch"}),
        ("missing_delegated_child", {"observable_child_actor_mismatch"}),
        ("extra_orchestrated_child", {"observable_child_actor_mismatch"}),
        ("source_not_read", {"scheduler_source_not_read"}),
        ("source_write", {"scheduler_source_write_detected"}),
    ):
        with tempfile.TemporaryDirectory(prefix=f"receipt-{mutation}-") as temp:
            root = Path(temp)
            scheduler = stage_scheduler_inputs(root)
            write_capture(
                root,
                now=now,
                prompt_text=scheduler["prompt"].read_text(encoding="utf-8"),
                mutation=mutation if mutation == "extra_orchestrated_child" else None,
            )
            support = write_task_export(
                root,
                identity,
                scheduler_paths=scheduler,
                mutation=mutation,
            )
            code, normalized = normalize(root, now)
            require(code == 0 and normalized["normalized"] is True, f"{mutation} R setup: {normalized}")
            code, result = run(
                RUNTIME_BUILDER,
                "receipt",
                "--staging-root",
                str(root),
                "--raw-export",
                f"bundle/{EVIDENCE_ID}-R.json",
                "--task-logical-path",
                str(support["task_logical_path"]).replace("\\", "/"),
                "--actor-manifest",
                str(support["actor"].relative_to(root)).replace("\\", "/"),
                "--artifact-index",
                str(support["artifact"].relative_to(root)).replace("\\", "/"),
                "--file-access",
                str(support["access"].relative_to(root)).replace("\\", "/"),
                "--output",
                f"bundle/{mutation}-receipt.json",
                "--now",
                timestamp(now),
            )
            expect_failure(code, result, expected, f"receipt {mutation}")
            guards.append(f"receipt_{mutation}")
    return guards


def collection_mutations(happy_root: Path) -> list[str]:
    guards: list[str] = []

    def clone(label: str) -> Path:
        destination = happy_root.parent / f"collection-{label}"
        shutil.copytree(happy_root, destination)
        return destination

    cases: list[tuple[Path, set[str], str]] = []
    root = clone("missing-slot")
    plan = read_json(root / "candidates" / "receipt-plan.json")
    plan["receipts"].pop()
    write_json(root / "candidates" / "receipt-plan.json", plan)
    cases.append((root, {"receipt_count"}, "missing_slot"))

    root = clone("entry-mode")
    receipt_path = root / "candidates" / "p7-l04-receipt.json"
    receipt = read_json(receipt_path)
    receipt["binding"]["scheduler_input"]["entry_mode"] = "standard"
    write_json(receipt_path, receipt)
    cases.append((root, {"scheduler_binding_mismatch"}, "entry_mode_mismatch"))

    root = clone("child-reuse")
    receipt_path = root / "candidates" / "p7-l02-receipt.json"
    receipt = read_json(receipt_path)
    receipt["binding"]["scheduler_input"]["observable_child_or_delegate_ids"] = [
        "child-evaluator-001"
    ]
    write_json(receipt_path, receipt)
    cases.append((root, {"scheduler_child_id_reused"}, "child_id_reuse"))

    root = clone("source-digest")
    receipt_path = root / "candidates" / "p7-l02-receipt.json"
    receipt = read_json(receipt_path)
    receipt["binding"]["scheduler_input"]["source"]["sha256"] = "sha256:" + "0" * 64
    write_json(receipt_path, receipt)
    cases.append((root, {"scheduler_source_binding_mismatch"}, "source_digest_mismatch"))

    root = clone("support-reuse")
    first = read_json(root / "candidates" / "p7-l01-receipt.json")
    receipt_path = root / "candidates" / "p7-l02-receipt.json"
    receipt = read_json(receipt_path)
    receipt["binding"]["actor_manifest"] = copy.deepcopy(first["binding"]["actor_manifest"])
    write_json(receipt_path, receipt)
    cases.append((root, {"receipt_support_reused"}, "support_path_digest_reuse"))

    root = clone("task-path")
    receipt_path = root / "candidates" / "p7-l02-receipt.json"
    receipt = read_json(receipt_path)
    receipt["binding"]["task_export"]["path"] = "../task-export.json"
    write_json(receipt_path, receipt)
    cases.append((root, {"unsafe_relative_path"}, "task_path_escape"))

    root = clone("manifest-drift")
    manifest_path = root / "scheduler" / "manifest.yaml"
    manifest_path.write_bytes(manifest_path.read_bytes() + b"\n")
    cases.append((root, {"scheduler_manifest_not_committed"}, "collection_manifest_drift"))

    for root, expected, label in cases:
        code, result = run(
            RUNTIME_BUILDER,
            "collection",
            "--staging-root",
            str(root),
            "--plan",
            "candidates/receipt-plan.json",
            "--scheduler-manifest",
            "scheduler/manifest.yaml",
            "--output",
            f"bundle/{label}.json",
        )
        expect_failure(code, result, expected, label)
        guards.append(label)
    return guards


def builder_mutations(happy_root: Path, now: datetime) -> list[str]:
    guards: list[str] = []

    def clone(label: str) -> Path:
        destination = happy_root.parent / label
        shutil.copytree(happy_root, destination)
        for path in (destination / "bundle").glob("*-I.json"):
            path.unlink()
        return destination

    cases = []
    root = clone("escape")
    plan = read_json(root / "api" / "plan.json")
    plan["assets"][0]["path"] = "../outside.json"
    write_json(root / "api" / "plan.json", plan)
    cases.append((root, {"unsafe_relative_path"}, "plan_path_escape"))

    root = clone("reuse")
    plan = read_json(root / "api" / "plan.json")
    plan["assets"][2]["github_asset_snapshot"] = plan["assets"][1]["github_asset_snapshot"]
    write_json(root / "api" / "plan.json", plan)
    cases.append((root, {"path_reused"}, "snapshot_path_reuse"))

    root = clone("preassigned")
    plan = read_json(root / "api" / "plan.json")
    plan["assets"][0]["asset_id"] = 999
    write_json(root / "api" / "plan.json", plan)
    cases.append((root, {"plan_asset_fields"}, "preassigned_fake_id"))

    root = clone("missing-v")
    plan = read_json(root / "api" / "plan.json")
    plan["assets"] = [item for item in plan["assets"] if item["role"] != "V"]
    write_json(root / "api" / "plan.json", plan)
    cases.append((root, {"required_role_count"}, "missing_v"))

    root = clone("digest")
    snapshot = read_json(root / "api" / "v-asset.json")
    snapshot["digest"] = "sha256:" + "0" * 64
    write_json(root / "api" / "v-asset.json", snapshot)
    release = read_json(root / "api" / "release.json")
    next(item for item in release["assets"] if item["id"] == snapshot["id"])["digest"] = snapshot["digest"]
    write_json(root / "api" / "release.json", release)
    cases.append((root, {"asset_payload_mismatch"}, "digest_mismatch"))

    root = clone("forged-v")
    v_path = next((root / "bundle").glob("*-V.json"))
    report = read_json(v_path)
    report["independent"] = False
    payload = write_json(v_path, report)
    snapshot = read_json(root / "api" / "v-asset.json")
    snapshot["digest"] = sha256_bytes(payload)
    snapshot["size"] = len(payload)
    write_json(root / "api" / "v-asset.json", snapshot)
    release = read_json(root / "api" / "release.json")
    release_asset = next(item for item in release["assets"] if item["id"] == snapshot["id"])
    release_asset.update(digest=snapshot["digest"], size=snapshot["size"])
    write_json(root / "api" / "release.json", release)
    cases.append((root, {"verifier_report_binding_mismatch"}, "forged_v_independence"))

    for root, expected, label in cases:
        code, output = run(
            BUILDER,
            "index",
            "--staging-root",
            str(root),
            "--plan",
            "api/plan.json",
            "--release-snapshot",
            "api/release.json",
            "--workflow-run-snapshot",
            "api/source-ci.json",
            "--output",
            f"bundle/{label}-I.json",
            "--now",
            timestamp(now),
        )
        expect_failure(code, output, expected, label)
        guards.append(label)
    return guards


def live_verifier_requery_guards(happy_root: Path, now: datetime) -> list[str]:
    spec = importlib.util.spec_from_file_location(
        "preview_live_verifier_requery_test",
        REPO / "tests" / "openai_phase8" / "verify_preview_evidence.py",
    )
    require(spec is not None and spec.loader is not None, "load live verifier module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report_path = next((happy_root / "bundle").glob("*-V.json"))
    report = read_json(report_path)
    execution = report["execution"]
    live = {
        "id": execution["workflow_run_id"],
        "run_attempt": execution["run_attempt"],
        "path": ".github/workflows/openai-preview-draft-bundle-verifier.yml",
        "event": "workflow_dispatch",
        "head_sha": report["source_identity"]["source_commit"],
        "head_branch": "main",
        "status": "completed",
        "conclusion": "success",
        "repository": {"full_name": REPOSITORY},
        "actor": {"login": execution["actor"]},
        "run_started_at": timestamp(now - timedelta(minutes=1)),
        "updated_at": timestamp(now + timedelta(minutes=1)),
    }

    def query(url: str, *, binary: bool) -> dict:
        require(
            url
            == f"https://api.github.com/repos/{REPOSITORY}/actions/runs/{execution['workflow_run_id']}"
            and binary is False,
            "live verifier requery URL",
        )
        return live

    module.github_request = query
    module.validate_draft_verifier_execution(
        report_payload=report_path.read_bytes(),
        repository=REPOSITORY,
        source_commit=report["source_identity"]["source_commit"],
        source_ci_run_id=9001,
    )
    live["conclusion"] = "failure"
    try:
        module.validate_draft_verifier_execution(
            report_payload=report_path.read_bytes(),
            repository=REPOSITORY,
            source_commit=report["source_identity"]["source_commit"],
            source_ci_run_id=9001,
        )
    except module.VerificationError as exc:
        require("workflow witness mismatch" in str(exc), "failed V workflow rejection")
    else:
        raise AssertionError("failed V workflow run was accepted")
    return ["live_requeries_draft_v_workflow", "failed_draft_v_workflow_rejected"]


def execute_workflow_python_guards(text: str) -> list[str]:
    def command_with(marker: str) -> str:
        line = next(line.strip() for line in text.splitlines() if "python -c '" in line and marker in line)
        prefix = "python -c '"
        require(line.startswith(prefix) and line.endswith("'"), f"extract workflow command: {marker}")
        return line[len(prefix) : -1]

    with tempfile.TemporaryDirectory(prefix="draft-workflow-snippets-") as temp:
        root = Path(temp)
        (root / "api").mkdir(parents=True)
        release = {
            "draft": True,
            "prerelease": True,
            "assets": [
                {"id": 1, "name": "R.json"},
                {"id": 2, "name": "E.json"},
            ],
        }
        write_json(root / "api" / "release.json", release)
        environment = {
            **os.environ,
            "STAGING_ROOT": str(root),
            "RAW_NAME": "R.json",
            "ENVELOPE_NAME": "E.json",
        }
        completed = subprocess.run(
            [sys.executable, "-c", command_with("release must remain a draft prerelease")],
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        require(completed.returncode == 0, f"release extraction snippet: {completed.stderr}")
        require(
            (root / "api" / "raw-asset.json").is_file()
            and (root / "api" / "envelope-asset.json").is_file(),
            "success path executed statements after release guard",
        )
        write_json(
            root / "api" / "release-after-v.json",
            {"assets": [{"id": 3, "name": "V.json"}]},
        )
        completed = subprocess.run(
            [sys.executable, "-c", command_with("uploaded V did not resolve exactly once")],
            env={**environment, "VERIFIER_NAME": "V.json"},
            check=False,
            capture_output=True,
            text=True,
        )
        require(completed.returncode == 0, f"V extraction snippet: {completed.stderr}")
        require((root / "api" / "v-asset.json").is_file(), "V API snapshot was written")
    return ["draft_release_snippet_executes", "draft_v_snapshot_snippet_executes"]


def workflow_guards() -> list[str]:
    text = WORKFLOW.read_text(encoding="utf-8")
    for required in (
        "workflow_dispatch:",
        "permissions:\n  actions: read\n  contents: write",
        "release must remain a draft prerelease",
        "gh api -H \"Accept: application/octet-stream\"",
        "verify_openai_preview_draft_bundle.py",
        "gh release upload",
        "V asset name already exists",
        "overwrite: false",
    ):
        require(required in text, f"draft workflow missing guard: {required}")
    require("--clobber" not in text, "draft workflow must not overwrite V")
    dangerous = re_find_success_exit_followed_by_statement(text)
    require(not dangerous, f"successful sys.exit short-circuits workflow extraction: {dangerous}")
    return [
        "draft_download_exact_r_e",
        "draft_no_clobber",
        "no_success_exit_short_circuit",
        *execute_workflow_python_guards(text),
    ]


def re_find_success_exit_followed_by_statement(text: str) -> list[str]:
    import re

    return re.findall(r"sys\.exit\([^\n]*else 0\);\s*[^'\n]+", text)


def main() -> int:
    global ISOLATED_GIT_ENV
    now = datetime.now(timezone.utc).replace(microsecond=0)
    with tempfile.TemporaryDirectory(prefix="preview-evidence-clean-git-") as git_temp:
        ISOLATED_GIT_ENV = initialize_isolated_clean_git(Path(git_temp) / "git")
        identity = production_identity()
        guards = normalization_mutations(identity, now)
        guards.extend(receipt_mutations(identity, now))
        parent = Path(git_temp) / "bundles"
        parent.mkdir()
        happy = parent / "happy"
        happy.mkdir()
        build_happy_fixture(happy, now)
        guards.extend(live_verifier_requery_guards(happy, now))
        guards.extend(builder_mutations(happy, now))
        guards.extend(collection_mutations(happy))
        guards.extend(workflow_guards())
    require(len(guards) == 41, f"expected 41 mutation/static guards, got {len(guards)}")
    print("OpenAI Preview capture normalizer and mini-bundle tests passed")
    print(f"guards: {len(guards)}; R/E/V/I happy path plus {', '.join(guards)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
