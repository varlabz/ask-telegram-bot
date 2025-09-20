# varlabzbot

A Telegram bot that provides AI-powered answers to questions in a specific chat or topic thread.

## Features

- Activate the bot in a Telegram chat/topic using `/start`
- In the activated topic, any message is treated as a question
- Deactivate the bot with `/stop`
- Responses are generated using an AI agent configured via YAML files

## Getting Started

1. Ensure `uv` is installed.
2. Install dependencies: `uv sync`
3. Create `.bot-config.json` and put your Telegram token there
4. Configure the AI agent by editing `bot.yaml`, `bot-llm.yaml`, and `bot-reply.yaml`
5. Run the bot: `uv run telegram-bot.py`

## Usage

- Send `/start` in the desired chat/topic to activate the bot
- In the activated topic, just write your message
- The bot will only respond in the activated chat/topic
- Send `/stop` to deactivate the bot

## Configuration

- `.bot-config.json`: runtime settings for the bot.
  - Required: `telegram_token` (your BotFather token)
  - Auto-managed by the bot: `chat_id`, `topic_id`
  - Example:

    ```json
    {
      "telegram_token": "123456789:ABCDEF..."
    }
    ```

- `bot-llm.yaml`: shared LLM settings merged into agents.
  - Keys: `llm.model`, `llm.base_url`
  - Example:

    ```yaml
    llm:
      model: ollama:qwen3:30b-a3b-instruct-2507-q4_K_M
      base_url: http://localhost:11434/v1/
    ```

- `bot.yaml`: main answering agent.
  - Core instructions and optional MCP tool configs.
  - If you use external tools, set required env vars as needed.

- `bot-reply.yaml`: short, playful reply agent for status/aux messages.

- Activation scope: `/start` in a forum topic stores `chat_id`/`topic_id` in `.bot-config.json`; the bot answers only there until `/stop`.

## Requirements

- Python (managed via uv)
- Dependencies: `ask`, `python-telegram-bot`

Install dependencies with:
```
uv sync
```

Or add new dependencies with `uv add <package>`.
