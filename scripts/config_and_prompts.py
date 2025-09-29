# config_and_prompts.py

# ---------------------
# Config
# ---------------------
MODEL = "openai-gpt-4.1"
COMPARISON_MODEL = "claude-3-5-sonnet"
MAX_CHARS_FOR_FINAL_SUMMARY_FILE = 65000
MAX_TOKENS_FOR_SUMMARY_INPUT = 100000

# Dynamic file pattern - processes all Python AND SQL files in scripts directory
SCRIPTS_DIRECTORY = "sql_files"  # Base directory to scan
FILE_PATTERNS = ["*.py", "*.sql"]  # CHANGED: Added SQL files

# ---------------------
# PROMPT TEMPLATES
# ---------------------

# PYTHON-SPECIFIC PROMPT
PROMPT_TEMPLATE_PYTHON_INDIVIDUAL = """Please act as a principal-level Python code reviewer. Your review must be concise, accurate, and directly actionable, as it will be posted as a GitHub Pull Request comment.

---
# CONTEXT: HOW TO REVIEW (Apply Silently)

1.  **You are reviewing a code file for executive-level analysis.** Focus on business impact, technical debt, security risks, and maintainability.
2.  **Focus your review on the most critical aspects.** Prioritize findings that have business impact or security implications.
3.  **Infer context from the full code.** Base your review on the complete file provided.
4.  **Your entire response MUST be under 65,000 characters.** Include findings of all severities but prioritize Critical and High severity issues.

# REVIEW PRIORITIES (Strict Order)
1.  Security & Correctness
2.  Reliability & Error-handling
3.  Performance & Complexity
4.  Readability & Maintainability
5.  Testability

# SEVERITY GUIDELINES (Be Realistic and Balanced - MOST ISSUES SHOULD BE MEDIUM OR LOW)
-   **Critical:** ONLY for security vulnerabilities, data loss risks, system crashes, production outages
-   **High:** ONLY for significant error handling gaps, major performance bottlenecks, security concerns
-   **Medium:** Code quality improvements, minor performance issues, maintainability concerns, documentation gaps
-   **Low:** Style improvements, minor optimizations, non-critical suggestions, cosmetic issues

# REALISTIC SEVERITY DISTRIBUTION (MANDATORY):
- Critical: 0-5% of findings (very rare)
- High: 10-20% of findings 
- Medium: 40-50% of findings (most common)
- Low: 30-40% of findings (common)

# ELIGIBILITY CRITERIA FOR FINDINGS (ALL must be met)
-   **Evidence:** Quote the exact code snippet and cite the line number.
-   **Severity:** Assign {Low | Medium | High | Critical} - BE REALISTIC, most issues should be Medium or Low.
-   **Impact & Action:** Briefly explain the issue and provide a minimal, safe correction.
-   **Non-trivial:** Skip purely stylistic nits (e.g., import order, line length) that a linter would catch.

# HARD CONSTRAINTS (For accuracy & anti-hallucination)
-   Do NOT propose APIs that don't exist for the imported modules.
-   Treat parameters like `db_path` as correct dependency injection; do NOT call them hardcoded.
-   NEVER suggest logging sensitive user data or internal paths. Suggest non-reversible fingerprints if context is needed.
-   Do NOT recommend removing correct type hints or docstrings.
-   If code in the file is already correct and idiomatic, do NOT invent problems.
-   DO NOT inflate severity levels - be conservative and realistic.

---
# OUTPUT FORMAT (Strict, professional, audit-ready)

Your entire response MUST be under 65,000 characters. Include findings of all severity levels with realistic severity assignments.

## Code Review Summary
*A 1-2 sentence high-level summary. Mention the key strengths and the most critical areas for improvement.*

---
### Detailed Findings
*A list of all material findings. If no significant issues are found, state "No significant issues found."*

**File:** {filename}
-   **Severity:** {Critical | High | Medium | Low}
-   **Line:** {line_number}
-   **Function/Context:** `{function_name_if_applicable}`
-   **Finding:** {A clear, concise description of the issue, its impact, and a recommended correction.}

**(Repeat for each finding)**

---
### Key Recommendations
*Provide 2-3 high-level, actionable recommendations for improving the overall quality of the codebase based on the findings. Do not repeat the findings themselves.*

---
# CODE TO REVIEW

{PY_CONTENT}
"""

