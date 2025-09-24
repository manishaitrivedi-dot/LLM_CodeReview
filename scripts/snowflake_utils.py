# snowflake_utils.py

import os, sys, json
from snowflake.snowpark import Session

# ---------------------
# Snowflake session - FIXED: Hybrid approach with fallbacks
# ---------------------
def get_snowflake_config():
    """Get Snowflake configuration with fallbacks"""
    # Try environment variables first (for dynamic repos)
    if os.getenv("SNOWFLAKE_ACCOUNT"):
        print("🔧 Using environment variable configuration")
        return {
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "role": os.getenv("SNOWFLAKE_ROLE", "SYSADMIN"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": os.getenv("SNOWFLAKE_DATABASE"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        }
    else:
        # Fallback to hardcoded values (for repos without env setup)
        print("⚠️ Environment variables not found, using fallback configuration")
        return {
            "account": "XKB93357.us-west-2",
            "user": "MANISHAT007",
            "password": "Welcome@987654321",
            "role": "SYSADMIN",
            "warehouse": "COMPUTE_WH",
            "database": "MY_DB",
            "schema": "PUBLIC",
        }

def get_snowflake_session():
    """Initialize Snowflake session with configuration"""
    cfg = get_snowflake_config()

    # Validate required fields
    required_fields = ["account", "user", "password"]
    missing_fields = [field for field in required_fields if not cfg.get(field)]
    if missing_fields:
        print(f"❌ Missing required Snowflake configuration: {missing_fields}")
        print("Please set environment variables or check hardcoded fallback values")
        sys.exit(1)

    try:
        session = Session.builder.configs(cfg).create()
        print(f"✅ Connected to Snowflake: {cfg['account']} as {cfg['user']}")
        return session, cfg
    except Exception as e:
        print(f"❌ Failed to connect to Snowflake: {e}")
        sys.exit(1)

# FIX DATABASE PERMISSIONS AND SETUP: Enhanced approach
def setup_database_with_fallback(session, cfg):
    """Setup database with multiple fallback strategies"""
    database_available = False
    current_database = None
    current_schema = None
   
    print("🔧 Setting up database for review logging...")
   
    # Use config values with safe fallbacks
    db_env = cfg.get("database") or "MY_DB"
    schema_env = cfg.get("schema") or "PUBLIC"
    role_env = cfg.get("role") or "SYSADMIN"
   
    print(f"  Attempting to use: {db_env}.{schema_env} with role {role_env}")
   
    # Strategy 1: Try specified database with specified role
    try:
        session.sql(f"USE ROLE {role_env}").collect()
        print(f"    ✓ Using role {role_env}")
        
        # Try to grant permissions (these might fail silently, which is okay)
        try:
            session.sql(f"GRANT USAGE ON DATABASE {db_env} TO ROLE {role_env}").collect()
            session.sql(f"GRANT USAGE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
            session.sql(f"GRANT CREATE TABLE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
            session.sql(f"GRANT INSERT ON ALL TABLES IN SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
            print(f"    ✓ Granted permissions (if allowed)")
        except Exception as grant_e:
            print(f"    ⚠️ Grant permissions failed (may not have GRANT privileges): {grant_e}")
        
        # Try to use the database and schema
        session.sql(f"USE DATABASE {db_env}").collect()
        session.sql(f"USE SCHEMA {schema_env}").collect()
        current_database = db_env
        current_schema = schema_env
        print(f"✅ Strategy 1: Successfully using {db_env}.{schema_env}")
        database_available = True
        return database_available, current_database, current_schema
        
    except Exception as e:
        print(f"⚠️ Strategy 1 failed: {e}")

    # Strategy 2: Create our own database as current role
    try:
        session.sql(f"USE ROLE {role_env}").collect()
        session.sql("CREATE DATABASE IF NOT EXISTS CODE_REVIEWS").collect()
        session.sql("USE DATABASE CODE_REVIEWS").collect()
        session.sql("CREATE SCHEMA IF NOT EXISTS REVIEWS").collect()
        session.sql("USE SCHEMA REVIEWS").collect()
        current_database = "CODE_REVIEWS"
        current_schema = "REVIEWS"
        print("✅ Strategy 2: Successfully created and using CODE_REVIEWS.REVIEWS")
        database_available = True
        return database_available, current_database, current_schema
    except Exception as e:
        print(f"⚠️ Strategy 2 failed: {e}")

    # Strategy 3: Try user's personal database
    try:
        session.sql(f"USE ROLE {role_env}").collect()
        user_db = f"DB_{cfg.get('user', 'USER').upper()}"
        session.sql(f"CREATE DATABASE IF NOT EXISTS {user_db}").collect()
        session.sql(f"USE DATABASE {user_db}").collect()
        session.sql("CREATE SCHEMA IF NOT EXISTS LOGS").collect()
        session.sql("USE SCHEMA LOGS").collect()
        current_database = user_db
        current_schema = "LOGS"
        print(f"✅ Strategy 3: Successfully created and using {user_db}.LOGS")
        database_available = True
        return database_available, current_database, current_schema
    except Exception as e:
        print(f"⚠️ Strategy 3 failed: {e}")

    # Strategy 4: Try with ACCOUNTADMIN role if available
    try:
        session.sql("USE ROLE ACCOUNTADMIN").collect()
        session.sql(f"CREATE DATABASE IF NOT EXISTS {db_env}").collect()
        session.sql(f"USE DATABASE {db_env}").collect()
        session.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_env}").collect()
        session.sql(f"USE SCHEMA {schema_env}").collect()
        # Grant permissions back to original role
        session.sql(f"GRANT USAGE ON DATABASE {db_env} TO ROLE {role_env}").collect()
        session.sql(f"GRANT USAGE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
        session.sql(f"GRANT CREATE TABLE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
        # Switch back to original role
        session.sql(f"USE ROLE {role_env}").collect()
        current_database = db_env
        current_schema = schema_env
        print(f"✅ Strategy 4: Successfully created {db_env}.{schema_env} with ACCOUNTADMIN")
        database_available = True
        return database_available, current_database, current_schema
    except Exception as e:
        print(f"⚠️ Strategy 4 failed: {e}")

    print("❌ All database strategies failed - continuing without logging")
    print("  This means review history and comparison features will be disabled")
    database_available = False
    return database_available, current_database, current_schema

def setup_review_log_table(session, database_available, current_database, current_schema):
    """ENHANCED: Setup the review log table with VARIANT columns and comparison_result field"""
    if not database_available:
        return False
       
    try:
        # Check if table exists and has the correct structure
        check_table_query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{current_schema}'
        AND TABLE_NAME = 'CODE_REVIEW_LOG'
        """
       
        try:
            existing_columns = session.sql(check_table_query).collect()
            column_names = [row['COLUMN_NAME'] for row in existing_columns]
           
            # Check if COMPARISON_RESULT column exists
            if 'COMPARISON_RESULT' not in column_names:
                print(f"  🔧 Adding COMPARISON_RESULT column to existing table...")
                alter_table_query = f"""
                ALTER TABLE {current_database}.{current_schema}.CODE_REVIEW_LOG
                ADD COLUMN COMPARISON_RESULT VARIANT
                """
                session.sql(alter_table_query).collect()
                print(f"✅ Added COMPARISON_RESULT column to existing table")
                return True
            else:
                print(f"✅ Review log table already has correct structure in {current_database}.{current_schema}")
                return True
               
        except Exception as check_error:
            print(f"  🔧 Table doesn't exist or error checking: {check_error}. Creating new table...")
       
        # Create table with comparison_result field
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
        print(f"✅ Review log table created with COMPARISON_RESULT field in {current_database}.{current_schema}")
        return True
       
    except Exception as e:
        print(f"❌ Failed to create/update review log table: {e}")
        return False

def store_review_log(session, database_available, current_database, current_schema, pull_request_number, commit_sha, executive_summary, consolidated_json, processed_files, comparison_result=None):
    """ENHANCED: Store review with VARIANT columns, comparison_result, and APPEND (don't overwrite)"""
    if not database_available:
        print("  ⚠️ Database not available - cannot store review")
        return False
       
    try:
        findings = consolidated_json.get("detailed_findings", [])
       
        # APPEND mode - always insert new record, don't overwrite existing ones
        insert_sql = f"""
        INSERT INTO {current_database}.{current_schema}.CODE_REVIEW_LOG
            (PULL_REQUEST_NUMBER, COMMIT_SHA, REVIEW_SUMMARY, DETAILED_FINDINGS_JSON, COMPARISON_RESULT)
            SELECT ?, ?, PARSE_JSON(?), PARSE_JSON(?), PARSE_JSON(?)
        """
       
        # Prepare comparison result for storage
        comparison_json = json.dumps(comparison_result) if comparison_result else None
       
        # 5 parameters to match the query
        params = [
            pull_request_number,
            commit_sha,
            json.dumps(consolidated_json) if consolidated_json else None,  # Store entire JSON as VARIANT
            json.dumps(findings) if findings else None,  # Store findings as VARIANT
            comparison_json  # Store comparison result as VARIANT
        ]
       
        session.sql(insert_sql, params=params).collect()
        print(f"  ✅ Review APPENDED successfully to {current_database}.{current_schema}.CODE_REVIEW_LOG")
       
        # Verify the insert worked
        verify_query = f"""
        SELECT REVIEW_ID, PULL_REQUEST_NUMBER, COMMIT_SHA, REVIEW_TIMESTAMP
        FROM {current_database}.{current_schema}.CODE_REVIEW_LOG
        WHERE PULL_REQUEST_NUMBER = {pull_request_number} AND COMMIT_SHA = '{commit_sha}'
        ORDER BY REVIEW_TIMESTAMP DESC LIMIT 1
        """
        result = session.sql(verify_query).collect()
       
        if result:
            row = result[0]
            print(f"  📋 Verified: Review ID {row['REVIEW_ID']} appended at {row['REVIEW_TIMESTAMP']}")
        else:
            print("  ⚠️ Warning: Could not verify review was stored")
           
        return True
       
    except Exception as e:
        print(f"  ❌ Failed to store review: {e}")
        import traceback
        traceback.print_exc()
        return False

# FIXED FUNCTION: Filter by current files being reviewed
def get_previous_review(session, database_available, current_database, current_schema, pull_request_number, current_files_being_reviewed):
    """
    FIXED: Get previous review with line numbers and filenames FILTERED by current files
    Only returns previous issues for files that are being reviewed in the current iteration
    """
    if not database_available:
        return None
       
    try:
        query = f"""
        SELECT
            REVIEW_SUMMARY,
            DETAILED_FINDINGS_JSON,
            COMPARISON_RESULT,
            REVIEW_TIMESTAMP
        FROM {current_database}.{current_schema}.CODE_REVIEW_LOG
        WHERE PULL_REQUEST_NUMBER = {pull_request_number}
        ORDER BY REVIEW_TIMESTAMP DESC
        LIMIT 1
        """
       
        result = session.sql(query).collect()
       
        if result:
            row = result[0]
            # Extract from VARIANT columns properly
            review_summary = json.loads(str(row['REVIEW_SUMMARY'])) if row['REVIEW_SUMMARY'] else {}
            findings_json = json.loads(str(row['DETAILED_FINDINGS_JSON'])) if row['DETAILED_FINDINGS_JSON'] else []
            
            # CRITICAL FIX: Filter findings to only include files being reviewed currently
            current_file_basenames = [os.path.basename(f) if '/' in f or '\\' in f else f for f in current_files_being_reviewed]
            print(f"  📋 Current files being reviewed: {current_file_basenames}")
            
            filtered_findings = []
            for finding in findings_json:
                finding_filename = finding.get('filename', 'N/A')
                if finding_filename in current_file_basenames:
                    filtered_findings.append(finding)
                    print(f"    ✓ Including previous finding from {finding_filename}")
                else:
                    print(f"    ✗ Excluding previous finding from {finding_filename} (not in current review)")
            
            print(f"  📊 Filtered findings: {len(filtered_findings)} out of {len(findings_json)} previous findings")
            
            # If no relevant previous findings, return None
            if not filtered_findings:
                print("  📋 No previous findings for currently reviewed files - treating as initial review")
                return None
           
            # Build detailed previous context with line numbers and filenames - ONLY for current files
            previous_context = f"""Previous Review Summary:
{json.dumps(review_summary, indent=2)[:1500]}

Previous Detailed Findings for Currently Reviewed Files:
"""
           
            # Include line numbers, filenames and detailed info for each FILTERED finding
            for i, finding in enumerate(filtered_findings[:10]):  # Limit to first 10 findings
                line_num = finding.get('line_number', 'N/A')
                filename = finding.get('filename', 'N/A')
                severity = finding.get('severity', 'Unknown')
                issue = finding.get('finding', 'No description')[:100]  # Truncate long descriptions
               
                previous_context += f"""
{i+1}. [{severity}] {filename}:{line_num} - {issue}
"""
           
            print(f"  📋 Retrieved {len(filtered_findings)} relevant previous findings from {row['REVIEW_TIMESTAMP']}")
            return previous_context
        else:
            print("  📋 No previous review found for this PR")
            return None
           
    except Exception as e:
        print(f"  ⚠️ Error retrieving previous review: {e}")
        return None

# FIXED FUNCTION: Filter by current files being reviewed
def fetch_last_review_for_comparison(session, database_available, current_database, current_schema, pr_number, current_files_being_reviewed):
    """
    FIXED: Fetches the most recent review FILTERED by current files for comparison purposes
    """
    if not database_available:
        return None
       
    try:
        query = f"""
        SELECT
            REVIEW_SUMMARY,
            DETAILED_FINDINGS_JSON,
            REVIEW_TIMESTAMP
        FROM {current_database}.{current_schema}.CODE_REVIEW_LOG
        WHERE PULL_REQUEST_NUMBER = {pr_number}
        ORDER BY REVIEW_TIMESTAMP DESC
        LIMIT 1
        """
       
        result = session.sql(query).collect()
       
        if result:
            row = result[0]
            # Extract the detailed findings and filter by current files
            findings_json = json.loads(str(row['DETAILED_FINDINGS_JSON'])) if row['DETAILED_FINDINGS_JSON'] else []
            
            # CRITICAL FIX: Filter by current files being reviewed
            current_file_basenames = [os.path.basename(f) if '/' in f or '\\' in f else f for f in current_files_being_reviewed]
            filtered_findings = [f for f in findings_json if f.get('filename', 'N/A') in current_file_basenames]
            
            if not filtered_findings:
                print("📋 No previous findings for currently reviewed files")
                return None
            
            # Build a summary that includes only relevant findings
            review_summary_filtered = {
                "executive_summary": json.loads(str(row['REVIEW_SUMMARY'])).get("executive_summary", "") if row['REVIEW_SUMMARY'] else "",
                "detailed_findings": filtered_findings,
                "files_reviewed": current_file_basenames
            }
            
            review_summary_text = json.dumps(review_summary_filtered, indent=2)
            print(f"📋 Retrieved filtered review for comparison from {row['REVIEW_TIMESTAMP']} ({len(filtered_findings)} relevant findings)")
            return review_summary_text
        else:
            print("📋 No previous review found for comparison")
            return None
           
    except Exception as e:
        print(f"❌ Error fetching filtered review for comparison: {e}")
        return None

def get_llm_comparison(model: str, prompt_messages: str, session):
    """ENHANCED: Uses an LLM to compare two reviews and returns the structured result."""
    print("🔄 Performing LLM comparison of reviews...")
    try:
        clean_prompt = prompt_messages.replace("'", "''").replace("\\", "\\\\")
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{clean_prompt}') as response"
        df = session.sql(query)
        result = df.collect()[0][0]
        
        print(f"📊 LLM comparison response received: {len(result)} characters")
       
        # Try to parse as JSON
        try:
            comparison_result = json.loads(result)
            print("✅ LLM comparison successfully parsed as JSON")
            return comparison_result
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed, attempting to extract JSON from response: {e}")
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                comparison_result = json.loads(json_match.group())
                print("✅ Successfully extracted JSON from LLM response")
                return comparison_result
            else:
                print("❌ Could not extract valid JSON from LLM response")
                return None
               
    except Exception as e:
        print(f"❌ Error calling LLM for comparison: {e}")
        return None
