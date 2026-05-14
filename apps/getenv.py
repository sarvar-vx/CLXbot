from dotenv import load_dotenv
from os import getenv

load_dotenv()

class BotConfig:
    BOT_TOKEN = getenv("BOT_TOKEN")
    CHANNEL_ID = getenv("CHANNEL_ID")
    LOG_CHANNEL = getenv("LOG_CHANNEL")
    BACKUP_CHANNEL = getenv("BACKUP_CHANNEL")
    FEEDBACK_CHANNEL = getenv("FEEDBACK_CHANNEL")


class AdminConfig:
    ADMIN_PASS = getenv("ADMIN_PASS")


class DatabaseConfig:
    DB_URL = getenv("DB_URL")
    POSTGRES_USER = getenv("POSTGRES_USER")
    POSTGRES_DB = getenv("POSTGRES_DB")


class ENV:
    bot = BotConfig()
    db = DatabaseConfig()
    admin = AdminConfig()