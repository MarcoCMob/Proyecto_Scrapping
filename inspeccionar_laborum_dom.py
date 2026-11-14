
from modulos.scraping.browser import browser_session

SEARCH_URL = (
    "https://www.laborum.pe/search-jobs"
    "?q=Ingeniero%20de%20Sistemas"
)

DETAIL_URL = (
    "https://www.laborum.pe/job/"
    "facturactiva-del-peru-s-a-c/"
    "practica-profesional-ingeniero-de-sistemas/"
    "6aeab493f9137e58a5e0a1a0"
    "?q=Ingeniero%20de%20Sistemas"
)


def main():
    with browser_session(headless=False) as page:

        print("\n=== RESULTADOS DE BÚSQUEDA ===")

        page.goto(
            SEARCH_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )
        page.wait_for_timeout(6000)

        print("URL:", page.url)

        print("\nCampos de entrada:")
        print(page.locator("input").evaluate_all("""
            elements => elements.map(e => ({
                type: e.type,
                placeholder: e.placeholder,
                name: e.name,
                id: e.id,
                value: e.value
            }))
        """))

        print("\nEnlaces de ofertas:")
        links = page.locator('a[href*="/job/"]')

        for i in range(min(10, links.count())):
            link = links.nth(i)

            print({
                "text": link.inner_text().strip()[:300],
                "href": link.get_attribute("href"),
                "class": link.get_attribute("class")
            })

        print("\n=== ESTRUCTURA DEL DETALLE ===")

        page.goto(
            DETAIL_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )
        page.wait_for_timeout(5000)

        print("URL:", page.url)

        selectors = [
            "h1",
            "h2",
            "main",
            "article",
            "[class*='title']",
            "[class*='company']",
            "[class*='description']",
            "[class*='location']"
        ]

        for selector in selectors:
            locator = page.locator(selector)

            print(f"\nSelector: {selector}")
            print("Coincidencias:", locator.count())

            for i in range(min(5, locator.count())):
                element = locator.nth(i)

                print({
                    "text": element.inner_text().strip()[:500],
                    "class": element.get_attribute("class")
                })


if __name__ == "__main__":
    main()
