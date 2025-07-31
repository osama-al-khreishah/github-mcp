from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from github_service import *
from llm_parser import parse_prompt

app = FastAPI()

@app.post("/github")
async def handle_github_command(request: Request):
    data = await request.json()
    print("Received from client:", data)
    operation = data.get("operation")

    if operation == "create_repo":
        repo_name = data.get("name")
        return {"status": "success", "Result": create_repo(repo_name)}
    # --- --- --- --- --- --- --- ---
    elif operation == "create_issue":
        repo = data.get("repo")
        title = data.get("title")
        body = data.get("body","")
        return {"status":"success", "Result": create_issue(repo,title,body)}
    # --- --- --- --- --- --- --- ---
    elif operation == "list_issues":
     return list_issues(data["repo"])
    # --- --- --- --- --- --- --- ---
    elif operation == "close_issue":
     return close_issue(data["repo"], data["issue_number"])
    # --- --- --- --- --- --- --- ---
    elif operation == "create_pull_request":
        repo = data.get("repo")
        title = data.get("title")
        body = data.get("body")
        head = data.get("head")
        base = data.get("base")
        return {"status": "success", "Result": create_pull_request(repo, title, body, head, base)}
    # --- --- --- --- --- --- --- ---
    
    elif operation == "create_branch":
        return {
            "status": "success",
            "Result": create_branch(data["repo"], data["branch"])
        }
    elif operation == "delete_branch":
        return {
            "status": "success",
            "Result": delete_branch(data["repo"], data["branch"])
        }
    # --- --- --- --- --- --- --- ---
    elif operation == "get_repo_analytics":
        return {"status": "success",
                "Result": get_repo_analytics(data)}
    # --- --- --- --- --- --- --- ---
    elif operation == "get_collaborators":
        repo = data.get("repo")
        url = f"{GITHUB_API_URL}/repos/{repo}/collaborators"
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
        response = requests.get(url, headers=headers)
        return response.json()
    
    raise HTTPException(status_code=400, detail="Invalid operation")