import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

SECRET_KEY = os.environ.get("SECRET_KEY", "upfolio-dev-secret-key")

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
