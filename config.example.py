import os

# ============================================================
# config.py — Bot va AI konfiguratsiyasi
# ============================================================

# Telegram Bot token (@BotFather dan oling)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# OpenAI API kalit (https://platform.openai.com dan oling)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# OpenAI model
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Faqat shu Telegram user ID botdan foydalana oladi
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "123456789"))
