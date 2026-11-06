
from modulos.scraping.browser import browser_session
from modulos.scraping.offer_details import extract_offer_details


def main():

    url = "https://pe.computrabajo.com/trabajo-de-it"

    with browser_session(headless=False) as page:

        print("Accediendo a Computrabajo...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        cards = page.locator("article.box_offer")
        cards.first.wait_for(timeout=30000)

        print("\nSeleccionando primera oferta...")

        details = extract_offer_details(
            page,
            cards.first
        )

        print("\nDETALLES EXTRAÍDOS")
        print("=" * 60)

        for key, value in details.items():

            print(f"\n{key.upper()}:")

            if isinstance(value, list):
                for item in value:
                    print("-", item)
            else:
                print(value)

        input("\nPresiona ENTER para cerrar...")


if __name__ == "__main__":
    main()
