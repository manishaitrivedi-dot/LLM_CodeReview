# review_test.py
# Purpose: Test file for validating follow-up review classification logic.

import json
# Past issue: unused imports
# FIXED → should be classified as Resolved

# --- Example of Not Addressed issue ---
def unsafe_concat_query(table, column, value):
    # Old flagged issue: SQL injection risk → still present
    query = f"SELECT {column} FROM {table} WHERE value = '{value}'"
    return query

# --- Example of Partially Resolved issue ---
def load_config(path):
    try:
        # Previously: no error handling at all
        # Now: basic try/except but too generic → only partially resolved
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        print("Error loading config")

# --- Example of Worsened issue ---
def duplicate_block(x):
    # Old issue: duplication in logic
    # Now made worse → copy-paste repeated 4 times
    if x > 0:
        return x * 2
    if x > 0:
        return x * 2
    if x > 0:
        return x * 2
    if x > 0:
        return x * 2
    return x

# --- Example of No Longer Applicable issue ---
def legacy_feature():
    # Function body removed → issue is no longer applicable
    pass
