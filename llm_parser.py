# create_repo
from utills import extract_between, extract_after

def parse_prompt(prompt: str) -> dict:
   prompt = prompt.lower().strip()

   if "create" in prompt and ("repo" in prompt or "repository" in prompt):
     
       name = None 
       private = "private" in prompt
       auto_init = "readme" in prompt or "init" in prompt

# Extract the repository name from the prompt

       words = prompt.split()
               
       if "named" in words:
            idx = words.index("named")
       elif "called" in words:
            idx = words.index("called")
       else:
            raise ValueError("'named' or 'called' not found in prompt.")
       if "named" or "name" in words:
           idx = words.index("named")
           if idx + 1 < len(words):
               name = words[idx + 1].strip(".,!?\"'")


       return {"operation": "create_repo", "name": name, "private": private, "auto_init": auto_init}

  #---- --- --- --- --- --- --- ---
# Create Issue

   elif "create issue" in prompt:
        repo = extract_between(prompt, "in ", " called")
        title = extract_between(prompt, "called ", " with") or extract_between(prompt, "called ", "")
        body = extract_between(prompt, "with body ", "") or ""
        return {"operation": "create_issue", "repo": repo, "title": title, "body": body}   
# list issues

   elif "list" in prompt and "issues" in prompt:
        repo = extract_after(prompt, "repo ")
        return {"operation": "list_issues", "repo": repo.strip()}
   
# close issue
   
   elif "close issue" in prompt:
    repo = extract_between(prompt, "in ", " number") or extract_after(prompt, "in ")
    if "#" in prompt:
        issue_number = int(prompt.split("#")[-1].strip())
    elif "number" in prompt:
        issue_number = int(prompt.split("number")[-1].strip())
    else:
        issue_number = None
    return {"operation": "close_issue", "repo": repo.strip(), "issue_number": issue_number}

   #--- --- --- --- --- --- --- --- ---
# Create Pull Request
   elif "pull request" in prompt or "pr" in prompt:
    # Extract full repo string
    raw_repo = extract_after(prompt, "in").strip()
    if raw_repo.startswith("in "):
        raw_repo = raw_repo[3:].strip()  # Remove leading "in "

    # Parse the other parts
    title = extract_between(prompt, 'titled "', '"').strip()
    head = extract_between(prompt, "from", "to").strip()
    base = extract_between(prompt, "to", "in").strip()

    return {
        "operation": "create_pull_request",
        "repo": raw_repo,
        "title": title,
        "body": "",
        "head": head,
        "base": base
    }
   #--- --- --- --- --- --- --- --- ---
#create a branch

   elif "create a branch" in prompt:
        branch_name = extract_between(prompt, "branch called", "in").strip()
        repo = extract_after(prompt, "in").strip()
        return {
            "operation": "create_branch",
            "repo" : repo,
            "branch": branch_name
        }
    #--- --- --- --- --- --- --- ---
# delete a branch
   elif "delete the branch" in prompt:
       branch_name = extract_between(prompt, "branch","from").strip()
       repo = extract_after(prompt, "from").strip()
       return {
           "operation": "delete_branch",
           "repo": repo,
           "branch": branch_name
       }
    #--- --- --- --- --- --- --- ---
# get repo analytics
   elif "analytics" in prompt or "stats" in prompt:
       repo = extract_after(prompt, "in").strip()
       return {
           "operation": "get_repo_analytics",
           "repo": repo
       }
    #---- --- --- --- --- --- --- ---
# Security / collaborators
   elif "access" in prompt or "collaborators" in prompt:
       repo = extract_after(prompt, "to").strip() or extract_after(prompt, "in").strip()
       return{
              "operation": "get_collaborators",
              "repo": repo
       }
   else: 
    return {"operation": "UNKNOWN OPERATION"}