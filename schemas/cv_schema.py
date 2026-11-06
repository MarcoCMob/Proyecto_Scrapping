from pydantic import BaseModel
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

    skills: list[str] = []

    experience: list[Experience] = []

    education: list[Education] = []

    target_positions: list[str] = []
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
