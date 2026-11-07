
from sqlalchemy import select, func

from database.connection import SessionLocal
from models.job_offer_model import JobOfferModel


def test_job_offer_model():
    with SessionLocal() as session:
        total = session.scalar(
            select(func.count()).select_from(JobOfferModel)
        )

    print(f"Ofertas registradas actualmente: {total}")

    assert total >= 0
