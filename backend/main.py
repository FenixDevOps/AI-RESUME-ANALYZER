from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api import analyzer_routes, builder_routes, dashboard_routes, jobs_routes

app = FastAPI(title="Smart AI Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyzer_routes.router, prefix="/api/analyzer", tags=["Analyzer"])
app.include_router(builder_routes.router, prefix="/api/builder", tags=["Builder"])
app.include_router(dashboard_routes.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(jobs_routes.router, prefix="/api/jobs", tags=["Jobs"])

# Ensure the frontend build directory exists before mounting
frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

if os.path.exists(frontend_dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_path, "assets")), name="assets")

    # Serve the main index.html for any other route (React Router support)
    @app.api_route("/{full_path:path}", methods=["GET", "HEAD"])
    def serve_frontend(full_path: str):
        # Allow requests to /api to fall through (though they should be caught by router above)
        if full_path.startswith("api/"):
            return {"error": "API route not found"}
        
        index_path = os.path.join(frontend_dist_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend build not found. Please run 'npm run build' in frontend directory."}
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to Smart AI Resume Analyzer API (Frontend not built)"}
