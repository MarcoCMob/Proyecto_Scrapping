
from modulos.scraping.browser import browser_session

SEARCH_URL = "https://www.laborum.pe/search-jobs"

DETAIL_URL = (
    "https://www.laborum.pe/job/"
    "facturactiva-del-peru-s-a-c/"
    "practica-profesional-ingeniero-de-sistemas/"
    "6aeab493f9137e58a5e0a1a0"
    "?q=Ingeniero%20de%20Sistemas"
)


def main():
    with browser_session(headless=False) as page:

        # 1. Inspeccionar el buscador.
        print("\n=== BUSCADOR DE LABORUM ===")

        page.goto(
            SEARCH_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        inputs = page.locator("input").evaluate_all("""
            elements => elements.map(element => ({
                type: element.type,
                placeholder: element.placeholder,
                name: element.name,
                id: element.id,
                ariaLabel: element.getAttribute("aria-label")
            }))
        """)

        print("\nCampos encontrados:")
        for item in inputs:
            print(item)

        search_box = page.locator(
            'input[placeholder*="Busca"]'
        ).first

        if search_box.count() > 0:
            search_box.fill("Ingeniero de Sistemas")
            search_box.press("Enter")
            page.wait_for_timeout(7000)

            print("\nURL después de buscar:")
            print(page.url)
        else:
            print("\nNo se encontró el campo de búsqueda.")

        # 2. Inspeccionar las publicaciones encontradas.
        print("\n=== ENLACES DE OFERTAS ===")

        links = page.locator('a[href*="/job/"]')
        total = links.count()

        print(f"Enlaces encontrados: {total}")

        for index in range(min(total, 15)):
            link = links.nth(index)

            print(f"\nOferta {index + 1}")
            print("Título:", link.inner_text().strip())
            print("URL:", link.get_attribute("href"))

        # 3. Inspeccionar el detalle de una publicación.
        print("\n=== DETALLE DE UNA OFERTA ===")

        page.goto(
            DETAIL_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        print("\nTítulos HTML:")
        headings = page.locator("h1, h2, h3").all_inner_texts()

        for heading in headings:
            print("-", heading.strip())

        print("\nContenido de la publicación:")
        print(page.locator("body").inner_text()[:7000])


if __name__ == "__main__":
    main()
