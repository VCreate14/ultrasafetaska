from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now()

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message")
    session_id: Optional[str] = Field(None, description="Optional session ID for continuing conversation")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The assistant's response")
    session_id: str = Field(..., description="The session ID for the conversation")
    sources: Optional[List[str]] = None
    timestamp: datetime = Field(..., description="Timestamp of the response")

class ErrorResponse(BaseModel):
    error: str
    detail: str = Field(..., description="Error message") 