#!/usr/bin/env python3
"""
MCP Homelab Server - Model Context Protocol server for homelab management

Gives AI agents access to Docker, Ollama, and system stats in your homelab.
"""

import sys
import json
import subprocess
from typing import Any
from pathlib import Path

# MCP imports
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: mcp package not installed. Run: uv install 'mcp[cli]'", file=sys.stderr)
    sys.exit(1)

# Initialize FastMCP server
mcp = FastMCP("homelab")

# Constants
DOCKER_SOCK = "/var/run/docker.sock"
OLLAMA_HOST = "http://localhost:11434"


# ============================================================================
# DOCKER TOOLS
# ============================================================================

@mcp.tool()
async def docker_ps() -> str:
    """List all running Docker containers with their status.

    Returns:
        JSON string with container information (name, image, status, ports)
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    containers.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return json.dumps({
            "running_containers": len(containers),
            "containers": containers
        }, indent=2)

    except subprocess.TimeoutExpired:
        return "Error: Docker command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def docker_stats(container_name: str = None) -> str:
    """Get resource usage statistics for Docker containers.

    Args:
        container_name: Optional container name to filter. If None, shows all containers.

    Returns:
        JSON string with CPU, memory, network I/O, and block I/O stats
    """
    try:
        cmd = ["docker", "stats", "--format", "json", "--no-stream"]
        if container_name:
            cmd.append(container_name)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        stats = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    stats.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return json.dumps({
            "container_stats": stats
        }, indent=2)

    except subprocess.TimeoutExpired:
        return "Error: Docker stats command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def docker_logs(container_name: str, tail: int = 100) -> str:
    """Fetch recent logs from a Docker container.

    Args:
        container_name: Name or ID of the container
        tail: Number of recent lines to fetch (default: 100)

    Returns:
        String with container logs
    """
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(tail), container_name],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        return result.stdout

    except subprocess.TimeoutExpired:
        return "Error: Docker logs command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# OLLAMA TOOLS
# ============================================================================

@mcp.tool()
async def ollama_list() -> str:
    """List all available Ollama models on the local server.

    Returns:
        JSON string with model names, sizes, and quantization info
    """
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10,
            env={**subprocess.os.environ, "OLLAMA_HOST": OLLAMA_HOST}
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        # Parse ollama list output (simple parsing)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        models = []
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    models.append({
                        "name": parts[0],
                        "id": parts[1][:12] if len(parts) > 1 else "",
                        "size": parts[2] if len(parts) > 2 else "",
                        "quantization": parts[3] if len(parts) > 3 else ""
                    })

        return json.dumps({
            "available_models": len(models),
            "models": models
        }, indent=2)

    except subprocess.TimeoutExpired:
        return "Error: Ollama command timed out"
    except FileNotFoundError:
        return "Error: Ollama not found. Is it installed and in PATH?"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def ollama_generate(model: str, prompt: str) -> str:
    """Generate text using a local Ollama model.

    Args:
        model: Model name (e.g., "phi3:mini", "llama3.2:3b")
        prompt: Text prompt to generate from

    Returns:
        String with generated text
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minutes timeout for generation
            env={**subprocess.os.environ, "OLLAMA_HOST": OLLAMA_HOST}
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        return result.stdout

    except subprocess.TimeoutExpired:
        return "Error: Ollama generation timed out (model may be too slow)"
    except FileNotFoundError:
        return "Error: Ollama not found. Is it installed and in PATH?"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# SYSTEM TOOLS
# ============================================================================

@mcp.tool()
async def system_stats() -> str:
    """Get comprehensive system statistics.

    Returns:
        JSON string with CPU usage, memory, disk space, and load average
    """
    try:
        # CPU and memory (using /proc/meminfo on Linux)
        meminfo = Path("/proc/meminfo").read_text()
        mem_total = 0
        mem_available = 0
        for line in meminfo.split('\n'):
            if 'MemTotal:' in line:
                mem_total = int(line.split()[1]) // 1024  # Convert KB to MB
            elif 'MemAvailable:' in line:
                mem_available = int(line.split()[1]) // 1024

        # Load average
        loadavg = Path("/proc/loadavg").read_text().split()[:3]

        # Disk usage
        disk_result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True,
            text=True,
            timeout=5
        )
        disk_lines = disk_result.stdout.split('\n')
        disk_info = disk_lines[1].split() if len(disk_lines) > 1 else []

        return json.dumps({
            "memory_mb": {
                "total": mem_total,
                "available": mem_available,
                "used_percent": ((mem_total - mem_available) / mem_total * 100) if mem_total > 0 else 0
            },
            "load_average": [float(x) for x in loadavg],
            "disk": {
                "total": disk_info[1] if len(disk_info) > 1 else "N/A",
                "used": disk_info[2] if len(disk_info) > 2 else "N/A",
                "available": disk_info[3] if len(disk_info) > 3 else "N/A",
                "use_percent": disk_info[4] if len(disk_info) > 4 else "N/A"
            }
        }, indent=2)

    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def backup_status() -> str:
    """Check the status of backups (if restic or similar is configured).

    Returns:
        JSON string with last backup time and status
    """
    try:
        # Check if restic is available
        result = subprocess.run(
            ["which", "restic"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return json.dumps({
                "status": "not_configured",
                "message": "Restic not found. Backup system not configured."
            }, indent=2)

        # Try to get last backup time (this is a simplified check)
        # In production, you'd check a status file or run restic snapshots
        return json.dumps({
            "status": "configured",
            "message": "Backup system found (restic). Run 'restic snapshots' for details.",
            "note": "Detailed backup status checking requires repository configuration."
        }, indent=2)

    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the MCP server."""
    print("Starting MCP Homelab Server...", file=sys.stderr)
    print(f"Docker socket: {DOCKER_SOCK}", file=sys.stderr)
    print(f"Ollama host: {OLLAMA_HOST}", file=sys.stderr)

    # Run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
