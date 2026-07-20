from datetime import date, timedelta


# Components-backed date (Phase 2 of #428): the date is constructed from a
# symbolic-integer year, so it keeps (year, month, day) primary and must derive
# the ordinal lazily on the `+` (the _ymd2ord bridge), then decompose again to
# read .month (_ord2ymd).  Jan 1 + 365 days lands on Jan 1 of the next year in a
# common year but on Dec 31 of the same year in a leap year, so the
# postcondition is falsifiable exactly on leap years.
def add_a_year(year: int):
    """
    pre: 1 <= year <= 9998
    post: __return__.month == 1
    raises: OverflowError
    """
    return date(year, 1, 1) + timedelta(days=365)
