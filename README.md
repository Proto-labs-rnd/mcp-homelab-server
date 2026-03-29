# MCP Homelab Server 🏠

> **Model Context Protocol server for homelab management**
> Give AI agents access to your homelab: Docker, Ollama, system stats, and more.

## What Is This?

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that exposes homelab tools to AI agents like Claude, GPT, or any MCP-compatible client. Instead of writing scripts yourself, just ask your AI agent to manage your infrastructure.

**Example conversations:**
- "List all running Docker containers"
- "How much RAM is Ollama using?"
- "Pull the llama3 model"
- "Show me disk usage on the server"

## Tools Provided

### Docker Management
| Tool | Description |
|------|-------------|
| `docker_ps` | List running containers |
| `docker_logs` | Get container logs |
| `docker_restart` | Restart a container |
| `docker_stop` | Stop a container |
| `docker_stats` | Resource usage (CPU, RAM, network) |

### Ollama / LLM Management
| Tool | Description |
|------|-------------|
| `ollama_list` | List installed models |
| `ollama_pull` | Pull a new model |
| `ollama_ps` | Show running models and memory usage |
| `ollama_generate` | Run a quick inference test |

### System Monitoring
| Tool | Description |
|------|-------------|
| `system_stats` | CPU, RAM, disk, uptime |
| `disk_usage` | Detailed disk usage by mount |
| `network_status` | Network interfaces and connections |
| `process_top` | Top processes by CPU/RAM |

## Quick Start

### With Claude Desktop / Cursor / any MCP client

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "homelab": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-homelab"]
    }
  }
}
```

### With OpenClaw

```json
{
  "mcpServers": {
    "homelab": {
      "command": "python3",
      "args": ["path/to/mcp-homelab-server/src/server.py"]
    }
  }
}
```

### Standalone (for testing)

```bash
git clone https://github.com/Proto-labs-rnd/mcp-homelab-server.git
cd mcp-homelab-server
pip install -r requirements.txt
python3 src/server.py
```

## Requirements

- Python 3.10+
- Docker (for Docker tools)
- Ollama (for LLM tools, optional)
- Linux/macOS (system stats rely on standard Unix tools)

## Architecture

```
MCP Client (Claude, Cursor, OpenClaw, etc.)
        │
        ▼
┌─────────────────────┐
│  MCP Server (stdio)  │
│  ┌───────────────┐  │
│  │ Docker Tools  │  │
│  │ Ollama Tools  │  │
│  │ System Tools  │  │
│  └───────────────┘  │
└─────────────────────┘
        │
        ▼
   Your Homelab
```

## License

MIT
