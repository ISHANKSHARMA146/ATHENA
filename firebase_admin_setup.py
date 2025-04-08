# firebase_admin_setup.py
import os
import firebase_admin
from firebase_admin import credentials
from config.settings import settings

def initialize_firebase():
    if not firebase_admin._apps:  # Initialize only once
        # Resolve the relative path based on the directory of this file (project root)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        service_account_path = os.path.join(base_dir, settings.firebase_service_account)
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {
            "projectId": settings.firebase_project_id,
        })

initialize_firebase()
