
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.job_offer_model import JobOfferModel
from schemas.job_schema import JobOffer


class JobOfferRepository:
    """
    Gestiona las operaciones de persistencia de ofertas laborales.
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, offer: JobOffer) -> JobOfferModel:
        """Guarda una oferta laboral en PostgreSQL."""

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

    def save_many(
        self,
        offers: List[JobOffer]
    ) -> List[JobOfferModel]:
        """Guarda varias ofertas en una sola transacción."""

        if not offers:
            return []

        try:
            db_offers = [
                JobOfferModel(**offer.model_dump())
                for offer in offers
            ]

            self.session.add_all(db_offers)
            self.session.commit()

            for offer in db_offers:
                self.session.refresh(offer)

            return db_offers

        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, offer_id: int) -> Optional[JobOfferModel]:
        """Busca una oferta por su identificador."""

        return self.session.get(JobOfferModel, offer_id)

    def get_all(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[JobOfferModel]:
        """Obtiene ofertas con paginación."""

        statement = (
            select(JobOfferModel)
            .order_by(JobOfferModel.scraped_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(self.session.scalars(statement).all())

    def count(self) -> int:
        """Devuelve la cantidad total de ofertas almacenadas."""

        statement = select(func.count()).select_from(JobOfferModel)

        return self.session.scalar(statement)

    def delete_by_id(self, offer_id: int) -> bool:
        """Elimina una oferta por su identificador."""

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
