
from urllib.parse import urljoin

from modulos.scraping.browser import browser_session


BASE_URL = "https://pe.computrabajo.com"


def get_text(element, selector):
    """
    Obtiene el texto de un elemento hijo.
    Devuelve None si no existe.
    """
    locator = element.locator(selector).first

    if locator.count() == 0:
        return None

    text = locator.inner_text().strip()

    return text if text else None


def scrape_it_offers():

    url = f"{BASE_URL}/trabajo-de-it"

    extracted_offers = []

    with browser_session(headless=False) as page:

        print("Accediendo a Computrabajo...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        cards = page.locator("article.box_offer")

        cards.first.wait_for(timeout=30000)

        total = cards.count()

        print(f"\nTarjetas encontradas: {total}")

        for index in range(total):

            card = cards.nth(index)

            # Título
            title = get_text(card, "a.js-o-link")

            # URL
            link = card.locator("a.js-o-link").first
            relative_url = link.get_attribute("href")

            full_url = (
                urljoin(BASE_URL, relative_url)
                if relative_url
                else None
            )

            # Empresa
            company = get_text(
                card,
                "a.fc_base.t_ellipsis"
            )

            # Ubicación
            location = get_text(
                card,
                "p.fs16.fc_base.mt5:not(.dFlex)"
            )

            # Salario
            salary = get_text(
                card,
                "div.fs13.mt15"
            )

            # Fecha de publicación
            publication_date = get_text(
                card,
                "p.fs13.fc_aux.mt15"
            )

            # Calificación de la empresa
            rating = get_text(
                card,
                "p.dFlex span.fwB"
            )

            # Oferta destacada
            is_featured = (
                card.locator("div.list_dot").count() > 0
            )

            offer = {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "publication_date": publication_date,
                "rating": rating,
                "is_featured": is_featured,
                "url": full_url,
                "source": "Computrabajo"
            }

            extracted_offers.append(offer)

    return extracted_offers


if __name__ == "__main__":

    offers = scrape_it_offers()

    print("\nRESULTADOS DE EXTRACCIÓN")
    print("=" * 60)

    for index, offer in enumerate(offers, start=1):

        print(f"\nOFERTA {index}")
        print("-" * 60)

        for key, value in offer.items():
            print(f"{key}: {value}")

    print("\nTotal extraído:", len(offers))
