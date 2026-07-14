#!/usr/bin/env python3
"""Contract tests for the Phase 7 external runtime-evidence runner."""

from __future__ import annotations

import json
import copy
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import yaml

from openai_preview_evidence import (
    EVIDENCE_ENVELOPE_SCHEMA,
    PREVIEW_ATTESTED,
    RELEASE_ASSET_INDEX_SCHEMA,
    VERIFIER_REPORT_SCHEMA,
    canonical_json_bytes,
    sha256_bytes,
)
from validate_openai_phase7_runtime_evidence import (
    ExternalRuntimeEvidenceRun,
    PREVIEW_ADAPTER_ID,
    WORKSPACE_MANIFEST_SCHEMA,
    RuntimeEvidenceError,
    current_checkout_source_identity,
    validate_external_runtime_evidence,
)


IDENTITY = current_checkout_source_identity()
WORKFLOW_CASES = [
    ("idea", "happy"),
    ("idea", "control"),
    ("proposal", "happy"),
    ("proposal", "control"),
    ("article", "happy"),
    ("article", "control"),
    ("perspective", "happy"),
    ("perspective", "control"),
    ("research_polisher", "happy"),
    ("research_polisher", "control"),
]


def json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def final_state(workflow: str, case_kind: str) -> str:
    if case_kind == "control":
        return {
            "idea": "stopped",
            "proposal": "blocked",
            "article": "blocked",
            "perspective": "stopped",
            "research_polisher": "no_defensible_option",
        }[workflow]
    return (
        "human_strategy_selection_required"
        if workflow == "research_polisher"
        else "human_signoff_required"
    )


def make_receipts() -> tuple[dict[str, Any], list[dict[str, bytes]]]:
    receipts: list[dict[str, Any]] = []
    payloads: list[dict[str, bytes]] = []
    for offset, (workflow, case_kind) in enumerate(WORKFLOW_CASES):
        receipt_id = f"phase7-{workflow.replace('_', '-')}-{case_kind}"
        prefix = f"runs/{offset:02d}-{receipt_id}"
        actor = json_bytes({"schema_version": 1, "actors": []})
        artifact = json_bytes({"schema_version": 1, "artifacts": []})
        actor_path = f"{prefix}/actor-manifest.json"
        artifact_path = f"{prefix}/artifact-index.json"
        access_path = f"{prefix}/file-access.json"
        task_path = f"{prefix}/task-export.json"
        access = json_bytes(
            {
                "schema_version": 1,
                "task_id": f"task-{offset:02d}",
                "plugin_version": IDENTITY["plugin_version"],
                "registry_sha256": IDENTITY["registry_sha256"],
                "source_commit": IDENTITY["source_commit"],
                "workflow": workflow,
                "reads": [],
                "writes": [],
                "source_artifact_hashes_unchanged": True,
            }
        )
        task = json_bytes(
            {
                "schema_version": 1,
                "captured_at": "2026-07-13T00:00:00Z",
                "receipt_id": receipt_id,
                "workflow": workflow,
                "case_kind": case_kind,
                "file_access": {
                    "path": access_path,
                    "sha256": sha256_bytes(access),
                },
            }
        )
        state = final_state(workflow, case_kind)
        receipts.append(
            {
                "receipt_id": receipt_id,
                "workflow": workflow,
                "case_kind": case_kind,
                "expected_final_state": state,
                "status": "verified",
                "binding": {
                    "plugin_version": IDENTITY["plugin_version"],
                    "registry_sha256": IDENTITY["registry_sha256"],
                    "source_commit": IDENTITY["source_commit"],
                    "task_export": {
                        "platform": "codex",
                        "task_id": f"task-{offset:02d}",
                        "path": task_path,
                        "sha256": sha256_bytes(task),
                    },
                    "actor_manifest": {"path": actor_path, "sha256": sha256_bytes(actor)},
                    "artifact_index": {
                        "path": artifact_path,
                        "sha256": sha256_bytes(artifact),
                    },
                },
                "file_access": {
                    "reads": [],
                    "writes": [],
                    "source_artifact_hashes_unchanged": True,
                },
                "lineage": {
                    "complete": True,
                    "current_artifact_ref": "primary@v001",
                    "evaluated_artifact_ref": "primary@v001",
                },
                "review_state": {
                    "dissent_ids": [],
                    "preserved_dissent_ids": [],
                    "fatal_finding_ids": [],
                    "unresolved_fatal_finding_ids": [],
                    "fatal_findings_visible": True,
                },
                "control_evidence": {
                    "input_condition": None,
                    "gate": None,
                    "finding": None,
                    "route": None,
                    "continuation_artifact_ref": None,
                },
                "final_state": state,
                "automatic_external_submission": False,
                "reason": "Externally witnessed test fixture.",
            }
        )
        payloads.append(
            {"task": task, "actor": actor, "artifact": artifact, "access": access}
        )
    collection = {
        "schema_version": 2,
        "evidence_kind": "current_version_durable_runtime_receipts",
        "platform_trust": {
            "adapter_status": "configured",
            "adapter_id": PREVIEW_ADAPTER_ID,
            "verification_level": PREVIEW_ATTESTED,
            "provider_authenticated": False,
            "reason": "Fixture uses an injected live-verifier contract.",
        },
        "receipts": receipts,
    }
    return collection, payloads


