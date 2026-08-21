"""ATS scoring engine.

Combines a parsed resume and parsed job description into the analysis
payload the frontend dashboard renders: an overall ATS score, per-section
scores, matched/missing skills, strengths, weaknesses and suggestions.

Every score is deterministic and rule-driven so a user can always trace
why they got the number they got.
"""

import re

from models.job_requirements import JobRequirements
from nlp.tfidf import cosine_similarity
from utils.logger import logger
from utils.patterns import SKILLS_DB

# Weights used to blend section scores into the headline ATS score.
SECTION_WEIGHTS = {
    "skillMatch": 0.35,
    "keywordMatch": 0.25,
    "experience": 0.15,
    "education": 0.10,
    "formatting": 0.15,
}

# Action keywords a healthy resume tends to contain even when there is no
# JD to compare against — used as the fallback keyword benchmark.
_GENERIC_KEYWORDS = [
    "developed", "designed", "implemented", "built", "led", "managed",
    "improved", "optimized", "reduced", "increased", "automated",
    "delivered", "collaborated", "architected", "launched", "migrated",
    "tested", "deployed",
]

_CURRENT_YEAR = 2026

_YEAR_RANGE = re.compile(
    r"(\d{4})\s*(?:-|–|—|to)\s*(present|current|now|\d{4})", re.IGNORECASE
)
_YEARS_MENTION = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*years?", re.IGNORECASE)
_REQUIRED_YEARS = re.compile(r"(\d+)(?:\s*-\s*\d+)?")

_QUANTIFIED = re.compile(r"\d+\s?%|\b\d[\d,\.]{2,}\b|\b\d+\s?\+\b")
_BULLET = re.compile(r"(^|\n)\s*(•|·|▪|- |\* )")
_HEADINGS = ("skill", "experience", "education", "project")


def _norm(term: str) -> str:
    """Normalize a skill name so 'React.js' and 'reactjs' compare equal."""
    return re.sub(r"[^a-z0-9+#]+", "", term.lower())


def _contains_term(text_lower: str, term_lower: str) -> bool:
    """Word-boundary search that tolerates ., + and # inside skill names."""
    pattern = rf"(?<![a-z0-9]){re.escape(term_lower)}(?![a-z0-9])"
    return re.search(pattern, text_lower) is not None


def _match_skills_against_resume(
    required_skills: list[str], resume_skills: list[str], resume_text_lower: str
) -> tuple[list[str], list[str]]:
    resume_norms = {_norm(skill) for skill in resume_skills}
    matched: list[str] = []
    missing: list[str] = []

    for skill in required_skills:
        if _norm(skill) in resume_norms or _contains_term(resume_text_lower, skill.lower()):
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing[:12]


def _estimate_years(experiences: list[dict]) -> float:
    """Total years of experience from merged date ranges + explicit mentions."""
    spans: list[tuple[float, float]] = []
    for exp in experiences:
        duration = exp.get("duration", "")
        m = _YEAR_RANGE.search(duration)
        if not m:
            continue
        start = float(m.group(1))
        end_raw = m.group(2).lower()
        end = (
            float(_CURRENT_YEAR)
            if re.search(r"present|current|now", end_raw)
            else float(end_raw)
        )
        if end >= start:
            spans.append((start, end))

    spans.sort()
    merged: list[list[float]] = []
    for start, end in spans:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    span_years = sum(end - start for start, end in merged)

    mention_years = 0.0
    for exp in experiences:
        m = _YEARS_MENTION.search(exp.get("description", ""))
        if m:
            mention_years = max(mention_years, float(m.group(1)))

    return round(max(span_years, mention_years), 1)


def _parse_required_years(experience_str: str) -> int | None:
    if not experience_str:
        return None
    m = _REQUIRED_YEARS.search(experience_str)
    return int(m.group(1)) if m else None


_EDUCATION_RANKS = [
    (r"ph\.?d|doctorate", 4),
    (r"master|m\.tech|m\.sc|mba|m\.e\b", 3),
    (r"bachelor|b\.tech|btech|b\.sc|b\.e\b|undergraduate", 2),
    (r"diploma|associate", 1),
]


def _degree_level(text: str) -> int:
    lowered = text.lower()
    for pattern, rank in _EDUCATION_RANKS:
        if re.search(pattern, lowered):
            return rank
    return 0


def _score_skill_match(
    jd_req: dict, resume_skills: list[str], resume_text_lower: str
) -> tuple[int, list[str], list[str]]:
    """How well resume skills cover the JD's required skills.

    Without a JD this falls back to measuring breadth — how many distinct
    skills the resume declares on its own.
    """
    required = jd_req.get("skills") or []
    if required:
        matched, missing = _match_skills_against_resume(
            required, resume_skills, resume_text_lower
        )
        score = round(len(matched) / len(required) * 100) if required else 0
        return min(score, 100), matched, missing

    breadth = len({_norm(skill) for skill in resume_skills})
    return min(breadth * 8, 100), [], []


