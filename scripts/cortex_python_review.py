import os, sys, json, re, uuid, glob
from pathlib import Path
from snowflake.snowpark import Session
import pandas as pd
from datetime import datetime

# ---------------------
# Config
# ---------------------
MODEL = "openai-gpt-4.1"
COMPARISON_MODEL = "claude-3-5-sonnet"
MAX_CHARS_FOR_FINAL_SUMMARY_FILE = 65000
MAX_TOKENS_FOR_SUMMARY_INPUT = 100000

# Dynamic file pattern - processes all Python AND SQL files in scripts directory
SCRIPTS_DIRECTORY = "scripts"  # Base directory to scan
FILE_PATTERNS = ["*.py", "*.sql"]  # CHANGED: Added SQL files

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
except Exception as e:
    print(f"❌ Failed to connect to Snowflake: {e}")
    sys.exit(1)

# FIX DATABASE PERMISSIONS AND SETUP: Enhanced approach
database_available = False
current_database = None
current_schema = None

def setup_database_with_fallback():
    """Setup database with multiple fallback strategies"""
    global database_available, current_database, current_schema
   
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
        return True
       
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
        return True
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
        return True
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
        return True
    except Exception as e:
        print(f"⚠️ Strategy 4 failed: {e}")

    print("❌ All database strategies failed - continuing without logging")
    print("  This means review history and comparison features will be disabled")
    database_available = False
    return False

# Setup database
setup_database_with_fallback()

# ---------------------
# PROMPT TEMPLATES
# ---------------------
PROMPT_TEMPLATE_INDIVIDUAL = """Please act as a principal-level code reviewer with expertise in Python, SQL, and database security. Your review must be concise, accurate, and directly actionable, as it will be posted as a GitHub Pull Request comment.

---
# CONTEXT: HOW TO REVIEW (Apply Silently)

1.  **You are reviewing a code file for executive-level analysis.** Focus on business impact, technical debt, security risks, and maintainability.
2.  **Focus your review on the most critical aspects.** Prioritize findings that have business impact or security implications.
3.  **Infer context from the full code.** Base your review on the complete file provided.
4.  **Your entire response MUST be under 65,000 characters.** Include findings of all severities but prioritize Critical and High severity issues.

# REVIEW PRIORITIES (Strict Order)
1.  Security & Correctness (Real SQL Injection with User Input, Production Credentials)
2.  Reliability & Error-handling
3.  Performance & Complexity (Major Bottlenecks, Resource Issues)
4.  Readability & Maintainability
5.  Testability

# BALANCED SECURITY FOCUS AREAS:
**For SQL Code & Database Operations (BE REALISTIC):**
-   **CRITICAL ONLY:** Confirmed SQL injection with user input paths, production credentials exposed in code, DELETE/UPDATE without WHERE affecting entire tables, data breach risks
-   **HIGH:** Missing parameterization with potential user input exposure, significant security gaps, major performance bottlenecks affecting production
-   **MEDIUM:** Hardcoded non-production values, suboptimal queries, missing indexes, maintainability issues, code organization problems
-   **LOW:** Style inconsistencies, minor optimizations, documentation gaps, cosmetic improvements

**For Python Code (BE REALISTIC):**
-   **CRITICAL ONLY:** Confirmed code injection with user input (eval/exec with user data), production credential exposure, data corruption risks
-   **HIGH:** Significant error handling gaps, major security concerns, subprocess vulnerabilities with user input
-   **MEDIUM:** Code quality improvements, minor security concerns, maintainability issues, missing error handling
-   **LOW:** Style improvements, minor optimizations, documentation gaps, cosmetic issues

# REALISTIC SEVERITY GUIDELINES (MANDATORY - MOST ISSUES ARE NOT CRITICAL):
-   **Critical:** 0-2% of findings (extremely rare - only for confirmed security vulnerabilities with user input or production credential exposure)
-   **High:** 5-15% of findings (significant but fixable issues)
-   **Medium:** 50-60% of findings (most common - code quality and maintainability)
-   **Low:** 25-40% of findings (style and minor improvements)

# COMMON SQL PATTERNS THAT ARE **NOT CRITICAL**:
- Hardcoded database/schema names: **Medium** (maintainability issue)
- Missing comments: **Low** (documentation)
- Suboptimal JOIN patterns: **Medium** (performance)
- Missing indexes (without proof of performance impact): **Medium**
- Static SQL without user input: **Medium at most** (not critical)
- Development/test connection strings: **Medium** (not critical unless production)

# ELIGIBILITY CRITERIA FOR FINDINGS (ALL must be met)
-   **Evidence:** Quote the exact code snippet and cite the line number.
-   **Severity:** Assign {Low | Medium | High | Critical} - BE VERY CONSERVATIVE. Only use Critical for confirmed security vulnerabilities.
-   **Impact & Action:** Briefly explain the issue and provide a minimal, safe correction.
-   **Non-trivial:** Skip purely stylistic nits (e.g., import order, line length) that a linter would catch.

# HARD CONSTRAINTS (For accuracy & anti-hallucination)
-   Do NOT propose APIs that don't exist for the imported modules.
-   Treat parameters like `db_path` as correct dependency injection; do NOT call them hardcoded.
-   NEVER suggest logging sensitive user data or internal paths. Suggest non-reversible fingerprints if context is needed.
-   Do NOT recommend removing correct type hints or docstrings.
-   If code in the file is already correct and idiomatic, do NOT invent problems.
-   DO NOT inflate severity levels - be very conservative. Most findings should be Medium or Low.
-   **For SQL files:** Only mark Critical if there's confirmed SQL injection with user input. Hardcoded values are usually Medium.
-   **For Python files with SQL:** Only mark Critical if there's confirmed injection vulnerability with user data.

---
# OUTPUT FORMAT (Strict, professional, audit-ready)

Your entire response MUST be under 65,000 characters. Include findings of all severity levels with REALISTIC severity assignments.

## Code Review Summary
*A 2-3 sentence high-level summary. Mention the key strengths and the most critical areas for improvement, being realistic about severity.*

---
### Detailed Findings
*A list of all material findings. If no significant issues are found, state "No significant issues found."*

**File:** {filename}
-   **Severity:** {Critical | High | Medium | Low}
-   **Line:** {line_number}
-   **Function/Context:** `{function_name_if_applicable}`
-   **Finding:** {A clear, concise description of the issue, its impact, and a recommended correction. Be realistic about severity - most issues are Medium or Low.}

**(Repeat for each finding)**

---
### Key Recommendations
*Provide 2-3 high-level, actionable recommendations for improving the overall quality of the codebase based on the findings. Focus on the most impactful improvements.*

---
# CODE TO REVIEW

{PY_CONTENT}
"""

PROMPT_TEMPLATE_CONSOLIDATED = """
You are an expert code review summarization engine for executive-level reporting. Your task is to analyze individual code reviews and generate a single, consolidated executive summary with business impact focus.

You MUST respond ONLY with a valid JSON object that conforms to the executive schema. Do not include any other text, explanations, or markdown formatting outside of the JSON structure.

Follow these instructions to populate the JSON fields:

1.  **`executive_summary` (string):** Write a 2-3 sentence high-level summary of the entire code change, covering the most important findings across all files with business impact focus.
2.  **`quality_score` (number):** Assign an overall quality score (0-100) based on severity and number of findings.
3.  **`business_impact` (string):** Assess overall business risk as "LOW", "MEDIUM", or "HIGH".
4.  **`technical_debt_score` (string):** Evaluate technical debt as "LOW", "MEDIUM", or "HIGH".
5.  **`security_risk_level` (string):** Determine security risk as "LOW", "MEDIUM", "HIGH", or "CRITICAL". Only use CRITICAL for confirmed SQL injection or production credential exposure.
6.  **`maintainability_rating` (string):** Rate maintainability as "POOR", "FAIR", "GOOD", or "EXCELLENT".
7.  **`detailed_findings` (array of objects):** Create an array of objects, where each object represents a single, distinct issue found in the code:
         -   **`severity`**: Assign severity VERY CONSERVATIVELY: "Low", "Medium", "High", or "Critical". CRITICAL should be 0-2% of all findings (only for confirmed security vulnerabilities with user input or production credential exposure). HIGH should be 5-15%. MEDIUM should be 50-60% (most common). LOW should be 25-40%.
         -   **`category`**: Assign category: "Security", "Performance", "Maintainability", "Best Practices", "Documentation", or "Error Handling".
         -   **`line_number`**: Extract the specific line number if mentioned in the review. If no line number is available, use "N/A".
         -   **`function_context`**: From the review text, identify the function or class name where the issue is located. If not applicable, use "global scope".
         -   **`finding`**: Write a clear, concise description of the issue, its potential impact, and a concrete recommendation.
         -   **`business_impact`**: Explain how this affects business operations or risk. Be realistic - most issues have low to medium business impact.
         -   **`recommendation`**: Provide specific technical solution.
         -   **`effort_estimate`**: Estimate effort as "LOW", "MEDIUM", or "HIGH".
         -   **`priority_ranking`**: Assign priority ranking (1 = highest priority).
         -   **`filename`**: The name of the file where the issue was found.
8.  **`metrics` (object):** Include technical metrics:
         -   **`lines_of_code`**: Total number of lines analyzed across all files.
         -   **`complexity_score`**: "LOW", "MEDIUM", or "HIGH".
         -   **`code_coverage_gaps`**: Array of areas needing test coverage.
         -   **`dependency_risks`**: Array of dependency-related risks.
9.  **`strategic_recommendations` (array of strings):** Provide 2-3 high-level, actionable recommendations for technical leadership.
10. **`immediate_actions` (array of strings):** List critical items requiring immediate attention. Should be very few items.
11. **`previous_issues_resolved` (array of objects):** For each issue from previous review, indicate status:
         -   **`original_issue`**: Brief description of the previous issue
         -   **`line_number`**: Line number from the previous issue (if available)
         -   **`filename`**: Filename from the previous issue (if available)
         -   **`status`**: "RESOLVED", "PARTIALLY_RESOLVED", "NOT_ADDRESSED", or "WORSENED"
         -   **`details`**: Explanation of current status

**CRITICAL INSTRUCTION FOR REALISTIC REVIEWS:**
Your entire response MUST be under {MAX_CHARS_FOR_FINAL_SUMMARY_FILE} characters. Include findings of all severity levels with VERY CONSERVATIVE severity assignments:
-   Use "Critical" ONLY for confirmed SQL injection with user input, production credential exposure, or confirmed data breach risks (0-2% of findings)
-   Use "High" for significant security concerns, major performance issues, or significant error handling gaps (5-15% of findings)
-   Use "Medium" for code quality issues, maintainability concerns, minor performance issues, hardcoded non-production values (50-60% of findings - MOST COMMON)
-   Use "Low" for style improvements, minor optimizations, documentation gaps, cosmetic issues (25-40% of findings)

**IMPORTANT SQL GUIDANCE:**
- Hardcoded database names/schemas: Medium (maintainability issue, not security)
- Missing comments in SQL: Low (documentation)
- Suboptimal queries without performance proof: Medium
- Static SQL without user input: Medium at most
- Only mark SQL issues as Critical if there's confirmed injection with user input

Here are the individual code reviews to process:
{ALL_REVIEWS_CONTENT}
"""

PROMPT_TEMPLATE_WITH_CONTEXT = """
You are reviewing subsequent commits for Pull Request #{pr_number}.

PREVIOUS REVIEW SUMMARY AND FINDINGS:
{previous_context}

CRITICAL INSTRUCTION: You must analyze the new code changes with full awareness of the previous feedback. Specifically:
1. Check if previous Critical/High severity issues were addressed in the new code
2. Identify if any previous recommendations were implemented
3. Note any new issues that may have been introduced
4. Maintain continuity with previous review comments
5. In the "previous_issues_resolved" section, provide specific status for each previous issue INCLUDING LINE NUMBERS AND FILENAMES

{consolidated_template}
"""

# LLM COMPARISON PROMPT TEMPLATE - ENHANCED VERSION FROM SECOND CODE
PROMPT_TO_COMPARE_REVIEWS = """You are an expert AI code review assistant. Your task is to compare a previous code review with a new code review for the same pull request. The developer has pushed new code, attempting to fix the issues mentioned in the previous review.

Analyze if the feedback in the **[NEW REVIEW]** suggests that the specific issues raised in the **[PREVIOUS REVIEW]** have been addressed. Do not just look for the exact same text. Understand the underlying problem described in the previous review and see if the new review sounds positive, different, or no longer mentions that specific problem.

**[PREVIOUS REVIEW]:**
'''
{previous_review_text}
'''

**[NEW REVIEW]:**
'''
{new_review_text}
'''

CRITICAL INSTRUCTION: You must analyze the new code changes with full awareness of the previous feedback. Specifically:
1. Check if previous Critical/High severity issues were addressed in the new code
2. Identify if any previous recommendations were implemented
3. Note any new issues that may have been introduced
4. Maintain continuity with previous review comments
5. In the "previous_issues_resolved" section, provide specific status for each previous issue INCLUDING FILENAMES

**[YOUR TASK]:**
Provide your analysis in a structured JSON format. For each major issue identified in the **[PREVIOUS REVIEW]**, determine its status based on the **[NEW REVIEW]**. The possible statuses are:

- **"RESOLVED"**: The issue is no longer mentioned in the new review, or the new review provides positive feedback on that area.
- **"PARTIALLY_RESOLVED"**: The new review indicates some improvement but mentions that the issue is not fully fixed.
- **"NOT_ADDRESSED"**: The new review repeats the same criticism or feedback.
- **"WORSENED"**: Despite attempting to fix the issue, some new errors were added to the code, which made it worse.
- **"NO_LONGER_APPLICABLE"**: The code related to the original feedback was removed or changed so significantly that the feedback doesn't apply.

The JSON output should follow this exact structure:
{
  "comparison_summary": "A brief, one-sentence summary of whether the developer addressed the feedback.",
  "issue_status": [
    {
      "issue": "A concise summary of the original issue from the previous review.",
      "line_number": "Line number from the original issue if available, otherwise 'N/A'",
      "filename": "Filename from the original issue if available, otherwise 'N/A'",
      "status": "RESOLVED | PARTIALLY_RESOLVED | NOT_ADDRESSED | WORSENED | NO_LONGER_APPLICABLE",
      "reasoning": "A brief explanation for your status decision, referencing the new review."
    }
  ],
  "new_issues_introduced": [
    {
      "issue": "Description of any new issues found in the new review that weren't in the previous review",
      "severity": "Critical | High | Medium | Low",
      "line_number": "Line number if available",
      "filename": "Filename if available"
    }
  ],
  "overall_improvement": "IMPROVED | NEUTRAL | WORSENED",
  "quality_trend": "Quality score trend analysis comparing previous vs current review"
}

STRICTLY provide the result within 3000 characters. DO NOT exceed the character limit.
"""

