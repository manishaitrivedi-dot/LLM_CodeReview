import os, sys, json, re, uuid
#import snowflake.connector
from textwrap import dedent
from pathlib import Path
from snowflake.snowpark import Session
from snowflake.cortex import complete
from snowflake.cortex._complete import CompleteOptions
import tiktoken
import pandas as pd
from datetime import datetime

# ---------------------
# Config
# ---------------------
MODEL = "openai-gpt-4.1"
MAX_CHARS_FOR_FINAL_SUMMARY_FILE = 62000
MAX_TOKENS_FOR_SUMMARY_INPUT = 100000
#FILE_TO_REVIEW = "scripts/simple_test.py"

# ---------------------
# Snowflake session
# ---------------------
cfg = {
    "account": "XKB93357.us-west-2",
    "user": "MANISHAT007", 
    "password": "Welcome@987654321",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "MY_DB",
    "schema": "PUBLIC",
}
session = Session.builder.configs(cfg).create()

# ---------------------
# PROMPT TEMPLATES
# ---------------------
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
*A 2-3 sentence high-level summary. Mention the key strengths and the most critical areas for improvement.*

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
PROMPT_TEMPLATE_SQL_INDIVIDUAL ="""
Please act as a principal-level SQL and Database Engineer. Your review must be concise, accurate, and directly actionable, as it will be posted as a GitHub Pull Request comment.

CONTEXT: HOW TO REVIEW (Apply Silently)
1) You are reviewing a SQL script for executive-level analysis. Focus on business impact, data integrity, security risks, performance, and maintainability.
2) Focus your review on the most critical aspects. Prioritize findings that have business impact, data loss risks, or security implications.
3) Infer context from the full script. Base your review on the complete file provided, assuming the implied schema is correct.
4) Your entire response MUST be under 65,000 characters. Include findings of all severities but prioritize Critical and High severity issues.

REVIEW PRIORITIES (Strict Order)
1) Security & Correctness: (e.g., SQL injection risks, data type mismatches, incorrect logic leading to data corruption).
2) Data Integrity & Reliability: (e.g., Proper transaction handling, constraints, handling of edge cases).
3) Performance & Scalability: (e.g., Inefficient joins, missing indexes, non-sargable predicates, table scan issues).
4) Readability & Maintainability: (e.g., Consistent formatting, clear aliasing, use of CTEs, comments for complex logic).
5) Modularity & Reusability: (e.g., Potential for abstraction into views or stored procedures).

SEVERITY GUIDELINES (Be Realistic and Balanced - MOST ISSUES SHOULD BE MEDIUM OR LOW)
    -   **Critical:** ONLY for security vulnerabilities (like SQL injection), data loss risks, or actions that could cause a production outage.
    -   **High:** ONLY for major performance bottlenecks under load, incorrect results, or significant data integrity concerns.
    -   **Medium:** Code quality improvements, minor performance issues, maintainability concerns, lack of clarity.
    -   **Low:** Style improvements, minor optimizations, non-critical suggestions, formatting inconsistencies.

REALISTIC SEVERITY DISTRIBUTION (MANDATORY):
    -  Critical: 0-5% of findings (very rare)
    -  High: 10-20% of findings
    -  Medium: 40-50% of findings (most common)
    -  Low: 30-40% of findings (common)

ELIGIBILITY CRITERIA FOR FINDINGS (ALL must be met)
    -   **Evidence:** Quote the exact code snippet and cite the line number.
    -   **Severity:** Assign {Low | Medium | High | Critical} - BE REALISTIC, most issues should be Medium or Low.
    -   **Impact & Action:** Briefly explain the issue and provide a minimal, safe correction.
    -   **Non-trivial:** Skip purely stylistic nits (e.g., capitalization of keywords, trailing commas) that a formatter would catch.

HARD CONSTRAINTS (For accuracy & anti-hallucination)
1) Do NOT propose non-standard SQL functions or syntax that are not compatible with the inferred SQL dialect (e.g., PostgreSQL, T-SQL, etc.).
2) Assume the table schema is as implied by the query. Do NOT invent columns or tables that are not used.
3) Focus on the provided script. Do NOT suggest broad architectural changes like switching database systems.
4) Recognize common patterns like temporary tables or CTEs and review them for correctness and efficiency.
5) If the SQL is already correct and optimized, do NOT invent problems.
6) DO NOT inflate severity levels - be conservative and realistic.

OUTPUT FORMAT (Strict, professional, audit-ready)
Your entire response MUST be under 65,000 characters. Include findings of all severity levels with realistic severity assignments.

Code Review Summary
A 2-3 sentence high-level summary. Mention the key strengths and the most critical areas for improvement in terms of performance and correctness.

Detailed Findings
A list of all material findings. If no significant issues are found, state "No significant issues found."

File: {filename}

Severity: {Critical | High | Medium | Low}

Line: {line_number}

Query/Object Context: {CTE_name, Stored_Procedure_name, or relevant SELECT block}

Finding: {A clear, concise description of the issue, its impact, and a recommended correction.}

(Repeat for each finding)

Key Recommendations
Provide 2-3 high-level, actionable recommendations for improving the overall quality of the SQL codebase based on the findings. Do not repeat the findings themselves.

CODE TO REVIEW
{SQL_CONTENT}
"""

