from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.resume_builder import ResumeBuilder

router = APIRouter()
builder = ResumeBuilder()

class ResumeData(BaseModel):
    template: str = "Modern"
    personal_info: Dict[str, Any]
    summary: Optional[str] = None
    experience: Optional[List[Dict[str, Any]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[Dict[str, Any]]] = None

@router.get("/")
def builder_status():
    return {"status": "Builder API is running"}

@router.post("/generate")
async def generate_resume(data: ResumeData):
    try:
        data_dict = data.model_dump()
        buffer = builder.generate_resume(data_dict)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={data.personal_info.get('full_name', 'resume').replace(' ', '_')}_resume.docx"}
        )
    except Exception as e:
        print(f"Error generating resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))
