
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class JobOffer(BaseModel):
    """
    Representa una oferta laboral extraída de un portal
    de empleo.
    """

    title: str

    subtitle: Optional[str] = None

    company: Optional[str] = None

    location: Optional[str] = None

    summary: list[str] = Field(
        default_factory=list
    )

    description: str

    url: Optional[str] = None

    source: str

    scraped_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
