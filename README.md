# 🤖 GitHub MCP – Natural Language Command Interface

GitHub MCP is a lightweight server that enables you to interact with GitHub using natural language prompts. It uses a local LLM client and a FastAPI server to interpret your commands and call GitHub’s REST API behind the scenes.

---

##  Features

You can perform the following operations on your GitHub repositories by typing simple commands:

| Operation           | Description                                     | Example Prompt |
|---------------------|-------------------------------------------------|----------------|
| Create Repository    | Create a public/private repo with optional README | Create a private repo named `test_repo` with README |
| Create Issue         | Open a new issue in a specific repo             | Create issue in `osama-al-khreishah/circa_game` called `Bug` with body `Fix the error` |
| List Issues          | List all open issues in a repository            | List issues in repo `osama-al-khreishah/circa_game` |
| Close Issue          | Close a specific issue by number                | Close issues in repo `osama-al-khreishah/circa_game` #2 |
| Create Pull Request  | Make a PR between branches                      | Create a pull request titled `"Add tests"` from `dev` to `main` in `osama-al-khreishah/circa_game` |
| Create Branch        | Create a new branch in a repository             | Create a branch called `feature-x` in `osama-al-khreishah/circa_game` |
| Delete Branch        | Delete a branch from a repository               | Delete the branch `feature-x` from `osama-al-khreishah/circa_game` |
| View Analytics       | Show traffic and clone stats                    | Show me analytics for `osama-al-khreishah/circa_game` |
| View Collaborators   | List users who have access to a repo            | Who has access to `osama-al-khreishah/circa_game` |

---

##  How It Works

- `llm_client.py`: Acts as the natural language interface, sending parsed commands to the MCP server.
- `llm_parser.py`: Parses natural language input into a structured MCP payload.

---

##  Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/osama-al-khreishah/github-mcp
   cd github-mcp
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Set GitHub Token**
   ```bash
   Add your GitHub token to a .env file:
   GITHUB_TOKEN=your_personal_access_token
4. **Run the MCP Server**
   ```bash
   uvicorn main:app --reload
5. **Run the LLM Client**
   ```bash
   In another terminal:
   python llm_client.py

## Author
ENG. Osama Al-Khreishah

BSc. in Intelligent Systems Engineering

osamakhreishah@gmail.com