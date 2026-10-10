import dotenv
import os
from os import path

dotenv.load_dotenv()

# db config
HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
USER = os.environ["DB_USER"]
PASSWORD = os.environ["DB_PASSWORD"]

CONN_STRING = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"

# path to root dir to access logs
ROOT_DIR = os.getenv("ROOT_DIR", path.join(path.dirname(path.abspath(__file__)), "..", ".." ,".."))

# Telegram API keys
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_BOT_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]