def asset_record(
    asset_id: int, name: str, kind: str, payload: bytes
) -> dict[str, Any]:
    return {
        "asset_id": asset_id,
        "name": name,
        "evidence_kind": kind,
        "sha256": sha256_bytes(payload),
        "size": len(payload),
    }


def build_bundle(
    directory: Path,
    *,
    bundle_number: int,
    receipt: Mapping[str, Any],
    payloads: Mapping[str, bytes],
    collection_bytes: bytes,
    bundle_id: str | None = None,
    logical_path_override: str | None = None,
) -> None:
    directory.mkdir(parents=True)
    ids = {name: bundle_number * 100 + offset for offset, name in enumerate(
        ("task", "actor", "artifact", "access", "collection", "manifest", "envelope", "report"), start=1
    )}
    local_names = {
        "task": "task-export.json",
        "actor": "actor-manifest.json",
        "artifact": "artifact-index.json",
        "access": "file-access.json",
        "collection": "runtime-receipts.yaml",
        "manifest": "workspace-manifest.json",
        "envelope": "evidence-envelope.json",
        "report": "verifier-report.json",
    }
    binding = receipt["binding"]
    paths = {
        "task": binding["task_export"]["path"],
        "actor": binding["actor_manifest"]["path"],
        "artifact": binding["artifact_index"]["path"],
        "access": json.loads(payloads["task"])["file_access"]["path"],
    }
    if logical_path_override is not None:
        paths["task"] = logical_path_override
    manifest = {
        "schema_version": WORKSPACE_MANIFEST_SCHEMA,
        "bundle_id": bundle_id or f"bundle-{bundle_number:02d}",
        "receipt_id": receipt["receipt_id"],
        "source_identity": IDENTITY,
        "runtime_receipts": {
            "logical_path": "phase7/runtime-receipts.yaml",
            "asset_id": ids["collection"],
            "sha256": sha256_bytes(collection_bytes),
            "size": len(collection_bytes),
        },
        "files": [
            {
                "logical_path": paths[key],
                "asset_id": ids[key],
                "sha256": sha256_bytes(payloads[key]),
                "size": len(payloads[key]),
            }
            for key in ("task", "actor", "artifact", "access")
        ],
    }
    manifest_bytes = json_bytes(manifest)
    captured = datetime.now(timezone.utc) - timedelta(minutes=3)
    witnessed = captured + timedelta(minutes=1)
    verified = witnessed + timedelta(minutes=1)
    stamp = lambda value: value.isoformat().replace("+00:00", "Z")
    envelope = {
        "schema_version": EVIDENCE_ENVELOPE_SCHEMA,
        "evidence_id": f"evidence-{bundle_number:02d}",
        "verification_level": PREVIEW_ATTESTED,
        "provider_verified": False,
        "counts_as_preview_acceptance": True,
        "source_identity": IDENTITY,
        "adapter": {
            "adapter_id": "codex-capture-adapter-v1",
            "adapter_code_sha256": "sha256:" + "4" * 64,
        },
        "capture": {
            "surface": "codex",
            "task_or_thread_id": binding["task_export"]["task_id"],
            "captured_at": stamp(captured),
            "raw_export_asset_id": ids["task"],
            "raw_export_sha256": sha256_bytes(payloads["task"]),
        },
        "github_witness": {
            "repository": "example/research-skills",
            "release_id": 700,
            "release_tag": f"v{IDENTITY['plugin_version']}",
            "workflow_run_id": 800,
            "actor": "fixture-actor",
            "raw_export_asset_id": ids["task"],
            "source_commit": IDENTITY["source_commit"],
        },
        "expected_verifier": {
            "verifier_id": "independent-preview-verifier-v1",
            "verifier_code_sha256": "sha256:" + "5" * 64,
            "independent": True,
        },
    }
    envelope_bytes = canonical_json_bytes(envelope)
    report = {
        "schema_version": VERIFIER_REPORT_SCHEMA,
        "verifier_id": "independent-preview-verifier-v1",
        "verifier_code_sha256": "sha256:" + "5" * 64,
        "source_identity": IDENTITY,
        "envelope_asset_id": ids["envelope"],
        "envelope_sha256": sha256_bytes(envelope_bytes),
        "raw_export_asset_id": ids["task"],
        "raw_export_sha256": sha256_bytes(payloads["task"]),
        "verdict": "accepted",
        "independent": True,
        "verified_at": stamp(verified),
    }
    report_bytes = json_bytes(report)
    bundle_payloads = {
        "task": payloads["task"],
        "actor": payloads["actor"],
        "artifact": payloads["artifact"],
        "access": payloads["access"],
        "collection": collection_bytes,
        "manifest": manifest_bytes,
        "envelope": envelope_bytes,
        "report": report_bytes,
    }
    records = [
        asset_record(ids["task"], local_names["task"], "task_export", bundle_payloads["task"]),
        asset_record(ids["actor"], local_names["actor"], "supporting_file", bundle_payloads["actor"]),
        asset_record(ids["artifact"], local_names["artifact"], "supporting_file", bundle_payloads["artifact"]),
        asset_record(ids["access"], local_names["access"], "supporting_file", bundle_payloads["access"]),
        asset_record(ids["collection"], local_names["collection"], "supporting_file", collection_bytes),
        asset_record(ids["manifest"], local_names["manifest"], "supporting_file", manifest_bytes),
        asset_record(ids["envelope"], local_names["envelope"], "evidence_envelope", envelope_bytes),
        asset_record(ids["report"], local_names["report"], "verifier_report", report_bytes),
    ]
    index = {
        "schema_version": RELEASE_ASSET_INDEX_SCHEMA,
        "source_identity": IDENTITY,
        "github_release": {
            "repository": "example/research-skills",
            "release_id": 700,
            "release_tag": f"v{IDENTITY['plugin_version']}",
        },
        "github_witness": {
            "workflow_run_id": 800,
            "actor": "fixture-actor",
            "source_commit": IDENTITY["source_commit"],
            "witnessed_at": stamp(witnessed),
        },
        "assets": records,
    }
    for key, payload in bundle_payloads.items():
        write(directory / local_names[key], payload)
    write(directory / "asset-index.json", json_bytes(index))