PROMPT_TEMPLATE_CONSOLIDATED = """
You are an expert code review summarization engine for executive-level reporting. Your task is to analyze a collection of individual code reviews for both Python and SQL files and generate a single, consolidated executive summary with a business impact focus.

You MUST respond ONLY with a valid JSON object that conforms to the executive schema. Do not include any other text, explanations, or markdown formatting outside of the JSON structure.

Follow these instructions to populate the JSON fields:

1.  **`executive_summary` (string):** Write a 1-2 sentence high-level summary of the entire code change, covering the most important findings across all files with business impact focus.
2.  **`quality_score` (number):** Assign an overall quality score (0-100) based on severity and number of findings.
3.  **`business_impact` (string):** Assess overall business risk as "LOW", "MEDIUM", or "HIGH".
4.  **`technical_debt_score` (string):** Evaluate technical debt as "LOW", "MEDIUM", or "HIGH".
5.  **`security_risk_level` (string):** Determine security risk as "LOW", "MEDIUM", "HIGH", or "CRITICAL".
6.  **`maintainability_rating` (string):** Rate maintainability as "POOR", "FAIR", "GOOD", or "EXCELLENT".
7.  **`detailed_findings` (array of objects):** Create an array of objects, where each object represents a single, distinct issue found in the code:
         -   **`severity`**: Assign severity realistically: "Low", "Medium", "High", or "Critical". MOST ISSUES SHOULD BE Medium or Low. Only use Critical for security vulnerabilities or data loss risks. Only use High for significant errors or performance issues.
         -   **`category`**: Assign category: "Security", "Performance", "Maintainability", "Best Practices", "Data Integrity", "Query Optimization", "Documentation", or "Error Handling".
         -   **`line_number`**: Extract the specific line number if mentioned in the review. If no line number is available, use "N/A".
         -   **`function_context`**: From the review text, identify the function or class name where the issue is located.(e.g., function/class for Python, stored procedure/CTE for SQL). If not applicable, use "global scope".
         -   **`finding`**: Write a clear, concise description of the issue, its potential impact, and a concrete recommendation.
         -   **`business_impact`**: Explain how this affects business operations or risk.
         -   **`recommendation`**: Provide specific technical solution.
         -   **`effort_estimate`**: Estimate effort as "LOW", "MEDIUM", or "HIGH".
         -   **`priority_ranking`**: Assign priority ranking (1 = highest priority).
         -   **`filename`**: The name of the file where the issue was found.
8.  **`metrics` (object):** Include technical metrics. Populate language-specific sub-sections only if files of that type were reviewed.
         -   **`lines_of_code`**: Total number of lines analyzed across all files.
         -   **`complexity_score`**: "LOW", "MEDIUM", or "HIGH".
         -   **`python_specific (object)`**: Populate this only if Python files were reviewed. Can be an empty object otherwise.
                -  **`code_coverage_gaps`**: Array of areas needing better test coverage.
                -  **`dependency_risks`**: Array of risks related to package dependencies.
         -   **`sql_specific (object)`**: Populate this only if SQL files were reviewed. Can be an empty object otherwise.
                -  **`indexing_opportunities`**: Array of potential columns or queries that would benefit from indexing.
                -  **`schema_dependency_risks`**: Array of risks related to dependencies on specific tables or views.
9. **`immediate_actions` (array of strings):** List critical items requiring immediate attention.
10. **`previous_issues_resolved` (array of objects):** For each issue from previous review, indicate status:
         -   **`original_issue`**: Brief description of the previous issue
         -   **`status`**: "RESOLVED", "PARTIALLY_RESOLVED", "NOT_ADDRESSED", "WORSENED" or "NO_LONGER_APPLICABLE"
         -   **`details`**: Explanation of current status

**CRITICAL INSTRUCTION FOR BALANCED REVIEWS:**
Your entire response MUST be under {MAX_CHARS_FOR_FINAL_SUMMARY_FILE} characters. Include findings of all severity levels with realistic severity assignments:
-   Use "Critical" only for security vulnerabilities, data loss risks, or system crashes
-   Use "High" only for significant error handling gaps or major performance issues  
-   Use "Medium" for code quality improvements and minor performance issues
-   Use "Low" for style improvements and non-critical suggestions
-   REALISTIC DISTRIBUTION: Expect mostly Medium (40-50%) and Low (30-40%) severity findings, with fewer High (10-20%) and very few Critical (0-5%)

Here are the individual code reviews to process:
{ALL_REVIEWS_CONTENT}
"""

PROMPT_TO_COMPARE_REVIEWS = f""" You are an expert AI code review assistant. Your task is to compare a previous code review with a new code review for the same pull request. The developer has pushed new code, attempting to fix the issues mentioned in the previous review.

Analyze if the feedback in the **[NEW REVIEW]** suggests that the specific issues raised in the **[PREVIOUS REVIEW]** have been addressed. Do not just look for the exact same text. Understand the underlying problem described in the previous review and see if the new review sounds positive, different, or no longer mentions that specific problem.

**[PREVIOUS REVIEW]:**
'''
{{previous_review_text}}
'''

**[NEW REVIEW]:**
'''
{{new_review_text}}
'''

CRITICAL INSTRUCTION: You must analyze the new code changes with full awareness of the previous feedback. Specifically:
1. Check if previous Critical/High severity issues were addressed in the new code
2. Identify if any previous recommendations were implemented
3. Note any new issues that may have been introduced
4. Maintain continuity with previous review comments
5. In the "previous_issues_resolved" section, provide specific status for each previous issue
**[YOUR TASK]:**
Provide your analysis in a structured JSON format. For each major issue identified in the **[PREVIOUS REVIEW]**, determine its status based on the **[NEW REVIEW]**. The possible statuses are:

- **"RESOLVED"**: The issue is no longer mentioned in the new review, or the new review provides positive feedback on that area.
- **"PARTIALLY_RESOLVED"**: The new review indicates some improvement but mentions that the issue is not fully fixed.
- **"NOT_ADDRESSED"**: The new review repeats the same criticism or feedback.
- **"WORSENED"**: inspite of rectifying the issue, some new errors are added to the code, which made it worsened.
- **"NO_LONGER_APPLICABLE"**: The code related to the original feedback was removed or changed so significantly that the feedback doesn't apply.

The JSON output should follow this exact structure:
{{
  "comparison_summary": "A brief, one-sentence summary of whether the developer addressed the feedback.",
  "issue_status": [
    {{
      "issue": "A concise summary of the original issue from the previous review.",
      "status": "Resolved | Partially Resolved | Not Resolved | No Longer Applicable",
      "reasoning": "A brief explanation for your status decision, referencing the new review."
    }}
  ]
}}
STRICTLY provide the result within 3000 characters. DO NOT exceed the character limit.
"""

