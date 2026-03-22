# MCP Homelab Server

> **Model Context Protocol server for homelab management**
> Give AI agents access to your homelab: Docker, Ollama, system stats, and more

## What is this?

An MCP server that exposes tools for managing and monitoring a local homelab. AI agents like Claude, ChatGPT, or Cursor can use these tools to interact with your homelab infrastructure safely.

## Features

### Tools
- **`docker_ps`** - List running Docker containers
- **`docker_stats`** - Get container resource usage (CPU, RAM, network)
- **`docker_logs`** - Fetch logs from a specific container
- **`ollama_list`** - List available Ollama models
- **`ollama_generate`** - Generate text with a local Ollama model
- **`system_stats`** - Get system statistics (CPU, RAM, disk, temperature)
- **`backup_status`** - Check backup status and last backup time

### Why is this useful?

Instead of remembering Docker commands or SSH'ing into your homelab, you can ask Claude:
- "Show me the resource usage of all containers"
- "Generate a summary with phi3:mini"
- "Are my backups working?"
- "What's the CPU temperature on cortex?"

## Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/mcp-homelab-server.git
cd mcp-homelab-server

# Install dependencies
uv venv
source .venv/bin/activate
uv install mcp httpx docker

# Run the server
python src/server.py
```

## Configuration (Claude Desktop)

Add to your `claude_desktop_config.json`:

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

## Security

⚠️ **This server gives AI agents access to your homelab. Use with caution:**

- Only connect to trusted AI clients (Claude, ChatGPT, Cursor)
- Review tool permissions before enabling
- Consider running in a sandboxed environment
- Never expose this server to the public internet

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Format
uv run ruff format src/
```

## License

MIT License - feel free to use and modify for your homelab!

## Contributing

Contributions welcome! Please open an issue or PR.

---

**Built with ❤️ for the self-hosting community**
