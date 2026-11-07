from typing import Any, Sequence

from schemas.cv_schema import CVProfile

from modulos.matching.text_builder import (
    build_cv_text,
    build_offer_text,
    OfferLike
)
from modulos.matching.embedding_service import EmbeddingService
from modulos.matching.similarity_service import SimilarityService
from modulos.matching.skill_matching import find_skill_matches

SEMANTIC_WEIGHT = 0.6
SKILLS_WEIGHT = 0.4
SKILLS_CAP = 5  # con 5 coincidencias la señal ya es máxima


class MatchingService:

    def __init__(self, embedding_service=None):
        self.embedding_service = (
            embedding_service
            if embedding_service is not None
            else EmbeddingService()
        )

    def match_offers(
        self,
        profile: CVProfile,
        offers: Sequence[OfferLike]
    ) -> list[dict[str, Any]]:
        """
        Combina similitud semántica y coincidencia de skills
        técnicas. Devuelve las ofertas ordenadas por "score".
        """

        if not offers:
            return []

        cv_text = build_cv_text(profile)

        if not cv_text.strip():
            raise ValueError(
                "El perfil del candidato no contiene información."
            )

        offer_texts = [build_offer_text(offer) for offer in offers]

        cv_embedding = self.embedding_service.encode_text(cv_text)
        offer_embeddings = self.embedding_service.encode_texts(
            offer_texts
        )

        similarities = [
            SimilarityService.calculate_similarity(
                cv_embedding, offer_embedding
            )
            for offer_embedding in offer_embeddings
        ]

        # Reescalar la similitud a 0-1 dentro del lote,
        # para recuperar la separación que e5 comprime.
        low, high = min(similarities), max(similarities)
        spread = high - low

        results = []

        for offer, offer_text, similarity in zip(
            offers, offer_texts, similarities, strict=True
        ):
            semantic = (
                (similarity - low) / spread if spread > 0 else 0.0
            )

            matched = find_skill_matches(profile.skills, offer_text)
            skills_signal = min(len(matched), SKILLS_CAP) / SKILLS_CAP

            results.append({
                "offer": offer,
                "similarity": similarity,
                "skill_matches": matched,
                "score": (
                    SEMANTIC_WEIGHT * semantic
                    + SKILLS_WEIGHT * skills_signal
                ),
            })

        results.sort(key=lambda r: r["score"], reverse=True)

        return results