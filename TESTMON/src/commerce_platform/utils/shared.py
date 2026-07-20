"""Shared utilities used across modules - TESTMON_SHARED_UTILITY_TARGET."""
from __future__ import annotations

import re
from typing import Any


IDENTIFIER_PATTERN = re.compile(r"^[A-Z0-9_-]{3,64}$")


def normalize_identifier(value: str) -> str:
    """Normalize business identifiers for cross-module usage."""
    cleaned = value.strip().upper().replace(" ", "_")
    if not IDENTIFIER_PATTERN.match(cleaned):
        raise ValueError(f"invalid identifier: {value}")
    return cleaned


def merge_context(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, val in extra.items():
        if val is not None:
            merged[key] = val
    return merged


def stable_sort_key(record: dict[str, Any]) -> tuple:
    return (
        record.get("priority", 99),
        record.get("created_at", ""),
        record.get("id", ""),
    )
