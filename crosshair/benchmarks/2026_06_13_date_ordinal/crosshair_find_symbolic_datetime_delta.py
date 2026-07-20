from datetime import datetime, timedelta


# Phase 3 of issue #428: the same ordinal-backing extended to datetime.  A
# symbolic datetime plus a constant delta; mirrors the existing concrete-base
# crosshair_find_datetime_delta.py but makes the datetime itself symbolic.
def datetime_addition(base: datetime):
    """
    raises: OverflowError
    post: __return__ != datetime(2022, 10, 6, 13, 15, 59)
    """
    return base + timedelta(days=8314)
