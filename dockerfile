FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl git && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN npm install -g npm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY telegram-bot.py bot*.yaml ./

ENV UV_CACHE_DIR=/cache/.uv-cache
ENV npm_config_cache=/cache/.npm-cache

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app && \
    mkdir -p /cache && chown appuser:appuser /cache
USER appuser

# Command to run the bot
ENTRYPOINT ["uv", "run"]
CMD ["telegram-bot.py", "--config", "/cache/bot-config.json"]

LABEL description="Docker image for ASK Telegram Bot"
LABEL version="0.1.0"
LABEL repository="https://github.com/varlabz/ask-telegram-bot"
LABEL usage.example=" docker run --rm -it --env-file .key -v varlabzbot_cache:/cache varlabzbot"
