from typing import List, Dict, Any, Optional
import httpx
from app.rag.embeddings import embedding_manager
from app.db.qdrant_client import qdrant_manager
from app.rag.reranker import reranker
from app.core.logging import get_logger
from app.core.config import settings
from pydantic import BaseModel

logger = get_logger()

class Document(BaseModel):
    content: str
    metadata: Dict[str, Any]

class RAGPipeline:
    def __init__(self):
        self.api_url = settings.USF_API_URL
        self.api_key = settings.USF_API_KEY.get_secret_value()
        self.model = settings.USF_MODEL
        logger.info(f"Initialized RAG pipeline with model: {self.model}")

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve and rerank relevant documents for the query."""
        try:
            # Generate query embedding
            query_embedding = embedding_manager.get_embedding(query)
            
            # Search for relevant documents
            search_results = qdrant_manager.search(query_embedding)
            
            # Format results
            documents = []
            for result in search_results:
                documents.append(Document(
                    content=result.payload.get("content", ""),
                    metadata={
                        "source": result.payload.get("source", "unknown"),
                        "score": result.score
                    }
                ))
            
            # Rerank documents
            reranked_docs = reranker.rerank(query, [doc.dict() for doc in documents])
            
            # Convert back to Document objects
            return [Document(**doc) for doc in reranked_docs]
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise

    async def generate_response(self, query: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate response using RAG pipeline."""
        try:
            # Get relevant documents
            documents = self.get_relevant_documents(query)
            
            # Create context from documents
            context = "\n".join([doc.content for doc in documents])
            
            # Prepare messages for USF API
            messages = []
            if chat_history:
                messages.extend(chat_history)
            
            # Add system message with context
            messages.append({
                "role": "system",
                "content": f"Use the following context to answer the user's question:\n\n{context}"
            })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": query
            })

            # Prepare request payload
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.1,
                "stream": False,
                "max_tokens": 1024
            }

            # Make request to USF API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract the response text
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    raise ValueError("Invalid response format from USF API")

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

rag_pipeline = RAGPipeline() 