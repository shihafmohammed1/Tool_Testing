"""Discount calculation with operator-sensitive comparisons."""

PERCENT_FLOOR = 0.0
PERCENT_CEILING = 100.0


def apply_percentage_discount(price: float, percent: float) -> float:
    """Apply a percentage discount and never return a negative price."""
    bounded_percent = min(max(percent, PERCENT_FLOOR), PERCENT_CEILING)
    discount_amount = price * bounded_percent / PERCENT_CEILING
    discounted = price - discount_amount
    return max(discounted, PERCENT_FLOOR)


def tiered_shipping(weight_kg: float) -> float:
    """Return shipping cost based on weight boundaries."""
    if weight_kg <= 0:
        return 0.0
    if weight_kg <= 5:
        return 5.0
    if weight_kg <= 20:
        return 12.0
    return 25.0
