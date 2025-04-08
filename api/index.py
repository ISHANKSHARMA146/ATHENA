from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}

@app.get("/api/debug")
async def debug_info():
    """Debug endpoint to check environment variables"""
    env_vars = {}
    # Add safe environment variables (don't include secrets)
    for key in ["VERCEL", "VERCEL_ENV", "VERCEL_URL", "VERCEL_REGION", 
                "FIREBASE_PROJECT_ID", "ENVIRONMENT"]:
        env_vars[key] = os.environ.get(key, "Not set")
        
    # Check if Firebase service account is set
    env_vars["FIREBASE_SERVICE_ACCOUNT_JSON_SET"] = "Yes" if os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON") else "No"
    
    return {
        "environment": env_vars,
        "message": "Debug information"
    }

@app.get("/api/config/firebase")
async def get_firebase_config():
    """Securely serve Firebase configuration"""
    return {
        "apiKey": os.environ.get("FIREBASE_API_KEY", ""),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.environ.get("FIREBASE_PROJECT", ""),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": os.environ.get("FIREBASE_APP_ID", ""),
        "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID", "")
    }

@app.get("/")
async def root():
    return {"message": "Welcome to Athena API"}

# Import routes at the bottom to avoid circular imports
from routes import auth, company, jd

app.include_router(auth.router, prefix="/auth")
app.include_router(company.router, prefix="/company")
app.include_router(jd.router, prefix="/jd") 