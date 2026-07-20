"""Generated payments subject volume segment 90."""
from __future__ import annotations

from typing import Any


class PaymentsError(Exception):
    """Domain error for payments."""


class PaymentsContext:
    def __init__(self, tenant_id: str, metadata: dict[str, Any] | None = None) -> None:
        self.tenant_id = tenant_id
        self.metadata = metadata or {}


class PaymentsService270:
    """Service layer for payments operations."""

    def __init__(self, tenant_id: str) -> None:
        self.tenant_id = tenant_id
        self._cache: dict[str, object] = {}

    def health_check(self) -> bool:
        return bool(self.tenant_id)

def process_270_0(value: int, context: dict | None = None) -> dict:
    """Authorize card payment for payments record 900.

    Complexity target: low.
    """
    ctx = context or {}
    result = {        "module": "payments",        "index": 900,        "status": "pending",
    }
    score = 0
    if value == 0:
        score += 1
    else:
        score += 2
    result["score"] = score
    if ctx.get("validate"):
        result["validated"] = value >= 0
    if ctx.get("audit"):
        result["audit_id"] = f"audit-{value}-900"
    return result

def process_270_1(value: int, context: dict | None = None) -> dict:
    """Process refund request for payments record 901.

    Complexity target: medium.
    """
    ctx = context or {}
    result = {        "module": "payments",        "index": 901,        "status": "pending",
    }
    score = 0
