#!/usr/bin/env python3
"""Portable release validation for the OpenAI Preview plugin and marketplace."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    registry = yaml.safe_load((PLUGIN / "workflow-registry.yaml").read_text(encoding="utf-8"))
    marketplace = json.loads((REPO / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    version = str(manifest.get("version", ""))

    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        errors.append(f"manifest version is not release SemVer without build metadata: {version}")
    if "+codex." in version:
        errors.append("main Preview manifest contains a local cachebuster")
    if registry.get("plugin_version") != version:
        errors.append("manifest and registry versions differ")
    if registry.get("schema_version") != 4:
        errors.append("release requires registry schema 4")
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
        if summary.get("workflows_passed") != 4 or summary.get("negative_guards_rejected", 0) < 10:
            errors.append("Phase 4 scenario or negative-guard coverage is incomplete")
        if summary.get("automatic_external_submission") is not False:
            errors.append("Phase 4 report permits automatic external submission")

    validation_path = PLUGIN / "reports" / "validation.json"
    if not validation_path.is_file():
        errors.append("portable plugin validation report is missing")
    else:
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if validation.get("plugin_version") != version or validation.get("expected_skill_count") != 45 or validation.get("ok") is not True:
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
    if "Phase 5" in roadmap and "Status: Complete" in roadmap.split("## Phase 5", 1)[-1]:
        upgrade_path = PLUGIN / "reports" / "phase5-upgrade-smoke.md"
        if not upgrade_path.is_file() or "Status: `upgrade_verified`" not in upgrade_path.read_text(encoding="utf-8"):
            errors.append("Phase 5 is marked complete without a verified upgrade receipt")

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
