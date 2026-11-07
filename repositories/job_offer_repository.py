
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.job_offer_model import JobOfferModel
from schemas.job_schema import JobOffer
from services.offer_deduplication_service import (
    compare_offers,
    normalize_url
)

class JobOfferRepository:

    def __init__(self, session: Session):
        self.session = session

    def find_duplicate(self, offer: JobOffer) -> Optional[JobOfferModel]:

        # 1. Buscar primero por URL.
        if offer.url:
            candidates = self.session.scalars(
                select(JobOfferModel).where(
                    JobOfferModel.source == offer.source,
                    JobOfferModel.url.isnot(None)
                )
            ).all()

            normalized_new_url = normalize_url(offer.url)

            for candidate in candidates:
                if normalize_url(candidate.url) == normalized_new_url:
                    return candidate

        # 2. Si faltan datos de identidad, no podemos
        # realizar una comparación de contenido confiable.
        if not offer.title or not offer.company or not offer.location:
            return None

        # 3. Buscar candidatos por título, empresa y ubicación.
        statement = select(JobOfferModel).where(
            func.lower(func.trim(JobOfferModel.title))
            == offer.title.strip().lower(),

            func.lower(func.trim(JobOfferModel.company))
            == offer.company.strip().lower(),

            func.lower(func.trim(JobOfferModel.location))
            == offer.location.strip().lower()
        )

        candidates = self.session.scalars(statement).all()

        for candidate in candidates:
            if compare_offers(offer, candidate):
                return candidate

        return None

    def save(self, offer: JobOffer) -> JobOfferModel:
        """
        Guarda una oferta individual.
        Si ya existe, devuelve el registro existente.
        """

        duplicate = self.find_duplicate(offer)

        if duplicate:
            return duplicate

        try:
            offer_data = offer.model_dump()
            db_offer = JobOfferModel(**offer_data)

            self.session.add(db_offer)
            self.session.commit()
            self.session.refresh(db_offer)

            return db_offer

        except Exception:
            self.session.rollback()
            raise

    def save_many(self, offers: List[JobOffer]) -> List[JobOfferModel]:
        """
        Guarda múltiples ofertas evitando duplicados.

        Comprueba tanto los registros existentes en PostgreSQL
        como las ofertas repetidas dentro del mismo lote.
        """

        if not offers:
            return []

        saved_offers = []
        pending_offers = []

        try:
            for offer in offers:

                # 1. Comprobar duplicados dentro del mismo lote.
                duplicate_in_batch = any(
                    compare_offers(offer, pending)
                    for pending in pending_offers
                )

                if duplicate_in_batch:
                    continue

                # 2. Comprobar duplicados en PostgreSQL.
                duplicate_in_database = self.find_duplicate(offer)

                if duplicate_in_database:
                    continue

                # 3. Preparar el nuevo registro.
                db_offer = JobOfferModel(**offer.model_dump())

                self.session.add(db_offer)

                pending_offers.append(db_offer)
                saved_offers.append(db_offer)

            # Guardar todos los registros nuevos en una transacción.
            self.session.commit()

            return saved_offers

        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, offer_id: int) -> Optional[JobOfferModel]:
        return self.session.get(JobOfferModel, offer_id)

    
    def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        title: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        source: Optional[str] = None
    ) -> List[JobOfferModel]:

        statement = select(JobOfferModel)

        # Filtro por título
        if title:
            statement = statement.where(
                JobOfferModel.title.ilike(f"%{title}%")
            )

        # Filtro por empresa
        if company:
            statement = statement.where(
                JobOfferModel.company.ilike(f"%{company}%")
            )

        # Filtro por ubicación
        if location:
            statement = statement.where(
                JobOfferModel.location.ilike(f"%{location}%")
            )

        # Filtro por fuente
        if source:
            statement = statement.where(
                JobOfferModel.source.ilike(f"%{source}%")
            )

        # Ordenar y aplicar paginación
        statement = (
            statement
            .order_by(JobOfferModel.scraped_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(self.session.scalars(statement).all())

    def count(
        self,
        title: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        source: Optional[str] = None
    ) -> int:
        statement = select(func.count()).select_from(JobOfferModel)

        if title:
            statement = statement.where(
                JobOfferModel.title.ilike(f"%{title}%")
            )

        if company:
            statement = statement.where(
                JobOfferModel.company.ilike(f"%{company}%")
            )

        if location:
            statement = statement.where(
                JobOfferModel.location.ilike(f"%{location}%")
            )

        if source:
            statement = statement.where(
                JobOfferModel.source.ilike(f"%{source}%")
            )

        return self.session.scalar(statement)

    def delete_by_id(self, offer_id: int) -> bool:
        offer = self.get_by_id(offer_id)

        if offer is None:
            return False

        try:
            self.session.delete(offer)
            self.session.commit()
            return True

        except Exception:
            self.session.rollback()
            raise
    def list_all(self) -> List[JobOfferModel]:
        """Devuelve todas las ofertas, las más recientes primero."""
        statement = select(JobOfferModel).order_by(
            JobOfferModel.scraped_at.desc()
        )
        return list(self.session.scalars(statement).all())