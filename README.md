# Quechua Q&A System

A complete AI-powered Q&A system for answering questions about the Quechua language, featuring a FastAPI backend and Next.js frontend.

## 🌟 Features

- **AI-Powered Answers**: Uses Google Gemini to provide intelligent responses
- **Multi-Document Search**: Searches through Quechua grammar documents
- **Source Tracking**: Shows which document sections were used
- **Clean Architecture**: Layered backend with KISS principles
- **Modern Frontend**: Next.js with TypeScript and Tailwind CSS
- **Reusable Components**: Modular, maintainable codebase

## 📁 Project Structure

```
.
├── backend/              # FastAPI REST API
│   ├── app.py           # Main application
│   ├── api/             # API routes and models
│   ├── services/        # Business logic
│   ├── repositories/    # Data access layer
│   ├── core/            # Configuration and clients
│   └── data/            # JSON tree files
│
└── frontend/            # Next.js application
    ├── app/             # Pages and layouts
    ├── components/      # Reusable UI components
    └── lib/             # API client and types
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- pnpm (or npm)
- Google Gemini API key
- Page Index API key

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
PAGE_INDEX_API_KEY=your_page_index_api_key_here
GEMINI_MODEL=gemini-2.0-flash-thinking-exp-01-21
EOF

# Make sure data files exist
# - data/quechua_tree.json
# - data/gramar_tree.json

# Start the backend
python app.py
```

Backend will run on `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
pnpm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the frontend
pnpm dev
```

Frontend will run on `http://localhost:3000`

## 🏗️ Architecture

### Backend (FastAPI)

**Layered Architecture:**
- **API Layer** (`api/`): Request/response models, routes
- **Service Layer** (`services/`): Business logic, orchestration
- **Repository Layer** (`repositories/`): Data access
- **Core Layer** (`core/`): Configuration, external clients

**Key Features:**
- Clean separation of concerns
- Type-safe with Pydantic models
- Async/await for performance
- Comprehensive error handling

### Frontend (Next.js)

**Component-Based Architecture:**
- **Pages** (`app/`): Route-based pages
- **Components** (`components/`): Reusable UI components
- **Library** (`lib/`): API client, types, utilities

**Key Features:**
- TypeScript for type safety
- Tailwind CSS for styling
- Client-side rendering for interactivity
- Responsive design

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

**POST** `/api/v1/ask` - Ask a question
```json
{
  "question": "¿Cuáles son las reglas de formación de plural en quechua?"
}
```

**GET** `/api/v1/health` - Health check

## 🎨 Frontend Components

### QuestionInput
Input component for entering questions with Enter key support.

### AnswerCard
Displays AI-generated answers with reasoning and sources.

### SourceCard
Shows individual document sources with page numbers.

### LoadingSpinner / ErrorMessage
UI feedback components for different states.

## 💡 Usage Examples

### Example Questions

- "¿Cuáles son las reglas de formación de plural en quechua?"
- "¿Cómo se forman los verbos en tiempo presente?"
- "¿Qué son los sufijos en quechua?"
- "Traduce al español: Ñuqa hatun wasipi tiyani"

### Using the API Directly

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cómo se forma el plural en quechua?"}'
```

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/ask",
    json={"question": "¿Cómo se forma el plural en quechua?"}
)
print(response.json())
```

## 🧪 Testing

### Backend

```bash
cd backend
python test_api.py
```

### Frontend

```bash
cd frontend
pnpm build  # Check for build errors
```

## 🛠️ Development

### Backend Development

```bash
# With auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# With fast refresh
pnpm dev
```

## 🚢 Production Deployment

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
cd frontend
pnpm build
pnpm start
```

Or deploy to Vercel:
```bash
vercel deploy
```

## 📝 Environment Variables

### Backend (`.env`)
```env
GEMINI_API_KEY=your_api_key
PAGE_INDEX_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.0-flash-thinking-exp-01-21
```

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

This project follows KISS (Keep It Simple, Stupid) principles:
- Simple, readable code
- Clear separation of concerns
- Minimal dependencies
- Comprehensive documentation

## 📄 License

MIT

## 👥 Support

For questions or issues, please refer to:
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
