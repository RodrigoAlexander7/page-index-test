from pydantic import BaseModel, Field
from typing import List, Optional


class QuestionRequest(BaseModel):
    """Request model for asking questions about Quechua"""
    question: str = Field(..., description="Question about Quechua language", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "¿Cuáles son las reglas de formación de plural en quechua?"
            }
        }


class NodeInfo(BaseModel):
    """Information about a retrieved node"""
    node_id: str
    page_index: int
    title: str
    source: str  # "quechua" or "gramar"


class AnswerResponse(BaseModel):
    """Response model with answer and metadata"""
    answer: str
    reasoning: str
    nodes_used: List[NodeInfo]
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
