
from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    BigInteger,
    String,
    Text,
    DateTime,
    func,
    text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class JobOfferModel(Base):
    """
    Modelo ORM que representa la tabla job_offers
    de PostgreSQL.
    """

    __tablename__ = "job_offers"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    subtitle: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    company: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    summary: Mapped[List[str]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'[]'::jsonb")
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    url: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
