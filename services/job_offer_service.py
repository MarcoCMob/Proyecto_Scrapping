
import math
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from repositories.job_offer_repository import JobOfferRepository


class JobOfferService:

    def __init__(self, session: Session):
        self.repository = JobOfferRepository(session)

    def search_offers(
        self,
        page: int = 1,
        per_page: int = 10,
        title: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        source: Optional[str] = None
    ) -> Dict[str, Any]:

        if page < 1:
            raise ValueError("La página debe ser mayor o igual a 1.")

        if per_page < 1:
            raise ValueError("La cantidad por página debe ser mayor a 0.")

        # Calcular cuántos registros debemos omitir.
        offset = (page - 1) * per_page

        # Recuperar las ofertas correspondientes a la página.
        offers = self.repository.get_all(
            limit=per_page,
            offset=offset,
            title=title,
            company=company,
            location=location,
            source=source
        )

        # Contar todas las ofertas que cumplen los filtros.
        total = self.repository.count(
            title=title,
            company=company,
            location=location,
            source=source
        )

        # Calcular el número total de páginas.
        total_pages = math.ceil(total / per_page)

        return {
            "offers": offers,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
