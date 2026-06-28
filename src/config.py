import dotenv
import os

dotenv.load_dotenv()
HOST = os.environ["host"]
DB_NAME = os.environ["dbname"]
USER = os.environ["user"]
PASSWORD = os.environ["password"]