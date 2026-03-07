from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

# Create FastAPI app
app = FastAPI(
    title="Quechua Q&A API",
    description="REST API for answering questions about Quechua language using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1", tags=["quechua"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Quechua Q&A API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "ask": "/api/v1/ask",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