@dataclass
class Fixture:
    root: Path
    receipts: Path
    identity: Path
    collection: dict[str, Any]
    payloads: list[dict[str, bytes]]


def create_fixture(base: Path, *, duplicate_bundle: bool = False, duplicate_receipt: bool = False, path_escape: bool = False) -> Fixture:
    collection, payloads = make_receipts()
    control = base / "control"
    root = base / "evidence"
    root.mkdir(parents=True)
    control.mkdir(parents=True)
    collection_bytes = yaml.safe_dump(collection, sort_keys=False).encode("utf-8")
    receipts_path = control / "runtime-receipts.yaml"
    identity_path = control / "source-identity.json"
    write(receipts_path, collection_bytes)
    write(identity_path, json_bytes(IDENTITY))
    for offset in range(10):
        source_offset = 0 if duplicate_receipt and offset == 1 else offset
        build_bundle(
            root / f"bundle-{offset:02d}",
            bundle_number=offset + 1,
            receipt=collection["receipts"][source_offset],
            payloads=payloads[source_offset],
            collection_bytes=collection_bytes,
            bundle_id="bundle-duplicate" if duplicate_bundle and offset < 2 else None,
            logical_path_override="../escape.json" if path_escape and offset == 0 else None,
        )
    return Fixture(root, receipts_path, identity_path, collection, payloads)


