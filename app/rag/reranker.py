from typing import List, Dict, Any
from sentence_transformers import CrossEncoder
from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger()

class Reranker:
    def __init__(self):
        self.model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
        try:
            self.model = CrossEncoder(self.model_name)
            logger.info(f"Initialized reranker model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error initializing reranker model: {str(e)}")
            raise

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        """Rerank documents based on relevance to the query."""
        try:
            # Prepare document pairs for reranking
            pairs = [(query, doc["content"]) for doc in documents]
            
            # Get relevance scores
            scores = self.model.predict(pairs)
            
            # Combine documents with scores
            scored_docs = list(zip(documents, scores))
            
            # Sort by score in descending order
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            
            # Return top k documents
            reranked_docs = [doc for doc, _ in scored_docs[:top_k]]
            
            return reranked_docs
        except Exception as e:
            logger.error(f"Error reranking documents: {str(e)}")
            raise

# Create singleton instance
reranker = Reranker() 