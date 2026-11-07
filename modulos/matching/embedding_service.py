
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:

    MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self):
        """
        Carga el modelo una sola vez al crear el servicio.
        """
        self.model = SentenceTransformer(self.MODEL_NAME)

    def encode_text(self, text: str) -> np.ndarray:
        """
        Convierte un texto individual en un embedding.
        """
        if not text or not text.strip():
            raise ValueError("El texto no puede estar vacío.")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embedding

    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """
        Convierte una lista de textos en embeddings.
        """
        if not texts:
            raise ValueError("La lista de textos no puede estar vacía.")

        if any(not text or not text.strip() for text in texts):
            raise ValueError("Ningún texto puede estar vacío.")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings
