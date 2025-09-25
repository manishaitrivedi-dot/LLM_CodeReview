# review_engine.py

import os, sys, json, re, glob
from pathlib import Path
from config_and_prompts import *

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

def chunk_large_file(code_text: str, max_chunk_size: int = 95000) -> list:
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
