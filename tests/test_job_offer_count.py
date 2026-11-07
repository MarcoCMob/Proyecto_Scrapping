from database.connection import SessionLocal
from repositories.job_offer_repository import JobOfferRepository


def test_count_job_offers():
    with SessionLocal() as session:
        repository = JobOfferRepository(session)

        # Contar todas las ofertas
        total = repository.count()

        # Contar ofertas que contienen IT en el título
        it_count = repository.count(title="IT")

        # Contar ofertas de Computrabajo
        source_count = repository.count(source="Computrabajo")

        # Contar ofertas que cumplen ambos filtros
        combined_count = repository.count(
            title="IT",
            source="Computrabajo"
        )

        print("\nTOTAL DE OFERTAS:", total)
        print("OFERTAS CON IT:", it_count)
        print("OFERTAS DE COMPUTRABAJO:", source_count)
        print("OFERTAS IT DE COMPUTRABAJO:", combined_count)

        # Comprobar que count() coincide con get_all()
        assert total == len(repository.get_all(limit=1000))

        assert it_count == len(
            repository.get_all(title="IT", limit=1000)
        )

        assert source_count == len(
            repository.get_all(source="Computrabajo", limit=1000)
        )

        assert combined_count == len(
            repository.get_all(
                title="IT",
                source="Computrabajo",
                limit=1000
            )
        )