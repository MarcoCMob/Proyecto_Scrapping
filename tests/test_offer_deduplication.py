
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
