from pydantic import BaseModel, Field


class JobRequirements(BaseModel):
    title: str = ""
    skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    discovered_keywords: list[str] = Field(default_factory=list)
    experience_years: str = ""
    education: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
