
from modulos.scraping.laborum_scraper import scrape_searches


def main():

    queries = ["Ingeniero de Sistemas"]

    offers, errors = scrape_searches(
        queries,
        headless=False,
        max_per_query=3
    )

    print("\n" + "=" * 60)
    print("RESULTADOS DE LABORUM")
    print("=" * 60)

    for index, offer in enumerate(offers, start=1):

        print(f"\nOFERTA {index}")
        print("-" * 60)

        print("Título:", offer.title)
        print("Empresa:", offer.company)
        print("Ubicación:", offer.location)
        print("Fuente:", offer.source)
        print("URL:", offer.url)

        print("\nDescripción:")
        print(offer.description[:1500])

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)

    print("Ofertas extraídas:", len(offers))
    print("Errores:", len(errors))

    for error in errors:
        print(error)


if __name__ == "__main__":
    main()
