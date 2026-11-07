
from database.connection import SessionLocal
from repositories.job_offer_repository import JobOfferRepository


def test_filter_job_offers():

    with SessionLocal() as session:

        repository = JobOfferRepository(session)

        # Recuperar todas las ofertas
        all_offers = repository.get_all(limit=100)

        print("\nTOTAL DE OFERTAS:", len(all_offers))

        # Buscar ofertas relacionadas con IT
        it_offers = repository.get_all(
            title="IT",
            limit=100
        )

        print("OFERTAS CON IT EN EL TÍTULO:", len(it_offers))

        # Buscar ofertas de Computrabajo
        computrabajo_offers = repository.get_all(
            source="Computrabajo",
            limit=100
        )

        print(
            "OFERTAS DE COMPUTRABAJO:",
            len(computrabajo_offers)
        )

        # Verificar que los filtros se apliquen
        assert all(
            "it" in offer.title.lower()
            for offer in it_offers
        )

        assert all(
            offer.source.lower() == "computrabajo"
            for offer in computrabajo_offers
        )