class FakeLiveVerifier:
    adapter_id = PREVIEW_ADAPTER_ID

    def __call__(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return {"schema_version": 3, "request": dict(request), "live": True}


class FactoryContractLiveVerifier:
    """Structured v3 verifier used to exercise the real Phase 7 issuer."""

    adapter_id = PREVIEW_ADAPTER_ID

    def __call__(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "schema_version": 3,
            "verification_level": PREVIEW_ATTESTED,
            "provider_verified": False,
            "counts_as_preview_attested": True,
            "counts_as_provider_verified": False,
            "source_identity": request["expected_source_identity"],
            "integrity_result": request["_integrity_contract"],
            "live_verifier": {
                "adapter_id": PREVIEW_ADAPTER_ID,
                "live_requery_performed": True,
                "requery_source": "github_api",
                "independent": True,
                "verifier_workflow_run_id": 7001,
                "verified_at": "2026-07-13T00:00:00Z",
            },
            "gate_eligibility": {
                "eligible": True,
                "level": PREVIEW_ATTESTED,
                "determined_by": "registered_live_verifier",
                "provider_adapter_id": None,
                "provider_authenticated": False,
            },
        }


class FakeAttestationIssuer:
    def __init__(self, mutate: Path | None = None, mutation: Any = None) -> None:
        self.calls: list[str] = []
        self.mutate = mutate
        self.mutation = mutation

    def __call__(
        self,
        integrity_result,
        *,
        receipt_id: str,
        live_verifier,
        live_verifier_request,
        expected_adapter_id: str,
    ):
        assert expected_adapter_id == PREVIEW_ADAPTER_ID
        assert live_verifier(live_verifier_request)["live"] is True
        self.calls.append(receipt_id)
        if self.mutate is not None and len(self.calls) == 1:
            self.mutate.write_bytes(self.mutate.read_bytes() + b"tamper")
        if callable(self.mutation) and len(self.calls) == 1:
            self.mutation()
        return {"receipt_id": receipt_id, "integrity": integrity_result}


def request_builder(*, bundle) -> dict[str, Any]:
    return {"receipt_id": bundle.receipt_id, "evidence_id": bundle.integrity_result.evidence_id}


def factory_request_builder(*, bundle) -> dict[str, Any]:
    integrity = bundle.integrity_result
    contract = {
        "evidence_id": integrity.evidence_id,
        "integrity_valid": integrity.integrity_valid,
        "gate_eligible": integrity.gate_eligible,
        "claimed_verification_level": integrity.verification_level,
        "claimed_provider_verified": integrity.claimed_provider_verified,
        "claimed_counts_as_preview_acceptance": (
            integrity.claimed_counts_as_preview_acceptance
        ),
        "source_identity_bound": integrity.source_identity_bound,
        "raw_export_asset_id": integrity.raw_export_asset_id,
        "raw_export_sha256": integrity.raw_export_sha256,
        "envelope_asset_id": integrity.evidence_envelope_asset_id,
        "envelope_sha256": integrity.evidence_envelope_sha256,
        "verifier_report_asset_id": integrity.verifier_report_asset_id,
        "verifier_report_sha256": integrity.verifier_report_sha256,
        "release_asset_index_sha256": integrity.release_asset_index_sha256,
    }
    return {
        "receipt_id": bundle.receipt_id,
        "evidence_id": integrity.evidence_id,
        "adapter_id": PREVIEW_ADAPTER_ID,
        "expected_adapter_id": PREVIEW_ADAPTER_ID,
        "verification_level": PREVIEW_ATTESTED,
        "expected_verification_level": PREVIEW_ATTESTED,
        "source_identity": dict(integrity.source_identity),
        "expected_source_identity": dict(integrity.source_identity),
        "_integrity_contract": contract,
    }


def fake_runtime_validator(collection, **kwargs):
    root = kwargs["root"]
    attestations = kwargs["validated_evidence_results"]
    assert kwargs["supported_preview_adapter_ids"] == frozenset({PREVIEW_ADAPTER_ID})
    assert kwargs["supported_provider_adapter_ids"] == frozenset()
    assert set(attestations) == {item["receipt_id"] for item in collection["receipts"]}
    for receipt in collection["receipts"]:
        for key in ("task_export", "actor_manifest", "artifact_index"):
            path = root / Path(*receipt["binding"][key]["path"].split("/"))
            assert path.is_file()
            assert sha256_bytes(path.read_bytes()) == receipt["binding"][key]["sha256"]
    return [
        {
            "receipt_id": receipt["receipt_id"],
            "workflow": receipt["workflow"],
            "case_kind": receipt["case_kind"],
            "status": "verified",
            "verification_level": getattr(
                attestations[receipt["receipt_id"]],
                "verification_level",
                PREVIEW_ATTESTED,
            ),
            "evidence_accounting_status": "externally_attested_runtime_evidence",
            "external_evidence_id": getattr(
                attestations[receipt["receipt_id"]], "evidence_id", None
            ),
            "external_live_result_digest": getattr(
                attestations[receipt["receipt_id"]], "live_result_digest", None
            ),
            "external_verifier_workflow_run_id": getattr(
                attestations[receipt["receipt_id"]],
                "verifier_workflow_run_id",
                None,
            ),
            "external_verified_at": getattr(
                attestations[receipt["receipt_id"]], "verified_at", None
            ),
            "source_commit": receipt["binding"]["source_commit"],
            "platform": receipt["binding"]["task_export"]["platform"],
            "task_id": receipt["binding"]["task_export"]["task_id"],
            "task_export_path": receipt["binding"]["task_export"]["path"],
            "task_export_sha256": receipt["binding"]["task_export"]["sha256"],
        }
        for receipt in collection["receipts"]
    ]


def run(
    fixture: Fixture,
    issuer: FakeAttestationIssuer | None = None,
    runtime_validator: Any = fake_runtime_validator,
) -> dict[str, Any]:
    return validate_external_runtime_evidence(
        evidence_root=fixture.root,
        runtime_receipts_path=fixture.receipts,
        expected_source_identity_path=fixture.identity,
        asset_index_pattern="*/asset-index.json",
        registry={},
        schema={},
        attestation_issuer=issuer or FakeAttestationIssuer(),
        runtime_validator=runtime_validator,
        live_verifier=FakeLiveVerifier(),
        request_builder=request_builder,
    )


def expect_rejection(
    fixture: Fixture,
    expected_code: str,
    issuer: FakeAttestationIssuer | None = None,
    runtime_validator: Any = fake_runtime_validator,
) -> None:
    try:
        run(fixture, issuer, runtime_validator)
    except RuntimeEvidenceError as exc:
        if exc.code != expected_code:
            raise AssertionError(f"expected {expected_code}, got {exc.code}: {exc}") from exc
    else:
        raise AssertionError(f"fixture unexpectedly accepted; expected {expected_code}")


def main() -> int:
    checks = 0
    with tempfile.TemporaryDirectory(prefix="phase7-external-runner-tests-") as directory:
        base = Path(directory)

        happy = create_fixture(base / "happy")
        issuer = FakeAttestationIssuer()
        result = run(happy, issuer)
        assert result["accepted"] is True and result["bundle_count"] == 10
        assert len(issuer.calls) == 10 and len(set(issuer.calls)) == 10
        checks += 1

        # Exercise the public factory rather than relying only on the injected
        # fixture issuer. This catches request/result-field drift across files.
        from test_openai_phase7_modes import (
            ModeViolation,
            assert_phase7_complete_preview,
            consume_external_runtime_validation_session,
            edge_derived_actor_edges,
            issue_external_runtime_attestation,
            issue_external_runtime_validation_session,
            runtime_actor_role_contract,
            runtime_artifact_role_contract,
        )

        repository_root = Path(__file__).resolve().parents[1]
        registry = yaml.safe_load(
            (repository_root / "research-skills-openai" / "workflow-registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        schema = yaml.safe_load(
            (repository_root / "tests" / "openai_phase7" / "runtime-receipts.schema.yaml").read_text(
                encoding="utf-8"
            )
        )
        role_contract = runtime_actor_role_contract(registry, schema)
        assert {"supporting_reviewer", "supporting_writer"} <= set(
            role_contract["allowed_roles"]
        )
        proposal_supporting_writers = edge_derived_actor_edges(
            registry, "proposal", "supporting_writer"
        )
        assert {edge[1] for edge in proposal_supporting_writers} == {"sap-writer"}
        assert {edge[0] for edge in proposal_supporting_writers} == {
            "proposal-orchestrator",
            "sap-refinement-controller",
        }
        polisher_roles = runtime_artifact_role_contract(registry)
        assert (
            polisher_roles["finding_index_role_by_workflow"]["research_polisher"]
            == "research_polisher_review_finding_index"
        )
        assert "research_polisher_specialist_findings_bundle" in polisher_roles[
            "assembler_outputs_by_skill"
        ]["research-polisher-plan-assembler"]
        assert polisher_roles["supporting_writer_outputs_by_skill"] == {
            "sap-writer": ["sap"],
            "article-frontmatter-drafter": ["frontmatter"],
        }
        checks += 1

        factory_contract = create_fixture(base / "factory-contract")
        factory_result = validate_external_runtime_evidence(
            evidence_root=factory_contract.root,
            runtime_receipts_path=factory_contract.receipts,
            expected_source_identity_path=factory_contract.identity,
            asset_index_pattern="*/asset-index.json",
            registry={},
            schema={},
            attestation_issuer=issue_external_runtime_attestation,
            runtime_validator=fake_runtime_validator,
            live_verifier=FactoryContractLiveVerifier(),
            request_builder=factory_request_builder,
            report_session_issuer=issue_external_runtime_validation_session,
            retain_report_session=True,
        )
        assert isinstance(factory_result, ExternalRuntimeEvidenceRun)
        assert factory_result.summary["accepted"] is True
        retained_results = consume_external_runtime_validation_session(
            factory_result.report_session,
            collection=factory_contract.collection,
            runtime_receipts_path=factory_contract.receipts,
            expected_source_commit=IDENTITY["source_commit"],
        )
        assert len(retained_results) == 10
        assert all(
            item["evidence_accounting_status"]
            == "externally_attested_runtime_evidence"
            for item in retained_results
        )
        strict_report = {
            "schema_version": 3,
            "phase_status": "complete_preview_attested",
            "verification_level": PREVIEW_ATTESTED,
            "provider_verified": False,
            "counts_as_preview_acceptance": True,
            "pending_gates": [],
            "live_model_execution": True,
            "completion_gates": {
                f"gate-{offset:02d}": {"status": "verified"}
                for offset in range(13)
            },
            "runtime_receipts": {
                "verified_receipt_count": 10,
                "pending_receipt_count": 0,
                "results": retained_results,
            },
            "summary": {
                "runtime_receipts_verified": 10,
                "runtime_receipts_pending": 0,
                "live_model_runs_claimed": 10,
                "completion_gates_verified": 13,
                "completion_gates_pending": 0,
                "false_ready_count": 0,
            },
        }
        assert_phase7_complete_preview(strict_report)
        incomplete_report = copy.deepcopy(strict_report)
        incomplete_report["summary"]["completion_gates_pending"] = 1
        try:
            assert_phase7_complete_preview(incomplete_report)
        except ModeViolation as exc:
            assert exc.code == "phase7_complete_preview_summary_invalid"
        else:
            raise AssertionError("strict Phase 7 checker accepted a pending gate")
        try:
            copy.deepcopy(factory_result)
        except TypeError:
            pass
        else:
            raise AssertionError("opaque external runtime run was copyable")
        try:
            json.dumps(factory_result)
        except TypeError:
            pass
        else:
            raise AssertionError("opaque external runtime run was JSON serializable")
        checks += 1

        missing_session_issuer = create_fixture(base / "missing-session-issuer")
        try:
            validate_external_runtime_evidence(
                evidence_root=missing_session_issuer.root,
                runtime_receipts_path=missing_session_issuer.receipts,
                expected_source_identity_path=missing_session_issuer.identity,
                asset_index_pattern="*/asset-index.json",
                registry={},
                schema={},
                attestation_issuer=issue_external_runtime_attestation,
                runtime_validator=fake_runtime_validator,
                live_verifier=FactoryContractLiveVerifier(),
                request_builder=factory_request_builder,
                retain_report_session=True,
            )
        except RuntimeEvidenceError as exc:
            assert exc.code == "report_session_issuer_missing"
        else:
            raise AssertionError("retained validation accepted without session issuer")
        checks += 1

        wrong_identity = create_fixture(base / "wrong-identity")
        mismatched = dict(IDENTITY)
        mismatched["skill_tree_sha256"] = "sha256:" + "f" * 64
        write(wrong_identity.identity, json_bytes(mismatched))
        expect_rejection(wrong_identity, "local_source_identity_mismatch")
        checks += 1

        missing = create_fixture(base / "missing")
        shutil.rmtree(missing.root / "bundle-09")
        expect_rejection(missing, "runtime_bundle_count")
        checks += 1

        escaping = create_fixture(base / "escaping", path_escape=True)
        expect_rejection(escaping, "logical_path_not_canonical")
        checks += 1

        stray = create_fixture(base / "stray")
        write(stray.root / "bundle-00" / "not-indexed.txt", b"not indexed")
        expect_rejection(stray, "unindexed_evidence_file")
        checks += 1

        duplicate_bundle = create_fixture(base / "duplicate-bundle", duplicate_bundle=True)
        expect_rejection(duplicate_bundle, "duplicate_bundle")
        checks += 1

        duplicate_receipt = create_fixture(base / "duplicate-receipt", duplicate_receipt=True)
        expect_rejection(duplicate_receipt, "duplicate_receipt_bundle")
        checks += 1

        changing = create_fixture(base / "changing")
        changed_path = changing.root / "bundle-00" / "task-export.json"
        original = changed_path.read_bytes()
        try:
            expect_rejection(
                changing,
                "source_changed_during_validation",
                FakeAttestationIssuer(mutate=changed_path),
            )
        finally:
            changed_path.write_bytes(original)
        checks += 1

        adding_file = create_fixture(base / "adding-file")
        injected_file = adding_file.root / "bundle-00" / "injected" / "new.txt"
        expect_rejection(
            adding_file,
            "source_inventory_changed_during_validation",
            FakeAttestationIssuer(
                mutation=lambda: write(injected_file, b"new evidence")
            ),
        )
        checks += 1

        adding_directory = create_fixture(base / "adding-directory")
        injected_directory = adding_directory.root / "bundle-00" / "empty-added"
        expect_rejection(
            adding_directory,
            "source_inventory_changed_during_validation",
            FakeAttestationIssuer(mutation=lambda: injected_directory.mkdir()),
        )
        checks += 1

        workspace_mutation = create_fixture(base / "workspace-mutation")

        def add_workspace_entry(collection, **kwargs):
            results = fake_runtime_validator(collection, **kwargs)
            write(kwargs["root"] / "validator-added" / "new.txt", b"mutation")
            return results

        expect_rejection(
            workspace_mutation,
            "temporary_workspace_changed",
            runtime_validator=add_workspace_entry,
        )
        checks += 1

        symlink_mutation = create_fixture(base / "symlink-mutation")
        symlink_target = symlink_mutation.root / "bundle-00" / "task-export.json"
        symlink_path = symlink_mutation.root / "bundle-00" / "injected-link.json"
        symlink_supported = False
        try:
            symlink_path.symlink_to(symlink_target)
            symlink_supported = symlink_path.is_symlink()
        except OSError:
            symlink_supported = False
        finally:
            if symlink_path.is_symlink():
                symlink_path.unlink()
        if symlink_supported:
            expect_rejection(
                symlink_mutation,
                "symlink_rejected",
                FakeAttestationIssuer(
                    mutation=lambda: symlink_path.symlink_to(symlink_target)
                ),
            )
            checks += 1

        unsafe_pattern = create_fixture(base / "unsafe-pattern")
        try:
            validate_external_runtime_evidence(
                evidence_root=unsafe_pattern.root,
                runtime_receipts_path=unsafe_pattern.receipts,
                expected_source_identity_path=unsafe_pattern.identity,
                asset_index_pattern="../*.json",
                registry={},
                schema={},
                attestation_issuer=FakeAttestationIssuer(),
                runtime_validator=fake_runtime_validator,
                live_verifier=FakeLiveVerifier(),
                request_builder=request_builder,
            )
        except RuntimeEvidenceError as exc:
            assert exc.code == "unsafe_asset_index_pattern"
        else:
            raise AssertionError("unsafe index pattern was accepted")
        checks += 1

    print(f"Phase 7 external runtime runner tests passed: {checks} contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
