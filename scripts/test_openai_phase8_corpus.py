#!/usr/bin/env python3
"""Validate the Phase 8 corpus, bounded repeats, and native-research receipts.

Synthetic oracle/replay fixtures remain separate from current-task live
fresh-subagent and Search evidence. Pending Deep Research receipts are valid
planning records but can never make the phase pass.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Callable

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
FIXTURE_ROOT = REPO / "tests" / "openai_phase8"
CORPUS_PATH = FIXTURE_ROOT / "corpus.yaml"
REPEAT_PATH = FIXTURE_ROOT / "fresh-repeat-runs.yaml"
LIVE_REPEAT_PATH = FIXTURE_ROOT / "live-repeat-receipts.yaml"
RETRIEVAL_SCHEMA_PATH = FIXTURE_ROOT / "retrieval-receipt.schema.yaml"
RETRIEVAL_RECEIPTS_PATH = FIXTURE_ROOT / "retrieval-receipts.yaml"
PROVIDER_VERIFIER_REGISTRY_PATH = FIXTURE_ROOT / "provider-verifier-registry.yaml"
REPORT_PATH = PLUGIN / "reports" / "phase8-corpus-results.json"

WORKFLOWS = {"idea", "proposal", "article", "perspective"}
OUTCOME_CLASSES = {"happy", "fixable", "fatal_or_pending", "revision_no_gain"}
LINEAGE_FIELDS = {
    "complete",
    "artifact_id",
    "version_id",
    "round_id",
    "plugin_version_binding",
    "source_skill",
    "based_on",
    "change_type",
}
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
GIT_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
EVIDENCE_FRESHNESS_DAYS = 90
FUTURE_CLOCK_SKEW = timedelta(minutes=5)
SYNTHETIC_PROVIDER_ADAPTER_ID = "synthetic_ephemeral_validator_override"
SOURCE_IDENTITY_FIELDS = (
    "source_commit",
    "manifest_digest",
    "registry_digest",
    "skill_tree_digest",
)
SOURCE_INPUT_REVIEW_LEAK_PATTERNS = {
    "generic_review_instruction": re.compile(
        r"^\s*#{1,6}\s+(?:requested\s+)?(?:review|assessment|evaluation)\s*$"
        r"|^\s*(?:perform|conduct|assess|evaluate|review|triage|audit|inspect)\b"
        r"[^\n]{0,200}\b(?:return|report|produce)\b"
        r"|^\s*(?:return|report|produce)\b[^\n]{0,200}"
        r"\b(?:route|final[_ -]?state|decision|findings?|scores?|contract)\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "revision_control_material": re.compile(
        r"\b(?:author[_ -]?)?revision[_ -]+(?:brief|plan|delta|instructions?|request)\b"
        r"|\bmust[_ -]?fix[_ -]+(?:brief|list|plan|items?)\b"
        r"|\bchange[_ -]+request\b",
        re.IGNORECASE,
    ),
    "expected_result_oracle": re.compile(
        r"^\s*(?:#{1,6}\s*)?(?:expected|gold|oracle|ground[_ -]?truth)\s+"
        r"(?:result|outcome|route|state|decision|findings?|score|label)\b"
        r"|\b(?:should|must)\s+(?:be\s+)?"
        r"(?:accepted|rejected|blocked|promoted|ready[_ -]for[_ -]signoff)\b"
        r"|\b(?:happy|fixable|fatal[_ -]or[_ -]pending|revision[_ -]no[_ -]gain)\s+"
        r"(?:case|outcome|label)\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "prior_review_role_reference": re.compile(
        r"\b(?:prior|previous|earlier)\s+"
        r"(?:evaluation|evaluator|review|reviewer|panel|audit|auditor)\b",
        re.IGNORECASE,
    ),
    "review_artifact_identifier": re.compile(
        r"\b(?:evaluation|evaluator|review|reviewer|panel|audit|auditor)"
        r"(?:[-_@][a-z0-9.]+)*[-_@](?:r|v)?\d+[a-z0-9._-]*\b",
        re.IGNORECASE,
    ),
    "review_artifact_id_field": re.compile(
        r"\b(?:evaluation|evaluator|review|reviewer|panel|audit|auditor)"
        r"(?:[_ -](?:output|report|artifact))?[_ -]?id\s*[:=]",
        re.IGNORECASE,
    ),
    "review_score_or_decision_field": re.compile(
        r"\b(?:"
        r"(?:prior|previous|earlier)[_ -]*"
        r"(?:(?:evaluation|evaluator|review|reviewer|panel|audit|auditor)[_ -]*)?"
        r"(?:scores?|decisions?)"
        r"|(?:evaluation|evaluator|review|reviewer|panel|audit|auditor)"
        r"[_ -]*(?:scores?|decisions?)"
        r")\s*[:=]",
        re.IGNORECASE,
    ),
    "audit_conclusion": re.compile(
        r"\b(?:methods(?:/statistics)?|methodology|statistics|claim)?\s*"
        r"audit\s*:\s*(?:pass|fail|accept|revise|reject)\b",
        re.IGNORECASE,
    ),
    "review_role_conclusion": re.compile(
        r"\b(?:evaluator|reviewer|auditor)\s+"
        r"(?:requested|recommended|accepted|rejected|concluded|found|decided|scored)\b"
        r"|\bpanel\s+(?:member|decision|finding|conclusion|report|output)\b",
        re.IGNORECASE,
    ),
}
REVIEW_LINEAGE_ROLE_RE = re.compile(
    r"(?:^|[-_@])(?:evaluation|evaluator|review|reviewer|panel|audit|auditor|"
    r"assessment|assessor|triage|expected|oracle|score|decision|finding|rubric)"
    r"(?:$|[-_@])",
    re.IGNORECASE,
)
SOURCE_INPUT_METADATA_FIELDS = {
    "artifact_id",
    "version_id",
    "workflow_id",
    "round_id",
    "plugin_version",
    "source_skill",
    "created_by_instance_id",
    "based_on",
    "change_type",
    "frozen",
    "anonymity",
}
SOURCE_LINEAGE_ALLOWED_KIND_RE = re.compile(
    r"(?:^|[-_@])(?:source|data|dataset|context|blueprint|analysis|evidence|ledger|"
    r"notes?|study|literature|cohort|stakeholder|outlet|call)(?:$|[-_@])",
    re.IGNORECASE,
)
SOURCE_LINEAGE_FORBIDDEN_KIND_RE = re.compile(
    r"(?:^|[-_@])(?:revision|revise|evaluation|evaluator|review|reviewer|panel|"
    r"audit|auditor|assessment|assessor|triage|expected|oracle|score|decision|"
    r"finding|rubric|accept|reject)(?:$|[-_@])",
    re.IGNORECASE,
)
REVIEW_VISIBLE_OUTCOME_ORACLE_TOKENS = {
    "happy",
    "fixable",
    "fatal",
    "pending",
    "nogain",
    "expected",
    "gold",
    "oracle",
    "accept",
    "accepted",
    "reject",
    "rejected",
    "blocked",
    "ready",
}
SKILL_RESOURCE_PATH_MARKER = "research-skills-openai/skills/"

# A real adapter must be implemented in code so a repository-authored YAML
# label cannot make itself trusted. The Preview currently has no such adapter.
BUILTIN_PROVIDER_VERIFIERS: dict[
    str, Callable[[Path, dict[str, Any], dict[str, Any]], bool]
] = {}


class CorpusViolation(AssertionError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise CorpusViolation(code, message)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    require(isinstance(value, dict), "yaml_root", str(path))
    return value


def load_current_version() -> str:
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8-sig"))
    registry = load_yaml(PLUGIN / "workflow-registry.yaml")
    require(manifest.get("version") == registry.get("plugin_version"), "plugin_version_drift", "manifest/registry")
    version = manifest.get("version")
    require(isinstance(version, str) and bool(version), "plugin_version_missing", "manifest")
    return version


def safe_review_path(value: str, allowed_prefixes: list[str], case_id: str) -> bool:
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    require(not path.is_absolute() and ".." not in path.parts, "unsafe_review_path", f"{case_id}: {value}")
    return any(normalized.startswith(prefix) for prefix in allowed_prefixes)


def reviewer_visible_oracle_tokens(value: Any) -> set[str]:
    text = str(value or "").lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    found = set(tokens).intersection(REVIEW_VISIBLE_OUTCOME_ORACLE_TOKENS)
    if any(
        left == "no" and right == "gain"
        for left, right in zip(tokens, tokens[1:])
    ):
        found.add("no-gain")
    return found


def is_reviewer_skill_resource_path(value: Any) -> bool:
    return SKILL_RESOURCE_PATH_MARKER in str(value or "").replace("\\", "/").lower()


def validate_reviewer_visible_identifier(
    value: Any,
    *,
    label: str,
    code: str = "reviewer_visible_outcome_oracle",
) -> None:
    require(
        isinstance(value, str) and bool(value.strip()),
        code,
        f"{label}: missing reviewer-visible identifier",
    )
    leaked = reviewer_visible_oracle_tokens(value)
    require(
        not leaked,
        code,
        f"{label}: outcome-oracle token(s) {sorted(leaked)} in {value}",
    )


def validate_blind_dispatch_prompt_identifiers(
    prompt: dict[str, Any],
    *,
    label: str,
    code: str = "reviewer_visible_outcome_oracle",
) -> None:
    frozen_input = prompt.get("frozen_input", {})
    blind_bundle = prompt.get("blind_bundle", {})
    require(
        isinstance(frozen_input, dict) and isinstance(blind_bundle, dict),
        code,
        f"{label}: prompt input/bundle identifiers",
    )
    visible_values: list[tuple[str, Any]] = [
        ("prompt_contract_id", prompt.get("prompt_contract_id")),
        ("frozen_input.path", frozen_input.get("path")),
        ("blind_bundle.path", blind_bundle.get("path")),
    ]
    for path in prompt.get("declared_resource_closure", []):
        if not is_reviewer_skill_resource_path(path):
            visible_values.append(("declared_resource_closure", path))
    for path in prompt.get("allowed_write_prefixes", []):
        visible_values.append(("allowed_write_prefix", path))
    for field, value in visible_values:
        validate_reviewer_visible_identifier(
            value,
            label=f"{label}: {field}",
            code=code,
        )


def percent(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 2) if denominator else 100.0


def canonical_case_digest(case: dict[str, Any]) -> str:
    payload = json.dumps(case, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_digest(payload: bytes) -> str:
    normalized = payload.replace(b"\r\n", b"\n")
    return "sha256:" + hashlib.sha256(normalized).hexdigest()


def normalized_file_digest(path: Path) -> str:
    return normalized_digest(path.read_bytes())


def git_bytes(*args: str) -> bytes:
    process = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        process.returncode == 0,
        "phase8_source_identity",
        process.stderr.decode("utf-8", errors="replace").strip() or "git command failed",
    )
    return process.stdout


def skill_tree_digest_from_items(items: list[tuple[str, bytes]]) -> str:
    tree = [
        {
            "path": relative.replace("\\", "/"),
            "digest": normalized_digest(payload),
        }
        for relative, payload in sorted(items)
    ]
    payload = json.dumps(
        tree, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


@lru_cache(maxsize=1)
def current_contract_identity() -> dict[str, str]:
    source_commit = git_bytes("rev-parse", "HEAD").decode("ascii").strip()
    require(
        GIT_COMMIT_RE.fullmatch(source_commit) is not None,
        "phase8_source_identity",
        "HEAD is not an immutable commit ID",
    )
    skill_items = [
        (path.relative_to(PLUGIN / "skills").as_posix(), path.read_bytes())
        for path in (PLUGIN / "skills").rglob("*")
        if path.is_file()
    ]
    return {
        "source_commit": source_commit,
        "manifest_digest": normalized_file_digest(
            PLUGIN / ".codex-plugin" / "plugin.json"
        ),
        "registry_digest": normalized_file_digest(PLUGIN / "workflow-registry.yaml"),
        "skill_tree_digest": skill_tree_digest_from_items(skill_items),
    }


@lru_cache(maxsize=4)
def committed_contract_identity(source_commit: str) -> dict[str, str]:
    require(
        GIT_COMMIT_RE.fullmatch(source_commit) is not None,
        "phase8_source_identity",
        "source commit is not a full immutable SHA",
    )
    manifest_path = "research-skills-openai/.codex-plugin/plugin.json"
    registry_path = "research-skills-openai/workflow-registry.yaml"
    skill_prefix = "research-skills-openai/skills/"
    paths = [
        line.strip()
        for line in git_bytes(
            "ls-tree",
            "-r",
            "--name-only",
            source_commit,
            "--",
            "research-skills-openai/skills",
        )
        .decode("utf-8")
        .splitlines()
        if line.strip()
    ]
    skill_items = [
        (path.removeprefix(skill_prefix), git_bytes("show", f"{source_commit}:{path}"))
        for path in paths
    ]
    return {
        "source_commit": source_commit,
        "manifest_digest": normalized_digest(
            git_bytes("show", f"{source_commit}:{manifest_path}")
        ),
        "registry_digest": normalized_digest(
            git_bytes("show", f"{source_commit}:{registry_path}")
        ),
        "skill_tree_digest": skill_tree_digest_from_items(skill_items),
    }


def validate_source_identity(
    subject: dict[str, Any],
    *,
    label: str,
    synthetic_override: bool,
) -> dict[str, str]:
    expected = current_contract_identity()
    for field in SOURCE_IDENTITY_FIELDS:
        require(
            subject.get(field) == expected[field],
            "phase8_source_identity",
            f"{label}: {field} does not bind the current plugin tree",
        )
    if not synthetic_override:
        committed = committed_contract_identity(str(subject.get("source_commit", "")))
        require(
            committed == expected,
            "phase8_source_identity",
            f"{label}: source commit does not contain the current plugin identity",
        )
    return expected


@lru_cache(maxsize=1)
def provider_verifier_registry() -> dict[str, Any]:
    registry = load_yaml(PROVIDER_VERIFIER_REGISTRY_PATH)
    require(
        registry.get("schema_version") == 1,
        "provider_verifier_registry",
        "schema_version",
    )
    policy = registry.get("policy", {})
    require(
        policy.get("repository_authored_files_are_not_trust_anchors") is True
        and policy.get("real_verification_requires_builtin_adapter") is True
        and policy.get("synthetic_override_counts_as_runtime_evidence") is False,
        "provider_verifier_registry",
        "trust policy",
    )
    synthetic = registry.get("synthetic_self_test", {})
    require(
        synthetic.get("adapter_id") == SYNTHETIC_PROVIDER_ADAPTER_ID
        and synthetic.get("ephemeral_temp_root_required") is True,
        "provider_verifier_registry",
        "synthetic override policy",
    )
    adapters = registry.get("adapters", [])
    require(isinstance(adapters, list), "provider_verifier_registry", "adapters")
    ids = [item.get("adapter_id") for item in adapters if isinstance(item, dict)]
    require(
        len(ids) == len(adapters) == len(set(ids)) and all(ids),
        "provider_verifier_registry",
        "adapter IDs",
    )
    return registry


def real_provider_adapter_ids() -> set[str]:
    registry = provider_verifier_registry()
    configured = {
        str(item["adapter_id"])
        for item in registry.get("adapters", [])
        if isinstance(item, dict) and item.get("enabled") is True
    }
    return configured.intersection(BUILTIN_PROVIDER_VERIFIERS)


def validate_provider_trust_anchor(
    subject: dict[str, Any],
    platform_export: dict[str, Any],
    export_path: Path,
    *,
    root: Path,
    synthetic_override: bool,
) -> None:
    provider_verifier_registry()
    adapter_id = subject.get("provider_verifier_adapter")
    require(
        platform_export.get("provider_verifier_adapter") == adapter_id,
        "provider_trust_anchor",
        "platform export adapter mismatch",
    )
    if synthetic_override:
        try:
            inside_repository = root.resolve().is_relative_to(REPO.resolve())
        except ValueError:
            inside_repository = False
        require(
            adapter_id == SYNTHETIC_PROVIDER_ADAPTER_ID
            and platform_export.get("synthetic_test_only") is True
            and not inside_repository,
            "provider_trust_anchor",
            "synthetic override is limited to an ephemeral validator temp root",
        )
        return

    require(
        isinstance(adapter_id, str) and adapter_id in real_provider_adapter_ids(),
        "provider_trust_anchor_unavailable",
        "no executable provider verifier adapter can authenticate this export",
    )
    verifier = BUILTIN_PROVIDER_VERIFIERS[adapter_id]
    require(
        verifier(export_path, platform_export, subject) is True,
        "provider_trust_anchor",
        f"provider adapter {adapter_id} rejected the export",
    )


def bound_file(
    path_value: Any,
    digest_value: Any,
    *,
    root: Path,
    code: str,
    label: str,
) -> Path:
    normalized = str(path_value or "").replace("\\", "/")
    relative = PurePosixPath(normalized)
    require(
        bool(normalized) and not relative.is_absolute() and ".." not in relative.parts,
        code,
        f"{label}: unsafe or missing path",
    )
    path = root / normalized
    require(path.is_file(), code, f"{label}: missing {normalized}")
    require(
        SHA256_RE.fullmatch(str(digest_value or "")) is not None,
        code,
        f"{label}: invalid digest",
    )
    require(file_digest(path) == digest_value, code, f"{label}: digest mismatch")
    return path


def bound_mapping(
    path_value: Any,
    digest_value: Any,
    *,
    root: Path,
    code: str,
    label: str,
) -> dict[str, Any]:
    path = bound_file(
        path_value,
        digest_value,
        root=root,
        code=code,
        label=label,
    )
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    require(isinstance(value, dict), code, f"{label}: export root is not a mapping")
    return value


def write_temp_mapping(root: Path, relative: str, value: dict[str, Any]) -> tuple[str, str]:
    """Create deterministic ephemeral evidence used only by validator self-tests."""
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )
    return relative, file_digest(path)


def write_temp_text(root: Path, relative: str, value: str) -> tuple[str, str]:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")
    return relative, file_digest(path)


def validate_corpus(current_version: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    corpus = load_yaml(CORPUS_PATH)
    require(corpus.get("schema_version") == 1, "corpus_schema", "schema_version")
    require(corpus.get("evidence_class") == "synthetic_contract_oracle", "corpus_evidence_class", "fixture")
    require(corpus.get("runtime_claim") == "none", "corpus_runtime_claim", "fixture must not claim live execution")
    require(set(corpus.get("outcome_classes", [])) == OUTCOME_CLASSES, "outcome_classes", "coverage declaration")
    policy = corpus.get("anonymization_policy", {})
    required_statement = policy.get("required_statement")
    require(policy.get("identifying_source_material_committed") is False, "anonymity", "policy")
    require(policy.get("permitted_source_kinds") == ["synthetic"], "anonymity", "source kinds")

    cases = corpus.get("cases", [])
    require(isinstance(cases, list) and len(cases) >= 16, "corpus_size", str(len(cases)))
    ids = [case.get("case_id") for case in cases]
    require(all(isinstance(case_id, str) and case_id for case_id in ids), "case_id", "missing")
    require(len(ids) == len(set(ids)), "case_id", "duplicate")
    by_id = {case["case_id"]: case for case in cases}

    coverage: Counter[tuple[str, str]] = Counter()
    fatal_total = 0
    fatal_detected = 0
    fatal_or_blocking_total = 0
    fatal_or_blocking_detected = 0
    major_total = 0
    major_detected = 0
    false_ready = 0
    lineage_ok = 0
    isolation_ok = 0
    edit_boundary_ok = 0
    dissent_expected = 0
    dissent_preserved = 0
    case_summaries: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["case_id"]
        workflow = case.get("workflow")
        outcome = case.get("outcome_class")
        require(workflow in WORKFLOWS, "workflow", case_id)
        require(outcome in OUTCOME_CLASSES, "outcome_class", case_id)
        require(case.get("risk_tier") in {"low", "medium", "high"}, "risk_tier", case_id)
        require(isinstance(case.get("scenario"), str) and case["scenario"].strip(), "scenario", case_id)
        coverage[(workflow, outcome)] += 1

        anonymity = case.get("anonymity", {})
        require(anonymity.get("source_kind") == "synthetic", "anonymity", case_id)
        require(anonymity.get("contains_identifying_material") is False, "anonymity", case_id)
        require(anonymity.get("statement") == required_statement, "anonymity_statement", case_id)

        expected = case.get("expected", {})
        missing_expected = {
            "route",
            "final_state",
            "required_outputs",
            "forbidden_outputs",
            "critical_findings",
            "dissent_ids",
        } - set(expected)
        require(not missing_expected, "expected_contract", f"{case_id}: {sorted(missing_expected)}")
        required_outputs = set(expected["required_outputs"])
        forbidden_outputs = set(expected["forbidden_outputs"])
        require(required_outputs and not required_outputs.intersection(forbidden_outputs), "output_contract", case_id)

        observation = case.get("oracle_observation", {})
        require(observation.get("route") == expected["route"], "route_disagreement", case_id)
        require(observation.get("final_state") == expected["final_state"], "state_disagreement", case_id)
        observed_outputs = set(observation.get("outputs", []))
        require(required_outputs <= observed_outputs, "required_output_missing", case_id)
        require(not forbidden_outputs.intersection(observed_outputs), "forbidden_output", case_id)

        ready_claimed = observation.get("ready_claimed") is True
        false_ready_case = ready_claimed and expected["final_state"] != "human_signoff_required"
        false_ready_case = false_ready_case or (
            observation.get("final_state") == "human_signoff_required"
            and expected["final_state"] != "human_signoff_required"
        )
        false_ready += int(false_ready_case)
        if expected["final_state"] == "human_signoff_required":
            require(ready_claimed, "missing_ready_claim", case_id)

        critical = expected["critical_findings"]
        require(isinstance(critical, list), "critical_findings", case_id)
        finding_ids = [finding.get("finding_id") for finding in critical]
        require(len(finding_ids) == len(set(finding_ids)), "finding_id", case_id)
        detected = set(observation.get("detected_finding_ids", []))
        for finding in critical:
            require(
                set(finding) >= {"finding_id", "severity", "blocking"},
                "finding_contract",
                case_id,
            )
            finding_id = finding["finding_id"]
            if finding["severity"] == "fatal":
                fatal_total += 1
                fatal_detected += int(finding_id in detected)
            is_fatal_or_blocking = finding["severity"] in {"fatal", "blocking"} or finding["blocking"] is True
            if is_fatal_or_blocking:
                fatal_or_blocking_total += 1
                fatal_or_blocking_detected += int(finding_id in detected)
            if finding["severity"] == "major":
                major_total += 1
                major_detected += int(finding_id in detected)
        if outcome in {"fixable", "fatal_or_pending", "revision_no_gain"}:
            require(bool(critical), "critical_findings", f"{case_id}: outcome requires labeled finding")
        if outcome == "happy":
            require(not critical, "critical_findings", f"{case_id}: happy fixture")

        lineage = observation.get("lineage", {})
        lineage_case_ok = (
            set(lineage) >= LINEAGE_FIELDS
            and lineage.get("complete") is True
            and lineage.get("plugin_version_binding") == "manifest_current"
            and bool(lineage.get("artifact_id"))
            and bool(lineage.get("version_id"))
            and bool(lineage.get("round_id"))
            and bool(lineage.get("source_skill"))
            and bool(lineage.get("based_on"))
            and bool(lineage.get("change_type"))
        )
        require(lineage_case_ok, "lineage", case_id)
        lineage_ok += 1

        isolation = observation.get("isolation", {})
        isolation_case_ok = (
            isolation.get("fresh_subagent") is True
            and isolation.get("prior_scores_visible") is False
            and bool(isolation.get("writer_instance_id"))
            and bool(isolation.get("reviewer_instance_id"))
            and isolation.get("writer_instance_id") != isolation.get("reviewer_instance_id")
        )
        require(isolation_case_ok, "reviewer_isolation", case_id)
        isolation_ok += 1

        boundary = observation.get("edit_boundary", {})
        allowed_prefixes = boundary.get("allowed_prefixes", [])
        writes = boundary.get("reviewer_write_paths", [])
        boundary_case_ok = (
            boundary.get("source_edits_performed_by_reviewer") is False
            and bool(allowed_prefixes)
            and bool(writes)
            and all(safe_review_path(path, allowed_prefixes, case_id) for path in writes)
        )
        require(boundary_case_ok, "reviewer_edit_boundary", case_id)
        edit_boundary_ok += 1

        expected_dissent = set(expected["dissent_ids"])
        observed_dissent = set(observation.get("preserved_dissent_ids", []))
        require(expected_dissent <= observed_dissent, "dissent_hidden", case_id)
        dissent_expected += len(expected_dissent)
        dissent_preserved += len(expected_dissent.intersection(observed_dissent))

        case_summaries.append(
            {
                "case_id": case_id,
                "workflow": workflow,
                "outcome_class": outcome,
                "risk_tier": case["risk_tier"],
                "expected_state": expected["final_state"],
                "critical_findings": len(critical),
                "fixture_contract": "passed",
            }
        )

    require(
        set(coverage) == {(workflow, outcome) for workflow in WORKFLOWS for outcome in OUTCOME_CLASSES},
        "corpus_coverage",
        str(sorted(coverage)),
    )
    require(all(count >= 1 for count in coverage.values()), "corpus_coverage", str(coverage))
    fatal_recall = percent(fatal_detected, fatal_total)
    fatal_or_blocking_recall = percent(fatal_or_blocking_detected, fatal_or_blocking_total)
    major_recall = percent(major_detected, major_total)
    lineage_rate = percent(lineage_ok, len(cases))
    isolation_rate = percent(isolation_ok, len(cases))
    boundary_rate = percent(edit_boundary_ok, len(cases))
    dissent_rate = percent(dissent_preserved, dissent_expected)
    require(fatal_recall == 100.0, "fatal_recall", str(fatal_recall))
    require(fatal_or_blocking_recall == 100.0, "fatal_or_blocking_recall", str(fatal_or_blocking_recall))
    require(major_recall >= 90.0, "major_recall", str(major_recall))
    require(false_ready == 0, "false_ready", str(false_ready))
    require(lineage_rate == 100.0, "lineage_rate", str(lineage_rate))
    require(isolation_rate == 100.0, "isolation_rate", str(isolation_rate))
    require(boundary_rate == 100.0, "edit_boundary_rate", str(boundary_rate))
    require(dissent_rate == 100.0, "dissent_rate", str(dissent_rate))

    summary = {
        "evidence_class": corpus["evidence_class"],
        "runtime_claim": corpus["runtime_claim"],
        "plugin_version_binding": current_version,
        "case_count": len(cases),
        "coverage": {
            workflow: {outcome: coverage[(workflow, outcome)] for outcome in sorted(OUTCOME_CLASSES)}
            for workflow in sorted(WORKFLOWS)
        },
        "metrics": {
            "false_ready_count": false_ready,
            "fatal_finding_recall_percent": fatal_recall,
            "fatal_or_blocking_finding_recall_percent": fatal_or_blocking_recall,
            "major_finding_recall_percent": major_recall,
            "lineage_compliance_percent": lineage_rate,
            "reviewer_isolation_compliance_percent": isolation_rate,
            "reviewer_edit_boundary_compliance_percent": boundary_rate,
            "dissent_preservation_percent": dissent_rate,
        },
        "case_results": case_summaries,
        "status": "synthetic_contract_oracle_passed",
    }
    return summary, by_id


def validate_repeat_selection(policy: dict[str, Any], selection: dict[str, Any]) -> None:
    default_count = policy.get("default_case_count")
    max_count = policy.get("max_automatic_case_count")
    count = selection.get("automatic_case_count")
    ids = selection.get("selected_case_ids", [])
    require(default_count == 3, "repeat_default_budget", str(default_count))
    require(max_count == 5, "repeat_max_budget", str(max_count))
    require(policy.get("explicit_owner_decision_required_above") == 5, "repeat_owner_gate", "threshold")
    require(count == len(ids) == len(set(ids)), "repeat_selection_count", str(count))
    require(count <= max_count, "repeat_budget_exceeded", str(count))
    reasons = selection.get("expansion_reasons", [])
    allowed_reasons = set(policy.get("expansion_triggers", []))
    if selection.get("expansion_triggered"):
        require(default_count < count <= max_count, "repeat_expansion_size", str(count))
        require(bool(reasons) and set(reasons) <= allowed_reasons, "repeat_expansion_reason", str(reasons))
    else:
        require(count == default_count, "repeat_expansion_without_trigger", str(count))
        require(reasons == [], "repeat_expansion_reason", str(reasons))


def validate_repeat_budget_negative_guards(
    policy: dict[str, Any], selection: dict[str, Any], all_case_ids: list[str]
) -> list[dict[str, str]]:
    probes: list[tuple[str, dict[str, Any], str]] = []
    over_budget = copy.deepcopy(selection)
    over_budget.update(
        selected_case_ids=all_case_ids[:6],
        automatic_case_count=6,
        expansion_triggered=True,
        expansion_reasons=["route_or_state_disagreement"],
    )
    probes.append(("automatic-six-rejected", over_budget, "repeat_budget_exceeded"))

    untriggered_four = copy.deepcopy(selection)
    untriggered_four.update(selected_case_ids=all_case_ids[:4], automatic_case_count=4)
    probes.append(("untriggered-four-rejected", untriggered_four, "repeat_expansion_without_trigger"))

    invalid_reason = copy.deepcopy(selection)
    invalid_reason.update(
        selected_case_ids=all_case_ids[:4],
        automatic_case_count=4,
        expansion_triggered=True,
        expansion_reasons=["more_confidence_requested"],
    )
    probes.append(("unsupported-trigger-rejected", invalid_reason, "repeat_expansion_reason"))

    results: list[dict[str, str]] = []
    for probe_id, candidate, expected_code in probes:
        try:
            validate_repeat_selection(policy, candidate)
        except CorpusViolation as exc:
            require(exc.code == expected_code, "repeat_guard_wrong_error", f"{probe_id}: {exc.code}")
            results.append({"probe_id": probe_id, "status": "rejected", "error_code": exc.code})
        else:
            raise CorpusViolation("repeat_guard_accepted", probe_id)
    return results


def validate_fresh_repeats(cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    data = load_yaml(REPEAT_PATH)
    require(data.get("schema_version") == 1, "repeat_schema", "schema_version")
    require(data.get("evidence_class") == "synthetic_contract_replay", "repeat_evidence_class", "fixture")
    require(data.get("runtime_claim") == "none", "repeat_runtime_claim", "must not claim model execution")
    policy = data.get("policy", {})
    selection = data.get("selection", {})
    require(set(policy.get("expansion_triggers", [])) == {"route_or_state_disagreement", "missed_critical_finding"}, "repeat_expansion_trigger", "policy")
    validate_repeat_selection(policy, selection)

    selected = selection["selected_case_ids"]
    require(all(case_id in cases for case_id in selected), "repeat_unknown_case", str(selected))
    selected_risks = [cases[case_id]["risk_tier"] for case_id in selected]
    require(selection.get("mode") == "default_risk_stratified", "repeat_selection_mode", "default")
    require(selected_risks == selection.get("risk_tiers"), "repeat_risk_binding", str(selected_risks))
    require(set(selected_risks) == {"high", "medium", "low"}, "repeat_risk_stratification", str(selected_risks))

    repeats = data.get("repeats", [])
    require({repeat.get("case_id") for repeat in repeats} == set(selected), "repeat_case_binding", "selection")
    require(len(repeats) == len(selected), "repeat_case_count", str(len(repeats)))
    run_ids: set[str] = set()
    evaluator_ids: set[str] = set()
    disagreements: list[str] = []
    missed_findings: list[str] = []
    run_count = 0
    for repeat in repeats:
        case_id = repeat["case_id"]
        case = cases[case_id]
        expected = case["expected"]
        critical_ids = {finding["finding_id"] for finding in expected["critical_findings"]}
        expected_dissent = set(expected["dissent_ids"])
        source_digest = str(repeat.get("source_artifact_digest", ""))
        require(SHA256_RE.fullmatch(source_digest) is not None, "repeat_digest", case_id)
        require(source_digest == canonical_case_digest(case), "repeat_case_digest_mismatch", case_id)
        runs = repeat.get("runs", [])
        require(len(runs) >= 2, "repeat_fresh_run_count", case_id)
        observed_contracts: set[tuple[str, str]] = set()
        for run in runs:
            run_count += 1
            run_id = run.get("run_id")
            evaluator_id = run.get("evaluator_instance_id")
            require(run_id not in run_ids and bool(run_id), "repeat_run_id", str(run_id))
            require(evaluator_id not in evaluator_ids and bool(evaluator_id), "repeat_evaluator_reuse", str(evaluator_id))
            run_ids.add(run_id)
            evaluator_ids.add(evaluator_id)
            oracle_isolation = case["oracle_observation"]["isolation"]
            require(evaluator_id not in {oracle_isolation["writer_instance_id"], oracle_isolation["reviewer_instance_id"]}, "repeat_evaluator_not_fresh", str(evaluator_id))
            require(run.get("isolation_mode") == "fresh_subagent", "repeat_isolation", str(run_id))
            require(run.get("prior_scores_visible") is False, "repeat_prior_scores", str(run_id))
            require(run.get("source_edits_performed") is False, "repeat_source_edit", str(run_id))
            write_paths = run.get("reviewer_write_paths", [])
            require(bool(write_paths), "repeat_write_scope", str(run_id))
            require(all(safe_review_path(path, ["reviews/"], case_id) for path in write_paths), "repeat_write_scope", str(run_id))
            contract = (run.get("route"), run.get("final_state"))
            observed_contracts.add(contract)
            if contract != (expected["route"], expected["final_state"]):
                disagreements.append(run_id)
            detected = set(run.get("detected_finding_ids", []))
            if not critical_ids <= detected:
                missed_findings.append(run_id)
            require(expected_dissent <= set(run.get("preserved_dissent_ids", [])), "repeat_dissent", str(run_id))
        if len(observed_contracts) != 1:
            disagreements.append(case_id)

    required_triggers = set()
    if disagreements:
        required_triggers.add("route_or_state_disagreement")
    if missed_findings:
        required_triggers.add("missed_critical_finding")
    if selection.get("expansion_triggered"):
        require(required_triggers, "repeat_unnecessary_expansion", "no disagreement or missed critical finding")
        require(set(selection.get("expansion_reasons", [])) <= required_triggers, "repeat_expansion_evidence", str(required_triggers))
    else:
        require(not required_triggers, "repeat_expansion_required", str(sorted(required_triggers)))
    require(not disagreements, "repeat_contract_disagreement", str(disagreements))
    require(not missed_findings, "repeat_critical_finding_missed", str(missed_findings))

    guards = validate_repeat_budget_negative_guards(policy, selection, list(cases))
    return {
        "evidence_class": data["evidence_class"],
        "runtime_claim": data["runtime_claim"],
        "default_case_count": policy["default_case_count"],
        "maximum_automatic_case_count": policy["max_automatic_case_count"],
        "selected_case_count": len(selected),
        "fresh_run_count": run_count,
        "selected_case_ids": selected,
        "risk_tiers": selected_risks,
        "expansion_triggered": selection["expansion_triggered"],
        "route_or_state_disagreements": len(disagreements),
        "missed_critical_findings": len(missed_findings),
        "budget_negative_guards": guards,
        "synthetic_contract_status": "passed",
        "live_repeat_receipts_completed": 0,
        "live_repeat_gate_status": "pending_live_evidence",
        "status": "synthetic_repeat_contract_passed_live_repeat_pending",
    }


def infer_live_review_stage(raw: dict[str, Any]) -> str | None:
    reviewer = raw.get("reviewer_skill")
    decision = raw.get("decision")
    route = str(raw.get("route", ""))
    state = str(raw.get("final_state", ""))
    findings = raw.get("findings", [])
    fatal_blocking = any(
        finding.get("severity") == "fatal" and finding.get("blocking") is True
        for finding in findings
        if isinstance(finding, dict)
    )
    if (
        reviewer == "proposal-readiness-triage"
        and decision == "not_proposalizable_yet"
        and route == "stop"
        and fatal_blocking
    ):
        return "blocked"
    if (
        reviewer == "article-evaluator"
        and decision == "revise"
        and route == "article-refinement-controller"
        and state == "revision_required"
    ):
        return "revision_required"
    if (
        reviewer == "perspective-evaluator"
        and decision == "accept"
        and "panel" in route
        and state in {"pre_panel_eligible", "pre_panel_ready"}
    ):
        return "pre_panel_eligible"
    return None


def live_label_supported(label: str, raw: dict[str, Any]) -> bool:
    finding_text = " ".join(
        str(finding.get("summary", ""))
        for finding in raw.get("findings", [])
        if isinstance(finding, dict)
    ).lower()
    unresolved_text = " ".join(str(item) for item in raw.get("unresolved_issues", [])).lower()
    combined = f"{finding_text} {unresolved_text}"
    if label == "data_access_impossible":
        access_term = any(term in combined for term in ("inaccessible", "unobtainable", "no accessible", "no credible data"))
        alternative_term = any(term in combined for term in ("no approval route", "no substitute", "all stated alternatives excluded", "no remaining"))
        return access_term and alternative_term
    if label == "prespecified_sensitivity_result_omitted":
        return "sensitivity" in combined and any(term in combined for term in ("omit", "does not report"))
    if label == "annual_reassessment_frequency":
        dissent_text = " ".join(str(item) for item in raw.get("dissent_ids", [])).lower()
        return "annual" in combined and "reassess" in combined and bool(dissent_text)
    return False


def nested_string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for value_item in value for item in nested_string_values(value_item)]
    if isinstance(value, dict):
        return [
            item
            for key, value_item in value.items()
            for item in (nested_string_values(key) + nested_string_values(value_item))
        ]
    return []


def validate_source_only_input_artifact(
    input_path: str,
    input_digest: str,
    *,
    root: Path,
    label: str,
) -> None:
    validate_reviewer_visible_identifier(
        input_path,
        label=f"{label}: source input path",
    )
    path = bound_file(
        input_path,
        input_digest,
        root=root,
        code="live_repeat_source_input_review_leak",
        label=f"{label}: source input",
    )
    text = path.read_text(encoding="utf-8-sig")
    leaks = {
        leak_kind
        for leak_kind, pattern in SOURCE_INPUT_REVIEW_LEAK_PATTERNS.items()
        if pattern.search(text)
    }
    metadata_matches = list(re.finditer(
        r"```ya?ml\s*\r?\n(.*?)\r?\n```",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    ))
    if len(metadata_matches) != 1:
        leaks.add("embedded_metadata_block_count")
        metadata: dict[str, Any] = {}
    else:
        try:
            loaded_metadata = yaml.safe_load(metadata_matches[0].group(1))
        except yaml.YAMLError as exc:
            raise CorpusViolation(
                "live_repeat_source_input_review_leak",
                f"{label}: source lineage metadata is invalid YAML",
            ) from exc
        if not isinstance(loaded_metadata, dict):
            leaks.add("embedded_metadata_not_mapping")
            metadata = {}
        else:
            metadata = loaded_metadata

    if set(metadata) != SOURCE_INPUT_METADATA_FIELDS:
        leaks.add("embedded_metadata_fields_not_allowlisted")
    required_strings = SOURCE_INPUT_METADATA_FIELDS - {"based_on", "frozen"}
    if any(
        not isinstance(metadata.get(field), str)
        or not str(metadata.get(field, "")).strip()
        for field in required_strings
    ):
        leaks.add("embedded_metadata_identity_invalid")
    if metadata.get("frozen") is not True:
        leaks.add("embedded_metadata_not_frozen")
    for field in ("artifact_id", "workflow_id", "created_by_instance_id"):
        try:
            validate_reviewer_visible_identifier(
                metadata.get(field),
                label=f"{label}: embedded {field}",
            )
        except CorpusViolation as exc:
            if exc.code != "reviewer_visible_outcome_oracle":
                raise
            leaks.add(f"outcome_oracle_in_{field}")

    based_on = metadata.get("based_on")
    if not isinstance(based_on, list) or any(
        not isinstance(ref, str) or not ref.strip() for ref in based_on
    ):
        leaks.add("source_lineage_not_string_list")
        source_refs: list[str] = []
    else:
        source_refs = based_on
    for ref in source_refs:
        try:
            validate_reviewer_visible_identifier(
                ref,
                label=f"{label}: based_on",
            )
        except CorpusViolation as exc:
            if exc.code != "reviewer_visible_outcome_oracle":
                raise
            leaks.add("outcome_oracle_in_source_lineage")
        if SOURCE_LINEAGE_FORBIDDEN_KIND_RE.search(ref):
            leaks.add("review_or_oracle_artifact_in_source_lineage")
        if SOURCE_LINEAGE_ALLOWED_KIND_RE.search(ref) is None:
            leaks.add("non_source_artifact_in_source_lineage")

    lineage_values = nested_string_values(
        {
            "based_on": source_refs,
            "source_skill": metadata.get("source_skill"),
            "created_by_instance_id": metadata.get("created_by_instance_id"),
        }
    )
    if any(REVIEW_LINEAGE_ROLE_RE.search(value) for value in lineage_values):
        leaks.add("review_role_or_artifact_in_lineage")
    require(
        not leaks,
        "live_repeat_source_input_review_leak",
        f"{label}: {sorted(leaks)}",
    )


def validate_source_only_blind_bundle(
    bundle: dict[str, Any],
    *,
    bundle_path: str,
    input_path: str,
    input_digest: str,
    reviewer_skill: str,
    root: Path,
    code: str,
    label: str,
) -> set[str]:
    validate_reviewer_visible_identifier(
        bundle_path,
        label=f"{label}: blind bundle path",
        code=code,
    )
    validate_reviewer_visible_identifier(
        input_path,
        label=f"{label}: frozen input path",
        code=code,
    )
    validate_source_only_input_artifact(
        input_path,
        input_digest,
        root=root,
        label=label,
    )
    require(
        set(bundle)
        == {
            "schema_version",
            "artifact_type",
            "bundle_id",
            "source_artifacts",
            "reviewer_resources",
            "review_context",
            "lineage",
        },
        code,
        f"{label}: blind bundle contains undeclared or missing fields",
    )
    require(
        bundle.get("schema_version") == 1
        and bundle.get("artifact_type") == "source_only_sanitized_blind_bundle"
        and isinstance(bundle.get("bundle_id"), str)
        and bool(bundle["bundle_id"].strip()),
        code,
        f"{label}: blind bundle identity",
    )
    validate_reviewer_visible_identifier(
        bundle.get("bundle_id"),
        label=f"{label}: blind bundle ID",
        code=code,
    )
    require(
        bundle.get("source_artifacts")
        == [
            {
                "artifact_role": "frozen_source_input",
                "path": input_path,
                "sha256": input_digest,
            }
        ],
        code,
        f"{label}: blind bundle is not source-only",
    )
    require(
        bundle.get("review_context")
        == {
            "prior_reviewer_outputs": [],
            "prior_evaluator_outputs": [],
            "prior_scores": [],
            "prior_decisions": [],
            "expected_findings": [],
            "expected_decision": None,
        }
        and bundle.get("lineage")
        == {
            "based_on_source_artifact_digests": [input_digest],
            "based_on_review_artifact_refs": [],
        },
        code,
        f"{label}: prior review/evaluator context leaked into blind bundle",
    )
    reviewer_resources = bundle.get("reviewer_resources")
    require(
        isinstance(reviewer_resources, list),
        code,
        f"{label}: reviewer resource closure",
    )
    allowed_reads = {bundle_path, input_path}
    seen_resources: set[str] = set()
    expected_prefix = f"research-skills-openai/skills/{reviewer_skill}/"
    for resource in reviewer_resources:
        require(
            isinstance(resource, dict)
            and set(resource) == {"path", "sha256"},
            code,
            f"{label}: reviewer resource entry",
        )
        resource_path = str(resource.get("path", "")).replace("\\", "/")
        require(
            resource_path.startswith(expected_prefix)
            and resource_path not in seen_resources
            and (root / resource_path).is_file()
            and resource.get("sha256") == file_digest(root / resource_path),
            code,
            f"{label}: unbound or out-of-scope reviewer resource {resource_path}",
        )
        seen_resources.add(resource_path)
        allowed_reads.add(resource_path)
    return allowed_reads


def validate_durable_live_repeat_bindings(
    data: dict[str, Any],
    current_version: str,
    *,
    root: Path = REPO,
    synthetic_override: bool = False,
) -> None:
    code = "live_repeat_durable_binding"
    validate_reviewer_visible_identifier(
        data.get("task_id"),
        label="live repeat task ID",
        code="reviewer_visible_outcome_oracle",
    )
    require(
        isinstance(data.get("platform_task_or_delegation_export_path"), str)
        and bool(data["platform_task_or_delegation_export_path"].strip()),
        code,
        "task/delegation export path is missing",
    )
    validate_reviewer_visible_identifier(
        data.get("platform_task_or_delegation_export_path"),
        label="live repeat platform export path",
        code="reviewer_visible_outcome_oracle",
    )
    export_path = bound_file(
        data.get("platform_task_or_delegation_export_path"),
        data.get("platform_task_or_delegation_export_digest"),
        root=root,
        code=code,
        label="task/delegation export",
    )
    export = yaml.safe_load(export_path.read_text(encoding="utf-8-sig"))
    require(isinstance(export, dict), code, "task/delegation export root")
    export_id = data.get("platform_task_or_delegation_export_id")
    require(bool(export_id), code, "platform export ID is missing")
    validate_reviewer_visible_identifier(
        export_id,
        label="live repeat platform export ID",
        code="reviewer_visible_outcome_oracle",
    )
    require(export.get("schema_version") == 1, code, "platform export schema")
    require(export.get("export_id") == export_id, code, "platform export ID mismatch")
    require(export.get("provider_surface") in {"codex", "chatgpt"}, code, "provider surface")
    require(export.get("task_id") == data.get("task_id"), code, "task ID mismatch")
    require(export.get("plugin_version") == current_version, code, "plugin version mismatch")
    for field in SOURCE_IDENTITY_FIELDS:
        require(
            export.get(field) == data.get(field),
            "phase8_source_identity",
            f"live repeat platform export: {field}",
        )
    validate_provider_trust_anchor(
        data,
        export,
        export_path,
        root=root,
        synthetic_override=synthetic_override,
    )
    validate_source_identity(
        data,
        label="live repeat receipt collection",
        synthetic_override=synthetic_override,
    )
    data_capture = parse_timestamp(data.get("captured_at"), "live-repeat-capture")
    require(
        parse_timestamp(export.get("captured_at"), "live-repeat-platform-export")
        == data_capture,
        code,
        "capture timestamp mismatch",
    )
    export_runs = export.get("runs", [])
    require(isinstance(export_runs, list) and bool(export_runs), code, "platform run list")
    export_by_id = {
        item.get("run_id"): item for item in export_runs if isinstance(item, dict)
    }
    declared_runs = [
        run
        for case in data.get("cases", [])
        if isinstance(case, dict)
        for run in case.get("runs", [])
        if isinstance(run, dict)
    ]
    declared_ids = [run.get("run_id") for run in declared_runs]
    require(
        len(export_by_id) == len(export_runs) == len(declared_ids)
        and set(export_by_id) == set(declared_ids),
        code,
        "platform export run coverage mismatch",
    )
    delegated_thread_ids: set[str] = set()
    for case in data.get("cases", []):
        validate_reviewer_visible_identifier(
            case.get("case_id"),
            label="live repeat case ID",
            code="reviewer_visible_outcome_oracle",
        )
        reviewer_skill = str(case.get("reviewer_skill", ""))
        input_path = str(case.get("input_path", "")).replace("\\", "/")
        validate_reviewer_visible_identifier(
            input_path,
            label=f"{case.get('case_id')}: input path",
            code="reviewer_visible_outcome_oracle",
        )
        input_digest = case.get("input_digest")
        require(
            SHA256_RE.fullmatch(str(input_digest or "")) is not None,
            code,
            f"{case.get('case_id')}: input digest",
        )
        for run in case.get("runs", []):
            run_id = str(run.get("run_id", ""))
            validate_reviewer_visible_identifier(
                run_id,
                label=f"{case.get('case_id')}: run ID",
                code="reviewer_visible_outcome_oracle",
            )
            platform_receipt_id = run.get("platform_receipt_id")
            require(bool(platform_receipt_id), code, f"{run_id}: platform receipt ID")
            validate_reviewer_visible_identifier(
                platform_receipt_id,
                label=f"{run_id}: platform receipt ID",
                code="reviewer_visible_outcome_oracle",
            )
            delegated_thread_id = run.get("delegated_thread_id")
            require(
                isinstance(delegated_thread_id, str)
                and bool(delegated_thread_id)
                and delegated_thread_id != data.get("task_id")
                and delegated_thread_id not in delegated_thread_ids,
                code,
                f"{run_id}: delegated thread identity is missing, reused, or not fresh",
            )
            delegated_thread_ids.add(delegated_thread_id)
            validate_reviewer_visible_identifier(
                delegated_thread_id,
                label=f"{run_id}: delegated thread ID",
                code="reviewer_visible_outcome_oracle",
            )
            instance_created_at = parse_timestamp(
                run.get("reviewer_instance_created_at"),
                f"{run_id}: reviewer instance created",
            )
            require(
                data_capture - timedelta(days=1)
                <= instance_created_at
                <= data_capture + FUTURE_CLOCK_SKEW,
                code,
                f"{run_id}: reviewer instance is not current to the delegated task",
            )
            blind_bundle_path = str(run.get("blind_bundle_path", "")).replace(
                "\\", "/"
            )
            validate_reviewer_visible_identifier(
                blind_bundle_path,
                label=f"{run_id}: blind bundle path",
                code="reviewer_visible_outcome_oracle",
            )
            blind_bundle = bound_mapping(
                blind_bundle_path,
                run.get("blind_bundle_digest"),
                root=root,
                code=code,
                label=f"{run_id}: source-only blind bundle",
            )
            allowed_reads = validate_source_only_blind_bundle(
                blind_bundle,
                bundle_path=blind_bundle_path,
                input_path=input_path,
                input_digest=str(input_digest),
                reviewer_skill=reviewer_skill,
                root=root,
                code=code,
                label=run_id,
            )
            for path_field in (
                "dispatch_prompt_path",
                "raw_transport_output_path",
                "platform_read_scope_export_path",
            ):
                validate_reviewer_visible_identifier(
                    run.get(path_field),
                    label=f"{run_id}: {path_field}",
                    code="reviewer_visible_outcome_oracle",
                )
            prompt = bound_mapping(
                run.get("dispatch_prompt_path"),
                run.get("dispatch_prompt_digest"),
                root=root,
                code=code,
                label=f"{run_id}: dispatch prompt",
            )
            raw_output = bound_mapping(
                run.get("raw_transport_output_path"),
                run.get("raw_output_digest"),
                root=root,
                code=code,
                label=f"{run_id}: raw transport output",
            )
            read_scope = bound_mapping(
                run.get("platform_read_scope_export_path"),
                run.get("platform_read_scope_export_digest"),
                root=root,
                code=code,
                label=f"{run_id}: read-scope export",
            )
            review_contract = run.get("review_contract")
            require(
                isinstance(review_contract, dict),
                code,
                f"{run_id}: review contract",
            )
            instance_id = review_contract.get("reviewer_instance_id")
            validate_reviewer_visible_identifier(
                instance_id,
                label=f"{run_id}: reviewer instance ID",
                code="reviewer_visible_outcome_oracle",
            )
            require(
                set(prompt)
                == {
                    "schema_version",
                    "prompt_contract_id",
                    "reviewer_skill",
                    "frozen_input",
                    "blind_bundle",
                    "declared_resource_closure",
                    "allowed_write_prefixes",
                    "blindness",
                },
                code,
                f"{run_id}: prompt contains undeclared or missing fields",
            )
            require(
                prompt.get("schema_version") == 1
                and prompt.get("prompt_contract_id")
                == "independent_blind_review_v1"
                and prompt.get("reviewer_skill") == reviewer_skill
                and prompt.get("frozen_input")
                == {"path": input_path, "digest": input_digest}
                and prompt.get("blind_bundle")
                == {
                    "path": blind_bundle_path,
                    "digest": run.get("blind_bundle_digest"),
                    "artifact_type": "source_only_sanitized_blind_bundle",
                }
                and prompt.get("blindness")
                == {
                    "oracle_material_visible": False,
                    "prior_scores_visible": False,
                    "other_reviewer_outputs_visible": False,
                    "expected_decision_visible": False,
                },
                code,
                f"{run_id}: prompt is not the strict blind-review contract",
            )
            validate_blind_dispatch_prompt_identifiers(
                prompt,
                label=f"{run_id}: dispatch prompt",
            )
            declared_reads = prompt.get("declared_resource_closure")
            require(
                isinstance(declared_reads, list)
                and bool(declared_reads)
                and len(declared_reads) == len(set(declared_reads))
                and set(declared_reads) == allowed_reads,
                code,
                f"{run_id}: invalid declared resource closure",
            )
            for declared_path in declared_reads:
                normalized = str(declared_path).replace("\\", "/")
                relative = PurePosixPath(normalized)
                require(
                    not relative.is_absolute()
                    and ".." not in relative.parts
                    and (root / normalized).is_file(),
                    code,
                    f"{run_id}: unsafe or missing declared read {normalized}",
                )
            allowed_write_prefixes = prompt.get("allowed_write_prefixes")
            require(
                allowed_write_prefixes == ["runtime-artifacts/reviews/"],
                code,
                f"{run_id}: review-only write prefix",
            )
            for artifact, label in ((raw_output, "raw output"), (read_scope, "read scope")):
                require(artifact.get("task_id") == data.get("task_id"), code, f"{run_id}: {label} task")
                require(artifact.get("run_id") == run_id, code, f"{run_id}: {label} run")
                require(
                    artifact.get("platform_receipt_id") == platform_receipt_id,
                    code,
                    f"{run_id}: {label} receipt",
                )
                require(
                    artifact.get("reviewer_instance_id") == instance_id,
                    code,
                    f"{run_id}: {label} instance",
                )
                require(
                    artifact.get("delegated_thread_id") == delegated_thread_id,
                    code,
                    f"{run_id}: {label} delegated thread",
                )
            require(
                raw_output.get("review_contract") == review_contract,
                code,
                f"{run_id}: raw/structured review mismatch",
            )
            files_read = review_contract.get("files_read")
            files_written = review_contract.get("files_written")
            require(
                isinstance(files_read, list)
                and bool(files_read)
                and set(files_read) == allowed_reads,
                code,
                f"{run_id}: reviewer read outside the declared closure",
            )
            for read_path in files_read:
                if not is_reviewer_skill_resource_path(read_path):
                    validate_reviewer_visible_identifier(
                        read_path,
                        label=f"{run_id}: reviewer read path",
                        code="reviewer_visible_outcome_oracle",
                    )
            require(
                isinstance(files_written, list)
                and all(
                    str(path).replace("\\", "/").startswith(
                        "runtime-artifacts/reviews/"
                    )
                    for path in files_written
                )
                and not set(files_read).intersection(files_written),
                code,
                f"{run_id}: reviewer write scope",
            )
            for written_path in files_written:
                validate_reviewer_visible_identifier(
                    written_path,
                    label=f"{run_id}: reviewer write path",
                    code="reviewer_visible_outcome_oracle",
                )
            file_digests = read_scope.get("file_digests", {})
            require(
                isinstance(file_digests, dict)
                and set(file_digests) == set(files_read),
                code,
                f"{run_id}: read digest closure mismatch",
            )
            for read_path in files_read:
                require(
                    file_digests.get(read_path) == file_digest(root / read_path),
                    code,
                    f"{run_id}: unbound read {read_path}",
                )
            write_digests = read_scope.get("write_digests", {})
            require(
                isinstance(write_digests, dict)
                and set(write_digests) == set(files_written),
                code,
                f"{run_id}: write digest closure mismatch",
            )
            for written_path in files_written:
                require(
                    (root / written_path).is_file()
                    and write_digests.get(written_path)
                    == file_digest(root / written_path),
                    code,
                    f"{run_id}: unbound review output {written_path}",
                )
            require(
                read_scope.get("attestation_kind")
                == "platform_read_write_scope_export"
                and read_scope.get("files_read") == files_read
                and read_scope.get("files_written") == files_written
                and read_scope.get("source_edits_performed")
                == review_contract.get("source_edits_performed")
                is False
                and review_contract.get("input_digest_before") == input_digest
                and review_contract.get("input_digest_after") == input_digest
                and read_scope.get("input_digest_before") == input_digest
                and read_scope.get("input_digest_after") == input_digest,
                code,
                f"{run_id}: read-scope attestation mismatch",
            )
            export_run = export_by_id[run_id]
            require(
                export_run
                == {
                    "run_id": run_id,
                    "platform_receipt_id": platform_receipt_id,
                    "reviewer_instance_id": instance_id,
                    "delegated_thread_id": delegated_thread_id,
                    "reviewer_instance_created_at": run.get(
                        "reviewer_instance_created_at"
                    ),
                    "blind_bundle_digest": run.get("blind_bundle_digest"),
                    "dispatch_prompt_digest": run.get("dispatch_prompt_digest"),
                    "raw_output_digest": run.get("raw_output_digest"),
                    "read_scope_digest": run.get("platform_read_scope_export_digest"),
                },
                code,
                f"{run_id}: platform export binding mismatch",
            )


def build_live_repeat_durable_self_test(root: Path, current_version: str) -> dict[str, Any]:
    captured_dt = datetime.now(timezone.utc).replace(microsecond=0)
    captured_at = captured_dt.isoformat()
    identity = current_contract_identity()
    task_id = "phase8-live-durable-self-test"
    run_id = "phase8-live-durable-self-test-run"
    receipt_id = "platform-receipt-live-self-test"
    delegated_thread_id = "delegated-thread-live-self-test"
    instance_created_at = (captured_dt - timedelta(minutes=1)).isoformat()
    input_path = "inputs/reviewer-input.md"
    _, input_digest = write_temp_text(
        root,
        input_path,
        f"""# Synthetic frozen source input

