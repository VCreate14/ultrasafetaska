from sentence_transformers import SentenceTransformer
from app.core.logging import get_logger
from app.core.config import settings
from typing import List
import numpy as np

logger = get_logger()

class EmbeddingManager:
    def __init__(self):
        self.model_name = "all-MiniLM-L6-v2"
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Initialized embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {str(e)}")
            raise

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text."""
        try:
            # Convert text to embedding
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        try:
            # Convert texts to embeddings
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

# Create singleton instance
embedding_manager = EmbeddingManager() 