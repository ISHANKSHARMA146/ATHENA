from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
import os

# Add parent directory to path so we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes import auth, company, jd
from config.settings import settings
# Import Vercel-compatible Firebase initialization
from api.firebase_helper import initialize_firebase_for_vercel

# Initialize Firebase with Vercel compatibility
initialize_firebase_for_vercel()

app = FastAPI(title="Athena - Firebase + Hasura Integration")

# Configure CORS to allow all origins for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory of the current file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set up templates and static folders
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Mount static files directory
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")

# Include routers with prefixes
app.include_router(auth.router, prefix="/auth")
app.include_router(company.router, prefix="/company")
app.include_router(jd.router, prefix="/jd")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/templates/{component_type}/{file_name}")
async def get_component(component_type: str, file_name: str):
    """Serve component templates"""
    file_path = os.path.join(base_dir, "templates", component_type, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

@app.get("/api/config/firebase")
async def get_firebase_config():
    """Securely serve Firebase configuration"""
    return {
        "apiKey": settings.firebase_api_key,
        "authDomain": settings.firebase_auth_domain,
        "projectId": settings.firebase_project,
        "storageBucket": settings.firebase_storage_bucket,
        "messagingSenderId": settings.firebase_messaging_sender_id,
        "appId": settings.firebase_app_id,
        "measurementId": settings.firebase_measurement_id
    } 