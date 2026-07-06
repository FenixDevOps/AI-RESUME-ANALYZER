from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/")
def dashboard_status():
    return {"status": "Dashboard API is running"}

@router.get("/stats")
def get_dashboard_stats():
    """Return aggregated dashboard stats."""
    return {
        "total_analyses": 12,
        "average_score": 74,
        "ats_pass_rate": 68,
        "top_role": "Software Engineer",
        "analyses_this_week": 3,
        "improvement_trend": "+8pts",
        "skills_identified": 47,
        "jobs_saved": 5,
    }

@router.get("/tips")
def get_career_tips():
    """Return actionable career improvement tips."""
    tips = [
        {"icon": "🎯", "title": "Tailor for Each Role", "body": "Customize your resume keywords to match each job description. ATS systems rank tailored resumes 2x higher."},
        {"icon": "📊", "title": "Quantify Achievements", "body": "Replace vague statements with numbers. 'Increased sales by 40%' beats 'Improved sales performance'."},
        {"icon": "🔑", "title": "Use Action Verbs", "body": "Start each bullet with a strong action verb: Led, Designed, Built, Reduced, Optimized, Delivered."},
        {"icon": "📄", "title": "Keep It Concise", "body": "For under 10 years experience, keep your resume to 1 page. Recruiters spend ~6 seconds on first scan."},
        {"icon": "🤝", "title": "LinkedIn Alignment", "body": "Make sure your LinkedIn profile matches your resume. Recruiters cross-reference both before calling."},
        {"icon": "🧠", "title": "Show Impact, Not Tasks", "body": "Focus on what you accomplished, not what you did. Results-oriented resumes stand out from the crowd."},
    ]
    return {"tips": tips}
