
from typing import Any, Sequence

from schemas.cv_schema import CVProfile
from schemas.job_schema import JobOffer

from modulos.matching.text_builder import (
    build_cv_text,
    build_offer_text
)
from modulos.matching.embedding_service import EmbeddingService
from modulos.matching.similarity_service import SimilarityService


class MatchingService:

    def __init__(self, embedding_service=None):
        """
        Inicializa el servicio de compatibilidad.

        Permite recibir un EmbeddingService externo
        para facilitar las pruebas unitarias.
        """
        self.embedding_service = (
            embedding_service
            if embedding_service is not None
            else EmbeddingService()
        )

    def match_offers(
        self,
        profile: CVProfile,
        offers: Sequence[JobOffer]
    ) -> list[dict[str, Any]]:
        """
        Calcula la similitud semántica entre un CV
        y una lista de ofertas laborales.

        Devuelve las ofertas ordenadas de mayor
        a menor similitud.
        """

        if not offers:
            return []

        # 1. Convertir el perfil del candidato en texto.
        cv_text = build_cv_text(profile)

        if not cv_text.strip():
            raise ValueError(
                "El perfil del candidato no contiene información."
            )

        # 2. Convertir todas las ofertas en texto.
        offer_texts = [
            build_offer_text(offer)
            for offer in offers
        ]

        # 3. Generar el embedding del CV una sola vez.
        cv_embedding = self.embedding_service.encode_text(
            cv_text
        )

        # 4. Generar los embeddings de todas las ofertas
        # en una sola operación.
        offer_embeddings = self.embedding_service.encode_texts(
            offer_texts
        )

        # 5. Calcular la similitud de cada oferta con el CV.
        results = []

        for offer, offer_embedding in zip(
            offers,
            offer_embeddings,
            strict=True
        ):
            similarity = SimilarityService.calculate_similarity(
                cv_embedding,
                offer_embedding
            )

            results.append({
                "offer": offer,
                "similarity": similarity
            })

        # 6. Ordenar de mayor a menor similitud.
        results.sort(
            key=lambda result: result["similarity"],
            reverse=True
        )

        return results
