"""
Tool Registry - Tools available to Claude Agent
Each tool has: definition (for API), executor (actual logic)

FILE PROTECTION SYSTEM:
- New files: push directly
- Existing files: show diff → require user confirmation → backup → push → log
- Delete: blocked unless explicitly confirmed
"""

import asyncio
import os
import json
import subprocess
import aiohttp
import difflib
import base64
from datetime import datetime
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
        "description": """Push a file to GitHub. FILE PROTECTION RULES:
- NEW file (doesn't exist): pushes directly, no confirmation needed.
- EXISTING file: MUST set confirmed=true. If confirmed=false (default), returns a diff preview and asks user to confirm. You MUST show the diff to the user and get their approval before calling again with confirmed=true.
- Always include a clear commit_message.""",
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
                },
                "confirmed": {
                    "type": "boolean",
                    "description": "Set to true ONLY after user has reviewed and approved the diff. Default false."
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
    {
        "name": "github_changelog",
        "description": "View the file modification changelog. Shows recent changes with timestamps, files modified, and who made the change.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of recent entries to show (default 20)"
                }
            },
            "required": []
        }
    },
]


# ============================================================
# GitHub Helper Functions
# ============================================================

async def _github_get_file(file_path: str) -> tuple:
    """Get file content and SHA from GitHub. Returns (content, sha) or (None, None)."""
    if not GITHUB_TOKEN:
        return None, None

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
                return content, data.get("sha")
            return None, None


async def _github_put_file(file_path: str, content: str, commit_message: str, sha: str = None) -> str:
    """Actually push file to GitHub. Internal function."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "message": commit_message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, json=payload) as resp:
            if resp.status in (200, 201):
                action = "Updated" if sha else "Created"
                return f"✅ {action}: {file_path}"
            else:
                error = await resp.text()
                return f"❌ GitHub error ({resp.status}): {error[:500]}"


async def _github_backup(file_path: str, old_content: str) -> str:
    """Backup old version before modification."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = file_path.replace("/", "_")
    backup_path = f"backups/{datetime.now().strftime('%Y-%m-%d')}/{timestamp}_{filename}"

    result = await _github_put_file(
        backup_path,
        old_content,
        f"Backup: {file_path} before modification"
    )
    return backup_path if "✅" in result else None


