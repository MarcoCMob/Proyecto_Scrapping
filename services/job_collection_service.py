
from modulos.scraping.scraper_service import scrape_detailed_offers
from database.connection import SessionLocal
from repositories.job_offer_repository import JobOfferRepository


def collect_and_save_offers(headless=False):
    """
    Ejecuta el scraping de Computrabajo y almacena
    las ofertas extraídas en PostgreSQL.
    """

    # 1. Ejecutar el scraper
    offers, errors = scrape_detailed_offers(headless=headless)

    print("\nRESULTADO DEL SCRAPING")
    print(f"Ofertas extraídas: {len(offers)}")
    print(f"Errores de extracción: {len(errors)}")

    # 2. Si no hay ofertas, no abrir una sesión innecesariamente
    if not offers:
        return {
            "extracted": 0,
            "saved": 0,
            "errors": errors
        }

    # 3. Guardar las ofertas en PostgreSQL
    session = SessionLocal()

    try:
        repository = JobOfferRepository(session)

        saved_offers = repository.save_many(offers)

        print("\nRESULTADO DE PERSISTENCIA")
        print(f"Ofertas guardadas: {len(saved_offers)}")

        return {
            "extracted": len(offers),
            "saved": len(saved_offers),
            "errors": errors
        }

    except Exception as error:
        print(f"\nError al guardar las ofertas: {error}")
        raise

    finally:
        session.close()
