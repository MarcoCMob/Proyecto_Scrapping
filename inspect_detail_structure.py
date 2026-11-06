
from modulos.scraping.browser import browser_session


def inspect_detail_structure():

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

        # Seleccionar la primera oferta
        first_card = cards.first

        title = first_card.locator(
            "a.js-o-link"
        ).first.inner_text().strip()

        print(f"\nSeleccionando: {title}")

        first_card.locator("a.js-o-link").first.click()

        # Esperar a que aparezca el detalle
        description_heading = page.get_by_text(
            "Descripción de la oferta",
            exact=True
        )

        description_heading.wait_for(timeout=30000)

        print("\nESTRUCTURA HTML DEL DETALLE")
        print("=" * 60)

        # Recorrer los elementos padres del encabezado
        ancestors = description_heading.evaluate("""
            element => {
                const result = [];
                let current = element;

                for (let level = 0; level < 7 && current; level++) {

                    result.push({
                        level: level,
                        tag: current.tagName,
                        id: current.id,
                        class: current.className,
                        text_length: current.innerText.length,
                        text_preview: current.innerText.substring(0, 500),
                        html: current.outerHTML.substring(0, 1500)
                    });

                    current = current.parentElement;
                }

                return result;
            }
        """)

        for item in ancestors:

            print(f"\nNIVEL {item['level']}")
            print("-" * 60)

            print("TAG:", item["tag"])
            print("ID:", item["id"])
            print("CLASS:", item["class"])
            print("LONGITUD DEL TEXTO:", item["text_length"])
            print("TEXTO:", item["text_preview"])
            print("HTML:", item["html"])

        input("\nPresiona ENTER para cerrar...")


if __name__ == "__main__":
    inspect_detail_structure()
