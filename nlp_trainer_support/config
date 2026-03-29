import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("APP_DATA_DIR", str(ROOT_DIR / "data")))
STATIC_DIR = ROOT_DIR / "static"
UPLOADS_DIR = Path(os.getenv("APP_UPLOADS_DIR", str(STATIC_DIR / "uploads")))
DB_PATH = Path(os.getenv("APP_DB_PATH", str(DATA_DIR / "nlp_trainer_support.db")))

APP_TITLE = "NLP Trainer Support Platform"
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")
DEFAULT_PORT = int(os.getenv("PORT", "8080"))
SESSION_HOURS = int(os.getenv("APP_SESSION_HOURS", "12"))
