#!/usr/bin/env python3
"""Validate Phase 6 discovery policy, context proxies, and entry quickstarts."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import yaml

from openai_ui_utils import (
    SHORT_DESCRIPTION_MAX,
    SHORT_DESCRIPTION_MIN,
    short_description_error,
)


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"
REGISTRY = PLUGIN / "workflow-registry.yaml"
README = PLUGIN / "README.md"
ROUTING_RECEIPTS = REPO / "tests" / "openai_phase6" / "quickstart-routing-receipts.yaml"
REPORT = PLUGIN / "reports" / "phase6-context-measurement.md"

EXPECTED_PUBLIC_ENTRIES = {
    "academic-deep-search",
    "article-orchestrator",
    "perspective-orchestrator",
    "proposal-orchestrator",
    "research-idea-orchestrator",
    "research-opportunity-mapper",
    "research-polisher-orchestrator",
}
EXPECTED_IMPLICIT_ENTRIES = EXPECTED_PUBLIC_ENTRIES - {
    "research-polisher-orchestrator"
}
DESCRIPTION_PROXY_LIMIT = 6_200
ORCHESTRATOR_PROXY_LIMIT = 13_400
DESCRIPTION_REGRESSION_LIMIT = 6_171
ORCHESTRATOR_REGRESSION_LIMITS = {
    "research-idea-orchestrator": 13_354,
    "proposal-orchestrator": 13_288,
    "article-orchestrator": 13_146,
}
TOUCHED_SKILL_BODY_REGRESSION_LIMIT = 73_043
TOUCHED_SKILLS = {
    "research-idea-orchestrator", "multi-path-idea-generator", "idea-evaluator",
    "idea-portfolio-assembler", "proposal-orchestrator", "proposal-evaluator",
    "proposal-drafter", "sap-evaluator", "article-orchestrator",
    "article-architect", "article-drafter", "article-evaluator",
    "article-refinement-controller", "article-submission-compositor",
}
QUICKSTART_FIELDS = ("Minimum input:", "Expected output:", "Stop states:", "Resume:")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_repository_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(
        path.read_bytes().replace(b"\r\n", b"\n")
    ).hexdigest()


def frontmatter(path: Path) -> dict[str, object]:
    text = read(path)
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"{path}: unclosed frontmatter")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError(f"{path}: invalid frontmatter mapping")
    return data


def quickstart_segment(readme: str, name: str) -> str | None:
    heading = f"### `${name}`"
    start = readme.find(heading)
    if start < 0:
        return None
    next_heading = readme.find("\n### ", start + len(heading))
    return readme[start:] if next_heading < 0 else readme[start:next_heading]


def main() -> int:
    errors: list[str] = []
    registry = yaml.safe_load(read(REGISTRY))
    entries = registry.get("skills", []) if isinstance(registry, dict) else []
    registered_names = [entry.get("name") for entry in entries]
    if not registered_names or any(not isinstance(name, str) for name in registered_names):
        errors.append("registry skill names are missing or invalid")
    if len(registered_names) != len(set(registered_names)):
        errors.append("registry contains duplicate skill names")

    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    descriptions: dict[str, str] = {}
    for skill_file in skill_files:
        try:
            data = frontmatter(skill_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or name != skill_file.parent.name:
            errors.append(f"{skill_file}: name does not match its directory")
            continue
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{skill_file}: description is missing")
            continue
        descriptions[name] = description

    if set(descriptions) != set(registered_names):
        missing = sorted(set(registered_names) - set(descriptions))
        extra = sorted(set(descriptions) - set(registered_names))
        errors.append(f"source/registry skill mismatch; missing={missing}, extra={extra}")

    implicit_names = {
        entry["name"]
        for entry in entries
        if isinstance(entry, dict) and entry.get("invocation_policy") == "implicit"
    }
    public_entry_policy = registry.get("public_entry_policy", {})
    public_names = set(public_entry_policy.get("declared_entries", []))
    if public_names != EXPECTED_PUBLIC_ENTRIES:
        errors.append(
            "declared public entry boundary changed: "
            f"expected={sorted(EXPECTED_PUBLIC_ENTRIES)}, actual={sorted(public_names)}"
        )
    if implicit_names != EXPECTED_IMPLICIT_ENTRIES:
        errors.append(
            "active implicit entry boundary changed: "
            f"expected={sorted(EXPECTED_IMPLICIT_ENTRIES)}, actual={sorted(implicit_names)}"
        )
    if set(public_entry_policy.get("implicit_active_entries", [])) != implicit_names:
        errors.append("public entry policy and per-skill implicit policies disagree")

    short_descriptions_valid = 0
    for name in sorted(descriptions):
        policy_path = SKILLS / name / "agents" / "openai.yaml"
        if not policy_path.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")
            continue
        policy_data = yaml.safe_load(read(policy_path)) or {}
        interface = policy_data.get("interface", {}) if isinstance(policy_data, dict) else {}
        short_error = short_description_error(interface.get("short_description"))
        if short_error:
            errors.append(f"{name}: {short_error}")
        else:
            short_descriptions_valid += 1
        allow = policy_data.get("policy", {}).get("allow_implicit_invocation")
        expected = name in implicit_names
        if allow is not expected:
            errors.append(
                f"{name}: allow_implicit_invocation={allow!r}, expected {expected!r}"
            )

    short_description_boundary_cases = (
        ("minimum accepted", "x" * SHORT_DESCRIPTION_MIN, True),
        ("maximum accepted", "x" * SHORT_DESCRIPTION_MAX, True),
        ("below minimum rejected", "x" * (SHORT_DESCRIPTION_MIN - 1), False),
        ("above maximum rejected", "x" * (SHORT_DESCRIPTION_MAX + 1), False),
    )
    short_description_boundary_guards = 0
    for label, value, expected_valid in short_description_boundary_cases:
        actual_valid = short_description_error(value) is None
        if actual_valid is not expected_valid:
            errors.append(f"short-description boundary guard failed: {label}")
        else:
            short_description_boundary_guards += 1

    description_chars = sum(len(value) for value in descriptions.values())
    if description_chars > DESCRIPTION_PROXY_LIMIT:
        errors.append(
            f"all-skill description proxy exceeds {DESCRIPTION_PROXY_LIMIT}: {description_chars}"
        )
    if description_chars > DESCRIPTION_REGRESSION_LIMIT:
        errors.append(
            "all-skill descriptions grew beyond the 9f64ad3 regression baseline: "
            f"{description_chars}/{DESCRIPTION_REGRESSION_LIMIT}"
        )

    orchestrators = {
        entry["name"]
        for entry in entries
        if isinstance(entry, dict) and entry.get("role") == "orchestrator"
    }
    if not orchestrators:
        errors.append("registry declares no orchestrators")
    orchestrator_proxies: dict[str, int] = {}
    for name in sorted(orchestrators):
        skill_path = SKILLS / name / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"{name}: orchestrator SKILL.md is missing")
            continue
        proxy = description_chars + len(read(skill_path))
        orchestrator_proxies[name] = proxy
        if proxy > ORCHESTRATOR_PROXY_LIMIT:
            errors.append(
                f"{name}: description+full-SKILL proxy exceeds "
                f"{ORCHESTRATOR_PROXY_LIMIT}: {proxy}"
            )
        regression_limit = ORCHESTRATOR_REGRESSION_LIMITS.get(name)
        if regression_limit is not None and proxy > regression_limit:
            errors.append(
                f"{name}: initial-load proxy grew beyond the 9f64ad3 baseline "
                f"{proxy}/{regression_limit}"
            )

    touched_body_chars = sum(
        len(read(SKILLS / name / "SKILL.md")) for name in TOUCHED_SKILLS
    )
    if touched_body_chars > TOUCHED_SKILL_BODY_REGRESSION_LIMIT:
        errors.append(
            "touched SKILL.md bodies grew beyond the 9f64ad3 aggregate baseline: "
            f"{touched_body_chars}/{TOUCHED_SKILL_BODY_REGRESSION_LIMIT}"
        )

    readme = read(README)
    if "## Entry-skill quickstarts" not in readme:
        errors.append("README lacks the entry-skill quickstarts section")
    state_machines = registry.get("workflow_state_machines", {})
    modes_by_orchestrator = {
        machine.get("orchestrator"): set(machine.get("entry_modes", []))
        for machine in state_machines.values()
        if isinstance(machine, dict) and isinstance(machine.get("orchestrator"), str)
    }
    quickstarts_passed = 0
    quickstart_prompts: dict[str, str] = {}
    for name in sorted(public_names):
        error_count_before = len(errors)
        segment = quickstart_segment(readme, name)
        if segment is None:
            errors.append(f"README quickstart missing: {name}")
            continue
        for field in QUICKSTART_FIELDS:
            if field not in segment:
                errors.append(f"{name} quickstart lacks `{field}`")
        blocks = re.findall(r"```text\n(.*?)\n```", segment, flags=re.S)
        if len(blocks) != 1:
            errors.append(f"{name} quickstart must contain one copy-paste text block")
            continue
        prompt = blocks[0]
        quickstart_prompts[name] = prompt
        if f"${name}" not in prompt:
            errors.append(f"{name} quickstart does not explicitly invoke its entry skill")
        unrelated = sorted(other for other in public_names - {name} if f"${other}" in prompt)
        if unrelated:
            errors.append(f"{name} quickstart invokes unrelated public skills: {unrelated}")
        missing_modes = sorted(mode for mode in modes_by_orchestrator.get(name, set()) if mode not in prompt)
        if missing_modes:
            errors.append(f"{name} quickstart omits declared entry modes: {missing_modes}")
        if len(errors) == error_count_before:
            quickstarts_passed += 1

    routing_smokes_passed = 0
    historical_routing_smokes = 0
    routing_receipts_current = False
    if not ROUTING_RECEIPTS.is_file():
        errors.append("Phase 6 fresh-subagent routing receipts are missing")
    else:
        receipts = yaml.safe_load(read(ROUTING_RECEIPTS))
        if receipts.get("schema_version") != 1:
            errors.append("Phase 6 routing receipt schema is invalid")
        if receipts.get("evidence_class") != "current_task_self_attested_routing_snapshot":
            errors.append("Phase 6 routing receipts do not claim the expected evidence class")
        if (
            receipts.get("verification_level") != "self_attested_current_task_snapshot"
            or receipts.get("portable_platform_execution_export_available") is not False
        ):
            errors.append("Phase 6 routing receipt verification boundary is invalid")
        routing_receipts_current = (
            receipts.get("plugin_version") == registry.get("plugin_version")
        )
        execution = receipts.get("execution_contract", {})
        if (
            execution.get("isolation_mode") != "fresh_subagent"
            or execution.get("routing_only") is not True
            or execution.get("full_workflow_executed") is not False
            or execution.get("unrelated_public_skill_read_forbidden") is not True
        ):
            errors.append("Phase 6 routing execution contract is invalid")
        runs = receipts.get("runs", [])
        receipt_entries = {run.get("public_entry") for run in runs}
        if routing_receipts_current and receipt_entries != public_names:
            errors.append("Phase 6 routing receipt entries differ from the public-entry set")
        elif not routing_receipts_current and not receipt_entries <= set(registered_names):
            errors.append("historical Phase 6 routing receipt names are not registered skills")
        instance_ids: set[str] = set()
        for run in runs:
            error_count_before = len(errors)
            name = run.get("public_entry")
            contract = run.get("routing_contract", {})
            prompt = str(run.get("prompt", ""))
            instance_id = contract.get("reviewer_instance_id")
            if contract.get("selected_skill") != name:
                errors.append(f"{name}: fresh routing selected {contract.get('selected_skill')!r}")
            if f"${name}" not in prompt:
                errors.append(f"{name}: fresh routing prompt does not explicitly invoke the entry")
            if routing_receipts_current and run.get(
                "quickstart_template_sha256"
            ) != sha256_text(quickstart_prompts.get(str(name), "")):
                errors.append(f"{name}: README quickstart template digest is missing or stale")
            if run.get("prompt_sha256") != sha256_text(prompt):
                errors.append(f"{name}: routing prompt digest is missing or stale")
            skill_path = SKILLS / str(name) / "SKILL.md"
            if not skill_path.is_file():
                errors.append(f"{name}: routing source skill is missing")
            elif routing_receipts_current and run.get(
                "skill_sha256"
            ) != sha256_repository_file(skill_path):
                errors.append(f"{name}: routing source skill digest is missing or stale")
            elif not routing_receipts_current and not re.fullmatch(
                r"sha256:[0-9a-f]{64}", str(run.get("skill_sha256", ""))
            ):
                errors.append(f"{name}: historical routing skill digest is invalid")
            unrelated_prompt_entries = sorted(
                other for other in public_names - {name} if f"${other}" in prompt
            )
            if unrelated_prompt_entries:
                errors.append(f"{name}: routing prompt names unrelated entries: {unrelated_prompt_entries}")
            if not instance_id or instance_id in instance_ids:
                errors.append(f"{name}: routing instance is missing or reused: {instance_id}")
            else:
                instance_ids.add(instance_id)
            expected_file = f"research-skills-openai/skills/{name}/SKILL.md"
            if contract.get("files_read") != [expected_file]:
                errors.append(f"{name}: fresh routing read scope is not isolated")
            if contract.get("unrelated_public_skill_files_read") != []:
                errors.append(f"{name}: fresh routing loaded an unrelated public skill")
            if contract.get("minimum_input_sufficient") is not True:
                errors.append(f"{name}: quickstart minimum input was not sufficient")
            if contract.get("source_edits_performed") is not False:
                errors.append(f"{name}: routing smoke performed a source edit")
            if len(errors) == error_count_before:
                if routing_receipts_current:
                    routing_smokes_passed += 1
                else:
                    historical_routing_smokes += 1

    public_description_chars = sum(len(descriptions[name]) for name in public_names)
    max_proxy = max(orchestrator_proxies.values(), default=0)
    if not REPORT.is_file():
        errors.append("Phase 6 context measurement report is missing")
    else:
        report = read(REPORT)
        expected_report_markers = {
            "Status: Complete",
            "ChatGPT web: not tested",
            f"`{registry.get('plugin_version')}`",
            f"| Declared-entry descriptions | {public_description_chars:,} | Informational |",
            f"| All {len(registered_names)} descriptions | {description_chars:,} | {DESCRIPTION_PROXY_LIMIT:,} |",
            "routing snapshot",
            "SHA-256",
        }
        expected_report_markers.update(f"`{name}`" for name in public_names)
        for name, proxy in orchestrator_proxies.items():
            label = name.removesuffix("-orchestrator").capitalize()
            expected_report_markers.add(
                f"| {label} orchestrator proxy | {proxy:,} | {ORCHESTRATOR_PROXY_LIMIT:,} |"
            )
        missing_report_markers = sorted(
            marker for marker in expected_report_markers if marker not in report
        )
        if missing_report_markers:
            errors.append(
                "Phase 6 context measurement report is stale: "
                + ", ".join(missing_report_markers)
            )
    print("OpenAI Phase 6 context validation")
    print(f"source skills (derived from registry): {len(registered_names)}")
    print(f"declared entries: {len(public_names)}/{len(EXPECTED_PUBLIC_ENTRIES)}")
    print(
        "implicit-active entries: "
        f"{len(implicit_names)}/{len(EXPECTED_IMPLICIT_ENTRIES)} "
        "(personal-owner; Research Polisher explicit-only)"
    )
    print(f"non-implicit roles: {len(registered_names) - len(implicit_names)}")
    print(
        "short-description range: "
        f"{short_descriptions_valid}/{len(registered_names)} "
        f"({SHORT_DESCRIPTION_MIN}-{SHORT_DESCRIPTION_MAX} characters)"
    )
    print(
        "short-description boundary guards: "
        f"{short_description_boundary_guards}/{len(short_description_boundary_cases)}"
    )
    print(f"declared-entry description characters: {public_description_chars}")
    print(f"all-skill description proxy: {description_chars}/{DESCRIPTION_PROXY_LIMIT}")
    print(
        "description regression baseline: "
        f"{description_chars}/{DESCRIPTION_REGRESSION_LIMIT}"
    )
    for name, proxy in sorted(orchestrator_proxies.items()):
        print(f"{name} conservative description+full-SKILL proxy: {proxy}/{ORCHESTRATOR_PROXY_LIMIT}")
    print(f"maximum orchestrator proxy: {max_proxy}/{ORCHESTRATOR_PROXY_LIMIT}")
    print(
        "touched SKILL.md aggregate regression baseline: "
        f"{touched_body_chars}/{TOUCHED_SKILL_BODY_REGRESSION_LIMIT}"
    )
    print(f"quickstarts: {quickstarts_passed}/{len(public_names)}")
    print(f"fresh-subagent routing smokes: {routing_smokes_passed}/{len(public_names)}")
    print(
        "historical routing smokes retained: "
        f"{historical_routing_smokes}; current-version receipts: "
        f"{'yes' if routing_receipts_current else 'pending'}"
    )
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
