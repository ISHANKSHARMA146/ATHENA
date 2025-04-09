# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv(verbose=False)

# Base settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# API Keys and Services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

# Firebase Settings
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "firebase/service-account.json")

# Hasura Settings
HASURA_GRAPHQL_URL = os.getenv("HASURA_GRAPHQL_URL", "http://localhost:8080/v1/graphql")
HASURA_ADMIN_SECRET = os.getenv("HASURA_ADMIN_SECRET", "")

# File Upload Settings
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 5 * 1024 * 1024))  # 5MB by default
ALLOWED_UPLOAD_EXTENSIONS = [".pdf", ".docx", ".doc", ".jpg", ".jpeg", ".png"]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/athena.log")

class Config:
    """Configuration class for getting configuration values."""
    
    @staticmethod
    def get_openai_key():
        """Get OpenAI API key."""
        return OPENAI_API_KEY
    
    @staticmethod
    def get_openai_model():
        """Get OpenAI model name."""
        return OPENAI_MODEL
    
    @staticmethod
    def get_openai_embedding_model():
        """Get OpenAI embedding model name."""
        return OPENAI_EMBEDDING_MODEL
    
    @staticmethod
    def get_hasura_url():
        """Get Hasura GraphQL URL."""
        return HASURA_GRAPHQL_URL
    
    @staticmethod
    def get_hasura_admin_secret():
        """Get Hasura admin secret."""
        return HASURA_ADMIN_SECRET
    
    @staticmethod
    def get_firebase_credentials():
        """Get Firebase credentials file path."""
        return FIREBASE_CREDENTIALS

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
