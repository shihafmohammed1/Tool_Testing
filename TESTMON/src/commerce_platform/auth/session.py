"""Authentication session management."""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta
from typing import Any


class SessionError(Exception):
    pass


def create_session_token(user_id: str, secret: str) -> str:
    """Low complexity session token creator - TESTMON_LOW_COMPLEXITY_TARGET."""
    if not user_id:
        raise SessionError("user_id required")
    payload = f"{user_id}:{secret}"
    return hashlib.sha256(payload.encode()).hexdigest()


def validate_session_expiry(issued_at: datetime, ttl_hours: int = 24) -> bool:
    if ttl_hours <= 0:
        return False
    return datetime.utcnow() <= issued_at + timedelta(hours=ttl_hours)


def enrich_session_metadata(session: dict[str, Any]) -> dict[str, Any]:
    session = dict(session)
    session.setdefault("created_at", datetime.utcnow().isoformat())
    session.setdefault("active", True)
    return session
