
def get_optional_text(container, selector):
    """Obtiene el texto de un elemento o devuelve None."""

    element = container.locator(selector).first

    if element.count() == 0:
        return None

    text = element.inner_text().strip()

    return text if text else None


def extract_offer_details(page, card):
    """Selecciona una oferta y extrae su información detallada."""

    card_title = get_optional_text(card, "a.js-o-link")

    if not card_title:
        raise ValueError("La tarjeta no tiene título.")

    # Seleccionar la oferta
    card.locator("a.js-o-link").first.click()

    # Esperar hasta que el panel muestre el título seleccionado
    page.wait_for_function(
        """
        expectedTitle => {
            const element = document.querySelector(
                '[data-offers-grid-detail-title]'
            );

            return element &&
                   element.textContent.trim() === expectedTitle;
        }
        """,
        arg=card_title,
        timeout=30000
    )

    detail = page.locator("[data-offers-grid-box-detail]")

    description_element = detail.locator(
        '[data-testid="offer-description"]'
    )

    description_element.wait_for(
        state="visible",
        timeout=30000
    )

    description = description_element.inner_text().strip()

    summary = detail.locator(
        ".description_offer p.dFlex.mb10"
    ).all_inner_texts()

    return {
        "title": get_optional_text(
            detail,
            "[data-offers-grid-detail-title]"
        ),
        "subtitle": get_optional_text(
            detail,
            ".header_detail p[offer-detail-not-applied]"
        ),
        "company": get_optional_text(
            detail,
            ".header_detail p.fs16 a"
        ),
        "location": get_optional_text(
            detail,
            ".header_detail p.fs16.mb5"
        ),
        "summary": [
            item.strip() for item in summary
        ],
        "description": description
    }
