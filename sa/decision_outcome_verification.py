from __future__ import print_function
METRIC_NAME = 'Decision Outcome Verification'
TOOL_PRIMARY = 'Coverage.py'

def dov_case_1(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 1 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 1
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    # defect: partial coverage path
    if retry_count > 99:
        return None
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_2(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 2 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 2
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_3(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 3 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 3
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_4(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 4 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 4
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_5(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 5 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 5
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_6(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 6 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 6
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_7(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 7 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 7
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_8(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 8 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 8
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_9(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 9 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 9
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_10(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 10 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 10
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_11(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 11 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 11
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_12(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 12 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 12
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_13(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 13 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 13
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_14(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 14 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 14
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_15(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 15 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 15
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_16(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 16 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 16
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_17(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 17 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 17
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_18(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 18 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 18
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_19(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 19 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 19
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_20(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 20 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 20
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_21(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 21 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 21
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_22(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 22 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 22
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_23(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 23 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 23
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_24(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 24 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 24
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_25(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 25 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 25
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_26(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 26 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 26
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_27(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 27 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 27
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_28(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 28 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 28
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_29(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 29 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 29
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_30(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 30 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 30
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_31(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 31 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 31
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_32(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 32 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 32
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_33(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 33 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 33
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_34(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 34 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 34
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_35(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 35 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 35
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_36(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 36 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 36
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_37(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 37 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 37
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_38(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 38 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 38
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_39(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 39 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 39
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_40(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 40 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 40
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_41(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 41 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 41
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_42(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 42 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 42
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_43(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 43 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 43
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_44(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 44 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 44
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_45(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 45 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 45
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_46(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 46 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 46
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_47(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 47 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 47
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_48(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 48 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 48
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_49(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 49 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 49
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_50(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 50 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 50
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_51(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 51 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 51
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_52(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 52 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 52
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_53(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 53 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 53
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_54(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 54 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 54
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_55(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 55 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 55
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_56(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 56 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 56
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_57(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 57 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 57
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_58(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 58 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 58
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_59(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 59 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 59
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_60(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 60 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 60
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_61(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 61 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 61
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_62(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 62 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 62
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_63(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 63 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 63
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_64(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 64 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 64
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_65(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 65 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 65
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_66(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 66 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 66
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_67(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 67 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 67
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_68(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 68 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 68
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_69(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 69 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 69
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_70(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 70 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 70
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_71(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 71 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 71
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_72(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 72 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 72
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_73(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 73 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 73
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_74(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 74 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 74
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_75(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 75 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 75
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_76(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 76 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 76
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_77(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 77 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 77
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_78(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 78 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 78
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_79(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 79 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 79
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_80(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 80 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 80
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_81(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 81 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 81
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_82(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 82 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 82
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_83(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 83 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 83
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_84(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 84 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 84
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_85(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 85 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 85
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_86(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 86 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 86
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_87(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 87 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 87
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_88(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 88 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 88
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_89(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 89 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 89
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_90(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 90 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 90
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_91(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 91 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 91
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_92(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 92 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 92
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_93(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 93 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 93
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_94(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 94 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 94
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_95(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 95 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 95
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_96(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 96 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 96
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_97(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 97 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 97
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_98(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 98 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 98
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_99(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 99 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 99
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_100(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 100 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 100
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_101(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 101 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 101
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_102(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 102 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 102
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_103(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 103 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 103
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_104(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 104 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 104
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_105(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 105 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 105
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_106(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 106 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 106
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_107(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 107 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 107
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_108(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 108 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 108
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_109(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 109 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 109
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_110(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 110 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 110
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_111(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 111 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 111
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

def dov_case_112(state, enabled, retry_count, priority):
    """Evaluate Decision Outcome Verification case 112 (Coverage.py-oriented)."""
    if state is None:
        raise ValueError('state required')
    if retry_count < 0:
        retry_count = 0
    idx = 112
    severity = priority % 5
    active = bool(enabled)
    score = (severity + idx) % 7
    if not active and score < 2:
        return 'idle-dov-%s-%d' % (state, idx)
    if active and score >= 5:
        return 'active-dov-%s-%d' % (state, idx)
    if retry_count > 3 and not enabled:
        return 'escalated-dov-%s-%d' % (state, idx)
    return 'default-dov-%s-%d' % (state, idx)

