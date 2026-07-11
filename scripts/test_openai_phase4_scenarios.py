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
        self.artifacts: dict[str, dict[str, Any]] = {}
        self.current_primary: dict[str, Any] | None = None
        self.first_primary: dict[str, Any] | None = None
        self.primary_versions: list[str] = []
        self.latest_evaluated_version: str | None = None
        self.state = "initialized"
        self.reviewer_instances: set[str] = set()
        self.writer_instances: set[str] = set()
        self.evaluator_instances: list[str] = []
        self.panel_instances: dict[str, str] = {}
        self.panel_complete = False
        self.panel_patch_pending = False
        self.dissent_ids: set[str] = set()
        self.fatal_ids: set[str] = set()
        self.events: list[dict[str, Any]] = []
        self.edge_receipts: list[str] = []

    def validate_header(self) -> None:
        missing = missing_fields(self.fixture, self.schema["fixture_required"])
        require(not missing, "fixture_schema", f"missing fixture fields: {missing}")
        require(self.fixture["schema_version"] == self.schema["schema_version"], "fixture_schema", "schema version mismatch")
        require(self.fixture["execution_kind"] == "deterministic_replay", "execution_kind", "fixture is not a deterministic replay")
        require(self.workflow in self.registry["workflow_state_machines"], "unknown_workflow", self.workflow)
        require(self.fixture["plugin_version"] == self.registry["plugin_version"], "plugin_version", "fixture/registry mismatch")
        require(self.fixture["registry_schema_version"] == self.registry["schema_version"], "registry_schema", "fixture/registry mismatch")
        require(self.fixture["entry_mode"] in self.machine["entry_modes"], "entry_mode", self.fixture["entry_mode"])
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
        return edge

    def validate_artifact(self, artifact: dict[str, Any], event: dict[str, Any]) -> None:
        missing = missing_fields(artifact, self.schema["artifact_required"])
        require(not missing, "artifact_schema", f"{event['event_id']} missing artifact fields: {missing}")
        require(artifact["workflow_id"] == self.fixture["workflow_id"], "artifact_lineage", artifact["artifact_id"])
        require(artifact["plugin_version"] == self.registry["plugin_version"], "artifact_lineage", artifact["artifact_id"])
        require(artifact["source_skill"] == event["destination_skill"], "artifact_lineage", artifact["artifact_id"])
        require(artifact["created_by_instance_id"] == event["actor_instance_id"], "artifact_lineage", artifact["artifact_id"])
        require(artifact["frozen"] is True, "artifact_not_frozen", artifact["artifact_id"])
        require(artifact["content_digest"] == "computed", "artifact_digest", "fixtures must require runtime-computed digests")
        artifact["path"] = safe_relative(artifact["path"])
        require(artifact["artifact_id"] not in self.artifacts, "duplicate_artifact_id", artifact["artifact_id"])
        for parent in artifact["based_on"]:
            parent_id = parent.split("@", 1)[0]
            require(parent_id in self.artifacts, "dangling_lineage", parent)

    def materialize_outputs(self, event: dict[str, Any], outputs: list[dict[str, Any]], report: dict[str, Any] | None) -> dict[str, Any]:
        before = tree_hashes(self.workspace)
        input_paths = {self.artifacts[item]["path"] for item in event["input_artifact_ids"]}
        input_hashes_before = {path: before[path] for path in input_paths}
        declared_paths = {safe_relative(item["path"]) for item in outputs}
        allowed_writes = {safe_relative(path) for path in event["allowed_write_paths"]}
        require(declared_paths <= allowed_writes, "write_scope_escape", f"{event['event_id']}: {sorted(declared_paths - allowed_writes)}")
        require(not (declared_paths & input_paths), "input_write_overlap", f"{event['event_id']}: {sorted(declared_paths & input_paths)}")

        for artifact in outputs:
            self.validate_artifact(artifact, event)
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

        return {
            "files_read": list(report["files_read"]) if report else [],
            "actual_write_paths": actual_writes,
            "input_hashes_before": input_hashes_before,
            "input_hashes_after": input_hashes_after,
        }

    def process_produce(self, event: dict[str, Any]) -> dict[str, Any]:
        self.validate_dispatch(event)
        outputs = event.get("outputs", [])
        require(outputs, "event_schema", f"{event['event_id']} has no outputs")
        observation = self.materialize_outputs(event, outputs, None)
        self.writer_instances.add(event["actor_instance_id"])
        for artifact in outputs:
            if artifact["artifact_role"] != self.machine["primary_artifact_type"]:
                continue
            if self.current_primary is not None:
                expected_parent = f"{self.current_primary['artifact_id']}@{self.current_primary['version_id']}"
                require(expected_parent in artifact["based_on"], "artifact_lineage", f"missing {expected_parent}")
                require(artifact["version_id"] != self.current_primary["version_id"], "version_not_advanced", artifact["version_id"])
            self.current_primary = artifact
            self.first_primary = self.first_primary or artifact
            self.primary_versions.append(artifact["version_id"])
            self.state = "artifact_frozen"
            if event.get("panel_patch"):
                self.panel_patch_pending = True
        return observation

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
        require(set(report["files_read"]) <= set(event["allowed_read_paths"]), "read_scope", event["event_id"])
        require(set(report["files_read"]) == {self.artifacts[item]["path"] for item in event["input_artifact_ids"]}, "files_read_mismatch", event["event_id"])
        require(event["actor_instance_id"] not in self.reviewer_instances, "duplicate_reviewer_instance", event["actor_instance_id"])
        require(event["actor_instance_id"] not in self.writer_instances, "reviewer_is_writer", event["actor_instance_id"])
        for artifact_id in event["input_artifact_ids"]:
            require(self.artifacts[artifact_id]["created_by_instance_id"] != event["actor_instance_id"], "reviewer_is_writer", event["event_id"])

        final_verifier = destination in self.contract["verifier_compositor_outputs"]
        forbidden_roles = set(self.contract["blindness_policy"]["forbidden_input_roles_for_evaluator_or_panel"])
        if not final_verifier:
            visible_roles = {self.artifacts[item]["artifact_role"] for item in event["input_artifact_ids"]}
            require(not (visible_roles & forbidden_roles), "forbidden_review_input", f"{event['event_id']}: {visible_roles & forbidden_roles}")

        for finding in report["findings"]:
            missing_finding = missing_fields(finding, self.schema["finding_required"])
            require(not missing_finding, "finding_schema", f"{event['event_id']}: {missing_finding}")
            require(finding["source_review_id"] == report["review_id"], "finding_provenance", finding["finding_id"])

    def process_review(self, event: dict[str, Any]) -> dict[str, Any]:
        self.validate_dispatch(event)
        report = event.get("review_report")
        require(isinstance(report, dict), "review_schema", event["event_id"])
        self.validate_review(event, report)
        outputs = event.get("outputs", [])
        require(outputs, "review_schema", f"{event['event_id']} has no report artifact")
        observation = self.materialize_outputs(event, outputs, report)
        self.reviewer_instances.add(event["actor_instance_id"])

        destination = event["destination_skill"]
        final_verifier = destination in self.contract["verifier_compositor_outputs"]
        is_panel = destination.endswith("review-panel") or destination == "idea-adversarial-review-panel"
        for finding in report["findings"]:
            if finding.get("dissent"):
                self.dissent_ids.add(finding["finding_id"])
            if finding["severity"] in {"fatal", "blocking"} or finding["blocking"] is True:
                self.fatal_ids.add(finding["finding_id"])

        if self.fatal_ids:
            self.state = "blocked"
            return observation

        if is_panel:
            role = report["reviewer_role"]
            require(role not in self.panel_instances, "duplicate_panel_role", role)
            require(event["actor_instance_id"] not in self.panel_instances.values(), "duplicate_reviewer_instance", event["actor_instance_id"])
            require(report.get("peer_outputs_visible") is False, "peer_output_visible", event["event_id"])
            self.panel_instances[role] = event["actor_instance_id"]
            self.state = "panel_pending"
        elif destination == self.machine["evaluator_skill"]:
            require(self.current_primary is not None, "missing_primary_artifact", event["event_id"])
            require(self.current_primary["artifact_id"] in report["input_artifact_ids"], "review_inputs", event["event_id"])
            require(self.current_primary["version_id"] in report["input_versions"], "review_inputs", event["event_id"])
            self.evaluator_instances.append(event["actor_instance_id"])
            if report["decision"] in {"revise", "major_revision", "minor_revision"}:
                self.state = "revision_required"
            elif report["decision"] in {"accept", "strong_support", "support"}:
                self.latest_evaluated_version = self.current_primary["version_id"]
                if self.panel_patch_pending:
                    require(self.panel_complete, "panel_gate", "panel patch lacks completed panel")
                    self.state = "packaging_pending"
                    self.panel_patch_pending = False
                else:
                    self.state = "panel_pending"
            else:
                self.state = "stopped"
        elif final_verifier:
            self.validate_ready_for_package(event)
            copied = [item for item in outputs if item.get("copy_of") == self.current_primary["artifact_id"]]
            for item in copied:
                require(item["content_digest"] == self.current_primary["content_digest"], "compositor_copy_mismatch", event["event_id"])
            if destination == "perspective-final-compositor":
                require(copied, "compositor_copy_mismatch", event["event_id"])
            self.state = "human_signoff_required"
        else:
            self.state = "pending_review"
        return observation

    def process_panel_gate(self, event: dict[str, Any]) -> dict[str, Any]:
        required_roles = set(self.fixture["panel"]["required_roles"])
        require(set(self.panel_instances) == required_roles, "panel_roles_incomplete", f"expected {sorted(required_roles)}, got {sorted(self.panel_instances)}")
        require(set(event.get("preserved_dissent_ids", [])) >= self.dissent_ids, "dissent_not_preserved", event["event_id"])
        self.panel_complete = True
        if event["decision"] in {"minor_revision", "major_revision"}:
            self.state = "revision_required"
        elif event["decision"] == "pass":
            self.state = "packaging_pending"
        else:
            self.state = "stopped"
        return {"files_read": [], "actual_write_paths": [], "input_hashes_before": {}, "input_hashes_after": {}}

    def validate_ready_for_package(self, event: dict[str, Any]) -> None:
        require(self.current_primary is not None, "missing_primary_artifact", event["event_id"])
        qualifying = event.get("qualifying_evaluation_version", self.latest_evaluated_version)
        require(qualifying == self.current_primary["version_id"], "stale_evaluation", f"{qualifying} != {self.current_primary['version_id']}")
        require(self.latest_evaluated_version == self.current_primary["version_id"], "stale_evaluation", event["event_id"])
        require(self.panel_complete, "panel_gate", event["event_id"])
        require(not self.fatal_ids, "fatal_gate_bypassed", event["event_id"])
        require(set(event.get("preserved_dissent_ids", [])) >= self.dissent_ids, "dissent_not_preserved", event["event_id"])
        require(set(event.get("artifact_index_dissent_ids", [])) >= self.dissent_ids, "dissent_not_indexed", event["event_id"])
        require(event.get("automatic_external_submission") is False, "external_submission", event["event_id"])

    def process_package(self, event: dict[str, Any]) -> dict[str, Any]:
        self.validate_dispatch(event)
        self.validate_ready_for_package(event)
        outputs = event.get("outputs", [])
        require(outputs, "event_schema", f"{event['event_id']} has no package outputs")
        observation = self.materialize_outputs(event, outputs, None)
        self.writer_instances.add(event["actor_instance_id"])
        self.state = "human_signoff_required"
        return observation

    def validate_expected(self) -> None:
        expected = self.fixture["expected"]
        require(self.state == expected["final_state"], "expected_trace", f"final state {self.state}")
        require(self.primary_versions == expected["primary_versions"], "expected_trace", f"primary versions {self.primary_versions}")
        require(self.evaluator_instances == expected["evaluator_instances"], "expected_trace", f"evaluator instances {self.evaluator_instances}")
        require(self.panel_instances == expected["panel_role_instances"], "expected_trace", f"panel instances {self.panel_instances}")
        require(sorted(self.dissent_ids) == sorted(expected["dissent_ids"]), "expected_trace", f"dissent {self.dissent_ids}")
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
            if event["type"] == "produce":
                observation = self.process_produce(event)
            elif event["type"] == "review":
                observation = self.process_review(event)
            elif event["type"] == "panel_gate":
                observation = self.process_panel_gate(event)
            else:
                observation = self.process_package(event)
            require(self.state == event["expected_state_after"], "state_transition", f"{event['event_id']}: {self.state}")
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
                        else "orchestrator_internal_panel_gate"
                    ),
                    "observation": observation,
                }
            )
        self.validate_expected()
        return {
            "fixture_id": self.fixture["fixture_id"],
            "workflow": self.workflow,
            "execution_kind": self.fixture["execution_kind"],
            "final_state": self.state,
            "primary_versions": self.primary_versions,
            "evaluator_instances": self.evaluator_instances,
            "panel_role_instances": self.panel_instances,
            "dissent_ids": sorted(self.dissent_ids),
            "registry_edges_exercised": sorted(set(self.edge_receipts)),
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
        second["allowed_write_paths"] = [first_path]
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

    return {
        "schema_version": 1,
        "plugin_version": registry["plugin_version"],
        "registry_schema_version": registry["schema_version"],
        "execution_scope": "deterministic_replay_plus_separate_live_receipts",
        "scenario_results": scenario_results,
        "negative_guard_results": guard_results,
        "retrieval_receipts": validate_retrieval_receipts(),
        "summary": {
            "workflows_passed": len(scenario_results),
            "negative_guards_rejected": len(guard_results),
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
    print("context profiles: conservative character proxy for 16K/32K behavior")
    print("runtime scope: deterministic replay; live receipts validated separately")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
