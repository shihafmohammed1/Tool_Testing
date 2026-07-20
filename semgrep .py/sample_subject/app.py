"""Secure training subject for Semgrep OSS + Bandit SAST metrics (100/100)."""

from __future__ import annotations

import hashlib
import hmac
import html
import logging
import secrets
from typing import Any

logger = logging.getLogger(__name__)


def sanitize_input(value: str) -> str:
    """Escape and trim external user input before use."""
    return html.escape(value.strip())


def verify_password(stored_hash: str, password: str) -> bool:
    """Compare password digests using a constant-time check."""
    digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(stored_hash, digest)


def fetch_user(user_id: str, cursor) -> dict[str, Any]:
    """Fetch a user record using a parameterized query."""
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else {}


def require_role(session: dict | None, role: str) -> bool:
    """Verify authenticated session role before privileged actions."""
    if not session or not session.get("authenticated"):
        return False
    return session.get("role") == role


def process_payload(payload: dict[str, Any]) -> dict[str, str]:
    """Validate and process an external payload without leaking sensitive data."""
    name = sanitize_input(str(payload.get("name", "")))
    if not name:
        raise ValueError("name is required")
    logger.info("request processed")
    return {"name": name, "status": "ok"}


def mask_token(token: str) -> str:
    """Mask sensitive tokens before logging or display."""
    if len(token) <= 4:
        return "****"
    return f"{token[:2]}****{token[-2:]}"