```yaml
artifact_id: durable-self-test-source
version_id: v001
workflow_id: durable-live-self-test
round_id: r001
plugin_version: {current_version}
source_skill: article-drafter
created_by_instance_id: synthetic-writer
based_on: [article-context-source@v001, article-analysis-output@v001]
change_type: initial_draft
frozen: true
anonymity: Synthetic validator fixture.
```

The source artifact contains a bounded synthetic claim and its analysis values.
""",
    )
    blind_bundle_path, blind_bundle_digest = write_temp_mapping(
        root,
        "exports/source-only-blind-bundle.yaml",
        {
            "schema_version": 1,
            "artifact_type": "source_only_sanitized_blind_bundle",
            "bundle_id": "phase8-live-durable-self-test-blind-bundle",
            "source_artifacts": [
                {
                    "artifact_role": "frozen_source_input",
                    "path": input_path,
                    "sha256": input_digest,
                }
            ],
            "reviewer_resources": [],
            "review_context": {
                "prior_reviewer_outputs": [],
                "prior_evaluator_outputs": [],
                "prior_scores": [],
                "prior_decisions": [],
                "expected_findings": [],
                "expected_decision": None,
            },
            "lineage": {
                "based_on_source_artifact_digests": [input_digest],
                "based_on_review_artifact_refs": [],
            },
        },
    )
    prompt_path, prompt_digest = write_temp_mapping(
        root,
        "exports/dispatch-prompt.yaml",
        {
            "schema_version": 1,
            "prompt_contract_id": "independent_blind_review_v1",
            "reviewer_skill": "article-evaluator",
            "frozen_input": {"path": input_path, "digest": input_digest},
            "blind_bundle": {
                "path": blind_bundle_path,
                "digest": blind_bundle_digest,
                "artifact_type": "source_only_sanitized_blind_bundle",
            },
            "declared_resource_closure": [blind_bundle_path, input_path],
            "allowed_write_prefixes": ["runtime-artifacts/reviews/"],
            "blindness": {
                "oracle_material_visible": False,
                "prior_scores_visible": False,
                "other_reviewer_outputs_visible": False,
                "expected_decision_visible": False,
            },
        },
    )
    review_contract = {
        "reviewer_skill": "article-evaluator",
        "reviewer_instance_id": "durable-reviewer-instance-001",
        "files_read": [blind_bundle_path, input_path],
        "files_written": [],
        "input_digest_before": input_digest,
        "input_digest_after": input_digest,
        "isolation_mode": "fresh_subagent",
        "prior_scores_visible": False,
        "source_edits_performed": False,
        "decision": "accept",
        "findings": [],
        "unresolved_issues": [],
    }
    raw_path, raw_digest = write_temp_mapping(
        root,
        "exports/raw-output.yaml",
        {
            "task_id": task_id,
            "run_id": run_id,
            "platform_receipt_id": receipt_id,
            "reviewer_instance_id": review_contract["reviewer_instance_id"],
            "delegated_thread_id": delegated_thread_id,
            "review_contract": review_contract,
        },
    )
    scope_path, scope_digest = write_temp_mapping(
        root,
        "exports/read-scope.yaml",
        {
            "task_id": task_id,
            "run_id": run_id,
            "platform_receipt_id": receipt_id,
            "reviewer_instance_id": review_contract["reviewer_instance_id"],
            "delegated_thread_id": delegated_thread_id,
            "attestation_kind": "platform_read_write_scope_export",
            "files_read": review_contract["files_read"],
            "files_written": review_contract["files_written"],
            "file_digests": {
                blind_bundle_path: blind_bundle_digest,
                input_path: input_digest,
            },
            "write_digests": {},
            "input_digest_before": input_digest,
            "input_digest_after": input_digest,
            "source_edits_performed": False,
        },
    )
    export_id = "platform-export-live-self-test"
    export_path, export_digest = write_temp_mapping(
        root,
        "exports/task-export.yaml",
        {
            "schema_version": 1,
            "export_id": export_id,
            "provider_surface": "codex",
            "provider_verifier_adapter": SYNTHETIC_PROVIDER_ADAPTER_ID,
            "synthetic_test_only": True,
            "task_id": task_id,
            "plugin_version": current_version,
            **identity,
            "captured_at": captured_at,
            "runs": [
                {
                    "run_id": run_id,
                    "platform_receipt_id": receipt_id,
                    "reviewer_instance_id": review_contract["reviewer_instance_id"],
                    "delegated_thread_id": delegated_thread_id,
                    "reviewer_instance_created_at": instance_created_at,
                    "blind_bundle_digest": blind_bundle_digest,
                    "dispatch_prompt_digest": prompt_digest,
                    "raw_output_digest": raw_digest,
                    "read_scope_digest": scope_digest,
                }
            ],
        },
    )
    return {
        "evidence_class": "durable_platform_fresh_subagent_receipts",
        "verification_level": "durable_platform_provenance",
        "verified_live_gate_eligible": True,
        "durable_verification_missing": [],
        "provider_verifier_adapter": SYNTHETIC_PROVIDER_ADAPTER_ID,
        **identity,
        "platform_task_or_delegation_export_id": export_id,
        "platform_task_or_delegation_export_path": export_path,
        "platform_task_or_delegation_export_digest": export_digest,
        "captured_at": captured_at,
        "plugin_version": current_version,
        "task_id": task_id,
        "cases": [
            {
                "case_id": "durable-live-self-test",
                "input_path": input_path,
                "input_digest": input_digest,
                "reviewer_skill": "article-evaluator",
                "runs": [
                    {
                        "run_id": run_id,
                        "platform_receipt_id": receipt_id,
                        "delegated_thread_id": delegated_thread_id,
                        "reviewer_instance_created_at": instance_created_at,
                        "blind_bundle_path": blind_bundle_path,
                        "blind_bundle_digest": blind_bundle_digest,
                        "dispatch_prompt_path": prompt_path,
                        "dispatch_prompt_digest": prompt_digest,
                        "raw_transport_output_path": raw_path,
                        "raw_output_digest": raw_digest,
                        "platform_read_scope_export_path": scope_path,
                        "platform_read_scope_export_digest": scope_digest,
                        "review_contract": review_contract,
                    }
                ],
            }
        ],
    }


def validate_live_repeat_durable_negative_guards(
    current_version: str,
) -> list[dict[str, str]]:
    mutations = {
        "label-only-promotion": lambda data: data.pop(
            "platform_task_or_delegation_export_path"
        ),
        "platform-export-digest-mismatch": lambda data: data.update(
            {"platform_task_or_delegation_export_digest": "sha256:" + "0" * 64}
        ),
        "raw-output-digest-mismatch": lambda data: data["cases"][0]["runs"][0].update(
            {"raw_output_digest": "sha256:" + "1" * 64}
        ),
        "raw-contract-mismatch": lambda data: data["cases"][0]["runs"][0][
            "review_contract"
        ].update({"decision": "revise"}),
        "read-scope-mismatch": lambda data: data["cases"][0]["runs"][0][
            "review_contract"
        ].update({"files_read": ["inputs/not-read.md"]}),
        "platform-receipt-mismatch": lambda data: data["cases"][0]["runs"][0].update(
            {"platform_receipt_id": "different-platform-receipt"}
        ),
    }
    results: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="phase8-live-durable-") as temp:
        root = Path(temp)
        baseline = build_live_repeat_durable_self_test(root, current_version)
        try:
            validate_durable_live_repeat_bindings(
                baseline, current_version, root=root
            )
        except CorpusViolation as exc:
            require(
                exc.code == "provider_trust_anchor_unavailable",
                "provider_synthetic_override_guard",
                f"unexpected real-evidence rejection: {exc.code}",
            )
        else:
            raise CorpusViolation(
                "provider_synthetic_override_guard",
                "ephemeral synthetic export counted as runtime evidence",
            )
        validate_durable_live_repeat_bindings(
            baseline,
            current_version,
            root=root,
            synthetic_override=True,
        )
        for probe_id, mutate in mutations.items():
            candidate = copy.deepcopy(baseline)
            mutate(candidate)
            try:
                validate_durable_live_repeat_bindings(
                    candidate,
                    current_version,
                    root=root,
                    synthetic_override=True,
                )
            except CorpusViolation as exc:
                require(
                    exc.code == "live_repeat_durable_binding",
                    "live_repeat_durable_guard_wrong_error",
                    f"{probe_id}: {exc.code}",
                )
                results.append(
                    {
                        "probe_id": f"{probe_id}-rejected",
                        "status": "rejected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise CorpusViolation("live_repeat_durable_guard_accepted", probe_id)
    return results


def validate_live_blind_bundle_negative_guard(
    current_version: str,
) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="phase8-live-blind-bundle-") as temp:
        root = Path(temp)
        candidate = build_live_repeat_durable_self_test(root, current_version)
        run = candidate["cases"][0]["runs"][0]
        original = bound_mapping(
            run["blind_bundle_path"],
            run["blind_bundle_digest"],
            root=root,
            code="live_repeat_durable_binding",
            label="blind-bundle-negative-baseline",
        )
        poisoned = copy.deepcopy(original)
        poisoned["review_context"]["prior_scores"] = [0.93]
        poison_path, poison_digest = write_temp_mapping(
            root, "exports/poisoned-blind-bundle.yaml", poisoned
        )
        run["blind_bundle_path"] = poison_path
        run["blind_bundle_digest"] = poison_digest
        try:
            validate_durable_live_repeat_bindings(
                candidate,
                current_version,
                root=root,
                synthetic_override=True,
            )
        except CorpusViolation as exc:
            require(
                exc.code == "live_repeat_durable_binding",
                "live_blind_bundle_guard_wrong_error",
                exc.code,
            )
            return {
                "mutation": "blind_bundle_contains_prior_evaluator_score",
                "status": "rejected",
                "error_code": exc.code,
            }
        raise CorpusViolation(
            "live_blind_bundle_guard_accepted",
            "blind bundle containing prior score was accepted",
        )


def validate_live_source_input_negative_guards(
    current_version: str,
) -> list[dict[str, Any]]:
    base_metadata = f"""artifact_id: negative-source-v001
