# Saudi Legal AI — MCP Server

MCP server exposing the Saudi Legal AI Framework as tools for Claude Desktop.

## Prerequisites

Before setting up the MCP server, ensure you have:

1. **Docker** installed and running
2. **Anthropic API Key** — required for `analyze_contract_clause` and `get_regulation_summary` tools
   - Get your API key from [console.anthropic.com](https://console.anthropic.com/)
   - Set it as an environment variable: `export ANTHROPIC_API_KEY=your-key-here`

> **Note:** The `search_contract_risks` tool works without an API key (it queries local data only).

## Tools

| Tool | Requires API Key | Description |
|------|------------------|-------------|
| `analyze_contract_clause` | **Yes** | Analyzes a contract clause against Saudi law using Claude |
| `get_regulation_summary` | **Yes** | Returns a structured summary of a Saudi regulation using Claude |
| `search_contract_risks` | No | Queries the contract risk dataset by type / level / category |

## Claude Desktop Setup

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "saudi-legal-ai": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/path/to/saudi-legal-ai-framework:/repo:ro",
        "-e", "REPO_PATH=/repo",
        "-e", "ANTHROPIC_API_KEY=your-api-key-here",
        "saudi-legal-mcp"
      ]
    }
  }
}
```

**Important:** Replace:
- `/path/to/saudi-legal-ai-framework` with the actual path to your cloned repository
- `your-api-key-here` with your actual Anthropic API key

Then restart Claude Desktop. Claude will automatically call the tools when you ask legal questions.

### Using Environment Variables (Recommended)

Instead of hardcoding your API key in the config file, use environment variable expansion:

```json
{
  "mcpServers": {
    "saudi-legal-ai": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "${REPO_PATH}:/repo:ro",
        "-e", "REPO_PATH=/repo",
        "-e", "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}",
        "saudi-legal-mcp"
      ]
    }
  }
}
```

Set the environment variables before starting Claude Desktop:
```bash
export REPO_PATH=/path/to/saudi-legal-ai-framework
export ANTHROPIC_API_KEY=your-api-key-here
```

## Build

```bash
cd mcp-server
docker build -t saudi-legal-mcp .
```

## Local Development (no Docker)

```bash
cd mcp-server
pip install -r requirements.txt
export REPO_PATH=/path/to/saudi-legal-ai-framework
export ANTHROPIC_API_KEY=your-api-key-here
python server.py
```

## Example Queries

Once connected in Claude Desktop:

- "راجع هذا العقد وحدد البنود المخالفة لنظام العمل السعودي"
- "ما شروط التحكيم في المملكة؟"
- "ما مخاطر عقود الـ SaaS من الدرجة الحرجة؟"
- "أعطني ملخص نظام المحاكم التجارية م/93"

## Troubleshooting

### Error: "ANTHROPIC_API_KEY environment variable not set"

**Cause:** The `analyze_contract_clause` and `get_regulation_summary` tools require an Anthropic API key to function.

**Solution:**
1. Ensure you have an Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
2. Add `-e`, `ANTHROPIC_API_KEY=your-key-here` to the Docker args in your Claude Desktop config
3. Restart Claude Desktop after updating the config

### Tools return no results or errors

**Check:**
- Docker is running: `docker ps`
- Repository path is correct and accessible
- API key is valid (test with a simple curl request to Anthropic API)

### Server won't start

**Check:**
- Docker image is built: `docker images | grep saudi-legal-mcp`
- Rebuild if needed: `cd mcp-server && docker build -t saudi-legal-mcp .`

## Notes

- The repo is mounted read-only — the server reads live files, nothing is copied into the image.
- Uses `stdio` transport (default), compatible with Claude Desktop's MCP client.
- Requires Docker to be running when Claude Desktop starts.
- The server logs startup warnings to stderr if `ANTHROPIC_API_KEY` is missing.
