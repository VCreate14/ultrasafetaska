from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import Optional
from functools import lru_cache
import secrets

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = Field(default="Customer Support RAG", description="Application name")
    DEBUG: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    API_V1_STR: str = Field(default="/api/v1", description="API version prefix")
    PROJECT_NAME: str = Field(default="Customer Support RAG Chatbot", description="Project name")
    
    # Authentication Settings
    SECRET_KEY: str = Field(..., description="Secret key for JWT tokens")
    ALGORITHM: str = Field(default="HS256", description="Algorithm for JWT tokens")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration time in minutes")
    
    # USF API Settings
    USF_API_URL: str = Field(..., description="USF API URL")
    USF_API_KEY: SecretStr = Field(..., description="USF API key")
    USF_MODEL: str = Field(default="usf1-mini", description="USF model to use")
    
    # Qdrant Settings
    QDRANT_URL: str = Field(..., description="Qdrant server URL")
    QDRANT_API_KEY: Optional[SecretStr] = Field(None, description="Qdrant API key")
    
    # Session Settings
    SESSION_TIMEOUT_MINUTES: int = Field(default=30, description="Session timeout in minutes")
    MAX_CHAT_HISTORY: int = Field(default=10, description="Maximum number of messages in chat history")
    
    # Model Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def validate_settings(self):
        """Validate that all required settings are properly configured."""
        required_settings = {
            "QDRANT_URL": self.QDRANT_URL,
            "USF_API_URL": self.USF_API_URL,
            "USF_API_KEY": self.USF_API_KEY,
            "SECRET_KEY": self.SECRET_KEY,
        }
        
        missing_settings = [
            key for key, value in required_settings.items()
            if not value
        ]
        
        if missing_settings:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_settings)}. "
                "Please set them in your .env file."
            )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Create settings instance
settings = get_settings()
settings.validate_settings() 