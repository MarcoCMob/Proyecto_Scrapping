
import numpy as np
import pytest

from modulos.matching.similarity_service import SimilarityService


def test_identical_vectors():
    vector_a = np.array([1.0, 0.0, 0.0])
    vector_b = np.array([1.0, 0.0, 0.0])

    result = SimilarityService.calculate_similarity(
        vector_a, vector_b
    )

    assert result == pytest.approx(1.0)


def test_orthogonal_vectors():
    vector_a = np.array([1.0, 0.0])
    vector_b = np.array([0.0, 1.0])

    result = SimilarityService.calculate_similarity(
        vector_a, vector_b
    )

    assert result == pytest.approx(0.0)


def test_opposite_vectors():
    vector_a = np.array([1.0, 0.0])
    vector_b = np.array([-1.0, 0.0])

    result = SimilarityService.calculate_similarity(
        vector_a, vector_b
    )

    assert result == pytest.approx(-1.0)


def test_different_dimensions():
    vector_a = np.array([1.0, 0.0])
    vector_b = np.array([1.0, 0.0, 0.0])

    with pytest.raises(ValueError):
        SimilarityService.calculate_similarity(
            vector_a, vector_b
        )


def test_zero_vector():
    vector_a = np.array([0.0, 0.0])
    vector_b = np.array([1.0, 0.0])

    with pytest.raises(ValueError):
        SimilarityService.calculate_similarity(
            vector_a, vector_b
        )


def test_multidimensional_array():
    vector_a = np.array([[1.0, 0.0]])
    vector_b = np.array([[1.0, 0.0]])

    with pytest.raises(ValueError):
        SimilarityService.calculate_similarity(
            vector_a, vector_b
        )