def build_prompt_for_individual_review(code_text: str, filename: str) -> str:
    if filename.endswith((".py"):
        prompt = PROMPT_TEMPLATE_PYTHON_INDIVIDUAL.replace("{PY_CONTENT}", code_text)
    elif filename.endswith((".sql"):
        prompt = PROMPT_TEMPLATE_SQL_INDIVIDUAL.replace("{SQL_CONTENT}", code_text)
    prompt = prompt.replace("{filename}", filename)
    return prompt

def build_prompt_for_consolidated_summary(all_reviews_content: str) -> str:
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
        "Critical": 8,     # Each critical issue deducts 8 points (was 15)
        "High": 3,         # Each high issue deducts 3 points (was 6)
        "Medium": 1.5,     # Each medium issue deducts 1.5 points (was 3)
        "Low": 0.5         # Each low issue deducts 0.5 points (was 1)
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
                # Critical: 8, 12, 16, 20 for 1,2,3,4 issues (much more reasonable)
                if count <= 3:
                    deduction = weight * count
                else:
                    deduction = weight * 3 + (count - 3) * (weight + 2)
                # Cap critical deductions at 25 points max (was 50)
                deduction = min(25, deduction)
            elif severity == "High":
                # High: Linear scaling with small bonus after 8 issues
                if count <= 8:
                    deduction = weight * count
                else:
                    deduction = weight * 8 + (count - 8) * (weight + 1)
                # Cap high severity deductions at 20 points max (was 40)
                deduction = min(20, deduction)
            else:
                # Medium/Low: Pure linear scaling with caps
                deduction = weight * count
                # Much lower caps
                if severity == "Medium":
                    deduction = min(15, deduction)  # Was 20
                else:
                    deduction = min(8, deduction)   # Was 10
                
            total_deductions += deduction
            print(f"    {severity}: {count} issues = -{deduction:.1f} points (capped)")
    
    # MUCH REDUCED penalties
    if total_lines_of_code > 0:
        affected_ratio = total_affected_lines / total_lines_of_code
        if affected_ratio > 0.3:  # Only penalize if more than 30% affected (was 20%)
            coverage_penalty = min(5, int(affected_ratio * 25))  # Max 5 point penalty (was 10)
            total_deductions += coverage_penalty
            print(f"    Coverage penalty: -{coverage_penalty} points ({affected_ratio:.1%} affected)")
    
    # MUCH REDUCED critical threshold penalties
    if severity_counts["Critical"] >= 10:  # Raised threshold from 5 to 10
        total_deductions += 8  # Reduced from 15 to 8
        print(f"    Executive threshold penalty: -8 points (10+ critical issues)")
    
    if severity_counts["Critical"] + severity_counts["High"] >= 25:  # Raised from 15 to 25
        total_deductions += 5  # Reduced from 10 to 5
        print(f"    Production readiness penalty: -5 points (25+ critical/high issues)")
    
    # Calculate final score
    final_score = max(0, base_score - int(total_deductions))
    
    print(f"  🎯 Final calculation: {base_score} - {int(total_deductions)} = {final_score}")
    
    # ADJUSTED executive score bands for more realistic scoring
    if final_score >= 85:
        return min(100, final_score)  # Excellent
    elif final_score >= 70:  # Lowered from 65
        return final_score  # Good
    elif final_score >= 50:  # Lowered from 40
        return final_score  # Fair - needs attention
    else:
        return max(25, final_score)  # Poor - but never below 25 for functional code
        
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
    
    risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
    quality_emoji = "🟢" if quality_score >= 80 else ("🟡" if quality_score >= 60 else "🔴")
    
    display_text = f"""# 📊 Executive Code Review Report

**Files Analyzed:** {len(processed_files)} files | **Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}

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

"""

    # Add Critical Issues Summary section if there are critical issues
    critical_findings = [f for f in findings if str(f.get("severity", "")).upper() == "CRITICAL"]
    if critical_findings:
        display_text += """## 🚨 Critical Issues Summary

**⚠️ IMMEDIATE ACTION REQUIRED** - The following critical issues must be addressed before deployment:

"""
        for i, finding in enumerate(critical_findings, 1):
            line_num = finding.get("line_number", "N/A")
            filename = finding.get("filename", "N/A")
            issue_desc = finding.get("finding", "No description available")
            business_impact = finding.get("business_impact", "No business impact specified")
            recommendation = finding.get("recommendation", finding.get("finding", "No recommendation available"))
            
            display_text += f"""**{i}. Critical Issue - Line {line_num}**
- **File:** {filename}
- **Issue:** {issue_desc}
- **Business Impact:** {business_impact}
- **Required Action:** {recommendation}

"""
        display_text += """---

"""
    # Add previous issues resolution status
    if previous_issues:
        display_text += """<details>
<summary><strong>📈 Previous Issues Resolution Status</strong> (Click to expand)</summary>

| Previous Issue | Status | Details |
|----------------|--------|---------|
"""
        for issue in previous_issues:
            status = issue.get("status", "UNKNOWN")
            status_emoji = {"RESOLVED": "✅", "PARTIALLY_RESOLVED": "⚠️", "NOT_ADDRESSED": "❌", "WORSENED": "🔴", "NO_LONGER_APPLICABLE" : "🗑️" }.get(status, "❓")
            original = issue.get("original_issue", "")[:80]
            details = issue.get("details", "")[:100]
            display_text += f"| {original}... | {status_emoji} {status} | {details}... |\n"
        
        display_text += "\n</details>\n\n"

    if findings:
        display_text += """<details>
<summary><strong>🔍 Current Review Findings</strong> (Click to expand)</summary>

| Priority | File | Line | Issue | Business Impact |
|----------|------|------|-------|-----------------|
"""
        
        severity_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        sorted_findings = sorted(findings, key=lambda x: severity_order.get(str(x.get("severity", "Low")), 4))
        
        for finding in sorted_findings[:15]:
            severity = str(finding.get("severity", "Medium"))
            filename = finding.get("filename", "N/A")
            line = finding.get("line_number", "N/A")
            issue = str(finding.get("finding", ""))[:100] + ("..." if len(str(finding.get("finding", ""))) > 100 else "")
            business_impact_text = str(finding.get("business_impact", ""))[:80] + ("..." if len(str(finding.get("business_impact", ""))) > 80 else "")
            
            priority_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(severity, "🟡")
            
            display_text += f"| {priority_emoji} {severity} | {filename} | {line} | {issue} | {business_impact_text} |\n"
        
        display_text += "\n</details>\n\n"

    if strategic_recs:
        display_text += """<details>
<summary><strong>🎯 Strategic Recommendations</strong> (Click to expand)</summary>

"""
        for i, rec in enumerate(strategic_recs, 1):
            display_text += f"{i}. {rec}\n"
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

*🔬 Powered by Snowflake Cortex AI • Two-Stage Executive Analysis*"""

    return display_text

#### code to compare review and save it to snowflake table ####
# def get_llm_comparison(model :str ,  prompt_messages: str,session):
#     """Uses an LLM to compare two reviews and returns the structured result."""
#     # This function does not interact with Snowflake, so no changes are needed.
#     print("get_llm_comparison")
#     try:
#         review = complete(
#           model=model,
#           prompt=prompt_messages,
#           session=session
#           #options=CompleteOptions(temperature=0.2),
#           #response_format={"type": "json_object"}
#       )
#         print("Response of llm comparision", review)
#         return  json.loads(review)
#     except Exception as e:
#         print(f"Error calling LLM for comparison: {e}")
#         return None
            
def fetch_last_review(session, pr_number):
    """Fetches the most recent review for a given PR number."""
    try:
        query = f"""
            SELECT REVIEW_SUMMARY FROM CODE_REVIEW_LOG_NEW
            WHERE PULL_REQUEST_NUMBER = {pr_number}
            ORDER BY REVIEW_TIMESTAMP DESC
            LIMIT 1;
        """
        result = session.sql(query).collect()
        print("fetch_last_review",result[0]["REVIEW_SUMMARY"])
        return result[0]["REVIEW_SUMMARY"] if result else None
    except Exception as e:
        print(f"Error fetching last review: {e}")
        return None
                
def save_review_to_snowflake(session, pr_number: int, commit_sha: str, review_summary: dict, comparison_result : dict = None):
    """
    Saves the code review summary to a dedicated log table in Snowflake.
    Creates the table if it doesn't already exist.
    """
    table_name = "CODE_REVIEW_LOG_NEW"
    print(f"\n--- Attempting to save review to Snowflake table: {table_name} ---")

    try:
        # Step 1: Create the table if it doesn't exist.
        # AUTOINCREMENT handles the "incremental column" requirement automatically.
        # DEFAULT CURRENT_TIMESTAMP() is useful for tracking when the review happened.
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            REVIEW_ID INTEGER AUTOINCREMENT START 1 INCREMENT 1,
            PULL_REQUEST_NUMBER INTEGER,
            COMMIT_SHA VARCHAR(40),
            REVIEW_SUMMARY VARIANT,
            COMPARISON_RESULT VARIANT,
            REVIEW_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        );
        """
        session.sql(create_table_query).collect()
        print(f"  Table '{table_name}' is ready.")

        
        # Step 2: Create a Snowpark DataFrame with the new data.
        # This is the safest way to insert data, preventing SQL injection issues.
        insert_sql = f"""
            INSERT INTO {table_name} 
                (PULL_REQUEST_NUMBER, COMMIT_SHA, REVIEW_SUMMARY, COMPARISON_RESULT)
                SELECT ?, ?, PARSE_JSON(?), PARSE_JSON(?)
        """
        # Step 3: Define the parameters to be safely injected into the '?' placeholders.
        params = [
            pr_number,
            commit_sha,
            json.dumps(review_summary) if review_summary else None,
            json.dumps(comparison_result) if comparison_result else None # <-- FIX 2: Add the 4th parameter and convert it to a JSON string
        ]

        # Step 4: Execute the parameterized query.
        session.sql(insert_sql, params=params).collect()
        print(f"  Successfully saved review for PR #{pr_number} and commit {commit_sha[:7]} to Snowflake.")

    except Exception as e:
        # Log the error but don't fail the whole workflow, as the PR comment is more critical.
        print(f"  ERROR: Could not save review to Snowflake. Reason: {e}", file=sys.stderr)
      
def main():
    if len(sys.argv) >= 5:
        folder_path = sys.argv[1]
        output_folder_path = sys.argv[2]
        try:
            pull_request_number = int(sys.argv[3]) if sys.argv[3] and sys.argv[3].strip() else None
        except (ValueError, IndexError):
            print(f"⚠️  Warning: Invalid or empty PR number '{sys.argv[3] if len(sys.argv) > 3 else 'None'}', using None")
            pull_request_number = None
        commit_sha = sys.argv[4]
        directory_mode = True
    else:
        # folder_path = None
        # output_folder_path = "output_reviews"
        # pull_request_number = 0
        # commit_sha = "test"
        print("Usage: python run_cortex_review.py  <input_directory_path> <output_directory_path> <pr_number> <commit_sha>", file=sys.stderr)
        directory_mode = False
        sys.exit(1)
        
        #print(f"Running in single-file mode with: {FILE_TO_REVIEW}")

    if os.path.exists(output_folder_path):
        import shutil
        shutil.rmtree(output_folder_path)
    os.makedirs(output_folder_path, exist_ok=True)

    all_individual_reviews = []
    processed_files = []

    print("\n🔍 STAGE 1: Individual File Analysis...")
    print("=" * 60)
    
    if directory_mode:
        files_to_process = [f for f in os.listdir(folder_path) if f.endswith((".py", ".sql"))]

    else:
        if not os.path.exists(file_path):
            print(f"❌ File {file_path} not found")
            return
        # files_to_process = [FILE_TO_REVIEW]
        # folder_path = os.path.dirname(FILE_TO_REVIEW)

    for filename in files_to_process:
        if directory_mode:
            file_path = os.path.join(folder_path, filename)
        else:
            file_path = filename
            filename = os.path.basename(filename)
            
        print(f"\n--- Reviewing file: {filename} ---")
        processed_files.append(filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()

            if not code_content.strip():
                review_text = "No code found in file, skipping review."
            else:                  
                individual_prompt = build_prompt_for_individual_review(code_content, filename)
                review_text = review_with_cortex(MODEL, individual_prompt, session)

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
        # CRITICAL: Retrieve previous review context BEFORE generating new review
        
        combined_reviews_json = json.dumps(all_individual_reviews, indent=2)
        print(f"  Combined reviews: {len(combined_reviews_json)} characters")

        # Generate consolidation prompt with or without previous context
        consolidation_prompt = build_prompt_for_consolidated_summary(
            combined_reviews_json
        )
        consolidation_prompt = consolidation_prompt.replace("{MAX_CHARS_FOR_FINAL_SUMMARY_FILE}", str(MAX_CHARS_FOR_FINAL_SUMMARY_FILE))
        consolidated_raw = review_with_cortex(MODEL, consolidation_prompt, session)
        
        try:
            consolidated_json = json.loads(consolidated_raw)
            print("  ✅ Successfully parsed consolidated JSON response")
            # OVERRIDE: Calculate rule-based quality score (don't trust LLM for this)
            findings = consolidated_json.get("detailed_findings", [])
            total_lines = sum(len(review.get("review_feedback", "").split('\n')) for review in all_individual_reviews)
            
            rule_based_score = calculate_executive_quality_score(findings, total_lines)
            consolidated_json["quality_score"] = rule_based_score
            
            print(f"  🎯 Rule-based quality score calculated: {rule_based_score}/100 (overriding LLM score)")
            if len(consolidated_json) > MAX_CHARS_FOR_FINAL_SUMMARY_FILE:
                print(f"Warning: Final consolidated summary exceeds {MAX_CHARS_FOR_FINAL_SUMMARY_FILE} characters. Truncating for file save.", file=sys.stderr)
                consolidated_summary_text = consolidated_json[:MAX_CHARS_FOR_FINAL_SUMMARY_FILE]

                print(f"  Consolidated summary received (first 500 chars): {consolidated_summary_text[:500].strip()}...") 

        except json.JSONDecodeError as e:
            print(f"  ⚠️ JSON parsing failed: {e}")
            json_match = re.search(r'\{.*\}', consolidated_raw, re.DOTALL)
            if json_match:
                consolidated_json = json.loads(json_match.group())
            else:
                consolidated_json = {
                    "executive_summary": "Consolidation failed - using fallback",
                    "quality_score": 75,
                    "business_impact": "LOW",
                    "detailed_findings": [],
                    "strategic_recommendations": [],
                    "immediate_actions": [],
                    "previous_issues_resolved": []
                }

        executive_summary = format_executive_pr_display(consolidated_json, processed_files)
        
        consolidated_path = os.path.join(output_folder_path, "consolidated_executive_summary.md")
        with open(consolidated_path, 'w', encoding='utf-8') as f:
            f.write(executive_summary)
        print(f"  ✅ Executive summary saved: consolidated_executive_summary.md")

        json_path = os.path.join(output_folder_path, "consolidated_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(consolidated_json, f, indent=2)

        # Generate review_output.json for inline_comment.py compatibility
        criticals = []
        for f in consolidated_json.get("detailed_findings", []):
            if str(f.get("severity", "")).upper() == "CRITICAL":
                critical = {
                    "line": f.get("line_number", 1),
                    "issue": f.get("finding", "Critical issue found"),
                    "recommendation": f.get("recommendation", f.get("finding", "")),
                    "severity": f.get("severity", "Critical"),
                    "filename": f.get("filename", "N/A"),
                    "business_impact": f.get("business_impact", "No business impact specified"),
                    "description": f.get("finding", "Critical issue found")  # Add explicit description field
                }
                criticals.append(critical)
        critical_summary = ""
        if critical_findings:
            critical_summary = "Critical Issues Summary:\n"
            for i, finding in enumerate(critical_findings, 1):
                line_num = finding.get("line_number", "N/A")
                issue_desc = finding.get("finding", "Critical issue found")
                critical_summary += f"* **Line {line_num}:** {issue_desc}\n"

        review_output_data = {
            "full_review": executive_summary,
            "full_review_markdown": executive_summary,
            "full_review_json": consolidated_json,
            "criticals": criticals,
            "critical_summary": critical_summary,  # Add explicit critical summary
            "critical_count": len(critical_findings),
            "file": processed_files[0] if processed_files else "unknown",
            "timestamp": datetime.now().isoformat()
        }

        with open("review_output.json", "w", encoding='utf-8') as f:
            json.dump(review_output_data, f, indent=2, ensure_ascii=False)
        print("  ✅ review_output.json saved for inline.py compatibility")

        # Store current review for future comparisons
        print("Fetching last review from Snowflake...")
        previous_review = fetch_last_review(session, pull_request_number)

        comparison_result = None
        if previous_review:
            print("Previous review found. Comparing with the new review...")
            formatted_prompt = PROMPT_TO_COMPARE_REVIEWS.replace(
                "{{previous_review}}",json.dumps(previous_review, indent=2) 
            ).replace(
                "{{new_review}}", json.dumps(consolidated_json, indent=2)
            )
            comparison_result = review_with_cortex('claude-3-5-sonnet',formatted_prompt , session)
                
        if comparison_result:
            print("Comparison successful")
              
        if consolidated_json:
            save_review_to_snowflake(
                    session=session, # Your active Snowpark session object
                    pr_number=pull_request_number,
                    commit_sha=commit_sha,
                    review_summary=consolidated_raw,
                    comparison_result = comparison_result,
                )
            
        if 'GITHUB_OUTPUT' in os.environ:
            delimiter = str(uuid.uuid4())
            with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_out:
                gh_out.write(f'consolidated_summary_text<<{delimiter}\n')
                gh_out.write(f'{executive_summary}\n')
                gh_out.write(f'{delimiter}\n')
            print("  ✅ GitHub Actions output written")

        print(f"\n🎉 TWO-STAGE ANALYSIS COMPLETED!")
        print("=" * 60)
        print(f"📁 Files processed: {len(processed_files)}")
        print(f"🔍 Individual reviews: {len(all_individual_reviews)} (PROMPT 1)")
        print(f"📊 Executive summary: 1 (PROMPT 2)")
        print(f"🎯 Quality Score: {consolidated_json.get('quality_score', 'N/A')}/100")
        print(f"📈 Findings: {len(consolidated_json.get('detailed_findings', []))}")
        if comparison_result:
            print(f"🔄 Previous context included: ✅ Subsequent commit review")
            print(json.loads(comparison_result, indent=2))
        else:
            print(f"🔄 Previous context: ❌ Initial commit review")
        
    except Exception as e:
        print(f"❌ Consolidation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    finally:
        if 'session' in locals():
            session.close()
            print("\n🔒 Session closed")

















