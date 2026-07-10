from pathlib import Path
import fitz  # PyMuPDF
from utils.logger import logger


class PDFParser:
    """Extract text from PDF files using PyMuPDF with pdfplumber fallback."""

    def extract_text(self, path: Path) -> tuple[str, int]:
        text = ""
        pages = 0

        try:
            doc = fitz.open(str(path))
            pages = len(doc)
            for page in doc:
                text += page.get_text()
            doc.close()
            logger.info("PyMuPDF extracted %d pages from %s", pages, path.name)
        except Exception as e:
            logger.warning("PyMuPDF failed for %s: %s. Trying pdfplumber...", path.name, e)
            text, pages = self._fallback(path)

        return text, pages

    def _fallback(self, path: Path) -> tuple[str, int]:
        try:
            import pdfplumber

            text = ""
            with pdfplumber.open(str(path)) as pdf:
                pages = len(pdf.pages)
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text
            logger.info("pdfplumber extracted %d pages from %s", pages, path.name)
            return text, pages
        except Exception as e:
            logger.error("pdfplumber also failed for %s: %s", path.name, e)
            return "", 0
