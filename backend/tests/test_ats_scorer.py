"""Unit tests for the ATS scoring engine."""

import pytest

from scoring.ats_scorer import (
    SECTION_WEIGHTS,
    _estimate_years,
    _parse_required_years,
    analyze_resume,
)

STRONG_RESUME = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1 555 0100",
    "linkedin": "linkedin.com/in/janedoe",
    "github": "github.com/janedoe",
    "portfolio": "",
    "skills": ["Python", "React", "PostgreSQL", "Docker", "AWS", "Git"],
    "projects": [],
    "education": [
        {
            "college": "MIT",
            "degree": "B.Tech Computer Science",
            "branch": "CSE",
            "cgpa": "8.9",
            "graduation_year": "2022",
        }
    ],
    "experience": [
        {
            "company": "Acme",
            "role": "Backend Engineer",
            "duration": "2022 - Present",
            "description": (
                "Built REST APIs with Python serving 500k requests per day, "
                "deployed on AWS with Docker and reduced latency by 35%."
            ),
        }
    ],
    "certifications": [],
}

STRONG_RESUME_TEXT = """Jane Doe
jane@example.com | +1 555 0100 | linkedin.com/in/janedoe | github.com/janedoe

Skills
Python React PostgreSQL Docker AWS Git

Experience
Backend Engineer — Acme (2022 - Present)
Built REST APIs with Python serving 500k requests per day, deployed on AWS
with Docker and reduced latency by 35%.

• Optimized database queries in PostgreSQL cutting report time by 60%

Education
B.Tech Computer Science, MIT, 2022, CGPA 8.9"""

JD_REQUIREMENTS = {
    "title": "Full Stack Developer",
    "skills": ["Python", "React", "Docker", "Kubernetes"],
    "preferred_skills": ["AWS"],
    "keywords": ["python", "react", "api"],
    "discovered_keywords": ["microservices"],
    "experience_years": "1-3 Years",
    "education": ["Bachelor degree in Computer Science"],
    "responsibilities": [],
}

JD_TEXT = """Full Stack Developer

Required Skills:
- Python
- React
- Docker
- Kubernetes

We are building microservices and rest api backends."""


def test_strong_resume_scores_well():
    result = analyze_resume(STRONG_RESUME, JD_REQUIREMENTS, STRONG_RESUME_TEXT, JD_TEXT)

    assert result["atsScore"] >= 65
    assert set(SECTION_WEIGHTS) == set(result["sectionScores"])

    assert "Kubernetes" in result["missingSkills"]
    assert {"Python", "React", "Docker"} <= set(result["matchedSkills"])
    assert result["strengths"] and result["suggestions"]
    assert str(result["atsScore"]) in result["summary"]


def test_empty_resume_against_jd_scores_low():
    result = analyze_resume({}, JD_REQUIREMENTS, "", JD_TEXT)

    assert result["atsScore"] <= 40
    assert result["missingSkills"] == [] or len(result["missingSkills"]) <= 12
    assert result["weaknesses"]


def test_works_without_job_description():
    result = analyze_resume(STRONG_RESUME, None, STRONG_RESUME_TEXT, "")

    for key in ("atsScore", "sectionScores", "matchedSkills", "missingSkills",
                "strengths", "weaknesses", "suggestions", "summary"):
        assert key in result

    assert 0 <= result["atsScore"] <= 100


def test_section_scores_are_bounded_ints():
    result = analyze_resume(STRONG_RESUME, JD_REQUIREMENTS, STRONG_RESUME_TEXT, JD_TEXT)

    for value in result["sectionScores"].values():
        assert isinstance(value, int)
        assert 0 <= value <= 100

    assert 0 <= result["atsScore"] <= 100


def test_estimate_years_merges_overlapping_ranges():
    experiences = [
        {"duration": "2019 - 2021", "description": ""},
        {"duration": "2020 - Present", "description": ""},
    ]
    # merged span 2019 -> current year
    years = _estimate_years(experiences)

    assert years >= 7.0
    assert _parse_required_years("3-5 Years") == 3
    assert _parse_required_years("5+ Years") == 5
    assert _parse_required_years("") is None


@pytest.mark.parametrize("resume,jd,text", [
    ({}, None, ""),
    ({}, {}, "some plain text"),
])
def test_never_crashes_on_degenerate_input(resume, jd, text):
    result = analyze_resume(resume, jd, text, "")

    assert isinstance(result["atsScore"], int)
