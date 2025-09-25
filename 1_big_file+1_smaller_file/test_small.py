# test_small.py
# Small test file to produce review findings:
# - Critical: executable SQL injection (cursor.execute on interpolated input)
# - Medium: broad exception handling
# - Medium: small duplication
# - Low: unused import

import json   # LOW: unused import (should be removed)
import sqlite3

def unsafe_execute(user_input):
    """CRITICAL: directly executes an interpolated query using user_input."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (name TEXT);")
    # unsafe: interpolated user input executed -> likely Critical
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cur.execute(query)   # <-- this execution is what makes it critical
    return cur.fetchall()

def load_config(path):
    # MEDIUM / PARTIALLY RESOLVED example: handles FileNotFoundError specifically,
    # but still catches broad Exception which can hide errors.
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config file missing:", path)
    except Exception:
        # MEDIUM: broad exception - mask underlying failures
        print("Unexpected error while loading config")

def duplicate_demo(x):
    # MEDIUM: small duplication to test maintainability detection
    if x > 0:
        return x * 2
    if x > 0:
        return x * 2
    return x