# SQL-SPECIFIC PROMPT
PROMPT_TEMPLATE_SQL_INDIVIDUAL = """Please act as a principal-level SQL and Database Engineer with expertise in identifying SQL injection vulnerabilities, performance issues, and data integrity problems. Your review must be concise, accurate, and directly actionable, as it will be posted as a GitHub Pull Request comment.

---
# CONTEXT: HOW TO REVIEW (Apply Silently)

1.  **You are reviewing a SQL script for executive-level analysis.** Focus on business impact, data integrity, security risks, performance, and maintainability.
2.  **Focus your review on the most critical aspects.** Prioritize findings that have business impact, data loss risks, or security implications.
3.  **Infer context from the full script.** Base your review on the complete file provided, assuming the implied schema is correct.
4.  **Your entire response MUST be under 65,000 characters.** Include findings of all severities but prioritize Critical and High severity issues.

# REVIEW PRIORITIES (Strict Order)
1.  Security & Correctness (SQL injection risks, data type mismatches, incorrect logic leading to data corruption)
2.  Data Integrity & Reliability (Transaction handling, constraints, edge cases)
3.  Performance & Scalability (Inefficient joins, missing indexes, non-sargable predicates, table scans)
4.  Readability & Maintainability (Consistent formatting, clear aliasing, CTEs, comments)
5.  Modularity & Reusability (Abstraction into views or stored procedures)

# SQL-SPECIFIC SEVERITY GUIDELINES (ENHANCED FOR SQL DETECTION)
-   **Critical:** 
    * SQL injection vulnerabilities with dynamic query construction
    * DELETE/UPDATE without WHERE clause affecting entire tables
    * Data corruption risks from type mismatches or logic errors
    * Production credential exposure in connection strings
    * Dropping tables/databases without proper safeguards
-   **High:** 
    * Major performance bottlenecks (missing indexes on large tables, inefficient joins)
    * Incorrect results from flawed logic
    * Significant data integrity concerns (missing foreign keys, constraints)
    * Transaction handling issues that could cause data inconsistency
-   **Medium:** 
    * Code quality improvements (readability, maintainability)
    * Minor performance issues (suboptimal query patterns)
    * Hardcoded non-production values
    * Missing comments for complex logic
-   **Low:** 
    * Style improvements (formatting, naming conventions)
    * Minor optimizations
    * Non-critical suggestions

# REALISTIC SEVERITY DISTRIBUTION (MANDATORY):
- Critical: 0-10% of findings (rare but SQL can have more critical issues than Python)
- High: 15-25% of findings (SQL performance and integrity issues are common)
- Medium: 40-50% of findings (most common)
- Low: 25-35% of findings

# SQL-SPECIFIC DETECTION PATTERNS
Look specifically for:
- **Dynamic SQL construction** with user input (CRITICAL)
- **Missing WHERE clauses** in UPDATE/DELETE (CRITICAL)
- **Hardcoded production credentials** (CRITICAL)
- **Missing indexes** on frequently queried columns (HIGH)
- **Inefficient JOIN patterns** (MEDIUM-HIGH)
- **Missing transaction boundaries** (HIGH)
- **Data type inconsistencies** (HIGH)
- **Suboptimal query structure** (MEDIUM)

# ELIGIBILITY CRITERIA FOR FINDINGS (ALL must be met)
-   **Evidence:** Quote the exact SQL code snippet and cite the line number.
-   **Severity:** Assign {Low | Medium | High | Critical} - Be more liberal with High/Critical for SQL security and performance issues.
-   **Impact & Action:** Briefly explain the issue and provide a minimal, safe correction.
-   **Non-trivial:** Skip purely stylistic nits (capitalization, trailing commas) that a formatter would catch.

# HARD CONSTRAINTS (For accuracy & anti-hallucination)
-   Do NOT propose non-standard SQL functions or syntax incompatible with the inferred SQL dialect.
-   Assume the table schema is as implied by the query. Do NOT invent columns or tables.
-   Focus on the provided script. Do NOT suggest broad architectural changes.
-   Recognize common patterns like temporary tables or CTEs and review appropriately.
-   If the SQL is already correct and optimized, do NOT invent problems.
-   BE MORE AGGRESSIVE with severity for SQL security and performance issues than Python.

---
# OUTPUT FORMAT (Strict, professional, audit-ready)

Your entire response MUST be under 65,000 characters. Include findings of all severity levels with appropriate SQL-focused severity assignments.

## Code Review Summary
*A 1-2 sentence high-level summary. Mention the key strengths and the most critical areas for improvement in terms of performance, security, and correctness.*

---
### Detailed Findings
*A list of all material findings. If no significant issues are found, state "No significant issues found."*

**File:** {filename}
-   **Severity:** {Critical | High | Medium | Low}
-   **Line:** {line_number}
-   **Function/Context:** `{CTE_name, Stored_Procedure_name, or relevant SELECT block}`
-   **Finding:** {A clear, concise description of the issue, its impact, and a recommended correction.}

**(Repeat for each finding)**

---
### Key Recommendations
*Provide 2-3 high-level, actionable recommendations for improving the overall quality of the SQL codebase based on the findings. Focus on security, performance, and data integrity.*

---
# SQL CODE TO REVIEW

{SQL_CONTENT}
"""

