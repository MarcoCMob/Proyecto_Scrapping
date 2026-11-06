
from modulos.scraping.browser import browser_session


def main():

    url = "https://pe.computrabajo.com/trabajo-de-it"

    print("Iniciando navegador...")

    with browser_session(headless=False) as page:

        print("Accediendo a Computrabajo...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("\nPÁGINA CARGADA")
        print("-------------------------")

        print("Título:", page.title())
        print("URL:", page.url)

        print("\nCONTENIDO DE LA PÁGINA")
        print("-------------------------")

        contenido = page.locator("body").inner_text()

        print(contenido[:5000])

        input(
            "\nPresiona ENTER para cerrar el navegador..."
        )


if __name__ == "__main__":
    main()
