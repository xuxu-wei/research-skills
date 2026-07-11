#!/usr/bin/env python3
"""Portable release validation for the OpenAI Preview plugin and marketplace."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def parse_semver(value: str) -> tuple[tuple[int, int, int], tuple[int | str, ...] | None] | None:
    match = SEMVER_PATTERN.fullmatch(value)
    if not match:
        return None
    prerelease: tuple[int | str, ...] | None = None
    if match.group(4) is not None:
        identifiers: list[int | str] = []
        for identifier in match.group(4).split("."):
            if identifier.isdigit():
                if len(identifier) > 1 and identifier.startswith("0"):
                    return None
                identifiers.append(int(identifier))
            else:
                identifiers.append(identifier)
        prerelease = tuple(identifiers)
    return (int(match.group(1)), int(match.group(2)), int(match.group(3))), prerelease


def compare_semver(left: str, right: str) -> int:
    parsed_left = parse_semver(left)
    parsed_right = parse_semver(right)
    if parsed_left is None or parsed_right is None:
        raise ValueError("invalid SemVer")
    left_core, left_prerelease = parsed_left
    right_core, right_prerelease = parsed_right
    if left_core != right_core:
        return -1 if left_core < right_core else 1
    if left_prerelease is None or right_prerelease is None:
        if left_prerelease is right_prerelease:
            return 0
        return 1 if left_prerelease is None else -1
    for left_identifier, right_identifier in zip(left_prerelease, right_prerelease):
        if left_identifier == right_identifier:
            continue
        if isinstance(left_identifier, int) and isinstance(right_identifier, str):
            return -1
        if isinstance(left_identifier, str) and isinstance(right_identifier, int):
            return 1
        return -1 if left_identifier < right_identifier else 1
    if len(left_prerelease) == len(right_prerelease):
        return 0
    return -1 if len(left_prerelease) < len(right_prerelease) else 1


def markdown_h2_section(markdown: str, title: str) -> str | None:
    heading = re.search(rf"^##[ \t]+{re.escape(title)}(?:[ \t]+.*)?$", markdown, re.MULTILINE)
    if not heading:
        return None
    next_heading = re.search(r"^##[ \t]+", markdown[heading.end() :], re.MULTILINE)
    end = heading.end() + next_heading.start() if next_heading else len(markdown)
    return markdown[heading.start() : end]


def section_status(section: str) -> str | None:
    status_pattern = re.compile(
        r"^Status:[ \t]*(?P<status>[A-Za-z][0-9A-Za-z_-]*)"
        r"(?:[ \t]+\([^\r\n)]*\))?[ \t]*$"
    )
    for line in section.splitlines()[1:]:
        if not line.strip():
            continue
        match = status_pattern.fullmatch(line)
        return match.group("status").lower() if match else None
    return None


def validate_phase5_upgrade_receipt(upgrade: str, current_version: str) -> list[str]:
    errors: list[str] = []
    required_upgrade_evidence = (
        "Status: upgrade_verified",
        current_version,
        '"discovery_status": "verified"',
        '"skill_count": 45',
        '"pubmed_present": false',
        "human_signoff_required",
    )
    for marker in required_upgrade_evidence:
        if marker not in upgrade:
            errors.append(f"Phase 5 upgrade receipt missing evidence: {marker}")

    automatic_submission_false = any(
        re.search(pattern, upgrade, re.MULTILINE)
        for pattern in (
            r'^[ \t]*(?:[-*][ \t]+)?["`]?automatic_external_submission["`]?[ \t]*:[ \t]*false[ \t]*[,.]?[ \t]*$',
            r"^[ \t]*-[ \t]+`automatic_external_submission`[ \t]+remains[ \t]+`false`\.[ \t]*$",
        )
    )
    if not automatic_submission_false:
        errors.append("Phase 5 upgrade receipt does not prove automatic_external_submission: false")

    baseline_match = re.search(
        r"^1\.[ \t]+The previously installed[^\r\n]*:[ \t]*\r?\n"
        r"[ \t]*-[ \t]+version:[ \t]+`([^`]+)`[ \t]*$",
        upgrade,
        re.MULTILINE,
    )
    if not baseline_match:
        errors.append("Phase 5 upgrade receipt lacks an installed baseline version")
    else:
        baseline_version = baseline_match.group(1)
        if parse_semver(baseline_version) is None:
            errors.append(f"Phase 5 upgrade receipt baseline is not SemVer: {baseline_version}")
        elif parse_semver(current_version) is not None and compare_semver(baseline_version, current_version) >= 0:
            errors.append(
                "Phase 5 upgrade receipt baseline must be strictly older than "
                f"the current version: {baseline_version} !< {current_version}"
            )

    actions_chain = re.search(
        r"^2\.[ \t]+GitHub `main` was updated to commit `(?P<commit>[0-9a-f]{40})`[^\r\n]*\r?\n"
        r"3\.[ \t]+GitHub Actions run `[0-9]+`[^\r\n]*conclusion `success` for "
        r"(?:that commit|commit `(?P=commit)`):[ \t]*$",
        upgrade,
        re.MULTILINE,
    )
    if not actions_chain:
        errors.append(
            "Phase 5 upgrade receipt does not bind a successful GitHub Actions run "
            "to the same full commit SHA"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    registry = yaml.safe_load((PLUGIN / "workflow-registry.yaml").read_text(encoding="utf-8"))
    marketplace = json.loads((REPO / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    version = str(manifest.get("version", ""))

    if parse_semver(version) is None:
        errors.append(f"manifest version is not release SemVer without build metadata: {version}")
    if "+codex." in version:
        errors.append("main Preview manifest contains a local cachebuster")
    if registry.get("plugin_version") != version:
        errors.append("manifest and registry versions differ")
    if registry.get("schema_version") != 5:
        errors.append("release requires registry schema 5")
    if manifest.get("name") != "research-skills-openai" or manifest.get("skills") != "./skills/":
        errors.append("plugin manifest identity or skills path is invalid")

    product_text = " ".join(
        [
            str(manifest.get("description", "")),
            str(manifest.get("interface", {}).get("displayName", "")),
            str(manifest.get("interface", {}).get("longDescription", "")),
        ]
    ).lower()
    if "preview" not in product_text or "experimental" not in product_text:
        errors.append("plugin is not clearly labeled Preview/Experimental")
    if registry.get("workflow_state_policy", {}).get("final_handoff_state") != "human_signoff_required":
        errors.append("final workflow state is not human_signoff_required")
    if registry.get("scenario_eval_contract", {}).get("automatic_external_submission") is not False:
        errors.append("release contract does not prohibit automatic external submission")

    entries = [item for item in marketplace.get("plugins", []) if item.get("name") == "research-skills-openai"]
    if len(entries) != 1:
        errors.append(f"marketplace must contain exactly one plugin entry, found {len(entries)}")
    else:
        entry = entries[0]
        expected_source = {
            "source": "git-subdir",
            "url": "https://github.com/xuxu-wei/research-skills.git",
            "path": "./research-skills-openai",
            "ref": "main",
        }
        if entry.get("source") != expected_source:
            errors.append("marketplace must track the GitHub main git-subdir source")
        if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            errors.append("marketplace policy is invalid")
        if entry.get("category") != "Research":
            errors.append("marketplace category is invalid")

    phase4_path = PLUGIN / "reports" / "phase4-scenario-results.json"
    if not phase4_path.is_file():
        errors.append("Phase 4 scenario report is missing")
    else:
        phase4 = json.loads(phase4_path.read_text(encoding="utf-8"))
        if phase4.get("plugin_version") != version:
            errors.append("Phase 4 report version differs from the plugin")
        summary = phase4.get("summary", {})
        if (
            summary.get("workflows_passed") != 4
            or summary.get("negative_guards_rejected", 0) < 39
            or summary.get("finding_routes_verified") != 5
            or summary.get("live_workflows_receipts_audited") != 4
            or summary.get("live_workflows_reached_human_signoff_gate") != 0
            or summary.get("live_workflows_stopped_at_valid_gate") != 2
            or summary.get("live_workflows_blocked_at_valid_gate") != 1
            or summary.get("live_workflows_independent_review_pending") != 1
            or summary.get("live_raw_state_claims_corrected") != 2
        ):
            errors.append("Phase 4 scenario or negative-guard coverage is incomplete")
        if summary.get("automatic_external_submission") is not False:
            errors.append("Phase 4 report permits automatic external submission")

    validation_path = PLUGIN / "reports" / "validation.json"
    if not validation_path.is_file():
        errors.append("portable plugin validation report is missing")
    else:
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if (
            validation.get("plugin_version") != version
            or validation.get("registry_schema_version") != registry.get("schema_version")
            or validation.get("expected_skill_count") != 45
            or validation.get("ok") is not True
        ):
            errors.append("portable plugin validation report is stale or invalid")

    workflow_path = REPO / ".github" / "workflows" / "openai-plugin-preview.yml"
    if not workflow_path.is_file():
        errors.append("GitHub Actions Preview validation workflow is missing")
    else:
        workflow = workflow_path.read_text(encoding="utf-8")
        for command in (
            "audit_openai_research_plugin.py",
            "test_openai_phase2_phase3.py",
            "test_openai_phase4_scenarios.py --check-report",
            "codex_plugin_converter.py --mode codex --fail-on-invalid",
            "validate_openai_preview_release.py",
            "check_openai_version_bump.py",
        ):
            if command not in workflow:
                errors.append(f"CI workflow missing command: {command}")

    roadmap = (PLUGIN / "ROADMAP.md").read_text(encoding="utf-8")
    phase5_section = markdown_h2_section(roadmap, "Phase 5")
    if phase5_section is None:
        errors.append("Roadmap Phase 5 section is missing")
    elif section_status(phase5_section) == "complete":
        upgrade_path = PLUGIN / "reports" / "phase5-upgrade-smoke.md"
        if not upgrade_path.is_file():
            errors.append("Phase 5 is marked complete without a verified upgrade receipt")
        else:
            upgrade = upgrade_path.read_text(encoding="utf-8")
            errors.extend(validate_phase5_upgrade_receipt(upgrade, version))

    if errors:
        print("OpenAI Preview release validation failed")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OpenAI Preview release validation passed")
    print(f"version: {version}")
    print("skills: 45")
    print("channel: GitHub main Preview")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
