
from database.connection import SessionLocal
from services.job_offer_service import JobOfferService


def test_search_offers_with_pagination():

    with SessionLocal() as session:
        service = JobOfferService(session)

        # Primera página: todas las ofertas.
        result = service.search_offers(
            page=1,
            per_page=10
        )

        print("\nTOTAL DE OFERTAS:", result["total"])
        print("PÁGINA ACTUAL:", result["page"])
        print("OFERTAS POR PÁGINA:", result["per_page"])
        print("PÁGINAS TOTALES:", result["total_pages"])
        print("OFERTAS RECUPERADAS:", len(result["offers"]))
        print("TIENE SIGUIENTE:", result["has_next"])
        print("TIENE ANTERIOR:", result["has_previous"])

        assert result["total"] == 24
        assert result["total_pages"] == 3
        assert len(result["offers"]) == 10
        assert result["has_next"] is True
        assert result["has_previous"] is False

        # Segunda página.
        second_page = service.search_offers(
            page=2,
            per_page=10
        )

        assert len(second_page["offers"]) == 10
        assert second_page["has_next"] is True
        assert second_page["has_previous"] is True

        # Tercera página.
        third_page = service.search_offers(
            page=3,
            per_page=10
        )

        assert len(third_page["offers"]) == 4
        assert third_page["has_next"] is False
        assert third_page["has_previous"] is True


def test_search_offers_with_filters():

    with SessionLocal() as session:
        service = JobOfferService(session)

        result = service.search_offers(
            page=1,
            per_page=10,
            title="IT",
            source="Computrabajo"
        )

        print("\nOFERTAS FILTRADAS:", result["total"])
        print("PÁGINAS FILTRADAS:", result["total_pages"])

        assert result["total"] == 7
        assert len(result["offers"]) == 7

        for offer in result["offers"]:
            assert "it" in offer.title.lower()
            assert offer.source.lower() == "computrabajo"
