
import re
import unicodedata
from difflib import SequenceMatcher
from urllib.parse import urlsplit, urlunsplit


def normalize_url(url):
    """
    Normaliza una URL eliminando fragmentos de navegación
    y diferencias irrelevantes al final de la ruta.
    """
    if not url:
        return ""

    parts = urlsplit(url.strip())

    return urlunsplit((
        parts.scheme.lower(),
        parts.netloc.lower(),
        parts.path.rstrip("/"),
        parts.query,
        ""
    ))

def normalize_text(value):
    """
    Normaliza un texto para facilitar su comparación.
    Convierte a minúsculas, elimina tildes y espacios innecesarios.
    """
    if not value:
        return ""

    value = value.lower().strip()

    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value
        if unicodedata.category(char) != "Mn"
    )

    value = re.sub(r"\s+", " ", value)

    return value


def calculate_description_similarity(description_a, description_b):
    """
    Calcula la similitud entre dos descripciones.
    Devuelve un valor entre 0 y 1.
    """
    text_a = normalize_text(description_a)
    text_b = normalize_text(description_b)

    if not text_a or not text_b:
        return 0.0

    return SequenceMatcher(
        None,
        text_a,
        text_b
    ).ratio()


def compare_offers(new_offer, existing_offer, threshold=0.95):

    # Primera comprobación: URL de la publicación.
    new_url = normalize_url(getattr(new_offer, "url", None))
    existing_url = normalize_url(getattr(existing_offer, "url", None))

    if new_url and existing_url and new_url == existing_url:
        return True

    # Segunda comprobación: identidad de la oferta.
    identity_fields = ["title", "company", "location"]

    for field in identity_fields:
        new_value = normalize_text(getattr(new_offer, field, None))
        existing_value = normalize_text(
            getattr(existing_offer, field, None)
        )

        if not new_value or not existing_value:
            return False

        if new_value != existing_value:
            return False

    # Tercera comprobación: similitud de las descripciones.
    similarity = calculate_description_similarity(
        new_offer.description,
        existing_offer.description
    )

    return similarity >= threshold