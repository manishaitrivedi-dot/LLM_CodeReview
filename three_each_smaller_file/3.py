
# py_sql_exec.py
# CRITICAL: executes interpolated SQL using user input (exploitable SQL injection)

import sqlite3

def unsafe_execute(user_input):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (name TEXT);")
    # CRITICAL: executed interpolated query - real exploitable flow
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cur.execute(query)   # <-- change this single line for a small diff
    return cur.fetchall()
