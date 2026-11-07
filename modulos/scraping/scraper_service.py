import re
import unicodedata
from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeout

from schemas.job_schema import JobOffer
from services.offer_deduplication_service import normalize_url

from modulos.scraping.browser import browser_session
from modulos.scraping.offer_details import extract_offer_details


BASE_URL = "https://pe.computrabajo.com"
DEFAULT_SEARCH_URL = f"{BASE_URL}/trabajo-de-it"


def build_search_url(query: str) -> str:
    """
    'desarrollador java junior'
    -> https://pe.computrabajo.com/trabajo-de-desarrollador-java-junior
    """
    text = unicodedata.normalize("NFD", query.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")

    if not slug:
        raise ValueError("El término de búsqueda está vacío.")

    return f"{BASE_URL}/trabajo-de-{slug}"


def _scrape_search_page(page, search_url, max_offers=None, seen_urls=None):
    results = []
    errors = []
    seen_urls = seen_urls if seen_urls is not None else set()

    print(f"\nAccediendo a {search_url}")

    page.goto(
        search_url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    cards = page.locator("article.box_offer")

    try:
        cards.first.wait_for(timeout=15000)
    except PlaywrightTimeout:
        print("  Sin resultados para esta búsqueda.")
        errors.append({
            "title": "(búsqueda)",
            "url": search_url,
            "error": "No se encontraron ofertas."
        })
        return results, errors

    total = cards.count()

    if max_offers:
        total = min(total, max_offers)

    print(f"  Tarjetas a procesar: {total}")

    for index in range(total):

        card = cards.nth(index)
        title_element = card.locator("a.js-o-link").first

        title = title_element.inner_text().strip()
        relative_url = title_element.get_attribute("href")

        offer_url = (
            urljoin(BASE_URL, relative_url) if relative_url else None
        )

        # Saltar ofertas ya extraídas en otra búsqueda.
        key = normalize_url(offer_url)

        if key and key in seen_urls:
            print(f"  [{index + 1}/{total}] (repetida) {title}")
            continue

        print(f"  [{index + 1}/{total}] {title}")

        try:
            details = extract_offer_details(page, card)
            details["url"] = offer_url
            details["source"] = "Computrabajo"

            results.append(JobOffer(**details))

            if key:
                seen_urls.add(key)

        except Exception as error:
            errors.append({
                "title": title,
                "url": offer_url,
                "error": str(error)
            })
            print(f"    Error: {error}")

    return results, errors


def scrape_searches(queries, headless=False, max_per_query=None):
    """Busca cada término en Computrabajo con un solo navegador."""
    results = []
    errors = []
    seen_urls = set()

    with browser_session(headless=headless) as page:
        for query in queries:
            search_url = build_search_url(query)

            offers, query_errors = _scrape_search_page(
                page, search_url, max_per_query, seen_urls
            )

            results.extend(offers)
            errors.extend(query_errors)

    return results, errors


def scrape_detailed_offers(headless=False):
    """Compatibilidad: scraping de la categoría fija 'trabajo-de-it'."""
    with browser_session(headless=headless) as page:
        return _scrape_search_page(page, DEFAULT_SEARCH_URL)