def get_changed_python_files(folder_path=None):
    """
    Dynamically get all Python AND SQL files from the specified folder or scripts directory.
    Uses wildcard pattern matching for flexibility.
    """
    # If no folder specified, use the scripts directory
    if not folder_path:
        folder_path = SCRIPTS_DIRECTORY
       
    if not os.path.exists(folder_path):
        print(f"❌ Directory {folder_path} not found")
        return []
   
    all_files = []
   
    # Process both Python and SQL files
    for pattern in FILE_PATTERNS:
        # Use glob pattern to find files
        pattern_path = os.path.join(folder_path, pattern)
        found_files = glob.glob(pattern_path)
       
        # Also check subdirectories recursively
        recursive_pattern = os.path.join(folder_path, "**", pattern)
        found_files.extend(glob.glob(recursive_pattern, recursive=True))
       
        all_files.extend(found_files)
   
    # Remove duplicates and sort
    all_files = sorted(list(set(all_files)))
   
    print(f"📁 Found {len(all_files)} code files in {folder_path} using patterns {FILE_PATTERNS}:")
    for file in all_files:
        file_type = "SQL" if file.lower().endswith('.sql') else "Python"
        print(f"  - {file} ({file_type})")
   
    return all_files

def build_prompt_for_individual_review(code_text: str, filename: str = "code_file") -> str:
    prompt = PROMPT_TEMPLATE_INDIVIDUAL.replace("{PY_CONTENT}", code_text)
    prompt = prompt.replace("{filename}", filename)
    return prompt

def build_prompt_for_consolidated_summary(all_reviews_content: str, previous_context: str = None, pr_number: int = None) -> str:
    if previous_context and pr_number:
        prompt = PROMPT_TEMPLATE_WITH_CONTEXT.replace("{previous_context}", previous_context)
        prompt = prompt.replace("{pr_number}", str(pr_number))
        prompt = prompt.replace("{consolidated_template}", PROMPT_TEMPLATE_CONSOLIDATED)
        prompt = prompt.replace("{ALL_REVIEWS_CONTENT}", all_reviews_content)
    else:
        prompt = PROMPT_TEMPLATE_CONSOLIDATED.replace("{ALL_REVIEWS_CONTENT}", all_reviews_content)
    return prompt

def review_with_cortex(model, prompt_text: str, session) -> str:
    try:
        clean_prompt = prompt_text.replace("'", "''").replace("\\", "\\\\")
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{clean_prompt}') as response"
        df = session.sql(query)
        result = df.collect()[0][0]
        return result
    except Exception as e:
        print(f"Error calling Cortex complete for model '{model}': {e}", file=sys.stderr)
        return f"ERROR: Could not get response from Cortex. Reason: {e}"

def chunk_large_file(code_text: str, max_chunk_size: int = 50000) -> list:
    if len(code_text) <= max_chunk_size:
        return [code_text]
   
    lines = code_text.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0
   
    for line in lines:
        line_size = len(line) + 1
        if current_size + line_size > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size
   
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
   
    return chunks

def calculate_executive_quality_score(findings: list, total_lines_of_code: int) -> int:
    """
    Executive-level rule-based quality scoring (0-100).
    MUCH MORE BALANCED - Fixed overly harsh scoring.
   
    Scoring Logic (REALISTIC):
    - Start with base score of 100
    - Reasonable deductions that won't hit zero easily
    - Focus on actionable scoring for executives
    """
    if not findings or len(findings) == 0:
        return 100
   
    base_score = 100
    total_deductions = 0
   
    # MUCH MORE BALANCED severity weightings
    severity_weights = {
        "Critical": 12,    # Each critical issue deducts 12 points (but there should be very few)
        "High": 4,         # Each high issue deducts 4 points
        "Medium": 1.5,     # Each medium issue deducts 1.5 points
        "Low": 0.3         # Each low issue deducts 0.3 points
    }
   
    # Count issues by severity - STRICT PRECISION (NO CONVERSION)
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    total_affected_lines = 0
   
    print(f"  📊 Scoring {len(findings)} findings...")
   
    for finding in findings:
        severity = str(finding.get("severity", "")).strip()  # Keep original case
       
        # STRICT MATCHING - NO CONVERSION TO MEDIUM
        if severity == "Critical":
            severity_counts["Critical"] += 1
        elif severity == "High":
            severity_counts["High"] += 1
        elif severity == "Medium":
            severity_counts["Medium"] += 1
        elif severity == "Low":
            severity_counts["Low"] += 1
        else:
            # LOG UNRECOGNIZED SEVERITY BUT DON'T COUNT IT
            print(f"    ⚠️ UNRECOGNIZED SEVERITY: '{severity}' in finding: {finding.get('finding', 'Unknown')[:50]}... - SKIPPING")
            continue  # Skip this finding entirely instead of converting
           
        print(f"    - {severity}: {finding.get('finding', 'No description')[:50]}...")
       
        # Count affected lines (treat N/A as 1 line)
        line_num = finding.get("line_number", "N/A")
        total_affected_lines += 1
   
    print(f"  📈 Severity breakdown: Critical={severity_counts['Critical']}, High={severity_counts['High']}, Medium={severity_counts['Medium']}, Low={severity_counts['Low']}")
   
    # Calculate REALISTIC deductions from severity
    for severity, count in severity_counts.items():
        if count > 0:
            weight = severity_weights[severity]
           
            # MUCH MORE BALANCED progressive penalty
            if severity == "Critical":
                # Critical: Should be very rare, but high impact
                if count <= 2:
                    deduction = weight * count
                else:
                    deduction = weight * 2 + (count - 2) * (weight + 3)
                # Cap critical deductions at 30 points max
                deduction = min(30, deduction)
            elif severity == "High":
                # High: Linear scaling with small bonus after 10 issues
                if count <= 10:
                    deduction = weight * count
                else:
                    deduction = weight * 10 + (count - 10) * (weight + 1)
                # Cap high severity deductions at 25 points max
                deduction = min(25, deduction)
            else:
                # Medium/Low: Pure linear scaling with caps
                deduction = weight * count
                # Reasonable caps
                if severity == "Medium":
                    deduction = min(20, deduction)
                else:
                    deduction = min(10, deduction)
               
            total_deductions += deduction
            print(f"    {severity}: {count} issues = -{deduction:.1f} points (capped)")
   
    # MUCH REDUCED penalties
    if total_lines_of_code > 0:
        affected_ratio = total_affected_lines / total_lines_of_code
        if affected_ratio > 0.4:  # Only penalize if more than 40% affected
            coverage_penalty = min(5, int(affected_ratio * 20))  # Max 5 point penalty
            total_deductions += coverage_penalty
            print(f"    Coverage penalty: -{coverage_penalty} points ({affected_ratio:.1%} affected)")
   
    # REALISTIC critical threshold penalties (should rarely trigger)
    if severity_counts["Critical"] >= 3:  # Very high threshold
        total_deductions += 10
        print(f"    Executive threshold penalty: -10 points (3+ critical issues)")
   
    if severity_counts["Critical"] + severity_counts["High"] >= 20:  # High threshold
        total_deductions += 5
        print(f"    Production readiness penalty: -5 points (20+ critical/high issues)")
   
    # Calculate final score
    final_score = max(0, base_score - int(total_deductions))
   
    print(f"  🎯 Final calculation: {base_score} - {int(total_deductions)} = {final_score}")
   
    # ADJUSTED executive score bands for more realistic scoring
    if final_score >= 85:
        return min(100, final_score)  # Excellent
    elif final_score >= 70:
        return final_score  # Good
    elif final_score >= 50:
        return final_score  # Fair - needs attention
    else:
        return max(30, final_score)  # Poor - but never below 30 for functional code

def setup_review_log_table():
    """ENHANCED: Setup the review log table with VARIANT columns and comparison_result field"""
    global database_available
   
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

def store_review_log(pull_request_number, commit_sha, executive_summary, consolidated_json, processed_files, comparison_result=None):
    """ENHANCED: Store review with VARIANT columns, comparison_result, and APPEND (don't overwrite)"""
    global database_available
   
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

def get_previous_review(pull_request_number):
    """ENHANCED: Get previous review with line numbers and filenames from detailed findings"""
    global database_available
   
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
           
            # Build detailed previous context with line numbers and filenames
            previous_context = f"""Previous Review Summary:
{json.dumps(review_summary, indent=2)[:1500]}

Previous Detailed Findings with Line Numbers and Filenames:
"""
           
            # Include line numbers, filenames and detailed info for each finding
            for i, finding in enumerate(findings_json[:10]):  # Limit to first 10 findings
                line_num = finding.get('line_number', 'N/A')
                filename = finding.get('filename', 'N/A')  # ENHANCED: Include filename
                severity = finding.get('severity', 'Unknown')
                issue = finding.get('finding', 'No description')[:100]  # Truncate long descriptions
               
                previous_context += f"""
{i+1}. [{severity}] {filename}:{line_num} - {issue}
"""
           
            print(f"  📋 Retrieved previous review from {row['REVIEW_TIMESTAMP']} with line numbers and filenames")
            return previous_context
        else:
            print("  📋 No previous review found for this PR")
            return None
           
    except Exception as e:
        print(f"  ⚠️ Error retrieving previous review: {e}")
        return None

def get_llm_comparison(model: str, prompt_messages: str, session):
    """ENHANCED: Uses an LLM to compare two reviews and returns the structured result."""
    print("🔄 Performing LLM comparison of reviews...")
    try:
        review = review_with_cortex(model, prompt_messages, session)
        print(f"📊 LLM comparison response received: {len(review)} characters")
       
        # Try to parse as JSON
        try:
            comparison_result = json.loads(review)
            print("✅ LLM comparison successfully parsed as JSON")
            return comparison_result
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed, attempting to extract JSON from response: {e}")
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', review, re.DOTALL)
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

def fetch_last_review_for_comparison(session, pr_number):
    """Fetches the most recent review for a given PR number for comparison purposes"""
    global database_available
   
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
            # Extract the review summary as string for comparison
            review_summary = str(row['REVIEW_SUMMARY']) if row['REVIEW_SUMMARY'] else None
            print(f"📋 Retrieved last review for comparison from {row['REVIEW_TIMESTAMP']}")
            return review_summary
        else:
            print("📋 No previous review found for comparison")
            return None
           
    except Exception as e:
        print(f"❌ Error fetching last review for comparison: {e}")
        return None

