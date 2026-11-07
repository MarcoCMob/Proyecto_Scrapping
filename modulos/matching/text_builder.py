
from schemas.cv_schema import CVProfile
from schemas.job_schema import JobOffer


def build_cv_text(profile: CVProfile) -> str:
    """
    Convierte el perfil del candidato en un texto
    que represente sus conocimientos y experiencia.
    """

    sections = []

    if profile.profession:
        sections.append(
            f"Profesión: {profile.profession}"
        )

    if profile.skills:
        sections.append(
            "Habilidades: " + ", ".join(profile.skills)
        )

    if profile.target_positions:
        sections.append(
            "Puestos buscados: "
            + ", ".join(profile.target_positions)
        )

    for experience in profile.experience:
        experience_text = (
            f"Experiencia laboral: {experience.position}. "
            f"{experience.description}"
        )

        if experience.company:
            experience_text += (
                f" Empresa: {experience.company}."
            )

        sections.append(experience_text)

    for education in profile.education:
        sections.append(
            f"Formación académica: {education.degree}. "
            f"Institución: {education.institution}."
        )

    return "\n".join(sections)


def build_offer_text(offer: JobOffer) -> str:
    """
    Convierte una oferta laboral en un texto
    que represente sus requisitos y características.
    """

    sections = [
        f"Puesto laboral: {offer.title}"
    ]

    if offer.subtitle:
        sections.append(
            f"Especialidad: {offer.subtitle}"
        )

    if offer.company:
        sections.append(
            f"Empresa: {offer.company}"
        )

    if offer.location:
        sections.append(
            f"Ubicación: {offer.location}"
        )

    if offer.summary:
        sections.append(
            "Resumen: " + ", ".join(offer.summary)
        )

    if offer.description:
        sections.append(
            f"Descripción y requisitos: {offer.description}"
        )

    return "\n".join(sections)
