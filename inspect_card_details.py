
from modulos.scraping.browser import browser_session


def main():

    url = "https://pe.computrabajo.com/trabajo-de-it"

    with browser_session(headless=False) as page:

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        cards = page.locator("article.box_offer")
        cards.first.wait_for(timeout=30000)

        # Inspeccionaremos las primeras 3 tarjetas
        for index in range(min(cards.count(), 3)):

            card = cards.nth(index)

            print("\n" + "=" * 70)
            print(f"DETALLES DE LA TARJETA {index + 1}")
            print("=" * 70)

            elements = card.locator("*").evaluate_all("""
                elements => elements.map(element => ({
                    tag: element.tagName,
                    class: typeof element.className === "string"
                        ? element.className
                        : "",
                    text: (element.innerText || "")
                        .trim()
                        .replace(/\\s+/g, " ")
                }))
                .filter(element => element.text.length > 0)
            """)

            for element in elements:

                print(
                    f"TAG: {element['tag']} | "
                    f"CLASS: {element['class']} | "
                    f"TEXT: {element['text'][:150]}"
                )

        input("\nPresiona ENTER para cerrar...")


if __name__ == "__main__":
    main()
