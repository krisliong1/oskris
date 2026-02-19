"""
Claude Agent - Core intelligence with tool_use loop
Sends messages to Claude API, handles tool calls, returns final response
"""

import anthropic
import logging
from typing import Callable, Optional
from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS, SYSTEM_PROMPT_FILE
from core.tools import TOOL_DEFINITIONS, execute_tool
from core.memory import memory

logger = logging.getLogger("agent")

# Load system prompt
DEFAULT_SYSTEM = "You are OskrisAgent, a personal AI assistant running on a VPS. You can execute commands, manage files, search the web, and sync with GitHub. Respond in Chinese (华文) by default, keep code/commands in English. Be concise and action-oriented."

def load_system_prompt() -> str:
    if SYSTEM_PROMPT_FILE.exists():
        return SYSTEM_PROMPT_FILE.read_text()
    return DEFAULT_SYSTEM


class Agent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.max_tool_rounds = 10  # Max tool-use iterations per request

    async def process(
        self,
        chat_id: str,
        user_message: str,
        on_status: Optional[Callable] = None
    ) -> str:
        """
        Process a user message through Claude with tool use.
        on_status: callback to send status updates (e.g., "🔧 Running bash...")
        Returns final text response.
        """

        # Get history
        history = memory.get_history(chat_id)

        # Build messages (strip timestamps for API)
        messages = []
        for msg in history:
            content = msg["content"]
            messages.append({"role": msg["role"], "content": content})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Store user message
        memory.add_message(chat_id, "user", user_message)

        system_prompt = load_system_prompt()

        # Tool use loop
        for round_num in range(self.max_tool_rounds):
            try:
                response = self.client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=MAX_TOKENS,
                    system=system_prompt,
                    tools=TOOL_DEFINITIONS,
                    messages=messages
                )
            except anthropic.APIError as e:
                error_msg = f"❌ Claude API error: {str(e)}"
                logger.error(error_msg)
                return error_msg

            # Check if we need to handle tool use
            if response.stop_reason == "tool_use":
                # Extract all content blocks
                assistant_content = []
                tool_calls = []

                for block in response.content:
                    if block.type == "text":
                        assistant_content.append({
                            "type": "text",
                            "text": block.text
                        })
                    elif block.type == "tool_use":
                        assistant_content.append({
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input
                        })
                        tool_calls.append(block)

                # Add assistant's response with tool calls
                messages.append({
                    "role": "assistant",
                    "content": assistant_content
                })

                # Execute tools and build results
                tool_results = []
                for tool_call in tool_calls:
                    if on_status:
                        tool_icon = {
                            "bash": "🖥️",
                            "read_file": "📖",
                            "write_file": "✍️",
                            "list_directory": "📁",
                            "web_search": "🌐",
                            "github_push": "📤",
                            "github_read": "📥",
                        }.get(tool_call.name, "🔧")
                        await on_status(
                            f"{tool_icon} {tool_call.name}: {_summarize_input(tool_call.name, tool_call.input)}"
                        )

                    result = await execute_tool(tool_call.name, tool_call.input)
                    logger.info(f"Tool {tool_call.name} -> {len(result)} chars")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": result[:15000]  # Limit tool result size
                    })

                # Add tool results
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

                continue  # Next round

            else:
                # Final response - extract text
                final_text = ""
                for block in response.content:
                    if block.type == "text":
                        final_text += block.text

                # Store assistant response
                memory.add_message(chat_id, "assistant", final_text)

                return final_text

        return "⚠️ Reached maximum tool iterations. Task may be incomplete."


def _summarize_input(tool_name: str, inp: dict) -> str:
    """Create a short summary of tool input for status updates"""
    if tool_name == "bash":
        cmd = inp.get("command", "")
        return cmd[:80] + ("..." if len(cmd) > 80 else "")
    elif tool_name in ("read_file", "list_directory"):
        return inp.get("path", "")
    elif tool_name == "write_file":
        return inp.get("path", "")
    elif tool_name == "web_search":
        return inp.get("query", "")
    elif tool_name in ("github_push", "github_read"):
        return inp.get("file_path", "")
    return str(inp)[:60]


# Singleton
agent = Agent()
