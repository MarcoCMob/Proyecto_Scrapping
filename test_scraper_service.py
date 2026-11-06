
from modulos.scraping.scraper_service import scrape_detailed_offers


def main():

    offers, errors = scrape_detailed_offers(headless=False)

    print("\n\nRESUMEN DE EXTRACCIÓN")
    print("=" * 60)

    print(f"Ofertas extraídas correctamente: {len(offers)}")
    print(f"Ofertas con errores: {len(errors)}")

    for offer in offers:

        print("\n" + "-" * 60)
        print("Título:", offer["title"])
        print("Empresa:", offer["company"])
        print("Ubicación:", offer["location"])
        print("URL:", offer["url"])
        print("Longitud de descripción:", len(offer["description"]))

    if errors:

        print("\nERRORES")
        print("=" * 60)

        for error in errors:
            print(error)


if __name__ == "__main__":
    main()
