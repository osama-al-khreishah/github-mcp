import os 
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"
headers = {
    "Authorization": f"Token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Function to create a GitHub repository

def create_repo(repo_name):
    
    # Validate the repository name (debugging purposes)
    if not repo_name or not isinstance(repo_name, str):
       raise ValueError("Invalid repository name")
    
    url= f"{GITHUB_API_URL}/user/repos"
    
    data={
        "name": repo_name.strip(), # strip for debugging purposes
        "private": False,
        "auto_init": True
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to create a GitHub issue

def create_issue(repo,title,body=""):
    url = f"{GITHUB_API_URL}/repos/{repo}/issues"
    data = {
        "title": title,
        "body": body
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to list issues in a repository
def list_issues(repo):
    url = f"{GITHUB_API_URL}/repos/{repo}/issues"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        issues = response.json()
        return {
            "status": "success",
            "issues": [
                {"title": issue["title"], "number": issue["number"], "state": issue["state"]}
                for issue in issues
            ]
        }
    else:
        return {
            "status": "error",
            "message": response.text,
            "code": response.status_code
        }
    # Function to close an issue
def close_issue(repo, issue_number):
    url = f"{GITHUB_API_URL}/repos/{repo}/issues/{issue_number}"
    data = {"state": "closed"}
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        return {"status": "success", "message": f"Issue #{issue_number} closed successfully."}
    else:
        return {"status": "error", "message": response.text, "code": response.status_code}

    # function to make pull request
def create_pull_request(repo: str, title: str, body: str, head: str, base: str ):
    url = f"{GITHUB_API_URL}/repos/{repo}/pulls"
    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }
    response =requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()
    return {"error": response.status_code, "detail": response.text}

# function to create & delete a branch
def create_branch(repo: str, branch: str, base_branch: str = "main") -> str:
    url = f"{GITHUB_API_URL}/repos/{repo}/git/refs/heads/{base_branch}"
    base_response = requests.get(url, headers=headers)

    if base_response.status_code != 200:
        raise ValueError(f"Base branch '{base_branch}' not found in {repo}")

    try:
        sha = base_response.json()["object"]["sha"]
    except (KeyError, TypeError) as e:
        print("Error extracting SHA:", base_response.text)
        raise

    data = {
        "ref": f"refs/heads/{branch}",
        "sha": sha
    }
    response = requests.post(f"{GITHUB_API_URL}/repos/{repo}/git/refs", headers=headers, json=data)

    if response.status_code == 201:
        return f"Branch '{branch}' created successfully in {repo}"
    else:
        raise Exception(f"Failed to create branch: {response.text}")

def delete_branch(repo, branch):
    
    url = f"{GITHUB_API_URL}/repos/{repo}/git/refs/heads/{branch}"
    
    response = requests.delete(url, headers=headers)
    return {"status": "deleted"} if response.status_code == 204 else {"error": response.status_code, "detail": response.text}

# function to get repo analytics
def get_repo_analytics(data):
    repo = data["repo"]
    url = f"{GITHUB_API_URL}/repos/{repo}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"status": "error", "detail": response.text}
    
    repo_data = response.json()
    
    # find open PRs
    pulls_url = f"{GITHUB_API_URL}/repos/{repo}/pulls?state=open"
    pulls_response = requests.get(pulls_url, headers=headers)
    pull_count = len(pulls_response.json()) if pulls_response.status_code == 200 else "N/A"

    return {
        "status": "success",
        "analytics":{
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "open_issues": repo_data.get("open_issues_count", 0),
            "watchers": repo_data.get("watchers_count", 0),
            "open_pull_requests": pull_count,
        },
    }