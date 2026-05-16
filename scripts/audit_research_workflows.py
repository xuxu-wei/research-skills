#!/usr/bin/env python3
"""Audit cross-package research workflow consistency.

The active research workflow source of truth is ``research-skills/``. Legacy
skill trees may exist for archival comparison, but this audit intentionally
does not inspect them.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "research-skills"
PACKAGES = ("research-idea", "research-perspective", "research-proposal", "research-article")
MAX_SKILL_LINES = 300


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def skill_files() -> list[Path]:
    return sorted(SKILLS.glob("*/*/SKILL.md"))


def skill_name(path: Path) -> str | None:
    match = re.search(r"^name:\s*(\S+)", read(path), re.M)
    return match.group(1) if match else None


def installed_skill_names() -> set[str]:
    return {name for path in skill_files() if (name := skill_name(path))}


def check_terms(path: Path, terms: tuple[str, ...], message: str) -> list[str]:
    if not path.exists():
        return [f"{message}: missing {rel(path)}"]
    text = read(path)
    missing = [term for term in terms if term not in text]
    return [f"{message}: missing terms {missing}"] if missing else []


def package_errors() -> list[str]:
    errors: list[str] = []
    for package in PACKAGES:
        if not (SKILLS / package).exists():
            errors.append(f"missing package: research-skills/{package}")
    return errors


def related_skill_errors(names: set[str]) -> list[str]:
    errors: list[str] = []
    bullet = re.compile(r"^\s+-\s+([A-Za-z0-9_-]+)\s*$")
    for package in PACKAGES:
        root = SKILLS / package
        if not root.exists():
            continue
        for path in sorted(root.glob("*/SKILL.md")):
            text = read(path)
            if "related_skills:" not in text:
                errors.append(f"{rel(path)}: missing metadata.hermes.related_skills")
                continue
            in_related = False
            for line in text.splitlines():
                if "related_skills:" in line:
                    in_related = True
                    continue
                if in_related and line and not line.startswith(" "):
                    in_related = False
                if not in_related:
                    continue
                match = bullet.match(line)
                if match and match.group(1) not in names:
                    errors.append(f"{rel(path)}: unresolved related_skill `{match.group(1)}`")
    return errors


def isolation_errors() -> list[str]:
    errors: list[str] = []
    role_pattern = re.compile(r"(evaluator|review-panel|adversarial|final-compositor|auditor|triage)")
    isolation_pattern = re.compile(r"(delegate_task|isolated|isolation|independent|隔离|独立)", re.I)
    boundary_pattern = re.compile(r"(do not|must not|不得|不可|只评|不修订|不重写|does NOT)", re.I)
    for package in PACKAGES:
        root = SKILLS / package
        if not root.exists():
            continue
        for path in sorted(root.glob("*/SKILL.md")):
            name = skill_name(path) or path.parent.name
            if not role_pattern.search(name):
                continue
            text = read(path)
            if not isolation_pattern.search(text):
                errors.append(f"{rel(path)}: reviewer/evaluator role missing isolation/delegation language")
            if not boundary_pattern.search(text):
                errors.append(f"{rel(path)}: reviewer/evaluator role missing prohibited-action boundary")
    return errors


def governance_errors() -> list[str]:
    errors: list[str] = []
    package_specs = {
        "research-idea": {
            "orchestrator": "research-idea-orchestrator",
            "state": "09_state",
            "terms": ("artifact-naming-and-directory-rules.md", "academic-language-assessor", "language-assessment-vNNN.md", "language-change-log-rNNN.md"),
        },
        "research-perspective": {
            "orchestrator": "perspective-orchestrator",
            "state": "09_state",
            "terms": ("04_drafts/", "06_revisions/round-NNN", "response-to-reviewers-rNNN.md", "revision-delta", "language-assessment", "change_type: language_only"),
        },
        "research-proposal": {
            "orchestrator": "proposal-orchestrator",
            "state": "10_state",
            "terms": ("04_drafts/proposal-vNNN.md", "06_revisions/round-NNN", "response-to-reviewers file", "delta report", "language-assessment-vNNN.md", "change_type: language_only"),
        },
        "research-article": {
            "orchestrator": "article-orchestrator",
            "state": "13_state",
            "terms": ("06_drafts/manuscript-vNNN.md", "09_revisions/round-NNN", "response-to-reviewers-rNNN.md", "revision-delta-rNNN.md", "language-assessment-vNNN.md", "change_type: language_only"),
        },
    }
    for package, spec in package_specs.items():
        orch = SKILLS / package / spec["orchestrator"]
        errors.extend(check_terms(orch / "SKILL.md", spec["terms"], f"{package} orchestrator missing artifact/language governance"))
        errors.extend(check_terms(orch / "references" / "artifact-naming-and-directory-rules.md", (spec["state"], "source_skill", "change_type", "based_on"), f"{package} artifact naming rules missing shared lineage fields"))
    return errors


def invariant_errors() -> list[str]:
    errors: list[str] = []
    errors.extend(check_terms(
        SKILLS / "research-idea" / "research-idea-orchestrator" / "SKILL.md",
        ("idea-adversarial-review-panel", "adversarial review", "proposal_handoff_status"),
        "research-idea orchestrator missing pre-handoff adversarial review",
    ))
    errors.extend(check_terms(
        SKILLS / "research-idea" / "research-idea-orchestrator" / "references" / "idea-id-and-lineage-rules.md",
        ("I<round>-<sequence>", "previous_ids", "I02-M001", "Do not rename an idea after"),
        "research-idea orchestrator-owned lineage rules missing canonical idea ID governance",
    ))
    errors.extend(check_terms(
        SKILLS / "research-idea" / "research-idea-orchestrator" / "references" / "artifact-contracts.md",
        ("idea-id-and-lineage-rules.md", "previous_ids", "origin_round", "revision_round"),
        "research-idea orchestrator-owned artifact contracts missing idea ID lineage fields",
    ))
    errors.extend(check_terms(
        SKILLS / "research-proposal" / "proposal-review-panel" / "SKILL.md",
        ("lightweight_panel", "standard_panel", "full_panel"),
        "research-proposal panel missing 3/5/7 tier terms",
    ))
    errors.extend(check_terms(
        SKILLS / "research-perspective" / "perspective-review-panel" / "SKILL.md",
        ("Conditional Reviewers", "Methodology / Statistics Reviewer", "Practicing-Clinician Reviewer", "Outlet-Fit Editor Reviewer"),
        "research-perspective panel missing conditional reviewer rules",
    ))
    errors.extend(check_terms(
        SKILLS / "research-article" / "DESCRIPTION.md",
        ("research-article", "article-*", "Do not rename"),
        "research-article package missing article-* naming note",
    ))
    return errors


def double_number_errors() -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"\b\d{2}_\d{2}_[A-Za-z0-9_-]+")
    for package in PACKAGES:
        root = SKILLS / package
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            matches = sorted(set(pattern.findall(read(path))))
            if matches:
                errors.append(f"{rel(path)}: double-numbered directory references {matches}")
    return errors


def shared_residue_errors() -> list[str]:
    errors: list[str] = []
    shared_name = "research-idea-" + "shared"
    shared_suffix = "_" + "shared"
    shared_path = "research-idea/" + shared_suffix
    residue_pattern = re.compile(rf"({shared_name}|{re.escape(shared_path)}|[/\\]_shared\b)")
    targets = [REPO / "flatten-validation.json", REPO / "codex-plugin-validation.json"]
    targets.extend((SKILLS / package).rglob("*.md") for package in PACKAGES if (SKILLS / package).exists())
    flat_targets: list[Path] = []
    for item in targets:
        if isinstance(item, Path):
            flat_targets.append(item)
        else:
            flat_targets.extend(item)
    for path in flat_targets:
        if path.exists() and residue_pattern.search(read(path)):
            errors.append(f"{rel(path)}: stale shared-skill reference")
    if (SKILLS / "research-idea" / shared_suffix).exists():
        errors.append("research-skills/research-idea legacy shared-skill directory still exists")
    return errors


def referenced_markdown_errors() -> list[str]:
    errors: list[str] = []
    ref_pattern = re.compile(r"`([^`]+\.md)`")
    for package in PACKAGES:
        root = SKILLS / package
        if not root.exists():
            continue
        for skill in sorted(root.glob("*/SKILL.md")):
            for ref in sorted(set(ref_pattern.findall(read(skill)))):
                if ref.startswith("references/"):
                    target = skill.parent / ref
                elif ref.startswith(f"{skill.parent.name}/references/"):
                    target = root / ref
                elif ref.startswith("article-orchestrator/references/") and package == "research-article":
                    target = root / ref
                elif ref.startswith("proposal-orchestrator/references/") and package == "research-proposal":
                    target = root / ref
                elif ref.startswith("perspective-orchestrator/references/") and package == "research-perspective":
                    target = root / ref
                elif ref.startswith("research-idea-orchestrator/references/") and package == "research-idea":
                    target = root / ref
                else:
                    continue
                if not target.exists():
                    errors.append(f"{rel(skill)}: missing referenced markdown `{ref}` -> {rel(target)}")
    return errors


def article_contract_errors() -> list[str]:
    errors: list[str] = []
    root = SKILLS / "research-article"
    if not root.exists():
        return errors

    naming = root / "article-orchestrator" / "references" / "artifact-naming-and-directory-rules.md"
    contracts = root / "article-orchestrator" / "references" / "artifact-contracts.md"
    state = root / "article-orchestrator" / "references" / "workflow-state-schema.md"
    orchestrator = root / "article-orchestrator" / "SKILL.md"
    cover_letter = root / "article-cover-letter" / "SKILL.md"
    frontmatter = root / "article-frontmatter-drafter" / "SKILL.md"
    evaluator = root / "article-evaluator" / "SKILL.md"
    refinement = root / "article-refinement-controller" / "SKILL.md"
    compositor = root / "article-submission-compositor" / "SKILL.md"

    errors.extend(check_terms(
        naming,
        ("08_evaluations/evaluation-v001.md", "response-to-reviewers-r001.md", "10_panel/panel-report-v001.md", "11_cover-letter/cover-letter.md", "12_package/submission-package.md"),
        "research-article artifact naming rules missing canonical filenames",
    ))
    errors.extend(check_terms(
        contracts,
        ("artifact_id: \"eval-001\"", "draft_ref:", "independence_status: true_isolated | inline_degraded | invalid", "response_to_reviewers:", "enter_manuscript | response_only | decline", "cover_letter:", "cover-letter-001", "pre_submission_verification:", "fixability: fixable_by_downscaling", "supplementary_required: true | false"),
        "research-article artifact contracts missing canonical evaluation/revision/submission fields",
    ))
    errors.extend(check_terms(
        state,
        ("artifacts:", "registry:", "based_on:", "change_type:", "cover_letter_path:", "cover_letter_review_path:", "verification:", "true_isolated_evaluation_completed:", "human_signoff:"),
        "research-article workflow state missing lineage or verification fields",
    ))
    errors.extend(check_terms(
        orchestrator,
        ("article-cover-letter", "Cover Letter Drafting", "Fast-track entry must pass minimum backfill gates", "Reference verification", "table/figure/result consistency", "ethics and declarations checklist"),
        "research-article orchestrator missing fast-track or pre-submission gates",
    ))
    errors.extend(check_terms(
        cover_letter,
        ("medical-journal-review", "cover-letter-only", "apparent_article_tier", "11_cover-letter/cover-letter.md", "templates/cover-letter.md"),
        "research-article cover letter skill missing independent biomedical review or artifact contract",
    ))
    if frontmatter.exists():
        frontmatter_text = read(frontmatter)
        forbidden = ("cover_letter_draft", "11_frontmatter/cover-letter.md")
        present = [term for term in forbidden if term in frontmatter_text]
        if present:
            errors.append(f"{rel(frontmatter)}: frontmatter skill still owns cover-letter artifacts {present}")
    errors.extend(check_terms(
        evaluator,
        ("independence_status", "inline_degraded", "enter_manuscript | response_only | decline"),
        "research-article evaluator missing isolation or entry strategy contract",
    ))
    errors.extend(check_terms(
        refinement,
        ("enter_manuscript", "response_only", "decline", "response-to-reviewers-rNNN.md"),
        "research-article refinement controller missing canonical revision strategy terms",
    ))
    errors.extend(check_terms(
        compositor,
        ("article-cover-letter", "11_cover-letter/**", "cover_letter_quality_check", "medical_cover_letter_review", "pre_submission_verification", "reference_verification", "table_figure_result_consistency", "journal_instruction_verification", "ethics_declarations", "`ready_for_author_signoff` requires", "supplementary_required", "Recoverable mismatch", "Unresolvable mismatch"),
        "research-article compositor missing pre-submission verification gates",
    ))
    return errors


def article_dry_run_errors() -> list[str]:
    """Exercise research-article routing invariants with compact simulated states."""

    errors: list[str] = []

    def can_signoff(state: dict[str, object]) -> bool:
        return (
            state.get("primary_results_present") is True
            and state.get("fatal_overclaim_unfixable") is not True
            and not (state.get("supplementary_required") is True and state.get("supplementary_present") is False)
            and state.get("version_mismatch_unresolvable") is not True
            and state.get("true_isolated_evaluation_completed") is True
            and state.get("references_verified") == "pass"
            and state.get("result_consistency") == "pass"
            and state.get("journal_verified") == "verified"
            and state.get("ethics_declarations") in {"complete", "not_applicable"}
        )

    def route_status(state: dict[str, object]) -> str:
        if state.get("primary_results_present") is False:
            return "blocked"
        if state.get("fatal_overclaim_unfixable") is True:
            return "blocked"
        if state.get("fatal_overclaim_fixable") is True:
            return "revision_required"
        if state.get("supplementary_required") is True and state.get("supplementary_present") is False:
            return "blocked"
        if state.get("version_mismatch_unresolvable") is True:
            return "blocked"
        if state.get("version_mismatch_recoverable") is True:
            return "ready_for_author_check"
        if can_signoff(state):
            return "ready_for_author_signoff"
        return "ready_for_author_check"

    standard = {
        "entry_mode": "standard",
        "primary_results_present": True,
        "true_isolated_evaluation_completed": True,
        "references_verified": "pass",
        "result_consistency": "pass",
        "journal_verified": "verified",
        "ethics_declarations": "complete",
    }
    fast_track = {
        "entry_mode": "fast_track_has_draft",
        "primary_results_present": True,
        "true_isolated_evaluation_completed": True,
        "references_verified": "partial",
        "result_consistency": "partial",
        "journal_verified": "user_supplied_only",
        "ethics_declarations": "complete",
        "scope_limitations": ["fast_track_backfill"],
    }
    submission_only = {
        "entry_mode": "submission_only",
        "primary_results_present": True,
        "true_isolated_evaluation_completed": True,
        "references_verified": "pass",
        "result_consistency": "pass",
        "journal_verified": "verified",
        "ethics_declarations": "complete",
    }

    expected = {
        "standard": (standard, "ready_for_author_signoff"),
        "fast_track": (fast_track, "ready_for_author_check"),
        "submission_only": (submission_only, "ready_for_author_signoff"),
        "missing_primary_result": ({**standard, "primary_results_present": False}, "blocked"),
        "fatal_overclaim_fixable": ({**standard, "fatal_overclaim_fixable": True}, "revision_required"),
        "fatal_overclaim_unfixable": ({**standard, "fatal_overclaim_unfixable": True}, "blocked"),
        "supplementary_not_required_absent": ({**standard, "supplementary_required": False, "supplementary_present": False}, "ready_for_author_signoff"),
        "supplementary_required_missing": ({**standard, "supplementary_required": True, "supplementary_present": False}, "blocked"),
        "version_mismatch_recoverable": ({**standard, "version_mismatch_recoverable": True}, "ready_for_author_check"),
        "version_mismatch_unresolvable": ({**standard, "version_mismatch_unresolvable": True}, "blocked"),
        "delegate_unavailable": ({**standard, "true_isolated_evaluation_completed": False}, "ready_for_author_check"),
    }

    for name, (state, wanted) in expected.items():
        got = route_status(state)
        if got != wanted:
            errors.append(f"research-article dry-run `{name}` expected {wanted}, got {got}")
        if name == "fast_track" and "scope_limitations" not in state:
            errors.append("research-article dry-run `fast_track` missing scope_limitations")
    return errors


def skill_length_warnings() -> list[str]:
    warnings: list[str] = []
    for path in skill_files():
        line_count = len(read(path).splitlines())
        if line_count > MAX_SKILL_LINES:
            warnings.append(f"{rel(path)}: SKILL.md has {line_count} lines; target maximum is {MAX_SKILL_LINES}")
    return warnings


def main() -> int:
    names = installed_skill_names()
    errors: list[str] = []
    errors.extend(package_errors())
    errors.extend(related_skill_errors(names))
    errors.extend(isolation_errors())
    errors.extend(governance_errors())
    errors.extend(invariant_errors())
    errors.extend(double_number_errors())
    errors.extend(shared_residue_errors())
    errors.extend(referenced_markdown_errors())
    errors.extend(article_contract_errors())
    errors.extend(article_dry_run_errors())
    warnings = skill_length_warnings()

    print("research workflow audit")
    print(f"root: {rel(SKILLS)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"warnings: {len(warnings)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
