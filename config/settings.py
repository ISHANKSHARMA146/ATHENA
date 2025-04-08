# config/settings.py
import os
from dotenv import load_dotenv

# Load variables from .env, but don't fail if file doesn't exist (for Vercel)
load_dotenv(verbose=False)

class Settings:
    # Firebase Backend Settings
    firebase_project_id: str = os.environ.get("FIREBASE_PROJECT_ID", "")
    firebase_service_account: str = os.environ.get("FIREBASE_SERVICE_ACCOUNT", "./firebase/service-account.json")

    # Firebase Frontend Settings
    firebase_api_key: str = os.environ.get("FIREBASE_API_KEY", "")
    firebase_auth_domain: str = os.environ.get("FIREBASE_AUTH_DOMAIN", "")
    firebase_project: str = os.environ.get("FIREBASE_PROJECT", "")
    firebase_storage_bucket: str = os.environ.get("FIREBASE_STORAGE_BUCKET", "")
    firebase_messaging_sender_id: str = os.environ.get("FIREBASE_MESSAGING_SENDER_ID", "")
    firebase_app_id: str = os.environ.get("FIREBASE_APP_ID", "")
    firebase_measurement_id: str = os.environ.get("FIREBASE_MEASUREMENT_ID", "")
    
    # Hasura Settings
    hasura_graphql_endpoint: str = os.environ.get("HASURA_GRAPHQL_ENDPOINT", "")
    hasura_admin_secret: str = os.environ.get("HASURA_ADMIN_SECRET", "")
    
    # Application Settings
    environment: str = os.environ.get("ENVIRONMENT", "development")
    app_port: int = int(os.environ.get("APP_PORT", 8000))
    
    # Check if running on Vercel
    is_vercel: bool = "VERCEL" in os.environ

settings = Settings()
