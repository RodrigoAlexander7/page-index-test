from fastapi import APIRouter, HTTPException, status
from api.models import QuestionRequest, AnswerResponse, HealthResponse
from services.quechua_service import QuechuaService
from repositories.tree_repository import TreeRepository
from pathlib import Path

# Initialize repository and service
root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"
tree_repository = TreeRepository(data_dir)
quechua_service = QuechuaService(tree_repository)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        message="Quechua API is running"
    )


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about Quechua language.
    
    The API will search through Quechua grammar documents and provide
    an answer based on the relevant content found.
    """
    try:
        result = await quechua_service.answer_question(request.question)
        
        return AnswerResponse(
            answer=result["answer"],
            reasoning=result["reasoning"],
            nodes_used=result["nodes_used"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )
