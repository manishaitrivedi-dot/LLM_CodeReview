# py_dup_unused.py
# MEDIUM: duplicated logic
# LOW: unused import

import math   # LOW: may be unused

def compute(x):
    # duplicated blocks -> maintainability issue
    if x > 10:
        return x * 2
    if x > 10:
        return x * 2
    if x > 10:
        return x * 2
    return x