def _score_keyword_match(
    jd_req: dict, resume_text: str, resume_text_lower: str, jd_text: str
) -> int:
    """Coverage of JD keywords blended with TF-IDF cosine similarity."""
    terms: list[str] = []
    for term in list(jd_req.get("keywords") or []) + list(
        jd_req.get("discovered_keywords") or []
    ):
        lowered = term.lower().strip()
        if lowered and lowered not in terms:
            terms.append(lowered)

    if not terms:
        terms = _GENERIC_KEYWORDS
        coverage_weight = 1.0
        semantic = 0.0
    elif jd_text.strip():
        coverage_weight = 0.7
        semantic = cosine_similarity(resume_text, jd_text)
    else:
        coverage_weight = 1.0
        semantic = 0.0

    hits = sum(1 for term in terms if _contains_term(resume_text_lower, term))
    coverage = hits / len(terms) if terms else 0.0
    return min(round(100 * (coverage_weight * coverage + (1 - coverage_weight) * semantic)), 100)


def _score_experience(jd_req: dict, parsed_data: dict) -> int:
    experiences = parsed_data.get("experience") or []
    years = _estimate_years(experiences)
    required_years = _parse_required_years(jd_req.get("experience_years", ""))

    score = 30 if experiences else 0

    target = required_years or 3
    score += round(min(years / target, 1.0) * 45)

    descriptions = [exp.get("description", "") for exp in experiences]
    avg_length = (
        sum(len(desc) for desc in descriptions) / len(descriptions) if descriptions else 0
    )
    if avg_length >= 100:
        score += 25
    elif avg_length >= 40:
        score += 15

    return min(score, 100)


def _score_education(jd_req: dict, parsed_data: dict) -> int:
    education = parsed_data.get("education") or []
    if not education:
        return 0

    score = 55

    jd_level = 0
    for line in jd_req.get("education") or []:
        jd_level = max(jd_level, _degree_level(line))

    resume_level = max(_degree_level(f"{edu.get('degree', '')}") for edu in education)

    if jd_level:
        if resume_level >= jd_level:
            score += 25
    else:
        score += 20

    if any(edu.get("cgpa") for edu in education):
        score += 20

    return min(score, 100)


def _score_formatting(parsed_data: dict, resume_text: str) -> int:
    score = 0

    if parsed_data.get("email"):
        score += 15
    if parsed_data.get("phone"):
        score += 10
    if parsed_data.get("linkedin"):
        score += 10
    if parsed_data.get("github") or parsed_data.get("portfolio"):
        score += 10

    headings_found = sum(
        1 for heading in _HEADINGS if heading in resume_text.lower()
    )
    if headings_found >= 3:
        score += 15
    elif headings_found == 2:
        score += 10

    if _BULLET.search(resume_text):
        score += 10

    words = len(resume_text.split())
    if 250 <= words <= 1200:
        score += 15
    elif words > 1200:
        score += 5

    body_text = " ".join(
        exp.get("description", "") for exp in parsed_data.get("experience") or []
    ) + " ".join(
        project.get("description", "") for project in parsed_data.get("projects") or []
    )
    if _QUANTIFIED.search(body_text):
        score += 15

    return min(score, 100)


def _build_strengths_weaknesses(
    section_scores: dict,
    matched: list[str],
    missing: list[str],
    jd_present: bool,
    years: float,
    required_years: int | None,
    quantified: bool,
    contact_complete: bool,
) -> tuple[list[str], list[str], list[str]]:
    strengths: list[str] = []
    weaknesses: list[str] = []
    suggestions: list[str] = []

    # --- skills -----------------------------------------------------------
    if jd_present and matched:
        strengths.append(
            f"{len(matched)} of the job's required skills ({', '.join(matched[:4])})"
            f"{' and more' if len(matched) > 4 else ''} are present on your resume"
        )
    if missing:
        weaknesses.append(
            f"Key skills mentioned in the job description are missing from your resume"
            f" ({', '.join(missing[:4])})"
        )
        suggestions.append(
            f"Weave these missing skills into your resume where you genuinely used them:"
            f" {', '.join(missing[:5])}"
        )

    # --- keywords ---------------------------------------------------------
    keyword_score = section_scores["keywordMatch"]
    if keyword_score >= 70:
        strengths.append(
            "Strong keyword alignment with the target role — ATS parsers will pick up most relevant terms"
        )
    elif keyword_score < 45:
        weaknesses.append(
            "Low keyword coverage: many terms from the job description never appear in your resume"
        )
        suggestions.append(
            "Mirror the exact terminology used in the job description instead of synonyms"
            " (e.g. write 'CI/CD' if the JD says 'CI/CD')"
        )

    # --- experience -------------------------------------------------------
    experience_score = section_scores["experience"]
    if required_years and years >= required_years:
        strengths.append(
            f"Your ~{years:g} years of experience meets the {required_years}+ year requirement"
        )
    elif required_years and years < required_years:
        weaknesses.append(
            f"The role asks for {required_years}+ years but your resume only shows about {years:g}"
        )
    if experience_score >= 70:
        strengths.append(
            "Work experience entries are detailed with clear roles, companies and dates"
        )
    elif experience_score < 50:
        weaknesses.append(
            "Experience section is thin — short or missing role descriptions hurt both ATS and human readers"
        )
        suggestions.append(
            "Expand each role with 2–3 bullet points covering what you built, how, and its impact"
        )

    # --- achievements -----------------------------------------------------
    if quantified:
        strengths.append(
            "Experience includes quantified results (numbers, percentages, scale), which recruiters weight heavily"
        )
    else:
        weaknesses.append(
            "No quantifiable achievements detected — accomplishments are described without metrics"
        )
        suggestions.append(
            'Add measurable outcomes to your bullets (e.g. "cut load time by 40%", "served 1M+ requests/day")'
        )

    # --- education --------------------------------------------------------
    if section_scores["education"] >= 70:
        strengths.append("Education section is complete with degree details")
    elif section_scores["education"] < 40:
        weaknesses.append("Education details are incomplete or hard to parse")
        suggestions.append(
            "List your degree, institution and graduation year in a dedicated Education section"
        )

    # --- formatting -------------------------------------------------------
    formatting_score = section_scores["formatting"]
    if formatting_score >= 80:
        strengths.append(
            "Clean, ATS-friendly layout with standard sections and complete contact information"
        )
    elif formatting_score < 50:
        weaknesses.append(
            "Formatting issues detected: missing standard section headers or contact details"
        )
        suggestions.append(
            "Use standard one-column layout with clear headers (Summary, Skills, Experience, Education)"
            " and include email, phone and LinkedIn"
        )

    if not contact_complete:
        suggestions.append(
            "Add all contact channels — email, phone, LinkedIn and GitHub/portfolio links"
        )

    suggestions.append(
        "Keep the resume to one page per ~5 years of experience and export as PDF before submitting"
    )

    return strengths[:5], weaknesses[:5], suggestions[:6]


