import dotenv
import os
from os import path

dotenv.load_dotenv()
HOST = os.environ["host"]
DB_NAME = os.environ["dbname"]
USER = os.environ["user"]
PASSWORD = os.environ["password"]

CONN_STRING = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"

# path to root dir to access logs
ROOT_DIR = path.join(path.dirname(path.abspath(__file__)), "..", ".." ,"..")