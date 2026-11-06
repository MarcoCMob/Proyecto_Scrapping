
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from modulos.scraping.browser import browser_session


def main():

    url = "https://pe.computrabajo.com/trabajo-de-it"

    with browser_session(headless=False) as page:

        print("Accediendo a Computrabajo...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        # Esperar a que la página termine de cargar
        try:
            page.wait_for_load_state(
                "networkidle",
                timeout=15000
            )
        except PlaywrightTimeoutError:
            print("La página continúa realizando solicitudes.")

        # Obtener los enlaces de la página
        links = page.locator("a").evaluate_all("""
            elements => elements.map(element => ({
                text: element.innerText.trim(),
                href: element.href,
                class: element.className
            }))
        """)

        print("\nTOTAL DE ENLACES:", len(links))
        print("\nENLACES ENCONTRADOS")
        print("=" * 60)

        for index, link in enumerate(links, start=1):

            if link["text"] or link["href"]:

                print(f"\nENLACE {index}")
                print("Texto:", link["text"][:150])
                print("URL:", link["href"])
                print("Clase:", link["class"])

        input("\nPresiona ENTER para cerrar...")


if __name__ == "__main__":
    main()
