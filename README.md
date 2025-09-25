# 🤖 RidvanYigit.com AI Chatbot

A FastAPI-powered AI chatbot integrated into Rıdvan Yiğit's personal portfolio website. Features real-time chat with GPT-4, professional AI consultation, and seamless Vercel deployment.

## ✨ Features

- **🚀 FastAPI Backend**: High-performance REST API with async support
- **🧠 OpenAI GPT-4 Integration**: Intelligent responses powered by OpenAI API
- **💬 Real-time Chat Interface**: Smooth, responsive UI without iframe dependencies
- **🔒 Rate Limiting**: Built-in protection against API abuse
- **🎯 Conversation Memory**: Maintains context within chat sessions  
- **⚡ Lightning Fast**: Optimized for performance and scalability
- **🐳 Docker Ready**: Containerized for consistent deployments
- **📱 Mobile Responsive**: Works perfectly on all devices
- **🌙 Dark Mode**: Supports light/dark theme switching

## 🛠 Tech Stack

- **Backend**: FastAPI + Python 3.11
- **Frontend**: Vanilla JavaScript (ES6+)
- **AI**: OpenAI GPT-4 API
- **Package Management**: UV (fastest Python package manager)
- **Deployment**: Vercel (serverless functions)
- **Containerization**: Docker + Docker Compose
- **Styling**: Modern CSS with CSS Variables

## 📁 Project Structure

```
ridvan-chatbot-project/
├── .env                    # Environment variables
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── pyproject.toml          # UV/Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup
├── vercel.json             # Vercel deployment config
├── api/                    # FastAPI backend
│   ├── __init__.py
│   ├── main.py             # Main FastAPI app
│   ├── models.py           # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── openai_service.py # OpenAI integration
│   └── utils/
│       ├── __init__.py
│       └── config.py       # Configuration management
└── public/                 # Frontend assets
    └── index.html          # Main website
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [UV package manager](https://github.com/astral-sh/uv)
- OpenAI API key
- Git

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ridvanyigit/ridvan-chatbot-project.git
cd ridvan-chatbot-project

# Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

**Required Environment Variables:**
```env
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,https://www.ridvanyigit.com
```

### 3. Run Locally

```bash
# Start the development server
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
uv run python -m uvicorn api.main:app --reload
```

Visit `http://localhost:8000` to see your application!

## 🐳 Docker Deployment

### Development with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Docker Build

```bash
# Build production image
docker build -t ridvan-chatbot:latest .

# Run production container
docker run -d \
  --name ridvan-chatbot \
  -p 8000:8000 \
  --env-file .env \
  ridvan-chatbot:latest
```

## ☁️ Vercel Deployment

### One-Time Setup

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Configure Environment Variables**:
```bash
# Add your OpenAI API key
vercel env add OPENAI_API_KEY
```

### Deploy to Production

```bash
# Deploy to production
vercel --prod

# Or deploy specific branch
vercel --prod --target production
```

### Environment Variables in Vercel

Add these environment variables in your Vercel dashboard:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ENVIRONMENT`: `production`
- `LOG_LEVEL`: `INFO`
- `ALLOWED_ORIGINS`: `https://www.ridvanyigit.com,https://ridvanyigit.com`

## 🧪 Testing

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=api tests/

# Lint code
uv run black api/
uv run isort api/
uv run flake8 api/
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve main website |
| `POST` | `/api/chat` | Send chat message |
| `GET` | `/api/health` | Health check |

### Example Chat Request

```bash
curl -X POST "https://your-domain.com/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Hello! Can you tell me about Rıdvan'\''s AI expertise?",
       "conversation_id": "conv_123"
     }'
```

### Example Response

```json
{
  "response": "Hello! I'd be happy to tell you about Rıdvan's expertise...",
  "conversation_id": "conv_123",
  "timestamp": "2025-01-15T10:30:00Z",
  "model_used": "gpt-4"
}
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | OpenAI API key (required) |
| `ENVIRONMENT` | `development` | Environment mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `AI_MODEL` | `gpt-4` | OpenAI model to use |
| `AI_MAX_TOKENS` | `500` | Max tokens per response |
| `AI_TEMPERATURE` | `0.7` | Response creativity (0-1) |
| `RATE_LIMIT_REQUESTS` | `30` | Requests per minute |
| `ALLOWED_ORIGINS` | `*` | CORS allowed origins |

### Model Configuration

The chatbot uses GPT-4 by default but can be configured to use other models:

```env
AI_MODEL=gpt-4-turbo
AI_MAX_TOKENS=750
AI_TEMPERATURE=0.8
```

## 🔐 Security Features

- **Rate Limiting**: 30 requests per minute per IP
- **CORS Protection**: Configurable allowed origins
- **Input Validation**: Pydantic models for all requests
- **Error Handling**: Secure error responses
- **Environment Isolation**: Separate configs for dev/prod

## 📱 Frontend Integration

The chatbot integrates seamlessly with the existing website:

```javascript
// Initialize chatbot
const chatbot = new ChatbotManager();

// Send a message
await chatbot.sendMessage("Hello!");
```

## 🔍 Monitoring & Logging

### Health Check

```bash
curl https://your-domain.com/api/health
```

### Log Levels

- `DEBUG`: Detailed debugging information
- `INFO`: General information (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages only

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Workflow

```bash
# Install development dependencies
uv sync --group dev

# Format code
uv run black .
uv run isort .

# Run tests
uv run pytest

# Check types
uv run mypy api/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rıdvan Yiğit**
- Website: [ridvanyigit.com](https://ridvanyigit.com)
- LinkedIn: [ridvan-yigit-5494842b6](https://linkedin.com/in/ridvan-yigit-5494842b6/)
- GitHub: [@ridvanyigit](https://github.com/ridvanyigit)
- Email: ridvanyigit@gmx.net

## 🙏 Acknowledgments

- OpenAI for the GPT-4 API
- FastAPI team for the amazing framework
- Vercel for seamless deployment
- UV team for fast Python package management

---

**Built with ❤️ in Vienna, Austria 🇦🇹**
