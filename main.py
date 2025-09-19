import json
import sys
from typing import cast
from ask import AgentASK
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, PrefixHandler
from dotenv import load_dotenv
import os

load_dotenv('.key')
TOKEN = os.getenv('TELEGRAM_TOKEN') or ''
if not TOKEN:
    print("Error: TELEGRAM_TOKEN not found")
    exit(1)

def save_config(config, filename='.bot-config.json'):
    """Save configuration to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

def load_config(filename='.bot-config.json'):
    """Load configuration from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

config = load_config()

agent = AgentASK.create_from_file(["~/.config/ask/llm-ollama.yaml", "bot.yaml"])

async def control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # save chat info, as chat id, topic id,
    if update.message and update.message.text == "/start":
        config["chat_id"] = update.message.chat.id
        config["topic_id"] = update.message.message_thread_id
        save_config(config)
        await update.message.reply_text(f"Бот активирован. Задавайте вопросы с префиксом `?` или /stop")

    if update.message and update.message.text == "/stop":
        config["chat_id"] = None
        config["topic_id"] = None
        save_config(config)
        await update.message.reply_text(f"Бот деактивирован.")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # print(f"ask {update}", file=sys.stderr)
    if (update.message is None):
        print("no message", file=sys.stderr)
        return

    chat_id = config.get("chat_id")
    topic_id = config.get("topic_id")
    if chat_id is None:
        print("no chat_id", file=sys.stderr)
        await update.message.reply_text("Это не место для дискуссий. Используйте /start в нужной теме.")
        return

    if (not (update.message.chat.id == chat_id and update.message.message_thread_id == topic_id)):
        print(f"ignoring chat {update.effective_chat}", file=sys.stderr)
        await update.message.reply_text("Это не место для дискуссий.")
        return
    
    question = None
    for i in {"/ask ", "/вопрос ", "?"}:
        if update.message and update.message.text and update.message.text.startswith(i):
            question = update.message.text.removeprefix(i).strip()
            break

    if update.message and question:
        print(f">>> {question}", file=sys.stderr)
        response = await agent.run(question)
        print(f"<<< {response}", file=sys.stderr)
        await update.message.reply_text(response,)
        
async def photo(update, context):
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
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^\?"), ask))
    application.add_handler(PrefixHandler("/", {"ask", "вопрос"}, ask))
    application.add_handler(PrefixHandler("/", {"start", "stop"}, control))
    # application.add_handler(CommandHandler("ask", ask))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    # application.add_handler(MessageHandler(filters.PHOTO, photo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()