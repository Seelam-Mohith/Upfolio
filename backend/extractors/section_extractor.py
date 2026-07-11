import re
from utils.logger import logger
from utils.patterns import SECTION_HEADINGS, _SECTION_PATTERN, _GENERIC_HEADER

# Canonical names that each extractor understands.
_CANONICAL_MAP: dict[str, str] = {
    "summary": "summary",
    "profile": "summary",
    "objective": "summary",
    "about": "summary",
    "about me": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "tech stack": "skills",
    "technologies": "skills",
    "programming languages": "skills",
    "tools and technologies": "skills",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "employment history": "experience",
    "internships": "experience",
    "internship experience": "experience",
    "projects": "projects",
    "personal projects": "projects",
    "key projects": "projects",
    "notable projects": "projects",
    "education": "education",
    "academic background": "education",
    "certifications": "certifications",
    "certificates": "certifications",
    "licenses": "certifications",
    "achievements": "achievements",
    "awards": "achievements",
    "honors": "achievements",
    "extracurricular": "achievements",
    "publications": "achievements",
    "contact": "contact",
    "contact information": "contact",
    "personal information": "contact",
    "references": "references",
    "languages": "languages",
    "volunteer": "volunteer",
    "volunteer experience": "volunteer",
}


def extract_sections(text: str) -> dict[str, str]:
    """Split resume text into named sections.

    Returns a dict mapping canonical section names to their text content.
    Sections that are not recognised are stored under their original heading.
    """
    lines = text.splitlines()
    boundaries: list[tuple[int, str, str]] = []  # (line_idx, heading_key, canonical)

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        # Check against known heading patterns
        m = _SECTION_PATTERN.match(stripped)
        if m:
            key = m.group(1).strip().lower()
            canonical = _CANONICAL_MAP.get(key, key)
            boundaries.append((idx, key, canonical))
            continue

        # Heuristic: short, all-caps or Title Case line that isn't a bullet
        if len(stripped) < 40 and not stripped.startswith(("•", "-", "*", "►")):
            if _GENERIC_HEADER.match(stripped):
                low = stripped.lower().rstrip(":").rstrip("-").strip()
                canonical = _CANONICAL_MAP.get(low, low)
                # Only treat as a heading if it looks like a known section
                if canonical in _CANONICAL_MAP.values():
                    boundaries.append((idx, low, canonical))

    # Fallback: if no headings found, treat the whole text as one block
    if not boundaries:
        logger.warning("No section headings detected — treating entire text as a single block")
        return {"raw": text.strip()}

    sections: dict[str, str] = {}
    for i, (start, key, canonical) in enumerate(boundaries):
        end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(lines)
        body = "\n".join(lines[start + 1 : end]).strip()
        # Merge duplicate sections
        if canonical in sections:
            sections[canonical] += "\n\n" + body
        else:
            sections[canonical] = body

    logger.info("Extracted %d sections: %s", len(sections), list(sections.keys()))
    return sections
