"""Configuration management for the application."""
import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str
    ai_model: str = "gpt-4"
    ai_max_tokens: int = 500
    ai_temperature: float = 0.7
    
    # Application Configuration
    environment: str = "development"
    log_level: str = "INFO"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,https://www.ridvanyigit.com,https://ridvanyigit.com"
    
    # Rate Limiting
    rate_limit_requests: int = 30
    rate_limit_window: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()