"""
OskrisAgent - Telegram Bot Handler
Main entry point for the application
"""

import asyncio
import logging
import time
import platform
import psutil
from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from telegram.constants import ChatAction, ParseMode
from core.config import (
    TELEGRAM_BOT_TOKEN, OWNER_TELEGRAM_ID,
    validate, CLAUDE_MODEL, MAX_MESSAGE_LENGTH
)
from core.agent import agent
from core.memory import memory

# Logging setup
logging.basicConfig(
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("bot")

START_TIME = time.time()


# ============================================================
# Auth middleware
# ============================================================

def owner_only(func):
    """Decorator: only allow the owner to use the bot"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != OWNER_TELEGRAM_ID:
            await update.message.reply_text("⛔ Unauthorized. This bot is private.")
            logger.warning(f"Unauthorized access attempt: {update.effective_user.id}")
            return
        return await func(update, context)
    return wrapper


# ============================================================
# Command Handlers
# ============================================================

@owner_only
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *OskrisAgent Online*\n\n"
        "直接发消息跟我聊天，我可以：\n"
        "• 执行VPS命令\n"
        "• 管理文件和代码\n"
        "• 搜索网络信息\n"
        "• 同步GitHub\n\n"
        "命令：\n"
        "/status - 系统状态\n"
        "/clear - 清除对话记录\n"
        "/exec <cmd> - 直接执行命令",
        parse_mode=ParseMode.MARKDOWN
    )


@owner_only
async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = time.time() - START_TIME
    hours, remainder = divmod(int(uptime), 3600)
    minutes, seconds = divmod(remainder, 60)

    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    mem_stats = memory.get_stats()

    status = (
        "📊 *System Status*\n\n"
        f"⏱ Uptime: {hours}h {minutes}m {seconds}s\n"
        f"🧠 Model: `{CLAUDE_MODEL}`\n"
        f"💾 RAM: {mem.percent}% ({mem.used // (1024**3)}/{mem.total // (1024**3)} GB)\n"
        f"💿 Disk: {disk.percent}% ({disk.used // (1024**3)}/{disk.total // (1024**3)} GB)\n"
        f"🐧 OS: {platform.system()} {platform.release()}\n\n"
        f"💬 Conversations: {mem_stats['total_conversations']}\n"
        f"📝 Total messages: {mem_stats['total_messages']}\n"
    )

    await update.message.reply_text(status, parse_mode=ParseMode.MARKDOWN)


@owner_only
async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    memory.clear_history(chat_id)
    await update.message.reply_text("🗑️ 对话记录已清除")


@owner_only
async def cmd_exec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Direct command execution without Claude"""
    command = " ".join(context.args) if context.args else ""
    if not command:
        await update.message.reply_text("用法: /exec <command>")
        return

    await update.message.reply_text(f"🖥️ Executing: `{command}`", parse_mode=ParseMode.MARKDOWN)

    from core.tools import execute_bash
    result = await execute_bash(command)

    # Split long results
    for chunk in _split_message(f"```\n{result}\n```"):
        await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)


# ============================================================
# Message Handler (Main chat)
# ============================================================

@owner_only
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages - send to Claude Agent"""
    user_message = update.message.text
    chat_id = str(update.effective_chat.id)

    if not user_message:
        return

    # Show typing indicator
    await update.message.chat.send_action(ChatAction.TYPING)

    # Status callback for tool use updates
    status_message = None

    async def on_status(text: str):
        nonlocal status_message
        try:
            if status_message:
                await status_message.edit_text(f"⚙️ {text}")
            else:
                status_message = await update.message.reply_text(f"⚙️ {text}")
        except Exception:
            pass

    try:
        # Process through Claude Agent
        response = await agent.process(chat_id, user_message, on_status=on_status)

        # Delete status message if exists
        if status_message:
            try:
                await status_message.delete()
            except Exception:
                pass

        # Send response (split if needed)
        for chunk in _split_message(response):
            await update.message.reply_text(
                chunk,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Error: {str(e)[:500]}")


# ============================================================
# File Handler
# ============================================================

@owner_only
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads"""
    doc = update.message.document
    if not doc:
        return

    # Download file
    file = await context.bot.get_file(doc.file_id)
    save_path = f"/tmp/uploads/{doc.file_name}"
    import os
    os.makedirs("/tmp/uploads", exist_ok=True)
    await file.download_to_drive(save_path)

    # Tell Claude about it
    caption = update.message.caption or ""
    msg = f"[User uploaded file: {doc.file_name} saved at {save_path}]\n{caption}"

    await update.message.chat.send_action(ChatAction.TYPING)
    chat_id = str(update.effective_chat.id)
    response = await agent.process(chat_id, msg)

    for chunk in _split_message(response):
        await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)


# ============================================================
# Utilities
# ============================================================

def _split_message(text: str, max_len: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Split message into Telegram-compatible chunks"""
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break

        # Try to split at newline
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = max_len

        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    return chunks


# ============================================================
# Main
# ============================================================

async def post_init(app: Application):
    """Set bot commands menu"""
    commands = [
        BotCommand("start", "启动机器人"),
        BotCommand("status", "系统状态"),
        BotCommand("clear", "清除对话记录"),
        BotCommand("exec", "直接执行命令"),
    ]
    await app.bot.set_my_commands(commands)
    logger.info("Bot commands set")


def main():
    # Validate config
    errors = validate()
    if errors:
        for e in errors:
            logger.error(f"Config error: {e}")
        logger.error("Fix the above errors in .env file")
        return

    logger.info(f"Starting OskrisAgent with model {CLAUDE_MODEL}")

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Register handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(CommandHandler("exec", cmd_exec))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start polling
    logger.info("Bot is running... Press Ctrl+C to stop")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