async def _github_log_change(file_path: str, action: str, commit_message: str, has_backup: str = None):
    """Log the modification to changelog."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read existing changelog
    old_log, sha = await _github_get_file("logs/changelog.md")

    entry = f"| {timestamp} | `{file_path}` | {action} | {commit_message} | {has_backup or 'N/A'} |\n"

    if old_log:
        new_log = old_log.rstrip("\n") + "\n" + entry
    else:
        new_log = (
            "# File Modification Changelog\n\n"
            "All file changes are logged here automatically.\n\n"
            "| Time | File | Action | Message | Backup |\n"
            "|------|------|--------|---------|--------|\n"
            + entry
        )

    await _github_put_file(
        "logs/changelog.md",
        new_log,
        f"Log: {action} {file_path}",
        sha
    )


def _generate_diff(old_content: str, new_content: str, file_path: str) -> str:
    """Generate a unified diff between old and new content."""
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile=f"a/{file_path} (current)",
        tofile=f"b/{file_path} (new)",
        lineterm=""
    )

    diff_text = "\n".join(diff)
    if not diff_text:
        return "No changes detected."

    # Count changes
    added = sum(1 for line in diff_text.split("\n") if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff_text.split("\n") if line.startswith("-") and not line.startswith("---"))

    summary = f"📊 Changes: +{added} lines added, -{removed} lines removed\n\n"
    return summary + diff_text


# ============================================================
# Tool Executors
# ============================================================

async def execute_bash(command: str) -> str:
    """Execute a bash command with safety checks"""
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

        import re
        results = []
        links = re.findall(r'class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html)
        snippets = re.findall(r'class="result__snippet">(.*?)</span>', html, re.DOTALL)

        for i, (link, title) in enumerate(links[:5]):
            title = re.sub(r'<[^>]+>', '', title).strip()
            snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
            if "uddg=" in link:
                from urllib.parse import unquote
                link = unquote(link.split("uddg=")[1].split("&")[0])
            results.append(f"{i+1}. {title}\n   {link}\n   {snippet}\n")

        return "\n".join(results) if results else "No results found"

    except Exception as e:
        return f"❌ Search error: {str(e)}"


async def execute_github_push(file_path: str, content: str, commit_message: str, confirmed: bool = False) -> str:
    """
    Push a file to GitHub with FILE PROTECTION.

    - New file: push directly
    - Existing file + confirmed=False: return diff, request confirmation
    - Existing file + confirmed=True: backup old → push new → log change
    """
    if not GITHUB_TOKEN:
        return "❌ GitHub token not configured"

    try:
        # Step 1: Check if file exists
        old_content, sha = await _github_get_file(file_path)

        # === NEW FILE: push directly ===
        if old_content is None:
            result = await _github_put_file(file_path, content, commit_message)
            if "✅" in result:
                await _github_log_change(file_path, "CREATE", commit_message)
            return result

        # === EXISTING FILE: protection kicks in ===

        # Check if content actually changed
        if old_content.strip() == content.strip():
            return "ℹ️ No changes detected. File content is identical."

        # Not confirmed yet → show diff and ask for confirmation
        if not confirmed:
            diff = _generate_diff(old_content, content, file_path)
            return (
                f"🔒 FILE PROTECTION: `{file_path}` already exists!\n\n"
                f"This file will be MODIFIED. Please review the diff:\n\n"
                f"```\n{diff[:3000]}\n```\n\n"
                f"⚠️ Reply '确认修改' or 'confirm' to proceed.\n"
                f"Reply '取消' or 'cancel' to abort."
            )

        # Confirmed → backup + push + log
        # Step 2: Backup old version
        backup_path = await _github_backup(file_path, old_content)
        backup_info = f"`{backup_path}`" if backup_path else "backup failed"

        # Step 3: Push new content
        result = await _github_put_file(file_path, content, commit_message, sha)

        # Step 4: Log the change
        if "✅" in result:
            await _github_log_change(file_path, "MODIFY", commit_message, backup_info)
            result += f"\n📦 Backup saved: {backup_info}"
            result += f"\n📝 Change logged to logs/changelog.md"

        return result

    except Exception as e:
        return f"❌ GitHub error: {str(e)}"


async def execute_github_read(file_path: str) -> str:
    """Read a file from GitHub"""
    if not GITHUB_TOKEN:
        return "❌ GitHub token not configured"

    try:
        content, _ = await _github_get_file(file_path)
        if content is not None:
            return content
        return f"❌ File not found in repo: {file_path}"
    except Exception as e:
        return f"❌ GitHub error: {str(e)}"


async def execute_github_changelog(limit: int = 20) -> str:
    """View recent changelog entries"""
    if not GITHUB_TOKEN:
        return "❌ GitHub token not configured"

    try:
        content, _ = await _github_get_file("logs/changelog.md")
        if content is None:
            return "📝 No changelog yet. Changes will be logged automatically."

        lines = content.strip().split("\n")
        # Return header + last N entries
        header = "\n".join(lines[:5])
        entries = lines[5:]
        recent = entries[-limit:] if len(entries) > limit else entries

        return header + "\n" + "\n".join(recent)

    except Exception as e:
        return f"❌ Error: {str(e)}"


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
        args["file_path"], args["content"], args["commit_message"],
        args.get("confirmed", False)
    ),
    "github_read": lambda args: execute_github_read(args["file_path"]),
    "github_changelog": lambda args: execute_github_changelog(args.get("limit", 20)),
}


async def execute_tool(name: str, arguments: dict) -> str:
    """Route and execute a tool call"""
    executor = TOOL_EXECUTORS.get(name)
    if not executor:
        return f"❌ Unknown tool: {name}"
    return await executor(arguments)
