
from urllib.parse import quote_plus, urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeout

from schemas.job_schema import JobOffer
from modulos.scraping.browser import browser_session


BASE_URL = "https://www.laborum.pe"
SEARCH_URL = f"{BASE_URL}/search-jobs"


def build_search_url(query: str) -> str:
    """Construye la URL de búsqueda de Laborum."""

    query = " ".join(query.split())

    if not query:
        raise ValueError("El término de búsqueda está vacío.")

    return f"{SEARCH_URL}?q={quote_plus(query)}"


def extract_card_data(link):
    """Extrae los datos disponibles en una tarjeta de resultados."""

    title_element = link.locator("h6[title]").first
    company_element = link.locator("p[title]").first

    title = (
        title_element.get_attribute("title")
        if title_element.count()
        else None
    )

    company = (
        company_element.get_attribute("title")
        if company_element.count()
        else None
    )

    relative_url = link.get_attribute("href")

    if not title or not relative_url:
        raise ValueError("La tarjeta no contiene título o URL.")

    return {
        "title": title.strip(),
        "company": company.strip() if company else None,
        "url": urljoin(BASE_URL, relative_url)
    }


def extract_offer_details(page, offer_url, expected_title):
    page.goto(
        offer_url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    # Buscar el h2 que coincida con el título de la tarjeta.
    title_element = page.locator("h2").filter(
        has_text=expected_title
    ).first

    title_element.wait_for(state="visible", timeout=30000)

    detail = title_element.locator(
        "xpath=ancestor::div[contains(@class, 'MuiPaper-root')][1]"
    )

    detail.wait_for(state="visible", timeout=15000)

    data = detail.evaluate("""
        container => {
            const titleElement = container.querySelector("h2");
            const companyElement = container.querySelector("h5");

            const locationElement = titleElement
                ?.parentElement
                ?.querySelector("span");

            return {
                title: titleElement?.innerText?.trim() || null,
                company: companyElement?.innerText?.trim() || null,
                location: locationElement?.innerText?.trim() || null,
                description: container.innerText?.trim() || ""
            };
        }
    """)

    if not data["title"]:
        raise ValueError("No se pudo extraer el título de la publicación.")

    if not data["description"]:
        raise ValueError("La publicación no contiene descripción.")

    return data


def _scrape_search_page(
    page,
    search_url,
    max_offers=None,
    seen_urls=None
):
    """Extrae las ofertas correspondientes a una búsqueda."""

    results = []
    errors = []

    seen_urls = seen_urls if seen_urls is not None else set()

    print(f"\nAccediendo a Laborum: {search_url}")

    page.goto(
        search_url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    cards = page.locator('ul#listJobs a[href*="/job/"]')

    try:
        cards.first.wait_for(timeout=20000)

    except PlaywrightTimeout:
        print("No se encontraron ofertas.")

        errors.append({
            "title": "(búsqueda)",
            "url": search_url,
            "error": "No se encontraron ofertas."
        })

        return results, errors

    total = cards.count()

    if max_offers is not None:
        total = min(total, max_offers)

    print(f"Ofertas encontradas: {total}")

    # Primero recopilamos los enlaces para evitar perder
    # las referencias al navegar hacia cada detalle.
    card_data = []

    for index in range(total):
        try:
            data = extract_card_data(cards.nth(index))

            if data["url"] in seen_urls:
                continue

            seen_urls.add(data["url"])
            card_data.append(data)

        except Exception as error:
            errors.append({
                "title": f"Tarjeta {index + 1}",
                "url": search_url,
                "error": str(error)
            })

    # Después visitamos cada publicación individualmente.
    for index, card in enumerate(card_data, start=1):

        print(f"[{index}/{len(card_data)}] {card['title']}")

        try:
            details = extract_offer_details(
                page,
                card["url"],
                card["title"]
            )

            offer = JobOffer(
                title=details["title"],
                subtitle=None,
                company=details["company"] or card["company"],
                location=details["location"],
                summary=[],
                description=details["description"],
                url=card["url"],
                source="Laborum"
            )

            results.append(offer)

        except Exception as error:
            errors.append({
                "title": card["title"],
                "url": card["url"],
                "error": str(error)
            })

            print(f"  Error: {error}")

    return results, errors


def scrape_searches(
    queries,
    headless=False,
    max_per_query=None
):
    """
    Busca ofertas en Laborum para varios términos.

    Devuelve:
        results: ofertas extraídas como JobOffer.
        errors: errores producidos durante la extracción.
    """

    results = []
    errors = []
    seen_urls = set()

    with browser_session(headless=headless) as page:

        for query in queries:

            search_url = build_search_url(query)

            offers, query_errors = _scrape_search_page(
                page,
                search_url,
                max_per_query,
                seen_urls
            )

            results.extend(offers)
            errors.extend(query_errors)

    return results, errors
