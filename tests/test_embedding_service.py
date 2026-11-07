
import numpy as np
import pytest
from unittest.mock import Mock, patch

from modulos.matching.embedding_service import EmbeddingService


@patch("modulos.matching.embedding_service.SentenceTransformer")
def test_encode_text(mock_transformer):
    mock_model = Mock()
    mock_model.encode.return_value = np.zeros(384)
    mock_transformer.return_value = mock_model

    service = EmbeddingService()

    result = service.encode_text(
        "Desarrollador Java con Spring Boot"
    )

    assert isinstance(result, np.ndarray)
    assert result.shape == (384,)

    mock_model.encode.assert_called_once_with(
        "Desarrollador Java con Spring Boot",
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )


@patch("modulos.matching.embedding_service.SentenceTransformer")
def test_encode_texts(mock_transformer):
    mock_model = Mock()
    mock_model.encode.return_value = np.zeros((2, 384))
    mock_transformer.return_value = mock_model

    service = EmbeddingService()

    texts = [
        "Desarrollador Java",
        "Programador backend"
    ]

    result = service.encode_texts(texts)

    assert isinstance(result, np.ndarray)
    assert result.shape == (2, 384)


@patch("modulos.matching.embedding_service.SentenceTransformer")
def test_encode_text_rejects_empty_text(mock_transformer):
    service = EmbeddingService()

    with pytest.raises(ValueError):
        service.encode_text("")


@patch("modulos.matching.embedding_service.SentenceTransformer")
def test_encode_texts_rejects_empty_list(mock_transformer):
    service = EmbeddingService()

    with pytest.raises(ValueError):
        service.encode_texts([])


@patch("modulos.matching.embedding_service.SentenceTransformer")
def test_encode_texts_rejects_empty_elements(mock_transformer):
    service = EmbeddingService()

    with pytest.raises(ValueError):
        service.encode_texts([
            "Desarrollador Java",
            ""
        ])
