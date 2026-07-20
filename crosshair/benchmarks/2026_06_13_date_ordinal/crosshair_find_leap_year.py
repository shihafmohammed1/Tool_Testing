from datetime import date, timedelta


# The test_leap_year scenario from CrossHair's datetimelib_test.py, but WITHOUT
# the `pre: start.month == 1 and start.day == 1` workaround that had to be added
# (issue #427) because the (y, m, d) representation made this 12-22s and flaky.
# Adding 365 days does not always advance the year by one (leap years have 366),
# so the postcondition is falsifiable.  Exercises arithmetic (should be linear
# after #428) plus a single field decomposition (.year) on the result.
def leap_year_add(start: date):
    """
    raises: OverflowError
    post: __return__.year == start.year + 1
    """
    return start + timedelta(days=365)
