#!/usr/bin/env python3
"""Validate the personal-owner anonymous corpus and bounded repeat set."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
CORPUS = REPO / "tests" / "openai_phase8" / "corpus.yaml"
REPEATS = REPO / "tests" / "openai_phase8" / "fresh-repeat-runs.yaml"
REPORT = PLUGIN / "reports" / "phase8-corpus-results.json"
WORKFLOWS = {"idea", "proposal", "article", "perspective", "research_polisher"}
OUTCOMES = {"happy", "fixable", "fatal_or_pending", "revision_no_gain"}
READY_STATES = {"human_signoff_required", "human_strategy_selection_required"}
LINEAGE_FIELDS = {"artifact_id", "version_id", "round_id", "plugin_version_binding", "source_skill", "based_on", "change_type"}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def percent(passed: int, total: int) -> float:
    return 100.0 if total == 0 else round(100.0 * passed / total, 2)


def build_report() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    version = str(json.loads(MANIFEST.read_text(encoding="utf-8")).get("version", ""))
    corpus = load_yaml(CORPUS)
    repeats = load_yaml(REPEATS)
    cases = corpus.get("cases", [])
    require(corpus.get("evidence_class") == "synthetic_contract_oracle", "corpus evidence class is invalid", errors)
    require(corpus.get("runtime_claim") == "none", "corpus must not claim runtime evidence", errors)
    require(isinstance(cases, list) and len(cases) == 20, "expected 20 anonymous corpus cases", errors)

    coverage: dict[str, set[str]] = {workflow: set() for workflow in WORKFLOWS}
    case_results: list[dict[str, Any]] = []
    fatal_total = fatal_detected = 0
    major_total = major_detected = 0
    lineage_passed = isolation_passed = edit_passed = dissent_passed = 0
    false_ready_count = 0

    for case in cases if isinstance(cases, list) else []:
        if not isinstance(case, dict):
            errors.append("malformed corpus case")
            continue
        case_id = str(case.get("case_id", ""))
        workflow = str(case.get("workflow", ""))
        outcome = str(case.get("outcome_class", ""))
        coverage.setdefault(workflow, set()).add(outcome)
        expected = case.get("expected", {})
        observed = case.get("oracle_observation", {})
        anonymity = case.get("anonymity", {})
        case_errors: list[str] = []
        require(workflow in WORKFLOWS, f"{case_id}: unknown workflow", case_errors)
        require(outcome in OUTCOMES, f"{case_id}: unknown outcome", case_errors)
        require(anonymity.get("source_kind") == "synthetic", f"{case_id}: source is not synthetic", case_errors)
        require(anonymity.get("contains_identifying_material") is False, f"{case_id}: identifying material present", case_errors)
        require(expected.get("route") == observed.get("route"), f"{case_id}: route mismatch", case_errors)
        require(expected.get("final_state") == observed.get("final_state"), f"{case_id}: final-state mismatch", case_errors)
        outputs = set(observed.get("outputs", []))
        require(set(expected.get("required_outputs", [])) <= outputs, f"{case_id}: required output missing", case_errors)
        require(not (set(expected.get("forbidden_outputs", [])) & outputs), f"{case_id}: forbidden output present", case_errors)

        detected = set(observed.get("detected_finding_ids", []))
        findings = expected.get("critical_findings", [])
        fatal_ids = {item.get("finding_id") for item in findings if isinstance(item, dict) and (item.get("severity") == "fatal" or item.get("blocking") is True)}
        major_ids = {item.get("finding_id") for item in findings if isinstance(item, dict) and item.get("severity") in {"major", "fatal"}}
        fatal_total += len(fatal_ids)
        fatal_detected += len(fatal_ids & detected)
        major_total += len(major_ids)
        major_detected += len(major_ids & detected)
        require(fatal_ids <= detected, f"{case_id}: fatal/blocking finding missed", case_errors)
        require(major_ids <= detected, f"{case_id}: major finding missed", case_errors)

        lineage = observed.get("lineage", {})
        lineage_ok = isinstance(lineage, dict) and LINEAGE_FIELDS <= set(lineage) and all(lineage.get(field) not in (None, "") for field in LINEAGE_FIELDS)
        require(lineage_ok, f"{case_id}: lineage incomplete", case_errors)
        lineage_passed += int(lineage_ok)

        isolation = observed.get("isolation", {})
        isolation_ok = (
            isolation.get("fresh_subagent") is True
            and isolation.get("writer_instance_id") != isolation.get("reviewer_instance_id")
            and isolation.get("prior_scores_visible") is False
        )
        require(isolation_ok, f"{case_id}: reviewer isolation failed", case_errors)
        isolation_passed += int(isolation_ok)

        boundary = observed.get("edit_boundary", {})
        prefixes = tuple(boundary.get("allowed_prefixes", []))
        write_paths = boundary.get("reviewer_write_paths", [])
        edit_ok = boundary.get("source_edits_performed_by_reviewer") is False and bool(prefixes) and all(str(path).startswith(prefixes) for path in write_paths)
        require(edit_ok, f"{case_id}: reviewer edit boundary failed", case_errors)
        edit_passed += int(edit_ok)

        expected_dissent = set(expected.get("dissent_ids", []))
        preserved_dissent = set(observed.get("preserved_dissent_ids", []))
        dissent_ok = expected_dissent <= preserved_dissent
        require(dissent_ok, f"{case_id}: dissent was not preserved", case_errors)
        dissent_passed += int(dissent_ok)

        false_ready = bool(fatal_ids) and (observed.get("ready_claimed") is True or observed.get("final_state") in READY_STATES)
        false_ready_count += int(false_ready)
        require(not false_ready, f"{case_id}: false-ready result", case_errors)
        errors.extend(case_errors)
        case_results.append(
            {
                "case_id": case_id,
                "workflow": workflow,
                "outcome_class": outcome,
                "risk_tier": case.get("risk_tier"),
                "expected_state": expected.get("final_state"),
                "status": "passed" if not case_errors else "failed",
            }
        )

    require(set(coverage) == WORKFLOWS, "corpus workflow coverage differs", errors)
    for workflow in WORKFLOWS:
        require(coverage.get(workflow) == OUTCOMES, f"{workflow}: outcome coverage differs", errors)

    repeat_items = repeats.get("repeats", [])
    require(repeats.get("evidence_class") == "synthetic_contract_replay", "repeat evidence class is invalid", errors)
    require(repeats.get("runtime_claim") == "none", "repeats must not claim runtime evidence", errors)
    require(isinstance(repeat_items, list) and len(repeat_items) == 3, "expected three bounded repeat cases", errors)
    repeat_results: list[dict[str, Any]] = []
    for item in repeat_items if isinstance(repeat_items, list) else []:
        runs = item.get("runs", []) if isinstance(item, dict) else []
        run_ids = {run.get("run_id") for run in runs if isinstance(run, dict)}
        evaluator_ids = {run.get("evaluator_instance_id") for run in runs if isinstance(run, dict)}
        consistent = len({(run.get("route"), run.get("final_state"), tuple(run.get("detected_finding_ids", [])), tuple(run.get("preserved_dissent_ids", []))) for run in runs if isinstance(run, dict)}) == 1
        isolated = all(
            run.get("isolation_mode") == "fresh_subagent"
            and run.get("prior_scores_visible") is False
            and run.get("source_edits_performed") is False
            for run in runs
            if isinstance(run, dict)
        )
        require(len(runs) == 2 and len(run_ids) == 2 and len(evaluator_ids) == 2, f"{item.get('case_id')}: repeat instances are not unique", errors)
        require(consistent, f"{item.get('case_id')}: repeat result differs", errors)
        require(isolated, f"{item.get('case_id')}: repeat isolation failed", errors)
        repeat_results.append({"case_id": item.get("case_id"), "run_count": len(runs), "status": "passed" if consistent and isolated else "failed"})

    total = len(case_results)
    metrics = {
        "false_ready_count": false_ready_count,
        "fatal_or_blocking_finding_recall_percent": percent(fatal_detected, fatal_total),
        "major_finding_recall_percent": percent(major_detected, major_total),
        "lineage_compliance_percent": percent(lineage_passed, total),
        "reviewer_isolation_compliance_percent": percent(isolation_passed, total),
        "reviewer_edit_boundary_compliance_percent": percent(edit_passed, total),
        "dissent_preservation_percent": percent(dissent_passed, total),
    }
    report = {
        "schema_version": 1,
        "plugin_version": version,
        "profile": "personal-owner",
        "execution_kind": "deterministic_replay",
        "live_runtime_evidence": False,
        "corpus": {"case_count": total, "case_results": case_results, "metrics": metrics},
        "bounded_repeats": {"case_count": len(repeat_results), "results": repeat_results},
        "errors": errors,
    }
    return report, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write-report", action="store_true")
    group.add_argument("--check-report", action="store_true")
    args = parser.parse_args()
    try:
        report, errors = build_report()
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"Phase 8 validation failed: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.write_report:
        REPORT.write_text(rendered, encoding="utf-8", newline="\n")
    if args.check_report and (not REPORT.exists() or REPORT.read_text(encoding="utf-8") != rendered):
        print("Phase 8 report is missing or stale", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Phase 8 personal corpus validation passed: 20/20; false-ready 0; quality metrics 100%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
