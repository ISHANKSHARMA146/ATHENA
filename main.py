# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routes import auth, company, jd
from config.settings import settings
import firebase_admin_setup  # This ensures Firebase is initialized

app = FastAPI(title="Athena - Firebase + Hasura Integration")

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

# Include routers with prefixes
app.include_router(auth.router, prefix="/auth")
app.include_router(company.router, prefix="/company")
app.include_router(jd.router, prefix="/jd")

@app.get("/")
async def read_root():
    return FileResponse('templates/index.html')

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.app_port, reload=True)
