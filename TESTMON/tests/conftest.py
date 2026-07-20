import pytest
from commerce_platform.utils.shared import merge_context, normalize_identifier


@pytest.fixture
def tenant_context():
    return {"tenant_id": "tenant-alpha", "validate": True, "audit": True}


@pytest.fixture
def shared_identifier():
    return normalize_identifier("order-1001")
