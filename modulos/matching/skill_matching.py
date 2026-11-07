import re

from services.offer_deduplication_service import normalize_text

# Skills que no deben contar como señal técnica.
NON_TECHNICAL_SKILLS = {
    normalize_text(skill) for skill in [
        "Español",
        "Inglés",
        "Inglés Avanzado C1",
        "Atención al cliente",
        "Análisis de ventas",
        "Excel Intermedio"
    ]
}


def technical_skills(skills: list[str]) -> list[str]:
    normalized = (normalize_text(skill) for skill in skills)
    return [
        skill for skill in normalized
        if skill and skill not in NON_TECHNICAL_SKILLS
    ]


def find_skill_matches(skills: list[str], offer_text: str) -> list[str]:
    """
    Devuelve las skills técnicas del candidato que aparecen
    como palabra completa en el texto de la oferta.
    ("java" no coincide con "javascript").
    """
    text = normalize_text(offer_text)

    return [
        skill for skill in technical_skills(skills)
        if re.search(rf"(?<!\w){re.escape(skill)}(?!\w)", text)
    ]