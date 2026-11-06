
from urllib.parse import urljoin

from modulos.scraping.browser import browser_session
from modulos.scraping.offer_details import extract_offer_details


BASE_URL = "https://pe.computrabajo.com"


def scrape_detailed_offers(headless=False):

    search_url = f"{BASE_URL}/trabajo-de-it"

    results = []
    errors = []

    with browser_session(headless=headless) as page:

        print("Accediendo a Computrabajo...")

        page.goto(
            search_url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        cards = page.locator("article.box_offer")
        cards.first.wait_for(timeout=30000)

        total = cards.count()

        print(f"\nTarjetas encontradas: {total}")
        print("\nIniciando extracción detallada...\n")

        for index in range(total):

            card = cards.nth(index)

            # Extraer datos básicos antes de seleccionar la oferta
            title_element = card.locator("a.js-o-link").first

            title = title_element.inner_text().strip()

            relative_url = title_element.get_attribute("href")

            offer_url = (
                urljoin(BASE_URL, relative_url)
                if relative_url
                else None
            )

            print(f"[{index + 1}/{total}] {title}")

            try:

                details = extract_offer_details(page, card)

                # Añadir información de origen
                details["url"] = offer_url
                details["source"] = "Computrabajo"

                results.append(details)

                print("  Extracción completada.")

            except Exception as error:

                errors.append({
                    "title": title,
                    "url": offer_url,
                    "error": str(error)
                })

                print(f"  Error: {error}")

    return results, errors
