# review_engine.py

import os, sys, json, re, glob
from pathlib import Path
from config_and_prompts import *

def get_changed_python_files(folder_path=None):
    """Dynamically get all Python AND SQL files from the specified folder or scripts directory."""
    if not folder_path:
        folder_path = SCRIPTS_DIRECTORY
    if not os.path.exists(folder_path):
        print(f"Directory {folder_path} not found")
        return []
    all_files = []
    for pattern in FILE_PATTERNS:
        pattern_path = os.path.join(folder_path, pattern)
        found_files = glob.glob(pattern_path)
        recursive_pattern = os.path.join(folder_path, "**", pattern)
        found_files.extend(glob.glob(recursive_pattern, recursive=True))
        all_files.extend(found_files)
    all_files = sorted(list(set(all_files)))
    print(f"Found {len(all_files)} code files in {folder_path} using patterns {FILE_PATTERNS}:")
    for file in all_files:
        file_type = "SQL" if file.lower().endswith('.sql') else "Python"
        print(f"  - {file} ({file_type})")
    return all_files

def build_prompt_for_individual_review(code_text: str, filename: str = "code_file") -> str:
    """Build appropriate prompt based on file type (Python vs SQL)"""
    is_sql_file = filename.lower().endswith('.sql')
    is_python_file = filename.lower().endswith('.py')
    if is_sql_file:
        prompt = PROMPT_TEMPLATE_SQL_INDIVIDUAL.replace("{SQL_CONTENT}", code_text)
        prompt = prompt.replace("{filename}", filename)
        print(f"  Using SQL-specific review prompt for {filename}")
    elif is_python_file:
        prompt = PROMPT_TEMPLATE_PYTHON_INDIVIDUAL.replace("{PY_CONTENT}", code_text)
        prompt = prompt.replace("{filename}", filename)
        print(f"  Using Python-specific review prompt for {filename}")
    else:
        prompt = PROMPT_TEMPLATE_PYTHON_INDIVIDUAL.replace("{PY_CONTENT}", code_text)
        prompt = prompt.replace("{filename}", filename)
        print(f"  Using Python review prompt as fallback for {filename}")
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

def extract_findings_with_line_numbers(review_text: str, severity: str) -> list:
    """
    Extract findings of a specific severity with line numbers using multiple patterns.
    Returns list of dicts with 'line' and 'finding' keys.
    """
    findings = []
    
    # Pattern 1: Standard format with Line, Severity, Finding
    pattern1 = rf'-\s*\*\*Severity:\*\*\s*{severity}.*?\*\*Line:\*\*\s*(\d+).*?\*\*Finding:\*\*\s*(.*?)(?=\n-\s*\*\*Severity:|\n\*\*File:|\n###|\Z)'
    for match in re.finditer(pattern1, review_text, re.IGNORECASE | re.DOTALL):
        findings.append({
            "line": match.group(1),
            "finding": match.group(2).strip()[:300]
        })
    
    # Pattern 2: Line comes before Severity
    pattern2 = rf'-\s*\*\*Line:\*\*\s*(\d+).*?\*\*Severity:\*\*\s*{severity}.*?\*\*Finding:\*\*\s*(.*?)(?=\n-\s*\*\*|\n\*\*File:|\n###|\Z)'
    for match in re.finditer(pattern2, review_text, re.IGNORECASE | re.DOTALL):
        findings.append({
            "line": match.group(1),
            "finding": match.group(2).strip()[:300]
        })
    
    # Pattern 3: Compact format "Line: 123 ... Severity: Critical ... Finding: text"
    pattern3 = rf'Line:\s*(\d+).*?Severity:\s*{severity}.*?Finding:\s*(.*?)(?=\nLine:|\nFile:|\n###|\Z)'
    for match in re.finditer(pattern3, review_text, re.IGNORECASE | re.DOTALL):
        findings.append({
            "line": match.group(1),
            "finding": match.group(2).strip()[:300]
        })
    
    # Pattern 4: Just severity and finding, try to find nearest line number
    pattern4 = rf'\*\*Severity:\*\*\s*{severity}.*?\*\*Finding:\*\*\s*(.*?)(?=\n\*\*Severity:|\n\*\*File:|\n###|\Z)'
    for match in re.finditer(pattern4, review_text, re.IGNORECASE | re.DOTALL):
        finding_text = match.group(1).strip()[:300]
        # Look backwards for a line number
        preceding_text = review_text[:match.start()]
        line_match = re.search(r'\*\*Line:\*\*\s*(\d+)', preceding_text[-200:])
        if line_match:
            findings.append({
                "line": line_match.group(1),
                "finding": finding_text
            })
        else:
            findings.append({
                "line": "N/A",
                "finding": finding_text
            })
    
    # Remove duplicates (same finding text)
    seen = set()
    unique_findings = []
    for f in findings:
        finding_key = f["finding"][:100]  # Use first 100 chars as key
        if finding_key not in seen:
            seen.add(finding_key)
            unique_findings.append(f)
    
    return unique_findings

