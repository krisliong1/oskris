"""
Tool Registry - Tools available to Claude Agent
Each tool has: definition (for API), executor (actual logic)
"""

import asyncio
import os
import json
import subprocess
import aiohttp
from pathlib import Path
from core.config import (
    COMMAND_TIMEOUT, BLOCKED_COMMANDS, MAX_FILE_SIZE,
    GITHUB_TOKEN, GITHUB_REPO
)


# ============================================================
# Tool Definitions (sent to Claude API)
# ============================================================

TOOL_DEFINITIONS = [
    {
        "name": "bash",
        "description": "Execute a bash command on the VPS. Use for system operations, installing packages, running scripts, checking status, etc. Returns stdout and stderr.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file. For large files, only first 50KB is returned.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute path to the file"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file. Creates parent directories if needed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute path to the file"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write"
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "list_directory",
        "description": "List files and directories at a path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path to list"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for current information. Returns top results with snippets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "github_push",
        "description": "Push a file to the GitHub repository. Auto-commits with a message.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path in the repo (e.g., 'skills/my-skill/SKILL.md')"
                },
                "content": {
                    "type": "string",
                    "description": "File content to push"
                },
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message"
                }
            },
            "required": ["file_path", "content", "commit_message"]
        }
    },
    {
        "name": "github_read",
        "description": "Read a file from the GitHub repository.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path in the repo (e.g., 'README.md')"
                }
            },
            "required": ["file_path"]
        }
    },
]


# ============================================================
# Tool Executors
# ============================================================

async def execute_bash(command: str) -> str:
    """Execute a bash command with safety checks"""
    # Safety check
    for blocked in BLOCKED_COMMANDS:
        if blocked in command:
            return f"⛔ Command blocked for safety: contains '{blocked}'"

    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/home"
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=COMMAND_TIMEOUT
        )

        result = ""
        if stdout:
            result += stdout.decode("utf-8", errors="replace")
        if stderr:
            result += "\n[stderr] " + stderr.decode("utf-8", errors="replace")
        if proc.returncode != 0:
            result += f"\n[exit code: {proc.returncode}]"

        return result[:10000] or "(no output)"

    except asyncio.TimeoutError:
        return f"⏱️ Command timed out after {COMMAND_TIMEOUT}s"
    except Exception as e:
        return f"❌ Error: {str(e)}"


async def execute_read_file(path: str) -> str:
    """Read a file's contents"""
    try:
        p = Path(path)
        if not p.exists():
            return f"❌ File not found: {path}"
        if not p.is_file():
            return f"❌ Not a file: {path}"

        size = p.stat().st_size
        if size > MAX_FILE_SIZE:
            content = p.read_text(errors="replace")[:MAX_FILE_SIZE]
            return f"[Truncated to {MAX_FILE_SIZE // 1024}KB, total {size // 1024}KB]\n{content}"
        return p.read_text(errors="replace")

    except Exception as e:
        return f"❌ Error reading file: {str(e)}"


async def execute_write_file(path: str, content: str) -> str:
    """Write content to a file"""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"✅ Written {len(content)} bytes to {path}"
    except Exception as e:
        return f"❌ Error writing file: {str(e)}"


async def execute_list_directory(path: str) -> str:
    """List directory contents"""
    try:
        p = Path(path)
        if not p.exists():
            return f"❌ Directory not found: {path}"
        if not p.is_dir():
            return f"❌ Not a directory: {path}"

        items = sorted(p.iterdir())
        lines = []
        for item in items[:100]:
            prefix = "📁 " if item.is_dir() else "📄 "
            size = ""
            if item.is_file():
                s = item.stat().st_size
                size = f" ({s:,} bytes)"
            lines.append(f"{prefix}{item.name}{size}")

        if len(items) > 100:
            lines.append(f"... and {len(items) - 100} more items")

        return "\n".join(lines) or "(empty directory)"
    except Exception as e:
        return f"❌ Error: {str(e)}"


async def execute_web_search(query: str) -> str:
    """Web search using DuckDuckGo HTML (no API key needed)"""
    try:
        url = "https://html.duckduckgo.com/html/"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={"q": query}, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return f"Search failed with status {resp.status}"
                html = await resp.text()

        # Simple parsing
        results = []
        import re
        # Extract result snippets
        links = re.findall(r'class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html)
        snippets = re.findall(r'class="result__snippet">(.*?)</span>', html, re.DOTALL)

        for i, (link, title) in enumerate(links[:5]):
            title = re.sub(r'<[^>]+>', '', title).strip()
            snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
            # Decode URL
            if "uddg=" in link:
                from urllib.parse import unquote
                link = unquote(link.split("uddg=")[1].split("&")[0])
            results.append(f"{i+1}. {title}\n   {link}\n   {snippet}\n")

        return "\n".join(results) if results else "No results found"

    except Exception as e:
        return f"❌ Search error: {str(e)}"


async def execute_github_push(file_path: str, content: str, commit_message: str) -> str:
    """Push a file to GitHub via API"""
    if not GITHUB_TOKEN:
        return "❌ GitHub token not configured"

    try:
        import base64
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        async with aiohttp.ClientSession() as session:
            # Check if file exists (get SHA)
            sha = None
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    sha = data.get("sha")

            # Create/update file
            payload = {
                "message": commit_message,
                "content": base64.b64encode(content.encode()).decode(),
                "branch": "main"
            }
            if sha:
                payload["sha"] = sha

            async with session.put(url, headers=headers, json=payload) as resp:
                if resp.status in (200, 201):
                    action = "Updated" if sha else "Created"
                    return f"✅ {action}: {file_path}"
                else:
                    error = await resp.text()
                    return f"❌ GitHub error ({resp.status}): {error[:500]}"

    except Exception as e:
        return f"❌ GitHub error: {str(e)}"


async def execute_github_read(file_path: str) -> str:
    """Read a file from GitHub"""
    if not GITHUB_TOKEN:
        return "❌ GitHub token not configured"

    try:
        import base64
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = base64.b64decode(data["content"]).decode()
                    return content
                elif resp.status == 404:
                    return f"❌ File not found in repo: {file_path}"
                else:
                    return f"❌ GitHub error ({resp.status})"

    except Exception as e:
        return f"❌ GitHub error: {str(e)}"


# ============================================================
# Tool Router
# ============================================================

TOOL_EXECUTORS = {
    "bash": lambda args: execute_bash(args["command"]),
    "read_file": lambda args: execute_read_file(args["path"]),
    "write_file": lambda args: execute_write_file(args["path"], args["content"]),
    "list_directory": lambda args: execute_list_directory(args["path"]),
    "web_search": lambda args: execute_web_search(args["query"]),
    "github_push": lambda args: execute_github_push(
        args["file_path"], args["content"], args["commit_message"]
    ),
    "github_read": lambda args: execute_github_read(args["file_path"]),
}


async def execute_tool(name: str, arguments: dict) -> str:
    """Route and execute a tool call"""
    executor = TOOL_EXECUTORS.get(name)
    if not executor:
        return f"❌ Unknown tool: {name}"
    return await executor(arguments)
