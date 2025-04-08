# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

class Settings:
    # Firebase Backend Settings
    firebase_project_id: str = os.getenv("FIREBASE_PROJECT_ID")
    firebase_service_account: str = os.getenv("FIREBASE_SERVICE_ACCOUNT")

    # Firebase Frontend Settings (for reference)
    firebase_api_key: str = os.getenv("FIREBASE_API_KEY")
    firebase_auth_domain: str = os.getenv("FIREBASE_AUTH_DOMAIN")
    firebase_project: str = os.getenv("FIREBASE_PROJECT")
    firebase_storage_bucket: str = os.getenv("FIREBASE_STORAGE_BUCKET")
    firebase_messaging_sender_id: str = os.getenv("FIREBASE_MESSAGING_SENDER_ID")
    firebase_app_id: str = os.getenv("FIREBASE_APP_ID")
    firebase_measurement_id: str = os.getenv("FIREBASE_MEASUREMENT_ID")
    
    # Hasura Settings
    hasura_graphql_endpoint: str = os.getenv("HASURA_GRAPHQL_ENDPOINT")
    hasura_admin_secret: str = os.getenv("HASURA_ADMIN_SECRET")
    
    # Application Settings
    environment: str = os.getenv("ENVIRONMENT", "development")
    app_port: int = int(os.getenv("APP_PORT", 8000))

settings = Settings()
