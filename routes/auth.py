# routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json

router = APIRouter()

class TokenVerificationRequest(BaseModel):
    id_token: str

@router.post("/verify", tags=["Authentication"])
async def verify_token(token_req: TokenVerificationRequest):
    """
    Verifies the Firebase ID token and returns the corresponding user info.
    """
    try:
        # Import firebase_admin here to avoid initialization issues on Vercel
        import firebase_admin
        from firebase_admin import auth as firebase_auth
        
        # Ensure firebase is initialized
        if not firebase_admin._apps:
            from firebase_admin import credentials
            
            # Check if running on Vercel with environment variable
            if os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON'):
                try:
                    service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON'))
                    cred = credentials.Certificate(service_account_info)
                    firebase_admin.initialize_app(cred)
                except Exception as e:
                    return {"error": f"Firebase initialization failed: {str(e)}"}
            else:
                # Fallback to local file
                try:
                    service_account_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT', './firebase/service-account.json')
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                except Exception as e:
                    return {"error": f"Local Firebase initialization failed: {str(e)}"}
        
        # Now verify the token
        decoded_token = firebase_auth.verify_id_token(token_req.id_token)
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "claims": decoded_token
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Firebase ID token: {str(e)}")
