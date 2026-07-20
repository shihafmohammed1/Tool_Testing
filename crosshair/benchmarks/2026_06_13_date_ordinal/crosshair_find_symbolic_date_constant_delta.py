from datetime import date, timedelta


# Headline case for CrossHair issue #428: a *symbolic* date plus a constant
# delta.  Under the (year, month, day) representation this forces the nonlinear
# ordinal<->calendar conversion into the arithmetic; with an ordinal-primary
# representation it should be linear.  (This is the `days=8314` TODO left in
# 2022_10_06_date_arithmetic/crosshair_find_date_w_constant_delta.py.)
def date_addition(base_date: date):
    """
    raises: OverflowError
    post: __return__ != date(2022, 10, 6)
    """
    return base_date + timedelta(days=8314)
