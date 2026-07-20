"""Test case to trigger complexity detection (too many return statements and too many branches)."""

def complex_function(val):
    """Triggers too-many-return-statements (R0911) and too-many-branches (R0912)."""
    if val == 1:
        return "one"
    elif val == 2:
        return "two"
    elif val == 3:
        return "three"
    elif val == 4:
        return "four"
    elif val == 5:
        return "five"
    elif val == 6:
        return "six"
    elif val == 7:
        return "seven"
    
    # Extra branches to trigger R0912 too-many-branches (limit is 12)
    # Let's count branches: each if/elif adds a branch. We already have 7.
    # Let's add more:
    if val > 10:
        if val < 20:
            if val % 2 == 0:
                print("Even inside range")
            else:
                print("Odd inside range")
        else:
            if val % 3 == 0:
                print("Divisible by 3")
            else:
                print("Not divisible by 3")
    else:
        if val < 0:
            print("Negative")
        else:
            print("Zero or positive small")

    return "default"
