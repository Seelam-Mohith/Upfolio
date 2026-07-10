from pathlib import Path
from docx import Document
from utils.logger import logger


class DocxParser:
    """Extract text from DOCX files using python-docx."""

    def extract_text(self, path: Path) -> tuple[str, int]:
        try:
            doc = Document(str(path))
            paragraphs = [p.text for p in doc.paragraphs]
            text = "\n".join(paragraphs)
            pages = len(doc.sections)
            logger.info("python-docx extracted %d sections from %s", pages, path.name)
            return text, pages
        except Exception as e:
            logger.error("Failed to parse DOCX %s: %s", path.name, e)
            return "", 0
