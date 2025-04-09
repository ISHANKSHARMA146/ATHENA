# main.py
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import auth, company, jd
from config.settings import settings
import firebase_admin_setup  # This ensures Firebase is initialized
from utils.logger import Logger

# Initialize Logger
logger = Logger("main").get_logger()

# For Vercel serverless deployment - export the app directly
app = FastAPI(
    title="ATHENA AI API",
    description="API for ATHENA AI",
    version="0.1.0",
)

# Configure CORS to allow all origins for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/components", StaticFiles(directory="templates"), name="components")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers with prefixes
app.include_router(auth.router, prefix="/auth")
app.include_router(company.router, prefix="/company", tags=["company"])
app.include_router(jd.router, prefix="/jd", tags=["job_description"])

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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

@app.get("/components/{component_type}/{file_name}")
async def get_component(component_type: str, file_name: str):
    """Serve component templates"""
    return FileResponse(f'templates/{component_type}/{file_name}')

# Health check endpoint for Vercel
@app.get("/api/health")
async def health_check():
    """Health check endpoint for Vercel"""
    return {"status": "ok", "environment": settings.environment}

# This is only needed for local development, Vercel will use the app object directly
if __name__ == "__main__":
    # Get port from environment variable or use default 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Run server with host="0.0.0.0" to allow access from all network interfaces
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True,
        log_level="info"
    )