def _build_summary(
    ats_score: int, jd_req: dict, matched_count: int, total_required: int
) -> str:
    title = jd_req.get("title") or "the target role"

    if ats_score >= 80:
        verdict = "an excellent fit for"
    elif ats_score >= 65:
        verdict = "a good match for"
    elif ats_score >= 50:
        verdict = "a fair but improvable match for"
    else:
        verdict = "currently a weak match for"

    skill_line = (
        f" It covers {matched_count} of {total_required} skills listed in the job description."
        if total_required
        else ""
    )

    return f"This resume scores {ats_score}/100 and is {verdict} {title}.{skill_line}"


def analyze_resume(
    parsed_data: dict,
    jd_requirements: dict | None,
    resume_text: str,
    jd_text: str = "",
) -> dict:
    """Score a resume against (optionally) a job description.

    Returns the camelCase analysis payload consumed by the frontend
    ResultsDashboard.
    """
    jd_req = JobRequirements(**(jd_requirements or {})).model_dump()
    jd_present = bool(jd_text.strip())

    resume_text_lower = resume_text.lower()
    resume_skills = parsed_data.get("skills") or []

    skill_score, matched, missing = _score_skill_match(
        jd_req, resume_skills, resume_text_lower
    )
    keyword_score = _score_keyword_match(
        jd_req, resume_text, resume_text_lower, jd_text
    )
    experience_score = _score_experience(jd_req, parsed_data)
    education_score = _score_education(jd_req, parsed_data)
    formatting_score = _score_formatting(parsed_data, resume_text)

    section_scores = {
        "keywordMatch": keyword_score,
        "skillMatch": skill_score,
        "experience": experience_score,
        "education": education_score,
        "formatting": formatting_score,
    }

    ats_score = min(
        100,
        max(
            0,
            round(sum(section_scores[k] * w for k, w in SECTION_WEIGHTS.items())),
        ),
    )

    years = _estimate_years(parsed_data.get("experience") or [])
    required_years = _parse_required_years(jd_req.get("experience_years", ""))

    body_text = " ".join(
        exp.get("description", "") for exp in parsed_data.get("experience") or []
    )
    quantified = bool(_QUANTIFIED.search(body_text))
    contact_complete = all(
        parsed_data.get(field) for field in ("email", "phone", "linkedin")
    )

    strengths, weaknesses, suggestions = _build_strengths_weaknesses(
        section_scores=section_scores,
        matched=matched,
        missing=missing,
        jd_present=jd_present,
        years=years,
        required_years=required_years,
        quantified=quantified,
        contact_complete=contact_complete,
    )

    summary = _build_summary(ats_score, jd_req, len(matched), len(matched) + len(missing))

    analysis = {
        "atsScore": ats_score,
        "sectionScores": section_scores,
        "matchedSkills": matched[:10],
        "missingSkills": missing[:10],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "summary": summary,
    }

    logger.info(
        "ATS analysis complete — score=%d (skill=%d keyword=%d exp=%d edu=%d fmt=%d)",
        ats_score,
        skill_score,
        keyword_score,
        experience_score,
        education_score,
        formatting_score,
    )

    return analysis
