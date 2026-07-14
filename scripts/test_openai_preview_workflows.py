#!/usr/bin/env python3
"""Offline structural tests for the OpenAI Preview GitHub workflows."""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any

import yaml

from generate_openai_release_ledger import (
    VALIDATION_CONTRACT_FILES,
    validation_contract_paths,
)


REPO = Path(__file__).resolve().parents[1]
MAIN_PATH = REPO / ".github" / "workflows" / "openai-plugin-preview.yml"
EVIDENCE_PATH = REPO / ".github" / "workflows" / "openai-preview-evidence.yml"
ACCEPTED_PATH = (
    REPO / ".github" / "workflows" / "openai-preview-accepted-evidence.yml"
)
CONSUMER_PATH = (
    REPO
    / ".github"
    / "workflows"
    / "openai-preview-accepted-summary-consumer.yml"
)
DRAFT_VERIFIER_PATH = (
    REPO / ".github" / "workflows" / "openai-preview-draft-bundle-verifier.yml"
)
PINNED_ACTION_RE = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
RUNNER_CONTEXT_RE = re.compile(r"\brunner\b", re.IGNORECASE)


class WorkflowViolation(AssertionError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise WorkflowViolation(code, message)


def load(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    document = yaml.load(text, Loader=yaml.BaseLoader)
    require(isinstance(document, dict), "workflow_root", str(path))
    return document, text


def jobs(document: dict[str, Any]) -> list[dict[str, Any]]:
    value = document.get("jobs", {})
    require(isinstance(value, dict) and bool(value), "workflow_jobs", "jobs")
    result = [item for item in value.values() if isinstance(item, dict)]
    require(len(result) == len(value), "workflow_jobs", "job mappings")
    return result


def steps(document: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for job in jobs(document):
        raw_steps = job.get("steps", [])
        require(isinstance(raw_steps, list), "workflow_steps", "steps")
        require(
            all(isinstance(item, dict) for item in raw_steps),
            "workflow_steps",
            "step mappings",
        )
        result.extend(raw_steps)
    return result


def command_blob(document: dict[str, Any]) -> str:
    return "\n".join(str(item.get("run", "")) for item in steps(document))


def validate_permissions(
    document: dict[str, Any], expected: dict[str, str]
) -> None:
    require(
        document.get("permissions") == expected,
        "workflow_permissions",
        f"top-level permissions must be exactly {expected}",
    )
    for job in jobs(document):
        if "permissions" in job:
            require(
                job.get("permissions") == expected,
                "workflow_permissions",
                f"job permissions must be exactly {expected}",
            )


def validate_action_pins(document: dict[str, Any]) -> None:
    action_steps = [item for item in steps(document) if "uses" in item]
    require(bool(action_steps), "workflow_action_pin", "no action steps")
    for step in action_steps:
        uses = str(step.get("uses", ""))
        require(
            PINNED_ACTION_RE.fullmatch(uses) is not None,
            "workflow_action_pin",
            uses,
        )


def validate_main(document: dict[str, Any], text: str) -> None:
    validate_permissions(document, {"actions": "read", "contents": "read"})
    validate_action_pins(document)
    main_jobs = document.get("jobs", {})
    require(
        isinstance(main_jobs, dict)
        and set(main_jobs) == {"validate"}
        and isinstance(main_jobs.get("validate"), dict)
        and main_jobs["validate"].get("name") == "OpenAI Plugin Preview / validate",
        "main_required_check_name",
        "the protected status-check context must equal the actual GitHub check-run name",
    )
    triggers = document.get("on", {})
    require(
        isinstance(triggers, dict)
        and {"push", "pull_request", "workflow_dispatch"} <= set(triggers),
        "main_triggers",
        "push, pull_request, and workflow_dispatch are required",
    )
    commands = command_blob(document)
    required = {
        "python scripts/check_openai_version_bump.py": "installable behavior version guard",
        "python scripts/normalize_openai_skills.py": "skill metadata normalization",
        "python scripts/normalize_openai_references.py": "reference normalization",
        "python scripts/generate_openai_workflow_registry.py": "registry generation",
        "python scripts/sync_openai_fixture_versions.py": "fixture version synchronization",
        "python scripts/audit_openai_research_plugin.py": "plugin audit",
        "python scripts/test_openai_phase4_scenarios.py --check-report": "workflow scenarios",
        "python scripts/test_openai_phase6_context.py": "context budget checks",
        "python scripts/test_openai_phase7_modes.py --check-report": "entry-mode checks",
        "python scripts/test_openai_phase8_corpus.py --check-report": "regression corpus",
        "python scripts/test_validate_openai_personal_readiness.py": "personal readiness contract tests",
        "python scripts/validate_openai_personal_readiness.py --check-report": "non-promoting personal readiness report check",
        "python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid": "personal plugin package validation",
        "raw.githubusercontent.com/openai/codex/${OPENAI_CODEX_VALIDATOR_COMMIT}": "pinned canonical OpenAI validator source",
        "sha256sum --check --strict": "canonical validator digest check",
        'python "$OPENAI_CODEX_VALIDATOR_PATH" research-skills-openai': "canonical OpenAI plugin validation",
    }
    for marker, label in required.items():
        require(marker in commands, "main_personal_tests", label)
    deferred_commands = {
        "test_openai_preview_evidence.py",
        "test_build_openai_preview_accepted_summary.py",
        "test_validate_openai_release_evidence.py",
        "generate_openai_release_ledger.py",
        "validate_openai_preview_release.py",
    }
    require(
        not any(marker in commands for marker in deferred_commands),
        "main_personal_scope",
        "deferred shared/public validation must not block personal-owner CI",
    )
    require("codex app-server" not in commands, "hosted_capture_forbidden", "hosted CI may not perform an App capture")
    require("pull_request_target" not in text, "main_triggers", "unsafe trigger")


def validate_evidence(document: dict[str, Any], text: str) -> None:
    validate_permissions(document, {"actions": "read", "contents": "read"})
    validate_action_pins(document)
    triggers = document.get("on", {})
    require(
        isinstance(triggers, dict) and set(triggers) == {"workflow_dispatch"},
        "evidence_triggers",
        "evidence validation must be manual only",
    )
    inputs = triggers.get("workflow_dispatch", {}).get("inputs", {})
    require(
        isinstance(inputs, dict)
        and {
            "release_tag",
            "source_commit",
            "asset_index_pattern",
            "phase7_runtime_receipts_name",
            "phase7_asset_index_pattern",
            "phase8_reviewer_receipts_name",
            "phase8_retrieval_receipts_name",
            "phase8_asset_index_pattern",
        }
        <= set(inputs)
        and inputs["release_tag"].get("required") == "true"
        and inputs["source_commit"].get("required") == "true",
        "evidence_inputs",
        "immutable prerelease tag and full commit inputs are required",
    )
    require(
        inputs["phase7_asset_index_pattern"].get("required") == "false"
        and inputs["phase7_asset_index_pattern"].get("default") == ""
        and inputs["phase8_asset_index_pattern"].get("required") == "false"
        and inputs["phase8_asset_index_pattern"].get("default") == "",
        "evidence_inputs",
        "Phase 7/8 dedicated patterns must be optional but paired with receipt inputs",
    )
    evidence_jobs = jobs(document)
    require(
        all(job.get("runs-on") == "ubuntu-latest" for job in evidence_jobs)
        and all(int(job.get("timeout-minutes", "0")) > 0 for job in evidence_jobs),
        "evidence_runner",
        "bounded hosted jobs are required",
    )
    checkout = next(
        (item for item in steps(document) if str(item.get("uses", "")).startswith("actions/checkout@")),
        None,
    )
    require(isinstance(checkout, dict), "evidence_checkout", "checkout action")
    checkout_with = checkout.get("with", {})
    require(
        checkout_with.get("ref") == "${{ inputs.source_commit }}"
        and checkout_with.get("fetch-depth") == "0"
        and checkout_with.get("fetch-tags") == "true"
        and checkout_with.get("persist-credentials") == "false",
        "evidence_checkout",
        "checkout must use the exact input commit with tags and no persisted token",
    )
    commands = command_blob(document)
    evidence_steps = steps(document)
    offline_offset = next(
        (
            offset
            for offset, item in enumerate(evidence_steps)
            if item.get("name") == "Validate downloaded bundle offline"
        ),
        -1,
    )
    selection_offset = next(
        (
            offset
            for offset, item in enumerate(evidence_steps)
            if item.get("name")
            == "Validate optional Phase 7 and Phase 8 index selections"
        ),
        -1,
    )
    semantic_offset = next(
        (
            offset
            for offset, item in enumerate(evidence_steps)
            if item.get("name") == "Authenticate Preview witnesses and Release assets"
        ),
        -1,
    )
    phase7_offset = next(
        (
            offset
            for offset, item in enumerate(evidence_steps)
            if item.get("name") == "Validate Phase 7 runtime semantics"
        ),
        -1,
    )
    phase8_offset = next(
        (
            offset
            for offset, item in enumerate(evidence_steps)
            if item.get("name") == "Validate Phase 8 reviewer and retrieval semantics"
        ),
        -1,
    )
    summary_offset = next(
        (
            offset
            for offset, item in enumerate(evidence_steps)
            if item.get("name") == "Build immutable live-verifier run summary"
        ),
        -1,
    )
    upload_offset = next(
        (
            offset
            for offset, item in enumerate(evidence_steps)
            if item.get("name") == "Publish immutable live-verifier run summary"
        ),
        -1,
    )
    require(
        0 <= selection_offset < offline_offset < semantic_offset < phase7_offset < phase8_offset < summary_offset < upload_offset,
        "evidence_contract",
        "integrity and semantic validation must precede the immutable run summary upload",
    )
    require(
        evidence_steps[phase7_offset].get("if")
        == "${{ inputs.phase7_runtime_receipts_name != '' }}",
        "evidence_contract",
        "Phase 7 semantic validation must be explicitly enabled by its receipt input",
    )
    require(
        evidence_steps[phase8_offset].get("if")
        == "${{ inputs.phase8_reviewer_receipts_name != '' || inputs.phase8_retrieval_receipts_name != '' }}",
        "evidence_contract",
        "Phase 8 semantic validation must be explicitly enabled by either receipt input",
    )
    require(
        evidence_steps[phase7_offset].get("env", {}).get("ASSET_INDEX_PATTERN")
        == "${{ inputs.phase7_asset_index_pattern }}"
        and evidence_steps[phase7_offset].get("env", {}).get("ASSET_DIR")
        == "${{ runner.temp }}/openai-preview-phase7-evidence"
        and evidence_steps[phase8_offset]
        .get("env", {})
        .get("ASSET_INDEX_PATTERN")
        == "${{ inputs.phase8_asset_index_pattern }}"
        and evidence_steps[phase8_offset].get("env", {}).get("ASSET_DIR")
        == "${{ runner.temp }}/openai-preview-phase8-evidence",
        "evidence_contract",
        "Phase 7/8 semantic validators must use their distinct dedicated patterns",
    )
    required_markers = {
        "git rev-list -n 1": "tag-to-commit resolution",
        'data.get("prerelease") is True': "published prerelease check",
        'data.get("immutable") is True': "immutable prerelease check",
        "gh release download": "GitHub Release asset download",
        "if [[ ${#downloaded_assets[@]} -eq 0 ]]": "empty asset failure",
        "if [[ ${#asset_indexes[@]} -eq 0 ]]": "missing one-bundle index failure",
        "each asset index must bind exactly one safe evidence envelope name": "one envelope per index",
        "Two asset indexes bind the same evidence envelope": "duplicate envelope rejection",
        "python scripts/generate_openai_release_ledger.py --check": "checkout tree identity",
        "--expected-source-identity": "full source identity binding",
        "python scripts/validate_openai_preview_evidence_bundle.py": "offline bundle CLI",
        'item.get("gate_eligible") is False': "offline integrity layer is non-gating",
        'item.get("accepted") is False': "offline integrity layer cannot accept",
        'item.get("summary",{}).get("claimed_preview_attested")==1': "Preview claim accounting",
        'item.get("summary",{}).get("claimed_provider_verified")==0': "provider claim accounting",
        "tests/openai_phase8/verify_preview_evidence.py": "authenticated Phase 8 adapter",
        "--evidence-root": "semantic verifier evidence root",
        "--expected-source-identity": "semantic verifier source binding",
        'item.get("counts_as_preview_attested") is True': "authenticated Preview accounting",
        'item.get("counts_as_provider_verified") is True': "authenticated provider accounting",
        "preview==len(results)": "every result is Preview-attested",
        "provider==0": "provider promotion is forbidden in the Preview workflow",
        "scripts/validate_openai_phase7_runtime_evidence.py": "Phase 7 runtime semantic runner",
        "Phase 7 receipt and dedicated pattern must be supplied together": "Phase 7 receipt/pattern pairing",
        "Both Phase 8 receipts and the dedicated pattern must be supplied together": "Phase 8 receipt/pattern pairing",
        "Phase 7 dedicated pattern must select exactly ten indexes": "Phase 7 dedicated cardinality",
        "Phase 8 dedicated pattern must select exactly twelve indexes": "Phase 8 dedicated cardinality",
        "Phase 7 and Phase 8 dedicated index selections overlap": "Phase 7/8 selection disjointness",
        "materialize_openai_preview_evidence_subset.py": "trusted stage-specific evidence materializer",
        "Phase 7 and Phase 8 evidence subsets reuse physical assets": "cross-stage physical-asset isolation",
        'result.get("bundle_count")==10': "ten Phase 7 mini-bundles",
        'result.get("receipt_count")==10': "ten Phase 7 runtime receipts",
        "scripts/validate_openai_phase8_external_evidence.py": "Phase 8 external semantic runner",
        'result.get("bundle_count")==12': "twelve Phase 8 mini-bundles",
        'result.get("reviewer_slot_count")==6': "six Phase 8 reviewer slots",
        'result.get("retrieval_slot_count")==6': "six Phase 8 retrieval slots",
        "scripts/build_openai_preview_verifier_summary.py": "live-verifier summary builder",
    }
    for marker, label in required_markers.items():
        require(marker in commands, "evidence_contract", label)
    for marker, label in {
        "openai-preview-live-verifier-summary-${{ github.run_id }}": "run-bound summary artifact",
        "retention-days: 90": "bounded run-summary retention",
        "overwrite: false": "immutable run-summary upload",
        "include-hidden-files: false": "single-file summary artifact boundary",
    }.items():
        require(marker in text, "evidence_contract", label)
    require(
        "capture_openai_codex_app_server.py" not in commands
        and "codex app-server" not in commands
        and "test_openai_app_server_capture.py" not in commands,
        "hosted_capture_forbidden",
        "the hosted evidence job validates uploaded assets only",
    )
    require(
        'summary.get("preview_attested",0)+summary.get("provider_verified",0)'
        not in commands,
        "evidence_contract",
        "Preview and provider evidence may not be conflated",
    )
    require(
        "secrets." not in text and "pull_request_target" not in text,
        "evidence_privilege",
        "no secret, write-back, or privileged trigger is allowed",
    )
    require(
        text.count("actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02")
        == 1,
        "evidence_privilege",
        "exactly one pinned run-summary artifact upload is allowed",
    )


def validate_draft_verifier(document: dict[str, Any], text: str) -> None:
    require(
        ".github/workflows/openai-preview-draft-bundle-verifier.yml"
        in VALIDATION_CONTRACT_FILES,
        "draft_verifier_identity",
        "draft verifier workflow must be part of release validation identity",
    )
    require(
        DRAFT_VERIFIER_PATH in validation_contract_paths(),
        "draft_verifier_identity",
        "draft verifier bytes are absent from the worktree validation digest",
    )
    expected_permissions = {"actions": "read", "contents": "write"}
    validate_permissions(document, expected_permissions)
    validate_action_pins(document)
    triggers = document.get("on", {})
    require(
        isinstance(triggers, dict) and set(triggers) == {"workflow_dispatch"},
        "draft_verifier_trigger",
        "draft verifier must be manual workflow_dispatch only",
    )
    inputs = triggers.get("workflow_dispatch", {}).get("inputs", {})
    expected_inputs = {
        "source_commit",
        "release_id",
        "source_ci_run_id",
        "raw_asset_name",
        "envelope_asset_name",
        "verifier_asset_name",
    }
    require(
        isinstance(inputs, dict)
        and set(inputs) == expected_inputs
        and all(value.get("required") == "true" for value in inputs.values()),
        "draft_verifier_inputs",
        "source, Release, source-CI, and exact R/E/V names are mandatory",
    )
    draft_jobs = document.get("jobs", {})
    require(
        isinstance(draft_jobs, dict)
        and set(draft_jobs) == {"verify-uploaded-r-e"}
        and draft_jobs["verify-uploaded-r-e"].get("runs-on") == "ubuntu-latest"
        and int(draft_jobs["verify-uploaded-r-e"].get("timeout-minutes", "0")) == 15,
        "draft_verifier_job",
        "one bounded verifier job is required",
    )
    checkout = next(
        (
            item
            for item in steps(document)
            if str(item.get("uses", "")).startswith("actions/checkout@")
        ),
        None,
    )
    checkout_with = checkout.get("with", {}) if isinstance(checkout, dict) else {}
    require(
        checkout_with.get("ref") == "${{ inputs.source_commit }}"
        and checkout_with.get("fetch-depth") == "0"
        and checkout_with.get("persist-credentials") == "false",
        "draft_verifier_checkout",
        "checkout must use the exact source commit without persisted credentials",
    )
    commands = command_blob(document)
    for marker, label in {
        '[[ "$GITHUB_REF_NAME" == "main" && "$GITHUB_SHA" == "$SOURCE_COMMIT" ]]': "main dispatch SHA binding",
        '[[ "$(git rev-parse HEAD)" == "$SOURCE_COMMIT" ]]': "exact checkout binding",
        'gh api "repos/${GITHUB_REPOSITORY}/releases/${RELEASE_ID}"': "draft Release API snapshot",
        'gh api "repos/${GITHUB_REPOSITORY}/actions/runs/${SOURCE_CI_RUN_ID}"': "source CI API snapshot",
        "release must remain a draft prerelease": "draft prerelease guard",
        'gh api -H "Accept: application/octet-stream"': "asset-ID downloads",
        "verify_openai_preview_draft_bundle.py": "independent V implementation",
        'gh release upload "$tag" "$STAGING_ROOT/bundle/$VERIFIER_NAME"': "single V upload",
        "V asset name already exists": "V no-overwrite guard",
        "release-after-v.json": "post-upload Release snapshot",
        "uploaded V did not resolve exactly once": "unique V API object",
    }.items():
        require(marker in commands, "draft_verifier_contract", label)
    require(
        "--clobber" not in commands
        and "pull_request" not in str(triggers)
        and "pull_request_target" not in text
        and "continue-on-error" not in text
        and "|| true" not in commands
        and "set +e" not in commands,
        "draft_verifier_fail_closed",
        "draft verifier cannot overwrite, broaden triggers, or suppress failures",
    )
    dangerous = re.findall(r"sys\.exit\([^\n]*else 0\);\s*[^'\n]+", text)
    require(
        not dangerous,
        "draft_verifier_python_exit",
        "a successful inline Python guard must not exit before later statements",
    )
    upload = next(
        (
            item
            for item in steps(document)
            if str(item.get("uses", "")).startswith("actions/upload-artifact@")
        ),
        None,
    )
    upload_with = upload.get("with", {}) if isinstance(upload, dict) else {}
    upload_path = str(upload_with.get("path", ""))
    require(
        upload_with.get("name") == "openai-preview-draft-v-${{ github.run_id }}"
        and upload_with.get("if-no-files-found") == "error"
        and upload_with.get("retention-days") == "90"
        and upload_with.get("overwrite") == "false"
        and upload_with.get("include-hidden-files") == "false"
        and "${{ inputs.verifier_asset_name }}" in upload_path
        and "api/v-asset.json" in upload_path
        and "verification-result.json" in upload_path,
        "draft_verifier_artifact",
        "V, its GitHub asset snapshot, and result must be retained together without overwrite",
    )


def validate_accepted(document: dict[str, Any], text: str) -> None:
    require(
        document.get("permissions") == {},
        "accepted_permissions",
        "accepted-state workflow top-level permissions must be empty",
    )
    validate_action_pins(document)
    triggers = document.get("on", {})
    require(
        isinstance(triggers, dict) and set(triggers) == {"workflow_dispatch"},
        "accepted_triggers",
        "accepted-state validation must be workflow_dispatch only",
    )
    inputs = triggers.get("workflow_dispatch", {}).get("inputs", {})
    expected_inputs = {
        "evidence_release_tag",
        "candidate_release_tag",
        "candidate_ledger_name",
        "phase7_asset_index_pattern",
        "phase8_asset_index_pattern",
        "phase7_runtime_receipts_name",
        "phase8_reviewer_receipts_name",
        "phase8_retrieval_receipts_name",
    }
    require(
        isinstance(inputs, dict)
        and set(inputs) == expected_inputs
        and all(inputs[name].get("required") == "true" for name in expected_inputs),
        "accepted_inputs",
        "two release tags, two disjoint index patterns, and four candidate filenames are required",
    )
    require(
        "source_commit" not in inputs and "inputs.source_commit" not in text,
        "accepted_inputs",
        "a caller-selected source commit is forbidden",
    )

    raw_jobs = document.get("jobs", {})
    require(
        isinstance(raw_jobs, dict)
        and set(raw_jobs) == {"validate-dispatch", "validate-accepted-evidence"},
        "accepted_jobs",
        "one unprivileged dispatch guard and one protected validation job are required",
    )
    preflight = raw_jobs["validate-dispatch"]
    accepted = raw_jobs["validate-accepted-evidence"]
    require(
        preflight.get("permissions") == {}
        and "environment" not in preflight
        and preflight.get("runs-on") == "ubuntu-latest"
        and int(preflight.get("timeout-minutes", "0")) > 0,
        "accepted_permissions",
        "dispatch guard must be bounded, unprivileged, and environment-free",
    )
    require(
        accepted.get("permissions") == {"actions": "read", "contents": "read"}
        and accepted.get("runs-on") == "ubuntu-latest"
        and int(accepted.get("timeout-minutes", "0")) > 0,
        "accepted_permissions",
        "protected job permissions must be exactly Actions/Contents read",
    )
    require(
        accepted.get("needs") == "validate-dispatch"
        and accepted.get("if")
        == "${{ needs.validate-dispatch.result == 'success' }}",
        "accepted_dependency",
        "protected job must depend on a successful dispatch guard",
    )
    environment = accepted.get("environment", {})
    require(
        isinstance(environment, dict)
        and environment.get("name") == "openai-preview-governance",
        "accepted_environment",
        "the governance job must use the protected openai-preview-governance environment",
    )

    preflight_steps = preflight.get("steps", [])
    accepted_steps = accepted.get("steps", [])
    require(
        isinstance(preflight_steps, list)
        and all(isinstance(item, dict) for item in preflight_steps)
        and isinstance(accepted_steps, list)
        and all(isinstance(item, dict) for item in accepted_steps),
        "workflow_steps",
        "accepted workflow steps",
    )
    preflight_commands = "\n".join(str(item.get("run", "")) for item in preflight_steps)
    accepted_commands = "\n".join(str(item.get("run", "")) for item in accepted_steps)
    for marker, label in {
        '"$DISPATCH_REF" != "refs/heads/$DEFAULT_BRANCH"': "default-branch dispatch guard",
        "^[0-9a-f]{40}$": "full trusted commit guard",
        "release tag contains unsupported characters": "safe release-tag guard",
        "Every evidence input must be one safe asset filename": "safe candidate filename guard",
        "candidate ledger must be JSON": "candidate ledger type guard",
        "Phase 7 receipts must be YAML": "Phase 7 receipt type guard",
        "Phase 8 reviewer receipts must be YAML": "Phase 8 reviewer receipt type guard",
        "Phase 8 retrieval receipts must be YAML": "Phase 8 retrieval receipt type guard",
        '"$EVIDENCE_RELEASE_TAG" != "$CANDIDATE_RELEASE_TAG"': "distinct release-tag guard",
        '"$PHASE7_ASSET_INDEX_PATTERN" != "$PHASE8_ASSET_INDEX_PATTERN"': "distinct Phase 7/8 pattern guard",
        "asset index pattern must be a single-directory pattern": "safe Phase 7/8 pattern guard",
    }.items():
        require(marker in preflight_commands, "accepted_dispatch_guard", label)

    secret_ref = "${{ secrets.OPENAI_PREVIEW_GOVERNANCE_TOKEN }}"
    require(
        secret_ref not in str(preflight)
        and secret_ref not in str(document.get("env", {}))
        and secret_ref not in str(accepted.get("env", {})),
        "accepted_secret_scope",
        "governance credential must not enter preflight, top-level, or job-level env",
    )
    expected_secret_steps = {
        "Build Phase 7 and Phase 8 reports and validate complete Preview in one process",
        "Run standalone production release-evidence verifier",
    }
    actual_secret_steps = {
        str(item.get("name", ""))
        for item in accepted_steps
        if secret_ref in str(item)
    }
    require(
        actual_secret_steps == expected_secret_steps,
        "accepted_secret_scope",
        "governance credential may enter only the two production live-validation steps",
    )
    github_token_ref = "${{ github.token }}"
    expected_builtin_token_steps = {
        "Verify both immutable release and tag identities",
        "Download evidence release bundles into the bundle root",
        "Download candidate ledger and collections outside the bundle root",
        "Download accepted previous release assets",
    }
    actual_builtin_token_steps = {
        str(item.get("name", ""))
        for item in accepted_steps
        if github_token_ref in str(item)
    }
    require(
        actual_builtin_token_steps == expected_builtin_token_steps,
        "accepted_secret_scope",
        "the built-in read token may enter only release identity and asset download steps",
    )
    require(
        RUNNER_CONTEXT_RE.search(str(document.get("env", {}))) is None
        and all(
            RUNNER_CONTEXT_RE.search(str(job.get("env", {}))) is None
            for job in raw_jobs.values()
        ),
        "accepted_runner_temp_scope",
        "runner context is unavailable in workflow/job env and must be bound by a runner step",
    )
    path_binding = next(
        (
            item
            for item in accepted_steps
            if item.get("name") == "Bind runner-temp paths for subsequent steps"
        ),
        None,
    )
    require(
        isinstance(path_binding, dict)
        and path_binding.get("shell") == "bash",
        "accepted_asset_isolation",
        "runner-temp path binding step",
    )
    path_binding_run = str(path_binding.get("run", ""))
    required_runner_paths = {
        "BUNDLE_ROOT": "openai-preview-accepted-bundles",
        "CANDIDATE_ASSET_DIR": "openai-preview-candidate-assets",
        "CURRENT_ASSET_DIR": "openai-preview-accepted-bundles/current-release",
        "ISOLATED_WORKSPACE": "accepted-workspace",
        "RELEASE_RUNNER_WORKSPACE": "accepted-release-runner-workspace",
        "TRUSTED_WORKSPACE_HASH": "trusted-workspace.sha256",
        "EXPECTED_IDENTITY": "openai-preview-accepted-source-identity.json",
        "EVIDENCE_RELEASE_JSON": "openai-preview-evidence-release.json",
        "CANDIDATE_RELEASE_JSON": "openai-preview-candidate-release.json",
        "EVIDENCE_ASSETS_JSON": "openai-preview-evidence-assets.json",
        "CANDIDATE_ASSETS_JSON": "openai-preview-candidate-assets.json",
        "EVIDENCE_COMMIT_FILE": "openai-preview-evidence-commit.txt",
        "CANDIDATE_COMMIT_FILE": "openai-preview-candidate-commit.txt",
        "RELEASE_RUNNER_RESULT": "openai-preview-release-runner-result.json",
        "PHASE78_BRIDGE_RESULT": "openai-preview-phase78-bridge-result.json",
        "ACCEPTED_SUMMARY": "openai-preview-accepted-summary/openai-preview-accepted-summary.json",
    }
    require(
        "set -euo pipefail" in path_binding_run
        and '} >> "$GITHUB_ENV"' in path_binding_run
        and all(
            f"printf '{name}=%s\\n' \"$RUNNER_TEMP/{suffix}\""
            in path_binding_run
            for name, suffix in required_runner_paths.items()
        ),
        "accepted_asset_isolation",
        "runner paths must be fixed after runner allocation and keep candidate assets outside the evidence bundle root",
    )

    checkout = next(
        (
            item
            for item in accepted_steps
            if str(item.get("uses", "")).startswith("actions/checkout@")
        ),
        None,
    )
    require(isinstance(checkout, dict), "accepted_checkout", "trusted checkout action")
    checkout_with = checkout.get("with", {})
    require(
        checkout_with.get("ref") == "${{ github.sha }}"
        and checkout_with.get("fetch-depth") == "0"
        and checkout_with.get("fetch-tags") == "true"
        and checkout_with.get("persist-credentials") == "false",
        "accepted_checkout",
        "protected job must check out only the guarded default-branch SHA",
    )

    ordered_names = [
        "Check out the fixed trusted default-branch commit",
        "Set up Python",
        "Install validator dependency",
        "Bind runner-temp paths for subsequent steps",
        "Hash the immutable trusted checkout",
        "Create an isolated accepted-evidence workspace",
        "Verify both immutable release and tag identities",
        "Download evidence release bundles into the bundle root",
        "Download candidate ledger and collections outside the bundle root",
        "Download accepted previous release assets",
        "Stage only candidate evidence and bind the trusted source identity",
        "Build Phase 7 and Phase 8 reports and validate complete Preview in one process",
        "Run standalone production release-evidence verifier",
        "Build the non-overwriting accepted-run summary",
        "Prove all validation workspaces remained immutable",
        "Publish the non-overwriting accepted-run summary",
    ]
    offsets = [
        next(
            (
                offset
                for offset, item in enumerate(accepted_steps)
                if item.get("name") == name
            ),
            -1,
        )
        for name in ordered_names
    ]
    require(
        [item.get("name") for item in accepted_steps] == ordered_names
        and offsets == sorted(offsets)
        and all(offset >= 0 for offset in offsets),
        "accepted_contract",
        "the exact trusted checkout, live bridge, independent release pass, summary, and final hash sequence is required",
    )
    immutability_step = next(
        item
        for item in accepted_steps
        if item.get("name") == "Prove all validation workspaces remained immutable"
    )
    require(
        immutability_step.get("if") == "${{ always() }}",
        "accepted_immutability",
        "all trusted workspaces must be rechecked even when validation fails",
    )
    require(
        offsets[-1] == len(accepted_steps) - 1,
        "accepted_summary",
        "accepted summary upload must be the final step after immutability proof",
    )
    for marker, label in {
        "git ls-files -z": "tracked-file checkout hash",
        "git clone --no-hardlinks": "isolated trusted workspace",
        'data.get("immutable") is True': "GitHub Release immutable-state check",
        "validate_release_tag_target": "exact refs/tags lookup and annotated-tag peel",
        'assets?per_page=100&page=${page}': "explicit Release asset pagination",
        'if [[ "$count" -eq 0 ]]; then': "terminal empty asset page query",
        'validate_release_tag_target(repository,os.environ["EVIDENCE_RELEASE_TAG"],commit)': "evidence release source binding",
        'validate_release_tag_target(repository,os.environ["CANDIDATE_RELEASE_TAG"],commit)': "candidate release source binding",
        'gh release download "$EVIDENCE_RELEASE_TAG"': "evidence release asset download",
        'gh release download "$CANDIDATE_RELEASE_TAG"': "candidate release asset download",
        "candidate asset directory must remain outside the evidence bundle root": "candidate directory separation",
        "candidate asset leaked into the evidence bundle root": "candidate leakage rejection",
        "scripts/download_openai_release_ledger_assets.py": "accepted history download",
        '--current-release-tag "$EVIDENCE_RELEASE_TAG"': "history excludes the evidence release",
        '"$CANDIDATE_ASSET_DIR/$CANDIDATE_LEDGER_NAME"': "candidate ledger outside the bundle root",
        '"$ISOLATED_WORKSPACE/research-skills-openai/reports/release-ledger.json"': "isolated candidate ledger staging",
        '"$ISOLATED_WORKSPACE/tests/openai_phase7/current-version-runtime-receipts.yaml"': "isolated Phase 7 staging",
        '"$ISOLATED_WORKSPACE/tests/openai_phase8/live-repeat-receipts.yaml"': "isolated Phase 8 reviewer staging",
        '"$ISOLATED_WORKSPACE/tests/openai_phase8/retrieval-receipts.yaml"': "isolated Phase 8 retrieval staging",
        "validate_openai_preview_accepted_phase78.py": "same-process Phase 7/8 bridge",
        '--phase7-asset-index-pattern "$PHASE7_ASSET_INDEX_PATTERN"': "separate Phase 7 index selection",
        '--phase8-asset-index-pattern "$PHASE8_ASSET_INDEX_PATTERN"': "separate Phase 8 index selection",
        "Phase 7 pattern must select exactly ten asset indexes": "Phase 7 index cardinality guard",
        "Phase 8 pattern must select exactly twelve asset indexes": "Phase 8 index cardinality guard",
        "Phase 7 and Phase 8 asset index selections overlap": "Phase 7/8 index disjointness guard",
        "python scripts/validate_openai_release_evidence.py": "standalone production release runner",
        '--ledger research-skills-openai/reports/release-ledger.json': "candidate ledger binding",
        "build_openai_preview_accepted_summary.py": "run-bound accepted summary builder",
        '--run-attempt "$GITHUB_RUN_ATTEMPT"': "run-attempt summary binding",
        "isolated workspace changed outside the evidence allowlist": "isolated mutation allowlist",
        "trusted checkout content changed": "trusted checkout hash comparison",
        "trusted checkout worktree changed": "trusted checkout clean-worktree comparison",
        "isolated workspace final allowlist mismatch": "isolated workspace final proof",
        "release-runner workspace final allowlist mismatch": "release runner final proof",
    }.items():
        require(marker in accepted_commands, "accepted_contract", label)
    require(
        'commits/${EVIDENCE_RELEASE_TAG}' not in accepted_commands
        and 'commits/${CANDIDATE_RELEASE_TAG}' not in accepted_commands,
        "accepted_tag_resolution",
        "tag identity must use the exact refs/tags resolver, never the generic commits endpoint",
    )
    standalone_run = str(
        next(
            item
            for item in accepted_steps
            if item.get("name") == "Run standalone production release-evidence verifier"
        ).get("run", "")
    )
    bridge_run = str(
        next(
            item
            for item in accepted_steps
            if item.get("name")
            == "Build Phase 7 and Phase 8 reports and validate complete Preview in one process"
        ).get("run", "")
    )
    require(
        '--bundle-root "$BUNDLE_ROOT"' in standalone_run
        and '--bundle-root "$BUNDLE_ROOT"' in bridge_run,
        "accepted_contract",
        "standalone and same-process complete validators must each construct a fresh production callback",
    )
    require(
        all(
            "set -euo pipefail" in str(item.get("run", ""))
            for item in accepted_steps
            if item.get("shell") == "bash"
        )
        and "continue-on-error" not in text
        and "|| true" not in accepted_commands
        and "set +e" not in accepted_commands,
        "accepted_fail_closed",
        "all accepted-state shell steps must fail closed",
    )
    require(
        "live_gate_eligible" not in accepted_commands
        and '"validated"' not in accepted_commands
        and "serialized" not in accepted_commands.lower(),
        "accepted_serialized_bypass",
        "serialized success fields may not bridge the two production validations",
    )
    require(
        "pull_request_target" not in text
        and "actions/checkout@" not in preflight_commands,
        "accepted_privilege",
        "accepted-state workflow must not broaden its trigger, token, or preflight checkout",
    )
    require(
        text.count(
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02"
        )
        == 1,
        "accepted_summary",
        "exactly one pinned non-overwriting accepted-summary upload is required",
    )
    summary_upload = next(
        (
            item
            for item in accepted_steps
            if item.get("name") == "Publish the non-overwriting accepted-run summary"
        ),
        None,
    )
    summary_with = summary_upload.get("with", {}) if isinstance(summary_upload, dict) else {}
    require(
        summary_with.get("name")
        == "openai-preview-accepted-summary-${{ github.run_id }}-${{ github.run_attempt }}"
        and "if" not in summary_upload
        and summary_with.get("overwrite") == "false"
        and summary_with.get("if-no-files-found") == "error",
        "accepted_summary",
        "accepted summary must run only after prior success, remain run-attempt-bound, non-overwriting, and fail closed",
    )


def validate_consumer(document: dict[str, Any], text: str) -> None:
    require(
        document.get("permissions") == {},
        "consumer_permissions",
        "accepted-summary consumer top-level permissions must be empty",
    )
    validate_action_pins(document)
    triggers = document.get("on", {})
    workflow_run = triggers.get("workflow_run", {}) if isinstance(triggers, dict) else {}
    require(
        isinstance(triggers, dict)
        and set(triggers) == {"workflow_run"}
        and isinstance(workflow_run, dict)
        and workflow_run.get("workflows") == ["OpenAI Preview Accepted Evidence"]
        and workflow_run.get("types") == ["completed"],
        "consumer_triggers",
        "consumer must run only after completion of the accepted-evidence workflow",
    )

    raw_jobs = document.get("jobs", {})
    require(
        isinstance(raw_jobs, dict)
        and set(raw_jobs) == {"validate-source-run", "verify-accepted-summary"},
        "consumer_jobs",
        "one unprivileged source guard and one independent consumer job are required",
    )
    preflight = raw_jobs["validate-source-run"]
    consumer = raw_jobs["verify-accepted-summary"]
    require(
        preflight.get("permissions") == {}
        and "environment" not in preflight
        and preflight.get("runs-on") == "ubuntu-latest"
        and int(preflight.get("timeout-minutes", "0")) > 0,
        "consumer_permissions",
        "source-run guard must be bounded, unprivileged, and environment-free",
    )
    require(
        consumer.get("permissions")
        == {"actions": "read", "contents": "read", "deployments": "read"}
        and "environment" not in consumer
        and consumer.get("runs-on") == "ubuntu-latest"
        and int(consumer.get("timeout-minutes", "0")) > 0,
        "consumer_permissions",
        "consumer permissions must be exactly Actions/Contents/Deployments read",
    )
    require(
        consumer.get("needs") == "validate-source-run"
        and consumer.get("if")
        == "${{ needs.validate-source-run.result == 'success' }}",
        "consumer_dependency",
        "consumer must depend on the successful unprivileged source-run guard",
    )
    require(
        RUNNER_CONTEXT_RE.search(str(document.get("env", {}))) is None
        and all(
            RUNNER_CONTEXT_RE.search(str(job.get("env", {}))) is None
            for job in raw_jobs.values()
        ),
        "consumer_runner_temp_scope",
        "runner context is unavailable in workflow/job env and must remain step-scoped",
    )

    preflight_steps = preflight.get("steps", [])
    consumer_steps = consumer.get("steps", [])
    require(
        isinstance(preflight_steps, list)
        and len(preflight_steps) == 1
        and all(isinstance(item, dict) for item in preflight_steps)
        and isinstance(consumer_steps, list)
        and len(consumer_steps) == 4
        and all(isinstance(item, dict) for item in consumer_steps),
        "workflow_steps",
        "accepted-summary consumer steps",
    )
    preflight_commands = "\n".join(
        str(item.get("run", "")) for item in preflight_steps
    )
    consumer_commands = "\n".join(
        str(item.get("run", "")) for item in consumer_steps
    )
    for marker, label in {
        '"$CONSUMER_REF" == "refs/heads/$DEFAULT_BRANCH"': "trusted default-branch consumer guard",
        '"$SOURCE_REPOSITORY" == "$REPOSITORY"': "same-repository source guard",
        '"$SOURCE_WORKFLOW" == "OpenAI Preview Accepted Evidence"': "source workflow-name guard",
        '"$SOURCE_PATH" == ".github/workflows/openai-preview-accepted-evidence.yml"': "source workflow-path guard",
        '"$SOURCE_EVENT" == "workflow_dispatch"': "source event guard",
        '"$SOURCE_BRANCH" == "$DEFAULT_BRANCH"': "source default-branch guard",
        '"$CONSUMER_COMMIT" == "$SOURCE_COMMIT"': "source/consumer commit equality guard",
        '"$SOURCE_STATUS" == "completed" && "$SOURCE_CONCLUSION" == "success"': "successful completion guard",
        '"$SOURCE_RUN_ID" =~ ^[1-9][0-9]*$': "positive source run-ID guard",
        '"$SOURCE_RUN_ATTEMPT" =~ ^[1-9][0-9]*$': "positive run-attempt guard",
    }.items():
        require(marker in preflight_commands, "consumer_preflight", label)
    preflight_env = preflight_steps[0].get("env", {})
    require(
        preflight_env.get("CONSUMER_COMMIT") == "${{ github.sha }}"
        and preflight_env.get("CONSUMER_REF") == "${{ github.ref }}"
        and preflight_env.get("SOURCE_COMMIT")
        == "${{ github.event.workflow_run.head_sha }}"
        and preflight_env.get("SOURCE_RUN_ID")
        == "${{ github.event.workflow_run.id }}"
        and preflight_env.get("SOURCE_RUN_ATTEMPT")
        == "${{ github.event.workflow_run.run_attempt }}",
        "consumer_preflight",
        "preflight must bind the trusted consumer and exact source run attempt",
    )

    require(
        not any("uses" in item for item in preflight_steps),
        "consumer_preflight",
        "unprivileged preflight must not check out or run an action",
    )
    checkout = next(
        (
            item
            for item in consumer_steps
            if str(item.get("uses", "")).startswith("actions/checkout@")
        ),
        None,
    )
    require(isinstance(checkout, dict), "consumer_checkout", "trusted checkout action")
    checkout_with = checkout.get("with", {})
    require(
        checkout_with.get("ref") == "${{ github.sha }}"
        and checkout_with.get("fetch-depth") == "1"
        and checkout_with.get("persist-credentials") == "false",
        "consumer_checkout",
        "consumer must check out its trusted default-branch SHA, never the source SHA",
    )

    verify_step = next(
        (
            item
            for item in consumer_steps
            if item.get("name")
            == "Independently verify the protected run and accepted summary"
        ),
        None,
    )
    require(isinstance(verify_step, dict), "consumer_contract", "verification step")
    require(
        verify_step.get("env")
        == {
            "CONSUMER_RESULT": "${{ runner.temp }}/openai-preview-accepted-consumer-result.json",
            "GH_TOKEN": "${{ github.token }}",
        },
        "consumer_token_scope",
        "explicit github.token and runner-temp result path must be limited to the verification step",
    )
    actual_token_steps = {
        str(item.get("name", ""))
        for item in consumer_steps
        if "${{ github.token }}" in str(item)
    }
    require(
        actual_token_steps
        == {"Independently verify the protected run and accepted summary"},
        "consumer_token_scope",
        "explicit github.token injection must not enter setup or artifact upload",
    )
    require(
        str(document).count("${{ github.token }}") == 1,
        "consumer_token_scope",
        "the verifier env must be the only explicit github.token interpolation",
    )
    for marker, label in {
        "scripts/verify_openai_preview_accepted_summary.py": "independent verifier",
        '--repository "$GITHUB_REPOSITORY"': "repository binding",
        '--run-id "$SOURCE_RUN_ID"': "source run binding",
        '--run-attempt "$SOURCE_RUN_ATTEMPT"': "exact attempt binding",
        '--source-commit "$SOURCE_COMMIT"': "source SHA binding",
        '--consumer-commit "$GITHUB_SHA"': "trusted consumer SHA binding",
        '--consumer-run-id "$GITHUB_RUN_ID"': "consumer run lineage",
        '--consumer-run-attempt "$GITHUB_RUN_ATTEMPT"': "consumer attempt lineage",
        '--output "$CONSUMER_RESULT"': "fixed result output",
    }.items():
        require(marker in consumer_commands, "consumer_contract", label)
    require(
        "continue-on-error" not in text
        and "|| true" not in consumer_commands
        and "set +e" not in consumer_commands,
        "consumer_fail_closed",
        "accepted-summary consumer must fail closed",
    )
    serialized_document = str(document)
    require(
        "secrets." not in text
        and "secrets." not in serialized_document
        and "OPENAI_PREVIEW_GOVERNANCE_TOKEN" not in text
        and "OPENAI_PREVIEW_GOVERNANCE_TOKEN" not in serialized_document
        and "pull_request_target" not in text
        and "repository_dispatch" not in text
        and "workflow_call" not in text,
        "consumer_privilege",
        "consumer must not use caller inputs, privileged triggers, or governance secrets",
    )
    require(
        all("environment" not in job for job in raw_jobs.values()),
        "consumer_environment",
        "consumer must re-query deployments without entering a protected Environment",
    )

    ordered_names = [
        "Check out the trusted consumer from the default branch",
        "Set up Python",
        "Independently verify the protected run and accepted summary",
        "Publish the non-overwriting consumer result",
    ]
    offsets = [
        next(
            (
                offset
                for offset, item in enumerate(consumer_steps)
                if item.get("name") == name
            ),
            -1,
        )
        for name in ordered_names
    ]
    require(
        [item.get("name") for item in consumer_steps] == ordered_names
        and offsets == sorted(offsets)
        and all(offset >= 0 for offset in offsets)
        and offsets[-1] == len(consumer_steps) - 1,
        "consumer_order",
        "trusted checkout and verification must precede the final result upload",
    )
    require(
        text.count(
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02"
        )
        == 1,
        "consumer_result",
        "exactly one pinned consumer-result upload is required",
    )
    upload = consumer_steps[offsets[-1]]
    upload_with = upload.get("with", {})
    require(
        consumer_steps[0].get("uses")
        == "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5"
        and consumer_steps[1].get("uses")
        == "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065"
        and "uses" not in consumer_steps[2]
        and isinstance(consumer_steps[2].get("run"), str)
        and upload.get("uses")
        == "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02"
        and "if" not in upload
        and upload_with.get("name")
        == "openai-preview-accepted-consumer-${{ github.run_id }}-${{ github.run_attempt }}-${{ github.event.workflow_run.id }}-${{ github.event.workflow_run.run_attempt }}"
        and upload_with.get("path")
        == "${{ runner.temp }}/openai-preview-accepted-consumer-result.json"
        and upload_with.get("if-no-files-found") == "error"
        and upload_with.get("retention-days") == "90"
        and upload_with.get("overwrite") == "false"
        and upload_with.get("include-hidden-files") == "false",
        "consumer_result",
        "consumer result must be run-attempt-bound, bounded, non-overwriting, and fail closed",
    )


def expect_rejected(
    code: str, document: dict[str, Any], text: str, validator
) -> None:
    try:
        validator(document, text)
    except WorkflowViolation as exc:
        require(exc.code == code, "mutation_error", f"{code}: {exc.code}")
    else:
        raise WorkflowViolation("mutation_accepted", code)


def validate_mutation_guards(
    main: dict[str, Any],
    main_text: str,
    evidence: dict[str, Any],
    evidence_text: str,
    accepted: dict[str, Any],
    accepted_text: str,
    consumer: dict[str, Any],
    consumer_text: str,
) -> int:
    wrong_check_name = copy.deepcopy(main)
    wrong_check_name["jobs"]["validate"]["name"] = "validate"
    expect_rejected(
        "main_required_check_name",
        wrong_check_name,
        main_text,
        validate_main,
    )

    mutable_action = copy.deepcopy(main)
    next(item for item in steps(mutable_action) if "uses" in item)["uses"] = (
        "actions/checkout@v4"
    )
    expect_rejected("workflow_action_pin", mutable_action, main_text, validate_main)

    writable = copy.deepcopy(evidence)
    writable["permissions"] = {"contents": "write"}
    expect_rejected("workflow_permissions", writable, evidence_text, validate_evidence)

    wrong_ref = copy.deepcopy(evidence)
    next(
        item
        for item in steps(wrong_ref)
        if str(item.get("uses", "")).startswith("actions/checkout@")
    )["with"]["ref"] = "main"
    expect_rejected("evidence_checkout", wrong_ref, evidence_text, validate_evidence)

    capture = copy.deepcopy(evidence)
    jobs(capture)[0]["steps"].append(
        {"run": "python scripts/capture_openai_codex_app_server.py --output-dir evidence"}
    )
    expect_rejected("hosted_capture_forbidden", capture, evidence_text, validate_evidence)

    missing_asset_guard = copy.deepcopy(evidence)
    for step in steps(missing_asset_guard):
        if "if [[ ${#downloaded_assets[@]} -eq 0 ]]" in str(
            step.get("run", "")
        ):
            step["run"] = str(step["run"]).replace(
                "if [[ ${#downloaded_assets[@]} -eq 0 ]]", "if false", 1
            )
            break
    expect_rejected(
        "evidence_contract", missing_asset_guard, evidence_text, validate_evidence
    )

    provider_promotion = copy.deepcopy(evidence)
    for step in steps(provider_promotion):
        if "provider==0" in str(step.get("run", "")):
            step["run"] = str(step["run"]).replace("provider==0", "provider>=0")
    expect_rejected(
        "evidence_contract", provider_promotion, evidence_text, validate_evidence
    )

    missing_semantic_adapter = copy.deepcopy(evidence)
    for step in steps(missing_semantic_adapter):
        if "tests/openai_phase8/verify_preview_evidence.py" in str(
            step.get("run", "")
        ):
            step["run"] = str(step["run"]).replace(
                "tests/openai_phase8/verify_preview_evidence.py",
                "scripts/validate_openai_preview_evidence_bundle.py",
                1,
            )
            break
    expect_rejected(
        "evidence_contract",
        missing_semantic_adapter,
        evidence_text,
        validate_evidence,
    )

    unconditional_phase7 = copy.deepcopy(evidence)
    next(
        item
        for item in steps(unconditional_phase7)
        if item.get("name") == "Validate Phase 7 runtime semantics"
    ).pop("if", None)
    expect_rejected(
        "evidence_contract",
        unconditional_phase7,
        evidence_text,
        validate_evidence,
    )

    generic_phase7_pattern = copy.deepcopy(evidence)
    next(
        item
        for item in steps(generic_phase7_pattern)
        if item.get("name") == "Validate Phase 7 runtime semantics"
    )["env"]["ASSET_INDEX_PATTERN"] = "${{ inputs.asset_index_pattern }}"
    expect_rejected(
        "evidence_contract",
        generic_phase7_pattern,
        evidence_text,
        validate_evidence,
    )

    missing_phase8_pair_guard = copy.deepcopy(evidence)
    selection = next(
        item
        for item in steps(missing_phase8_pair_guard)
        if item.get("name")
        == "Validate optional Phase 7 and Phase 8 index selections"
    )
    selection["run"] = str(selection["run"]).replace(
        "Both Phase 8 receipts and the dedicated pattern must be supplied together",
        "pairing skipped",
        1,
    )
    expect_rejected(
        "evidence_contract",
        missing_phase8_pair_guard,
        evidence_text,
        validate_evidence,
    )

    accepted_writable = copy.deepcopy(accepted)
    accepted_writable["jobs"]["validate-accepted-evidence"]["permissions"] = {
        "contents": "write"
    }
    expect_rejected(
        "accepted_permissions",
        accepted_writable,
        accepted_text,
        validate_accepted,
    )

    accepted_unprotected = copy.deepcopy(accepted)
    accepted_unprotected["jobs"]["validate-accepted-evidence"].pop(
        "environment", None
    )
    expect_rejected(
        "accepted_environment",
        accepted_unprotected,
        accepted_text,
        validate_accepted,
    )

    accepted_wrong_ref = copy.deepcopy(accepted)
    next(
        item
        for item in accepted_wrong_ref["jobs"]["validate-accepted-evidence"]["steps"]
        if str(item.get("uses", "")).startswith("actions/checkout@")
    )["with"]["ref"] = "${{ inputs.source_commit }}"
    expect_rejected(
        "accepted_checkout",
        accepted_wrong_ref,
        accepted_text,
        validate_accepted,
    )

    accepted_secret_leak = copy.deepcopy(accepted)
    accepted_secret_leak["jobs"]["validate-dispatch"]["steps"][0]["env"] = {
        "GH_TOKEN": "${{ secrets.OPENAI_PREVIEW_GOVERNANCE_TOKEN }}"
    }
    expect_rejected(
        "accepted_secret_scope",
        accepted_secret_leak,
        accepted_text,
        validate_accepted,
    )

    accepted_missing_runner = copy.deepcopy(accepted)
    next(
        item
        for item in accepted_missing_runner["jobs"]["validate-accepted-evidence"]["steps"]
        if item.get("name") == "Run standalone production release-evidence verifier"
    )["run"] = "set -euo pipefail\necho skipped"
    expect_rejected(
        "accepted_contract",
        accepted_missing_runner,
        accepted_text,
        validate_accepted,
    )

    accepted_serialized_bypass = copy.deepcopy(accepted)
    next(
        item
        for item in accepted_serialized_bypass["jobs"]["validate-accepted-evidence"]["steps"]
        if item.get("name")
        == "Build Phase 7 and Phase 8 reports and validate complete Preview in one process"
    )["run"] += '\necho "live_gate_eligible=true"'
    expect_rejected(
        "accepted_serialized_bypass",
        accepted_serialized_bypass,
        accepted_text,
        validate_accepted,
    )

    accepted_push_trigger = copy.deepcopy(accepted)
    accepted_push_trigger["on"]["push"] = {"branches": ["main"]}
    expect_rejected(
        "accepted_triggers",
        accepted_push_trigger,
        accepted_text,
        validate_accepted,
    )

    accepted_without_guard = copy.deepcopy(accepted)
    accepted_without_guard["jobs"]["validate-accepted-evidence"].pop("needs", None)
    expect_rejected(
        "accepted_dependency",
        accepted_without_guard,
        accepted_text,
        validate_accepted,
    )

    accepted_same_tag = copy.deepcopy(accepted)
    guard_step = accepted_same_tag["jobs"]["validate-dispatch"]["steps"][0]
    guard_step["run"] = str(guard_step["run"]).replace(
        '[[ "$EVIDENCE_RELEASE_TAG" != "$CANDIDATE_RELEASE_TAG" ]]',
        "[[ true ]]",
        1,
    )
    expect_rejected(
        "accepted_dispatch_guard",
        accepted_same_tag,
        accepted_text,
        validate_accepted,
    )

    accepted_same_patterns = copy.deepcopy(accepted)
    pattern_guard = accepted_same_patterns["jobs"]["validate-dispatch"]["steps"][0]
    pattern_guard["run"] = str(pattern_guard["run"]).replace(
        '[[ "$PHASE7_ASSET_INDEX_PATTERN" != "$PHASE8_ASSET_INDEX_PATTERN" ]]',
        "[[ true ]]",
        1,
    )
    expect_rejected(
        "accepted_dispatch_guard",
        accepted_same_patterns,
        accepted_text,
        validate_accepted,
    )

    accepted_missing_bridge = copy.deepcopy(accepted)
    next(
        item
        for item in accepted_missing_bridge["jobs"]["validate-accepted-evidence"]["steps"]
        if item.get("name")
        == "Build Phase 7 and Phase 8 reports and validate complete Preview in one process"
    )["run"] = "set -euo pipefail\necho skipped"
    expect_rejected(
        "accepted_contract",
        accepted_missing_bridge,
        accepted_text,
        validate_accepted,
    )

    accepted_overwriting_summary = copy.deepcopy(accepted)
    next(
        item
        for item in accepted_overwriting_summary["jobs"]["validate-accepted-evidence"]["steps"]
        if item.get("name") == "Publish the non-overwriting accepted-run summary"
    )["with"]["overwrite"] = "true"
    expect_rejected(
        "accepted_summary",
        accepted_overwriting_summary,
        accepted_text,
        validate_accepted,
    )

    accepted_always_upload = copy.deepcopy(accepted)
    next(
        item
        for item in accepted_always_upload["jobs"]["validate-accepted-evidence"][
            "steps"
        ]
        if item.get("name") == "Publish the non-overwriting accepted-run summary"
    )["if"] = "${{ always() }}"
    expect_rejected(
        "accepted_summary",
        accepted_always_upload,
        accepted_text,
        validate_accepted,
    )

    accepted_upload_before_proof = copy.deepcopy(accepted)
    protected_steps = accepted_upload_before_proof["jobs"][
        "validate-accepted-evidence"
    ]["steps"]
    upload_offset = next(
        offset
        for offset, item in enumerate(protected_steps)
        if item.get("name") == "Publish the non-overwriting accepted-run summary"
    )
    proof_offset = next(
        offset
        for offset, item in enumerate(protected_steps)
        if item.get("name") == "Prove all validation workspaces remained immutable"
    )
    protected_steps[upload_offset], protected_steps[proof_offset] = (
        protected_steps[proof_offset],
        protected_steps[upload_offset],
    )
    expect_rejected(
        "accepted_contract",
        accepted_upload_before_proof,
        accepted_text,
        validate_accepted,
    )

    accepted_generic_tag_resolution = copy.deepcopy(accepted)
    tag_step = next(
        item
        for item in accepted_generic_tag_resolution["jobs"][
            "validate-accepted-evidence"
        ]["steps"]
        if item.get("name") == "Verify both immutable release and tag identities"
    )
    tag_step["run"] = str(tag_step["run"]).replace(
        "PYTHONPATH=tests/openai_phase8 python -c 'import os; from verify_preview_evidence import validate_release_tag_target; repository=os.environ[\"GITHUB_REPOSITORY\"]; commit=os.environ[\"TRUSTED_COMMIT\"]; validate_release_tag_target(repository,os.environ[\"EVIDENCE_RELEASE_TAG\"],commit); validate_release_tag_target(repository,os.environ[\"CANDIDATE_RELEASE_TAG\"],commit)'",
        'evidence_commit="$(gh api "repos/${GITHUB_REPOSITORY}/commits/${EVIDENCE_RELEASE_TAG}" --jq .sha)"',
        1,
    )
    expect_rejected(
        "accepted_contract",
        accepted_generic_tag_resolution,
        accepted_text,
        validate_accepted,
    )

    accepted_truncated_inventory = copy.deepcopy(accepted)
    inventory_step = next(
        item
        for item in accepted_truncated_inventory["jobs"]["validate-accepted-evidence"]["steps"]
        if item.get("name") == "Verify both immutable release and tag identities"
    )
    inventory_step["run"] = str(inventory_step["run"]).replace(
        'if [[ "$count" -eq 0 ]]; then',
        'if [[ "$count" -lt 100 ]]; then',
        1,
    )
    expect_rejected(
        "accepted_contract",
        accepted_truncated_inventory,
        accepted_text,
        validate_accepted,
    )

    accepted_mixed_assets = copy.deepcopy(accepted)
    binding_step = next(
        item
        for item in accepted_mixed_assets["jobs"]["validate-accepted-evidence"][
            "steps"
        ]
        if item.get("name") == "Bind runner-temp paths for subsequent steps"
    )
    binding_step["run"] = str(binding_step["run"]).replace(
        '"$RUNNER_TEMP/openai-preview-candidate-assets"',
        '"$RUNNER_TEMP/openai-preview-accepted-bundles/candidate"',
        1,
    )
    expect_rejected(
        "accepted_asset_isolation",
        accepted_mixed_assets,
        accepted_text,
        validate_accepted,
    )

    accepted_job_runner_context = copy.deepcopy(accepted)
    accepted_job_runner_context["jobs"]["validate-accepted-evidence"]["env"] = {
        "BUNDLE_ROOT": "${{ runner.temp }}/openai-preview-accepted-bundles"
    }
    expect_rejected(
        "accepted_runner_temp_scope",
        accepted_job_runner_context,
        accepted_text,
        validate_accepted,
    )

    accepted_preflight_runner_context = copy.deepcopy(accepted)
    accepted_preflight_runner_context["jobs"]["validate-dispatch"]["env"] = {
        "BAD": "${{ runner.temp }}/x"
    }
    expect_rejected(
        "accepted_runner_temp_scope",
        accepted_preflight_runner_context,
        accepted_text,
        validate_accepted,
    )

    accepted_compact_runner_context = copy.deepcopy(accepted)
    accepted_compact_runner_context["jobs"]["validate-accepted-evidence"]["env"] = {
        "BAD": "${{runner.temp}}/x"
    }
    expect_rejected(
        "accepted_runner_temp_scope",
        accepted_compact_runner_context,
        accepted_text,
        validate_accepted,
    )

    accepted_index_runner_context = copy.deepcopy(accepted)
    accepted_index_runner_context["jobs"]["validate-accepted-evidence"]["env"] = {
        "BAD": "${{ runner['temp'] }}/x"
    }
    expect_rejected(
        "accepted_runner_temp_scope",
        accepted_index_runner_context,
        accepted_text,
        validate_accepted,
    )

    accepted_nested_runner_context = copy.deepcopy(accepted)
    accepted_nested_runner_context["jobs"]["validate-accepted-evidence"]["env"] = {
        "BAD": "${{ format('{0}', runner.temp) }}"
    }
    expect_rejected(
        "accepted_runner_temp_scope",
        accepted_nested_runner_context,
        accepted_text,
        validate_accepted,
    )

    accepted_bare_runner_context = copy.deepcopy(accepted)
    accepted_bare_runner_context["jobs"]["validate-dispatch"]["env"] = {
        "BAD": "${{ toJSON(runner) }}"
    }
    expect_rejected(
        "accepted_runner_temp_scope",
        accepted_bare_runner_context,
        accepted_text,
        validate_accepted,
    )

    accepted_checkout_after_hash = copy.deepcopy(accepted)
    ordered_steps = accepted_checkout_after_hash["jobs"]["validate-accepted-evidence"][
        "steps"
    ]
    checkout_offset = next(
        offset
        for offset, item in enumerate(ordered_steps)
        if item.get("name") == "Check out the fixed trusted default-branch commit"
    )
    hash_offset = next(
        offset
        for offset, item in enumerate(ordered_steps)
        if item.get("name") == "Hash the immutable trusted checkout"
    )
    ordered_steps[checkout_offset], ordered_steps[hash_offset] = (
        ordered_steps[hash_offset],
        ordered_steps[checkout_offset],
    )
    expect_rejected(
        "accepted_contract",
        accepted_checkout_after_hash,
        accepted_text,
        validate_accepted,
    )

    consumer_manual = copy.deepcopy(consumer)
    consumer_manual["on"]["workflow_dispatch"] = {}
    expect_rejected(
        "consumer_triggers", consumer_manual, consumer_text, validate_consumer
    )

    consumer_wrong_source = copy.deepcopy(consumer)
    consumer_wrong_source["on"]["workflow_run"]["workflows"] = [
        "OpenAI Plugin Preview"
    ]
    expect_rejected(
        "consumer_triggers", consumer_wrong_source, consumer_text, validate_consumer
    )

    consumer_writable = copy.deepcopy(consumer)
    consumer_writable["jobs"]["verify-accepted-summary"]["permissions"][
        "contents"
    ] = "write"
    expect_rejected(
        "consumer_permissions", consumer_writable, consumer_text, validate_consumer
    )

    consumer_without_deployments = copy.deepcopy(consumer)
    consumer_without_deployments["jobs"]["verify-accepted-summary"][
        "permissions"
    ].pop("deployments")
    expect_rejected(
        "consumer_permissions",
        consumer_without_deployments,
        consumer_text,
        validate_consumer,
    )

    consumer_protected = copy.deepcopy(consumer)
    consumer_protected["jobs"]["verify-accepted-summary"]["environment"] = {
        "name": "openai-preview-governance"
    }
    expect_rejected(
        "consumer_permissions", consumer_protected, consumer_text, validate_consumer
    )

    consumer_without_guard = copy.deepcopy(consumer)
    consumer_without_guard["jobs"]["verify-accepted-summary"].pop("needs")
    expect_rejected(
        "consumer_dependency",
        consumer_without_guard,
        consumer_text,
        validate_consumer,
    )

    consumer_source_checkout = copy.deepcopy(consumer)
    next(
        item
        for item in consumer_source_checkout["jobs"]["verify-accepted-summary"][
            "steps"
        ]
        if str(item.get("uses", "")).startswith("actions/checkout@")
    )["with"]["ref"] = "${{ github.event.workflow_run.head_sha }}"
    expect_rejected(
        "consumer_checkout",
        consumer_source_checkout,
        consumer_text,
        validate_consumer,
    )

    consumer_preflight_checkout = copy.deepcopy(consumer)
    consumer_preflight_checkout["jobs"]["validate-source-run"]["steps"].append(
        {
            "uses": "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5",
            "with": {"persist-credentials": "false"},
        }
    )
    expect_rejected(
        "workflow_steps",
        consumer_preflight_checkout,
        consumer_text,
        validate_consumer,
    )

    consumer_missing_path_guard = copy.deepcopy(consumer)
    guard = consumer_missing_path_guard["jobs"]["validate-source-run"]["steps"][0]
    guard["run"] = str(guard["run"]).replace(
        '"$SOURCE_PATH" == ".github/workflows/openai-preview-accepted-evidence.yml"',
        '"$SOURCE_PATH" != ""',
        1,
    )
    expect_rejected(
        "consumer_preflight",
        consumer_missing_path_guard,
        consumer_text,
        validate_consumer,
    )

    consumer_without_commit_equality = copy.deepcopy(consumer)
    guard = consumer_without_commit_equality["jobs"]["validate-source-run"]["steps"][0]
    guard["run"] = str(guard["run"]).replace(
        '"$CONSUMER_COMMIT" == "$SOURCE_COMMIT"', '"$CONSUMER_COMMIT" != ""', 1
    )
    expect_rejected(
        "consumer_preflight",
        consumer_without_commit_equality,
        consumer_text,
        validate_consumer,
    )

    consumer_secret = copy.deepcopy(consumer)
    consumer_secret["env"] = {
        "TOKEN": "${{ secrets.OPENAI_PREVIEW_GOVERNANCE_TOKEN }}"
    }
    expect_rejected(
        "consumer_privilege", consumer_secret, consumer_text, validate_consumer
    )

    consumer_wrong_attempt = copy.deepcopy(consumer)
    verify = next(
        item
        for item in consumer_wrong_attempt["jobs"]["verify-accepted-summary"]["steps"]
        if item.get("name")
        == "Independently verify the protected run and accepted summary"
    )
    verify["run"] = str(verify["run"]).replace(
        '--run-attempt "$SOURCE_RUN_ATTEMPT"', '--run-attempt "1"', 1
    )
    expect_rejected(
        "consumer_contract", consumer_wrong_attempt, consumer_text, validate_consumer
    )

    consumer_token_leak = copy.deepcopy(consumer)
    checkout = next(
        item
        for item in consumer_token_leak["jobs"]["verify-accepted-summary"]["steps"]
        if str(item.get("uses", "")).startswith("actions/checkout@")
    )
    checkout["env"] = {"GH_TOKEN": "${{ github.token }}"}
    expect_rejected(
        "consumer_token_scope", consumer_token_leak, consumer_text, validate_consumer
    )

    consumer_job_token_leak = copy.deepcopy(consumer)
    consumer_job_token_leak["jobs"]["verify-accepted-summary"].setdefault(
        "env", {}
    )["LEAK"] = "${{ github.token }}"
    expect_rejected(
        "consumer_token_scope",
        consumer_job_token_leak,
        consumer_text,
        validate_consumer,
    )

    consumer_job_runner_context = copy.deepcopy(consumer)
    consumer_job_runner_context["jobs"]["verify-accepted-summary"]["env"][
        "CONSUMER_RESULT"
    ] = "${{ runner.temp }}/openai-preview-accepted-consumer-result.json"
    expect_rejected(
        "consumer_runner_temp_scope",
        consumer_job_runner_context,
        consumer_text,
        validate_consumer,
    )

    consumer_preflight_runner_context = copy.deepcopy(consumer)
    consumer_preflight_runner_context["jobs"]["validate-source-run"]["env"] = {
        "BAD": "${{ runner.temp }}/x"
    }
    expect_rejected(
        "consumer_runner_temp_scope",
        consumer_preflight_runner_context,
        consumer_text,
        validate_consumer,
    )

    consumer_compact_runner_context = copy.deepcopy(consumer)
    consumer_compact_runner_context["jobs"]["verify-accepted-summary"]["env"][
        "BAD"
    ] = "${{runner.temp}}/x"
    expect_rejected(
        "consumer_runner_temp_scope",
        consumer_compact_runner_context,
        consumer_text,
        validate_consumer,
    )

    consumer_extra_step = copy.deepcopy(consumer)
    consumer_extra_step["jobs"]["verify-accepted-summary"]["steps"].insert(
        3, {"name": "Unreviewed extra command", "run": "echo extra"}
    )
    expect_rejected(
        "workflow_steps", consumer_extra_step, consumer_text, validate_consumer
    )

    consumer_overwrite = copy.deepcopy(consumer)
    next(
        item
        for item in consumer_overwrite["jobs"]["verify-accepted-summary"]["steps"]
        if item.get("name") == "Publish the non-overwriting consumer result"
    )["with"]["overwrite"] = "true"
    expect_rejected(
        "consumer_result", consumer_overwrite, consumer_text, validate_consumer
    )

    consumer_always_upload = copy.deepcopy(consumer)
    next(
        item
        for item in consumer_always_upload["jobs"]["verify-accepted-summary"][
            "steps"
        ]
        if item.get("name") == "Publish the non-overwriting consumer result"
    )["if"] = "${{ always() }}"
    expect_rejected(
        "consumer_result",
        consumer_always_upload,
        consumer_text,
        validate_consumer,
    )

    consumer_unbound_artifact = copy.deepcopy(consumer)
    next(
        item
        for item in consumer_unbound_artifact["jobs"]["verify-accepted-summary"][
            "steps"
        ]
        if item.get("name") == "Publish the non-overwriting consumer result"
    )["with"]["name"] = "openai-preview-accepted-consumer"
    expect_rejected(
        "consumer_result",
        consumer_unbound_artifact,
        consumer_text,
        validate_consumer,
    )

    consumer_upload_first = copy.deepcopy(consumer)
    consumer_job_steps = consumer_upload_first["jobs"]["verify-accepted-summary"][
        "steps"
    ]
    consumer_job_steps[0], consumer_job_steps[-1] = (
        consumer_job_steps[-1],
        consumer_job_steps[0],
    )
    expect_rejected(
        "consumer_order", consumer_upload_first, consumer_text, validate_consumer
    )

    consumer_mutable_action = copy.deepcopy(consumer)
    next(
        item
        for item in consumer_mutable_action["jobs"]["verify-accepted-summary"]["steps"]
        if "uses" in item
    )["uses"] = "actions/checkout@v4"
    expect_rejected(
        "workflow_action_pin",
        consumer_mutable_action,
        consumer_text,
        validate_consumer,
    )
    return 58


def main() -> int:
    main_document, main_text = load(MAIN_PATH)
    evidence_document, evidence_text = load(EVIDENCE_PATH)
    accepted_document, accepted_text = load(ACCEPTED_PATH)
    consumer_document, consumer_text = load(CONSUMER_PATH)
    draft_document, draft_text = load(DRAFT_VERIFIER_PATH)
    validate_main(main_document, main_text)
    validate_evidence(evidence_document, evidence_text)
    validate_accepted(accepted_document, accepted_text)
    validate_consumer(consumer_document, consumer_text)
    validate_draft_verifier(draft_document, draft_text)
    mutation_count = validate_mutation_guards(
        main_document,
        main_text,
        evidence_document,
        evidence_text,
        accepted_document,
        accepted_text,
        consumer_document,
        consumer_text,
    )
    draft_mutable_action = copy.deepcopy(draft_document)
    next(item for item in steps(draft_mutable_action) if "uses" in item)["uses"] = (
        "actions/checkout@v4"
    )
    expect_rejected(
        "workflow_action_pin",
        draft_mutable_action,
        draft_text,
        validate_draft_verifier,
    )
    draft_read_only = copy.deepcopy(draft_document)
    draft_read_only["permissions"] = {"actions": "read", "contents": "read"}
    expect_rejected(
        "workflow_permissions",
        draft_read_only,
        draft_text,
        validate_draft_verifier,
    )
    draft_wrong_ref = copy.deepcopy(draft_document)
    next(
        item
        for item in steps(draft_wrong_ref)
        if str(item.get("uses", "")).startswith("actions/checkout@")
    )["with"]["ref"] = "main"
    expect_rejected(
        "draft_verifier_checkout",
        draft_wrong_ref,
        draft_text,
        validate_draft_verifier,
    )
    mutation_count += 3
    print("OpenAI Preview workflow invariants passed")
    print(
        "coverage: pinned actions, least-privilege read permissions, immutable tag/commit, "
        "prerelease assets, offline verifier, fail-closed empty assets, protected accepted-state "
        "production callbacks, immutable trusted checkout, independent workflow-run consumer, "
        "no hosted capture; "
        f"mutation guards={mutation_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
