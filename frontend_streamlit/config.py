import os
from dotenv import load_dotenv

DOT_ENV_PATH = os.environ.get("DOT_ENV_PATH", default=".env.local")

load_dotenv(DOT_ENV_PATH)

API_ROOT = "http://" + os.environ.get("API_ROOT")  # type: ignore
