from dotenv import load_dotenv
import os
from pathlib import Path

# Find the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = "StratPilot AI"

    BROKER = os.getenv("BROKER", "WEBULL")
    BOT_MODE = os.getenv("BOT_MODE", "SIM")

    WEBULL_APP_KEY = os.getenv("WEBULL_APP_KEY")
    WEBULL_APP_SECRET = os.getenv("WEBULL_APP_SECRET")
    WEBULL_ACCOUNT_ID = os.getenv("WEBULL_ACCOUNT_ID")


settings = Settings()	