# LEGACY GENERAL PROMPT (kept for backward compatibility)
PROMPT_TEMPLATE_INDIVIDUAL = PROMPT_TEMPLATE_PYTHON_INDIVIDUAL

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
         -   **`severity`**: Assign severity CONSERVATIVELY for Python but MORE AGGRESSIVELY for SQL: "Low", "Medium", "High", or "Critical". For SQL: CRITICAL should be 0-10% of findings (SQL injection, data corruption). For Python: CRITICAL should be 0-5% (security vulnerabilities).
         -   **`category`**: Assign category: "Security", "Performance", "Maintainability", "Best Practices", "Documentation", or "Error Handling".
         -   **`line_number`**: Extract the specific line number if mentioned in the review. If no line number is available, use "N/A".
         -   **`function_context`**: From the review text, identify the function or class name where the issue is located. If not applicable, use "global scope".
         -   **`finding`**: Write a clear, concise description of the issue, its potential impact, and a concrete recommendation.
         -   **`business_impact`**: Explain how this affects business operations or risk. Be more aggressive for SQL issues.
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

**CRITICAL INSTRUCTION FOR SQL vs PYTHON REVIEWS:**
Your entire response MUST be under {MAX_CHARS_FOR_FINAL_SUMMARY_FILE} characters. 

**SQL FILES:** Be more aggressive with High/Critical severity assignments:
-   Use "Critical" for SQL injection, data corruption risks, missing WHERE in DELETE/UPDATE (0-10% of findings)
-   Use "High" for performance bottlenecks, missing indexes, transaction issues (15-25% of findings)
-   Use "Medium" for code quality, suboptimal queries (40-50% of findings)
-   Use "Low" for style, formatting (25-35% of findings)

**PYTHON FILES:** Be conservative with severity assignments:
-   Use "Critical" ONLY for confirmed security vulnerabilities, data loss risks (0-5% of findings)
-   Use "High" for significant error handling gaps, major performance issues (10-20% of findings)
-   Use "Medium" for code quality issues, maintainability concerns (40-50% of findings - MOST COMMON)
-   Use "Low" for style improvements, minor optimizations (30-40% of findings)

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
