import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN=os.getenv("TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("token telegram introvable")
