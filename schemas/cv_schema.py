from pydantic import BaseModel, Field
from typing import Optional


class Experience(BaseModel):
    position: str
    company: Optional[str] = None
    description: str


class Education(BaseModel):
    degree: str
    institution: str


class CVProfile(BaseModel):

    full_name: Optional[str] = None

    profession: Optional[str] = None

    skills: list[str] = Field(default_factory=list)

    experience: list[Experience] = Field(
        default_factory=list
    )

    education: list[Education] = Field(
        default_factory=list
    )

    target_positions: list[str] = Field(
        default_factory=list
    )

    search_queries: list[str] = Field(
        default_factory=list
    )

"""
EJEMPLO DE USO DE LA CLASE CVProfile
profile = CVProfile(
    full_name="Marco Castro",
    profession="Estudiante de Ingeniería de Software",
    skills=[
        "Java",
        "JavaScript",
        "SQL",
        "Python"
    ],
    target_positions=[
        "Backend Developer",
        "Software Developer"
    ]
)
"""
