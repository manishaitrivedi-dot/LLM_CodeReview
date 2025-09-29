# py_config_creds.py
# HIGH: hardcoded credentials
# MEDIUM: broad exception handling

import json
import requests  # LOW: unused (may be flagged)

DB_USER = "admin"           # HIGH: hardcoded credential
DB_PASSWORD = "P@ssw0rd!"   # HIGH: hardcoded credential

def connect_and_fetch():
    try:
        # pretend to use credentials
        conn_string = f"user={DB_USER} password={DB_PASSWORD}"
        # Simulate a network call (not executed for safety)
        # requests.get("https://example.com/health")
        return conn_string
    except Exception:
        # MEDIUM: broad except masks real errors
        print("Connection error")

def load_settings(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Settings missing")
    except Exception:
        print("Unexpected error loading settings")
