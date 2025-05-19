from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.logging import get_logger
from app.core.config import settings
from typing import List, Dict, Any, Optional
import numpy as np

logger = get_logger()

class QdrantManager:
    def __init__(self):
        try:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY.get_secret_value() if settings.QDRANT_API_KEY else None
            )
            self.collection_name = "customer_support_docs"
            self._ensure_collection()
            logger.info("Initialized Qdrant client")
        except Exception as e:
            logger.error(f"Error initializing Qdrant client: {str(e)}")
            raise

    def _ensure_collection(self):
        """Ensure the collection exists with proper configuration."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=384,  # Size for all-MiniLM-L6-v2
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection: {str(e)}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Add documents to the collection."""
        try:
            points = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                points.append(models.PointStruct(
                    id=i,
                    vector=embedding,
                    payload={
                        "content": doc["content"],
                        "source": doc.get("source", "unknown"),
                        "metadata": doc.get("metadata", {})
                    }
                ))
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Added {len(documents)} documents to collection")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            
            results = []
            for scored_point in search_result:
                results.append({
                    "content": scored_point.payload.get("content", ""),
                    "source": scored_point.payload.get("source", "unknown"),
                    "score": scored_point.score,
                    "metadata": scored_point.payload.get("metadata", {})
                })
            
            return results
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise

# Create singleton instance
qdrant_manager = QdrantManager() 