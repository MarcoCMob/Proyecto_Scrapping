
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

        # 1. Inspeccionar la tarjeta de resultados
        print("\n=== ESTRUCTURA DE UNA TARJETA ===")

        page.goto(
            SEARCH_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )
        page.wait_for_timeout(5000)

        card = page.locator('a[href*="/job/"]').first

        if card.count():
            structure = card.evaluate("""
                element => {
                    const result = [];
                    let current = element;

                    for (let i = 0; i < 5 && current; i++) {
                        result.push({
                            tag: current.tagName,
                            class: current.className,
                            text: current.innerText?.slice(0, 500),
                            html: current.outerHTML.slice(0, 1200)
                        });

                        current = current.parentElement;
                    }

                    return result;
                }
            """)

            for item in structure:
                print("\nElemento:")
                print(item)

        # 2. Inspeccionar el detalle de la oferta
        print("\n=== ESTRUCTURA DEL DETALLE ===")

        page.goto(
            DETAIL_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )
        page.wait_for_timeout(5000)

        result = page.evaluate("""
            () => {
                const target = "Práctica Profesional - Ingeniero de Sistemas";

                const elements = Array.from(
                    document.querySelectorAll("body *")
                );

                const matches = elements.filter(element => {
                    return (
                        element.children.length === 0 &&
                        element.innerText?.trim()
                            .toLowerCase()
                            .includes(target.toLowerCase())
                    );
                });

                return matches.slice(0, 5).map(element => {
                    const ancestors = [];
                    let current = element;

                    for (let i = 0; i < 6 && current; i++) {
                        ancestors.push({
                            tag: current.tagName,
                            class: current.className,
                            text: current.innerText?.slice(0, 700),
                            html: current.outerHTML.slice(0, 1500)
                        });

                        current = current.parentElement;
                    }

                    return ancestors;
                });
            }
        """)

        for index, ancestors in enumerate(result):
            print(f"\nCoincidencia {index + 1}")

            for item in ancestors:
                print("\nElemento:")
                print(item)

        # 3. Mostrar texto del contenido principal
        print("\n=== TEXTO DE MAIN ===")

        print(
            page.locator("main").inner_text()[-5000:]
        )


if __name__ == "__main__":
    main()
