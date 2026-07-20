from datetime import date


# date - date -> timedelta.  Should stay linear (subtract two ordinals) under
# issue #428.  Falsifiable for any pair of dates exactly 8314 days apart.
def days_between(d1: date, d2: date):
    """
    post: __return__.days != 8314
    """
    return d1 - d2
