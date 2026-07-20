import pytest
from commerce_platform.auth.session import (
    SessionError,
    create_session_token,
    enrich_session_metadata,
    validate_session_expiry,
)
from datetime import datetime, timedelta


def test_create_session_token_success():
    token = create_session_token("user-1", "secret")
    assert len(token) == 64


def test_create_session_token_requires_user_id():
    with pytest.raises(SessionError):
        create_session_token("", "secret")


@pytest.mark.fragile
def test_create_session_token_deterministic():
    assert create_session_token("user-1", "secret") == create_session_token("user-1", "secret")


def test_validate_session_expiry_active():
    issued = datetime.utcnow()
    assert validate_session_expiry(issued, 24) is True


def test_validate_session_expiry_invalid_ttl():
    issued = datetime.utcnow()
    assert validate_session_expiry(issued, 0) is False


def test_enrich_session_metadata_defaults():
    result = enrich_session_metadata({"user_id": "u1"})
    assert result["active"] is True
    assert "created_at" in result
