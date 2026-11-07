from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:

    MODEL_NAME = "intfloat/multilingual-e5-base"

    def __init__(self):
        """
        Carga el modelo una sola vez al crear el servicio.
        """
        self.model = SentenceTransformer(self.MODEL_NAME)

    def encode_text(self, text: str) -> np.ndarray:
        """
        Convierte el texto de una consulta (el CV) en un embedding.
        """
        if not text or not text.strip():
            raise ValueError("El texto no puede estar vacío.")

        return self.model.encode(
            f"query: {text}",
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """
        Convierte una lista de documentos (las ofertas) en embeddings.
        """
        if not texts:
            raise ValueError("La lista de textos no puede estar vacía.")

        if any(not text or not text.strip() for text in texts):
            raise ValueError("Ningún texto puede estar vacío.")

        return self.model.encode(
            [f"passage: {text}" for text in texts],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )