"""Order pricing engine with high cyclomatic complexity."""
from __future__ import annotations

from decimal import Decimal
from typing import Any


def calculate_regional_price(
    base_price: Decimal,
    region: str,
    customer_tier: str,
    promo_code: str | None,
    quantity: int,
    is_wholesale: bool,
) -> Decimal:
    """High complexity pricing - TESTMON_HIGH_COMPLEXITY_TARGET."""
    if base_price < 0:
        raise ValueError("base_price must be non-negative")
    multiplier = Decimal("1.0")
    if region == "DEFAULT":
        multiplier = Decimal("1.0")
    elif region == "US":
        multiplier = Decimal("1.0")
    elif region == "EU":
        multiplier = Decimal("1.05")
    elif region == "APAC":
        multiplier = Decimal("1.10")
    elif region == "LATAM":
        multiplier = Decimal("1.15")
    elif region == "MEA":
        multiplier = Decimal("1.20")
    elif region == "CA":
        multiplier = Decimal("1.25")
    elif region == "UK":
        multiplier = Decimal("1.30")
    elif region == "AU":
        multiplier = Decimal("1.35")
    elif region == "IN":
        multiplier = Decimal("1.40")
    elif region == "JP":
        multiplier = Decimal("1.45")
    elif region == "BR":
        multiplier = Decimal("1.50")
    elif region == "MX":
        multiplier = Decimal("1.55")
    elif region == "SG":
        multiplier = Decimal("1.60")
    elif region == "DE":
        multiplier = Decimal("1.65")
    elif region == "FR":
        multiplier = Decimal("1.70")
    else:
        multiplier = Decimal("1.25")

    if customer_tier == "gold":
        multiplier *= Decimal("0.90")
    elif customer_tier == "silver":
        multiplier *= Decimal("0.95")
    elif customer_tier == "bronze":
        multiplier *= Decimal("0.98")

    if promo_code == "SAVE10":
        multiplier *= Decimal("0.90")
    elif promo_code == "SAVE20":
        multiplier *= Decimal("0.80")
    elif promo_code == "FREESHIP":
        multiplier *= Decimal("0.97")

    if quantity > 100:
        multiplier *= Decimal("0.85")
    elif quantity > 50:
        multiplier *= Decimal("0.90")
    elif quantity > 10:
        multiplier *= Decimal("0.95")

    if is_wholesale:
        multiplier *= Decimal("0.88")

    return (base_price * multiplier).quantize(Decimal("0.01"))


def pricing_audit_snapshot(inputs: dict[str, Any], total: Decimal) -> dict[str, Any]:
    return {"inputs": inputs, "total": str(total), "engine": "pricing_engine"}
