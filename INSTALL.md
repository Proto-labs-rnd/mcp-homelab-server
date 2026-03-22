# Installation Guide - MCP Homelab Server

Complete guide to install and configure the MCP Homelab Server with Claude Desktop.

## Prerequisites

- Python 3.10 or higher
- Docker installed and running
- Ollama installed (optional, for Ollama tools)
- Claude Desktop (latest version)
- `uv` package manager (recommended)

## Step 1: Install Dependencies

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your terminal
```

## Step 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mcp-homelab-server.git
cd mcp-homelab-server

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Step 3: Configure Claude Desktop

### Find your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Add the MCP server configuration:

```json
{
  "mcpServers": {
    "homelab": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/mcp-homelab-server",
        "run",
        "python src/server.py"
      ]
    }
  }
}
```

**Important**: Replace `/ABSOLUTE/PATH/TO/mcp-homelab-server` with the actual absolute path. You can get it by running `pwd` in the server directory.

### Optional: Add environment variables

```json
{
  "mcpServers": {
    "homelab": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/mcp-homelab-server",
        "run",
        "python src/server.py"
      ],
      "env": {
        "DOCKER_HOST": "unix:///var/run/docker.sock",
        "OLLAMA_HOST": "http://localhost:11434"
      }
    }
  }
}
```

## Step 4: Restart Claude Desktop

Quit and restart Claude Desktop. The MCP server should now be available!

## Step 5: Test the Server

In Claude Desktop, try these prompts:

```
"List all running Docker containers in my homelab"

"What's the resource usage of my containers?"

"Show me available Ollama models"

"Generate a haiku about homelabs using phi3:mini"

"What's my current system memory usage?"
```

## Troubleshooting

### Server not showing up in Claude

1. Check the config file path is correct
2. Verify Python 3.10+ is installed: `python --version`
3. Check Claude Desktop logs: `~/Library/Logs/Claude/` (macOS)
4. Try running the server manually: `python src/server.py`

### Docker commands failing

Make sure Docker is running and you have permissions:
```bash
docker ps  # Should list containers
```

### Ollama commands failing

Make sure Ollama is installed and running:
```bash
ollama list  # Should list models
```

### "Command not found" errors

Make sure `uv` is installed and in your PATH:
```bash
which uv  # Should show uv path
```

## Advanced: Run without uv

If you prefer not to use `uv`, you can modify the config:

```json
{
  "mcpServers": {
    "homelab": {
      "command": "/ABSOLUTE/PATH/TO/mcp-homelab-server/.venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-homelab-server/src/server.py"]
    }
  }
}
```

## Security Considerations

⚠️ **This server gives AI agents access to your homelab. To stay safe:**

1. **Only use with trusted AI clients** (Claude, ChatGPT, Cursor)
2. **Don't expose to the internet** - run locally only
3. **Review permissions** - understand what each tool does
4. **Monitor usage** - check Claude logs if something seems wrong
5. **Sandbox if possible** - consider running in a VM or container

## Next Steps

- Customize the server by editing `src/server.py`
- Add your own tools using the `@mcp.tool()` decorator
- Share your modifications with the community!

---

**Need help?** Open an issue on GitHub!
