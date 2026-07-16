#!/usr/bin/env python3
"""Replay every declared OpenAI workflow entry mode against registry contracts.

This is a synthetic deterministic contract replay. Registry-declared gate and
lifecycle contracts are exercised with generated artifacts and reviewer
receipts plus negative mutations. It does not execute a live model, Search,
Deep Research, Codex task, or ChatGPT task. Runtime evidence is a separate
Phase 7 deliverable and must not be inferred from this report.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pickle
import re
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping

import yaml

from openai_preview_evidence import (
    PREVIEW_ATTESTED,
    PROVIDER_VERIFIED,
    EvidenceValidationError,
    EvidenceValidationResult,
    canonical_json_bytes,
    sha256_bytes as evidence_sha256_bytes,
    validate_evidence_bundle,
)
from test_openai_release_ledger import (
    build_cache_artifact,
    configured_external_evidence_level,
    release_source_identity,
    validate_bound_external_evidence,
    validate_cache_artifact,
    validate_verified_source_commit_tree,
)


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
REGISTRY_PATH = PLUGIN / "workflow-registry.yaml"
FIXTURE_PATH = REPO / "tests" / "openai_phase7" / "mode-cases.yaml"
POLISHER_ROUTING_BOUNDARY_PATH = (
    REPO / "tests" / "openai_phase7" / "research-polisher-routing-boundaries.yaml"
)
RUNTIME_SCHEMA_PATH = REPO / "tests" / "openai_phase7" / "runtime-receipts.schema.yaml"
RUNTIME_RECEIPTS_PATH = (
    REPO / "tests" / "openai_phase7" / "current-version-runtime-receipts.yaml"
)
RELEASE_LEDGER_PATH = PLUGIN / "reports" / "release-ledger.json"
REPORT_PATH = PLUGIN / "reports" / "phase7-mode-results.json"
# Repository-authored exports and hashes prove integrity, not platform origin.
# Add an adapter here only when its verifier independently re-queries the
# declared external witness rather than trusting fields from the receipt itself.
SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS: frozenset[str] = frozenset()
PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID = "github_release_asset_preview_v1"
SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS: frozenset[str] = frozenset(
    {PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID}
)
ACCEPTANCE_LEVELS = frozenset({PREVIEW_ATTESTED, PROVIDER_VERIFIED})


class _ExternalRuntimeAttestationCapability:
    """Private in-process capability that cannot be serialized or copied."""

    def __reduce__(self) -> Any:
        raise TypeError("external runtime attestation capabilities are not serializable")

    def __deepcopy__(self, _memo: dict[int, Any]) -> Any:
        raise TypeError("external runtime attestation capabilities are not copyable")


_EXTERNAL_RUNTIME_ATTESTATION_CAPABILITY = _ExternalRuntimeAttestationCapability()


@dataclass(frozen=True)
class ExternalRuntimeAttestation:
    """Gate-eligible runtime attestation issued only after a live re-query."""

    integrity_result: EvidenceValidationResult
    verification_level: str
    provider_verified: bool
    counts_as_preview_acceptance: bool
    counts_as_runtime_evidence: bool
    adapter_id: str
    attestation_scope: str
    live_result_digest: str
    verifier_workflow_run_id: int
    verified_at: str
    _capability: _ExternalRuntimeAttestationCapability

    @property
    def evidence_id(self) -> str:
        return self.integrity_result.evidence_id


@dataclass(frozen=True)
class ExternalRuntimeValidationSession:
    """Opaque handoff from live validation to Phase 7 report generation.

    The session keeps the actual in-process attestations alongside the
    semantic validator results.  A serialized receipt, result dictionary, or
    boolean can therefore never stand in for the live validation run.
    """

    runtime_receipts_sha256: str
    expected_source_commit: str
    verification_level: str
    provider_verified: bool
    adapter_id: str
    receipt_ids: tuple[str, ...]
    attestations: Mapping[str, ExternalRuntimeAttestation]
    runtime_results: tuple[Mapping[str, Any], ...]
    _capability: _ExternalRuntimeAttestationCapability

    def __reduce__(self) -> Any:
        raise TypeError("external runtime validation sessions are not serializable")

    def __deepcopy__(self, _memo: dict[int, Any]) -> Any:
        raise TypeError("external runtime validation sessions are not copyable")


def _integrity_result_contract(
    integrity_result: EvidenceValidationResult,
) -> dict[str, Any]:
    return {
        "evidence_id": integrity_result.evidence_id,
        "integrity_valid": integrity_result.integrity_valid,
        "gate_eligible": integrity_result.gate_eligible,
        "claimed_verification_level": integrity_result.verification_level,
        "claimed_provider_verified": integrity_result.claimed_provider_verified,
        "claimed_counts_as_preview_acceptance": (
            integrity_result.claimed_counts_as_preview_acceptance
        ),
        "source_identity_bound": integrity_result.source_identity_bound,
        "raw_export_asset_id": integrity_result.raw_export_asset_id,
        "raw_export_sha256": integrity_result.raw_export_sha256,
        "envelope_asset_id": integrity_result.evidence_envelope_asset_id,
        "envelope_sha256": integrity_result.evidence_envelope_sha256,
        "verifier_report_asset_id": integrity_result.verifier_report_asset_id,
        "verifier_report_sha256": integrity_result.verifier_report_sha256,
        "release_asset_index_sha256": (
            integrity_result.release_asset_index_sha256
        ),
    }


def issue_external_runtime_attestation(
    integrity_result: EvidenceValidationResult,
    *,
    receipt_id: str,
    live_verifier: Any,
    live_verifier_request: Mapping[str, Any],
    expected_adapter_id: str,
) -> ExternalRuntimeAttestation:
    """Call an allowlisted live verifier and issue an in-process attestation.

    The returned value, rather than the verifier's serializable document, is
    the only external-evidence type that can promote a Phase 7 runtime receipt.
    """

    require(
        isinstance(receipt_id, str) and bool(receipt_id.strip()),
        "runtime_external_attestation_receipt_id_invalid",
        str(receipt_id),
    )
    require(
        isinstance(integrity_result, EvidenceValidationResult)
        and integrity_result.integrity_valid
        and not integrity_result.gate_eligible
        and not integrity_result.provider_verified
        and not integrity_result.counts_as_preview_acceptance,
        "runtime_external_attestation_integrity_boundary_invalid",
        "shared evidence validation must remain integrity-only",
    )
    expected_verification_level = integrity_result.verification_level
    expected_source_identity = dict(integrity_result.source_identity)
    require(
        expected_verification_level in ACCEPTANCE_LEVELS
        and integrity_result.verification_level == expected_verification_level
        and integrity_result.claimed_provider_verified
        is (expected_verification_level == PROVIDER_VERIFIED)
        and integrity_result.claimed_counts_as_preview_acceptance is True,
        "runtime_external_attestation_claim_mismatch",
        expected_verification_level,
    )
    require(
        integrity_result.source_identity_bound,
        "runtime_external_attestation_source_identity_mismatch",
        integrity_result.evidence_id,
    )
    supported_adapters = (
        SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS
        if expected_verification_level == PROVIDER_VERIFIED
        else SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS
    )
    require(
        expected_adapter_id in supported_adapters,
        "runtime_external_attestation_adapter_not_allowlisted",
        expected_adapter_id,
    )
    require(
        callable(live_verifier)
        and getattr(live_verifier, "adapter_id", None) == expected_adapter_id,
        "runtime_external_attestation_verifier_invalid",
        expected_adapter_id,
    )
    require(
        isinstance(live_verifier_request, Mapping),
        "runtime_external_attestation_request_invalid",
        receipt_id,
    )
    try:
        request_document = copy.deepcopy(dict(live_verifier_request))
    except Exception as exc:
        raise ModeViolation(
            "runtime_external_attestation_request_invalid",
            f"{receipt_id}: {type(exc).__name__}: {exc}",
        ) from exc
    request_bindings = {
        "receipt_id": receipt_id,
        "evidence_id": integrity_result.evidence_id,
        "adapter_id": expected_adapter_id,
        "expected_adapter_id": expected_adapter_id,
        "verification_level": expected_verification_level,
        "expected_verification_level": expected_verification_level,
        "source_identity": expected_source_identity,
        "expected_source_identity": expected_source_identity,
    }
    for field, expected_value in request_bindings.items():
        if field in request_document:
            require(
                request_document[field] == expected_value,
                "runtime_external_attestation_request_binding_mismatch",
                f"{receipt_id}: {field}",
            )
    expected_integrity = _integrity_result_contract(integrity_result)
    try:
        result_document = live_verifier(request_document)
    except Exception as exc:
        raise ModeViolation(
            "runtime_external_attestation_live_requery_failed",
            f"{type(exc).__name__}: {exc}",
        ) from exc
    require(
        isinstance(result_document, dict),
        "runtime_external_attestation_result_invalid",
        "live verifier must return an object",
    )
    require(
        result_document.get("schema_version") == 3,
        "runtime_external_attestation_schema_invalid",
        "live verifier result schema_version must be 3",
    )
    require(
        result_document.get("verification_level") == expected_verification_level
        and result_document.get("provider_verified")
        is (expected_verification_level == PROVIDER_VERIFIED),
        "runtime_external_attestation_level_invalid",
        expected_verification_level,
    )
    optional_level_flags = {
        "counts_as_preview_attested": True,
        "counts_as_preview_acceptance": True,
        "counts_as_provider_verified": (
            expected_verification_level == PROVIDER_VERIFIED
        ),
    }
    for field, expected_value in optional_level_flags.items():
        if field in result_document:
            require(
                result_document[field] is expected_value,
                "runtime_external_attestation_level_invalid",
                f"{expected_verification_level}: {field}",
            )
    require(
        result_document.get("source_identity") == dict(expected_source_identity),
        "runtime_external_attestation_source_identity_mismatch",
        integrity_result.evidence_id,
    )
    live_integrity = result_document.get("integrity_result")
    require(
        isinstance(live_integrity, dict),
        "runtime_external_attestation_integrity_result_missing",
        integrity_result.evidence_id,
    )
    for field in (
        "evidence_id",
        "integrity_valid",
        "gate_eligible",
        "claimed_verification_level",
        "claimed_provider_verified",
        "claimed_counts_as_preview_acceptance",
        "source_identity_bound",
        "raw_export_asset_id",
        "raw_export_sha256",
        "envelope_asset_id",
        "envelope_sha256",
        "verifier_report_asset_id",
        "verifier_report_sha256",
        "release_asset_index_sha256",
    ):
        require(
            live_integrity.get(field) == expected_integrity[field],
            "runtime_external_attestation_integrity_binding_mismatch",
            f"{integrity_result.evidence_id}: {field}",
        )
    live_verifier = result_document.get("live_verifier")
    require(
        isinstance(live_verifier, dict)
        and live_verifier.get("adapter_id") == expected_adapter_id
        and live_verifier.get("live_requery_performed") is True
        and live_verifier.get("requery_source") == "github_api"
        and live_verifier.get("independent") is True
        and isinstance(live_verifier.get("verifier_workflow_run_id"), int)
        and not isinstance(live_verifier.get("verifier_workflow_run_id"), bool)
        and live_verifier.get("verifier_workflow_run_id") > 0
        and isinstance(live_verifier.get("verified_at"), str)
        and bool(live_verifier.get("verified_at")),
        "runtime_external_attestation_live_requery_invalid",
        integrity_result.evidence_id,
    )
    gate = result_document.get("gate_eligibility")
    require(
        isinstance(gate, dict)
        and gate.get("eligible") is True
        and gate.get("level") == expected_verification_level
        and gate.get("determined_by") == "registered_live_verifier",
        "runtime_external_attestation_gate_invalid",
        integrity_result.evidence_id,
    )
    if expected_verification_level == PREVIEW_ATTESTED:
        require(
            gate.get("provider_authenticated") is False
            and gate.get("provider_adapter_id") is None,
            "runtime_external_attestation_preview_provider_confusion",
            integrity_result.evidence_id,
        )
    else:
        provider_adapter_id = gate.get("provider_adapter_id")
        require(
            gate.get("provider_authenticated") is True
            and provider_adapter_id
            in SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS,
            "runtime_external_attestation_provider_boundary_invalid",
            integrity_result.evidence_id,
        )
    return ExternalRuntimeAttestation(
        integrity_result=integrity_result,
        verification_level=expected_verification_level,
        provider_verified=expected_verification_level == PROVIDER_VERIFIED,
        counts_as_preview_acceptance=True,
        counts_as_runtime_evidence=True,
        adapter_id=expected_adapter_id,
        attestation_scope="phase7_external_runtime_live_requery",
        live_result_digest=evidence_sha256_bytes(
            canonical_json_bytes(result_document)
        ),
        verifier_workflow_run_id=live_verifier["verifier_workflow_run_id"],
        verified_at=live_verifier["verified_at"],
        _capability=_EXTERNAL_RUNTIME_ATTESTATION_CAPABILITY,
    )


def _is_valid_external_runtime_attestation(value: Any) -> bool:
    return (
        isinstance(value, ExternalRuntimeAttestation)
        and value._capability is _EXTERNAL_RUNTIME_ATTESTATION_CAPABILITY
        and value.attestation_scope == "phase7_external_runtime_live_requery"
        and value.adapter_id
        in (
            SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS
            if value.verification_level == PROVIDER_VERIFIED
            else SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS
        )
        and value.counts_as_preview_acceptance is True
        and value.counts_as_runtime_evidence is True
        and bool(re.fullmatch(r"sha256:[0-9a-f]{64}", value.live_result_digest))
        and isinstance(value.verifier_workflow_run_id, int)
        and not isinstance(value.verifier_workflow_run_id, bool)
        and value.verifier_workflow_run_id > 0
        and isinstance(value.verified_at, str)
        and bool(value.verified_at)
        and value.provider_verified
        is (value.verification_level == PROVIDER_VERIFIED)
        and value.integrity_result.integrity_valid
        and not value.integrity_result.gate_eligible
        and not value.integrity_result.provider_verified
        and not value.integrity_result.counts_as_preview_acceptance
    )


def issue_external_runtime_validation_session(
    *,
    collection: Mapping[str, Any],
    runtime_receipts_sha256: str,
    expected_source_commit: str,
    expected_adapter_id: str,
    validated_evidence_results: Mapping[str, Any],
    validated_runtime_results: list[dict[str, Any]],
) -> ExternalRuntimeValidationSession:
    """Seal one fully validated 10-slot run for same-process reporting."""

    receipts = collection.get("receipts")
    require(
        isinstance(receipts, list) and len(receipts) == 10,
        "runtime_external_session_receipt_count",
        str(len(receipts) if isinstance(receipts, list) else type(receipts).__name__),
    )
    require(
        valid_commit_sha(expected_source_commit),
        "runtime_external_session_source_commit_invalid",
        str(expected_source_commit),
    )
    require(
        isinstance(runtime_receipts_sha256, str)
        and re.fullmatch(r"sha256:[0-9a-f]{64}", runtime_receipts_sha256)
        is not None,
        "runtime_external_session_collection_digest_invalid",
        str(runtime_receipts_sha256),
    )
    receipt_ids = [receipt.get("receipt_id") for receipt in receipts]
    require(
        all(isinstance(item, str) and bool(item) for item in receipt_ids)
        and len(set(receipt_ids)) == 10,
        "runtime_external_session_receipt_ids_invalid",
        str(receipt_ids),
    )
    receipt_pairs = [
        (receipt.get("workflow"), receipt.get("case_kind")) for receipt in receipts
    ]
    require(
        Counter(kind for _, kind in receipt_pairs) == Counter({"happy": 5, "control": 5}),
        "runtime_external_session_case_matrix_invalid",
        str(receipt_pairs),
    )
    require(
        set(validated_evidence_results) == set(receipt_ids),
        "runtime_external_session_attestation_coverage",
        str(sorted(validated_evidence_results)),
    )
    attestations: dict[str, ExternalRuntimeAttestation] = {}
    for receipt_id in receipt_ids:
        attestation = validated_evidence_results[receipt_id]
        require(
            _is_valid_external_runtime_attestation(attestation),
            "runtime_external_session_attestation_invalid",
            str(receipt_id),
        )
        require(
            attestation.verification_level == PREVIEW_ATTESTED
            and attestation.provider_verified is False
            and attestation.adapter_id == expected_adapter_id
            and attestation.integrity_result.source_identity.get("source_commit")
            == expected_source_commit,
            "runtime_external_session_attestation_binding_mismatch",
            str(receipt_id),
        )
        attestations[str(receipt_id)] = attestation

    require(
        isinstance(validated_runtime_results, list)
        and len(validated_runtime_results) == 10,
        "runtime_external_session_result_count",
        str(len(validated_runtime_results)),
    )
    result_by_id: dict[str, Mapping[str, Any]] = {}
    expected_by_id = {str(receipt["receipt_id"]): receipt for receipt in receipts}
    for result in validated_runtime_results:
        require(
            isinstance(result, Mapping),
            "runtime_external_session_result_invalid",
            type(result).__name__,
        )
        receipt_id = result.get("receipt_id")
        require(
            isinstance(receipt_id, str)
            and receipt_id in expected_by_id
            and receipt_id not in result_by_id,
            "runtime_external_session_result_coverage",
            str(receipt_id),
        )
        receipt = expected_by_id[receipt_id]
        require(
            result.get("status") == "verified"
            and result.get("verification_level") == PREVIEW_ATTESTED
            and result.get("evidence_accounting_status")
            == "externally_attested_runtime_evidence"
            and result.get("external_evidence_id")
            == attestations[receipt_id].evidence_id
            and result.get("external_live_result_digest")
            == attestations[receipt_id].live_result_digest
            and result.get("external_verifier_workflow_run_id")
            == attestations[receipt_id].verifier_workflow_run_id
            and result.get("external_verified_at")
            == attestations[receipt_id].verified_at
            and result.get("source_commit") == expected_source_commit
            and result.get("workflow") == receipt.get("workflow")
            and result.get("case_kind") == receipt.get("case_kind"),
            "runtime_external_session_result_binding_mismatch",
            receipt_id,
        )
        result_by_id[receipt_id] = MappingProxyType(copy.deepcopy(dict(result)))
    require(
        set(result_by_id) == set(receipt_ids),
        "runtime_external_session_result_coverage",
        str(sorted(result_by_id)),
    )
    return ExternalRuntimeValidationSession(
        runtime_receipts_sha256=runtime_receipts_sha256,
        expected_source_commit=expected_source_commit,
        verification_level=PREVIEW_ATTESTED,
        provider_verified=False,
        adapter_id=expected_adapter_id,
        receipt_ids=tuple(sorted(str(item) for item in receipt_ids)),
        attestations=MappingProxyType(attestations),
        runtime_results=tuple(result_by_id[item] for item in sorted(result_by_id)),
        _capability=_EXTERNAL_RUNTIME_ATTESTATION_CAPABILITY,
    )


def _is_valid_external_runtime_validation_session(value: Any) -> bool:
    return (
        isinstance(value, ExternalRuntimeValidationSession)
        and value._capability is _EXTERNAL_RUNTIME_ATTESTATION_CAPABILITY
        and value.verification_level == PREVIEW_ATTESTED
        and value.provider_verified is False
        and value.adapter_id in SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS
        and len(value.receipt_ids) == 10
        and len(value.attestations) == 10
        and len(value.runtime_results) == 10
        and set(value.receipt_ids) == set(value.attestations)
        and all(
            _is_valid_external_runtime_attestation(item)
            for item in value.attestations.values()
        )
    )


def consume_external_runtime_validation_session(
    session: ExternalRuntimeValidationSession,
    *,
    collection: Mapping[str, Any],
    runtime_receipts_path: Path,
    expected_source_commit: str | None,
) -> list[dict[str, Any]]:
    """Consume an opaque session only for its exact frozen collection/commit."""

    require(
        _is_valid_external_runtime_validation_session(session),
        "runtime_external_session_invalid",
        type(session).__name__,
    )
    require(
        runtime_receipts_path.is_file()
        and sha256_file(runtime_receipts_path) == session.runtime_receipts_sha256,
        "runtime_external_session_collection_changed",
        str(runtime_receipts_path),
    )
    receipts = collection.get("receipts")
    receipt_ids = (
        [str(receipt.get("receipt_id")) for receipt in receipts]
        if isinstance(receipts, list)
        else []
    )
    require(
        tuple(sorted(receipt_ids)) == session.receipt_ids,
        "runtime_external_session_collection_mismatch",
        str(receipt_ids),
    )
    require(
        expected_source_commit == session.expected_source_commit,
        "runtime_external_session_release_commit_mismatch",
        f"session={session.expected_source_commit} ledger={expected_source_commit}",
    )
    return [copy.deepcopy(dict(item)) for item in session.runtime_results]


class _SyntheticAttestationCapability:
    """Unserializable capability for this module's reachability self-test only."""


_SYNTHETIC_ATTESTATION_CAPABILITY = _SyntheticAttestationCapability()


@dataclass(frozen=True)
class _TestOnlyAuthenticatedAttestation:
    """Authenticated-outcome simulation that cannot count as runtime evidence."""

    integrity_result: EvidenceValidationResult
    verification_level: str
    provider_verified: bool
    counts_as_preview_acceptance: bool
    counts_as_runtime_evidence: bool
    attestation_scope: str
    _capability: _SyntheticAttestationCapability

    @property
    def evidence_id(self) -> str:
        return self.integrity_result.evidence_id


def _issue_test_only_authenticated_attestation(
    integrity_result: EvidenceValidationResult,
    *,
    verification_level: str,
    capability: _SyntheticAttestationCapability,
) -> _TestOnlyAuthenticatedAttestation:
    require(
        capability is _SYNTHETIC_ATTESTATION_CAPABILITY,
        "synthetic_attestation_capability_invalid",
        "test-only attestation requires the private in-process capability",
    )
    require(
        integrity_result.integrity_valid
        and not integrity_result.gate_eligible
        and not integrity_result.provider_verified
        and not integrity_result.counts_as_preview_acceptance,
        "synthetic_attestation_integrity_boundary_invalid",
        "shared validation must remain integrity-only",
    )
    require(
        integrity_result.verification_level == verification_level
        and integrity_result.claimed_provider_verified
        is (verification_level == PROVIDER_VERIFIED),
        "synthetic_attestation_claim_mismatch",
        verification_level,
    )
    return _TestOnlyAuthenticatedAttestation(
        integrity_result=integrity_result,
        verification_level=verification_level,
        provider_verified=verification_level == PROVIDER_VERIFIED,
        counts_as_preview_acceptance=True,
        counts_as_runtime_evidence=False,
        attestation_scope="phase7_synthetic_reachability_self_test_only",
        _capability=capability,
    )


def _is_valid_test_only_attestation(
    value: Any,
) -> bool:
    return (
        isinstance(value, _TestOnlyAuthenticatedAttestation)
        and value._capability is _SYNTHETIC_ATTESTATION_CAPABILITY
        and value.attestation_scope
        == "phase7_synthetic_reachability_self_test_only"
        and value.counts_as_runtime_evidence is False
    )


class ModeViolation(AssertionError):
    """A stable, machine-readable mode replay failure."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise ModeViolation(code, message)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8-sig"))


def validate_polisher_routing_boundaries(
    fixture: dict[str, Any], registry: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require(fixture.get("schema_version") == 1, "polisher_routing_schema", "schema")
    require(
        fixture.get("evidence_class") == "synthetic_routing_boundary_contract"
        and fixture.get("runtime_claim") == "none",
        "polisher_routing_scope",
        "fixture cannot claim live routing",
    )
    entry = fixture.get("entry_skill")
    registered = {item.get("name") for item in registry.get("skills", [])}
    require(entry == "research-polisher-orchestrator", "polisher_routing_entry", str(entry))
    public_entry_policy = registry.get("public_entry_policy", {})
    implicit_entries = set(public_entry_policy.get("implicit_active_entries", []))
    explicit_only_route = public_entry_policy.get("explicit_only_entries", {}).get(
        entry, {}
    )
    require(
        entry not in implicit_entries
        and explicit_only_route
        == {
            "status": "explicit_only_personal_routing_policy",
            "change_authority": "owner_only",
        },
        "polisher_routing_gate",
        "Research Polisher must remain explicit-only under the personal routing policy",
    )
    cases = fixture.get("cases", [])
    require(isinstance(cases, list) and cases, "polisher_routing_cases", "missing")
    ids = [case.get("case_id") for case in cases]
    require(len(ids) == len(set(ids)), "polisher_routing_cases", "duplicate IDs")
    required_exclusions = {
        "language_polish",
        "ordinary_drafting",
        "new_idea_generation",
        "general_literature_search",
    }
    observed_exclusions: set[str] = set()
    positive_results: list[dict[str, Any]] = []
    negative_results: list[dict[str, Any]] = []

    def validate_case(case: dict[str, Any]) -> None:
        case_id = str(case.get("case_id"))
        prompt = case.get("prompt")
        route = case.get("observed_route")
        expected_route = case.get("expected_route")
        require(isinstance(prompt, str) and prompt.strip(), "polisher_routing_prompt", case_id)
        require(expected_route in registered, "polisher_routing_expected_route", case_id)
        if case.get("expected_selected") is True:
            require(f"${entry}" in prompt, "polisher_routing_explicit_invocation", case_id)
            require(route == entry, "polisher_routing_missed", case_id)
        else:
            require(route != entry, "polisher_routing_boundary_takeover", case_id)
        require(route == expected_route, "polisher_routing_disagreement", case_id)

    for case in cases:
        validate_case(case)
        if case.get("expected_selected") is False:
            observed_exclusions.add(str(case.get("request_class")))
        positive_results.append(
            {
                "case_id": case["case_id"],
                "request_class": case["request_class"],
                "status": "routed_as_expected",
                "observed_route": case["observed_route"],
            }
        )
        if case.get("expected_selected") is False:
            mutated = copy.deepcopy(case)
            mutated["observed_route"] = entry
            try:
                validate_case(mutated)
            except ModeViolation as exc:
                require(
                    exc.code == "polisher_routing_boundary_takeover",
                    "polisher_routing_negative_guard",
                    f"{case['case_id']}: {exc.code}",
                )
                negative_results.append(
                    {
                        "case_id": case["case_id"],
                        "mutation": "force_research_polisher_takeover",
                        "status": "rejected_as_expected",
                    }
                )
            else:
                raise ModeViolation("polisher_routing_negative_guard", case["case_id"])
    require(
        required_exclusions <= observed_exclusions,
        "polisher_routing_exclusion_coverage",
        str(sorted(required_exclusions - observed_exclusions)),
    )
    return positive_results, negative_results


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_repository_bytes(value: bytes) -> str:
    return sha256_bytes(value.replace(b"\r\n", b"\n"))


def sha256_repository_file(path: Path) -> str:
    """Hash a tracked contract independent of Git CRLF/LF checkout policy."""

    return sha256_repository_bytes(path.read_bytes())


def normalized_id(value: str) -> str:
    return value.replace("_", "-")


def registry_mode_pairs(registry: dict[str, Any], workflows: list[str]) -> list[tuple[str, str]]:
    machines = registry["workflow_state_machines"]
    return [
        (workflow, mode)
        for workflow in workflows
        for mode in machines[workflow]["entry_modes"]
    ]


def entry_gates_for(case: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    return list(
        registry["workflow_state_machines"][case["workflow"]]["entry_gates"][
            case["entry_mode"]
        ]
    )


def artifact_digest(artifact: dict[str, Any]) -> str:
    digest_input = {key: value for key, value in artifact.items() if key != "content_digest"}
    rendered = json.dumps(digest_input, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(rendered.encode("utf-8"))


def build_artifact(
    *,
    case: dict[str, Any],
    registry: dict[str, Any],
    artifact_id: str,
    version_id: str,
    artifact_role: str,
    source_skill: str,
    created_by_instance_id: str,
    based_on: list[str],
    change_type: str,
) -> dict[str, Any]:
    artifact = {
        "artifact_id": artifact_id,
        "version_id": version_id,
        "workflow_id": f"phase7-{case['case_id']}",
        "round_id": "round-001" if version_id == "v001" else "round-002",
        "plugin_version": registry["plugin_version"],
        "source_skill": source_skill,
        "created_by_instance_id": created_by_instance_id,
        "based_on": based_on,
        "change_type": change_type,
        "path": f"phase7/{case['case_id']}/{artifact_id}-{version_id}.yaml",
        "status": "frozen",
        "content_digest": "computed",
        "frozen": True,
        "artifact_role": artifact_role,
    }
    artifact["content_digest"] = artifact_digest(artifact)
    return artifact


def receipt_kind(gate: str) -> str:
    review_markers = ("passed", "evaluated", "review", "reports_complete", "audit")
    return "review_gate" if any(marker in gate for marker in review_markers) else "artifact_gate"


def decision_for(skill_name: str, category: str, registry: dict[str, Any]) -> str:
    contract = registry["scenario_eval_contract"]["review_decision_contracts"].get(
        skill_name
    )
    require(contract is not None, "review_decision_contract", skill_name)
    decisions = contract.get(category, [])
    require(bool(decisions), "review_decision_contract", f"{skill_name}: {category}")
    return decisions[0]


def build_review_receipt(
    *,
    case: dict[str, Any],
    registry: dict[str, Any],
    reviewer_skill: str,
    reviewer_instance_id: str,
    reviewer_role: str,
    review_scope: str,
    input_artifacts: list[dict[str, Any]],
    decision_category: str,
    receipt_suffix: str,
) -> dict[str, Any]:
    require(bool(input_artifacts), "review_inputs", f"{case['case_id']}: {receipt_suffix}")
    decision = decision_for(reviewer_skill, decision_category, registry)
    finding_id = f"{case['case_id']}-{receipt_suffix}-finding-001"
    findings = []
    unresolved_issues = []
    if decision_category == "revise":
        findings = [
            {
                "finding_id": finding_id,
                "severity": "major",
                "blocking": False,
                "status": "open",
                "summary": "Synthetic fixable finding used only for contract replay.",
            }
        ]
        unresolved_issues = [finding_id]
    receipt = {
        "review_id": f"{case['case_id']}-{receipt_suffix}-review",
        "reviewer_skill": reviewer_skill,
        "reviewer_instance_id": reviewer_instance_id,
        "reviewer_role": reviewer_role,
        "review_scope": review_scope,
        "workflow_id": f"phase7-{case['case_id']}",
        "round_id": input_artifacts[0]["round_id"],
        "input_artifact_ids": [artifact["artifact_id"] for artifact in input_artifacts],
        "input_versions": [artifact["version_id"] for artifact in input_artifacts],
        "input_digests": [artifact["content_digest"] for artifact in input_artifacts],
        "files_read": [artifact["path"] for artifact in input_artifacts],
        "isolation_mode": "fresh_subagent",
        "prior_scores_visible": False,
        "source_edits_performed": False,
        "decision": decision,
        "findings": findings,
        "unresolved_issues": unresolved_issues,
        "frozen": True,
    }
    if "panel" in reviewer_skill:
        receipt["peer_outputs_visible"] = False
    extension = registry["scenario_eval_contract"].get(
        "workflow_review_extensions", {}
    ).get(reviewer_skill)
    if extension is not None:
        require(
            len(input_artifacts) == extension["exact_input_artifact_count"],
            "review_extension_input_count",
            f"{case['case_id']}: {reviewer_skill}",
        )
        receipt.update(
            {
                "reviewed_dossier_digest": input_artifacts[0]["content_digest"],
                "complete_dossier_confirmed": True,
                "dossier_only_input_confirmed": True,
            }
        )
        for finding in receipt["findings"]:
            finding.setdefault("title", finding["summary"])
            finding.setdefault("dossier_locator", "Expected outputs and falsification criteria")
    return receipt


def validate_review_extension(
    *,
    payload: Mapping[str, Any],
    reviewer_skill: str,
    expected_artifacts: list[dict[str, Any]],
    registry: dict[str, Any],
    digest_field: str,
    error_code: str,
    label: str,
) -> None:
    extension = registry["scenario_eval_contract"].get(
        "workflow_review_extensions", {}
    ).get(reviewer_skill)
    if extension is None:
        return
    require(
        set(extension["required_fields"]) <= set(payload)
        and len(expected_artifacts) == extension["exact_input_artifact_count"]
        and all(
            artifact["artifact_role"]
            in set(extension["allowed_input_artifact_roles"])
            for artifact in expected_artifacts
        )
        and payload.get("reviewed_dossier_digest")
        == expected_artifacts[0][digest_field]
        and payload.get("complete_dossier_confirmed") is True
        and payload.get("dossier_only_input_confirmed") is True,
        error_code,
        label,
    )
    findings = payload.get("findings")
    require(isinstance(findings, list), error_code, label)
    required_finding_fields = set(extension["finding_required_fields"])
    require(
        all(
            isinstance(finding, Mapping)
            and required_finding_fields <= set(finding)
            and all(
                isinstance(finding[field], str) and bool(finding[field].strip())
                for field in required_finding_fields
            )
            for finding in findings
        ),
        error_code,
        label,
    )


def validate_review_receipt(
    *,
    receipt: dict[str, Any] | None,
    case: dict[str, Any],
    registry: dict[str, Any],
    expected_skill: str,
    expected_artifacts: list[dict[str, Any]],
    expected_category: str,
    missing_code: str,
    stale_code: str,
    writer_instance_id: str | None = None,
) -> None:
    require(receipt is not None, missing_code, case["case_id"])
    required = registry["scenario_eval_contract"]["required_review_fields"]
    missing = sorted(set(required) - set(receipt))
    require(not missing, "review_schema", f"{case['case_id']}: {missing}")
    skills = {skill["name"]: skill for skill in registry["skills"]}
    require(expected_skill in skills, "reviewer_skill_missing", expected_skill)
    require(
        skills[expected_skill]["requires_independent_subagent"] is True,
        "review_not_independent",
        expected_skill,
    )
    require(receipt["reviewer_skill"] == expected_skill, "review_identity", case["case_id"])
    require(
        receipt["workflow_id"] == f"phase7-{case['case_id']}",
        "review_identity",
        case["case_id"],
    )
    require(receipt["isolation_mode"] == "fresh_subagent", "review_not_independent", case["case_id"])
    require(receipt["prior_scores_visible"] is False, "prior_score_visible", case["case_id"])
    require(receipt["source_edits_performed"] is False, "source_edit_claim", case["case_id"])
    require(receipt["frozen"] is True, "review_schema", f"{case['case_id']}: frozen")
    expected_ids = [artifact["artifact_id"] for artifact in expected_artifacts]
    expected_versions = [artifact["version_id"] for artifact in expected_artifacts]
    expected_digests = [artifact["content_digest"] for artifact in expected_artifacts]
    require(receipt["input_artifact_ids"] == expected_ids, stale_code, f"{case['case_id']}: ids")
    require(receipt["input_versions"] == expected_versions, stale_code, f"{case['case_id']}: versions")
    require(receipt.get("input_digests") == expected_digests, stale_code, f"{case['case_id']}: digests")
    require(
        receipt["files_read"] == [artifact["path"] for artifact in expected_artifacts],
        "files_read_mismatch",
        case["case_id"],
    )
    validate_review_extension(
        payload=receipt,
        reviewer_skill=expected_skill,
        expected_artifacts=expected_artifacts,
        registry=registry,
        digest_field="content_digest",
        error_code="review_extension_invalid",
        label=f"{case['case_id']}: {expected_skill}",
    )
    contract = registry["scenario_eval_contract"]["review_decision_contracts"][
        expected_skill
    ]
    require(receipt["decision"] in contract["allowed"], "review_decision_invalid", case["case_id"])
    require(
        receipt["decision"] in contract[expected_category],
        "review_decision_category",
        case["case_id"],
    )
    if writer_instance_id is not None:
        require(
            receipt["reviewer_instance_id"] != writer_instance_id,
            "reviewer_writer_overlap",
            case["case_id"],
        )
    require(
        all(
            artifact["created_by_instance_id"] != receipt["reviewer_instance_id"]
            for artifact in expected_artifacts
        ),
        "reviewer_writer_overlap",
        case["case_id"],
    )


def build_runtime(case: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    machine = registry["workflow_state_machines"][case["workflow"]]
    primary_id = f"{case['case_id']}-primary-v001"
    primary = build_artifact(
        case=case,
        registry=registry,
        artifact_id=primary_id,
        version_id="v001",
        artifact_role=machine["primary_artifact_type"],
        source_skill="external-input",
        created_by_instance_id=f"fixture-user-{case['case_id']}",
        based_on=[],
        change_type="imported_for_mode_replay",
    )
    artifacts = {primary_id: primary}
    role_artifacts = {machine["primary_artifact_type"]: primary}
    receipts: dict[str, dict[str, Any]] = {}
    for gate in entry_gates_for(case, registry):
        gate_contract = (
            machine.get("scenario_entry_gate_contracts", {})
            .get(case["entry_mode"], {})
            .get(gate, {})
        )
        reviewer_skill = gate_contract.get("review_skill")
        if reviewer_skill:
            artifact_roles = list(gate_contract.get("input_artifact_roles", []))
        elif gate_contract.get("artifact_roles"):
            artifact_roles = list(gate_contract["artifact_roles"])
        elif "versioned" in gate or gate.startswith("latest_version_"):
            artifact_roles = [machine["primary_artifact_type"]]
        else:
            artifact_roles = [f"entry_gate_evidence:{gate}"]
        bound_artifacts = []
        for role in artifact_roles:
            bound = role_artifacts.get(role)
            if bound is None:
                artifact_id = f"{case['case_id']}-gate-{normalized_id(gate)}-{len(bound_artifacts) + 1:02d}"
                bound = build_artifact(
                    case=case,
                    registry=registry,
                    artifact_id=artifact_id,
                    version_id="v001",
                    artifact_role=role,
                    source_skill="external-input",
                    created_by_instance_id=f"fixture-user-{case['case_id']}",
                    based_on=[],
                    change_type="entry_gate_evidence_import",
                )
                artifacts[artifact_id] = bound
                role_artifacts[role] = bound
            bound_artifacts.append(bound)
        if reviewer_skill:
            receipt = build_review_receipt(
                case=case,
                registry=registry,
                reviewer_skill=reviewer_skill,
                reviewer_instance_id=(
                    f"{case['case_id']}-entry-{normalized_id(gate)}-reviewer-001"
                ),
                reviewer_role="entry_gate_reviewer",
                review_scope=f"entry_gate:{gate}",
                input_artifacts=bound_artifacts,
                decision_category="pass",
                receipt_suffix=f"entry-{normalized_id(gate)}",
            )
            receipt.update(
                {
                    "receipt_id": f"{case['case_id']}-{normalized_id(gate)}-receipt",
                    "gate": gate,
                    "receipt_kind": "review_gate",
                    "workflow": case["workflow"],
                    "entry_mode": case["entry_mode"],
                    "plugin_version": registry["plugin_version"],
                }
            )
        else:
            receipt = {
                "receipt_id": f"{case['case_id']}-{normalized_id(gate)}-receipt",
                "gate": gate,
                "receipt_kind": receipt_kind(gate),
                "workflow_id": f"phase7-{case['case_id']}",
                "workflow": case["workflow"],
                "entry_mode": case["entry_mode"],
                "plugin_version": registry["plugin_version"],
                "reviewer_skill": None,
                "input_artifact_ids": [artifact["artifact_id"] for artifact in bound_artifacts],
                "input_versions": [artifact["version_id"] for artifact in bound_artifacts],
                "input_digests": [artifact["content_digest"] for artifact in bound_artifacts],
                "decision": "pass",
                "frozen": True,
            }
        receipts[gate] = receipt
    return {
        "artifacts": artifacts,
        "entry_gate_receipts": receipts,
        "primary_artifact_id": primary_id,
    }


def validate_artifact(
    artifact: dict[str, Any], case: dict[str, Any], registry: dict[str, Any]
) -> None:
    required = registry["scenario_eval_contract"]["required_lineage_fields"] + ["artifact_role"]
    missing = sorted(set(required) - set(artifact))
    require(not missing, "invalid_lineage", f"{case['case_id']}: missing {missing}")
    require(
        artifact["workflow_id"] == f"phase7-{case['case_id']}",
        "invalid_lineage",
        f"{case['case_id']}: workflow_id",
    )
    require(
        artifact["plugin_version"] == registry["plugin_version"],
        "invalid_lineage",
        f"{case['case_id']}: plugin_version",
    )
    require(artifact["frozen"] is True, "invalid_lineage", f"{case['case_id']}: not frozen")
    require(artifact["status"] == "frozen", "invalid_lineage", f"{case['case_id']}: status")
    require(isinstance(artifact["based_on"], list), "invalid_lineage", f"{case['case_id']}: based_on")
    require(
        artifact["content_digest"] == artifact_digest(artifact),
        "invalid_lineage",
        f"{case['case_id']}: digest",
    )


def validate_entry_gates(
    case: dict[str, Any], runtime: dict[str, Any], registry: dict[str, Any]
) -> None:
    expected = entry_gates_for(case, registry)
    receipts = runtime["entry_gate_receipts"]
    missing = [gate for gate in expected if gate not in receipts]
    require(not missing, "missing_entry_gate_receipt", f"{case['case_id']}: {missing}")
    unexpected = sorted(set(receipts) - set(expected))
    require(not unexpected, "unexpected_entry_gate_receipt", f"{case['case_id']}: {unexpected}")
    for artifact in runtime["artifacts"].values():
        validate_artifact(artifact, case, registry)
    for gate in expected:
        receipt = receipts[gate]
        require(receipt["gate"] == gate, "gate_receipt_mismatch", f"{case['case_id']}: {gate}")
        require(
            receipt["workflow"] == case["workflow"]
            and receipt["entry_mode"] == case["entry_mode"],
            "gate_receipt_mismatch",
            f"{case['case_id']}: scope",
        )
        require(
            receipt["plugin_version"] == registry["plugin_version"],
            "gate_receipt_mismatch",
            f"{case['case_id']}: plugin_version",
        )
        input_ids = receipt["input_artifact_ids"]
        input_versions = receipt["input_versions"]
        input_digests = receipt["input_digests"]
        require(
            len(input_ids) == len(input_versions) == len(input_digests) and bool(input_ids),
            "gate_receipt_mismatch",
            f"{case['case_id']}: {gate} input lists",
        )
        bound_artifacts = []
        for artifact_id, version, digest in zip(input_ids, input_versions, input_digests):
            artifact = runtime["artifacts"].get(artifact_id)
            require(artifact is not None, "invalid_lineage", f"{case['case_id']}: dangling gate input")
            require(
                version == artifact["version_id"],
                "stale_gate_input",
                f"{case['case_id']}: {gate}",
            )
            require(
                digest == artifact["content_digest"],
                "stale_gate_input",
                f"{case['case_id']}: {gate} digest",
            )
            bound_artifacts.append(artifact)
        gate_contract = (
            registry["workflow_state_machines"][case["workflow"]]
            .get("scenario_entry_gate_contracts", {})
            .get(case["entry_mode"], {})
            .get(gate, {})
        )
        if gate_contract.get("artifact_roles"):
            require(
                [artifact["artifact_role"] for artifact in bound_artifacts]
                == gate_contract["artifact_roles"],
                "entry_gate_role_mismatch",
                f"{case['case_id']}: {gate}",
            )
        if gate_contract.get("review_skill"):
            reviewer_skill = gate_contract["review_skill"]
            require(receipt["reviewer_skill"] == reviewer_skill, "entry_gate_reviewer_mismatch", gate)
            require(
                [artifact["artifact_role"] for artifact in bound_artifacts]
                == gate_contract.get("input_artifact_roles", []),
                "entry_gate_role_mismatch",
                f"{case['case_id']}: {gate}",
            )
            validate_review_receipt(
                receipt=receipt,
                case=case,
                registry=registry,
                expected_skill=reviewer_skill,
                expected_artifacts=bound_artifacts,
                expected_category="pass",
                missing_code="missing_entry_gate_receipt",
                stale_code="stale_gate_input",
            )
        require(receipt["frozen"] is True, "gate_receipt_mismatch", f"{case['case_id']}: {gate}")


def workflow_profile(case: dict[str, Any], registry: dict[str, Any]) -> str:
    return registry["workflow_state_machines"][case["workflow"]].get(
        "workflow_profile", "default"
    )


def direction_profile_for(
    workflow: str,
    registry: dict[str, Any],
    declared_profile: str | None = None,
) -> str | None:
    """Resolve the internal Idea direction profile from registry contracts."""

    if workflow != "idea":
        require(
            declared_profile in {None, ""},
            "direction_profile_unexpected",
            f"{workflow}: {declared_profile}",
        )
        return None
    machine = registry["workflow_state_machines"][workflow]
    profiles = machine.get("internal_direction_profiles", {})
    default_profile = machine.get("routing_contract", {}).get(
        "clear_supported_direction"
    )
    selected = declared_profile or default_profile
    require(
        isinstance(profiles, dict)
        and bool(profiles)
        and isinstance(selected, str)
        and selected in profiles,
        "direction_profile_invalid",
        f"{workflow}: {selected}",
    )
    return selected


def workflow_conditions_for(
    workflow: str,
    registry: dict[str, Any],
    declared_conditions: Mapping[str, Any] | None = None,
    *,
    default_active: bool,
) -> dict[str, bool]:
    """Resolve package conditions declared by the workflow registry."""

    condition_names = {
        rule["required_when_condition"]
        for rule in registry["scenario_eval_contract"]["package_input_contracts"][
            workflow
        ]["required_inputs"]
        if isinstance(rule.get("required_when_condition"), str)
        and bool(rule["required_when_condition"])
    }
    declared = dict(declared_conditions or {})
    conditions: dict[str, bool] = {}
    for name in sorted(condition_names):
        value = declared.get(name, default_active)
        require(
            isinstance(value, bool),
            "workflow_condition_invalid",
            f"{workflow}: {name}={value}",
        )
        conditions[name] = value
    return conditions


def workflow_final_state_for(
    workflow: str,
    registry: dict[str, Any],
    direction_profile: str | None,
) -> str:
    """Return the base or direction-conditional terminal handoff state."""

    contract = registry["scenario_eval_contract"]
    expected = contract["workflow_final_states"][workflow]
    conditional = contract.get("workflow_conditional_final_states", {}).get(
        workflow, {}
    )
    if direction_profile in conditional:
        expected = conditional[direction_profile]
    if workflow == "idea":
        profile_contract = registry["workflow_state_machines"][workflow][
            "internal_direction_profiles"
        ][direction_profile]
        require(
            profile_contract.get("final_state") == expected,
            "direction_profile_final_state_mismatch",
            f"{direction_profile}: {profile_contract.get('final_state')} != {expected}",
        )
    return expected


def writer_skills_for(case: dict[str, Any], registry: dict[str, Any]) -> set[str]:
    machine = registry["workflow_state_machines"][case["workflow"]]
    candidates = set(machine.get("primary_writer_skills", []))
    if workflow_profile(case, registry) == "reviewer_matrix_assemble_evaluate":
        require(not candidates, "writer_skill_unexpected", case["case_id"])
        return candidates
    require(bool(candidates), "writer_skill_missing", case["case_id"])
    skills = {skill["name"]: skill for skill in registry["skills"]}
    require(
        all(
            name in skills and skills[name]["role"] in {"generator", "drafter"}
            for name in candidates
        ),
        "writer_skill_missing",
        case["case_id"],
    )
    return candidates


def writer_skill_for(case: dict[str, Any], registry: dict[str, Any]) -> str | None:
    candidates = writer_skills_for(case, registry)
    return sorted(candidates)[0] if candidates else None


def registered_panel_skill_for(
    workflow: str, registry: dict[str, Any], *, label: str
) -> str | None:
    candidates = {
        edge["destination"]
        for edge in registry["workflow_edges"]
        if edge["workflow"] == workflow and "panel" in edge["destination"]
    }
    require(len(candidates) <= 1, "panel_skill_missing", label)
    return next(iter(candidates), None)


def panel_required_for(
    workflow: str,
    registry: dict[str, Any],
    *,
    direction_profile: str | None,
    workflow_conditions: Mapping[str, bool],
) -> bool:
    machine = registry["workflow_state_machines"][workflow]
    required = bool(machine.get("post_evaluation_panel_required", True))
    if workflow == "idea":
        profile = machine["internal_direction_profiles"][direction_profile]
        requirement_fields = [
            value
            for key, value in profile.items()
            if key.startswith("adversarial_panel_required_")
        ]
        require(
            len(requirement_fields) == 1
            and isinstance(requirement_fields[0], bool),
            "panel_role_contract",
            str(direction_profile),
        )
        required = requirement_fields[0]
    panel_skill = registered_panel_skill_for(
        workflow, registry, label=f"{workflow}:panel-requirement"
    )
    panel_rules = [
        rule
        for rule in registry["scenario_eval_contract"]["package_input_contracts"][
            workflow
        ]["required_inputs"]
        if rule.get("artifact_role") == "panel_report"
        and (
            panel_skill is None
            or rule.get("source_skill") == panel_skill
        )
    ]
    for rule in panel_rules:
        condition = rule.get("required_when_condition")
        if condition is not None:
            require(
                condition in workflow_conditions,
                "workflow_condition_missing",
                f"{workflow}: {condition}",
            )
            required = required and workflow_conditions[condition]
    return required


def panel_skill_for(
    case: dict[str, Any],
    registry: dict[str, Any],
    *,
    direction_profile: str | None = None,
    workflow_conditions: Mapping[str, bool] | None = None,
) -> str | None:
    machine = registry["workflow_state_machines"][case["workflow"]]
    selected_profile = direction_profile_for(
        case["workflow"], registry, direction_profile
    )
    selected_conditions = workflow_conditions_for(
        case["workflow"],
        registry,
        workflow_conditions,
        default_active=True,
    )
    candidate = registered_panel_skill_for(
        case["workflow"], registry, label=case["case_id"]
    )
    if not panel_required_for(
        case["workflow"],
        registry,
        direction_profile=selected_profile,
        workflow_conditions=selected_conditions,
    ):
        if machine.get("post_evaluation_panel_required") is False:
            require(candidate is None, "panel_skill_unexpected", case["case_id"])
        return None
    require(candidate is not None, "panel_skill_missing", case["case_id"])
    return candidate


def ref_for(artifact: dict[str, Any]) -> str:
    return f"{artifact['artifact_id']}@{artifact['version_id']}"


def default_panel_roles(
    workflow: str,
    registry: dict[str, Any],
    *,
    direction_profile: str | None = None,
    workflow_conditions: Mapping[str, bool] | None = None,
) -> tuple[str, list[str]]:
    panel_contract = registry["scenario_eval_contract"]["panel_contracts"][workflow]
    tier = panel_contract["default_tier"]
    roles = list(panel_contract["tiers"][tier])
    selected_profile = direction_profile_for(workflow, registry, direction_profile)
    selected_conditions = workflow_conditions_for(
        workflow, registry, workflow_conditions, default_active=True
    )
    panel_required = panel_required_for(
        workflow,
        registry,
        direction_profile=selected_profile,
        workflow_conditions=selected_conditions,
    )
    require(
        len(roles) == len(set(roles)) and (bool(roles) or not panel_required),
        "panel_role_contract",
        workflow,
    )
    return tier, roles if panel_required else []


def package_rule_count_bounds(
    rule: dict[str, Any],
    *,
    direction_profile: str | None,
    current_idea_count: int,
    panel_role_count: int,
    workflow_conditions: Mapping[str, bool],
) -> tuple[int, int | None]:
    """Interpret one declarative package cardinality rule."""

    required_profile = rule.get("required_when_direction_profile")
    if required_profile is not None and required_profile != direction_profile:
        return 0, 0
    required_condition = rule.get("required_when_condition")
    if required_condition is not None:
        require(
            required_condition in workflow_conditions,
            "workflow_condition_missing",
            str(required_condition),
        )
        if not workflow_conditions[required_condition]:
            return 0, 0
    profile_counts = rule.get("count_by_direction_profile", {})
    if direction_profile in profile_counts:
        count_contract = profile_counts[direction_profile]
        if isinstance(count_contract, int) and not isinstance(count_contract, bool):
            return count_contract, count_contract
        require(
            isinstance(count_contract, dict)
            and isinstance(count_contract.get("minimum"), int)
            and not isinstance(count_contract.get("minimum"), bool)
            and isinstance(count_contract.get("maximum"), int)
            and not isinstance(count_contract.get("maximum"), bool)
            and 0 <= count_contract["minimum"] <= count_contract["maximum"],
            "package_count_contract_invalid",
            str(rule),
        )
        return count_contract["minimum"], count_contract["maximum"]
    if rule.get("count_per_current_idea_node") is not None:
        per_node = rule["count_per_current_idea_node"]
        require(
            isinstance(per_node, int) and not isinstance(per_node, bool) and per_node >= 0,
            "package_count_contract_invalid",
            str(rule),
        )
        expected = current_idea_count * per_node
        return expected, expected
    if rule.get("count_must_equal_current_idea_dossier_count"):
        return current_idea_count, current_idea_count
    if rule.get("count_from_panel_roles"):
        return panel_role_count, panel_role_count
    if "count" in rule:
        count = rule["count"]
        require(
            isinstance(count, int) and not isinstance(count, bool) and count >= 0,
            "package_count_contract_invalid",
            str(rule),
        )
        return count, count
    minimum = rule.get("minimum_count", 1)
    maximum = rule.get("maximum_count")
    require(
        isinstance(minimum, int)
        and not isinstance(minimum, bool)
        and minimum >= 0
        and (
            maximum is None
            or (
                isinstance(maximum, int)
                and not isinstance(maximum, bool)
                and maximum >= minimum
            )
        ),
        "package_count_contract_invalid",
        str(rule),
    )
    return minimum, maximum


def validate_adaptive_idea_registry_contract(
    registry: dict[str, Any],
) -> dict[str, Any]:
    """Validate the declarative focused/bounded Idea contract as one unit."""

    machine = registry["workflow_state_machines"]["idea"]
    contract = registry["scenario_eval_contract"]
    package_rules = {
        rule["artifact_role"]: rule
        for rule in contract["package_input_contracts"]["idea"]["required_inputs"]
    }
    focused = direction_profile_for("idea", registry, "focused_optimization")
    bounded = direction_profile_for("idea", registry, "bounded_exploration")
    focused_candidate = workflow_conditions_for(
        "idea",
        registry,
        {"proposal_handoff_candidate": True},
        default_active=False,
    )
    focused_no_candidate = workflow_conditions_for(
        "idea",
        registry,
        {"proposal_handoff_candidate": False},
        default_active=False,
    )
    require(
        panel_required_for(
            "idea",
            registry,
            direction_profile=focused,
            workflow_conditions=focused_candidate,
        )
        and not panel_required_for(
            "idea",
            registry,
            direction_profile=focused,
            workflow_conditions=focused_no_candidate,
        )
        and not panel_required_for(
            "idea",
            registry,
            direction_profile=bounded,
            workflow_conditions=focused_no_candidate,
        ),
        "adaptive_idea_panel_contract_invalid",
        "focused candidate / focused navigation / bounded exploration",
    )
    require(
        workflow_final_state_for("idea", registry, focused)
        == "human_signoff_required"
        and workflow_final_state_for("idea", registry, bounded)
        == "human_direction_selection_required",
        "adaptive_idea_final_state_contract_invalid",
        "direction-conditional terminal state",
    )

    panel_count = len(
        contract["panel_contracts"]["idea"]["tiers"]
        [contract["panel_contracts"]["idea"]["default_tier"]]
    )

    def bounds(
        role: str,
        *,
        profile: str,
        current_count: int,
        active_panel_count: int,
        conditions: Mapping[str, bool],
    ) -> tuple[int, int | None]:
        return package_rule_count_bounds(
            package_rules[role],
            direction_profile=profile,
            current_idea_count=current_count,
            panel_role_count=active_panel_count,
            workflow_conditions=conditions,
        )

    require(
        package_rules["idea_dossier"].get("current_by_idea_index") is True
        and bounds(
            "idea_dossier",
            profile=focused,
            current_count=1,
            active_panel_count=panel_count,
            conditions=focused_candidate,
        )
        == (1, 1)
        and bounds(
            "reference_ledger",
            profile=bounded,
            current_count=2,
            active_panel_count=0,
            conditions=focused_no_candidate,
        )
        == (2, 2)
        and bounds(
            "evaluation_report",
            profile=bounded,
            current_count=2,
            active_panel_count=0,
            conditions=focused_no_candidate,
        )
        == (2, 2)
        and bounds(
            "opportunity_map",
            profile=bounded,
            current_count=2,
            active_panel_count=0,
            conditions=focused_no_candidate,
        )
        == (2, 2)
        and bounds(
            "panel_report",
            profile=focused,
            current_count=1,
            active_panel_count=panel_count,
            conditions=focused_candidate,
        )
        == (panel_count, panel_count)
        and bounds(
            "panel_report",
            profile=focused,
            current_count=1,
            active_panel_count=0,
            conditions=focused_no_candidate,
        )
        == (0, 0)
        and bounds(
            "revision_plan",
            profile=bounded,
            current_count=2,
            active_panel_count=0,
            conditions=focused_no_candidate,
        )
        == (2, 3)
        and bounds(
            "revision_delta",
            profile=bounded,
            current_count=2,
            active_panel_count=0,
            conditions=focused_no_candidate,
        )
        == (4, 6),
        "adaptive_idea_package_count_contract_invalid",
        "focused/bounded package cardinalities",
    )
    extension = contract["workflow_review_extensions"]["idea-evaluator"]
    require(
        extension["exact_input_artifact_count"] == 1
        and extension["allowed_input_artifact_roles"] == ["idea_dossier"]
        and set(extension["required_fields"])
        == {
            "reviewed_dossier_digest",
            "complete_dossier_confirmed",
            "dossier_only_input_confirmed",
        }
        and set(extension["finding_required_fields"])
        == {"title", "dossier_locator"},
        "adaptive_idea_review_extension_contract_invalid",
        "idea-evaluator",
    )
    output_roles = contract["runtime_artifact_role_contract"][
        "actor_output_roles_by_skill"
    ]
    require(
        "proposed_navigation_metadata"
        in output_roles["multi-path-idea-generator"]
        and not {
            "idea_index",
            "reference_ledger",
        }.intersection(output_roles["multi-path-idea-generator"])
        and {"idea_index", "reference_ledger"}
        <= set(output_roles["research-idea-orchestrator"])
        and "proposed_navigation_metadata"
        not in output_roles["research-idea-orchestrator"],
        "adaptive_idea_metadata_ownership_invalid",
        "generator proposals / orchestrator authoritative metadata",
    )
    dispatch = machine["evaluation_dispatch_by_direction_profile"]
    handoff = machine["proposal_handoff_contract"]
    require(
        dispatch["bounded_exploration"].get(
            "initial_or_pre_remap_dossier_evaluation_forbidden"
        )
        is True
        and handoff["required_current_evaluation_decision"] == "promote"
        and handoff["fresh_evaluation_required"] is True
        and handoff["revise_then_promote_is_not_a_handoff_decision"] is True,
        "adaptive_idea_evaluation_route_contract_invalid",
        "bounded dispatch / proposal handoff",
    )
    return {
        "direction_profiles": [focused, bounded],
        "focused_panel_roles_when_candidate": panel_count,
        "bounded_revision_delta_bounds": [4, 6],
        "conditional_final_state": workflow_final_state_for(
            "idea", registry, bounded
        ),
    }


def package_rule_matches(
    artifacts: list[dict[str, Any]],
    rule: dict[str, Any],
    *,
    current_ref: str,
    current_idea_refs: set[str] | None = None,
) -> list[dict[str, Any]]:
    matches = [
        artifact
        for artifact in artifacts
        if artifact["artifact_role"] == rule["artifact_role"]
        and (
            "source_skill" not in rule
            or artifact["source_skill"] == rule["source_skill"]
        )
        and (
            "source_skills" not in rule
            or artifact["source_skill"] in set(rule["source_skills"])
        )
    ]
    if rule.get("current_primary"):
        matches = [artifact for artifact in matches if ref_for(artifact) == current_ref]
    if rule.get("current_by_idea_index"):
        require(
            current_idea_refs is not None,
            "package_current_idea_index_missing",
            str(rule),
        )
        matches = [
            artifact
            for artifact in matches
            if ref_for(artifact) in current_idea_refs
        ]
    if rule.get("current_primary_lineage"):
        expected_refs = current_idea_refs or {current_ref}
        matches = [
            artifact
            for artifact in matches
            if expected_refs.intersection(artifact["based_on"])
        ]
    if rule.get("selected_artifact_lineage_role"):
        selected_role = rule["selected_artifact_lineage_role"]
        selected_refs = {
            ref_for(artifact)
            for artifact in artifacts
            if artifact["artifact_role"] == selected_role
        }
        matches = [
            artifact
            for artifact in matches
            if selected_refs.intersection(artifact["based_on"])
        ]
    if rule.get("sealed_review_lineage"):
        review_refs = {
            ref_for(artifact)
            for artifact in artifacts
            if artifact["artifact_role"] in {"evaluation_report", "panel_report"}
        }
        matches = [
            artifact
            for artifact in matches
            if review_refs.intersection(artifact["based_on"])
        ]
    return matches


def ensure_synthetic_package_inputs(
    *,
    case: dict[str, Any],
    runtime: dict[str, Any],
    registry: dict[str, Any],
    current_artifact: dict[str, Any],
    panel_roles: list[str],
) -> list[dict[str, Any]]:
    contract = registry["scenario_eval_contract"]["package_input_contracts"][case["workflow"]]
    current_ref = ref_for(current_artifact)
    direction_profile = direction_profile_for(
        case["workflow"], registry, case.get("direction_profile")
    )
    workflow_conditions = workflow_conditions_for(
        case["workflow"],
        registry,
        case.get("workflow_conditions"),
        default_active=True,
    )
    current_idea_refs = {current_ref}
    selected: list[dict[str, Any]] = []
    for rule_index, rule in enumerate(contract["required_inputs"], start=1):
        artifacts = list(runtime["artifacts"].values())
        matches = package_rule_matches(
            artifacts,
            rule,
            current_ref=current_ref,
            current_idea_refs=current_idea_refs,
        )
        minimum_count, maximum_count = package_rule_count_bounds(
            rule,
            direction_profile=direction_profile,
            current_idea_count=len(current_idea_refs),
            panel_role_count=len(panel_roles),
            workflow_conditions=workflow_conditions,
        )
        while len(matches) < minimum_count:
            require(
                not rule.get("current_primary")
                and not rule.get("current_by_idea_index")
                and not rule.get("count_from_panel_roles")
                and not rule.get("count_must_equal_current_idea_dossier_count"),
                "package_required_input_missing",
                f"{case['case_id']}: {rule}",
            )
            source_skill = rule.get(
                "source_skill",
                next(
                    (
                        skill
                        for skill in rule.get("source_skills", [])
                        if skill != "external-input"
                    ),
                    registry["workflow_state_machines"][case["workflow"]]["orchestrator"],
                ),
            )
            parent_refs = [current_ref]
            selected_role = rule.get("selected_artifact_lineage_role")
            if selected_role:
                selected_parent = next(
                    (
                        artifact
                        for artifact in runtime["artifacts"].values()
                        if artifact["artifact_role"] == selected_role
                    ),
                    None,
                )
                require(selected_parent is not None, "package_required_input_missing", selected_role)
                parent_refs = [ref_for(selected_parent)]
            if rule.get("sealed_review_lineage"):
                parent_refs = [
                    ref_for(artifact)
                    for artifact in runtime["artifacts"].values()
                    if artifact["artifact_role"] in {"evaluation_report", "panel_report"}
                ]
            artifact_id = (
                f"{case['case_id']}-package-input-{rule_index:02d}-{len(matches) + 1:02d}"
            )
            created = build_artifact(
                case=case,
                registry=registry,
                artifact_id=artifact_id,
                version_id="v001",
                artifact_role=rule["artifact_role"],
                source_skill=source_skill,
                created_by_instance_id=f"{case['case_id']}-{normalized_id(source_skill)}-001",
                based_on=parent_refs,
                change_type="synthetic_required_package_input",
            )
            runtime["artifacts"][artifact_id] = created
            matches.append(created)
        require(
            maximum_count is None or len(matches) <= maximum_count,
            "package_required_input_count_invalid",
            f"{case['case_id']}: {rule}",
        )
        if rule.get("include_all_created") or rule.get("all_panel_instances"):
            chosen = matches
        else:
            chosen = matches[:minimum_count]
        selected.extend(chosen)
    deduplicated = {ref_for(artifact): artifact for artifact in selected}
    return list(deduplicated.values())


def validate_synthetic_package(
    *,
    case: dict[str, Any],
    runtime: dict[str, Any],
    registry: dict[str, Any],
    current_artifact: dict[str, Any],
    panel_roles: list[str],
    package_artifact: dict[str, Any],
    package_receipt: dict[str, Any],
) -> None:
    machine = registry["workflow_state_machines"][case["workflow"]]
    contract = registry["scenario_eval_contract"]["package_input_contracts"][case["workflow"]]
    direction_profile = direction_profile_for(
        case["workflow"], registry, case.get("direction_profile")
    )
    workflow_conditions = workflow_conditions_for(
        case["workflow"],
        registry,
        case.get("workflow_conditions"),
        default_active=True,
    )
    expected_final_state = workflow_final_state_for(
        case["workflow"], registry, direction_profile
    )
    expected_package_role = (
        "research_polisher_selection_dossier"
        if expected_final_state == "human_strategy_selection_required"
        else "final_handoff_package"
    )
    current_ref = ref_for(current_artifact)
    current_idea_refs = {current_ref}
    artifacts = list(runtime["artifacts"].values())
    for rule in contract["required_inputs"]:
        matches = package_rule_matches(
            artifacts,
            rule,
            current_ref=current_ref,
            current_idea_refs=current_idea_refs,
        )
        minimum_count, maximum_count = package_rule_count_bounds(
            rule,
            direction_profile=direction_profile,
            current_idea_count=len(current_idea_refs),
            panel_role_count=len(panel_roles),
            workflow_conditions=workflow_conditions,
        )
        require(
            len(matches) >= minimum_count
            and (maximum_count is None or len(matches) <= maximum_count),
            "package_required_input_missing",
            f"{case['case_id']}: {rule}",
        )
        if rule.get("current_by_idea_index"):
            require(
                {ref_for(artifact) for artifact in matches} == current_idea_refs,
                "package_current_idea_set_mismatch",
                case["case_id"],
            )
        if rule.get("all_panel_instances"):
            require(len(matches) == len(panel_roles), "package_panel_input_incomplete", case["case_id"])
    require(
        package_artifact["source_skill"] == machine["final_package_skill"]
        and package_artifact["artifact_role"] == expected_package_role
        and package_artifact["created_by_instance_id"] == package_receipt["package_instance_id"],
        "package_creator_invalid",
        case["case_id"],
    )
    require(
        package_receipt["package_artifact_ref"] == ref_for(package_artifact)
        and package_receipt["input_artifact_refs"] == package_artifact["based_on"]
        and package_receipt["source_edits_performed"] is False
        and package_receipt["final_state"] == expected_final_state,
        "package_receipt_invalid",
        case["case_id"],
    )


def lifecycle_match(
    state: str, transition: dict[str, str], registry: dict[str, Any]
) -> dict[str, Any]:
    matches = [
        item
        for item in registry["workflow_state_policy"]["lifecycle_transitions"]
        if item["to"] == transition["to"]
        and item["trigger"] == transition["trigger"]
        and item["from"] in {state, "*"}
    ]
    require(
        len(matches) == 1,
        "registry_lifecycle_mismatch",
        f"{state} --{transition['trigger']}--> {transition['to']}",
    )
    return matches[0]


def replay_case(
    case: dict[str, Any],
    runtime: dict[str, Any],
    fixture: dict[str, Any],
    registry: dict[str, Any],
    transition_receipt_mutation: str | None = None,
) -> dict[str, Any]:
    validate_entry_gates(case, runtime, registry)
    profile = fixture["path_profiles"][case["path_profile"]]
    machine = registry["workflow_state_machines"][case["workflow"]]
    profile_kind = workflow_profile(case, registry)
    is_reviewer_matrix = profile_kind == "reviewer_matrix_assemble_evaluate"
    direction_profile = direction_profile_for(
        case["workflow"], registry, case.get("direction_profile")
    )
    workflow_conditions = workflow_conditions_for(
        case["workflow"],
        registry,
        case.get("workflow_conditions"),
        default_active=True,
    )
    expected_final_state = workflow_final_state_for(
        case["workflow"], registry, direction_profile
    )
    state = "initialized"
    current_artifact = runtime["artifacts"][runtime["primary_artifact_id"]]
    latest_evaluated_version: str | None = None
    evaluator_instances: list[str] = []
    writer_instance = None if is_reviewer_matrix else f"{case['case_id']}-writer-001"
    writer_skill = writer_skill_for(case, registry)
    panel_skill = panel_skill_for(
        case,
        registry,
        direction_profile=direction_profile,
        workflow_conditions=workflow_conditions,
    )
    panel_tier, required_panel_roles = default_panel_roles(
        case["workflow"],
        registry,
        direction_profile=direction_profile,
        workflow_conditions=workflow_conditions,
    )
    skills = {skill["name"]: skill for skill in registry["skills"]}
    evaluator_skill = machine["evaluator_skill"]
    require(skills[evaluator_skill]["requires_independent_subagent"] is True, "review_not_independent", evaluator_skill)
    if panel_skill is not None:
        require(skills[panel_skill]["requires_independent_subagent"] is True, "review_not_independent", panel_skill)
    strategy_contract = (
        registry["scenario_eval_contract"]["review_group_contracts"][case["workflow"]]
        if is_reviewer_matrix
        else None
    )
    strategy_skill = strategy_contract["skill"] if strategy_contract else None
    if strategy_skill is not None:
        require(
            skills[strategy_skill]["requires_independent_subagent"] is True,
            "review_not_independent",
            strategy_skill,
        )
    artifact_creator_skill = (
        machine["primary_assembler_skill"] if is_reviewer_matrix else writer_skill
    )
    artifact_creator_instance = (
        f"{case['case_id']}-assembler-001" if is_reviewer_matrix else writer_instance
    )
    require(
        isinstance(artifact_creator_skill, str)
        and bool(artifact_creator_skill)
        and isinstance(artifact_creator_instance, str)
        and bool(artifact_creator_instance),
        "primary_artifact_creator_missing",
        case["case_id"],
    )
    panel_complete = False
    fatal_findings: list[str] = []
    pending_evaluator_instance: str | None = None
    evaluator_receipts: list[dict[str, Any]] = []
    panel_receipts: list[dict[str, Any]] = []
    mutation_applied = False
    transition_receipts: list[dict[str, Any]] = []
    generation_receipts: list[dict[str, Any]] = []
    package_receipts: list[dict[str, Any]] = []
    control_receipts: list[dict[str, Any]] = []
    panel_role_instances: dict[str, str] = {}
    strategy_role_instances: dict[str, str] = {}
    strategy_receipts: list[dict[str, Any]] = []
    for sequence, transition in enumerate(profile["transitions"], start=1):
        require(transition["from"] == state, "fixture_lifecycle_mismatch", case["case_id"])
        registry_transition = lifecycle_match(state, transition, registry)
        trigger = transition["trigger"]
        next_latest_evaluated_version = latest_evaluated_version
        next_panel_complete = panel_complete
        qualifying_receipt: dict[str, Any] | None = None

        if trigger == "versioned_artifact_created":
            prior = current_artifact
            if is_reviewer_matrix:
                require(strategy_contract is not None, "review_group_contract", case["case_id"])
                dossier = next(
                    (
                        artifact
                        for artifact in runtime["artifacts"].values()
                        if artifact["artifact_role"] == "research_polisher_dossier"
                    ),
                    None,
                )
                require(dossier is not None, "strategy_dossier_missing", case["case_id"])
                strategy_report_artifacts: list[dict[str, Any]] = []
                expected_roles = list(strategy_contract["roles"])
                expected_tiers = list(strategy_contract["effort_tiers"])
                for role_index, strategy_role in enumerate(expected_roles, start=1):
                    strategy_instance = f"{case['case_id']}-strategy-{role_index:03d}"
                    if (
                        transition_receipt_mutation == "duplicate_strategy_reviewer_instance"
                        and role_index == 2
                    ):
                        strategy_instance = f"{case['case_id']}-strategy-001"
                        mutation_applied = True
                    strategy_role_instances[strategy_role] = strategy_instance
                    strategy_receipt = build_review_receipt(
                        case=case,
                        registry=registry,
                        reviewer_skill=strategy_skill,
                        reviewer_instance_id=strategy_instance,
                        reviewer_role="independent_strategy_reviewer",
                        review_scope=f"research_polisher_lens:{strategy_role}",
                        input_artifacts=[dossier],
                        decision_category="pass",
                        receipt_suffix=f"strategy-{role_index:03d}",
                    )
                    strategy_receipt.update(
                        {
                            "strategy_role": strategy_role,
                            "effort_tiers": expected_tiers,
                            "matrix_cells": [
                                f"{strategy_role}:{tier}" for tier in expected_tiers
                            ],
                            "peer_outputs_visible": False,
                        }
                    )
                    if (
                        transition_receipt_mutation == "missing_strategy_reviewer_receipt"
                        and role_index == 1
                    ):
                        strategy_receipt = None
                        mutation_applied = True
                    elif (
                        transition_receipt_mutation == "stale_strategy_reviewer_receipt"
                        and role_index == 1
                    ):
                        strategy_receipt["input_digests"] = ["sha256:" + "0" * 64]
                        mutation_applied = True
                    validate_review_receipt(
                        receipt=strategy_receipt,
                        case=case,
                        registry=registry,
                        expected_skill=strategy_skill,
                        expected_artifacts=[dossier],
                        expected_category="pass",
                        missing_code="missing_strategy_reviewer_receipt",
                        stale_code="stale_strategy_reviewer_receipt",
                        writer_instance_id=artifact_creator_instance,
                    )
                    require(
                        strategy_receipt["peer_outputs_visible"] is False
                        and strategy_receipt["strategy_role"] == strategy_role
                        and strategy_receipt["effort_tiers"] == expected_tiers
                        and len(strategy_receipt["matrix_cells"]) == len(expected_tiers),
                        "strategy_review_group_contract",
                        case["case_id"],
                    )
                    strategy_report = build_artifact(
                        case=case,
                        registry=registry,
                        artifact_id=f"{case['case_id']}-strategy-report-{role_index:03d}",
                        version_id="v001",
                        artifact_role="research_polisher_strategy_report",
                        source_skill=strategy_skill,
                        created_by_instance_id=strategy_instance,
                        based_on=[ref_for(dossier)],
                        change_type=f"independent_strategy_review:{strategy_role}",
                    )
                    runtime["artifacts"][strategy_report["artifact_id"]] = strategy_report
                    strategy_report_artifacts.append(strategy_report)
                    strategy_receipts.append(strategy_receipt)
                require(
                    set(strategy_role_instances) == set(expected_roles)
                    and len(set(strategy_role_instances.values()))
                    == strategy_contract["required_instance_count"]
                    and sum(len(item["matrix_cells"]) for item in strategy_receipts)
                    == strategy_contract["required_matrix_cell_count"],
                    "strategy_review_group_contract",
                    case["case_id"],
                )
                manifest = build_artifact(
                    case=case,
                    registry=registry,
                    artifact_id=f"{case['case_id']}-strategy-report-manifest",
                    version_id="v001",
                    artifact_role=strategy_contract["manifest_artifact_role"],
                    source_skill=artifact_creator_skill,
                    created_by_instance_id=artifact_creator_instance,
                    based_on=[ref_for(artifact) for artifact in strategy_report_artifacts],
                    change_type="sealed_anonymous_strategy_report_manifest",
                )
                runtime["artifacts"][manifest["artifact_id"]] = manifest
                generated_id = f"{case['case_id']}-generated-primary"
                generated = build_artifact(
                    case=case,
                    registry=registry,
                    artifact_id=generated_id,
                    version_id="v001",
                    artifact_role=prior["artifact_role"],
                    source_skill=artifact_creator_skill,
                    created_by_instance_id=artifact_creator_instance,
                    based_on=[ref_for(manifest), ref_for(prior)],
                    change_type="anonymous_strategy_portfolio_assembly",
                )
                validate_artifact(generated, case, registry)
                runtime["artifacts"][generated_id] = generated
                current_artifact = generated
            else:
                existing_only_modes = {
                    "portfolio_only",
                    "package_only",
                    "submission_only",
                    "existing_draft",
                    "draft_and_external_review",
                }
                if case["entry_mode"] not in existing_only_modes:
                    generated_id = f"{case['case_id']}-generated-primary"
                    generated = build_artifact(
                        case=case,
                        registry=registry,
                        artifact_id=generated_id,
                        version_id="v001",
                        artifact_role=prior["artifact_role"],
                        source_skill=artifact_creator_skill,
                        created_by_instance_id=artifact_creator_instance,
                        based_on=[ref_for(prior)],
                        change_type="initial_generation",
                    )
                    validate_artifact(generated, case, registry)
                    runtime["artifacts"][generated_id] = generated
                    current_artifact = generated
            validate_artifact(current_artifact, case, registry)
            generation_receipt = {
                "receipt_id": f"{case['case_id']}-versioned-artifact-created",
                "trigger": trigger,
                "artifact_ref": ref_for(current_artifact),
                "artifact_digest": current_artifact["content_digest"],
                "source_skill": current_artifact["source_skill"],
                "frozen": current_artifact["frozen"],
            }
            require(
                generation_receipt["frozen"] is True
                and generation_receipt["artifact_digest"] == current_artifact["content_digest"],
                "generation_receipt_invalid",
                case["case_id"],
            )
            generation_receipts.append(generation_receipt)
        elif trigger == "new_version_created":
            parent = current_artifact
            revised_id = f"{case['case_id']}-primary-v002"
            revised = build_artifact(
                case=case,
                registry=registry,
                artifact_id=revised_id,
                version_id="v002",
                artifact_role=parent["artifact_role"],
                source_skill=artifact_creator_skill,
                created_by_instance_id=artifact_creator_instance,
                based_on=[f"{parent['artifact_id']}@{parent['version_id']}"],
                change_type="targeted_revision",
            )
            validate_artifact(revised, case, registry)
            require(
                revised["based_on"] == [f"{parent['artifact_id']}@{parent['version_id']}"],
                "invalid_lineage",
                f"{case['case_id']}: revision parent",
            )
            runtime["artifacts"][revised_id] = revised
            current_artifact = revised
            next_latest_evaluated_version = None
        elif trigger == "independent_review_dispatched":
            evaluator_instance = f"{case['case_id']}-evaluator-{len(evaluator_instances) + 1:03d}"
            require(evaluator_instance != artifact_creator_instance, "reviewer_writer_overlap", case["case_id"])
            require(
                evaluator_instance not in set(strategy_role_instances.values()),
                "reviewer_instance_reused",
                case["case_id"],
            )
            require(evaluator_instance not in evaluator_instances, "reviewer_instance_reused", case["case_id"])
            evaluator_instances.append(evaluator_instance)
            pending_evaluator_instance = evaluator_instance
        elif trigger == "fixable_revision_requested":
            require(
                pending_evaluator_instance is not None,
                "missing_evaluator_receipt",
                case["case_id"],
            )
            qualifying_receipt = build_review_receipt(
                case=case,
                registry=registry,
                reviewer_skill=evaluator_skill,
                reviewer_instance_id=pending_evaluator_instance,
                reviewer_role="independent_evaluator",
                review_scope="current_frozen_primary_artifact",
                input_artifacts=[current_artifact],
                decision_category="revise",
                receipt_suffix=f"evaluator-{len(evaluator_receipts) + 1:03d}",
            )
            validate_review_receipt(
                receipt=qualifying_receipt,
                case=case,
                registry=registry,
                expected_skill=evaluator_skill,
                expected_artifacts=[current_artifact],
                expected_category="revise",
                missing_code="missing_evaluator_receipt",
                stale_code="stale_evaluator_receipt",
                writer_instance_id=artifact_creator_instance,
            )
            review_artifact = build_artifact(
                case=case,
                registry=registry,
                artifact_id=f"{case['case_id']}-evaluation-{len(evaluator_receipts) + 1:03d}",
                version_id="v001",
                artifact_role="evaluation_report",
                source_skill=evaluator_skill,
                created_by_instance_id=pending_evaluator_instance,
                based_on=[ref_for(current_artifact)],
                change_type="independent_evaluation",
            )
            runtime["artifacts"][review_artifact["artifact_id"]] = review_artifact
        elif trigger in {"latest_version_accepted", "latest_strategy_portfolio_accepted"}:
            require(
                pending_evaluator_instance is not None,
                "missing_evaluator_receipt",
                case["case_id"],
            )
            qualifying_receipt = build_review_receipt(
                case=case,
                registry=registry,
                reviewer_skill=evaluator_skill,
                reviewer_instance_id=pending_evaluator_instance,
                reviewer_role="independent_evaluator",
                review_scope="current_frozen_primary_artifact",
                input_artifacts=[current_artifact],
                decision_category="pass",
                receipt_suffix=f"evaluator-{len(evaluator_receipts) + 1:03d}",
            )
            if transition_receipt_mutation == "missing_evaluator_receipt":
                qualifying_receipt = None
                mutation_applied = True
            elif transition_receipt_mutation == "stale_evaluator_receipt":
                qualifying_receipt["input_versions"] = ["v000"]
                mutation_applied = True
            validate_review_receipt(
                receipt=qualifying_receipt,
                case=case,
                registry=registry,
                expected_skill=evaluator_skill,
                expected_artifacts=[current_artifact],
                expected_category="pass",
                missing_code="missing_evaluator_receipt",
                stale_code="stale_evaluator_receipt",
                writer_instance_id=artifact_creator_instance,
            )
            review_artifact = build_artifact(
                case=case,
                registry=registry,
                artifact_id=f"{case['case_id']}-evaluation-{len(evaluator_receipts) + 1:03d}",
                version_id="v001",
                artifact_role="evaluation_report",
                source_skill=evaluator_skill,
                created_by_instance_id=pending_evaluator_instance,
                based_on=[ref_for(current_artifact)],
                change_type="fresh_independent_evaluation",
            )
            runtime["artifacts"][review_artifact["artifact_id"]] = review_artifact
            next_latest_evaluated_version = current_artifact["version_id"]
        elif trigger == "panel_gate_passed":
            require(
                panel_skill is not None and bool(required_panel_roles),
                "panel_skill_missing",
                case["case_id"],
            )
            current_panel_receipts: list[dict[str, Any]] = []
            for role_index, panel_role in enumerate(required_panel_roles, start=1):
                panel_instance = f"{case['case_id']}-panel-{role_index:03d}"
                require(panel_instance != artifact_creator_instance, "reviewer_writer_overlap", case["case_id"])
                require(panel_instance not in evaluator_instances, "reviewer_instance_reused", case["case_id"])
                panel_role_instances[panel_role] = panel_instance
                panel_receipt = build_review_receipt(
                    case=case,
                    registry=registry,
                    reviewer_skill=panel_skill,
                    reviewer_instance_id=panel_instance,
                    reviewer_role="independent_panel_role",
                    review_scope="current_frozen_primary_artifact",
                    input_artifacts=[current_artifact],
                    decision_category="pass",
                    receipt_suffix=f"panel-{role_index:03d}",
                )
                panel_receipt.update(
                    {
                        "panel_tier": panel_tier,
                        "panel_role": panel_role,
                        "dissent_ids": [],
                        "preserved_dissent_ids": [],
                    }
                )
                if transition_receipt_mutation == "missing_panel_receipt" and role_index == 1:
                    panel_receipt = None
                    mutation_applied = True
                elif transition_receipt_mutation == "stale_panel_receipt" and role_index == 1:
                    panel_receipt["input_digests"] = ["sha256:" + "0" * 64]
                    mutation_applied = True
                validate_review_receipt(
                    receipt=panel_receipt,
                    case=case,
                    registry=registry,
                    expected_skill=panel_skill,
                    expected_artifacts=[current_artifact],
                    expected_category="pass",
                    missing_code="missing_panel_receipt",
                    stale_code="stale_panel_receipt",
                    writer_instance_id=artifact_creator_instance,
                )
                require(
                    panel_receipt["peer_outputs_visible"] is False
                    and panel_receipt["preserved_dissent_ids"] == panel_receipt["dissent_ids"],
                    "panel_role_contract",
                    case["case_id"],
                )
                panel_artifact = build_artifact(
                    case=case,
                    registry=registry,
                    artifact_id=f"{case['case_id']}-panel-report-{role_index:03d}",
                    version_id="v001",
                    artifact_role="panel_report",
                    source_skill=panel_skill,
                    created_by_instance_id=panel_instance,
                    based_on=[ref_for(current_artifact)],
                    change_type=f"independent_panel_role:{panel_role}",
                )
                runtime["artifacts"][panel_artifact["artifact_id"]] = panel_artifact
                current_panel_receipts.append(panel_receipt)
            require(
                set(panel_role_instances) == set(required_panel_roles)
                and len(set(panel_role_instances.values())) == len(required_panel_roles),
                "panel_role_contract",
                case["case_id"],
            )
            panel_receipts.extend(current_panel_receipts)
            qualifying_receipt = {
                "review_id": f"{case['case_id']}-complete-panel",
                "panel_role_receipt_ids": [item["review_id"] for item in current_panel_receipts],
            }
            next_panel_complete = True
        elif trigger in {"package_verified", "selection_dossier_verified"}:
            package_inputs = ensure_synthetic_package_inputs(
                case=case,
                runtime=runtime,
                registry=registry,
                current_artifact=current_artifact,
                panel_roles=required_panel_roles,
            )
            package_instance = f"{case['case_id']}-final-package-001"
            package_artifact = build_artifact(
                case=case,
                registry=registry,
                artifact_id=f"{case['case_id']}-final-handoff-package",
                version_id="v001",
                artifact_role=(
                    "research_polisher_selection_dossier"
                    if trigger == "selection_dossier_verified"
                    else "final_handoff_package"
                ),
                source_skill=machine["final_package_skill"],
                created_by_instance_id=package_instance,
                based_on=[ref_for(artifact) for artifact in package_inputs],
                change_type=(
                    "verified_human_strategy_selection_packaging"
                    if trigger == "selection_dossier_verified"
                    else "verified_human_review_packaging"
                ),
            )
            runtime["artifacts"][package_artifact["artifact_id"]] = package_artifact
            package_receipt = {
                "receipt_id": f"{case['case_id']}-package-verification",
                "package_instance_id": package_instance,
                "package_artifact_ref": ref_for(package_artifact),
                "input_artifact_refs": list(package_artifact["based_on"]),
                "source_edits_performed": False,
                "final_state": expected_final_state,
            }
            validate_synthetic_package(
                case=case,
                runtime=runtime,
                registry=registry,
                current_artifact=current_artifact,
                panel_roles=required_panel_roles,
                package_artifact=package_artifact,
                package_receipt=package_receipt,
            )
            package_receipts.append(package_receipt)
        elif trigger == "unfixable_no_gain_or_user_stop":
            continuation = build_artifact(
                case=case,
                registry=registry,
                artifact_id=f"{case['case_id']}-continuation-brief",
                version_id="v001",
                artifact_role="continuation_brief",
                source_skill=registry["workflow_state_machines"][case["workflow"]]["orchestrator"],
                created_by_instance_id=f"{case['case_id']}-orchestrator-001",
                based_on=[ref_for(current_artifact)],
                change_type="valid_stop_continuation",
            )
            runtime["artifacts"][continuation["artifact_id"]] = continuation
            control_receipts.append(
                {
                    "receipt_id": f"{case['case_id']}-valid-stop",
                    "gate": "unfixable_no_gain_or_user_stop",
                    "finding": "mode_scope_completed_or_no_gain",
                    "route": "human_review_or_explicit_resume",
                    "continuation_artifact_ref": ref_for(continuation),
                }
            )

        checks = {
            "prior_panel_complete": next_panel_complete,
            "patch_scope_minor": False,
            "fresh_evaluation_current": next_latest_evaluated_version
            == current_artifact["version_id"],
            "no_unresolved_fatal_finding": not fatal_findings,
        }
        requirements = set(registry_transition.get("requires", []))
        unknown = requirements - set(checks)
        require(not unknown, "unknown_lifecycle_requirement", f"{case['case_id']}: {sorted(unknown)}")
        unmet = sorted(requirement for requirement in requirements if not checks[requirement])
        require(not unmet, "lifecycle_gate_bypass", f"{case['case_id']}: {unmet}")

        # Commit reviewer-derived state only after the receipt and every registry
        # prerequisite have been validated. Failed receipts cannot advance state.
        latest_evaluated_version = next_latest_evaluated_version
        panel_complete = next_panel_complete
        if qualifying_receipt is not None:
            if trigger in {
                "fixable_revision_requested",
                "latest_version_accepted",
                "latest_strategy_portfolio_accepted",
            }:
                evaluator_receipts.append(qualifying_receipt)
                pending_evaluator_instance = None
            elif trigger == "panel_gate_passed":
                pass

        previous = state
        state = transition["to"]
        transition_receipts.append(
            {
                "sequence": sequence,
                "from": previous,
                "to": state,
                "trigger": trigger,
                "current_primary_version": current_artifact["version_id"],
                "qualifying_review_id": (
                    qualifying_receipt["review_id"]
                    if qualifying_receipt is not None
                    else None
                ),
            }
        )

    require(
        transition_receipt_mutation is None or mutation_applied,
        "transition_mutation_not_applicable",
        f"{case['case_id']}: {transition_receipt_mutation}",
    )

    require(state == profile["expected_final_state"], "unexpected_final_state", case["case_id"])
    is_non_ready = case["entry_mode"] in machine.get("non_ready_modes", [])
    require(
        (state == "stopped") == is_non_ready,
        "non_ready_mode_contract",
        f"{case['case_id']}: {state}",
    )
    require(
        state
        != expected_final_state
        or latest_evaluated_version == current_artifact["version_id"],
        "stale_evaluation",
        case["case_id"],
    )
    require(not fatal_findings, "hidden_fatal_finding", case["case_id"])
    if state == expected_final_state:
        require(bool(evaluator_receipts), "missing_evaluator_receipt", case["case_id"])
        if panel_skill is not None:
            require(bool(panel_receipts), "missing_panel_receipt", case["case_id"])
            require(panel_complete is True, "missing_panel_receipt", case["case_id"])
        else:
            require(not panel_receipts, "panel_skill_unexpected", case["case_id"])
            require(
                strategy_contract is not None
                and len(strategy_receipts)
                == strategy_contract["required_instance_count"],
                "strategy_review_group_contract",
                case["case_id"],
            )
    return {
        "case_id": case["case_id"],
        "workflow": case["workflow"],
        "entry_mode": case["entry_mode"],
        "execution_kind": "deterministic_replay",
        "live_model_execution": False,
        "path_profile": case["path_profile"],
        "entry_gates_verified": entry_gates_for(case, registry),
        "entry_gate_contract_source": "workflow-registry.yaml",
        "entry_gate_receipt_count": len(runtime["entry_gate_receipts"]),
        "artifacts_validated": len(runtime["artifacts"]),
        "primary_versions": [
            artifact["version_id"]
            for artifact in runtime["artifacts"].values()
            if artifact["artifact_role"] == machine["primary_artifact_type"]
        ],
        "writer_skill": writer_skill,
        "writer_instance_id": writer_instance,
        "primary_artifact_creator_skill": artifact_creator_skill,
        "primary_artifact_creator_instance_id": artifact_creator_instance,
        "evaluator_skill": evaluator_skill,
        "evaluator_instance_ids": evaluator_instances,
        "synthetic_evaluator_receipt_ids": [
            receipt["review_id"] for receipt in evaluator_receipts
        ],
        "panel_skill": panel_skill,
        "synthetic_panel_receipt_ids": [
            receipt["review_id"] for receipt in panel_receipts
        ],
        "synthetic_panel_role_instances": panel_role_instances,
        "strategy_reviewer_skill": strategy_skill,
        "synthetic_strategy_reviewer_receipt_ids": [
            receipt["review_id"] for receipt in strategy_receipts
        ],
        "synthetic_strategy_role_instances": strategy_role_instances,
        "synthetic_generation_receipt_ids": [
            receipt["receipt_id"] for receipt in generation_receipts
        ],
        "synthetic_package_receipt_ids": [
            receipt["receipt_id"] for receipt in package_receipts
        ],
        "synthetic_control_receipts": control_receipts,
        "panel_dissent_preservation_contract_checked": bool(panel_receipts),
        "reviewer_receipts_are_synthetic": True,
        "transition_receipts": transition_receipts,
        "final_state": state,
        "mode_scope_completed": profile["mode_scope_completed"],
        "promotion_performed": state
        == expected_final_state,
        "automatic_external_submission": False,
    }


def mutate_runtime(
    runtime: dict[str, Any], case: dict[str, Any], registry: dict[str, Any], mutation: str
) -> str:
    gates = entry_gates_for(case, registry)
    target_gate = gates[0 if mutation == "gate_bypass" else -1]
    if mutation == "gate_bypass":
        runtime["entry_gate_receipts"].pop(target_gate)
        return "missing_entry_gate_receipt"
    receipt = runtime["entry_gate_receipts"][target_gate]
    if mutation == "stale_input":
        receipt["input_versions"][0] = "v000"
        return "stale_gate_input"
    if mutation == "invalid_lineage":
        runtime["artifacts"][receipt["input_artifact_ids"][0]]["workflow_id"] = "wrong-workflow-id"
        return "invalid_lineage"
    raise ModeViolation("unknown_mutation", mutation)


def expect_rejection(
    case: dict[str, Any], fixture: dict[str, Any], registry: dict[str, Any], mutation: str
) -> dict[str, Any]:
    runtime = copy.deepcopy(build_runtime(case, registry))
    expected_code = mutate_runtime(runtime, case, registry, mutation)
    mutation_id = f"{case['case_id']}-{mutation.replace('_', '-')}"
    try:
        replay_case(case, runtime, fixture, registry)
    except ModeViolation as exc:
        require(
            exc.code == expected_code,
            "negative_case_wrong_error",
            f"{mutation_id}: expected {expected_code}, got {exc.code}",
        )
        return {
            "mutation_id": mutation_id,
            "case_id": case["case_id"],
            "workflow": case["workflow"],
            "entry_mode": case["entry_mode"],
            "mutation": mutation,
            "guard_scope": "entry_gate_receipt_or_artifact_lineage",
            "status": "rejected_as_expected",
            "error_code": exc.code,
        }
    raise ModeViolation("negative_case_accepted", mutation_id)


def expect_transition_receipt_rejection(
    case: dict[str, Any],
    fixture: dict[str, Any],
    registry: dict[str, Any],
    mutation: str,
) -> dict[str, Any]:
    expected_codes = {
        "missing_evaluator_receipt": "missing_evaluator_receipt",
        "stale_evaluator_receipt": "stale_evaluator_receipt",
        "missing_panel_receipt": "missing_panel_receipt",
        "stale_panel_receipt": "stale_panel_receipt",
        "missing_strategy_reviewer_receipt": "missing_strategy_reviewer_receipt",
        "stale_strategy_reviewer_receipt": "stale_strategy_reviewer_receipt",
        "duplicate_strategy_reviewer_instance": "strategy_review_group_contract",
    }
    expected_code = expected_codes[mutation]
    mutation_id = f"{case['case_id']}-{mutation.replace('_', '-')}"
    try:
        replay_case(
            case,
            build_runtime(case, registry),
            fixture,
            registry,
            transition_receipt_mutation=mutation,
        )
    except ModeViolation as exc:
        require(
            exc.code == expected_code,
            "negative_case_wrong_error",
            f"{mutation_id}: expected {expected_code}, got {exc.code}",
        )
        return {
            "mutation_id": mutation_id,
            "case_id": case["case_id"],
            "workflow": case["workflow"],
            "entry_mode": case["entry_mode"],
            "mutation": mutation,
            "guard_scope": "lifecycle_qualifying_reviewer_receipt",
            "status": "rejected_as_expected",
            "error_code": exc.code,
        }
    raise ModeViolation("negative_case_accepted", mutation_id)


def validate_fixture(fixture: dict[str, Any], registry: dict[str, Any]) -> list[tuple[str, str]]:
    require(fixture.get("schema_version") == 2, "fixture_schema", "schema_version")
    require(fixture.get("execution_kind") == "deterministic_replay", "execution_kind", "fixture")
    require(fixture.get("live_model_execution") is False, "execution_kind", "live flag")
    require("not represent a" in fixture.get("notice", ""), "execution_notice", "missing live disclaimer")
    workflows = fixture["expected_workflows"]
    require(
        workflows == registry["scenario_eval_contract"]["required_workflows"],
        "workflow_coverage",
        "fixture/registry workflow order differs",
    )
    declared_pairs = registry_mode_pairs(registry, workflows)
    require(
        len(declared_pairs) == fixture["expected_mode_count"],
        "mode_count",
        f"registry={len(declared_pairs)} fixture={fixture['expected_mode_count']}",
    )
    case_pairs = [(case["workflow"], case["entry_mode"]) for case in fixture["cases"]]
    require(len(case_pairs) == len(set(case_pairs)), "duplicate_mode_case", str(case_pairs))
    require(case_pairs == declared_pairs, "mode_coverage", f"fixture={case_pairs}, registry={declared_pairs}")
    case_ids = [case["case_id"] for case in fixture["cases"]]
    require(len(case_ids) == len(set(case_ids)), "duplicate_case_id", str(case_ids))
    skills = {skill["name"]: skill for skill in registry["skills"]}

    for workflow in workflows:
        machine = registry["workflow_state_machines"][workflow]
        contracts = machine.get("scenario_entry_gate_contracts", {})
        require(
            list(contracts) == machine["entry_modes"],
            "entry_gate_contract_coverage",
            f"{workflow}: contracts={list(contracts)} modes={machine['entry_modes']}",
        )
        for mode in machine["entry_modes"]:
            mode_contracts = contracts[mode]
            declared_gates = machine["entry_gates"][mode]
            require(
                list(mode_contracts) == declared_gates,
                "entry_gate_contract_coverage",
                f"{workflow}/{mode}: contracts={list(mode_contracts)} gates={declared_gates}",
            )
            for gate, contract in mode_contracts.items():
                artifact_contract = bool(contract.get("artifact_roles"))
                reviewer_contract = bool(contract.get("review_skill")) and bool(
                    contract.get("input_artifact_roles")
                )
                require(
                    artifact_contract ^ reviewer_contract,
                    "entry_gate_contract",
                    f"{workflow}/{mode}/{gate}",
                )
                if reviewer_contract:
                    reviewer = contract["review_skill"]
                    require(reviewer in skills, "reviewer_skill_missing", reviewer)
                    require(
                        skills[reviewer]["requires_independent_subagent"] is True,
                        "review_not_independent",
                        reviewer,
                    )

    profiles = fixture["path_profiles"]
    for profile_name, profile in profiles.items():
        require(profile["mode_scope_completed"] is True, "path_profile", profile_name)
        state = "initialized"
        for transition in profile["transitions"]:
            require(transition["from"] == state, "fixture_lifecycle_mismatch", profile_name)
            lifecycle_match(state, transition, registry)
            state = transition["to"]
        require(state == profile["expected_final_state"], "path_profile", profile_name)

    for case in fixture["cases"]:
        machine = registry["workflow_state_machines"][case["workflow"]]
        require(
            "expected_entry_gates" not in case,
            "fixture_duplicates_registry_contract",
            f"{case['case_id']}: entry gates must be derived from workflow-registry.yaml",
        )
        require(case["path_profile"] in profiles, "path_profile", case["case_id"])
        is_non_ready = case["entry_mode"] in machine.get("non_ready_modes", [])
        non_ready_profiles = {
            "scoped_non_ready_delivery",
            "evaluated_scoped_non_ready_delivery",
        }
        require(
            (case["path_profile"] in non_ready_profiles) == is_non_ready,
            "non_ready_mode_contract",
            case["case_id"],
        )
        require(
            case["secondary_mutation"] in {"stale_input", "invalid_lineage"},
            "mutation_contract",
            case["case_id"],
        )
    return declared_pairs


def nested_value(value: dict[str, Any], dotted_path: str) -> Any:
    current: Any = value
    for key in dotted_path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def valid_commit_sha(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def valid_file_digest(value: Any) -> bool:
    return (
        isinstance(value, str)
        and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None
    )


def resolve_durable_file(
    binding: dict[str, Any], *, root: Path, label: str
) -> Path:
    path_value = binding.get("path")
    digest = binding.get("sha256")
    require(
        isinstance(path_value, str) and bool(path_value.strip()),
        "runtime_binding_missing",
        f"{label}.path",
    )
    require(valid_file_digest(digest), "runtime_binding_missing", f"{label}.sha256")
    require("\\" not in path_value, "runtime_path_not_canonical_posix", label)
    posix_relative = PurePosixPath(path_value)
    require(
        not posix_relative.is_absolute()
        and bool(posix_relative.parts)
        and "." not in posix_relative.parts
        and ".." not in posix_relative.parts,
        "runtime_path_not_durable",
        label,
    )
    relative = Path(*posix_relative.parts)
    resolved_root = root.resolve()
    resolved = (resolved_root / relative).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ModeViolation("runtime_path_not_durable", label) from exc
    require(resolved.is_file(), "runtime_bound_file_missing", f"{label}: {path_value}")
    require(sha256_file(resolved) == digest, "runtime_bound_file_digest_mismatch", label)
    return resolved


def load_structured_file(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    require(isinstance(value, dict), "runtime_bound_file_schema", str(path))
    return value


def current_idea_refs_from_index(
    *,
    artifacts: list[dict[str, Any]],
    artifacts_by_ref: Mapping[str, dict[str, Any]],
    resolved_artifact_paths: Mapping[str, Path],
    registry: dict[str, Any],
    direction_profile: str,
    label: str,
) -> set[str]:
    """Resolve and validate the exact current Idea dossier set."""

    indexes = [
        artifact for artifact in artifacts if artifact["artifact_role"] == "idea_index"
    ]
    require(len(indexes) == 1, "runtime_idea_index_missing", label)
    index = load_structured_file(resolved_artifact_paths[indexes[0]["path"]])
    nodes = index.get("current_nodes")
    require(
        index.get("schema_version") == 1
        and index.get("direction_profile") == direction_profile
        and isinstance(nodes, list)
        and bool(nodes),
        "runtime_idea_index_invalid",
        label,
    )
    dispatch_contract = registry["workflow_state_machines"]["idea"][
        "evaluation_dispatch_by_direction_profile"
    ][direction_profile]
    if dispatch_contract.get("initial_or_pre_remap_dossier_evaluation_forbidden"):
        require(
            index.get("overall_remap_status") == "complete"
            and all(node.get("remap_status") == "complete" for node in nodes),
            "runtime_bounded_evaluator_before_remap",
            label,
        )
    current_refs = [node.get("current_ref") for node in nodes if isinstance(node, dict)]
    require(
        len(current_refs) == len(nodes)
        and len(current_refs) == len(set(current_refs))
        and all(ref in artifacts_by_ref for ref in current_refs),
        "runtime_idea_index_invalid",
        label,
    )
    for node, current_ref in zip(nodes, current_refs):
        dossier = artifacts_by_ref[current_ref]
        require(
            dossier["artifact_role"] == "idea_dossier"
            and node.get("current_digest") == dossier["sha256"],
            "runtime_idea_index_digest_mismatch",
            f"{label}: {current_ref}",
        )
        if dispatch_contract.get("initial_or_pre_remap_dossier_evaluation_forbidden"):
            require(
                dossier.get("change_type") == "evidence_claim_sync",
                "runtime_bounded_evaluator_nonterminal_dossier",
                f"{label}: {current_ref}",
            )
    count_contract = registry["workflow_state_machines"]["idea"][
        "internal_direction_profiles"
    ][direction_profile]["current_dossier_count"]
    if isinstance(count_contract, int):
        minimum = maximum = count_contract
    else:
        minimum = count_contract["minimum"]
        maximum = count_contract["maximum"]
    require(
        minimum <= len(current_refs) <= maximum,
        "runtime_idea_direction_count_mismatch",
        f"{label}: {len(current_refs)}",
    )
    return set(current_refs)


def bounded_idea_evaluator_negative_self_tests(
    *, root: Path, registry: dict[str, Any]
) -> list[dict[str, Any]]:
    """Reject bounded evaluation before remap or on a nonterminal dossier."""

    evidence = root / "adaptive-idea"
    evidence.mkdir(parents=True, exist_ok=True)
    dossier_path = evidence / "dossier-v001.md"
    dossier_path.write_text(
        "synthetic bounded dossier\n", encoding="utf-8", newline="\n"
    )
    index_path = evidence / "idea-index.json"
    dossier = {
        "artifact_id": "bounded-dossier",
        "version_id": "v001",
        "artifact_role": "idea_dossier",
        "path": "adaptive-idea/dossier-v001.md",
        "sha256": sha256_file(dossier_path),
        "change_type": "create",
    }
    index_artifact = {
        "artifact_id": "bounded-index",
        "version_id": "v001",
        "artifact_role": "idea_index",
        "path": "adaptive-idea/idea-index.json",
    }
    artifacts = [dossier, index_artifact]
    artifacts_by_ref = {ref_for(dossier): dossier}
    resolved = {
        dossier["path"]: dossier_path,
        index_artifact["path"]: index_path,
    }
    valid_index = {
        "schema_version": 1,
        "direction_profile": "bounded_exploration",
        "overall_remap_status": "complete",
        "current_nodes": [
            {
                "node_id": "bounded-node-001",
                "current_ref": ref_for(dossier),
                "current_digest": dossier["sha256"],
                "remap_status": "complete",
            }
        ],
    }
    cases = [
        (
            "bounded_evaluator_before_remap",
            "runtime_bounded_evaluator_before_remap",
            {**valid_index, "overall_remap_status": "pending"},
            "evidence_claim_sync",
        ),
        (
            "bounded_evaluator_bound_to_initial_dossier",
            "runtime_bounded_evaluator_nonterminal_dossier",
            valid_index,
            "create",
        ),
    ]
    results: list[dict[str, Any]] = []
    for mutation, expected_code, index_document, change_type in cases:
        dossier["change_type"] = change_type
        write_json_file(index_path, index_document)
        try:
            current_idea_refs_from_index(
                artifacts=artifacts,
                artifacts_by_ref=artifacts_by_ref,
                resolved_artifact_paths=resolved,
                registry=registry,
                direction_profile="bounded_exploration",
                label=mutation,
            )
        except ModeViolation as exc:
            require(
                exc.code == expected_code,
                "runtime_negative_wrong_error",
                f"{mutation}: expected {expected_code}, got {exc.code}",
            )
            results.append(
                {
                    "mutation": mutation,
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation("runtime_negative_accepted", mutation)
    return results


def runtime_case_contract(
    schema: dict[str, Any], workflow: str, case_kind: str
) -> dict[str, Any]:
    contracts = schema.get("x-phase7-contract", {}).get(
        "workflow_case_contracts"
    )
    required_workflows = {
        "idea",
        "proposal",
        "article",
        "perspective",
        "research_polisher",
    }
    require(
        isinstance(contracts, dict) and set(contracts) == required_workflows,
        "runtime_schema_case_contract_invalid",
        "workflow coverage",
    )
    workflow_contract = contracts.get(workflow)
    require(
        isinstance(workflow_contract, dict)
        and set(workflow_contract) == {"happy", "control"},
        "runtime_schema_case_contract_invalid",
        f"{workflow}: case coverage",
    )
    contract = workflow_contract.get(case_kind)
    required_fields = {
        "expected_final_state",
        "input_condition",
        "gate",
        "route",
        "continuation_artifact_role",
        "required_review_skills",
        "required_strategy_matrix",
        "control_finding_decisions_by_skill",
        "control_finding_allowed_severities",
        "control_finding_blocking",
        "control_finding_resolved",
    }
    require(
        isinstance(contract, dict) and set(contract) == required_fields,
        "runtime_schema_case_contract_invalid",
        f"{workflow}/{case_kind}: fields",
    )
    if case_kind == "happy":
        expected_ready_state = (
            "human_strategy_selection_required"
            if workflow == "research_polisher"
            else "human_signoff_required"
        )
        require(
            contract["expected_final_state"] == expected_ready_state
            and all(
                contract[field] is None
                for field in (
                    "input_condition",
                    "gate",
                    "route",
                    "continuation_artifact_role",
                )
            )
            and isinstance(contract["required_review_skills"], list)
            and isinstance(contract["required_strategy_matrix"], bool)
            and contract["control_finding_decisions_by_skill"] == {}
            and contract["control_finding_allowed_severities"] == []
            and contract["control_finding_blocking"] is None
            and contract["control_finding_resolved"] is None,
            "runtime_schema_case_contract_invalid",
            f"{workflow}/{case_kind}: values",
        )
    else:
        require(
            contract["expected_final_state"]
            in {
                "stopped",
                "blocked",
                "independent_review_pending",
                "no_defensible_option",
            }
            and all(
                isinstance(contract[field], str) and bool(contract[field])
                for field in (
                    "input_condition",
                    "gate",
                    "route",
                    "continuation_artifact_role",
                )
            )
            and isinstance(contract["required_review_skills"], list)
            and bool(contract["required_review_skills"])
            and isinstance(contract["required_strategy_matrix"], bool)
            and isinstance(contract["control_finding_decisions_by_skill"], dict)
            and bool(contract["control_finding_decisions_by_skill"])
            and isinstance(contract["control_finding_allowed_severities"], list)
            and bool(contract["control_finding_allowed_severities"])
            and contract["control_finding_blocking"] is True
            and contract["control_finding_resolved"] is False,
            "runtime_schema_case_contract_invalid",
            f"{workflow}/{case_kind}: values",
        )
    expected_required_reviews = {
        ("idea", "happy"): [],
        ("idea", "control"): ["idea-evaluator"],
        ("proposal", "happy"): [],
        ("proposal", "control"): [
            "proposal-readiness-triage",
            "proposal-evaluator",
        ],
        ("article", "happy"): ["article-readiness-triage"],
        ("article", "control"): [
            "article-readiness-triage",
            "article-methods-statistics-auditor",
            "article-claim-auditor",
            "article-evaluator",
        ],
        ("perspective", "happy"): [],
        ("perspective", "control"): ["perspective-evaluator"],
        ("research_polisher", "happy"): [],
        ("research_polisher", "control"): [
            "research-polisher-methodology-publishability-reviewer"
        ],
    }
    expected_control_decisions = {
        "idea": {"idea-evaluator": ["keep_as_backup"]},
        "proposal": {
            "proposal-readiness-triage": ["not_proposalizable_yet"],
            "proposal-evaluator": ["reject"],
        },
        "article": {
            "article-readiness-triage": ["not_ready"],
            "article-methods-statistics-auditor": ["methodologically_blocked"],
            "article-claim-auditor": ["blocked"],
            "article-evaluator": ["reject"],
        },
        "perspective": {
            "perspective-evaluator": ["reject_not_salvageable"]
        },
        "research_polisher": {
            "research-polisher-methodology-publishability-reviewer": [
                "no_defensible_option"
            ]
        },
    }
    expected_control_severities = {
        "idea": {"major", "fatal"},
        "proposal": {"fatal"},
        "article": {"fatal"},
        "perspective": {"major", "fatal"},
        "research_polisher": {"major", "fatal"},
    }
    require(
        contract["required_review_skills"]
        == expected_required_reviews[(workflow, case_kind)]
        and contract["required_strategy_matrix"]
        is (workflow == "research_polisher")
        and (
            case_kind == "happy"
            or (
                contract["control_finding_decisions_by_skill"]
                == expected_control_decisions[workflow]
                and set(contract["control_finding_allowed_severities"])
                == expected_control_severities[workflow]
                and set(contract["control_finding_decisions_by_skill"])
                <= set(contract["required_review_skills"])
            )
        ),
        "runtime_schema_case_contract_invalid",
        f"{workflow}/{case_kind}: independent gates",
    )
    return contract


def validate_reviewer_unavailable_fault_injection(
    schema: dict[str, Any], registry: dict[str, Any]
) -> dict[str, Any]:
    """Keep reviewer-unavailable coverage separate from live control receipts."""

    contract = schema.get("x-phase7-contract", {}).get(
        "fault_injection_contracts", {}
    ).get("reviewer_unavailable")
    expected = {
        "input_condition": "injected_reviewer_delegation_unavailable",
        "gate": "required_reviewer_unavailable",
        "expected_final_state": "independent_review_pending",
        "route": "resume_in_fresh_delegated_task",
        "counts_as_live_control": False,
    }
    require(
        contract == expected,
        "reviewer_unavailable_fault_contract",
        str(contract),
    )
    transitions = registry.get("workflow_state_policy", {}).get(
        "lifecycle_transitions", []
    )
    require(
        any(
            transition.get("from") == "*"
            and transition.get("to") == contract["expected_final_state"]
            and transition.get("trigger") == contract["gate"]
            for transition in transitions
        ),
        "reviewer_unavailable_fault_route",
        str(contract),
    )
    return {
        "status": "passed",
        "fault": "reviewer_unavailable",
        "derived_state": contract["expected_final_state"],
        "route": contract["route"],
        "counts_as_live_control": False,
    }


def validate_runtime_receipt_declaration(
    receipt: dict[str, Any], schema: dict[str, Any], registry: dict[str, Any]
) -> dict[str, Any]:
    contract = runtime_case_contract(
        schema, receipt.get("workflow"), receipt.get("case_kind")
    )
    machine_modes = {
        "idea": {"standard", "resume_candidates", "portfolio_only"},
        "proposal": {"standard", "existing_draft", "draft_and_external_review", "package_only"},
        "article": {"standard", "fast_track_draft", "fast_track_draft_and_evaluation", "blueprint_only", "section_specific", "submission_only"},
        "perspective": {"lite", "standard", "full"},
        "research_polisher": {"standard"},
    }
    require(
        receipt.get("entry_mode") in machine_modes.get(receipt.get("workflow"), set()),
        "runtime_entry_mode_invalid",
        str(receipt.get("receipt_id")),
    )
    task_binding = receipt.get("binding", {}).get("task_export", {})
    require(
        task_binding.get("entry_mode") == receipt.get("entry_mode"),
        "runtime_entry_mode_binding_mismatch",
        str(receipt.get("receipt_id")),
    )
    direction_profile = direction_profile_for(
        receipt.get("workflow"), registry, receipt.get("direction_profile")
    )
    expected_final_state = (
        workflow_final_state_for(receipt["workflow"], registry, direction_profile)
        if receipt.get("case_kind") == "happy"
        else contract["expected_final_state"]
    )
    require(
        receipt.get("expected_final_state") == expected_final_state,
        "runtime_expected_state_contract_mismatch",
        str(receipt.get("receipt_id")),
    )
    control_evidence = receipt.get("control_evidence")
    require(
        isinstance(control_evidence, dict),
        "runtime_control_contract",
        str(receipt.get("receipt_id")),
    )
    if receipt.get("case_kind") == "happy":
        require(
            control_evidence.get("input_condition") is None
            and control_evidence.get("gate") is None
            and control_evidence.get("route") is None,
            "runtime_happy_control_evidence_present",
            str(receipt.get("receipt_id")),
        )
    else:
        require(
            control_evidence.get("input_condition")
            == contract["input_condition"],
            "runtime_control_input_condition_mismatch",
            str(receipt.get("receipt_id")),
        )
        require(
            control_evidence.get("gate") == contract["gate"],
            "runtime_control_gate_mismatch",
            str(receipt.get("receipt_id")),
        )
        require(
            control_evidence.get("route") == contract["route"],
            "runtime_control_route_mismatch",
            str(receipt.get("receipt_id")),
        )
    return contract


def runtime_actor_role_contract(
    registry: dict[str, Any], schema: dict[str, Any]
) -> dict[str, Any]:
    contract = registry.get("scenario_eval_contract", {}).get(
        "runtime_actor_role_contract"
    )
    require(
        isinstance(contract, dict),
        "runtime_actor_role_contract_invalid",
        "registry contract missing",
    )
    allowed_roles = contract.get("allowed_roles")
    mapping = contract.get("registry_roles_by_actor_role")
    finalizer_roles = contract.get("finalizer_roles")
    happy_required_roles = contract.get("happy_required_roles")
    happy_roles_by_profile = contract.get("happy_required_roles_by_workflow_profile")
    edge_derived_roles = contract.get("edge_derived_roles")
    independent_reviewer_roles = contract.get("independent_reviewer_actor_roles")
    independent_reviewer_isolation = contract.get(
        "independent_reviewer_isolation_mode"
    )
    edge_provenance_roles = contract.get("edge_provenance_required_actor_roles")
    edge_provenance_fields = contract.get("edge_provenance_required_fields")
    require(
        isinstance(allowed_roles, list)
        and bool(allowed_roles)
        and len(allowed_roles) == len(set(allowed_roles))
        and isinstance(mapping, dict)
        and set(mapping) == set(allowed_roles)
        and all(
            isinstance(registry_roles, list)
            and bool(registry_roles)
            and all(isinstance(role, str) and role for role in registry_roles)
            for registry_roles in mapping.values()
        )
        and isinstance(finalizer_roles, list)
        and set(finalizer_roles) == {"assembler", "verifier_compositor"}
        and isinstance(happy_required_roles, list)
        and set(happy_required_roles)
        == {"orchestrator", "writer", "evaluator", "panel"}
        and isinstance(happy_roles_by_profile, dict)
        and set(happy_roles_by_profile)
        == {"default", "reviewer_matrix_assemble_evaluate"}
        and happy_roles_by_profile["default"] == happy_required_roles
        and set(happy_roles_by_profile["reviewer_matrix_assemble_evaluate"])
        == {"orchestrator", "strategy_reviewer", "assembler", "evaluator"}
        and edge_derived_roles
        == {
            "supporting_reviewer": {
                "registry_role": "reviewer",
                "dispatch_mode": "delegated",
                "requires_independent_subagent": True,
                "isolation_mode": "fresh_subagent",
                "exclude_designated_reviewer_slots": True,
            },
            "supporting_writer": {
                "registry_role": "drafter",
                "dispatch_mode": "orchestrated",
                "exclude_primary_writer_skills": True,
            },
        }
        and set(independent_reviewer_roles or [])
        == {
            "evaluator",
            "panel",
            "strategy_reviewer",
            "supporting_reviewer",
            "verifier_compositor",
        }
        and independent_reviewer_isolation == "fresh_subagent"
        and set(edge_provenance_roles or []) == set(allowed_roles) - {"orchestrator"}
        and edge_provenance_fields
        == ["dispatch_source", "dispatch_mode", "dispatch_trigger"]
        and contract.get("root_actor_role") == "orchestrator"
        and contract.get("unknown_roles_rejected") is True
        and contract.get("registry_role_mapping_enforced") is True
        and contract.get("orchestrator_skill_must_match_workflow") is True,
        "runtime_actor_role_contract_invalid",
        "registry values",
    )
    schema_roles = schema.get("x-phase7-contract", {}).get(
        "verified_actor_roles"
    )
    require(
        isinstance(schema_roles, list)
        and set(schema_roles) == set(allowed_roles),
        "runtime_actor_role_contract_invalid",
        "schema/registry role mismatch",
    )
    schema_actor_contract = schema.get("x-phase7-contract", {}).get(
        "actor_manifest_contract", {}
    )
    require(
        all(
            schema_actor_contract.get(field) is True
            for field in (
                "unknown_actor_roles_rejected",
                "actor_role_must_match_registry_skill_role",
                "workflow_orchestrator_actor_required",
                "workflow_orchestrator_skill_matches_registry",
                "finalizer_role_matches_registry_final_package_skill",
                "artifact_creator_reviewer_finalizer_ids_pairwise_disjoint",
                "strategy_reviewer_roles_exactly_match_registry_review_group",
                "supporting_actor_membership_derived_from_workflow_edges",
            )
        ),
        "runtime_actor_role_contract_invalid",
        "schema actor-role flags",
    )
    require(
        schema_actor_contract.get("panel_actor_required_fields")
        == ["panel_tier", "panel_role"]
        and schema_actor_contract.get("strategy_reviewer_actor_required_fields")
        == ["strategy_role"]
        and schema_actor_contract.get("supporting_reviewer_actor_required_fields")
        == [
            "round_id",
            "isolation_mode",
            "dispatch_source",
            "dispatch_mode",
            "dispatch_trigger",
        ]
        and schema_actor_contract.get("supporting_writer_actor_required_fields")
        == ["dispatch_source", "dispatch_mode", "dispatch_trigger"]
        and schema_actor_contract.get("supporting_reviewer_isolation_mode")
        == "fresh_subagent"
        and schema_actor_contract.get("independent_reviewer_actor_required_fields")
        == ["round_id", "isolation_mode"]
        and set(schema_actor_contract.get("independent_reviewer_actor_roles", []))
        == set(independent_reviewer_roles)
        and schema_actor_contract.get("independent_reviewer_isolation_mode")
        == independent_reviewer_isolation,
        "runtime_actor_role_contract_invalid",
        "schema role-specific fields",
    )
    require(
        set(schema_actor_contract.get("edge_provenance_required_actor_roles", []))
        == set(edge_provenance_roles)
        and schema_actor_contract.get("edge_provenance_required_fields")
        == edge_provenance_fields
        and schema_actor_contract.get("root_actor_role") == "orchestrator",
        "runtime_actor_role_contract_invalid",
        "schema edge provenance",
    )
    schema_access = schema.get("x-phase7-contract", {}).get(
        "reviewer_access_contract", {}
    )
    registry_blindness = registry.get("scenario_eval_contract", {}).get(
        "blindness_policy", {}
    )
    expected_blind_roles = {
        "evaluator",
        "panel",
        "strategy_reviewer",
        "supporting_reviewer",
    }
    expected_oracle_roles = {
        "answer_key",
        "expected_decision",
        "expected_findings",
        "expected_score",
        "result_oracle",
        "review_oracle",
    }
    require(
        schema_access.get("evaluator_prior_scores_visible") is False
        and schema_access.get("evaluator_may_read_prior_reviewer_outputs")
        is False
        and set(schema_access.get("evaluator_forbidden_source_actor_roles", []))
        == set(
            registry_blindness.get(
                "runtime_evaluator_forbidden_source_actor_roles", []
            )
        )
        == {
            "evaluator",
            "panel",
            "strategy_reviewer",
            "supporting_reviewer",
            "verifier_compositor",
        }
        and registry_blindness.get("evaluator_prior_scores_visible") is False
        and registry_blindness.get("evaluator_may_read_prior_reviewer_outputs")
        is False
        and set(schema_access.get("blind_reviewer_actor_roles", []))
        == set(registry_blindness.get("runtime_blind_reviewer_actor_roles", []))
        == expected_blind_roles
        and set(schema_access.get("forbidden_oracle_artifact_roles", []))
        == set(
            registry_blindness.get("runtime_forbidden_oracle_artifact_roles", [])
        )
        == expected_oracle_roles
        and schema_access.get("blind_reviewer_inputs_must_be_indexed_artifacts")
        is True,
        "runtime_reviewer_access_contract_invalid",
        "schema/registry blindness mismatch",
    )
    schema_report = schema.get("x-phase7-contract", {}).get(
        "runtime_review_report_contract", {}
    )
    registry_report = registry.get("scenario_eval_contract", {}).get(
        "runtime_artifact_role_contract", {}
    ).get("runtime_review_report_contract", {})
    require(
        schema_report.get("required_fields") == registry_report.get("required_fields")
        and schema_report.get("finding_required_fields")
        == registry_report.get("finding_required_fields")
        and set(schema_report.get("allowed_severities", []))
        == set(registry_report.get("allowed_severities", []))
        and schema_report.get("finding_indexes_are_derived_bidirectionally")
        is True
        and schema_report.get("decision_vocabulary_is_registry_fail_closed")
        is True
        and schema_report.get("ready_qualifying_reviewer_decisions_must_pass")
        is True
        and schema_report.get("one_review_report_per_actor")
        is registry_report.get("one_review_report_per_actor")
        is True
        and schema_report.get(
            "pass_decision_requires_no_unresolved_blocking_findings"
        )
        is registry_report.get(
            "pass_decision_requires_no_unresolved_blocking_findings"
        )
        is True
        and schema_report.get(
            "review_input_refs_must_equal_actual_read_artifact_refs"
        )
        is registry_report.get(
            "review_input_refs_must_equal_actual_read_artifact_refs"
        )
        is True,
        "runtime_reviewer_access_contract_invalid",
        "schema/registry report contract mismatch",
    )
    schema_external = schema.get("x-phase7-contract", {}).get(
        "external_input_contract", {}
    )
    registry_external = registry.get("scenario_eval_contract", {}).get(
        "runtime_artifact_role_contract", {}
    ).get("external_input_contract", {})
    require(
        all(
            schema_external.get(field) == registry_external.get(field)
            for field in (
                "creator_sentinel",
                "source_skill_sentinel",
                "source_identity_field",
                "source_identity_prefix",
            )
        )
        and all(
            schema_external.get(field) is True
            for field in (
                "workflow_and_entry_mode_allowlist_required",
                "generated_or_review_artifact_impersonation_rejected",
                "current_primary_external_only_in_declared_modes",
            )
        )
        and all(
            value is True
            for value in schema.get("x-phase7-contract", {})
            .get("primary_lineage_contract", {})
            .values()
        ),
        "runtime_actor_role_contract_invalid",
        "schema external/primary lineage contract",
    )
    return contract


def edge_derived_actor_edges(
    registry: dict[str, Any], workflow: str, actor_role: str
) -> set[tuple[str, str, str, str]]:
    """Return exact registered dispatch edges allowed for a supporting actor."""

    role_contract = registry["scenario_eval_contract"]["runtime_actor_role_contract"]
    edge_contract = role_contract.get("edge_derived_roles", {}).get(actor_role)
    require(
        actor_role in {"supporting_reviewer", "supporting_writer"}
        and isinstance(edge_contract, dict),
        "runtime_actor_role_contract_invalid",
        f"edge-derived role: {actor_role}",
    )
    machine = registry["workflow_state_machines"].get(workflow)
    require(
        isinstance(machine, dict),
        "runtime_actor_role_contract_invalid",
        f"unknown workflow: {workflow}",
    )
    skill_contracts = {skill["name"]: skill for skill in registry["skills"]}
    excluded_skills: set[str] = set()
    if actor_role == "supporting_reviewer":
        excluded_skills.update(
            {
                machine["evaluator_skill"],
                machine["final_package_skill"],
            }
        )
        panel_skill = panel_skill_for(
            {"workflow": workflow, "case_id": f"{workflow}:supporting-reviewer"},
            registry,
        )
        if panel_skill is not None:
            excluded_skills.add(panel_skill)
        review_group = (
            registry["scenario_eval_contract"]
            .get("review_group_contracts", {})
            .get(workflow)
        )
        if review_group:
            excluded_skills.add(review_group["skill"])
    else:
        excluded_skills.update(machine.get("primary_writer_skills", []))

    allowed: set[tuple[str, str, str, str]] = set()
    for edge in registry["workflow_edges"]:
        if edge["workflow"] != workflow:
            continue
        destination = edge["destination"]
        skill = skill_contracts.get(destination)
        if (
            skill is None
            or skill["role"] != edge_contract["registry_role"]
            or edge["dispatch_mode"] != edge_contract["dispatch_mode"]
            or destination in excluded_skills
        ):
            continue
        if actor_role == "supporting_reviewer" and (
            skill["requires_independent_subagent"] is not True
        ):
            continue
        allowed.add(
            (
                edge["source"],
                destination,
                edge["dispatch_mode"],
                edge["trigger"],
            )
        )
    return allowed


def runtime_artifact_role_contract(registry: dict[str, Any]) -> dict[str, Any]:
    """Validate role-specific report, assembler, and finding-index allowlists."""

    scenario_contract = registry.get("scenario_eval_contract", {})
    contract = scenario_contract.get("runtime_artifact_role_contract")
    require(
        isinstance(contract, dict)
        and set(contract)
        == {
            "review_output_roles",
            "assembler_outputs_by_skill",
            "supporting_writer_outputs_by_skill",
            "research_polisher_review_outputs_by_actor_role_and_skill",
            "research_polisher_strategy_matrix_contract",
            "verification_report_contributes_review_findings",
            "runtime_review_report_contract",
            "actor_output_roles_by_skill",
            "verifier_compositor_internal_output_contracts",
            "external_input_contract",
            "entry_mode_bound_to_receipt_and_task_export",
            "finding_index_role_by_workflow",
        },
        "runtime_artifact_role_contract_invalid",
        "contract shape",
    )
    review_roles = contract["review_output_roles"]
    require(
        isinstance(review_roles, list)
        and bool(review_roles)
        and len(review_roles) == len(set(review_roles))
        and {
            "evaluation_report",
            "research_polisher_evaluation_report",
            "research_polisher_strategy_report",
            "review_report",
            "audit_report",
            "panel_report",
            "verification_report",
            "readiness_report",
            "preflight_report",
            "language_assessment_report",
            "medical_journal_review_report",
        }
        <= set(review_roles),
        "runtime_artifact_role_contract_invalid",
        "review output roles",
    )
    skill_contracts = {skill["name"]: skill for skill in registry["skills"]}
    machines = registry["workflow_state_machines"]
    expected_assembler_skills = {
        machine["final_package_skill"]
        for machine in machines.values()
        if skill_contracts[machine["final_package_skill"]]["role"] == "assembler"
    }
    assembler_outputs = contract["assembler_outputs_by_skill"]
    require(
        isinstance(assembler_outputs, dict)
        and set(assembler_outputs) == expected_assembler_skills
        and all(
            isinstance(roles, list)
            and bool(roles)
            and len(roles) == len(set(roles))
            for roles in assembler_outputs.values()
        ),
        "runtime_artifact_role_contract_invalid",
        "assembler output coverage",
    )
    require(
        set(assembler_outputs["research-polisher-plan-assembler"])
        == {
            "research_polisher_sealed_provenance",
            "research_polisher_candidate_portfolio",
            "research_polisher_specialist_findings_bundle",
            "research_polisher_review_finding_index",
            "research_polisher_revision_brief",
            "research_polisher_revision_delta",
            "research_polisher_selection_dossier",
        },
        "runtime_artifact_role_contract_invalid",
        "Research Polisher assembler outputs",
    )
    expected_supporting_writer_skills = {
        edge[1]
        for workflow in machines
        for edge in edge_derived_actor_edges(registry, workflow, "supporting_writer")
    }
    supporting_writer_outputs = contract["supporting_writer_outputs_by_skill"]
    require(
        isinstance(supporting_writer_outputs, dict)
        and set(supporting_writer_outputs) == expected_supporting_writer_skills
        and supporting_writer_outputs
        == {
            "sap-writer": ["sap"],
            "article-frontmatter-drafter": ["frontmatter"],
        },
        "runtime_artifact_role_contract_invalid",
        "supporting writer outputs",
    )
    polisher_review_outputs = contract[
        "research_polisher_review_outputs_by_actor_role_and_skill"
    ]
    require(
        polisher_review_outputs
        == {
            "strategy_reviewer": {
                "research-polisher-strategy-reviewer": [
                    "research_polisher_strategy_report"
                ]
            },
            "evaluator": {
                "research-polisher-methodology-publishability-reviewer": [
                    "research_polisher_evaluation_report"
                ]
            },
            "supporting_reviewer": {
                "methodology-statistics-preflight": ["preflight_report"],
                "medical-journal-review": ["medical_journal_review_report"],
            },
        },
        "runtime_artifact_role_contract_invalid",
        "Research Polisher reviewer outputs",
    )
    review_group = scenario_contract["review_group_contracts"]["research_polisher"]
    matrix_contract = contract["research_polisher_strategy_matrix_contract"]
    expected_matrix_core = {
            "strategy_skill": review_group["skill"],
            "strategy_artifact_role": "research_polisher_strategy_report",
            "portfolio_skill": "research-polisher-plan-assembler",
            "portfolio_artifact_role": "research_polisher_candidate_portfolio",
            "strategy_roles": review_group["roles"],
            "effort_tiers": review_group["effort_tiers"],
            "reports_per_portfolio": review_group["required_instance_count"],
            "cells_per_report": len(review_group["effort_tiers"]),
            "total_matrix_cells": review_group["required_matrix_cell_count"],
            "portfolio_binds_all_strategy_reports": True,
            "assembler_reads_all_strategy_reports": True,
            "generic_review_reports_do_not_satisfy_strategy_lineage": True,
        }
    require(
        all(matrix_contract.get(key) == value for key, value in expected_matrix_core.items())
        and matrix_contract.get("required_option_fields")
        and matrix_contract.get("new_work_flag_fields")
        == ["new_analysis", "new_experiment", "new_data", "new_validation"]
        and set(matrix_contract.get("allowed_feasibility_ratings", []))
        == {"certain", "high", "low", "unknown"}
        and set(matrix_contract.get("proposed_extension_feasibility_ratings", []))
        == {"certain", "high"}
        and matrix_contract.get("reposition_requires_no_added_work") is True
        and matrix_contract.get("extensions_must_be_bounded") is True
        and matrix_contract.get(
            "low_or_unknown_extension_requires_no_defensible_option"
        )
        is True
        and contract.get("verification_report_contributes_review_findings") is True,
        "runtime_artifact_role_contract_invalid",
        "Research Polisher matrix or verifier finding contract",
    )
    finding_roles = contract["finding_index_role_by_workflow"]
    require(
        isinstance(finding_roles, dict)
        and set(finding_roles) == set(machines)
        and finding_roles["research_polisher"]
        == "research_polisher_review_finding_index"
        and all(
            finding_roles[workflow] == "review_finding_index"
            for workflow in set(machines) - {"research_polisher"}
        ),
        "runtime_artifact_role_contract_invalid",
        "finding-index roles",
    )
    review_report_contract = contract["runtime_review_report_contract"]
    require(
        review_report_contract.get("required_fields")
        == [
            "decision",
            "findings",
            "unresolved_issues",
            "dissent_ids",
            "fatal_finding_ids",
            "unresolved_fatal_finding_ids",
        ]
        and review_report_contract.get("finding_required_fields")
        == ["id", "severity", "blocking", "resolved", "dissent"]
        and set(review_report_contract.get("allowed_severities", []))
        == {"fatal", "major", "minor", "info"}
        and review_report_contract.get(
            "decision_vocabulary_from_review_decision_contracts"
        )
        is True
        and set(review_report_contract.get("ready_actor_roles_require_pass_decision", []))
        == {
            "evaluator",
            "panel",
            "strategy_reviewer",
            "supporting_reviewer",
            "verifier_compositor",
        }
        and review_report_contract.get("one_review_report_per_actor") is True
        and review_report_contract.get(
            "pass_decision_requires_no_unresolved_blocking_findings"
        )
        is True
        and review_report_contract.get(
            "review_input_refs_must_equal_actual_read_artifact_refs"
        )
        is True,
        "runtime_artifact_role_contract_invalid",
        "review report contract",
    )
    output_roles = contract["actor_output_roles_by_skill"]
    require(
        isinstance(output_roles, dict)
        and set(skill_contracts) <= set(output_roles)
        and all(
            isinstance(roles, list)
            and bool(roles)
            and len(roles) == len(set(roles))
            for roles in output_roles.values()
        ),
        "runtime_artifact_role_contract_invalid",
        "actor output roles",
    )
    internal_outputs = contract["verifier_compositor_internal_output_contracts"]
    require(
        internal_outputs
        == {
            "perspective-final-compositor": {
                "ordered_output_roles": [
                    "panel_summary",
                    "artifact_index",
                    "verification_report",
                    "review_finding_index",
                    "final_handoff_package",
                ],
                "final_output_role": "final_handoff_package",
                "internal_dependency_roles": [
                    "panel_summary",
                    "artifact_index",
                    "verification_report",
                    "review_finding_index",
                ],
                "creation_sequence_field": "creation_sequence",
                "internal_output_refs_field": "internal_output_refs",
                "internal_dependencies_are_not_file_reads": True,
                "single_instance_required": True,
            }
        },
        "runtime_artifact_role_contract_invalid",
        "verifier compositor internal outputs",
    )
    external = contract["external_input_contract"]
    require(
        external.get("creator_sentinel") == "external-input"
        and external.get("source_skill_sentinel") == "external-input"
        and external.get("source_identity_field") == "external_source_id"
        and external.get("source_identity_prefix") == "external:"
        and set(external.get("allowed_artifact_roles_by_workflow_and_mode", {}))
        == set(machines)
        and set(external.get("external_primary_allowed_modes", {}))
        == set(machines)
        and external.get(
            "external_generated_or_review_artifact_impersonation_rejected"
        )
        is True
        and contract.get("entry_mode_bound_to_receipt_and_task_export") is True,
        "runtime_artifact_role_contract_invalid",
        "external input contract",
    )
    package_contracts = scenario_contract["package_input_contracts"]
    require(
        all(
            "source_skill" in rule or "source_skills" in rule
            for package in package_contracts.values()
            for rule in package["required_inputs"]
        ),
        "runtime_artifact_role_contract_invalid",
        "package source-skill bindings",
    )
    proposal_sap_rules = [
        rule
        for rule in package_contracts["proposal"]["required_inputs"]
        if rule.get("artifact_role") in {"sap", "evaluation_report"}
        and rule.get("source_skill") in {"sap-writer", "sap-evaluator"}
    ]
    require(
        len(proposal_sap_rules) == 2
        and next(
            rule for rule in proposal_sap_rules if rule["source_skill"] == "sap-writer"
        ).get("latest_selected_artifact")
        is True
        and all(
            next(
                rule
                for rule in proposal_sap_rules
                if rule["source_skill"] == "sap-evaluator"
            ).get(field)
            is True
            for field in ("exact_selected_artifact_lineage", "fresh_review_required")
        ),
        "runtime_artifact_role_contract_invalid",
        "proposal SAP package contract",
    )
    return contract


def artifact_is_review_finding_report(
    *, creator_role: str, artifact_role: str, contract: dict[str, Any]
) -> bool:
    """Identify reports whose findings must be included in the review-state union."""

    if creator_role in {
        "evaluator",
        "panel",
        "strategy_reviewer",
        "supporting_reviewer",
    }:
        return artifact_role in set(contract["review_output_roles"])
    return (
        creator_role == "verifier_compositor"
        and artifact_role == "verification_report"
        and contract["verification_report_contributes_review_findings"] is True
    )


def validate_actor_dispatch_edge_runtime(
    actor: dict[str, Any], workflow: str, registry: dict[str, Any]
) -> None:
    """Bind every non-root runtime actor to one exact registered workflow edge."""

    identity = (
        actor.get("dispatch_source"),
        actor.get("skill"),
        actor.get("dispatch_mode"),
        actor.get("dispatch_trigger"),
    )
    registered = {
        (
            edge["source"],
            edge["destination"],
            edge["dispatch_mode"],
            edge["trigger"],
        )
        for edge in registry["workflow_edges"]
        if edge["workflow"] == workflow
    }
    require(
        identity in registered,
        "runtime_actor_edge_provenance_mismatch",
        f"{actor.get('instance_id')}: {identity}",
    )


def validate_actor_output_role_runtime(
    *, actor: dict[str, Any], artifact: dict[str, Any], contract: dict[str, Any]
) -> None:
    allowed = contract["actor_output_roles_by_skill"].get(actor["skill"], [])
    require(
        artifact["artifact_role"] in set(allowed),
        "runtime_actor_output_role_mismatch",
        f"{actor['skill']}: {artifact['artifact_role']}",
    )


def validate_external_input_artifact_runtime(
    *,
    artifact: dict[str, Any],
    workflow: str,
    entry_mode: str,
    contract: dict[str, Any],
) -> None:
    external_identity = artifact.get(contract["source_identity_field"])
    allowed_roles = set(
        contract["allowed_artifact_roles_by_workflow_and_mode"][workflow][
            entry_mode
        ]
    )
    require(
        artifact.get("created_by_instance_id") == contract["creator_sentinel"]
        and artifact.get("source_skill") == contract["source_skill_sentinel"]
        and isinstance(external_identity, str)
        and external_identity.startswith(contract["source_identity_prefix"])
        and len(external_identity) > len(contract["source_identity_prefix"])
        and artifact.get("artifact_role") in allowed_roles,
        "runtime_external_input_impersonation",
        str(artifact.get("artifact_id")),
    )


def validate_blind_reviewer_inputs_runtime(
    *,
    reviewer_id: str,
    read_paths: set[str],
    artifacts_by_path: dict[str, dict[str, Any]],
    forbidden_oracle_roles: set[str],
) -> None:
    unindexed_inputs = read_paths - set(artifacts_by_path)
    require(
        not unindexed_inputs,
        "runtime_blind_reviewer_input_not_indexed",
        f"{reviewer_id}: {sorted(unindexed_inputs)}",
    )
    oracle_inputs = {
        path
        for path in read_paths
        if artifacts_by_path[path]["artifact_role"] in forbidden_oracle_roles
    }
    require(
        not oracle_inputs,
        "runtime_reviewer_oracle_visible",
        f"{reviewer_id}: {sorted(oracle_inputs)}",
    )


def validate_runtime_review_report_findings(
    report: dict[str, Any], contract: dict[str, Any], label: str
) -> tuple[set[str], set[str], set[str], set[str]]:
    """Derive all review indexes from typed finding objects; never trust arrays."""

    report_contract = contract["runtime_review_report_contract"]
    required = set(report_contract["required_fields"])
    require(
        not (required - set(report)),
        "runtime_review_output_schema",
        f"{label}: missing {sorted(required - set(report))}",
    )
    findings = report.get("findings")
    unresolved_issues = report.get("unresolved_issues")
    require(
        isinstance(report.get("decision"), str)
        and bool(report["decision"])
        and isinstance(findings, list)
        and isinstance(unresolved_issues, list)
        and all(
            isinstance(report.get(key), list)
            for key in (
                "dissent_ids",
                "fatal_finding_ids",
                "unresolved_fatal_finding_ids",
            )
        )
        and all(
            all(isinstance(value, str) and value for value in report[key])
            for key in (
                "dissent_ids",
                "fatal_finding_ids",
                "unresolved_fatal_finding_ids",
            )
        )
        and all(
            len(report[key]) == len(set(report[key]))
            for key in (
                "dissent_ids",
                "fatal_finding_ids",
                "unresolved_fatal_finding_ids",
            )
        )
        and len(unresolved_issues) == len(set(unresolved_issues))
        and all(isinstance(value, str) and value for value in unresolved_issues),
        "runtime_review_output_schema",
        label,
    )
    finding_ids: set[str] = set()
    derived_dissent: set[str] = set()
    derived_fatal: set[str] = set()
    derived_unresolved_fatal: set[str] = set()
    derived_unresolved: set[str] = set()
    finding_required = set(report_contract["finding_required_fields"])
    allowed_severities = set(report_contract["allowed_severities"])
    for finding in findings:
        require(
            isinstance(finding, dict) and not (finding_required - set(finding)),
            "runtime_review_finding_schema",
            label,
        )
        finding_id = finding.get("id")
        require(
            isinstance(finding_id, str)
            and bool(finding_id)
            and finding_id not in finding_ids
            and finding.get("severity") in allowed_severities
            and isinstance(finding.get("blocking"), bool)
            and isinstance(finding.get("resolved"), bool)
            and isinstance(finding.get("dissent"), bool),
            "runtime_review_finding_schema",
            label,
        )
        finding_ids.add(finding_id)
        if finding["dissent"]:
            derived_dissent.add(finding_id)
        if finding["severity"] == "fatal":
            derived_fatal.add(finding_id)
            if not finding["resolved"]:
                derived_unresolved_fatal.add(finding_id)
        if finding["blocking"] and not finding["resolved"]:
            derived_unresolved.add(finding_id)
    require(
        set(report["dissent_ids"]) == derived_dissent
        and set(report["fatal_finding_ids"]) == derived_fatal
        and set(report["unresolved_fatal_finding_ids"])
        == derived_unresolved_fatal
        and set(unresolved_issues) == derived_unresolved,
        "runtime_review_finding_derivation_mismatch",
        label,
    )
    return (
        derived_dissent,
        derived_fatal,
        derived_unresolved_fatal,
        derived_unresolved,
    )


def validate_runtime_review_decision(
    report: dict[str, Any], creator: dict[str, Any], registry: dict[str, Any], label: str
) -> bool:
    contract = registry["scenario_eval_contract"]["review_decision_contracts"].get(
        creator["skill"]
    )
    require(
        isinstance(contract, dict)
        and report.get("decision") in set(contract.get("allowed", [])),
        "runtime_review_decision_unknown",
        f"{label}: {creator['skill']}={report.get('decision')}",
    )
    return report["decision"] in set(contract["pass"])


def version_number(version_id: str, label: str) -> int:
    match = re.fullmatch(r"v(\d+)", version_id or "")
    require(match is not None, "runtime_artifact_version_invalid", label)
    return int(match.group(1))


def validate_proposal_sap_package_runtime(
    *,
    package_parent_artifacts: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    actor_by_id: dict[str, dict[str, Any]],
) -> None:
    """Bind a proposal package to the latest SAP and its exact fresh evaluation."""

    all_saps = [
        item
        for item in artifacts
        if item["artifact_role"] == "sap" and item["source_skill"] == "sap-writer"
    ]
    require(bool(all_saps), "runtime_sap_writer_artifact_missing", "proposal package")
    latest_number = max(
        version_number(item["version_id"], ref_for(item)) for item in all_saps
    )
    latest_saps = [
        item
        for item in all_saps
        if version_number(item["version_id"], ref_for(item)) == latest_number
    ]
    require(
        len(latest_saps) == 1,
        "runtime_sap_latest_version_ambiguous",
        "proposal package",
    )
    latest_ref = ref_for(latest_saps[0])
    selected_saps = [item for item in package_parent_artifacts if item["artifact_role"] == "sap"]
    require(
        len(selected_saps) == 1 and ref_for(selected_saps[0]) == latest_ref,
        "runtime_sap_package_stale_selection",
        latest_ref,
    )
    sap_writer_actor = actor_by_id.get(latest_saps[0].get("created_by_instance_id"))
    require(
        sap_writer_actor is not None
        and sap_writer_actor.get("role") == "supporting_writer"
        and sap_writer_actor.get("skill") == "sap-writer",
        "runtime_sap_writer_actor_mismatch",
        latest_ref,
    )
    selected_reviews = [
        item
        for item in package_parent_artifacts
        if item["artifact_role"] == "evaluation_report"
        and item["source_skill"] == "sap-evaluator"
    ]
    require(
        len(selected_reviews) == 1
        and selected_reviews[0]["based_on"] == [latest_ref]
        and selected_reviews[0]["change_type"]
        in {"independent_evaluation", "fresh_independent_evaluation"},
        "runtime_sap_evaluation_lineage_mismatch",
        latest_ref,
    )
    sap_evaluator_actor = actor_by_id.get(
        selected_reviews[0].get("created_by_instance_id")
    )
    require(
        sap_evaluator_actor is not None
        and sap_evaluator_actor.get("role") == "supporting_reviewer"
        and sap_evaluator_actor.get("skill") == "sap-evaluator"
        and sap_evaluator_actor.get("isolation_mode") == "fresh_subagent"
        and sap_evaluator_actor.get("instance_id")
        != sap_writer_actor.get("instance_id"),
        "runtime_sap_evaluator_actor_mismatch",
        latest_ref,
    )


def validate_control_independent_gates_runtime(
    *,
    workflow: str,
    case_contract: dict[str, Any],
    current_ref: str,
    control_finding_id: str,
    review_reports_by_skill: dict[str, list[dict[str, Any]]],
    finding_provenance: dict[str, dict[str, Any]],
    strategy_role_instances: dict[str, str],
    strategy_cells_by_ref: dict[str, set[tuple[str, str]]],
    registry: dict[str, Any],
) -> None:
    """Prevent a control receipt from bypassing the independent gate it cites."""

    for skill in case_contract["required_review_skills"]:
        require(
            bool(review_reports_by_skill.get(skill)),
            "runtime_control_required_independent_gate_missing",
            f"{workflow}: {skill}",
        )
    if case_contract["required_strategy_matrix"]:
        group = registry["scenario_eval_contract"]["review_group_contracts"].get(
            workflow
        )
        require(
            isinstance(group, dict)
            and set(strategy_role_instances) == set(group["roles"])
            and len(set(strategy_role_instances.values()))
            == group["required_instance_count"]
            and len(set().union(*strategy_cells_by_ref.values()))
            == group["required_matrix_cell_count"],
            "runtime_control_required_independent_gate_missing",
            f"{workflow}: strategy matrix",
        )
    provenance = finding_provenance.get(control_finding_id)
    decision_contracts = registry["scenario_eval_contract"][
        "review_decision_contracts"
    ]
    decisions_by_skill = case_contract["control_finding_decisions_by_skill"]
    for skill, decisions in decisions_by_skill.items():
        skill_contract = decision_contracts.get(skill, {})
        require(
            bool(decisions)
            and set(decisions) <= set(skill_contract.get("allowed", []))
            and set(decisions) <= set(skill_contract.get("stop", [])),
            "runtime_control_finding_contract_invalid",
            f"{workflow}: {skill}",
        )
    provenance_skill = (
        provenance["creator"]["skill"] if provenance is not None else None
    )
    provenance_decision = (
        provenance.get("report", {}).get("decision")
        if provenance is not None
        else None
    )
    provenance_finding = (
        provenance.get("finding", {}) if provenance is not None else {}
    )
    require(
        provenance is not None
        and provenance_skill in decisions_by_skill
        and provenance_decision in set(decisions_by_skill[provenance_skill])
        and current_ref in provenance["input_refs"]
        and provenance.get("decision_pass") is False,
        "runtime_control_finding_provenance_mismatch",
        f"{workflow}: {control_finding_id}",
    )
    require(
        provenance_finding.get("severity")
        in set(case_contract["control_finding_allowed_severities"])
        and provenance_finding.get("blocking")
        is case_contract["control_finding_blocking"]
        and provenance_finding.get("resolved")
        is case_contract["control_finding_resolved"],
        "runtime_control_finding_semantics_mismatch",
        f"{workflow}: {control_finding_id}",
    )


def validate_ready_has_no_unresolved_fatal(
    unresolved_fatal_ids: set[str], label: str
) -> None:
    require(not unresolved_fatal_ids, "runtime_false_ready", label)


def validate_research_polisher_strategy_report_runtime(
    report: dict[str, Any],
    actor: dict[str, Any],
    contract: dict[str, Any],
    label: str,
) -> set[tuple[str, str]]:
    """Validate one blind strategy lens and its three required effort tiers."""

    matrix = contract["research_polisher_strategy_matrix_contract"]
    require(
        actor.get("role") == "strategy_reviewer"
        and actor.get("skill") == matrix["strategy_skill"]
        and report.get("strategy_role") == actor.get("strategy_role")
        and report.get("strategy_role") in matrix["strategy_roles"]
        and report.get("peer_outputs_visible") is False,
        "runtime_polisher_strategy_report_identity",
        label,
    )
    options = report.get("strategy_options")
    require(
        isinstance(options, list)
        and len(options) == matrix["cells_per_report"],
        "runtime_polisher_strategy_matrix_incomplete",
        label,
    )
    observed_tiers = [option.get("effort_tier") for option in options]
    require(
        observed_tiers == matrix["effort_tiers"]
        and len(set(observed_tiers)) == matrix["cells_per_report"]
        and all(
            option.get("status") in {"proposed", "no_defensible_option"}
            for option in options
        ),
        "runtime_polisher_strategy_matrix_incomplete",
        label,
    )
    required_option_fields = set(matrix["required_option_fields"])
    flag_fields = set(matrix["new_work_flag_fields"])
    allowed_feasibility = set(matrix["allowed_feasibility_ratings"])
    proposed_feasibility = set(
        matrix["proposed_extension_feasibility_ratings"]
    )
    proposal_ids: set[str] = set()
    for option in options:
        require(
            isinstance(option, dict)
            and not (required_option_fields - set(option)),
            "runtime_polisher_strategy_option_schema",
            label,
        )
        proposal_id = option.get("proposal_id")
        feasibility = option.get("feasibility")
        flags = option.get("new_work_flags")
        require(
            isinstance(proposal_id, str)
            and bool(proposal_id)
            and proposal_id not in proposal_ids
            and all(
                isinstance(option.get(field), str) and bool(option[field])
                for field in (
                    "positioning_change",
                    "value_gain_mechanism",
                    "claim_delta",
                    "target_audience",
                )
            )
            and all(
                isinstance(option.get(field), list)
                for field in (
                    "added_work_items",
                    "resource_dependencies",
                    "evidence_dependencies",
                    "risks",
                    "stop_conditions",
                )
            )
            and bool(option["risks"])
            and bool(option["stop_conditions"])
            and isinstance(feasibility, dict)
            and feasibility.get("rating") in allowed_feasibility
            and isinstance(feasibility.get("basis"), str)
            and bool(feasibility["basis"])
            and isinstance(flags, dict)
            and set(flags) == flag_fields
            and all(isinstance(value, bool) for value in flags.values())
            and isinstance(option.get("bounded_package"), bool)
            and isinstance(option.get("independent_new_study"), bool)
            and isinstance(option.get("core_design_rebuild"), bool),
            "runtime_polisher_strategy_option_schema",
            f"{label}: {proposal_id}",
        )
        proposal_ids.add(proposal_id)
        tier = option["effort_tier"]
        if tier == "reposition_only":
            require(
                option["added_work_items"] == []
                and not any(flags.values())
                and option["bounded_package"] is True
                and option["independent_new_study"] is False
                and option["core_design_rebuild"] is False,
                "runtime_polisher_reposition_smuggles_new_work",
                f"{label}: {proposal_id}",
            )
        else:
            require(
                option["independent_new_study"] is False
                and option["core_design_rebuild"] is False,
                "runtime_polisher_extension_scope_exceeded",
                f"{label}: {proposal_id}",
            )
            if option["status"] == "proposed":
                require(
                    bool(option["added_work_items"])
                    and option["bounded_package"] is True
                    and feasibility["rating"] in proposed_feasibility,
                    "runtime_polisher_extension_feasibility_invalid",
                    f"{label}: {proposal_id}",
                )
            else:
                require(
                    feasibility["rating"] in {"low", "unknown"}
                    or bool(option["added_work_items"]) is False,
                    "runtime_polisher_no_defensible_option_invalid",
                    f"{label}: {proposal_id}",
                )
    return {(report["strategy_role"], tier) for tier in observed_tiers}


def validate_research_polisher_portfolio_lineage_runtime(
    *,
    artifacts: list[dict[str, Any]],
    actor_by_id: dict[str, dict[str, Any]],
    strategy_cells_by_ref: dict[str, set[tuple[str, str]]],
    read_paths_by_actor: dict[str, set[str]],
    contract: dict[str, Any],
) -> None:
    """Require each candidate portfolio to bind and read three real strategy reports."""

    matrix = contract["research_polisher_strategy_matrix_contract"]
    artifacts_by_ref = {ref_for(artifact): artifact for artifact in artifacts}
    portfolios = [
        artifact
        for artifact in artifacts
        if artifact["artifact_role"] == matrix["portfolio_artifact_role"]
    ]
    require(bool(portfolios), "runtime_polisher_candidate_portfolio_missing", "portfolio")
    for portfolio in portfolios:
        creator = actor_by_id.get(portfolio["created_by_instance_id"])
        require(
            creator is not None
            and creator.get("role") == "assembler"
            and creator.get("skill") == matrix["portfolio_skill"],
            "runtime_polisher_candidate_portfolio_creator",
            ref_for(portfolio),
        )
        strategy_parent_refs = [
            parent_ref
            for parent_ref in portfolio["based_on"]
            if parent_ref in strategy_cells_by_ref
        ]
        require(
            len(strategy_parent_refs) == matrix["reports_per_portfolio"]
            and len(set(strategy_parent_refs)) == matrix["reports_per_portfolio"],
            "runtime_polisher_candidate_portfolio_strategy_lineage",
            ref_for(portfolio),
        )
        parent_artifacts = [artifacts_by_ref[parent] for parent in strategy_parent_refs]
        require(
            all(
                artifact["artifact_role"] == matrix["strategy_artifact_role"]
                and artifact["source_skill"] == matrix["strategy_skill"]
                and actor_by_id[artifact["created_by_instance_id"]]["role"]
                == "strategy_reviewer"
                for artifact in parent_artifacts
            ),
            "runtime_polisher_candidate_portfolio_strategy_lineage",
            ref_for(portfolio),
        )
        observed_cells = set().union(
            *(strategy_cells_by_ref[parent] for parent in strategy_parent_refs)
        )
        expected_cells = {
            (role, tier)
            for role in matrix["strategy_roles"]
            for tier in matrix["effort_tiers"]
        }
        require(
            observed_cells == expected_cells
            and len(observed_cells) == matrix["total_matrix_cells"],
            "runtime_polisher_candidate_portfolio_matrix_incomplete",
            ref_for(portfolio),
        )
        require(
            {artifact["path"] for artifact in parent_artifacts}
            <= read_paths_by_actor[portfolio["created_by_instance_id"]],
            "runtime_polisher_assembler_strategy_report_not_read",
            ref_for(portfolio),
        )


def validate_verifier_compositor_internal_outputs_runtime(
    *,
    artifacts: list[dict[str, Any]],
    actor_by_id: dict[str, dict[str, Any]],
    read_paths_by_actor: dict[str, set[str]],
    contract: dict[str, Any],
) -> None:
    """Bind same-instance compositor outputs by ordering, never by self-read."""

    internal_contracts = contract["verifier_compositor_internal_output_contracts"]
    for skill, output_contract in internal_contracts.items():
        actor_ids = {
            actor_id
            for actor_id, actor in actor_by_id.items()
            if actor.get("skill") == skill
            and actor.get("role") == "verifier_compositor"
        }
        if not actor_ids:
            continue
        require(
            not output_contract.get("single_instance_required")
            or len(actor_ids) == 1,
            "runtime_compositor_instance_count_mismatch",
            skill,
        )
        sequence_field = output_contract["creation_sequence_field"]
        refs_field = output_contract["internal_output_refs_field"]
        expected_roles = output_contract["ordered_output_roles"]
        for actor_id in actor_ids:
            actor_outputs = [
                artifact
                for artifact in artifacts
                if artifact["created_by_instance_id"] == actor_id
                and artifact["artifact_role"] in set(expected_roles)
            ]
            by_role: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for artifact in actor_outputs:
                by_role[artifact["artifact_role"]].append(artifact)
            require(
                set(by_role) == set(expected_roles)
                and all(len(items) == 1 for items in by_role.values()),
                "runtime_compositor_internal_output_missing",
                actor_id,
            )
            ordered = [by_role[role][0] for role in expected_roles]
            sequences = [artifact.get(sequence_field) for artifact in ordered]
            require(
                all(isinstance(value, int) and value > 0 for value in sequences)
                and sequences == sorted(sequences)
                and len(sequences) == len(set(sequences)),
                "runtime_compositor_creation_order_mismatch",
                actor_id,
            )
            final_artifact = by_role[output_contract["final_output_role"]][0]
            dependency_artifacts = [
                by_role[role][0]
                for role in output_contract["internal_dependency_roles"]
            ]
            dependency_refs = {ref_for(artifact) for artifact in dependency_artifacts}
            dependency_paths = {artifact["path"] for artifact in dependency_artifacts}
            require(
                set(final_artifact.get(refs_field, [])) == dependency_refs
                and not (dependency_refs & set(final_artifact["based_on"])),
                "runtime_compositor_internal_dependency_mismatch",
                actor_id,
            )
            require(
                not (dependency_paths & read_paths_by_actor[actor_id]),
                "runtime_compositor_reads_internal_output",
                actor_id,
            )


def validate_runtime_receipt(
    receipt: dict[str, Any],
    *,
    registry: dict[str, Any],
    schema: dict[str, Any],
    expected_source_commit: str | None,
    root: Path,
    evidence_result: (
        ExternalRuntimeAttestation
        | EvidenceValidationResult
        | _TestOnlyAuthenticatedAttestation
        | None
    ) = None,
) -> dict[str, Any]:
    required = schema["$defs"]["runtime_receipt"]["required"]
    missing = sorted(set(required) - set(receipt))
    require(not missing, "runtime_receipt_schema", f"{receipt.get('receipt_id')}: {missing}")
    case_contract = validate_runtime_receipt_declaration(receipt, schema, registry)
    require(receipt["status"] == "verified", "runtime_receipt_not_verified", receipt["receipt_id"])
    required_bindings = schema["x-phase7-contract"][
        "verified_receipt_required_bindings"
    ]
    populated_bindings = [nested_value(receipt, path) for path in required_bindings]
    substantive_bindings = [
        value
        for path, value in zip(required_bindings, populated_bindings)
        if path != "binding.task_export.entry_mode"
    ]
    if not any(value not in {None, ""} for value in substantive_bindings):
        raise ModeViolation("runtime_verified_label_only", receipt["receipt_id"])
    missing_bindings = [
        path for path, value in zip(required_bindings, populated_bindings) if value in {None, ""}
    ]
    require(
        not missing_bindings,
        "runtime_binding_missing",
        f"{receipt['receipt_id']}: {missing_bindings}",
    )
    binding = receipt["binding"]
    current_registry_digest = sha256_repository_file(REGISTRY_PATH)
    require(
        binding["plugin_version"] == registry["plugin_version"],
        "runtime_plugin_version_mismatch",
        receipt["receipt_id"],
    )
    require(
        binding["registry_sha256"] == current_registry_digest,
        "runtime_registry_digest_mismatch",
        receipt["receipt_id"],
    )
    require(valid_commit_sha(binding["source_commit"]), "runtime_source_commit_invalid", receipt["receipt_id"])
    require(
        expected_source_commit is not None,
        "runtime_release_source_commit_pending",
        receipt["receipt_id"],
    )
    require(
        binding["source_commit"] == expected_source_commit,
        "runtime_source_commit_mismatch",
        receipt["receipt_id"],
    )

    task_export = binding["task_export"]
    require(task_export["platform"] in {"codex", "chatgpt"}, "runtime_platform_invalid", receipt["receipt_id"])
    require(
        isinstance(task_export["task_id"], str) and bool(task_export["task_id"].strip()),
        "runtime_task_id_missing",
        receipt["receipt_id"],
    )
    verification_level: str | None = None
    evidence_accounting_status = "contract_self_test_only"
    external_evidence_id: str | None = None
    external_live_result_digest: str | None = None
    external_verifier_workflow_run_id: int | None = None
    external_verified_at: str | None = None
    if evidence_result is not None:
        if _is_valid_external_runtime_attestation(evidence_result):
            attestation = evidence_result
            integrity_result = attestation.integrity_result
            promoted_counts_as_preview = attestation.counts_as_preview_acceptance
            promoted_provider_verified = attestation.provider_verified
            verification_level = attestation.verification_level
            evidence_accounting_status = "externally_attested_runtime_evidence"
            external_evidence_id = attestation.evidence_id
            external_live_result_digest = attestation.live_result_digest
            external_verifier_workflow_run_id = (
                attestation.verifier_workflow_run_id
            )
            external_verified_at = attestation.verified_at
        elif _is_valid_test_only_attestation(evidence_result):
            attestation = evidence_result
            integrity_result = attestation.integrity_result
            promoted_counts_as_preview = attestation.counts_as_preview_acceptance
            promoted_provider_verified = attestation.provider_verified
            verification_level = attestation.verification_level
            evidence_accounting_status = (
                "synthetic_authenticated_reachability_only"
            )
        elif isinstance(evidence_result, EvidenceValidationResult):
            raise ModeViolation(
                "runtime_evidence_authenticated_attestation_missing",
                "an integrity-only core result cannot promote a runtime receipt",
            )
        else:
            raise ModeViolation(
                "runtime_evidence_attestation_type_invalid",
                receipt["receipt_id"],
            )
        require(
            promoted_counts_as_preview is True,
            "runtime_evidence_not_preview_acceptable",
            receipt["receipt_id"],
        )
        require(
            verification_level in ACCEPTANCE_LEVELS
            and promoted_provider_verified
            is (verification_level == PROVIDER_VERIFIED),
            "runtime_evidence_verification_level_invalid",
            receipt["receipt_id"],
        )
        result_identity = integrity_result.source_identity
        require(
            result_identity.get("plugin_version") == binding["plugin_version"]
            and result_identity.get("source_commit") == binding["source_commit"]
            and result_identity.get("registry_sha256")
            == binding["registry_sha256"],
            "runtime_evidence_source_identity_mismatch",
            receipt["receipt_id"],
        )
        require(
            integrity_result.raw_export_sha256 == task_export["sha256"],
            "runtime_evidence_raw_export_mismatch",
            receipt["receipt_id"],
        )
    task_export_path = resolve_durable_file(
        task_export, root=root, label=f"{receipt['receipt_id']}.task_export"
    )
    actor_manifest_path = resolve_durable_file(
        binding["actor_manifest"],
        root=root,
        label=f"{receipt['receipt_id']}.actor_manifest",
    )
    artifact_index_path = resolve_durable_file(
        binding["artifact_index"],
        root=root,
        label=f"{receipt['receipt_id']}.artifact_index",
    )

    task_export_document = load_structured_file(task_export_path)
    actor_manifest = load_structured_file(actor_manifest_path)
    artifact_index = load_structured_file(artifact_index_path)
    expected_identity = {
        "platform": task_export["platform"],
        "task_id": task_export["task_id"],
        "plugin_version": binding["plugin_version"],
        "registry_sha256": binding["registry_sha256"],
        "source_commit": binding["source_commit"],
        "workflow": receipt["workflow"],
        "entry_mode": receipt["entry_mode"],
        "case_kind": receipt["case_kind"],
    }
    require(
        task_export_document.get("schema_version") == 1,
        "runtime_task_export_schema",
        receipt["receipt_id"],
    )
    for key, expected in expected_identity.items():
        require(
            task_export_document.get(key) == expected,
            "runtime_task_export_identity_mismatch",
            f"{receipt['receipt_id']}: {key}",
        )
    require(
        task_export_document.get("final_state") == receipt["final_state"],
        "runtime_task_export_final_state_mismatch",
        receipt["receipt_id"],
    )
    require(
        task_export_document.get("automatic_external_submission")
        == receipt["automatic_external_submission"],
        "runtime_task_export_submission_mismatch",
        receipt["receipt_id"],
    )
    require(
        task_export_document.get("actor_manifest") == binding["actor_manifest"],
        "runtime_task_export_binding_mismatch",
        f"{receipt['receipt_id']}: actor_manifest",
    )
    require(
        task_export_document.get("artifact_index") == binding["artifact_index"],
        "runtime_task_export_binding_mismatch",
        f"{receipt['receipt_id']}: artifact_index",
    )
    file_access_binding = task_export_document.get("file_access")
    require(
        isinstance(file_access_binding, dict),
        "runtime_task_export_binding_mismatch",
        f"{receipt['receipt_id']}: file_access",
    )
    file_access_path = resolve_durable_file(
        file_access_binding,
        root=root,
        label=f"{receipt['receipt_id']}.file_access",
    )
    file_access_document = load_structured_file(file_access_path)
    require(
        file_access_document.get("schema_version") == 1,
        "runtime_file_access_schema",
        receipt["receipt_id"],
    )
    for key in ("task_id", "plugin_version", "registry_sha256", "source_commit", "workflow", "entry_mode"):
        require(
            file_access_document.get(key) == expected_identity[key],
            "runtime_linked_identity_mismatch",
            f"{receipt['receipt_id']}: file_access.{key}",
        )
    require(
        {
            "reads": file_access_document.get("reads"),
            "writes": file_access_document.get("writes"),
            "source_artifact_hashes_unchanged": file_access_document.get(
                "source_artifact_hashes_unchanged"
            ),
        }
        == receipt["file_access"],
        "runtime_file_access_receipt_mismatch",
        receipt["receipt_id"],
    )

    require(actor_manifest.get("schema_version") == 1, "runtime_actor_manifest_schema", receipt["receipt_id"])
    require(actor_manifest.get("workflow") == receipt["workflow"], "runtime_actor_manifest_scope", receipt["receipt_id"])
    require(artifact_index.get("schema_version") == 1, "runtime_artifact_index_schema", receipt["receipt_id"])
    require(artifact_index.get("workflow") == receipt["workflow"], "runtime_artifact_index_scope", receipt["receipt_id"])
    for document, label in (
        (actor_manifest, "actor_manifest"),
        (artifact_index, "artifact_index"),
    ):
        for key in ("task_id", "plugin_version", "registry_sha256", "source_commit"):
            require(
                document.get(key) == expected_identity[key],
                "runtime_linked_identity_mismatch",
                f"{receipt['receipt_id']}: {label}.{key}",
            )
    actors = actor_manifest.get("actors")
    require(isinstance(actors, list) and bool(actors), "runtime_actor_manifest_schema", receipt["receipt_id"])
    actor_ids: list[str] = []
    actor_by_id: dict[str, dict[str, Any]] = {}
    actor_role_contract = runtime_actor_role_contract(registry, schema)
    allowed_actor_roles = set(actor_role_contract["allowed_roles"])
    registry_roles_by_actor_role = actor_role_contract[
        "registry_roles_by_actor_role"
    ]
    actors_by_role: dict[str, set[str]] = {
        role: set() for role in actor_role_contract["allowed_roles"]
    }
    independent_reviewer_actor_roles = set(
        actor_role_contract["independent_reviewer_actor_roles"]
    )
    independent_reviewer_isolation_mode = actor_role_contract[
        "independent_reviewer_isolation_mode"
    ]
    skill_contracts = {skill["name"]: skill for skill in registry["skills"]}
    machine = registry["workflow_state_machines"][receipt["workflow"]]
    direction_profile = direction_profile_for(
        receipt["workflow"],
        registry,
        receipt.get("direction_profile")
        or task_export_document.get("direction_profile"),
    )
    condition_contract = workflow_conditions_for(
        receipt["workflow"], registry, {}, default_active=True
    )
    declared_conditions = {
        name: task_export_document.get(name, receipt.get(name, default_value))
        for name, default_value in condition_contract.items()
    }
    workflow_conditions = workflow_conditions_for(
        receipt["workflow"],
        registry,
        declared_conditions,
        default_active=True,
    )
    if receipt["workflow"] == "idea":
        require(
            task_export_document.get("direction_profile", direction_profile)
            == direction_profile
            and all(
                receipt.get(name, value) == value
                and task_export_document.get(name, value) == value
                for name, value in workflow_conditions.items()
            ),
            "runtime_direction_profile_binding_mismatch",
            receipt["receipt_id"],
        )
    runtime_profile = machine.get("workflow_profile", "default")
    expected_evaluator_skill = machine["evaluator_skill"]
    expected_writer_skills = set(machine["primary_writer_skills"])
    expected_panel_skill = panel_skill_for(
        {"workflow": receipt["workflow"], "case_id": receipt["receipt_id"]},
        registry,
        direction_profile=direction_profile,
        workflow_conditions=workflow_conditions,
    )
    expected_panel_tier, expected_panel_roles = default_panel_roles(
        receipt["workflow"],
        registry,
        direction_profile=direction_profile,
        workflow_conditions=workflow_conditions,
    )
    strategy_group_contract = (
        registry["scenario_eval_contract"].get("review_group_contracts", {}).get(
            receipt["workflow"]
        )
    )
    expected_strategy_skill = (
        strategy_group_contract["skill"] if strategy_group_contract else None
    )
    expected_strategy_roles = (
        list(strategy_group_contract["roles"]) if strategy_group_contract else []
    )
    expected_final_skill = machine["final_package_skill"]
    expected_final_role = (
        "verifier_compositor"
        if skill_contracts[expected_final_skill]["requires_independent_subagent"] is True
        else "assembler"
    )
    require(
        expected_final_role in set(actor_role_contract["finalizer_roles"]),
        "runtime_actor_role_contract_invalid",
        f"{receipt['workflow']}: finalizer role",
    )
    expected_supporting_edges = {
        role: edge_derived_actor_edges(registry, receipt["workflow"], role)
        for role in ("supporting_reviewer", "supporting_writer")
    }
    panel_role_instances: dict[str, str] = {}
    strategy_role_instances: dict[str, str] = {}
    for actor in actors:
        require(isinstance(actor, dict), "runtime_actor_manifest_schema", receipt["receipt_id"])
        require(
            all(isinstance(actor.get(key), str) and actor[key] for key in ("instance_id", "skill", "role"))
            and isinstance(actor.get("allowed_read_roots"), list)
            and isinstance(actor.get("allowed_write_roots"), list),
            "runtime_actor_manifest_schema",
            receipt["receipt_id"],
        )
        actor_ids.append(actor["instance_id"])
        actor_by_id[actor["instance_id"]] = actor
        require(
            actor["role"] in allowed_actor_roles,
            "runtime_actor_role_unknown",
            f"{actor['instance_id']}: {actor['role']}",
        )
        actors_by_role[actor["role"]].add(actor["instance_id"])
        require(actor["skill"] in skill_contracts, "runtime_actor_skill_missing", actor["skill"])
        skill_contract = skill_contracts[actor["skill"]]
        require(
            skill_contract["role"]
            in set(registry_roles_by_actor_role[actor["role"]]),
            "runtime_actor_role_registry_mismatch",
            (
                f"{actor['instance_id']}: actor={actor['role']}, "
                f"registry={skill_contract['role']}"
            ),
        )
        if actor["role"] in independent_reviewer_actor_roles:
            require(
                isinstance(actor.get("round_id"), str)
                and bool(actor["round_id"])
                and actor.get("isolation_mode")
                == independent_reviewer_isolation_mode,
                "runtime_reviewer_isolation_mismatch",
                actor["instance_id"],
            )
        if actor["role"] == "writer":
            require(
                actor["skill"] in expected_writer_skills
                and skill_contract["role"] in {"generator", "drafter"},
                "runtime_writer_skill_mismatch",
                actor["instance_id"],
            )
        elif actor["role"] == "evaluator":
            require(
                actor["skill"] == expected_evaluator_skill
                and skill_contract["requires_independent_subagent"] is True
                and actor["role"] in independent_reviewer_actor_roles,
                "runtime_evaluator_skill_mismatch",
                actor["instance_id"],
            )
        elif actor["role"] == "panel":
            require(expected_panel_skill is not None, "runtime_panel_skill_mismatch", actor["instance_id"])
            require(
                actor["skill"] == expected_panel_skill
                and skill_contract["requires_independent_subagent"] is True
                and actor["role"] in independent_reviewer_actor_roles,
                "runtime_panel_skill_mismatch",
                actor["instance_id"],
            )
            require(
                actor.get("panel_tier") == expected_panel_tier
                and actor.get("panel_role") in expected_panel_roles
                and actor["panel_role"] not in panel_role_instances,
                "runtime_panel_role_mismatch",
                actor["instance_id"],
            )
            panel_role_instances[actor["panel_role"]] = actor["instance_id"]
        elif actor["role"] == "strategy_reviewer":
            require(
                expected_strategy_skill is not None
                and actor["skill"] == expected_strategy_skill
                and skill_contract["requires_independent_subagent"] is True
                and actor.get("strategy_role") in expected_strategy_roles
                and actor["strategy_role"] not in strategy_role_instances,
                "runtime_strategy_reviewer_role_mismatch",
                actor["instance_id"],
            )
            strategy_role_instances[actor["strategy_role"]] = actor["instance_id"]
        elif actor["role"] == "supporting_reviewer":
            edge_identity = (
                actor.get("dispatch_source"),
                actor["skill"],
                actor.get("dispatch_mode"),
                actor.get("dispatch_trigger"),
            )
            require(
                edge_identity in expected_supporting_edges["supporting_reviewer"],
                "runtime_supporting_reviewer_edge_mismatch",
                actor["instance_id"],
            )
            require(
                skill_contract["requires_independent_subagent"] is True
                and actor.get("isolation_mode") == "fresh_subagent",
                "runtime_supporting_reviewer_isolation_mismatch",
                actor["instance_id"],
            )
        elif actor["role"] == "supporting_writer":
            edge_identity = (
                actor.get("dispatch_source"),
                actor["skill"],
                actor.get("dispatch_mode"),
                actor.get("dispatch_trigger"),
            )
            require(
                edge_identity in expected_supporting_edges["supporting_writer"]
                and skill_contract["role"] == "drafter",
                "runtime_supporting_writer_edge_mismatch",
                actor["instance_id"],
            )
        elif actor["role"] == "orchestrator":
            require(
                actor["skill"] == machine["orchestrator"],
                "runtime_orchestrator_skill_mismatch",
                actor["instance_id"],
            )
        elif actor["role"] in {"assembler", "verifier_compositor"}:
            require(
                actor["skill"] == expected_final_skill
                and actor["role"] == expected_final_role
                and (
                    actor["role"] != "verifier_compositor"
                    or skill_contract["requires_independent_subagent"] is True
                ),
                "runtime_assembler_skill_mismatch",
                actor["instance_id"],
            )
        if actor["role"] in set(
            actor_role_contract["edge_provenance_required_actor_roles"]
        ):
            validate_actor_dispatch_edge_runtime(actor, receipt["workflow"], registry)
    require(len(actor_ids) == len(set(actor_ids)), "runtime_actor_id_reused", receipt["receipt_id"])
    role_ids = list(actors_by_role.values())
    require(
        all(not (left & right) for index, left in enumerate(role_ids) for right in role_ids[index + 1 :]),
        "runtime_actor_role_overlap",
        receipt["receipt_id"],
    )
    require(
        bool(actors_by_role["orchestrator"]),
        "runtime_orchestrator_actor_missing",
        receipt["receipt_id"],
    )
    if receipt["case_kind"] == "happy":
        required_happy_roles = actor_role_contract[
            "happy_required_roles_by_workflow_profile"
        ].get(runtime_profile)
        require(
            isinstance(required_happy_roles, list) and bool(required_happy_roles),
            "runtime_actor_role_contract_invalid",
            f"{receipt['workflow']}: happy roles",
        )
        effective_happy_roles = [
            role
            for role in required_happy_roles
            if role != "panel" or expected_panel_skill is not None
        ]
        require(
            all(
                actors_by_role[role]
                for role in (*effective_happy_roles, expected_final_role)
            ),
            "runtime_happy_actor_role_missing",
            receipt["receipt_id"],
        )
        require(
            len(actors_by_role["evaluator"]) >= 2,
            "runtime_fresh_evaluator_round_missing",
            receipt["receipt_id"],
        )
        if expected_panel_skill is not None:
            require(
                set(panel_role_instances) == set(expected_panel_roles)
                and len(set(panel_role_instances.values())) == len(expected_panel_roles),
                "runtime_panel_role_mismatch",
                receipt["receipt_id"],
            )
            require(
                task_export_document.get("panel_tier") == expected_panel_tier
                and task_export_document.get("panel_role_instances") == panel_role_instances,
                "runtime_task_export_actor_contract_mismatch",
                receipt["receipt_id"],
            )
        elif strategy_group_contract is not None:
            require(
                not panel_role_instances
                and set(strategy_role_instances) == set(expected_strategy_roles)
                and len(set(strategy_role_instances.values()))
                == strategy_group_contract["required_instance_count"],
                "runtime_strategy_reviewer_role_mismatch",
                receipt["receipt_id"],
            )
            require(
                task_export_document.get("strategy_role_instances")
                == strategy_role_instances,
                "runtime_task_export_actor_contract_mismatch",
                receipt["receipt_id"],
            )
        else:
            require(
                not panel_role_instances
                and not strategy_role_instances
                and task_export_document.get("panel_role_instances") in (None, {})
                and task_export_document.get("strategy_role_instances")
                in (None, {}),
                "runtime_panel_role_mismatch",
                receipt["receipt_id"],
            )
        require(
            task_export_document.get("final_package_actor_instance_id")
            in actors_by_role[expected_final_role],
            "runtime_task_export_actor_contract_mismatch",
            receipt["receipt_id"],
        )

    artifacts = artifact_index.get("artifacts")
    require(isinstance(artifacts, list) and bool(artifacts), "runtime_artifact_index_schema", receipt["receipt_id"])
    artifact_refs: set[str] = set()
    final_package_count = 0
    artifacts_by_path: dict[str, dict[str, Any]] = {}
    resolved_artifact_paths: dict[str, Path] = {}
    review_output_artifacts: list[dict[str, Any]] = []
    finding_index_artifacts: list[dict[str, Any]] = []
    final_package_artifacts: list[dict[str, Any]] = []
    artifact_role_contract = runtime_artifact_role_contract(registry)
    review_output_roles = set(artifact_role_contract["review_output_roles"])
    verifier_outputs = set(
        registry["scenario_eval_contract"]
        .get("verifier_compositor_outputs", {})
        .get(expected_final_skill, [])
    )
    assembler_outputs = set(
        artifact_role_contract["assembler_outputs_by_skill"].get(
            expected_final_skill, []
        )
    )
    finding_index_role = artifact_role_contract["finding_index_role_by_workflow"][
        receipt["workflow"]
    ]
    polisher_review_outputs = artifact_role_contract[
        "research_polisher_review_outputs_by_actor_role_and_skill"
    ]
    final_package_roles = {
        "final_handoff_package",
        "research_polisher_selection_dossier",
    }
    external_input_contract = artifact_role_contract["external_input_contract"]
    artifact_required = {
        "artifact_id",
        "version_id",
        "artifact_role",
        "path",
        "sha256",
        "source_skill",
        "created_by_instance_id",
        "based_on",
        "change_type",
        "status",
    }
    for artifact in artifacts:
        require(isinstance(artifact, dict), "runtime_artifact_index_schema", receipt["receipt_id"])
        require(
            not (artifact_required - set(artifact)),
            "runtime_artifact_index_schema",
            receipt["receipt_id"],
        )
        resolved_artifact = resolve_durable_file(
            artifact,
            root=root,
            label=f"{receipt['receipt_id']}.artifact:{artifact['artifact_id']}",
        )
        require(
            artifact["path"] not in artifacts_by_path,
            "runtime_artifact_path_reused",
            artifact["path"],
        )
        artifacts_by_path[artifact["path"]] = artifact
        resolved_artifact_paths[artifact["path"]] = resolved_artifact
        artifact_ref = f"{artifact['artifact_id']}@{artifact['version_id']}"
        require(artifact_ref not in artifact_refs, "runtime_artifact_ref_reused", artifact_ref)
        artifact_refs.add(artifact_ref)
        require(isinstance(artifact["based_on"], list), "runtime_lineage_invalid", artifact_ref)
        if receipt["workflow"] == "idea" and artifact["artifact_role"] == "idea_dossier":
            require(
                artifact["change_type"]
                in set(
                    registry["artifact_completeness_policy"][
                        "idea_dossier_change_types"
                    ]
                ),
                "runtime_idea_dossier_change_type_invalid",
                artifact_ref,
            )
        require(
            artifact["created_by_instance_id"] in set(actor_ids) | {"external-input"},
            "runtime_artifact_actor_missing",
            artifact_ref,
        )
        if artifact["created_by_instance_id"] == external_input_contract[
            "creator_sentinel"
        ]:
            validate_external_input_artifact_runtime(
                artifact=artifact,
                workflow=receipt["workflow"],
                entry_mode=receipt["entry_mode"],
                contract=external_input_contract,
            )
        else:
            creator = actor_by_id[artifact["created_by_instance_id"]]
            require(
                creator["skill"] == artifact["source_skill"],
                "runtime_artifact_creator_skill_mismatch",
                artifact_ref,
            )
            if receipt["workflow"] == "research_polisher" and creator["role"] in set(
                polisher_review_outputs
            ):
                allowed_polisher_outputs = (
                    polisher_review_outputs[creator["role"]].get(
                        creator["skill"], []
                    )
                )
                require(
                    artifact["artifact_role"] in set(allowed_polisher_outputs),
                    "runtime_polisher_actor_output_role_mismatch",
                    artifact_ref,
                )
            if creator["role"] in {
                "evaluator",
                "panel",
                "strategy_reviewer",
                "supporting_reviewer",
            }:
                require(
                    artifact["artifact_role"] in review_output_roles,
                    "runtime_reviewer_wrote_source_artifact",
                    artifact_ref,
                )
            elif creator["role"] == "verifier_compositor":
                require(
                    artifact["artifact_role"] in verifier_outputs,
                    "runtime_compositor_wrote_source_artifact",
                    artifact_ref,
                )
            elif creator["role"] == "assembler":
                require(
                    artifact["artifact_role"] in assembler_outputs,
                    "runtime_assembler_wrote_source_artifact",
                    artifact_ref,
                )
            elif creator["role"] == "supporting_writer":
                supporting_writer_outputs = artifact_role_contract[
                    "supporting_writer_outputs_by_skill"
                ].get(creator["skill"], [])
                require(
                    artifact["artifact_role"] in set(supporting_writer_outputs),
                    "runtime_supporting_writer_output_mismatch",
                    artifact_ref,
                )
            if artifact["artifact_role"] not in final_package_roles:
                validate_actor_output_role_runtime(
                    actor=creator,
                    artifact=artifact,
                    contract=artifact_role_contract,
                )
            if artifact_is_review_finding_report(
                creator_role=creator["role"],
                artifact_role=artifact["artifact_role"],
                contract=artifact_role_contract,
            ):
                review_output_artifacts.append(artifact)
        require(artifact["status"] == "frozen", "runtime_artifact_not_frozen", artifact_ref)
        if artifact["artifact_role"] in final_package_roles:
            final_package_count += 1
            final_package_artifacts.append(artifact)
            creator = actor_by_id.get(artifact["created_by_instance_id"])
            require(
                creator is not None
                and creator["skill"] == expected_final_skill
                and creator["role"] == expected_final_role,
                "runtime_final_package_creator_mismatch",
                artifact_ref,
            )
        if artifact["artifact_role"] == finding_index_role:
            finding_index_artifacts.append(artifact)
    for artifact in artifacts:
        for parent in artifact["based_on"]:
            require(
                parent in artifact_refs or (isinstance(parent, str) and parent.startswith("external:")),
                "runtime_lineage_dangling_parent",
                f"{receipt['receipt_id']}: {parent}",
            )
    evaluator_forbidden_source_roles = set(
        registry["scenario_eval_contract"]["blindness_policy"][
            "runtime_evaluator_forbidden_source_actor_roles"
        ]
    )
    reviewer_output_paths = {
        artifact["path"]
        for artifact in artifacts
        if artifact["created_by_instance_id"] in actor_by_id
        and actor_by_id[artifact["created_by_instance_id"]]["role"]
        in evaluator_forbidden_source_roles
    }
    parent_graph = {
        f"{artifact['artifact_id']}@{artifact['version_id']}": [
            parent for parent in artifact["based_on"] if parent in artifact_refs
        ]
        for artifact in artifacts
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit_artifact(artifact_ref: str) -> None:
        require(
            artifact_ref not in visiting,
            "runtime_lineage_cycle",
            f"{receipt['receipt_id']}: {artifact_ref}",
        )
        if artifact_ref in visited:
            return
        visiting.add(artifact_ref)
        for parent_ref in parent_graph[artifact_ref]:
            visit_artifact(parent_ref)
        visiting.remove(artifact_ref)
        visited.add(artifact_ref)

    for artifact_ref in sorted(artifact_refs):
        visit_artifact(artifact_ref)

    lineage = receipt["lineage"]
    require(lineage["complete"] is True, "runtime_lineage_incomplete", receipt["receipt_id"])
    require(lineage["current_artifact_ref"] in artifact_refs, "runtime_current_artifact_missing", receipt["receipt_id"])
    if lineage["evaluated_artifact_ref"] is not None:
        require(lineage["evaluated_artifact_ref"] in artifact_refs, "runtime_evaluated_artifact_missing", receipt["receipt_id"])
    artifacts_by_ref = {ref_for(artifact): artifact for artifact in artifacts}
    current_artifact = artifacts_by_ref[lineage["current_artifact_ref"]]
    current_idea_refs = (
        current_idea_refs_from_index(
            artifacts=artifacts,
            artifacts_by_ref=artifacts_by_ref,
            resolved_artifact_paths=resolved_artifact_paths,
            registry=registry,
            direction_profile=direction_profile,
            label=receipt["receipt_id"],
        )
        if receipt["workflow"] == "idea"
        else {lineage["current_artifact_ref"]}
    )
    require(
        lineage["current_artifact_ref"] in current_idea_refs,
        "runtime_current_artifact_missing",
        receipt["receipt_id"],
    )
    require(
        current_artifact["artifact_role"] == machine["primary_artifact_type"],
        "runtime_current_primary_role_mismatch",
        lineage["current_artifact_ref"],
    )
    primary_creator_skills = set(machine["primary_artifact_creator_skills"])
    if current_artifact["created_by_instance_id"] == "external-input":
        require(
            receipt["entry_mode"]
            in set(
                external_input_contract["external_primary_allowed_modes"][
                    receipt["workflow"]
                ]
            ),
            "runtime_current_primary_external_forbidden",
            receipt["entry_mode"],
        )
    else:
        require(
            current_artifact["source_skill"] in primary_creator_skills,
            "runtime_current_primary_creator_mismatch",
            lineage["current_artifact_ref"],
        )
    if receipt["case_kind"] == "happy" and receipt["entry_mode"] not in set(
        external_input_contract["external_primary_allowed_modes"][receipt["workflow"]]
    ):
        lineage_closure: set[str] = set()
        pending_lineage = [lineage["current_artifact_ref"]]
        while pending_lineage:
            candidate_ref = pending_lineage.pop()
            if candidate_ref in lineage_closure:
                continue
            lineage_closure.add(candidate_ref)
            pending_lineage.extend(parent_graph.get(candidate_ref, []))
        require(
            any(
                ref in artifacts_by_ref
                and artifacts_by_ref[ref]["source_skill"] in primary_creator_skills
                and artifacts_by_ref[ref]["created_by_instance_id"] != "external-input"
                for ref in lineage_closure
            ),
            "runtime_primary_writer_lineage_missing",
            receipt["receipt_id"],
        )

    file_access = receipt["file_access"]
    reads = file_access.get("reads")
    writes = file_access.get("writes")
    require(isinstance(reads, list) and bool(reads), "runtime_files_read_missing", receipt["receipt_id"])
    require(isinstance(writes, list) and bool(writes), "runtime_files_written_missing", receipt["receipt_id"])
    read_paths_by_actor: dict[str, set[str]] = {actor_id: set() for actor_id in actor_ids}
    write_paths_by_actor: dict[str, set[str]] = {actor_id: set() for actor_id in actor_ids}
    for access_kind, entries in (("read", reads), ("write", writes)):
        for entry in entries:
            require(isinstance(entry, dict), "runtime_file_access_schema", receipt["receipt_id"])
            require(
                entry.get("actor_instance_id") in actor_ids,
                "runtime_file_access_actor_missing",
                receipt["receipt_id"],
            )
            accessed_path = resolve_durable_file(
                entry,
                root=root,
                label=f"{receipt['receipt_id']}.{access_kind}:{entry.get('path')}",
            )
            if access_kind == "read":
                require(
                    entry.get("sha256_before") == entry["sha256"]
                    and entry.get("sha256_after") == entry["sha256"],
                    "runtime_source_artifact_hash_changed",
                    f"{receipt['receipt_id']}: {entry.get('path')}",
                )
                read_paths_by_actor[entry["actor_instance_id"]].add(entry["path"])
            else:
                write_paths_by_actor[entry["actor_instance_id"]].add(entry["path"])
                indexed_artifact = artifacts_by_path.get(entry["path"])
                require(
                    indexed_artifact is not None
                    and indexed_artifact["created_by_instance_id"]
                    == entry["actor_instance_id"],
                    "runtime_write_artifact_mismatch",
                    f"{receipt['receipt_id']}: {entry.get('path')}",
                )
            if access_kind == "write":
                scope_values = actor_by_id[entry["actor_instance_id"]][
                    "allowed_write_roots"
                ]
                missing_scope_code = "runtime_write_scope_missing"
                out_of_scope_code = "runtime_write_out_of_scope"
            else:
                scope_values = actor_by_id[entry["actor_instance_id"]][
                    "allowed_read_roots"
                ]
                missing_scope_code = "runtime_read_scope_missing"
                out_of_scope_code = "runtime_read_out_of_scope"
            require(bool(scope_values), missing_scope_code, receipt["receipt_id"])
            scope_match = False
            for scope_value in scope_values:
                require(
                    isinstance(scope_value, str) and scope_value,
                    missing_scope_code,
                    receipt["receipt_id"],
                )
                require(
                    "\\" not in scope_value,
                    "runtime_path_not_canonical_posix",
                    receipt["receipt_id"],
                )
                posix_scope = PurePosixPath(scope_value)
                require(
                    not posix_scope.is_absolute()
                    and bool(posix_scope.parts)
                    and "." not in posix_scope.parts
                    and ".." not in posix_scope.parts,
                    out_of_scope_code,
                    receipt["receipt_id"],
                )
                relative_scope = Path(*posix_scope.parts)
                allowed_root = (root.resolve() / relative_scope).resolve()
                try:
                    accessed_path.relative_to(allowed_root)
                except ValueError:
                    continue
                scope_match = True
                break
            require(scope_match, out_of_scope_code, receipt["receipt_id"])
    for artifact in artifacts:
        creator = artifact["created_by_instance_id"]
        if creator in actor_by_id:
            require(
                artifact["path"] in write_paths_by_actor[creator],
                "runtime_artifact_write_missing",
                f"{receipt['receipt_id']}: {artifact['path']}",
            )
    reviewer_like_ids = (
        actors_by_role["evaluator"]
        | actors_by_role["panel"]
        | actors_by_role["strategy_reviewer"]
        | actors_by_role["supporting_reviewer"]
        | actors_by_role["verifier_compositor"]
    )
    blind_reviewer_roles = set(
        registry["scenario_eval_contract"]["blindness_policy"][
            "runtime_blind_reviewer_actor_roles"
        ]
    )
    forbidden_oracle_roles = set(
        registry["scenario_eval_contract"]["blindness_policy"][
            "runtime_forbidden_oracle_artifact_roles"
        ]
    )
    for reviewer_id in reviewer_like_ids:
        indexed_reviewer_writes = {
            artifact["path"]
            for artifact in artifacts
            if artifact["created_by_instance_id"] == reviewer_id
        }
        require(indexed_reviewer_writes, "runtime_reviewer_output_missing", reviewer_id)
        require(
            write_paths_by_actor[reviewer_id] == indexed_reviewer_writes,
            "runtime_reviewer_write_set_mismatch",
            reviewer_id,
        )
        require(read_paths_by_actor[reviewer_id], "runtime_reviewer_read_missing", reviewer_id)
        require(
            not (read_paths_by_actor[reviewer_id] & write_paths_by_actor[reviewer_id]),
            "runtime_reviewer_modified_input",
            reviewer_id,
        )
        if actor_by_id[reviewer_id]["role"] in blind_reviewer_roles:
            validate_blind_reviewer_inputs_runtime(
                reviewer_id=reviewer_id,
                read_paths=read_paths_by_actor[reviewer_id],
                artifacts_by_path=artifacts_by_path,
                forbidden_oracle_roles=forbidden_oracle_roles,
            )
        if reviewer_id in actors_by_role["panel"]:
            require(
                all(
                    artifacts_by_path[path]["artifact_role"]
                    not in review_output_roles
                    for path in read_paths_by_actor[reviewer_id]
                    if path in artifacts_by_path
                ),
                "runtime_panel_peer_output_visible",
                reviewer_id,
            )
        if reviewer_id in actors_by_role["strategy_reviewer"]:
            require(
                all(
                    artifacts_by_path[path]["artifact_role"]
                    not in review_output_roles
                    for path in read_paths_by_actor[reviewer_id]
                    if path in artifacts_by_path
                ),
                "runtime_strategy_reviewer_peer_output_visible",
                reviewer_id,
            )
        if reviewer_id in actors_by_role["supporting_reviewer"]:
            require(
                all(
                    artifacts_by_path[path]["artifact_role"]
                    not in review_output_roles
                    for path in read_paths_by_actor[reviewer_id]
                    if path in artifacts_by_path
                ),
                "runtime_supporting_reviewer_prior_review_visible",
                reviewer_id,
            )
    for evaluator_id in actors_by_role["evaluator"]:
        forbidden_reads = (
            read_paths_by_actor[evaluator_id] & reviewer_output_paths
        )
        require(
            not forbidden_reads,
            "runtime_evaluator_prior_review_visible",
            f"{evaluator_id}: {sorted(forbidden_reads)}",
        )
    require(
        file_access["source_artifact_hashes_unchanged"] is True,
        "runtime_source_artifact_edited",
        receipt["receipt_id"],
    )
    access_attestation = task_export_document.get("file_access_attestation", {})
    require(
        isinstance(access_attestation, dict)
        and access_attestation.get("source_artifact_hashes_unchanged") is True
        and access_attestation.get("files_read_count") == len(reads)
        and access_attestation.get("files_written_count") == len(writes),
        "runtime_task_export_access_attestation_mismatch",
        receipt["receipt_id"],
    )
    validate_verifier_compositor_internal_outputs_runtime(
        artifacts=artifacts,
        actor_by_id=actor_by_id,
        read_paths_by_actor=read_paths_by_actor,
        contract=artifact_role_contract,
    )

    review_state = receipt["review_state"]
    dissent = set(review_state["dissent_ids"])
    preserved = set(review_state["preserved_dissent_ids"])
    fatal = set(review_state["fatal_finding_ids"])
    unresolved_fatal = set(review_state["unresolved_fatal_finding_ids"])
    observed_dissent: set[str] = set()
    observed_fatal: set[str] = set()
    observed_unresolved_fatal: set[str] = set()
    evaluator_inputs: set[str] = set()
    panel_inputs: set[str] = set()
    review_inputs_by_actor: dict[str, set[str]] = {}
    strategy_cells_by_ref: dict[str, set[tuple[str, str]]] = {}
    review_outputs_by_actor: dict[str, int] = Counter()
    review_reports_by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    review_pass_by_actor: dict[str, bool] = {}
    review_unresolved_by_actor: dict[str, set[str]] = {}
    finding_provenance: dict[str, dict[str, Any]] = {}
    for artifact in review_output_artifacts:
        report = load_structured_file(resolved_artifact_paths[artifact["path"]])
        creator_id = artifact["created_by_instance_id"]
        creator = actor_by_id[creator_id]
        require(report.get("schema_version") == 1, "runtime_review_output_schema", artifact["path"])
        require(
            report.get("reviewer_instance_id") == creator_id
            and report.get("round_id") == creator.get("round_id")
            and report.get("source_edits_performed") is False,
            "runtime_review_output_identity_mismatch",
            artifact["path"],
        )
        require(
            report.get("prior_scores_visible") is False,
            "runtime_prior_scores_visible",
            artifact["path"],
        )
        if creator["role"] in independent_reviewer_actor_roles:
            require(
                report.get("isolation_mode")
                == independent_reviewer_isolation_mode,
                "runtime_reviewer_report_isolation_mismatch",
                artifact["path"],
            )
        if creator["role"] == "panel":
            require(
                report.get("panel_tier") == creator.get("panel_tier")
                and report.get("panel_role") == creator.get("panel_role"),
                "runtime_panel_role_mismatch",
                artifact["path"],
            )
        elif creator["role"] == "strategy_reviewer":
            require(
                report.get("strategy_role") == creator.get("strategy_role")
                and report.get("peer_outputs_visible") is False,
                "runtime_strategy_reviewer_role_mismatch",
                artifact["path"],
            )
            if receipt["workflow"] == "research_polisher":
                strategy_cells_by_ref[ref_for(artifact)] = (
                    validate_research_polisher_strategy_report_runtime(
                        report,
                        creator,
                        artifact_role_contract,
                        artifact["path"],
                    )
                )
        input_refs = report.get("input_artifact_refs")
        require(
            isinstance(input_refs, list)
            and bool(input_refs)
            and set(input_refs) <= artifact_refs
            and set(input_refs) <= set(artifact["based_on"]),
            "runtime_review_output_inputs_invalid",
            artifact["path"],
        )
        expected_read_paths = {
            artifacts_by_ref[input_ref]["path"] for input_ref in input_refs
        }
        require(
            read_paths_by_actor[creator_id] == expected_read_paths,
            "runtime_review_input_read_mismatch",
            (
                f"{creator_id}: claimed={sorted(expected_read_paths)}, "
                f"actual={sorted(read_paths_by_actor[creator_id])}"
            ),
        )
        (
            report_dissent,
            report_fatal,
            report_unresolved_fatal,
            report_unresolved,
        ) = validate_runtime_review_report_findings(
            report, artifact_role_contract, artifact["path"]
        )
        validate_review_extension(
            payload=report,
            reviewer_skill=creator["skill"],
            expected_artifacts=[artifacts_by_ref[input_ref] for input_ref in input_refs],
            registry=registry,
            digest_field="sha256",
            error_code="runtime_review_extension_invalid",
            label=artifact["path"],
        )
        observed_dissent.update(report_dissent)
        observed_fatal.update(report_fatal)
        observed_unresolved_fatal.update(report_unresolved_fatal)
        require(
            review_outputs_by_actor[creator_id] == 0,
            "runtime_reviewer_multiple_reports",
            creator_id,
        )
        review_pass_by_actor[creator_id] = validate_runtime_review_decision(
            report, creator, registry, artifact["path"]
        )
        review_unresolved_by_actor[creator_id] = report_unresolved
        report_record = {
            "artifact": artifact,
            "report": report,
            "creator": creator,
            "input_refs": set(input_refs),
            "decision_pass": review_pass_by_actor[creator_id],
        }
        review_reports_by_skill[creator["skill"]].append(report_record)
        for finding in report["findings"]:
            require(
                finding["id"] not in finding_provenance,
                "runtime_review_finding_id_reused",
                finding["id"],
            )
            finding_provenance[finding["id"]] = {
                **report_record,
                "finding": finding,
            }
        review_outputs_by_actor[creator_id] += 1
        review_inputs_by_actor[creator_id] = set(input_refs)
        if creator["role"] == "evaluator":
            evaluator_inputs.update(input_refs)
        elif creator["role"] == "panel":
            panel_inputs.update(input_refs)
    for reviewer_id in (
        actors_by_role["evaluator"]
        | actors_by_role["panel"]
        | actors_by_role["strategy_reviewer"]
        | actors_by_role["supporting_reviewer"]
        | actors_by_role["verifier_compositor"]
    ):
        require(
            review_outputs_by_actor[reviewer_id] == 1,
            "runtime_reviewer_output_missing",
            reviewer_id,
        )
    if receipt["workflow"] == "research_polisher":
        validate_research_polisher_portfolio_lineage_runtime(
            artifacts=artifacts,
            actor_by_id=actor_by_id,
            strategy_cells_by_ref=strategy_cells_by_ref,
            read_paths_by_actor=read_paths_by_actor,
            contract=artifact_role_contract,
        )
    if receipt["case_kind"] == "happy":
        require(
            current_idea_refs <= evaluator_inputs,
            "runtime_current_version_review_missing",
            receipt["receipt_id"],
        )
        if expected_panel_skill is not None:
            require(
                panel_inputs == current_idea_refs
                and all(
                    review_inputs_by_actor[panel_instance]
                    == current_idea_refs
                    for panel_instance in panel_role_instances.values()
                ),
                "runtime_current_version_review_missing",
                receipt["receipt_id"],
            )
        require(
            any(ref != lineage["current_artifact_ref"] for ref in evaluator_inputs),
            "runtime_fresh_evaluator_round_missing",
            receipt["receipt_id"],
        )
        current_evaluators = {
            actor_id
            for actor_id in actors_by_role["evaluator"]
            if current_idea_refs.intersection(
                review_inputs_by_actor.get(actor_id, set())
            )
        }
        ready_decision_actor_ids = (
            current_evaluators
            | set(panel_role_instances.values())
            | actors_by_role["strategy_reviewer"]
            | actors_by_role["supporting_reviewer"]
            | actors_by_role["verifier_compositor"]
        )
        require(
            bool(current_evaluators)
            and all(
                review_pass_by_actor.get(actor_id) is True
                and not review_unresolved_by_actor.get(actor_id, set())
                for actor_id in ready_decision_actor_ids
            ),
            "runtime_ready_review_decision_not_pass",
            receipt["receipt_id"],
        )
        if receipt["workflow"] == "idea" and workflow_conditions.get(
            "proposal_handoff_candidate", False
        ):
            handoff = machine["proposal_handoff_contract"]
            current_reports = [
                record
                for record in review_reports_by_skill[machine["evaluator_skill"]]
                if record["input_refs"] <= current_idea_refs
                and bool(record["input_refs"])
            ]
            require(
                direction_profile in set(handoff["eligible_direction_profiles"])
                and len(current_reports) == len(current_idea_refs)
                and all(
                    record["report"].get("decision")
                    == handoff["required_current_evaluation_decision"]
                    and record["artifact"].get("change_type")
                    == "fresh_independent_evaluation"
                    and record["report"].get("reviewed_dossier_digest")
                    == artifacts_by_ref[next(iter(record["input_refs"]))]["sha256"]
                    for record in current_reports
                ),
                "runtime_idea_proposal_handoff_evaluation_invalid",
                receipt["receipt_id"],
            )
        for required_skill in case_contract["required_review_skills"]:
            require(
                bool(review_reports_by_skill.get(required_skill)),
                "runtime_happy_required_independent_gate_missing",
                f"{receipt['receipt_id']}: {required_skill}",
            )

    require(
        dissent == observed_dissent
        and fatal == observed_fatal
        and unresolved_fatal == observed_unresolved_fatal,
        "runtime_review_state_mismatch",
        receipt["receipt_id"],
    )
    require(
        len(finding_index_artifacts) == 1,
        "runtime_finding_index_missing",
        receipt["receipt_id"],
    )
    finding_index = load_structured_file(
        resolved_artifact_paths[finding_index_artifacts[0]["path"]]
    )
    require(
        finding_index.get("schema_version") == 1
        and finding_index.get("task_id") == task_export["task_id"]
        and set(finding_index.get("dissent_ids", [])) == dissent
        and set(finding_index.get("preserved_dissent_ids", [])) == preserved
        and set(finding_index.get("fatal_finding_ids", [])) == fatal
        and set(finding_index.get("unresolved_fatal_finding_ids", []))
        == unresolved_fatal,
        "runtime_finding_index_mismatch",
        receipt["receipt_id"],
    )
    require(dissent <= preserved, "runtime_dissent_not_preserved", receipt["receipt_id"])
    require(unresolved_fatal <= fatal, "runtime_fatal_finding_index_invalid", receipt["receipt_id"])
    require(review_state["fatal_findings_visible"] is True, "runtime_fatal_findings_hidden", receipt["receipt_id"])
    require(
        receipt["final_state"]
        == (
            workflow_final_state_for(
                receipt["workflow"], registry, direction_profile
            )
            if receipt["case_kind"] == "happy"
            else case_contract["expected_final_state"]
        ),
        "runtime_final_state_mismatch",
        receipt["receipt_id"],
    )
    require(
        receipt["automatic_external_submission"] is False,
        "runtime_external_submission",
        receipt["receipt_id"],
    )
    control_evidence = receipt.get("control_evidence")
    require(isinstance(control_evidence, dict), "runtime_control_contract", receipt["receipt_id"])
    control_fields = (
        "input_condition",
        "gate",
        "finding",
        "route",
        "continuation_artifact_ref",
    )
    if receipt["case_kind"] == "happy":
        require(
            all(control_evidence.get(field) is None for field in control_fields),
            "runtime_happy_control_evidence_present",
            receipt["receipt_id"],
        )
        require(
            receipt["final_state"]
            == workflow_final_state_for(
                receipt["workflow"], registry, direction_profile
            ),
            "runtime_happy_not_ready",
            receipt["receipt_id"],
        )
        validate_ready_has_no_unresolved_fatal(
            unresolved_fatal, receipt["receipt_id"]
        )
        require(
            lineage["evaluated_artifact_ref"] == lineage["current_artifact_ref"],
            "runtime_stale_evaluation",
            receipt["receipt_id"],
        )
        require(final_package_count == 1, "runtime_final_package_missing", receipt["receipt_id"])
        for artifact in final_package_artifacts:
            package = load_structured_file(resolved_artifact_paths[artifact["path"]])
            package_parent_refs = set(artifact["based_on"])
            package_parent_artifacts = [
                candidate
                for candidate in artifacts
                if ref_for(candidate) in package_parent_refs
            ]
            package_creator_id = artifact["created_by_instance_id"]
            package_contract = registry["scenario_eval_contract"]["package_input_contracts"][
                receipt["workflow"]
            ]
            require(
                len(package_parent_artifacts) == len(package_parent_refs)
                and all(
                    candidate["artifact_role"] in set(package_contract["allowed_roles"])
                    for candidate in package_parent_artifacts
                ),
                "runtime_package_input_not_allowed",
                receipt["receipt_id"],
            )
            require(
                {candidate["path"] for candidate in package_parent_artifacts}
                <= read_paths_by_actor[package_creator_id],
                "runtime_package_input_not_read",
                receipt["receipt_id"],
            )
            for rule in package_contract["required_inputs"]:
                matches = package_rule_matches(
                    package_parent_artifacts,
                    rule,
                    current_ref=lineage["current_artifact_ref"],
                    current_idea_refs=current_idea_refs,
                )
                minimum_count, maximum_count = package_rule_count_bounds(
                    rule,
                    direction_profile=direction_profile,
                    current_idea_count=len(current_idea_refs),
                    panel_role_count=len(expected_panel_roles),
                    workflow_conditions=workflow_conditions,
                )
                require(
                    len(matches) >= minimum_count
                    and (maximum_count is None or len(matches) <= maximum_count),
                    "runtime_package_required_input_missing",
                    f"{receipt['receipt_id']}: {rule}",
                )
                if rule.get("current_by_idea_index"):
                    require(
                        {ref_for(item) for item in matches} == current_idea_refs,
                        "runtime_package_current_idea_set_mismatch",
                        receipt["receipt_id"],
                    )
                if rule.get("all_panel_instances"):
                    require(
                        len(matches) == len(expected_panel_roles),
                        "runtime_package_panel_input_incomplete",
                        receipt["receipt_id"],
                    )
                if rule.get("include_all_created"):
                    all_matching = package_rule_matches(
                        artifacts,
                        rule,
                        current_ref=lineage["current_artifact_ref"],
                        current_idea_refs=current_idea_refs,
                    )
                    require(
                        {ref_for(item) for item in all_matching} <= package_parent_refs,
                        "runtime_package_input_omitted",
                        receipt["receipt_id"],
                    )
            if receipt["workflow"] == "proposal":
                validate_proposal_sap_package_runtime(
                    package_parent_artifacts=package_parent_artifacts,
                    artifacts=artifacts,
                    actor_by_id=actor_by_id,
                )
            require(
                package.get("schema_version") == 1
                and package.get("final_state") == receipt["final_state"]
                and package.get("source_edits_performed") is False
                and package.get("source_identity_unchanged") is True
                and set(package.get("input_artifact_refs", [])) == package_parent_refs
                and set(package.get("preserved_dissent_ids", [])) >= dissent
                and set(package.get("unresolved_fatal_finding_ids", []))
                == unresolved_fatal,
                "runtime_final_package_state_mismatch",
                receipt["receipt_id"],
            )
    else:
        require(
            all(
                isinstance(control_evidence.get(field), str)
                and bool(control_evidence[field].strip())
                for field in control_fields
            ),
            "runtime_control_contract",
            receipt["receipt_id"],
        )
        continuation_ref = control_evidence["continuation_artifact_ref"]
        continuation = next(
            (artifact for artifact in artifacts if ref_for(artifact) == continuation_ref),
            None,
        )
        require(
            continuation is not None
            and continuation["artifact_role"]
            == case_contract["continuation_artifact_role"]
            and continuation["source_skill"] == machine["orchestrator"],
            "runtime_control_continuation_type_mismatch",
            receipt["receipt_id"],
        )
        require(
            receipt["final_state"] == case_contract["expected_final_state"],
            "runtime_control_invalid_state",
            receipt["receipt_id"],
        )
        require(final_package_count == 0, "runtime_control_false_ready", receipt["receipt_id"])
        validate_control_independent_gates_runtime(
            workflow=receipt["workflow"],
            case_contract=case_contract,
            current_ref=lineage["current_artifact_ref"],
            control_finding_id=control_evidence["finding"],
            review_reports_by_skill=review_reports_by_skill,
            finding_provenance=finding_provenance,
            strategy_role_instances=strategy_role_instances,
            strategy_cells_by_ref=strategy_cells_by_ref,
            registry=registry,
        )
        if receipt["final_state"] == "blocked":
            require(bool(unresolved_fatal), "runtime_blocked_without_fatal", receipt["receipt_id"])

    return {
        "receipt_id": receipt["receipt_id"],
        "workflow": receipt["workflow"],
        "case_kind": receipt["case_kind"],
        "status": "verified",
        "verification_level": verification_level,
        "evidence_accounting_status": evidence_accounting_status,
        "external_evidence_id": external_evidence_id,
        "external_live_result_digest": external_live_result_digest,
        "external_verifier_workflow_run_id": external_verifier_workflow_run_id,
        "external_verified_at": external_verified_at,
        "platform": task_export["platform"],
        "task_id": task_export["task_id"],
        "task_export_path": task_export["path"],
        "task_export_sha256": task_export["sha256"],
        "source_commit": binding["source_commit"],
        "actor_counts": {role: len(ids) for role, ids in actors_by_role.items()},
        "artifact_count": len(artifacts),
        "files_read_count": len(reads),
        "files_written_count": len(writes),
        "final_state": receipt["final_state"],
        "dissent_count": len(dissent),
        "unresolved_fatal_count": len(unresolved_fatal),
    }


def authenticated_platform_adapter_available(
    collection: dict[str, Any],
    *,
    supported_adapter_ids: frozenset[str] = SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS,
) -> bool:
    platform_trust = collection.get("platform_trust", {})
    if not isinstance(platform_trust, dict):
        return False
    adapter_id = platform_trust.get("adapter_id")
    return (
        platform_trust.get("adapter_status") == "configured"
        and platform_trust.get("verification_level") == PROVIDER_VERIFIED
        and platform_trust.get("provider_authenticated") is True
        and isinstance(adapter_id, str)
        and adapter_id in supported_adapter_ids
    )


def preview_attestation_adapter_available(
    collection: dict[str, Any],
    *,
    supported_adapter_ids: frozenset[str] = SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS,
) -> bool:
    platform_trust = collection.get("platform_trust", {})
    if not isinstance(platform_trust, dict):
        return False
    adapter_id = platform_trust.get("adapter_id")
    return (
        platform_trust.get("adapter_status") == "configured"
        and platform_trust.get("verification_level") == PREVIEW_ATTESTED
        and platform_trust.get("provider_authenticated") is False
        and isinstance(adapter_id, str)
        and adapter_id in supported_adapter_ids
    )


def configured_runtime_verification_level(
    collection: dict[str, Any],
    *,
    supported_preview_adapter_ids: frozenset[str] = SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS,
    supported_provider_adapter_ids: frozenset[str] = SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS,
) -> str | None:
    if authenticated_platform_adapter_available(
        collection, supported_adapter_ids=supported_provider_adapter_ids
    ):
        return PROVIDER_VERIFIED
    if preview_attestation_adapter_available(
        collection, supported_adapter_ids=supported_preview_adapter_ids
    ):
        return PREVIEW_ATTESTED
    return None


def accepted_runtime_verification_level(
    collection: dict[str, Any],
    external_runtime_session: ExternalRuntimeValidationSession | None,
) -> str | None:
    """Return a report-eligible level only from the opaque live session."""

    configured = configured_runtime_verification_level(collection)
    if external_runtime_session is None:
        return None
    require(
        _is_valid_external_runtime_validation_session(external_runtime_session)
        and configured == external_runtime_session.verification_level,
        "runtime_external_session_verification_level_mismatch",
        f"configured={configured} session={getattr(external_runtime_session, 'verification_level', None)}",
    )
    return external_runtime_session.verification_level


def validate_runtime_collection(
    collection: dict[str, Any],
    *,
    schema: dict[str, Any],
    registry: dict[str, Any],
    expected_source_commit: str | None,
    root: Path,
    supported_preview_adapter_ids: frozenset[str] = SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS,
    supported_provider_adapter_ids: frozenset[str] = SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS,
    validated_evidence_results: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    collection_contract = schema["x-phase7-contract"].get("collection_contract", {})
    required_collection_flags = {
        "receipt_ids_unique",
        "all_ten_runs_are_fresh_tasks",
        "platform_task_ids_unique",
        "task_export_paths_unique",
        "task_export_digests_unique",
        "task_export_binds_receipt_identity",
        "task_export_binds_actor_manifest",
        "task_export_binds_artifact_index",
        "verified_receipts_share_one_release_identity",
        "verified_receipts_share_one_verification_level",
        "preview_attested_is_not_provider_verified",
    }
    require(
        all(collection_contract.get(field) is True for field in required_collection_flags),
        "runtime_collection_contract_incomplete",
        str(sorted(required_collection_flags - set(collection_contract))),
    )
    missing_top = sorted(set(schema["required"]) - set(collection))
    require(not missing_top, "runtime_collection_schema", str(missing_top))
    require(collection["schema_version"] == 2, "runtime_collection_schema", "schema_version")
    require(
        collection["evidence_kind"] == "current_version_durable_runtime_receipts",
        "runtime_collection_schema",
        "evidence_kind",
    )
    platform_trust = collection.get("platform_trust", {})
    require(
        isinstance(platform_trust, dict),
        "runtime_platform_trust_schema",
        "platform_trust",
    )
    required_trust_fields = {
        "adapter_status",
        "adapter_id",
        "verification_level",
        "provider_authenticated",
        "reason",
    }
    require(
        isinstance(platform_trust, dict)
        and required_trust_fields <= set(platform_trust),
        "runtime_platform_trust_schema",
        str(sorted(required_trust_fields - set(platform_trust))),
    )
    configured_verification_level = configured_runtime_verification_level(
        collection,
        supported_preview_adapter_ids=supported_preview_adapter_ids,
        supported_provider_adapter_ids=supported_provider_adapter_ids,
    )
    require(
        isinstance(platform_trust.get("reason"), str)
        and bool(platform_trust["reason"].strip()),
        "runtime_platform_trust_schema",
        "reason",
    )
    receipts = collection["receipts"]
    require(isinstance(receipts, list) and len(receipts) == 10, "runtime_receipt_count", str(len(receipts)))
    required_pairs = [tuple(pair) for pair in schema["x-phase7-contract"]["required_workflow_case_pairs"]]
    actual_pairs = [(receipt.get("workflow"), receipt.get("case_kind")) for receipt in receipts]
    require(
        Counter(actual_pairs) == Counter(required_pairs),
        "runtime_receipt_pair_coverage",
        str(actual_pairs),
    )
    receipt_ids = [receipt.get("receipt_id") for receipt in receipts]
    require(len(receipt_ids) == len(set(receipt_ids)), "runtime_receipt_id_reused", str(receipt_ids))

    results = []
    for receipt in receipts:
        required = schema["$defs"]["runtime_receipt"]["required"]
        missing = sorted(set(required) - set(receipt))
        require(not missing, "runtime_receipt_schema", f"{receipt.get('receipt_id')}: {missing}")
        validate_runtime_receipt_declaration(receipt, schema, registry)
        require(
            receipt["status"] in {"pending_live_evidence", "verified"},
            "runtime_receipt_status",
            receipt["receipt_id"],
        )
        require(
            isinstance(receipt["reason"], str) and bool(receipt["reason"].strip()),
            "runtime_receipt_reason_missing",
            receipt["receipt_id"],
        )
        if receipt["status"] == "verified":
            evidence_result = (validated_evidence_results or {}).get(
                receipt["receipt_id"]
            )
            require(
                configured_verification_level is not None,
                "runtime_platform_trust_unavailable",
                receipt["receipt_id"],
            )
            require(
                evidence_result is not None,
                "runtime_evidence_validation_missing",
                receipt["receipt_id"],
            )
            if isinstance(evidence_result, EvidenceValidationResult):
                raise ModeViolation(
                    "runtime_evidence_authenticated_attestation_missing",
                    receipt["receipt_id"],
                )
            require(
                _is_valid_external_runtime_attestation(evidence_result)
                or _is_valid_test_only_attestation(evidence_result),
                "runtime_evidence_attestation_type_invalid",
                receipt["receipt_id"],
            )
            require(
                evidence_result.verification_level
                == configured_verification_level,
                "runtime_verification_level_mismatch",
                receipt["receipt_id"],
            )
            results.append(
                validate_runtime_receipt(
                    receipt,
                    registry=registry,
                    schema=schema,
                    expected_source_commit=expected_source_commit,
                    root=root,
                    evidence_result=evidence_result,
                )
            )
        else:
            require(
                receipt.get("verification_level") is None
                and receipt.get("attestation") is None,
                "runtime_pending_receipt_claims_evidence",
                receipt["receipt_id"],
            )
            results.append(
                {
                    "receipt_id": receipt["receipt_id"],
                    "workflow": receipt["workflow"],
                    "case_kind": receipt["case_kind"],
                    "status": "pending_live_evidence",
                    "reason": receipt["reason"],
                }
            )
    verified = [item for item in results if item["status"] == "verified"]
    verified_levels = {item["verification_level"] for item in verified}
    require(
        len(verified_levels) <= 1
        and (
            not verified_levels
            or verified_levels == {configured_verification_level}
        ),
        "runtime_mixed_verification_levels",
        str(sorted(verified_levels)),
    )
    for field in ("task_id", "task_export_path", "task_export_sha256"):
        values = [item[field] for item in verified]
        require(
            len(values) == len(set(values)),
            "runtime_fresh_task_reused",
            field,
        )
    platform_task_ids = [(item["platform"], item["task_id"]) for item in verified]
    require(
        len(platform_task_ids) == len(set(platform_task_ids)),
        "runtime_fresh_task_reused",
        "platform+task_id",
    )
    return results


def write_json_file(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _build_test_only_attested_evidence(
    *,
    raw_payload: bytes,
    registry: dict[str, Any],
    source_commit: str,
    verification_level: str,
    raw_evidence_kind: str = "task_export",
) -> _TestOnlyAuthenticatedAttestation:
    """Build R->E->V->I, then simulate a scoped outer attestation."""

    require(
        verification_level in ACCEPTANCE_LEVELS,
        "synthetic_evidence_level",
        verification_level,
    )
    source_identity = {
        "plugin_version": registry["plugin_version"],
        "source_commit": source_commit,
        "manifest_sha256": "sha256:" + "1" * 64,
        "registry_sha256": sha256_repository_file(REGISTRY_PATH),
        "skill_tree_sha256": "sha256:" + "2" * 64,
    }
    payloads: dict[int, bytes] = {101: raw_payload}
    asset_records: list[dict[str, Any]] = [
        {
            "asset_id": 101,
            "name": "synthetic-task-export.json",
            "sha256": evidence_sha256_bytes(raw_payload),
            "size": len(raw_payload),
            "evidence_kind": raw_evidence_kind,
        }
    ]
    provider_payload: bytes | None = None
    if verification_level == PROVIDER_VERIFIED:
        provider_payload = b'{"provider":"synthetic-self-test"}\n'
        payloads[102] = provider_payload
        asset_records.append(
            {
                "asset_id": 102,
                "name": "synthetic-provider-receipt.json",
                "sha256": evidence_sha256_bytes(provider_payload),
                "size": len(provider_payload),
                "evidence_kind": "provider_receipt",
            }
        )
    capture = {
        "surface": "codex",
        "task_or_thread_id": "phase7-synthetic-self-test",
        "captured_at": "2026-07-13T00:00:00Z",
        "raw_export_asset_id": 101,
        "raw_export_sha256": evidence_sha256_bytes(raw_payload),
    }
    if verification_level == PROVIDER_VERIFIED:
        capture["provider_receipt_asset_id"] = 102
    envelope = {
        "schema_version": "openai-preview-evidence-envelope/v1",
        "evidence_id": f"phase7-{verification_level}-self-test",
        "verification_level": verification_level,
        "provider_verified": verification_level == PROVIDER_VERIFIED,
        "counts_as_preview_acceptance": True,
        "source_identity": source_identity,
        "adapter": {
            "adapter_id": "phase7-synthetic-capture",
            "adapter_code_sha256": "sha256:" + "3" * 64,
        },
        "capture": capture,
        "github_witness": {
            "repository": "xuxu-wei/research-skills",
            "release_id": 7001,
            "release_tag": "phase7-synthetic-self-test",
            "workflow_run_id": 7002,
            "actor": "phase7-self-test",
            "raw_export_asset_id": 101,
            "source_commit": source_commit,
        },
        "expected_verifier": {
            "verifier_id": "phase7-independent-self-test",
            "verifier_code_sha256": "sha256:" + "4" * 64,
            "independent": True,
        },
    }
    envelope_bytes = canonical_json_bytes(envelope)
    payloads[103] = envelope_bytes
    asset_records.append(
        {
            "asset_id": 103,
            "name": "synthetic-evidence-envelope.json",
            "sha256": evidence_sha256_bytes(envelope_bytes),
            "size": len(envelope_bytes),
            "evidence_kind": "evidence_envelope",
        }
    )
    verifier_report = {
        "schema_version": "openai-preview-verifier-report/v1",
        "verifier_id": "phase7-independent-self-test",
        "verifier_code_sha256": "sha256:" + "4" * 64,
        "independent": True,
        "verified_at": "2026-07-13T00:02:00Z",
        "verdict": "accepted",
        "source_identity": source_identity,
        "envelope_asset_id": 103,
        "envelope_sha256": evidence_sha256_bytes(envelope_bytes),
        "raw_export_asset_id": 101,
        "raw_export_sha256": evidence_sha256_bytes(raw_payload),
    }
    if verification_level == PROVIDER_VERIFIED:
        require(
            provider_payload is not None,
            "synthetic_provider_payload_missing",
            verification_level,
        )
        verifier_report.update(
            {
                "provider_receipt_asset_id": 102,
                "provider_receipt_sha256": evidence_sha256_bytes(
                    provider_payload
                ),
                "provider_attestation_checked": True,
            }
        )
    verifier_report_bytes = canonical_json_bytes(verifier_report)
    payloads[104] = verifier_report_bytes
    asset_records.append(
        {
            "asset_id": 104,
            "name": "synthetic-verifier-report.json",
            "sha256": evidence_sha256_bytes(verifier_report_bytes),
            "size": len(verifier_report_bytes),
            "evidence_kind": "verifier_report",
        }
    )
    index = {
        "schema_version": "openai-preview-release-asset-index/v1",
        "source_identity": source_identity,
        "github_release": {
            "repository": "xuxu-wei/research-skills",
            "release_id": 7001,
            "release_tag": "phase7-synthetic-self-test",
        },
        "github_witness": {
            "workflow_run_id": 7002,
            "actor": "phase7-self-test",
            "source_commit": source_commit,
            "witnessed_at": "2026-07-13T00:01:00Z",
        },
        "assets": asset_records,
    }
    index_bytes = canonical_json_bytes(index)
    integrity_result = validate_evidence_bundle(
        envelope,
        index,
        lambda record: payloads[int(record["asset_id"])],
        envelope_bytes=envelope_bytes,
        expected_source_identity=source_identity,
        index_bytes=index_bytes,
        now=datetime(2026, 7, 13, 1, 0, 0, tzinfo=timezone.utc),
    )
    return _issue_test_only_authenticated_attestation(
        integrity_result,
        verification_level=verification_level,
        capability=_SYNTHETIC_ATTESTATION_CAPABILITY,
    )


def _build_legacy_runtime_validator_fixture(
    root: Path, registry: dict[str, Any], source_commit: str
) -> dict[str, Any]:
    evidence = root / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    identity = {
        "task_id": "validator-self-test",
        "plugin_version": registry["plugin_version"],
        "registry_sha256": sha256_repository_file(REGISTRY_PATH),
        "source_commit": source_commit,
    }
    task_export = evidence / "task-export.json"
    primary_v1 = evidence / "primary-v1.md"
    primary_v2 = evidence / "primary-v2.md"
    evaluator_v1 = evidence / "evaluator-v1.json"
    evaluator_v2 = evidence / "evaluator-v2.json"
    panel_report = evidence / "panel-report.json"
    finding_index = evidence / "finding-index.json"
    final_package = evidence / "final-package.json"
    primary_v1.write_text("complete Idea dossier v1\n", encoding="utf-8")
    primary_v2.write_text("complete Idea dossier v2\n", encoding="utf-8")
    write_json_file(
        evaluator_v1,
        {
            "schema_version": 1,
            "reviewer_instance_id": "evaluator-001",
            "round_id": "round-001",
            "isolation_mode": "fresh_subagent",
            "input_artifact_refs": ["primary@v001"],
            "decision": "revise",
            "findings": [],
            "unresolved_issues": [],
            "dissent_ids": [],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
            "prior_scores_visible": False,
            "source_edits_performed": False,
            "reviewed_dossier_digest": sha256_file(primary_v1),
            "complete_dossier_confirmed": True,
            "dossier_only_input_confirmed": True,
        },
    )
    write_json_file(
        evaluator_v2,
        {
            "schema_version": 1,
            "reviewer_instance_id": "evaluator-002",
            "round_id": "round-002",
            "isolation_mode": "fresh_subagent",
            "input_artifact_refs": ["primary@v002"],
            "decision": "promote",
            "findings": [],
            "unresolved_issues": [],
            "dissent_ids": [],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
            "prior_scores_visible": False,
            "source_edits_performed": False,
            "reviewed_dossier_digest": sha256_file(primary_v2),
            "complete_dossier_confirmed": True,
            "dossier_only_input_confirmed": True,
        },
    )
    write_json_file(
        panel_report,
        {
            "schema_version": 1,
            "reviewer_instance_id": "panel-001",
            "round_id": "round-002-panel",
            "isolation_mode": "fresh_subagent",
            "input_artifact_refs": ["primary@v002"],
            "decision": "handoff_ready",
            "findings": [
                {
                    "id": "dissent-001",
                    "severity": "minor",
                    "blocking": False,
                    "resolved": False,
                    "dissent": True,
                }
            ],
            "unresolved_issues": [],
            "dissent_ids": ["dissent-001"],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
            "prior_scores_visible": False,
            "source_edits_performed": False,
        },
    )
    write_json_file(
        finding_index,
        {
            "schema_version": 1,
            "task_id": identity["task_id"],
            "dissent_ids": ["dissent-001"],
            "preserved_dissent_ids": ["dissent-001"],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
        },
    )
    write_json_file(
        final_package,
        {
            "schema_version": 1,
            "final_state": "human_signoff_required",
            "preserved_dissent_ids": ["dissent-001"],
            "unresolved_fatal_finding_ids": [],
        },
    )

    actor_manifest = evidence / "actor-manifest.json"
    write_json_file(
        actor_manifest,
        {
            "schema_version": 1,
            "workflow": "idea",
            "entry_mode": "standard",
            **identity,
            "actors": [
                {
                    "instance_id": "writer-001",
                    "skill": "multi-path-idea-generator",
                    "role": "writer",
                    "allowed_read_roots": ["evidence"],
                    "allowed_write_roots": ["evidence"],
                },
                {
                    "instance_id": "evaluator-001",
                    "skill": "idea-evaluator",
                    "role": "evaluator",
                    "round_id": "round-001",
                    "isolation_mode": "fresh_subagent",
                    "allowed_read_roots": ["evidence"],
                    "allowed_write_roots": ["evidence"],
                },
                {
                    "instance_id": "evaluator-002",
                    "skill": "idea-evaluator",
                    "role": "evaluator",
                    "round_id": "round-002",
                    "isolation_mode": "fresh_subagent",
                    "allowed_read_roots": ["evidence"],
                    "allowed_write_roots": ["evidence"],
                },
                {
                    "instance_id": "panel-001",
                    "skill": "idea-adversarial-review-panel",
                    "role": "panel",
                    "round_id": "round-002-panel",
                    "isolation_mode": "fresh_subagent",
                    "allowed_read_roots": ["evidence"],
                    "allowed_write_roots": ["evidence"],
                },
                {
                    "instance_id": "assembler-001",
                    "skill": "idea-portfolio-assembler",
                    "role": "assembler",
                    "allowed_read_roots": ["evidence"],
                    "allowed_write_roots": ["evidence"],
                },
            ],
        },
    )
    artifact_index = evidence / "artifact-index.json"
    write_json_file(
        artifact_index,
        {
            "schema_version": 1,
            "workflow": "idea",
            **identity,
            "artifacts": [
                {
                    "artifact_id": "primary",
                    "version_id": "v001",
                    "artifact_role": "idea_dossier",
                    "path": "evidence/primary-v1.md",
                    "sha256": sha256_file(primary_v1),
                    "source_skill": "multi-path-idea-generator",
                    "created_by_instance_id": "writer-001",
                    "based_on": [],
                    "change_type": "create",
                    "status": "frozen",
                },
                {
                    "artifact_id": "evaluation-v1",
                    "version_id": "v001",
                    "artifact_role": "evaluation_report",
                    "path": "evidence/evaluator-v1.json",
                    "sha256": sha256_file(evaluator_v1),
                    "source_skill": "idea-evaluator",
                    "created_by_instance_id": "evaluator-001",
                    "based_on": ["primary@v001"],
                    "change_type": "independent_evaluation",
                    "status": "frozen",
                },
                {
                    "artifact_id": "primary",
                    "version_id": "v002",
                    "artifact_role": "idea_dossier",
                    "path": "evidence/primary-v2.md",
                    "sha256": sha256_file(primary_v2),
                    "source_skill": "multi-path-idea-generator",
                    "created_by_instance_id": "writer-001",
                    "based_on": ["primary@v001", "evaluation-v1@v001"],
                    "change_type": "revise",
                    "status": "frozen",
                },
                {
                    "artifact_id": "evaluation-v2",
                    "version_id": "v001",
                    "artifact_role": "evaluation_report",
                    "path": "evidence/evaluator-v2.json",
                    "sha256": sha256_file(evaluator_v2),
                    "source_skill": "idea-evaluator",
                    "created_by_instance_id": "evaluator-002",
                    "based_on": ["primary@v002"],
                    "change_type": "fresh_independent_evaluation",
                    "status": "frozen",
                },
                {
                    "artifact_id": "panel-report",
                    "version_id": "v001",
                    "artifact_role": "panel_report",
                    "path": "evidence/panel-report.json",
                    "sha256": sha256_file(panel_report),
                    "source_skill": "idea-adversarial-review-panel",
                    "created_by_instance_id": "panel-001",
                    "based_on": ["primary@v002"],
                    "change_type": "independent_review",
                    "status": "frozen",
                },
                {
                    "artifact_id": "finding-index",
                    "version_id": "v001",
                    "artifact_role": "review_finding_index",
                    "path": "evidence/finding-index.json",
                    "sha256": sha256_file(finding_index),
                    "source_skill": "idea-portfolio-assembler",
                    "created_by_instance_id": "assembler-001",
                    "based_on": ["evaluation-v2@v001", "panel-report@v001"],
                    "change_type": "finding_index_assembly",
                    "status": "frozen",
                },
                {
                    "artifact_id": "final-package",
                    "version_id": "v001",
                    "artifact_role": "final_handoff_package",
                    "path": "evidence/final-package.json",
                    "sha256": sha256_file(final_package),
                    "source_skill": "idea-portfolio-assembler",
                    "created_by_instance_id": "assembler-001",
                    "based_on": [
                        "primary@v002",
                        "evaluation-v2@v001",
                        "panel-report@v001",
                        "finding-index@v001",
                    ],
                    "change_type": "human_review_packaging",
                    "status": "frozen",
                },
            ],
        },
    )
    read_specs = [
        ("evaluator-001", primary_v1, "evidence/primary-v1.md"),
        ("writer-001", primary_v1, "evidence/primary-v1.md"),
        ("writer-001", evaluator_v1, "evidence/evaluator-v1.json"),
        ("evaluator-002", primary_v2, "evidence/primary-v2.md"),
        ("panel-001", primary_v2, "evidence/primary-v2.md"),
        ("assembler-001", evaluator_v2, "evidence/evaluator-v2.json"),
        ("assembler-001", panel_report, "evidence/panel-report.json"),
    ]
    write_specs = [
        ("writer-001", primary_v1, "evidence/primary-v1.md"),
        ("evaluator-001", evaluator_v1, "evidence/evaluator-v1.json"),
        ("writer-001", primary_v2, "evidence/primary-v2.md"),
        ("evaluator-002", evaluator_v2, "evidence/evaluator-v2.json"),
        ("panel-001", panel_report, "evidence/panel-report.json"),
        ("assembler-001", finding_index, "evidence/finding-index.json"),
        ("assembler-001", final_package, "evidence/final-package.json"),
    ]
    read_records = [
        {
            "actor_instance_id": actor_id,
            "path": path,
            "sha256": sha256_file(file_path),
            "sha256_before": sha256_file(file_path),
            "sha256_after": sha256_file(file_path),
        }
        for actor_id, file_path, path in read_specs
    ]
    write_records = [
        {
            "actor_instance_id": actor_id,
            "path": path,
            "sha256": sha256_file(file_path),
            "allowed_write_root": "evidence",
        }
        for actor_id, file_path, path in write_specs
    ]
    actor_binding = {
        "path": "evidence/actor-manifest.json",
        "sha256": sha256_file(actor_manifest),
    }
    artifact_binding = {
        "path": "evidence/artifact-index.json",
        "sha256": sha256_file(artifact_index),
    }
    file_access = evidence / "file-access.json"
    write_json_file(
        file_access,
        {
            "schema_version": 1,
            "workflow": "idea",
            "entry_mode": "standard",
            **identity,
            "reads": read_records,
            "writes": write_records,
            "source_artifact_hashes_unchanged": True,
        },
    )
    file_access_binding = {
        "path": "evidence/file-access.json",
        "sha256": sha256_file(file_access),
    }
    write_json_file(
        task_export,
        {
            "schema_version": 1,
            "platform": "codex",
            **identity,
            "workflow": "idea",
            "entry_mode": "standard",
            "case_kind": "happy",
            "direction_profile": "focused_optimization",
            "proposal_handoff_candidate": True,
            "final_state": "human_signoff_required",
            "automatic_external_submission": False,
            "actor_manifest": actor_binding,
            "artifact_index": artifact_binding,
            "file_access": file_access_binding,
            "file_access_attestation": {
                "source_artifact_hashes_unchanged": True,
                "files_read_count": len(read_specs),
                "files_written_count": len(write_specs),
            },
        },
    )
    return {
        "receipt_id": "phase7-validator-self-test",
        "workflow": "idea",
        "entry_mode": "standard",
        "case_kind": "happy",
        "direction_profile": "focused_optimization",
        "proposal_handoff_candidate": True,
        "expected_final_state": "human_signoff_required",
        "status": "verified",
        "binding": {
            "plugin_version": registry["plugin_version"],
            "registry_sha256": sha256_repository_file(REGISTRY_PATH),
            "source_commit": source_commit,
            "task_export": {
                "platform": "codex",
                "task_id": identity["task_id"],
                "entry_mode": "standard",
                "path": "evidence/task-export.json",
                "sha256": sha256_file(task_export),
            },
            "actor_manifest": actor_binding,
            "artifact_index": artifact_binding,
        },
        "file_access": {
            "reads": read_records,
            "writes": write_records,
            "source_artifact_hashes_unchanged": True,
        },
        "lineage": {
            "complete": True,
            "current_artifact_ref": "primary@v002",
            "evaluated_artifact_ref": "primary@v002",
        },
        "review_state": {
            "dissent_ids": ["dissent-001"],
            "preserved_dissent_ids": ["dissent-001"],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
            "fatal_findings_visible": True,
        },
        "final_state": "human_signoff_required",
        "automatic_external_submission": False,
        "reason": "Local validator self-test only; never counted as runtime evidence.",
    }


def build_runtime_validator_fixture(
    root: Path, registry: dict[str, Any], source_commit: str
) -> dict[str, Any]:
    """Build a contract-complete synthetic fixture for validator self-tests only."""

    receipt = _build_legacy_runtime_validator_fixture(root, registry, source_commit)
    actor_path = root / receipt["binding"]["actor_manifest"]["path"]
    artifact_path = root / receipt["binding"]["artifact_index"]["path"]
    task_path = root / receipt["binding"]["task_export"]["path"]
    actor_manifest = load_structured_file(actor_path)
    artifact_index = load_structured_file(artifact_path)
    panel_tier, panel_roles = default_panel_roles("idea", registry)

    first_panel = next(actor for actor in actor_manifest["actors"] if actor["role"] == "panel")
    first_panel.update(panel_tier=panel_tier, panel_role=panel_roles[0])
    panel_one_path = root / "evidence" / "panel-report.json"
    panel_one = load_structured_file(panel_one_path)
    panel_one.update(panel_tier=panel_tier, panel_role=panel_roles[0])
    write_json_file(panel_one_path, panel_one)

    new_artifacts: list[dict[str, Any]] = []
    for index, role in enumerate(panel_roles[1:], start=2):
        instance_id = f"panel-{index:03d}"
        actor_manifest["actors"].append(
            {
                "instance_id": instance_id,
                "skill": "idea-adversarial-review-panel",
                "role": "panel",
                "round_id": "round-002-panel",
                "isolation_mode": "fresh_subagent",
                "panel_tier": panel_tier,
                "panel_role": role,
                "allowed_read_roots": ["evidence"],
                "allowed_write_roots": ["evidence"],
            }
        )
        report_rel = f"evidence/panel-report-{index:03d}.json"
        report_path = root / Path(*PurePosixPath(report_rel).parts)
        write_json_file(
            report_path,
            {
                "schema_version": 1,
                "reviewer_instance_id": instance_id,
                "round_id": "round-002-panel",
                "isolation_mode": "fresh_subagent",
                "panel_tier": panel_tier,
                "panel_role": role,
                "input_artifact_refs": ["primary@v002"],
                "decision": "handoff_ready",
                "findings": [],
                "unresolved_issues": [],
                "dissent_ids": [],
                "fatal_finding_ids": [],
                "unresolved_fatal_finding_ids": [],
                "prior_scores_visible": False,
                "source_edits_performed": False,
            },
        )
        new_artifacts.append(
            {
                "artifact_id": f"panel-report-{index:03d}",
                "version_id": "v001",
                "artifact_role": "panel_report",
                "path": report_rel,
                "sha256": sha256_file(report_path),
                "source_skill": "idea-adversarial-review-panel",
                "created_by_instance_id": instance_id,
                "based_on": ["primary@v002"],
                "change_type": f"independent_panel_role:{role}",
                "status": "frozen",
            }
        )
        primary_path = root / "evidence" / "primary-v2.md"
        receipt["file_access"]["reads"].append(
            {
                "actor_instance_id": instance_id,
                "path": "evidence/primary-v2.md",
                "sha256": sha256_file(primary_path),
                "sha256_before": sha256_file(primary_path),
                "sha256_after": sha256_file(primary_path),
            }
        )
        receipt["file_access"]["writes"].append(
            {
                "actor_instance_id": instance_id,
                "path": report_rel,
                "sha256": sha256_file(report_path),
                "allowed_write_root": "evidence",
            }
        )

    supporting_reviewer_id = "supporting-reviewer-001"
    supporting_report_rel = "evidence/supporting-preflight-report.json"
    supporting_report_path = root / Path(*PurePosixPath(supporting_report_rel).parts)
    actor_manifest["actors"].append(
        {
            "instance_id": supporting_reviewer_id,
            "skill": "methodology-statistics-preflight",
            "role": "supporting_reviewer",
            "round_id": "round-002-supporting-preflight",
            "isolation_mode": "fresh_subagent",
            "dispatch_source": "research-idea-orchestrator",
            "dispatch_mode": "delegated",
            "dispatch_trigger": "method_or_endpoint_fit_needs_review",
            "allowed_read_roots": ["evidence"],
            "allowed_write_roots": ["evidence"],
        }
    )
    write_json_file(
        supporting_report_path,
        {
            "schema_version": 1,
            "reviewer_instance_id": supporting_reviewer_id,
            "round_id": "round-002-supporting-preflight",
            "isolation_mode": "fresh_subagent",
            "input_artifact_refs": ["primary@v002"],
            "decision": "pass",
            "findings": [
                {
                    "id": "support-dissent-001",
                    "severity": "minor",
                    "blocking": False,
                    "resolved": False,
                    "dissent": True,
                }
            ],
            "unresolved_issues": [],
            "dissent_ids": ["support-dissent-001"],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
            "prior_scores_visible": False,
            "source_edits_performed": False,
        },
    )
    new_artifacts.append(
        {
            "artifact_id": "supporting-preflight-report",
            "version_id": "v001",
            "artifact_role": "preflight_report",
            "path": supporting_report_rel,
            "sha256": sha256_file(supporting_report_path),
            "source_skill": "methodology-statistics-preflight",
            "created_by_instance_id": supporting_reviewer_id,
            "based_on": ["primary@v002"],
            "change_type": "fresh_independent_supporting_review",
            "status": "frozen",
        }
    )
    primary_path = root / "evidence" / "primary-v2.md"
    receipt["file_access"]["reads"].append(
        {
            "actor_instance_id": supporting_reviewer_id,
            "path": "evidence/primary-v2.md",
            "sha256": sha256_file(primary_path),
            "sha256_before": sha256_file(primary_path),
            "sha256_after": sha256_file(primary_path),
        }
    )
    receipt["file_access"]["writes"].append(
        {
            "actor_instance_id": supporting_reviewer_id,
            "path": supporting_report_rel,
            "sha256": sha256_file(supporting_report_path),
            "allowed_write_root": "evidence",
        }
    )

    support_specs = [
        ("context-001", "research-context-builder", "builder", "research-context", "research_context"),
        ("evidence-001", "research-opportunity-mapper", "retrieval", "evidence-map", "evidence_map"),
        ("orchestrator-001", "research-idea-orchestrator", "orchestrator", "idea-routing-decision", "idea_routing_decision"),
        ("writer-001", "multi-path-idea-generator", "writer", "proposed-navigation-metadata", "proposed_navigation_metadata"),
        ("orchestrator-001", "research-idea-orchestrator", "orchestrator", "idea-index", "idea_index"),
        ("orchestrator-001", "research-idea-orchestrator", "orchestrator", "reference-ledger", "reference_ledger"),
        ("orchestrator-001", "research-idea-orchestrator", "orchestrator", "revision-plan", "revision_plan"),
        ("writer-001", "multi-path-idea-generator", "writer", "revision-delta", "revision_delta"),
    ]
    for instance_id, skill, role, stem, artifact_role in support_specs:
        if not any(actor["instance_id"] == instance_id for actor in actor_manifest["actors"]):
            actor_manifest["actors"].append(
                {
                    "instance_id": instance_id,
                    "skill": skill,
                    "role": role,
                    "allowed_read_roots": ["evidence"],
                    "allowed_write_roots": ["evidence"],
                }
            )
        relative = f"evidence/{stem}.md"
        file_path = root / Path(*PurePosixPath(relative).parts)
        if artifact_role == "idea_index":
            write_json_file(
                file_path,
                {
                    "schema_version": 1,
                    "direction_profile": "focused_optimization",
                    "current_nodes": [
                        {
                            "node_id": "idea-focused-001",
                            "current_ref": "primary@v002",
                            "current_digest": sha256_file(
                                root / "evidence" / "primary-v2.md"
                            ),
                        }
                    ],
                },
            )
        else:
            file_path.write_text(
                f"synthetic {artifact_role}\n",
                encoding="utf-8",
                newline="\n",
            )
        new_artifacts.append(
            {
                "artifact_id": stem,
                "version_id": "v001",
                "artifact_role": artifact_role,
                "path": relative,
                "sha256": sha256_file(file_path),
                "source_skill": skill,
                "created_by_instance_id": instance_id,
                "based_on": ["primary@v002"],
                "change_type": "synthetic_required_package_input",
                "status": "frozen",
            }
        )
        receipt["file_access"]["writes"].append(
            {
                "actor_instance_id": instance_id,
                "path": relative,
                "sha256": sha256_file(file_path),
                "allowed_write_root": "evidence",
            }
        )

    for artifact in artifact_index["artifacts"]:
        if artifact["path"] == "evidence/panel-report.json":
            artifact["sha256"] = sha256_file(panel_one_path)
    for entry in receipt["file_access"]["writes"] + receipt["file_access"]["reads"]:
        if entry["path"] == "evidence/panel-report.json":
            digest = sha256_file(panel_one_path)
            entry["sha256"] = digest
            if "sha256_before" in entry:
                entry["sha256_before"] = digest
                entry["sha256_after"] = digest
    artifact_index["artifacts"].extend(new_artifacts)

    finding_index_artifact = next(
        artifact
        for artifact in artifact_index["artifacts"]
        if artifact["artifact_role"] == "review_finding_index"
    )
    finding_index_artifact["based_on"].append("supporting-preflight-report@v001")
    finding_index_path = root / Path(*PurePosixPath(finding_index_artifact["path"]).parts)
    finding_index_document = load_structured_file(finding_index_path)
    finding_index_document["dissent_ids"].append("support-dissent-001")
    finding_index_document["preserved_dissent_ids"].append("support-dissent-001")
    write_json_file(finding_index_path, finding_index_document)
    finding_index_artifact["sha256"] = sha256_file(finding_index_path)
    for entry in receipt["file_access"]["writes"]:
        if entry["path"] == finding_index_artifact["path"]:
            entry["sha256"] = finding_index_artifact["sha256"]
    receipt["file_access"]["reads"].append(
        {
            "actor_instance_id": "assembler-001",
            "path": supporting_report_rel,
            "sha256": sha256_file(supporting_report_path),
            "sha256_before": sha256_file(supporting_report_path),
            "sha256_after": sha256_file(supporting_report_path),
        }
    )

    package_artifact = next(
        artifact
        for artifact in artifact_index["artifacts"]
        if artifact["artifact_role"] == "final_handoff_package"
    )
    package_parent_refs = [
        "research-context@v001",
        "evidence-map@v001",
        "idea-routing-decision@v001",
        "idea-index@v001",
        "reference-ledger@v001",
        "primary@v002",
        "evaluation-v2@v001",
        "panel-report@v001",
        "panel-report-002@v001",
        "panel-report-003@v001",
        "revision-plan@v001",
        "revision-delta@v001",
    ]
    package_artifact["based_on"] = package_parent_refs
    final_package_path = root / package_artifact["path"]
    final_package = load_structured_file(final_package_path)
    final_package.update(
        {
            "input_artifact_refs": package_parent_refs,
            "source_edits_performed": False,
            "source_identity_unchanged": True,
            "preserved_dissent_ids": ["dissent-001", "support-dissent-001"],
        }
    )
    write_json_file(final_package_path, final_package)
    package_artifact["sha256"] = sha256_file(final_package_path)
    for entry in receipt["file_access"]["writes"]:
        if entry["path"] == package_artifact["path"]:
            entry["sha256"] = package_artifact["sha256"]

    artifacts_by_ref = {
        f"{artifact['artifact_id']}@{artifact['version_id']}": artifact
        for artifact in artifact_index["artifacts"]
    }
    assembler_reads = {
        entry["path"]
        for entry in receipt["file_access"]["reads"]
        if entry["actor_instance_id"] == "assembler-001"
    }
    for parent_ref in package_parent_refs:
        parent = artifacts_by_ref[parent_ref]
        if parent["path"] in assembler_reads:
            continue
        parent_path = root / Path(*PurePosixPath(parent["path"]).parts)
        digest = sha256_file(parent_path)
        receipt["file_access"]["reads"].append(
            {
                "actor_instance_id": "assembler-001",
                "path": parent["path"],
                "sha256": digest,
                "sha256_before": digest,
                "sha256_after": digest,
            }
        )

    idea_edges_by_destination: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in registry["workflow_edges"]:
        if edge["workflow"] == "idea":
            idea_edges_by_destination[edge["destination"]].append(edge)
    for actor in actor_manifest["actors"]:
        if actor["role"] == "orchestrator":
            continue
        candidate_edges = idea_edges_by_destination.get(actor["skill"], [])
        require(
            bool(candidate_edges),
            "runtime_fixture_actor_edge_missing",
            actor["skill"],
        )
        edge = candidate_edges[0]
        actor.setdefault("dispatch_source", edge["source"])
        actor.setdefault("dispatch_mode", edge["dispatch_mode"])
        actor.setdefault("dispatch_trigger", edge["trigger"])

    write_json_file(actor_path, actor_manifest)
    receipt["binding"]["actor_manifest"]["sha256"] = sha256_file(actor_path)
    write_json_file(artifact_path, artifact_index)
    receipt["binding"]["artifact_index"]["sha256"] = sha256_file(artifact_path)
    task_export = load_structured_file(task_path)
    file_access_path = root / task_export["file_access"]["path"]
    file_access_document = load_structured_file(file_access_path)
    file_access_document.update(receipt["file_access"])
    write_json_file(file_access_path, file_access_document)
    task_export.update(
        {
            "actor_manifest": receipt["binding"]["actor_manifest"],
            "artifact_index": receipt["binding"]["artifact_index"],
            "file_access": {
                "path": task_export["file_access"]["path"],
                "sha256": sha256_file(file_access_path),
            },
            "panel_tier": panel_tier,
            "panel_role_instances": {
                role: f"panel-{index:03d}"
                for index, role in enumerate(panel_roles, start=1)
            },
            "final_package_actor_instance_id": "assembler-001",
            "direction_profile": "focused_optimization",
            "proposal_handoff_candidate": True,
        }
    )
    task_export["file_access_attestation"] = {
        "source_artifact_hashes_unchanged": True,
        "files_read_count": len(receipt["file_access"]["reads"]),
        "files_written_count": len(receipt["file_access"]["writes"]),
    }
    write_json_file(task_path, task_export)
    receipt["binding"]["task_export"]["sha256"] = sha256_file(task_path)
    receipt["control_evidence"] = {
        "input_condition": None,
        "gate": None,
        "finding": None,
        "route": None,
        "continuation_artifact_ref": None,
    }
    receipt["review_state"]["dissent_ids"] = [
        "dissent-001",
        "support-dissent-001",
    ]
    receipt["review_state"]["preserved_dissent_ids"] = [
        "dissent-001",
        "support-dissent-001",
    ]
    return receipt


def build_runtime_control_validator_fixture(
    root: Path, registry: dict[str, Any], source_commit: str
) -> dict[str, Any]:
    receipt = build_runtime_validator_fixture(root, registry, source_commit)
    receipt["case_kind"] = "control"
    receipt["expected_final_state"] = "stopped"
    receipt["final_state"] = "stopped"
    receipt["control_evidence"] = {
        "input_condition": "independent_review_no_incremental_gain",
        "gate": "unfixable_no_gain_or_user_stop",
        "finding": "no-gain-001",
        "route": "human_review_or_explicit_resume",
        "continuation_artifact_ref": "continuation-brief@v001",
    }
    continuation_path = root / "evidence" / "continuation-brief.json"
    write_json_file(
        continuation_path,
        {
            "schema_version": 1,
            "input_condition": receipt["control_evidence"]["input_condition"],
            "gate": receipt["control_evidence"]["gate"],
            "finding": receipt["control_evidence"]["finding"],
            "route": receipt["control_evidence"]["route"],
        },
    )
    artifact_path = root / "evidence" / "artifact-index.json"
    artifact_document = load_structured_file(artifact_path)
    evaluator_path = root / "evidence" / "evaluator-v2.json"
    evaluator_document = load_structured_file(evaluator_path)
    evaluator_document["decision"] = "keep_as_backup"
    evaluator_document["findings"] = [
        {
            "id": "no-gain-001",
            "title": "No incremental gain after the bounded revision",
            "dossier_locator": "Expected outputs and falsification criteria",
            "severity": "major",
            "blocking": True,
            "resolved": False,
            "dissent": False,
        }
    ]
    evaluator_document["unresolved_issues"] = ["no-gain-001"]
    write_json_file(evaluator_path, evaluator_document)
    evaluator_digest = sha256_file(evaluator_path)
    next(
        artifact
        for artifact in artifact_document["artifacts"]
        if artifact["path"] == "evidence/evaluator-v2.json"
    )["sha256"] = evaluator_digest
    artifact_document["artifacts"] = [
        artifact
        for artifact in artifact_document["artifacts"]
        if artifact["artifact_role"] != "final_handoff_package"
    ]
    artifact_document["artifacts"].append(
        {
            "artifact_id": "continuation-brief",
            "version_id": "v001",
            "artifact_role": "continuation_brief",
            "path": "evidence/continuation-brief.json",
            "sha256": sha256_file(continuation_path),
            "source_skill": "research-idea-orchestrator",
            "created_by_instance_id": "orchestrator-001",
            "based_on": ["primary@v002"],
            "change_type": "valid_control_continuation",
            "status": "frozen",
        }
    )
    write_json_file(artifact_path, artifact_document)
    receipt["binding"]["artifact_index"]["sha256"] = sha256_file(artifact_path)
    receipt["file_access"]["writes"] = [
        entry
        for entry in receipt["file_access"]["writes"]
        if entry["path"] != "evidence/final-package.json"
    ]
    for entry in receipt["file_access"]["writes"]:
        if entry["path"] == "evidence/evaluator-v2.json":
            entry["sha256"] = evaluator_digest
    for entry in receipt["file_access"]["reads"]:
        if entry["path"] == "evidence/evaluator-v2.json":
            entry["sha256"] = evaluator_digest
            entry["sha256_before"] = evaluator_digest
            entry["sha256_after"] = evaluator_digest
    receipt["file_access"]["writes"].append(
        {
            "actor_instance_id": "orchestrator-001",
            "path": "evidence/continuation-brief.json",
            "sha256": sha256_file(continuation_path),
            "allowed_write_root": "evidence",
        }
    )
    task_path = root / "evidence" / "task-export.json"
    task_document = load_structured_file(task_path)
    file_access_path = root / "evidence" / "file-access.json"
    file_access_document = load_structured_file(file_access_path)
    file_access_document.update(receipt["file_access"])
    write_json_file(file_access_path, file_access_document)
    task_document["case_kind"] = "control"
    task_document["final_state"] = "stopped"
    task_document["artifact_index"] = receipt["binding"]["artifact_index"]
    task_document["file_access"] = {
        "path": "evidence/file-access.json",
        "sha256": sha256_file(file_access_path),
    }
    task_document["final_package_actor_instance_id"] = None
    task_document["file_access_attestation"] = {
        "source_artifact_hashes_unchanged": True,
        "files_read_count": len(receipt["file_access"]["reads"]),
        "files_written_count": len(receipt["file_access"]["writes"]),
    }
    write_json_file(task_path, task_document)
    receipt["binding"]["task_export"]["sha256"] = sha256_file(task_path)
    return receipt


def build_contract_complete_workflow_fixture(
    root: Path,
    registry: dict[str, Any],
    source_commit: str,
    workflow: str,
) -> dict[str, Any]:
    """Build one complete happy-path runtime receipt for any registered workflow."""

    entry_modes = {
        "idea": "standard",
        "proposal": "standard",
        "article": "standard",
        "perspective": "full",
        "research_polisher": "standard",
    }
    evidence = root / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    machine = registry["workflow_state_machines"][workflow]
    direction_profile = direction_profile_for(workflow, registry)
    workflow_conditions = workflow_conditions_for(
        workflow,
        registry,
        None,
        default_active=True,
    )
    entry_mode = entry_modes[workflow]
    task_id = f"contract-complete-{workflow}"
    identity = {
        "task_id": task_id,
        "plugin_version": registry["plugin_version"],
        "registry_sha256": sha256_repository_file(REGISTRY_PATH),
        "source_commit": source_commit,
    }
    skill_contracts = {skill["name"]: skill for skill in registry["skills"]}
    artifact_contract = registry["scenario_eval_contract"][
        "runtime_artifact_role_contract"
    ]
    review_output_roles = set(artifact_contract["review_output_roles"])
    decision_contracts = registry["scenario_eval_contract"][
        "review_decision_contracts"
    ]
    package_contract = registry["scenario_eval_contract"][
        "package_input_contracts"
    ][workflow]
    panel_tier, panel_roles = default_panel_roles(
        workflow,
        registry,
        direction_profile=direction_profile,
        workflow_conditions=workflow_conditions,
    )
    panel_skill = panel_skill_for(
        {"workflow": workflow, "case_id": f"contract-complete-{workflow}"},
        registry,
        direction_profile=direction_profile,
        workflow_conditions=workflow_conditions,
    )
    review_group = (
        registry["scenario_eval_contract"]
        .get("review_group_contracts", {})
        .get(workflow)
    )

    actors: list[dict[str, Any]] = []
    actor_by_id: dict[str, dict[str, Any]] = {}
    actor_by_skill_role: dict[tuple[str, str], list[str]] = defaultdict(list)
    actor_serials: Counter[str] = Counter()
    artifacts: list[dict[str, Any]] = []
    artifacts_by_ref: dict[str, dict[str, Any]] = {}
    actor_read_refs: dict[str, set[str]] = defaultdict(set)
    actor_write_paths: dict[str, set[str]] = defaultdict(set)
    artifact_serial = 0

    workflow_edges_by_destination: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in registry["workflow_edges"]:
        if edge["workflow"] == workflow:
            workflow_edges_by_destination[edge["destination"]].append(edge)

    def add_actor(
        skill: str,
        role: str,
        *,
        suffix: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> str:
        actor_serials[role] += 1
        serial = actor_serials[role]
        instance_id = (
            f"{normalized_id(skill)}-{suffix}"
            if suffix
            else f"{normalized_id(skill)}-{serial:03d}"
        )
        actor: dict[str, Any] = {
            "instance_id": instance_id,
            "skill": skill,
            "role": role,
            "allowed_read_roots": ["evidence"],
            "allowed_write_roots": ["evidence"],
        }
        if role != "orchestrator":
            edges = workflow_edges_by_destination.get(skill, [])
            require(
                bool(edges),
                "runtime_fixture_actor_edge_missing",
                f"{workflow}: {skill}",
            )
            edge = edges[0]
            actor.update(
                {
                    "dispatch_source": edge["source"],
                    "dispatch_mode": edge["dispatch_mode"],
                    "dispatch_trigger": edge["trigger"],
                }
            )
        if role in {
            "evaluator",
            "panel",
            "strategy_reviewer",
            "supporting_reviewer",
            "verifier_compositor",
        }:
            actor.setdefault("round_id", f"round-{serial:03d}-{role}")
            actor.setdefault("isolation_mode", "fresh_subagent")
        if extra:
            actor.update(extra)
        require(
            instance_id not in actor_by_id,
            "runtime_fixture_actor_id_reused",
            instance_id,
        )
        actors.append(actor)
        actor_by_id[instance_id] = actor
        actor_by_skill_role[(skill, role)].append(instance_id)
        return instance_id

    orchestrator_id = add_actor(machine["orchestrator"], "orchestrator")
    expected_final_skill = machine["final_package_skill"]
    expected_final_role = (
        "verifier_compositor"
        if skill_contracts[expected_final_skill]["requires_independent_subagent"]
        else "assembler"
    )
    finalizer_id = add_actor(expected_final_skill, expected_final_role)

    def existing_actor(skill: str, role: str) -> str | None:
        values = actor_by_skill_role.get((skill, role), [])
        return values[0] if values else None

    def ensure_actor(skill: str) -> str:
        if skill == machine["orchestrator"]:
            return orchestrator_id
        if skill == expected_final_skill:
            return finalizer_id
        if (
            skill in set(machine.get("primary_writer_skills", []))
            and primary_writer_id is not None
        ):
            return primary_writer_id
        registry_role = skill_contracts[skill]["role"]
        runtime_role = {
            "builder": "builder",
            "retrieval": "retrieval",
            "controller": "controller",
            "drafter": "supporting_writer",
            "reviewer": "supporting_reviewer",
            "assembler": "assembler",
            "generator": "writer",
        }.get(registry_role)
        require(
            runtime_role is not None,
            "runtime_fixture_actor_role_missing",
            f"{workflow}: {skill}/{registry_role}",
        )
        found = existing_actor(skill, runtime_role)
        return found if found is not None else add_actor(skill, runtime_role)

    def add_artifact(
        *,
        artifact_role: str,
        source_skill: str,
        creator_id: str,
        based_on: list[str],
        change_type: str,
        artifact_id: str | None = None,
        version_id: str = "v001",
        document: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        external_source_id: str | None = None,
    ) -> dict[str, Any]:
        nonlocal artifact_serial
        artifact_serial += 1
        selected_id = artifact_id or (
            f"{normalized_id(artifact_role)}-{artifact_serial:03d}"
        )
        extension = "json" if document is not None else "md"
        relative = f"evidence/{selected_id}-{version_id}.{extension}"
        path = root / Path(*PurePosixPath(relative).parts)
        if document is None:
            path.write_text(
                f"contract-complete {workflow} {artifact_role}\n",
                encoding="utf-8",
                newline="\n",
            )
        else:
            write_json_file(path, document)
        artifact: dict[str, Any] = {
            "artifact_id": selected_id,
            "version_id": version_id,
            "artifact_role": artifact_role,
            "path": relative,
            "sha256": sha256_file(path),
            "source_skill": source_skill,
            "created_by_instance_id": creator_id,
            "based_on": list(based_on),
            "change_type": change_type,
            "status": "frozen",
        }
        if extra:
            artifact.update(extra)
        if external_source_id is not None:
            artifact["external_source_id"] = external_source_id
        artifact_ref = ref_for(artifact)
        require(
            artifact_ref not in artifacts_by_ref,
            "runtime_fixture_artifact_ref_reused",
            artifact_ref,
        )
        artifacts.append(artifact)
        artifacts_by_ref[artifact_ref] = artifact
        if creator_id != "external-input":
            actor_write_paths[creator_id].add(relative)
            actor_read_refs[creator_id].update(based_on)
        return artifact

    def add_external(artifact_role: str, artifact_id: str) -> dict[str, Any]:
        return add_artifact(
            artifact_role=artifact_role,
            source_skill="external-input",
            creator_id="external-input",
            based_on=[],
            change_type="frozen_external_input",
            artifact_id=artifact_id,
            external_source_id=f"external:{workflow}:{artifact_id}",
        )

    source_artifact = add_external("source_material", "external-source")
    source_ref = ref_for(source_artifact)
    minimal_intake_ref: str | None = None
    if workflow == "article":
        minimal_intake_ref = ref_for(
            add_external("minimal_intake", "external-minimal-intake")
        )

    def pass_decision(skill: str) -> str:
        values = decision_contracts[skill]["pass"]
        require(bool(values), "runtime_fixture_pass_decision_missing", skill)
        return values[0]

    def revise_decision(skill: str) -> str:
        values = decision_contracts[skill]["revise"]
        require(bool(values), "runtime_fixture_revise_decision_missing", skill)
        return values[0]

    def polisher_option(strategy_role: str, tier: str) -> dict[str, Any]:
        reposition = tier == "reposition_only"
        return {
            "proposal_id": f"{strategy_role}-{tier}",
            "effort_tier": tier,
            "status": "proposed",
            "positioning_change": "Reframe the contribution for this lens.",
            "value_gain_mechanism": "Clarify why the frozen result matters.",
            "claim_delta": "Reorder only claims supported by frozen evidence.",
            "target_audience": "Relevant scientific and practice stakeholders.",
            "added_work_items": [] if reposition else ["One bounded validation."],
            "resource_dependencies": [] if reposition else ["Existing assets."],
            "feasibility": {
                "rating": "high",
                "basis": "The bounded package uses available assets.",
            },
            "evidence_dependencies": ["Frozen dossier evidence."],
            "risks": ["The impact gain may remain outlet-dependent."],
            "stop_conditions": ["Stop if claims exceed frozen evidence."],
            "new_work_flags": {
                "new_analysis": tier == "moderate_extension",
                "new_experiment": False,
                "new_data": False,
                "new_validation": tier == "small_extension",
            },
            "bounded_package": True,
            "independent_new_study": False,
            "core_design_rebuild": False,
        }

    def add_review_report(
        *,
        actor_id: str,
        artifact_role: str,
        input_refs: list[str],
        decision: str,
        artifact_id: str,
        change_type: str,
        artifact_extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        actor = actor_by_id[actor_id]
        report: dict[str, Any] = {
            "schema_version": 1,
            "reviewer_instance_id": actor_id,
            "round_id": actor["round_id"],
            "isolation_mode": "fresh_subagent",
            "input_artifact_refs": list(input_refs),
            "decision": decision,
            "findings": [],
            "unresolved_issues": [],
            "dissent_ids": [],
            "fatal_finding_ids": [],
            "unresolved_fatal_finding_ids": [],
            "prior_scores_visible": False,
            "source_edits_performed": False,
        }
        if actor["role"] == "panel":
            report.update(
                {
                    "panel_tier": actor["panel_tier"],
                    "panel_role": actor["panel_role"],
                }
            )
        if actor["role"] == "strategy_reviewer":
            report.update(
                {
                    "strategy_role": actor["strategy_role"],
                    "peer_outputs_visible": False,
                    "strategy_options": [
                        polisher_option(actor["strategy_role"], tier)
                        for tier in review_group["effort_tiers"]
                    ],
                }
            )
        extension = registry["scenario_eval_contract"].get(
            "workflow_review_extensions", {}
        ).get(actor["skill"])
        if extension is not None:
            require(
                len(input_refs) == extension["exact_input_artifact_count"],
                "runtime_fixture_review_extension_invalid",
                actor_id,
            )
            report.update(
                {
                    "reviewed_dossier_digest": artifacts_by_ref[input_refs[0]][
                        "sha256"
                    ],
                    "complete_dossier_confirmed": True,
                    "dossier_only_input_confirmed": True,
                }
            )
        return add_artifact(
            artifact_role=artifact_role,
            source_skill=actor["skill"],
            creator_id=actor_id,
            based_on=input_refs,
            change_type=change_type,
            artifact_id=artifact_id,
            document=report,
            extra=artifact_extra,
        )

    primary_writer_id: str | None = None
    strategy_report_refs: list[str] = []
    dossier_ref: str | None = None
    evidence_map_ref: str | None = None
    if workflow != "research_polisher":
        primary_skill = machine["primary_writer_skills"][0]
        primary_writer_id = add_actor(primary_skill, "writer")
        primary_v1 = add_artifact(
            artifact_role=machine["primary_artifact_type"],
            source_skill=primary_skill,
            creator_id=primary_writer_id,
            based_on=[source_ref],
            change_type="create" if workflow == "idea" else "initial_generation",
            artifact_id="primary",
            version_id="v001",
        )
        evaluator_one_id = add_actor(
            machine["evaluator_skill"], "evaluator", suffix="round-001"
        )
        evaluation_role = (
            "research_polisher_evaluation_report"
            if workflow == "research_polisher"
            else "evaluation_report"
        )
        evaluation_v1 = add_review_report(
            actor_id=evaluator_one_id,
            artifact_role=evaluation_role,
            input_refs=[ref_for(primary_v1)],
            decision=revise_decision(machine["evaluator_skill"]),
            artifact_id="evaluation-round-001",
            change_type="independent_evaluation",
        )
        primary_v2 = add_artifact(
            artifact_role=machine["primary_artifact_type"],
            source_skill=primary_skill,
            creator_id=primary_writer_id,
            based_on=[ref_for(primary_v1), ref_for(evaluation_v1)],
            change_type="revise" if workflow == "idea" else "targeted_revision",
            artifact_id="primary",
            version_id="v002",
        )
    else:
        dossier_actor = ensure_actor("article-context-builder")
        dossier = add_artifact(
            artifact_role="research_polisher_dossier",
            source_skill="article-context-builder",
            creator_id=dossier_actor,
            based_on=[source_ref],
            change_type="context_normalization",
            artifact_id="research-polisher-dossier",
        )
        dossier_ref = ref_for(dossier)
        evidence_actor = ensure_actor("research-opportunity-mapper")
        evidence_map = add_artifact(
            artifact_role="evidence_map",
            source_skill="research-opportunity-mapper",
            creator_id=evidence_actor,
            based_on=[source_ref],
            change_type="evidence_mapping",
            artifact_id="research-polisher-evidence-map",
        )
        evidence_map_ref = ref_for(evidence_map)
        for index, strategy_role in enumerate(review_group["roles"], start=1):
            strategy_id = add_actor(
                review_group["skill"],
                "strategy_reviewer",
                suffix=f"{index:03d}",
                extra={"strategy_role": strategy_role},
            )
            strategy_report = add_review_report(
                actor_id=strategy_id,
                artifact_role="research_polisher_strategy_report",
                input_refs=[dossier_ref, evidence_map_ref],
                decision=pass_decision(review_group["skill"]),
                artifact_id=f"strategy-report-{index:03d}",
                change_type="blind_strategy_review",
            )
            strategy_report_refs.append(ref_for(strategy_report))
        primary_v1 = add_artifact(
            artifact_role=machine["primary_artifact_type"],
            source_skill=expected_final_skill,
            creator_id=finalizer_id,
            based_on=strategy_report_refs,
            change_type="candidate_portfolio_assembly",
            artifact_id="portfolio",
            version_id="v001",
        )
        evaluator_one_id = add_actor(
            machine["evaluator_skill"], "evaluator", suffix="round-001"
        )
        evaluation_v1 = add_review_report(
            actor_id=evaluator_one_id,
            artifact_role="research_polisher_evaluation_report",
            input_refs=[ref_for(primary_v1)],
            decision=revise_decision(machine["evaluator_skill"]),
            artifact_id="evaluation-round-001",
            change_type="independent_evaluation",
        )
        primary_v2 = add_artifact(
            artifact_role=machine["primary_artifact_type"],
            source_skill=expected_final_skill,
            creator_id=finalizer_id,
            based_on=[
                *strategy_report_refs,
                ref_for(primary_v1),
                ref_for(evaluation_v1),
            ],
            change_type="candidate_portfolio_revision",
            artifact_id="portfolio",
            version_id="v002",
        )

    current_ref = ref_for(primary_v2)
    current_idea_refs = {current_ref}
    evaluator_two_id = add_actor(
        machine["evaluator_skill"], "evaluator", suffix="round-002"
    )
    current_evaluation = add_review_report(
        actor_id=evaluator_two_id,
        artifact_role=(
            "research_polisher_evaluation_report"
            if workflow == "research_polisher"
            else "evaluation_report"
        ),
        input_refs=[current_ref],
        decision=pass_decision(machine["evaluator_skill"]),
        artifact_id="evaluation-round-002",
        change_type="fresh_independent_evaluation",
    )
    if workflow == "idea":
        add_artifact(
            artifact_role="proposed_navigation_metadata",
            source_skill=machine["primary_writer_skills"][0],
            creator_id=primary_writer_id,
            based_on=[current_ref],
            change_type="proposed_navigation_metadata",
            artifact_id="proposed-navigation-metadata",
        )

    panel_role_instances: dict[str, str] = {}
    panel_artifacts: list[dict[str, Any]] = []
    if panel_skill is not None:
        for index, panel_role in enumerate(panel_roles, start=1):
            panel_id = add_actor(
                panel_skill,
                "panel",
                suffix=f"{index:03d}",
                extra={"panel_tier": panel_tier, "panel_role": panel_role},
            )
            panel_role_instances[panel_role] = panel_id
            panel_artifacts.append(
                add_review_report(
                    actor_id=panel_id,
                    artifact_role="panel_report",
                    input_refs=[current_ref],
                    decision=pass_decision(panel_skill),
                    artifact_id=f"panel-report-{index:03d}",
                    change_type=f"independent_panel_role:{panel_role}",
                )
            )

    def artifacts_matching_rule(rule: dict[str, Any]) -> list[dict[str, Any]]:
        return package_rule_matches(
            artifacts,
            rule,
            current_ref=current_ref,
            current_idea_refs=current_idea_refs,
        )

    def input_refs_for_supporting_review(skill: str, rule: dict[str, Any]) -> list[str]:
        if skill == "article-readiness-triage" and minimal_intake_ref is not None:
            return [minimal_intake_ref]
        if skill == "proposal-readiness-triage":
            context = next(
                (
                    artifact
                    for artifact in artifacts
                    if artifact["artifact_role"] == "proposal_context"
                ),
                None,
            )
            return [ref_for(context)] if context is not None else [current_ref]
        if rule.get("selected_artifact_lineage_role"):
            selected = [
                artifact
                for artifact in artifacts
                if artifact["artifact_role"]
                == rule["selected_artifact_lineage_role"]
            ]
            require(bool(selected), "runtime_fixture_selected_input_missing", skill)
            return [ref_for(selected[-1])]
        return [current_ref]

    def create_required_artifact(rule: dict[str, Any]) -> dict[str, Any]:
        source_skill = rule.get("source_skill")
        if source_skill is None:
            source_skill = next(
                skill
                for skill in rule.get("source_skills", [])
                if skill != "external-input"
            )
        actor_id = ensure_actor(source_skill)
        artifact_role = rule["artifact_role"]
        if artifact_role in review_output_roles:
            input_refs = input_refs_for_supporting_review(source_skill, rule)
            return add_review_report(
                actor_id=actor_id,
                artifact_role=artifact_role,
                input_refs=input_refs,
                decision=pass_decision(source_skill),
                artifact_id=(
                    f"{normalized_id(source_skill)}-{normalized_id(artifact_role)}"
                ),
                change_type=(
                    "fresh_independent_evaluation"
                    if source_skill == "sap-evaluator"
                    else "fresh_independent_supporting_review"
                ),
            )
        parent_refs = [source_ref]
        if rule.get("selected_artifact_lineage_role"):
            selected = [
                artifact
                for artifact in artifacts
                if artifact["artifact_role"]
                == rule["selected_artifact_lineage_role"]
            ]
            require(bool(selected), "runtime_fixture_selected_input_missing", source_skill)
            parent_refs = [ref_for(selected[-1])]
        elif artifact_role == "research_polisher_sealed_provenance":
            parent_refs = list(strategy_report_refs)
        elif artifact_role not in {"proposal_context", "research_context", "evidence_map"}:
            parent_refs = [current_ref]
        document = None
        if workflow == "idea" and artifact_role == "idea_index":
            document = {
                "schema_version": 1,
                "direction_profile": direction_profile,
                "current_nodes": [
                    {
                        "node_id": "idea-current-001",
                        "current_ref": current_ref,
                        "current_digest": artifacts_by_ref[current_ref]["sha256"],
                    }
                ],
            }
        return add_artifact(
            artifact_role=artifact_role,
            source_skill=source_skill,
            creator_id=actor_id,
            based_on=parent_refs,
            change_type="required_package_input",
            artifact_id=(
                "sap"
                if artifact_role == "sap"
                else f"{normalized_id(source_skill)}-{normalized_id(artifact_role)}"
            ),
            document=document,
        )

    for rule in package_contract["required_inputs"]:
        if (
            workflow == "research_polisher"
            and rule["artifact_role"]
            == artifact_contract["finding_index_role_by_workflow"][workflow]
        ):
            # The finding index must be assembled from the completed review set,
            # not synthesized as a generic package prerequisite.
            continue
        required_count, _ = package_rule_count_bounds(
            rule,
            direction_profile=direction_profile,
            current_idea_count=len(current_idea_refs),
            panel_role_count=len(panel_roles),
            workflow_conditions=workflow_conditions,
        )
        if required_count == 0:
            continue
        matches = artifacts_matching_rule(rule)
        while len(matches) < required_count:
            create_required_artifact(rule)
            matches = artifacts_matching_rule(rule)

    def review_artifacts() -> list[dict[str, Any]]:
        return [
            artifact
            for artifact in artifacts
            if artifact["created_by_instance_id"] in actor_by_id
            and artifact_is_review_finding_report(
                creator_role=actor_by_id[artifact["created_by_instance_id"]]["role"],
                artifact_role=artifact["artifact_role"],
                contract=artifact_contract,
            )
        ]

    finding_index_role = artifact_contract["finding_index_role_by_workflow"][workflow]

    def add_finding_index(*, creation_sequence: int | None = None) -> dict[str, Any]:
        all_review_artifacts = review_artifacts()
        prior_review_artifacts = [
            artifact
            for artifact in all_review_artifacts
            if artifact["created_by_instance_id"] != finalizer_id
        ]
        internal_review_refs = [
            ref_for(artifact)
            for artifact in all_review_artifacts
            if artifact["created_by_instance_id"] == finalizer_id
        ]
        extra: dict[str, Any] = {
            "internal_output_refs": internal_review_refs,
        }
        if creation_sequence is not None:
            extra["creation_sequence"] = creation_sequence
        return add_artifact(
            artifact_role=finding_index_role,
            source_skill=expected_final_skill,
            creator_id=finalizer_id,
            based_on=[ref_for(artifact) for artifact in prior_review_artifacts],
            change_type="finding_index_assembly",
            artifact_id="review-finding-index",
            document={
                "schema_version": 1,
                "task_id": task_id,
                "dissent_ids": [],
                "preserved_dissent_ids": [],
                "fatal_finding_ids": [],
                "unresolved_fatal_finding_ids": [],
            },
            extra=extra,
        )

    if workflow == "research_polisher":
        add_finding_index()

    package_parents: list[dict[str, Any]] = []
    for rule in package_contract["required_inputs"]:
        matches = artifacts_matching_rule(rule)
        required_count, _ = package_rule_count_bounds(
            rule,
            direction_profile=direction_profile,
            current_idea_count=len(current_idea_refs),
            panel_role_count=len(panel_roles),
            workflow_conditions=workflow_conditions,
        )
        if rule.get("include_all_created") or rule.get("all_panel_instances"):
            chosen = matches
        else:
            chosen = matches[:required_count]
        package_parents.extend(chosen)
    package_parent_by_ref = {
        ref_for(artifact): artifact for artifact in package_parents
    }
    package_parents = list(package_parent_by_ref.values())
    package_parent_refs = [ref_for(artifact) for artifact in package_parents]

    perspective_internal_artifacts: list[dict[str, Any]] = []
    if expected_final_role == "verifier_compositor":
        prior_review_refs = [ref_for(artifact) for artifact in review_artifacts()]
        verifier_input_refs = list(
            dict.fromkeys([*package_parent_refs, *prior_review_refs])
        )
        if workflow == "perspective":
            panel_refs = [ref_for(artifact) for artifact in panel_artifacts]
            perspective_internal_artifacts.extend(
                [
                    add_artifact(
                        artifact_role="panel_summary",
                        source_skill=expected_final_skill,
                        creator_id=finalizer_id,
                        based_on=panel_refs,
                        change_type="panel_summary_assembly",
                        artifact_id="panel-summary",
                        document={"schema_version": 1, "panel_report_refs": panel_refs},
                        extra={"creation_sequence": 1},
                    ),
                    add_artifact(
                        artifact_role="artifact_index",
                        source_skill=expected_final_skill,
                        creator_id=finalizer_id,
                        based_on=prior_review_refs,
                        change_type="handoff_artifact_index",
                        artifact_id="handoff-artifact-index",
                        document={"schema_version": 1, "review_refs": prior_review_refs},
                        extra={"creation_sequence": 2},
                    ),
                ]
            )
        verification = add_review_report(
            actor_id=finalizer_id,
            artifact_role="verification_report",
            input_refs=verifier_input_refs,
            decision=pass_decision(expected_final_skill),
            artifact_id="final-verification",
            change_type="independent_final_verification",
            artifact_extra=(
                {"creation_sequence": 3} if workflow == "perspective" else None
            ),
        )
        if workflow == "perspective":
            perspective_internal_artifacts.append(verification)
        finding_index = add_finding_index(
            creation_sequence=4 if workflow == "perspective" else None
        )
        if workflow == "perspective":
            perspective_internal_artifacts.append(finding_index)
    elif workflow != "research_polisher":
        finding_index = add_finding_index()

    final_state = workflow_final_state_for(workflow, registry, direction_profile)
    final_role = (
        "research_polisher_selection_dossier"
        if workflow == "research_polisher"
        else "final_handoff_package"
    )
    package_extra: dict[str, Any] | None = None
    if workflow == "perspective":
        package_extra = {
            "creation_sequence": 5,
            "internal_output_refs": [
                ref_for(artifact) for artifact in perspective_internal_artifacts
            ],
        }
    final_package = add_artifact(
        artifact_role=final_role,
        source_skill=expected_final_skill,
        creator_id=finalizer_id,
        based_on=package_parent_refs,
        change_type="human_review_packaging",
        artifact_id="final-package",
        document={
            "schema_version": 1,
            "final_state": final_state,
            "source_edits_performed": False,
            "source_identity_unchanged": True,
            "input_artifact_refs": package_parent_refs,
            "preserved_dissent_ids": [],
            "unresolved_fatal_finding_ids": [],
        },
        extra=package_extra,
    )

    reads: list[dict[str, Any]] = []
    for actor_id, input_refs in actor_read_refs.items():
        for input_ref in sorted(input_refs):
            artifact = artifacts_by_ref[input_ref]
            path = root / Path(*PurePosixPath(artifact["path"]).parts)
            digest = sha256_file(path)
            reads.append(
                {
                    "actor_instance_id": actor_id,
                    "path": artifact["path"],
                    "sha256": digest,
                    "sha256_before": digest,
                    "sha256_after": digest,
                }
            )
    writes: list[dict[str, Any]] = []
    artifact_by_path = {artifact["path"]: artifact for artifact in artifacts}
    for actor_id, paths in actor_write_paths.items():
        for relative in sorted(paths):
            writes.append(
                {
                    "actor_instance_id": actor_id,
                    "path": relative,
                    "sha256": artifact_by_path[relative]["sha256"],
                    "allowed_write_root": "evidence",
                }
            )

    actor_manifest_path = evidence / "actor-manifest.json"
    write_json_file(
        actor_manifest_path,
        {
            "schema_version": 1,
            "workflow": workflow,
            "entry_mode": entry_mode,
            **identity,
            "actors": actors,
        },
    )
    artifact_index_path = evidence / "artifact-index.json"
    write_json_file(
        artifact_index_path,
        {
            "schema_version": 1,
            "workflow": workflow,
            "entry_mode": entry_mode,
            **identity,
            "artifacts": artifacts,
        },
    )
    file_access_path = evidence / "file-access.json"
    file_access_document = {
        "schema_version": 1,
        "workflow": workflow,
        "entry_mode": entry_mode,
        **identity,
        "reads": reads,
        "writes": writes,
        "source_artifact_hashes_unchanged": True,
    }
    write_json_file(file_access_path, file_access_document)
    actor_binding = {
        "path": "evidence/actor-manifest.json",
        "sha256": sha256_file(actor_manifest_path),
    }
    artifact_binding = {
        "path": "evidence/artifact-index.json",
        "sha256": sha256_file(artifact_index_path),
    }
    file_access_binding = {
        "path": "evidence/file-access.json",
        "sha256": sha256_file(file_access_path),
    }
    task_export_path = evidence / "task-export.json"
    task_export: dict[str, Any] = {
        "schema_version": 1,
        "platform": "codex",
        **identity,
        "workflow": workflow,
        "entry_mode": entry_mode,
        "case_kind": "happy",
        "final_state": final_state,
        "automatic_external_submission": False,
        "actor_manifest": actor_binding,
        "artifact_index": artifact_binding,
        "file_access": file_access_binding,
        "file_access_attestation": {
            "source_artifact_hashes_unchanged": True,
            "files_read_count": len(reads),
            "files_written_count": len(writes),
        },
        "final_package_actor_instance_id": finalizer_id,
    }
    if workflow == "idea":
        task_export["direction_profile"] = direction_profile
        task_export.update(workflow_conditions)
    if panel_skill is not None:
        task_export.update(
            {
                "panel_tier": panel_tier,
                "panel_role_instances": panel_role_instances,
            }
        )
    else:
        task_export["strategy_role_instances"] = {
            actor["strategy_role"]: actor["instance_id"]
            for actor in actors
            if actor["role"] == "strategy_reviewer"
        }
    write_json_file(task_export_path, task_export)
    task_binding = {
        "platform": "codex",
        "task_id": task_id,
        "entry_mode": entry_mode,
        "path": "evidence/task-export.json",
        "sha256": sha256_file(task_export_path),
    }
    receipt = {
        "receipt_id": f"phase7-contract-complete-{workflow}",
        "workflow": workflow,
        "entry_mode": entry_mode,
        "case_kind": "happy",
        "expected_final_state": final_state,
        "status": "verified",
        "binding": {
            "plugin_version": registry["plugin_version"],
            "registry_sha256": sha256_repository_file(REGISTRY_PATH),
            "source_commit": source_commit,
            "task_export": task_binding,
            "actor_manifest": actor_binding,
            "artifact_index": artifact_binding,
        },
        "file_access": {
            "reads": reads,
            "writes": writes,
            "source_artifact_hashes_unchanged": True,
        },
        "lineage": {
            "complete": True,
            "current_artifact_ref": current_ref,
            "evaluated_artifact_ref": current_ref,
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
        "final_state": final_state,
        "automatic_external_submission": False,
        "reason": "Contract-complete synthetic validator fixture only.",
    }
    if workflow == "idea":
        receipt["direction_profile"] = direction_profile
        receipt.update(workflow_conditions)
    return receipt


def run_runtime_validator_self_tests(
    *, schema: dict[str, Any], collection: dict[str, Any], registry: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fake_commit = "a" * 40
    results: list[dict[str, Any]] = []
    positive_workflow_results: list[dict[str, Any]] = []
    runtime_actor_role_contract(registry, schema)
    runtime_artifact_role_contract(registry)
    adaptive_idea_contract = validate_adaptive_idea_registry_contract(registry)
    expected_supporting_reviewer_skills = {
        "idea": {"academic-language-assessor", "methodology-statistics-preflight"},
        "proposal": {
            "academic-language-assessor",
            "methodology-statistics-preflight",
            "proposal-readiness-triage",
            "sap-evaluator",
        },
        "article": {
            "academic-language-assessor",
            "article-claim-auditor",
            "article-methods-statistics-auditor",
            "article-readiness-triage",
            "medical-journal-review",
            "methodology-statistics-preflight",
        },
        "perspective": {"academic-language-assessor", "medical-journal-review"},
        "research_polisher": {
            "medical-journal-review",
            "methodology-statistics-preflight",
        },
    }
    expected_supporting_writer_skills = {
        "idea": set(),
        "proposal": {"sap-writer"},
        "article": {"article-frontmatter-drafter"},
        "perspective": set(),
        "research_polisher": set(),
    }
    for workflow in registry["workflow_state_machines"]:
        reviewer_edges = edge_derived_actor_edges(
            registry, workflow, "supporting_reviewer"
        )
        writer_edges = edge_derived_actor_edges(
            registry, workflow, "supporting_writer"
        )
        require(
            {edge[1] for edge in reviewer_edges}
            == expected_supporting_reviewer_skills[workflow],
            "runtime_supporting_reviewer_edge_contract_invalid",
            workflow,
        )
        require(
            {edge[1] for edge in writer_edges}
            == expected_supporting_writer_skills[workflow],
            "runtime_supporting_writer_edge_contract_invalid",
            workflow,
        )

    def expect_direct_rejection(
        callback: Any, mutation: str, expected_code: str
    ) -> None:
        try:
            callback()
        except ModeViolation as exc:
            require(
                exc.code == expected_code,
                "runtime_negative_wrong_error",
                f"{mutation}: expected {expected_code}, got {exc.code}",
            )
            results.append(
                {
                    "mutation": mutation,
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation("runtime_negative_accepted", mutation)

    artifact_contract = runtime_artifact_role_contract(registry)

    def strategy_option(role: str, tier: str) -> dict[str, Any]:
        is_reposition = tier == "reposition_only"
        flags = {
            "new_analysis": tier == "moderate_extension",
            "new_experiment": False,
            "new_data": False,
            "new_validation": tier == "small_extension",
        }
        return {
            "proposal_id": f"{role}-{tier}",
            "effort_tier": tier,
            "status": "proposed",
            "positioning_change": "Reframe the contribution for the selected lens.",
            "value_gain_mechanism": "Clarifies why the result matters to the audience.",
            "claim_delta": "Keeps claims traceable while changing their hierarchy.",
            "target_audience": "Relevant scientific and practice stakeholders.",
            "added_work_items": [] if is_reposition else ["One bounded validation package."],
            "resource_dependencies": [] if is_reposition else ["Existing study assets."],
            "feasibility": {"rating": "high", "basis": "Uses available assets and a bounded method."},
            "evidence_dependencies": ["Frozen dossier evidence."],
            "risks": ["The impact gain may remain outlet-dependent."],
            "stop_conditions": ["Stop if the claim would exceed frozen evidence."],
            "new_work_flags": flags,
            "bounded_package": True,
            "independent_new_study": False,
            "core_design_rebuild": False,
        }

    polisher_matrix = artifact_contract["research_polisher_strategy_matrix_contract"]
    strategy_actors: dict[str, dict[str, Any]] = {}
    strategy_reports: dict[str, dict[str, Any]] = {}
    strategy_cells: dict[str, set[tuple[str, str]]] = {}
    strategy_artifacts: list[dict[str, Any]] = []
    for index, role in enumerate(polisher_matrix["strategy_roles"], start=1):
        actor_id = f"strategy-{index:03d}"
        actor = {
            "instance_id": actor_id,
            "skill": polisher_matrix["strategy_skill"],
            "role": "strategy_reviewer",
            "strategy_role": role,
        }
        report = {
            "strategy_role": role,
            "peer_outputs_visible": False,
            "strategy_options": [
                strategy_option(role, tier)
                for tier in polisher_matrix["effort_tiers"]
            ],
        }
        report_ref = f"strategy-report-{index:03d}@v001"
        strategy_actors[actor_id] = actor
        strategy_reports[report_ref] = report
        strategy_cells[report_ref] = validate_research_polisher_strategy_report_runtime(
            report, actor, artifact_contract, report_ref
        )
        strategy_artifacts.append(
            {
                "artifact_id": f"strategy-report-{index:03d}",
                "version_id": "v001",
                "artifact_role": "research_polisher_strategy_report",
                "path": f"evidence/strategy-report-{index:03d}.json",
                "source_skill": polisher_matrix["strategy_skill"],
                "created_by_instance_id": actor_id,
                "based_on": ["dossier@v001"],
            }
        )
    assembler_id = "polisher-assembler-001"
    portfolio_artifact = {
        "artifact_id": "portfolio",
        "version_id": "v001",
        "artifact_role": "research_polisher_candidate_portfolio",
        "path": "evidence/portfolio.json",
        "source_skill": polisher_matrix["portfolio_skill"],
        "created_by_instance_id": assembler_id,
        "based_on": list(strategy_reports),
    }
    polisher_actor_map = {
        **strategy_actors,
        assembler_id: {
            "instance_id": assembler_id,
            "skill": polisher_matrix["portfolio_skill"],
            "role": "assembler",
        },
    }
    polisher_reads = {
        assembler_id: {artifact["path"] for artifact in strategy_artifacts}
    }
    validate_research_polisher_portfolio_lineage_runtime(
        artifacts=[*strategy_artifacts, portfolio_artifact],
        actor_by_id=polisher_actor_map,
        strategy_cells_by_ref=strategy_cells,
        read_paths_by_actor=polisher_reads,
        contract=artifact_contract,
    )

    missing_tier_report = copy.deepcopy(next(iter(strategy_reports.values())))
    missing_tier_report["strategy_options"].pop()
    expect_direct_rejection(
        lambda: validate_research_polisher_strategy_report_runtime(
            missing_tier_report,
            strategy_actors["strategy-001"],
            artifact_contract,
            "missing-tier",
        ),
        "polisher_strategy_report_missing_tier",
        "runtime_polisher_strategy_matrix_incomplete",
    )
    smuggled_reposition = copy.deepcopy(next(iter(strategy_reports.values())))
    smuggled_reposition["strategy_options"][0]["added_work_items"] = [
        "Run an undeclared new analysis."
    ]
    smuggled_reposition["strategy_options"][0]["new_work_flags"][
        "new_analysis"
    ] = True
    expect_direct_rejection(
        lambda: validate_research_polisher_strategy_report_runtime(
            smuggled_reposition,
            strategy_actors["strategy-001"],
            artifact_contract,
            "smuggled-reposition",
        ),
        "polisher_reposition_smuggles_new_analysis",
        "runtime_polisher_reposition_smuggles_new_work",
    )
    low_feasibility = copy.deepcopy(next(iter(strategy_reports.values())))
    low_feasibility["strategy_options"][1]["feasibility"]["rating"] = "low"
    expect_direct_rejection(
        lambda: validate_research_polisher_strategy_report_runtime(
            low_feasibility,
            strategy_actors["strategy-001"],
            artifact_contract,
            "low-feasibility",
        ),
        "polisher_low_feasibility_marked_proposed",
        "runtime_polisher_extension_feasibility_invalid",
    )
    missing_claim_delta = copy.deepcopy(next(iter(strategy_reports.values())))
    missing_claim_delta["strategy_options"][1].pop("claim_delta")
    expect_direct_rejection(
        lambda: validate_research_polisher_strategy_report_runtime(
            missing_claim_delta,
            strategy_actors["strategy-001"],
            artifact_contract,
            "missing-claim-delta",
        ),
        "polisher_strategy_option_missing_required_field",
        "runtime_polisher_strategy_option_schema",
    )
    generic_strategy_artifacts = copy.deepcopy(strategy_artifacts)
    generic_strategy_artifacts[-1]["artifact_role"] = "review_report"
    expect_direct_rejection(
        lambda: validate_research_polisher_portfolio_lineage_runtime(
            artifacts=[*generic_strategy_artifacts, portfolio_artifact],
            actor_by_id=polisher_actor_map,
            strategy_cells_by_ref=strategy_cells,
            read_paths_by_actor=polisher_reads,
            contract=artifact_contract,
        ),
        "polisher_generic_review_substitutes_strategy_report",
        "runtime_polisher_candidate_portfolio_strategy_lineage",
    )
    expect_direct_rejection(
        lambda: validate_actor_output_role_runtime(
            actor=strategy_actors["strategy-001"],
            artifact={"artifact_role": "review_report"},
            contract=artifact_contract,
        ),
        "polisher_strategist_writes_generic_review_report",
        "runtime_actor_output_role_mismatch",
    )
    incomplete_reads = {assembler_id: set(polisher_reads[assembler_id])}
    incomplete_reads[assembler_id].remove(strategy_artifacts[-1]["path"])
    expect_direct_rejection(
        lambda: validate_research_polisher_portfolio_lineage_runtime(
            artifacts=[*strategy_artifacts, portfolio_artifact],
            actor_by_id=polisher_actor_map,
            strategy_cells_by_ref=strategy_cells,
            read_paths_by_actor=incomplete_reads,
            contract=artifact_contract,
        ),
        "polisher_assembler_does_not_read_all_strategy_reports",
        "runtime_polisher_assembler_strategy_report_not_read",
    )

    sap_actor_map = {
        "sap-writer-001": {
            "instance_id": "sap-writer-001",
            "role": "supporting_writer",
            "skill": "sap-writer",
        },
        "sap-evaluator-001": {
            "instance_id": "sap-evaluator-001",
            "role": "supporting_reviewer",
            "skill": "sap-evaluator",
            "isolation_mode": "fresh_subagent",
        },
    }
    sap_v1 = {"artifact_id": "sap", "version_id": "v001", "artifact_role": "sap", "source_skill": "sap-writer", "created_by_instance_id": "sap-writer-001"}
    sap_v2 = {"artifact_id": "sap", "version_id": "v002", "artifact_role": "sap", "source_skill": "sap-writer", "created_by_instance_id": "sap-writer-001"}
    sap_eval_v2 = {"artifact_id": "sap-eval", "version_id": "v002", "artifact_role": "evaluation_report", "source_skill": "sap-evaluator", "created_by_instance_id": "sap-evaluator-001", "based_on": ["sap@v002"], "change_type": "fresh_independent_evaluation"}
    validate_proposal_sap_package_runtime(
        package_parent_artifacts=[sap_v2, sap_eval_v2],
        artifacts=[sap_v1, sap_v2, sap_eval_v2],
        actor_by_id=sap_actor_map,
    )
    expect_direct_rejection(
        lambda: validate_proposal_sap_package_runtime(
            package_parent_artifacts=[sap_eval_v2], artifacts=[sap_eval_v2], actor_by_id=sap_actor_map
        ),
        "proposal_package_missing_sap_writer_artifact",
        "runtime_sap_writer_artifact_missing",
    )
    expect_direct_rejection(
        lambda: validate_proposal_sap_package_runtime(
            package_parent_artifacts=[sap_v2], artifacts=[sap_v1, sap_v2], actor_by_id=sap_actor_map
        ),
        "proposal_package_missing_sap_evaluator",
        "runtime_sap_evaluation_lineage_mismatch",
    )
    wrong_sap_writer_actor = copy.deepcopy(sap_actor_map)
    wrong_sap_writer_actor["sap-writer-001"]["role"] = "writer"
    expect_direct_rejection(
        lambda: validate_proposal_sap_package_runtime(
            package_parent_artifacts=[sap_v2, sap_eval_v2],
            artifacts=[sap_v1, sap_v2, sap_eval_v2],
            actor_by_id=wrong_sap_writer_actor,
        ),
        "proposal_sap_not_created_by_supporting_writer",
        "runtime_sap_writer_actor_mismatch",
    )
    inline_sap_evaluator = copy.deepcopy(sap_actor_map)
    inline_sap_evaluator["sap-evaluator-001"]["isolation_mode"] = "inline"
    expect_direct_rejection(
        lambda: validate_proposal_sap_package_runtime(
            package_parent_artifacts=[sap_v2, sap_eval_v2],
            artifacts=[sap_v1, sap_v2, sap_eval_v2],
            actor_by_id=inline_sap_evaluator,
        ),
        "proposal_sap_evaluator_not_fresh",
        "runtime_sap_evaluator_actor_mismatch",
    )
    expect_direct_rejection(
        lambda: validate_proposal_sap_package_runtime(
            package_parent_artifacts=[sap_v1, {**sap_eval_v2, "based_on": ["sap@v001"]}],
            artifacts=[sap_v1, sap_v2, sap_eval_v2],
            actor_by_id=sap_actor_map,
        ),
        "proposal_package_selects_stale_sap",
        "runtime_sap_package_stale_selection",
    )
    expect_direct_rejection(
        lambda: validate_proposal_sap_package_runtime(
            package_parent_artifacts=[sap_v2, {**sap_eval_v2, "based_on": ["sap@v001"]}],
            artifacts=[sap_v1, sap_v2, sap_eval_v2],
            actor_by_id=sap_actor_map,
        ),
        "proposal_sap_evaluator_reviews_stale_version",
        "runtime_sap_evaluation_lineage_mismatch",
    )

    external_contract = artifact_contract["external_input_contract"]
    for mutation, workflow, role, spoofed_skill in (
        ("external_input_impersonates_sap_writer", "proposal", "sap", "sap-writer"),
        ("external_input_impersonates_sap_evaluator", "proposal", "evaluation_report", "sap-evaluator"),
        ("external_input_impersonates_readiness_reviewer", "proposal", "readiness_report", "proposal-readiness-triage"),
        ("external_input_impersonates_article_auditor", "article", "audit_report", "article-claim-auditor"),
        ("external_input_impersonates_revision_delta", "proposal", "revision_delta", "proposal-drafter"),
    ):
        fake_external = {
            "artifact_id": mutation,
            "artifact_role": role,
            "created_by_instance_id": "external-input",
            "source_skill": spoofed_skill,
            "external_source_id": "external:user-file",
        }
        expect_direct_rejection(
            lambda artifact=fake_external, selected_workflow=workflow: validate_external_input_artifact_runtime(
                artifact=artifact,
                workflow=selected_workflow,
                entry_mode="standard",
                contract=external_contract,
            ),
            mutation,
            "runtime_external_input_impersonation",
        )
    expect_direct_rejection(
        lambda: validate_blind_reviewer_inputs_runtime(
            reviewer_id="blind-evaluator",
            read_paths={"evidence/result-oracle.json"},
            artifacts_by_path={
                "evidence/result-oracle.json": {"artifact_role": "result_oracle"}
            },
            forbidden_oracle_roles={"result_oracle", "review_oracle"},
        ),
        "blind_reviewer_reads_result_oracle",
        "runtime_reviewer_oracle_visible",
    )

    verifier_fatal_report = {
        "decision": "human_signoff_required",
        "findings": [{"id": "verifier-fatal-001", "severity": "fatal", "blocking": True, "resolved": False, "dissent": False}],
        "unresolved_issues": ["verifier-fatal-001"],
        "dissent_ids": [],
        "fatal_finding_ids": ["verifier-fatal-001"],
        "unresolved_fatal_finding_ids": ["verifier-fatal-001"],
    }
    _, _, verifier_unresolved_fatal, _ = validate_runtime_review_report_findings(
        verifier_fatal_report, artifact_contract, "verifier-fatal"
    )
    require(
        artifact_is_review_finding_report(
            creator_role="verifier_compositor",
            artifact_role="verification_report",
            contract=artifact_contract,
        )
        and not artifact_is_review_finding_report(
            creator_role="verifier_compositor",
            artifact_role="final_handoff_package",
            contract=artifact_contract,
        ),
        "runtime_verifier_finding_contract_invalid",
        "verification report selection",
    )
    expect_direct_rejection(
        lambda: validate_ready_has_no_unresolved_fatal(
            verifier_unresolved_fatal, "verifier-fatal"
        ),
        "verifier_fatal_finding_false_ready",
        "runtime_false_ready",
    )

    for workflow in (
        "idea",
        "proposal",
        "article",
        "perspective",
        "research_polisher",
    ):
        control_contract = runtime_case_contract(schema, workflow, "control")
        current_ref = f"{workflow}-current@v001"
        finding_id = f"{workflow}-control-finding"
        reports = {
            skill: [{"synthetic": True}]
            for skill in control_contract["required_review_skills"]
        }
        finding_skill = next(
            reversed(control_contract["control_finding_decisions_by_skill"])
        )
        finding_decision = control_contract[
            "control_finding_decisions_by_skill"
        ][finding_skill][0]
        provenance = {
            finding_id: {
                "creator": {"skill": finding_skill},
                "input_refs": {current_ref},
                "decision_pass": False,
                "report": {"decision": finding_decision},
                "finding": {
                    "id": finding_id,
                    "severity": control_contract[
                        "control_finding_allowed_severities"
                    ][0],
                    "blocking": control_contract["control_finding_blocking"],
                    "resolved": control_contract["control_finding_resolved"],
                    "dissent": False,
                },
            }
        }
        control_strategy_roles: dict[str, str] = {}
        control_strategy_cells: dict[str, set[tuple[str, str]]] = {}
        if control_contract["required_strategy_matrix"]:
            control_strategy_roles = {
                role: f"{workflow}-{index}"
                for index, role in enumerate(polisher_matrix["strategy_roles"], start=1)
            }
            control_strategy_cells = strategy_cells
        validate_control_independent_gates_runtime(
            workflow=workflow,
            case_contract=control_contract,
            current_ref=current_ref,
            control_finding_id=finding_id,
            review_reports_by_skill=reports,
            finding_provenance=provenance,
            strategy_role_instances=control_strategy_roles,
            strategy_cells_by_ref=control_strategy_cells,
            registry=registry,
        )
        if workflow == "research_polisher":
            mutated_strategy_roles = dict(control_strategy_roles)
            mutated_strategy_roles.pop(next(iter(mutated_strategy_roles)))
            callback = lambda roles=mutated_strategy_roles: validate_control_independent_gates_runtime(
                workflow=workflow,
                case_contract=control_contract,
                current_ref=current_ref,
                control_finding_id=finding_id,
                review_reports_by_skill=reports,
                finding_provenance=provenance,
                strategy_role_instances=roles,
                strategy_cells_by_ref=control_strategy_cells,
                registry=registry,
            )
        else:
            missing_reports = dict(reports)
            missing_reports.pop(control_contract["required_review_skills"][0])
            callback = lambda report_map=missing_reports: validate_control_independent_gates_runtime(
                workflow=workflow,
                case_contract=control_contract,
                current_ref=current_ref,
                control_finding_id=finding_id,
                review_reports_by_skill=report_map,
                finding_provenance=provenance,
                strategy_role_instances=control_strategy_roles,
                strategy_cells_by_ref=control_strategy_cells,
                registry=registry,
            )
        expect_direct_rejection(
            callback,
            f"{workflow}_control_missing_required_independent_gate",
            "runtime_control_required_independent_gate_missing",
        )

        wrong_decision_provenance = copy.deepcopy(provenance)
        allowed_decisions = registry["scenario_eval_contract"][
            "review_decision_contracts"
        ][finding_skill]["allowed"]
        wrong_decision = next(
            (
                decision
                for decision in allowed_decisions
                if decision
                not in set(
                    control_contract["control_finding_decisions_by_skill"][
                        finding_skill
                    ]
                )
            ),
            "invalid_control_decision",
        )
        wrong_decision_provenance[finding_id]["report"]["decision"] = (
            wrong_decision
        )
        expect_direct_rejection(
            lambda provenance_map=wrong_decision_provenance: validate_control_independent_gates_runtime(
                workflow=workflow,
                case_contract=control_contract,
                current_ref=current_ref,
                control_finding_id=finding_id,
                review_reports_by_skill=reports,
                finding_provenance=provenance_map,
                strategy_role_instances=control_strategy_roles,
                strategy_cells_by_ref=control_strategy_cells,
                registry=registry,
            ),
            f"{workflow}_control_finding_uses_non_stop_decision",
            "runtime_control_finding_provenance_mismatch",
        )

        for field, value, mutation in (
            (
                "blocking",
                not control_contract["control_finding_blocking"],
                "nonblocking_control_finding",
            ),
            (
                "resolved",
                not control_contract["control_finding_resolved"],
                "resolved_control_finding",
            ),
        ):
            wrong_semantics_provenance = copy.deepcopy(provenance)
            wrong_semantics_provenance[finding_id]["finding"][field] = value
            expect_direct_rejection(
                lambda provenance_map=wrong_semantics_provenance: validate_control_independent_gates_runtime(
                    workflow=workflow,
                    case_contract=control_contract,
                    current_ref=current_ref,
                    control_finding_id=finding_id,
                    review_reports_by_skill=reports,
                    finding_provenance=provenance_map,
                    strategy_role_instances=control_strategy_roles,
                    strategy_cells_by_ref=control_strategy_cells,
                    registry=registry,
                ),
                f"{workflow}_{mutation}",
                "runtime_control_finding_semantics_mismatch",
            )

    def expect_registry_contract_rejection(
        mutated_registry: dict[str, Any], mutation: str, expected_code: str
    ) -> None:
        try:
            runtime_artifact_role_contract(mutated_registry)
        except ModeViolation as exc:
            require(
                exc.code == expected_code,
                "runtime_negative_wrong_error",
                f"{mutation}: expected {expected_code}, got {exc.code}",
            )
            results.append(
                {
                    "mutation": mutation,
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation("runtime_negative_accepted", mutation)

    missing_polisher_assembler_role = copy.deepcopy(registry)
    missing_polisher_assembler_role["scenario_eval_contract"][
        "runtime_artifact_role_contract"
    ]["assembler_outputs_by_skill"]["research-polisher-plan-assembler"].remove(
        "research_polisher_specialist_findings_bundle"
    )
    expect_registry_contract_rejection(
        missing_polisher_assembler_role,
        "polisher_assembler_output_role_omitted",
        "runtime_artifact_role_contract_invalid",
    )
    wrong_polisher_finding_role = copy.deepcopy(registry)
    wrong_polisher_finding_role["scenario_eval_contract"][
        "runtime_artifact_role_contract"
    ]["finding_index_role_by_workflow"]["research_polisher"] = "review_finding_index"
    expect_registry_contract_rejection(
        wrong_polisher_finding_role,
        "polisher_finding_index_uses_generic_role",
        "runtime_artifact_role_contract_invalid",
    )
    with tempfile.TemporaryDirectory(prefix="phase7-runtime-validator-") as directory:
        root = Path(directory)
        results.extend(
            bounded_idea_evaluator_negative_self_tests(root=root, registry=registry)
        )

        for workflow in registry["workflow_state_machines"]:
            complete_fixture = build_contract_complete_workflow_fixture(
                root, registry, fake_commit, workflow
            )
            validated_complete = validate_runtime_receipt(
                complete_fixture,
                registry=registry,
                schema=schema,
                expected_source_commit=fake_commit,
                root=root,
            )
            workflow_result = {
                    "workflow": workflow,
                    "status": "passed",
                    "receipt_id": validated_complete["receipt_id"],
                    "final_state": validated_complete["final_state"],
                    "actor_counts": validated_complete["actor_counts"],
                    "artifact_count": validated_complete["artifact_count"],
                }
            if workflow == "idea":
                workflow_result["adaptive_direction_contract"] = adaptive_idea_contract
            positive_workflow_results.append(workflow_result)

        def expect_runtime_rejection(
            mutated: dict[str, Any], mutation: str, expected_code: str
        ) -> None:
            try:
                validate_runtime_receipt(
                    mutated,
                    registry=registry,
                    schema=schema,
                    expected_source_commit=fake_commit,
                    root=root,
                )
            except ModeViolation as exc:
                require(
                    exc.code == expected_code,
                    "runtime_negative_wrong_error",
                    f"{mutation}: expected {expected_code}, got {exc.code}",
                )
                results.append(
                    {
                        "mutation": mutation,
                        "status": "rejected_as_expected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise ModeViolation("runtime_negative_accepted", mutation)

        def refresh_linked_bindings(mutated: dict[str, Any]) -> None:
            actor_path = root / Path(
                *PurePosixPath(mutated["binding"]["actor_manifest"]["path"]).parts
            )
            artifact_path = root / Path(
                *PurePosixPath(mutated["binding"]["artifact_index"]["path"]).parts
            )
            task_path = root / Path(
                *PurePosixPath(mutated["binding"]["task_export"]["path"]).parts
            )
            mutated["binding"]["actor_manifest"]["sha256"] = sha256_file(actor_path)
            mutated["binding"]["artifact_index"]["sha256"] = sha256_file(artifact_path)
            task_document = load_structured_file(task_path)
            file_access_binding = task_document.get("file_access")
            if isinstance(file_access_binding, dict) and file_access_binding.get("path"):
                file_access_path = root / Path(
                    *PurePosixPath(file_access_binding["path"]).parts
                )
                file_access_document = load_structured_file(file_access_path)
                file_access_document.update(mutated["file_access"])
                write_json_file(file_access_path, file_access_document)
                task_document["file_access"] = {
                    "path": file_access_binding["path"],
                    "sha256": sha256_file(file_access_path),
                }
            task_document["actor_manifest"] = mutated["binding"]["actor_manifest"]
            task_document["artifact_index"] = mutated["binding"]["artifact_index"]
            task_document["file_access_attestation"] = {
                "source_artifact_hashes_unchanged": True,
                "files_read_count": len(mutated["file_access"]["reads"]),
                "files_written_count": len(mutated["file_access"]["writes"]),
            }
            write_json_file(task_path, task_document)
            mutated["binding"]["task_export"]["sha256"] = sha256_file(task_path)

        def refresh_indexed_artifact_binding(
            mutated: dict[str, Any],
            relative_path: str,
            *,
            based_on: list[str] | None = None,
        ) -> None:
            target_path = root / Path(*PurePosixPath(relative_path).parts)
            digest = sha256_file(target_path)
            artifact_path = root / Path(
                *PurePosixPath(
                    mutated["binding"]["artifact_index"]["path"]
                ).parts
            )
            artifact_document = load_structured_file(artifact_path)
            indexed_artifact = next(
                artifact
                for artifact in artifact_document["artifacts"]
                if artifact["path"] == relative_path
            )
            indexed_artifact["sha256"] = digest
            if based_on is not None:
                indexed_artifact["based_on"] = based_on
            write_json_file(artifact_path, artifact_document)
            for entry in mutated["file_access"]["reads"]:
                if entry["path"] == relative_path:
                    entry["sha256"] = digest
                    entry["sha256_before"] = digest
                    entry["sha256_after"] = digest
            for entry in mutated["file_access"]["writes"]:
                if entry["path"] == relative_path:
                    entry["sha256"] = digest
            refresh_linked_bindings(mutated)

        def load_bound_artifact_index(
            receipt: dict[str, Any],
        ) -> tuple[Path, dict[str, Any]]:
            artifact_path = root / Path(
                *PurePosixPath(receipt["binding"]["artifact_index"]["path"]).parts
            )
            return artifact_path, load_structured_file(artifact_path)

        def load_bound_actor_manifest(
            receipt: dict[str, Any],
        ) -> dict[str, Any]:
            actor_path = root / Path(
                *PurePosixPath(receipt["binding"]["actor_manifest"]["path"]).parts
            )
            return load_structured_file(actor_path)

        supporting_nonpass = build_contract_complete_workflow_fixture(
            root, registry, fake_commit, "article"
        )
        _, supporting_index = load_bound_artifact_index(supporting_nonpass)
        supporting_artifact = next(
            artifact
            for artifact in supporting_index["artifacts"]
            if artifact["source_skill"] == "article-methods-statistics-auditor"
        )
        supporting_report_path = root / Path(
            *PurePosixPath(supporting_artifact["path"]).parts
        )
        supporting_report = load_structured_file(supporting_report_path)
        supporting_report["decision"] = "methodologically_blocked"
        supporting_report["findings"] = [
            {
                "id": "supporting-block-001",
                "severity": "major",
                "blocking": True,
                "resolved": False,
                "dissent": False,
            }
        ]
        supporting_report["unresolved_issues"] = ["supporting-block-001"]
        write_json_file(supporting_report_path, supporting_report)
        refresh_indexed_artifact_binding(
            supporting_nonpass, supporting_artifact["path"]
        )
        expect_runtime_rejection(
            supporting_nonpass,
            "ready_article_with_nonpass_supporting_reviewer",
            "runtime_ready_review_decision_not_pass",
        )

        unresolved_pass = build_contract_complete_workflow_fixture(
            root, registry, fake_commit, "article"
        )
        _, unresolved_index = load_bound_artifact_index(unresolved_pass)
        current_ref = unresolved_pass["lineage"]["current_artifact_ref"]
        current_evaluation = next(
            artifact
            for artifact in unresolved_index["artifacts"]
            if artifact["source_skill"] == "article-evaluator"
            and current_ref in artifact["based_on"]
        )
        unresolved_report_path = root / Path(
            *PurePosixPath(current_evaluation["path"]).parts
        )
        unresolved_report = load_structured_file(unresolved_report_path)
        unresolved_report["findings"] = [
            {
                "id": "major-block-001",
                "severity": "major",
                "blocking": True,
                "resolved": False,
                "dissent": False,
            }
        ]
        unresolved_report["unresolved_issues"] = ["major-block-001"]
        write_json_file(unresolved_report_path, unresolved_report)
        refresh_indexed_artifact_binding(
            unresolved_pass, current_evaluation["path"]
        )
        expect_runtime_rejection(
            unresolved_pass,
            "ready_article_with_pass_decision_and_unresolved_blocking_finding",
            "runtime_ready_review_decision_not_pass",
        )

        duplicate_reviewer_report = build_contract_complete_workflow_fixture(
            root, registry, fake_commit, "idea"
        )
        duplicate_index_path, duplicate_index = load_bound_artifact_index(
            duplicate_reviewer_report
        )
        duplicate_actor_manifest = load_bound_actor_manifest(
            duplicate_reviewer_report
        )
        panel_actor_ids = {
            actor["instance_id"]
            for actor in duplicate_actor_manifest["actors"]
            if actor["role"] == "panel"
        }
        original_panel_artifact = next(
            artifact
            for artifact in duplicate_index["artifacts"]
            if artifact["created_by_instance_id"] in panel_actor_ids
        )
        original_panel_path = root / Path(
            *PurePosixPath(original_panel_artifact["path"]).parts
        )
        duplicate_panel_path_value = "evidence/duplicate-panel-report.json"
        duplicate_panel_path = root / Path(
            *PurePosixPath(duplicate_panel_path_value).parts
        )
        duplicate_panel_document = copy.deepcopy(
            load_structured_file(original_panel_path)
        )
        write_json_file(duplicate_panel_path, duplicate_panel_document)
        duplicate_panel_artifact = copy.deepcopy(original_panel_artifact)
        duplicate_panel_artifact.update(
            {
                "artifact_id": "duplicate-panel-report",
                "version_id": "v001",
                "path": duplicate_panel_path_value,
                "sha256": sha256_file(duplicate_panel_path),
            }
        )
        duplicate_index["artifacts"].append(duplicate_panel_artifact)
        write_json_file(duplicate_index_path, duplicate_index)
        duplicate_reviewer_report["file_access"]["writes"].append(
            {
                "actor_instance_id": original_panel_artifact[
                    "created_by_instance_id"
                ],
                "path": duplicate_panel_path_value,
                "sha256": sha256_file(duplicate_panel_path),
            }
        )
        refresh_linked_bindings(duplicate_reviewer_report)
        expect_runtime_rejection(
            duplicate_reviewer_report,
            "same_reviewer_instance_emits_multiple_reports",
            "runtime_reviewer_multiple_reports",
        )

        stale_actual_panel_read = build_contract_complete_workflow_fixture(
            root, registry, fake_commit, "perspective"
        )
        _, stale_read_index = load_bound_artifact_index(stale_actual_panel_read)
        stale_actor_manifest = load_bound_actor_manifest(stale_actual_panel_read)
        stale_panel_id = next(
            actor["instance_id"]
            for actor in stale_actor_manifest["actors"]
            if actor["role"] == "panel"
        )
        stale_current_artifact_id, stale_current_version = (
            stale_actual_panel_read["lineage"]["current_artifact_ref"].split("@")
        )
        stale_source = next(
            artifact
            for artifact in stale_read_index["artifacts"]
            if artifact["artifact_id"] == stale_current_artifact_id
            and artifact["version_id"] != stale_current_version
        )
        stale_read_entry = next(
            entry
            for entry in stale_actual_panel_read["file_access"]["reads"]
            if entry["actor_instance_id"] == stale_panel_id
        )
        stale_read_entry.update(
            {
                "path": stale_source["path"],
                "sha256": stale_source["sha256"],
                "sha256_before": stale_source["sha256"],
                "sha256_after": stale_source["sha256"],
            }
        )
        refresh_linked_bindings(stale_actual_panel_read)
        expect_runtime_rejection(
            stale_actual_panel_read,
            "panel_claims_current_input_but_reads_stale_file",
            "runtime_review_input_read_mismatch",
        )

        compositor_self_read = build_contract_complete_workflow_fixture(
            root, registry, fake_commit, "perspective"
        )
        _, compositor_index = load_bound_artifact_index(compositor_self_read)
        compositor_actor_manifest = load_bound_actor_manifest(compositor_self_read)
        compositor_id = next(
            actor["instance_id"]
            for actor in compositor_actor_manifest["actors"]
            if actor["skill"] == "perspective-final-compositor"
        )
        compositor_internal_artifact = next(
            artifact
            for artifact in compositor_index["artifacts"]
            if artifact["created_by_instance_id"] == compositor_id
            and artifact["artifact_role"] == "artifact_index"
        )
        compositor_self_read["file_access"]["reads"].append(
            {
                "actor_instance_id": compositor_id,
                "path": compositor_internal_artifact["path"],
                "sha256": compositor_internal_artifact["sha256"],
                "sha256_before": compositor_internal_artifact["sha256"],
                "sha256_after": compositor_internal_artifact["sha256"],
            }
        )
        refresh_linked_bindings(compositor_self_read)
        expect_runtime_rejection(
            compositor_self_read,
            "perspective_compositor_reads_its_own_internal_output",
            "runtime_reviewer_modified_input",
        )

        compositor_order = build_contract_complete_workflow_fixture(
            root, registry, fake_commit, "perspective"
        )
        compositor_order_index_path, compositor_order_index = (
            load_bound_artifact_index(compositor_order)
        )
        order_actor_manifest = load_bound_actor_manifest(compositor_order)
        order_compositor_id = next(
            actor["instance_id"]
            for actor in order_actor_manifest["actors"]
            if actor["skill"] == "perspective-final-compositor"
        )
        next(
            artifact
            for artifact in compositor_order_index["artifacts"]
            if artifact["created_by_instance_id"] == order_compositor_id
            and artifact["artifact_role"] == "artifact_index"
        )["creation_sequence"] = 1
        write_json_file(compositor_order_index_path, compositor_order_index)
        refresh_linked_bindings(compositor_order)
        expect_runtime_rejection(
            compositor_order,
            "perspective_compositor_internal_outputs_out_of_order",
            "runtime_compositor_creation_order_mismatch",
        )

        compositor_dependencies = build_contract_complete_workflow_fixture(
            root, registry, fake_commit, "perspective"
        )
        dependency_index_path, dependency_index = load_bound_artifact_index(
            compositor_dependencies
        )
        dependency_actor_manifest = load_bound_actor_manifest(
            compositor_dependencies
        )
        dependency_compositor_id = next(
            actor["instance_id"]
            for actor in dependency_actor_manifest["actors"]
            if actor["skill"] == "perspective-final-compositor"
        )
        next(
            artifact
            for artifact in dependency_index["artifacts"]
            if artifact["created_by_instance_id"] == dependency_compositor_id
            and artifact["artifact_role"] == "final_handoff_package"
        )["internal_output_refs"] = []
        write_json_file(dependency_index_path, dependency_index)
        refresh_linked_bindings(compositor_dependencies)
        expect_runtime_rejection(
            compositor_dependencies,
            "perspective_compositor_internal_dependencies_omitted",
            "runtime_compositor_internal_dependency_mismatch",
        )

        def expect_collection_rejection(
            mutated: dict[str, Any],
            mutation: str,
            expected_code: str,
            *,
            validated_evidence_results: dict[str, Any] | None = None,
        ) -> None:
            try:
                validate_runtime_collection(
                    mutated,
                    schema=schema,
                    registry=registry,
                    expected_source_commit=fake_commit,
                    root=root,
                    validated_evidence_results=validated_evidence_results,
                )
            except ModeViolation as exc:
                require(
                    exc.code == expected_code,
                    "runtime_negative_wrong_error",
                    f"{mutation}: expected {expected_code}, got {exc.code}",
                )
                results.append(
                    {
                        "mutation": mutation,
                        "status": "rejected_as_expected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise ModeViolation("runtime_negative_accepted", mutation)

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        validate_runtime_receipt(
            valid,
            registry=registry,
            schema=schema,
            expected_source_commit=fake_commit,
            root=root,
        )
        raw_payload = (
            root / Path(*PurePosixPath(valid["binding"]["task_export"]["path"]).parts)
        ).read_bytes()
        integrity_results: dict[str, EvidenceValidationResult] = {}
        for verification_level in (PREVIEW_ATTESTED, PROVIDER_VERIFIED):
            evidence_result = _build_test_only_attested_evidence(
                raw_payload=raw_payload,
                registry=registry,
                source_commit=fake_commit,
                verification_level=verification_level,
            )
            integrity_results[verification_level] = evidence_result.integrity_result
            accounted = validate_runtime_receipt(
                valid,
                registry=registry,
                schema=schema,
                expected_source_commit=fake_commit,
                root=root,
                evidence_result=evidence_result,
            )
            require(
                accounted["verification_level"] == verification_level
                and accounted["evidence_accounting_status"]
                == "synthetic_authenticated_reachability_only",
                "runtime_evidence_accounting_mapping",
                verification_level,
            )
            require(
                evidence_result.counts_as_runtime_evidence is False,
                "synthetic_attestation_runtime_evidence_leak",
                verification_level,
            )
            if verification_level == PREVIEW_ATTESTED:
                try:
                    validate_runtime_receipt(
                        valid,
                        registry=registry,
                        schema=schema,
                        expected_source_commit=fake_commit,
                        root=root,
                        evidence_result=evidence_result.integrity_result,
                    )
                except ModeViolation as exc:
                    require(
                        exc.code
                        == "runtime_evidence_authenticated_attestation_missing",
                        "runtime_negative_wrong_error",
                        f"integrity_only_promotion: {exc.code}",
                    )
                    results.append(
                        {
                            "mutation": "integrity_only_result_promoted_without_attestation",
                            "status": "rejected_as_expected",
                            "error_code": exc.code,
                        }
                    )
                else:
                    raise ModeViolation(
                        "runtime_negative_accepted",
                        "integrity_only_result_promoted_without_attestation",
                    )

        class SyntheticRuntimeLiveVerifier:
            adapter_id = PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID

            def __init__(self, mutator: Any = None) -> None:
                self.mutator = mutator
                self.call_count = 0

            def __call__(self, request: dict[str, Any]) -> dict[str, Any]:
                self.call_count += 1
                integrity = integrity_results[PREVIEW_ATTESTED]
                document = {
                    "schema_version": 3,
                    "verification_level": PREVIEW_ATTESTED,
                    "provider_verified": False,
                    "source_identity": dict(integrity.source_identity),
                    "integrity_result": _integrity_result_contract(integrity),
                    "live_verifier": {
                        "adapter_id": self.adapter_id,
                        "live_requery_performed": True,
                        "requery_source": "github_api",
                        "independent": True,
                        "verifier_workflow_run_id": 7003,
                        "verified_at": "2026-07-13T00:03:00Z",
                    },
                    "gate_eligibility": {
                        "eligible": True,
                        "level": PREVIEW_ATTESTED,
                        "determined_by": "registered_live_verifier",
                        "provider_adapter_id": None,
                        "provider_authenticated": False,
                    },
                }
                if callable(self.mutator):
                    self.mutator(document)
                return document

        preview_integrity = integrity_results[PREVIEW_ATTESTED]
        live_request = {
            "receipt_id": valid["receipt_id"],
            "evidence_id": preview_integrity.evidence_id,
            "adapter_id": PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
            "expected_verification_level": PREVIEW_ATTESTED,
            "expected_source_identity": dict(preview_integrity.source_identity),
        }
        live_verifier = SyntheticRuntimeLiveVerifier()
        external_attestation = issue_external_runtime_attestation(
            preview_integrity,
            receipt_id=valid["receipt_id"],
            live_verifier=live_verifier,
            live_verifier_request=live_request,
            expected_adapter_id=PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
        )
        require(
            live_verifier.call_count == 1
            and external_attestation.counts_as_runtime_evidence is True,
            "runtime_external_attestation_factory_not_exercised",
            valid["receipt_id"],
        )
        externally_accounted = validate_runtime_receipt(
            valid,
            registry=registry,
            schema=schema,
            expected_source_commit=fake_commit,
            root=root,
            evidence_result=external_attestation,
        )
        require(
            externally_accounted["verification_level"] == PREVIEW_ATTESTED
            and externally_accounted["evidence_accounting_status"]
            == "externally_attested_runtime_evidence",
            "runtime_external_attestation_accounting_mapping",
            valid["receipt_id"],
        )
        try:
            pickle.dumps(external_attestation)
        except TypeError:
            results.append(
                {
                    "mutation": "serialize_external_runtime_attestation_capability",
                    "status": "rejected_as_expected",
                    "error_code": (
                        "runtime_external_attestation_capability_not_serializable"
                    ),
                }
            )
        else:
            raise ModeViolation(
                "runtime_negative_accepted",
                "serialize_external_runtime_attestation_capability",
            )

        configured_collection = copy.deepcopy(collection)
        configured_collection["platform_trust"] = {
            "adapter_status": "configured",
            "adapter_id": PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
            "verification_level": PREVIEW_ATTESTED,
            "provider_authenticated": False,
            "reason": "Synthetic contract exercise of the registered Preview adapter.",
        }
        configured_collection["receipts"][0] = copy.deepcopy(valid)
        configured_results = validate_runtime_collection(
            configured_collection,
            schema=schema,
            registry=registry,
            expected_source_commit=fake_commit,
            root=root,
            validated_evidence_results={valid["receipt_id"]: external_attestation},
        )
        require(
            sum(item["status"] == "verified" for item in configured_results) == 1,
            "runtime_external_attestation_collection_unreachable",
            valid["receipt_id"],
        )

        def expect_external_factory_rejection(
            mutation: str,
            expected_code: str,
            mutator: Any,
        ) -> None:
            try:
                issue_external_runtime_attestation(
                    preview_integrity,
                    receipt_id=valid["receipt_id"],
                    live_verifier=SyntheticRuntimeLiveVerifier(mutator),
                    live_verifier_request=live_request,
                    expected_adapter_id=PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
                )
            except ModeViolation as exc:
                require(
                    exc.code == expected_code,
                    "runtime_negative_wrong_error",
                    f"{mutation}: expected {expected_code}, got {exc.code}",
                )
                results.append(
                    {
                        "mutation": mutation,
                        "status": "rejected_as_expected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise ModeViolation("runtime_negative_accepted", mutation)

        external_result_mutations = (
            (
                "external_attestation_wrong_schema",
                "runtime_external_attestation_schema_invalid",
                lambda value: value.update(schema_version=2),
            ),
            (
                "external_attestation_wrong_source_identity",
                "runtime_external_attestation_source_identity_mismatch",
                lambda value: value["source_identity"].update(source_commit="b" * 40),
            ),
            (
                "external_attestation_wrong_evidence_id",
                "runtime_external_attestation_integrity_binding_mismatch",
                lambda value: value["integrity_result"].update(evidence_id="forged"),
            ),
            (
                "external_attestation_wrong_raw_digest",
                "runtime_external_attestation_integrity_binding_mismatch",
                lambda value: value["integrity_result"].update(
                    raw_export_sha256="sha256:" + "0" * 64
                ),
            ),
            (
                "external_attestation_wrong_envelope_digest",
                "runtime_external_attestation_integrity_binding_mismatch",
                lambda value: value["integrity_result"].update(
                    envelope_sha256="sha256:" + "0" * 64
                ),
            ),
            (
                "external_attestation_wrong_verifier_report_digest",
                "runtime_external_attestation_integrity_binding_mismatch",
                lambda value: value["integrity_result"].update(
                    verifier_report_sha256="sha256:" + "0" * 64
                ),
            ),
            (
                "external_attestation_wrong_index_digest",
                "runtime_external_attestation_integrity_binding_mismatch",
                lambda value: value["integrity_result"].update(
                    release_asset_index_sha256="sha256:" + "0" * 64
                ),
            ),
            (
                "external_attestation_wrong_adapter",
                "runtime_external_attestation_live_requery_invalid",
                lambda value: value["live_verifier"].update(adapter_id="forged"),
            ),
            (
                "external_attestation_without_live_requery",
                "runtime_external_attestation_live_requery_invalid",
                lambda value: value["live_verifier"].update(
                    live_requery_performed=False
                ),
            ),
            (
                "external_attestation_gate_not_eligible",
                "runtime_external_attestation_gate_invalid",
                lambda value: value["gate_eligibility"].update(eligible=False),
            ),
            (
                "preview_attestation_claims_provider_authentication",
                "runtime_external_attestation_preview_provider_confusion",
                lambda value: value["gate_eligibility"].update(
                    provider_authenticated=True,
                    provider_adapter_id="forged-provider",
                ),
            ),
        )
        for mutation, expected_code, mutator in external_result_mutations:
            expect_external_factory_rejection(mutation, expected_code, mutator)

        mismatched_request = copy.deepcopy(live_request)
        mismatched_request["evidence_id"] = "wrong-evidence"
        try:
            issue_external_runtime_attestation(
                preview_integrity,
                receipt_id=valid["receipt_id"],
                live_verifier=SyntheticRuntimeLiveVerifier(),
                live_verifier_request=mismatched_request,
                expected_adapter_id=PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
            )
        except ModeViolation as exc:
            require(
                exc.code == "runtime_external_attestation_request_binding_mismatch",
                "runtime_negative_wrong_error",
                f"external_request_binding: {exc.code}",
            )
            results.append(
                {
                    "mutation": "external_attestation_request_evidence_id_mismatch",
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation(
                "runtime_negative_accepted",
                "external_attestation_request_evidence_id_mismatch",
            )

        try:
            issue_external_runtime_attestation(
                integrity_results[PROVIDER_VERIFIED],
                receipt_id=valid["receipt_id"],
                live_verifier=SyntheticRuntimeLiveVerifier(),
                live_verifier_request={},
                expected_adapter_id=PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
            )
        except ModeViolation as exc:
            require(
                exc.code == "runtime_external_attestation_adapter_not_allowlisted",
                "runtime_negative_wrong_error",
                f"provider_allowlist: {exc.code}",
            )
            results.append(
                {
                    "mutation": "provider_attestation_without_provider_adapter",
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation(
                "runtime_negative_accepted",
                "provider_attestation_without_provider_adapter",
            )

        def expect_evidence_type_rejection(
            evidence_value: Any, mutation: str, expected_code: str
        ) -> None:
            try:
                validate_runtime_receipt(
                    valid,
                    registry=registry,
                    schema=schema,
                    expected_source_commit=fake_commit,
                    root=root,
                    evidence_result=evidence_value,
                )
            except ModeViolation as exc:
                require(
                    exc.code == expected_code,
                    "runtime_negative_wrong_error",
                    f"{mutation}: expected {expected_code}, got {exc.code}",
                )
                results.append(
                    {
                        "mutation": mutation,
                        "status": "rejected_as_expected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise ModeViolation("runtime_negative_accepted", mutation)

        forged_attestation = ExternalRuntimeAttestation(
            integrity_result=preview_integrity,
            verification_level=PREVIEW_ATTESTED,
            provider_verified=False,
            counts_as_preview_acceptance=True,
            counts_as_runtime_evidence=True,
            adapter_id=PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
            attestation_scope="phase7_external_runtime_live_requery",
            live_result_digest="sha256:" + "0" * 64,
            verifier_workflow_run_id=1,
            verified_at="2026-07-13T00:00:00Z",
            _capability=_ExternalRuntimeAttestationCapability(),
        )
        for evidence_value, mutation in (
            (True, "bare_boolean_runtime_attestation"),
            ({"gate_eligible": True}, "serialized_runtime_attestation_object"),
            (forged_attestation, "forged_runtime_attestation_capability"),
        ):
            expect_evidence_type_rejection(
                evidence_value,
                mutation,
                "runtime_evidence_attestation_type_invalid",
            )

        expect_collection_rejection(
            configured_collection,
            "collection_accepts_bare_boolean_attestation",
            "runtime_evidence_attestation_type_invalid",
            validated_evidence_results={valid["receipt_id"]: True},
        )
        expect_collection_rejection(
            configured_collection,
            "collection_accepts_integrity_only_result",
            "runtime_evidence_authenticated_attestation_missing",
            validated_evidence_results={valid["receipt_id"]: preview_integrity},
        )

        try:
            _build_test_only_attested_evidence(
                raw_payload=raw_payload,
                registry=registry,
                source_commit=fake_commit,
                verification_level=PREVIEW_ATTESTED,
                raw_evidence_kind="screenshot",
            )
        except EvidenceValidationError as exc:
            require(
                exc.code == "non_substantive_evidence_only",
                "runtime_negative_wrong_error",
                f"screenshot_only: {exc.code}",
            )
            results.append(
                {
                    "mutation": "single_screenshot_without_raw_export",
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation(
                "runtime_negative_accepted",
                "single_screenshot_without_raw_export",
            )

        for workflow in (
            "idea",
            "proposal",
            "article",
            "perspective",
            "research_polisher",
        ):
            for field, invalid_value, expected_code in (
                (
                    "expected_final_state",
                    "human_signoff_required",
                    "runtime_expected_state_contract_mismatch",
                ),
                (
                    "input_condition",
                    "mutable_receipt_selected_input",
                    "runtime_control_input_condition_mismatch",
                ),
                (
                    "gate",
                    "mutable_receipt_selected_gate",
                    "runtime_control_gate_mismatch",
                ),
                (
                    "route",
                    "mutable_receipt_selected_route",
                    "runtime_control_route_mismatch",
                ),
            ):
                mutated_collection = copy.deepcopy(collection)
                control_receipt = next(
                    receipt
                    for receipt in mutated_collection["receipts"]
                    if receipt["workflow"] == workflow
                    and receipt["case_kind"] == "control"
                )
                if field == "expected_final_state":
                    control_receipt[field] = invalid_value
                else:
                    control_receipt["control_evidence"][field] = invalid_value
                expect_collection_rejection(
                    mutated_collection,
                    f"{workflow}_control_mutable_{field}",
                    expected_code,
                )

        label_only = copy.deepcopy(collection["receipts"][0])
        label_only["status"] = "verified"
        try:
            validate_runtime_receipt(
                label_only,
                registry=registry,
                schema=schema,
                expected_source_commit=fake_commit,
                root=REPO,
            )
        except ModeViolation as exc:
            require(exc.code == "runtime_verified_label_only", "runtime_negative_wrong_error", exc.code)
            results.append(
                {
                    "mutation": "label_only_verified_status",
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation("runtime_negative_accepted", "label_only_verified_status")

        missing_binding = copy.deepcopy(valid)
        missing_binding["binding"]["actor_manifest"]["path"] = None
        try:
            validate_runtime_receipt(
                missing_binding,
                registry=registry,
                schema=schema,
                expected_source_commit=fake_commit,
                root=root,
            )
        except ModeViolation as exc:
            require(exc.code == "runtime_binding_missing", "runtime_negative_wrong_error", exc.code)
            results.append(
                {
                    "mutation": "missing_durable_actor_manifest_binding",
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation("runtime_negative_accepted", "missing_durable_actor_manifest_binding")

        task_digest_mismatch = copy.deepcopy(valid)
        task_digest_mismatch["binding"]["task_export"]["sha256"] = "sha256:" + "0" * 64
        expect_runtime_rejection(
            task_digest_mismatch,
            "task_export_digest_mismatch",
            "runtime_bound_file_digest_mismatch",
        )

        entry_mode_binding_mismatch = copy.deepcopy(valid)
        entry_mode_binding_mismatch["binding"]["task_export"]["entry_mode"] = (
            "resume_candidates"
        )
        expect_runtime_rejection(
            entry_mode_binding_mismatch,
            "receipt_and_task_slot_entry_mode_mismatch",
            "runtime_entry_mode_binding_mismatch",
        )

        task_content_mismatch = copy.deepcopy(valid)
        task_path = root / task_content_mismatch["binding"]["task_export"]["path"]
        task_document = load_structured_file(task_path)
        task_document["plugin_version"] = "0.0.0-invalid"
        write_json_file(task_path, task_document)
        task_content_mismatch["binding"]["task_export"]["sha256"] = sha256_file(task_path)
        expect_runtime_rejection(
            task_content_mismatch,
            "task_export_content_identity_mismatch",
            "runtime_task_export_identity_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        supporting_finding_omitted = copy.deepcopy(valid)
        supporting_finding_omitted["review_state"]["dissent_ids"] = ["dissent-001"]
        supporting_finding_omitted["review_state"]["preserved_dissent_ids"] = [
            "dissent-001"
        ]
        expect_runtime_rejection(
            supporting_finding_omitted,
            "supporting_reviewer_finding_omitted_from_review_state",
            "runtime_review_state_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        dissent_hidden = copy.deepcopy(valid)
        dissent_hidden["review_state"]["dissent_ids"] = []
        dissent_hidden["review_state"]["preserved_dissent_ids"] = []
        expect_runtime_rejection(
            dissent_hidden,
            "review_artifact_dissent_hidden",
            "runtime_review_state_mismatch",
        )

        fatal_hidden = copy.deepcopy(valid)
        panel_path = root / "evidence" / "panel-report.json"
        panel_document = load_structured_file(panel_path)
        panel_document["findings"].append(
            {
                "id": "fatal-001",
                "severity": "fatal",
                "blocking": True,
                "resolved": False,
                "dissent": False,
            }
        )
        panel_document["unresolved_issues"] = ["fatal-001"]
        panel_document["fatal_finding_ids"] = ["fatal-001"]
        panel_document["unresolved_fatal_finding_ids"] = ["fatal-001"]
        write_json_file(panel_path, panel_document)
        for entry in fatal_hidden["file_access"]["reads"]:
            if entry["path"] == "evidence/panel-report.json":
                entry["sha256"] = sha256_file(panel_path)
                entry["sha256_before"] = sha256_file(panel_path)
                entry["sha256_after"] = sha256_file(panel_path)
        for entry in fatal_hidden["file_access"]["writes"]:
            if entry["path"] == "evidence/panel-report.json":
                entry["sha256"] = sha256_file(panel_path)
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        for artifact in artifact_document["artifacts"]:
            if artifact["path"] == "evidence/panel-report.json":
                artifact["sha256"] = sha256_file(panel_path)
        write_json_file(artifact_path, artifact_document)
        fatal_hidden["binding"]["artifact_index"]["sha256"] = sha256_file(artifact_path)
        task_path = root / "evidence" / "task-export.json"
        task_document = load_structured_file(task_path)
        task_document["artifact_index"] = fatal_hidden["binding"]["artifact_index"]
        write_json_file(task_path, task_document)
        fatal_hidden["binding"]["task_export"]["sha256"] = sha256_file(task_path)
        refresh_linked_bindings(fatal_hidden)
        expect_runtime_rejection(
            fatal_hidden,
            "review_artifact_fatal_hidden_false_ready",
            "runtime_ready_review_decision_not_pass",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        supporting_report_missing_isolation = copy.deepcopy(valid)
        supporting_report_path = root / "evidence" / "supporting-preflight-report.json"
        supporting_report_document = load_structured_file(supporting_report_path)
        supporting_report_document.pop("isolation_mode")
        write_json_file(supporting_report_path, supporting_report_document)
        refresh_indexed_artifact_binding(
            supporting_report_missing_isolation,
            "evidence/supporting-preflight-report.json",
        )
        expect_runtime_rejection(
            supporting_report_missing_isolation,
            "supporting_reviewer_report_missing_fresh_isolation",
            "runtime_reviewer_report_isolation_mismatch",
        )

        for actor_id, mutation in (
            ("evaluator-001", "evaluator_actor_not_fresh_subagent"),
            ("panel-001", "panel_actor_not_fresh_subagent"),
        ):
            valid = build_runtime_validator_fixture(root, registry, fake_commit)
            mutated = copy.deepcopy(valid)
            actor_path = root / "evidence" / "actor-manifest.json"
            actor_document = load_structured_file(actor_path)
            next(
                actor
                for actor in actor_document["actors"]
                if actor["instance_id"] == actor_id
            )["isolation_mode"] = "inline"
            write_json_file(actor_path, actor_document)
            refresh_linked_bindings(mutated)
            expect_runtime_rejection(
                mutated,
                mutation,
                "runtime_reviewer_isolation_mismatch",
            )

        for report_path_value, mutation in (
            ("evidence/evaluator-v2.json", "evaluator_report_missing_fresh_isolation"),
            ("evidence/panel-report.json", "panel_report_not_fresh_subagent"),
        ):
            valid = build_runtime_validator_fixture(root, registry, fake_commit)
            mutated = copy.deepcopy(valid)
            report_path = root / Path(*PurePosixPath(report_path_value).parts)
            report_document = load_structured_file(report_path)
            if "evaluator" in mutation:
                report_document.pop("isolation_mode")
            else:
                report_document["isolation_mode"] = "inline"
            write_json_file(report_path, report_document)
            refresh_indexed_artifact_binding(mutated, report_path_value)
            expect_runtime_rejection(
                mutated,
                mutation,
                "runtime_reviewer_report_isolation_mismatch",
            )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        current_evaluator_rejects = copy.deepcopy(valid)
        evaluator_path = root / "evidence" / "evaluator-v2.json"
        evaluator_document = load_structured_file(evaluator_path)
        evaluator_document["decision"] = "reject"
        write_json_file(evaluator_path, evaluator_document)
        refresh_indexed_artifact_binding(
            current_evaluator_rejects, "evidence/evaluator-v2.json"
        )
        expect_runtime_rejection(
            current_evaluator_rejects,
            "ready_state_with_reject_decision_and_empty_fatal_ids",
            "runtime_ready_review_decision_not_pass",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        unknown_decision = copy.deepcopy(valid)
        evaluator_path = root / "evidence" / "evaluator-v2.json"
        evaluator_document = load_structured_file(evaluator_path)
        evaluator_document["decision"] = "fabricated_acceptance"
        write_json_file(evaluator_path, evaluator_document)
        refresh_indexed_artifact_binding(
            unknown_decision, "evidence/evaluator-v2.json"
        )
        expect_runtime_rejection(
            unknown_decision,
            "reviewer_uses_unknown_decision_value",
            "runtime_review_decision_unknown",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        fatal_finding_id_omitted = copy.deepcopy(valid)
        evaluator_path = root / "evidence" / "evaluator-v2.json"
        evaluator_document = load_structured_file(evaluator_path)
        evaluator_document["findings"] = [
            {
                "id": "fatal-omitted-001",
                "severity": "fatal",
                "blocking": True,
                "resolved": False,
                "dissent": False,
            }
        ]
        evaluator_document["unresolved_issues"] = ["fatal-omitted-001"]
        write_json_file(evaluator_path, evaluator_document)
        refresh_indexed_artifact_binding(
            fatal_finding_id_omitted, "evidence/evaluator-v2.json"
        )
        expect_runtime_rejection(
            fatal_finding_id_omitted,
            "fatal_finding_object_omitted_from_id_arrays",
            "runtime_review_finding_derivation_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        dissent_finding_id_omitted = copy.deepcopy(valid)
        panel_path = root / "evidence" / "panel-report.json"
        panel_document = load_structured_file(panel_path)
        panel_document["dissent_ids"] = []
        write_json_file(panel_path, panel_document)
        refresh_indexed_artifact_binding(
            dissent_finding_id_omitted, "evidence/panel-report.json"
        )
        expect_runtime_rejection(
            dissent_finding_id_omitted,
            "dissent_finding_object_omitted_from_id_arrays",
            "runtime_review_finding_derivation_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        supporting_reviewer_source_write = copy.deepcopy(valid)
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        next(
            artifact
            for artifact in artifact_document["artifacts"]
            if artifact["created_by_instance_id"] == "supporting-reviewer-001"
        ).update(artifact_role="idea_dossier", change_type="revise")
        write_json_file(artifact_path, artifact_document)
        refresh_linked_bindings(supporting_reviewer_source_write)
        expect_runtime_rejection(
            supporting_reviewer_source_write,
            "supporting_reviewer_writes_source_artifact",
            "runtime_reviewer_wrote_source_artifact",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        reviewer_primary_write = copy.deepcopy(valid)
        panel_write = next(
            item
            for item in reviewer_primary_write["file_access"]["writes"]
            if item["actor_instance_id"] == "panel-001"
        )
        primary_path = root / "evidence" / "primary-v2.md"
        panel_write["path"] = "evidence/primary-v2.md"
        panel_write["sha256"] = sha256_file(primary_path)
        refresh_linked_bindings(reviewer_primary_write)
        expect_runtime_rejection(
            reviewer_primary_write,
            "panel_writes_primary_input",
            "runtime_write_artifact_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        invalid_actor_skill = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(
            actor
            for actor in actor_document["actors"]
            if actor["instance_id"] == "evaluator-001"
        )["skill"] = "not-a-registered-reviewer"
        write_json_file(actor_path, actor_document)
        invalid_actor_skill["binding"]["actor_manifest"]["sha256"] = sha256_file(actor_path)
        task_path = root / "evidence" / "task-export.json"
        task_document = load_structured_file(task_path)
        task_document["actor_manifest"] = invalid_actor_skill["binding"]["actor_manifest"]
        write_json_file(task_path, task_document)
        invalid_actor_skill["binding"]["task_export"]["sha256"] = sha256_file(task_path)
        expect_runtime_rejection(
            invalid_actor_skill,
            "unregistered_evaluator_actor_skill",
            "runtime_actor_skill_missing",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        unknown_actor_role = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(
            actor
            for actor in actor_document["actors"]
            if actor["instance_id"] == "context-001"
        )["role"] = "unregistered-runtime-role"
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(unknown_actor_role)
        expect_runtime_rejection(
            unknown_actor_role,
            "unknown_actor_role",
            "runtime_actor_role_unknown",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        actor_registry_role_mismatch = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(
            actor
            for actor in actor_document["actors"]
            if actor["instance_id"] == "context-001"
        )["role"] = "evaluator"
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(actor_registry_role_mismatch)
        expect_runtime_rejection(
            actor_registry_role_mismatch,
            "actor_role_disagrees_with_skill_registry_role",
            "runtime_actor_role_registry_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        supporting_reviewer_wrong_skill = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(
            actor
            for actor in actor_document["actors"]
            if actor["instance_id"] == "supporting-reviewer-001"
        )["skill"] = "proposal-readiness-triage"
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(supporting_reviewer_wrong_skill)
        expect_runtime_rejection(
            supporting_reviewer_wrong_skill,
            "supporting_reviewer_not_on_workflow_edge",
            "runtime_supporting_reviewer_edge_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        supporting_reviewer_not_fresh = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(
            actor
            for actor in actor_document["actors"]
            if actor["instance_id"] == "supporting-reviewer-001"
        )["isolation_mode"] = "inline"
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(supporting_reviewer_not_fresh)
        expect_runtime_rejection(
            supporting_reviewer_not_fresh,
            "supporting_reviewer_not_fresh_subagent",
            "runtime_reviewer_isolation_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        supporting_reviewer_missing_round = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(
            actor
            for actor in actor_document["actors"]
            if actor["instance_id"] == "supporting-reviewer-001"
        ).pop("round_id")
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(supporting_reviewer_missing_round)
        expect_runtime_rejection(
            supporting_reviewer_missing_round,
            "supporting_reviewer_missing_round_id",
            "runtime_reviewer_isolation_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        arbitrary_supporting_writer = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        actor_document["actors"].append(
            {
                "instance_id": "supporting-writer-invalid-001",
                "skill": "proposal-drafter",
                "role": "supporting_writer",
                "dispatch_source": "research-idea-orchestrator",
                "dispatch_mode": "orchestrated",
                "dispatch_trigger": "fabricated_conditional_draft",
                "allowed_read_roots": ["evidence"],
                "allowed_write_roots": ["evidence"],
            }
        )
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(arbitrary_supporting_writer)
        expect_runtime_rejection(
            arbitrary_supporting_writer,
            "supporting_writer_not_on_conditional_drafter_edge",
            "runtime_supporting_writer_edge_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        wrong_workflow_orchestrator = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(
            actor
            for actor in actor_document["actors"]
            if actor["instance_id"] == "orchestrator-001"
        )["skill"] = "proposal-orchestrator"
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(wrong_workflow_orchestrator)
        expect_runtime_rejection(
            wrong_workflow_orchestrator,
            "orchestrator_skill_from_another_workflow",
            "runtime_orchestrator_skill_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        wrong_workflow_writer = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        next(actor for actor in actor_document["actors"] if actor["role"] == "writer")[
            "skill"
        ] = "article-drafter"
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(wrong_workflow_writer)
        expect_runtime_rejection(
            wrong_workflow_writer,
            "writer_skill_from_another_workflow",
            "runtime_writer_skill_mismatch",
        )

        for actor_id, replacement_skill, mutation in (
            (
                "context-001",
                "proposal-context-brief-builder",
                "cross_workflow_builder_actor",
            ),
            (
                "evidence-001",
                "academic-deep-search",
                "cross_workflow_retrieval_actor",
            ),
        ):
            valid = build_runtime_validator_fixture(root, registry, fake_commit)
            cross_workflow_actor = copy.deepcopy(valid)
            actor_path = root / "evidence" / "actor-manifest.json"
            actor_document = load_structured_file(actor_path)
            next(
                actor
                for actor in actor_document["actors"]
                if actor["instance_id"] == actor_id
            )["skill"] = replacement_skill
            write_json_file(actor_path, actor_document)
            refresh_linked_bindings(cross_workflow_actor)
            expect_runtime_rejection(
                cross_workflow_actor,
                mutation,
                "runtime_actor_edge_provenance_mismatch",
            )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        cross_workflow_controller = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        actor_document["actors"].append(
            {
                "instance_id": "cross-workflow-controller-001",
                "skill": "article-refinement-controller",
                "role": "controller",
                "dispatch_source": "research-idea-orchestrator",
                "dispatch_mode": "orchestrated",
                "dispatch_trigger": "fabricated_revision",
                "allowed_read_roots": ["evidence"],
                "allowed_write_roots": ["evidence"],
            }
        )
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(cross_workflow_controller)
        expect_runtime_rejection(
            cross_workflow_controller,
            "cross_workflow_controller_actor",
            "runtime_actor_edge_provenance_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        unrelated_writer_output = copy.deepcopy(valid)
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        next(
            artifact
            for artifact in artifact_document["artifacts"]
            if artifact["artifact_id"] == "revision-delta"
        )["artifact_role"] = "research_context"
        write_json_file(artifact_path, artifact_document)
        refresh_linked_bindings(unrelated_writer_output)
        expect_runtime_rejection(
            unrelated_writer_output,
            "primary_writer_emits_unrelated_output_role",
            "runtime_actor_output_role_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        standard_external_primary = copy.deepcopy(valid)
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        current_primary = next(
            artifact
            for artifact in artifact_document["artifacts"]
            if ref_for(artifact) == "primary@v002"
        )
        current_primary.update(
            source_skill="external-input",
            created_by_instance_id="external-input",
            external_source_id="external:user-draft",
        )
        write_json_file(artifact_path, artifact_document)
        refresh_linked_bindings(standard_external_primary)
        expect_runtime_rejection(
            standard_external_primary,
            "standard_mode_current_primary_is_external",
            "runtime_external_input_impersonation",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        missing_panel_role = copy.deepcopy(valid)
        actor_path = root / "evidence" / "actor-manifest.json"
        actor_document = load_structured_file(actor_path)
        actor_document["actors"] = [
            actor
            for actor in actor_document["actors"]
            if actor.get("panel_role") != "pi-strategy"
        ]
        write_json_file(actor_path, actor_document)
        refresh_linked_bindings(missing_panel_role)
        expect_runtime_rejection(
            missing_panel_role,
            "missing_registry_panel_role",
            "runtime_panel_role_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        stale_panel_role = copy.deepcopy(valid)
        stale_panel_path = root / "evidence" / "panel-report-002.json"
        stale_panel_document = load_structured_file(stale_panel_path)
        stale_panel_document["input_artifact_refs"] = ["primary@v001"]
        write_json_file(stale_panel_path, stale_panel_document)
        primary_v1_path = root / "evidence" / "primary-v1.md"
        primary_v1_digest = sha256_file(primary_v1_path)
        stale_panel_read = next(
            entry
            for entry in stale_panel_role["file_access"]["reads"]
            if entry["actor_instance_id"] == "panel-002"
            and entry["path"] == "evidence/primary-v2.md"
        )
        stale_panel_read.update(
            path="evidence/primary-v1.md",
            sha256=primary_v1_digest,
            sha256_before=primary_v1_digest,
            sha256_after=primary_v1_digest,
        )
        refresh_indexed_artifact_binding(
            stale_panel_role,
            "evidence/panel-report-002.json",
            based_on=["primary@v001"],
        )
        expect_runtime_rejection(
            stale_panel_role,
            "one_panel_role_reviews_stale_primary_version",
            "runtime_current_version_review_missing",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        panel_reads_peer = copy.deepcopy(valid)
        peer_path = root / "evidence" / "panel-report.json"
        peer_digest = sha256_file(peer_path)
        panel_reads_peer["file_access"]["reads"].append(
            {
                "actor_instance_id": "panel-002",
                "path": "evidence/panel-report.json",
                "sha256": peer_digest,
                "sha256_before": peer_digest,
                "sha256_after": peer_digest,
            }
        )
        refresh_linked_bindings(panel_reads_peer)
        expect_runtime_rejection(
            panel_reads_peer,
            "panel_role_reads_peer_output",
            "runtime_panel_peer_output_visible",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        supporting_reviewer_reads_review = copy.deepcopy(valid)
        prior_review_path = root / "evidence" / "evaluator-v1.json"
        prior_review_digest = sha256_file(prior_review_path)
        supporting_reviewer_reads_review["file_access"]["reads"].append(
            {
                "actor_instance_id": "supporting-reviewer-001",
                "path": "evidence/evaluator-v1.json",
                "sha256": prior_review_digest,
                "sha256_before": prior_review_digest,
                "sha256_after": prior_review_digest,
            }
        )
        refresh_linked_bindings(supporting_reviewer_reads_review)
        expect_runtime_rejection(
            supporting_reviewer_reads_review,
            "supporting_reviewer_reads_prior_review_output",
            "runtime_supporting_reviewer_prior_review_visible",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        evaluator_reads_supporting_review = copy.deepcopy(valid)
        supporting_report_path = root / "evidence" / "supporting-preflight-report.json"
        supporting_report_digest = sha256_file(supporting_report_path)
        evaluator_reads_supporting_review["file_access"]["reads"].append(
            {
                "actor_instance_id": "evaluator-002",
                "path": "evidence/supporting-preflight-report.json",
                "sha256": supporting_report_digest,
                "sha256_before": supporting_report_digest,
                "sha256_after": supporting_report_digest,
            }
        )
        refresh_linked_bindings(evaluator_reads_supporting_review)
        expect_runtime_rejection(
            evaluator_reads_supporting_review,
            "fresh_evaluator_reads_supporting_reviewer_output",
            "runtime_evaluator_prior_review_visible",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        evaluator_reads_prior_review = copy.deepcopy(valid)
        prior_review_path = root / "evidence" / "evaluator-v1.json"
        prior_review_digest = sha256_file(prior_review_path)
        evaluator_reads_prior_review["file_access"]["reads"].append(
            {
                "actor_instance_id": "evaluator-002",
                "path": "evidence/evaluator-v1.json",
                "sha256": prior_review_digest,
                "sha256_before": prior_review_digest,
                "sha256_after": prior_review_digest,
            }
        )
        refresh_linked_bindings(evaluator_reads_prior_review)
        expect_runtime_rejection(
            evaluator_reads_prior_review,
            "fresh_evaluator_reads_prior_evaluator_output",
            "runtime_evaluator_prior_review_visible",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        evaluator_prior_scores_visible = copy.deepcopy(valid)
        evaluator_v2_path = root / "evidence" / "evaluator-v2.json"
        evaluator_v2_document = load_structured_file(evaluator_v2_path)
        evaluator_v2_document["prior_scores_visible"] = True
        write_json_file(evaluator_v2_path, evaluator_v2_document)
        refresh_indexed_artifact_binding(
            evaluator_prior_scores_visible,
            "evidence/evaluator-v2.json",
        )
        expect_runtime_rejection(
            evaluator_prior_scores_visible,
            "fresh_evaluator_prior_scores_visible",
            "runtime_prior_scores_visible",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        evaluator_digest_missing = copy.deepcopy(valid)
        evaluator_v2_path = root / "evidence" / "evaluator-v2.json"
        evaluator_v2_document = load_structured_file(evaluator_v2_path)
        evaluator_v2_document.pop("reviewed_dossier_digest")
        write_json_file(evaluator_v2_path, evaluator_v2_document)
        refresh_indexed_artifact_binding(
            evaluator_digest_missing,
            "evidence/evaluator-v2.json",
        )
        expect_runtime_rejection(
            evaluator_digest_missing,
            "focused_evaluator_reviewed_dossier_digest_missing",
            "runtime_review_extension_invalid",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        stale_fresh_evaluator = copy.deepcopy(valid)
        evaluator_v2_path = root / "evidence" / "evaluator-v2.json"
        evaluator_v2_document = load_structured_file(evaluator_v2_path)
        evaluator_v2_document["input_artifact_refs"] = ["primary@v001"]
        write_json_file(evaluator_v2_path, evaluator_v2_document)
        refresh_indexed_artifact_binding(
            stale_fresh_evaluator,
            "evidence/evaluator-v2.json",
            based_on=["primary@v001"],
        )
        expect_runtime_rejection(
            stale_fresh_evaluator,
            "fresh_evaluator_reviews_stale_artifact_version",
            "runtime_review_input_read_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        noncanonical_path = copy.deepcopy(valid)
        noncanonical_path["binding"]["task_export"]["path"] = "evidence\\task-export.json"
        expect_runtime_rejection(
            noncanonical_path,
            "windows_backslash_runtime_path",
            "runtime_path_not_canonical_posix",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        missing_package_input = copy.deepcopy(valid)
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        final_artifact = next(
            artifact
            for artifact in artifact_document["artifacts"]
            if artifact["artifact_role"] == "final_handoff_package"
        )
        final_artifact["based_on"].remove("revision-delta@v001")
        final_path = root / Path(*PurePosixPath(final_artifact["path"]).parts)
        final_document = load_structured_file(final_path)
        final_document["input_artifact_refs"].remove("revision-delta@v001")
        write_json_file(final_path, final_document)
        final_artifact["sha256"] = sha256_file(final_path)
        for entry in missing_package_input["file_access"]["writes"]:
            if entry["path"] == final_artifact["path"]:
                entry["sha256"] = final_artifact["sha256"]
        write_json_file(artifact_path, artifact_document)
        refresh_linked_bindings(missing_package_input)
        expect_runtime_rejection(
            missing_package_input,
            "final_package_omits_created_revision_delta",
            "runtime_package_input_omitted",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        assembler_source_write = copy.deepcopy(valid)
        extra_path = root / "evidence" / "assembler-primary-v3.md"
        extra_path.write_text("invalid assembler source edit\n", encoding="utf-8", newline="\n")
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        artifact_document["artifacts"].append(
            {
                "artifact_id": "primary",
                "version_id": "v003",
                "artifact_role": "idea_dossier",
                "path": "evidence/assembler-primary-v3.md",
                "sha256": sha256_file(extra_path),
                "source_skill": "idea-portfolio-assembler",
                "created_by_instance_id": "assembler-001",
                "based_on": ["primary@v002"],
                "change_type": "revise",
                "status": "frozen",
            }
        )
        write_json_file(artifact_path, artifact_document)
        assembler_source_write["file_access"]["writes"].append(
            {
                "actor_instance_id": "assembler-001",
                "path": "evidence/assembler-primary-v3.md",
                "sha256": sha256_file(extra_path),
                "allowed_write_root": "evidence",
            }
        )
        refresh_linked_bindings(assembler_source_write)
        expect_runtime_rejection(
            assembler_source_write,
            "assembler_writes_new_primary",
            "runtime_assembler_wrote_source_artifact",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        wrong_package_creator = copy.deepcopy(valid)
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        final_artifact = next(
            artifact
            for artifact in artifact_document["artifacts"]
            if artifact["artifact_role"] == "final_handoff_package"
        )
        final_artifact["created_by_instance_id"] = "writer-001"
        final_artifact["source_skill"] = "multi-path-idea-generator"
        write_json_file(artifact_path, artifact_document)
        refresh_linked_bindings(wrong_package_creator)
        expect_runtime_rejection(
            wrong_package_creator,
            "final_package_created_by_writer",
            "runtime_final_package_creator_mismatch",
        )

        valid = build_runtime_validator_fixture(root, registry, fake_commit)
        happy_with_control = copy.deepcopy(valid)
        happy_with_control["control_evidence"]["gate"] = "fabricated_control_gate"
        expect_runtime_rejection(
            happy_with_control,
            "happy_receipt_carries_control_evidence",
            "runtime_happy_control_evidence_present",
        )

        valid_control = build_runtime_control_validator_fixture(root, registry, fake_commit)
        validate_runtime_receipt(
            valid_control,
            registry=registry,
            schema=schema,
            expected_source_commit=fake_commit,
            root=root,
        )
        control_without_route = copy.deepcopy(valid_control)
        control_without_route["control_evidence"]["route"] = None
        expect_runtime_rejection(
            control_without_route,
            "control_receipt_without_route",
            "runtime_control_route_mismatch",
        )

        valid_control = build_runtime_control_validator_fixture(
            root, registry, fake_commit
        )
        control_unknown_finding = copy.deepcopy(valid_control)
        control_unknown_finding["control_evidence"]["finding"] = (
            "fabricated-control-finding"
        )
        expect_runtime_rejection(
            control_unknown_finding,
            "control_finding_not_bound_to_required_report",
            "runtime_control_finding_provenance_mismatch",
        )

        valid_control = build_runtime_control_validator_fixture(
            root, registry, fake_commit
        )
        wrong_continuation_type = copy.deepcopy(valid_control)
        artifact_path = root / "evidence" / "artifact-index.json"
        artifact_document = load_structured_file(artifact_path)
        continuation_artifact = next(
            artifact
            for artifact in artifact_document["artifacts"]
            if artifact["artifact_id"] == "continuation-brief"
        )
        continuation_artifact["artifact_role"] = "revision_plan"
        write_json_file(artifact_path, artifact_document)
        refresh_linked_bindings(wrong_continuation_type)
        expect_runtime_rejection(
            wrong_continuation_type,
            "control_continuation_wrong_artifact_type",
            "runtime_control_continuation_type_mismatch",
        )

        untrusted_collection = copy.deepcopy(collection)
        untrusted_collection["receipts"][0] = copy.deepcopy(valid)
        try:
            validate_runtime_collection(
                untrusted_collection,
                schema=schema,
                registry=registry,
                expected_source_commit=fake_commit,
                root=root,
            )
        except ModeViolation as exc:
            require(
                exc.code == "runtime_platform_trust_unavailable",
                "runtime_negative_wrong_error",
                exc.code,
            )
            results.append(
                {
                    "mutation": "repository_authored_export_without_platform_trust_adapter",
                    "status": "rejected_as_expected",
                    "error_code": exc.code,
                }
            )
        else:
            raise ModeViolation(
                "runtime_negative_accepted",
                "repository_authored_export_without_platform_trust_adapter",
            )
    return results, positive_workflow_results


def release_gate_statuses(
    ledger: dict[str, Any],
    registry: dict[str, Any],
    *,
    test_only_reachability_capability: _SyntheticAttestationCapability | None = None,
    live_evidence_verifier: Any = None,
) -> dict[str, dict[str, str]]:
    if test_only_reachability_capability is not None:
        require(
            test_only_reachability_capability
            is _SYNTHETIC_ATTESTATION_CAPABILITY,
            "synthetic_gate_capability_invalid",
            "release-gate reachability override requires the private capability",
        )
    synthetic_gate_reachability = (
        test_only_reachability_capability is _SYNTHETIC_ATTESTATION_CAPABILITY
    )
    release = ledger.get("release", {}) if isinstance(ledger, dict) else {}
    version = registry["plugin_version"]
    source = release.get("source_commit", {})
    source_sha = source.get("sha") if isinstance(source, dict) else None
    source_tree_errors: list[str] = []
    validate_verified_source_commit_tree(release, source_tree_errors)
    source_tree_verified = synthetic_gate_reachability or not source_tree_errors
    source_verified = (
        isinstance(source, dict)
        and source.get("status") == "verified"
        and valid_commit_sha(source_sha)
        and source_tree_verified
        and release.get("version") == version
        and release.get("installable_contracts", {}).get("registry_sha256")
        == sha256_repository_file(REGISTRY_PATH).removeprefix("sha256:")
    )

    def gate(verified: bool, reason: str) -> dict[str, str]:
        return {"status": "verified" if verified else "pending", "reason": reason}

    ci = release.get("ci", {})
    repository_ci = ci.get("repository_preview", {}) if isinstance(ci, dict) else {}
    canonical_ci = (
        ci.get("canonical_plugin_validator", {}).get("ci", {})
        if isinstance(ci, dict)
        else {}
    )
    marketplace = release.get("marketplace_source", {})
    resolved = marketplace.get("resolved_commit", {}) if isinstance(marketplace, dict) else {}
    receipts = release.get("receipts", {})
    governance = release.get("governance", {})
    branch = governance.get("main_branch_protection", {}) if isinstance(governance, dict) else {}
    configured_external_level = configured_external_evidence_level(release)
    # A status in the source-controlled ledger is only a claim.  Outside the
    # private reachability self-test, no external gate may advance unless the
    # caller supplies the one-use live callback that re-queries every locator.
    external_adapter_available = synthetic_gate_reachability or (
        configured_external_level is not None
        and not isinstance(live_evidence_verifier, bool)
        and callable(live_evidence_verifier)
    )
    external_adapter_id = release.get("external_evidence_trust", {}).get(
        "adapter_id"
    )
    expected_external_identity = release_source_identity(release)

    def external_status_accepted(record: Any) -> bool:
        if not isinstance(record, dict):
            return False
        if synthetic_gate_reachability:
            return record.get("status") == "verified"
        return (
            external_adapter_available
            and configured_external_level in ACCEPTANCE_LEVELS
            and record.get("status") == configured_external_level
        )

    # Several higher-level gates depend on the same install receipt (for
    # example, discovery and rollback both depend on the selected install).
    # The production Release callback is intentionally one-use per immutable
    # locator, so cache the result of that one live re-query instead of
    # invoking the callback again while deriving dependent gates.
    evidence_verification_cache: dict[str, bool] = {}

    def evidence_verified(record: Any, evidence_type: str) -> bool:
        if synthetic_gate_reachability:
            return True
        cached = evidence_verification_cache.get(evidence_type)
        if cached is not None:
            return cached
        evidence_errors: list[str] = []
        validate_bound_external_evidence(
            record,
            evidence_type,
            f"phase7.{evidence_type}",
            evidence_errors,
            authenticated_external_adapter=external_adapter_available,
            synthetic_external_trust_override=(
                synthetic_gate_reachability
            ),
            expected_source_identity=expected_external_identity,
            expected_adapter_id=external_adapter_id,
            live_evidence_verifier=live_evidence_verifier,
        )
        verified = not evidence_errors
        evidence_verification_cache[evidence_type] = verified
        return verified

    def cache_artifact_verified(
        artifact: Any, expected_release: dict[str, Any]
    ) -> bool:
        cache_errors: list[str] = []
        validate_cache_artifact(
            artifact,
            expected_release,
            "phase7 cache artifact",
            cache_errors,
        )
        return not cache_errors

    repository_ci_verified = (
        source_verified
        and external_status_accepted(repository_ci)
        and repository_ci.get("run_id") is not None
        and isinstance(repository_ci.get("run_url"), str)
        and bool(repository_ci["run_url"])
        and repository_ci.get("commit_sha") == source_sha
        and repository_ci.get("conclusion") == "success"
        and evidence_verified(repository_ci, "repository_preview_ci")
    )
    canonical_ci_verified = (
        source_verified
        and external_status_accepted(canonical_ci)
        and canonical_ci.get("run_id") is not None
        and canonical_ci.get("commit_sha") == source_sha
        and canonical_ci.get("conclusion") == "success"
        and evidence_verified(canonical_ci, "canonical_plugin_validator_ci")
    )
    marketplace_verified = (
        source_verified
        and external_status_accepted(resolved)
        and resolved.get("sha") == source_sha
        and evidence_verified(resolved, "marketplace_resolved_commit")
    )

    def install_receipt_verified(name: str) -> bool:
        record = receipts.get(name, {}) if isinstance(receipts, dict) else {}
        cache_artifact = record.get("cache_artifact", {})
        return (
            source_verified
            and external_status_accepted(record)
            and record.get("installed_version") == version
            and record.get("source_commit") == source_sha
            and isinstance(record.get("cache_path"), str)
            and bool(record["cache_path"])
            and isinstance(cache_artifact, dict)
            and cache_artifact.get("cache_path") == record.get("cache_path")
            and cache_artifact_verified(cache_artifact, release)
            and evidence_verified(record, name)
        )

    discovery = receipts.get("fresh_task_discovery", {}) if isinstance(receipts, dict) else {}
    expected_explicit_entries = set(
        registry.get("public_entry_policy", {}).get("declared_entries", [])
    )
    expected_implicit_entries = set(
        registry.get("public_entry_policy", {}).get("implicit_active_entries", [])
    )
    installed_via = discovery.get("installed_via")
    discovery_install = (
        receipts.get(installed_via, {})
        if isinstance(receipts, dict)
        and installed_via in {"marketplace_upgrade", "explicit_reinstall"}
        else {}
    )
    discovery_verified = (
        source_verified
        and external_status_accepted(discovery)
        and discovery.get("plugin_version") == version
        and discovery.get("source_commit") == source_sha
        and isinstance(discovery.get("task_id"), str)
        and bool(discovery["task_id"])
        and discovery.get("installed_skill_count") == len(registry["skills"])
        and discovery.get("explicit_callable_entries")
        == len(expected_explicit_entries)
        and discovery.get("implicit_prompt_entries")
        == len(expected_implicit_entries)
        and isinstance(discovery.get("explicit_callable_entry_skills"), list)
        and set(discovery["explicit_callable_entry_skills"])
        == expected_explicit_entries
        and isinstance(discovery.get("implicit_prompt_entry_skills"), list)
        and set(discovery["implicit_prompt_entry_skills"])
        == expected_implicit_entries
        and isinstance(discovery_install, dict)
        and install_receipt_verified(str(installed_via))
        and discovery.get("cache_artifact")
        == discovery_install.get("cache_artifact")
        and cache_artifact_verified(discovery.get("cache_artifact"), release)
        and evidence_verified(discovery, "fresh_task_discovery")
    )
    rollback = receipts.get("rollback", {}) if isinstance(receipts, dict) else {}
    previous = ledger.get("previous_releases", []) if isinstance(ledger, dict) else []
    rollback_matches = []
    for item in previous:
        previous_tree_errors: list[str] = []
        validate_verified_source_commit_tree(item, previous_tree_errors, "previous release")
        previous_tree_verified = (
            synthetic_gate_reachability or not previous_tree_errors
        )
        if (
            item.get("version") == rollback.get("to_version")
            and item.get("source_commit", {}).get("status") == "verified"
            and item.get("source_commit", {}).get("sha") == rollback.get("target_commit")
            and previous_tree_verified
        ):
            rollback_matches.append(item)
    rollback_previous = rollback_matches[0] if len(rollback_matches) == 1 else {}
    candidate_from = rollback.get("candidate_from_receipt")
    candidate_install = (
        receipts.get(candidate_from, {})
        if isinstance(receipts, dict)
        and candidate_from in {"marketplace_upgrade", "explicit_reinstall"}
        else {}
    )
    candidate_cache = rollback.get("candidate_cache_artifact", {})
    restored_cache = rollback.get("restored_cache_artifact", {})
    rollback_verified = (
        external_status_accepted(rollback)
        and rollback.get("from_version") == version
        and len(rollback_matches) == 1
        and isinstance(rollback.get("restored_cache_path"), str)
        and bool(rollback["restored_cache_path"])
        and isinstance(rollback.get("candidate_cache_path"), str)
        and bool(rollback["candidate_cache_path"])
        and isinstance(candidate_install, dict)
        and install_receipt_verified(str(candidate_from))
        and candidate_cache == candidate_install.get("cache_artifact")
        and cache_artifact_verified(candidate_cache, release)
        and cache_artifact_verified(restored_cache, rollback_previous)
        and candidate_cache.get("cache_path") == rollback.get("candidate_cache_path")
        and restored_cache.get("cache_path") == rollback.get("restored_cache_path")
        and candidate_cache.get("cache_instance_id")
        != restored_cache.get("cache_instance_id")
        and candidate_cache.get("cache_identity_sha256")
        != restored_cache.get("cache_identity_sha256")
        and rollback.get("cache_mixing_absent") is True
        and evidence_verified(rollback, "rollback")
    )
    branch_verified = (
        external_status_accepted(branch)
        and branch.get("branch") == "main"
        and branch.get("required_check") == "OpenAI Plugin Preview / validate"
        and branch.get("verified_at") is not None
        and evidence_verified(branch, "main_branch_protection")
    )
    return {
        "accepted_external_evidence_adapter": gate(
            external_adapter_available,
            "No accepted live-requery Preview or authenticated provider adapter is configured.",
        ),
        "release_source_commit": gate(source_verified, "Immutable current-version source commit is not verified."),
        "repository_preview_ci": gate(repository_ci_verified, "Successful repository Preview CI is not bound to the release commit."),
        "canonical_plugin_validator_ci": gate(canonical_ci_verified, "Canonical plugin validator CI is not verified on the release commit."),
        "marketplace_resolved_commit": gate(marketplace_verified, "Marketplace source revision is not bound to the release commit."),
        "marketplace_upgrade": gate(install_receipt_verified("marketplace_upgrade"), "Marketplace upgrade receipt is not verified for the release identity."),
        "explicit_reinstall": gate(install_receipt_verified("explicit_reinstall"), "Explicit reinstall receipt is not verified for the release identity."),
        "fresh_task_discovery": gate(discovery_verified, "Fresh-task discovery is not verified for the installed release."),
        "immutable_previous_artifact_rollback": gate(rollback_verified, "Rollback is not verified against one immutable previous release."),
        "main_branch_required_check_protection": gate(branch_verified, "Main branch protection with the required Preview check is not verified."),
    }


def completion_gate_statuses(
    runtime_results: list[dict[str, Any]],
    release_gates: dict[str, dict[str, str]],
    *,
    accepted_verification_level: str | None,
    accepted_platform_adapter: bool,
) -> dict[str, dict[str, str]]:
    verified_happy = sum(
        item["status"] == "verified"
        and item.get("verification_level") == accepted_verification_level
        and item["case_kind"] == "happy"
        for item in runtime_results
    )
    verified_control = sum(
        item["status"] == "verified"
        and item.get("verification_level") == accepted_verification_level
        and item["case_kind"] == "control"
        for item in runtime_results
    )
    level_label = accepted_verification_level or "unconfigured"
    runtime_gates = {
        "accepted_platform_capture_adapter": {
            "status": "verified" if accepted_platform_adapter else "pending",
            "reason": (
                f"A {level_label} Codex/ChatGPT evidence adapter is configured."
                if accepted_platform_adapter
                else "No accepted Preview or provider-verified evidence adapter is configured."
            ),
            "verification_level": accepted_verification_level,
        },
        "five_current_version_live_happy_paths": {
            "status": "verified" if verified_happy == 5 else "pending",
            "reason": f"{verified_happy}/5 durable {level_label} happy receipts verified.",
            "verification_level": accepted_verification_level,
        },
        "five_current_version_valid_control_paths": {
            "status": "verified" if verified_control == 5 else "pending",
            "reason": f"{verified_control}/5 durable {level_label} control receipts verified.",
            "verification_level": accepted_verification_level,
        },
    }
    return {**runtime_gates, **release_gates}


def run_completion_reachability_self_test(
    registry: dict[str, Any], schema: dict[str, Any]
) -> dict[str, Any]:
    current_commit = "a" * 40
    previous_commit = "b" * 40
    previous_version = "0.5.0-preview.2"
    explicit_entries = list(
        registry.get("public_entry_policy", {}).get("declared_entries", [])
    )
    implicit_entries = list(
        registry.get("public_entry_policy", {}).get("implicit_active_entries", [])
    )
    ledger = {
        "release": {
            "version": registry["plugin_version"],
            "source_commit": {"status": "verified", "sha": current_commit},
            "installable_skill_tree": {
                "root": "skills/",
                "algorithm": "sha256_sorted_posix_relative_path_nul_crlf_normalized_bytes_nul",
                "file_count": 330,
                "sha256": "4" * 64,
            },
            "installable_contracts": {
                "manifest_sha256": "1" * 64,
                "registry_sha256": sha256_repository_file(REGISTRY_PATH).removeprefix("sha256:"),
                "license_sha256": "3" * 64,
            },
            "ci": {
                "repository_preview": {
                    "status": "verified",
                    "run_id": "1",
                    "run_url": "https://example.invalid/actions/runs/1",
                    "commit_sha": current_commit,
                    "conclusion": "success",
                },
                "canonical_plugin_validator": {
                    "ci": {
                        "status": "verified",
                        "run_id": "2",
                        "commit_sha": current_commit,
                        "conclusion": "success",
                    }
                },
            },
            "governance": {
                "main_branch_protection": {
                    "status": "verified",
                    "branch": "main",
                    "required_check": "OpenAI Plugin Preview / validate",
                    "verified_at": "2026-07-12T00:00:00Z",
                }
            },
            "marketplace_source": {
                "resolved_commit": {"status": "verified", "sha": current_commit}
            },
            "receipts": {
                "marketplace_upgrade": {
                    "status": "verified",
                    "installed_version": registry["plugin_version"],
                    "source_commit": current_commit,
                    "cache_path": "cache/upgrade",
                    "cache_artifact": None,
                },
                "explicit_reinstall": {
                    "status": "verified",
                    "installed_version": registry["plugin_version"],
                    "source_commit": current_commit,
                    "cache_path": "cache/reinstall",
                    "cache_artifact": None,
                },
                "fresh_task_discovery": {
                    "status": "verified",
                    "plugin_version": registry["plugin_version"],
                    "source_commit": current_commit,
                    "task_id": "reachability-self-test",
                    "installed_skill_count": len(registry["skills"]),
                    "explicit_callable_entries": len(explicit_entries),
                    "implicit_prompt_entries": len(implicit_entries),
                    "explicit_callable_entry_skills": explicit_entries,
                    "implicit_prompt_entry_skills": implicit_entries,
                    "installed_via": "explicit_reinstall",
                    "cache_artifact": None,
                },
                "rollback": {
                    "status": "verified",
                    "from_version": registry["plugin_version"],
                    "to_version": previous_version,
                    "target_commit": previous_commit,
                    "restored_cache_path": "cache/previous",
                    "candidate_cache_path": "cache/reinstall",
                    "candidate_from_receipt": "explicit_reinstall",
                    "candidate_cache_artifact": None,
                    "restored_cache_artifact": None,
                    "cache_mixing_absent": True,
                },
            },
        },
        "previous_releases": [
            {
                "version": previous_version,
                "source_commit": {"status": "verified", "sha": previous_commit},
                "installable_skill_tree": {
                    "root": "skills/",
                    "algorithm": "sha256_sorted_posix_relative_path_nul_crlf_normalized_bytes_nul",
                    "file_count": 329,
                    "sha256": "8" * 64,
                },
                "installable_contracts": {
                    "manifest_sha256": "5" * 64,
                    "registry_sha256": "6" * 64,
                    "license_sha256": "7" * 64,
                },
            }
        ],
    }
    current_release = ledger["release"]
    current_receipts = current_release["receipts"]
    upgrade_cache = build_cache_artifact(
        current_release,
        cache_path="cache/upgrade",
        cache_instance_id="reachability-upgrade-cache",
    )
    reinstall_cache = build_cache_artifact(
        current_release,
        cache_path="cache/reinstall",
        cache_instance_id="reachability-reinstall-cache",
    )
    restored_cache = build_cache_artifact(
        ledger["previous_releases"][0],
        cache_path="cache/previous",
        cache_instance_id="reachability-previous-cache",
    )
    current_receipts["marketplace_upgrade"]["cache_artifact"] = upgrade_cache
    current_receipts["explicit_reinstall"]["cache_artifact"] = reinstall_cache
    current_receipts["fresh_task_discovery"]["cache_artifact"] = copy.deepcopy(
        reinstall_cache
    )
    current_receipts["rollback"]["candidate_cache_artifact"] = copy.deepcopy(
        reinstall_cache
    )
    current_receipts["rollback"]["restored_cache_artifact"] = restored_cache
    capability_negative_guards: list[dict[str, str]] = []
    try:
        release_gate_statuses(
            ledger,
            registry,
            test_only_reachability_capability=True,  # type: ignore[arg-type]
        )
    except ModeViolation as exc:
        require(
            exc.code == "synthetic_gate_capability_invalid",
            "phase7_reachability_capability_wrong_error",
            exc.code,
        )
        capability_negative_guards.append(
            {
                "mutation": "bare_boolean_gate_override",
                "status": "rejected_as_expected",
                "error_code": exc.code,
            }
        )
    else:
        raise ModeViolation(
            "phase7_reachability_capability_bypassed",
            "bare Boolean reached synthetic release gates",
        )
    claimed_adapter_ledger = {
        "release": {
            "version": registry["plugin_version"],
            "external_evidence_trust": {
                "adapter_status": "configured",
                "adapter_id": PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
                "verification_level": PREVIEW_ATTESTED,
                "provider_authenticated": False,
            },
        }
    }
    claimed_adapter_gates = release_gate_statuses(
        claimed_adapter_ledger, registry
    )
    require(
        all(item["status"] == "pending" for item in claimed_adapter_gates.values()),
        "phase7_source_claim_advanced_release_gate",
        str(claimed_adapter_gates),
    )
    capability_negative_guards.append(
        {
            "mutation": "source_controlled_adapter_claim_without_live_callback",
            "status": "rejected_as_expected",
            "error_code": "live_release_callback_missing",
        }
    )
    claimed_runtime_collection = {
        "platform_trust": {
            "adapter_status": "configured",
            "adapter_id": PREVIEW_RUNTIME_ATTESTATION_ADAPTER_ID,
            "verification_level": PREVIEW_ATTESTED,
            "provider_authenticated": False,
        }
    }
    claimed_runtime_level = accepted_runtime_verification_level(
        claimed_runtime_collection, None
    )
    claimed_runtime_gates = completion_gate_statuses(
        [],
        {},
        accepted_verification_level=claimed_runtime_level,
        accepted_platform_adapter=claimed_runtime_level is not None,
    )
    require(
        claimed_runtime_level is None
        and claimed_runtime_gates["accepted_platform_capture_adapter"]["status"]
        == "pending",
        "phase7_source_claim_advanced_runtime_gate",
        str(claimed_runtime_gates),
    )
    capability_negative_guards.append(
        {
            "mutation": "source_controlled_runtime_adapter_without_live_session",
            "status": "rejected_as_expected",
            "error_code": "live_runtime_session_missing",
        }
    )
    release_gates = release_gate_statuses(
        ledger,
        registry,
        test_only_reachability_capability=_SYNTHETIC_ATTESTATION_CAPABILITY,
    )
    level_results: dict[str, Any] = {}
    for verification_level in (PREVIEW_ATTESTED, PROVIDER_VERIFIED):
        validated_evidence = _build_test_only_attested_evidence(
            raw_payload=(
                f'{{"verification_level":"{verification_level}"}}\n'.encode(
                    "utf-8"
                )
            ),
            registry=registry,
            source_commit=current_commit,
            verification_level=verification_level,
        )
        if verification_level == PREVIEW_ATTESTED:
            try:
                _issue_test_only_authenticated_attestation(
                    validated_evidence.integrity_result,
                    verification_level=verification_level,
                    capability=_SyntheticAttestationCapability(),
                )
            except ModeViolation as exc:
                require(
                    exc.code == "synthetic_attestation_capability_invalid",
                    "phase7_reachability_capability_wrong_error",
                    exc.code,
                )
                capability_negative_guards.append(
                    {
                        "mutation": "forged_attestation_capability",
                        "status": "rejected_as_expected",
                        "error_code": exc.code,
                    }
                )
            else:
                raise ModeViolation(
                    "phase7_reachability_capability_bypassed",
                    "forged capability issued an attestation",
                )
        runtime_results = [
            {
                "receipt_id": f"reachability-{workflow}-{case_kind}",
                "workflow": workflow,
                "case_kind": case_kind,
                "status": "verified",
                "verification_level": validated_evidence.verification_level,
            }
            for workflow, case_kind in schema["x-phase7-contract"][
                "required_workflow_case_pairs"
            ]
        ]
        gates = completion_gate_statuses(
            runtime_results,
            release_gates,
            accepted_verification_level=verification_level,
            accepted_platform_adapter=True,
        )
        pending = [
            name for name, value in gates.items() if value["status"] != "verified"
        ]
        require(
            not pending,
            "phase7_completion_unreachable",
            f"{verification_level}: {pending}",
        )
        level_results[verification_level] = {
            "verified_gate_count": len(gates),
            "validated_evidence_id": validated_evidence.evidence_id,
            "provider_verified": validated_evidence.provider_verified,
            "attestation_scope": validated_evidence.attestation_scope,
            "counts_as_runtime_evidence": (
                validated_evidence.counts_as_runtime_evidence
            ),
            "derived_phase_status": (
                "complete_preview_attested"
                if verification_level == PREVIEW_ATTESTED
                else "complete_provider_verified"
            ),
        }

    discovery_count_mutations: list[dict[str, Any]] = []
    for field in (
        "installed_skill_count",
        "explicit_callable_entries",
        "implicit_prompt_entries",
    ):
        mutated = copy.deepcopy(ledger)
        mutated_discovery = mutated["release"]["receipts"]["fresh_task_discovery"]
        mutated_discovery[field] += 1
        mutated_gates = release_gate_statuses(
            mutated,
            registry,
            test_only_reachability_capability=_SYNTHETIC_ATTESTATION_CAPABILITY,
        )
        require(
            mutated_gates["fresh_task_discovery"]["status"] == "pending",
            "phase7_discovery_wrong_count_accepted",
            field,
        )
        discovery_count_mutations.append(
            {
                "mutation": f"wrong_{field}",
                "status": "rejected_as_expected",
            }
        )
    return {
        "status": "passed",
        "evidence_kind": "synthetic_gate_logic_self_test_only",
        "counts_as_runtime_evidence": False,
        "capability_negative_guards": capability_negative_guards,
        "verification_levels": level_results,
        "discovery_count_mutations": discovery_count_mutations,
    }


def run_all(
    *,
    external_runtime_session: ExternalRuntimeValidationSession | None = None,
    live_release_evidence_verifier: Any = None,
) -> dict[str, Any]:
    require(
        sha256_repository_bytes(b"phase7\ncontract\n")
        == sha256_repository_bytes(b"phase7\r\ncontract\r\n"),
        "repository_digest_not_portable",
        "CRLF/LF normalization",
    )
    registry = load_yaml(REGISTRY_PATH)
    fixture = load_yaml(FIXTURE_PATH)
    polisher_routing_fixture = load_yaml(POLISHER_ROUTING_BOUNDARY_PATH)
    runtime_schema = load_yaml(RUNTIME_SCHEMA_PATH)
    runtime_collection = load_yaml(RUNTIME_RECEIPTS_PATH)
    reviewer_unavailable_fault_injection = (
        validate_reviewer_unavailable_fault_injection(runtime_schema, registry)
    )
    release_ledger = (
        json.loads(RELEASE_LEDGER_PATH.read_text(encoding="utf-8"))
        if RELEASE_LEDGER_PATH.is_file()
        else {}
    )
    declared_pairs = validate_fixture(fixture, registry)
    polisher_routing_results, polisher_routing_negative_results = (
        validate_polisher_routing_boundaries(polisher_routing_fixture, registry)
    )
    positive_results = [
        replay_case(case, build_runtime(case, registry), fixture, registry)
        for case in fixture["cases"]
    ]
    entry_gate_negative_results = []
    for case in fixture["cases"]:
        entry_gate_negative_results.append(
            expect_rejection(case, fixture, registry, "gate_bypass")
        )
        entry_gate_negative_results.append(
            expect_rejection(case, fixture, registry, case["secondary_mutation"])
        )

    evaluator_cases = [
        case
        for case in fixture["cases"]
        if any(
            transition["trigger"]
            in {"latest_version_accepted", "latest_strategy_portfolio_accepted"}
            for transition in fixture["path_profiles"][case["path_profile"]]["transitions"]
        )
    ]
    panel_cases = [
        case
        for case in fixture["cases"]
        if any(
            transition["trigger"] == "panel_gate_passed"
            for transition in fixture["path_profiles"][case["path_profile"]]["transitions"]
        )
    ]
    strategy_group_cases = [
        case
        for case in fixture["cases"]
        if workflow_profile(case, registry) == "reviewer_matrix_assemble_evaluate"
    ]
    transition_receipt_negative_results = [
        expect_transition_receipt_rejection(case, fixture, registry, mutation)
        for case in evaluator_cases
        for mutation in ("missing_evaluator_receipt", "stale_evaluator_receipt")
    ] + [
        expect_transition_receipt_rejection(case, fixture, registry, mutation)
        for case in panel_cases
        for mutation in ("missing_panel_receipt", "stale_panel_receipt")
    ] + [
        expect_transition_receipt_rejection(case, fixture, registry, mutation)
        for case in strategy_group_cases
        for mutation in (
            "missing_strategy_reviewer_receipt",
            "stale_strategy_reviewer_receipt",
            "duplicate_strategy_reviewer_instance",
        )
    ]
    negative_results = entry_gate_negative_results + transition_receipt_negative_results

    gate_bypass_count = sum(
        item["mutation"] == "gate_bypass" for item in entry_gate_negative_results
    )
    require(gate_bypass_count == len(declared_pairs), "gate_bypass_coverage", str(gate_bypass_count))
    final_states = Counter(item["final_state"] for item in positive_results)
    skill_count = len(registry["skills"])
    declared_entry_set = set(
        registry.get("public_entry_policy", {}).get("declared_entries", [])
    )
    implicit_entry_set = set(
        registry.get("public_entry_policy", {}).get("implicit_active_entries", [])
    )
    explicit_callable_entries = len(declared_entry_set)
    implicit_prompt_entries = len(implicit_entry_set)
    expected_implicit_entries = declared_entry_set - {"research-polisher-orchestrator"}
    require(
        skill_count == 49
        and explicit_callable_entries == 7
        and "research-polisher-orchestrator" in declared_entry_set
        and implicit_entry_set == expected_implicit_entries,
        "phase7_release_discovery_baseline",
        str((skill_count, explicit_callable_entries, implicit_prompt_entries)),
    )
    reviewer_count = sum(
        skill["requires_independent_subagent"] for skill in registry["skills"]
    )
    ledger_source = release_ledger.get("release", {}).get("source_commit", {})
    expected_source_commit = (
        ledger_source.get("sha")
        if isinstance(ledger_source, dict)
        and ledger_source.get("status") == "verified"
        and valid_commit_sha(ledger_source.get("sha"))
        else None
    )
    if external_runtime_session is None:
        runtime_results = validate_runtime_collection(
            runtime_collection,
            schema=runtime_schema,
            registry=registry,
            expected_source_commit=expected_source_commit,
            root=REPO,
        )
    else:
        runtime_results = consume_external_runtime_validation_session(
            external_runtime_session,
            collection=runtime_collection,
            runtime_receipts_path=RUNTIME_RECEIPTS_PATH,
            expected_source_commit=expected_source_commit,
        )
    (
        runtime_negative_results,
        runtime_contract_complete_results,
    ) = run_runtime_validator_self_tests(
        schema=runtime_schema,
        collection=runtime_collection,
        registry=registry,
    )
    completion_reachability = run_completion_reachability_self_test(
        registry, runtime_schema
    )
    require(
        live_release_evidence_verifier is None
        or external_runtime_session is not None,
        "release_live_verifier_without_runtime_session",
        "protected release verification requires the same-process runtime session",
    )
    if live_release_evidence_verifier is not None:
        from validate_openai_release_evidence import ReleaseEvidenceLiveCallback

        prepare_ledger = getattr(live_release_evidence_verifier, "prepare_ledger", None)
        assert_complete = getattr(
            live_release_evidence_verifier, "assert_complete", None
        )
        require(
            isinstance(
                live_release_evidence_verifier, ReleaseEvidenceLiveCallback
            )
            and callable(prepare_ledger)
            and callable(assert_complete),
            "release_live_verifier_invalid",
            type(live_release_evidence_verifier).__name__,
        )
        prepare_ledger(release_ledger)
    release_gates = release_gate_statuses(
        release_ledger,
        registry,
        live_evidence_verifier=live_release_evidence_verifier,
    )
    if live_release_evidence_verifier is not None:
        live_release_evidence_verifier.assert_complete()
    runtime_verification_level = accepted_runtime_verification_level(
        runtime_collection, external_runtime_session
    )
    platform_adapter_available = runtime_verification_level is not None
    completion_gates = completion_gate_statuses(
        runtime_results,
        release_gates,
        accepted_verification_level=runtime_verification_level,
        accepted_platform_adapter=platform_adapter_available,
    )
    pending_gates = [
        gate_id
        for gate_id, gate_result in completion_gates.items()
        if gate_result["status"] != "verified"
    ]
    if pending_gates:
        phase_status = "in_progress_live_and_release_evidence_pending"
    elif runtime_verification_level == PREVIEW_ATTESTED:
        phase_status = "complete_preview_attested"
    elif runtime_verification_level == PROVIDER_VERIFIED:
        phase_status = "complete_provider_verified"
    else:
        raise ModeViolation(
            "phase7_completion_without_verification_level",
            "all gates verified without an accepted evidence level",
        )
    runtime_gate_ids = {
        "accepted_platform_capture_adapter",
        "five_current_version_live_happy_paths",
        "five_current_version_valid_control_paths",
    }
    runtime_pending = any(gate_id in runtime_gate_ids for gate_id in pending_gates)
    release_pending = any(
        gate_id not in runtime_gate_ids for gate_id in pending_gates
    )
    if not pending_gates:
        phase_status_detail = "all_runtime_and_release_gates_verified"
    elif runtime_pending and release_pending:
        phase_status_detail = "runtime_and_release_evidence_pending"
    elif runtime_pending:
        phase_status_detail = "runtime_evidence_pending"
    else:
        phase_status_detail = "release_evidence_pending"
    return {
        "schema_version": 3,
        "active_acceptance_profile": "personal-owner",
        "personal_profile_status": "in_progress_owner_observation",
        "personal_readiness_report": "research-skills-openai/reports/personal-readiness.json",
        "deferred_preview_status": phase_status,
        "phase_status": phase_status,
        "verification_level": runtime_verification_level,
        "provider_verified": runtime_verification_level == PROVIDER_VERIFIED,
        "counts_as_preview_acceptance": (
            not pending_gates
            and runtime_verification_level in ACCEPTANCE_LEVELS
        ),
        "phase_status_detail": phase_status_detail,
        "phase_status_derivation": (
            "complete_preview_attested or complete_provider_verified only when every runtime and release-ledger gate is verified at one evidence level"
        ),
        "pending_gates": pending_gates,
        "completion_gates": completion_gates,
        "plugin_version": registry["plugin_version"],
        "registry_schema_version": registry["schema_version"],
        "registry_skill_count": skill_count,
        "discovery_contract": {
            "installed_skill_count": skill_count,
            "explicit_callable_entries": explicit_callable_entries,
            "implicit_prompt_entries": implicit_prompt_entries,
            "release_stage": "A",
        },
        "registry_workflow_edge_count": len(registry["workflow_edges"]),
        "registry_independent_reviewer_count": reviewer_count,
        "registry_sha256": sha256_repository_file(REGISTRY_PATH),
        "fixture_sha256": sha256_repository_file(FIXTURE_PATH),
        "research_polisher_routing_boundary_sha256": sha256_repository_file(
            POLISHER_ROUTING_BOUNDARY_PATH
        ),
        "runtime_receipt_schema_sha256": sha256_repository_file(RUNTIME_SCHEMA_PATH),
        "runtime_receipt_collection_sha256": sha256_repository_file(RUNTIME_RECEIPTS_PATH),
        "release_ledger_sha256": (
            sha256_repository_file(RELEASE_LEDGER_PATH)
            if RELEASE_LEDGER_PATH.is_file()
            else None
        ),
        "repository_contract_digest_policy": "sha256_crlf_normalized_to_lf",
        "runtime_evidence_file_digest_policy": "sha256_raw_file_bytes",
        "execution_kind": (
            "deterministic_replay_with_external_runtime_evidence"
            if external_runtime_session is not None
            else "deterministic_replay"
        ),
        "evidence_class": (
            "synthetic_contract_and_external_runtime_evidence"
            if external_runtime_session is not None
            else "synthetic_contract_evidence_only"
        ),
        "execution_scope": fixture["execution_scope"],
        "contract_source": "research-skills-openai/workflow-registry.yaml",
        "state_advance_order": (
            "validate_qualifying_receipt_then_validate_registry_prerequisites_"
            "then_commit_derived_state_then_execute_transition"
        ),
        "live_model_execution": external_runtime_session is not None,
        "deterministic_replay_notice": fixture["notice"],
        "positive_mode_results": positive_results,
        "negative_guard_results": negative_results,
        "research_polisher_routing_boundary_results": polisher_routing_results,
        "research_polisher_routing_negative_guards": polisher_routing_negative_results,
        "runtime_receipts": {
            "schema_path": "tests/openai_phase7/runtime-receipts.schema.yaml",
            "collection_path": "tests/openai_phase7/current-version-runtime-receipts.yaml",
            "expected_receipt_count": 10,
            "expected_workflow_case_matrix": "5 workflows x {happy, control}",
            "platform_trust": {
                **runtime_collection["platform_trust"],
                "supported_preview_attestation_adapter_ids": sorted(
                    SUPPORTED_PREVIEW_ATTESTATION_ADAPTERS
                ),
                "supported_authenticated_adapter_ids": sorted(
                    SUPPORTED_AUTHENTICATED_PLATFORM_ADAPTERS
                ),
                "completion_gate_verified": platform_adapter_available,
                "accepted_verification_level": runtime_verification_level,
                "repository_files_alone_count_as_platform_authenticity": False,
            },
            "verified_receipt_count": sum(
                item["status"] == "verified" for item in runtime_results
            ),
            "pending_receipt_count": sum(
                item["status"] == "pending_live_evidence" for item in runtime_results
            ),
            "results": runtime_results,
            "validator_negative_guards": runtime_negative_results,
            "contract_complete_positive_fixtures": (
                runtime_contract_complete_results
            ),
            "reviewer_unavailable_fault_injection": (
                reviewer_unavailable_fault_injection
            ),
            "completion_reachability_self_test": completion_reachability,
            "live_evidence_claimed": any(
                item["status"] == "verified" for item in runtime_results
            ),
        },
        "summary": {
            "declared_workflows": len(fixture["expected_workflows"]),
            "installed_skill_count": skill_count,
            "explicit_callable_entries": explicit_callable_entries,
            "implicit_prompt_entries": implicit_prompt_entries,
            "declared_entry_modes": len(declared_pairs),
            "registry_entry_mode_contracts_verified": len(declared_pairs),
            "registry_entry_gate_contracts_verified": sum(
                len(
                    registry["workflow_state_machines"][workflow]["entry_gates"][mode]
                )
                for workflow, mode in declared_pairs
            ),
            "fixture_declared_entry_gate_lists": sum(
                "expected_entry_gates" in case for case in fixture["cases"]
            ),
            "positive_modes_passed": len(positive_results),
            "mode_specific_gate_bypasses_rejected": gate_bypass_count,
            "additional_stale_or_lineage_guards_rejected": len(entry_gate_negative_results)
            - gate_bypass_count,
            "entry_gate_negative_guards_rejected": len(entry_gate_negative_results),
            "missing_evaluator_receipts_rejected": sum(
                item["mutation"] == "missing_evaluator_receipt"
                for item in transition_receipt_negative_results
            ),
            "stale_evaluator_receipts_rejected": sum(
                item["mutation"] == "stale_evaluator_receipt"
                for item in transition_receipt_negative_results
            ),
            "missing_panel_receipts_rejected": sum(
                item["mutation"] == "missing_panel_receipt"
                for item in transition_receipt_negative_results
            ),
            "stale_panel_receipts_rejected": sum(
                item["mutation"] == "stale_panel_receipt"
                for item in transition_receipt_negative_results
            ),
            "strategy_reviewer_group_mutations_rejected": sum(
                item["mutation"]
                in {
                    "missing_strategy_reviewer_receipt",
                    "stale_strategy_reviewer_receipt",
                    "duplicate_strategy_reviewer_instance",
                }
                for item in transition_receipt_negative_results
            ),
            "qualifying_reviewer_receipt_negatives_rejected": len(
                transition_receipt_negative_results
            ),
            "negative_guards_rejected": len(negative_results),
            "research_polisher_routing_boundaries_verified": len(
                polisher_routing_results
            ),
            "research_polisher_takeover_mutations_rejected": len(
                polisher_routing_negative_results
            ),
            "human_signoff_required_modes": final_states["human_signoff_required"],
            "human_strategy_selection_required_modes": final_states[
                "human_strategy_selection_required"
            ],
            "mode_scoped_stopped_modes": final_states["stopped"],
            "false_ready_count": 0,
            "automatic_external_submission": False,
            "live_model_runs_claimed": sum(
                item["status"] == "verified" for item in runtime_results
            ),
            "runtime_receipts_expected": 10,
            "runtime_receipts_verified": sum(
                item["status"] == "verified" for item in runtime_results
            ),
            "runtime_receipts_pending": sum(
                item["status"] == "pending_live_evidence" for item in runtime_results
            ),
            "runtime_validator_negative_guards_rejected": len(
                runtime_negative_results
            ),
            "runtime_contract_complete_workflows_verified": len(
                runtime_contract_complete_results
            ),
            "reviewer_unavailable_fault_injections_verified": 1,
            "completion_gates_verified": sum(
                item["status"] == "verified" for item in completion_gates.values()
            ),
            "completion_gates_pending": len(pending_gates),
            "synthetic_evaluator_receipts_validated": sum(
                len(item["synthetic_evaluator_receipt_ids"])
                for item in positive_results
            ),
            "synthetic_panel_receipts_validated": sum(
                len(item["synthetic_panel_receipt_ids"])
                for item in positive_results
            ),
            "synthetic_strategy_reviewer_receipts_validated": sum(
                len(item["synthetic_strategy_reviewer_receipt_ids"])
                for item in positive_results
            ),
            "synthetic_generation_receipts_validated": sum(
                len(item["synthetic_generation_receipt_ids"])
                for item in positive_results
            ),
            "synthetic_package_receipts_validated": sum(
                len(item["synthetic_package_receipt_ids"])
                for item in positive_results
            ),
            "synthetic_control_receipts_validated": sum(
                len(item["synthetic_control_receipts"])
                for item in positive_results
            ),
        },
    }


def assert_phase7_complete_preview(report: Mapping[str, Any]) -> None:
    """Fail closed unless a report proves the complete 10-slot Preview gate."""

    require(
        report.get("schema_version") == 3
        and report.get("phase_status") == "complete_preview_attested"
        and report.get("verification_level") == PREVIEW_ATTESTED
        and report.get("provider_verified") is False
        and report.get("counts_as_preview_acceptance") is True
        and report.get("pending_gates") == []
        and report.get("live_model_execution") is True,
        "phase7_complete_preview_required",
        str(report.get("phase_status")),
    )
    completion_gates = report.get("completion_gates")
    require(
        isinstance(completion_gates, Mapping)
        and len(completion_gates) == 13
        and all(
            isinstance(value, Mapping) and value.get("status") == "verified"
            for value in completion_gates.values()
        ),
        "phase7_complete_preview_gate_matrix_invalid",
        str(len(completion_gates) if isinstance(completion_gates, Mapping) else None),
    )
    runtime = report.get("runtime_receipts")
    results = runtime.get("results") if isinstance(runtime, Mapping) else None
    expected_pairs = {
        (workflow, case_kind)
        for workflow in (
            "idea",
            "proposal",
            "article",
            "perspective",
            "research_polisher",
        )
        for case_kind in ("happy", "control")
    }
    require(
        isinstance(results, list)
        and len(results) == 10
        and all(isinstance(item, Mapping) for item in results)
        and {
            (item.get("workflow"), item.get("case_kind")) for item in results
        }
        == expected_pairs
        and len({item.get("receipt_id") for item in results}) == 10
        and len(
            {(item.get("platform"), item.get("task_id")) for item in results}
        )
        == 10
        and len({item.get("task_export_path") for item in results}) == 10
        and len({item.get("task_export_sha256") for item in results}) == 10
        and all(
            item.get("status") == "verified"
            and item.get("verification_level") == PREVIEW_ATTESTED
            and item.get("evidence_accounting_status")
            == "externally_attested_runtime_evidence"
            for item in results
        )
        and runtime.get("verified_receipt_count") == 10
        and runtime.get("pending_receipt_count") == 0,
        "phase7_complete_preview_runtime_matrix_invalid",
        str(len(results) if isinstance(results, list) else None),
    )
    summary = report.get("summary")
    require(
        isinstance(summary, Mapping)
        and summary.get("runtime_receipts_verified") == 10
        and summary.get("runtime_receipts_pending") == 0
        and summary.get("live_model_runs_claimed") == 10
        and summary.get("completion_gates_verified") == 13
        and summary.get("completion_gates_pending") == 0
        and summary.get("false_ready_count") == 0,
        "phase7_complete_preview_summary_invalid",
        str(summary),
    )


def build_attested_phase7_report(
    *,
    external_runtime_session: ExternalRuntimeValidationSession,
    live_release_evidence_verifier: Any,
) -> dict[str, Any]:
    """Build the accepted report while both live capabilities remain in memory."""

    report = run_all(
        external_runtime_session=external_runtime_session,
        live_release_evidence_verifier=live_release_evidence_verifier,
    )
    assert_phase7_complete_preview(report)
    return report


def write_phase7_report(
    report: Mapping[str, Any], *, output_path: Path = REPORT_PATH
) -> None:
    """Atomically write a report only after strict Preview validation."""

    assert_phase7_complete_preview(report)
    require(
        output_path.parent.is_dir()
        and not output_path.parent.is_symlink()
        and not output_path.is_symlink(),
        "phase7_report_output_invalid",
        str(output_path),
    )
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            dir=output_path.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(
                json.dumps(
                    dict(report), indent=2, ensure_ascii=False, sort_keys=True
                )
                + "\n"
            )
        temporary.replace(output_path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


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
        require(
            REPORT_PATH.read_text(encoding="utf-8") == rendered,
            "report_drift",
            str(REPORT_PATH),
        )

    summary = result["summary"]
    print("Phase 7 synthetic entry-mode contract replays passed")
    print(
        f"entry modes: {summary['positive_modes_passed']}/{summary['declared_entry_modes']}"
    )
    print(
        "personal-owner discovery: "
        f"{summary['installed_skill_count']} installed skills / "
        f"{summary['explicit_callable_entries']} explicit entries / "
        f"{summary['implicit_prompt_entries']} implicit entries"
    )
    print(
        "negative guards: "
        f"{summary['mode_specific_gate_bypasses_rejected']} mode-specific gate bypasses + "
        f"{summary['additional_stale_or_lineage_guards_rejected']} entry stale/lineage mutations + "
        f"{summary['qualifying_reviewer_receipt_negatives_rejected']} evaluator/panel/strategy/supporting-reviewer receipt mutations rejected"
    )
    print(
        "Research Polisher routing boundaries: "
        f"{summary['research_polisher_routing_boundaries_verified']} cases; "
        f"{summary['research_polisher_takeover_mutations_rejected']} false-takeover mutations rejected"
    )
    print(
        "evidence scope: synthetic deterministic contract replay only; no live model, "
        "Search, Deep Research, Codex task, or ChatGPT task was run"
    )
    print(
        "synthetic closed-loop receipts: "
        f"{summary['synthetic_generation_receipts_validated']} generation/version + "
        f"{summary['synthetic_strategy_reviewer_receipts_validated']} role-isolated strategy-reviewer + "
        f"{summary['synthetic_panel_receipts_validated']} role-isolated panel + "
        f"{summary['synthetic_package_receipts_validated']} package + "
        f"{summary['synthetic_control_receipts_validated']} control"
    )
    print(
        "runtime contract-complete fixtures: "
        f"{summary['runtime_contract_complete_workflows_verified']}/5 workflows"
    )
    print(
        "durable runtime receipts: "
        f"{summary['runtime_receipts_verified']}/{summary['runtime_receipts_expected']} verified; "
        f"{summary['completion_gates_pending']} completion gates pending"
    )
    print(f"Personal profile status: {result['personal_profile_status']}")
    print(f"Deferred Preview status: {result['deferred_preview_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
