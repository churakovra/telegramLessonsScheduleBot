from os import getenv

from dotenv import load_dotenv

APP_VERSION = getenv("APP_VERSION", "dev")

if APP_VERSION == "qa":
    load_dotenv("tests/.env")
else:
    load_dotenv(".env")

BOT_TOKEN = getenv("BOT_TOKEN")

DB_PORT = int(getenv("DB_PORT") or "5432")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")
