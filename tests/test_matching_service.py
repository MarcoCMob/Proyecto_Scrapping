
import numpy as np
import pytest
from unittest.mock import Mock

from schemas.cv_schema import CVProfile
from schemas.job_schema import JobOffer

from modulos.matching.matching_service import MatchingService


def create_offer(title):
    return JobOffer(
        title=title,
        company="Empresa de prueba",
        location="Lima",
        description="Oferta laboral de prueba.",
        source="Computrabajo"
    )


def test_match_offers_orders_by_similarity():

    # Perfil del candidato.
    profile = CVProfile(
        profession="Ingeniería de Software",
        skills=["Java", "Spring Boot", "PostgreSQL"],
        target_positions=["Desarrollador Backend Junior"]
    )

    # Ofertas de prueba.
    offer_a = create_offer("Analista de soporte")
    offer_b = create_offer("Desarrollador Backend")
    
    # Simular el servicio de embeddings.
    mock_embedding_service = Mock()

    mock_embedding_service.encode_text.return_value = np.array(
        [1.0, 0.0]
    )

    mock_embedding_service.encode_texts.return_value = np.array([
        [0.0, 1.0],
        [1.0, 0.0]
    ])

    service = MatchingService(
        embedding_service=mock_embedding_service
    )

    results = service.match_offers(
        profile,
        [offer_a, offer_b]
    )

    # La oferta B debe tener mayor similitud.
    assert len(results) == 2
    assert results[0]["offer"] is offer_b
    assert results[1]["offer"] is offer_a

    assert results[0]["similarity"] == pytest.approx(1.0)
    assert results[1]["similarity"] == pytest.approx(0.0)

    # El CV debe codificarse una sola vez.
    mock_embedding_service.encode_text.assert_called_once()

    # Las ofertas deben codificarse en un solo lote.
    mock_embedding_service.encode_texts.assert_called_once()


def test_match_offers_with_empty_list():

    profile = CVProfile(
        profession="Ingeniería de Software"
    )

    mock_embedding_service = Mock()

    service = MatchingService(
        embedding_service=mock_embedding_service
    )

    results = service.match_offers(profile, [])

    assert results == []

    # No es necesario generar embeddings.
    mock_embedding_service.encode_text.assert_not_called()
    mock_embedding_service.encode_texts.assert_not_called()


def test_match_offers_rejects_empty_profile():

    profile = CVProfile()

    offer = create_offer("Desarrollador Backend")

    mock_embedding_service = Mock()

    service = MatchingService(
        embedding_service=mock_embedding_service
    )

    with pytest.raises(ValueError):
        service.match_offers(profile, [offer])

    mock_embedding_service.encode_text.assert_not_called()
