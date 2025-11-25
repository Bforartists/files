import requests
import json
import time
from datetime import datetime

##### INFO #####
# This creates a short print of the commit logs of a nested from the date, and filters the Bforartists commits
# This script assumes you have a python environment installed to your operating system. 

#### Use #####
# 1. Place the script in the root of where the Bforartists repository is
# 2. Open the script in something like VS Code
# 3. Run the script by pressing the play button to the top right, it should run with a python terminal

# 🔧 CONFIGURATION
REPO_OWNER = "Bforartists"  # GitHub repository owner
REPO_NAME = "Bforartists"   # GitHub repository name
START_DATE = "2025-08-27"   # YYYY-MM-DD format
OUTPUT_FILE = "git_log_tasks.txt"

# GitHub API URL for searching issues
API_URL = "https://api.github.com/search/issues"

# 📋 Search query parameters
query_params = {
    'q': f'repo:{REPO_OWNER}/{REPO_NAME} is:issue sort:updated-desc closed:>{START_DATE} -label:"6 - wontfix" -label:"8 - invalid" -label:"3 - duplicate" -label:"Known Issue"'
}

def fetch_github_issues():
    """Fetch GitHub issues using the search API with pagination"""
    all_issues = []
    page = 1
    per_page = 100  # GitHub API max per page
    
    try:
        print(f"Fetching issues from GitHub...")
        print(f"Search query: {query_params['q']}")
        
        while True:
            # Add pagination parameters
            params = query_params.copy()
            params['page'] = page
            params['per_page'] = per_page
            
            print(f"Fetching page {page}...")
            response = requests.get(API_URL, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            issues = data.get('items', [])
            
            if not issues:
                break
                
            all_issues.extend(issues)
            
            # Check if we've reached the end (GitHub limits search to 1000 items)
            if len(all_issues) >= data.get('total_count', 0) or len(issues) < per_page:
                break
                
            page += 1
            
            # Add a small delay to respect GitHub API rate limits
            time.sleep(0.5)
            
        return all_issues
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return all_issues
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return all_issues

def format_issue(issue):
    """Format a single issue in the requested format"""
    title = issue.get('title', 'No title')
    number = issue.get('number', '')
    
    # Format as "Title - #number"
    return f"{title} #{number}"

def main():
    # Fetch issues from GitHub
    issues = fetch_github_issues()
    
    if not issues:
        print("No issues found matching the criteria.")
        return
    
    # Format issues
    task_list = []
    for issue in issues:
        formatted = format_issue(issue)
        task_list.append(formatted)
        print(formatted)
    
    # Write results to file
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            file.write("\n".join(task_list))
        print(f"\nResults have been written to {OUTPUT_FILE}")
        print(f"Total issues found: {len(issues)}")
        
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
