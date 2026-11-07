
from schemas.cv_schema import (
    CVProfile,
    Experience,
    Education
)

from schemas.job_schema import JobOffer

from modulos.matching.text_builder import (
    build_cv_text,
    build_offer_text
)


def test_build_cv_text():

    profile = CVProfile(
        profession="Ingeniería de Software",
        skills=["Java", "Python", "SQL"],
        target_positions=["Desarrollador Backend Junior"],
        experience=[
            Experience(
                position="Practicante de desarrollo",
                company="Empresa de prueba",
                description="Desarrollo de aplicaciones con Java."
            )
        ],
        education=[
            Education(
                degree="Ingeniería de Software",
                institution="Universidad de prueba"
            )
        ]
    )

    result = build_cv_text(profile)

    assert "Ingeniería de Software" in result
    assert "Java" in result
    assert "Python" in result
    assert "SQL" in result
    assert "Desarrollador Backend Junior" in result
    assert "Empresa de prueba" in result


def test_build_offer_text():

    offer = JobOffer(
        title="Desarrollador Backend Junior",
        subtitle="Java y Spring Boot",
        company="Empresa de prueba",
        location="Lima",
        summary=[
            "Tiempo completo",
            "Contrato a plazo indeterminado"
        ],
        description=(
            "Se requiere conocimiento de Java, "
            "Spring Boot y PostgreSQL."
        ),
        source="Computrabajo"
    )

    result = build_offer_text(offer)

    assert "Desarrollador Backend Junior" in result
    assert "Java y Spring Boot" in result
    assert "Lima" in result
    assert "PostgreSQL" in result
    assert "Computrabajo" not in result
