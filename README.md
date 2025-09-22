# varlabzbot

A Telegram bot that provides AI-powered answers to questions in a specific chat or topic thread.

## Features

- Activate the bot in a Telegram chat/topic using `/start`
- In the activated topic, any message is treated as a question
- Deactivate the bot with `/stop`
- Responses are generated using an AI agent configured via YAML files

## Running with Docker

You can run the bot using Docker Compose:

1. Create a `.key` file in the project root with your Telegram token:

   ```
   TELEGRAM_TOKEN=your_telegram_token_here
   ```

2. Build and run the bot:

   ```bash
   docker compose up --build
   ```

   The bot will start and use a persistent volume for caching and configuration.

## Usage

- Send `/start` in the desired chat/topic to activate the bot
- In the activated topic, just write your message
- The bot will only respond in the activated chat/topic
- Send `/stop` to deactivate the bot

## Configuration

- `.bot-config.json`: runtime settings for the bot.
  - Auto-managed by the bot: `chat_id`, `topic_id`
 
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

## Getting Started

- Configure the AI agent by editing `bot.yaml`, `bot-llm.yaml`, and `bot-reply.yaml`
- Run the bot: `TELEGRAM_TOKEN=your_telegram_token_here uv run telegram-bot.py`

