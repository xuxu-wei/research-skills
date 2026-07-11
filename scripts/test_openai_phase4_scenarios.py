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
FIXTURE_NAMES = ("idea.yaml", "proposal.yaml", "article.yaml", "perspective.yaml")
LIVE_RECEIPT_PATH = FIXTURE_ROOT / "live-forward-test-receipts.yaml"
PANEL_SKILLS = {
    "idea": "idea-adversarial-review-panel",
    "proposal": "proposal-review-panel",
    "article": "article-review-panel",
    "perspective": "perspective-review-panel",
}


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
        self.pending_revision_review_ids: set[str] = set()
        self.entry_gate_verified = False
        self.dissent_ids: set[str] = set()
        self.fatal_ids: set[str] = set()
        self.events: list[dict[str, Any]] = []
        self.edge_receipts: list[str] = []
        self.lifecycle_receipts: list[dict[str, Any]] = []
        self.initial_artifact_ids: list[str] = []

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
            require(artifact["source_skill"] == "external-input", "artifact_lineage", artifact["artifact_id"])
            require(artifact["created_by_instance_id"].startswith("fixture-user"), "artifact_lineage", artifact["artifact_id"])
            require(artifact["based_on"] == [], "artifact_lineage", artifact["artifact_id"])
            require(artifact["frozen"] is True, "artifact_not_frozen", artifact["artifact_id"])
            require(artifact["content_digest"] == "computed", "artifact_digest", artifact["artifact_id"])
            artifact["path"] = safe_relative(artifact["path"])
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
            elif report is not None and artifact["artifact_role"] in {"evaluation_report", "audit_report", "panel_report", "verification_report", "review_report"}:
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
                if self.artifacts[artifact_id]["artifact_role"] == revision_contract["controller_output_role"]
            ]
            require(len(plans) == 1, "revision_plan_missing", event["event_id"])
            require(plans[0]["source_skill"] == event["source_skill"], "revision_plan_missing", event["event_id"])
            output_roles = {artifact["artifact_role"] for artifact in outputs}
            required_output_roles = {"revision_delta"}
            if self.skills[event["destination_skill"]]["role"] == "drafter":
                required_output_roles.add("response_to_reviewers")
            require(
                required_output_roles <= output_roles,
                "revision_artifacts_missing",
                event["event_id"],
            )
        observation = self.materialize_outputs(event, outputs, None)
        self.writer_instances.add(event["actor_instance_id"])
        for artifact in outputs:
            if artifact["artifact_role"] != self.machine["primary_artifact_type"]:
                continue
            if self.current_primary is not None:
                expected_parent = f"{self.current_primary['artifact_id']}@{self.current_primary['version_id']}"
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
                    and sorted(artifact["artifact_role"] for artifact in artifacts) == sorted(expected_roles),
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

        final_verifier = destination in self.contract["verifier_compositor_outputs"]
        is_panel = destination == PANEL_SKILLS[self.workflow]
        forbidden_roles = set(self.contract["blindness_policy"]["forbidden_input_roles_for_evaluator_or_panel"])
        if destination == self.machine["evaluator_skill"] or is_panel:
            visible_roles = {self.artifacts[item]["artifact_role"] for item in event["input_artifact_ids"]}
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

        if is_panel:
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
            if route in {"blocked", "stopped"}:
                self.transition(route, "fatal_or_blocking_finding" if route == "blocked" else "unfixable_no_gain_or_user_stop", event["event_id"])
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
        require(self.panel_complete, "panel_gate", event["event_id"])
        require(not self.fatal_ids, "fatal_gate_bypassed", event["event_id"])
        require(set(event.get("preserved_dissent_ids", [])) >= self.dissent_ids, "dissent_not_preserved", event["event_id"])
        require(set(event.get("artifact_index_dissent_ids", [])) >= self.dissent_ids, "dissent_not_indexed", event["event_id"])
        require(event.get("automatic_external_submission") is False, "external_submission", event["event_id"])
        contract = self.contract["package_input_contracts"][self.workflow]
        input_artifacts = [self.artifacts[artifact_id] for artifact_id in event.get("input_artifact_ids", [])]
        require(input_artifacts, "package_input_contract", event["event_id"])
        require(
            {artifact["artifact_role"] for artifact in input_artifacts} <= set(contract["allowed_roles"]),
            "verifier_forbidden_input",
            event["event_id"],
        )
        current_ref = f"{self.current_primary['artifact_id']}@{self.current_primary['version_id']}"
        for requirement in contract["required_inputs"]:
            matches = [
                artifact
                for artifact in input_artifacts
                if artifact["artifact_role"] == requirement["artifact_role"]
                and (
                    "source_skill" not in requirement
                    or artifact["source_skill"] == requirement["source_skill"]
                )
            ]
            if requirement.get("count_from_panel_roles"):
                expected_count = len(self.fixture["panel"]["required_roles"])
                require(len(matches) == expected_count, "package_input_contract", f"{event['event_id']}: {requirement}")
            elif "minimum_count" in requirement:
                require(len(matches) >= requirement["minimum_count"], "package_input_contract", f"{event['event_id']}: {requirement}")
            else:
                require(len(matches) == requirement["count"], "package_input_contract", f"{event['event_id']}: {requirement}")
            require(all(artifact["frozen"] is True for artifact in matches), "package_input_contract", event["event_id"])
            if requirement.get("include_all_created"):
                all_created = {
                    artifact_id
                    for artifact_id, artifact in self.artifacts.items()
                    if artifact["artifact_role"] == requirement["artifact_role"]
                    and artifact["source_skill"] == requirement["source_skill"]
                }
                require({artifact["artifact_id"] for artifact in matches} == all_created, "package_input_contract", event["event_id"])
            if requirement.get("current_primary"):
                require(matches[0]["artifact_id"] == self.current_primary["artifact_id"], "package_input_contract", event["event_id"])
            if requirement.get("current_primary_lineage"):
                require(current_ref in matches[0]["based_on"], "package_input_contract", event["event_id"])
            if requirement.get("selected_artifact_lineage_role"):
                selected = [
                    artifact
                    for artifact in input_artifacts
                    if artifact["artifact_role"] == requirement["selected_artifact_lineage_role"]
                ]
                require(len(selected) == 1, "package_input_contract", event["event_id"])
                selected_ref = f"{selected[0]['artifact_id']}@{selected[0]['version_id']}"
                require(selected_ref in matches[0]["based_on"], "package_input_contract", event["event_id"])
            if requirement.get("all_panel_instances"):
                require(
                    {artifact["created_by_instance_id"] for artifact in matches}
                    == set(self.panel_instances.values()),
                    "package_input_contract",
                    event["event_id"],
                )
                require(
                    all(current_ref in artifact["based_on"] for artifact in matches),
                    "package_input_contract",
                    event["event_id"],
                )
        if self.workflow == "perspective":
            sealed = [artifact for artifact in input_artifacts if artifact["artifact_role"] in {"panel_summary", "artifact_index"}]
            sealed_parent_ids = {
                parent.split("@", 1)[0]
                for artifact in sealed
                for parent in artifact["based_on"]
            }
            required_review_artifact_ids = {
                artifact_id
                for artifact_id, artifact in self.artifacts.items()
                if artifact["source_skill"] == PANEL_SKILLS[self.workflow]
                or (
                    artifact["source_skill"] == self.machine["evaluator_skill"]
                    and current_ref in artifact["based_on"]
                )
                or artifact["artifact_role"] in {"revision_plan", "response_to_reviewers", "revision_delta"}
            }
            require(required_review_artifact_ids <= sealed_parent_ids, "package_input_contract", event["event_id"])

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
        observation = self.materialize_outputs(event, outputs, None)
        self.validate_package_output_lineage(event, outputs)
        self.writer_instances.add(event["actor_instance_id"])
        self.transition("human_signoff_required", "package_verified", event["event_id"])
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
    }[evaluator]
    evaluator_reviews = [event for event in reviews if event["destination_skill"] == evaluator_name]
    primary_produces = [
        event for event in fixture["events"]
        if event["type"] == "produce" and any(item["artifact_role"] in {"candidate_idea_set", "proposal", "manuscript", "perspective"} for item in event["outputs"])
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
        fixture["entry_mode"] = "resume_candidates"
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
        event["allowed_read_paths"][index] = "03_ideas/round-001/generated-idea-set-v001.md"
        event["review_report"]["input_artifact_ids"][index] = "ideas-v1"
        event["review_report"]["input_versions"][index] = "v001"
        event["review_report"]["files_read"][index] = "03_ideas/round-001/generated-idea-set-v001.md"
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
    else:
        raise ValueError(f"Unknown mutation: {mutation}")


def validate_retrieval_receipts() -> dict[str, Any]:
    receipts = load_yaml(FIXTURE_ROOT / "retrieval-receipts.yaml")
    targeted = receipts["targeted_search"]
    require(targeted["status"] == "targeted_search_verified", "search_receipt", "targeted status")
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


def validate_live_forward_test_receipts(registry: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    data = load_yaml(LIVE_RECEIPT_PATH)
    require(data.get("schema_version") == 2, "live_receipt_schema", "schema_version")
    require(data.get("capture_method") == "codex_fresh_delegated_instances", "live_receipt_schema", "capture method")
    require(data.get("evidence_class") == "self_attested_live_output_snapshot", "live_receipt_schema", "evidence class")
    require(
        data.get("applicability") == "skill_bodies_unchanged_by_phase4_registry_and_test_hardening",
        "live_receipt_schema",
        "applicability",
    )
    captured_version = str(data.get("plugin_version_under_test", ""))
    require(captured_version == "0.5.0-preview.1", "live_receipt_version", captured_version)
    require(registry.get("plugin_version") == "0.5.0-preview.2", "live_receipt_version", str(registry.get("plugin_version")))
    digest_record = data.get("skills_tree_digest", {})
    require(
        digest_record.get("algorithm") == "sha256_sorted_posix_relative_path_nul_crlf_normalized_bytes_nul",
        "live_receipt_digest",
        "algorithm",
    )
    file_count, current_digest = normalized_skills_tree_digest(PLUGIN / "skills")
    require(digest_record.get("file_count") == file_count, "live_receipt_digest", "file count")
    require(digest_record.get("current_preview_2") == current_digest, "live_receipt_digest", "current tree")
    require(digest_record.get("installed_preview_1") == current_digest, "live_receipt_digest", "installed/current mismatch")
    receipts = data.get("workflows", [])
    by_workflow = {item.get("workflow"): item for item in receipts}
    require(set(by_workflow) == {Path(name).stem for name in FIXTURE_NAMES}, "live_receipt_workflows", str(sorted(by_workflow)))

    audited = 0
    completed = 0
    stopped = 0
    blocked = 0
    pending = 0
    corrected_claims = 0
    orchestrators: list[str] = []
    summaries: list[dict[str, Any]] = []
    for workflow in ("idea", "proposal", "article", "perspective"):
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
    }
    return summaries, counts


def run_all() -> dict[str, Any]:
    registry = load_yaml(PLUGIN / "workflow-registry.yaml")
    schema = load_yaml(SCHEMA_PATH)
    scenario_results = []
    for name in FIXTURE_NAMES:
        fixture = load_yaml(FIXTURE_ROOT / name)
        with tempfile.TemporaryDirectory(prefix=f"openai-phase4-{fixture['workflow']}-") as temp:
            scenario_results.append(ScenarioEngine(fixture, registry, schema, Path(temp)).run())

    guard_spec = load_yaml(FIXTURE_ROOT / "guard-cases.yaml")
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
    return {
        "schema_version": 1,
        "plugin_version": registry["plugin_version"],
        "registry_schema_version": registry["schema_version"],
        "execution_scope": "deterministic_replay_plus_separate_live_receipts",
        "scenario_results": scenario_results,
        "negative_guard_results": guard_results,
        "finding_route_results": validate_finding_route_cases(),
        "live_forward_test_receipts": live_results,
        "retrieval_receipts": validate_retrieval_receipts(),
        "summary": {
            "workflows_passed": len(scenario_results),
            "negative_guards_rejected": len(guard_results),
            "finding_routes_verified": 5,
            "live_workflows_receipts_audited": live_counts["receipts_audited"],
            "live_workflows_reached_human_signoff_gate": live_counts["reached_human_signoff_gate"],
            "live_workflows_stopped_at_valid_gate": live_counts["stopped_at_valid_gate"],
            "live_workflows_blocked_at_valid_gate": live_counts["blocked_at_valid_gate"],
            "live_workflows_independent_review_pending": live_counts["independent_review_pending"],
            "live_raw_state_claims_corrected": live_counts["raw_state_claims_corrected"],
            "final_state": "human_signoff_required",
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
    print(f"workflows: {result['summary']['workflows_passed']}/4")
    print(f"negative guards: {result['summary']['negative_guards_rejected']}/{len(result['negative_guard_results'])}")
    print(f"finding routes: {result['summary']['finding_routes_verified']}/5")
    print(
        "live output snapshots: "
        f"{result['summary']['live_workflows_receipts_audited']}/4 raw-bound receipts audited; "
        f"{result['summary']['live_workflows_reached_human_signoff_gate']} reached a validated human-signoff gate; "
        f"{result['summary']['live_workflows_stopped_at_valid_gate']} stopped at valid gates; "
        f"{result['summary']['live_workflows_blocked_at_valid_gate']} blocked at a valid gate; "
        f"{result['summary']['live_workflows_independent_review_pending']} independent-review pending; "
        f"{result['summary']['live_raw_state_claims_corrected']} raw state claims corrected"
    )
    print("context profiles: conservative character proxy for 16K/32K behavior")
    print("runtime scope: deterministic replay; live receipts validated separately")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
