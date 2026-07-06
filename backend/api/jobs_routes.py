from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def jobs_status():
    return {"status": "Jobs API is running"}
