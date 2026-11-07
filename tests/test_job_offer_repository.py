
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
