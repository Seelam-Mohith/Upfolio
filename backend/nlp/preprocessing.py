import re
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from utils.logger import logger

NLTK_DATA_DIR = Path(__file__).resolve().parent.parent / "nltk_data"

_REQUIRED_PACKAGES = [
    "punkt",
    "averaged_perceptron_tagger",
    "wordnet",
    "omw-1.4",
    "stopwords",
]

# Real NLTK resource paths for each package, used to verify installs.
# (NLTK 3.8.1 needs the explicit .zip suffix for zip-backed corpora.)
_RESOURCE_PATHS = {
    "punkt": "tokenizers/punkt/english.pickle",
    "averaged_perceptron_tagger": "taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle",
    "wordnet": "corpora/wordnet.zip",
    "omw-1.4": "corpora/omw-1.4.zip",
    "stopwords": "corpora/stopwords",
}

_stopwords: set[str] | None = None
_lemmatizer = WordNetLemmatizer()

# Map NLTK POS tags to WordNet part-of-speech codes for better lemmatization.
_POS_MAP = {
    "J": "a",   # adjectives
    "V": "v",   # verbs
    "R": "r",   # adverbs
    "N": "n",   # nouns (default)
}

_NON_ALPHA = re.compile(r"[^a-z]")


def ensure_nltk_data() -> None:
    """Download any missing or corrupt NLTK datasets into nltk_data."""
    NLTK_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if str(NLTK_DATA_DIR) not in nltk.data.path:
        nltk.data.path.insert(0, str(NLTK_DATA_DIR))

    for package in _REQUIRED_PACKAGES:
        try:
            nltk.data.find(_RESOURCE_PATHS[package])
            continue
        except Exception:
            pass  # missing or corrupt — (re)download below

        # Remove any partial/corrupt files before retrying.
        for f in NLTK_DATA_DIR.rglob(f"{package}*"):
            if f.is_file():
                f.unlink()

        logger.info("Downloading NLTK package: %s", package)
        nltk.download(package, download_dir=str(NLTK_DATA_DIR), quiet=True)


def _load_stopwords() -> set[str]:
    global _stopwords
    if _stopwords is None:
        _stopwords = set(stopwords.words("english"))
    return _stopwords


def _wordnet_pos(tag: str) -> str:
    return _POS_MAP.get(tag[0].upper(), "n")


def preprocess_text(text: str) -> list[str]:
    """Tokenize, clean, and lemmatize text.

    Returns lowercased, stopword-free, lemmatized tokens. Plurals collapse
    ("APIs" -> "api", "frameworks" -> "framework") so downstream TF-IDF and
    cosine comparisons are less noisy.

    NOTE: this is used only for similarity/quality analysis. Skill matching
    keeps using the exact regex + SKILLS_DB path.
    """
    if not text or not text.strip():
        return []

    ensure_nltk_data()
    stop = _load_stopwords()

    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if _NON_ALPHA.search(t) is None]
    tokens = [t for t in tokens if t not in stop]

    if not tokens:
        return []

    tagged = pos_tag(tokens)
    return [
        _lemmatizer.lemmatize(word, _wordnet_pos(tag))
        for word, tag in tagged
    ]


def sentence_count(text: str) -> int:
    """Rough sentence count using NLTK sentence tokenization."""
    if not text or not text.strip():
        return 0
    ensure_nltk_data()
    return len(nltk.sent_tokenize(text))
