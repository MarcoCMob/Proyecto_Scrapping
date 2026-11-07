
from database.connection import SessionLocal
from models.job_offer_model import JobOfferModel
from services.offer_deduplication_service import (
    calculate_description_similarity,
    compare_offers
)


with SessionLocal() as session:
    offer_a = session.get(JobOfferModel, 16)
    offer_b = session.get(JobOfferModel, 17)

    if offer_a is None or offer_b is None:
        print("No se encontraron ambas ofertas.")
    else:
        similarity = calculate_description_similarity(
            offer_a.description,
            offer_b.description
        )

        print("\nCOMPARACIÓN DE OFERTAS REALES")
        print("=" * 40)
        print(f"Oferta A: {offer_a.id} - {offer_a.title}")
        print(f"Oferta B: {offer_b.id} - {offer_b.title}")
        print(f"\nSimilitud: {similarity:.4f}")
        print(f"Porcentaje: {similarity * 100:.2f}%")

        is_duplicate = compare_offers(
            offer_a,
            offer_b
        )

        print(
            "¿Se consideran duplicadas?:",
            "Sí" if is_duplicate else "No"
        )
