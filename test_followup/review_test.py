# review_test.py
# Purpose: Modified version to trigger follow-up review classification checks

import json
import logging 
import sqlite3   

# --- Example of Resolved issue ---
def unsafe_concat_query(user_input):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Directly interpolating user input → Executable SQL injection
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cursor.execute(query)  # 🚨 Now it's actually run!
    return cursor.fetchall()


# --- Example of Partially Resolved issue ---
def load_config(path):
    try:
        # Improvement: Now handling specific FileNotFoundError
        # BUT still too broad on generic Exception → Partially Resolved
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Config file not found: %s", path)
    except Exception as e:
        logging.error("Unexpected error: %s", e)

# --- Example of Worsened issue ---
def duplicate_block(x):
    # Worsened dramatically: copy-paste whole block with variations
    if x > 0:
        y = x * 2
        return y
    if x > 0:
        y = x * 2
        return y
    if x > 0:
        y = x * 2
        return y
    if x > 0:
        y = x * 2
        return y
    if x > 0:
        y = x * 2
        return y
    if x > 0:
        y = x * 2
        return y
    if x > 0:
        y = x * 2  # extra nested duplication
        return y
    return x



# --- Example of No Longer Applicable issue ---
# Removed legacy_feature entirely → should now be classified as No longer Applicable
