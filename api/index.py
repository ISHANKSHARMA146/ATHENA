from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
import os
import pathlib

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get base directory (for resolving templates)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

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

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main index.html file"""
    try:
        index_path = os.path.join(TEMPLATES_DIR, "index.html")
        if os.path.exists(index_path) and os.path.isfile(index_path):
            return FileResponse(index_path)
        
        # Fallback content if file doesn't exist
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Athena API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                .links { margin-top: 20px; }
                .links a { display: block; margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <h1>Athena API</h1>
            <p>The API is running successfully. You can access:</p>
            <div class="links">
                <a href="/api/health">API Health Check</a>
                <a href="/api/debug">Environment Debug Info</a>
                <a href="/api/debug/templates">Templates Debug Info</a>
                <a href="/components/job/job-form.html">Job Form Template</a>
                <a href="/components/company/company-form.html">Company Form Template</a>
            </div>
        </body>
        </html>
        """)
    except Exception as e:
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Athena API - Error</title>
        </head>
        <body>
            <h1>Error Loading Template</h1>
            <p>There was an error loading the index template: {str(e)}</p>
            <p>The API is still running. Try accessing /api/health to check.</p>
        </body>
        </html>
        """, status_code=500)

@app.get("/templates/{path:path}")
async def serve_template(path: str):
    """Serve template files directly"""
    file_path = os.path.join(TEMPLATES_DIR, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return {"error": "Template not found"}

@app.get("/components/{component_type}/{file_name}")
async def get_component(component_type: str, file_name: str):
    """Serve component templates for backward compatibility"""
    try:
        file_path = os.path.join(TEMPLATES_DIR, component_type, file_name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return {"error": f"Template not found: {component_type}/{file_name}"}
    except Exception as e:
        return {"error": f"Error serving template: {str(e)}"}

@app.get("/api/debug/templates")
async def debug_templates():
    """Debug endpoint to check template paths and files"""
    try:
        templates_info = {
            "base_dir": BASE_DIR,
            "templates_dir": TEMPLATES_DIR,
            "templates_exists": os.path.exists(TEMPLATES_DIR),
            "templates_is_dir": os.path.isdir(TEMPLATES_DIR) if os.path.exists(TEMPLATES_DIR) else False,
            "available_templates": []
        }
        
        # List available templates if directory exists
        if templates_info["templates_exists"] and templates_info["templates_is_dir"]:
            for root, dirs, files in os.walk(TEMPLATES_DIR):
                rel_path = os.path.relpath(root, TEMPLATES_DIR)
                if rel_path == ".":
                    rel_path = ""
                for file in files:
                    file_path = os.path.join(rel_path, file) if rel_path else file
                    templates_info["available_templates"].append(file_path)
        
        return templates_info
    except Exception as e:
        return {"error": f"Error checking templates: {str(e)}"}

# Import routes at the bottom to avoid circular imports
from routes import auth, company, jd

app.include_router(auth.router, prefix="/auth")
app.include_router(company.router, prefix="/company")
app.include_router(jd.router, prefix="/jd") 