version_id: v001
workflow_id: phase8-source-negative
round_id: r001
plugin_version: {current_version}
source_skill: article-drafter
created_by_instance_id: synthetic-writer
based_on: [article-context-source@v001, article-analysis-output@v001]
change_type: initial_draft
frozen: true
anonymity: Synthetic validator fixture.
"""
    probes = [
        (
            "generic_review_instruction",
            base_metadata,
            "Inspect this frozen artifact and return route, final state, and findings.\n",
            {"generic_review_instruction"},
            ["source_content"],
        ),
        (
            "revision_brief_or_plan",
            base_metadata,
            "The author revision brief lists the must-fix plan for this draft.\n",
            {"revision_control_material"},
            ["source_content"],
        ),
        (
            "expected_result_oracle",
            base_metadata,
            "Expected outcome: blocked. The artifact must be rejected.\n",
            {"expected_result_oracle"},
            ["source_content"],
        ),
        (
            "review_artifact_in_source_lineage",
            base_metadata.replace(
                "article-analysis-output@v001",
                "article-evaluation-r001",
            ),
            "The source artifact contains a bounded synthetic claim.\n",
            {
                "review_or_oracle_artifact_in_source_lineage",
                "review_role_or_artifact_in_lineage",
            },
            ["source_lineage"],
        ),
        (
            "undeclared_expected_metadata_field",
            base_metadata + "expected_result: accept\n",
            "The source artifact contains a bounded synthetic claim.\n",
            {"embedded_metadata_fields_not_allowlisted"},
            ["embedded_metadata"],
        ),
    ]
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="phase8-live-source-input-") as temp:
        root = Path(temp)
        for probe_index, (
            mutation,
            metadata,
            body,
            expected_leaks,
            polluted_surfaces,
        ) in enumerate(probes, start=1):
            input_path, input_digest = write_temp_text(
                root,
                f"inputs/probe-n{probe_index:02d}.md",
                f"# Poisoned frozen source input\n\n```yaml\n{metadata}```\n\n{body}",
            )
            try:
                validate_source_only_input_artifact(
                    input_path,
                    input_digest,
                    root=root,
                    label=f"direct-source-input-poisoning:{mutation}",
                )
            except CorpusViolation as exc:
                require(
                    exc.code == "live_repeat_source_input_review_leak"
                    and all(leak in str(exc) for leak in expected_leaks),
                    "live_source_input_guard_wrong_error",
                    f"{mutation}: {exc}",
                )
                results.append(
                    {
                        "mutation": mutation,
                        "polluted_surfaces": polluted_surfaces,
                        "status": "rejected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise CorpusViolation(
                    "live_source_input_guard_accepted",
                    f"source input mutation was accepted: {mutation}",
                )
    return results


def validate_reviewer_visible_identifier_negative_guards(
    current_version: str,
) -> list[dict[str, str]]:
    valid_source = f"""# Neutral source

