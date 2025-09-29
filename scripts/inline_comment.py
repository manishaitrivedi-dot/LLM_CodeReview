# inline_comment.py

import os, json, requests, time

GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPOSITORY", "your-username/LLM_CodeReview")
PR_NUMBER = str(os.environ.get("GITHUB_PR_NUMBER") or os.environ.get("GITHUB_RUN_NUMBER", "1"))

if not GH_TOKEN:
    print("Error: GH_TOKEN or GITHUB_TOKEN environment variable required")
    exit(1)

headers = {
    "Authorization": f"token {GH_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_pr_files(max_retries=3):
    """Get list of files changed in the PR with retry logic"""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                files = response.json()
                changed_files = {}
                for file in files:
                    filename = file['filename']
                    patch = file.get('patch', '')
                    changed_files[filename] = {
                        'patch': patch,
                        'status': file['status'],
                        'additions': file['additions'],
                        'deletions': file['deletions']
                    }
                    print(f"Found changed file: {filename} (status: {file['status']})")
                return changed_files
            elif response.status_code == 404:
                print(f"PR #{PR_NUMBER} not found in {REPO}")
                return {}
            else:
                print(f"Failed to get PR files (attempt {attempt+1}/{max_retries}): {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            print(f"Request error (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return {}

def parse_patch_lines(patch):
    """Parse patch to get valid line numbers for commenting"""
    if not patch:
        return set()
    valid_lines = set()
    current_line = 0
    for line in patch.split('\n'):
        if line.startswith('@@'):
            parts = line.split()
            if len(parts) >= 3:
                new_info = parts[2]
                if new_info.startswith('+'):
                    try:
                        new_start = int(new_info[1:].split(',')[0])
                        current_line = new_start
                    except:
                        continue
        elif line.startswith('+') and not line.startswith('+++'):
            valid_lines.add(current_line)
            current_line += 1
        elif line.startswith(' '):
            current_line += 1
    return valid_lines

def post_pr_comment(body: str, max_retries=3):
    """Post general PR review comment with retry logic"""
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json={"body": body}, timeout=10)
            if response.status_code == 201:
                print("Posted PR comment successfully")
                return True
            else:
                print(f"Failed to post PR comment (attempt {attempt+1}/{max_retries}): {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            print(f"Request error posting comment (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    print(f"Failed to post PR comment after {max_retries} attempts")
    return False

def find_matching_file(filename, changed_files):
    """Find the actual file path in changed_files that matches the given filename"""
    if filename in changed_files:
        return filename
    import os
    basename = os.path.basename(filename)
    for changed_file in changed_files.keys():
        if os.path.basename(changed_file) == basename:
            print(f"Matched {filename} -> {changed_file}")
            return changed_file
    filename_lower = filename.lower()
    for changed_file in changed_files.keys():
        if filename_lower in changed_file.lower() or os.path.basename(changed_file).lower() == filename_lower:
            print(f"Partial matched {filename} -> {changed_file}")
            return changed_file
    return None

def post_inline_comments(comments, changed_files, max_retries=3):
    """Post inline comments for critical issues only with retry logic"""
    commits_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/commits"
    commits = None
    for attempt in range(max_retries):
        try:
            commits_response = requests.get(commits_url, headers=headers, timeout=10)
            if commits_response.status_code == 200:
                commits = commits_response.json()
                break
            else:
                print(f"Failed to get commits (attempt {attempt+1}/{max_retries}): {commits_response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            print(f"Request error getting commits (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    if not commits:
        print("Failed to get commits after retries")
        return
    latest_sha = commits[-1]["sha"]
    print(f"Using commit SHA: {latest_sha}")
    comment_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/comments"
    posted_count = 0
    skipped_count = 0
    print(f"Available changed files: {list(changed_files.keys())}")
    for c in comments:
        original_path = c["path"]
        line_num = c["line"]
        actual_file_path = find_matching_file(original_path, changed_files)
        if not actual_file_path:
            print(f"Skipping comment for {original_path}: no matching file found in PR changes")
            skipped_count += 1
            continue
        print(f"Processing comment for {actual_file_path} (originally {original_path}) at line {line_num}")
        if changed_files[actual_file_path]['status'] == 'removed':
            print(f"Skipping comment for {actual_file_path}: file was deleted")
            skipped_count += 1
            continue
        if changed_files[actual_file_path]['status'] == 'added':
            valid_lines = set(range(1, 1000))
        else:
            valid_lines = parse_patch_lines(changed_files[actual_file_path]['patch'])
        if not valid_lines and changed_files[actual_file_path]['status'] == 'added':
            line_num = 1
        elif valid_lines and line_num not in valid_lines:
            closest_line = min(valid_lines, key=lambda x: abs(x - line_num)) if valid_lines else 1
            print(f"Line {line_num} not in diff for {actual_file_path}, using closest line {closest_line}")
            line_num = closest_line
        data = {
            "body": c["body"],
            "commit_id": latest_sha,
            "path": actual_file_path,
            "side": "RIGHT",
            "line": line_num
        }
        posted = False
        for attempt in range(max_retries):
            try:
                response = requests.post(comment_url, headers=headers, json=data, timeout=10)
                if response.status_code == 201:
                    print(f"Posted inline comment on {actual_file_path}:{line_num}")
                    posted_count += 1
                    posted = True
                    break
                else:
                    print(f"Failed to post inline comment (attempt {attempt+1}/{max_retries}): {response.status_code}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
            except requests.exceptions.RequestException as e:
                print(f"Request error posting inline comment (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        if not posted and line_num != 1:
            print(f"Retrying with line 1 for {actual_file_path}")
            data["line"] = 1
            try:
                retry_response = requests.post(comment_url, headers=headers, json=data, timeout=10)
                if retry_response.status_code == 201:
                    print(f"Posted inline comment on {actual_file_path}:1 (fallback)")
                    posted_count += 1
                else:
                    print(f"Fallback also failed: {retry_response.status_code}")
                    skipped_count += 1
            except requests.exceptions.RequestException as e:
                print(f"Fallback request error: {e}")
                skipped_count += 1
        elif not posted:
            skipped_count += 1
    print(f"Posted {posted_count}/{len(comments)} inline comments ({skipped_count} skipped)")

if __name__ == "__main__":
    try:
        print(f"Processing review for PR #{PR_NUMBER} in {REPO}")
        print("Waiting 2 seconds for PR to stabilize...")
        time.sleep(2)
        changed_files = get_pr_files()
        if not changed_files:
            print("No changed files found in PR. Cannot post inline comments.")
            exit(1)
        if not os.path.exists("review_output.json"):
            print("review_output.json not found. Run main.py first.")
            exit(1)
        with open("review_output.json", encoding='utf-8') as f:
            review_data = json.load(f)
        print(f"Found {len(review_data.get('criticals', []))} critical issues")
        review_body = f"""## Automated LLM Code Review

### Full Review:
{review_data.get('full_review', 'Review completed')}

"""
        review_body += "\n*Critical issues are also posted as inline comments on specific lines where possible.*"
        post_pr_comment(review_body)
        inline_comments = []
        for c in review_data.get("criticals", []):
            finding_text = c.get('finding', '') or c.get('description', '') or c.get('issue', '') or c.get('message', '')
            if not finding_text:
                finding_text = c.get('title', '') or c.get('summary', '')
                if not finding_text:
                    finding_text = "Critical security or code quality issue detected"
            recommendation_text = c.get('recommendation', 'Please review this issue')
            line_num = c.get('line', c.get('line_number', 1))
            filename = c.get('filename', c.get('file', review_data.get('file', 'unknown.py')))
            severity = c.get('severity', 'Critical')
            try:
                if line_num == 'N/A':
                    line_num = 1
                else:
                    line_num = int(line_num)
            except (ValueError, TypeError):
                line_num = 1
            if filename.startswith('./'):
                filename = filename[2:]
            issue_description = f"line no. {line_num}, Issue : {finding_text}"
            inline_comments.append({
                "path": filename,
                "line": line_num,
                "body": f"**CRITICAL ISSUE**\n{issue_description}\n**Recommendation:** {recommendation_text}\n\n---\n*Generated by automated LLM code review*"
            })
        if inline_comments:
            print(f"Posting {len(inline_comments)} critical inline comments...")
            post_inline_comments(inline_comments, changed_files)
        else:
            print("No critical issues found for inline comments")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing review_output.json: {e}")
        exit(1)
    except KeyError as e:
        print(f"Error: Missing key in review data: {e}")
        if 'review_data' in locals():
            print("Available keys in review data:")
            print(list(review_data.keys()))
            if 'criticals' in review_data and len(review_data['criticals']) > 0:
                print("Available keys in criticals[0]:")
                print(list(review_data['criticals'][0].keys()))
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
