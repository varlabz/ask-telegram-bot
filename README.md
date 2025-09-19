# varlabzbot

A Telegram bot that provides AI-powered answers to questions in a specific chat or topic thread.

## Features

- Activate the bot in a Telegram chat/topic using `/start`
- Ask questions with prefixes: `?`, `/ask`, or `/вопрос`
- Deactivate the bot with `/stop`
- Responses are generated using an AI agent configured via YAML files

## Getting Started

1. Ensure `uv` is installed.
2. Install dependencies: `uv sync`
3. Set up your Telegram bot token in a `.key` file as `TELEGRAM_TOKEN=your_token_here`
4. Configure the AI agent by creating `bot.yaml` and `~/.config/ask/llm-ollama.yaml` files
5. Run the bot: `uv run main.py`

## Usage

- Send `/start` in the desired chat/topic to activate the bot
- Ask questions by prefixing with `?`, `/ask`, or `/вопрос`
- The bot will only respond in the activated chat/topic
- Send `/stop` to deactivate the bot

## Requirements

- Python (managed via uv)
- Dependencies: `ask`, `python-telegram-bot`, `python-dotenv`

Install dependencies with:
```
uv sync
```

Or add new dependencies with `uv add <package>`.
