import re
import secrets
from pathlib import Path
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_FOLDER
from utils.logger import logger


def allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def is_valid_filename(filename: str) -> bool:
    blocked = {"..", "~", "#"}
    return not any(c in filename for c in blocked) and bool(filename.strip())


def save_upload(file_storage) -> Path | None:
    original_name = secure_filename(file_storage.filename or "upload")

    if not is_valid_filename(original_name):
        logger.warning("Invalid filename rejected: %s", original_name)
        return None

    if not allowed_file(original_name):
        logger.warning("File type not allowed: %s", original_name)
        return None

    file_storage.seek(0, 2)
    size = file_storage.tell()
    file_storage.seek(0)

    if size > MAX_FILE_SIZE:
        logger.warning("File too large: %d bytes", size)
        return None

    token = secrets.token_hex(8)
    ext = original_name.rsplit(".", 1)[1].lower()
    safe_name = f"{token}_{original_name}"
    dest = UPLOAD_FOLDER / safe_name

    file_storage.save(str(dest))
    logger.info("Saved upload: %s (%d bytes)", dest.name, size)
    return dest


def clean_text(raw: str) -> str:
    lines = [line.strip() for line in raw.splitlines()]
    lines = [line for line in lines if line]
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text).strip()
    return text
