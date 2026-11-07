from database.connection import SessionLocal
from modulos.cv_parser import extract_cv
from modulos.cv_analyzer import analyze_cv
from modulos.matching.matching_service import MatchingService
from services.job_offer_service import JobOfferService


def match_cv_file(file, matching_service=None) -> dict:
    """
    Flujo completo: archivo -> texto -> CVProfile -> ofertas
    de PostgreSQL -> ranking por similitud.
    """
    cv_text = extract_cv(file)
    profile = analyze_cv(cv_text)

    with SessionLocal() as session:
        offers = JobOfferService(session).get_all_offers()

        if not offers:
            return {"profile": profile, "results": []}

        service = matching_service or MatchingService()
        results = service.match_offers(profile, offers)

    return {"profile": profile, "results": results}