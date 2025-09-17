"""Pydantic models for request/response validation."""
from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Individual chat message model."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    history: Optional[List[ChatMessage]] = Field(default_factory=list, description="Chat history")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, can you help me with AI development?",
                "conversation_id": "conv_123",
                "history": [
                    {"role": "user", "content": "Hi there!"},
                    {"role": "assistant", "content": "Hello! How can I help you today?"}
                ]
            }
        }


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="AI assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    timestamp: str = Field(..., description="Response timestamp")
    model_used: str = Field(..., description="AI model used for the response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "I'd be happy to help you with AI development! What specific area are you interested in?",
                "conversation_id": "conv_123",
                "timestamp": "2025-01-15T10:30:00Z",
                "model_used": "gpt-4"
            }
        }


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="Application version")
    openai_available: bool = Field(..., description="OpenAI API availability")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-01-15T10:30:00Z",
                "version": "1.0.0",
                "openai_available": True
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "Message cannot be empty",
                "timestamp": "2025-01-15T10:30:00Z"
            }
        }