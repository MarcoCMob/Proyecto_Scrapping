
from modulos.scraping.scraper_service import scrape_detailed_offers
from database.connection import SessionLocal
from repositories.job_offer_repository import JobOfferRepository


def collect_and_save_offers(headless=False):
    # 1. Extraer ofertas desde Computrabajo.
    offers, errors = scrape_detailed_offers(headless=headless)

    extracted_count = len(offers)

    print("\nRESULTADO DEL SCRAPING")
    print(f"Ofertas extraídas correctamente: {extracted_count}")
    print(f"Errores de extracción: {len(errors)}")

    if not offers:
        return {
            "extracted": 0,
            "saved": 0,
            "duplicates": 0,
            "errors": errors
        }

    # 2. Guardar las ofertas evitando duplicados.
    session = SessionLocal()

    try:
        repository = JobOfferRepository(session)

        saved_offers = repository.save_many(offers)

        saved_count = len(saved_offers)
        duplicate_count = extracted_count - saved_count

        print("\nRESULTADO DE PERSISTENCIA")
        print(f"Ofertas nuevas guardadas: {saved_count}")
        print(f"Ofertas descartadas por duplicidad: {duplicate_count}")

        return {
            "extracted": extracted_count,
            "saved": saved_count,
            "duplicates": duplicate_count,
            "errors": errors
        }

    except Exception as error:
        print(f"\nError al guardar las ofertas: {error}")
        raise

    finally:
        session.close()
