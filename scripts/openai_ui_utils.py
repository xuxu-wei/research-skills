#!/usr/bin/env python3
"""Shared validation rules for OpenAI skill UI metadata."""

from __future__ import annotations


SHORT_DESCRIPTION_MIN = 25
SHORT_DESCRIPTION_MAX = 64


def short_description_error(value: object) -> str | None:
    """Return a validation error for a short UI description, or ``None``."""

    if not isinstance(value, str):
        return "interface.short_description must be a string"
    if value != value.strip():
        return "interface.short_description must not have surrounding whitespace"
    if "\n" in value or "\r" in value:
        return "interface.short_description must be a single line"
    length = len(value)
    if not SHORT_DESCRIPTION_MIN <= length <= SHORT_DESCRIPTION_MAX:
        return (
            "interface.short_description must contain "
            f"{SHORT_DESCRIPTION_MIN}-{SHORT_DESCRIPTION_MAX} characters; got {length}"
        )
    return None
