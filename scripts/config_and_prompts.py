# config_and_prompts.py

# ---------------------
# Config
# ---------------------
MODEL = "openai-gpt-4.1"
COMPARISON_MODEL = "claude-3-5-sonnet"
MAX_CHARS_FOR_FINAL_SUMMARY_FILE = 65000
MAX_TOKENS_FOR_SUMMARY_INPUT = 100000

# Dynamic file pattern - processes all Python AND SQL files in scripts directory
SCRIPTS_DIRECTORY = "test"  # Base directory to scan
FILE_PATTERNS = ["*.py", "*.sql"]  # CHANGED: Added SQL files

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
