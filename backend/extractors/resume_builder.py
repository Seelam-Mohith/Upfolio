import re
from models.resume_schema import (
    Resume, Education, Experience, Project, Certification,
)
from extractors.section_extractor import extract_sections
from utils.patterns import (
    EMAIL_PATTERN, PHONE_PATTERN, LINKEDIN_PATTERN, GITHUB_PATTERN,
    PORTFOLIO_PATTERN, DEGREE_PATTERN, CGPA_PATTERN, YEAR_PATTERN,
    COLLEGE_KEYWORDS, DATE_RANGE_PATTERN, YEAR_RANGE_PATTERN,
    TECH_LIST_PATTERN, TECH_COLON_PATTERN, PROJECT_BULLET_PATTERN,
    SKILLS_DB,
)
from utils.logger import logger


def _extract_contact(text: str) -> dict:
    """Extract contact information from the top of the resume or full text."""
    contact: dict[str, str] = {
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "portfolio": "",
    }

    # Email
    m = EMAIL_PATTERN.search(text)
    if m:
        contact["email"] = m.group().strip()

    # Phone
    m = PHONE_PATTERN.search(text)
    if m:
        contact["phone"] = m.group().strip()

    # LinkedIn
    m = LINKEDIN_PATTERN.search(text)
    if m:
        contact["linkedin"] = m.group().strip()

    # GitHub
    m = GITHUB_PATTERN.search(text)
    if m:
        contact["github"] = m.group().strip()

    # Portfolio — find URLs that are NOT email, linkedin, or github
    for m in PORTFOLIO_PATTERN.finditer(text):
        url = m.group().strip()
        if "linkedin.com" in url or "github.com" in url:
            continue
        if "@" in url:
            continue
        contact["portfolio"] = url
        break

    # Name — heuristic: first non-empty line that isn't a section heading
    # and doesn't contain email/phone/url
    lines = text.splitlines()
    for line in lines[:10]:
        stripped = line.strip()
        if not stripped or len(stripped) > 60:
            continue
        if EMAIL_PATTERN.search(stripped) or PHONE_PATTERN.search(stripped):
            continue
        if LINKEDIN_PATTERN.search(stripped) or GITHUB_PATTERN.search(stripped):
            continue
        if any(c in stripped for c in "@:/"):
            continue
        # Likely a name if it's 2-5 words, mostly alphabetic
        words = stripped.split()
        if 2 <= len(words) <= 5 and all(w.replace(".", "").replace(",", "").isalpha() for w in words):
            contact["name"] = stripped
            break

    return contact


def _extract_skills(text: str) -> list[str]:
    """Match text against the skills database."""
    found: list[str] = []
    text_lower = text.lower()

    for _category, skills in SKILLS_DB.items():
        for skill in skills:
            # Use word-boundary match to avoid partial hits
            pattern = re.compile(r"(?<![a-zA-Z])" + re.escape(skill) + r"(?![a-zA-Z])", re.IGNORECASE)
            if pattern.search(text) and skill not in found:
                found.append(skill)

    return found


def _extract_education(section_text: str) -> list[dict]:
    """Parse education entries from the education section."""
    education: list[dict] = []
    lines = section_text.splitlines()
    current: dict[str, str] = {
        "college": "", "degree": "", "branch": "", "cgpa": "", "graduation_year": "",
    }

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current["degree"] or current["college"]:
                education.append(current)
                current = {k: "" for k in current}
            continue

        # Degree
        dm = DEGREE_PATTERN.search(stripped)
        if dm:
            if current["degree"] and (current["college"] or current["degree"]):
                education.append(current)
                current = {k: "" for k in current}
            current["degree"] = dm.group().strip()
            # Check if branch/specialization follows the degree
            remainder = stripped[dm.end():].strip().lstrip("in,").strip()
            if remainder and len(remainder) < 60:
                current["branch"] = remainder

        # CGPA
        gm = CGPA_PATTERN.search(stripped)
        if gm:
            current["cgpa"] = gm.group(1)

        # Year
        ym = YEAR_PATTERN.search(stripped)
        if ym:
            current["graduation_year"] = ym.group()

        # College
        cm = COLLEGE_KEYWORDS.search(stripped)
        if cm and not current["college"]:
            current["college"] = stripped

    if current["degree"] or current["college"]:
        education.append(current)

    return education


