
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

        # Identificar los enlaces correspondientes a ofertas
        offers = page.locator("a.js-o-link")

        offers.first.wait_for(timeout=30000)

        total = offers.count()

        print(f"\nOfertas encontradas: {total}")

        # Inspeccionar las primeras 3 ofertas
        for index in range(min(total, 3)):

            offer = offers.nth(index)

            print("\n" + "=" * 70)
            print(f"OFERTA {index + 1}")
            print("=" * 70)

            print("Título:", offer.inner_text())
            print("URL:", offer.get_attribute("href"))

            # Examinar los elementos superiores del enlace
            ancestors = offer.evaluate("""
                element => {
                    const result = [];
                    let current = element;

                    for (let i = 0; i < 5 && current; i++) {

                        result.push({
                            tag: current.tagName,
                            class: current.className,
                            text: (current.innerText || "")
                                .trim()
                                .slice(0, 300)
                        });

                        current = current.parentElement;
                    }

                    return result;
                }
            """)

            print("\nESTRUCTURA DE ELEMENTOS:")

            for level, ancestor in enumerate(ancestors):

                print(f"\nNivel {level}")
                print("Etiqueta:", ancestor["tag"])
                print("Clase:", ancestor["class"])
                print("Texto:", ancestor["text"])


        input("\nPresiona ENTER para cerrar...")


if __name__ == "__main__":
    main()
