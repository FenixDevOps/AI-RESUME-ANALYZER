from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import io
import sys
import os
import re

# Ensure we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ai_resume_analyzer import AIResumeAnalyzer

router = APIRouter()
analyzer = AIResumeAnalyzer()

@router.get("/")
def analyzer_status():
    return {"status": "Analyzer API is running"}

def extract_keywords(text: str) -> set:
    """Extract meaningful keywords from text."""
    stopwords = {
        "with", "that", "this", "have", "from", "they", "will", "been",
        "your", "more", "when", "into", "than", "then", "some", "what",
        "about", "also", "which", "their", "would", "other", "should",
        "must", "able", "work", "role", "team", "good", "strong",
        "experience", "knowledge", "skills", "ability", "excellent",
        "proficiency", "understanding", "familiarity", "years", "the",
        "and", "for", "are", "not", "you", "all", "can", "her", "was",
        "one", "our", "out", "day", "get", "has", "him", "his", "how",
        "its", "use", "may", "new", "now", "old", "see", "two", "who",
        "did", "let", "put", "say", "she", "too", "any", "here", "high",
        "come", "give", "just", "look", "make", "most", "over", "such",
        "take", "time", "very", "well", "year"
    }
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]{2,}\b', text.lower())
    return {w for w in words if w not in stopwords and len(w) >= 3}

def compute_jd_match(resume_text: str, job_description: str):
    """Compute keyword match between resume and job description."""
    jd_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)

    matched = sorted(jd_keywords & resume_keywords)
    missing = sorted(jd_keywords - resume_keywords)

    # Limit to top results
    matched = matched[:30]
    missing = missing[:30]

    match_percent = round(len(matched) / max(len(jd_keywords), 1) * 100)
    return {
        "match_percent": min(match_percent, 100),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "total_jd_keywords": len(jd_keywords),
    }

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_role: str = Form(None),
    job_description: str = Form(None)
):
    try:
        contents = await file.read()
        file_obj = io.BytesIO(contents)
        file_obj.name = file.filename

        if file.filename.lower().endswith('.pdf'):
            text = analyzer.extract_text_from_pdf(file_obj)
        elif file.filename.lower().endswith('.docx'):
            text = analyzer.extract_text_from_docx(file_obj)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")

        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from the file.")

        analysis_result = analyzer.analyze_resume_with_gemini(
            resume_text=text,
            job_description=job_description,
            job_role=job_role
        )

        if isinstance(analysis_result, dict) and "error" in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result["error"])

        # Compute JD keyword match if job description provided
        jd_match = None
        if job_description and job_description.strip():
            jd_match = compute_jd_match(text, job_description)

        return {
            "analysis": analysis_result,
            "jd_match": jd_match
        }
    except Exception as e:
        print(f"Error in analyze_resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