```yaml
artifact_id: source-n01
version_id: v001
workflow_id: workflow-n01
round_id: r001
plugin_version: {current_version}
source_skill: article-drafter
created_by_instance_id: writer-n01
based_on: [article-context-source@v001]
change_type: initial_draft
frozen: true
anonymity: Synthetic validator fixture.
```

Neutral synthetic source content.
"""
    results: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="phase8-visible-identifier-") as temp:
        root = Path(temp)

        poisoned_path, poisoned_digest = write_temp_text(
            root,
            "inputs/source-fatal.md",
            valid_source,
        )
        neutral_input_path, neutral_input_digest = write_temp_text(
            root,
            "inputs/source-n01.md",
            valid_source,
        )
        neutral_bundle = {
            "schema_version": 1,
            "artifact_type": "source_only_sanitized_blind_bundle",
            "bundle_id": "bundle-happy-n01",
            "source_artifacts": [
                {
                    "artifact_role": "frozen_source_input",
                    "path": neutral_input_path,
                    "sha256": neutral_input_digest,
                }
            ],
            "reviewer_resources": [],
            "review_context": {
                "prior_reviewer_outputs": [],
                "prior_evaluator_outputs": [],
                "prior_scores": [],
                "prior_decisions": [],
                "expected_findings": [],
                "expected_decision": None,
            },
            "lineage": {
                "based_on_source_artifact_digests": [neutral_input_digest],
                "based_on_review_artifact_refs": [],
            },
        }
        prompt_with_oracle_id = {
            "prompt_contract_id": "blind-dispatch-expected-n01",
            "frozen_input": {"path": neutral_input_path},
            "blind_bundle": {"path": "bundles/bundle-n01.yaml"},
            "declared_resource_closure": [
                neutral_input_path,
                "bundles/bundle-n01.yaml",
                "research-skills-openai/skills/article-evaluator/references/evaluation-gates.md",
            ],
            "allowed_write_prefixes": ["runtime-artifacts/reviews/"],
        }

        probes: list[tuple[str, Callable[[], None]]] = [
            (
                "source_path_contains_outcome_token",
                lambda: validate_source_only_input_artifact(
                    poisoned_path,
                    poisoned_digest,
                    root=root,
                    label="outcome-path-negative",
                ),
            ),
            (
                "blind_bundle_id_contains_outcome_token",
                lambda: validate_source_only_blind_bundle(
                    neutral_bundle,
                    bundle_path="bundles/bundle-n01.yaml",
                    input_path=neutral_input_path,
                    input_digest=neutral_input_digest,
                    reviewer_skill="article-evaluator",
                    root=root,
                    code="reviewer_visible_outcome_oracle",
                    label="bundle-id-negative",
                ),
            ),
            (
                "dispatch_prompt_id_contains_outcome_token",
                lambda: validate_blind_dispatch_prompt_identifiers(
                    prompt_with_oracle_id,
                    label="prompt-id-negative",
                ),
            ),
            (
                "run_or_case_id_contains_outcome_token",
                lambda: validate_reviewer_visible_identifier(
                    "case-ready-01",
                    label="run/case-ID-negative",
                ),
            ),
        ]
        for mutation, probe in probes:
            try:
                probe()
            except CorpusViolation as exc:
                require(
                    exc.code == "reviewer_visible_outcome_oracle",
                    "reviewer_visible_identifier_guard_wrong_error",
                    f"{mutation}: {exc}",
                )
                results.append(
                    {
                        "mutation": mutation,
                        "status": "rejected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise CorpusViolation(
                    "reviewer_visible_identifier_guard_accepted",
                    mutation,
                )
    return results


def validate_live_fresh_repeats(
    current_version: str,
    cases: dict[str, dict[str, Any]],
    selected_case_ids: list[str],
) -> dict[str, Any]:
    data = load_yaml(LIVE_REPEAT_PATH)
    require(data.get("schema_version") == 1, "live_repeat_schema", "schema_version")
    evidence_class = data.get("evidence_class")
    require(
        evidence_class
        in {
            "current_task_self_attested_fresh_subagent_snapshot",
            "durable_platform_fresh_subagent_receipts",
        },
        "live_repeat_evidence_class",
        str(evidence_class),
    )
    require(data.get("plugin_version") == current_version, "live_repeat_plugin_version", "manifest")
    require(bool(data.get("task_id")), "live_repeat_task_id", "missing")
    validate_reviewer_visible_identifier(
        data.get("task_id"),
        label="live repeat task ID",
    )
    durable_evidence = evidence_class == "durable_platform_fresh_subagent_receipts"
    if durable_evidence:
        require(
            data.get("verification_level") == "durable_platform_provenance"
            and data.get("verified_live_gate_eligible") is True
            and data.get("durable_verification_missing") == [],
            "live_repeat_verification_level",
            "durable receipt contract",
        )
        validate_durable_live_repeat_bindings(data, current_version)
    else:
        require(
            data.get("verification_level") == "self_attested_current_task_snapshot"
            and data.get("verified_live_gate_eligible") is False,
            "live_repeat_verification_level",
            "self-attested snapshots cannot satisfy the live gate",
        )
        require(
            set(data.get("durable_verification_missing", []))
            == {
                "executable_provider_verifier_adapter",
                "platform_task_or_delegation_export",
                "exact_dispatched_prompt_digest",
                "raw_transport_output_digest",
                "platform_attested_read_scope",
                "strict_blind_dispatch_contract",
                "source_only_sanitized_blind_bundle",
                "declared_read_resource_closure",
                "files_written_and_input_before_after_digests",
                "source_commit_and_plugin_tree_identity",
            },
            "live_repeat_durable_evidence",
            "missing-evidence declaration",
        )
    capture_policy = data.get("capture_policy", {})
    require(
        capture_policy.get("raw_transport_envelope_preserved") is durable_evidence,
        "live_repeat_capture_policy",
        "raw envelope",
    )
    require(capture_policy.get("structured_review_contract_preserved") is True, "live_repeat_capture_policy", "contract")
    durable_negative_guards = validate_live_repeat_durable_negative_guards(
        current_version
    )
    blind_bundle_negative_guard = validate_live_blind_bundle_negative_guard(
        current_version
    )
    source_input_negative_guards = validate_live_source_input_negative_guards(
        current_version
    )
    visible_identifier_negative_guards = (
        validate_reviewer_visible_identifier_negative_guards(current_version)
    )
    live_capture_state = validate_timestamp_window(
        data.get("captured_at"),
        "live-repeat-capture",
        max_age_days=EVIDENCE_FRESHNESS_DAYS,
    )
    require(
        live_capture_state == "current",
        "live_repeat_stale",
        "reviewer evidence is older than the current-release window",
    )
    repeated_cases = data.get("cases", [])
    require(len(repeated_cases) == 3, "live_repeat_case_count", str(len(repeated_cases)))
    require(
        {case.get("case_id") for case in repeated_cases} == set(selected_case_ids),
        "live_repeat_case_selection",
        str([case.get("case_id") for case in repeated_cases]),
    )

    forbidden = [str(item).replace("\\", "/").lower() for item in data.get("forbidden_read_fragments", [])]
    reviewer_ids: set[str] = set()
    run_ids: set[str] = set()
    review_digests: dict[str, str] = {}
    run_count = 0
    historical_oracle_exposed_run_count = 0
    critical_labels_required = 0
    critical_labels_detected = 0
    dissent_labels_required = 0
    dissent_labels_preserved = 0
    case_results: list[dict[str, Any]] = []
    for receipt in repeated_cases:
        case_id = receipt.get("case_id")
        require(case_id in cases, "live_repeat_unknown_case", str(case_id))
        validate_reviewer_visible_identifier(
            case_id,
            label="live repeat case ID",
        )
        historical_runs = receipt.get("historical_oracle_exposed_runs", [])
        require(
            isinstance(historical_runs, list) and len(historical_runs) == 2,
            "live_repeat_historical_oracle_exposure",
            f"{case_id}: expected two excluded historical runs",
        )
        historical_oracle_exposed_run_count += len(historical_runs)
        input_rel = str(receipt.get("input_path", "")).replace("\\", "/")
        input_path = REPO / input_rel
        require(input_path.is_file(), "live_repeat_input_missing", input_rel)
        require(receipt.get("input_digest") == file_digest(input_path), "live_repeat_input_digest", case_id)
        validate_source_only_input_artifact(
            input_rel,
            str(receipt.get("input_digest")),
            root=REPO,
            label=str(case_id),
        )
        reviewer_skill = receipt.get("reviewer_skill")
        expected_state = receipt.get("expected_review_stage_state")
        required_critical = set(receipt.get("required_critical_finding_labels", []))
        required_dissent = set(receipt.get("required_dissent_labels", []))
        critical_labels_required += len(required_critical) * 2
        dissent_labels_required += len(required_dissent) * 2
        runs = receipt.get("runs", [])
        require(len(runs) == 2, "live_repeat_run_count", case_id)
        observed_states: set[str] = set()
        case_instance_ids: list[str] = []
        case_run_ids: list[str] = []
        for run in runs:
            run_count += 1
            run_id = run.get("run_id")
            require(bool(run_id) and run_id not in run_ids, "live_repeat_run_id", str(run_id))
            validate_reviewer_visible_identifier(
                run_id,
                label=f"{case_id}: run ID",
            )
            run_ids.add(str(run_id))
            case_run_ids.append(str(run_id))
            raw = run.get("review_contract")
            require(isinstance(raw, dict), "live_repeat_review_contract", str(run_id))
            instance_id = raw.get("reviewer_instance_id")
            require(bool(instance_id) and instance_id not in reviewer_ids, "live_repeat_reviewer_reuse", str(instance_id))
            validate_reviewer_visible_identifier(
                instance_id,
                label=f"{run_id}: reviewer instance ID",
            )
            reviewer_ids.add(str(instance_id))
            case_instance_ids.append(str(instance_id))
            oracle_writer = cases[case_id]["oracle_observation"]["isolation"]["writer_instance_id"]
            require(instance_id != oracle_writer, "live_repeat_writer_reviewer_overlap", str(instance_id))
            require(raw.get("reviewer_skill") == reviewer_skill, "live_repeat_reviewer_skill", str(run_id))
            require(raw.get("isolation_mode") == "fresh_subagent", "live_repeat_isolation", str(run_id))
            require(raw.get("prior_scores_visible") is False, "live_repeat_prior_scores", str(run_id))
            require(raw.get("source_edits_performed") is False, "live_repeat_source_edit", str(run_id))
            files_read = raw.get("files_read", [])
            require(isinstance(files_read, list) and bool(files_read), "live_repeat_files_read", str(run_id))
            normalized_reads = [str(item).replace("\\", "/").lower() for item in files_read]
            for read_path in files_read:
                if not is_reviewer_skill_resource_path(read_path):
                    validate_reviewer_visible_identifier(
                        read_path,
                        label=f"{run_id}: reviewer read path",
                    )
            require(any(path.endswith(input_rel.lower()) for path in normalized_reads), "live_repeat_input_not_read", str(run_id))
            leaked = sorted(
                fragment
                for fragment in forbidden
                if any(fragment in path for path in normalized_reads)
            )
            require(not leaked, "live_repeat_forbidden_read", f"{run_id}: {leaked}")
            require(isinstance(raw.get("findings"), list), "live_repeat_findings", str(run_id))
            normalized = run.get("normalization", {})
            state = normalized.get("review_stage_state")
            require(state == expected_state, "live_repeat_expected_state", str(run_id))
            require(state == infer_live_review_stage(raw), "live_repeat_state_normalization", str(run_id))
            observed_states.add(str(state))
            detected_critical = set(normalized.get("critical_finding_labels", []))
            detected_dissent = set(normalized.get("dissent_labels", []))
            require(required_critical <= detected_critical, "live_repeat_critical_missed", str(run_id))
            require(required_dissent <= detected_dissent, "live_repeat_dissent_missed", str(run_id))
            require(all(live_label_supported(label, raw) for label in detected_critical), "live_repeat_critical_unsupported", str(run_id))
            require(all(live_label_supported(label, raw) for label in detected_dissent), "live_repeat_dissent_unsupported", str(run_id))
            critical_labels_detected += len(required_critical)
            dissent_labels_preserved += len(required_dissent)
            payload = json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            review_digests[str(run_id)] = "sha256:" + hashlib.sha256(payload).hexdigest()
        require(len(observed_states) == 1, "live_repeat_state_disagreement", case_id)
        case_results.append(
            {
                "case_id": case_id,
                "input_path": input_rel,
                "input_digest": receipt.get("input_digest"),
                "reviewer_skill": reviewer_skill,
                "run_ids": case_run_ids,
                "reviewer_instance_ids": case_instance_ids,
                "review_stage_state": expected_state,
                "fresh_runs": len(runs),
                "state_agreement": True,
                "critical_finding_labels": sorted(required_critical),
                "dissent_labels": sorted(required_dissent),
            }
        )

    return {
        "evidence_class": data["evidence_class"],
        "runtime_claim": data["runtime_claim"],
        "captured_at": data["captured_at"].isoformat() if isinstance(data["captured_at"], datetime) else data["captured_at"],
        "task_id": data["task_id"],
        "case_count": len(repeated_cases),
        "observed_review_snapshot_count": run_count,
        "historical_oracle_exposed_snapshot_count": historical_oracle_exposed_run_count,
        "historical_oracle_exposed_snapshots_count_as_evidence": False,
        "verified_live_review_count": run_count if durable_evidence else 0,
        "unique_reviewer_instance_count": len(reviewer_ids),
        "snapshot_contract_state_agreement_percent": 100.0,
        "snapshot_critical_label_recall_percent": percent(critical_labels_detected, critical_labels_required),
        "self_attested_isolation_field_compliance_percent": 100.0,
        "self_attested_source_edit_field_compliance_percent": 100.0,
        "snapshot_dissent_label_preservation_percent": percent(dissent_labels_preserved, dissent_labels_required),
        "review_content_digests": review_digests,
        "case_results": case_results,
        "internal_contract_validation": "passed",
        "durable_binding_negative_guard_count": len(durable_negative_guards),
        "durable_binding_negative_guards": durable_negative_guards,
        "blind_bundle_semantic_negative_guard": blind_bundle_negative_guard,
        "source_input_semantic_negative_guard_count": len(
            source_input_negative_guards
        ),
        "source_input_semantic_negative_guards": source_input_negative_guards,
        "reviewer_visible_identifier_negative_guard_count": len(
            visible_identifier_negative_guards
        ),
        "reviewer_visible_identifier_negative_guards": (
            visible_identifier_negative_guards
        ),
        "blind_bundle_contract": (
            "source-only sanitized bundle; prior reviewer/evaluator outputs, "
            "scores, decisions, expected findings, and review lineage are empty; "
            "the bound source file content and parsed metadata are scanned directly; "
            "embedded metadata uses an exact allowlist and based_on accepts only "
            "declared source-artifact kinds"
        ),
        "provider_verifier_adapter_count": len(real_provider_adapter_ids()),
        "synthetic_provider_override_self_test": {
            "status": "passed",
            "counts_as_runtime_evidence": False,
            "ephemeral_temp_root_required": True,
        },
        "source_identity_binding_required": list(SOURCE_IDENTITY_FIELDS),
        "freshness_days": EVIDENCE_FRESHNESS_DAYS,
        "verified_live_gate_status": "completed" if durable_evidence else "pending_durable_execution_evidence",
        "status": "completed" if durable_evidence else "observed_unverified",
    }


def parse_timestamp(value: Any, receipt_id: str) -> datetime:
    try:
        parsed = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise CorpusViolation("retrieval_timestamp", receipt_id) from exc
    require(parsed.tzinfo is not None, "retrieval_timestamp", receipt_id)
    return parsed.astimezone(timezone.utc)


def validate_timestamp_window(
    value: Any,
    label: str,
    *,
    max_age_days: int,
    now: datetime | None = None,
) -> str:
    captured = parse_timestamp(value, label)
    reference = now or datetime.now(timezone.utc)
    require(
        captured <= reference + FUTURE_CLOCK_SKEW,
        "phase8_future_timestamp",
        f"{label}: timestamp is beyond the allowed clock skew",
    )
    age_days = (reference - captured).total_seconds() / 86400
    return "stale" if age_days > max_age_days else "current"


def validate_time_and_identity_self_tests() -> dict[str, Any]:
    reference = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    try:
        validate_timestamp_window(
            reference + timedelta(hours=1),
            "synthetic-future-probe",
            max_age_days=EVIDENCE_FRESHNESS_DAYS,
            now=reference,
        )
    except CorpusViolation as exc:
        require(
            exc.code == "phase8_future_timestamp",
            "phase8_time_guard_self_test",
            exc.code,
        )
    else:
        raise CorpusViolation(
            "phase8_time_guard_self_test", "future timestamp was accepted"
        )
    require(
        validate_timestamp_window(
            reference - timedelta(days=EVIDENCE_FRESHNESS_DAYS + 1),
            "synthetic-stale-probe",
            max_age_days=EVIDENCE_FRESHNESS_DAYS,
            now=reference,
        )
        == "stale",
        "phase8_time_guard_self_test",
        "stale timestamp was not classified",
    )
    mutated_identity = current_contract_identity().copy()
    mutated_identity["manifest_digest"] = "sha256:" + "0" * 64
    try:
        validate_source_identity(
            mutated_identity,
            label="synthetic identity mutation",
            synthetic_override=True,
        )
    except CorpusViolation as exc:
        require(
            exc.code == "phase8_source_identity",
            "phase8_identity_guard_self_test",
            exc.code,
        )
    else:
        raise CorpusViolation(
            "phase8_identity_guard_self_test",
            "altered plugin identity was accepted",
        )
    return {
        "future_timestamp_rejected": True,
        "older_than_90_days_classified_stale": True,
        "source_identity_mutation_rejected": True,
        "counts_as_runtime_evidence": False,
    }


def validate_populated_retrieval_receipt(
    receipt: dict[str, Any],
    contract: dict[str, Any],
    current_version: str,
    freshness_days: int,
    *,
    root: Path = REPO,
) -> str:
    receipt_id = receipt["receipt_id"]
    expected_capability = {
        "search": "chatgpt_codex_builtin_search",
        "deep_research_completed": "chatgpt_deep_research",
        "deep_research_inactive_control": "chatgpt_deep_research",
    }[receipt["kind"]]
    require(
        receipt.get("capability") == expected_capability,
        "retrieval_capability",
        receipt_id,
    )
    require(receipt.get("expected_completion_status") == contract["expected_status"], "retrieval_expected_status", receipt_id)
    for field in ("captured_at", "plugin_version", "task_id"):
        require(bool(receipt.get(field)), "retrieval_live_field", f"{receipt_id}: {field}")
    require(receipt["plugin_version"] == current_version, "retrieval_plugin_version", receipt_id)
    if (
        validate_timestamp_window(
            receipt["captured_at"], receipt_id, max_age_days=freshness_days
        )
        == "stale"
    ):
        return "stale"
    artifact_digests = receipt.get("artifact_digests", [])
    require(all(SHA256_RE.fullmatch(str(value)) for value in artifact_digests), "retrieval_artifact_digest", receipt_id)
    require(bool(artifact_digests), "retrieval_artifact_digest", receipt_id)
    artifact_paths = receipt.get("artifact_paths", [])
    require(len(artifact_paths) == len(artifact_digests), "retrieval_artifact_path", receipt_id)
    bound_artifacts: list[dict[str, Any]] = []
    for artifact_path, expected_digest in zip(artifact_paths, artifact_digests):
        normalized = str(artifact_path).replace("\\", "/")
        path = PurePosixPath(normalized)
        require(not path.is_absolute() and ".." not in path.parts, "retrieval_artifact_path", receipt_id)
        resolved = root / normalized
        require(resolved.is_file(), "retrieval_artifact_path", f"{receipt_id}: {normalized}")
        require(file_digest(resolved) == expected_digest, "retrieval_artifact_digest", f"{receipt_id}: {normalized}")
        artifact = load_yaml(resolved)
        require(artifact.get("plugin_version") == current_version, "retrieval_artifact_version", receipt_id)
        require(artifact.get("task_id") == receipt.get("task_id"), "retrieval_artifact_task", receipt_id)
        require(
            parse_timestamp(artifact.get("captured_at"), receipt_id)
            == parse_timestamp(receipt.get("captured_at"), receipt_id),
            "retrieval_artifact_timestamp",
            receipt_id,
        )
        bound_artifacts.append(artifact)
    sources = receipt.get("opened_sources", [])
    require(len(sources) >= contract["min_opened_sources"], "retrieval_source_count", receipt_id)
    source_ids = set()
    for source in sources:
        source_id = source.get("source_id")
        require(bool(source_id) and source_id not in source_ids, "retrieval_source_id", receipt_id)
        source_ids.add(source_id)
        require(bool(source.get("url")), "retrieval_source_url", receipt_id)
        if receipt["kind"] != "deep_research_inactive_control":
            require(source.get("primary_or_authoritative") is True, "retrieval_source_authority", receipt_id)
            require(source.get("identity_verified") is True, "retrieval_source_identity", receipt_id)
    traces = receipt.get("material_claim_trace", [])
    if receipt["kind"] != "deep_research_inactive_control":
        require(bool(traces), "retrieval_claim_trace", receipt_id)
        claim_ids: set[str] = set()
        traced_source_ids: set[str] = set()
        for trace in traces:
            claim_id = trace.get("claim_id")
            require(
                bool(claim_id) and claim_id not in claim_ids,
                "retrieval_claim_trace",
                receipt_id,
            )
            claim_ids.add(str(claim_id))
            bound_sources = set(trace.get("source_ids", []))
            require(bool(bound_sources) and bound_sources <= source_ids, "retrieval_claim_trace", receipt_id)
            traced_source_ids.update(bound_sources)
        require(
            traced_source_ids == source_ids,
            "retrieval_claim_trace",
            f"{receipt_id}: every opened source must support a material claim",
        )
    if receipt["kind"] == "deep_research_completed":
        require(bool(receipt.get("handoff_artifact")), "deep_research_handoff", receipt_id)
        require(bool(receipt.get("mapper_return_artifact")), "deep_research_return", receipt_id)
        require(bool(receipt.get("resumed_pending_edge")), "deep_research_resume", receipt_id)
    elif receipt["kind"] == "deep_research_inactive_control":
        require(receipt.get("capability_active") is False, "deep_research_inactive", receipt_id)
        require(receipt.get("workflow_paused") is True, "deep_research_pause", receipt_id)
        require(receipt.get("downstream_evidence_map_created") is False, "deep_research_inline_simulation", receipt_id)
        require(bool(receipt.get("continuation_artifact")), "deep_research_continuation", receipt_id)
        require(
            receipt.get("continuation_artifact") == artifact_paths[0],
            "deep_research_continuation_binding",
            receipt_id,
        )
        require(
            len(bound_artifacts) == 1
            and bound_artifacts[0].get("handoff_status") == "deep_research_handoff_required",
            "deep_research_continuation_binding",
            receipt_id,
        )
    elif receipt["kind"] == "search":
        require(len(bound_artifacts) == 1, "search_artifact_binding", receipt_id)
        artifact = bound_artifacts[0]
        artifact_sources = {
            (source.get("source_id"), source.get("url"))
            for source in artifact.get("opened_sources", [])
            if isinstance(source, dict)
        }
        receipt_sources = {
            (source.get("source_id"), source.get("url"))
            for source in sources
            if isinstance(source, dict)
        }
        require(artifact_sources == receipt_sources, "search_artifact_source_binding", receipt_id)
        artifact_claims = {
            claim.get("claim_id")
            for claim in artifact.get("material_claims", [])
            if isinstance(claim, dict)
        }
        receipt_claims = {trace.get("claim_id") for trace in traces if isinstance(trace, dict)}
        require(artifact_claims == receipt_claims, "search_artifact_claim_binding", receipt_id)
        require(
            artifact.get("question_class") == receipt.get("question_class")
            and artifact.get("route") == "chatgpt_codex_builtin_search",
            "search_artifact_route_binding",
            receipt_id,
        )
    return "completed"


def validate_deep_research_event_order(
    handoff: dict[str, Any],
    user_start: dict[str, Any],
    provider_completed: dict[str, Any],
    mapper_return: dict[str, Any],
    resume: dict[str, Any],
    captured_at: Any,
    receipt_id: str,
) -> None:
    event_times = [
        parse_timestamp(handoff.get("event_at"), f"{receipt_id}: handoff"),
        parse_timestamp(user_start.get("event_at"), f"{receipt_id}: user start"),
        parse_timestamp(
            provider_completed.get("event_at"),
            f"{receipt_id}: provider run completed",
        ),
        parse_timestamp(mapper_return.get("event_at"), f"{receipt_id}: mapper return"),
        parse_timestamp(resume.get("event_at"), f"{receipt_id}: resume"),
    ]
    cycle_capture = parse_timestamp(captured_at, receipt_id)
    require(
        all(left < right for left, right in zip(event_times, event_times[1:]))
        and cycle_capture - timedelta(days=EVIDENCE_FRESHNESS_DAYS)
        <= event_times[0]
        and event_times[-1] <= cycle_capture,
        "retrieval_durable_binding",
        f"{receipt_id}: Deep Research events are not strictly monotonic",
    )


def validate_deep_research_evidence_linkage(
    receipt: dict[str, Any],
    mapper_return: dict[str, Any],
    resume: dict[str, Any],
    evidence_artifact_ids: list[str],
    receipt_id: str,
) -> None:
    require(
        mapper_return.get("evidence_artifact_ids") == evidence_artifact_ids
        and mapper_return.get("evidence_artifacts")
        == receipt.get("evidence_artifacts")
        and resume.get("evidence_artifact_ids") == evidence_artifact_ids
        and resume.get("evidence_artifacts") == receipt.get("evidence_artifacts"),
        "retrieval_durable_binding",
        f"{receipt_id}: mapper return and resume do not bind the same evidence artifacts",
    )


def validate_verified_retrieval_provenance(
    receipt: dict[str, Any],
    schema: dict[str, Any],
    evidence_class: str,
    *,
    root: Path = REPO,
    synthetic_override: bool = False,
) -> None:
    policy = schema.get("verification_policy", {})
    require(
        evidence_class == policy.get("verified_evidence_class"),
        "retrieval_verified_evidence_class",
        str(receipt.get("receipt_id")),
    )
    require(
        policy.get("repository_files_alone_are_not_provider_provenance") is True
        and policy.get("provider_verifier_adapter_required") is True
        and policy.get("source_identity_required") == list(SOURCE_IDENTITY_FIELDS),
        "retrieval_durable_schema",
        "provider/source trust policy",
    )
    common_fields = policy.get("verified_live_common_required", [])
    kind_fields = policy.get("verified_live_kind_required", {}).get(receipt.get("kind"), [])
    require(
        isinstance(common_fields, list) and bool(common_fields),
        "retrieval_durable_schema",
        "verified_live_common_required",
    )
    require(
        isinstance(kind_fields, list) and bool(kind_fields),
        "retrieval_durable_schema",
        str(receipt.get("kind")),
    )
    required_fields = [*common_fields, *kind_fields]
    missing = [field for field in required_fields if not receipt.get(field)]
    require(
        not missing,
        "retrieval_durable_provenance",
        f"{receipt.get('receipt_id')}: missing {missing}",
    )
    identity_or_provider_missing = [
        field
        for field in ("provider_verifier_adapter", *SOURCE_IDENTITY_FIELDS)
        if not receipt.get(field)
    ]
    require(
        not identity_or_provider_missing,
        "retrieval_durable_provenance",
        f"{receipt.get('receipt_id')}: missing {identity_or_provider_missing}",
    )
    digest_fields = [field for field in required_fields if field.endswith("_digest")]
    invalid_digests = [
        field
        for field in digest_fields
        if SHA256_RE.fullmatch(str(receipt.get(field, ""))) is None
    ]
    require(
        not invalid_digests,
        "retrieval_durable_provenance",
        f"{receipt.get('receipt_id')}: invalid digests {invalid_digests}",
    )
    query = receipt.get("query")
    require(
        isinstance(query, str) and bool(query.strip()),
        "retrieval_durable_query_binding",
        str(receipt.get("receipt_id")),
    )
    expected_query_digest = "sha256:" + hashlib.sha256(query.encode("utf-8")).hexdigest()
    require(
        receipt.get("query_or_request_digest") == expected_query_digest,
        "retrieval_durable_query_binding",
        str(receipt.get("receipt_id")),
    )

    receipt_id = str(receipt.get("receipt_id"))
    kind = str(receipt.get("kind"))
    if kind == "deep_research_completed":
        cycle_fields = policy.get("deep_research_cycle_identity_required", [])
        require(
            cycle_fields
            == [
                "deep_research_session_id",
                "deep_research_run_id",
                "user_start_event_path",
                "user_start_event_digest",
                "provider_run_completed_receipt_id",
                "provider_run_completed_path",
                "provider_run_completed_digest",
                "provider_run_completed_status",
                "mapper_return_receipt_id",
                "resume_transaction_id",
                "evidence_artifacts",
            ],
            "retrieval_durable_schema",
            "Deep Research cycle identity contract",
        )
        missing_cycle = [field for field in cycle_fields if not receipt.get(field)]
        require(
            not missing_cycle,
            "retrieval_durable_provenance",
            f"{receipt_id}: missing {missing_cycle}",
        )
        require(
            SHA256_RE.fullmatch(str(receipt.get("user_start_event_digest")))
            is not None
            and SHA256_RE.fullmatch(
                str(receipt.get("provider_run_completed_digest"))
            )
            is not None
            and receipt.get("provider_run_completed_status") == "completed",
            "retrieval_durable_provenance",
            f"{receipt_id}: invalid user-start/provider-completion contract",
        )
    path_digest_pairs: list[tuple[str, str, str]] = [
        (
            "platform_receipt_or_export_path",
            "platform_receipt_or_export_digest",
            "platform receipt/export",
        )
    ]
    if kind == "search":
        path_digest_pairs.extend(
            [
                ("raw_search_output_path", "raw_search_output_digest", "raw Search output"),
                ("citation_export_path", "citation_export_digest", "Search citation export"),
            ]
        )
    elif kind == "deep_research_completed":
        path_digest_pairs.extend(
            [
                (
                    "raw_deep_research_output_path",
                    "raw_deep_research_output_digest",
                    "raw Deep Research output",
                ),
                ("citation_export_path", "citation_export_digest", "Deep Research citation export"),
                ("handoff_artifact", "handoff_artifact_digest", "Deep Research handoff"),
                (
                    "user_start_event_path",
                    "user_start_event_digest",
                    "user-started Deep Research event",
                ),
                (
                    "provider_run_completed_path",
                    "provider_run_completed_digest",
                    "provider run-completed receipt",
                ),
                (
                    "mapper_return_artifact",
                    "mapper_return_artifact_digest",
                    "mapper return artifact",
                ),
                ("resume_receipt_path", "resume_receipt_digest", "resume receipt"),
            ]
        )
    elif kind == "deep_research_inactive_control":
        path_digest_pairs.extend(
            [
                (
                    "capability_state_export_path",
                    "capability_state_export_digest",
                    "capability-state export",
                ),
                (
                    "continuation_artifact",
                    "continuation_artifact_digest",
                    "Deep Research continuation",
                ),
            ]
        )
    else:
        raise CorpusViolation("retrieval_durable_schema", kind)

    bound: dict[str, dict[str, Any]] = {}
    normalized_paths: list[str] = []
    for path_field, digest_field, label in path_digest_pairs:
        normalized_paths.append(str(receipt.get(path_field, "")).replace("\\", "/"))
        bound[path_field] = bound_mapping(
            receipt.get(path_field),
            receipt.get(digest_field),
            root=root,
            code="retrieval_durable_binding",
            label=f"{receipt_id}: {label}",
        )
    evidence_artifact_digests: dict[str, str] = {}
    evidence_artifact_ids: list[str] = []
    if kind == "deep_research_completed":
        evidence_artifacts = receipt.get("evidence_artifacts")
        require(
            isinstance(evidence_artifacts, list) and bool(evidence_artifacts),
            "retrieval_durable_binding",
            f"{receipt_id}: evidence artifacts are missing",
        )
        for entry in evidence_artifacts:
            require(
                isinstance(entry, dict)
                and set(entry) == {"artifact_id", "path", "sha256"}
                and isinstance(entry.get("artifact_id"), str)
                and bool(entry["artifact_id"].strip()),
                "retrieval_durable_binding",
                f"{receipt_id}: evidence artifact entry",
            )
            evidence_path = str(entry.get("path", "")).replace("\\", "/")
            evidence_document = bound_mapping(
                evidence_path,
                entry.get("sha256"),
                root=root,
                code="retrieval_durable_binding",
                label=f"{receipt_id}: evidence artifact {entry.get('artifact_id')}",
            )
            require(
                evidence_document.get("schema_version") == 1
                and evidence_document.get("artifact_type")
                == "deep_research_evidence_artifact"
                and evidence_document.get("artifact_id") == entry["artifact_id"]
                and evidence_document.get("task_id") == receipt.get("task_id")
                and evidence_document.get("plugin_version")
                == receipt.get("plugin_version")
                and evidence_document.get("deep_research_session_id")
                == receipt.get("deep_research_session_id")
                and evidence_document.get("deep_research_run_id")
                == receipt.get("deep_research_run_id"),
                "retrieval_durable_binding",
                f"{receipt_id}: evidence artifact identity mismatch",
            )
            normalized_paths.append(evidence_path)
            evidence_artifact_ids.append(entry["artifact_id"])
            evidence_artifact_digests[evidence_path] = str(entry["sha256"])
        require(
            len(evidence_artifact_ids) == len(set(evidence_artifact_ids))
            and len(evidence_artifact_digests) == len(evidence_artifacts),
            "retrieval_durable_binding",
            f"{receipt_id}: evidence artifact IDs or paths are reused",
        )
    require(
        len(normalized_paths) == len(set(normalized_paths)),
        "retrieval_durable_binding",
        f"{receipt_id}: durable evidence files must be distinct",
    )

    platform_export = bound["platform_receipt_or_export_path"]
    platform_export_path = root / str(
        receipt.get("platform_receipt_or_export_path", "")
    ).replace("\\", "/")
    expected_bound_digests = {
        path_field: receipt[digest_field]
        for path_field, digest_field, _ in path_digest_pairs
        if path_field != "platform_receipt_or_export_path"
    }
    require(platform_export.get("schema_version") == 1, "retrieval_durable_binding", f"{receipt_id}: export schema")
    require(
        platform_export.get("provider_surface") in {"codex", "chatgpt"}
        and platform_export.get("export_id")
        == receipt.get("platform_receipt_or_export_id")
        and platform_export.get("receipt_id") == receipt_id
        and platform_export.get("kind") == kind
        and platform_export.get("task_id") == receipt.get("task_id")
        and platform_export.get("plugin_version") == receipt.get("plugin_version")
        and platform_export.get("query_or_request_digest")
        == receipt.get("query_or_request_digest")
        and platform_export.get("provider_verifier_adapter")
        == receipt.get("provider_verifier_adapter")
        and platform_export.get("bound_digests") == expected_bound_digests
        and platform_export.get("evidence_artifact_digests", {})
        == evidence_artifact_digests,
        "retrieval_durable_binding",
        f"{receipt_id}: platform export identity/binding mismatch",
    )
    require(
        parse_timestamp(platform_export.get("captured_at"), receipt_id)
        == parse_timestamp(receipt.get("captured_at"), receipt_id),
        "retrieval_durable_binding",
        f"{receipt_id}: platform export timestamp mismatch",
    )
    for field in SOURCE_IDENTITY_FIELDS:
        require(
            platform_export.get(field) == receipt.get(field),
            "phase8_source_identity",
            f"{receipt_id}: platform export {field}",
        )
    validate_provider_trust_anchor(
        receipt,
        platform_export,
        platform_export_path,
        root=root,
        synthetic_override=synthetic_override,
    )
    validate_source_identity(
        receipt,
        label=f"retrieval receipt {receipt_id}",
        synthetic_override=synthetic_override,
    )

    raw_field = {
        "search": "raw_search_output_path",
        "deep_research_completed": "raw_deep_research_output_path",
    }.get(kind)
    if raw_field:
        raw_output = bound[raw_field]
        require(
            raw_output.get("kind") == kind
            and raw_output.get("query") == receipt.get("query")
            and raw_output.get("opened_sources") == receipt.get("opened_sources")
            and raw_output.get("material_claim_trace")
            == receipt.get("material_claim_trace"),
            "retrieval_durable_binding",
            f"{receipt_id}: raw output differs from receipt",
        )
        citation_export = bound["citation_export_path"]
        require(
            citation_export.get("opened_sources") == receipt.get("opened_sources")
            and citation_export.get("material_claim_trace")
            == receipt.get("material_claim_trace"),
            "retrieval_durable_binding",
            f"{receipt_id}: citation export differs from receipt",
        )

    if kind == "deep_research_completed":
        handoff = bound["handoff_artifact"]
        user_start = bound["user_start_event_path"]
        provider_completed = bound["provider_run_completed_path"]
        mapper_return = bound["mapper_return_artifact"]
        resume = bound["resume_receipt_path"]
        workflow_id = handoff.get("workflow_id")
        pending_edge_id = handoff.get("pending_edge_id")
        session_id = receipt.get("deep_research_session_id")
        deep_run_id = receipt.get("deep_research_run_id")
        provider_completed_receipt_id = receipt.get(
            "provider_run_completed_receipt_id"
        )
        mapper_receipt_id = receipt.get("mapper_return_receipt_id")
        resume_transaction_id = receipt.get("resume_transaction_id")
        require(
            handoff.get("artifact_type") == "deep_research_handoff"
            and handoff.get("handoff_status") == "deep_research_handoff_required"
            and bool(workflow_id)
            and bool(pending_edge_id),
            "retrieval_durable_binding",
            f"{receipt_id}: invalid Deep Research handoff",
        )
        require(
            user_start.get("artifact_type")
            == "deep_research_user_start_event"
            and user_start.get("initiated_by") == "user"
            and user_start.get("deep_research_session_id") == session_id
            and user_start.get("deep_research_run_id") == deep_run_id
            and user_start.get("workflow_id") == workflow_id
            and user_start.get("pending_edge_id") == pending_edge_id
            and user_start.get("handoff_artifact_digest")
            == receipt.get("handoff_artifact_digest"),
            "retrieval_durable_binding",
            f"{receipt_id}: missing user-started Deep Research event",
        )
        require(
            provider_completed.get("schema_version") == 1
            and provider_completed.get("artifact_type")
            == "deep_research_provider_run_completed_receipt"
            and provider_completed.get("status") == "completed"
            and provider_completed.get("provider_run_completed_receipt_id")
            == provider_completed_receipt_id
            and provider_completed.get("deep_research_session_id") == session_id
            and provider_completed.get("deep_research_run_id") == deep_run_id
            and provider_completed.get("workflow_id") == workflow_id
            and provider_completed.get("pending_edge_id") == pending_edge_id
            and provider_completed.get("user_start_event_digest")
            == receipt.get("user_start_event_digest")
            and provider_completed.get("raw_deep_research_output_digest")
            == receipt.get("raw_deep_research_output_digest"),
            "retrieval_durable_binding",
            f"{receipt_id}: invalid provider run-completed receipt",
        )
        require(
            mapper_return.get("artifact_type") == "mapper_return"
            and mapper_return.get("return_status") == "deep_research_return_completed"
            and mapper_return.get("workflow_id") == workflow_id
            and mapper_return.get("pending_edge_id") == pending_edge_id
            and mapper_return.get("deep_research_session_id") == session_id
            and mapper_return.get("deep_research_run_id") == deep_run_id
            and mapper_return.get("mapper_return_receipt_id") == mapper_receipt_id
            and mapper_return.get("provider_run_completed_receipt_id")
            == provider_completed_receipt_id
            and mapper_return.get("provider_run_completed_digest")
            == receipt.get("provider_run_completed_digest")
            and mapper_return.get("handoff_artifact_digest")
            == receipt.get("handoff_artifact_digest")
            and mapper_return.get("evidence_artifact_ids")
            == evidence_artifact_ids
            and mapper_return.get("evidence_artifacts")
            == receipt.get("evidence_artifacts"),
            "retrieval_durable_binding",
            f"{receipt_id}: invalid mapper return",
        )
        require(
            resume.get("artifact_type") == "workflow_resume_receipt"
            and resume.get("resume_status") == "resumed"
            and resume.get("resume_count") == 1
            and resume.get("workflow_id") == workflow_id
            and resume.get("pending_edge_id") == pending_edge_id
            and resume.get("resume_transaction_id") == resume_transaction_id
            and resume.get("deep_research_session_id") == session_id
            and resume.get("deep_research_run_id") == deep_run_id
            and resume.get("mapper_return_receipt_id") == mapper_receipt_id
            and resume.get("provider_run_completed_receipt_id")
            == provider_completed_receipt_id
            and resume.get("provider_run_completed_digest")
            == receipt.get("provider_run_completed_digest")
            and resume.get("evidence_artifact_ids") == evidence_artifact_ids
            and resume.get("evidence_artifacts")
            == receipt.get("evidence_artifacts")
            and resume.get("handoff_artifact_digest")
            == receipt.get("handoff_artifact_digest")
            and resume.get("mapper_return_artifact_digest")
            == receipt.get("mapper_return_artifact_digest")
            and resume.get("resumed_from_state") == "deep_research_handoff_required"
            and resume.get("resumed_to_state") == "preprocessing",
            "retrieval_durable_binding",
            f"{receipt_id}: invalid or non-unique resume receipt",
        )
        validate_deep_research_evidence_linkage(
            receipt,
            mapper_return,
            resume,
            evidence_artifact_ids,
            receipt_id,
        )
        validate_deep_research_event_order(
            handoff,
            user_start,
            provider_completed,
            mapper_return,
            resume,
            receipt.get("captured_at"),
            receipt_id,
        )
        require(
            platform_export.get("deep_research_session_id") == session_id
            and platform_export.get("deep_research_run_id") == deep_run_id
            and platform_export.get("user_initiated") is True
            and platform_export.get("provider_run_completed_receipt_id")
            == provider_completed_receipt_id
            and platform_export.get("mapper_return_receipt_id")
            == mapper_receipt_id
            and platform_export.get("resume_transaction_id")
            == resume_transaction_id,
            "retrieval_durable_binding",
            f"{receipt_id}: platform cycle identity mismatch",
        )
        raw_deep_research = bound["raw_deep_research_output_path"]
        require(
            receipt.get("resumed_pending_edge") == pending_edge_id
            and raw_deep_research.get("deep_research_session_id") == session_id
            and raw_deep_research.get("deep_research_run_id") == deep_run_id
            and raw_deep_research.get("provider_run_completed_receipt_id")
            == provider_completed_receipt_id,
            "retrieval_durable_binding",
            f"{receipt_id}: pending-edge resume binding mismatch",
        )
        required_artifact_paths = {
            str(receipt.get("handoff_artifact")).replace("\\", "/"),
            str(receipt.get("user_start_event_path")).replace("\\", "/"),
            str(receipt.get("provider_run_completed_path")).replace("\\", "/"),
            str(receipt.get("mapper_return_artifact")).replace("\\", "/"),
            str(receipt.get("resume_receipt_path")).replace("\\", "/"),
            *evidence_artifact_digests,
        }
        require(
            required_artifact_paths
            <= {str(path).replace("\\", "/") for path in receipt.get("artifact_paths", [])},
            "retrieval_durable_binding",
            f"{receipt_id}: Deep Research lineage artifacts are not indexed",
        )
    elif kind == "deep_research_inactive_control":
        capability = bound["capability_state_export_path"]
        continuation = bound["continuation_artifact"]
        require(
            capability.get("capability") == "deep_research"
            and capability.get("capability_active") is False
            and capability.get("task_id") == receipt.get("task_id")
            and capability.get("plugin_version") == receipt.get("plugin_version"),
            "retrieval_durable_binding",
            f"{receipt_id}: invalid capability-state export",
        )
        require(
            continuation.get("handoff_status") == "deep_research_handoff_required"
            and continuation.get("plugin_version") == receipt.get("plugin_version")
            and continuation.get("task_id") == receipt.get("task_id"),
            "retrieval_durable_binding",
            f"{receipt_id}: invalid continuation artifact",
        )


def build_durable_retrieval_self_test(
    root: Path, kind: str, schema: dict[str, Any], current_version: str
) -> dict[str, Any]:
    captured_dt = datetime.now(timezone.utc).replace(microsecond=0)
    captured_at = captured_dt.isoformat()
    identity = current_contract_identity()
    receipt_id = f"durable-self-test-{kind}"
    task_id = f"task-{receipt_id}"
    query = f"Synthetic durable retrieval query for {kind}"
    query_digest = "sha256:" + hashlib.sha256(query.encode("utf-8")).hexdigest()
    sources = [] if kind == "deep_research_inactive_control" else [
        {
            "source_id": f"{receipt_id}-source-1",
            "url": "https://example.invalid/primary-1",
            "primary_or_authoritative": True,
            "identity_verified": True,
        },
        {
            "source_id": f"{receipt_id}-source-2",
            "url": "https://example.invalid/primary-2",
            "primary_or_authoritative": True,
            "identity_verified": True,
        },
    ]
    traces = [] if not sources else [
        {
            "claim_id": f"{receipt_id}-claim-1",
            "source_ids": [source["source_id"] for source in sources],
        }
    ]
    contract = schema["completion_contracts"][kind]
    receipt: dict[str, Any] = {
        "receipt_id": receipt_id,
        "kind": kind,
        "capability": (
            "chatgpt_codex_builtin_search"
            if kind == "search"
            else "chatgpt_deep_research"
        ),
        "question_class": "current" if kind == "search" else "broad_synthesis",
        "expected_completion_status": contract["expected_status"],
        "evidence_status": "verified_live_evidence",
        "verification_level": "durable_platform_provenance",
        "query": query,
        "query_or_request_digest": query_digest,
        "captured_at": captured_at,
        "plugin_version": current_version,
        "task_id": task_id,
        "opened_sources": sources,
        "material_claim_trace": traces,
        "artifact_paths": [],
        "artifact_digests": [],
        "platform_receipt_or_export_id": f"platform-export-{receipt_id}",
        "provider_verifier_adapter": SYNTHETIC_PROVIDER_ADAPTER_ID,
        **identity,
    }

    bound_digests: dict[str, str] = {}
    platform_cycle_fields: dict[str, Any] = {}
    if kind == "search":
        result_path, result_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-result.yaml",
            {
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
                "question_class": "current",
                "route": "chatgpt_codex_builtin_search",
                "opened_sources": sources,
                "material_claims": [{"claim_id": traces[0]["claim_id"]}],
            },
        )
        raw_path, raw_digest = write_temp_mapping(
            root,
            f"exports/{receipt_id}-raw-search.yaml",
            {
                "kind": kind,
                "query": query,
                "opened_sources": sources,
                "material_claim_trace": traces,
            },
        )
        citation_path, citation_digest = write_temp_mapping(
            root,
            f"exports/{receipt_id}-citations.yaml",
            {"opened_sources": sources, "material_claim_trace": traces},
        )
        receipt.update(
            {
                "artifact_paths": [result_path],
                "artifact_digests": [result_digest],
                "raw_search_output_path": raw_path,
                "raw_search_output_digest": raw_digest,
                "citation_export_path": citation_path,
                "citation_export_digest": citation_digest,
            }
        )
        bound_digests = {
            "raw_search_output_path": raw_digest,
            "citation_export_path": citation_digest,
        }
    elif kind == "deep_research_completed":
        workflow_id = f"workflow-{receipt_id}"
        edge_id = f"pending-edge-{receipt_id}"
        session_id = f"deep-research-session-{receipt_id}"
        deep_run_id = f"deep-research-run-{receipt_id}"
        provider_completed_receipt_id = f"provider-run-completed-{receipt_id}"
        mapper_receipt_id = f"mapper-return-receipt-{receipt_id}"
        resume_transaction_id = f"resume-transaction-{receipt_id}"
        handoff_path, handoff_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-handoff.yaml",
            {
                "artifact_type": "deep_research_handoff",
                "handoff_status": "deep_research_handoff_required",
                "workflow_id": workflow_id,
                "pending_edge_id": edge_id,
                "event_at": (captured_dt - timedelta(minutes=5)).isoformat(),
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        user_start_path, user_start_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-user-start.yaml",
            {
                "artifact_type": "deep_research_user_start_event",
                "initiated_by": "user",
                "deep_research_session_id": session_id,
                "deep_research_run_id": deep_run_id,
                "workflow_id": workflow_id,
                "pending_edge_id": edge_id,
                "handoff_artifact_digest": handoff_digest,
                "event_at": (captured_dt - timedelta(minutes=4)).isoformat(),
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        raw_path, raw_digest = write_temp_mapping(
            root,
            f"exports/{receipt_id}-raw-deep-research.yaml",
            {
                "kind": kind,
                "query": query,
                "opened_sources": sources,
                "material_claim_trace": traces,
                "deep_research_session_id": session_id,
                "deep_research_run_id": deep_run_id,
                "provider_run_completed_receipt_id": provider_completed_receipt_id,
            },
        )
        provider_completed_path, provider_completed_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-provider-run-completed.yaml",
            {
                "schema_version": 1,
                "artifact_type": "deep_research_provider_run_completed_receipt",
                "status": "completed",
                "provider_run_completed_receipt_id": provider_completed_receipt_id,
                "deep_research_session_id": session_id,
                "deep_research_run_id": deep_run_id,
                "workflow_id": workflow_id,
                "pending_edge_id": edge_id,
                "user_start_event_digest": user_start_digest,
                "raw_deep_research_output_digest": raw_digest,
                "event_at": (captured_dt - timedelta(minutes=3)).isoformat(),
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        evidence_path, evidence_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-evidence-map.yaml",
            {
                "schema_version": 1,
                "artifact_type": "deep_research_evidence_artifact",
                "artifact_id": f"evidence-{receipt_id}",
                "deep_research_session_id": session_id,
                "deep_research_run_id": deep_run_id,
                "opened_sources": sources,
                "material_claim_trace": traces,
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        evidence_artifacts = [
            {
                "artifact_id": f"evidence-{receipt_id}",
                "path": evidence_path,
                "sha256": evidence_digest,
            }
        ]
        evidence_ids = [item["artifact_id"] for item in evidence_artifacts]
        mapper_path, mapper_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-mapper-return.yaml",
            {
                "artifact_type": "mapper_return",
                "return_status": "deep_research_return_completed",
                "workflow_id": workflow_id,
                "pending_edge_id": edge_id,
                "deep_research_session_id": session_id,
                "deep_research_run_id": deep_run_id,
                "mapper_return_receipt_id": mapper_receipt_id,
                "provider_run_completed_receipt_id": provider_completed_receipt_id,
                "provider_run_completed_digest": provider_completed_digest,
                "handoff_artifact_digest": handoff_digest,
                "evidence_artifact_ids": evidence_ids,
                "evidence_artifacts": evidence_artifacts,
                "event_at": (captured_dt - timedelta(minutes=2)).isoformat(),
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        resume_path, resume_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-resume.yaml",
            {
                "artifact_type": "workflow_resume_receipt",
                "resume_status": "resumed",
                "resume_count": 1,
                "workflow_id": workflow_id,
                "pending_edge_id": edge_id,
                "resume_transaction_id": resume_transaction_id,
                "deep_research_session_id": session_id,
                "deep_research_run_id": deep_run_id,
                "mapper_return_receipt_id": mapper_receipt_id,
                "provider_run_completed_receipt_id": provider_completed_receipt_id,
                "provider_run_completed_digest": provider_completed_digest,
                "evidence_artifact_ids": evidence_ids,
                "evidence_artifacts": evidence_artifacts,
                "handoff_artifact_digest": handoff_digest,
                "mapper_return_artifact_digest": mapper_digest,
                "resumed_from_state": "deep_research_handoff_required",
                "resumed_to_state": "preprocessing",
                "event_at": (captured_dt - timedelta(minutes=1)).isoformat(),
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        citation_path, citation_digest = write_temp_mapping(
            root,
            f"exports/{receipt_id}-citations.yaml",
            {"opened_sources": sources, "material_claim_trace": traces},
        )
        receipt.update(
            {
                "artifact_paths": [
                    handoff_path,
                    user_start_path,
                    provider_completed_path,
                    evidence_path,
                    mapper_path,
                    resume_path,
                ],
                "artifact_digests": [
                    handoff_digest,
                    user_start_digest,
                    provider_completed_digest,
                    evidence_digest,
                    mapper_digest,
                    resume_digest,
                ],
                "handoff_artifact": handoff_path,
                "handoff_artifact_digest": handoff_digest,
                "user_start_event_path": user_start_path,
                "user_start_event_digest": user_start_digest,
                "deep_research_session_id": session_id,
                "deep_research_run_id": deep_run_id,
                "provider_run_completed_receipt_id": provider_completed_receipt_id,
                "provider_run_completed_path": provider_completed_path,
                "provider_run_completed_digest": provider_completed_digest,
                "provider_run_completed_status": "completed",
                "evidence_artifacts": evidence_artifacts,
                "mapper_return_artifact": mapper_path,
                "mapper_return_artifact_digest": mapper_digest,
                "mapper_return_receipt_id": mapper_receipt_id,
                "resumed_pending_edge": edge_id,
                "resume_receipt_path": resume_path,
                "resume_receipt_digest": resume_digest,
                "resume_transaction_id": resume_transaction_id,
                "raw_deep_research_output_path": raw_path,
                "raw_deep_research_output_digest": raw_digest,
                "citation_export_path": citation_path,
                "citation_export_digest": citation_digest,
            }
        )
        bound_digests = {
            "raw_deep_research_output_path": raw_digest,
            "citation_export_path": citation_digest,
            "handoff_artifact": handoff_digest,
            "user_start_event_path": user_start_digest,
            "provider_run_completed_path": provider_completed_digest,
            "mapper_return_artifact": mapper_digest,
            "resume_receipt_path": resume_digest,
        }
        platform_cycle_fields = {
            "deep_research_session_id": session_id,
            "deep_research_run_id": deep_run_id,
            "user_initiated": True,
            "provider_run_completed_receipt_id": provider_completed_receipt_id,
            "mapper_return_receipt_id": mapper_receipt_id,
            "resume_transaction_id": resume_transaction_id,
            "evidence_artifact_digests": {evidence_path: evidence_digest},
        }
    else:
        continuation_path, continuation_digest = write_temp_mapping(
            root,
            f"artifacts/{receipt_id}-continuation.yaml",
            {
                "handoff_status": "deep_research_handoff_required",
                "workflow_id": f"workflow-{receipt_id}",
                "pending_edge_id": f"pending-edge-{receipt_id}",
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        capability_path, capability_digest = write_temp_mapping(
            root,
            f"exports/{receipt_id}-capability.yaml",
            {
                "capability": "deep_research",
                "capability_active": False,
                "provider_surface": "codex",
                "plugin_version": current_version,
                "task_id": task_id,
                "captured_at": captured_at,
            },
        )
        receipt.update(
            {
                "artifact_paths": [continuation_path],
                "artifact_digests": [continuation_digest],
                "capability_active": False,
                "workflow_paused": True,
                "downstream_evidence_map_created": False,
                "continuation_artifact": continuation_path,
                "continuation_artifact_digest": continuation_digest,
                "capability_state_export_path": capability_path,
                "capability_state_export_digest": capability_digest,
            }
        )
        bound_digests = {
            "capability_state_export_path": capability_digest,
            "continuation_artifact": continuation_digest,
        }

    platform_path, platform_digest = write_temp_mapping(
        root,
        f"exports/{receipt_id}-platform-export.yaml",
        {
            "schema_version": 1,
            "provider_surface": "codex",
            "provider_verifier_adapter": SYNTHETIC_PROVIDER_ADAPTER_ID,
            "synthetic_test_only": True,
            "export_id": receipt["platform_receipt_or_export_id"],
            "receipt_id": receipt_id,
            "kind": kind,
            "task_id": task_id,
            "plugin_version": current_version,
            "captured_at": captured_at,
            "query_or_request_digest": query_digest,
            "bound_digests": bound_digests,
            **platform_cycle_fields,
            **identity,
        },
    )
    receipt["platform_receipt_or_export_path"] = platform_path
    receipt["platform_receipt_or_export_digest"] = platform_digest
    return receipt


def validate_retrieval_durable_negative_guards(
    schema: dict[str, Any], current_version: str
) -> list[dict[str, str]]:
    policy = schema.get("verification_policy", {})
    durable_class = policy.get("verified_evidence_class")
    common_fields = policy.get("verified_live_common_required", [])
    kind_fields = policy.get("verified_live_kind_required", {})
    require(isinstance(durable_class, str) and bool(durable_class), "retrieval_durable_schema", "evidence class")
    require(isinstance(kind_fields, dict), "retrieval_durable_schema", "kind fields")
    results: list[dict[str, str]] = []

    def expect_rejection(
        probe_id: str,
        candidate: dict[str, Any],
        expected_codes: set[str],
        *,
        root: Path,
    ) -> None:
        try:
            validate_verified_retrieval_provenance(
                candidate,
                schema,
                str(durable_class),
                root=root,
                synthetic_override=True,
            )
        except CorpusViolation as exc:
            require(
                exc.code in expected_codes,
                "retrieval_durable_guard_wrong_error",
                f"{probe_id}: {exc.code}",
            )
            results.append(
                {
                    "probe_id": f"{probe_id}-rejected",
                    "status": "rejected",
                    "error_code": exc.code,
                }
            )
        else:
            raise CorpusViolation("retrieval_durable_guard_accepted", probe_id)

    label_only = {
        "receipt_id": "label-only-promotion",
        "kind": "search",
        "query": "label-only promotion must fail",
        "evidence_status": "verified_live_evidence",
        "verification_level": "durable_platform_provenance",
    }
    with tempfile.TemporaryDirectory(prefix="phase8-retrieval-durable-") as temp:
        root = Path(temp)
        expect_rejection(
            "label-only-promotion",
            label_only,
            {"retrieval_durable_provenance"},
            root=root,
        )
        for kind, specific_fields in sorted(kind_fields.items()):
            require(isinstance(specific_fields, list) and bool(specific_fields), "retrieval_durable_schema", str(kind))
            complete = build_durable_retrieval_self_test(
                root, kind, schema, current_version
            )
            validate_populated_retrieval_receipt(
                complete,
                schema["completion_contracts"][kind],
                current_version,
                int(schema["freshness_days"]),
                root=root,
            )
            validate_verified_retrieval_provenance(
                complete,
                schema,
                str(durable_class),
                root=root,
                synthetic_override=True,
            )
            try:
                validate_verified_retrieval_provenance(
                    complete, schema, str(durable_class), root=root
                )
            except CorpusViolation as exc:
                require(
                    exc.code == "provider_trust_anchor_unavailable",
                    "provider_synthetic_override_guard",
                    f"{kind}: unexpected real-evidence rejection {exc.code}",
                )
            else:
                raise CorpusViolation(
                    "provider_synthetic_override_guard",
                    f"{kind}: ephemeral synthetic export counted as runtime evidence",
                )
            for field in [*common_fields, *specific_fields]:
                candidate = copy.deepcopy(complete)
                candidate.pop(field, None)
                expect_rejection(
                    f"{kind}-missing-{field}",
                    candidate,
                    {"retrieval_durable_provenance"},
                    root=root,
                )

            candidate = copy.deepcopy(complete)
            candidate["query_or_request_digest"] = "sha256:" + "0" * 64
            expect_rejection(
                f"{kind}-query-digest-mismatch",
                candidate,
                {"retrieval_durable_query_binding"},
                root=root,
            )
            candidate = copy.deepcopy(complete)
            candidate["platform_receipt_or_export_digest"] = "sha256:" + "1" * 64
            expect_rejection(
                f"{kind}-platform-export-digest-mismatch",
                candidate,
                {"retrieval_durable_binding"},
                root=root,
            )
            candidate = copy.deepcopy(complete)
            candidate["task_id"] = "different-task"
            expect_rejection(
                f"{kind}-platform-export-identity-mismatch",
                candidate,
                {"retrieval_durable_binding"},
                root=root,
            )

            if kind == "search":
                candidate = copy.deepcopy(complete)
                candidate["raw_search_output_digest"] = "sha256:" + "2" * 64
                expect_rejection(
                    "search-raw-output-digest-mismatch",
                    candidate,
                    {"retrieval_durable_binding"},
                    root=root,
                )
            elif kind == "deep_research_completed":
                candidate = copy.deepcopy(complete)
                candidate["mapper_return_artifact"] = candidate["handoff_artifact"]
                candidate["mapper_return_artifact_digest"] = candidate[
                    "handoff_artifact_digest"
                ]
                expect_rejection(
                    "deep-research-reused-handoff-as-return",
                    candidate,
                    {"retrieval_durable_binding"},
                    root=root,
                )
                candidate = copy.deepcopy(complete)
                candidate["resumed_pending_edge"] = "different-pending-edge"
                expect_rejection(
                    "deep-research-fake-resume-edge",
                    candidate,
                    {"retrieval_durable_binding"},
                    root=root,
                )
            else:
                candidate = copy.deepcopy(complete)
                candidate["capability_state_export_digest"] = "sha256:" + "3" * 64
                expect_rejection(
                    "deep-research-inactive-capability-digest-mismatch",
                    candidate,
                    {"retrieval_durable_binding"},
                    root=root,
                )
    return results


def validate_deep_research_semantic_negative_guards(
    schema: dict[str, Any], current_version: str
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []

    def record_rejection(mutation: str, exc: CorpusViolation, code: str) -> None:
        require(
            exc.code == code,
            "deep_research_semantic_guard_wrong_error",
            f"{mutation}: {exc.code}",
        )
        results.append(
            {"mutation": mutation, "status": "rejected", "error_code": exc.code}
        )

    with tempfile.TemporaryDirectory(prefix="phase8-deep-semantic-") as temp:
        root = Path(temp)
        baseline = build_durable_retrieval_self_test(
            root, "deep_research_completed", schema, current_version
        )
        contract = schema["completion_contracts"]["deep_research_completed"]

        for mutation, mutate, expected_code in (
            (
                "deep_source_not_authoritative",
                lambda candidate: candidate["opened_sources"][0].update(
                    {"primary_or_authoritative": False}
                ),
                "retrieval_source_authority",
            ),
            (
                "deep_source_identity_unverified",
                lambda candidate: candidate["opened_sources"][0].update(
                    {"identity_verified": False}
                ),
                "retrieval_source_identity",
            ),
            (
                "deep_material_claim_trace_omits_opened_source",
                lambda candidate: candidate["material_claim_trace"][0].update(
                    {
                        "source_ids": [
                            candidate["opened_sources"][0]["source_id"]
                        ]
                    }
                ),
                "retrieval_claim_trace",
            ),
        ):
            candidate = copy.deepcopy(baseline)
            mutate(candidate)
            try:
                validate_populated_retrieval_receipt(
                    candidate,
                    contract,
                    current_version,
                    int(schema["freshness_days"]),
                    root=root,
                )
            except CorpusViolation as exc:
                record_rejection(mutation, exc, expected_code)
            else:
                raise CorpusViolation(
                    "deep_research_semantic_guard_accepted", mutation
                )

        unbound_evidence = copy.deepcopy(baseline)
        unbound_evidence["evidence_artifacts"][0]["sha256"] = (
            "sha256:" + "0" * 64
        )
        try:
            validate_verified_retrieval_provenance(
                unbound_evidence,
                schema,
                str(schema["verification_policy"]["verified_evidence_class"]),
                root=root,
                synthetic_override=True,
            )
        except CorpusViolation as exc:
            record_rejection(
                "deep_evidence_artifact_digest_unbound",
                exc,
                "retrieval_durable_binding",
            )
        else:
            raise CorpusViolation(
                "deep_research_semantic_guard_accepted",
                "deep_evidence_artifact_digest_unbound",
            )

        mapper_return = load_yaml(root / baseline["mapper_return_artifact"])
        resume = load_yaml(root / baseline["resume_receipt_path"])
        mismatched_mapper = copy.deepcopy(mapper_return)
        mismatched_mapper["evidence_artifact_ids"] = ["different-evidence"]
        try:
            validate_deep_research_evidence_linkage(
                baseline,
                mismatched_mapper,
                resume,
                [item["artifact_id"] for item in baseline["evidence_artifacts"]],
                "deep-evidence-linkage-probe",
            )
        except CorpusViolation as exc:
            record_rejection(
                "mapper_return_resume_evidence_set_mismatch",
                exc,
                "retrieval_durable_binding",
            )
        else:
            raise CorpusViolation(
                "deep_research_semantic_guard_accepted",
                "mapper_return_resume_evidence_set_mismatch",
            )

        failed_provider = copy.deepcopy(baseline)
        failed_provider["provider_run_completed_status"] = "failed"
        try:
            validate_verified_retrieval_provenance(
                failed_provider,
                schema,
                str(schema["verification_policy"]["verified_evidence_class"]),
                root=root,
                synthetic_override=True,
            )
        except CorpusViolation as exc:
            record_rejection(
                "provider_run_completed_status_not_completed",
                exc,
                "retrieval_durable_provenance",
            )
        else:
            raise CorpusViolation(
                "deep_research_semantic_guard_accepted",
                "provider_run_completed_status_not_completed",
            )

        handoff = load_yaml(root / baseline["handoff_artifact"])
        user_start = load_yaml(root / baseline["user_start_event_path"])
        provider_completed = load_yaml(
            root / baseline["provider_run_completed_path"]
        )
        nonmonotonic_provider = copy.deepcopy(provider_completed)
        nonmonotonic_provider["event_at"] = mapper_return["event_at"]
        try:
            validate_deep_research_event_order(
                handoff,
                user_start,
                nonmonotonic_provider,
                mapper_return,
                resume,
                baseline["captured_at"],
                "deep-event-order-probe",
            )
        except CorpusViolation as exc:
            record_rejection(
                "provider_completion_not_before_mapper_return",
                exc,
                "retrieval_durable_binding",
            )
        else:
            raise CorpusViolation(
                "deep_research_semantic_guard_accepted",
                "provider_completion_not_before_mapper_return",
            )
    return results


def validate_retrieval_receipts(current_version: str) -> dict[str, Any]:
    schema = load_yaml(RETRIEVAL_SCHEMA_PATH)
    data = load_yaml(RETRIEVAL_RECEIPTS_PATH)
    require(schema.get("schema_version") == data.get("schema_version") == 1, "retrieval_schema", "schema version")
    require(
        schema.get("freshness_days") == EVIDENCE_FRESHNESS_DAYS,
        "retrieval_schema",
        "reviewer and retrieval freshness windows must agree",
    )
    require(
        schema.get("provider_verifier_registry")
        == "tests/openai_phase8/provider-verifier-registry.yaml",
        "retrieval_schema",
        "provider verifier registry binding",
    )
    require(
        data.get("evidence_class")
        in {
            "live_receipt_placeholders",
            "self_attested_current_task_snapshots_and_pending_placeholders",
            "durable_platform_retrieval_receipts",
        },
        "retrieval_evidence_class",
        str(data.get("evidence_class")),
    )
    durable_missing = {
        "executable_provider_verifier_adapter",
        "authenticated_platform_export",
        "source_commit_and_plugin_tree_identity",
        "provider_attested_source_and_citation_provenance",
        "deep_research_session_run_and_event_receipts",
        "provider_run_completed_receipt",
        "evidence_artifact_path_digest_bindings",
        "deep_research_authoritative_source_traceability",
    }
    if data.get("evidence_class") == "durable_platform_retrieval_receipts":
        require(
            data.get("durable_verification_missing") == [],
            "retrieval_durable_provenance",
            "durable collection still declares missing provenance",
        )
    else:
        require(
            set(data.get("durable_verification_missing", [])) == durable_missing,
            "retrieval_durable_provenance",
            "missing durable-evidence declaration",
        )
    receipts = data.get("receipts", [])
    require(len(receipts) == 6, "retrieval_receipt_count", str(len(receipts)))
    ids = [receipt.get("receipt_id") for receipt in receipts]
    require(len(ids) == len(set(ids)) and all(ids), "retrieval_receipt_id", "duplicate or missing")
    contracts = schema.get("completion_contracts", {})
    counts = Counter(receipt.get("kind") for receipt in receipts)
    require(set(counts) == set(contracts), "retrieval_kind", str(counts))
    for kind, contract in contracts.items():
        require(counts[kind] == contract["count"], "retrieval_kind_count", f"{kind}: {counts[kind]}")
    require(
        {receipt["question_class"] for receipt in receipts if receipt["kind"] == "search"}
        == {"current", "exact", "narrow_academic"},
        "search_question_classes",
        "current/exact/narrow_academic required",
    )

    allowed_statuses = set(schema.get("allowed_evidence_statuses", []))
    required_fields = set(schema.get("common_required", []))
    pending = 0
    completed = 0
    completed_by_kind: Counter[str] = Counter()
    observed = 0
    observed_by_kind: Counter[str] = Counter()
    stale = 0
    verified_current_receipts: list[dict[str, Any]] = []
    results = []
    for receipt in receipts:
        receipt_id = receipt["receipt_id"]
        missing = required_fields - set(receipt)
        require(not missing, "retrieval_receipt_schema", f"{receipt_id}: {sorted(missing)}")
        status = receipt.get("evidence_status")
        require(status in allowed_statuses, "retrieval_evidence_status", receipt_id)
        verification_level = receipt.get("verification_level")
        contract = contracts[receipt["kind"]]
        require(receipt.get("expected_completion_status") == contract["expected_status"], "retrieval_expected_status", receipt_id)
        if status == "pending_live_evidence":
            pending += 1
            require(verification_level == "none", "retrieval_verification_level", receipt_id)
            require(
                any(not receipt.get(field) for field in ("captured_at", "plugin_version", "task_id", "artifact_digests")),
                "retrieval_pending_has_complete_evidence",
                receipt_id,
            )
            result_status = "pending_live_evidence"
        else:
            require(
                verification_level
                in {"self_attested_current_task_snapshot", "durable_platform_provenance"},
                "retrieval_verification_level",
                receipt_id,
            )
            result_status = validate_populated_retrieval_receipt(
                receipt, contract, current_version, int(schema["freshness_days"])
            )
            if result_status == "stale":
                stale += 1
            elif status == "observed_unverified":
                require(
                    verification_level == "self_attested_current_task_snapshot",
                    "retrieval_observed_verification_level",
                    receipt_id,
                )
                observed += 1
                observed_by_kind[receipt["kind"]] += 1
                result_status = "observed_unverified"
            else:
                require(
                    status == "verified_live_evidence"
                    and verification_level == "durable_platform_provenance",
                    "retrieval_verified_provenance",
                    receipt_id,
                )
                validate_verified_retrieval_provenance(
                    receipt, schema, str(data.get("evidence_class"))
                )
                completed += 1
                completed_by_kind[receipt["kind"]] += 1
                verified_current_receipts.append(receipt)
        results.append(
            {
                "receipt_id": receipt_id,
                "kind": receipt["kind"],
                "expected_completion_status": receipt["expected_completion_status"],
                "evidence_status": result_status,
                "captured_at": (
                    receipt["captured_at"].isoformat()
                    if isinstance(receipt.get("captured_at"), datetime)
                    else receipt.get("captured_at")
                ),
                "plugin_version": receipt.get("plugin_version"),
                "task_id": receipt.get("task_id"),
                "opened_source_count": len(receipt.get("opened_sources", [])),
                "artifact_digests": receipt.get("artifact_digests", []),
                "artifact_paths": receipt.get("artifact_paths", []),
            }
        )

    export_ids = [
        receipt.get("platform_receipt_or_export_id")
        for receipt in verified_current_receipts
    ]
    require(
        len(export_ids) == len(set(export_ids)),
        "retrieval_durable_cross_receipt_binding",
        "verified receipts reuse a platform export ID",
    )
    indexed_paths = [
        str(path).replace("\\", "/")
        for receipt in verified_current_receipts
        for path in receipt.get("artifact_paths", [])
    ]
    require(
        len(indexed_paths) == len(set(indexed_paths)),
        "retrieval_durable_cross_receipt_binding",
        "verified receipts reuse a lineage artifact",
    )
    resumed_edges = [
        receipt.get("resumed_pending_edge")
        for receipt in verified_current_receipts
        if receipt.get("kind") == "deep_research_completed"
    ]
    require(
        len(resumed_edges) == len(set(resumed_edges)),
        "retrieval_durable_cross_receipt_binding",
        "Deep Research cycles reuse a pending edge",
    )
    verified_deep_research = [
        receipt
        for receipt in verified_current_receipts
        if receipt.get("kind") == "deep_research_completed"
    ]
    for field in (
        "task_id",
        "deep_research_session_id",
        "deep_research_run_id",
        "provider_run_completed_receipt_id",
        "mapper_return_receipt_id",
        "resume_transaction_id",
    ):
        values = [receipt.get(field) for receipt in verified_deep_research]
        require(
            len(values) == len(set(values)) and all(values),
            "retrieval_durable_cross_receipt_binding",
            f"Deep Research cycles reuse or omit {field}",
        )
    evidence_ids = [
        entry.get("artifact_id")
        for receipt in verified_deep_research
        for entry in receipt.get("evidence_artifacts", [])
        if isinstance(entry, dict)
    ]
    evidence_paths = [
        entry.get("path")
        for receipt in verified_deep_research
        for entry in receipt.get("evidence_artifacts", [])
        if isinstance(entry, dict)
    ]
    require(
        len(evidence_ids) == len(set(evidence_ids))
        and len(evidence_paths) == len(set(evidence_paths)),
        "retrieval_durable_cross_receipt_binding",
        "Deep Research cycles reuse evidence artifact IDs or paths",
    )

    # Pending placeholders are valid planning artifacts but never a retrieval pass.
    gate_status = "completed" if completed == len(receipts) and not stale else "pending_live_evidence"
    require(schema.get("pending_policy", {}).get("pending_is_not_pass") is True, "retrieval_pending_policy", "schema")
    require(
        schema.get("verification_policy", {}).get("observed_unverified_is_not_pass") is True,
        "retrieval_verification_policy",
        "schema",
    )
    durable_negative_guards = validate_retrieval_durable_negative_guards(
        schema, current_version
    )
    deep_semantic_negative_guards = (
        validate_deep_research_semantic_negative_guards(schema, current_version)
    )
    return {
        "required_receipt_count": len(receipts),
        "required_distribution": {kind: contracts[kind]["count"] for kind in sorted(contracts)},
        "completed_current_receipts": completed,
        "completed_current_receipts_by_kind": {
            kind: completed_by_kind[kind] for kind in sorted(contracts)
        },
        "observed_unverified_receipts": observed,
        "observed_unverified_receipts_by_kind": {
            kind: observed_by_kind[kind] for kind in sorted(contracts)
        },
        "pending_receipts": pending,
        "stale_receipts": stale,
        "durable_provenance_negative_guard_count": len(durable_negative_guards),
        "durable_provenance_negative_guards": durable_negative_guards,
        "deep_research_semantic_negative_guard_count": len(
            deep_semantic_negative_guards
        ),
        "deep_research_semantic_negative_guards": deep_semantic_negative_guards,
        "provider_verifier_adapter_count": len(real_provider_adapter_ids()),
        "durable_verification_missing": sorted(durable_missing),
        "repository_authored_files_count_as_verified": False,
        "synthetic_provider_override_self_test": {
            "status": "passed",
            "counts_as_runtime_evidence": False,
            "ephemeral_temp_root_required": True,
        },
        "source_identity_binding_required": list(SOURCE_IDENTITY_FIELDS),
        "deep_research_unique_cycle_fields": [
            "task_id",
            "deep_research_session_id",
            "deep_research_run_id",
            "provider_run_completed_receipt_id",
            "mapper_return_receipt_id",
            "resume_transaction_id",
            "resumed_pending_edge",
            "evidence_artifact_id_and_path",
        ],
        "deep_research_event_order": (
            "handoff < user_start < provider_run_completed < mapper_return < resume"
        ),
        "freshness_days": schema["freshness_days"],
        "receipt_results": results,
        "status": gate_status,
    }


def run_all() -> dict[str, Any]:
    current_version = load_current_version()
    validator_self_tests = validate_time_and_identity_self_tests()
    corpus_summary, cases = validate_corpus(current_version)
    repeat_summary = validate_fresh_repeats(cases)
    live_repeat_summary = validate_live_fresh_repeats(
        current_version, cases, repeat_summary["selected_case_ids"]
    )
    repeat_summary["observed_current_task_repeat_snapshots"] = live_repeat_summary[
        "observed_review_snapshot_count"
    ]
    repeat_summary["live_repeat_receipts_completed"] = live_repeat_summary[
        "verified_live_review_count"
    ]
    repeat_summary["live_repeat_gate_status"] = live_repeat_summary[
        "verified_live_gate_status"
    ]
    retrieval_summary = validate_retrieval_receipts(current_version)
    phase_complete = (
        bool(real_provider_adapter_ids())
        and live_repeat_summary["verified_live_gate_status"] == "completed"
        and retrieval_summary["status"] == "completed"
    )
    repeat_summary["status"] = (
        "synthetic_repeat_and_provider_verified_live_gate_completed"
        if live_repeat_summary["verified_live_gate_status"] == "completed"
        else "synthetic_repeat_passed_live_gate_pending_provider_verified_evidence"
    )
    evidence_scope = (
        "synthetic_corpus_plus_provider_verified_current_release_runtime_and_native_research_evidence"
        if phase_complete
        else "synthetic_corpus_plus_self_attested_snapshots_and_pending_provider_verified_runtime_evidence"
    )
    return {
        "schema_version": 1,
        "plugin_version": current_version,
        "evidence_scope": evidence_scope,
        "phase_status": "complete" if phase_complete else "in_progress_live_runtime_evidence_pending",
        "corpus": corpus_summary,
        "fresh_repeat": repeat_summary,
        "live_fresh_repeat": live_repeat_summary,
        "retrieval": retrieval_summary,
        "provider_trust": {
            "real_adapter_count": len(real_provider_adapter_ids()),
            "real_adapter_ids": sorted(real_provider_adapter_ids()),
            "repository_authored_files_are_trust_anchors": False,
            "synthetic_override_counts_as_runtime_evidence": False,
        },
        "validator_self_tests": validator_self_tests,
        "claims": {
            "live_model_runs_performed_by_this_validator": False,
            "live_fresh_evaluator_repeats_counted_as_pass": live_repeat_summary[
                "verified_live_review_count"
            ],
            "self_attested_reviewer_snapshots_observed": live_repeat_summary[
                "observed_review_snapshot_count"
            ],
            "live_search_receipts_counted_as_pass": retrieval_summary[
                "completed_current_receipts_by_kind"
            ]["search"],
            "self_attested_search_snapshots_observed": retrieval_summary[
                "observed_unverified_receipts_by_kind"
            ]["search"],
            "deep_research_cycles_claimed_without_receipts": 0,
            "repository_authored_files_counted_as_verified": False,
            "phase8_complete": phase_complete,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write-report", action="store_true")
    group.add_argument("--check-report", action="store_true")
    args = parser.parse_args()

    result = run_all()
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    if args.check_report:
        require(REPORT_PATH.is_file(), "report_missing", str(REPORT_PATH))
        require(REPORT_PATH.read_text(encoding="utf-8") == rendered, "report_drift", str(REPORT_PATH))

    metrics = result["corpus"]["metrics"]
    repeat = result["fresh_repeat"]
    live_repeat = result["live_fresh_repeat"]
    retrieval = result["retrieval"]
    print("Phase 8 corpus contracts passed")
    print(f"synthetic cases: {result['corpus']['case_count']}/16 minimum")
    print(
        "quality metrics: "
        f"false-ready={metrics['false_ready_count']}; "
        f"fatal recall={metrics['fatal_finding_recall_percent']}%; "
        f"fatal/blocking recall={metrics['fatal_or_blocking_finding_recall_percent']}%; "
        f"major recall={metrics['major_finding_recall_percent']}%"
    )
    print(
        "governance metrics: "
        f"lineage={metrics['lineage_compliance_percent']}%; "
        f"isolation={metrics['reviewer_isolation_compliance_percent']}%; "
        f"edit-boundary={metrics['reviewer_edit_boundary_compliance_percent']}%; "
        f"dissent={metrics['dissent_preservation_percent']}%"
    )
    print(
        "fresh-repeat budget: "
        f"{repeat['selected_case_count']} default cases, "
        f"{repeat['fresh_run_count']} synthetic runs, max automatic {repeat['maximum_automatic_case_count']}"
    )
    print(
        "live fresh-repeat gate: "
        f"{live_repeat['observed_review_snapshot_count']} observed snapshots / "
        f"{live_repeat['unique_reviewer_instance_count']} unique instances; "
        f"verified={live_repeat['verified_live_review_count']}; "
        f"status={live_repeat['verified_live_gate_status']}"
    )
    print(
        "live retrieval gate: "
        f"{retrieval['completed_current_receipts']}/{retrieval['required_receipt_count']} verified receipts; "
        f"{retrieval['observed_unverified_receipts']} observed-unverified; "
        f"{retrieval['pending_receipts']} pending; status={retrieval['status']}"
    )
    print(f"Phase 8 status: {result['phase_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
