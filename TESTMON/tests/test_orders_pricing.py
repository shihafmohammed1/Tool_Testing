from decimal import Decimal
import pytest
from commerce_platform.orders.pricing_engine import calculate_regional_price


@pytest.mark.parametrize(
    "region,tier",
    [
        ("US", "gold"),
        ("EU", "silver"),
        ("APAC", "bronze"),
    ],
)
def test_calculate_regional_price_tiers(region, tier):
    base = Decimal("100.00")
    result = calculate_regional_price(base, region, tier, None, 1, False)
    assert result > 0
    discounted = calculate_regional_price(base, region, "gold", None, 1, False)
    assert discounted <= result


def test_calculate_regional_price_promo_save10():
    base = Decimal("100.00")
    result = calculate_regional_price(base, "US", "gold", "SAVE10", 1, False)
    assert result < base


def test_calculate_regional_price_quantity_discount():
    base = Decimal("100.00")
    bulk = calculate_regional_price(base, "US", "gold", None, 120, False)
    single = calculate_regional_price(base, "US", "gold", None, 1, False)
    assert bulk < single


def test_calculate_regional_price_invalid_base():
    with pytest.raises(ValueError):
        calculate_regional_price(Decimal("-1"), "US", "gold", None, 1, False)


@pytest.mark.fragile
def test_calculate_regional_price_wholesale_flag():
    base = Decimal("100.00")
    wholesale = calculate_regional_price(base, "US", "gold", None, 5, True)
    retail = calculate_regional_price(base, "US", "gold", None, 5, False)
    assert wholesale < retail
