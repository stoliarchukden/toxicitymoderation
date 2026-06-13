from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")
DIRECT_URL = os.getenv("DIRECT_URL")

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

DEMO_USERNAME = os.getenv("DEMO_USERNAME", "moderator")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "admin123")


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")