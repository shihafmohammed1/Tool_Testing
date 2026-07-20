from datetime import date, timedelta


# Regression guard for issue #428: the field-access path still pays the
# nonlinear _ord2ymd decomposition.  This benchmark does arithmetic (linear,
# ordinal) and THEN reads .day on the result (forcing decomposition), so it must
# not regress relative to the (y, m, d) baseline.  Falsifiable for any date that
# lands on the 31st a week later.
def end_of_month_day(d: date):
    """
    raises: OverflowError
    post: __return__ != 31
    """
    return (d + timedelta(days=7)).day