def format_executive_pr_display(json_response: dict, processed_files: list) -> str:
    summary = json_response.get("executive_summary", "Technical analysis completed")
    findings = json_response.get("detailed_findings", [])
    quality_score = json_response.get("quality_score", 75)
    business_impact = json_response.get("business_impact", "MEDIUM")
    security_risk = json_response.get("security_risk_level", "MEDIUM")
    tech_debt = json_response.get("technical_debt_score", "MEDIUM")
    maintainability = json_response.get("maintainability_rating", "FAIR")
    metrics = json_response.get("metrics", {})
    strategic_recs = json_response.get("strategic_recommendations", [])
    immediate_actions = json_response.get("immediate_actions", [])
    previous_issues = json_response.get("previous_issues_resolved", [])
   
    critical_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "CRITICAL")
    high_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "HIGH")
    medium_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "MEDIUM")
    low_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "LOW")
   
    # Count by file type for better reporting
    python_files = [f for f in processed_files if f.lower().endswith('.py')]
    sql_files = [f for f in processed_files if f.lower().endswith('.sql')]
   
    # Count critical/high issues by file type
    python_critical = sum(1 for f in findings if f.get("filename", "").lower().endswith('.py') and str(f.get("severity", "")).upper() == "CRITICAL")
    python_high = sum(1 for f in findings if f.get("filename", "").lower().endswith('.py') and str(f.get("severity", "")).upper() == "HIGH")
    sql_critical = sum(1 for f in findings if f.get("filename", "").lower().endswith('.sql') and str(f.get("severity", "")).upper() == "CRITICAL")
    sql_high = sum(1 for f in findings if f.get("filename", "").lower().endswith('.sql') and str(f.get("severity", "")).upper() == "HIGH")
   
    risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
    quality_emoji = "🟢" if quality_score >= 80 else ("🟡" if quality_score >= 60 else "🔴")
   
    # FIXED: Executive Summary - No truncation, just ensure minimum 30 characters
    if len(summary) < 30:
        summary = summary + " Code review analysis completed."
   
    display_text = f"""# 📊 Executive Code Review Report

**Files Analyzed:** {len(processed_files)} files | **Analysis Date:** {datetime.now().strftime('%Y-%m-%d')} | **Database:** {current_database}.{current_schema}

## 🎯 Executive Summary
{summary}

## 📈 Quality Dashboard

| Metric | Score | Status | Business Impact |
|--------|-------|--------|-----------------|
| **Overall Quality** | {quality_score}/100 | {quality_emoji} | {business_impact} Risk |
| **Security Risk** | {security_risk} | {risk_emoji.get(security_risk, "🟡")} | Critical security concerns |
| **Technical Debt** | {tech_debt} | {risk_emoji.get(tech_debt, "🟡")} | {len(findings)} items |
| **Maintainability** | {maintainability} | {risk_emoji.get(maintainability, "🟡")} | Long-term sustainability |

## 🔍 Issue Distribution

| Severity | Count | Priority Actions |
|----------|-------|------------------|
| 🔴 Critical | {critical_count} | Immediate fix required |
| 🟠 High | {high_count} | Fix within sprint |
| 🟡 Medium | {medium_count} | Plan for next release |
| 🟢 Low | {low_count} | Technical improvement |

## 📁 File Analysis Breakdown

| File Type | Count | Critical Issues | High Issues |
|-----------|-------|----------------|-------------|
| 🐍 Python | {len(python_files)} | {python_critical} | {python_high} |
| 🗄️ SQL | {len(sql_files)} | {sql_critical} | {sql_high} |

"""

    # ENHANCED: Previous issues resolution status WITH LINE NUMBERS AND FILENAMES
    if previous_issues:
        display_text += """<details>
<summary><strong>📈 Previous Issues Resolution Status</strong> (Click to expand)</summary>

| Previous Issue | File | Line | Status | Details |
|----------------|------|------|--------|---------|
"""
        for issue in previous_issues:
            status = issue.get("status", "UNKNOWN")
            status_emoji = {"RESOLVED": "✅", "PARTIALLY_RESOLVED": "⚠️", "NOT_ADDRESSED": "❌", "WORSENED": "🔴"}.get(status, "❓")
           
            original_display = issue.get("original_issue", "")
            filename = issue.get("filename", "N/A")  # ENHANCED: Include filename
            line_number = issue.get("line_number", "N/A")
            details_display = issue.get("details", "")
           
            display_text += f"| {original_display} | {filename} | {line_number} | {status_emoji} {status} | {details_display} |\n"
       
        display_text += "\n</details>\n\n"

    # FILTER OUT LOW PRIORITY ISSUES from Current Review Findings
    non_low_findings = [f for f in findings if str(f.get("severity", "")).upper() != "LOW"]
   
    if non_low_findings:
        display_text += """<details>
<summary><strong>🔍 Current Review Findings</strong> (Click to expand)</summary>

| Priority | File | Line | Issue | Business Impact |
|----------|------|------|-------|-----------------|
"""
       
        severity_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        sorted_findings = sorted(non_low_findings, key=lambda x: severity_order.get(str(x.get("severity", "Low")), 4))
       
        for finding in sorted_findings[:20]:  # Show top 20 non-low findings
            severity = str(finding.get("severity", "Medium"))
            filename = finding.get("filename", "N/A")
            line = finding.get("line_number", "N/A")
           
            issue_display = str(finding.get("finding", ""))
            business_impact_display = str(finding.get("business_impact", ""))
           
            priority_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(severity, "🟡")
           
            display_text += f"| {priority_emoji} {severity} | {filename} | {line} | {issue_display} | {business_impact_display} |\n"
       
        display_text += "\n</details>\n\n"

    if immediate_actions:
        display_text += """<details>
<summary><strong>⚡ Immediate Actions Required</strong> (Click to expand)</summary>

"""
        for i, action in enumerate(immediate_actions, 1):
            display_text += f"{i}. {action}\n"
        display_text += "\n</details>\n\n"

    display_text += f"""---

**📋 Review Summary:** {len(findings)} findings identified | **🎯 Quality Score:** {quality_score}/100 | **⚡ Critical Issues:** {critical_count}

*🔬 Powered by Snowflake Cortex AI • Two-Stage Executive Analysis • Stored in {current_database}.{current_schema}*"""

    return display_text

