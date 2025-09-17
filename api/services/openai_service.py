"""OpenAI API service for chat functionality."""
import logging
from typing import List, Dict, Any
from datetime import datetime
import uuid

import openai
from openai import AsyncOpenAI

from api.models import ChatMessage, ChatRequest, ChatResponse
from api.utils.config import settings

# Setup logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)


class OpenAIService:
    """Service class for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize OpenAI service."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI assistant."""
        return """You are an AI assistant for Rıdvan Yiğit, an AI Engineer and Autonomous Agent Developer based in Vienna. 

Your role is to represent Rıdvan professionally and help visitors learn about his work, expertise, and services. Here's what you should know about him:

**About Rıdvan:**
- AI Engineer specializing in autonomous agent systems
- Expert in CrewAI, LangChain, LangGraph, AutoGen, OpenAI Agents SDK, and MCP
- Based in Vienna, Austria (originally from Hakkari, Turkey)
- Focuses on building practical AI solutions for businesses
- Offers custom AI agent development, web development, and AI consulting

**Key Expertise:**
- Autonomous Agent Systems (CrewAI, LangChain, LangGraph, AutoGen)
- OpenAI API Integration and fine-tuning
- Backend Development (Python, FastAPI)
- Machine Learning and NLP
- Web Development with AI integration
- Business process automation

**Notable Projects:**
- Fine-tuned LLM for price prediction (outperformed GPT-4o)
- RAG-powered Q&A systems
- Multi-agent SDLC automation with CrewAI
- Self-refining AI assistants with LangGraph
- Multi-modal customer service assistants

**Services Offered:**
1. Custom AI Agent Development
2. AI-Powered Web Applications  
3. AI Strategy & Consulting

**Communication Style:**
- Be professional but approachable
- Focus on practical AI applications and business value
- Highlight Rıdvan's engineering-first approach
- Emphasize his ability to create clear, functional solutions
- Be knowledgeable about AI technologies but explain them clearly

**Guidelines:**
- Always stay in character as Rıdvan's AI assistant
- Direct complex technical discussions or project inquiries toward contacting Rıdvan directly
- Be helpful in explaining AI concepts and Rıdvan's expertise
- Don't make commitments on behalf of Rıdvan (pricing, timelines, etc.)
- Encourage visitors to reach out through the contact form for serious inquiries

Remember: Your goal is to be helpful, informative, and to showcase Rıdvan's expertise while encouraging meaningful connections with potential clients or collaborators."""

    async def generate_response(self, chat_request: ChatRequest) -> ChatResponse:
        """Generate a response using OpenAI API."""
        try:
            # Prepare messages for OpenAI API
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if available
            if chat_request.history:
                for msg in chat_request.history[-10:]:  # Limit to last 10 messages
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Add current user message
            messages.append({
                "role": "user", 
                "content": chat_request.message
            })
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=settings.ai_model,
                messages=messages,
                max_tokens=settings.ai_max_tokens,
                temperature=settings.ai_temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # Extract response content
            ai_response = response.choices[0].message.content.strip()
            
            # Generate conversation ID if not provided
            conversation_id = chat_request.conversation_id or str(uuid.uuid4())
            
            # Create response object
            chat_response = ChatResponse(
                response=ai_response,
                conversation_id=conversation_id,
                timestamp=datetime.utcnow().isoformat() + "Z",
                model_used=settings.ai_model
            )
            
            logger.info(f"Generated response for conversation {conversation_id}")
            return chat_response
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise Exception(f"AI service error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in generate_response: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible."""
        try:
            # Simple API call to test connectivity
            response = await self.client.models.list()
            return len(list(response.data)) > 0
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False
    
    def _prepare_conversation_history(self, history: List[ChatMessage]) -> List[Dict[str, Any]]:
        """Prepare conversation history for OpenAI API format."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]


# Global service instance
openai_service = OpenAIService()