from flask import Blueprint, request, jsonify
from pathlib import Path
from utils.logger import logger
from utils.file_utils import save_upload, clean_text
from parsers.pdf_parser import PDFParser
from parsers.docx_parser import DocxParser

analyze_bp = Blueprint("analyze", __name__)

EXTENSION_PARSER_MAP = {
    ".pdf": PDFParser,
    ".docx": DocxParser,
}


@analyze_bp.route("/api/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        logger.warning("No 'resume' field in request")
        return jsonify({"success": False, "error": "No resume file provided"}), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({"success": False, "error": "Empty filename"}), 400

    path = save_upload(file)
    if path is None:
        return jsonify({"success": False, "error": "Invalid file or file too large"}), 400

    ext = path.suffix.lower()
    parser_cls = EXTENSION_PARSER_MAP.get(ext)

    if parser_cls is None:
        logger.error("No parser registered for extension: %s", ext)
        return jsonify({"success": False, "error": "Unsupported file format"}), 400

    parser = parser_cls()
    raw_text, pages = parser.extract_text(path)

    text = clean_text(raw_text)

    logger.info(
        "Parsed %s — %d pages, %d characters",
        path.name, pages, len(text),
    )

    return jsonify({
        "success": True,
        "filename": path.name,
        "pages": pages,
        "text": text,
    }), 200