def main():
    print(f"🚀 Starting Cortex Code Review System")
    print(f"📋 Configuration: {cfg['account']} | User: {cfg['user']} | Database: {cfg.get('database', 'N/A')}")
   
    if len(sys.argv) >= 5:
        output_folder_path = sys.argv[2]  # Keep output folder from args
        try:
            pull_request_number = int(sys.argv[3]) if sys.argv[3] and sys.argv[3].strip() else None
        except (ValueError, IndexError):
            print(f"⚠️  Warning: Invalid or empty PR number '{sys.argv[3] if len(sys.argv) > 3 else 'None'}', using None")
            pull_request_number = None
        commit_sha = sys.argv[4]
        directory_mode = True
       
        # ALWAYS use scripts directory regardless of first argument
        print(f"📁 Command line mode: Using {SCRIPTS_DIRECTORY} directory instead of '{sys.argv[1]}'")
        code_files = get_changed_python_files(SCRIPTS_DIRECTORY)
        if not code_files:
            print(f"❌ No Python/SQL files found in {SCRIPTS_DIRECTORY} directory using patterns {FILE_PATTERNS}")
            return
           
        folder_path = SCRIPTS_DIRECTORY  # Always use scripts directory
           
    else:
        # Fallback for single file mode - use scripts directory with wildcard pattern
        code_files = get_changed_python_files(SCRIPTS_DIRECTORY)
        if not code_files:
            print(f"❌ No Python/SQL files found in {SCRIPTS_DIRECTORY} directory using patterns {FILE_PATTERNS}")
            return
           
        folder_path = SCRIPTS_DIRECTORY
        output_folder_path = "output_reviews"
        pull_request_number = 0
        commit_sha = "test"
        directory_mode = False
        print(f"Running in dynamic pattern mode with {len(code_files)} code files from {SCRIPTS_DIRECTORY}")

    if os.path.exists(output_folder_path):
        import shutil
        shutil.rmtree(output_folder_path)
    os.makedirs(output_folder_path, exist_ok=True)

    all_individual_reviews = []
    processed_files = []

    print("\n🔍 STAGE 1: Individual File Analysis...")
    print("=" * 60)
   
    for file_path in code_files:
        filename = os.path.basename(file_path)
        print(f"\n--- Reviewing file: {filename} ---")
        processed_files.append(filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            if not code_content.strip():
                review_text = "No code found in file, skipping review."
            else:
                chunks = chunk_large_file(code_content)
                print(f"  File split into {len(chunks)} chunk(s)")
               
                chunk_reviews = []
                for i, chunk in enumerate(chunks):
                    chunk_name = f"{filename}_chunk_{i+1}" if len(chunks) > 1 else filename
                    print(f"  Processing chunk: {chunk_name}")
                   
                    individual_prompt = build_prompt_for_individual_review(chunk, chunk_name)
                    review_text = review_with_cortex(MODEL, individual_prompt, session)
                    chunk_reviews.append(review_text)
               
                if len(chunk_reviews) > 1:
                    review_text = "\n\n".join([f"## Chunk {i+1}\n{review}" for i, review in enumerate(chunk_reviews)])
                else:
                    review_text = chunk_reviews[0]

            all_individual_reviews.append({
                "filename": filename,
                "review_feedback": review_text
            })

            output_filename = f"{Path(filename).stem}_individual_review.md"
            output_file_path = os.path.join(output_folder_path, output_filename)
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(review_text)
            print(f"  ✅ Individual review saved: {output_filename}")

        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
            all_individual_reviews.append({
                "filename": filename,
                "review_feedback": f"ERROR: Could not generate review. Reason: {e}"
            })

    print(f"\n🔄 STAGE 2: Executive Consolidation...")
    print("=" * 60)
    print(f"Consolidating {len(all_individual_reviews)} individual reviews...")

    if not all_individual_reviews:
        print("❌ No reviews to consolidate")
        return

    try:
        # Setup the review log table with comparison_result field
        if database_available:
            setup_review_log_table()

        # Get previous review context if available
        previous_review_context = None
        if pull_request_number and pull_request_number != 0 and database_available:
            previous_review_context = get_previous_review(pull_request_number)
            if previous_review_context:
                print("  📋 This is a subsequent commit review with previous context")
            else:
                print("  📋 This is the initial commit review")
        elif not database_available:
            print("  ⚠️ Database not available - cannot retrieve previous reviews")

        combined_reviews_json = json.dumps(all_individual_reviews, indent=2)
        print(f"  Combined reviews: {len(combined_reviews_json)} characters")

        # Generate consolidation prompt with or without previous context
        consolidation_prompt = build_prompt_for_consolidated_summary(
            combined_reviews_json,
            previous_review_context,
            pull_request_number
        )
        consolidation_prompt = consolidation_prompt.replace("{MAX_CHARS_FOR_FINAL_SUMMARY_FILE}", str(MAX_CHARS_FOR_FINAL_SUMMARY_FILE))
        consolidated_raw = review_with_cortex(MODEL, consolidation_prompt, session)
       
        try:
            consolidated_json = json.loads(consolidated_raw)
            print("  ✅ Successfully parsed consolidated JSON response")
           
        except json.JSONDecodeError as e:
            print(f"  ⚠️ JSON parsing failed: {e}")
            print(f"  📝 Raw response preview: {consolidated_raw[:500]}...")
           
            # ENHANCED: Multiple JSON extraction strategies
            consolidated_json = None
           
            # Strategy 1: Find JSON between ```json and ```
            json_code_match = re.search(r'```json\s*(\{.*?\})\s*```', consolidated_raw, re.DOTALL)
            if json_code_match:
                try:
                    consolidated_json = json.loads(json_code_match.group(1))
                    print("  ✅ Successfully extracted JSON from code block")
                except json.JSONDecodeError:
                    pass
           
            # Strategy 2: Find largest JSON-like structure
            if not consolidated_json:
                json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', consolidated_raw, re.DOTALL)
                for match in sorted(json_matches, key=len, reverse=True):
                    try:
                        consolidated_json = json.loads(match)
                        print("  ✅ Successfully extracted JSON using pattern matching")
                        break
                    except json.JSONDecodeError:
                        continue
           
            # Strategy 3: Clean and fix common JSON issues
            if not consolidated_json:
                try:
                    # Common fixes for malformed JSON
                    cleaned_json = consolidated_raw
                    # Fix trailing commas
                    cleaned_json = re.sub(r',(\s*[}\]])', r'\1', cleaned_json)
                    # Fix unquoted keys (basic cases)
                    cleaned_json = re.sub(r'(\w+):', r'"\1":', cleaned_json)
                    # Extract first complete JSON object
                    json_match = re.search(r'\{.*\}', cleaned_json, re.DOTALL)
                    if json_match:
                        consolidated_json = json.loads(json_match.group())
                        print("  ✅ Successfully parsed cleaned JSON")
                except json.JSONDecodeError:
                    pass
           
            # Strategy 4: Fallback with basic structure
            if not consolidated_json:
                print("  ❌ All JSON parsing strategies failed, using fallback")
                consolidated_json = {
                    "executive_summary": "JSON parsing failed - analysis completed with " + str(len(all_individual_reviews)) + " files reviewed",
                    "quality_score": 75,
                    "business_impact": "MEDIUM",
                    "technical_debt_score": "MEDIUM",
                    "security_risk_level": "MEDIUM",
                    "maintainability_rating": "FAIR",
                    "detailed_findings": [],
                    "metrics": {"lines_of_code": 0, "complexity_score": "MEDIUM", "code_coverage_gaps": [], "dependency_risks": []},
                    "strategic_recommendations": ["Review LLM output formatting", "Implement JSON validation"],
                    "immediate_actions": ["Fix JSON parsing issues"],
                    "previous_issues_resolved": []
                }
       
        # ALWAYS calculate rule-based quality score
        findings = consolidated_json.get("detailed_findings", [])
        total_lines = sum(len(review.get("review_feedback", "").split('\n')) for review in all_individual_reviews)
       
        rule_based_score = calculate_executive_quality_score(findings, total_lines)
        consolidated_json["quality_score"] = rule_based_score
       
        print(f"  🎯 Rule-based quality score calculated: {rule_based_score}/100 (overriding LLM score)")

        executive_summary = format_executive_pr_display(consolidated_json, processed_files)
       
        consolidated_path = os.path.join(output_folder_path, "consolidated_executive_summary.md")
        with open(consolidated_path, 'w', encoding='utf-8') as f:
            f.write(executive_summary)
        print(f"  ✅ Executive summary saved: consolidated_executive_summary.md")

        json_path = os.path.join(output_folder_path, "consolidated_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(consolidated_json, f, indent=2)

        # Generate review_output.json for inline_comment.py compatibility - MOVED AFTER comparison
        critical_findings = [f for f in consolidated_json.get("detailed_findings", []) if str(f.get("severity", "")).upper() == "CRITICAL"]
       
        criticals = []
        for f in critical_findings:
            critical = {
                "line": f.get("line_number", "N/A"),
                "issue": f.get("finding", "Critical issue found"),
                "recommendation": f.get("recommendation", f.get("finding", "")),
                "severity": f.get("severity", "Critical"),
                "filename": f.get("filename", "N/A"),
                "business_impact": f.get("business_impact", "No business impact specified"),
                "description": f.get("finding", "Critical issue found")
            }
            criticals.append(critical)

        # Create a proper critical issues summary for inline_comment.py with CUSTOM FORMAT
        critical_summary = ""
        if critical_findings:
            critical_summary = "Critical Issues Summary:\n"
            for i, finding in enumerate(critical_findings, 1):
                line_num = finding.get("line_number", "N/A")
                # CUSTOM FORMAT: "Critical issues are also posted as inline comments on X line"
                critical_summary += f"* **Line {line_num}:** Critical issues are also posted as inline comments on {line_num} line\n"

        # IMPORTANT: Generate this BEFORE the LLM comparison stage so it's always available
        review_output_data = {
            "full_review": executive_summary,
            "full_review_markdown": executive_summary,
            "full_review_json": consolidated_json,
            "criticals": criticals,
            "critical_summary": critical_summary,
            "critical_count": len(critical_findings),
            "file": processed_files[0] if processed_files else "unknown",
            "timestamp": datetime.now().isoformat()
        }

        with open("review_output.json", "w", encoding='utf-8') as f:
            json.dump(review_output_data, f, indent=2, ensure_ascii=False)
        print("  ✅ review_output.json saved for inline_comment.py compatibility")

        # ENHANCED: LLM-based comparison with previous review
        comparison_result = None
        if pull_request_number and pull_request_number != 0 and database_available:
            print("\n🔄 STAGE 3: LLM Comparison with Previous Review...")
            print("=" * 60)
           
            # Fetch the previous review for comparison
            previous_review_summary = fetch_last_review_for_comparison(session, pull_request_number)
           
            if previous_review_summary:
                print("📋 Previous review found. Performing LLM comparison...")
               
                # Format the comparison prompt using the template from second code
                formatted_prompt = PROMPT_TO_COMPARE_REVIEWS.replace(
                    "{previous_review_text}", str(previous_review_summary)
                ).replace(
                    "{new_review_text}", json.dumps(consolidated_json, indent=2)
                )
               
                # Use the LLM comparison function
                comparison_result = get_llm_comparison(COMPARISON_MODEL, formatted_prompt, session)
               
                if comparison_result:
                    print("✅ LLM comparison successful")
                    print(f"📊 Comparison summary: {comparison_result.get('comparison_summary', 'No summary available')}")
                   
                    # Update consolidated JSON with comparison insights
                    if 'issue_status' in comparison_result:
                        # Convert LLM comparison results to our previous_issues_resolved format
                        previous_issues_resolved = []
                        for issue_status in comparison_result.get('issue_status', []):
                            resolved_issue = {
                                "original_issue": issue_status.get('issue', ''),
                                "line_number": issue_status.get('line_number', 'N/A'),
                                "filename": issue_status.get('filename', 'N/A'),  # ENHANCED: Include filename
                                "status": issue_status.get('status', 'UNKNOWN'),
                                "details": issue_status.get('reasoning', '')
                            }
                            previous_issues_resolved.append(resolved_issue)
                       
                        # Update the consolidated JSON with the comparison results
                        consolidated_json["previous_issues_resolved"] = previous_issues_resolved
                       
                        print(f"📈 Updated consolidated JSON with {len(previous_issues_resolved)} previous issue statuses")
                       
                        # Regenerate executive summary with comparison data
                        executive_summary = format_executive_pr_display(consolidated_json, processed_files)
                       
                        # Update the saved files
                        with open(consolidated_path, 'w', encoding='utf-8') as f:
                            f.write(executive_summary)
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(consolidated_json, f, indent=2)
                       
                        # IMPORTANT: Also update the review_output.json for inline_comment.py compatibility
                        review_output_data["full_review"] = executive_summary
                        review_output_data["full_review_markdown"] = executive_summary
                        review_output_data["full_review_json"] = consolidated_json
                       
                        with open("review_output.json", "w", encoding='utf-8') as f:
                            json.dump(review_output_data, f, indent=2, ensure_ascii=False)
                       
                        print("✅ Updated executive summary, JSON files, and review_output.json with comparison results")
                else:
                    print("⚠️ LLM comparison failed or returned no results")
            else:
                print("📋 No previous review found for comparison - this appears to be the initial review")

        # Store current review for future comparisons - ENHANCED with comparison_result and APPEND mode
        if pull_request_number and pull_request_number != 0 and database_available:
            store_review_log(pull_request_number, commit_sha, executive_summary, consolidated_json, processed_files, comparison_result)

        if 'GITHUB_OUTPUT' in os.environ:
            delimiter = str(uuid.uuid4())
            with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_out:
                gh_out.write(f'consolidated_summary_text<<{delimiter}\n')
                gh_out.write(f'{executive_summary}\n')
                gh_out.write(f'{delimiter}\n')
            print("  ✅ GitHub Actions output written")

        print(f"\n🎉 THREE-STAGE ANALYSIS COMPLETED!")
        print("=" * 60)
        print(f"📁 Files processed: {len(processed_files)}")
        print(f"🔍 Individual reviews: {len(all_individual_reviews)} (STAGE 1)")
        print(f"📊 Executive summary: 1 (STAGE 2)")
        if comparison_result:
            print(f"🔄 LLM comparison: ✅ (STAGE 3)")
            print(f"📈 Issues compared: {len(comparison_result.get('issue_status', []))}")
        else:
            print(f"🔄 LLM comparison: ❌ (No previous review or comparison failed)")
        print(f"🎯 Quality Score: {consolidated_json.get('quality_score', 'N/A')}/100")
        print(f"📈 Findings: {len(consolidated_json.get('detailed_findings', []))}")
       
        if database_available:
            print(f"💾 Database logging: ✅ APPENDED to {current_database}.{current_schema} with comparison_result")
        else:
            print(f"💾 Database logging: ❌ Not available")
       
    except Exception as e:
        print(f"❌ Consolidation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'session' in locals() and session:
            try:
                session.close()
                print("\n🔒 Snowflake session closed")
            except:
                pass

On Wed, Sep 24, 2025 at 8:08 PM Manisha T <tmanisha007@gmail.com> wrote:
import os, sys, json, re, uuid, glob
from pathlib import Path
from snowflake.snowpark import Session
import pandas as pd
from datetime import datetime

# ---------------------
# Config
# ---------------------
MODEL = "openai-gpt-4.1"
COMPARISON_MODEL = "claude-3-5-sonnet"
MAX_CHARS_FOR_FINAL_SUMMARY_FILE = 65000
MAX_TOKENS_FOR_SUMMARY_INPUT = 100000

# Dynamic file pattern - processes all Python AND SQL files in scripts directory
SCRIPTS_DIRECTORY = "scripts"  # Base directory to scan
FILE_PATTERNS = ["*.py", "*.sql"]  # CHANGED: Added SQL files

# ---------------------
# Snowflake session
# ---------------------
# MINIMAL CHANGE: read from env so it matches your YAML secrets/env
cfg = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE", "SYSADMIN"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
}
session = Session.builder.configs(cfg).create()

# FIX DATABASE PERMISSIONS AND SETUP: Enhanced approach
database_available = False
current_database = None
current_schema = None

def setup_database_with_fallback():
    """Setup database with multiple fallback strategies"""
    global database_available, current_database, current_schema
   
    print("🔧 Setting up database for review logging...")
   
    # MINIMAL CHANGE: use env-provided db/schema/role (no hardcoded ACCOUNTADMIN/MY_DB/PUBLIC)
    db_env = cfg.get("database") or "MY_DB"
    schema_env = cfg.get("schema") or "PUBLIC"
    role_env = cfg.get("role") or "SYSADMIN"
   
    # Strategy 1: Try env database with env role (grants if allowed)
    try:
        session.sql(f"USE ROLE {role_env}").collect()
        # Grants may or may not be allowed; harmless if they fail
        session.sql(f"GRANT USAGE ON DATABASE {db_env} TO ROLE {role_env}").collect()
        session.sql(f"GRANT USAGE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
        session.sql(f"GRANT CREATE TABLE ON SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
        session.sql(f"GRANT INSERT ON ALL TABLES IN SCHEMA {db_env}.{schema_env} TO ROLE {role_env}").collect()
        session.sql(f"USE ROLE {role_env}").collect()
        session.sql(f"USE DATABASE {db_env}").collect()
        session.sql(f"USE SCHEMA {schema_env}").collect()
        current_database = db_env
        current_schema = schema_env
        print(f"✅ Strategy 1: Using {db_env}.{schema_env} with role {role_env}")
        database_available = True
        return True
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
        return True
    except Exception as e:
        print(f"⚠️ Strategy 2 failed: {e}")

    # Strategy 3: Try user's personal database
    try:
        session.sql(f"USE ROLE {role_env}").collect()
        user_db = f"DB_{cfg.get('user','USER')}"
        session.sql(f"CREATE DATABASE IF NOT EXISTS {user_db}").collect()
        session.sql(f"USE DATABASE {user_db}").collect()
        session.sql("CREATE SCHEMA IF NOT EXISTS LOGS").collect()
        session.sql("USE SCHEMA LOGS").collect()
        current_database = user_db
        current_schema = "LOGS"
        print(f"✅ Strategy 3: Successfully created and using {user_db}.LOGS")
        database_available = True
        return True
    except Exception as e:
        print(f"⚠️ Strategy 3 failed: {e}")

    print("❌ All database strategies failed - continuing without logging")
    database_available = False
    return False

# Setup database
setup_database_with_fallback()

# ---------------------
# PROMPT TEMPLATES
# ---------------------
PROMPT_TEMPLATE_INDIVIDUAL = """Please act as a principal-level code reviewer with expertise in Python, SQL, and database security. Your review must be concise, accurate, and directly actionable, as it will be posted as a GitHub Pull Request comment.

---
# CONTEXT: HOW TO REVIEW (Apply Silently)

1.  **You are reviewing a code file for executive-level analysis.** Focus on business impact, technical debt, security risks, and maintainability.
2.  **Focus your review on the most critical aspects.** Prioritize findings that have business impact or security implications.
3.  **Infer context from the full code.** Base your review on the complete file provided.
4.  **Your entire response MUST be under 65,000 characters.** Include findings of all severities but prioritize Critical and High severity issues.

# REVIEW PRIORITIES (Strict Order)
1.  Security & Correctness (Real SQL Injection with User Input, Production Credentials)
2.  Reliability & Error-handling
3.  Performance & Complexity (Major Bottlenecks, Resource Issues)
4.  Readability & Maintainability
5.  Testability

# BALANCED SECURITY FOCUS AREAS:
**For SQL Code & Database Operations (BE REALISTIC):**
-   **CRITICAL ONLY:** Confirmed SQL injection with user input paths, production credentials exposed in code, DELETE/UPDATE without WHERE affecting entire tables, data breach risks
-   **HIGH:** Missing parameterization with potential user input exposure, significant security gaps, major performance bottlenecks affecting production
-   **MEDIUM:** Hardcoded non-production values, suboptimal queries, missing indexes, maintainability issues, code organization problems
-   **LOW:** Style inconsistencies, minor optimizations, documentation gaps, cosmetic improvements

**For Python Code (BE REALISTIC):**
-   **CRITICAL ONLY:** Confirmed code injection with user input (eval/exec with user data), production credential exposure, data corruption risks
-   **HIGH:** Significant error handling gaps, major security concerns, subprocess vulnerabilities with user input
-   **MEDIUM:** Code quality improvements, minor security concerns, maintainability issues, missing error handling
-   **LOW:** Style improvements, minor optimizations, documentation gaps, cosmetic issues

# REALISTIC SEVERITY GUIDELINES (MANDATORY - MOST ISSUES ARE NOT CRITICAL):
-   **Critical:** 0-2% of findings (extremely rare - only for confirmed security vulnerabilities with user input or production credential exposure)
-   **High:** 5-15% of findings (significant but fixable issues)
-   **Medium:** 50-60% of findings (most common - code quality and maintainability)
-   **Low:** 25-40% of findings (style and minor improvements)

# COMMON SQL PATTERNS THAT ARE **NOT CRITICAL**:
- Hardcoded database/schema names: **Medium** (maintainability issue)
- Missing comments: **Low** (documentation)
- Suboptimal JOIN patterns: **Medium** (performance)
- Missing indexes (without proof of performance impact): **Medium**
- Static SQL without user input: **Medium at most** (not critical)
- Development/test connection strings: **Medium** (not critical unless production)

# ELIGIBILITY CRITERIA FOR FINDINGS (ALL must be met)
-   **Evidence:** Quote the exact code snippet and cite the line number.
-   **Severity:** Assign {Low | Medium | High | Critical} - BE VERY CONSERVATIVE. Only use Critical for confirmed security vulnerabilities.
-   **Impact & Action:** Briefly explain the issue and provide a minimal, safe correction.
-   **Non-trivial:** Skip purely stylistic nits (e.g., import order, line length) that a linter would catch.

# HARD CONSTRAINTS (For accuracy & anti-hallucination)
-   Do NOT propose APIs that don't exist for the imported modules.
-   Treat parameters like `db_path` as correct dependency injection; do NOT call them hardcoded.
-   NEVER suggest logging sensitive user data or internal paths. Suggest non-reversible fingerprints if context is needed.
-   Do NOT recommend removing correct type hints or docstrings.
-   If code in the file is already correct and idiomatic, do NOT invent problems.
-   DO NOT inflate severity levels - be very conservative. Most findings should be Medium or Low.
-   **For SQL files:** Only mark Critical if there's confirmed SQL injection with user input. Hardcoded values are usually Medium.
-   **For Python files with SQL:** Only mark Critical if there's confirmed injection vulnerability with user data.

---
# OUTPUT FORMAT (Strict, professional, audit-ready)

Your entire response MUST be under 65,000 characters. Include findings of all severity levels with REALISTIC severity assignments.

## Code Review Summary
*A 2-3 sentence high-level summary. Mention the key strengths and the most critical areas for improvement, being realistic about severity.*

---
### Detailed Findings
*A list of all material findings. If no significant issues are found, state "No significant issues found."*

**File:** {filename}
-   **Severity:** {Critical | High | Medium | Low}
-   **Line:** {line_number}
-   **Function/Context:** `{function_name_if_applicable}`
-   **Finding:** {A clear, concise description of the issue, its impact, and a recommended correction. Be realistic about severity - most issues are Medium or Low.}

**(Repeat for each finding)**

---
### Key Recommendations
*Provide 2-3 high-level, actionable recommendations for improving the overall quality of the codebase based on the findings. Focus on the most impactful improvements.*

---
# CODE TO REVIEW

{PY_CONTENT}
"""

PROMPT_TEMPLATE_CONSOLIDATED = """
You are an expert code review summarization engine for executive-level reporting. Your task is to analyze individual code reviews and generate a single, consolidated executive summary with business impact focus.

You MUST respond ONLY with a valid JSON object that conforms to the executive schema. Do not include any other text, explanations, or markdown formatting outside of the JSON structure.

Follow these instructions to populate the JSON fields:

1.  **`executive_summary` (string):** Write a 2-3 sentence high-level summary of the entire code change, covering the most important findings across all files with business impact focus.
2.  **`quality_score` (number):** Assign an overall quality score (0-100) based on severity and number of findings.
3.  **`business_impact` (string):** Assess overall business risk as "LOW", "MEDIUM", or "HIGH".
4.  **`technical_debt_score` (string):** Evaluate technical debt as "LOW", "MEDIUM", or "HIGH".
5.  **`security_risk_level` (string):** Determine security risk as "LOW", "MEDIUM", "HIGH", or "CRITICAL". Only use CRITICAL for confirmed SQL injection or production credential exposure.
6.  **`maintainability_rating` (string):** Rate maintainability as "POOR", "FAIR", "GOOD", or "EXCELLENT".
7.  **`detailed_findings` (array of objects):** Create an array of objects, where each object represents a single, distinct issue found in the code:
         -   **`severity`**: Assign severity VERY CONSERVATIVELY: "Low", "Medium", "High", or "Critical". CRITICAL should be 0-2% of all findings (only for confirmed security vulnerabilities with user input or production credential exposure). HIGH should be 5-15%. MEDIUM should be 50-60% (most common). LOW should be 25-40%.
         -   **`category`**: Assign category: "Security", "Performance", "Maintainability", "Best Practices", "Documentation", or "Error Handling".
         -   **`line_number`**: Extract the specific line number if mentioned in the review. If no line number is available, use "N/A".
         -   **`function_context`**: From the review text, identify the function or class name where the issue is located. If not applicable, use "global scope".
         -   **`finding`**: Write a clear, concise description of the issue, its potential impact, and a concrete recommendation.
         -   **`business_impact`**: Explain how this affects business operations or risk. Be realistic - most issues have low to medium business impact.
         -   **`recommendation`**: Provide specific technical solution.
         -   **`effort_estimate`**: Estimate effort as "LOW", "MEDIUM", or "HIGH".
         -   **`priority_ranking`**: Assign priority ranking (1 = highest priority).
         -   **`filename`**: The name of the file where the issue was found.
8.  **`metrics` (object):** Include technical metrics:
         -   **`lines_of_code`**: Total number of lines analyzed across all files.
         -   **`complexity_score`**: "LOW", "MEDIUM", or "HIGH".
         -   **`code_coverage_gaps`**: Array of areas needing test coverage.
         -   **`dependency_risks`**: Array of dependency-related risks.
9.  **`strategic_recommendations` (array of strings):** Provide 2-3 high-level, actionable recommendations for technical leadership.
10. **`immediate_actions` (array of strings):** List critical items requiring immediate attention. Should be very few items.
11. **`previous_issues_resolved` (array of objects):** For each issue from previous review, indicate status:
         -   **`original_issue`**: Brief description of the previous issue
         -   **`line_number`**: Line number from the previous issue (if available)
         -   **`filename`**: Filename from the previous issue (if available)
         -   **`status`**: "RESOLVED", "PARTIALLY_RESOLVED", "NOT_ADDRESSED", or "WORSENED"
         -   **`details`**: Explanation of current status

**CRITICAL INSTRUCTION FOR REALISTIC REVIEWS:**
Your entire response MUST be under {MAX_CHARS_FOR_FINAL_SUMMARY_FILE} characters. Include findings of all severity levels with VERY CONSERVATIVE severity assignments:
-   Use "Critical" ONLY for confirmed SQL injection with user input, production credential exposure, or confirmed data breach risks (0-2% of findings)
-   Use "High" for significant security concerns, major performance issues, or significant error handling gaps (5-15% of findings)
-   Use "Medium" for code quality issues, maintainability concerns, minor performance issues, hardcoded non-production values (50-60% of findings - MOST COMMON)
-   Use "Low" for style improvements, minor optimizations, documentation gaps, cosmetic issues (25-40% of findings)

**IMPORTANT SQL GUIDANCE:**
- Hardcoded database names/schemas: Medium (maintainability issue, not security)
- Missing comments in SQL: Low (documentation)
- Suboptimal queries without performance proof: Medium
- Static SQL without user input: Medium at most
- Only mark SQL issues as Critical if there's confirmed injection with user input

Here are the individual code reviews to process:
{ALL_REVIEWS_CONTENT}
"""

PROMPT_TEMPLATE_WITH_CONTEXT = """
You are reviewing subsequent commits for Pull Request #{pr_number}.

PREVIOUS REVIEW SUMMARY AND FINDINGS:
{previous_context}

CRITICAL INSTRUCTION: You must analyze the new code changes with full awareness of the previous feedback. Specifically:
1. Check if previous Critical/High severity issues were addressed in the new code
2. Identify if any previous recommendations were implemented
3. Note any new issues that may have been introduced
4. Maintain continuity with previous review comments
5. In the "previous_issues_resolved" section, provide specific status for each previous issue INCLUDING LINE NUMBERS AND FILENAMES

{consolidated_template}
"""

# LLM COMPARISON PROMPT TEMPLATE - ENHANCED VERSION FROM SECOND CODE
PROMPT_TO_COMPARE_REVIEWS = """You are an expert AI code review assistant. Your task is to compare a previous code review with a new code review for the same pull request. The developer has pushed new code, attempting to fix the issues mentioned in the previous review.

Analyze if the feedback in the **[NEW REVIEW]** suggests that the specific issues raised in the **[PREVIOUS REVIEW]** have been addressed. Do not just look for the exact same text. Understand the underlying problem described in the previous review and see if the new review sounds positive, different, or no longer mentions that specific problem.

**[PREVIOUS REVIEW]:**
'''
{previous_review_text}
'''

**[NEW REVIEW]:**
'''
{new_review_text}
'''

CRITICAL INSTRUCTION: You must analyze the new code changes with full awareness of the previous feedback. Specifically:
1. Check if previous Critical/High severity issues were addressed in the new code
2. Identify if any previous recommendations were implemented
3. Note any new issues that may have been introduced
4. Maintain continuity with previous review comments
5. In the "previous_issues_resolved" section, provide specific status for each previous issue INCLUDING FILENAMES

**[YOUR TASK]:**
Provide your analysis in a structured JSON format. For each major issue identified in the **[PREVIOUS REVIEW]**, determine its status based on the **[NEW REVIEW]**. The possible statuses are:

- **"RESOLVED"**: The issue is no longer mentioned in the new review, or the new review provides positive feedback on that area.
- **"PARTIALLY_RESOLVED"**: The new review indicates some improvement but mentions that the issue is not fully fixed.
- **"NOT_ADDRESSED"**: The new review repeats the same criticism or feedback.
- **"WORSENED"**: Despite attempting to fix the issue, some new errors were added to the code, which made it worse.
- **"NO_LONGER_APPLICABLE"**: The code related to the original feedback was removed or changed so significantly that the feedback doesn't apply.

The JSON output should follow this exact structure:
{
  "comparison_summary": "A brief, one-sentence summary of whether the developer addressed the feedback.",
  "issue_status": [
    {
      "issue": "A concise summary of the original issue from the previous review.",
      "line_number": "Line number from the original issue if available, otherwise 'N/A'",
      "filename": "Filename from the original issue if available, otherwise 'N/A'",
      "status": "RESOLVED | PARTIALLY_RESOLVED | NOT_ADDRESSED | WORSENED | NO_LONGER_APPLICABLE",
      "reasoning": "A brief explanation for your status decision, referencing the new review."
    }
  ],
  "new_issues_introduced": [
    {
      "issue": "Description of any new issues found in the new review that weren't in the previous review",
      "severity": "Critical | High | Medium | Low",
      "line_number": "Line number if available",
      "filename": "Filename if available"
    }
  ],
  "overall_improvement": "IMPROVED | NEUTRAL | WORSENED",
  "quality_trend": "Quality score trend analysis comparing previous vs current review"
}

STRICTLY provide the result within 3000 characters. DO NOT exceed the character limit.
"""

def get_changed_python_files(folder_path=None):
    """
    Dynamically get all Python AND SQL files from the specified folder or scripts directory.
    Uses wildcard pattern matching for flexibility.
    """
    # If no folder specified, use the scripts directory
    if not folder_path:
        folder_path = SCRIPTS_DIRECTORY
       
    if not os.path.exists(folder_path):
        print(f"❌ Directory {folder_path} not found")
        return []
   
    all_files = []
   
    # Process both Python and SQL files
    for pattern in FILE_PATTERNS:
        # Use glob pattern to find files
        pattern_path = os.path.join(folder_path, pattern)
        found_files = glob.glob(pattern_path)
       
        # Also check subdirectories recursively
        recursive_pattern = os.path.join(folder_path, "**", pattern)
        found_files.extend(glob.glob(recursive_pattern, recursive=True))
       
        all_files.extend(found_files)
   
    # Remove duplicates and sort
    all_files = sorted(list(set(all_files)))
   
    print(f"📁 Found {len(all_files)} code files in {folder_path} using patterns {FILE_PATTERNS}:")
    for file in all_files:
        file_type = "SQL" if file.lower().endswith('.sql') else "Python"
        print(f"  - {file} ({file_type})")
   
    return all_files

def build_prompt_for_individual_review(code_text: str, filename: str = "code_file") -> str:
    prompt = PROMPT_TEMPLATE_INDIVIDUAL.replace("{PY_CONTENT}", code_text)
    prompt = prompt.replace("{filename}", filename)
    return prompt

def build_prompt_for_consolidated_summary(all_reviews_content: str, previous_context: str = None, pr_number: int = None) -> str:
    if previous_context and pr_number:
        prompt = PROMPT_TEMPLATE_WITH_CONTEXT.replace("{previous_context}", previous_context)
        prompt = prompt.replace("{pr_number}", str(pr_number))
        prompt = prompt.replace("{consolidated_template}", PROMPT_TEMPLATE_CONSOLIDATED)
        prompt = prompt.replace("{ALL_REVIEWS_CONTENT}", all_reviews_content)
    else:
        prompt = PROMPT_TEMPLATE_CONSOLIDATED.replace("{ALL_REVIEWS_CONTENT}", all_reviews_content)
    return prompt

def review_with_cortex(model, prompt_text: str, session) -> str:
    try:
        clean_prompt = prompt_text.replace("'", "''").replace("\\", "\\\\")
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{clean_prompt}') as response"
        df = session.sql(query)
        result = df.collect()[0][0]
        re
...

[Message clipped]  View entire message
 One attachment
  •  Scanned by Gmail
import os, sys, json, re, uuid, glob
from pathlib import Path
from snowflake.snowpark import Session
import pandas as pd
from datetime import datetime

# ---------------------
# Config
# ---------------------
MODEL = "openai-gpt-4.1"
COMPARISON_MODEL = "claude-3-5-sonnet"
MAX_CHARS_FOR_FINAL_SUMMARY_FILE = 65000
MAX_TOKENS_FOR_SUMMARY_INPUT = 100000

# Dynamic file pattern - processes all Python AND SQL files in scripts directory
SCRIPTS_DIRECTORY = "scripts"  # Base directory to scan
FILE_PATTERNS = ["*.py", "*.sql"]  # CHANGED: Added SQL files

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
except Exception as e:
    print(f"❌ Failed to connect to Snowflake: {e}")
    sys.exit(1)

# FIX DATABASE PERMISSIONS AND SETUP: Enhanced approach
database_available = False
current_database = None
current_schema = None

def setup_database_with_fallback():
    """Setup database with multiple fallback strategies"""
    global database_available, current_database, current_schema
   
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
        return True
        
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
        return True
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
        return True
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
        return True
    except Exception as e:
        print(f"⚠️ Strategy 4 failed: {e}")

    print("❌ All database strategies failed - continuing without logging")
    print("  This means review history and comparison features will be disabled")
    database_available = False
    return False

# Setup database
setup_database_with_fallback()

# ---------------------
# PROMPT TEMPLATES
# ---------------------
PROMPT_TEMPLATE_INDIVIDUAL = """Please act as a principal-level code reviewer with expertise in Python, SQL, and database security. Your review must be concise, accurate, and directly actionable, as it will be posted as a GitHub Pull Request comment.

---
# CONTEXT: HOW TO REVIEW (Apply Silently)

1.  **You are reviewing a code file for executive-level analysis.** Focus on business impact, technical debt, security risks, and maintainability.
2.  **Focus your review on the most critical aspects.** Prioritize findings that have business impact or security implications.
3.  **Infer context from the full code.** Base your review on the complete file provided.
4.  **Your entire response MUST be under 65,000 characters.** Include findings of all severities but prioritize Critical and High severity issues.

# REVIEW PRIORITIES (Strict Order)
1.  Security & Correctness (Real SQL Injection with User Input, Production Credentials)
2.  Reliability & Error-handling
3.  Performance & Complexity (Major Bottlenecks, Resource Issues)
4.  Readability & Maintainability
5.  Testability

# BALANCED SECURITY FOCUS AREAS:
**For SQL Code & Database Operations (BE REALISTIC):**
-   **CRITICAL ONLY:** Confirmed SQL injection with user input paths, production credentials exposed in code, DELETE/UPDATE without WHERE affecting entire tables, data breach risks
-   **HIGH:** Missing parameterization with potential user input exposure, significant security gaps, major performance bottlenecks affecting production
-   **MEDIUM:** Hardcoded non-production values, suboptimal queries, missing indexes, maintainability issues, code organization problems
-   **LOW:** Style inconsistencies, minor optimizations, documentation gaps, cosmetic improvements

**For Python Code (BE REALISTIC):**
-   **CRITICAL ONLY:** Confirmed code injection with user input (eval/exec with user data), production credential exposure, data corruption risks
-   **HIGH:** Significant error handling gaps, major security concerns, subprocess vulnerabilities with user input
-   **MEDIUM:** Code quality improvements, minor security concerns, maintainability issues, missing error handling
-   **LOW:** Style improvements, minor optimizations, documentation gaps, cosmetic issues

# REALISTIC SEVERITY GUIDELINES (MANDATORY - MOST ISSUES ARE NOT CRITICAL):
-   **Critical:** 0-2% of findings (extremely rare - only for confirmed security vulnerabilities with user input or production credential exposure)
-   **High:** 5-15% of findings (significant but fixable issues)
-   **Medium:** 50-60% of findings (most common - code quality and maintainability)
-   **Low:** 25-40% of findings (style and minor improvements)

# COMMON SQL PATTERNS THAT ARE **NOT CRITICAL**:
- Hardcoded database/schema names: **Medium** (maintainability issue)
- Missing comments: **Low** (documentation)
- Suboptimal JOIN patterns: **Medium** (performance)
- Missing indexes (without proof of performance impact): **Medium**
- Static SQL without user input: **Medium at most** (not critical)
- Development/test connection strings: **Medium** (not critical unless production)

# ELIGIBILITY CRITERIA FOR FINDINGS (ALL must be met)
-   **Evidence:** Quote the exact code snippet and cite the line number.
-   **Severity:** Assign {Low | Medium | High | Critical} - BE VERY CONSERVATIVE. Only use Critical for confirmed security vulnerabilities.
-   **Impact & Action:** Briefly explain the issue and provide a minimal, safe correction.
-   **Non-trivial:** Skip purely stylistic nits (e.g., import order, line length) that a linter would catch.

# HARD CONSTRAINTS (For accuracy & anti-hallucination)
-   Do NOT propose APIs that don't exist for the imported modules.
-   Treat parameters like `db_path` as correct dependency injection; do NOT call them hardcoded.
-   NEVER suggest logging sensitive user data or internal paths. Suggest non-reversible fingerprints if context is needed.
-   Do NOT recommend removing correct type hints or docstrings.
-   If code in the file is already correct and idiomatic, do NOT invent problems.
-   DO NOT inflate severity levels - be very conservative. Most findings should be Medium or Low.
-   **For SQL files:** Only mark Critical if there's confirmed SQL injection with user input. Hardcoded values are usually Medium.
-   **For Python files with SQL:** Only mark Critical if there's confirmed injection vulnerability with user data.

---
# OUTPUT FORMAT (Strict, professional, audit-ready)

Your entire response MUST be under 65,000 characters. Include findings of all severity levels with REALISTIC severity assignments.

## Code Review Summary
*A 2-3 sentence high-level summary. Mention the key strengths and the most critical areas for improvement, being realistic about severity.*

---
### Detailed Findings
*A list of all material findings. If no significant issues are found, state "No significant issues found."*

**File:** {filename}
-   **Severity:** {Critical | High | Medium | Low}
-   **Line:** {line_number}
-   **Function/Context:** `{function_name_if_applicable}`
-   **Finding:** {A clear, concise description of the issue, its impact, and a recommended correction. Be realistic about severity - most issues are Medium or Low.}

**(Repeat for each finding)**

---
### Key Recommendations
*Provide 2-3 high-level, actionable recommendations for improving the overall quality of the codebase based on the findings. Focus on the most impactful improvements.*

---
# CODE TO REVIEW

{PY_CONTENT}
"""

PROMPT_TEMPLATE_CONSOLIDATED = """
You are an expert code review summarization engine for executive-level reporting. Your task is to analyze individual code reviews and generate a single, consolidated executive summary with business impact focus.

You MUST respond ONLY with a valid JSON object that conforms to the executive schema. Do not include any other text, explanations, or markdown formatting outside of the JSON structure.

Follow these instructions to populate the JSON fields:

1.  **`executive_summary` (string):** Write a 2-3 sentence high-level summary of the entire code change, covering the most important findings across all files with business impact focus.
2.  **`quality_score` (number):** Assign an overall quality score (0-100) based on severity and number of findings.
3.  **`business_impact` (string):** Assess overall business risk as "LOW", "MEDIUM", or "HIGH".
4.  **`technical_debt_score` (string):** Evaluate technical debt as "LOW", "MEDIUM", or "HIGH".
5.  **`security_risk_level` (string):** Determine security risk as "LOW", "MEDIUM", "HIGH", or "CRITICAL". Only use CRITICAL for confirmed SQL injection or production credential exposure.
6.  **`maintainability_rating` (string):** Rate maintainability as "POOR", "FAIR", "GOOD", or "EXCELLENT".
7.  **`detailed_findings` (array of objects):** Create an array of objects, where each object represents a single, distinct issue found in the code:
         -   **`severity`**: Assign severity VERY CONSERVATIVELY: "Low", "Medium", "High", or "Critical". CRITICAL should be 0-2% of all findings (only for confirmed security vulnerabilities with user input or production credential exposure). HIGH should be 5-15%. MEDIUM should be 50-60% (most common). LOW should be 25-40%.
         -   **`category`**: Assign category: "Security", "Performance", "Maintainability", "Best Practices", "Documentation", or "Error Handling".
         -   **`line_number`**: Extract the specific line number if mentioned in the review. If no line number is available, use "N/A".
         -   **`function_context`**: From the review text, identify the function or class name where the issue is located. If not applicable, use "global scope".
         -   **`finding`**: Write a clear, concise description of the issue, its potential impact, and a concrete recommendation.
         -   **`business_impact`**: Explain how this affects business operations or risk. Be realistic - most issues have low to medium business impact.
         -   **`recommendation`**: Provide specific technical solution.
         -   **`effort_estimate`**: Estimate effort as "LOW", "MEDIUM", or "HIGH".
         -   **`priority_ranking`**: Assign priority ranking (1 = highest priority).
         -   **`filename`**: The name of the file where the issue was found.
8.  **`metrics` (object):** Include technical metrics:
         -   **`lines_of_code`**: Total number of lines analyzed across all files.
         -   **`complexity_score`**: "LOW", "MEDIUM", or "HIGH".
         -   **`code_coverage_gaps`**: Array of areas needing test coverage.
         -   **`dependency_risks`**: Array of dependency-related risks.
9.  **`strategic_recommendations` (array of strings):** Provide 2-3 high-level, actionable recommendations for technical leadership.
10. **`immediate_actions` (array of strings):** List critical items requiring immediate attention. Should be very few items.
11. **`previous_issues_resolved` (array of objects):** For each issue from previous review, indicate status:
         -   **`original_issue`**: Brief description of the previous issue
         -   **`line_number`**: Line number from the previous issue (if available)
         -   **`filename`**: Filename from the previous issue (if available)
         -   **`status`**: "RESOLVED", "PARTIALLY_RESOLVED", "NOT_ADDRESSED", or "WORSENED"
         -   **`details`**: Explanation of current status

**CRITICAL INSTRUCTION FOR REALISTIC REVIEWS:**
Your entire response MUST be under {MAX_CHARS_FOR_FINAL_SUMMARY_FILE} characters. Include findings of all severity levels with VERY CONSERVATIVE severity assignments:
-   Use "Critical" ONLY for confirmed SQL injection with user input, production credential exposure, or confirmed data breach risks (0-2% of findings)
-   Use "High" for significant security concerns, major performance issues, or significant error handling gaps (5-15% of findings)
-   Use "Medium" for code quality issues, maintainability concerns, minor performance issues, hardcoded non-production values (50-60% of findings - MOST COMMON)
-   Use "Low" for style improvements, minor optimizations, documentation gaps, cosmetic issues (25-40% of findings)

**IMPORTANT SQL GUIDANCE:**
- Hardcoded database names/schemas: Medium (maintainability issue, not security)
- Missing comments in SQL: Low (documentation)
- Suboptimal queries without performance proof: Medium
- Static SQL without user input: Medium at most
- Only mark SQL issues as Critical if there's confirmed injection with user input

Here are the individual code reviews to process:
{ALL_REVIEWS_CONTENT}
"""

PROMPT_TEMPLATE_WITH_CONTEXT = """
You are reviewing subsequent commits for Pull Request #{pr_number}.

PREVIOUS REVIEW SUMMARY AND FINDINGS:
{previous_context}

CRITICAL INSTRUCTION: You must analyze the new code changes with full awareness of the previous feedback. Specifically:
1. Check if previous Critical/High severity issues were addressed in the new code
2. Identify if any previous recommendations were implemented
3. Note any new issues that may have been introduced
4. Maintain continuity with previous review comments
5. In the "previous_issues_resolved" section, provide specific status for each previous issue INCLUDING LINE NUMBERS AND FILENAMES

{consolidated_template}
"""

# LLM COMPARISON PROMPT TEMPLATE - ENHANCED VERSION FROM SECOND CODE
PROMPT_TO_COMPARE_REVIEWS = """You are an expert AI code review assistant. Your task is to compare a previous code review with a new code review for the same pull request. The developer has pushed new code, attempting to fix the issues mentioned in the previous review.

Analyze if the feedback in the **[NEW REVIEW]** suggests that the specific issues raised in the **[PREVIOUS REVIEW]** have been addressed. Do not just look for the exact same text. Understand the underlying problem described in the previous review and see if the new review sounds positive, different, or no longer mentions that specific problem.

**[PREVIOUS REVIEW]:**
'''
{previous_review_text}
'''

**[NEW REVIEW]:**
'''
{new_review_text}
'''

CRITICAL INSTRUCTION: You must analyze the new code changes with full awareness of the previous feedback. Specifically:
1. Check if previous Critical/High severity issues were addressed in the new code
2. Identify if any previous recommendations were implemented
3. Note any new issues that may have been introduced
4. Maintain continuity with previous review comments
5. In the "previous_issues_resolved" section, provide specific status for each previous issue INCLUDING FILENAMES

**[YOUR TASK]:**
Provide your analysis in a structured JSON format. For each major issue identified in the **[PREVIOUS REVIEW]**, determine its status based on the **[NEW REVIEW]**. The possible statuses are:

- **"RESOLVED"**: The issue is no longer mentioned in the new review, or the new review provides positive feedback on that area.
- **"PARTIALLY_RESOLVED"**: The new review indicates some improvement but mentions that the issue is not fully fixed.
- **"NOT_ADDRESSED"**: The new review repeats the same criticism or feedback.
- **"WORSENED"**: Despite attempting to fix the issue, some new errors were added to the code, which made it worse.
- **"NO_LONGER_APPLICABLE"**: The code related to the original feedback was removed or changed so significantly that the feedback doesn't apply.

The JSON output should follow this exact structure:
{
  "comparison_summary": "A brief, one-sentence summary of whether the developer addressed the feedback.",
  "issue_status": [
    {
      "issue": "A concise summary of the original issue from the previous review.",
      "line_number": "Line number from the original issue if available, otherwise 'N/A'",
      "filename": "Filename from the original issue if available, otherwise 'N/A'",
      "status": "RESOLVED | PARTIALLY_RESOLVED | NOT_ADDRESSED | WORSENED | NO_LONGER_APPLICABLE",
      "reasoning": "A brief explanation for your status decision, referencing the new review."
    }
  ],
  "new_issues_introduced": [
    {
      "issue": "Description of any new issues found in the new review that weren't in the previous review",
      "severity": "Critical | High | Medium | Low",
      "line_number": "Line number if available",
      "filename": "Filename if available"
    }
  ],
  "overall_improvement": "IMPROVED | NEUTRAL | WORSENED",
  "quality_trend": "Quality score trend analysis comparing previous vs current review"
}

STRICTLY provide the result within 3000 characters. DO NOT exceed the character limit.
"""

def get_changed_python_files(folder_path=None):
    """
    Dynamically get all Python AND SQL files from the specified folder or scripts directory.
    Uses wildcard pattern matching for flexibility.
    """
    # If no folder specified, use the scripts directory
    if not folder_path:
        folder_path = SCRIPTS_DIRECTORY
       
    if not os.path.exists(folder_path):
        print(f"❌ Directory {folder_path} not found")
        return []
   
    all_files = []
   
    # Process both Python and SQL files
    for pattern in FILE_PATTERNS:
        # Use glob pattern to find files
        pattern_path = os.path.join(folder_path, pattern)
        found_files = glob.glob(pattern_path)
       
        # Also check subdirectories recursively
        recursive_pattern = os.path.join(folder_path, "**", pattern)
        found_files.extend(glob.glob(recursive_pattern, recursive=True))
       
        all_files.extend(found_files)
   
    # Remove duplicates and sort
    all_files = sorted(list(set(all_files)))
   
    print(f"📁 Found {len(all_files)} code files in {folder_path} using patterns {FILE_PATTERNS}:")
    for file in all_files:
        file_type = "SQL" if file.lower().endswith('.sql') else "Python"
        print(f"  - {file} ({file_type})")
   
    return all_files

def build_prompt_for_individual_review(code_text: str, filename: str = "code_file") -> str:
    prompt = PROMPT_TEMPLATE_INDIVIDUAL.replace("{PY_CONTENT}", code_text)
    prompt = prompt.replace("{filename}", filename)
    return prompt

def build_prompt_for_consolidated_summary(all_reviews_content: str, previous_context: str = None, pr_number: int = None) -> str:
    if previous_context and pr_number:
        prompt = PROMPT_TEMPLATE_WITH_CONTEXT.replace("{previous_context}", previous_context)
        prompt = prompt.replace("{pr_number}", str(pr_number))
        prompt = prompt.replace("{consolidated_template}", PROMPT_TEMPLATE_CONSOLIDATED)
        prompt = prompt.replace("{ALL_REVIEWS_CONTENT}", all_reviews_content)
    else:
        prompt = PROMPT_TEMPLATE_CONSOLIDATED.replace("{ALL_REVIEWS_CONTENT}", all_reviews_content)
    return prompt

def review_with_cortex(model, prompt_text: str, session) -> str:
    try:
        clean_prompt = prompt_text.replace("'", "''").replace("\\", "\\\\")
        query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{clean_prompt}') as response"
        df = session.sql(query)
        result = df.collect()[0][0]
        return result
    except Exception as e:
        print(f"Error calling Cortex complete for model '{model}': {e}", file=sys.stderr)
        return f"ERROR: Could not get response from Cortex. Reason: {e}"

def chunk_large_file(code_text: str, max_chunk_size: int = 50000) -> list:
    if len(code_text) <= max_chunk_size:
        return [code_text]
   
    lines = code_text.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0
   
    for line in lines:
        line_size = len(line) + 1
        if current_size + line_size > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size
   
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
   
    return chunks

def calculate_executive_quality_score(findings: list, total_lines_of_code: int) -> int:
    """
    Executive-level rule-based quality scoring (0-100).
    MUCH MORE BALANCED - Fixed overly harsh scoring.
   
    Scoring Logic (REALISTIC):
    - Start with base score of 100
    - Reasonable deductions that won't hit zero easily
    - Focus on actionable scoring for executives
    """
    if not findings or len(findings) == 0:
        return 100
   
    base_score = 100
    total_deductions = 0
   
    # MUCH MORE BALANCED severity weightings
    severity_weights = {
        "Critical": 12,    # Each critical issue deducts 12 points (but there should be very few)
        "High": 4,         # Each high issue deducts 4 points
        "Medium": 1.5,     # Each medium issue deducts 1.5 points
        "Low": 0.3         # Each low issue deducts 0.3 points
    }
   
    # Count issues by severity - STRICT PRECISION (NO CONVERSION)
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    total_affected_lines = 0
   
    print(f"  📊 Scoring {len(findings)} findings...")
   
    for finding in findings:
        severity = str(finding.get("severity", "")).strip()  # Keep original case
       
        # STRICT MATCHING - NO CONVERSION TO MEDIUM
        if severity == "Critical":
            severity_counts["Critical"] += 1
        elif severity == "High":
            severity_counts["High"] += 1
        elif severity == "Medium":
            severity_counts["Medium"] += 1
        elif severity == "Low":
            severity_counts["Low"] += 1
        else:
            # LOG UNRECOGNIZED SEVERITY BUT DON'T COUNT IT
            print(f"    ⚠️ UNRECOGNIZED SEVERITY: '{severity}' in finding: {finding.get('finding', 'Unknown')[:50]}... - SKIPPING")
            continue  # Skip this finding entirely instead of converting
           
        print(f"    - {severity}: {finding.get('finding', 'No description')[:50]}...")
       
        # Count affected lines (treat N/A as 1 line)
        line_num = finding.get("line_number", "N/A")
        total_affected_lines += 1
   
    print(f"  📈 Severity breakdown: Critical={severity_counts['Critical']}, High={severity_counts['High']}, Medium={severity_counts['Medium']}, Low={severity_counts['Low']}")
   
    # Calculate REALISTIC deductions from severity
    for severity, count in severity_counts.items():
        if count > 0:
            weight = severity_weights[severity]
           
            # MUCH MORE BALANCED progressive penalty
            if severity == "Critical":
                # Critical: Should be very rare, but high impact
                if count <= 2:
                    deduction = weight * count
                else:
                    deduction = weight * 2 + (count - 2) * (weight + 3)
                # Cap critical deductions at 30 points max
                deduction = min(30, deduction)
            elif severity == "High":
                # High: Linear scaling with small bonus after 10 issues
                if count <= 10:
                    deduction = weight * count
                else:
                    deduction = weight * 10 + (count - 10) * (weight + 1)
                # Cap high severity deductions at 25 points max
                deduction = min(25, deduction)
            else:
                # Medium/Low: Pure linear scaling with caps
                deduction = weight * count
                # Reasonable caps
                if severity == "Medium":
                    deduction = min(20, deduction)
                else:
                    deduction = min(10, deduction)
               
            total_deductions += deduction
            print(f"    {severity}: {count} issues = -{deduction:.1f} points (capped)")
   
    # MUCH REDUCED penalties
    if total_lines_of_code > 0:
        affected_ratio = total_affected_lines / total_lines_of_code
        if affected_ratio > 0.4:  # Only penalize if more than 40% affected
            coverage_penalty = min(5, int(affected_ratio * 20))  # Max 5 point penalty
            total_deductions += coverage_penalty
            print(f"    Coverage penalty: -{coverage_penalty} points ({affected_ratio:.1%} affected)")
   
    # REALISTIC critical threshold penalties (should rarely trigger)
    if severity_counts["Critical"] >= 3:  # Very high threshold
        total_deductions += 10
        print(f"    Executive threshold penalty: -10 points (3+ critical issues)")
   
    if severity_counts["Critical"] + severity_counts["High"] >= 20:  # High threshold
        total_deductions += 5
        print(f"    Production readiness penalty: -5 points (20+ critical/high issues)")
   
    # Calculate final score
    final_score = max(0, base_score - int(total_deductions))
   
    print(f"  🎯 Final calculation: {base_score} - {int(total_deductions)} = {final_score}")
   
    # ADJUSTED executive score bands for more realistic scoring
    if final_score >= 85:
        return min(100, final_score)  # Excellent
    elif final_score >= 70:
        return final_score  # Good
    elif final_score >= 50:
        return final_score  # Fair - needs attention
    else:
        return max(30, final_score)  # Poor - but never below 30 for functional code

def setup_review_log_table():
    """ENHANCED: Setup the review log table with VARIANT columns and comparison_result field"""
    global database_available
   
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

def store_review_log(pull_request_number, commit_sha, executive_summary, consolidated_json, processed_files, comparison_result=None):
    """ENHANCED: Store review with VARIANT columns, comparison_result, and APPEND (don't overwrite)"""
    global database_available
   
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

def get_previous_review(pull_request_number):
    """ENHANCED: Get previous review with line numbers and filenames from detailed findings"""
    global database_available
   
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
           
            # Build detailed previous context with line numbers and filenames
            previous_context = f"""Previous Review Summary:
{json.dumps(review_summary, indent=2)[:1500]}

Previous Detailed Findings with Line Numbers and Filenames:
"""
           
            # Include line numbers, filenames and detailed info for each finding
            for i, finding in enumerate(findings_json[:10]):  # Limit to first 10 findings
                line_num = finding.get('line_number', 'N/A')
                filename = finding.get('filename', 'N/A')  # ENHANCED: Include filename
                severity = finding.get('severity', 'Unknown')
                issue = finding.get('finding', 'No description')[:100]  # Truncate long descriptions
               
                previous_context += f"""
{i+1}. [{severity}] {filename}:{line_num} - {issue}
"""
           
            print(f"  📋 Retrieved previous review from {row['REVIEW_TIMESTAMP']} with line numbers and filenames")
            return previous_context
        else:
            print("  📋 No previous review found for this PR")
            return None
           
    except Exception as e:
        print(f"  ⚠️ Error retrieving previous review: {e}")
        return None

def get_llm_comparison(model: str, prompt_messages: str, session):
    """ENHANCED: Uses an LLM to compare two reviews and returns the structured result."""
    print("🔄 Performing LLM comparison of reviews...")
    try:
        review = review_with_cortex(model, prompt_messages, session)
        print(f"📊 LLM comparison response received: {len(review)} characters")
       
        # Try to parse as JSON
        try:
            comparison_result = json.loads(review)
            print("✅ LLM comparison successfully parsed as JSON")
            return comparison_result
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed, attempting to extract JSON from response: {e}")
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', review, re.DOTALL)
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

def fetch_last_review_for_comparison(session, pr_number):
    """Fetches the most recent review for a given PR number for comparison purposes"""
    global database_available
   
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
            # Extract the review summary as string for comparison
            review_summary = str(row['REVIEW_SUMMARY']) if row['REVIEW_SUMMARY'] else None
            print(f"📋 Retrieved last review for comparison from {row['REVIEW_TIMESTAMP']}")
            return review_summary
        else:
            print("📋 No previous review found for comparison")
            return None
           
    except Exception as e:
        print(f"❌ Error fetching last review for comparison: {e}")
        return None

def format_executive_pr_display(json_response: dict, processed_files: list) -> str:
    summary = json_response.get("executive_summary", "Technical analysis completed")
    findings = json_response.get("detailed_findings", [])
    quality_score = json_response.get("quality_score", 75)
    business_impact = json_response.get("business_impact", "MEDIUM")
    security_risk = json_response.get("security_risk_level", "MEDIUM")
    tech_debt = json_response.get("technical_debt_score", "MEDIUM")
    maintainability = json_response.get("maintainability_rating", "FAIR")
    metrics = json_response.get("metrics", {})
    strategic_recs = json_response.get("strategic_recommendations", [])
    immediate_actions = json_response.get("immediate_actions", [])
    previous_issues = json_response.get("previous_issues_resolved", [])
   
    critical_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "CRITICAL")
    high_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "HIGH")
    medium_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "MEDIUM")
    low_count = sum(1 for f in findings if str(f.get("severity", "")).upper() == "LOW")
   
    # Count by file type for better reporting
    python_files = [f for f in processed_files if f.lower().endswith('.py')]
    sql_files = [f for f in processed_files if f.lower().endswith('.sql')]
   
    # Count critical/high issues by file type
    python_critical = sum(1 for f in findings if f.get("filename", "").lower().endswith('.py') and str(f.get("severity", "")).upper() == "CRITICAL")
    python_high = sum(1 for f in findings if f.get("filename", "").lower().endswith('.py') and str(f.get("severity", "")).upper() == "HIGH")
    sql_critical = sum(1 for f in findings if f.get("filename", "").lower().endswith('.sql') and str(f.get("severity", "")).upper() == "CRITICAL")
    sql_high = sum(1 for f in findings if f.get("filename", "").lower().endswith('.sql') and str(f.get("severity", "")).upper() == "HIGH")
   
    risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
    quality_emoji = "🟢" if quality_score >= 80 else ("🟡" if quality_score >= 60 else "🔴")
   
    # FIXED: Executive Summary - No truncation, just ensure minimum 30 characters
    if len(summary) < 30:
        summary = summary + " Code review analysis completed."
   
    display_text = f"""# 📊 Executive Code Review Report

**Files Analyzed:** {len(processed_files)} files | **Analysis Date:** {datetime.now().strftime('%Y-%m-%d')} | **Database:** {current_database}.{current_schema}

## 🎯 Executive Summary
{summary}

## 📈 Quality Dashboard

| Metric | Score | Status | Business Impact |
|--------|-------|--------|-----------------|
| **Overall Quality** | {quality_score}/100 | {quality_emoji} | {business_impact} Risk |
| **Security Risk** | {security_risk} | {risk_emoji.get(security_risk, "🟡")} | Critical security concerns |
| **Technical Debt** | {tech_debt} | {risk_emoji.get(tech_debt, "🟡")} | {len(findings)} items |
| **Maintainability** | {maintainability} | {risk_emoji.get(maintainability, "🟡")} | Long-term sustainability |

## 🔍 Issue Distribution

| Severity | Count | Priority Actions |
|----------|-------|------------------|
| 🔴 Critical | {critical_count} | Immediate fix required |
| 🟠 High | {high_count} | Fix within sprint |
| 🟡 Medium | {medium_count} | Plan for next release |
| 🟢 Low | {low_count} | Technical improvement |

## 📁 File Analysis Breakdown

| File Type | Count | Critical Issues | High Issues |
|-----------|-------|----------------|-------------|
| 🐍 Python | {len(python_files)} | {python_critical} | {python_high} |
| 🗄️ SQL | {len(sql_files)} | {sql_critical} | {sql_high} |

"""

    # ENHANCED: Previous issues resolution status WITH LINE NUMBERS AND FILENAMES
    if previous_issues:
        display_text += """<details>
<summary><strong>📈 Previous Issues Resolution Status</strong> (Click to expand)</summary>

| Previous Issue | File | Line | Status | Details |
|----------------|------|------|--------|---------|
"""
        for issue in previous_issues:
            status = issue.get("status", "UNKNOWN")
            status_emoji = {"RESOLVED": "✅", "PARTIALLY_RESOLVED": "⚠️", "NOT_ADDRESSED": "❌", "WORSENED": "🔴"}.get(status, "❓")
           
            original_display = issue.get("original_issue", "")
            filename = issue.get("filename", "N/A")  # ENHANCED: Include filename
            line_number = issue.get("line_number", "N/A")
            details_display = issue.get("details", "")
           
            display_text += f"| {original_display} | {filename} | {line_number} | {status_emoji} {status} | {details_display} |\n"
       
        display_text += "\n</details>\n\n"

    # FILTER OUT LOW PRIORITY ISSUES from Current Review Findings
    non_low_findings = [f for f in findings if str(f.get("severity", "")).upper() != "LOW"]
   
    if non_low_findings:
        display_text += """<details>
<summary><strong>🔍 Current Review Findings</strong> (Click to expand)</summary>

| Priority | File | Line | Issue | Business Impact |
|----------|------|------|-------|-----------------|
"""
       
        severity_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        sorted_findings = sorted(non_low_findings, key=lambda x: severity_order.get(str(x.get("severity", "Low")), 4))
       
        for finding in sorted_findings[:20]:  # Show top 20 non-low findings
            severity = str(finding.get("severity", "Medium"))
            filename = finding.get("filename", "N/A")
            line = finding.get("line_number", "N/A")
           
            issue_display = str(finding.get("finding", ""))
            business_impact_display = str(finding.get("business_impact", ""))
           
            priority_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(severity, "🟡")
           
            display_text += f"| {priority_emoji} {severity} | {filename} | {line} | {issue_display} | {business_impact_display} |\n"
       
        display_text += "\n</details>\n\n"

    if immediate_actions:
        display_text += """<details>
<summary><strong>⚡ Immediate Actions Required</strong> (Click to expand)</summary>

"""
        for i, action in enumerate(immediate_actions, 1):
            display_text += f"{i}. {action}\n"
        display_text += "\n</details>\n\n"

    display_text += f"""---

**📋 Review Summary:** {len(findings)} findings identified | **🎯 Quality Score:** {quality_score}/100 | **⚡ Critical Issues:** {critical_count}

*🔬 Powered by Snowflake Cortex AI • Two-Stage Executive Analysis • Stored in {current_database}.{current_schema}*"""

    return display_text

def main():
    print(f"🚀 Starting Cortex Code Review System")
    print(f"📋 Configuration: {cfg['account']} | User: {cfg['user']} | Database: {cfg.get('database', 'N/A')}")
    
    if len(sys.argv) >= 5:
        output_folder_path = sys.argv[2]  # Keep output folder from args
        try:
            pull_request_number = int(sys.argv[3]) if sys.argv[3] and sys.argv[3].strip() else None
        except (ValueError, IndexError):
            print(f"⚠️  Warning: Invalid or empty PR number '{sys.argv[3] if len(sys.argv) > 3 else 'None'}', using None")
            pull_request_number = None
        commit_sha = sys.argv[4]
        directory_mode = True
       
        # ALWAYS use scripts directory regardless of first argument
        print(f"📁 Command line mode: Using {SCRIPTS_DIRECTORY} directory instead of '{sys.argv[1]}'")
        code_files = get_changed_python_files(SCRIPTS_DIRECTORY)
        if not code_files:
            print(f"❌ No Python/SQL files found in {SCRIPTS_DIRECTORY} directory using patterns {FILE_PATTERNS}")
            return
           
        folder_path = SCRIPTS_DIRECTORY  # Always use scripts directory
           
    else:
        # Fallback for single file mode - use scripts directory with wildcard pattern
        code_files = get_changed_python_files(SCRIPTS_DIRECTORY)
        if not code_files:
            print(f"❌ No Python/SQL files found in {SCRIPTS_DIRECTORY} directory using patterns {FILE_PATTERNS}")
            return
           
        folder_path = SCRIPTS_DIRECTORY
        output_folder_path = "output_reviews"
        pull_request_number = 0
        commit_sha = "test"
        directory_mode = False
        print(f"Running in dynamic pattern mode with {len(code_files)} code files from {SCRIPTS_DIRECTORY}")

    if os.path.exists(output_folder_path):
        import shutil
        shutil.rmtree(output_folder_path)
    os.makedirs(output_folder_path, exist_ok=True)

    all_individual_reviews = []
    processed_files = []

    print("\n🔍 STAGE 1: Individual File Analysis...")
    print("=" * 60)
   
    for file_path in code_files:
        filename = os.path.basename(file_path)
        print(f"\n--- Reviewing file: {filename} ---")
        processed_files.append(filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            if not code_content.strip():
                review_text = "No code found in file, skipping review."
            else:
                chunks = chunk_large_file(code_content)
                print(f"  File split into {len(chunks)} chunk(s)")
               
                chunk_reviews = []
                for i, chunk in enumerate(chunks):
                    chunk_name = f"{filename}_chunk_{i+1}" if len(chunks) > 1 else filename
                    print(f"  Processing chunk: {chunk_name}")
                   
                    individual_prompt = build_prompt_for_individual_review(chunk, chunk_name)
                    review_text = review_with_cortex(MODEL, individual_prompt, session)
                    chunk_reviews.append(review_text)
               
                if len(chunk_reviews) > 1:
                    review_text = "\n\n".join([f"## Chunk {i+1}\n{review}" for i, review in enumerate(chunk_reviews)])
                else:
                    review_text = chunk_reviews[0]

            all_individual_reviews.append({
                "filename": filename,
                "review_feedback": review_text
            })

            output_filename = f"{Path(filename).stem}_individual_review.md"
            output_file_path = os.path.join(output_folder_path, output_filename)
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(review_text)
            print(f"  ✅ Individual review saved: {output_filename}")

        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
            all_individual_reviews.append({
                "filename": filename,
                "review_feedback": f"ERROR: Could not generate review. Reason: {e}"
            })

    print(f"\n🔄 STAGE 2: Executive Consolidation...")
    print("=" * 60)
    print(f"Consolidating {len(all_individual_reviews)} individual reviews...")

    if not all_individual_reviews:
        print("❌ No reviews to consolidate")
        return

    try:
        # Setup the review log table with comparison_result field
        if database_available:
            setup_review_log_table()

        # Get previous review context if available
        previous_review_context = None
        if pull_request_number and pull_request_number != 0 and database_available:
            previous_review_context = get_previous_review(pull_request_number)
            if previous_review_context:
                print("  📋 This is a subsequent commit review with previous context")
            else:
                print("  📋 This is the initial commit review")
        elif not database_available:
            print("  ⚠️ Database not available - cannot retrieve previous reviews")

        combined_reviews_json = json.dumps(all_individual_reviews, indent=2)
        print(f"  Combined reviews: {len(combined_reviews_json)} characters")

        # Generate consolidation prompt with or without previous context
        consolidation_prompt = build_prompt_for_consolidated_summary(
            combined_reviews_json,
            previous_review_context,
            pull_request_number
        )
        consolidation_prompt = consolidation_prompt.replace("{MAX_CHARS_FOR_FINAL_SUMMARY_FILE}", str(MAX_CHARS_FOR_FINAL_SUMMARY_FILE))
        consolidated_raw = review_with_cortex(MODEL, consolidation_prompt, session)
       
        try:
            consolidated_json = json.loads(consolidated_raw)
            print("  ✅ Successfully parsed consolidated JSON response")
           
        except json.JSONDecodeError as e:
            print(f"  ⚠️ JSON parsing failed: {e}")
            print(f"  📝 Raw response preview: {consolidated_raw[:500]}...")
           
            # ENHANCED: Multiple JSON extraction strategies
            consolidated_json = None
           
            # Strategy 1: Find JSON between ```json and ```
            json_code_match = re.search(r'```json\s*(\{.*?\})\s*```', consolidated_raw, re.DOTALL)
            if json_code_match:
                try:
                    consolidated_json = json.loads(json_code_match.group(1))
                    print("  ✅ Successfully extracted JSON from code block")
                except json.JSONDecodeError:
                    pass
           
            # Strategy 2: Find largest JSON-like structure
            if not consolidated_json:
                json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', consolidated_raw, re.DOTALL)
                for match in sorted(json_matches, key=len, reverse=True):
                    try:
                        consolidated_json = json.loads(match)
                        print("  ✅ Successfully extracted JSON using pattern matching")
                        break
                    except json.JSONDecodeError:
                        continue
           
            # Strategy 3: Clean and fix common JSON issues
            if not consolidated_json:
                try:
                    # Common fixes for malformed JSON
                    cleaned_json = consolidated_raw
                    # Fix trailing commas
                    cleaned_json = re.sub(r',(\s*[}\]])', r'\1', cleaned_json)
                    # Fix unquoted keys (basic cases)
                    cleaned_json = re.sub(r'(\w+):', r'"\1":', cleaned_json)
                    # Extract first complete JSON object
                    json_match = re.search(r'\{.*\}', cleaned_json, re.DOTALL)
                    if json_match:
                        consolidated_json = json.loads(json_match.group())
                        print("  ✅ Successfully parsed cleaned JSON")
                except json.JSONDecodeError:
                    pass
           
            # Strategy 4: Fallback with basic structure
            if not consolidated_json:
                print("  ❌ All JSON parsing strategies failed, using fallback")
                consolidated_json = {
                    "executive_summary": "JSON parsing failed - analysis completed with " + str(len(all_individual_reviews)) + " files reviewed",
                    "quality_score": 75,
                    "business_impact": "MEDIUM",
                    "technical_debt_score": "MEDIUM",
                    "security_risk_level": "MEDIUM",
                    "maintainability_rating": "FAIR",
                    "detailed_findings": [],
                    "metrics": {"lines_of_code": 0, "complexity_score": "MEDIUM", "code_coverage_gaps": [], "dependency_risks": []},
                    "strategic_recommendations": ["Review LLM output formatting", "Implement JSON validation"],
                    "immediate_actions": ["Fix JSON parsing issues"],
                    "previous_issues_resolved": []
                }
       
        # ALWAYS calculate rule-based quality score
        findings = consolidated_json.get("detailed_findings", [])
        total_lines = sum(len(review.get("review_feedback", "").split('\n')) for review in all_individual_reviews)
       
        rule_based_score = calculate_executive_quality_score(findings, total_lines)
        consolidated_json["quality_score"] = rule_based_score
       
        print(f"  🎯 Rule-based quality score calculated: {rule_based_score}/100 (overriding LLM score)")

        executive_summary = format_executive_pr_display(consolidated_json, processed_files)
       
        consolidated_path = os.path.join(output_folder_path, "consolidated_executive_summary.md")
        with open(consolidated_path, 'w', encoding='utf-8') as f:
            f.write(executive_summary)
        print(f"  ✅ Executive summary saved: consolidated_executive_summary.md")

        json_path = os.path.join(output_folder_path, "consolidated_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(consolidated_json, f, indent=2)

        # Generate review_output.json for inline_comment.py compatibility - MOVED AFTER comparison
        critical_findings = [f for f in consolidated_json.get("detailed_findings", []) if str(f.get("severity", "")).upper() == "CRITICAL"]
       
        criticals = []
        for f in critical_findings:
            critical = {
                "line": f.get("line_number", "N/A"),
                "issue": f.get("finding", "Critical issue found"),
                "recommendation": f.get("recommendation", f.get("finding", "")),
                "severity": f.get("severity", "Critical"),
                "filename": f.get("filename", "N/A"),
                "business_impact": f.get("business_impact", "No business impact specified"),
                "description": f.get("finding", "Critical issue found")
            }
            criticals.append(critical)

        # Create a proper critical issues summary for inline_comment.py with CUSTOM FORMAT
        critical_summary = ""
        if critical_findings:
            critical_summary = "Critical Issues Summary:\n"
            for i, finding in enumerate(critical_findings, 1):
                line_num = finding.get("line_number", "N/A")
                # CUSTOM FORMAT: "Critical issues are also posted as inline comments on X line"
                critical_summary += f"* **Line {line_num}:** Critical issues are also posted as inline comments on {line_num} line\n"

        # IMPORTANT: Generate this BEFORE the LLM comparison stage so it's always available
        review_output_data = {
            "full_review": executive_summary,
            "full_review_markdown": executive_summary,
            "full_review_json": consolidated_json,
            "criticals": criticals,
            "critical_summary": critical_summary,
            "critical_count": len(critical_findings),
            "file": processed_files[0] if processed_files else "unknown",
            "timestamp": datetime.now().isoformat()
        }

        with open("review_output.json", "w", encoding='utf-8') as f:
            json.dump(review_output_data, f, indent=2, ensure_ascii=False)
        print("  ✅ review_output.json saved for inline_comment.py compatibility")

        # ENHANCED: LLM-based comparison with previous review
        comparison_result = None
        if pull_request_number and pull_request_number != 0 and database_available:
            print("\n🔄 STAGE 3: LLM Comparison with Previous Review...")
            print("=" * 60)
           
            # Fetch the previous review for comparison
            previous_review_summary = fetch_last_review_for_comparison(session, pull_request_number)
           
            if previous_review_summary:
                print("📋 Previous review found. Performing LLM comparison...")
               
                # Format the comparison prompt using the template from second code
                formatted_prompt = PROMPT_TO_COMPARE_REVIEWS.replace(
                    "{previous_review_text}", str(previous_review_summary)
                ).replace(
                    "{new_review_text}", json.dumps(consolidated_json, indent=2)
                )
               
                # Use the LLM comparison function
                comparison_result = get_llm_comparison(COMPARISON_MODEL, formatted_prompt, session)
               
                if comparison_result:
                    print("✅ LLM comparison successful")
                    print(f"📊 Comparison summary: {comparison_result.get('comparison_summary', 'No summary available')}")
                   
                    # Update consolidated JSON with comparison insights
                    if 'issue_status' in comparison_result:
                        # Convert LLM comparison results to our previous_issues_resolved format
                        previous_issues_resolved = []
                        for issue_status in comparison_result.get('issue_status', []):
                            resolved_issue = {
                                "original_issue": issue_status.get('issue', ''),
                                "line_number": issue_status.get('line_number', 'N/A'),
                                "filename": issue_status.get('filename', 'N/A'),  # ENHANCED: Include filename
                                "status": issue_status.get('status', 'UNKNOWN'),
                                "details": issue_status.get('reasoning', '')
                            }
                            previous_issues_resolved.append(resolved_issue)
                       
                        # Update the consolidated JSON with the comparison results
                        consolidated_json["previous_issues_resolved"] = previous_issues_resolved
                       
                        print(f"📈 Updated consolidated JSON with {len(previous_issues_resolved)} previous issue statuses")
                       
                        # Regenerate executive summary with comparison data
                        executive_summary = format_executive_pr_display(consolidated_json, processed_files)
                       
                        # Update the saved files
                        with open(consolidated_path, 'w', encoding='utf-8') as f:
                            f.write(executive_summary)
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(consolidated_json, f, indent=2)
                       
                        # IMPORTANT: Also update the review_output.json for inline_comment.py compatibility
                        review_output_data["full_review"] = executive_summary
                        review_output_data["full_review_markdown"] = executive_summary
                        review_output_data["full_review_json"] = consolidated_json
                       
                        with open("review_output.json", "w", encoding='utf-8') as f:
                            json.dump(review_output_data, f, indent=2, ensure_ascii=False)
                       
                        print("✅ Updated executive summary, JSON files, and review_output.json with comparison results")
                else:
                    print("⚠️ LLM comparison failed or returned no results")
            else:
                print("📋 No previous review found for comparison - this appears to be the initial review")

        # Store current review for future comparisons - ENHANCED with comparison_result and APPEND mode
        if pull_request_number and pull_request_number != 0 and database_available:
            store_review_log(pull_request_number, commit_sha, executive_summary, consolidated_json, processed_files, comparison_result)

        if 'GITHUB_OUTPUT' in os.environ:
            delimiter = str(uuid.uuid4())
            with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_out:
                gh_out.write(f'consolidated_summary_text<<{delimiter}\n')
                gh_out.write(f'{executive_summary}\n')
                gh_out.write(f'{delimiter}\n')
            print("  ✅ GitHub Actions output written")

        print(f"\n🎉 THREE-STAGE ANALYSIS COMPLETED!")
        print("=" * 60)
        print(f"📁 Files processed: {len(processed_files)}")
        print(f"🔍 Individual reviews: {len(all_individual_reviews)} (STAGE 1)")
        print(f"📊 Executive summary: 1 (STAGE 2)")
        if comparison_result:
            print(f"🔄 LLM comparison: ✅ (STAGE 3)")
            print(f"📈 Issues compared: {len(comparison_result.get('issue_status', []))}")
        else:
            print(f"🔄 LLM comparison: ❌ (No previous review or comparison failed)")
        print(f"🎯 Quality Score: {consolidated_json.get('quality_score', 'N/A')}/100")
        print(f"📈 Findings: {len(consolidated_json.get('detailed_findings', []))}")
       
        if database_available:
            print(f"💾 Database logging: ✅ APPENDED to {current_database}.{current_schema} with comparison_result")
        else:
            print(f"💾 Database logging: ❌ Not available")
       
    except Exception as e:
        print(f"❌ Consolidation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'session' in locals() and session:
            try:
                session.close()
                print("\n🔒 Snowflake session closed")
            except:
                pass
code.txt
Displaying code.txt.
