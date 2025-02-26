from dotenv import load_dotenv
from os import getenv


load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")

BOT_TOKEN = getenv("BOT_TOKEN")
FORUM_CHAT_ID = getenv("FORUM_CHAT_ID")
