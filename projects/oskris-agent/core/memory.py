"""
Conversation Memory Store
Persists conversation history to disk as JSON
"""

import json
import time
from pathlib import Path
from typing import Optional
from core.config import MEMORY_DIR, MAX_HISTORY_MESSAGES


class MemoryStore:
    def __init__(self):
        self.conversations: dict[str, list] = {}
        self.metadata_file = MEMORY_DIR / "metadata.json"
        self._load_metadata()

    def _load_metadata(self):
        if self.metadata_file.exists():
            try:
                self.metadata = json.loads(self.metadata_file.read_text())
            except Exception:
                self.metadata = {"created": time.time(), "total_messages": 0}
        else:
            self.metadata = {"created": time.time(), "total_messages": 0}

    def _save_metadata(self):
        self.metadata_file.write_text(json.dumps(self.metadata, indent=2))

    def _conversation_file(self, chat_id: str) -> Path:
        return MEMORY_DIR / f"chat_{chat_id}.json"

    def get_history(self, chat_id: str) -> list:
        """Get conversation history for a chat"""
        chat_id = str(chat_id)
        if chat_id not in self.conversations:
            filepath = self._conversation_file(chat_id)
            if filepath.exists():
                try:
                    data = json.loads(filepath.read_text())
                    self.conversations[chat_id] = data.get("messages", [])
                except Exception:
                    self.conversations[chat_id] = []
            else:
                self.conversations[chat_id] = []
        return self.conversations[chat_id][-MAX_HISTORY_MESSAGES:]

    def add_message(self, chat_id: str, role: str, content):
        """Add a message to conversation history"""
        chat_id = str(chat_id)
        if chat_id not in self.conversations:
            self.get_history(chat_id)

        self.conversations[chat_id].append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })

        # Trim to max
        if len(self.conversations[chat_id]) > MAX_HISTORY_MESSAGES * 2:
            self.conversations[chat_id] = self.conversations[chat_id][-MAX_HISTORY_MESSAGES:]

        self._save_conversation(chat_id)
        self.metadata["total_messages"] = self.metadata.get("total_messages", 0) + 1
        self._save_metadata()

    def _save_conversation(self, chat_id: str):
        filepath = self._conversation_file(chat_id)
        data = {
            "chat_id": chat_id,
            "updated": time.time(),
            "messages": self.conversations[chat_id]
        }
        filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def clear_history(self, chat_id: str):
        """Clear conversation history"""
        chat_id = str(chat_id)
        self.conversations[chat_id] = []
        filepath = self._conversation_file(chat_id)
        if filepath.exists():
            filepath.unlink()

    def get_stats(self) -> dict:
        """Get memory statistics"""
        total_convos = len(list(MEMORY_DIR.glob("chat_*.json")))
        return {
            "total_conversations": total_convos,
            "total_messages": self.metadata.get("total_messages", 0),
            "active_in_memory": len(self.conversations),
        }


# Singleton
memory = MemoryStore()
