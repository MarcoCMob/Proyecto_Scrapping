
from types import SimpleNamespace

from services.offer_deduplication_service import (
    normalize_text,
    calculate_description_similarity,
    compare_offers
)


def test_normalize_text():
    result = normalize_text("  Atención al CLIENTE  ")

    assert result == "atencion al cliente"


def test_description_similarity():
    description_a = (
        "Empresa solicita asesor de atención al cliente. "
        "Sueldo fijo y bono de desempeño de S/ 400."
    )

    description_b = (
        "Empresa solicita asesor de atención al cliente. "
        "Sueldo fijo y bono de desempeño de S/ 500."
    )

    similarity = calculate_description_similarity(
        description_a,
        description_b
    )

    print(f"\nSimilitud: {similarity:.4f}")

    assert similarity > 0.95


def test_compare_offers():
    offer_a = SimpleNamespace(
        title="Atención al cliente",
        company="Fractalia Perú",
        location="Lima, Lima",
        description="Oferta de atención al cliente con sueldo fijo."
    )

    offer_b = SimpleNamespace(
        title="Atención al cliente",
        company="Fractalia Perú",
        location="Lima, Lima",
        description="Oferta de atención al cliente con sueldo fijo."
    )

    result = compare_offers(offer_a, offer_b)

    assert result is True


def test_different_companies_are_not_duplicates():
    offer_a = SimpleNamespace(
        title="Atención al cliente",
        company="Empresa A",
        location="Lima",
        description="Oferta de atención al cliente."
    )

    offer_b = SimpleNamespace(
        title="Atención al cliente",
        company="Empresa B",
        location="Lima",
        description="Oferta de atención al cliente."
    )

    result = compare_offers(offer_a, offer_b)

    assert result is False

def test_same_offer_from_different_sources_are_not_duplicates():
    offer_computrabajo = SimpleNamespace(
        title="Desarrollador Backend Junior",
        company="Empresa ABC",
        location="Lima",
        description="Se requiere Java, Spring Boot y PostgreSQL.",
        url="https://computrabajo.com/oferta/123",
        source="Computrabajo"
    )

    offer_laborum = SimpleNamespace(
        title="Desarrollador Backend Junior",
        company="Empresa ABC",
        location="Lima",
        description="Se requiere Java, Spring Boot y PostgreSQL.",
        url="https://laborum.pe/job/oferta/123",
        source="Laborum"
    )

    result = compare_offers(
        offer_computrabajo,
        offer_laborum
    )

    assert result is False


def test_same_offer_from_same_source_are_duplicates():
    offer_a = SimpleNamespace(
        title="Desarrollador Backend Junior",
        company="Empresa ABC",
        location="Lima",
        description="Se requiere Java, Spring Boot y PostgreSQL.",
        url="https://computrabajo.com/oferta/123",
        source="Computrabajo"
    )

    offer_b = SimpleNamespace(
        title="Desarrollador Backend Junior",
        company="Empresa ABC",
        location="Lima",
        description="Se requiere Java, Spring Boot y PostgreSQL.",
        url="https://computrabajo.com/oferta/456",
        source="Computrabajo"
    )

    result = compare_offers(offer_a, offer_b)

    assert result is True
