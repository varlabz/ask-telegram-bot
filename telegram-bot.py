#!/usr/bin/env -S uvx --from git+https://github.com/varlabz/ask ask-run 

import json
import sys
from textwrap import dedent
from typing import Final, cast
from ask import AgentASK
from telegram import Message, Update, constants
from telegram.ext import Application, MessageHandler, filters, ContextTypes, PrefixHandler

DEFAULT_BOT_CONFIG_FILE: Final[str] = '.bot-config.json'

def save_config(config, filename=DEFAULT_BOT_CONFIG_FILE) -> None:
    with open(filename, 'w') as f: json.dump(config, f, indent=4)

def load_config(filename=DEFAULT_BOT_CONFIG_FILE) -> dict:
    try:
        with open(filename, 'r') as f: return json.load(f)
    except FileNotFoundError:
        return {}

config = {}

agent = AgentASK.create_from_file(["bot.yaml", "bot-llm.yaml"])
agent_reply = AgentASK.create_from_file(["bot-reply.yaml", "bot-llm.yaml"])

async def _reply(text: str) -> str:
    return await agent_reply.run(text)

def _get_topic_id(message: Message) -> int | None:
    """
    Returns the topic ID for any message in a forum-enabled group,
    correctly handling forwarded messages and replies.
    
    Args:
        message: The Message object received from an update.

    Returns:
        The topic ID as an integer (1 for the General topic),
        or None if not a topic-enabled group.
    """
    if message.chat.type != constants.ChatType.SUPERGROUP or not message.chat.is_forum:
        return None

    # Replies: use replied message to infer topic; General when not a topic message
    if message.reply_to_message:
        replied = message.reply_to_message
        replied.is_topic_message
        if replied.is_topic_message:
            # In a real forum topic
            if replied.message_thread_id:
                return replied.message_thread_id
        else:
            # Reply in General topic
            return 1

    # Not a reply: decide by current message flags
    if message.is_topic_message:
        if message.message_thread_id:
            return message.message_thread_id
        # Fallback: treat as General if no thread id provided
        return 1

    # General topic message (no topic flags)
    return 1
          
async def control(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text == "/start":
        config["chat_id"] = update.message.chat.id
        config["topic_id"] = _get_topic_id(update.message)
        save_config(config)
        await update.message.reply_text(await _reply("Бот активирован и будет отвечать в этой теме."))
  
    if update.message and (update.message.text == "/stop" or update.message.text == "/shut-up"):
        config.pop("chat_id", None)
        config.pop("topic_id", None)
        save_config(config)
        await update.message.reply_text(await _reply("Бот деактивирован и больше не будет отвечать в этой теме."))

    if update.message and update.message.text == "/status":
        chat_id = config.get("chat_id")
        topic_id = config.get("topic_id")
        if chat_id is None:
            return await update.message.reply_text(await _reply("Бот не активирован. Используйте /start в нужной теме."))
        if update.message.chat.id == chat_id and _get_topic_id(update.message) == topic_id:
            return await update.message.reply_text(await _reply("Бот активирован и участвует в теме"))
        else:
            return await update.message.reply_text(await _reply("Бот активирован, но не участвует в этой теме. Используйте /start в нужной теме."))

    if update.message and update.message.text == "/help":
        await update.message.reply_text(dedent("""
            Используйте /start в нужной теме, чтобы активировать бот.
            Задавайте вопросы с префиксом `?` или /ask.
            Используйте /stop, чтобы деактивировать бот.
            Используйте /status, чтобы проверить статус бот.
            Бот отвечает только в теме, где он был активирован.
        """))

async def ask(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if (update.message is None):
        print("no message", file=sys.stderr)
        return

    chat_id = config.get("chat_id")
    topic_id = config.get("topic_id")
    if chat_id is None:
        print("bot not activated", file=sys.stderr)
        return

    if not (update.message.chat.id == chat_id and _get_topic_id(update.message) == topic_id):
        await update.message.reply_text(await _reply("Это не место для дискуссий."))
        return

    if not update.message.text:
        print("no text", file=sys.stderr)
        await update.message.reply_text(await _reply("NO TEXT"))
        return

    question = update.message.text.strip()
    if update.message and question:
        print(f">>> {question}", file=sys.stderr)
        response = await agent.run(question)
        print(f"<<< {response}", file=sys.stderr)
        await update.message.reply_text(f"{response}\n\n{str(agent.stat)}")

async def photo(update, _: ContextTypes.DEFAULT_TYPE):
    # Get the largest available photo from the message
    # photo_file = update.message.photo[-1].get_file() 
    # Download the photo to a specific path
    # await photo_file.download_to_drive('received_image.jpg') 
    # You can also process the image in memory without saving it to a file
    # from io import BytesIO
    # image_bytes = await photo_file.download_as_bytearray()
    # img = Image.open(BytesIO(image_bytes)) 
    # Now 'img' is a PIL Image object you can work with
    if update.message.photo:
        await update.message.reply_text("Image received and ignored!") 

def main():
    """Starts the bot."""
    global config
    config = load_config()
    if (token := config.get("telegram_token")) is None:
        print("Error: TELEGRAM_TOKEN not found")
        exit(1)

    application = Application.builder().token(token).build()
    # application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^\?"), ask))
    # application.add_handler(PrefixHandler("/", {"ask", "вопрос"}, ask))
    application.add_handler(PrefixHandler("/", {"start", "stop", "shut-up", "status", "help"}, control))
    # application.add_handler(CommandHandler("ask", ask))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    # application.add_handler(MessageHandler(filters.PHOTO, photo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()