def extract_critical_findings_from_review(review_text: str, filename: str) -> dict:
    """
    Extract only critical/high severity findings WITH LINE NUMBERS and key summary.
    Uses multiple regex patterns to handle various review formats.
    """
    result = {
        "filename": filename,
        "summary": "",
        "critical_findings": [],
        "high_findings": [],
        "medium_findings": [],
        "stats": {"critical": 0, "high": 0, "medium": 0, "low": 0}
    }
    
    # Extract executive summary (first 500 chars)
    lines = review_text.split('\n')
    summary_lines = []
    for line in lines[:20]:
        if line.strip() and not line.startswith('#') and not line.startswith('**') and not line.startswith('-'):
            summary_lines.append(line.strip())
            if len(' '.join(summary_lines)) > 500:
                break
    result["summary"] = ' '.join(summary_lines)[:500]
    
    # Extract severity counts
    result["stats"]["critical"] = len(re.findall(r'\*\*Severity:\*\*\s*Critical', review_text, re.IGNORECASE))
    result["stats"]["high"] = len(re.findall(r'\*\*Severity:\*\*\s*High', review_text, re.IGNORECASE))
    result["stats"]["medium"] = len(re.findall(r'\*\*Severity:\*\*\s*Medium', review_text, re.IGNORECASE))
    result["stats"]["low"] = len(re.findall(r'\*\*Severity:\*\*\s*Low', review_text, re.IGNORECASE))
    
    # Extract findings with line numbers using robust multi-pattern approach
    result["critical_findings"] = extract_findings_with_line_numbers(review_text, "Critical")
    result["high_findings"] = extract_findings_with_line_numbers(review_text, "High")[:15]  # Limit to 15
    result["medium_findings"] = extract_findings_with_line_numbers(review_text, "Medium")[:5]  # Limit to 5
    
    return result

def create_condensed_reviews(all_reviews: list) -> str:
    """
    Create a condensed version of reviews that preserves critical information INCLUDING LINE NUMBERS.
    """
    condensed = []
    total_original_size = 0
    
    for review in all_reviews:
        filename = review.get('filename', 'unknown')
        review_feedback = review.get('review_feedback', '')
        total_original_size += len(review_feedback)
        
        # Extract critical info with line numbers
        extracted = extract_critical_findings_from_review(review_feedback, filename)
        
        # Build condensed review with line numbers preserved
        condensed_review = {
            "filename": filename,
            "summary": extracted["summary"],
            "severity_stats": extracted["stats"],
            "critical_issues": extracted["critical_findings"],
            "high_issues": extracted["high_findings"],
            "medium_issues": extracted["medium_findings"]
        }
        
        condensed.append(condensed_review)
    
    result = json.dumps(condensed, indent=2)
    
    print(f"  Condensed reviews: {total_original_size} -> {len(result)} chars ({(len(result)/total_original_size)*100:.1f}% of original)")
    
    return result

def calculate_executive_quality_score(findings: list, total_lines_of_code: int) -> int:
    """Executive-level rule-based quality scoring (0-100)."""
    if not findings or len(findings) == 0:
        return 100
    base_score = 100
    total_deductions = 0
    severity_weights = {
        "Critical": 12,
        "High": 4,
        "Medium": 1.5,
        "Low": 0.3
    }
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    total_affected_lines = 0
    print(f"  Scoring {len(findings)} findings...")
    for finding in findings:
        severity = str(finding.get("severity", "")).strip()
        if severity == "Critical":
            severity_counts["Critical"] += 1
        elif severity == "High":
            severity_counts["High"] += 1
        elif severity == "Medium":
            severity_counts["Medium"] += 1
        elif severity == "Low":
            severity_counts["Low"] += 1
        else:
            print(f"    UNRECOGNIZED SEVERITY: '{severity}' - SKIPPING")
            continue
        print(f"    - {severity}: {finding.get('finding', 'No description')[:50]}...")
        total_affected_lines += 1
    print(f"  Severity breakdown: Critical={severity_counts['Critical']}, High={severity_counts['High']}, Medium={severity_counts['Medium']}, Low={severity_counts['Low']}")
    for severity, count in severity_counts.items():
        if count > 0:
            weight = severity_weights[severity]
            if severity == "Critical":
                if count <= 2:
                    deduction = weight * count
                else:
                    deduction = weight * 2 + (count - 2) * (weight + 3)
                deduction = min(30, deduction)
            elif severity == "High":
                if count <= 10:
                    deduction = weight * count
                else:
                    deduction = weight * 10 + (count - 10) * (weight + 1)
                deduction = min(25, deduction)
            else:
                deduction = weight * count
                if severity == "Medium":
                    deduction = min(20, deduction)
                else:
                    deduction = min(10, deduction)
            total_deductions += deduction
            print(f"    {severity}: {count} issues = -{deduction:.1f} points")
    if total_lines_of_code > 0:
        affected_ratio = total_affected_lines / total_lines_of_code
        if affected_ratio > 0.4:
            coverage_penalty = min(5, int(affected_ratio * 20))
            total_deductions += coverage_penalty
            print(f"    Coverage penalty: -{coverage_penalty} points")
    if severity_counts["Critical"] >= 3:
        total_deductions += 10
        print(f"    Executive threshold penalty: -10 points")
    if severity_counts["Critical"] + severity_counts["High"] >= 20:
        total_deductions += 5
        print(f"    Production readiness penalty: -5 points")
    final_score = max(0, base_score - int(total_deductions))
    print(f"  Final calculation: {base_score} - {int(total_deductions)} = {final_score}")
    if final_score >= 85:
        return min(100, final_score)
    elif final_score >= 70:
        return final_score
    elif final_score >= 50:
        return final_score
    else:
        return max(30, final_score)
