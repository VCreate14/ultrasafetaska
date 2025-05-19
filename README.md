# Customer Support RAG Chatbot

A FastAPI-based customer support chatbot that uses Langchain and Qdrant Cloud for Retrieval-Augmented Generation (RAG).

## Features

- FastAPI backend with async support
- Langchain integration for RAG pipeline
- Qdrant Cloud for vector storage
- USF API integration for LLM responses
- Cross-encoder reranking for improved search results
- JWT authentication for secure access
- In-memory session management
- Comprehensive logging
- Evaluation metrics for RAG performance
- CORS support
- Environment-based configuration
- Pydantic settings management

## Prerequisites

- Python 3.9+
- USF API access
- Qdrant Cloud account
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd customer-support-rag
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
# USF API Configuration
USF_API_URL=your_usf_api_url
USF_API_KEY=your_usf_api_key
USF_MODEL=usf1-mini

# Qdrant Configuration
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=your_collection_name

# Application Settings
APP_NAME=Customer Support RAG
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=INFO
API_PREFIX=/api/v1
SESSION_EXPIRY=3600
MAX_HISTORY=10

# Security Settings
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Usage

Start the server:
```bash
# Using Python
python main.py

# Or using Uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Authentication

- `POST /api/v1/auth/token`: Get JWT access token
- `POST /api/v1/auth/refresh`: Refresh JWT token

### Chat

- `POST /api/v1/chat`: Send a message to the chatbot
  - Requires JWT authentication
  - Supports session management
  - Returns chat history and response

## Project Structure

```
customer-support-rag/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── deps.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   ├── qdrant_client.py
│   │   └── reranker.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── metrics.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── auth.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_rag.py
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Environment Variables

- `USF_API_URL`: URL for the USF API
- `USF_API_KEY`: Key for accessing the USF API
- `USF_MODEL`: Model to use (default: usf1-mini)
- `QDRANT_URL`: URL for Qdrant Cloud
- `QDRANT_API_KEY`: API key for Qdrant Cloud
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection
- `APP_NAME`: Name of the application
- `DEBUG`: Enable debug mode
- `ENVIRONMENT`: Environment (development/production)
- `LOG_LEVEL`: Logging level
- `API_PREFIX`: API prefix for all routes
- `SESSION_EXPIRY`: Session expiry time in seconds
- `MAX_HISTORY`: Maximum number of messages to keep in history
- `SECRET_KEY`: Secret key for JWT
- `ALGORITHM`: Algorithm for JWT
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiry time

## Features in Detail

### RAG Pipeline
- Document retrieval using Qdrant
- Cross-encoder reranking for improved relevance
- USF API integration for response generation
- Context-aware responses

### Authentication
- JWT-based authentication
- Token refresh mechanism
- Secure password hashing
- Token expiry management

### Session Management
- In-memory session storage
- Automatic session cleanup
- Session expiry handling
- Chat history management

### Evaluation Metrics
- Retrieval metrics (Precision, Recall, F1)
- Semantic similarity scoring
- Response quality assessment
- Performance monitoring

## Testing

Run tests using pytest:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 