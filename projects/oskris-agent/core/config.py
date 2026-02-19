"""
OskrisAgent Configuration
All sensitive values loaded from environment variables or .env file
"""

import os
from pathlib import Path

# Load .env file if exists
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

# === Required ===
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OWNER_TELEGRAM_ID = int(os.environ.get("OWNER_TELEGRAM_ID", "0"))

# === Claude Settings ===
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "8192"))
SYSTEM_PROMPT_FILE = Path(__file__).parent.parent / "system_prompt.md"

# === GitHub ===
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "krisliong1/oskris")

# === Paths ===
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MEMORY_DIR = DATA_DIR / "memory"
LOGS_DIR = DATA_DIR / "logs"
SKILLS_DIR = BASE_DIR / "skills"

# Create directories
for d in [DATA_DIR, MEMORY_DIR, LOGS_DIR, SKILLS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# === Limits ===
MAX_MESSAGE_LENGTH = 4096  # Telegram limit
MAX_HISTORY_MESSAGES = 30  # Keep last N messages in context
COMMAND_TIMEOUT = 120  # Bash command timeout in seconds
MAX_FILE_SIZE = 50 * 1024  # Max file content to show (50KB)

# === Security ===
ALLOWED_COMMANDS_PREFIXES = []  # Empty = allow all (owner only anyway)
BLOCKED_COMMANDS = ["rm -rf /", "mkfs", "dd if="]  # Safety blocklist


def validate():
    """Validate required config"""
    errors = []
    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN not set")
    if not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY not set")
    if OWNER_TELEGRAM_ID == 0:
        errors.append("OWNER_TELEGRAM_ID not set")
    return errors
