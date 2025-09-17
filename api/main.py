"""FastAPI main application for the chatbot API."""
import logging
from datetime import datetime
from typing import Dict, Any
import os

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
import uvicorn

from api.models import (
    ChatRequest, 
    ChatResponse, 
    HealthResponse, 
    ErrorResponse
)
from api.services.openai_service import openai_service
from api.utils.config import settings

# Setup logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Rıdvan Yiğit AI Chatbot",
    description="AI Assistant for ridvanyigit.com",
    version="1.0.0",
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Rate limiting storage (in-memory for simplicity)
rate_limit_storage: Dict[str, Dict[str, Any]] = {}

def check_rate_limit(client_ip: str) -> bool:
    """Simple rate limiting implementation."""
    current_time = datetime.utcnow().timestamp()
    
    if client_ip not in rate_limit_storage:
        rate_limit_storage[client_ip] = {
            "requests": 1,
            "window_start": current_time
        }
        return True
    
    client_data = rate_limit_storage[client_ip]
    
    # Reset window if expired
    if current_time - client_data["window_start"] > settings.rate_limit_window:
        rate_limit_storage[client_ip] = {
            "requests": 1,
            "window_start": current_time
        }
        return True
    
    # Check if within limits
    if client_data["requests"] < settings.rate_limit_requests:
        client_data["requests"] += 1
        return True
    
    return False

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error for {request.url}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception for {request.url}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )

# Routes
@app.get("/", response_class=FileResponse)
async def serve_index():
    """Serve the main HTML page."""
    index_path = "public/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Rıdvan Yiğit AI Chatbot API"}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        openai_available = await openai_service.health_check()
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat() + "Z",
            version="1.0.0",
            openai_available=openai_available
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: Request, chat_request: ChatRequest):
    """Main chat endpoint."""
    # Get client IP for rate limiting
    client_ip = request.client.host
    
    # Check rate limiting
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    
    try:
        # Generate AI response
        response = await openai_service.generate_response(chat_request)
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate response"
        )

@app.get("/api/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    """Get chat history for a conversation (placeholder for future implementation)."""
    # This would typically fetch from a database
    return {"message": "Chat history feature coming soon", "conversation_id": conversation_id}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting Rıdvan Yiğit AI Chatbot API")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Test OpenAI connection
    try:
        openai_available = await openai_service.health_check()
        logger.info(f"OpenAI API available: {openai_available}")
    except Exception as e:
        logger.error(f"OpenAI connection test failed: {e}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down Rıdvan Yiğit AI Chatbot API")

# For local development
if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )