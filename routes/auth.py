# routes/auth.py
from fastapi import APIRouter, HTTPException
from firebase_admin import auth as firebase_auth
from pydantic import BaseModel

router = APIRouter()

class TokenVerificationRequest(BaseModel):
    id_token: str

@router.post("/verify", tags=["Authentication"])
async def verify_token(token_req: TokenVerificationRequest):
    """
    Verifies the Firebase ID token and returns the corresponding user info.
    """
    try:
        decoded_token = firebase_auth.verify_id_token(token_req.id_token)
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "claims": decoded_token
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase ID token")
