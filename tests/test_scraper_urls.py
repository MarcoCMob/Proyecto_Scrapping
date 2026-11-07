import pytest

from modulos.scraping.scraper_service import build_search_url


def test_build_search_url():
    assert build_search_url("desarrollador java junior") == (
        "https://pe.computrabajo.com/trabajo-de-desarrollador-java-junior"
    )


def test_build_search_url_removes_accents_and_extra_spaces():
    assert build_search_url("  Practicante Ingeniería  de Software ") == (
        "https://pe.computrabajo.com/"
        "trabajo-de-practicante-ingenieria-de-software"
    )


def test_build_search_url_rejects_empty():
    with pytest.raises(ValueError):
        build_search_url("   ")