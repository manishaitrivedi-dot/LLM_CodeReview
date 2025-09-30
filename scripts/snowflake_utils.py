# snowflake_utils.py

import os, sys, json
from snowflake.snowpark import Session
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


PRIVATE_KEY_PATH = os.path.expanduser("~/.snowflake/sf_private_key.p8")

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key:
        p_key = serialization.load_pem_private_key(
            key.read(),
            password=None,  # or b"your-passphrase" if the key has one
            backend=default_backend()
        )
    return p_key
    
def get_snowflake_config():
    """Get Snowflake configuration with fallbacks"""
    if os.getenv("SNOWFLAKE_ACCOUNT"):
        print("Using environment variable configuration")
        return {
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            #"password": os.getenv("SNOWFLAKE_PASSWORD"),
            "private_key_path": load_private_key(),
            #"role": os.getenv("SNOWFLAKE_ROLE", "SYSADMIN"),
            #"warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            #"database": os.getenv("SNOWFLAKE_DATABASE"),
            #"schema": os.getenv("SNOWFLAKE_SCHEMA"),
            "role": "SYSADMIN",
            "warehouse": "COMPUTE_WH",
            "database": "MY_DB",
            "schema": "PUBLIC",
        }
    # else:
    #     print("Environment variables not found, using fallback configuration")
    #     return {
    #         "account": "XKB93357.us-west-2",
    #         "user": "MANISHAT007",
    #         "password": "Welcome@987654321",
    #         "role": "SYSADMIN",
    #         "warehouse": "COMPUTE_WH",
    #         "database": "MY_DB",
    #         "schema": "PUBLIC",
    #     }

def get_snowflake_session():
    """Initialize Snowflake session with configuration"""
    cfg = get_snowflake_config()
    required_fields = ["account", "user", "private_key_path"]
    missing_fields = [field for field in required_fields if not cfg.get(field)]
    if missing_fields:
        print(f"Missing required Snowflake configuration: {missing_fields}")
        sys.exit(1)

    try:
        session = Session.builder.configs(cfg).create()
        print(f"Connected to Snowflake: {cfg['account']} as {cfg['user']}")
        return session, cfg
    except Exception as e:
        print(f"Failed to connect to Snowflake: {e}")
        sys.exit(1)

