import pytest
from commerce_platform.auth.session import create_session_token
from commerce_platform.orders.pricing_engine import calculate_regional_price
from commerce_platform.utils.shared import merge_context, normalize_identifier
from decimal import Decimal


@pytest.mark.integration
def test_checkout_context_pipeline(shared_identifier, tenant_context):
    token = create_session_token("buyer-1", "secret")
    price = calculate_regional_price(Decimal("50.00"), "US", "gold", None, 2, False)
    ctx = merge_context(tenant_context, {"order_id": shared_identifier, "token": token, "price": str(price)})
    assert ctx["tenant_id"] == "tenant-alpha"
    assert ctx["order_id"] == "ORDER-1001"
