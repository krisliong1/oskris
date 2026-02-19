# OskrisAgent - Personal AI Agent via Telegram

A lightweight personal AI agent that combines Claude's intelligence with system-level tools,
accessible from anywhere via Telegram.

## Architecture

```
Telegram (Phone/Desktop)
        ↓
  Telegram Bot API
        ↓
┌─────────────────────────┐
│   OskrisAgent (VPS)     │
│                         │
│  ┌───────────────────┐  │
│  │   Bot Handler     │  │  ← Receives messages, manages sessions
│  └────────┬──────────┘  │
│           ↓             │
│  ┌───────────────────┐  │
│  │   Claude Agent    │  │  ← Claude API with tool_use
│  └────────┬──────────┘  │
│           ↓             │
│  ┌───────────────────┐  │
│  │   Tool Registry   │  │  ← Bash, Files, GitHub, Web Search
│  └───────────────────┘  │
│                         │
│  ┌───────────────────┐  │
│  │   Memory Store    │  │  ← Conversation history + context
│  └───────────────────┘  │
└─────────────────────────┘
```

## Features

- 💬 Chat with Claude via Telegram
- 🖥️ Execute bash commands on VPS
- 📁 Read/write/manage files
- 🔄 GitHub integration (auto-sync)
- 🧠 Persistent conversation memory
- 🌐 Web search capability
- 🔒 Owner-only access control

## Quick Start

```bash
# On your VPS
cd /opt/oskris-agent
chmod +x install.sh
./install.sh
```

## Commands

- `/start` - Start the bot
- `/clear` - Clear conversation history
- `/status` - Show system status
- `/exec <cmd>` - Execute bash command directly
- `/skills` - List available skills
- Any text message → Chat with Claude
