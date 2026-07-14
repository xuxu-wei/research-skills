#!/usr/bin/env python3
"""Shared dispatch for frozen Preview capture formats.

Phase 7 keeps its Codex App Server v1 capture contract.  Phase 8 uses a
profile-aware v2 contract.  Callers must dispatch by the explicit
``normalization_schema`` value; probing fields or falling back after a failed
validation would let a malformed capture select a weaker validator.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping


PHASE7_NORMALIZED_CAPTURE_SCHEMA = "openai-preview-normalized-capture/v1"
PHASE8_NORMALIZED_CAPTURE_SCHEMA = "openai-preview-normalized-capture/v2"
PHASE8_CAPTURE_ADAPTER_ID = "openai_phase8_capture_normalizer_v2"


def capture_schema(document: Mapping[str, Any]) -> str:
    value = document.get("normalization_schema")
    if not isinstance(value, str) or not value:
        raise ValueError("normalized capture has no explicit normalization_schema")
    return value


def validate_normalized_capture(
    document: Mapping[str, Any],
    *,
    now: datetime,
    verify_checkout: bool = True,
) -> Mapping[str, Any]:
    """Validate exactly one supported normalized capture without fallback."""

    schema = capture_schema(document)
    if schema == PHASE7_NORMALIZED_CAPTURE_SCHEMA:
        from normalize_openai_preview_capture import validate_normalized_capture as validate_v1

        return validate_v1(document, now=now, verify_checkout=verify_checkout)
    if schema == PHASE8_NORMALIZED_CAPTURE_SCHEMA:
        from normalize_openai_phase8_capture import validate_normalized_capture as validate_v2

        return validate_v2(document, now=now, verify_checkout=verify_checkout)
    raise ValueError(f"unsupported normalized capture schema: {schema!r}")


def normalized_capture_adapter_id(document: Mapping[str, Any]) -> str:
    adapter = document.get("capture_adapter")
    if not isinstance(adapter, Mapping):
        raise ValueError("normalized capture has no capture_adapter object")
    value = adapter.get("adapter_id")
    if not isinstance(value, str) or not value:
        raise ValueError("normalized capture adapter_id is missing")
    return value
