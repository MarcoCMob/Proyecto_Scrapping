from database.connection import SessionLocal
from modulos.cv_parser import extract_cv
from modulos.cv_analyzer import analyze_cv
from modulos.matching.matching_service import MatchingService
from modulos.scraping.scraper_service import scrape_searches
from repositories.job_offer_repository import JobOfferRepository
from schemas.cv_schema import CVProfile
from modulos.scraping.scraper_service import scrape_searches
from modulos.scraping.laborum_scraper import (
    scrape_searches as scrape_laborum_searches
)

MAX_QUERIES = 5


def analyze_cv_file(file) -> CVProfile:
    """Archivo -> texto -> CVProfile (con search_queries)."""
    return analyze_cv(extract_cv(file))


def get_search_terms(profile: CVProfile, limit: int = MAX_QUERIES) -> list[str]:
    """Usa search_queries; si Gemini no las generó, usa los puestos."""
    terms = profile.search_queries or profile.target_positions

    seen = set()
    cleaned = []

    for term in terms:
        term = " ".join(term.split())

        if term and term.lower() not in seen:
            seen.add(term.lower())
            cleaned.append(term)

    return cleaned[:limit]


def match_profile(
    profile: CVProfile,
    queries: list[str] | None = None,
    headless: bool = True,
    max_per_query: int | None = None,
    matching_service=None,
) -> dict:
    """
    Busca ofertas para cada término, las guarda en PostgreSQL
    (sin duplicados) y calcula la compatibilidad SOLO sobre las
    ofertas de esta búsqueda.
    """
    queries = queries or get_search_terms(profile)

    if not queries:
        raise ValueError(
            "No hay términos de búsqueda para este perfil."
        )

    # ESTO LO QUE HACE ES QUE PRIMERO: Busca ofertas en Computrabajo.
    computrabajo_offers, computrabajo_errors = scrape_searches(
        queries,
        headless=headless,
        max_per_query=max_per_query
    )

    # LUEGO ESO BUSQUE OFERTAS EN LABORUM!!
    laborum_offers, laborum_errors = scrape_laborum_searches(
        queries,
        headless=headless,
        max_per_query=max_per_query
    )

    # 3. FINALMENTE SE UNIFICAN LOS ERRORES Y OFERTAS PARA COMPARARLOS CON EL PERFIL DEL CANDIDATO.
    offers = computrabajo_offers + laborum_offers
    errors = computrabajo_errors + laborum_errors

    stats = {
        "queries": len(queries),
        "extracted": len(offers),
        "unique": 0,
        "new": 0,
    }

    if not offers:
        return {
            "profile": profile,
            "queries": queries,
            "results": [],
            "stats": stats,
            "errors": errors,
        }

    with SessionLocal() as session:
        stored, new_count = JobOfferRepository(session).save_many_all(offers)

        stats["unique"] = len(stored)
        stats["new"] = new_count

        service = matching_service or MatchingService()
        results = service.match_offers(profile, stored)

    return {
        "profile": profile,
        "queries": queries,
        "results": results,
        "stats": stats,
        "errors": errors,
    }


def match_cv_file(file, **kwargs) -> dict:
    """Flujo completo: CV -> perfil -> búsqueda -> ranking."""
    return match_profile(analyze_cv_file(file), **kwargs)