def setup_database_with_fallback(session, cfg):
    """Setup database with multiple fallback strategies"""
    database_available = False
    current_database = None
    current_schema = None
    print("Setting up database for review logging...")
    db_env = cfg.get("database") or "MY_DB"
    schema_env = cfg.get("schema") or "PUBLIC"
    role_env = cfg.get("role") or "SYSADMIN"
    print(f"  Attempting to use: {db_env}.{schema_env} with role {role_env}")
    
    try:
        session.sql(f"USE ROLE {role_env}").collect()
        print(f"    Using role {role_env}")
        try:
            session.sql(f"GRANT USAGE ON DATABASE {db_env} TO ROLE {role_env}").collect()
            session.sql(f"GRANT USAGE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
            session.sql(f"GRANT CREATE TABLE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
            session.sql(f"GRANT INSERT ON ALL TABLES IN SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
            print(f"    Granted permissions (if allowed)")
        except Exception as grant_e:
            print(f"    Grant permissions failed (may not have GRANT privileges): {grant_e}")
        session.sql(f"USE DATABASE {db_env}").collect()
        session.sql(f"USE SCHEMA {schema_env}").collect()
        current_database = db_env
        current_schema = schema_env
        print(f"Strategy 1: Successfully using {db_env}.{schema_env}")
        database_available = True
        return database_available, current_database, current_schema
    except Exception as e:
        print(f"Strategy 1 failed: {e}")

    try:
        session.sql(f"USE ROLE {role_env}").collect()
        session.sql("CREATE DATABASE IF NOT EXISTS CODE_REVIEWS").collect()
        session.sql("USE DATABASE CODE_REVIEWS").collect()
        session.sql("CREATE SCHEMA IF NOT EXISTS REVIEWS").collect()
        session.sql("USE SCHEMA REVIEWS").collect()
        current_database = "CODE_REVIEWS"
        current_schema = "REVIEWS"
        print("Strategy 2: Successfully created and using CODE_REVIEWS.REVIEWS")
        database_available = True
        return database_available, current_database, current_schema
    except Exception as e:
        print(f"Strategy 2 failed: {e}")

    try:
        session.sql(f"USE ROLE {role_env}").collect()
        user_db = f"DB_{cfg.get('user', 'USER').upper()}"
        session.sql(f"CREATE DATABASE IF NOT EXISTS {user_db}").collect()
        session.sql(f"USE DATABASE {user_db}").collect()
        session.sql("CREATE SCHEMA IF NOT EXISTS LOGS").collect()
        session.sql("USE SCHEMA LOGS").collect()
        current_database = user_db
        current_schema = "LOGS"
        print(f"Strategy 3: Successfully created and using {user_db}.LOGS")
        database_available = True
        return database_available, current_database, current_schema
    except Exception as e:
        print(f"Strategy 3 failed: {e}")

    try:
        session.sql("USE ROLE ACCOUNTADMIN").collect()
        session.sql(f"CREATE DATABASE IF NOT EXISTS {db_env}").collect()
        session.sql(f"USE DATABASE {db_env}").collect()
        session.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_env}").collect()
        session.sql(f"USE SCHEMA {schema_env}").collect()
        session.sql(f"GRANT USAGE ON DATABASE {db_env} TO ROLE {role_env}").collect()
        session.sql(f"GRANT USAGE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
        session.sql(f"GRANT CREATE TABLE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
        session.sql(f"USE ROLE {role_env}").collect()
        current_database = db_env
        current_schema = schema_env
        print(f"Strategy 4: Successfully created {db_env}.{schema_env} with ACCOUNTADMIN")
        database_available = True
        return database_available, current_database, current_schema
    except Exception as e:
        print(f"Strategy 4 failed: {e}")

    print("All database strategies failed - continuing without logging")
    database_available = False
    return database_available, current_database, current_schema

def setup_review_log_table(session, database_available, current_database, current_schema):
    """Setup the review log table with VARIANT columns and comparison_result field"""
    if not database_available:
        return False
    try:
        check_table_query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = ?
        AND TABLE_NAME = 'CODE_REVIEW_LOG'
        """
        try:
            existing_columns = session.sql(check_table_query, params=[current_schema]).collect()
            column_names = [row['COLUMN_NAME'] for row in existing_columns]
            if 'COMPARISON_RESULT' not in column_names:
                print(f"  Adding COMPARISON_RESULT column to existing table...")
                alter_table_query = f"""
                ALTER TABLE {current_database}.{current_schema}.CODE_REVIEW_LOG
                ADD COLUMN COMPARISON_RESULT VARIANT
                """
                session.sql(alter_table_query).collect()
                print(f"Added COMPARISON_RESULT column to existing table")
                return True
            else:
                print(f"Review log table already has correct structure in {current_database}.{current_schema}")
                return True
        except Exception as check_error:
            print(f"  Table doesn't exist or error checking: {check_error}. Creating new table...")
        create_table_query = f"""
        CREATE TABLE {current_database}.{current_schema}.CODE_REVIEW_LOG (
            REVIEW_ID INTEGER AUTOINCREMENT START 1 INCREMENT 1,
            PULL_REQUEST_NUMBER INTEGER,
            COMMIT_SHA VARCHAR(40),
            REVIEW_SUMMARY VARIANT,
            DETAILED_FINDINGS_JSON VARIANT,
            COMPARISON_RESULT VARIANT,
            REVIEW_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        );
        """
        session.sql(create_table_query).collect()
        print(f"Review log table created with COMPARISON_RESULT field in {current_database}.{current_schema}")
        return True
    except Exception as e:
        print(f"Failed to create/update review log table: {e}")
        return False

def store_review_log(session, database_available, current_database, current_schema, pull_request_number, commit_sha, executive_summary, consolidated_json, processed_files, comparison_result=None):
    """Store review with VARIANT columns, comparison_result, and APPEND mode"""
    if not database_available:
        print("  Database not available - cannot store review")
        return False
    try:
        findings = consolidated_json.get("detailed_findings", [])
        insert_sql = f"""
        INSERT INTO {current_database}.{current_schema}.CODE_REVIEW_LOG
            (PULL_REQUEST_NUMBER, COMMIT_SHA, REVIEW_SUMMARY, DETAILED_FINDINGS_JSON, COMPARISON_RESULT)
            SELECT ?, ?, PARSE_JSON(?), PARSE_JSON(?), PARSE_JSON(?)
        """
        comparison_json = json.dumps(comparison_result) if comparison_result else None
        params = [
            pull_request_number,
            commit_sha,
            json.dumps(consolidated_json) if consolidated_json else None,
            json.dumps(findings) if findings else None,
            comparison_json
        ]
        session.sql(insert_sql, params=params).collect()
        print(f"  Review APPENDED successfully to {current_database}.{current_schema}.CODE_REVIEW_LOG")
        verify_query = f"""
        SELECT REVIEW_ID, PULL_REQUEST_NUMBER, COMMIT_SHA, REVIEW_TIMESTAMP
        FROM {current_database}.{current_schema}.CODE_REVIEW_LOG
        WHERE PULL_REQUEST_NUMBER = ? AND COMMIT_SHA = ?
        ORDER BY REVIEW_TIMESTAMP DESC LIMIT 1
        """
        result = session.sql(verify_query, params=[pull_request_number, commit_sha]).collect()
        if result:
            row = result[0]
            print(f"  Verified: Review ID {row['REVIEW_ID']} appended at {row['REVIEW_TIMESTAMP']}")
        else:
            print("  Warning: Could not verify review was stored")
        return True
    except Exception as e:
        print(f"  Failed to store review: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_previous_review(session, database_available, current_database, current_schema, pull_request_number, current_files_being_reviewed):
    """Get previous review with line numbers and filenames FILTERED by current files"""
    if not database_available:
        return None
    try:
        query = f"""
        SELECT REVIEW_SUMMARY, DETAILED_FINDINGS_JSON, COMPARISON_RESULT, REVIEW_TIMESTAMP
        FROM {current_database}.{current_schema}.CODE_REVIEW_LOG
        WHERE PULL_REQUEST_NUMBER = ?
        ORDER BY REVIEW_TIMESTAMP DESC LIMIT 1
        """
        result = session.sql(query, params=[pull_request_number]).collect()
        if result:
            row = result[0]
            review_summary = json.loads(str(row['REVIEW_SUMMARY'])) if row['REVIEW_SUMMARY'] else {}
            findings_json = json.loads(str(row['DETAILED_FINDINGS_JSON'])) if row['DETAILED_FINDINGS_JSON'] else []
            current_file_basenames = [os.path.basename(f) if '/' in f or '\\' in f else f for f in current_files_being_reviewed]
            print(f"  Current files being reviewed: {current_file_basenames}")
            filtered_findings = []
            for finding in findings_json:
                finding_filename = finding.get('filename', 'N/A')
                if finding_filename in current_file_basenames:
                    filtered_findings.append(finding)
                    print(f"    Including previous finding from {finding_filename}")
                else:
                    print(f"    Excluding previous finding from {finding_filename} (not in current review)")
            print(f"  Filtered findings: {len(filtered_findings)} out of {len(findings_json)} previous findings")
            if not filtered_findings:
                print("  No previous findings for currently reviewed files - treating as initial review")
                return None
            previous_context = f"""Previous Review Summary:
{json.dumps(review_summary, indent=2)[:1500]}

Previous Detailed Findings for Currently Reviewed Files:
"""
            for i, finding in enumerate(filtered_findings[:10]):
                line_num = finding.get('line_number', 'N/A')
                filename = finding.get('filename', 'N/A')
                severity = finding.get('severity', 'Unknown')
                issue = finding.get('finding', 'No description')[:100]
                previous_context += f"""
{i+1}. [{severity}] {filename}:{line_num} - {issue}
"""
            print(f"  Retrieved {len(filtered_findings)} relevant previous findings from {row['REVIEW_TIMESTAMP']}")
            return previous_context
        else:
            print("  No previous review found for this PR")
            return None
    except Exception as e:
        print(f"  Error retrieving previous review: {e}")
        import traceback
        traceback.print_exc()
        return None

def fetch_last_review_for_comparison(session, database_available, current_database, current_schema, pr_number, current_files_being_reviewed):
    """Fetches the most recent review FILTERED by current files for comparison purposes"""
    if not database_available:
        return None
    try:
        query = f"""
        SELECT REVIEW_SUMMARY, DETAILED_FINDINGS_JSON, REVIEW_TIMESTAMP
        FROM {current_database}.{current_schema}.CODE_REVIEW_LOG
        WHERE PULL_REQUEST_NUMBER = ?
        ORDER BY REVIEW_TIMESTAMP DESC LIMIT 1
        """
        result = session.sql(query, params=[pr_number]).collect()
        if result:
            row = result[0]
            findings_json = json.loads(str(row['DETAILED_FINDINGS_JSON'])) if row['DETAILED_FINDINGS_JSON'] else []
            current_file_basenames = [os.path.basename(f) if '/' in f or '\\' in f else f for f in current_files_being_reviewed]
            filtered_findings = [f for f in findings_json if f.get('filename', 'N/A') in current_file_basenames]
            if not filtered_findings:
                print("No previous findings for currently reviewed files")
                return None
            review_summary_filtered = {
                "executive_summary": json.loads(str(row['REVIEW_SUMMARY'])).get("executive_summary", "") if row['REVIEW_SUMMARY'] else "",
                "detailed_findings": filtered_findings,
                "files_reviewed": current_file_basenames
            }
            review_summary_text = json.dumps(review_summary_filtered, indent=2)
            print(f"Retrieved filtered review for comparison from {row['REVIEW_TIMESTAMP']} ({len(filtered_findings)} relevant findings)")
            return review_summary_text
        else:
            print("No previous review found for comparison")
            return None
    except Exception as e:
        print(f"Error fetching filtered review for comparison: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_llm_comparison(model: str, prompt_messages: str, session):
    """Uses an LLM to compare two reviews and returns the structured result with robust error handling"""
    print("Performing LLM comparison of reviews...")
    try:
        clean_prompt = prompt_messages.replace("\\", "\\\\").replace("'", "''")
        max_prompt_length = 95000
        if len(clean_prompt) > max_prompt_length:
            print(f"Prompt too long ({len(clean_prompt)} chars), truncating to {max_prompt_length}")
            clean_prompt = clean_prompt[:max_prompt_length] + "\n... [truncated for length]"
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{clean_prompt}') as response"
        df = session.sql(query)
        result = df.collect()[0][0]
        print(f"LLM comparison response received: {len(result)} characters")
        try:
            comparison_result = json.loads(result)
            print("LLM comparison successfully parsed as JSON (direct)")
            return comparison_result
        except json.JSONDecodeError:
            pass
        import re
        json_code_match = re.search(r'```json\s*(\{.*?\})\s*```', result, re.DOTALL)
        if json_code_match:
            try:
                comparison_result = json.loads(json_code_match.group(1))
                print("Successfully extracted JSON from code block")
                return comparison_result
            except json.JSONDecodeError:
                pass
        json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result, re.DOTALL)
        for match in sorted(json_matches, key=len, reverse=True):
            try:
                comparison_result = json.loads(match)
                print("Successfully extracted JSON using pattern matching")
                return comparison_result
            except json.JSONDecodeError:
                continue
        try:
            cleaned_json = result
            cleaned_json = re.sub(r',(\s*[}\]])', r'\1', cleaned_json)
            json_match = re.search(r'\{.*\}', cleaned_json, re.DOTALL)
            if json_match:
                comparison_result = json.loads(json_match.group())
                print("Successfully parsed cleaned JSON")
                return comparison_result
        except json.JSONDecodeError:
            pass
        print("All JSON parsing strategies failed for comparison")
        return None
    except Exception as e:
        print(f"Error calling LLM for comparison: {e}")
        import traceback
        traceback.print_exc()
        return None
