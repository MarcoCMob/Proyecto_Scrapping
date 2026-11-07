
from database.connection import SessionLocal
from repositories.job_offer_repository import JobOfferRepository
from schemas.job_schema import JobOffer


def test_save_and_retrieve_offer():

    test_offer = JobOffer(
        title="Desarrollador Backend Junior",
        subtitle="Java y Spring Boot",
        company="Empresa de prueba",
        location="Lima, Perú",
        summary=[
            "Tiempo completo",
            "Modalidad híbrida"
        ],
        description="Oferta laboral utilizada para probar PostgreSQL.",
        url="https://example.com/test-offer",
        source="Test"
    )

    with SessionLocal() as session:
        repository = JobOfferRepository(session)

        # Guardar oferta
        saved_offer = repository.save(test_offer)

        assert saved_offer.id is not None
        assert saved_offer.title == test_offer.title

        print("\nOferta guardada correctamente.")
        print(f"ID: {saved_offer.id}")
        print(f"Título: {saved_offer.title}")

        # Recuperar oferta
        retrieved_offer = repository.get_by_id(saved_offer.id)

        assert retrieved_offer is not None
        assert retrieved_offer.company == "Empresa de prueba"

        print("Oferta recuperada correctamente.")

        # Eliminar registro de prueba
        deleted = repository.delete_by_id(saved_offer.id)

        assert deleted is True

        print("Registro de prueba eliminado.")

def test_save_many_avoids_duplicates():
    description_a = (
        "Empresa solicita desarrollador backend junior. "
        "Requisitos: Java, Spring Boot, SQL y conocimientos de REST API. "
        "Se ofrece sueldo de S/ 4000 y modalidad híbrida."
    )

    description_b = description_a.replace(
        "S/ 4000", "S/ 4100"
    )

    offer_a = JobOffer(
        title="Prueba deduplicacion repositorio",
        company="Empresa de prueba deduplicacion",
        location="Lima, Perú",
        summary=["Tiempo completo"],
        description=description_a,
        url="https://example.com/offer-duplicate-a",
        source="Test"
    )

    offer_b = JobOffer(
        title="Prueba deduplicacion repositorio",
        company="Empresa de prueba deduplicacion",
        location="Lima, Perú",
        summary=["Tiempo completo"],
        description=description_b,
        url="https://example.com/offer-duplicate-b",
        source="Test"
    )

    with SessionLocal() as session:
        repository = JobOfferRepository(session)

        saved_offers = repository.save_many([offer_a, offer_b])

        try:
            print("\nPRUEBA DE DEDUPLICACIÓN")
            print(f"Ofertas recibidas: 2")
            print(f"Ofertas guardadas: {len(saved_offers)}")

            assert len(saved_offers) == 1

            print("Duplicado descartado correctamente.")

        finally:
            for offer in saved_offers:
                repository.delete_by_id(offer.id)

def test_save_many_avoids_duplicates_without_company():

    offer_a = JobOffer(
        title="Coordinador de recursos humanos",
        company=None,
        location="Santiago De Surco, Lima",
        summary=["Tiempo completo"],
        description="Oferta de prueba sin empresa identificada.",
        url="https://example.com/oferta/recursos-humanos#publicacion-1",
        source="Test"
    )

    offer_b = JobOffer(
        title="Coordinador de recursos humanos",
        company=None,
        location="Santiago De Surco, Lima",
        summary=["Tiempo completo"],
        description="Oferta de prueba sin empresa identificada.",
        url="https://example.com/oferta/recursos-humanos#publicacion-2",
        source="Test"
    )

    with SessionLocal() as session:
        repository = JobOfferRepository(session)

        saved_offers = repository.save_many([offer_a, offer_b])

        try:
            print("\nPRUEBA DE DEDUPLICACIÓN SIN EMPRESA")
            print(f"Ofertas recibidas: 2")
            print(f"Ofertas guardadas: {len(saved_offers)}")

            assert len(saved_offers) == 1

            print("Duplicado descartado correctamente.")

        finally:
            for offer in saved_offers:
                repository.delete_by_id(offer.id)