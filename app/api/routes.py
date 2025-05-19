from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.schemas.chat import ChatRequest, ChatResponse
from app.rag.pipeline import rag_pipeline
from app.core.logging import get_logger
from app.core.config import settings
from app.core.models import User, Token
from app.core.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user
)
import uuid
from typing import Dict, List, Optional
from pydantic import BaseModel

router = APIRouter()
logger = get_logger()

class Session(BaseModel):
    created_at: datetime
    last_activity: datetime
    chat_history: List[Dict[str, str]]

# In-memory session storage
sessions: Dict[str, Session] = {}

def get_or_create_session(session_id: Optional[str] = None) -> str:
    """Get existing session or create new one."""
    if session_id and session_id in sessions:
        return session_id
    
    new_session_id = str(uuid.uuid4())
    sessions[new_session_id] = Session(
        created_at=datetime.now(),
        last_activity=datetime.now(),
        chat_history=[]
    )
    return new_session_id

def cleanup_expired_sessions():
    """Remove expired sessions."""
    current_time = datetime.now()
    expired_sessions = [
        session_id for session_id, session in sessions.items()
        if current_time - session.last_activity > timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
    ]
    for session_id in expired_sessions:
        del sessions[session_id]

@router.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Handle chat requests."""
    try:
        # Get or create session
        session_id = get_or_create_session(request.session_id)
        session = sessions[session_id]
        
        # Update session activity
        session.last_activity = datetime.now()
        
        # Generate response using RAG pipeline
        response = await rag_pipeline.generate_response(
            query=request.message,
            chat_history=session.chat_history
        )
        
        # Update chat history
        session.chat_history.append({
            "role": "user",
            "content": request.message
        })
        session.chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Keep only last N messages to prevent context window issues
        if len(session.chat_history) > settings.MAX_CHAT_HISTORY:
            session.chat_history = session.chat_history[-settings.MAX_CHAT_HISTORY:]
        
        # Cleanup expired sessions
        cleanup_expired_sessions()
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 