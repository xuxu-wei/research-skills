#!/usr/bin/env python3
"""Replay Phase 4 workflow fixtures against the generated plugin registry.

The replay engine materializes each trace in a temporary workspace, derives
actual writes from filesystem diffs, hashes every reviewer input before and
after execution, and rejects contract mutations. It does not claim that a
deterministic replay is a live model run; live receipts are audited separately.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import tempfile
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
FIXTURE_ROOT = REPO / "tests" / "openai_phase4"
SCHEMA_PATH = FIXTURE_ROOT / "runtime-trace.schema.yaml"
REPORT_PATH = PLUGIN / "reports" / "phase4-scenario-results.json"
FIXTURE_NAMES = (
    "idea.yaml",
    "proposal.yaml",
    "article.yaml",
    "perspective.yaml",
    "research-polisher.yaml",
)
BOUNDED_IDEA_FIXTURE = "idea-bounded-exploration.yaml"
IDEA_DOSSIER_SECTIONS = (
    "Title, summary, audience, and positioning",
    "Structured abstract",
    "Background, current state, gap, significance, and rationale",
    "Research question, objectives, and core hypothesis",
    "Research content and work packages",
    "Data, materials, and existing evidence base",
    "Research design and methods",
    "Key techniques and implementation",
    "Evidence chains",
    "Required analyses and evidence",
    "Expected outputs, falsification criteria, and interpretations",
    "Contribution, innovation, impact, application, and closest-work comparison",
    "Title and positioning claim-support table",
    "Feasibility, resources, risks, alternatives, and stop conditions",
    "References",
)
LIVE_RECEIPT_PATH = FIXTURE_ROOT / "live-forward-test-receipts.yaml"
PANEL_SKILLS = {
    "idea": "idea-adversarial-review-panel",
    "proposal": "proposal-review-panel",
    "article": "article-review-panel",
    "perspective": "perspective-review-panel",
    "research_polisher": None,
}
LIVE_RECEIPT_WORKFLOWS = ("idea", "proposal", "article", "perspective")
LIVE_IDENTITY_COMPONENTS = (
    "manifest",
    "workflow_registry",
    "registry_schema_version",
    "receipt_schema",
    "skills_tree",
)
DIGEST_ALGORITHM = "sha256_crlf_normalized_bytes"
SKILLS_TREE_DIGEST_ALGORITHM = "sha256_sorted_posix_relative_path_nul_crlf_normalized_bytes_nul"
POLISHER_ROLE_ALIASES = {
    "research_polisher_strategy_report": "strategy_report",
    "research_polisher_sealed_provenance": "strategy_report_manifest",
    "research_polisher_evaluation_report": "evaluation_report",
    "research_polisher_review_finding_index": "review_finding_index",
    "research_polisher_revision_brief": "revision_plan",
    "research_polisher_revision_delta": "revision_delta",
    "research_polisher_selection_dossier": "final_handoff_package",
}
POLISHER_PLAN_REQUIRED_FIELDS = (
    "proposed_repositioning",
    "value_mechanism",
    "scientific_significance_delta",
    "practical_value_delta",
    "dissemination_impact_delta",
    "story_arc",
    "target_audiences",
    "outlet_archetypes",
    "claim_delta",
    "existing_evidence_ids",
    "evidence_dependencies",
    "added_work_items",
    "feasibility_basis",
    "dependencies",
    "incompatible_with",
    "risks",
    "unknowns",
    "fallback",
    "stop_condition",
    "target_requirements_status",
)
POLISHER_DOSSIER_REQUIRED_FIELDS = (
    "source_artifacts",
    "normalized_context_artifact",
    "research_question",
    "design",
    "methods",
    "data",
    "existing_results",
    "current_claims",
    "current_framing",
    "intended_audiences",
    "target_outlets",
    "resource_constraints",
    "evidence_map",
    "target_requirements_adapter",
    "assumptions",
    "unresolved_inputs",
)
POLISHER_PARETO_AXES = (
    "effort",
    "feasibility",
    "methodological_risk",
    "scientific_significance_potential",
    "practical_value_potential",
    "dissemination_potential",
    "publication_positioning",
)
POLISHER_OPTION_DECISIONS = {"retain", "revise", "reject", "not_assessable"}
POLISHER_ANONYMOUS_OPTION_ID = re.compile(r"^anon-[0-9a-f]{8}$")
POLISHER_OPTION_DECISION_REQUIRED_FIELDS = (
    "option_id",
    "effort_tier",
    "decision",
    "method_design_compatibility",
    "evidence_claim_fit",
    "tier_correctness",
    "feasibility",
    "scientific_significance_potential",
    "practical_value_potential",
    "dissemination_potential",
    "narrative_differentiation",
    "publication_positioning",
    "target_fit",
    "fatal_findings",
    "major_findings",
    "required_repairs",
    "unresolved_issues",
)


class ScenarioViolation(AssertionError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise ScenarioViolation(code, message)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8-sig"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def missing_fields(value: dict[str, Any], fields: list[str]) -> list[str]:
    return sorted(set(fields) - set(value))


def safe_relative(value: str) -> str:
    normalized = Path(value.replace("\\", "/"))
    require(not normalized.is_absolute() and ".." not in normalized.parts, "unsafe_path", value)
    return normalized.as_posix()


class ScenarioEngine:
    def __init__(self, fixture: dict[str, Any], registry: dict[str, Any], schema: dict[str, Any], workspace: Path):
        self.fixture = fixture
        self.registry = registry
        self.schema = schema
        self.workspace = workspace
        self.workflow = fixture["workflow"]
        self.machine = registry["workflow_state_machines"][self.workflow]
        self.contract = registry["scenario_eval_contract"]
        self.skills = {entry["name"]: entry for entry in registry["skills"]}
        self.edges = {
            (edge["workflow"], edge["source"], edge["destination"]): edge
            for edge in registry["workflow_edges"]
        }
        self.lifecycle = registry["workflow_state_policy"]["lifecycle_transitions"]
        self.artifacts: dict[str, dict[str, Any]] = {}
        self.review_reports: dict[str, dict[str, Any]] = {}
        self.review_artifact_reports: dict[str, str] = {}
        self.findings_by_id: dict[str, dict[str, Any]] = {}
        self.current_primary: dict[str, Any] | None = None
        self.first_primary: dict[str, Any] | None = None
        self.primary_versions: list[str] = []
        self.latest_evaluated_version: str | None = None
        self.state = "initialized"
        self.reviewer_instances: set[str] = set()
        self.writer_instances: set[str] = set()
        self.evaluator_instances: list[str] = []
        self.panel_instances: dict[str, str] = {}
        self.panel_review_ids: set[str] = set()
        self.panel_complete = False
        self.panel_patch_pending = False
        self.panel_revision_scope: str | None = None
        self.strategy_reports_by_role: dict[str, list[str]] = {}
        self.pending_revision_review_ids: set[str] = set()
        self.entry_gate_verified = False
        self.dissent_ids: set[str] = set()
        self.fatal_ids: set[str] = set()
        self.events: list[dict[str, Any]] = []
        self.edge_receipts: list[str] = []
        self.lifecycle_receipts: list[dict[str, Any]] = []
        self.initial_artifact_ids: list[str] = []
        self.idea_node_id: str | None = None

    def canonical_artifact_role(self, role: str) -> str:
        if self.workflow == "research_polisher":
            return POLISHER_ROLE_ALIASES.get(role, role)
        return role

    def artifact_has_role(self, artifact: dict[str, Any], role: str) -> bool:
        return self.canonical_artifact_role(str(artifact.get("artifact_role", ""))) == role

    def direction_profile(self) -> str | None:
        if self.workflow != "idea":
            return None
        return str(self.fixture.get("direction_profile", "focused_optimization"))

    def post_evaluation_panel_required(self) -> bool:
        if self.workflow != "idea":
            return self.machine.get("post_evaluation_panel_required", True)
        profile = self.machine.get("internal_direction_profiles", {}).get(
            self.direction_profile(), {}
        )
        if self.direction_profile() == "bounded_exploration":
            return bool(profile.get("adversarial_panel_required_before_direction_selection", False))
        return bool(profile.get("adversarial_panel_required_before_handoff", True))

    def expected_final_state(self) -> str:
        conditional = self.contract.get("workflow_conditional_final_states", {}).get(
            self.workflow, {}
        )
        profile = self.direction_profile()
        if profile in conditional:
            return str(conditional[profile])
        return str(
            self.machine.get(
                "final_state",
                self.contract.get("workflow_final_states", {}).get(
                    self.workflow, "human_signoff_required"
                ),
            )
        )

    @staticmethod
    def polisher_decision_state(skill_name: str, decision: str) -> str:
        routes = {
            "research-polisher-strategy-reviewer": {
                "matrix_complete": "continue",
                "matrix_complete_with_no_defensible_option": "continue",
                "clarification_required": "clarification_stop",
                "independent_review_pending": "independent_review_pending",
            },
            "research-polisher-methodology-publishability-reviewer": {
                "ready_for_human_selection": "packaging_pending",
                "revision_required": "revision_required",
                "specialist_review_required": "specialist_review_pending",
                "no_defensible_option": "no_defensible_option",
                "not_assessable": "clarification_stop",
                "independent_review_pending": "independent_review_pending",
            },
        }
        route = routes.get(skill_name, {}).get(decision)
        require(route is not None, "polisher_decision_route", f"{skill_name}: {decision}")
        return route

    def set_polisher_route_state(self, target: str, decision: str, event_id: str) -> None:
        require(
            target
            in {
                "clarification_stop",
                "specialist_review_pending",
                "no_defensible_option",
            },
            "polisher_decision_route",
            f"unsupported direct state: {target}",
        )
        source = self.state
        self.state = target
        self.lifecycle_receipts.append(
            {
                "event_id": event_id,
                "from": source,
                "to": target,
                "trigger": decision,
            }
        )

    @staticmethod
    def polisher_plan_digest(plan: dict[str, Any]) -> str:
        encoded = json.dumps(plan, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return sha256_bytes(encoded)

    def validate_header(self) -> None:
        missing = missing_fields(self.fixture, self.schema["fixture_required"])
        require(not missing, "fixture_schema", f"missing fixture fields: {missing}")
        require(self.fixture["schema_version"] == self.schema["schema_version"], "fixture_schema", "schema version mismatch")
        require(self.fixture["execution_kind"] == "deterministic_replay", "execution_kind", "fixture is not a deterministic replay")
        require(
            self.fixture["execution_scope"] == "evaluation_revision_delivery_with_entry_receipts",
            "execution_scope",
            self.fixture["execution_scope"],
        )
        require(self.workflow in self.registry["workflow_state_machines"], "unknown_workflow", self.workflow)
        require(self.fixture["plugin_version"] == self.registry["plugin_version"], "plugin_version", "fixture/registry mismatch")
        require(self.fixture["registry_schema_version"] == self.registry["schema_version"], "registry_schema", "fixture/registry mismatch")
        require(self.fixture["entry_mode"] in self.machine["entry_modes"], "entry_mode", self.fixture["entry_mode"])
        require(
            self.fixture["entry_mode"] in self.machine["scenario_entry_gate_contracts"],
            "unsupported_scenario_entry_mode",
            self.fixture["entry_mode"],
        )
        require(
            self.schema["artifact_required"] == self.contract["required_lineage_fields"] + ["artifact_role"],
            "schema_registry_drift",
            "artifact schema and registry lineage contract differ",
        )
        require(
            self.schema["review_required"] == self.contract["required_review_fields"],
            "schema_registry_drift",
            "review schema and registry contract differ",
        )
        panel = self.fixture["panel"]
        missing_panel = missing_fields(panel, self.schema["panel_required"])
        require(not missing_panel, "panel_contract", f"missing panel fields: {missing_panel}")
        panel_contract = self.contract["panel_contracts"][self.workflow]
        require(panel["mode"] in panel_contract["modes"], "panel_contract", f"invalid mode: {panel['mode']}")
        require(panel["tier"] in panel_contract["tiers"], "panel_contract", f"invalid tier: {panel['tier']}")
        canonical_roles = panel_contract["tiers"][panel["tier"]]
        require(panel["required_roles"] == canonical_roles, "panel_contract", f"{panel['required_roles']} != {canonical_roles}")
        require(
            set(panel_contract["mandatory_roles"]) <= set(panel["required_roles"]),
            "panel_contract",
            "mandatory panel role missing",
        )
        panel_required = self.post_evaluation_panel_required()
        if not panel_required:
            require(
                panel["mode"] == "not_applicable"
                and panel["tier"] == "not_applicable"
                and panel["required_roles"] == [],
                "panel_contract",
                f"{self.workflow}: no-panel workflow must declare not_applicable",
            )
        if self.workflow == "proposal" and panel["tier"] == "lightweight_panel":
            require(
                panel.get("selection_basis") == "explicit_user_direction",
                "panel_contract",
                "lightweight proposal panel requires explicit user direction",
            )
        expected_gates = set(self.machine["entry_gates"][self.fixture["entry_mode"]])
        require(
            set(self.fixture["entry_gate_receipts"]) == expected_gates,
            "entry_gate_receipts",
            f"expected {sorted(expected_gates)}, got {sorted(self.fixture['entry_gate_receipts'])}",
        )
        gate_contracts = self.machine["scenario_entry_gate_contracts"][self.fixture["entry_mode"]]
        require(set(gate_contracts) == expected_gates, "entry_gate_contract", self.workflow)
        reviewers = {entry["name"] for entry in self.registry["skills"] if entry["requires_independent_subagent"]}
        decision_contracts = self.contract["review_decision_contracts"]
        require(set(decision_contracts) == reviewers, "review_decision_contract", "reviewer decision coverage differs from registry")
        for skill_name, decision_contract in decision_contracts.items():
            allowed = set(decision_contract["allowed"])
            routed = [set(decision_contract[key]) for key in ("pass", "revise", "stop")]
            require(set.union(*routed) == allowed, "review_decision_contract", f"unrouted decisions for {skill_name}")
            require(sum(len(values) for values in routed) == len(allowed), "review_decision_contract", f"overlapping decisions for {skill_name}")

    def transition(self, target: str, trigger: str, event_id: str) -> None:
        source = self.state
        matches = [
            item
            for item in self.lifecycle
            if item["to"] == target and item["trigger"] == trigger and item["from"] in {source, "*"}
        ]
        require(bool(matches), "registry_lifecycle_mismatch", f"{source} --{trigger}--> {target}")
        requirements = set(matches[0].get("requires", []))
        checks = {
            "prior_panel_complete": self.panel_complete,
            "patch_scope_minor": self.panel_revision_scope == "minor",
            "fresh_evaluation_current": (
                self.current_primary is not None
                and self.latest_evaluated_version == self.current_primary["version_id"]
            ),
            "no_unresolved_fatal_finding": not self.fatal_ids,
        }
        unknown = requirements - set(checks)
        require(not unknown, "registry_lifecycle_requirement", f"unknown requirements: {sorted(unknown)}")
        unmet = sorted(requirement for requirement in requirements if not checks[requirement])
        require(not unmet, "registry_lifecycle_requirement", f"{event_id}: unmet {unmet}")
        self.state = target
        self.lifecycle_receipts.append(
            {"event_id": event_id, "from": source, "to": target, "trigger": trigger}
        )

    def materialize_initial_artifacts(self) -> dict[str, Any]:
        before = tree_hashes(self.workspace)
        for artifact in self.fixture["initial_artifacts"]:
            missing = missing_fields(artifact, self.schema["artifact_required"])
            require(not missing, "artifact_schema", f"initial artifact missing: {missing}")
            require(artifact["workflow_id"] == self.fixture["workflow_id"], "artifact_lineage", artifact["artifact_id"])
            require(artifact["plugin_version"] == self.registry["plugin_version"], "artifact_lineage", artifact["artifact_id"])
            source_skill = artifact["source_skill"]
            if source_skill == "external-input":
                require(
                    artifact["created_by_instance_id"].startswith("fixture-user"),
                    "artifact_lineage",
                    artifact["artifact_id"],
                )
                require(
                    artifact["change_type"] == "supplied",
                    "artifact_lineage",
                    artifact["artifact_id"],
                )
            else:
                actor_outputs = self.contract["runtime_artifact_role_contract"][
                    "actor_output_roles_by_skill"
                ]
                allowed_roles = {
                    self.canonical_artifact_role(role)
                    for role in actor_outputs.get(source_skill, [])
                }
                require(
                    self.canonical_artifact_role(artifact["artifact_role"])
                    in allowed_roles,
                    "artifact_lineage",
                    f"{artifact['artifact_id']}: {source_skill} cannot create "
                    f"{artifact['artifact_role']}",
                )
                require(
                    artifact["created_by_instance_id"].startswith(
                        f"{source_skill}-"
                    ),
                    "artifact_lineage",
                    artifact["artifact_id"],
                )
                require(
                    artifact["change_type"] == "fixture_precomputed",
                    "artifact_lineage",
                    artifact["artifact_id"],
                )
            require(artifact["based_on"] == [], "artifact_lineage", artifact["artifact_id"])
            require(artifact["frozen"] is True, "artifact_not_frozen", artifact["artifact_id"])
            require(artifact["content_digest"] == "computed", "artifact_digest", artifact["artifact_id"])
            artifact["path"] = safe_relative(artifact["path"])
            if self.workflow == "research_polisher":
                self.validate_polisher_artifact_path(artifact)
                if artifact["artifact_role"] == "research_polisher_dossier":
                    self.validate_polisher_dossier(artifact)
            require(artifact["artifact_id"] not in self.artifacts, "duplicate_artifact_id", artifact["artifact_id"])
            target = self.workspace / artifact["path"]
            require(not target.exists(), "artifact_path_overwrite", artifact["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            content = str(artifact.get("content", artifact["artifact_id"] + "\n")).encode("utf-8")
            target.write_bytes(content)
            artifact["content_digest"] = sha256_bytes(content)
            self.artifacts[artifact["artifact_id"]] = artifact
            self.initial_artifact_ids.append(artifact["artifact_id"])
        after = tree_hashes(self.workspace)
        return {
            "actual_write_paths": sorted(path for path, digest in after.items() if before.get(path) != digest),
            "artifact_ids": list(self.initial_artifact_ids),
        }

    def validate_dispatch(self, event: dict[str, Any]) -> dict[str, Any]:
        missing = missing_fields(event, self.schema["dispatch_event_required"])
        require(not missing, "event_schema", f"{event['event_id']} missing dispatch fields: {missing}")
        key = (self.workflow, event["source_skill"], event["destination_skill"])
        edge = self.edges.get(key)
        require(edge is not None, "registry_edge_mismatch", f"edge not registered: {key}")
        require(event["dispatch_mode"] == edge["dispatch_mode"], "registry_edge_mismatch", f"dispatch mode for {key}")
        require(event["trigger"] == edge["trigger"], "registry_edge_mismatch", f"trigger for {key}")
        self.edge_receipts.append(" -> ".join(key))
        for path in event["allowed_read_paths"] + event["allowed_write_paths"]:
            safe_relative(path)
        require(len(event["input_artifact_ids"]) == len(event["input_versions"]), "input_version_mismatch", event["event_id"])
        for artifact_id, version in zip(event["input_artifact_ids"], event["input_versions"]):
            artifact = self.artifacts.get(artifact_id)
            require(artifact is not None, "unknown_input_artifact", artifact_id)
            require(artifact["version_id"] == version, "input_version_mismatch", f"{artifact_id}: {version}")
            require(artifact["path"] in event["allowed_read_paths"], "read_scope", artifact["path"])
        if event["destination_skill"] == "sap-writer":
            preflights = [
                self.artifacts[item]
                for item in event["input_artifact_ids"]
                if self.artifacts[item]["source_skill"] == "methodology-statistics-preflight"
            ]
            require(len(preflights) == 1, "sap_preflight_missing", event["event_id"])
            preflight = preflights[0]
            report_id = self.review_artifact_reports.get(preflight["artifact_id"])
            report = self.review_reports.get(report_id or "")
            require(report is not None, "sap_preflight_missing", event["event_id"])
            require(report["reviewer_skill"] == "methodology-statistics-preflight", "sap_preflight_missing", event["event_id"])
            require(self.decision_category(report["reviewer_skill"], report["decision"]) == "pass", "sap_preflight_missing", event["event_id"])
            require(self.finding_route(report["findings"]) is None, "sap_preflight_missing", event["event_id"])
            require(self.current_primary is not None, "sap_preflight_missing", event["event_id"])
            current_ref = f"{self.current_primary['artifact_id']}@{self.current_primary['version_id']}"
            require(current_ref in preflight["based_on"], "sap_preflight_missing", event["event_id"])
            require(self.current_primary["artifact_id"] in report["input_artifact_ids"], "sap_preflight_missing", event["event_id"])
        return edge

    def validate_artifact(
        self,
        artifact: dict[str, Any],
        event: dict[str, Any],
        pending_output_ids: set[str] | None = None,
    ) -> None:
        missing = missing_fields(artifact, self.schema["artifact_required"])
        require(not missing, "artifact_schema", f"{event['event_id']} missing artifact fields: {missing}")
        require(artifact["workflow_id"] == self.fixture["workflow_id"], "artifact_lineage", artifact["artifact_id"])
        require(artifact["plugin_version"] == self.registry["plugin_version"], "artifact_lineage", artifact["artifact_id"])
        expected_source = event.get("destination_skill", event.get("source_skill"))
        require(artifact["source_skill"] == expected_source, "artifact_lineage", artifact["artifact_id"])
        require(artifact["created_by_instance_id"] == event["actor_instance_id"], "artifact_lineage", artifact["artifact_id"])
        require(artifact["frozen"] is True, "artifact_not_frozen", artifact["artifact_id"])
        require(artifact["content_digest"] == "computed", "artifact_digest", "fixtures must require runtime-computed digests")
        artifact["path"] = safe_relative(artifact["path"])
        if self.workflow == "idea":
            self.validate_idea_artifact_path(artifact)
            if self.canonical_artifact_role(artifact["artifact_role"]) == "idea_dossier":
                allowed_change_types = set(self.registry["artifact_completeness_policy"]["idea_dossier_change_types"])
                require(artifact.get("change_type") in allowed_change_types, "idea_dossier_change_type", str(artifact.get("change_type")))
        elif self.workflow == "research_polisher":
            self.validate_polisher_artifact_path(artifact)
        require(artifact["artifact_id"] not in self.artifacts, "duplicate_artifact_id", artifact["artifact_id"])
        pending_output_ids = pending_output_ids or set()
        pending_outputs = {item["artifact_id"]: item for item in event.get("outputs", [])}
        for parent in artifact["based_on"]:
            require("@" in parent, "artifact_lineage", parent)
            parent_id, parent_version = parent.split("@", 1)
            require(parent_id in self.artifacts or parent_id in pending_output_ids, "dangling_lineage", parent)
            require(parent_id != artifact["artifact_id"], "artifact_lineage", parent)
            parent_artifact = self.artifacts.get(parent_id) or pending_outputs[parent_id]
            require(parent_artifact["version_id"] == parent_version, "artifact_lineage", parent)

    def materialize_outputs(self, event: dict[str, Any], outputs: list[dict[str, Any]], report: dict[str, Any] | None) -> dict[str, Any]:
        before = tree_hashes(self.workspace)
        input_paths = {self.artifacts[item]["path"] for item in event["input_artifact_ids"]}
        input_hashes_before = {path: before[path] for path in input_paths}
        declared_paths = {safe_relative(item["path"]) for item in outputs}
        allowed_writes = {safe_relative(path) for path in event["allowed_write_paths"]}
        require(declared_paths <= allowed_writes, "write_scope_escape", f"{event['event_id']}: {sorted(declared_paths - allowed_writes)}")
        require(not (declared_paths & input_paths), "input_write_overlap", f"{event['event_id']}: {sorted(declared_paths & input_paths)}")

        pending_output_ids = {artifact["artifact_id"] for artifact in outputs}
        require(len(pending_output_ids) == len(outputs), "duplicate_artifact_id", event["event_id"])
        for artifact in outputs:
            self.validate_artifact(artifact, event, pending_output_ids)
            target = self.workspace / artifact["path"]
            require(not target.exists(), "artifact_path_overwrite", artifact["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            if artifact.get("copy_of"):
                source = self.artifacts.get(artifact["copy_of"])
                require(source is not None, "unknown_copy_source", artifact["copy_of"])
                content = (self.workspace / source["path"]).read_bytes()
                if "content_override" in artifact:
                    content = str(artifact["content_override"]).encode("utf-8")
            elif report is not None and self.canonical_artifact_role(artifact["artifact_role"]) in {"evaluation_report", "audit_report", "panel_report", "verification_report", "review_report", "strategy_report"}:
                content = yaml.safe_dump(report, sort_keys=False, allow_unicode=True).encode("utf-8")
            else:
                content = str(artifact.get("content", f"{artifact['artifact_id']} {artifact['version_id']}\n")).encode("utf-8")
            target.write_bytes(content)
            artifact["content_digest"] = sha256_bytes(content)

        after = tree_hashes(self.workspace)
        actual_writes = sorted(path for path, digest in after.items() if before.get(path) != digest)
        require(set(actual_writes) <= allowed_writes, "write_scope_escape", f"{event['event_id']}: {actual_writes}")
        input_hashes_after = {path: after[path] for path in input_paths}
        require(input_hashes_before == input_hashes_after, "source_artifact_modified", event["event_id"])

        for artifact in outputs:
            self.artifacts[artifact["artifact_id"]] = artifact
            if report is not None:
                self.review_artifact_reports[artifact["artifact_id"]] = report["review_id"]

        return {
            "files_read": list(report["files_read"]) if report else [],
            "actual_write_paths": actual_writes,
            "input_hashes_before": input_hashes_before,
            "input_hashes_after": input_hashes_after,
        }

    def process_produce(self, event: dict[str, Any]) -> dict[str, Any]:
        self.validate_dispatch(event)
        require(event["actor_instance_id"] not in self.reviewer_instances, "writer_is_reviewer", event["actor_instance_id"])
        outputs = event.get("outputs", [])
        require(outputs, "event_schema", f"{event['event_id']} has no outputs")
        revision_contract = self.contract["revision_artifact_contract"]
        if event["destination_skill"].endswith("refinement-controller"):
            require(
                [artifact["artifact_role"] for artifact in outputs].count(revision_contract["controller_output_role"]) == 1,
                "revision_plan_missing",
                event["event_id"],
            )
            self.validate_revision_plan_lineage(event, outputs)
        primary_outputs = [
            artifact
            for artifact in outputs
            if artifact["artifact_role"] == self.machine["primary_artifact_type"]
        ]
        if self.current_primary is not None and primary_outputs:
            plans = [
                self.artifacts[artifact_id]
                for artifact_id in event["input_artifact_ids"]
                if self.artifact_has_role(
                    self.artifacts[artifact_id], revision_contract["controller_output_role"]
                )
            ]
            require(len(plans) == 1, "revision_plan_missing", event["event_id"])
            expected_plan_source = (
                self.machine.get("primary_assembler_skill")
                if self.workflow == "research_polisher"
                else event["source_skill"]
            )
            require(plans[0]["source_skill"] == expected_plan_source, "revision_plan_missing", event["event_id"])
            output_roles = {
                self.canonical_artifact_role(artifact["artifact_role"])
                for artifact in outputs
            }
            required_output_roles = {"revision_delta"}
            if self.skills[event["destination_skill"]]["role"] == "drafter":
                required_output_roles.add("response_to_reviewers")
            require(
                required_output_roles <= output_roles,
                "revision_artifacts_missing",
                event["event_id"],
            )
        if self.workflow == "research_polisher":
            self.validate_polisher_revision_brief(event, outputs)
            self.validate_polisher_assembler_outputs(event, outputs)
        observation = self.materialize_outputs(event, outputs, None)
        self.writer_instances.add(event["actor_instance_id"])
        for artifact in outputs:
            if artifact["artifact_role"] != self.machine["primary_artifact_type"]:
                continue
            if self.current_primary is not None:
                expected_parent = f"{self.current_primary['artifact_id']}@{self.current_primary['version_id']}"
                if self.workflow != "research_polisher":
                    require(expected_parent in artifact["based_on"], "artifact_lineage", f"missing {expected_parent}")
                require(artifact["version_id"] != self.current_primary["version_id"], "version_not_advanced", artifact["version_id"])
                require(self.state == "revision_required", "registry_lifecycle_mismatch", event["event_id"])
            self.current_primary = artifact
            self.first_primary = self.first_primary or artifact
            self.primary_versions.append(artifact["version_id"])
            if len(self.primary_versions) > 1:
                self.transition("artifact_frozen", "new_version_created", event["event_id"])
            if event.get("panel_patch"):
                require(
                    self.panel_revision_scope in {"minor", "substantive"},
                    "panel_patch_scope",
                    event["event_id"],
                )
                self.panel_patch_pending = self.panel_revision_scope == "minor"
        return observation

    def process_orchestrator_record(self, event: dict[str, Any]) -> dict[str, Any]:
        require(event.get("source_skill") == self.machine["orchestrator"], "orchestrator_record", event["event_id"])
        require(event["actor_instance_id"] not in self.reviewer_instances, "writer_is_reviewer", event["actor_instance_id"])
        for path in event.get("allowed_read_paths", []) + event.get("allowed_write_paths", []):
            safe_relative(path)
        require(
            len(event.get("input_artifact_ids", [])) == len(event.get("input_versions", [])),
            "input_version_mismatch",
            event["event_id"],
        )
        for artifact_id, version in zip(event["input_artifact_ids"], event["input_versions"]):
            artifact = self.artifacts.get(artifact_id)
            require(artifact is not None, "unknown_input_artifact", artifact_id)
            require(artifact["version_id"] == version, "input_version_mismatch", artifact_id)
            require(artifact["path"] in event["allowed_read_paths"], "read_scope", artifact["path"])
        outputs = event.get("outputs", [])
        require(outputs, "event_schema", f"{event['event_id']} has no outputs")
        if any(output["artifact_role"] == "revision_plan" for output in outputs):
            self.validate_revision_plan_lineage(event, outputs)
        observation = self.materialize_outputs(event, outputs, None)
        self.writer_instances.add(event["actor_instance_id"])
        return observation

    def validate_revision_plan_lineage(self, event: dict[str, Any], outputs: list[dict[str, Any]]) -> None:
        require(self.current_primary is not None, "revision_plan_trigger_missing", event["event_id"])
        plan = next((output for output in outputs if output["artifact_role"] == "revision_plan"), None)
        require(plan is not None, "revision_plan_missing", event["event_id"])
        current_ref = f"{self.current_primary['artifact_id']}@{self.current_primary['version_id']}"
        require(self.current_primary["artifact_id"] in event["input_artifact_ids"], "revision_plan_trigger_missing", event["event_id"])
        require(current_ref in plan["based_on"], "revision_plan_trigger_missing", event["event_id"])
        review_inputs = [
            self.artifacts[artifact_id]
            for artifact_id in event["input_artifact_ids"]
            if self.artifacts[artifact_id]["artifact_role"] in {"evaluation_report", "audit_report", "panel_report"}
        ]
        require(review_inputs, "revision_plan_trigger_missing", event["event_id"])
        review_refs = {f"{artifact['artifact_id']}@{artifact['version_id']}" for artifact in review_inputs}
        require(bool(review_refs & set(plan["based_on"])), "revision_plan_trigger_missing", event["event_id"])
        required_trigger_artifact_ids = {
            artifact_id
            for artifact_id, review_id in self.review_artifact_reports.items()
            if review_id in self.pending_revision_review_ids
        }
        require(required_trigger_artifact_ids, "revision_plan_trigger_missing", event["event_id"])
        consumed_trigger_ids = set(event["input_artifact_ids"]) & required_trigger_artifact_ids
        require(consumed_trigger_ids == required_trigger_artifact_ids, "revision_plan_trigger_missing", event["event_id"])
        require(
            all(
                any(parent.split("@", 1)[0] == trigger_id for parent in plan["based_on"])
                for trigger_id in consumed_trigger_ids
            ),
            "revision_plan_trigger_missing",
            event["event_id"],
        )
        self.pending_revision_review_ids = set()

    def decision_category(self, skill_name: str, decision: str) -> str:
        contract = self.contract["review_decision_contracts"].get(skill_name)
        require(contract is not None, "review_decision_contract", skill_name)
        require(decision in contract["allowed"], "review_decision_invalid", f"{skill_name}: {decision}")
        for category in ("pass", "revise", "stop"):
            if decision in contract[category]:
                return category
        raise ScenarioViolation("review_decision_contract", f"unrouted decision: {skill_name}: {decision}")

    @staticmethod
    def finding_route(findings: list[dict[str, Any]]) -> str | None:
        severe = [
            finding
            for finding in findings
            if finding.get("status") != "resolved"
            and (finding.get("blocking") is True or finding.get("severity") in {"fatal", "blocking"})
        ]
        if not severe:
            return None
        if any(finding.get("route") in {"stop", "stopped", "stop_no_gain"} for finding in severe):
            return "stopped"
        if any(
            finding.get("fixability") in {"unfixable", "unavailable"}
            or finding.get("route") in {"blocked", "reject", "reject_or_redesign"}
            for finding in severe
        ):
            return "blocked"
        return "revision_required"

    def polisher_strategy_roles(self) -> list[str]:
        return list(
            self.machine.get(
                "strategy_reviewer_roles",
                ["scientific_significance", "practical_value", "dissemination_editorial"],
            )
        )

    def validate_idea_artifact_path(self, artifact: dict[str, Any]) -> None:
        role = self.canonical_artifact_role(artifact["artifact_role"])
        folder_by_role = {
            "idea_dossier": "dossiers",
            "evaluation_report": "reviews",
            "revision_plan": "revisions",
            "revision_delta": "revisions",
            "panel_report": "adversarial",
        }
        path = Path(artifact["path"])
        if role == "idea_index":
            require(
                path.parent == Path("03_ideas") and path.name.startswith("idea-index-v"),
                "idea_artifact_path",
                artifact["path"],
            )
            return
        if role == "final_handoff_package":
            require(path.parts[0] == "04_portfolio", "idea_artifact_path", artifact["path"])
            return
        if role == "reference_ledger":
            require(
                len(path.parts) == 5
                and path.parts[:2] == ("03_ideas", "nodes")
                and path.parts[3] == "references"
                and path.name == "reference-ledger.md",
                "idea_artifact_path",
                artifact["path"],
            )
            node_id = path.parts[2]
            if self.idea_node_id is None:
                self.idea_node_id = node_id
            require(node_id == self.idea_node_id, "idea_artifact_path", "Idea artifacts span nodes")
            return
        folder = folder_by_role.get(role)
        if folder is None:
            return
        require(
            len(path.parts) >= 5
            and path.parts[:2] == ("03_ideas", "nodes")
            and path.parts[3] == folder,
            "idea_artifact_path",
            artifact["path"],
        )
        node_id = path.parts[2]
        if self.idea_node_id is None:
            self.idea_node_id = node_id
        require(node_id == self.idea_node_id, "idea_artifact_path", "Idea artifacts span nodes")
        if role == "idea_dossier":
            require(path.name.startswith("idea-dossier-v"), "idea_artifact_path", artifact["path"])

    def validate_polisher_artifact_path(self, artifact: dict[str, Any]) -> None:
        path = Path(artifact["path"])
        require(
            path.name.startswith("research_polisher_"),
            "polisher_artifact_path",
            artifact["path"],
        )
        canonical_role = self.canonical_artifact_role(artifact["artifact_role"])
        expected_root = {
            "research_polisher_dossier": "01_context",
            "evidence_map": "02_evidence",
            "strategy_report": "03_strategy",
            "strategy_report_manifest": "04_portfolios",
            "research_polisher_candidate_portfolio": "04_portfolios",
            "evaluation_report": "05_evaluations",
            "revision_plan": "06_revisions",
            "revision_delta": "06_revisions",
            "review_finding_index": "07_delivery",
            "final_handoff_package": "07_delivery",
        }.get(canonical_role)
        if expected_root:
            require(path.parts[0] == expected_root, "polisher_artifact_path", artifact["path"])

    def validate_polisher_dossier(self, artifact: dict[str, Any]) -> None:
        dossier = artifact.get("dossier_contract")
        require(isinstance(dossier, dict), "polisher_dossier_field_missing", artifact["artifact_id"])
        missing = missing_fields(dossier, list(POLISHER_DOSSIER_REQUIRED_FIELDS))
        require(not missing, "polisher_dossier_field_missing", f"{artifact['artifact_id']}: {missing}")
        sources = dossier["source_artifacts"]
        require(isinstance(sources, list) and sources, "polisher_dossier_field_missing", "source_artifacts")
        for source in sources:
            source_missing = missing_fields(
                source,
                [
                    "artifact_id",
                    "path",
                    "version",
                    "sha256",
                    "summary",
                    "summary_sha256",
                ],
            )
            require(not source_missing, "polisher_dossier_field_missing", f"source_artifacts: {source_missing}")
            safe_relative(source["path"])
            require(
                bool(source["artifact_id"])
                and bool(source["version"])
                and re.fullmatch(r"sha256:[0-9a-f]{64}", source["sha256"]),
                "polisher_dossier_source_binding",
                str(source.get("artifact_id")),
            )
            require(
                isinstance(source["summary"], str)
                and source["summary"].strip()
                and re.fullmatch(r"sha256:[0-9a-f]{64}", source["summary_sha256"]),
                "polisher_dossier_source_binding",
                str(source.get("artifact_id")),
            )
        for field in ("current_claims", "intended_audiences", "target_outlets"):
            require(isinstance(dossier[field], list) and dossier[field], "polisher_dossier_field_missing", field)
        for field in ("assumptions", "unresolved_inputs"):
            require(isinstance(dossier[field], list), "polisher_dossier_field_missing", field)
        constraints = dossier["resource_constraints"]
        constraint_fields = [
            "time",
            "people",
            "budget",
            "data_access",
            "technical_capacity",
            "maximum_effort_tier",
        ]
        require(
            isinstance(constraints, dict)
            and not missing_fields(constraints, constraint_fields)
            and all(isinstance(constraints[field], str) and constraints[field].strip() for field in constraint_fields),
            "polisher_dossier_field_missing",
            "resource_constraints",
        )
        for field in (
            "normalized_context_artifact",
            "research_question",
            "design",
            "methods",
            "data",
            "existing_results",
            "current_framing",
        ):
            require(isinstance(dossier[field], str) and bool(dossier[field].strip()), "polisher_dossier_field_missing", field)
        for field in ("evidence_map", "target_requirements_adapter"):
            value = dossier[field]
            require(
                value is None or value == "not_provided" or isinstance(value, dict),
                "polisher_dossier_field_missing",
                field,
            )
            if isinstance(value, dict):
                binding_fields = ["artifact_id", "version", "sha256"]
                require(
                    not missing_fields(value, binding_fields)
                    and bool(value["artifact_id"])
                    and bool(value["version"])
                    and re.fullmatch(r"sha256:[0-9a-f]{64}", value["sha256"]),
                    "polisher_dossier_source_binding",
                    field,
                )

    def polisher_effort_tiers(self) -> list[str]:
        return list(
            self.machine.get(
                "effort_tiers",
                ["reposition_only", "small_extension", "moderate_extension"],
            )
        )

    def validate_polisher_strategy_report(
        self, event: dict[str, Any], report: dict[str, Any]
    ) -> None:
        roles = self.polisher_strategy_roles()
        tiers = self.polisher_effort_tiers()
        role = report.get("reviewer_role")
        require(role in roles, "polisher_strategy_role", event["event_id"])
        require(
            report.get("peer_outputs_visible") is False,
            "peer_output_visible",
            event["event_id"],
        )
        visible_roles = {
            self.canonical_artifact_role(self.artifacts[artifact_id]["artifact_role"])
            for artifact_id in event["input_artifact_ids"]
        }
        require(
            not visible_roles.intersection(
                {"strategy_report", "strategy_report_manifest", "evaluation_report"}
            ),
            "polisher_strategy_peer_input",
            event["event_id"],
        )
        options = report.get("strategy_options")
        require(
            isinstance(options, list) and len(options) == len(tiers),
            "polisher_strategy_matrix_incomplete",
            event["event_id"],
        )
        observed_tiers = [option.get("effort_tier") for option in options]
        require(
            observed_tiers == tiers and len(set(observed_tiers)) == len(tiers),
            "polisher_strategy_matrix_incomplete",
            event["event_id"],
        )
        option_ids: set[str] = set()
        for option in options:
            tier = option.get("effort_tier")
            status = option.get("status")
            option_id = option.get("provisional_option_id") or f"no-defensible:{tier}"
            require(
                isinstance(option_id, str)
                and bool(option_id)
                and option_id not in option_ids,
                "polisher_strategy_option_id",
                event["event_id"],
            )
            option_ids.add(option_id)
            require(
                status in {"proposed", "no_defensible_option"},
                "polisher_strategy_option_status",
                option_id,
            )
            if status == "no_defensible_option":
                require(
                    option.get("plan") is None
                    and isinstance(option.get("reason"), str)
                    and bool(option["reason"].strip())
                    and isinstance(option.get("missing_or_infeasible_dependencies"), list)
                    and isinstance(option.get("clarification_needed"), list),
                    "polisher_no_defensible_option_schema",
                    option_id,
                )
                continue
            plan = option.get("plan")
            require(isinstance(plan, dict), "polisher_option_field_missing", option_id)
            missing_plan = missing_fields(plan, list(POLISHER_PLAN_REQUIRED_FIELDS))
            require(
                not missing_plan,
                "polisher_option_field_missing",
                f"{option_id}: {missing_plan}",
            )
            for field in (
                "proposed_repositioning",
                "value_mechanism",
                "scientific_significance_delta",
                "practical_value_delta",
                "dissemination_impact_delta",
                "story_arc",
                "feasibility_basis",
                "fallback",
                "stop_condition",
            ):
                require(isinstance(plan[field], str) and bool(plan[field].strip()), "polisher_option_field_missing", f"{option_id}: {field}")
            require(
                plan["target_requirements_status"]
                in {"verified", "target_requirements_unverified", "not_applicable"},
                "polisher_option_field_missing",
                f"{option_id}: target_requirements_status",
            )
            for field in (
                "target_audiences",
                "outlet_archetypes",
                "claim_delta",
                "existing_evidence_ids",
                "evidence_dependencies",
                "added_work_items",
                "incompatible_with",
                "risks",
                "unknowns",
            ):
                require(isinstance(plan[field], list), "polisher_option_field_missing", f"{option_id}: {field}")
            require(
                plan["target_audiences"]
                and plan["outlet_archetypes"]
                and plan["claim_delta"]
                and plan["existing_evidence_ids"]
                and plan["evidence_dependencies"]
                and plan["risks"],
                "polisher_option_field_missing",
                option_id,
            )
            dependencies = plan["dependencies"]
            require(
                isinstance(dependencies, dict)
                and set(dependencies) == {"data", "resources", "technical", "time"}
                and all(isinstance(value, list) for value in dependencies.values()),
                "polisher_option_field_missing",
                f"{option_id}: dependencies",
            )
            added_work = plan["added_work_items"]
            feasibility = option.get("feasibility")
            require(
                feasibility in {"certain", "high"},
                "polisher_extension_feasibility",
                option_id,
            )
            if tier == "reposition_only":
                require(
                    added_work == []
                    and option.get("introduces_new_analysis") is False
                    and option.get("introduces_new_data") is False
                    and option.get("introduces_new_experiment") is False,
                    "polisher_reposition_adds_work",
                    option_id,
                )
                require(
                    option.get("claim_traceable_to_frozen_source") is True,
                    "polisher_reposition_untraceable",
                    option_id,
                )
            else:
                require(
                    bool(added_work) and option.get("work_package_count") == 1,
                    "polisher_extension_scope",
                    option_id,
                )
            require(
                option.get("changes_core_design") is False
                and option.get("independent_new_study") is False
                and option.get("core_sample_rebuild") is False,
                "polisher_extension_scope",
                option_id,
            )

    def validate_polisher_assembler_outputs(
        self, event: dict[str, Any], outputs: list[dict[str, Any]]
    ) -> None:
        primary_outputs = [
            artifact
            for artifact in outputs
            if artifact["artifact_role"] == self.machine["primary_artifact_type"]
        ]
        if not primary_outputs:
            return
        require(
            event["destination_skill"]
            == self.machine.get("primary_assembler_skill", "research-polisher-plan-assembler"),
            "polisher_primary_assembler",
            event["event_id"],
        )
        strategy_skill = self.machine.get(
            "strategy_reviewer_skill", "research-polisher-strategy-reviewer"
        )
        strategy_artifacts = [
            self.artifacts[artifact_id]
            for artifact_id in event["input_artifact_ids"]
            if self.artifacts[artifact_id]["source_skill"] == strategy_skill
            and self.artifact_has_role(self.artifacts[artifact_id], "strategy_report")
        ]
        roles = self.polisher_strategy_roles()
        reports_by_role: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
        for artifact in strategy_artifacts:
            review_id = self.review_artifact_reports.get(artifact["artifact_id"])
            report = self.review_reports.get(review_id or "")
            require(report is not None, "polisher_strategy_report_missing", artifact["artifact_id"])
            role = report["reviewer_role"]
            require(role not in reports_by_role, "polisher_strategy_role_duplicate", role)
            reports_by_role[role] = (artifact, report)
        require(
            set(reports_by_role) == set(roles),
            "polisher_strategy_matrix_incomplete",
            event["event_id"],
        )
        instances = [report["reviewer_instance_id"] for _, report in reports_by_role.values()]
        require(
            len(instances) == len(set(instances)),
            "duplicate_reviewer_instance",
            event["event_id"],
        )
        portfolio = primary_outputs[0]
        allowed_visible_parent_roles = {"research_polisher_dossier", "evidence_map"}
        for parent in portfolio["based_on"]:
            parent_id = parent.split("@", 1)[0]
            parent_artifact = self.artifacts.get(parent_id)
            require(
                parent_artifact is not None
                and self.canonical_artifact_role(parent_artifact["artifact_role"])
                in allowed_visible_parent_roles
                and parent_artifact["source_skill"] != strategy_skill,
                "polisher_portfolio_lineage_leak",
                parent,
            )
        serialized_portfolio = json.dumps(portfolio, ensure_ascii=False, sort_keys=True)
        for forbidden_key in (
            "reviewer_role",
            "reviewer_lens",
            "source_report_ref",
            "source_option_id",
            "reviewer_instance_id",
            "report_refs",
        ):
            require(
                f'"{forbidden_key}"' not in serialized_portfolio,
                "polisher_portfolio_identity_leak",
                forbidden_key,
            )
        anonymous_options = portfolio.get("options")
        no_defensible_cells = portfolio.get("no_defensible_cells")
        expected_pairs = {
            (role, tier) for role in roles for tier in self.polisher_effort_tiers()
        }
        require(
            isinstance(anonymous_options, list)
            and isinstance(no_defensible_cells, list)
            and len(anonymous_options) + len(no_defensible_cells)
            == len(expected_pairs),
            "polisher_strategy_matrix_incomplete",
            portfolio["artifact_id"],
        )
        anonymous_ids = [option.get("anonymous_option_id") for option in anonymous_options]
        require(
            len(set(anonymous_ids)) == len(anonymous_options)
            and all(
                isinstance(option_id, str)
                and POLISHER_ANONYMOUS_OPTION_ID.fullmatch(option_id)
                for option_id in anonymous_ids
            ),
            "polisher_anonymous_option_id",
            portfolio["artifact_id"],
        )
        tiers = self.polisher_effort_tiers()
        require(
            all(cell.get("status") == "no_defensible_option" for cell in no_defensible_cells)
            and len(
                {
                    cell.get("anonymous_cell_id")
                    for cell in no_defensible_cells
                }
            )
            == len(no_defensible_cells)
            and all(
                POLISHER_ANONYMOUS_OPTION_ID.fullmatch(cell.get("anonymous_cell_id", ""))
                for cell in no_defensible_cells
            )
            and all(
                option.get("effort_tier") in tiers for option in anonymous_options
            )
            and all(
                cell.get("effort_tier") in tiers for cell in no_defensible_cells
            ),
            "polisher_strategy_matrix_incomplete",
            portfolio["artifact_id"],
        )
        for option in anonymous_options:
            require(
                option.get("status") == "proposed"
                and option.get("feasibility") in {"certain", "high"}
                and isinstance(option.get("plan"), dict)
                and not missing_fields(option["plan"], list(POLISHER_PLAN_REQUIRED_FIELDS)),
                "polisher_anonymous_portfolio_schema",
                str(option.get("anonymous_option_id")),
            )
        input_report_refs = {
            f"{artifact['artifact_id']}@{artifact['version_id']}": report
            for artifact, report in reports_by_role.values()
        }
        assembly = portfolio.get("assembler_contract", {})
        require(
            assembly.get("scoring_performed") is False
            and assembly.get("ranking_performed") is False
            and assembly.get("automatic_selection_performed") is False,
            "polisher_assembler_judgment",
            portfolio["artifact_id"],
        )
        require(
            assembly.get("invented_option_ids") == [],
            "polisher_assembler_invented_option",
            portfolio["artifact_id"],
        )
        require(
            set(portfolio.get("preserved_dissent_ids", [])) >= self.dissent_ids,
            "dissent_not_preserved",
            portfolio["artifact_id"],
        )
        require(
            portfolio.get("target_requirements_verified") is True
            or portfolio.get("target_specific_fit_claimed") is False,
            "target_requirements_unverified",
            portfolio["artifact_id"],
        )
        manifests = [
            artifact
            for artifact in outputs
            if self.artifact_has_role(artifact, "strategy_report_manifest")
        ]
        require(len(manifests) == 1, "polisher_strategy_manifest", event["event_id"])
        manifest = manifests[0].get("strategy_manifest", {})
        require(
            manifest.get("matrix_cell_count") == len(expected_pairs)
            and manifest.get("peer_outputs_visible") is False
            and manifest.get("sealed") is True
            and manifest.get("evaluator_visible") is False,
            "polisher_strategy_manifest",
            manifests[0]["artifact_id"],
        )
        mapping = manifest.get("source_report_bindings")
        require(
            isinstance(mapping, list) and len(mapping) == len(expected_pairs),
            "polisher_strategy_matrix_incomplete",
            manifests[0]["artifact_id"],
        )
        observed_pairs = {
            (
                cell.get("review_perspective"),
                cell.get("source_cell", {}).get("effort_tier"),
            )
            for cell in mapping
        }
        require(
            observed_pairs == expected_pairs and len(observed_pairs) == len(mapping),
            "polisher_strategy_matrix_incomplete",
            manifests[0]["artifact_id"],
        )
        mapped_anonymous_ids = {
            cell.get("anonymous_option_id")
            for cell in mapping
            if cell.get("source_cell", {}).get("status") == "proposed"
        }
        mapped_no_defensible_ids = {
            cell.get("anonymous_cell_id")
            for cell in mapping
            if cell.get("source_cell", {}).get("status") == "no_defensible_option"
        }
        require(
            mapped_anonymous_ids == set(anonymous_ids)
            and mapped_no_defensible_ids
            == {cell["anonymous_cell_id"] for cell in no_defensible_cells},
            "polisher_manifest_portfolio_mismatch",
            manifests[0]["artifact_id"],
        )
        anonymous_by_id = {
            option["anonymous_option_id"]: option for option in anonymous_options
        }
        mapped_instances: list[str] = []
        for cell in mapping:
            source_ref = cell.get("source_report_ref")
            report = input_report_refs.get(source_ref)
            require(
                report is not None
                and report["reviewer_role"] == cell.get("review_perspective")
                and report["reviewer_instance_id"] == cell.get("reviewer_instance_id")
                and report["review_id"] == cell.get("review_id"),
                "polisher_matrix_lineage",
                str(source_ref),
            )
            source_artifact = next(
                artifact
                for artifact, candidate_report in reports_by_role.values()
                if candidate_report is report
            )
            require(
                cell.get("raw_report_path") == source_artifact["path"]
                and cell.get("raw_report_sha256")
                in {"computed", source_artifact["content_digest"]},
                "polisher_matrix_lineage",
                str(source_ref),
            )
            cell["raw_report_sha256"] = source_artifact["content_digest"]
            mapped_instances.append(cell["reviewer_instance_id"])
            source_option = next(
                (
                    item
                    for item in report["strategy_options"]
                    if item["effort_tier"]
                    == cell.get("source_cell", {}).get("effort_tier")
                ),
                None,
            )
            require(source_option is not None, "polisher_matrix_lineage", str(source_ref))
            if source_option["status"] == "proposed":
                anonymous_option = anonymous_by_id[cell["anonymous_option_id"]]
                computed_plan_digest = self.polisher_plan_digest(source_option["plan"])
                require(
                    source_option["provisional_option_id"]
                    == cell.get("source_cell", {}).get("provisional_option_id")
                    and source_option["status"]
                    == cell.get("source_cell", {}).get("status")
                    and source_option["status"] == anonymous_option.get("status")
                    and source_option["effort_tier"] == anonymous_option.get("effort_tier")
                    and source_option.get("feasibility") == anonymous_option.get("feasibility")
                    and source_option.get("plan") == anonymous_option.get("plan")
                    and cell.get("plan_digest") in {"computed", computed_plan_digest},
                    "polisher_manifest_portfolio_mismatch",
                    str(source_ref),
                )
                cell["plan_digest"] = computed_plan_digest
            else:
                no_defensible = next(
                    item
                    for item in no_defensible_cells
                    if item["anonymous_cell_id"] == cell.get("anonymous_cell_id")
                )
                require(
                    cell.get("source_cell", {}).get("status")
                    == "no_defensible_option"
                    and no_defensible.get("effort_tier") == source_option["effort_tier"]
                    and no_defensible.get("reason") == source_option.get("reason"),
                    "polisher_manifest_portfolio_mismatch",
                    str(source_ref),
                )
        require(
            set(mapped_instances) == set(instances),
            "polisher_strategy_manifest",
            manifests[0]["artifact_id"],
        )
        require(
            manifest.get("access_scope")
            == "orchestrator_and_lineage_validator_only",
            "polisher_strategy_manifest",
            manifests[0]["artifact_id"],
        )
        report_refs = set(input_report_refs)
        manifest_parents = set(manifests[0]["based_on"])
        portfolio_ref = f"{portfolio['artifact_id']}@{portfolio['version_id']}"
        input_refs = {
            f"{self.artifacts[artifact_id]['artifact_id']}@{self.artifacts[artifact_id]['version_id']}"
            for artifact_id in event["input_artifact_ids"]
        }
        require(
            report_refs | input_refs | {portfolio_ref} <= manifest_parents,
            "polisher_matrix_lineage",
            manifests[0]["artifact_id"],
        )

    def validate_polisher_revision_brief(
        self, event: dict[str, Any], outputs: list[dict[str, Any]]
    ) -> None:
        briefs = [artifact for artifact in outputs if self.artifact_has_role(artifact, "revision_plan")]
        if not briefs:
            return
        require(
            event["destination_skill"]
            == self.machine.get("primary_assembler_skill", "research-polisher-plan-assembler")
            and len(briefs) == 1,
            "polisher_revision_brief_creator",
            event["event_id"],
        )
        input_artifacts = [self.artifacts[artifact_id] for artifact_id in event["input_artifact_ids"]]
        require(
            any(self.artifact_has_role(artifact, "strategy_report_manifest") for artifact in input_artifacts),
            "polisher_revision_brief_provenance",
            event["event_id"],
        )
        portfolio = next(
            (artifact for artifact in input_artifacts if self.artifact_has_role(artifact, self.machine["primary_artifact_type"])),
            None,
        )
        evaluation = next(
            (artifact for artifact in input_artifacts if self.artifact_has_role(artifact, "evaluation_report")),
            None,
        )
        require(portfolio is not None and evaluation is not None, "polisher_revision_brief_provenance", event["event_id"])
        contract = briefs[0].get("revision_brief_contract", {})
        require(
            contract.get("anonymous") is True
            and contract.get("source_reviewer_identities_included") is False
            and contract.get("raw_report_refs_included") is False
            and contract.get("prior_scores_included") is False
            and contract.get("overall_decision_included") is False,
            "polisher_revision_brief_identity_leak",
            briefs[0]["artifact_id"],
        )
        portfolio_ids = {
            option["anonymous_option_id"] for option in portfolio.get("options", [])
        }
        brief_ids = contract.get("anonymous_option_ids")
        require(
            isinstance(brief_ids, list)
            and bool(brief_ids)
            and set(brief_ids) <= portfolio_ids
            and all(POLISHER_ANONYMOUS_OPTION_ID.fullmatch(option_id) for option_id in brief_ids),
            "polisher_revision_brief_identity_leak",
            briefs[0]["artifact_id"],
        )
        must_fix_items = contract.get("must_fix_items")
        require(
            isinstance(must_fix_items, list)
            and must_fix_items
            and all(
                item.get("anonymous_option_id") in brief_ids
                and item.get("effort_tier") in self.polisher_effort_tiers()
                and isinstance(item.get("finding_scope"), str)
                and item["finding_scope"].strip()
                and isinstance(item.get("required_evidence_ids"), list)
                for item in must_fix_items
            ),
            "polisher_revision_brief_schema",
            briefs[0]["artifact_id"],
        )
        serialized = json.dumps(contract, ensure_ascii=False, sort_keys=True)
        require(
            "source_report_ref" not in serialized
            and "reviewer_instance_id" not in serialized,
            "polisher_revision_brief_identity_leak",
            briefs[0]["artifact_id"],
        )
        required_parents = {
            f"{portfolio['artifact_id']}@{portfolio['version_id']}",
            f"{evaluation['artifact_id']}@{evaluation['version_id']}",
        }
        require(required_parents <= set(briefs[0]["based_on"]), "polisher_revision_brief_provenance", event["event_id"])
        self.pending_revision_review_ids = set()

    def validate_polisher_evaluation_report(
        self, event: dict[str, Any], report: dict[str, Any]
    ) -> None:
        portfolio = next(
            (
                self.artifacts[artifact_id]
                for artifact_id in event["input_artifact_ids"]
                if self.artifact_has_role(
                    self.artifacts[artifact_id], self.machine["primary_artifact_type"]
                )
            ),
            None,
        )
        require(portfolio is not None, "polisher_option_adjudication_incomplete", event["event_id"])
        portfolio_ids = {
            option["anonymous_option_id"] for option in portfolio.get("options", [])
        }
        portfolio_tiers = {
            option["anonymous_option_id"]: option["effort_tier"]
            for option in portfolio.get("options", [])
        }
        adjudications = report.get("option_decisions")
        require(
            isinstance(adjudications, list)
            and len(adjudications) == len(portfolio_ids),
            "polisher_option_adjudication_incomplete",
            event["event_id"],
        )
        adjudication_ids = [item.get("option_id") for item in adjudications]
        require(
            set(adjudication_ids) == portfolio_ids
            and len(set(adjudication_ids)) == len(portfolio_ids),
            "polisher_option_adjudication_incomplete",
            event["event_id"],
        )
        for item in adjudications:
            missing = missing_fields(item, list(POLISHER_OPTION_DECISION_REQUIRED_FIELDS))
            require(not missing, "polisher_option_adjudication_incomplete", f"{item.get('option_id')}: {missing}")
            require(
                item.get("decision") in POLISHER_OPTION_DECISIONS,
                "polisher_option_adjudication_invalid",
                str(item.get("option_id")),
            )
            require(
                item.get("effort_tier") == portfolio_tiers[item["option_id"]],
                "polisher_option_tier_mismatch",
                item["option_id"],
            )
            for field in (
                "method_design_compatibility",
                "evidence_claim_fit",
                "tier_correctness",
                "feasibility",
                "scientific_significance_potential",
                "practical_value_potential",
                "dissemination_potential",
                "narrative_differentiation",
                "publication_positioning",
                "target_fit",
            ):
                require(isinstance(item[field], str) and item[field].strip(), "polisher_option_adjudication_incomplete", f"{item['option_id']}: {field}")
            for field in ("fatal_findings", "major_findings", "required_repairs", "unresolved_issues"):
                require(isinstance(item[field], list), "polisher_option_adjudication_incomplete", f"{item['option_id']}: {field}")
            require(
                item["target_fit"] in {"verified_assessment", "not_assessed"},
                "target_requirements_unverified",
                item["option_id"],
            )
        target_requirements = report.get("target_requirements", {})
        require(
            target_requirements.get("status")
            in {"verified", "target_requirements_unverified", "not_applicable"},
            "target_requirements_unverified",
            event["event_id"],
        )
        dossier = next(
            self.artifacts[artifact_id]
            for artifact_id in event["input_artifact_ids"]
            if self.artifacts[artifact_id]["artifact_role"] == "research_polisher_dossier"
        )
        adapter = dossier["dossier_contract"]["target_requirements_adapter"]
        if adapter is None or adapter == "not_provided":
            require(
                target_requirements["status"] == "target_requirements_unverified"
                and all(item["target_fit"] == "not_assessed" for item in adjudications),
                "target_requirements_unverified",
                event["event_id"],
            )
        else:
            require(
                target_requirements["status"] == "verified"
                and all(
                    target_requirements.get(field) == adapter.get(field)
                    for field in ("artifact_id", "version", "sha256")
                ),
                "target_requirements_unverified",
                event["event_id"],
            )
        pareto_values = report.get("pareto_axis_values")
        require(
            isinstance(pareto_values, list)
            and len(pareto_values) == len(portfolio_ids)
            and {item.get("option_id") for item in pareto_values} == portfolio_ids,
            "polisher_pareto_axes_incomplete",
            event["event_id"],
        )
        for item in pareto_values:
            axes = item.get("values")
            require(
                isinstance(axes, dict) and set(axes) == set(POLISHER_PARETO_AXES),
                "polisher_pareto_axes_incomplete",
                str(item.get("option_id")),
            )
            require(
                all(isinstance(value, str) and bool(value.strip()) for value in axes.values()),
                "polisher_pareto_axes_invalid",
                str(item.get("option_id")),
            )
        pareto_contract = report.get("pareto_axis_contract", {})
        directions = pareto_contract.get("axis_directions")
        ordered_values = pareto_contract.get("ordered_values")
        require(
            pareto_contract.get("comparison_scope") == "within_portfolio_only"
            and pareto_contract.get("values_are_qualitative") is True
            and pareto_contract.get("weighted_total_prohibited") is True
            and isinstance(directions, dict)
            and set(directions) == set(POLISHER_PARETO_AXES)
            and all(value in {"higher_is_better", "lower_is_better"} for value in directions.values())
            and isinstance(ordered_values, list)
            and len(ordered_values) >= 3
            and len(set(ordered_values)) == len(ordered_values)
            and all(
                value in set(ordered_values)
                for item in pareto_values
                for value in item["values"].values()
            ),
            "polisher_pareto_axes_incomplete",
            event["event_id"],
        )
        decisions = [item["decision"] for item in adjudications]
        if report["decision"] == "ready_for_human_selection":
            require(
                "retain" in decisions and "revise" not in decisions,
                "polisher_false_ready_adjudication",
                event["event_id"],
            )
        elif report["decision"] in {"revision_required", "specialist_review_required"}:
            require("revise" in decisions, "polisher_revision_adjudication_missing", event["event_id"])
        elif report["decision"] == "no_defensible_option":
            require("retain" not in decisions and "revise" not in decisions, "polisher_decision_route", event["event_id"])

    def validate_polisher_selection_outputs(
        self, event: dict[str, Any], outputs: list[dict[str, Any]]
    ) -> None:
        require(len(outputs) == 1, "polisher_selection_output", event["event_id"])
        package = outputs[0]
        contract = package.get("selection_dossier_contract", {})
        require(
            package["artifact_role"] == "research_polisher_selection_dossier"
            and contract.get("selection_status")
            == "human_strategy_selection_required",
            "polisher_selection_output",
            package["artifact_id"],
        )
        require(
            contract.get("pareto_comparison") is True
            and contract.get("weighted_total_score_used") is False
            and contract.get("automatic_selection_performed") is False
            and contract.get("unique_best_declared") is False
            and contract.get("source_content_modified") is False,
            "polisher_selection_judgment",
            package["artifact_id"],
        )
        require(
            set(contract.get("preserved_dissent_ids", [])) >= self.dissent_ids,
            "dissent_not_preserved",
            package["artifact_id"],
        )
        require(
            contract.get("target_requirements_verified") is True
            or contract.get("target_specific_fit_claimed") is False,
            "target_requirements_unverified",
            package["artifact_id"],
        )
        evaluation_artifacts = [
            self.artifacts[artifact_id]
            for artifact_id in event["input_artifact_ids"]
            if self.artifact_has_role(self.artifacts[artifact_id], "evaluation_report")
        ]
        require(len(evaluation_artifacts) == 1, "polisher_selection_adjudication", event["event_id"])
        review_id = self.review_artifact_reports.get(evaluation_artifacts[0]["artifact_id"])
        evaluation = self.review_reports.get(review_id or "")
        require(evaluation is not None, "polisher_selection_adjudication", event["event_id"])
        adjudications = evaluation.get("option_decisions", [])
        expected = {
            decision: sorted(
                item["option_id"]
                for item in adjudications
                if item["decision"] == decision
            )
            for decision in ("retain", "reject", "not_assessable", "revise")
        }
        require(
            expected["retain"]
            and not expected["revise"]
            and sorted(contract.get("retained_option_ids", [])) == expected["retain"]
            and sorted(contract.get("rejected_option_ids", [])) == expected["reject"]
            and sorted(contract.get("not_assessable_option_ids", []))
            == expected["not_assessable"],
            "polisher_selection_adjudication",
            package["artifact_id"],
        )
        pareto_data = contract.get("pareto_data")
        require(
            isinstance(pareto_data, list) and len(pareto_data) == len(expected["retain"]),
            "polisher_selection_adjudication",
            package["artifact_id"],
        )
        pareto_by_id = {
            item.get("option_id"): item.get("values") for item in pareto_data
        }
        evaluation_pareto = {
            item["option_id"]: item["values"]
            for item in evaluation.get("pareto_axis_values", [])
            if item["option_id"] in expected["retain"]
        }
        axis_contract = evaluation["pareto_axis_contract"]
        rank = {value: index for index, value in enumerate(axis_contract["ordered_values"])}

        def benefit(option_id: str, axis: str) -> int:
            raw = rank[evaluation_pareto[option_id][axis]]
            return raw if axis_contract["axis_directions"][axis] == "higher_is_better" else -raw

        expected_non_dominated = []
        for candidate in expected["retain"]:
            dominated = False
            for challenger in expected["retain"]:
                if challenger == candidate:
                    continue
                comparisons = [
                    (benefit(challenger, axis), benefit(candidate, axis))
                    for axis in POLISHER_PARETO_AXES
                ]
                if all(left >= right for left, right in comparisons) and any(
                    left > right for left, right in comparisons
                ):
                    dominated = True
                    break
            if not dominated:
                expected_non_dominated.append(candidate)
        require(
            set(pareto_by_id) == set(expected["retain"])
            and pareto_by_id == evaluation_pareto
            and expected_non_dominated
            and sorted(contract.get("non_dominated_option_ids", []))
            == sorted(expected_non_dominated)
            and contract.get("pareto_axis_contract") == axis_contract,
            "polisher_selection_adjudication",
            package["artifact_id"],
        )

    def process_entry_gate(self, event: dict[str, Any]) -> dict[str, Any]:
        require(not self.entry_gate_verified, "entry_gate_receipts", "entry gate repeated")
        require(self.current_primary is not None, "entry_gate_receipts", "primary artifact missing")
        verified: dict[str, dict[str, Any]] = {}
        gate_contracts = self.machine["scenario_entry_gate_contracts"][self.fixture["entry_mode"]]
        for gate_name, receipt in self.fixture["entry_gate_receipts"].items():
            artifact_ids = list(receipt.get("artifact_ids", []))
            if receipt.get("artifact_id"):
                artifact_ids = [receipt["artifact_id"]]
            review_id = receipt.get("review_id")
            require(bool(artifact_ids) ^ bool(review_id), "entry_gate_receipts", gate_name)
            if artifact_ids:
                artifacts = [self.artifacts.get(artifact_id) for artifact_id in artifact_ids]
                require(
                    all(artifact is not None and artifact["frozen"] is True for artifact in artifacts),
                    "entry_gate_receipts",
                    gate_name,
                )
                expected_roles = gate_contracts[gate_name].get("artifact_roles")
                require(
                    expected_roles is not None
                    and sorted(
                        self.canonical_artifact_role(artifact["artifact_role"])
                        for artifact in artifacts
                    )
                    == sorted(
                        self.canonical_artifact_role(role) for role in expected_roles
                    ),
                    "entry_gate_contract",
                    gate_name,
                )
                if "versioned" in gate_name:
                    require(
                        artifact_ids == [self.current_primary["artifact_id"]],
                        "entry_gate_receipts",
                        gate_name,
                    )
                verified[gate_name] = {
                    "artifacts": [
                        {
                            "artifact_id": artifact_id,
                            "version_id": artifact["version_id"],
                            "content_digest": artifact["content_digest"],
                        }
                        for artifact_id, artifact in zip(artifact_ids, artifacts)
                    ],
                }
            else:
                report = self.review_reports.get(review_id)
                require(report is not None, "entry_gate_receipts", gate_name)
                require(
                    report["reviewer_skill"] == gate_contracts[gate_name].get("review_skill"),
                    "entry_gate_contract",
                    gate_name,
                )
                category = self.decision_category(report["reviewer_skill"], report["decision"])
                require(category == "pass", "entry_gate_receipts", f"{gate_name}: {report['decision']}")
                require(self.finding_route(report["findings"]) is None, "entry_gate_receipts", gate_name)
                expected_input_roles = gate_contracts[gate_name].get("input_artifact_roles")
                if expected_input_roles is not None:
                    actual_input_roles = [
                        self.artifacts[artifact_id]["artifact_role"]
                        for artifact_id in report["input_artifact_ids"]
                    ]
                    require(
                        sorted(actual_input_roles) == sorted(expected_input_roles),
                        "entry_gate_contract",
                        gate_name,
                    )
                verified[gate_name] = {
                    "review_id": review_id,
                    "reviewer_instance_id": report["reviewer_instance_id"],
                    "decision": report["decision"],
                }
        self.transition("preprocessing", "entry_gate_passed", event["event_id"])
        self.transition("artifact_frozen", "versioned_artifact_created", event["event_id"])
        self.entry_gate_verified = True
        return {
            "files_read": [],
            "actual_write_paths": [],
            "input_hashes_before": {},
            "input_hashes_after": {},
            "verified_entry_gates": verified,
        }

    def validate_review(self, event: dict[str, Any], report: dict[str, Any]) -> None:
        missing = missing_fields(report, self.schema["review_required"])
        require(not missing, "review_schema", f"{event['event_id']} missing review fields: {missing}")
        destination = event["destination_skill"]
        skill = self.skills[destination]
        require(skill["requires_independent_subagent"] is True, "review_not_independent", destination)
        require(report["reviewer_skill"] == destination, "review_identity", event["event_id"])
        require(report["reviewer_instance_id"] == event["actor_instance_id"], "review_identity", event["event_id"])
        require(report["workflow_id"] == self.fixture["workflow_id"], "review_identity", event["event_id"])
        require(report["input_artifact_ids"] == event["input_artifact_ids"], "review_inputs", event["event_id"])
        require(report["input_versions"] == event["input_versions"], "review_inputs", event["event_id"])
        require(report["isolation_mode"] == self.contract["reviewer_isolation_mode"], "review_not_independent", event["event_id"])
        require(report["prior_scores_visible"] is False, "prior_score_visible", event["event_id"])
        require(report["source_edits_performed"] is False, "source_edit_claim", event["event_id"])
        self.decision_category(destination, report["decision"])
        require(set(report["files_read"]) <= set(event["allowed_read_paths"]), "read_scope", event["event_id"])
        require(set(report["files_read"]) == {self.artifacts[item]["path"] for item in event["input_artifact_ids"]}, "files_read_mismatch", event["event_id"])
        require(event["actor_instance_id"] not in self.reviewer_instances, "duplicate_reviewer_instance", event["actor_instance_id"])
        require(event["actor_instance_id"] not in self.writer_instances, "reviewer_is_writer", event["actor_instance_id"])
        for artifact_id in event["input_artifact_ids"]:
            require(self.artifacts[artifact_id]["created_by_instance_id"] != event["actor_instance_id"], "reviewer_is_writer", event["event_id"])

        if (
            self.workflow == "research_polisher"
            and destination
            == self.machine.get(
                "strategy_reviewer_skill", "research-polisher-strategy-reviewer"
            )
        ):
            self.validate_polisher_strategy_report(event, report)
        if (
            self.workflow == "research_polisher"
            and destination == self.machine["evaluator_skill"]
        ):
            visible_roles = {
                self.canonical_artifact_role(self.artifacts[item]["artifact_role"])
                for item in event["input_artifact_ids"]
            }
            require(
                not visible_roles.intersection(
                    {
                        "strategy_report",
                        "strategy_report_manifest",
                        "evaluation_report",
                        "revision_plan",
                    }
                ),
                "forbidden_review_input",
                event["event_id"],
            )
            require(
                report.get("raw_strategy_reports_visible") is False
                and report.get("strategist_identities_visible") is False,
                "polisher_evaluator_blindness",
                event["event_id"],
            )
            require(
                report.get("sealed_provenance_visible") is False,
                "polisher_evaluator_blindness",
                event["event_id"],
            )
            self.validate_polisher_evaluation_report(event, report)

        if self.workflow == "idea" and destination == self.machine["evaluator_skill"]:
            dossiers = [
                self.artifacts[item]
                for item in event["input_artifact_ids"]
                if self.artifact_has_role(self.artifacts[item], self.machine["primary_artifact_type"])
            ]
            require(len(dossiers) == 1, "idea_dossier_binding", event["event_id"])
            dossier = dossiers[0]
            expected_path = dossier["path"]
            require(
                event["input_artifact_ids"] == [dossier["artifact_id"]]
                and event["input_versions"] == [dossier["version_id"]]
                and event["allowed_read_paths"] == [expected_path]
                and report["input_artifact_ids"] == [dossier["artifact_id"]]
                and report["input_versions"] == [dossier["version_id"]]
                and report["files_read"] == [expected_path],
                "idea_dossier_only_input",
                event["event_id"],
            )
            if report.get("reviewed_dossier_digest") == "computed":
                report["reviewed_dossier_digest"] = dossier["content_digest"]
            require(
                report.get("reviewed_dossier_digest") == dossier["content_digest"]
                and report.get("complete_dossier_confirmed") is True
                and report.get("dossier_only_input_confirmed") is True,
                "idea_dossier_binding",
                event["event_id"],
            )
            require(
                report.get("identity_drift_detected") is False
                and report.get("prior_versions_visible") is False
                and report.get("revision_delta_visible") is False,
                "forbidden_review_input",
                event["event_id"],
            )
            require(
                all(finding.get("title") and finding.get("dossier_locator") for finding in report["findings"]),
                "idea_finding_locator",
                event["event_id"],
            )

        final_verifier = destination in self.contract["verifier_compositor_outputs"]
        is_panel = destination == PANEL_SKILLS[self.workflow]
        forbidden_roles = set(self.contract["blindness_policy"]["forbidden_input_roles_for_evaluator_or_panel"])
        if destination == self.machine["evaluator_skill"] or is_panel:
            visible_roles = {
                self.canonical_artifact_role(self.artifacts[item]["artifact_role"])
                for item in event["input_artifact_ids"]
            }
            require(not (visible_roles & forbidden_roles), "forbidden_review_input", f"{event['event_id']}: {visible_roles & forbidden_roles}")
            if is_panel:
                mode = self.fixture["panel"]["mode"]
                mode_forbidden = set(
                    self.contract["panel_contracts"][self.workflow]
                    .get("mode_forbidden_input_roles", {})
                    .get(mode, [])
                )
                require(
                    not (visible_roles & mode_forbidden),
                    "forbidden_panel_mode_input",
                    f"{event['event_id']}: {visible_roles & mode_forbidden}",
                )

        for finding in report["findings"]:
            missing_finding = missing_fields(finding, self.schema["finding_required"])
            require(not missing_finding, "finding_schema", f"{event['event_id']}: {missing_finding}")
            require(finding["source_review_id"] == report["review_id"], "finding_provenance", finding["finding_id"])

    def process_review(self, event: dict[str, Any]) -> dict[str, Any]:
        self.validate_dispatch(event)
        report = event.get("review_report")
        require(isinstance(report, dict), "review_schema", event["event_id"])
        self.validate_review(event, report)
        final_verifier = event["destination_skill"] in self.contract["verifier_compositor_outputs"]
        pre_materialize_category = self.decision_category(event["destination_skill"], report["decision"])
        outputs = event.get("outputs", [])
        if final_verifier:
            output_roles = [artifact["artifact_role"] for artifact in outputs]
            if pre_materialize_category == "pass":
                require(
                    sorted(output_roles)
                    == sorted(self.contract["verifier_compositor_outputs"][event["destination_skill"]]),
                    "verifier_output_contract",
                    event["event_id"],
                )
            else:
                require(
                    bool(output_roles)
                    and set(output_roles) <= {"verification_report", "continuation_brief"}
                    and "final_handoff_package" not in output_roles,
                    "verifier_output_contract",
                    event["event_id"],
                )
        if final_verifier and pre_materialize_category == "pass":
            self.validate_ready_for_package(event)
        require(outputs, "review_schema", f"{event['event_id']} has no report artifact")
        observation = self.materialize_outputs(event, outputs, report)
        self.reviewer_instances.add(event["actor_instance_id"])
        require(report["review_id"] not in self.review_reports, "duplicate_review_id", report["review_id"])
        self.review_reports[report["review_id"]] = report

        destination = event["destination_skill"]
        if (
            self.workflow == "research_polisher"
            and destination
            == self.machine.get(
                "strategy_reviewer_skill", "research-polisher-strategy-reviewer"
            )
        ):
            self.strategy_reports_by_role.setdefault(report["reviewer_role"], []).append(
                report["review_id"]
            )
        is_panel = destination == PANEL_SKILLS[self.workflow]
        category = self.decision_category(destination, report["decision"])
        for finding in report["findings"]:
            self.findings_by_id[finding["finding_id"]] = finding
            if finding.get("dissent"):
                self.dissent_ids.add(finding["finding_id"])
            if finding.get("status") == "resolved":
                self.fatal_ids.discard(finding["finding_id"])
            elif (
                finding["severity"] in {"fatal", "blocking"} or finding["blocking"] is True
            ):
                self.fatal_ids.add(finding["finding_id"])
        route = self.finding_route(report["findings"])
        is_polisher_strategy = (
            self.workflow == "research_polisher"
            and destination
            == self.machine.get(
                "strategy_reviewer_skill", "research-polisher-strategy-reviewer"
            )
        )

        if is_polisher_strategy:
            if route in {"blocked", "stopped"}:
                self.transition(route, "fatal_or_blocking_finding" if route == "blocked" else "unfixable_no_gain_or_user_stop", event["event_id"])
            else:
                routed_state = self.polisher_decision_state(destination, report["decision"])
                if routed_state == "independent_review_pending":
                    self.transition(
                        "independent_review_pending",
                        "required_reviewer_unavailable",
                        event["event_id"],
                    )
                elif routed_state in {"clarification_stop", "no_defensible_option"}:
                    self.set_polisher_route_state(routed_state, report["decision"], event["event_id"])
                else:
                    require(routed_state == "continue" and route is None, "polisher_decision_route", event["event_id"])
        elif is_panel:
            require(self.state == "panel_pending", "registry_lifecycle_mismatch", event["event_id"])
            require(self.current_primary is not None, "missing_primary_artifact", event["event_id"])
            require(self.current_primary["artifact_id"] in report["input_artifact_ids"], "panel_current_artifact", event["event_id"])
            require(self.current_primary["version_id"] in report["input_versions"], "panel_current_artifact", event["event_id"])
            role = report["reviewer_role"]
            require(role not in self.panel_instances, "duplicate_panel_role", role)
            require(event["actor_instance_id"] not in self.panel_instances.values(), "duplicate_reviewer_instance", event["actor_instance_id"])
            require(report.get("peer_outputs_visible") is False, "peer_output_visible", event["event_id"])
            self.panel_instances[role] = event["actor_instance_id"]
            self.panel_review_ids.add(report["review_id"])
        elif destination == self.machine["evaluator_skill"]:
            require(self.entry_gate_verified, "entry_gate_receipts", event["event_id"])
            require(self.state == "artifact_frozen", "registry_lifecycle_mismatch", event["event_id"])
            require(self.current_primary is not None, "missing_primary_artifact", event["event_id"])
            require(self.current_primary["artifact_id"] in report["input_artifact_ids"], "review_inputs", event["event_id"])
            require(self.current_primary["version_id"] in report["input_versions"], "review_inputs", event["event_id"])
            self.evaluator_instances.append(event["actor_instance_id"])
            self.transition("pending_review", "independent_review_dispatched", event["event_id"])
            polisher_route = (
                self.polisher_decision_state(destination, report["decision"])
                if self.workflow == "research_polisher"
                else None
            )
            if route in {"blocked", "stopped"}:
                self.transition(route, "fatal_or_blocking_finding" if route == "blocked" else "unfixable_no_gain_or_user_stop", event["event_id"])
            elif polisher_route == "independent_review_pending":
                self.transition("independent_review_pending", "required_reviewer_unavailable", event["event_id"])
            elif polisher_route in {
                "clarification_stop",
                "specialist_review_pending",
                "no_defensible_option",
            }:
                self.set_polisher_route_state(polisher_route, report["decision"], event["event_id"])
            elif category == "revise":
                self.pending_revision_review_ids = {report["review_id"]}
                self.transition("revision_required", "fixable_revision_requested", event["event_id"])
            elif category == "pass":
                require(route is None, "decision_finding_mismatch", event["event_id"])
                self.latest_evaluated_version = self.current_primary["version_id"]
                if self.panel_patch_pending:
                    require(self.panel_complete, "panel_gate", "panel patch lacks completed panel")
                    self.transition("packaging_pending", "panel_patch_latest_version_accepted", event["event_id"])
                    self.panel_patch_pending = False
                elif not self.post_evaluation_panel_required():
                    trigger = (
                        "bounded_exploration_reviews_complete"
                        if self.workflow == "idea"
                        and self.direction_profile() == "bounded_exploration"
                        else "latest_strategy_portfolio_accepted"
                    )
                    self.transition(
                        "packaging_pending",
                        trigger,
                        event["event_id"],
                    )
                else:
                    self.transition("panel_pending", "latest_version_accepted", event["event_id"])
            else:
                self.transition("stopped", "unfixable_no_gain_or_user_stop", event["event_id"])
        elif final_verifier:
            if category == "pass":
                require(route is None, "verification_decision", event["event_id"])
                require(report.get("workflow_state") == "human_signoff_required", "verifier_identity_contract", event["event_id"])
                if destination == "perspective-final-compositor":
                    require(report.get("source_version") == self.current_primary["version_id"], "verifier_identity_contract", event["event_id"])
                    require(report.get("evaluated_version") == self.latest_evaluated_version, "verifier_identity_contract", event["event_id"])
                    require(report.get("text_identity_verified") is True, "verifier_identity_contract", event["event_id"])
                copied = [item for item in outputs if item.get("copy_of") == self.current_primary["artifact_id"]]
                for item in copied:
                    require(item["content_digest"] == self.current_primary["content_digest"], "compositor_copy_mismatch", event["event_id"])
                if destination == "perspective-final-compositor":
                    require(copied, "compositor_copy_mismatch", event["event_id"])
                self.validate_package_output_lineage(event, outputs)
                self.transition("human_signoff_required", "package_verified", event["event_id"])
            elif report["decision"] == "independent_review_pending":
                self.transition("independent_review_pending", "required_reviewer_unavailable", event["event_id"])
            elif report["decision"] == "blocked":
                self.transition("blocked", "fatal_or_blocking_finding", event["event_id"])
            else:
                self.transition("stopped", "unfixable_no_gain_or_user_stop", event["event_id"])
        else:
            if route in {"blocked", "stopped"}:
                self.transition(route, "fatal_or_blocking_finding" if route == "blocked" else "unfixable_no_gain_or_user_stop", event["event_id"])
            elif category == "revise":
                raise ScenarioViolation("auxiliary_review_requires_revision", event["event_id"])
            elif category == "stop":
                self.transition("stopped", "unfixable_no_gain_or_user_stop", event["event_id"])
            else:
                require(route is None, "decision_finding_mismatch", event["event_id"])
        return observation

    def process_panel_gate(self, event: dict[str, Any]) -> dict[str, Any]:
        require(self.state == "panel_pending", "registry_lifecycle_mismatch", event["event_id"])
        required_roles = set(self.fixture["panel"]["required_roles"])
        require(set(self.panel_instances) == required_roles, "panel_roles_incomplete", f"expected {sorted(required_roles)}, got {sorted(self.panel_instances)}")
        require(set(event.get("preserved_dissent_ids", [])) >= self.dissent_ids, "dissent_not_preserved", event["event_id"])
        self.panel_complete = True
        category = self.decision_category(PANEL_SKILLS[self.workflow], event["decision"])
        panel_contract = self.contract["panel_contracts"][self.workflow]
        individual_decisions = [
            report["decision"]
            for review_id, report in self.review_reports.items()
            if review_id in self.panel_review_ids
        ]
        minor_decisions = set(panel_contract.get("minor_revision_decisions", []))
        substantive_decisions = set(panel_contract.get("substantive_revision_decisions", []))
        aggregate_decision = event["decision"]
        individual_categories = [
            self.decision_category(PANEL_SKILLS[self.workflow], decision)
            for decision in individual_decisions
        ]
        if "stop" in individual_categories:
            require(category == "stop", "panel_aggregate_understates_revision", event["event_id"])
        elif "revise" in individual_categories:
            require(category == "revise", "panel_aggregate_understates_revision", event["event_id"])
        if any(decision in substantive_decisions for decision in individual_decisions):
            require(
                aggregate_decision in substantive_decisions,
                "panel_aggregate_understates_revision",
                event["event_id"],
            )
        elif any(decision in minor_decisions for decision in individual_decisions):
            require(
                aggregate_decision in minor_decisions | substantive_decisions,
                "panel_aggregate_understates_revision",
                event["event_id"],
            )
        panel_findings = [
            finding
            for review_id, report in self.review_reports.items()
            if review_id in self.panel_review_ids
            for finding in report["findings"]
        ]
        route = self.finding_route(panel_findings)
        if route == "blocked":
            self.transition("blocked", "fatal_or_blocking_finding", event["event_id"])
        elif route == "stopped":
            self.transition("stopped", "unfixable_no_gain_or_user_stop", event["event_id"])
        elif route == "revision_required":
            require(category == "revise", "decision_finding_mismatch", event["event_id"])
            self.pending_revision_review_ids = {
                review_id
                for review_id in self.panel_review_ids
                if self.decision_category(PANEL_SKILLS[self.workflow], self.review_reports[review_id]["decision"]) == "revise"
                or self.finding_route(self.review_reports[review_id]["findings"]) == "revision_required"
            }
            self.panel_revision_scope = (
                "minor" if aggregate_decision in minor_decisions else "substantive"
            )
            self.transition("revision_required", "panel_requests_substantive_change", event["event_id"])
            if self.panel_revision_scope == "substantive":
                self.panel_instances = {}
                self.panel_review_ids = set()
                self.panel_complete = False
        elif category == "revise":
            self.pending_revision_review_ids = {
                review_id
                for review_id in self.panel_review_ids
                if self.decision_category(PANEL_SKILLS[self.workflow], self.review_reports[review_id]["decision"]) == "revise"
            }
            self.panel_revision_scope = (
                "minor" if aggregate_decision in minor_decisions else "substantive"
            )
            self.transition("revision_required", "panel_requests_substantive_change", event["event_id"])
            if self.panel_revision_scope == "substantive":
                self.panel_instances = {}
                self.panel_review_ids = set()
                self.panel_complete = False
        elif category == "pass":
            require(route is None, "decision_finding_mismatch", event["event_id"])
            self.transition("packaging_pending", "panel_gate_passed", event["event_id"])
        else:
            self.transition("stopped", "unfixable_no_gain_or_user_stop", event["event_id"])
        return {"files_read": [], "actual_write_paths": [], "input_hashes_before": {}, "input_hashes_after": {}}

    def validate_ready_for_package(self, event: dict[str, Any]) -> None:
        require(self.current_primary is not None, "missing_primary_artifact", event["event_id"])
        require(self.entry_gate_verified, "entry_gate_receipts", event["event_id"])
        qualifying = event.get("qualifying_evaluation_version", self.latest_evaluated_version)
        require(qualifying == self.current_primary["version_id"], "stale_evaluation", f"{qualifying} != {self.current_primary['version_id']}")
        require(self.latest_evaluated_version == self.current_primary["version_id"], "stale_evaluation", event["event_id"])
        if self.post_evaluation_panel_required():
            require(self.panel_complete, "panel_gate", event["event_id"])
        require(not self.fatal_ids, "fatal_gate_bypassed", event["event_id"])
        require(set(event.get("preserved_dissent_ids", [])) >= self.dissent_ids, "dissent_not_preserved", event["event_id"])
        require(set(event.get("artifact_index_dissent_ids", [])) >= self.dissent_ids, "dissent_not_indexed", event["event_id"])
        require(event.get("automatic_external_submission") is False, "external_submission", event["event_id"])
        contract = self.contract["package_input_contracts"][self.workflow]
        input_artifacts = [self.artifacts[artifact_id] for artifact_id in event.get("input_artifact_ids", [])]
        require(input_artifacts, "package_input_contract", event["event_id"])
        require(
            {
                self.canonical_artifact_role(artifact["artifact_role"])
                for artifact in input_artifacts
            }
            <= {
                self.canonical_artifact_role(role)
                for role in contract["allowed_roles"]
            },
            "verifier_forbidden_input",
            event["event_id"],
        )
        current_ref = f"{self.current_primary['artifact_id']}@{self.current_primary['version_id']}"
        direction_profile = self.fixture.get("direction_profile", "focused_optimization")
        current_dossier_count = len([
            artifact
            for artifact in input_artifacts
            if self.canonical_artifact_role(artifact["artifact_role"]) == "idea_dossier"
        ])
        for requirement in contract["required_inputs"]:
            matches = [
                artifact
                for artifact in input_artifacts
                if self.canonical_artifact_role(artifact["artifact_role"])
                == self.canonical_artifact_role(requirement["artifact_role"])
                and (
                    "source_skill" not in requirement
                    or artifact["source_skill"] == requirement["source_skill"]
                )
                and (
                    "source_skills" not in requirement
                    or artifact["source_skill"] in set(requirement["source_skills"])
                )
            ]
            required_profile = requirement.get("required_when_direction_profile")
            if required_profile and required_profile != direction_profile:
                require(not matches, "package_input_contract", f"{event['event_id']}: {requirement}")
                continue
            profile_counts = requirement.get("count_by_direction_profile", {})
            if direction_profile in profile_counts:
                expected = profile_counts[direction_profile]
                if isinstance(expected, int):
                    require(len(matches) == expected, "package_input_contract", f"{event['event_id']}: {requirement}")
                else:
                    require(
                        expected["minimum"] <= len(matches) <= expected["maximum"],
                        "package_input_contract",
                        f"{event['event_id']}: {requirement}",
                    )
            if requirement.get("count_from_panel_roles"):
                expected_count = len(self.fixture["panel"]["required_roles"])
                require(len(matches) == expected_count, "package_input_contract", f"{event['event_id']}: {requirement}")
            elif "minimum_count" in requirement:
                require(len(matches) >= requirement["minimum_count"], "package_input_contract", f"{event['event_id']}: {requirement}")
                if "maximum_count" in requirement:
                    require(len(matches) <= requirement["maximum_count"], "package_input_contract", f"{event['event_id']}: {requirement}")
            elif requirement.get("count_per_current_idea_node") is not None:
                require(
                    len(matches) == current_dossier_count * requirement["count_per_current_idea_node"],
                    "package_input_contract",
                    f"{event['event_id']}: {requirement}",
                )
            elif requirement.get("count_must_equal_current_idea_dossier_count"):
                require(len(matches) == current_dossier_count, "package_input_contract", f"{event['event_id']}: {requirement}")
            else:
                require(len(matches) == requirement["count"], "package_input_contract", f"{event['event_id']}: {requirement}")
            require(all(artifact["frozen"] is True for artifact in matches), "package_input_contract", event["event_id"])
            if requirement.get("include_all_created"):
                all_created = {
                    artifact_id
                    for artifact_id, artifact in self.artifacts.items()
                    if self.canonical_artifact_role(artifact["artifact_role"])
                    == self.canonical_artifact_role(requirement["artifact_role"])
                    and artifact["source_skill"] == requirement["source_skill"]
                }
                require({artifact["artifact_id"] for artifact in matches} == all_created, "package_input_contract", event["event_id"])
            if requirement.get("current_primary"):
                require(
                    any(
                        artifact["artifact_id"] == self.current_primary["artifact_id"]
                        and artifact["version_id"] == self.current_primary["version_id"]
                        for artifact in matches
                    ),
                    "package_input_contract",
                    event["event_id"],
                )
            if requirement.get("current_primary_lineage"):
                require(
                    any(current_ref in artifact.get("based_on", []) for artifact in matches),
                    "package_input_contract",
                    event["event_id"],
                )
            if requirement.get("latest_selected_artifact"):
                all_candidates = [
                    artifact
                    for artifact in self.artifacts.values()
                    if self.canonical_artifact_role(artifact["artifact_role"])
                    == self.canonical_artifact_role(requirement["artifact_role"])
                    and (
                        "source_skill" not in requirement
                        or artifact["source_skill"] == requirement["source_skill"]
                    )
                ]
                require(
                    bool(all_candidates) and matches[0] is all_candidates[-1],
                    "package_input_contract",
                    event["event_id"],
                )
            if requirement.get("current_primary_lineage"):
                require(current_ref in matches[0]["based_on"], "package_input_contract", event["event_id"])
            if requirement.get("selected_artifact_lineage_role"):
                selected = [
                    artifact
                    for artifact in input_artifacts
                    if self.canonical_artifact_role(artifact["artifact_role"])
                    == self.canonical_artifact_role(
                        requirement["selected_artifact_lineage_role"]
                    )
                ]
                require(len(selected) == 1, "package_input_contract", event["event_id"])
                selected_ref = f"{selected[0]['artifact_id']}@{selected[0]['version_id']}"
                require(selected_ref in matches[0]["based_on"], "package_input_contract", event["event_id"])
                if requirement.get("exact_selected_artifact_lineage"):
                    selected_role_refs = {
                        f"{artifact['artifact_id']}@{artifact['version_id']}"
                        for artifact in self.artifacts.values()
                        if self.canonical_artifact_role(artifact["artifact_role"])
                        == self.canonical_artifact_role(
                            requirement["selected_artifact_lineage_role"]
                        )
                    }
                    require(
                        set(matches[0]["based_on"]).intersection(selected_role_refs)
                        == {selected_ref},
                        "package_input_contract",
                        event["event_id"],
                    )
            if requirement.get("fresh_review_required"):
                review_id = self.review_artifact_reports.get(matches[0]["artifact_id"])
                review = self.review_reports.get(review_id or "")
                require(
                    review is not None
                    and review.get("isolation_mode") == "fresh_subagent"
                    and review.get("reviewer_instance_id")
                    == matches[0]["created_by_instance_id"],
                    "package_input_contract",
                    event["event_id"],
                )
            if requirement.get("all_panel_instances"):
                require(
                    {artifact["created_by_instance_id"] for artifact in matches}
                    == set(self.panel_instances.values()),
                    "package_input_contract",
                    event["event_id"],
                )

    def validate_package_output_lineage(self, event: dict[str, Any], outputs: list[dict[str, Any]]) -> None:
        input_refs = {
            f"{self.artifacts[artifact_id]['artifact_id']}@{self.artifacts[artifact_id]['version_id']}"
            for artifact_id in event["input_artifact_ids"]
        }
        output_parents = {parent for artifact in outputs for parent in artifact["based_on"]}
        require(input_refs <= output_parents, "package_output_lineage", event["event_id"])

    def process_package(self, event: dict[str, Any]) -> dict[str, Any]:
        self.validate_dispatch(event)
        require(event["actor_instance_id"] not in self.reviewer_instances, "writer_is_reviewer", event["actor_instance_id"])
        self.validate_ready_for_package(event)
        outputs = event.get("outputs", [])
        require(outputs, "event_schema", f"{event['event_id']} has no package outputs")
        if self.workflow == "research_polisher":
            self.validate_polisher_selection_outputs(event, outputs)
        observation = self.materialize_outputs(event, outputs, None)
        self.validate_package_output_lineage(event, outputs)
        self.writer_instances.add(event["actor_instance_id"])
        final_state = self.expected_final_state()
        trigger = (
            "selection_dossier_verified"
            if final_state == "human_strategy_selection_required"
            else (
                "bounded_exploration_comparison_handoff_verified"
                if final_state == "human_direction_selection_required"
                else "package_verified"
            )
        )
        self.transition(final_state, trigger, event["event_id"])
        return observation

    def validate_expected(self) -> None:
        expected = self.fixture["expected"]
        require(self.state == expected["final_state"], "expected_trace", f"final state {self.state}")
        require(self.primary_versions == expected["primary_versions"], "expected_trace", f"primary versions {self.primary_versions}")
        require(self.evaluator_instances == expected["evaluator_instances"], "expected_trace", f"evaluator instances {self.evaluator_instances}")
        require(self.panel_instances == expected["panel_role_instances"], "expected_trace", f"panel instances {self.panel_instances}")
        require(sorted(self.dissent_ids) == sorted(expected["dissent_ids"]), "expected_trace", f"dissent {self.dissent_ids}")
        actual_triggers = [item["trigger"] for item in self.lifecycle_receipts]
        require(actual_triggers == expected["lifecycle_triggers"], "expected_trace", f"lifecycle triggers {actual_triggers}")
        destinations = [event.get("destination_skill") for event in self.fixture["events"] if event.get("destination_skill")]
        cursor = 0
        for required in expected["required_destinations_in_order"]:
            try:
                cursor = destinations.index(required, cursor) + 1
            except ValueError as exc:
                raise ScenarioViolation("required_sequence", f"{required} missing after index {cursor}") from exc

    def context_results(self) -> dict[str, Any]:
        description_chars = 0
        for skill_md in sorted((PLUGIN / "skills").rglob("SKILL.md")):
            text = skill_md.read_text(encoding="utf-8-sig")
            front = text.split("---", 2)[1]
            description = yaml.safe_load("---\n" + front)["description"]
            description_chars += len(description)
        orchestrator = (PLUGIN / "skills" / self.machine["orchestrator"] / "SKILL.md").read_text(encoding="utf-8-sig")
        initial_load = description_chars + len(orchestrator)
        results: dict[str, Any] = {}
        policy = self.registry["context_profile_policy"]
        for name, profile in policy["profiles"].items():
            remaining = profile["total_character_budget"] - initial_load
            sufficient = remaining >= profile["minimum_working_reserve"]
            item: dict[str, Any] = {
                "measurement_unit": policy["measurement_unit"],
                "interpretation": policy["interpretation"],
                "initial_load": initial_load,
                "remaining": remaining,
                "minimum_working_reserve": profile["minimum_working_reserve"],
                "behavior": profile.get("sufficient_behavior") if sufficient else profile.get("insufficient_behavior"),
            }
            if not sufficient:
                primary = self.first_primary
                require(primary is not None, "context_profile", "fixture lacks primary artifact")
                continuation = {
                    "workflow_id": self.fixture["workflow_id"],
                    "plugin_version": self.registry["plugin_version"],
                    "entry_mode": self.fixture["entry_mode"],
                    "current_stage": "independent_evaluation",
                    "round_id": primary["round_id"],
                    "runtime_status": "context_handoff_required",
                    "suspended_workflow_state": "artifact_frozen",
                    "current_artifact_id": primary["artifact_id"],
                    "current_artifact_version": primary["version_id"],
                    "current_artifact_path": primary["path"],
                    "current_artifact_digest": primary["content_digest"],
                    "latest_qualifying_evaluation": None,
                    "gate_receipts": [],
                    "unresolved_finding_ids": [],
                    "dissent_ids": [],
                    "pending_edge": f"{self.machine['orchestrator']} -> {self.machine['evaluator_skill']}",
                    "isolation_requirements": "fresh_subagent; frozen read-only input; no prior scores",
                    "next_route": self.machine["evaluator_skill"],
                }
                missing = set(policy["continuation_required_fields"]) - set(continuation)
                require(not missing, "context_continuation", f"missing {sorted(missing)}")
                item["continuation_package"] = continuation
            results[name] = item
        return results

    def run(self) -> dict[str, Any]:
        self.validate_header()
        initial_observation = self.materialize_initial_artifacts()
        seen_events: set[str] = set()
        for sequence, event in enumerate(self.fixture["events"], start=1):
            missing = missing_fields(event, self.schema["event_base_required"])
            require(not missing, "event_schema", f"event {sequence} missing {missing}")
            require(event["type"] in self.schema["allowed_event_types"], "event_type", event["type"])
            require(event["event_id"] not in seen_events, "duplicate_event_id", event["event_id"])
            seen_events.add(event["event_id"])
            if self.state in self.schema["terminal_states"]:
                raise ScenarioViolation("event_after_terminal", f"{event['event_id']} after {self.state}")
            before_state = self.state
            lifecycle_start = len(self.lifecycle_receipts)
            if event["type"] == "entry_gate":
                observation = self.process_entry_gate(event)
            elif event["type"] == "orchestrator_record":
                observation = self.process_orchestrator_record(event)
            elif event["type"] == "produce":
                observation = self.process_produce(event)
            elif event["type"] == "review":
                observation = self.process_review(event)
            elif event["type"] == "panel_gate":
                observation = self.process_panel_gate(event)
            else:
                observation = self.process_package(event)
            require(self.state == event["expected_state_after"], "state_transition", f"{event['event_id']}: {self.state}")
            observation["lifecycle_transitions"] = self.lifecycle_receipts[lifecycle_start:]
            self.events.append(
                {
                    "event_id": event["event_id"],
                    "sequence": sequence,
                    "type": event["type"],
                    "state_before": before_state,
                    "state_after": self.state,
                    "edge": (
                        f"{event['source_skill']} -> {event['destination_skill']}"
                        if event.get("destination_skill")
                        else "orchestrator_internal_gate"
                    ),
                    "observation": observation,
                }
            )
        self.validate_expected()
        return {
            "fixture_id": self.fixture["fixture_id"],
            "workflow": self.workflow,
            "execution_kind": self.fixture["execution_kind"],
            "execution_scope": self.fixture["execution_scope"],
            "final_state": self.state,
            "initial_artifacts": initial_observation,
            "entry_gate_receipts": self.fixture["entry_gate_receipts"],
            "primary_versions": self.primary_versions,
            "evaluator_instances": self.evaluator_instances,
            "panel_role_instances": self.panel_instances,
            "dissent_ids": sorted(self.dissent_ids),
            "registry_edges_exercised": sorted(set(self.edge_receipts)),
            "registry_lifecycle_transitions": self.lifecycle_receipts,
            "events": self.events,
            "context_profiles": self.context_results(),
        }


def mutate_fixture(fixture: dict[str, Any], mutation: str) -> None:
    reviews = [event for event in fixture["events"] if event["type"] == "review"]
    panel_reviews = [event for event in reviews if event["destination_skill"].endswith("review-panel") or event["destination_skill"] == "idea-adversarial-review-panel"]
    evaluator = fixture["workflow"]
    evaluator_name = {
        "idea": "idea-evaluator",
        "proposal": "proposal-evaluator",
        "article": "article-evaluator",
        "perspective": "perspective-evaluator",
        "research_polisher": "research-polisher-methodology-publishability-reviewer",
    }[evaluator]
    evaluator_reviews = [event for event in reviews if event["destination_skill"] == evaluator_name]
    primary_produces = [
        event for event in fixture["events"]
        if event["type"] == "produce"
        and any(
            item["artifact_role"]
            in {
                "idea_dossier",
                "proposal",
                "manuscript",
                "perspective",
                "research_polisher_candidate_portfolio",
            }
            for item in event["outputs"]
        )
    ]

    if mutation == "duplicate_panel_instance":
        second = panel_reviews[1]
        first_id = panel_reviews[0]["actor_instance_id"]
        second["actor_instance_id"] = first_id
        second["review_report"]["reviewer_instance_id"] = first_id
        for output in second["outputs"]:
            output["created_by_instance_id"] = first_id
    elif mutation == "reviewer_writes_input":
        event = reviews[0]
        source_path = event["allowed_read_paths"][0]
        event["allowed_write_paths"] = [source_path]
        event["outputs"][0]["path"] = source_path
    elif mutation == "reevaluator_reads_prior_evaluation":
        prior = evaluator_reviews[0]["outputs"][0]
        event = evaluator_reviews[1]
        event["input_artifact_ids"].append(prior["artifact_id"])
        event["input_versions"].append(prior["version_id"])
        event["allowed_read_paths"].append(prior["path"])
        event["review_report"]["input_artifact_ids"].append(prior["artifact_id"])
        event["review_report"]["input_versions"].append(prior["version_id"])
        event["review_report"]["files_read"].append(prior["path"])
    elif mutation == "package_uses_stale_evaluation":
        package = next(event for event in fixture["events"] if event["type"] == "package")
        package["qualifying_evaluation_version"] = fixture["expected"]["primary_versions"][0]
    elif mutation == "fatal_finding_then_continue":
        event = evaluator_reviews[-1]
        review_id = event["review_report"]["review_id"]
        event["review_report"]["findings"].append(
            {
                "finding_id": "fatal-mutated",
                "source_review_id": review_id,
                "severity": "fatal",
                "blocking": True,
                "fixability": "unfixable",
                "status": "unresolved",
                "owner": "human_expert",
                "route": "blocked",
            }
        )
        event["expected_state_after"] = "blocked"
    elif mutation == "drop_package_dissent":
        package = next(event for event in reversed(fixture["events"]) if event["type"] in {"package", "review"} and "preserved_dissent_ids" in event)
        package["preserved_dissent_ids"] = []
    elif mutation == "remove_panel_role":
        fixture["events"].remove(panel_reviews[-1])
    elif mutation == "change_compositor_copy":
        final = next(event for event in reversed(fixture["events"]) if event["type"] == "review")
        copied = next(item for item in final["outputs"] if item.get("copy_of"))
        copied["content_override"] = "changed text"
    elif mutation == "change_registry_trigger":
        fixture["events"][0]["trigger"] = "not_registered"
    elif mutation == "overwrite_existing_artifact_path":
        first_path = primary_produces[0]["outputs"][0]["path"]
        second = primary_produces[1]
        second["outputs"][0]["path"] = first_path
        second["allowed_write_paths"] = [first_path] + [
            output["path"] for output in second["outputs"][1:]
        ]
    elif mutation == "invalid_review_decision":
        evaluator_reviews[0]["review_report"]["decision"] = "accept"
    elif mutation == "invalid_panel_tier":
        fixture["panel"]["tier"] = "full_panel"
    elif mutation == "missing_entry_gate_receipt":
        fixture["entry_gate_receipts"].pop(next(iter(fixture["entry_gate_receipts"])))
    elif mutation == "skip_entry_gate_event":
        fixture["events"] = [event for event in fixture["events"] if event["type"] != "entry_gate"]
    elif mutation == "remove_sap_preflight_input":
        event = next(event for event in fixture["events"] if event.get("destination_skill") == "sap-writer")
        index = event["input_artifact_ids"].index("proposal-sap-preflight-v1")
        event["input_artifact_ids"].pop(index)
        event["input_versions"].pop(index)
        event["allowed_read_paths"].remove("07_sap/methodology-statistics-preflight-v001.md")
    elif mutation == "misbind_entry_gate_artifact":
        fixture["entry_gate_receipts"]["context_frozen"] = {"artifact_id": "idea-evidence-v1"}
    elif mutation == "wrong_parent_version":
        primary_produces[0]["outputs"][0]["based_on"][0] = "idea-context-v1@wrong"
    elif mutation == "auxiliary_claim_requests_revision":
        event = next(event for event in reviews if event["event_id"] == "article-claim-audit-v2")
        event["review_report"]["decision"] = "revise_and_reaudit"
    elif mutation == "sap_evaluator_requests_revision":
        event = next(event for event in reviews if event["destination_skill"] == "sap-evaluator")
        event["review_report"]["decision"] = "revise"
    elif mutation == "panel_major_understated":
        event = next(event for event in panel_reviews if event["event_id"] == "perspective-panel-narrative")
        event["review_report"]["decision"] = "support_after_major_revision"
    elif mutation == "panel_stop_understated":
        panel_reviews[0]["review_report"]["decision"] = "do_not_handoff"
    elif mutation == "empty_package_contract":
        package = next(event for event in fixture["events"] if event["type"] == "package")
        package["input_artifact_ids"] = []
        package["input_versions"] = []
        package["allowed_read_paths"] = []
        for output in package["outputs"]:
            output["based_on"] = []
    elif mutation == "reviewer_reused_as_writer":
        event = primary_produces[1]
        reviewer_id = evaluator_reviews[0]["actor_instance_id"]
        event["actor_instance_id"] = reviewer_id
        for output in event["outputs"]:
            output["created_by_instance_id"] = reviewer_id
    elif mutation == "readiness_missing_inputs":
        event = next(event for event in reviews if event["destination_skill"] == "proposal-readiness-triage")
        event["input_artifact_ids"] = []
        event["input_versions"] = []
        event["allowed_read_paths"] = []
        event["review_report"]["input_artifact_ids"] = []
        event["review_report"]["input_versions"] = []
        event["review_report"]["files_read"] = []
    elif mutation == "stale_sap_preflight":
        event = next(event for event in reviews if event["destination_skill"] == "methodology-statistics-preflight")
        index = event["input_artifact_ids"].index("proposal-v2")
        event["input_artifact_ids"][index] = "proposal-v1"
        event["input_versions"][index] = "v001"
        event["allowed_read_paths"].remove("04_drafts/proposal-v002.md")
        event["allowed_read_paths"].append("04_drafts/proposal-v001.md")
        event["review_report"]["input_artifact_ids"][index] = "proposal-v1"
        event["review_report"]["input_versions"][index] = "v001"
        event["review_report"]["files_read"].remove("04_drafts/proposal-v002.md")
        event["review_report"]["files_read"].append("04_drafts/proposal-v001.md")
        event["outputs"][0]["based_on"] = [
            "proposal-context-v1@c001",
            "proposal-evidence-v1@e001",
            "proposal-v1@v001",
        ]
    elif mutation == "remove_revision_plan":
        event = next(event for event in fixture["events"] if event["event_id"] == "proposal-revise-v2")
        index = event["input_artifact_ids"].index("proposal-revision-plan-v2")
        event["input_artifact_ids"].pop(index)
        event["input_versions"].pop(index)
        event["allowed_read_paths"].remove("06_revisions/round-002/revision-plan-r002.md")
    elif mutation == "remove_revision_artifacts":
        event = next(event for event in fixture["events"] if event["event_id"] == "article-revise-v2")
        event["outputs"] = [artifact for artifact in event["outputs"] if artifact["artifact_role"] == "manuscript"]
        event["allowed_write_paths"] = ["06_drafts/manuscript-v002.md"]
    elif mutation == "verifier_reads_forbidden_context":
        event = next(event for event in reviews if event["destination_skill"] == "article-submission-compositor")
        event["input_artifact_ids"].append("article-context-v1")
        event["input_versions"].append("c001")
        event["allowed_read_paths"].append("01_context/article-context-v001.md")
        event["review_report"]["input_artifact_ids"].append("article-context-v1")
        event["review_report"]["input_versions"].append("c001")
        event["review_report"]["files_read"].append("01_context/article-context-v001.md")
    elif mutation == "unsupported_fixture_entry_mode":
        fixture["entry_mode"] = "unsupported_mode"
    elif mutation == "package_output_drops_input":
        package = next(event for event in fixture["events"] if event["type"] == "package")
        package["outputs"][0]["based_on"].pop()
    elif mutation == "panel_reads_forbidden_context":
        event = panel_reviews[0]
        event["input_artifact_ids"].append("proposal-context-v1")
        event["input_versions"].append("c001")
        event["allowed_read_paths"].append("01_context/proposal-context-v001.md")
        event["review_report"]["input_artifact_ids"].append("proposal-context-v1")
        event["review_report"]["input_versions"].append("c001")
        event["review_report"]["files_read"].append("01_context/proposal-context-v001.md")
        event["outputs"][0]["based_on"].append("proposal-context-v1@c001")
    elif mutation == "invalid_verifier_output_role":
        final = next(event for event in reversed(fixture["events"]) if event["type"] == "review")
        next(output for output in final["outputs"] if output["artifact_role"] == "final_handoff_package")["artifact_role"] = "text_identical_final_handoff_package"
    elif mutation == "substantive_panel_requires_fresh_panel":
        event = next(event for event in panel_reviews if event["event_id"] == "perspective-panel-narrative")
        event["review_report"]["decision"] = "support_after_major_revision"
        gate = next(event for event in fixture["events"] if event["event_id"] == "perspective-panel-gate")
        gate["decision"] = "support_after_major_revision"
    elif mutation == "panel_reviews_stale_primary":
        event = panel_reviews[0]
        index = event["input_artifact_ids"].index("ideas-v2")
        event["input_artifact_ids"][index] = "ideas-v1"
        event["input_versions"][index] = "v001"
        event["allowed_read_paths"][index] = "03_ideas/nodes/idea-001/dossiers/idea-dossier-v001.md"
        event["review_report"]["input_artifact_ids"][index] = "ideas-v1"
        event["review_report"]["input_versions"][index] = "v001"
        event["review_report"]["files_read"][index] = "03_ideas/nodes/idea-001/dossiers/idea-dossier-v001.md"
        event["outputs"][0]["based_on"] = ["ideas-v1@v001"]
    elif mutation == "sap_evaluator_unbound":
        event = next(event for event in reviews if event["destination_skill"] == "sap-evaluator")
        index = event["input_artifact_ids"].index("sap-v1")
        event["input_artifact_ids"][index] = "proposal-evidence-v1"
        event["input_versions"][index] = "e001"
        event["allowed_read_paths"].remove("07_sap/sap-v001.md")
        event["allowed_read_paths"].append("02_evidence/proposal-evidence-v001.md")
        event["review_report"]["input_artifact_ids"][index] = "proposal-evidence-v1"
        event["review_report"]["input_versions"][index] = "e001"
        event["review_report"]["files_read"].remove("07_sap/sap-v001.md")
        event["review_report"]["files_read"].append("02_evidence/proposal-evidence-v001.md")
        event["outputs"][0]["based_on"] = [
            parent for parent in event["outputs"][0]["based_on"] if not parent.startswith("sap-v1@")
        ] + ["proposal-evidence-v1@e001"]
    elif mutation == "revision_plan_wrong_trigger_review":
        event = next(event for event in fixture["events"] if event["event_id"] == "perspective-panel-plan-v3")
        index = event["input_artifact_ids"].index("perspective-panel-narrative-report")
        event["input_artifact_ids"][index] = "perspective-eval-v2"
        event["input_versions"][index] = "r002"
        event["allowed_read_paths"][index] = "05_evaluations/evaluation-report-v002.md"
        event["outputs"][0]["based_on"] = ["perspective-v2@v002", "perspective-eval-v2@r002"]
    elif mutation == "verifier_identity_false":
        final = next(event for event in reversed(fixture["events"]) if event["type"] == "review")
        final["review_report"]["workflow_state"] = "blocked"
        final["review_report"]["source_version"] = "v999"
        final["review_report"]["evaluated_version"] = "v000"
        final["review_report"]["text_identity_verified"] = False
    elif mutation == "controller_plan_missing_review":
        event = next(event for event in fixture["events"] if event["event_id"] == "proposal-plan-v2")
        index = event["input_artifact_ids"].index("proposal-eval-v1")
        event["input_artifact_ids"].pop(index)
        event["input_versions"].pop(index)
        event["allowed_read_paths"].remove("05_evaluations/proposal-v001-evaluation.md")
        event["outputs"][0]["based_on"] = ["proposal-v1@v001"]
    elif mutation == "revision_plan_drops_one_trigger":
        event = next(event for event in panel_reviews if event["event_id"] == "perspective-panel-evidence")
        event["review_report"]["decision"] = "support_with_minor_revision"
    elif mutation == "polisher_remove_matrix_cell":
        event = next(event for event in fixture["events"] if event["event_id"] == "polisher-assemble-v1")
        event["outputs"][0]["options"].pop()
    elif mutation == "polisher_duplicate_strategy_instance":
        first = next(event for event in reviews if event["event_id"] == "polisher-strategy-scientific-v1")
        second = next(event for event in reviews if event["event_id"] == "polisher-strategy-practical-v1")
        second["actor_instance_id"] = first["actor_instance_id"]
        second["review_report"]["reviewer_instance_id"] = first["actor_instance_id"]
        for output in second["outputs"]:
            output["created_by_instance_id"] = first["actor_instance_id"]
    elif mutation == "polisher_peer_output_visible":
        event = next(event for event in reviews if event["event_id"] == "polisher-strategy-scientific-v1")
        event["review_report"]["peer_outputs_visible"] = True
    elif mutation == "polisher_reposition_adds_analysis":
        event = next(event for event in reviews if event["event_id"] == "polisher-strategy-scientific-v1")
        option = event["review_report"]["strategy_options"][0]
        option["plan"]["added_work_items"] = ["new subgroup analysis"]
        option["introduces_new_analysis"] = True
    elif mutation == "polisher_small_low_feasibility":
        event = next(event for event in reviews if event["event_id"] == "polisher-strategy-practical-v1")
        event["review_report"]["strategy_options"][1]["feasibility"] = "unknown"
    elif mutation == "polisher_small_changes_core_design":
        event = next(event for event in reviews if event["event_id"] == "polisher-strategy-practical-v1")
        event["review_report"]["strategy_options"][1]["changes_core_design"] = True
    elif mutation == "polisher_moderate_new_study":
        event = next(event for event in reviews if event["event_id"] == "polisher-strategy-dissemination-v1")
        event["review_report"]["strategy_options"][2]["independent_new_study"] = True
    elif mutation == "polisher_assembler_scores":
        event = next(event for event in fixture["events"] if event["event_id"] == "polisher-assemble-v1")
        event["outputs"][0]["assembler_contract"]["scoring_performed"] = True
    elif mutation == "polisher_assembler_invents_option":
        event = next(event for event in fixture["events"] if event["event_id"] == "polisher-assemble-v1")
        event["outputs"][0]["assembler_contract"]["invented_option_ids"] = ["invented-hybrid-001"]
    elif mutation == "polisher_assembler_drops_dissent":
        event = next(event for event in fixture["events"] if event["event_id"] == "polisher-assemble-v1")
        event["outputs"][0]["preserved_dissent_ids"] = []
    elif mutation == "polisher_evaluator_reads_strategy_report":
        event = next(event for event in evaluator_reviews if event["event_id"] == "polisher-evaluate-v1")
        event["input_artifact_ids"].append("polisher-strategy-scientific-report-v1")
        event["input_versions"].append("sr001")
        event["allowed_read_paths"].append("03_strategy/research_polisher_strategy_report-scientific_significance-v001.yaml")
        event["review_report"]["input_artifact_ids"].append("polisher-strategy-scientific-report-v1")
        event["review_report"]["input_versions"].append("sr001")
        event["review_report"]["files_read"].append("03_strategy/research_polisher_strategy_report-scientific_significance-v001.yaml")
    elif mutation == "polisher_evaluator_reuses_strategy_instance":
        strategy = next(event for event in reviews if event["event_id"] == "polisher-strategy-scientific-v1")
        event = next(event for event in evaluator_reviews if event["event_id"] == "polisher-evaluate-v1")
        event["actor_instance_id"] = strategy["actor_instance_id"]
        event["review_report"]["reviewer_instance_id"] = strategy["actor_instance_id"]
        for output in event["outputs"]:
            output["created_by_instance_id"] = strategy["actor_instance_id"]
    elif mutation == "polisher_target_fit_unverified":
        event = next(event for event in fixture["events"] if event["event_id"] == "polisher-assemble-v1")
        event["outputs"][0]["target_specific_fit_claimed"] = True
    elif mutation == "polisher_fatal_then_selection":
        event = next(event for event in evaluator_reviews if event["event_id"] == "polisher-evaluate-v2")
        review_id = event["review_report"]["review_id"]
        event["review_report"]["findings"].append(
            {
                "finding_id": "polisher-fatal-mutated",
                "source_review_id": review_id,
                "severity": "fatal",
                "blocking": True,
                "fixability": "unfixable",
                "status": "unresolved",
                "owner": "human_expert",
                "route": "blocked",
            }
        )
        event["expected_state_after"] = "blocked"
    elif mutation == "polisher_portfolio_identity_leak":
        event = next(event for event in fixture["events"] if event["event_id"] == "polisher-assemble-v1")
        event["outputs"][0]["options"][0]["reviewer_role"] = "scientific_significance"
    elif mutation == "polisher_portfolio_lineage_leak":
        event = next(event for event in fixture["events"] if event["event_id"] == "polisher-assemble-v1")
        event["outputs"][0]["based_on"].append(
            "polisher-strategy-scientific-report-v1@sr001"
        )
    elif mutation == "polisher_dossier_missing_method":
        dossier = next(
            artifact
            for artifact in fixture["initial_artifacts"]
            if artifact["artifact_role"] == "research_polisher_dossier"
        )
        dossier["dossier_contract"].pop("methods")
    elif mutation == "polisher_option_missing_evidence_dependency":
        event = next(
            event
            for event in reviews
            if event["event_id"] == "polisher-strategy-scientific-v1"
        )
        event["review_report"]["strategy_options"][0]["plan"].pop(
            "evidence_dependencies"
        )
    elif mutation == "polisher_evaluation_missing_decision":
        event = next(
            event
            for event in evaluator_reviews
            if event["event_id"] == "polisher-evaluate-v2"
        )
        event["review_report"]["option_decisions"].pop()
    elif mutation == "polisher_evaluation_pareto_incomplete":
        event = next(
            event
            for event in evaluator_reviews
            if event["event_id"] == "polisher-evaluate-v2"
        )
        event["review_report"]["pareto_axis_values"].pop()
    elif mutation == "polisher_selection_missing_nondominated":
        event = next(
            event for event in fixture["events"] if event["event_id"] == "polisher-package"
        )
        event["outputs"][0]["selection_dossier_contract"][
            "non_dominated_option_ids"
        ] = []
    elif mutation == "polisher_revision_brief_identity_leak":
        event = next(
            event for event in fixture["events"] if event["event_id"] == "polisher-plan-v2"
        )
        event["outputs"][0]["revision_brief_contract"][
            "source_reviewer_identities_included"
        ] = True
    elif mutation == "polisher_reevaluator_reads_prior_evaluation":
        event = next(
            event
            for event in evaluator_reviews
            if event["event_id"] == "polisher-evaluate-v2"
        )
        event["input_artifact_ids"].append("polisher-evaluation-v1")
        event["input_versions"].append("er001")
        event["allowed_read_paths"].append(
            "05_evaluations/research_polisher_evaluation_report-v001.yaml"
        )
        event["review_report"]["input_artifact_ids"].append("polisher-evaluation-v1")
        event["review_report"]["input_versions"].append("er001")
        event["review_report"]["files_read"].append(
            "05_evaluations/research_polisher_evaluation_report-v001.yaml"
        )
    elif mutation == "polisher_final_reviewer_edits_source":
        event = next(
            event
            for event in evaluator_reviews
            if event["event_id"] == "polisher-evaluate-v2"
        )
        event["review_report"]["source_edits_performed"] = True
    else:
        raise ValueError(f"Unknown mutation: {mutation}")


def validate_retrieval_receipts() -> dict[str, Any]:
    receipts = load_yaml(FIXTURE_ROOT / "retrieval-receipts.yaml")
    targeted = receipts["targeted_search"]
    require(
        targeted["status"] == "self_attested_search_snapshot_validated",
        "search_receipt",
        "targeted status",
    )
    require(targeted["capability"] == "chatgpt_codex_builtin_search", "search_receipt", "wrong capability")
    require(len(targeted["opened_sources"]) >= 2, "search_receipt", "too few opened sources")
    require(all(item["identity_verified"] and item["adopted"] for item in targeted["opened_sources"]), "search_receipt", "unverified source adopted")
    require(targeted["local_script_invocations"] == [], "search_receipt", "local script used")
    deep = receipts["deep_research_inactive"]
    require(deep["status"] == "deep_research_handoff_required", "deep_research_receipt", "wrong status")
    require(deep["capability_active"] is False and deep["workflow_paused"] is True, "deep_research_receipt", "inactive route did not pause")
    require(deep["downstream_evidence_map_created"] is False, "deep_research_receipt", "fabricated downstream artifact")
    require((REPO / deep["continuation_artifact"]).is_file(), "deep_research_receipt", "continuation artifact missing")
    return {"targeted_search": targeted["status"], "deep_research": deep["status"]}


def validate_finding_route_cases() -> list[dict[str, Any]]:
    data = load_yaml(FIXTURE_ROOT / "finding-route-cases.yaml")
    require(data.get("schema_version") == 1, "finding_route_cases", "schema_version")
    results: list[dict[str, Any]] = []
    for case in data.get("cases", []):
        actual = ScenarioEngine.finding_route(case["findings"])
        require(actual == case.get("expected_route"), "finding_route_cases", case["case_id"])
        results.append({"case_id": case["case_id"], "route": actual})
    require(len(results) >= 5, "finding_route_cases", "insufficient route coverage")
    return results


def validate_polisher_decision_route_cases() -> list[dict[str, str]]:
    cases = (
        ("research-polisher-strategy-reviewer", "matrix_complete", "continue"),
        (
            "research-polisher-strategy-reviewer",
            "matrix_complete_with_no_defensible_option",
            "continue",
        ),
        (
            "research-polisher-strategy-reviewer",
            "clarification_required",
            "clarification_stop",
        ),
        (
            "research-polisher-strategy-reviewer",
            "independent_review_pending",
            "independent_review_pending",
        ),
        (
            "research-polisher-methodology-publishability-reviewer",
            "specialist_review_required",
            "specialist_review_pending",
        ),
        (
            "research-polisher-methodology-publishability-reviewer",
            "no_defensible_option",
            "no_defensible_option",
        ),
        (
            "research-polisher-methodology-publishability-reviewer",
            "not_assessable",
            "clarification_stop",
        ),
        (
            "research-polisher-methodology-publishability-reviewer",
            "independent_review_pending",
            "independent_review_pending",
        ),
    )
    results = []
    for skill, decision, expected in cases:
        actual = ScenarioEngine.polisher_decision_state(skill, decision)
        require(actual == expected, "polisher_decision_route", f"{decision}: {actual}")
        results.append(
            {
                "skill": skill,
                "decision": decision,
                "state": actual,
                "status": "verified",
            }
        )
    return results


def normalized_skills_tree_digest(root: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return len(files), digest.hexdigest()


def sha256_hex(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def current_live_runtime_identity(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    file_count, skills_digest = normalized_skills_tree_digest(PLUGIN / "skills")
    return {
        "manifest": {
            "applicable": True,
            "capture_status": "captured",
            "path": "research-skills-openai/.codex-plugin/plugin.json",
            "algorithm": DIGEST_ALGORITHM,
            "sha256": sha256_hex(PLUGIN / ".codex-plugin" / "plugin.json"),
        },
        "workflow_registry": {
            "applicable": True,
            "capture_status": "captured",
            "path": "research-skills-openai/workflow-registry.yaml",
            "algorithm": DIGEST_ALGORITHM,
            "sha256": sha256_hex(PLUGIN / "workflow-registry.yaml"),
        },
        "registry_schema_version": {
            "applicable": True,
            "capture_status": "captured",
            "value": registry["schema_version"],
        },
        "receipt_schema": {
            "applicable": False,
            "capture_status": "captured",
            "path": None,
            "algorithm": None,
            "sha256": None,
            "reason": "no_separate_live_receipt_schema_file",
        },
        "skills_tree": {
            "applicable": True,
            "capture_status": "captured",
            "algorithm": SKILLS_TREE_DIGEST_ALGORITHM,
            "file_count": file_count,
            "sha256": skills_digest,
        },
    }


def validate_captured_runtime_identity(identity: dict[str, Any]) -> None:
    require(
        set(identity) == set(LIVE_IDENTITY_COMPONENTS),
        "live_receipt_identity",
        f"identity components: {sorted(identity)}",
    )
    for name in LIVE_IDENTITY_COMPONENTS:
        record = identity[name]
        require(isinstance(record, dict), "live_receipt_identity", f"{name}: record")
        require(
            record.get("capture_status") in {"captured", "not_captured"},
            "live_receipt_identity",
            f"{name}: capture status",
        )
        applicable = record.get("applicable")
        require(
            isinstance(applicable, bool) or applicable == "unknown",
            "live_receipt_identity",
            f"{name}: applicability",
        )
        if record["capture_status"] == "not_captured":
            value_key = "value" if name == "registry_schema_version" else "sha256"
            require(record.get(value_key) is None, "live_receipt_identity", f"{name}: uncaptured value")
            continue
        require(isinstance(applicable, bool), "live_receipt_identity", f"{name}: captured applicability")
        if not applicable:
            require(bool(record.get("reason")), "live_receipt_identity", f"{name}: not-applicable reason")
            continue
        if name == "registry_schema_version":
            require(record.get("value") is not None, "live_receipt_identity", f"{name}: value")
            continue
        require(
            re.fullmatch(r"[0-9a-f]{64}", str(record.get("sha256", ""))) is not None,
            "live_receipt_identity",
            f"{name}: digest",
        )
        expected_algorithm = SKILLS_TREE_DIGEST_ALGORITHM if name == "skills_tree" else DIGEST_ALGORITHM
        require(record.get("algorithm") == expected_algorithm, "live_receipt_identity", f"{name}: algorithm")
        if name == "skills_tree":
            require(
                isinstance(record.get("file_count"), int) and record["file_count"] > 0,
                "live_receipt_identity",
                f"{name}: file count",
            )


def compare_live_runtime_identity(
    captured: dict[str, Any], current: dict[str, Any]
) -> dict[str, Any]:
    validate_captured_runtime_identity(captured)
    validate_captured_runtime_identity(current)
    incomplete: list[str] = []
    mismatches: list[str] = []
    for name in LIVE_IDENTITY_COMPONENTS:
        captured_record = captured[name]
        current_record = current[name]
        if captured_record["capture_status"] != "captured" or captured_record["applicable"] == "unknown":
            incomplete.append(name)
            continue
        if captured_record["applicable"] != current_record["applicable"]:
            mismatches.append(name)
            continue
        if captured_record["applicable"] is False:
            continue
        if name == "registry_schema_version":
            if captured_record["value"] != current_record["value"]:
                mismatches.append(name)
            continue
        comparable_fields = ["algorithm", "sha256"]
        if name == "skills_tree":
            comparable_fields.append("file_count")
        if any(captured_record.get(field) != current_record.get(field) for field in comparable_fields):
            mismatches.append(name)
    if incomplete:
        applicability = "historical_only_incomplete_identity"
    elif mismatches:
        applicability = "historical_only_identity_mismatch"
    else:
        applicability = "current_identity_compatible"
    return {
        "applicability": applicability,
        "identity_complete": not incomplete,
        "missing_identity_components": incomplete,
        "mismatched_identity_components": mismatches,
    }


def validate_live_identity_negative_guards(current: dict[str, Any]) -> list[dict[str, str]]:
    compatible = compare_live_runtime_identity(copy.deepcopy(current), current)
    require(
        compatible["applicability"] == "current_identity_compatible",
        "live_identity_self_test",
        "complete identical identity was not accepted",
    )

    cases: list[tuple[str, dict[str, Any], str]] = []
    skills_only = copy.deepcopy(current)
    for name in ("manifest", "workflow_registry", "registry_schema_version", "receipt_schema"):
        skills_only[name]["capture_status"] = "not_captured"
        skills_only[name]["applicable"] = "unknown" if name == "receipt_schema" else True
        if name == "registry_schema_version":
            skills_only[name]["value"] = None
        else:
            skills_only[name]["sha256"] = None
    cases.append(("skills-tree-only-is-incomplete", skills_only, "historical_only_incomplete_identity"))

    for name in LIVE_IDENTITY_COMPONENTS:
        mutated = copy.deepcopy(current)
        mutated[name]["capture_status"] = "not_captured"
        if name == "receipt_schema":
            mutated[name]["applicable"] = "unknown"
        if name == "registry_schema_version":
            mutated[name]["value"] = None
        else:
            mutated[name]["sha256"] = None
        cases.append((f"missing-{name}-is-incomplete", mutated, "historical_only_incomplete_identity"))

    for name in ("manifest", "workflow_registry", "skills_tree"):
        mutated = copy.deepcopy(current)
        mutated[name]["sha256"] = "0" * 64 if mutated[name]["sha256"] != "0" * 64 else "1" * 64
        cases.append((f"{name}-digest-mismatch", mutated, "historical_only_identity_mismatch"))

    file_count_mismatch = copy.deepcopy(current)
    file_count_mismatch["skills_tree"]["file_count"] += 1
    cases.append(("skills-tree-file-count-mismatch", file_count_mismatch, "historical_only_identity_mismatch"))

    schema_mismatch = copy.deepcopy(current)
    schema_mismatch["registry_schema_version"]["value"] = f"{current['registry_schema_version']['value']}-tampered"
    cases.append(("registry-schema-version-mismatch", schema_mismatch, "historical_only_identity_mismatch"))

    receipt_schema_current = copy.deepcopy(current)
    receipt_schema_current["receipt_schema"] = {
        "applicable": True,
        "capture_status": "captured",
        "path": "tests/openai_phase4/live-forward-test-receipts.schema.yaml",
        "algorithm": DIGEST_ALGORITHM,
        "sha256": "a" * 64,
    }
    receipt_schema_mismatch = copy.deepcopy(receipt_schema_current)
    receipt_schema_mismatch["receipt_schema"]["sha256"] = "b" * 64
    result = compare_live_runtime_identity(receipt_schema_mismatch, receipt_schema_current)
    require(
        result["applicability"] == "historical_only_identity_mismatch",
        "live_identity_negative_guard",
        "receipt-schema-digest-mismatch",
    )
    results = [
        {
            "case_id": "receipt-schema-digest-mismatch",
            "status": "rejected_as_expected",
            "applicability": result["applicability"],
        }
    ]
    for case_id, captured, expected in cases:
        result = compare_live_runtime_identity(captured, current)
        require(result["applicability"] == expected, "live_identity_negative_guard", case_id)
        results.append(
            {
                "case_id": case_id,
                "status": "rejected_as_expected",
                "applicability": result["applicability"],
            }
        )
    return sorted(results, key=lambda item: item["case_id"])


def extract_raw_execution_receipt(raw_text: str, workflow_id: str) -> dict[str, Any]:
    for language, body in re.findall(r"```(yaml|json)\s*\n(.*?)```", raw_text, re.S):
        try:
            parsed = yaml.safe_load(body) if language == "yaml" else json.loads(body)
        except (yaml.YAMLError, json.JSONDecodeError):
            continue
        if not isinstance(parsed, dict):
            continue
        candidate = parsed.get("receipt", parsed)
        if isinstance(candidate, dict) and candidate.get("workflow_id") == workflow_id:
            return candidate
    raise ScenarioViolation("live_raw_receipt_content", workflow_id)


def raw_receipt_state(raw: dict[str, Any]) -> str:
    for key in ("registry_state", "status", "final_status", "final_state"):
        if raw.get(key):
            return str(raw[key])
    raise ScenarioViolation("live_raw_receipt_content", "missing raw state")


def raw_receipt_version(workflow: str, raw: dict[str, Any]) -> str:
    if workflow == "idea":
        return str(raw["current_candidate"]).rsplit("@", 1)[-1]
    if workflow == "proposal":
        return str(raw["final_artifacts"]["proposal"]["version"])
    if workflow == "article":
        return str(raw["artifacts"]["manuscripts"][-1]).rsplit("@", 1)[-1]
    drafts = raw["artifacts"]["drafts"]
    return str(drafts[-1]["version"])


def validate_live_forward_test_receipts(registry: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    data = load_yaml(LIVE_RECEIPT_PATH)
    require(data.get("schema_version") == 4, "live_receipt_schema", "schema_version")
    require(data.get("capture_method") == "codex_fresh_delegated_instances", "live_receipt_schema", "capture method")
    require(data.get("evidence_class") == "self_attested_live_output_snapshot", "live_receipt_schema", "evidence class")
    require(
        data.get("applicability_policy") == "complete_captured_runtime_identity_exact_match",
        "live_receipt_schema",
        "applicability policy",
    )
    captured_plugin = data.get("captured_plugin", {})
    captured_version = str(captured_plugin.get("version", ""))
    require(bool(captured_version), "live_receipt_version", "captured version missing")
    captured_identity = captured_plugin.get("runtime_identity", {})
    current_identity = current_live_runtime_identity(registry)
    identity_comparison = compare_live_runtime_identity(captured_identity, current_identity)
    applicability = identity_comparison["applicability"]
    captured_digest = str(captured_identity["skills_tree"]["sha256"])
    current_digest = str(current_identity["skills_tree"]["sha256"])
    receipts = data.get("workflows", [])
    by_workflow = {item.get("workflow"): item for item in receipts}
    require(
        set(by_workflow) == set(LIVE_RECEIPT_WORKFLOWS),
        "live_receipt_workflows",
        str(sorted(by_workflow)),
    )

    audited = 0
    completed = 0
    stopped = 0
    blocked = 0
    pending = 0
    corrected_claims = 0
    orchestrators: list[str] = []
    summaries: list[dict[str, Any]] = []
    for workflow in LIVE_RECEIPT_WORKFLOWS:
        receipt = by_workflow[workflow]
        orchestrator = str(receipt.get("orchestrator_instance", ""))
        require(orchestrator.startswith("codex-cli:"), "live_orchestrator_instance", workflow)
        orchestrators.append(orchestrator)
        require(f"/{captured_version}/skills/" in str(receipt.get("installed_skill_path", "")).replace("\\", "/"), "live_skill_path", workflow)

        raw_path = REPO / safe_relative(receipt["raw_receipt"])
        require(raw_path.is_file(), "live_raw_receipt", workflow)
        require(sha256_file(raw_path) == "sha256:" + receipt["raw_sha256"], "live_raw_receipt_hash", workflow)
        raw_text = raw_path.read_text(encoding="utf-8-sig")
        raw = extract_raw_execution_receipt(raw_text, receipt["workflow_id"])
        raw_state = raw_receipt_state(raw)
        require(receipt.get("raw_claimed_state") == raw_state, "live_raw_state", workflow)
        require(receipt.get("current_artifact_version") == raw_receipt_version(workflow, raw), "live_raw_version", workflow)
        require(receipt.get("event_order") == raw.get("event_order"), "live_raw_event_order", workflow)
        if raw_state != receipt.get("final_state"):
            corrected_claims += 1

        writers = list(receipt.get("writer_instances", []))
        evaluators = list(receipt.get("evaluator_instances", []))
        additional = list(receipt.get("additional_reviewer_instances", []))
        panels = dict(receipt.get("panel_instances", {}))
        panel_ids = list(panels.values())
        require(len(writers) == len(set(writers)), "live_writer_instances", workflow)
        require(len(evaluators) >= 2 and len(evaluators) == len(set(evaluators)), "live_evaluator_instances", workflow)
        all_reviewers = evaluators + additional + panel_ids
        require(len(all_reviewers) == len(set(all_reviewers)), "live_reviewer_instances", workflow)
        require(set(writers).isdisjoint(all_reviewers), "live_writer_reviewer_overlap", workflow)
        require(receipt.get("actor_manifest_scope") == "qualifying_subset", "live_actor_scope", workflow)
        for instance_id in writers + all_reviewers:
            require(instance_id in raw_text, "live_raw_instance", f"{workflow}: {instance_id}")

        events = list(receipt.get("event_order", []))
        normalized_events = [str(event).lower() for event in events]
        evaluate_positions = [index for index, event in enumerate(normalized_events) if "evaluat" in event]
        revise_positions = [
            index
            for index, event in enumerate(normalized_events)
            if "revis" in event or "v002_created" in event or "v003_created" in event
        ]
        require(
            any(first < revision < second for first in evaluate_positions for revision in revise_positions for second in evaluate_positions),
            "live_revision_loop",
            workflow,
        )
        panel_contract = registry["scenario_eval_contract"]["panel_contracts"][workflow]
        if panels:
            selected_tier = receipt.get("panel_tier")
            require(selected_tier in panel_contract["tiers"], "live_panel_tier", workflow)
            required_roles = set(panel_contract["tiers"][selected_tier])
            require(required_roles == set(panels), "live_panel_roles", workflow)
            if workflow == "proposal" and selected_tier == "lightweight_panel":
                require(
                    receipt.get("panel_selection_basis") == "not_preserved_in_raw_receipt"
                    and "selection_basis" not in raw.get("panel", {}),
                    "live_panel_evidence",
                    workflow,
                )
        raw_files_written = raw.get("files_written")
        if workflow == "perspective":
            raw_files_written = raw.get("filesystem", {}).get("repository_files_written")
        require(raw_files_written == receipt.get("repository_files_written") == [], "live_repository_write", workflow)
        external_values = [
            raw.get("submitted_externally"),
            raw.get("external_submission_authorized"),
            raw.get("external_submission_performed"),
            raw.get("external_submission"),
        ]
        require(False in external_values and True not in external_values, "live_external_submission", workflow)
        require(receipt.get("automatic_external_submission") is False, "live_external_submission", workflow)

        outcome = receipt.get("outcome")
        if outcome == "reached_human_signoff_gate":
            require(receipt.get("final_state") == "human_signoff_required", "live_final_state", workflow)
            require(receipt.get("promotion_or_handoff_performed") is True, "live_promotion_state", workflow)
            require(bool(panels), "live_panel_roles", workflow)
            completed += 1
        elif outcome in {"stopped_at_valid_gate", "blocked_at_valid_gate"}:
            require(receipt.get("final_state") in {"stopped", "blocked"}, "live_final_state", workflow)
            require(receipt.get("promotion_or_handoff_performed") is False, "live_promotion_state", workflow)
            gate = receipt.get("valid_gate", {})
            require(all(gate.get(key) for key in ("gate", "finding", "route")), "live_valid_gate", workflow)
            if outcome == "blocked_at_valid_gate":
                blocked += 1
            else:
                stopped += 1
        elif outcome == "independent_review_pending":
            require(receipt.get("final_state") == "independent_review_pending", "live_final_state", workflow)
            require(receipt.get("promotion_or_handoff_performed") is False, "live_promotion_state", workflow)
            require(receipt.get("missing_required_roles") == ["broad-field", "skeptical"], "live_panel_evidence", workflow)
            gate = receipt.get("valid_gate", {})
            require(all(gate.get(key) for key in ("gate", "finding", "route")), "live_valid_gate", workflow)
            pending += 1
        else:
            raise ScenarioViolation("live_outcome", f"{workflow}: {outcome}")
        if workflow == "perspective":
            require(raw.get("readiness") == receipt.get("raw_readiness") == "outlet-targeting-only", "live_raw_state", workflow)
            require(receipt.get("contract_assessment") == "generic_outlet_caps_below_human_signoff", "live_contract_assessment", workflow)
        elif workflow == "proposal":
            require(receipt.get("contract_assessment") == "incomplete_panel_qualification", "live_contract_assessment", workflow)
        else:
            require(receipt.get("contract_assessment") == "outcome_consistent_valid_gate_stop", "live_contract_assessment", workflow)
        audited += 1
        summaries.append(
            {
                "workflow": workflow,
                "workflow_id": receipt["workflow_id"],
                "outcome": outcome,
                "final_state": receipt["final_state"],
                "raw_claimed_state": raw_state,
                "contract_assessment": receipt["contract_assessment"],
                "evidence_class": data["evidence_class"],
                "applicability": applicability,
                "identity_complete": identity_comparison["identity_complete"],
                "missing_identity_components": identity_comparison["missing_identity_components"],
                "mismatched_identity_components": identity_comparison["mismatched_identity_components"],
                "captured_plugin_version": captured_version,
                "captured_manifest_sha256": captured_identity["manifest"].get("sha256"),
                "captured_workflow_registry_sha256": captured_identity["workflow_registry"].get("sha256"),
                "captured_registry_schema_version": captured_identity["registry_schema_version"].get("value"),
                "captured_receipt_schema_sha256": captured_identity["receipt_schema"].get("sha256"),
                "captured_skills_tree_sha256": captured_digest,
                "current_plugin_version": registry.get("plugin_version"),
                "current_manifest_sha256": current_identity["manifest"]["sha256"],
                "current_workflow_registry_sha256": current_identity["workflow_registry"]["sha256"],
                "current_registry_schema_version": current_identity["registry_schema_version"]["value"],
                "current_receipt_schema_sha256": current_identity["receipt_schema"].get("sha256"),
                "current_skills_tree_sha256": current_digest,
                "orchestrator_instance": orchestrator,
                "evaluator_instances": evaluators,
                "panel_instances": panels,
                "raw_receipt": receipt["raw_receipt"],
                "raw_sha256": receipt["raw_sha256"],
            }
        )
    require(len(orchestrators) == len(set(orchestrators)), "live_orchestrator_reuse", "orchestrator instances")
    counts = {
        "receipts_audited": audited,
        "reached_human_signoff_gate": completed,
        "stopped_at_valid_gate": stopped,
        "blocked_at_valid_gate": blocked,
        "independent_review_pending": pending,
        "raw_state_claims_corrected": corrected_claims,
        "applicability": applicability,
        "identity_complete": identity_comparison["identity_complete"],
        "identity_missing_components": identity_comparison["missing_identity_components"],
        "identity_mismatched_components": identity_comparison["mismatched_identity_components"],
        "current_identity_compatible_receipts": audited if applicability == "current_identity_compatible" else 0,
    }
    return summaries, counts


def render_bounded_idea_dossier(node: dict[str, Any], version: dict[str, Any], plugin_version: str) -> str:
    title = str(node["title"])
    objective = str(node["objective"])
    work_package = str(node["work_package"])
    chain_output = str(node["output"])
    content = {
        IDEA_DOSSIER_SECTIONS[0]: "\n".join((
            f"- **Title:** {title}",
            f"- **One-sentence complete-Idea summary:** This complete Idea will {objective.lower()} and keep {node['qualifier']} visible.",
            "- **Primary audience:** Researchers evaluating reproducible clinical or methodological evidence.",
            f"- **Positioning and contribution frame:** {node['contribution_frame']}.",
        )),
        IDEA_DOSSIER_SECTIONS[1]: "\n".join((
            "- **Background and gap:** Prior work leaves a bounded validation or benchmark gap.",
            f"- **Objective and hypothesis:** {objective}; test rather than assume the prespecified hypothesis.",
            f"- **Approach:** {node['method']}.",
            f"- **Expected result:** {chain_output}.",
            f"- **Contribution and impact:** A reproducible {node['contribution_frame']} package for the stated audience.",
        )),
        IDEA_DOSSIER_SECTIONS[2]: "Prior work motivates the direction but leaves a bounded validation or comparison gap (Smith et al. 2024).",
        IDEA_DOSSIER_SECTIONS[3]: f"### Objective: {objective}\n\n### Core hypothesis: the prespecified workflow yields interpretable estimates\nThe hypothesis is tested rather than assumed.",
        IDEA_DOSSIER_SECTIONS[4]: f"### Work package: {work_package}\nExecute the bounded work package without changing the core question.",
        IDEA_DOSSIER_SECTIONS[5]: str(node["input"]),
        IDEA_DOSSIER_SECTIONS[6]: str(node["method"]),
        IDEA_DOSSIER_SECTIONS[7]: "Versioned preprocessing, prespecified quality control, uncertainty estimation, and reproducible reporting.",
        IDEA_DOSSIER_SECTIONS[8]: "\n".join((
            f"### Evidence chain: {work_package}",
            f"- **Input:** {node['input']}.",
            f"- **Method / analysis / processing:** {node['method']}.",
            f"- **Output:** {chain_output}.",
            f"- **Supports:** Objective: {objective}; Core hypothesis: the prespecified workflow yields interpretable estimates; Work package: {work_package}.",
            "- **Limits and failure conditions:** Stop or qualify the claim if calibration, robustness, identifiability, or transportability fails.",
        )),
        IDEA_DOSSIER_SECTIONS[9]: "Complete the prespecified primary analysis, uncertainty estimates, sensitivity analysis, and evidence-to-claim check.",
        IDEA_DOSSIER_SECTIONS[10]: "Expected outputs are estimates with uncertainty; failure to meet prespecified criteria falsifies the broad positioning claim.",
        IDEA_DOSSIER_SECTIONS[11]: "The contribution is a bounded validation or benchmark with an explicit audience and closest-work comparison, not an unsupported discovery claim.",
        IDEA_DOSSIER_SECTIONS[12]: "\n".join((
            "| Title or positioning claim | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or `none` | Support status | Required qualifier |",
            "|---|---|---|---|---|---|---|---|",
            f"| {title} | {node['contribution_frame']} | Research content and work packages > {work_package} | {chain_output}. | Smith et al. (2024) plus the prespecified work package | {chain_output} | supported | {node['qualifier']} |",
        )),
        IDEA_DOSSIER_SECTIONS[13]: "Use only frozen assets and prespecified analyses; stop if required variables, sample support, or quality controls are unavailable.",
        IDEA_DOSSIER_SECTIONS[14]: "Smith J, Lee K. Reproducible validation and benchmarking. Journal of Methods. 2024;1:1-10. https://doi.org/10.1000/example.",
    }
    lines = [
        "---", "schema_version: research-idea.v3", f"plugin_version: {plugin_version}",
        f"artifact_id: {version['artifact_id']}", f"idea_id: {node['node_id']}",
        f"version_id: {version['version_id']}", f"change_type: {version['stage']}",
        "source_skill: multi-path-idea-generator", "created_round: 1", "frozen: true", "---", "",
        f"# {title}", "",
    ]
    for heading in IDEA_DOSSIER_SECTIONS:
        lines.extend((f"## {heading}", "", content[heading], ""))
    return "\n".join(lines)


def parse_reference_ledger_payload(text: str) -> dict[str, dict[str, str]]:
    rows = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    require(len(rows) >= 3, "bounded_ledger_payload", "reference ledger table missing")
    headers = [cell.strip() for cell in rows[0].strip("|").split("|")]
    expected = ["Internal ID", "Type", "Human-readable label", "Definition artifact", "Original source", "Locator", "Version/status"]
    require(headers == expected, "bounded_ledger_payload", str(headers))
    entries: dict[str, dict[str, str]] = {}
    for row in rows[2:]:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        require(len(cells) == len(expected), "bounded_ledger_payload", row)
        entry = dict(zip(expected, cells))
        internal_id = entry["Internal ID"]
        require(internal_id and internal_id not in entries, "bounded_ledger_payload", internal_id)
        require(all(entry[field] for field in expected[2:]), "bounded_ledger_payload", internal_id)
        entries[internal_id] = entry
    return entries


def validate_bounded_idea_fixture(fixture: dict[str, Any], registry: dict[str, Any], workspace: Path) -> dict[str, Any]:
    profile = fixture.get("direction_profile")
    require(fixture.get("workflow") == "idea" and profile == "bounded_exploration", "bounded_direction_profile", str(profile))
    machine = registry["workflow_state_machines"]["idea"]
    bounds = machine["internal_direction_profiles"][profile]["current_dossier_count"]
    dispatch_contract = machine["evaluation_dispatch_by_direction_profile"][profile]
    require(
        dispatch_contract.get("eligible_artifact") == "terminal_current_idea_dossier_only"
        and dispatch_contract.get("initial_or_pre_remap_dossier_evaluation_forbidden") is True,
        "bounded_evaluator_dispatch_contract",
        str(dispatch_contract),
    )
    nodes = fixture.get("nodes", [])
    require(bounds["minimum"] <= len(nodes) <= bounds["maximum"], "bounded_node_count", str(len(nodes)))
    node_ids = [str(node.get("node_id", "")) for node in nodes]
    direction_ids = [str(node.get("direction_id", "")) for node in nodes]
    require(len(set(node_ids)) == len(nodes) and len(set(direction_ids)) == len(nodes), "bounded_direction_identity", str(node_ids))
    route = fixture.get("routing_decision", {})
    require(route.get("route") == profile and route.get("direction_ids") == node_ids, "bounded_route_payload", str(route))
    require(route.get("evidence_confidence") in {"high", "moderate"}, "bounded_route_payload", "confidence")

    artifacts: dict[str, dict[str, Any]] = {}

    def add(artifact_id: str, version_id: str, role: str, path: str, content: str, based_on: list[str], source_skill: str, node_id: str | None = None) -> dict[str, Any]:
        ref = f"{artifact_id}@{version_id}"
        require(ref not in artifacts, "bounded_artifact_ref", ref)
        require(set(based_on) <= set(artifacts), "bounded_lineage_parent", f"{ref}: {set(based_on) - set(artifacts)}")
        allowed_roles = registry["scenario_eval_contract"]["runtime_artifact_role_contract"]["actor_output_roles_by_skill"].get(source_skill, [])
        require(role in allowed_roles, "bounded_artifact_writer_role", f"{source_skill}: {role}")
        target = workspace / Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        require(not target.exists(), "bounded_artifact_overwrite", path)
        target.write_text(content, encoding="utf-8", newline="\n")
        artifact = {
            "artifact_id": artifact_id, "version_id": version_id, "artifact_role": role,
            "path": Path(path).as_posix(), "sha256": sha256_file(target), "based_on": list(based_on),
            "source_skill": source_skill, "node_id": node_id,
        }
        artifacts[ref] = artifact
        return artifact

    add("idea-context-bounded", "c001", "research_context", "01_context/research-context-v001.md", "Multiple credible directions remain.\n", [], "research-context-builder")
    add("idea-opportunity-seed", "o001", "opportunity_map", "02_evidence/opportunity-seed-v001.yaml", "credible_directions: 2\n", [], "research-opportunity-mapper")
    route_artifact = add(route["artifact_id"], route["version_id"], "idea_routing_decision", route["path"], yaml.safe_dump(route, sort_keys=False, allow_unicode=True), list(route["based_on"]), "research-idea-orchestrator")

    current_dossiers: dict[str, dict[str, Any]] = {}
    evaluations: dict[str, dict[str, Any]] = {}
    ledgers: dict[str, dict[str, Any]] = {}
    navigation_proposals: dict[str, dict[str, Any]] = {}
    revision_plans: dict[str, dict[str, Any]] = {}
    revision_deltas: list[dict[str, Any]] = []
    evaluator_ids: list[str] = []
    remap_refs: set[str] = set()
    for node in nodes:
        node_id = str(node["node_id"])
        versions = node.get("dossier_versions", [])
        require([item.get("stage") for item in versions] == ["create", "revise", "evidence_claim_sync"], "bounded_version_stages", node_id)
        created: list[dict[str, Any]] = []
        v1 = versions[0]
        created.append(add(v1["artifact_id"], v1["version_id"], "idea_dossier", f"03_ideas/nodes/{node_id}/dossiers/idea-dossier-v001.md", render_bounded_idea_dossier(node, v1, registry["plugin_version"]), list(v1["based_on"]), "multi-path-idea-generator", node_id))
        plan = node["revision_plan"]
        revision_plans[node_id] = add(plan["artifact_id"], plan["version_id"], "revision_plan", f"03_ideas/nodes/{node_id}/revisions/round-001/revision-plan.md", f"One bounded optimization for {node_id}.\n", list(plan["based_on"]), "research-idea-orchestrator", node_id)
        v2 = versions[1]
        created.append(add(v2["artifact_id"], v2["version_id"], "idea_dossier", f"03_ideas/nodes/{node_id}/dossiers/idea-dossier-v002.md", render_bounded_idea_dossier(node, v2, registry["plugin_version"]), list(v2["based_on"]), "multi-path-idea-generator", node_id))
        delta = node["revision_delta"]
        revision_deltas.append(add(delta["artifact_id"], delta["version_id"], "revision_delta", f"03_ideas/nodes/{node_id}/revisions/round-001/revision-delta.md", "One bounded optimization; no second optimization.\n", list(delta["based_on"]), "multi-path-idea-generator", node_id))
        remap = node["remap"]
        evidence = add(remap["evidence_artifact_id"], remap["evidence_version_id"], "evidence_map", f"02_evidence/{node_id}-evidence-remap-v001.yaml", f"node_id: {node_id}\nclaims_checked: true\n", list(remap["based_on"]), "research-opportunity-mapper", node_id)
        opportunity = add(remap["opportunity_artifact_id"], remap["opportunity_version_id"], "opportunity_map", f"02_evidence/{node_id}-opportunity-remap-v001.yaml", f"node_id: {node_id}\nclosest_work_checked: true\n", list(remap["based_on"]), "research-opportunity-mapper", node_id)
        remap_refs.update({f"{evidence['artifact_id']}@{evidence['version_id']}", f"{opportunity['artifact_id']}@{opportunity['version_id']}"})
        v3 = versions[2]
        dossier = add(v3["artifact_id"], v3["version_id"], "idea_dossier", f"03_ideas/nodes/{node_id}/dossiers/idea-dossier-v003.md", render_bounded_idea_dossier(node, v3, registry["plugin_version"]), list(v3["based_on"]), "multi-path-idea-generator", node_id)
        required_remaps = {f"{evidence['artifact_id']}@{evidence['version_id']}", f"{opportunity['artifact_id']}@{opportunity['version_id']}"}
        require(required_remaps <= set(dossier["based_on"]), "bounded_sync_lineage", node_id)
        sync_delta = node["sync_delta"]
        expected_sync_delta_lineage = {
            f"{v2['artifact_id']}@{v2['version_id']}",
            f"{evidence['artifact_id']}@{evidence['version_id']}",
            f"{opportunity['artifact_id']}@{opportunity['version_id']}",
            f"{dossier['artifact_id']}@{dossier['version_id']}",
        }
        require(
            expected_sync_delta_lineage <= set(sync_delta.get("based_on", [])),
            "bounded_sync_delta_lineage",
            node_id,
        )
        revision_deltas.append(add(
            sync_delta["artifact_id"], sync_delta["version_id"], "revision_delta",
            f"03_ideas/nodes/{node_id}/revisions/round-002/revision-delta.md",
            "Evidence/opportunity remap synchronized into the terminal dossier.\n",
            list(sync_delta["based_on"]), "multi-path-idea-generator", node_id,
        ))
        dossier_text = (workspace / dossier["path"]).read_text(encoding="utf-8")
        require(all(f"## {heading}" in dossier_text for heading in IDEA_DOSSIER_SECTIONS), "bounded_dossier_payload", node_id)
        require(len(re.findall(r"^# (?!#).+$", dossier_text, re.M)) == 1 and "\nstatus:" not in dossier_text, "bounded_dossier_payload", node_id)
        for field in ("Title", "One-sentence complete-Idea summary", "Primary audience", "Positioning and contribution frame", "Background and gap", "Objective and hypothesis", "Approach", "Expected result", "Contribution and impact"):
            require(f"- **{field}:**" in dossier_text, "bounded_dossier_payload", f"{node_id}: {field}")
        require(
            "| Title or positioning claim | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or `none` | Support status | Required qualifier |"
            in dossier_text,
            "bounded_claim_support_table",
            node_id,
        )
        current_dossiers[node_id] = dossier

        proposal = node["navigation_proposal"]
        navigation_proposals[node_id] = add(
            proposal["artifact_id"], proposal["version_id"], "proposed_navigation_metadata",
            f"05_state/{node_id}-proposed-navigation-metadata-v001.yaml",
            yaml.safe_dump({"node_id": node_id, "current_ref": f"{dossier['artifact_id']}@{dossier['version_id']}", "route_profile": profile}, sort_keys=False),
            list(proposal["based_on"]), "multi-path-idea-generator", node_id,
        )

        review = node["evaluation"]
        current_ref = f"{dossier['artifact_id']}@{dossier['version_id']}"
        require(review.get("input_ref") == current_ref, "bounded_evaluator_input", node_id)
        files_read = review.get("files_read", [dossier["path"]])
        require(files_read == [dossier["path"]], "bounded_evaluator_dossier_only", node_id)
        evaluator_ids.append(str(review["reviewer_instance_id"]))
        before = sha256_file(workspace / dossier["path"])
        report = {
            "reviewer_instance_id": review["reviewer_instance_id"], "isolation_mode": "fresh_subagent",
            "input_artifact_refs": [current_ref], "files_read": files_read,
            "reviewed_dossier_digest": dossier["sha256"], "complete_dossier_confirmed": True,
            "dossier_only_input_confirmed": True, "prior_scores_visible": False, "source_edits_performed": False,
            "decision": review["decision"], "unresolved_issues": [],
            "findings": [{"id": review["finding_id"], "title": review["finding_title"], "dossier_locator": review["dossier_locator"], "severity": "minor", "blocking": False, "resolved": False, "dissent": True}],
        }
        evaluation = add(review["artifact_id"], review["version_id"], "evaluation_report", f"03_ideas/nodes/{node_id}/reviews/evaluation-r001.json", json.dumps(report, indent=2, ensure_ascii=False) + "\n", [current_ref], "idea-evaluator", node_id)
        require(before == sha256_file(workspace / dossier["path"]), "bounded_reviewer_modified_source", node_id)
        evaluations[node_id] = evaluation

        ledger = node["ledger"]
        ledger_text = "\n".join((
            "| Internal ID | Type | Human-readable label | Definition artifact | Original source | Locator | Version/status |",
            "|---|---|---|---|---|---|---|",
            f"| {ledger['internal_id']} | finding | {ledger['label']} | ../reviews/evaluation-r001.json | ../dossiers/idea-dossier-v003.md | {review['dossier_locator']} | current |", "",
        ))
        ledger_artifact = add(ledger["artifact_id"], ledger["version_id"], "reference_ledger", f"03_ideas/nodes/{node_id}/references/reference-ledger.md", ledger_text, [current_ref, f"{evaluation['artifact_id']}@{evaluation['version_id']}"], "research-idea-orchestrator", node_id)
        ledger_entries = parse_reference_ledger_payload(ledger_text)
        require(review["finding_id"] in ledger_entries and ledger_entries[review["finding_id"]]["Human-readable label"] == review["finding_title"], "bounded_ledger_resolution", node_id)
        ledgers[node_id] = ledger_artifact

    require(len(set(evaluator_ids)) == len(nodes), "bounded_evaluator_instance_reuse", str(evaluator_ids))
    require(
        len(revision_deltas) == 2 * len(nodes),
        "bounded_revision_delta_count",
        str(len(revision_deltas)),
    )
    index = fixture["idea_index"]
    require(index.get("overall_remap_status") == "complete", "bounded_index_remap_status", str(index.get("overall_remap_status")))
    index_entries = index.get("current_nodes", [])
    require({entry.get("node_id") for entry in index_entries} == set(node_ids), "bounded_index_nodes", str(index_entries))
    resolved_entries = []
    for entry in index_entries:
        dossier = current_dossiers[str(entry["node_id"])]
        current_ref = f"{dossier['artifact_id']}@{dossier['version_id']}"
        require(
            entry.get("current_ref") == current_ref
            and entry.get("dossier_id") == dossier["artifact_id"]
            and isinstance(entry.get("parent_idea_ids"), list)
            and bool(entry.get("lineage_id"))
            and entry.get("route_profile") == profile,
            "bounded_index_current_ref",
            str(entry),
        )
        require(entry.get("remap_status") == "complete", "bounded_index_remap_status", str(entry))
        require(entry.get("current_digest") == "computed", "bounded_index_digest_marker", str(entry))
        resolved_entries.append({**entry, "current_digest": dossier["sha256"], "current_path": dossier["path"]})
    index_artifact = add(
        index["artifact_id"], index["version_id"], "idea_index", index["path"],
        yaml.safe_dump({"schema_version": 1, "direction_profile": profile, "overall_remap_status": index["overall_remap_status"], "current_nodes": resolved_entries}, sort_keys=False, allow_unicode=True),
        [f"{item['artifact_id']}@{item['version_id']}" for item in current_dossiers.values()]
        + [f"{item['artifact_id']}@{item['version_id']}" for item in navigation_proposals.values()],
        "research-idea-orchestrator",
    )
    parsed_index = load_yaml(workspace / index_artifact["path"])
    require(parsed_index.get("overall_remap_status") == "complete", "bounded_index_remap_status", "aggregate")
    require(all(entry["current_digest"] == current_dossiers[entry["node_id"]]["sha256"] for entry in parsed_index["current_nodes"]), "bounded_index_digest", "digest mismatch")

    package = fixture["package"]
    final_state = registry["scenario_eval_contract"]["workflow_conditional_final_states"]["idea"][profile]
    require(package.get("final_state") == final_state == fixture["expected"]["final_state"], "bounded_conditional_final_state", str(package.get("final_state")))
    require(package.get("panel_artifact_refs") == [], "bounded_panel_forbidden", str(package.get("panel_artifact_refs")))
    required_refs = {
        "idea-context-bounded@c001",
        f"{route_artifact['artifact_id']}@{route_artifact['version_id']}", f"{index_artifact['artifact_id']}@{index_artifact['version_id']}",
        *[f"{item['artifact_id']}@{item['version_id']}" for item in current_dossiers.values()],
        *[f"{item['artifact_id']}@{item['version_id']}" for item in evaluations.values()],
        *[f"{item['artifact_id']}@{item['version_id']}" for item in ledgers.values()],
        *[f"{item['artifact_id']}@{item['version_id']}" for item in revision_plans.values()],
        *[f"{item['artifact_id']}@{item['version_id']}" for item in revision_deltas],
        *remap_refs,
    }
    require(required_refs <= set(package.get("based_on", [])), "bounded_package_lineage", str(required_refs - set(package.get("based_on", []))))
    require({"evidence_and_opportunity_remap_complete", "fresh_evaluation_complete_for_each_current_dossier"} <= set(machine["before_packaging_by_direction_profile"][profile]), "bounded_profile_gates", profile)
    require(any(item.get("from") == "pending_review" and item.get("to") == "packaging_pending" and item.get("trigger") == "bounded_exploration_reviews_complete" for item in registry["workflow_state_policy"]["lifecycle_transitions"]), "bounded_lifecycle_transition", profile)
    add(package["artifact_id"], package["version_id"], "final_handoff_package", package["path"], "# Direction comparison\n\nHuman direction selection is required.\n", list(package["based_on"]), "idea-portfolio-assembler")
    return {"fixture_id": fixture["fixture_id"], "direction_profile": profile, "node_count": len(nodes), "current_dossier_refs": sorted(f"{item['artifact_id']}@{item['version_id']}" for item in current_dossiers.values()), "evaluator_instances": sorted(evaluator_ids), "panel_count": 0, "final_state": final_state, "artifact_count": len(artifacts), "status": "passed"}


def validate_bounded_idea_negative_guards(fixture: dict[str, Any], registry: dict[str, Any]) -> list[dict[str, str]]:
    cases = [
        ("route-profile-mismatch", "bounded_route_payload", lambda value: value["routing_decision"].update(route="focused_optimization")),
        ("legacy-dossier-change-type", "bounded_version_stages", lambda value: value["nodes"][0]["dossier_versions"][0].update(stage="initial")),
        ("duplicate-evaluator-instance", "bounded_evaluator_instance_reuse", lambda value: value["nodes"][1]["evaluation"].update(reviewer_instance_id=value["nodes"][0]["evaluation"]["reviewer_instance_id"])),
        ("stale-index-current-ref", "bounded_index_current_ref", lambda value: value["idea_index"]["current_nodes"][0].update(current_ref="idea-clinical-validation-v2@v002")),
        ("missing-node-remap-status", "bounded_index_remap_status", lambda value: value["idea_index"]["current_nodes"][0].pop("remap_status")),
        ("evaluator-reads-remap", "bounded_evaluator_dossier_only", lambda value: value["nodes"][0]["evaluation"].update(files_read=["03_ideas/nodes/idea-clinical-validation/dossiers/idea-dossier-v003.md", "02_evidence/idea-clinical-validation-evidence-remap-v001.yaml"])),
        ("evaluator-reads-initial-draft", "bounded_evaluator_input", lambda value: value["nodes"][0]["evaluation"].update(input_ref="idea-clinical-validation-v1@v001")),
        ("sync-drops-opportunity-remap", "bounded_sync_lineage", lambda value: value["nodes"][0]["dossier_versions"][2]["based_on"].pop()),
        ("sync-delta-drops-terminal-dossier", "bounded_sync_delta_lineage", lambda value: value["nodes"][0]["sync_delta"]["based_on"].pop()),
        ("bounded-enters-ordinary-signoff", "bounded_conditional_final_state", lambda value: value["package"].update(final_state="human_signoff_required")),
        ("bounded-adds-panel", "bounded_panel_forbidden", lambda value: value["package"]["panel_artifact_refs"].append("panel@p001")),
        ("ledger-label-does-not-resolve", "bounded_ledger_resolution", lambda value: value["nodes"][0]["ledger"].update(label="Wrong human-readable label")),
    ]
    results = []
    for name, expected, mutate in cases:
        candidate = copy.deepcopy(fixture)
        mutate(candidate)
        try:
            with tempfile.TemporaryDirectory(prefix=f"openai-phase4-bounded-negative-{name}-") as temp:
                validate_bounded_idea_fixture(candidate, registry, Path(temp))
        except ScenarioViolation as exc:
            require(exc.code == expected, "bounded_negative_wrong_error", f"{name}: {exc.code}")
            results.append({"case_id": name, "status": "rejected_as_expected", "error_code": exc.code})
        else:
            raise ScenarioViolation("bounded_negative_accepted", name)
    return results


def run_all() -> dict[str, Any]:
    registry = load_yaml(PLUGIN / "workflow-registry.yaml")
    schema = load_yaml(SCHEMA_PATH)
    scenario_results = []
    for name in FIXTURE_NAMES:
        fixture = load_yaml(FIXTURE_ROOT / name)
        with tempfile.TemporaryDirectory(prefix=f"openai-phase4-{fixture['workflow']}-") as temp:
            scenario_results.append(ScenarioEngine(fixture, registry, schema, Path(temp)).run())

    bounded_fixture = load_yaml(FIXTURE_ROOT / BOUNDED_IDEA_FIXTURE)
    with tempfile.TemporaryDirectory(prefix="openai-phase4-idea-bounded-") as temp:
        bounded_idea_result = validate_bounded_idea_fixture(
            bounded_fixture, registry, Path(temp)
        )
    bounded_idea_negative_results = validate_bounded_idea_negative_guards(
        bounded_fixture, registry
    )

    guard_spec = load_yaml(FIXTURE_ROOT / "guard-cases.yaml")
    polisher_guard_case_ids = {
        case["case_id"]
        for case in guard_spec["cases"]
        if case.get("base_fixture") == "research-polisher.yaml"
    }
    require(
        len(polisher_guard_case_ids) >= 12,
        "polisher_component_guard_coverage",
        str(len(polisher_guard_case_ids)),
    )
    guard_results = []
    for case in guard_spec["cases"]:
        fixture = copy.deepcopy(load_yaml(FIXTURE_ROOT / case["base_fixture"]))
        mutate_fixture(fixture, case["mutation"])
        try:
            with tempfile.TemporaryDirectory(prefix=f"openai-phase4-negative-{case['case_id']}-") as temp:
                ScenarioEngine(fixture, registry, schema, Path(temp)).run()
        except ScenarioViolation as exc:
            require(exc.code == case["expected_error"], "negative_case_wrong_error", f"{case['case_id']}: {exc.code}")
            guard_results.append({"case_id": case["case_id"], "status": "rejected_as_expected", "error_code": exc.code})
        else:
            raise ScenarioViolation("negative_case_accepted", case["case_id"])

    live_results, live_counts = validate_live_forward_test_receipts(registry)
    live_identity_guard_results = validate_live_identity_negative_guards(
        current_live_runtime_identity(registry)
    )
    final_states: dict[str, int] = {}
    for result in scenario_results:
        state = result["final_state"]
        final_states[state] = final_states.get(state, 0) + 1
    return {
        "schema_version": 1,
        "plugin_version": registry["plugin_version"],
        "registry_schema_version": registry["schema_version"],
        "execution_scope": "deterministic_replay_plus_separate_live_receipts",
        "scenario_results": scenario_results,
        "bounded_idea_result": bounded_idea_result,
        "bounded_idea_negative_results": bounded_idea_negative_results,
        "negative_guard_results": guard_results,
        "live_identity_negative_guard_results": live_identity_guard_results,
        "finding_route_results": validate_finding_route_cases(),
        "polisher_decision_route_results": validate_polisher_decision_route_cases(),
        "live_forward_test_receipts": live_results,
        "retrieval_receipts": validate_retrieval_receipts(),
        "summary": {
            "workflows_passed": len(scenario_results),
            "bounded_idea_profiles_passed": 1,
            "bounded_idea_negative_guards_rejected": len(
                bounded_idea_negative_results
            ),
            "negative_guards_rejected": len(guard_results),
            "research_polisher_component_guards_rejected": sum(
                item["case_id"] in polisher_guard_case_ids for item in guard_results
            ),
            "finding_routes_verified": 5,
            "polisher_decision_routes_verified": 8,
            "live_workflows_receipts_audited": live_counts["receipts_audited"],
            "live_workflows_reached_human_signoff_gate": live_counts["reached_human_signoff_gate"],
            "live_workflows_stopped_at_valid_gate": live_counts["stopped_at_valid_gate"],
            "live_workflows_blocked_at_valid_gate": live_counts["blocked_at_valid_gate"],
            "live_workflows_independent_review_pending": live_counts["independent_review_pending"],
            "live_raw_state_claims_corrected": live_counts["raw_state_claims_corrected"],
            "live_receipt_applicability": live_counts["applicability"],
            "live_receipt_identity_complete": live_counts["identity_complete"],
            "live_receipt_identity_missing_components": live_counts["identity_missing_components"],
            "live_receipt_identity_mismatched_components": live_counts["identity_mismatched_components"],
            "live_current_identity_compatible_receipts": live_counts["current_identity_compatible_receipts"],
            "live_identity_negative_guards_rejected": len(live_identity_guard_results),
            "final_states": final_states,
            "automatic_external_submission": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write-report", action="store_true")
    group.add_argument("--check-report", action="store_true")
    args = parser.parse_args()

    result = run_all()
    rendered = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    if args.check_report:
        require(REPORT_PATH.is_file(), "report_missing", str(REPORT_PATH))
        require(REPORT_PATH.read_text(encoding="utf-8") == rendered, "report_drift", str(REPORT_PATH))
    print("Phase 4 scenario evaluations passed")
    print(
        f"workflows: {result['summary']['workflows_passed']}/{len(FIXTURE_NAMES)}"
    )
    print(
        "Idea bounded profile: "
        f"{result['summary']['bounded_idea_profiles_passed']}/1; "
        f"negative guards={result['summary']['bounded_idea_negative_guards_rejected']}"
    )
    print(f"negative guards: {result['summary']['negative_guards_rejected']}/{len(result['negative_guard_results'])}")
    print(
        "Research Polisher component guards: "
        f"{result['summary']['research_polisher_component_guards_rejected']} passed "
        "(minimum 12)"
    )
    print(
        "live identity negative guards: "
        f"{result['summary']['live_identity_negative_guards_rejected']}/"
        f"{len(result['live_identity_negative_guard_results'])}"
    )
    print(f"finding routes: {result['summary']['finding_routes_verified']}/5")
    print(
        "polisher decision routes: "
        f"{result['summary']['polisher_decision_routes_verified']}/8"
    )
    print(
        "live output snapshots: "
        f"{result['summary']['live_workflows_receipts_audited']}/"
        f"{len(LIVE_RECEIPT_WORKFLOWS)} raw-bound receipts audited; "
        f"{result['summary']['live_workflows_reached_human_signoff_gate']} reached a validated human-signoff gate; "
        f"{result['summary']['live_workflows_stopped_at_valid_gate']} stopped at valid gates; "
        f"{result['summary']['live_workflows_blocked_at_valid_gate']} blocked at a valid gate; "
        f"{result['summary']['live_workflows_independent_review_pending']} independent-review pending; "
        f"{result['summary']['live_raw_state_claims_corrected']} raw state claims corrected; "
        f"applicability={result['summary']['live_receipt_applicability']}"
    )
    print("context profiles: conservative character proxy for 16K/32K behavior")
    print("runtime scope: deterministic replay; live receipts validated separately")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
