from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import uuid
from ..services.orchestrator import Orchestrator

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str = None

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.session_id:
        session_id = str(uuid.uuid4())
    else:
        session_id = request.session_id
    
    # Mock file info for now - in real implementation, this would come from upload
    file_info = {
        "filename": "sample_data.csv",
        "columns": ["date", "product", "revenue", "units_sold"],
        "size": 1024
    }
    
    orchestrator = Orchestrator()
    
    # Collect all steps for the response
    steps = []
    async for step in orchestrator.execute_workflow(session_id, request.query, file_info):
        steps.append(step)
    
    return {
        "session_id": session_id,
        "query": request.query,
        "steps": steps,
        "status": "completed"
    }
