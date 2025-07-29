import requests
from llm_parser import parse_prompt

server_url = "http://127.0.0.1:8000/github"

while True:
    prompt = input("🤖 What do you want to do on GitHub? (type 'exit' to quit):\n> ")
    if prompt.lower() == "exit":
        break

    mcp_payload = parse_prompt(prompt)
    print(f"sending: {mcp_payload}")

    response = requests.post(server_url, json=mcp_payload)
    print("Raw response:", response.text)# debugging purposes
    print("Response from MCP server:", response.json())
    