import re
from utils.patterns import SKILLS_DB
from models.job_requirements import JobRequirements
from nlp.tfidf import extract_unique_keywords
from utils.logger import logger

# ---------------------------------------------------------------------------
# Flatten the skills database into a case-insensitive lookup of aliases.
# Duplicate aliases (e.g. "Scikit-learn" / "scikit-learn", "Pytest" / "pytest")
# collapse to a single canonical name — the first (prettiest) form wins.
# ---------------------------------------------------------------------------

_SKILL_ALIASES: dict[str, str] = {}
for _category, skills in SKILLS_DB.items():
    for skill in skills:
        _SKILL_ALIASES.setdefault(skill.lower(), skill)

_SKILL_PATTERNS: list[tuple[re.Pattern, str]] = [
    (
        re.compile(r"(?<![a-zA-Z])" + re.escape(alias) + r"(?![a-zA-Z])"),
        canonical,
    )
    for alias, canonical in _SKILL_ALIASES.items()
]

# ---------------------------------------------------------------------------
# JD section headings mapped to canonical section names.
# ---------------------------------------------------------------------------

_JD_SECTIONS: dict[str, str] = {
    "job summary": "summary",
    "summary": "summary",
    "about the role": "summary",
    "about this role": "summary",
    "role overview": "summary",
    "position summary": "summary",
    "overview": "summary",
    "responsibilities": "responsibilities",
    "duties": "responsibilities",
    "duties and responsibilities": "responsibilities",
    "key responsibilities": "responsibilities",
    "what you will do": "responsibilities",
    "what you'll do": "responsibilities",
    "required skills": "required_skills",
    "requirements": "required_skills",
    "required qualifications": "required_skills",
    "qualifications": "required_skills",
    "skills and qualifications": "required_skills",
    "what we are looking for": "required_skills",
    "what you will need": "required_skills",
    "what you bring": "required_skills",
    "must haves": "required_skills",
    "preferred skills": "preferred_skills",
    "nice to have": "preferred_skills",
    "nice-to-have": "preferred_skills",
    "good to have": "preferred_skills",
    "bonus points": "preferred_skills",
    "preferred qualifications": "preferred_skills",
    "experience": "experience",
    "experience required": "experience",
    "experience requirements": "experience",
    "years of experience": "experience",
    "education": "education",
    "education requirements": "education",
    "educational qualifications": "education",
    "ats keywords": "keywords",
    "keywords": "keywords",
    "benefits": "benefits",
    "what we offer": "benefits",
    "perks": "benefits",
}

_EXPERIENCE_PATTERN = re.compile(
    r"(\d{1,2})\s*[-–—to]+\s*(\d{1,2})\s*\+?\s*(?:years|yrs)"
    r"|(\d{1,2})\s*\+?\s*(?:years|yrs)",
    re.IGNORECASE,
)

