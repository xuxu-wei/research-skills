#!/usr/bin/env python3
"""Evidence-graph and mutation tests for personal readiness validation."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

import yaml

import validate_openai_personal_readiness as validator
from test_openai_artifact_completeness import idea_dossier


def _rel(path: Path) -> str:
    return path.resolve().relative_to(validator.REPO.resolve()).as_posix()


def _file(path: Path, text: str) -> dict[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return {"path": _rel(path), "sha256": validator.raw_file_sha256(path)}


def _assert_skill_tree_hash_portable() -> None:
    """The tree digest must use POSIX relative-path order on every host OS."""
    with tempfile.TemporaryDirectory() as root_value:
        root = Path(root_value)
        files = {
            "sample/SKILL.md": "skill\n",
            "sample/_meta.json": "{}\n",
            "sample/agents/openai.yaml": "interface: {}\n",
        }
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        expected = hashlib.sha256()
        for relative in sorted(files):
            content = (root / relative).read_bytes().replace(b"\r\n", b"\n")
            expected.update(relative.encode("utf-8"))
            expected.update(b"\0")
            expected.update(hashlib.sha256(content).digest())
            expected.update(b"\0")
        assert validator.skill_tree_sha256(root) == expected.hexdigest()


def _artifact(path: Path, artifact_id: str, version: str, text: str) -> dict[str, str]:
    return {"artifact_id": artifact_id, "version": version, **_file(path, text)}


def _yaml_artifact(
    path: Path, artifact_id: str, version: str, value: dict[str, Any]
) -> dict[str, str]:
    return _artifact(
        path,
        artifact_id,
        version,
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
    )


def _complete_document(title: str, version: str) -> str:
    return (
        f"# {title}\n\n"
        f"## Complete summary\n\nThis {version} artifact states the full research question, "
        "population, contribution, evidence basis, and intended decision without relying on a prior version. "
        "It is deliberately long enough to be independently reviewed as a frozen substantive artifact.\n\n"
        "## Methods and evidence chain\n\nInput: frozen research material. Method: bounded analysis, "
        "independent evaluation, revision, and fresh re-evaluation. Output: a complete decision-ready package "
        "with traceable claims, methods, evidence needs, feasibility, and limitations.\n\n"
        "## Significance, application, and risks\n\nThe artifact records scientific significance, practical value, "
        "innovation, expected impact, assumptions, implementation risks, stopping conditions, and unresolved dissent.\n"
    )


def _sectioned_document(title: str, sections: list[tuple[str, str]]) -> str:
    body = [f"# {title}", ""]
    for heading, content in sections:
        body.extend((f"## {heading}", "", content, ""))
    return "\n".join(body)


def _workflow_document(profile: str, title: str, version: str) -> str:
    if profile == "idea":
        plugin_version = str(
            validator.load_json(validator.PLUGIN / ".codex-plugin" / "plugin.json")["version"]
        )
        return idea_dossier(plugin_version, version=int(version.removeprefix("v")))
    shared = {
        "proposal": [
            ("Executive summary", "This complete proposal states the decision, study population, contribution, and bounded plan."),
            ("Problem and gap", "Current evidence does not resolve the stated research problem in the target population."),
            ("Objectives", "The primary objective and testable secondary objectives are specified without relying on another artifact."),
            ("Research plan", "Work packages connect recruitment, measurement, analysis, validation, and interpretation."),
            ("Methods", "The design, variables, estimands, analyses, uncertainty, and sensitivity analyses are prespecified."),
            ("Feasibility", "Available data, staff, timing, dependencies, risks, alternatives, and stopping criteria are bounded."),
            ("Expected outputs", "The proposal defines decision-relevant results, evidence limits, and planned deliverables."),
            ("References", "Smith J. Complete proposal methods. Research Methods. 2025;1:1-10. doi:10.1000/proposal."),
        ],
        "article": [
            ("Abstract", "Background, objective, methods, principal results, and conclusion are reported for the complete manuscript."),
            ("Introduction", "The current evidence, unresolved gap, study objective, and contribution are established."),
            ("Methods", "Design, setting, participants, variables, analyses, uncertainty, and sensitivity checks are reproducible."),
            ("Results", "Primary and secondary findings are reported with effect estimates and uncertainty, without interpretation-only placeholders."),
            ("Discussion", "Findings, comparison, meaning, limitations, applicability, and calibrated conclusions are integrated."),
            ("References", "Smith J. Complete article methods. Research Methods. 2025;1:1-10. doi:10.1000/article."),
        ],
        "perspective": [
            ("Summary", "This complete perspective states the thesis, evidence base, counterposition, and intended consequence."),
            ("Background and context", "The field context and unresolved conceptual or practical problem are established."),
            ("Central thesis and argument", "A traceable thesis is developed through explicit premises and bounded claims."),
            ("Evidence and counterarguments", "Supporting evidence, contrary evidence, uncertainty, and dissent are addressed."),
            ("Implications and impact", "Scientific, practical, and audience implications follow from the supported argument."),
            ("Limitations", "Scope limits, assumptions, alternative interpretations, and failure conditions are explicit."),
            ("References", "Smith J. Perspective evidence. Research Methods. 2025;1:1-10. doi:10.1000/perspective."),
        ],
    }
    return _sectioned_document(f"{title} {version}", shared[profile])


def _polisher_portfolio_document(title: str, version: str) -> str:
    return _sectioned_document(
        f"{title} {version}",
        [
            ("Portfolio summary", "Nine bounded, source-traceable options cover three perspectives and three work tiers."),
            ("Scientific significance strategies", "Repositioning and extensions increase conceptual contribution while preserving claim support."),
            ("Practical value strategies", "Options connect existing assets to plausible use decisions and bounded validation work."),
            ("Dissemination and editorial strategies", "Audience, title, narrative, and outlet archetype remain constrained by implemented evidence."),
            ("Pareto trade-offs", "The portfolio preserves impact, workload, feasibility, rigor, and publishability trade-offs without auto-selection."),
            ("Risks and stop conditions", "Each option states dependencies, uncertainty, failure conditions, and conditions requiring rejection."),
        ],
    )


def _review_document(
    review_id: str,
    workflow_id: str,
    reviewer_actor_id: str,
    reviewer_skill: str,
    reviewer_instance_id: str,
    review_stage: str,
    files_read: list[str],
    files_written: list[str],
    reviewed_artifact: dict[str, Any],
    input_artifacts: list[dict[str, Any]],
    report_artifact_id: str,
    report_artifact_version: str,
    report_artifact_path: str,
    *,
    decision: str = "accept",
    fatal_findings: list[str] | None = None,
    blocking_findings: list[str] | None = None,
    dissent: list[str] | None = None,
    unresolved_issues: list[str] | None = None,
) -> str:
    record = {
        "review_id": review_id,
        "workflow_id": workflow_id,
        "reviewer_actor_id": reviewer_actor_id,
        "reviewer_skill": reviewer_skill,
        "reviewer_instance_id": reviewer_instance_id,
        "review_stage": review_stage,
        "round_id": f"round-{reviewer_actor_id}",
        "files_read": files_read,
        "files_written": files_written,
        "input_artifact_ids": [artifact["artifact_id"] for artifact in input_artifacts],
        "input_versions": [artifact["version"] for artifact in input_artifacts],
        "reviewed_artifact_id": reviewed_artifact["artifact_id"],
        "reviewed_artifact_version": reviewed_artifact["version"],
        "reviewed_artifact_path": reviewed_artifact["path"],
        "reviewed_artifact_digest": reviewed_artifact["sha256"],
        "report_artifact_id": report_artifact_id,
        "report_artifact_version": report_artifact_version,
        "report_artifact_path": report_artifact_path,
        "decision": decision,
        "review_scope": "complete frozen artifact and its bound supporting inputs",
        "complete_artifact_confirmed": True,
        "findings": ["The complete frozen artifact was independently assessed."],
        "fatal_findings": fatal_findings or [],
        "blocking_findings": blocking_findings or [],
        "dissent": dissent or [],
        "unresolved_issues": unresolved_issues or [],
        "isolation_mode": "fresh_subagent",
        "prior_scores_visible": False,
        "prior_versions_visible": False,
        "revision_delta_visible": False,
        "source_edits_performed": False,
    }
    return (
        "---\n"
        + yaml.safe_dump(record, sort_keys=False, allow_unicode=True)
        + "---\n\n# Independent review\n\nStructured findings for the frozen reviewed artifact.\n"
    )


def _review_artifact(
    path: Path,
    artifact_id: str,
    version: str,
    *,
    slot_id: str,
    actor_suffix: str,
    reviewer_skill: str,
    review_stage: str,
    reviewed_artifact: dict[str, Any],
    input_artifacts: list[dict[str, Any]] | None = None,
    additional_files_written: list[str] | None = None,
    decision: str = "accept",
    fatal_findings: list[str] | None = None,
    blocking_findings: list[str] | None = None,
    dissent: list[str] | None = None,
    unresolved_issues: list[str] | None = None,
) -> dict[str, str]:
    inputs = input_artifacts or [reviewed_artifact]
    report_path = _rel(path)
    return _artifact(
        path,
        artifact_id,
        version,
        _review_document(
            f"review-{slot_id}-{actor_suffix}",
            slot_id,
            f"actor-{slot_id}-{actor_suffix}",
            reviewer_skill,
            f"instance-{slot_id}-{actor_suffix}",
            review_stage,
            [artifact["path"] for artifact in inputs],
            [report_path, *(additional_files_written or [])],
            reviewed_artifact,
            inputs,
            artifact_id,
            version,
            report_path,
            decision=decision,
            fatal_findings=fatal_findings,
            blocking_findings=blocking_findings,
            dissent=dissent,
            unresolved_issues=unresolved_issues,
        ),
    )


def _actor(
    slot_id: str,
    suffix: str,
    role: str,
    reads: list[str],
    writes: list[str],
    *,
    skill: str | None = None,
    fresh: bool = False,
    review_stage: str = "not_applicable",
) -> dict[str, Any]:
    return {
        "actor_id": f"actor-{slot_id}-{suffix}",
        "role": role,
        "skill": skill or f"test-{role}",
        "instance_id": f"instance-{slot_id}-{suffix}",
        "review_stage": review_stage,
        "isolation_mode": "fresh_subagent" if fresh else "inline_nonreviewer",
        "prior_scores_visible": False,
        "prior_versions_visible": False,
        "revision_delta_visible": False,
        "source_edits_performed": False,
        "files_read": reads,
        "files_written": writes,
    }


def _source_identity(base: Path, plugin_version: str) -> dict[str, str]:
    codex_home = base / "fixture-codex-home"
    config = codex_home / "config.toml"
    _file(config, 'model = "test-model"\n')
    commit = validator._git_head(validator.REPO)
    metadata_path = (
        codex_home
        / ".tmp"
        / "marketplaces"
        / "xuxu-research-preview"
        / ".codex-marketplace-install.json"
    )
    metadata = {
        "source_type": "git",
        "source": "https://github.com/xuxu-wei/research-skills.git",
        "ref_name": "main",
        "sparse_paths": [],
        "revision": commit,
    }
    _file(metadata_path, json.dumps(metadata, indent=2) + "\n")

    source_plugin = validator.PLUGIN
    cache = (
        codex_home
        / "plugins"
        / "cache"
        / "xuxu-research-preview"
        / "research-skills-openai"
        / plugin_version
    )
    (cache / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_plugin / ".codex-plugin" / "plugin.json", cache / ".codex-plugin" / "plugin.json")
    shutil.copy2(source_plugin / "workflow-registry.yaml", cache / "workflow-registry.yaml")
    shutil.copytree(source_plugin / "skills", cache / "skills")
    cli = base / "fixture-bin" / ("codex.exe" if sys.platform == "win32" else "codex")
    cli.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(sys.executable, cli)
    return {
        "git_commit": commit,
        "marketplace_revision": commit,
        "manifest_sha256": validator.file_sha256(source_plugin / ".codex-plugin" / "plugin.json"),
        "registry_sha256": validator.file_sha256(source_plugin / "workflow-registry.yaml"),
        "skill_tree_sha256": validator.skill_tree_sha256(source_plugin / "skills"),
        "installed_cache_path": str(cache.resolve()),
        "installed_manifest_sha256": validator.file_sha256(cache / ".codex-plugin" / "plugin.json"),
        "installed_registry_sha256": validator.file_sha256(cache / "workflow-registry.yaml"),
        "installed_skill_tree_sha256": validator.skill_tree_sha256(cache / "skills"),
        "marketplace_metadata_path": str(metadata_path.resolve()),
        "marketplace_metadata_sha256": validator.raw_file_sha256(metadata_path),
        "marketplace_source": metadata["source"],
        "marketplace_ref": metadata["ref_name"],
        "config_path": str(config.resolve()),
        "config_sha256": validator.raw_file_sha256(config),
        "cli_version": "0.144.4",
        "cli_path": str(cli),
        "cli_sha256": validator.raw_file_sha256(cli),
        "model": "test-model",
    }


def _run(
    directory: Path,
    slot_id: str,
    task_id: str,
    session_id: str,
    plugin_version: str,
    source_identity: dict[str, Any],
    actors: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    *,
    final_text: str,
    web_ids: list[str] | None = None,
    search: bool = False,
    multi_agent: bool = True,
    resume: bool = False,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    directory.mkdir(parents=True, exist_ok=True)
    web_ids = web_ids or []
    events: list[dict[str, Any]] = [{"type": "thread.started", "thread_id": session_id}]
    for web_id in web_ids:
        events.append(
            {
                "type": "item.started",
                "item": {"id": web_id, "type": "web_search", "query": "fixture query"},
            }
        )
        events.append(
            {
                "type": "item.completed",
                "item": {"id": web_id, "type": "web_search", "query": "fixture query"},
            }
        )
    turn_id = f"line-{len(events) + 1:06d}:turn.completed"
    events.append({"type": "turn.completed"})
    prompt = _file(directory / "prompt.md", f"Execute {slot_id}\n")
    jsonl = _file(
        directory / "events.jsonl",
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
    )
    stderr = _file(directory / "stderr.txt", "")
    final_message = _file(directory / "final-message.md", final_text)
    argv = ["codex", "exec"]
    resume_ids: list[str] = []
    if resume:
        argv.extend(["resume", session_id])
        resume_ids = [f"resume-command:{session_id}"]
    argv.extend(["--json", "-"])
    index = {
        "schema_version": 1,
        "slot_id": slot_id,
        "task_id": task_id,
        "session_id": session_id,
        "plugin_version": plugin_version,
        "source_identity": copy.deepcopy(source_identity),
        "command": {
            "argv": argv,
            "cwd": str(validator.REPO.resolve()),
            "sandbox": "workspace-write",
            "approval_policy": "never",
            "search_enabled": search,
            "multi_agent_enabled": multi_agent,
        },
        "started_at": "2026-07-17T00:00:00Z",
        "completed_at": "2026-07-17T00:10:00Z",
        "exit_code": 0,
        "files": {
            "prompt": prompt,
            "jsonl": jsonl,
            "stderr": stderr,
            "final_message": final_message,
        },
        "input_bindings": copy.deepcopy(inputs),
        "output_bindings": copy.deepcopy(outputs),
        "actor_bindings": copy.deepcopy(actors),
        "event_summary": {
            "thread_started_event_id": session_id,
            "turn_completed_event_ids": [turn_id],
            "web_search_event_ids": list(web_ids),
            "resume_event_ids": resume_ids,
        },
    }
    index_path = directory / "runtime-run-index.yaml"
    index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
    index_binding = {"path": _rel(index_path), "sha256": validator.raw_file_sha256(index_path)}
    runtime = {
        "prompt": prompt,
        "jsonl": jsonl,
        "stderr": stderr,
        "final_message": final_message,
        "run_index": index_binding,
        "exit_code": 0,
    }
    return runtime, index, index_binding


def _state(slot: Path, slot_id: str, terminal: str, trace: list[str]) -> dict[str, str]:
    return _yaml_artifact(
        slot / "state" / "final-package-state.yaml",
        f"state-{slot_id}",
        "v001",
        {
            "terminal_state": terminal,
            "status_trace": trace,
            "dissent_preserved": True,
            "source_inputs_modified": False,
        },
    )


def _standard_workflow(
    slot: Path, item: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    slot_id = item["slot_id"]
    source = _artifact(slot / "input" / "source.md", f"source-{slot_id}", "v001", "Frozen source input\n")
    initial = _artifact(
        slot / "artifacts" / "complete-v001.md",
        f"complete-{slot_id}",
        "v001",
        _workflow_document(item["workflow"], slot_id, "v001"),
    )
    revised = _artifact(
        slot / "artifacts" / "complete-v002.md",
        f"complete-{slot_id}",
        "v002",
        _workflow_document(item["workflow"], slot_id, "v002")
        + "\nSubstantive revision incorporated.\n",
    )
    delta = _artifact(slot / "revisions" / "revision-delta.md", f"delta-{slot_id}", "v001", "Substantive revision: clarified the complete evidence chain and strengthened feasibility.\n")
    evaluation1 = _review_artifact(
        slot / "reviews" / "evaluation-r001.md",
        f"evaluation-1-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="evaluator",
        reviewer_skill="test-evaluator",
        review_stage="initial_evaluator",
        reviewed_artifact=initial,
        decision="revise",
        blocking_findings=["Clarify the evidence chain before fresh review."],
    )
    evaluation2 = _review_artifact(
        slot / "reviews" / "evaluation-r002.md",
        f"evaluation-2-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="reevaluator",
        reviewer_skill="test-evaluator",
        review_stage="fresh_reevaluator",
        reviewed_artifact=revised,
    )
    panel1 = _review_artifact(
        slot / "reviews" / "panel-review-1.md",
        f"panel-1-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="panel1",
        reviewer_skill="test-panel_reviewer",
        review_stage="panel_reviewer",
        reviewed_artifact=revised,
    )
    panel2 = _review_artifact(
        slot / "reviews" / "panel-review-2.md",
        f"panel-2-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="panel2",
        reviewer_skill="test-panel_reviewer",
        review_stage="panel_reviewer",
        reviewed_artifact=revised,
    )
    supporting = _review_artifact(
        slot / "reviews" / "supporting-review.md",
        f"supporting-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="supporting",
        reviewer_skill="test-supporting_reviewer",
        review_stage="supporting_historical",
        reviewed_artifact=initial,
        decision="revise",
        blocking_findings=["Historical supporting issue retained for owner visibility."],
    )
    final_package = _artifact(slot / "package" / "final-package.md", f"package-{slot_id}", "v001", _complete_document(f"Final {slot_id}", "package"))
    trace = ["drafted", "initial_reviewed", "revised", "fresh_reevaluated", item["expected_outcome"]]
    state = _state(slot, slot_id, item["expected_outcome"], trace)

    generator = _actor(slot_id, "generator", "generator", [source["path"]], [initial["path"]])
    reviser = _actor(
        slot_id,
        "reviser",
        "reviser",
        [initial["path"], supporting["path"]],
        [revised["path"], delta["path"]],
    )
    evaluator = _actor(slot_id, "evaluator", "evaluator", [initial["path"]], [evaluation1["path"]], fresh=True, review_stage="initial_evaluator")
    reevaluator = _actor(slot_id, "reevaluator", "evaluator", [revised["path"]], [evaluation2["path"]], fresh=True, review_stage="fresh_reevaluator")
    panel_actor1 = _actor(slot_id, "panel1", "panel_reviewer", [revised["path"]], [panel1["path"]], fresh=True, review_stage="panel_reviewer")
    panel_actor2 = _actor(slot_id, "panel2", "panel_reviewer", [revised["path"]], [panel2["path"]], fresh=True, review_stage="panel_reviewer")
    supporting_actor = _actor(slot_id, "supporting", "supporting_reviewer", [initial["path"]], [supporting["path"]], fresh=True, review_stage="supporting_historical")
    compositor_skill = {
        "article": "article-submission-compositor",
        "perspective": "perspective-final-compositor",
    }.get(item["workflow"])
    compositor_report = None
    if compositor_skill:
        compositor_report = _review_artifact(
            slot / "reviews" / "compositor-verification.md",
            f"compositor-verification-{slot_id}",
            "v001",
            slot_id=slot_id,
            actor_suffix="finalizer",
            reviewer_skill=compositor_skill,
            review_stage="final_verifier",
            reviewed_artifact=revised,
            input_artifacts=[revised, panel1, panel2],
            additional_files_written=[final_package["path"], state["path"]],
        )
    finalizer = _actor(
        slot_id,
        "finalizer",
        "final_compositor" if compositor_skill else "package_assembler",
        [revised["path"], panel1["path"], panel2["path"]],
        [
            *([compositor_report["path"]] if compositor_report else []),
            final_package["path"],
            state["path"],
        ],
        skill=compositor_skill,
        fresh=bool(compositor_skill),
        review_stage="final_verifier" if compositor_skill else "not_applicable",
    )
    actors = [generator, reviser, evaluator, reevaluator, panel_actor1, panel_actor2, supporting_actor, finalizer]
    outputs = [
        initial,
        revised,
        delta,
        evaluation1,
        evaluation2,
        panel1,
        panel2,
        supporting,
        *([compositor_report] if compositor_report else []),
        final_package,
        state,
    ]
    evidence = {
        "profile": item["workflow"],
        "source_inputs_before": [source],
        "source_inputs_after": [copy.deepcopy(source)],
        "frozen_review_inputs": [source],
        "version_artifacts": [initial, revised],
        "revision_delta": delta,
        "evaluation_artifacts": [evaluation1, evaluation2],
        "panel_or_compositor_artifacts": [
            panel1,
            panel2,
            final_package,
        ],
        "state_artifact": state,
        "compositor_verification_artifact": compositor_report,
        "status_trace": trace,
        "terminal_state": item["expected_outcome"],
        "generator_actor_ids": [generator["actor_id"], reviser["actor_id"]],
        "reviewer_actor_ids": [
            evaluator["actor_id"],
            reevaluator["actor_id"],
            panel_actor1["actor_id"],
            panel_actor2["actor_id"],
            supporting_actor["actor_id"],
        ],
        "assembler_actor_ids": [finalizer["actor_id"]],
        "dissent_preserved": True,
        "fresh_evaluation_rounds": 2,
        "polisher_matrix": None,
    }
    return actors, [source], {"outputs": outputs, "evidence": evidence}


def _polisher_workflow(
    slot: Path, item: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    slot_id = item["slot_id"]
    source = _artifact(
        slot / "input" / "source-material.md",
        f"source-{slot_id}",
        "v001",
        "Immutable raw research materials supplied by the owner.\n",
    )
    dossier = _artifact(
        slot / "context" / "research-dossier.md",
        f"dossier-{slot_id}",
        "v001",
        _complete_document("Frozen generated research dossier", "source"),
    )
    portfolio1 = _artifact(
        slot / "artifacts" / "portfolio-v001.md",
        f"portfolio-{slot_id}",
        "v001",
        _polisher_portfolio_document("Candidate portfolio", "v001"),
    )
    portfolio2 = _artifact(
        slot / "artifacts" / "portfolio-v002.md",
        f"portfolio-{slot_id}",
        "v002",
        _polisher_portfolio_document("Candidate portfolio", "v002")
        + "\nMust-fix revisions incorporated.\n",
    )
    delta = _artifact(slot / "revisions" / "portfolio-revision-delta.md", f"delta-{slot_id}", "v001", "Substantive portfolio revision addressing anonymous must-fix findings and preserving dissent.\n")
    evaluation1 = _review_artifact(
        slot / "reviews" / "methodology-evaluation-r001.md",
        f"evaluation-1-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="initial-final-reviewer",
        reviewer_skill="test-methodology_reviewer",
        review_stage="polisher_initial_final",
        reviewed_artifact=portfolio1,
        decision="revise",
        blocking_findings=["Resolve the bounded methodology issue before re-evaluation."],
    )
    evaluation2 = _review_artifact(
        slot / "reviews" / "methodology-evaluation-r002.md",
        f"evaluation-2-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="fresh-final-reviewer",
        reviewer_skill="test-methodology_reviewer",
        review_stage="polisher_fresh_final",
        reviewed_artifact=portfolio2,
    )
    perspectives = ["scientific_significance", "practical_value", "dissemination_editorial"]
    tiers = ["reposition_only", "small_extension", "moderate_extension"]
    strategy_reports = {
        perspective: _review_artifact(
            slot / "reviews" / f"strategy-review-{perspective}.md",
            f"strategy-{perspective}-{slot_id}",
            "v001",
            slot_id=slot_id,
            actor_suffix=f"strategist-{offset}",
            reviewer_skill="test-strategy_reviewer",
            review_stage="strategist_initial",
            reviewed_artifact=dossier,
        )
        for offset, perspective in enumerate(perspectives, 1)
    }
    revision_strategy = _review_artifact(
        slot / "reviews" / "revision-strategy-review.md",
        f"revision-strategy-{slot_id}",
        "v001",
        slot_id=slot_id,
        actor_suffix="revision-strategist",
        reviewer_skill="test-strategy_reviewer",
        review_stage="strategist_revision",
        reviewed_artifact=dossier,
    )
    anonymous_portfolio = _artifact(slot / "package" / "anonymous-candidate-portfolio.md", f"anonymous-portfolio-{slot_id}", "v001", _complete_document("Anonymous portfolio", "package"))
    selection = _artifact(slot / "package" / "selection-dossier.md", f"selection-{slot_id}", "v001", _complete_document("Selection dossier", "package"))
    trace = ["strategies_generated", "initial_reviewed", "revised", "fresh_reevaluated", item["expected_outcome"]]
    state = _state(slot, slot_id, item["expected_outcome"], trace)

    dossier_builder = _actor(
        slot_id,
        "dossier-builder",
        "context_builder",
        [source["path"]],
        [dossier["path"]],
    )
    initial_assembler = _actor(
        slot_id,
        "initial-assembler",
        "plan_assembler",
        [dossier["path"], *(report["path"] for report in strategy_reports.values())],
        [portfolio1["path"]],
    )
    revision_assembler = _actor(
        slot_id,
        "revision-assembler",
        "revision_assembler",
        [portfolio1["path"], revision_strategy["path"]],
        [portfolio2["path"], delta["path"]],
    )
    strategists = [
        _actor(
            slot_id,
            f"strategist-{offset}",
            "strategy_reviewer",
            [dossier["path"]],
            [strategy_reports[perspective]["path"]],
            fresh=True,
            review_stage="strategist_initial",
        )
        for offset, perspective in enumerate(perspectives, 1)
    ]
    revision_actor = _actor(slot_id, "revision-strategist", "strategy_reviewer", [dossier["path"]], [revision_strategy["path"]], fresh=True, review_stage="strategist_revision")
    initial_final = _actor(slot_id, "initial-final-reviewer", "methodology_reviewer", [portfolio1["path"]], [evaluation1["path"]], fresh=True, review_stage="polisher_initial_final")
    fresh_final = _actor(slot_id, "fresh-final-reviewer", "methodology_reviewer", [portfolio2["path"]], [evaluation2["path"]], fresh=True, review_stage="polisher_fresh_final")
    finalizer = _actor(slot_id, "selection-assembler", "selection_assembler", [portfolio2["path"]], [anonymous_portfolio["path"], selection["path"], state["path"]])
    actors = [dossier_builder, initial_assembler, revision_assembler, *strategists, revision_actor, initial_final, fresh_final, finalizer]
    outputs = [
        dossier,
        portfolio1,
        portfolio2,
        delta,
        evaluation1,
        evaluation2,
        *strategy_reports.values(),
        revision_strategy,
        anonymous_portfolio,
        selection,
        state,
    ]
    cells = [
        {
            "perspective": perspective,
            "tier": tier,
            "outcome": "option",
            "artifact_id": strategy_reports[perspective]["artifact_id"],
            "content_summary": f"{perspective} {tier} offers a bounded, source-traceable impact strategy with explicit feasibility and stop conditions.",
        }
        for perspective in perspectives
        for tier in tiers
    ]
    evidence = {
        "profile": "research_polisher",
        "source_inputs_before": [source],
        "source_inputs_after": [copy.deepcopy(source)],
        "frozen_review_inputs": [dossier],
        "version_artifacts": [portfolio1, portfolio2],
        "revision_delta": delta,
        "evaluation_artifacts": [evaluation1, evaluation2],
        "panel_or_compositor_artifacts": [anonymous_portfolio, selection],
        "state_artifact": state,
        "compositor_verification_artifact": None,
        "status_trace": trace,
        "terminal_state": item["expected_outcome"],
        "generator_actor_ids": [initial_assembler["actor_id"], revision_assembler["actor_id"]],
        "reviewer_actor_ids": [
            *(actor["actor_id"] for actor in strategists),
            revision_actor["actor_id"],
            initial_final["actor_id"],
            fresh_final["actor_id"],
        ],
        "assembler_actor_ids": [finalizer["actor_id"]],
        "dissent_preserved": True,
        "fresh_evaluation_rounds": 2,
        "polisher_matrix": {
            "initial_strategist_instance_ids": [actor["instance_id"] for actor in strategists],
            "revision_strategist_instance_id": revision_actor["instance_id"],
            "perspectives": perspectives,
            "tier_ids": tiers,
            "cells": cells,
            "initial_final_reviewer_instance_id": initial_final["instance_id"],
            "fresh_final_reviewer_instance_id": fresh_final["instance_id"],
        },
    }
    return actors, [source], {"outputs": outputs, "evidence": evidence}


def _base_binding(
    item: dict[str, Any],
    plugin_version: str,
    source_identity: dict[str, Any],
    runtime: dict[str, Any],
    actors: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "task_id": f"task-{item['slot_id']}",
        "session_id": f"session-{item['slot_id']}",
        "plugin_version": plugin_version,
        "source_identity": copy.deepcopy(source_identity),
        "runtime_evidence": runtime,
        "workflow_evidence": None,
        "artifact_bindings": artifacts,
        "actor_bindings": actors,
        "source_urls": [],
        "search_evidence": None,
        "control_evidence": None,
        "deep_research_evidence": None,
        "started_at": "2026-07-17T00:00:00Z",
        "completed_at": "2026-07-17T00:10:00Z",
        "owner_confirmed": True,
    }


def _build_receipts(base: Path, plugin_version: str) -> dict[str, Any]:
    receipts = copy.deepcopy(validator.load_yaml(validator.RECEIPTS))
    source_identity = _source_identity(base, plugin_version)
    items = [receipts["distribution"]]
    for group in ("workflow_runs", "control_runs", "retrieval_runs"):
        items.extend(receipts[group])
    for item in items:
        slot_id = item["slot_id"]
        slot = base / slot_id
        task_id = f"task-{slot_id}"
        session_id = f"session-{slot_id}"
        kind = item["kind"]

        if kind == "workflow_happy":
            builder = _polisher_workflow if item["workflow"] == "research_polisher" else _standard_workflow
            actors, inputs, graph = builder(slot, item)
            outputs = graph["outputs"]
            runtime, _, _ = _run(
                slot / "runtime",
                slot_id,
                task_id,
                session_id,
                plugin_version,
                source_identity,
                actors,
                inputs,
                outputs,
                final_text=f"status: {item['expected_outcome']}\n",
            )
            binding = _base_binding(item, plugin_version, source_identity, runtime, actors, outputs)
            binding["workflow_evidence"] = graph["evidence"]

        elif kind == "workflow_control":
            source = _artifact(slot / "input" / "source.md", f"source-{slot_id}", "v001", "Frozen control source\n")
            trace = ["running", item["expected_outcome"]]
            state = _yaml_artifact(
                slot / "state" / "control-state.yaml",
                f"state-{slot_id}",
                "v001",
                {"status_trace": trace, "terminal_state": item["expected_outcome"]},
            )
            host = _actor(slot_id, "host", "orchestrator", [source["path"]], [state["path"]])
            actors = [host]
            runtime, _, _ = _run(
                slot / "runtime",
                slot_id,
                task_id,
                session_id,
                plugin_version,
                source_identity,
                actors,
                [source],
                [state],
                final_text=(
                    f"status: {item['expected_outcome']}\n"
                    "The run did not reach human_signoff_required; this sentence is explanatory only.\n"
                ),
                multi_agent=slot_id != "personal-reviewer-unavailable-control",
            )
            mismatch = None
            if slot_id == "personal-fatal-finding-control":
                mismatch = {
                    "path": source["path"],
                    "expected_sha256": source["sha256"],
                    "supplied_sha256": "f" * 64,
                    "post_run_sha256": source["sha256"],
                    "mismatch_detected": True,
                }
            binding = _base_binding(item, plugin_version, source_identity, runtime, actors, [state])
            binding["control_evidence"] = {
                "control_type": validator.EXPECTED_CONTROL_TYPE[slot_id],
                "state_trace": trace,
                "terminal_state": item["expected_outcome"],
                "ready_state_observed": False,
                "source_inputs_modified": False,
                "state_artifact": state,
                "source_inputs_before": [source],
                "source_inputs_after": [copy.deepcopy(source)],
                "digest_mismatch_evidence": mismatch,
            }

        elif kind == "search":
            query = _artifact(slot / "input" / "query.md", f"query-{slot_id}", "v001", "Frozen search question\n")
            count = 2 if slot_id == "personal-search-narrow-academic" else 1
            web_ids = [f"web-{slot_id}-{index}" for index in range(1, count + 1)]
            source_type = "peer_reviewed_primary" if slot_id != "personal-search-current" else "official_primary"
            records = [
                {
                    "source_id": f"source-{index}",
                    "url": f"https://example.org/{slot_id}/{index}",
                    "title": f"Primary source {index}",
                    "publisher": "Official publisher" if source_type == "official_primary" else "Peer-reviewed journal",
                    "source_type": source_type,
                    "publication_date": "2026-01-01",
                    "accessed_at": "2026-07-17T00:05:00Z",
                    "applicability_scope": "Directly supports the bounded claim.",
                    "evidence_event_ids": [web_ids[index - 1]],
                }
                for index in range(1, count + 1)
            ]
            urls = [record["url"] for record in records]
            claims = [
                {
                    "claim_id": "claim-1",
                    "claim": "The bounded answer is supported by the opened primary sources.",
                    "source_urls": urls,
                    "source_record_ids": [record["source_id"] for record in records],
                }
            ]
            report_value = {
                "source_records": records,
                "claim_mappings": claims,
                "opened_urls": urls,
                "event_ids": web_ids,
            }
            report = _yaml_artifact(slot / "evidence" / "search-report.yaml", f"search-report-{slot_id}", "v001", report_value)
            host = _actor(slot_id, "host", "orchestrator", [query["path"]], [report["path"]])
            actors = [host]
            runtime, _, _ = _run(
                slot / "runtime",
                slot_id,
                task_id,
                session_id,
                plugin_version,
                source_identity,
                actors,
                [query],
                [report],
                final_text=f"status: {item['expected_outcome']}\n",
                web_ids=web_ids,
                search=True,
            )
            binding = _base_binding(item, plugin_version, source_identity, runtime, actors, [report])
            binding["source_urls"] = urls
            binding["search_evidence"] = {
                "web_search_event_count": len(web_ids),
                "event_ids": web_ids,
                "opened_urls": urls,
                "source_report": report,
                "source_records": records,
                "claim_mappings": claims,
            }

        elif kind in {"deep_research_inactive", "deep_research_complete"}:
            source = _artifact(slot / "input" / "question.md", f"question-{slot_id}", "v001", "Frozen multi-stage research question\n")
            continuation = _artifact(slot / "evidence" / "continuation-package.md", f"continuation-{slot_id}", "v001", _complete_document("Deep Research continuation package", "v001"))
            returned = None
            mapper = None
            if kind == "deep_research_complete":
                returned = _artifact(slot / "evidence" / "returned-result.md", f"returned-{slot_id}", "v001", _complete_document("Returned Deep Research result", "v001"))
                mapper = _artifact(slot / "evidence" / "mapper-artifact.md", f"mapper-{slot_id}", "v001", _complete_document("Mapped Deep Research evidence", "v001"))
            resume_ids = [] if returned is None else [f"resume-command:{session_id}"]
            pending_ledger_value = {
                "pending_edge_id": f"edge-{slot_id}",
                "origin_task_id": task_id,
                "origin_session_id": session_id,
                "continuation_package": continuation,
                "returned_result": None,
                "mapper_artifact": None,
                "resume_event_ids": [],
                "resume_count": 0,
                "edge_consumed": False,
            }
            pending_ledger = _yaml_artifact(
                slot / "evidence" / "edge-ledger-v001-pending.yaml",
                f"ledger-{slot_id}",
                "v001",
                pending_ledger_value,
            )
            ledger = pending_ledger
            if returned is not None:
                ledger = _yaml_artifact(
                    slot / "evidence" / "edge-ledger-v002-consumed.yaml",
                    f"ledger-{slot_id}",
                    "v002",
                    {
                        **pending_ledger_value,
                        "returned_result": returned,
                        "mapper_artifact": mapper,
                        "resume_event_ids": resume_ids,
                        "resume_count": 1,
                        "edge_consumed": True,
                    },
                )
            handoff_actor = _actor(
                slot_id,
                "handoff-host",
                "orchestrator",
                [source["path"]],
                [continuation["path"], pending_ledger["path"]],
            )
            handoff_outputs = [continuation, pending_ledger]
            handoff_runtime, _, handoff_binding = _run(
                slot / "handoff",
                slot_id,
                task_id,
                session_id,
                plugin_version,
                source_identity,
                [handoff_actor],
                [source],
                handoff_outputs,
                final_text=(
                    f"status: {item['expected_outcome']}\n"
                    if returned is None
                    else "status: deep_research_handoff_required\n"
                ),
            )
            if returned is None:
                runtime = handoff_runtime
                actors = [handoff_actor]
                artifacts = [continuation, pending_ledger]
                resume_binding = None
            else:
                resume_actor = _actor(slot_id, "resume-host", "orchestrator", [continuation["path"], returned["path"]], [mapper["path"], ledger["path"]])
                runtime, _, resume_binding = _run(
                    slot / "resume",
                    slot_id,
                    task_id,
                    session_id,
                    plugin_version,
                    source_identity,
                    [resume_actor],
                    [continuation, returned],
                    [mapper, ledger],
                    final_text=f"status: {item['expected_outcome']}\n",
                    resume=True,
                )
                actors = [resume_actor]
                artifacts = [continuation, returned, mapper, pending_ledger, ledger]
            binding = _base_binding(item, plugin_version, source_identity, runtime, actors, artifacts)
            binding["deep_research_evidence"] = {
                "mode": "inactive_handoff" if returned is None else "completed_resume",
                "pending_edge_id": f"edge-{slot_id}",
                "origin_task_id": task_id,
                "origin_session_id": session_id,
                "handoff_run_index": handoff_binding,
                "resume_run_index": resume_binding,
                "pending_edge_ledger": pending_ledger,
                "edge_ledger": ledger,
                "continuation_package": continuation,
                "returned_result": returned,
                "mapper_artifact": mapper,
                "resume_session_id": None if returned is None else session_id,
                "resume_event_ids": resume_ids,
                "resume_count": 0 if returned is None else 1,
                "edge_consumed": returned is not None,
            }

        else:
            source = _artifact(slot / "input" / "request.md", f"request-{slot_id}", "v001", "Frozen distribution request\n")
            report = _yaml_artifact(
                slot / "artifacts" / "distribution-report.yaml",
                f"distribution-{slot_id}",
                "v001",
                {
                    "plugin_version": plugin_version,
                    "installed_enabled": True,
                    "skill_count": 49,
                    "independent_reviewer_count": 20,
                    "declared_entries": sorted(validator.EXPECTED_DECLARED),
                    "implicit_entries": sorted(validator.EXPECTED_IMPLICIT),
                    "explicit_only_entries": ["research-polisher-orchestrator"],
                    "pubmed_present": False,
                    "explicit_polisher_resolved": True,
                    "marketplace_source": source_identity["marketplace_source"],
                    "marketplace_ref": source_identity["marketplace_ref"],
                    "marketplace_revision": source_identity["marketplace_revision"],
                },
            )
            host = _actor(slot_id, "host", "orchestrator", [source["path"]], [report["path"]])
            runtime, _, _ = _run(
                slot / "runtime",
                slot_id,
                task_id,
                session_id,
                plugin_version,
                source_identity,
                [host],
                [source],
                [report],
                final_text=f"status: {item['expected_outcome']}\n",
            )
            binding = _base_binding(item, plugin_version, source_identity, runtime, [host], [report])

        item["status"] = "owner_observed"
        item["actual_outcome"] = item["expected_outcome"]
        item["binding"] = binding
    return receipts


def _all_items(receipts: dict[str, Any]) -> list[dict[str, Any]]:
    result = [receipts["distribution"]]
    for group in ("workflow_runs", "control_runs", "retrieval_runs"):
        result.extend(receipts[group])
    return result


def _slot(receipts: dict[str, Any], slot_id: str) -> dict[str, Any]:
    return next(item for item in _all_items(receipts) if item["slot_id"] == slot_id)


def _bound_actor(item: dict[str, Any], actor_id: str) -> dict[str, Any]:
    return next(
        actor
        for actor in item["binding"]["actor_bindings"]
        if actor["actor_id"] == actor_id
    )


def _save_receipts(receipts: dict[str, Any], path: Path) -> None:
    path.write_text(yaml.safe_dump(receipts, sort_keys=False), encoding="utf-8")


def _assert_rejected(
    baseline: dict[str, Any],
    plugin_version: str,
    receipts_path: Path,
    name: str,
    mutate: Callable[[dict[str, Any]], None],
    *,
    preserve: set[str] | None = None,
    expected_error: str | None = None,
) -> None:
    candidate = copy.deepcopy(baseline)
    mutate(candidate)
    baseline_by_slot = {item["slot_id"]: item for item in _all_items(baseline)}
    pending_by_slot = {
        item["slot_id"]: item for item in _all_items(validator.load_yaml(validator.RECEIPTS))
    }
    changed = {
        item["slot_id"]
        for item in _all_items(candidate)
        if item != baseline_by_slot[item["slot_id"]]
    }
    keep = changed | (preserve or set())
    for item in _all_items(candidate):
        slot_id = item["slot_id"]
        if slot_id not in keep:
            item.clear()
            item.update(copy.deepcopy(pending_by_slot[slot_id]))
    _save_receipts(candidate, receipts_path)
    result, errors = validator.validate_receipts(
        candidate, plugin_version, receipts_path=receipts_path
    )
    assert errors, f"{name}: mutation was accepted"
    if expected_error is not None:
        assert any(expected_error in error for error in errors), (
            f"{name}: expected error containing {expected_error!r}; got {errors}"
        )
    assert result["status"] == "in_progress_owner_observation", name


def _assert_run_index_rejected(
    baseline: dict[str, Any],
    plugin_version: str,
    receipts_path: Path,
    slot_id: str,
    name: str,
    mutate_index: Callable[[dict[str, Any]], None],
    expected_error: str,
) -> None:
    original: bytes | None = None
    index_path: Path | None = None

    def mutate(candidate: dict[str, Any]) -> None:
        nonlocal original, index_path
        item = _slot(candidate, slot_id)
        binding = item["binding"]["runtime_evidence"]["run_index"]
        index_path = validator.REPO / binding["path"]
        original = index_path.read_bytes()
        index = validator.load_yaml(index_path)
        mutate_index(index)
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        binding["sha256"] = validator.raw_file_sha256(index_path)

    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            name,
            mutate,
            expected_error=expected_error,
        )
    finally:
        if original is not None and index_path is not None:
            index_path.write_bytes(original)


def _assert_started_only_search_rejected(
    baseline: dict[str, Any],
    plugin_version: str,
    receipts_path: Path,
) -> None:
    originals: dict[Path, bytes] = {}

    def mutate(candidate: dict[str, Any]) -> None:
        item = _slot(candidate, "personal-search-current")
        runtime = item["binding"]["runtime_evidence"]
        jsonl_path = validator.REPO / runtime["jsonl"]["path"]
        index_path = validator.REPO / runtime["run_index"]["path"]
        originals[jsonl_path] = jsonl_path.read_bytes()
        originals[index_path] = index_path.read_bytes()
        events = [
            json.loads(line)
            for line in jsonl_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        events = [
            event
            for event in events
            if not (
                event.get("type") == "item.completed"
                and isinstance(event.get("item"), dict)
                and event["item"].get("type") == "web_search"
            )
        ]
        jsonl_path.write_text(
            "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
            encoding="utf-8",
        )
        runtime["jsonl"]["sha256"] = validator.raw_file_sha256(jsonl_path)
        index = validator.load_yaml(index_path)
        index["files"]["jsonl"]["sha256"] = runtime["jsonl"]["sha256"]
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        runtime["run_index"]["sha256"] = validator.raw_file_sha256(index_path)

    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            "started-only Search event",
            mutate,
            expected_error="claimed web_search events are absent",
        )
    finally:
        for path, content in originals.items():
            path.write_bytes(content)


def _replace_digest_for_path(value: Any, path: str, digest: str) -> None:
    if isinstance(value, dict):
        if value.get("path") == path and "sha256" in value:
            value["sha256"] = digest
        for item in value.values():
            _replace_digest_for_path(item, path, digest)
    elif isinstance(value, list):
        for item in value:
            _replace_digest_for_path(item, path, digest)


def _assert_review_record_rejected(
    baseline: dict[str, Any],
    plugin_version: str,
    receipts_path: Path,
    name: str,
    mutate_record: Callable[[dict[str, Any]], None],
    expected_error: str,
    *,
    report_index: int = -1,
    slot_id: str = "personal-idea-happy",
    compositor_report: bool = False,
) -> None:
    originals: dict[Path, bytes] = {}

    def mutate(candidate: dict[str, Any]) -> None:
        item = _slot(candidate, slot_id)
        workflow = item["binding"]["workflow_evidence"]
        report = (
            workflow["compositor_verification_artifact"]
            if compositor_report
            else workflow["evaluation_artifacts"][report_index]
        )
        report_path = validator.REPO / report["path"]
        index_binding = item["binding"]["runtime_evidence"]["run_index"]
        index_path = validator.REPO / index_binding["path"]
        originals[report_path] = report_path.read_bytes()
        originals[index_path] = index_path.read_bytes()
        record, errors = validator._load_review_record(report_path, name)
        assert record is not None and not errors, errors
        mutate_record(record)
        report_path.write_text(
            "---\n"
            + yaml.safe_dump(record, sort_keys=False, allow_unicode=True)
            + "---\n\n# Independent review\n\nMutated test report.\n",
            encoding="utf-8",
        )
        digest = validator.raw_file_sha256(report_path)
        _replace_digest_for_path(item["binding"], report["path"], digest)
        index = validator.load_yaml(index_path)
        _replace_digest_for_path(index, report["path"], digest)
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        item["binding"]["runtime_evidence"]["run_index"]["sha256"] = (
            validator.raw_file_sha256(index_path)
        )

    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            name,
            mutate,
            expected_error=expected_error,
        )
    finally:
        for path, content in originals.items():
            path.write_bytes(content)


def _assert_version_document_rejected(
    baseline: dict[str, Any],
    plugin_version: str,
    receipts_path: Path,
    slot_id: str,
    name: str,
    mutate_text: Callable[[str], str],
    expected_error: str,
) -> None:
    originals: dict[Path, bytes] = {}

    def mutate(candidate: dict[str, Any]) -> None:
        item = _slot(candidate, slot_id)
        artifact = item["binding"]["workflow_evidence"]["version_artifacts"][-1]
        artifact_path = validator.REPO / artifact["path"]
        index_binding = item["binding"]["runtime_evidence"]["run_index"]
        index_path = validator.REPO / index_binding["path"]
        originals[artifact_path] = artifact_path.read_bytes()
        originals[index_path] = index_path.read_bytes()
        artifact_path.write_text(
            mutate_text(artifact_path.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
        digest = validator.raw_file_sha256(artifact_path)
        _replace_digest_for_path(item["binding"], artifact["path"], digest)
        index = validator.load_yaml(index_path)
        _replace_digest_for_path(index, artifact["path"], digest)
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        index_binding["sha256"] = validator.raw_file_sha256(index_path)

    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            name,
            mutate,
            expected_error=expected_error,
        )
    finally:
        for path, content in originals.items():
            path.write_bytes(content)


def _without_h2(text: str, heading: str) -> str:
    return re.sub(
        rf"^## {re.escape(heading)}\s*$\n.*?(?=^## |\Z)",
        "",
        text,
        flags=re.M | re.S,
    )


def _replace_h2_body(text: str, heading: str, replacement: str) -> str:
    return re.sub(
        rf"(^## {re.escape(heading)}\s*$\n).*?(?=^## |\Z)",
        rf"\1\n{replacement}\n\n",
        text,
        flags=re.M | re.S,
    )


def _assert_review_stage_routes_independently_of_role(
    baseline: dict[str, Any], plugin_version: str, receipts_path: Path
) -> None:
    candidate = copy.deepcopy(baseline)
    item = _slot(candidate, "personal-idea-happy")
    reviewer_ids = item["binding"]["workflow_evidence"]["reviewer_actor_ids"]
    evaluator = _bound_actor(item, reviewer_ids[0])
    panel = _bound_actor(item, reviewer_ids[2])
    evaluator["role"], panel["role"] = panel["role"], evaluator["role"]
    index_binding = item["binding"]["runtime_evidence"]["run_index"]
    index_path = validator.REPO / index_binding["path"]
    original = index_path.read_bytes()
    try:
        index = validator.load_yaml(index_path)
        indexed = {actor["actor_id"]: actor for actor in index["actor_bindings"]}
        indexed[evaluator["actor_id"]]["role"] = evaluator["role"]
        indexed[panel["actor_id"]]["role"] = panel["role"]
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        index_binding["sha256"] = validator.raw_file_sha256(index_path)
        _save_receipts(candidate, receipts_path)
        result, errors = validator.validate_receipts(
            candidate, plugin_version, receipts_path=receipts_path
        )
        assert not errors, errors
        assert result["status"] == "owner_observed_ready"
    finally:
        index_path.write_bytes(original)


def _assert_final_status_rejected(
    baseline: dict[str, Any], plugin_version: str, receipts_path: Path
) -> None:
    originals: dict[Path, bytes] = {}

    def mutate(candidate: dict[str, Any]) -> None:
        item = _slot(candidate, "personal-idea-happy")
        runtime = item["binding"]["runtime_evidence"]
        final_path = validator.REPO / runtime["final_message"]["path"]
        index_path = validator.REPO / runtime["run_index"]["path"]
        originals[final_path] = final_path.read_bytes()
        originals[index_path] = index_path.read_bytes()
        final_path.write_text("status: rejected\n", encoding="utf-8")
        runtime["final_message"]["sha256"] = validator.raw_file_sha256(final_path)
        index = validator.load_yaml(index_path)
        index["files"]["final_message"]["sha256"] = runtime["final_message"]["sha256"]
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        runtime["run_index"]["sha256"] = validator.raw_file_sha256(index_path)

    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            "final status mismatch",
            mutate,
            expected_error="final message status differs from actual outcome",
        )
    finally:
        for path, content in originals.items():
            path.write_bytes(content)


def _assert_distribution_report_rejected(
    baseline: dict[str, Any], plugin_version: str, receipts_path: Path
) -> None:
    originals: dict[Path, bytes] = {}

    def mutate(candidate: dict[str, Any]) -> None:
        item = _slot(candidate, "personal-distribution-current")
        report = item["binding"]["artifact_bindings"][0]
        report_path = validator.REPO / report["path"]
        runtime = item["binding"]["runtime_evidence"]
        index_path = validator.REPO / runtime["run_index"]["path"]
        originals[report_path] = report_path.read_bytes()
        originals[index_path] = index_path.read_bytes()
        value = validator.load_yaml(report_path)
        value["skill_count"] = 1
        report_path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
        digest = validator.raw_file_sha256(report_path)
        _replace_digest_for_path(item["binding"], report["path"], digest)
        index = validator.load_yaml(index_path)
        _replace_digest_for_path(index, report["path"], digest)
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        runtime["run_index"]["sha256"] = validator.raw_file_sha256(index_path)

    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            "distribution count mismatch",
            mutate,
            expected_error="distribution report skill_count differs from installed evidence",
        )
    finally:
        for path, content in originals.items():
            path.write_bytes(content)


def _assert_dr_handoff_index_rejected(
    baseline: dict[str, Any],
    plugin_version: str,
    receipts_path: Path,
    name: str,
    mutate_index: Callable[[dict[str, Any]], None],
    expected_error: str,
) -> None:
    original: bytes | None = None
    index_path: Path | None = None

    def mutate(candidate: dict[str, Any]) -> None:
        nonlocal original, index_path
        item = _slot(candidate, "personal-deep-research-complete")
        binding = item["binding"]["deep_research_evidence"]["handoff_run_index"]
        index_path = validator.REPO / binding["path"]
        original = index_path.read_bytes()
        index = validator.load_yaml(index_path)
        mutate_index(index)
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        binding["sha256"] = validator.raw_file_sha256(index_path)

    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            name,
            mutate,
            expected_error=expected_error,
        )
    finally:
        if original is not None and index_path is not None:
            index_path.write_bytes(original)


def _assert_extra_auditor_rejected(
    baseline: dict[str, Any],
    plugin_version: str,
    receipts_path: Path,
    *,
    registered: bool,
) -> None:
    original_index: bytes | None = None
    index_path: Path | None = None

    def mutate(candidate: dict[str, Any]) -> None:
        nonlocal original_index, index_path
        item = _slot(candidate, "personal-article-happy")
        evidence = item["binding"]["workflow_evidence"]
        revised = evidence["version_artifacts"][-1]
        suffix = f"extra-{'registered' if registered else 'unregistered'}"
        report = _review_artifact(
            validator.REPO
            / Path(revised["path"]).parents[1]
            / "reviews"
            / ("registered-extra-auditor.md" if registered else "unregistered-extra-auditor.md"),
            f"extra-auditor-personal-article-happy-{'registered' if registered else 'unregistered'}",
            "v001",
            slot_id="personal-article-happy",
            actor_suffix=suffix,
            reviewer_skill="article-claim-auditor",
            review_stage="supporting_historical",
            reviewed_artifact=revised,
            decision="reject",
            fatal_findings=["Fatal claim-evidence conflict."],
        )
        actor = _actor(
            "personal-article-happy",
            suffix,
            "claim_auditor",
            [revised["path"]],
            [report["path"]],
            skill="article-claim-auditor",
            fresh=True,
            review_stage="supporting_historical",
        )
        item["binding"]["artifact_bindings"].append(report)
        item["binding"]["actor_bindings"].append(actor)
        if registered:
            evidence["reviewer_actor_ids"].append(actor["actor_id"])
        runtime = item["binding"]["runtime_evidence"]
        index_path = validator.REPO / runtime["run_index"]["path"]
        original_index = index_path.read_bytes()
        index = validator.load_yaml(index_path)
        index["actor_bindings"].append(copy.deepcopy(actor))
        index["output_bindings"].append(copy.deepcopy(report))
        index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
        runtime["run_index"]["sha256"] = validator.raw_file_sha256(index_path)

    expected = (
        "fatal or terminal reject review conflicts with ready outcome"
        if registered
        else "reviewer actor is absent from reviewer/assembler inventory"
    )
    try:
        _assert_rejected(
            baseline,
            plugin_version,
            receipts_path,
            "registered fatal supporting auditor" if registered else "unregistered fatal supporting auditor",
            mutate,
            expected_error=expected,
        )
    finally:
        if original_index is not None and index_path is not None:
            index_path.write_bytes(original_index)


def main() -> int:
    assert "\ufffd" not in Path(validator.__file__).read_text(encoding="utf-8")
    _assert_skill_tree_hash_portable()
    deterministic, deterministic_errors = validator.deterministic_checks()
    assert not deterministic_errors, deterministic_errors
    plugin_version = deterministic["plugin_version"]
    pending_receipts = validator.load_yaml(validator.RECEIPTS)
    pending, pending_errors = validator.validate_receipts(pending_receipts, plugin_version)
    assert not pending_errors, pending_errors
    assert pending["pending_slot_count"] == 13

    original_cli_query = validator._query_cli_version
    original_environment = {
        name: os.environ.get(name)
        for name in ("CODEX_HOME", "PATH")
    }
    try:
        try:
            original_cli_query(Path(sys.executable))
        except ValueError:
            pass
        else:
            raise AssertionError("non-Codex executable was accepted as Codex CLI")
        validator._query_cli_version = lambda _path: "0.144.4"
        private_root = validator.REPO / "tests" / "article" / ".phase7-8-runs"
        private_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=private_root) as directory:
            base = Path(directory)
            receipts_path = base / "local-owner-observed-receipts.yaml"
            baseline = _build_receipts(base, plugin_version)
            os.environ["CODEX_HOME"] = str((base / "fixture-codex-home").resolve())
            os.environ["PATH"] = str((base / "fixture-bin").resolve()) + os.pathsep + os.environ.get("PATH", "")
            _save_receipts(baseline, receipts_path)
            ready, ready_errors = validator.validate_receipts(
                baseline, plugin_version, receipts_path=receipts_path
            )
            assert not ready_errors, "\n".join(ready_errors)
            assert ready["status"] == "owner_observed_ready"
            assert ready["owner_observed_slot_count"] == 13
            initial_report = _slot(baseline, "personal-idea-happy")["binding"][
                "workflow_evidence"
            ]["evaluation_artifacts"][0]
            initial_record, initial_errors = validator._load_review_record(
                validator.REPO / initial_report["path"], "historical-positive"
            )
            assert not initial_errors and initial_record is not None
            assert initial_record["review_stage"] == "initial_evaluator"
            assert initial_record["blocking_findings"] and initial_record["decision"] == "revise"
            _assert_review_stage_routes_independently_of_role(
                baseline, plugin_version, receipts_path
            )

            def drop_polisher_assembler_input(value: dict[str, Any]) -> None:
                item = _slot(value, "personal-research-polisher-happy")
                evidence = item["binding"]["workflow_evidence"]
                actor = _bound_actor(item, evidence["generator_actor_ids"][0])
                report_id = evidence["polisher_matrix"]["cells"][0]["artifact_id"]
                report = next(
                    artifact
                    for artifact in item["binding"]["artifact_bindings"]
                    if artifact["artifact_id"] == report_id
                )
                actor["files_read"].remove(report["path"])

            def add_forbidden_reviewer_read(value: dict[str, Any], source: str) -> None:
                item = _slot(value, "personal-idea-happy")
                evidence = item["binding"]["workflow_evidence"]
                actor = _bound_actor(item, evidence["reviewer_actor_ids"][1])
                if source == "initial":
                    path = evidence["version_artifacts"][0]["path"]
                elif source == "delta":
                    path = evidence["revision_delta"]["path"]
                else:
                    path = evidence["evaluation_artifacts"][0]["path"]
                actor["files_read"].append(path)

            def duplicate_task(value: dict[str, Any]) -> None:
                _slot(value, "personal-idea-happy")["binding"]["task_id"] = _slot(
                    value, "personal-proposal-happy"
                )["binding"]["task_id"]

            def duplicate_instance(value: dict[str, Any]) -> None:
                idea = _slot(value, "personal-idea-happy")
                proposal = _slot(value, "personal-proposal-happy")
                idea["binding"]["actor_bindings"][0]["instance_id"] = proposal[
                    "binding"
                ]["actor_bindings"][0]["instance_id"]

            def duplicate_narrow_search_url(value: dict[str, Any]) -> None:
                records = _slot(value, "personal-search-narrow-academic")["binding"][
                    "search_evidence"
                ]["source_records"]
                records[1]["url"] = records[0]["url"]

            def reuse_deep_research_continuation(value: dict[str, Any]) -> None:
                evidence = _slot(value, "personal-deep-research-complete")["binding"][
                    "deep_research_evidence"
                ]
                evidence["returned_result"] = copy.deepcopy(
                    evidence["continuation_package"]
                )

            def supporting_actor(value: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
                item = _slot(value, "personal-idea-happy")
                evidence = item["binding"]["workflow_evidence"]
                actor = next(
                    candidate
                    for candidate in item["binding"]["actor_bindings"]
                    if candidate.get("review_stage") == "supporting_historical"
                )
                return evidence, actor

            def historical_support_reads_latest(value: dict[str, Any]) -> None:
                evidence, actor = supporting_actor(value)
                actor["files_read"] = [evidence["version_artifacts"][-1]["path"]]

            def historical_support_not_consumed(value: dict[str, Any]) -> None:
                evidence, actor = supporting_actor(value)
                item = _slot(value, "personal-idea-happy")
                reviser = _bound_actor(item, evidence["generator_actor_ids"][1])
                reviser["files_read"].remove(actor["files_written"][0])

            def pregeneration_support_reads_version(value: dict[str, Any]) -> None:
                _evidence, actor = supporting_actor(value)
                actor["review_stage"] = "supporting_pre_generation"

            def polisher_normalized_path_overlap(value: dict[str, Any]) -> None:
                evidence = _slot(value, "personal-research-polisher-happy")["binding"]["workflow_evidence"]
                raw = evidence["source_inputs_before"][0]
                frozen = evidence["frozen_review_inputs"][0]
                frozen["path"] = raw["path"].replace("/", "\\")
                frozen["sha256"] = raw["sha256"]

            def polisher_identity_alias(value: dict[str, Any]) -> None:
                evidence = _slot(value, "personal-research-polisher-happy")["binding"]["workflow_evidence"]
                raw = evidence["source_inputs_before"][0]
                frozen = evidence["frozen_review_inputs"][0]
                frozen["artifact_id"] = raw["artifact_id"]
                frozen["version"] = raw["version"]

            mutations: list[tuple[str, Callable[[dict[str, Any]], None], set[str] | None, str | None]] = [
                (
                    "slot kind dispatch bypass",
                    lambda value: _slot(value, "personal-idea-happy").update({"kind": "distribution"}),
                    None,
                    "kind differs from the fixed slot contract",
                ),
                (
                    "incomplete workflow artifact",
                    lambda value: _slot(value, "personal-idea-happy")["binding"]["workflow_evidence"]["version_artifacts"].pop(),
                    None,
                    None,
                ),
                (
                    "missing panel reviewer",
                    lambda value: _slot(value, "personal-idea-happy")["binding"]["workflow_evidence"]["reviewer_actor_ids"].pop(),
                    None,
                    None,
                ),
                (
                    "Polisher incomplete matrix",
                    lambda value: _slot(value, "personal-research-polisher-happy")["binding"]["workflow_evidence"]["polisher_matrix"]["cells"].pop(),
                    None,
                    None,
                ),
                (
                    "Polisher placeholder matrix option",
                    lambda value: _slot(value, "personal-research-polisher-happy")["binding"]["workflow_evidence"]["polisher_matrix"]["cells"][0].update({"content_summary": "placeholder placeholder placeholder placeholder placeholder"}),
                    None,
                    "Research Polisher matrix contains a placeholder option",
                ),
                (
                    "Polisher dossier registered as raw source",
                    lambda value: _slot(value, "personal-research-polisher-happy")["binding"]["workflow_evidence"].update({
                        "source_inputs_before": copy.deepcopy(_slot(value, "personal-research-polisher-happy")["binding"]["workflow_evidence"]["frozen_review_inputs"]),
                        "source_inputs_after": copy.deepcopy(_slot(value, "personal-research-polisher-happy")["binding"]["workflow_evidence"]["frozen_review_inputs"]),
                    }),
                    None,
                    "Research Polisher dossier is incorrectly registered as raw source input",
                ),
                (
                    "Polisher assembler omitted strategist report",
                    drop_polisher_assembler_input,
                    None,
                    "initial assembler did not read all strategist reports",
                ),
                (
                    "wrong artifact hash",
                    lambda value: _slot(value, "personal-idea-happy")["binding"]["workflow_evidence"]["version_artifacts"][0].update({"sha256": "0" * 64}),
                    None,
                    "SHA-256 does not match file bytes",
                ),
                (
                    "artifact path escape",
                    lambda value: _slot(value, "personal-idea-happy")["binding"]["artifact_bindings"][0].update({"path": "../outside.md"}),
                    None,
                    "path escapes the repository",
                ),
                (
                    "reversed timestamps",
                    lambda value: _slot(value, "personal-idea-happy")["binding"].update({"completed_at": "2026-07-16T23:59:59Z"}),
                    None,
                    "completed_at precedes started_at",
                ),
                (
                    "duplicate task ID",
                    duplicate_task,
                    {"personal-proposal-happy"},
                    "duplicate global task_id",
                ),
                (
                    "duplicate reviewer instance ID",
                    duplicate_instance,
                    {"personal-proposal-happy"},
                    "duplicate global instance_id",
                ),
                (
                    "fresh reviewer read initial artifact",
                    lambda value: add_forbidden_reviewer_read(value, "initial"),
                    None,
                    "fresh reviewer read the initial artifact version",
                ),
                (
                    "fresh reviewer read revision delta",
                    lambda value: add_forbidden_reviewer_read(value, "delta"),
                    None,
                    "read delta, prior review, panel, or README evidence",
                ),
                (
                    "fresh reviewer read prior evaluation",
                    lambda value: add_forbidden_reviewer_read(value, "evaluation"),
                    None,
                    "read delta, prior review, panel, or README evidence",
                ),
                (
                    "historical supporting reviewer mislabeled on latest version",
                    historical_support_reads_latest,
                    None,
                    "supporting_historical reviewer must read v001 and not v002",
                ),
                (
                    "historical supporting report not consumed by reviser",
                    historical_support_not_consumed,
                    None,
                    "historical supporting report was not read by the reviser",
                ),
                (
                    "pre-generation supporting reviewer read a version",
                    pregeneration_support_reads_version,
                    None,
                    "supporting_pre_generation reviewer read a version artifact",
                ),
                (
                    "missing explicit compositor verification binding",
                    lambda value: _slot(value, "personal-article-happy")["binding"]["workflow_evidence"].update({"compositor_verification_artifact": None}),
                    None,
                    "independent compositor lacks explicit verification artifact",
                ),
                (
                    "Polisher normalized raw/frozen path overlap",
                    polisher_normalized_path_overlap,
                    None,
                    "Research Polisher dossier is incorrectly registered as raw source input",
                ),
                (
                    "Polisher artifact identity alias",
                    polisher_identity_alias,
                    None,
                    "artifact identity aliases multiple normalized paths",
                ),
                (
                    "source input changed",
                    lambda value: _slot(value, "personal-idea-happy")["binding"]["workflow_evidence"]["source_inputs_after"][0].update({"sha256": "1" * 64}),
                    None,
                    "source input 0 changed during the workflow",
                ),
                (
                    "control false-ready trace",
                    lambda value: _slot(value, "personal-reviewer-unavailable-control")["binding"]["control_evidence"]["state_trace"].append("human_signoff_required"),
                    None,
                    "control state trace contains a ready state",
                ),
                (
                    "fatal digest relationship",
                    lambda value: _slot(value, "personal-fatal-finding-control")["binding"]["control_evidence"]["digest_mismatch_evidence"].update({"supplied_sha256": _slot(value, "personal-fatal-finding-control")["binding"]["control_evidence"]["digest_mismatch_evidence"]["expected_sha256"]}),
                    None,
                    "fatal digest relationship is invalid",
                ),
                (
                    "fabricated Search source",
                    lambda value: _slot(value, "personal-search-current")["binding"]["search_evidence"]["source_records"][0].update({"url": "https://fabricated.invalid/source"}),
                    None,
                    "source records do not exactly cover opened URLs",
                ),
                (
                    "missing Search event",
                    lambda value: _slot(value, "personal-search-exact")["binding"]["search_evidence"].update({"event_ids": ["web-missing"]}),
                    None,
                    "claimed web_search events are absent",
                ),
                (
                    "narrow Search source count",
                    lambda value: _slot(value, "personal-search-narrow-academic")["binding"]["search_evidence"]["source_records"].pop(),
                    None,
                    "must use 2-5 primary papers",
                ),
                (
                    "duplicate narrow Search paper URL",
                    duplicate_narrow_search_url,
                    None,
                    "Search source record URLs must be unique",
                ),
                (
                    "Deep Research repeated resume",
                    lambda value: _slot(value, "personal-deep-research-complete")["binding"]["deep_research_evidence"].update({"resume_count": 2}),
                    None,
                    None,
                ),
                (
                    "Deep Research origin mismatch",
                    lambda value: _slot(value, "personal-deep-research-complete")["binding"]["deep_research_evidence"].update({"origin_task_id": "wrong-task"}),
                    None,
                    "Deep Research origin differs from receipt task/session",
                ),
                (
                    "Deep Research edge-ledger mismatch",
                    lambda value: _slot(value, "personal-deep-research-complete")["binding"]["deep_research_evidence"].update({"pending_edge_id": "edge-wrong"}),
                    None,
                    "edge ledger pending_edge_id differs",
                ),
                (
                    "Deep Research returned result reused continuation",
                    reuse_deep_research_continuation,
                    None,
                    "Deep Research content artifact roles are not distinct",
                ),
                (
                    "marketplace identity mismatch",
                    lambda value: _slot(value, "personal-distribution-current")["binding"]["source_identity"].update({"marketplace_ref": "dev"}),
                    None,
                    "marketplace metadata ref differs",
                ),
                (
                    "CLI version mismatch",
                    lambda value: _slot(value, "personal-distribution-current")["binding"]["source_identity"].update({"cli_version": "9.9.9"}),
                    None,
                    "CLI --version output differs from source identity",
                ),
                (
                    "inactive CODEX_HOME config",
                    lambda value: _slot(value, "personal-distribution-current")["binding"]["source_identity"].update({"config_path": str((base / "not-active" / "config.toml").resolve())}),
                    None,
                    "config_path is not the active CODEX_HOME config.toml",
                ),
            ]
            for name, mutate, preserve, expected_error in mutations:
                _assert_rejected(
                    baseline,
                    plugin_version,
                    receipts_path,
                    name,
                    mutate,
                    preserve=preserve,
                    expected_error=expected_error,
                )

            for slot_id, heading, expected_error in (
                (
                    "personal-idea-happy",
                    "Evidence chains",
                    "Idea dossier lacks required section(s): Evidence chains",
                ),
                (
                    "personal-proposal-happy",
                    "Methods",
                    "proposal artifact lacks required section Methods",
                ),
                (
                    "personal-article-happy",
                    "Results",
                    "article artifact lacks required section Results",
                ),
                (
                    "personal-perspective-happy",
                    "Evidence and counterarguments",
                    "perspective artifact lacks required section Evidence and counterarguments",
                ),
                (
                    "personal-research-polisher-happy",
                    "Pareto trade-offs",
                    "research_polisher artifact lacks required section Pareto trade-offs",
                ),
            ):
                _assert_version_document_rejected(
                    baseline,
                    plugin_version,
                    receipts_path,
                    slot_id,
                    f"{slot_id} missing complete section",
                    lambda text, heading=heading: _without_h2(text, heading),
                    expected_error,
                )
            _assert_version_document_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "personal-proposal-happy",
                "proposal one-character section",
                lambda text: _replace_h2_body(text, "Methods", "x"),
                "proposal section is empty or placeholder: Methods",
            )

            _assert_run_index_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "personal-reviewer-unavailable-control",
                "reviewer unavailable with multi-agent enabled",
                lambda index: index["command"].update({"multi_agent_enabled": True}),
                "reviewer-unavailable control did not disable multi-agent",
            )
            _assert_started_only_search_rejected(
                baseline, plugin_version, receipts_path
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "fatal review cannot reach ready",
                lambda record: record["fatal_findings"].append("fatal source-level flaw"),
                "fatal or terminal reject review conflicts with ready outcome",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "initial fatal cannot reach ready",
                lambda record: record["fatal_findings"].append("historical source-level fatal flaw"),
                "fatal or terminal reject review conflicts with ready outcome",
                report_index=0,
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "fresh revise decision cannot reach ready",
                lambda record: record.update({"decision": "revise"}),
                "qualifying blocking or non-qualifying decision conflicts with ready outcome",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "unknown qualifying decision cannot reach ready",
                lambda record: record.update({"decision": "undetermined_but_ok"}),
                "qualifying blocking or non-qualifying decision conflicts with ready outcome",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "qualifying blocking finding cannot reach ready",
                lambda record: record["blocking_findings"].append("Unresolved qualifying blocker."),
                "qualifying blocking or non-qualifying decision conflicts with ready outcome",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "review workflow cross-binding mismatch",
                lambda record: record.update({"workflow_id": "wrong-workflow"}),
                "workflow_id differs from the workflow receipt",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "review actor cross-binding mismatch",
                lambda record: record.update({"reviewer_actor_id": "wrong-actor"}),
                "reviewer_actor_id differs from the bound actor",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "review stage cross-binding mismatch",
                lambda record: record.update({"review_stage": "initial_evaluator"}),
                "review_stage differs from the bound actor",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "review input IDs cross-binding mismatch",
                lambda record: record.update({"input_artifact_ids": ["wrong-artifact"]}),
                "input_artifact_ids differ from bound files_read artifacts",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "review files cross-binding mismatch",
                lambda record: record.update({"files_read": []}),
                "files_read differs from the bound actor",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "review report artifact cross-binding mismatch",
                lambda record: record.update({"report_artifact_id": "wrong-report"}),
                "report_artifact_id differs from the report binding",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "review unified findings missing",
                lambda record: record.pop("findings"),
                "findings list is missing or malformed",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "reviewed digest mismatch",
                lambda record: record.update({"reviewed_artifact_digest": "0" * 64}),
                "reviewed artifact digest differs from the frozen input",
            )
            _assert_review_record_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "fatal compositor verification cannot reach ready",
                lambda record: record["fatal_findings"].append(
                    "Fatal package verification finding."
                ),
                "fatal or terminal reject review conflicts with ready outcome",
                slot_id="personal-article-happy",
                compositor_report=True,
            )
            _assert_extra_auditor_rejected(
                baseline,
                plugin_version,
                receipts_path,
                registered=False,
            )
            _assert_extra_auditor_rejected(
                baseline,
                plugin_version,
                receipts_path,
                registered=True,
            )
            _assert_final_status_rejected(baseline, plugin_version, receipts_path)
            _assert_distribution_report_rejected(
                baseline, plugin_version, receipts_path
            )
            _assert_dr_handoff_index_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "Deep Research handoff session mismatch",
                lambda index: index.update({"session_id": "wrong-session"}),
                "session_id differs from the Deep Research origin",
            )
            _assert_dr_handoff_index_rejected(
                baseline,
                plugin_version,
                receipts_path,
                "Deep Research handoff omitted pending ledger",
                lambda index: index["output_bindings"].pop(),
                "handoff output omits the pending edge ledger",
            )

            with tempfile.TemporaryDirectory(dir=validator.REPO / "tests") as unignored:
                unignored_receipts = Path(unignored) / "receipts.yaml"
                _save_receipts(baseline, unignored_receipts)
                result, privacy_errors = validator.validate_receipts(
                    baseline, plugin_version, receipts_path=unignored_receipts
                )
                assert privacy_errors, "unignored receipt path was accepted"
                assert result["status"] == "in_progress_owner_observation"
    finally:
        validator._query_cli_version = original_cli_query
        for name, value in original_environment.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    report, report_errors = validator.build_report()
    assert not report_errors, report_errors
    assert report["personal_status"] == "in_progress_owner_observation"
    print("Personal readiness validator tests passed: complete 13-slot graph + 64 mutations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
