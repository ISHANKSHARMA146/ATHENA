import os
import json
import firebase_admin
from firebase_admin import credentials

def initialize_firebase_for_vercel():
    """Initialize Firebase with credentials from environment variables for Vercel deployment"""
    if not firebase_admin._apps:
        # Check if running on Vercel and using environment variable for service account
        if os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON'):
            # Parse the JSON string from environment variable
            service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON'))
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred, {
                "projectId": os.environ.get('FIREBASE_PROJECT_ID'),
            })
        else:
            # Fallback to local file if not on Vercel
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            service_account_path = os.path.join(base_dir, os.environ.get('FIREBASE_SERVICE_ACCOUNT', './firebase/service-account.json'))
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred, {
                "projectId": os.environ.get('FIREBASE_PROJECT_ID'),
            }) 