_EDUCATION_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(?:bachelor(?:'s)?|master(?:'s)?|associate(?:'s)?|diploma|doctorate|"
    r"phd|ph\.?d\.?|mba|m\.?b\.?a\.?|b\.?s\.?|b\.?a\.?|b\.?e\.?|"
    r"b\.?tech\.?|m\.?s\.?|m\.?a\.?|m\.?tech\.?)"
    r"(?![A-Za-z0-9_])",
    re.IGNORECASE,
)

_EDUCATION_INDICATOR = re.compile(
    r"(?<![A-Za-z0-9_])(?:degree|related field|computer science|engineering)"
    r"(?![A-Za-z0-9_])",
    re.IGNORECASE,
)

_BULLET_LEAD = re.compile(r"^[\s]*[•\-\*\►\▹\d.)]+\s*")


def _match_heading(stripped: str) -> str | None:
    """Return the canonical section name for a heading line, or None."""
    key = stripped.rstrip(":").strip().lower()
    if key in _JD_SECTIONS:
        return _JD_SECTIONS[key]
    cleaned = re.sub(r"^[•\-\*\►\▹\s]+", "", key).strip()
    if cleaned in _JD_SECTIONS:
        return _JD_SECTIONS[cleaned]
    return None


def _split_sections(text: str) -> dict[str, str]:
    """Split JD text into named sections keyed by canonical names."""
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        heading = _match_heading(stripped)
        if heading is not None:
            current = heading
            sections.setdefault(current, [])
            continue

        if current is None:
            sections.setdefault("preamble", []).append(stripped)
        else:
            sections[current].append(stripped)

    return {k: "\n".join(v) for k, v in sections.items()}


def _match_skills(text: str) -> list[str]:
    """Find all known skills in the text.

    Overlapping aliases are deduplicated greedily so that the longest match
    wins (e.g. "React.js" beats "React", "React Native" beats "React").
    """
    if not text:
        return []

    lowered = text.lower()
    matches: list[tuple[int, int, str]] = []
    for pattern, canonical in _SKILL_PATTERNS:
        for m in pattern.finditer(lowered):
            matches.append((m.start(), m.end(), canonical))

    matches.sort(key=lambda t: (t[0], -(t[1] - t[0])))

    selected: list[tuple[int, int, str]] = []
    occupied: list[tuple[int, int]] = []
    for start, end, canonical in matches:
        if any(start < o_end and end > o_start for o_start, o_end in occupied):
            continue
        occupied.append((start, end))
        selected.append((start, canonical))

    seen: dict[str, None] = {}
    ordered: list[str] = []
    for start, canonical in sorted(selected, key=lambda t: t[0]):
        if canonical not in seen:
            seen[canonical] = None
            ordered.append(canonical)

    return ordered


def _extract_title(text: str, sections: dict[str, str]) -> str:
    candidates = sections.get("preamble", "").splitlines()
    if not candidates and sections.get("summary"):
        candidates = sections["summary"].splitlines()
    if not candidates:
        candidates = text.splitlines()

    for line in candidates:
        stripped = _BULLET_LEAD.sub("", line).strip()
        if not stripped or len(stripped) > 60:
            continue
        if stripped.endswith((".", ",", ";", ":")):
            continue
        if _match_heading(stripped) is not None:
            continue
        return stripped
    return ""


def _extract_experience(text: str) -> str:
    m = _EXPERIENCE_PATTERN.search(text)
    if not m:
        return ""
    if m.group(1) and m.group(2):
        return f"{m.group(1)}-{m.group(2)} Years"
    if m.group(3):
        return f"{m.group(3)}+ Years"
    return ""


def _extract_education(sections: dict[str, str]) -> list[str]:
    edu_text = sections.get("education", "")
    if edu_text:
        scope = edu_text
    else:
        # No dedicated education section — only pick up clear degree mentions
        # from the summary, requirements, and experience sections.
        scope = "\n".join(
            [
                sections.get("summary", ""),
                sections.get("required_skills", ""),
                sections.get("experience", ""),
            ]
        )

    results: list[str] = []
    for line in scope.splitlines():
        stripped = _BULLET_LEAD.sub("", line).strip()
        if not stripped:
            continue
        is_degree = bool(_EDUCATION_TOKEN.search(stripped))
        is_related = bool(edu_text and _EDUCATION_INDICATOR.search(stripped))
        if is_degree or is_related:
            if stripped not in results:
                results.append(stripped)
    return results


def _extract_keywords(keywords_text: str, fallback: list[str]) -> list[str]:
    if not keywords_text:
        return fallback
    parts = re.split(r"[,;\n]+", keywords_text)
    keywords: list[str] = []
    for part in parts:
        cleaned = _BULLET_LEAD.sub("", part).strip()
        if cleaned and cleaned not in keywords:
            keywords.append(cleaned)
    return keywords


def extract_jd_requirements(text: str) -> dict:
    """Parse a job description into structured requirements.

    This is the main entry point: raw JD text goes in, structured
    requirements come out (skills, keywords, experience, education...).
    """
    if not text or not text.strip():
        return JobRequirements().model_dump()

    sections = _split_sections(text)

    required_text = sections.get("required_skills", "")
    preferred_text = sections.get("preferred_skills", "")
    summary_text = sections.get("summary", "")
    responsibility_text = sections.get("responsibilities", "")

    skills_source = required_text or f"{summary_text}\n{responsibility_text}"
    required_skills = _match_skills(skills_source) or _match_skills(
        "\n".join(sections.values())
    )
    preferred_skills = _match_skills(preferred_text)

    keywords = _extract_keywords(sections.get("keywords", ""), required_skills)

    discovered_keywords = extract_unique_keywords(text, top_n=15)

    experience = _extract_experience(
        sections.get("experience", "") or "\n".join(sections.values())
    )

    education = _extract_education(sections)

    responsibilities = [
        _BULLET_LEAD.sub("", line).strip()
        for line in responsibility_text.splitlines()
        if _BULLET_LEAD.sub("", line).strip()
    ]

    requirements = JobRequirements(
        title=_extract_title(text, sections),
        skills=required_skills,
        preferred_skills=preferred_skills,
        keywords=keywords,
        discovered_keywords=discovered_keywords,
        experience_years=experience,
        education=education,
        responsibilities=responsibilities,
    )

    logger.info(
        "Parsed JD: %d required skills, %d preferred, %d keywords, experience=%s",
        len(required_skills),
        len(preferred_skills),
        len(keywords),
        experience or "(none)",
    )

    return requirements.model_dump()