def _extract_experience(section_text: str) -> list[dict]:
    """Parse experience entries from the experience section."""
    experiences: list[dict] = []
    lines = section_text.splitlines()
    current: dict[str, str] = {"company": "", "role": "", "duration": "", "description": ""}
    desc_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check for date range — signals a new entry or duration of current
        date_match = DATE_RANGE_PATTERN.search(stripped) or YEAR_RANGE_PATTERN.search(stripped)
        if date_match:
            # Save previous entry if exists
            if current["role"] or current["company"]:
                if desc_lines:
                    current["description"] = "\n".join(desc_lines).strip()
                experiences.append(current)
                current = {k: "" for k in current}
                desc_lines = []

            current["duration"] = date_match.group().strip()

            # The rest of the line might be the role or company
            before = stripped[:date_match.start()].strip().rstrip("·•-|")
            after = stripped[date_match.end():].strip().lstrip("·•-|").strip()

            if before:
                # Could be "Role at Company" or just "Role"
                if " at " in before:
                    parts = before.rsplit(" at ", 1)
                    current["role"] = parts[0].strip()
                    current["company"] = parts[1].strip()
                elif " | " in before:
                    parts = before.rsplit(" | ", 1)
                    current["role"] = parts[0].strip()
                    current["company"] = parts[1].strip()
                else:
                    current["role"] = before
            continue

        # If we have a current entry, accumulate description
        if current["role"] or current["company"]:
            desc_lines.append(stripped)
        else:
            # No entry yet — this line might be "Role at Company"
            if not current["role"]:
                if " at " in stripped:
                    parts = stripped.rsplit(" at ", 1)
                    current["role"] = parts[0].strip()
                    current["company"] = parts[1].strip()
                elif " | " in stripped:
                    parts = stripped.rsplit(" | ", 1)
                    current["role"] = parts[0].strip()
                    current["company"] = parts[1].strip()
                else:
                    current["role"] = stripped

    # Don't forget the last entry
    if current["role"] or current["company"]:
        if desc_lines:
            current["description"] = "\n".join(desc_lines).strip()
        experiences.append(current)

    return experiences


def _extract_projects(section_text: str) -> list[dict]:
    """Parse project entries from the projects section."""
    projects: list[dict] = []
    lines = section_text.splitlines()
    current: dict = {"name": "", "description": "", "technologies": []}
    desc_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if this is a bullet point (project entry)
        bullet_match = PROJECT_BULLET_PATTERN.match(stripped)
        if bullet_match:
            # Save previous project
            if current["name"]:
                if desc_lines:
                    current["description"] = "\n".join(desc_lines).strip()
                projects.append(current)
                current = {"name": "", "description": "", "technologies": []}
                desc_lines = []

            project_line = bullet_match.group(1).strip()

            # Check for tech list in parentheses
            tech_match = TECH_LIST_PATTERN.search(project_line)
            if tech_match:
                current["name"] = project_line[:tech_match.start()].strip().rstrip(":")
                current["technologies"] = [
                    t.strip() for t in tech_match.group(1).split(",") if t.strip()
                ]
            else:
                current["name"] = project_line.rstrip(":")
            continue

        # Check for tech colon pattern
        tech_colon = TECH_COLON_PATTERN.match(stripped)
        if tech_colon and current["name"]:
            current["technologies"] = [
                t.strip() for t in tech_colon.group(1).split(",") if t.strip()
            ]
            continue

        # Accumulate description
        if current["name"]:
            desc_lines.append(stripped)

    # Last project
    if current["name"]:
        if desc_lines:
            current["description"] = "\n".join(desc_lines).strip()
        projects.append(current)

    return projects


def _extract_certifications(section_text: str) -> list[dict]:
    """Parse certification entries from the certifications section."""
    certs: list[dict] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Skip lines that are just bullets with no content
        cleaned = re.sub(r"^[•\-\*\►\▹]\s*", "", stripped).strip()
        if cleaned:
            certs.append({"name": cleaned})
    return certs


def build_resume(raw_text: str) -> dict:
    """Convert raw extracted text into a structured Resume dict.

    This is the main entry point: raw text goes in, structured JSON comes out.
    """
    sections = extract_sections(raw_text)

    # Contact info — look in the first ~20 lines or the 'contact' section
    contact_section = sections.get("contact", "")
    header_text = "\n".join(raw_text.splitlines()[:20])
    contact_text = header_text + "\n" + contact_section
    contact = _extract_contact(contact_text)

    # Skills — combine 'skills' section + full text for broader matching
    skills_section = sections.get("skills", "")
    skills_text = skills_section + "\n" + raw_text
    skills = _extract_skills(skills_text)

    # Education
    edu_section = sections.get("education", "")
    education = _extract_education(edu_section)

    # Experience
    exp_section = sections.get("experience", "")
    experience = _extract_experience(exp_section)

    # Projects
    proj_section = sections.get("projects", "")
    projects = _extract_projects(proj_section)

    # Certifications
    cert_section = sections.get("certifications", "")
    certifications = _extract_certifications(cert_section)

    resume = Resume(
        name=contact.get("name", ""),
        email=contact.get("email", ""),
        phone=contact.get("phone", ""),
        linkedin=contact.get("linkedin", ""),
        github=contact.get("github", ""),
        portfolio=contact.get("portfolio", ""),
        skills=skills,
        projects=[Project(**p) for p in projects],
        education=[Education(**e) for e in education],
        experience=[Experience(**e) for e in experience],
        certifications=[Certification(**c) for c in certifications],
    )

    logger.info(
        "Built resume: %s | %d skills, %d education, %d experience, %d projects, %d certs",
        contact.get("name") or "(unnamed)",
        len(skills), len(education), len(experience), len(projects), len(certifications),
    )

    return resume.model_dump()
