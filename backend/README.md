# Quechua Q&A REST API

A FastAPI-based REST API for answering questions about the Quechua language using AI-powered document retrieval and generation.

## Architecture

The application follows a **layered architecture** based on **KISS principles**:

```
├── app.py                      # FastAPI application entry point
├── api/                        # API Layer
│   ├── models.py              # Request/Response models (Pydantic)
│   └── routes.py              # API endpoints
├── services/                   # Service Layer
│   └── quechua_service.py     # Business logic for Q&A
├── repositories/               # Data Layer
│   └── tree_repository.py     # Tree data access
├── core/                       # Core utilities
│   ├── client.py              # LLM client (Gemini)
│   └── config.py              # Configuration
└── data/                       # Data files
    ├── quechua_tree.json      # Quechua grammar document tree
    └── gramar_tree.json       # Gramar document tree
```

## Features

- **Question Answering**: Ask questions about Quechua grammar and language
- **Multi-Document Search**: Searches both Quechua grammar documents
- **AI-Powered**: Uses Google Gemini for intelligent retrieval and generation
- **Source Tracking**: Returns which document sections were used
- **RESTful API**: Clean, documented API endpoints

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
PAGE_INDEX_API_KEY=your_page_index_api_key_here
GEMINI_MODEL=gemini-2.0-flash-thinking-exp-01-21
```

### 3. Ensure Tree Data Files Exist

Make sure these files exist in the `data/` directory:
- `quechua_tree.json`
- `gramar_tree.json`

## Running the API

### Development Mode

```bash
python app.py
```

Or with uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint
- **GET** `/`
  - Returns API information and available endpoints

### Health Check
- **GET** `/api/v1/health`
  - Returns API health status

### Ask Question
- **POST** `/api/v1/ask`
  - Answer questions about Quechua language
  
**Request Body:**
```json
{
  "question": "¿Cuáles son las reglas de formación de plural en quechua?"
}
```

**Response:**
```json
{
  "answer": "En quechua, el plural se forma...",
  "reasoning": "Based on the grammar sections...",
  "nodes_used": [
    {
      "node_id": "node_123",
      "page_index": 45,
      "title": "Formación de plurales",
      "source": "quechua"
    }
  ]
}
```

## Interactive Documentation

Once the API is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Example Usage

### Using curl

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son las reglas de formación de plural en quechua?"}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/ask",
    json={"question": "¿Cuáles son las reglas de formación de plural en quechua?"}
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"\nSources used: {len(result['nodes_used'])} nodes")
```

## How It Works

1. **Question Received**: User sends a question via POST request
2. **Tree Search**: LLM searches both document trees for relevant sections
3. **Context Extraction**: Relevant text content is extracted from identified nodes
4. **Answer Generation**: LLM generates answer based on extracted context
5. **Response**: Answer with reasoning and source nodes is returned

## Layer Responsibilities

### API Layer (`api/`)
- Request validation
- Response formatting
- HTTP error handling

### Service Layer (`services/`)
- Business logic
- Orchestrating tree search and answer generation
- Coordinating between repository and LLM client

### Repository Layer (`repositories/`)
- Loading tree data from JSON files
- Node mapping and access
- Data extraction

### Core Layer (`core/`)
- LLM client configuration
- Application settings

## Development

The architecture is designed to be:
- **Simple**: Easy to understand and modify (KISS principle)
- **Maintainable**: Clear separation of concerns
- **Testable**: Each layer can be tested independently
- **Extensible**: Easy to add new features or data sources

## License

MIT
