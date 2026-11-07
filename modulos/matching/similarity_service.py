
import numpy as np


class SimilarityService:

    @staticmethod
    def calculate_similarity(
        embedding_a: np.ndarray,
        embedding_b: np.ndarray
    ) -> float:
        """
        Calcula la similitud coseno entre dos embeddings.
        """

        vector_a = np.asarray(embedding_a, dtype=float)
        vector_b = np.asarray(embedding_b, dtype=float)

        # Validar que ambos sean vectores unidimensionales.
        if vector_a.ndim != 1 or vector_b.ndim != 1:
            raise ValueError("Los embeddings deben ser vectores unidimensionales.")

        # Validar que tengan las mismas dimensiones.
        if vector_a.shape != vector_b.shape:
            raise ValueError("Los embeddings deben tener las mismas dimensiones.")

        # Validar que no contengan valores inválidos.
        if not np.all(np.isfinite(vector_a)) or not np.all(np.isfinite(vector_b)):
            raise ValueError("Los embeddings contienen valores inválidos.")

        # Calcular las magnitudes de los vectores.
        norm_a = np.linalg.norm(vector_a)
        norm_b = np.linalg.norm(vector_b)

        if norm_a == 0 or norm_b == 0:
            raise ValueError("No se puede calcular la similitud de un vector nulo.")

        # Calcular la similitud coseno.
        similarity = np.dot(vector_a, vector_b) / (norm_a * norm_b)

        # Evitar pequeñas desviaciones por precisión numérica.
        similarity = np.clip(similarity, -1.0, 1.0)

        return float(similarity)
