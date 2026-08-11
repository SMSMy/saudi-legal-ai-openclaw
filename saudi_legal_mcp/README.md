# السعودية القانوني لـ OpenClaw — MCP Server

سيرفر استرجاع خالص — لا يحتاج أي مفتاح API.

## Setup

```bash
cd saudi-legal-ai-framework
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## OpenClaw Registration

```bash
openclaw mcp set saudi-legal \
  '{"command":"'$(pwd)'/.venv/bin/python","args":["'$(pwd)'/mcp-server/server.py"],"env":{"REPO_PATH":"'$(pwd)'"},"cwd":"'$(pwd)'"}'

openclaw mcp reload
```

## Tools

| Tool | Description |
|------|-------------|
| `get_legal_skill` | Return legal skill guide for a domain |
| `get_regulation_source` | Return official Saudi regulation summary |
| `get_legal_context` | Full context for contract analysis (skill + source + risks) |
| `search_contract_risks` | Search contract risk dataset |
| `list_legal_domains` | List all available domains and sources |
