from datetime import date, timedelta


# Both operands symbolic: symbolic date + symbolic timedelta.  Pure ordinal
# arithmetic after issue #428; nonlinear under the (y, m, d) representation.
def date_addition(base_date: date, delta: timedelta):
    """
    raises: OverflowError
    post: __return__ != date(2022, 10, 6)
    """
    return base_date + delta
