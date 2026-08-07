from sklearn.feature_extraction.text import TfidfVectorizer

from data.jd_corpus import JD_CORPUS
from nlp.preprocessing import preprocess_text
from utils.logger import logger
from utils.patterns import SKILLS_DB

# Every skill alias the exact matcher already knows, lowercased. Discovered
# TF-IDF terms that match these are dropped so we only surface NEW keywords.
_KNOWN_SKILLS: set[str] = {
    alias.lower() for skills in SKILLS_DB.values() for alias in skills
}

_corpus_processed: list[list[str]] | None = None


def _get_corpus_processed() -> list[list[str]]:
    """Preprocessed corpus texts, cached after the first call."""
    global _corpus_processed
    if _corpus_processed is None:
        _corpus_processed = [preprocess_text(jd["description"]) for jd in JD_CORPUS]
        logger.info("Preprocessed %d corpus JDs for TF-IDF", len(_corpus_processed))
    return _corpus_processed


def _tokenizer(doc):
    """Tokenize strings on the fly but pass pre-tokenized lists through."""
    if isinstance(doc, str):
        return preprocess_text(doc)
    return doc


def _vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(tokenizer=_tokenizer, lowercase=False, token_pattern=None)


def _discovery_vectorizer() -> TfidfVectorizer:
    # Drop terms that appear in most of the corpus (headings like "summary",
    # "job", "experience") — they can't be unique to the pasted JD.
    return TfidfVectorizer(
        tokenizer=_tokenizer,
        lowercase=False,
        token_pattern=None,
        max_df=0.6,
    )


def extract_unique_keywords(jd_text: str, top_n: int = 15) -> list[str]:
    """Discover role-specific keywords via TF-IDF.

    The pasted JD is vectorized against the reference corpus of other JDs.
    Terms with the highest TF-IDF inside the JD are unique to this role —
    the ones the SKILLS_DB exact matcher misses.
    """
    if not jd_text or not jd_text.strip():
        return []

    docs = _get_corpus_processed() + [jd_text]

    vectorizer = _discovery_vectorizer()
    matrix = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()

    jd_row = matrix.getrow(matrix.shape[0] - 1).toarray()[0]
    order = jd_row.argsort()[::-1]

    keywords: list[str] = []
    for idx in order:
        score = jd_row[idx]
        if score <= 0:
            break
        term = feature_names[idx]
        if term in _KNOWN_SKILLS or term in keywords:
            continue
        keywords.append(term)
        if len(keywords) >= top_n:
            break

    return keywords


def cosine_similarity(resume_text: str, jd_text: str) -> float:
    """Semantic relevance of resume vs JD as TF-IDF cosine similarity.

    Returns a value in [0, 1] — 1.0 means identical word usage after
    stopword removal and lemmatization. Scale to 0-100 where needed.
    """
    if not resume_text or not resume_text.strip():
        return 0.0
    if not jd_text or not jd_text.strip():
        return 0.0

    vectorizer = _vectorizer()
    matrix = vectorizer.fit_transform([resume_text, jd_text])

    sim = (matrix[0] @ matrix[1].T).toarray()[0][0]
    return round(float(sim), 4)
