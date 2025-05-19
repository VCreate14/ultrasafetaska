from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.core.logging import get_logger

logger = get_logger()

class EvaluationMetrics:
    @staticmethod
    def calculate_retrieval_metrics(query: str, retrieved_docs: List[Dict[str, Any]], 
                                  relevant_docs: List[Dict[str, Any]], k: int = 3) -> Dict[str, float]:
        """Calculate retrieval metrics."""
        try:
            # Calculate precision@k
            retrieved_ids = set(doc["id"] for doc in retrieved_docs[:k])
            relevant_ids = set(doc["id"] for doc in relevant_docs)
            precision = len(retrieved_ids.intersection(relevant_ids)) / k if k > 0 else 0
            
            # Calculate recall@k
            recall = len(retrieved_ids.intersection(relevant_ids)) / len(relevant_ids) if relevant_ids else 0
            
            # Calculate F1@k
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            return {
                "precision@k": precision,
                "recall@k": recall,
                "f1@k": f1
            }
        except Exception as e:
            logger.error(f"Error calculating retrieval metrics: {str(e)}")
            raise

    @staticmethod
    def calculate_semantic_similarity(text1: str, text2: str, 
                                   embedding_model) -> float:
        """Calculate semantic similarity between two texts."""
        try:
            # Get embeddings
            embedding1 = embedding_model.encode(text1)
            embedding2 = embedding_model.encode(text2)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                embedding1.reshape(1, -1), 
                embedding2.reshape(1, -1)
            )[0][0]
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {str(e)}")
            raise

    @staticmethod
    def calculate_response_quality(response: str, 
                                 reference: str, 
                                 embedding_model) -> Dict[str, float]:
        """Calculate response quality metrics."""
        try:
            # Calculate semantic similarity
            similarity = EvaluationMetrics.calculate_semantic_similarity(
                response, reference, embedding_model
            )
            
            # Calculate length ratio
            length_ratio = len(response) / len(reference) if len(reference) > 0 else 0
            
            return {
                "semantic_similarity": similarity,
                "length_ratio": length_ratio
            }
        except Exception as e:
            logger.error(f"Error calculating response quality: {str(e)}")
            raise

# Create singleton instance
evaluation_metrics = EvaluationMetrics() 