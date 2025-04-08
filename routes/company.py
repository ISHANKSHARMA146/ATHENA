# routes/company.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import hasura_service

router = APIRouter()

class CompanyProfile(BaseModel):
    name: str
    address: str
    description: str = None
    user_id: str

class CompanyProfileUpdate(BaseModel):
    id: int
    name: str
    address: str
    description: str = None

@router.post("/create", tags=["Company Profile"])
async def create_company(profile: CompanyProfile):
    """
    Creates a company profile by inserting data into Hasura.
    """
    try:
        # Check if user already has a company
        existing_company = hasura_service.get_company_by_user_id(profile.user_id)
        if existing_company:
            raise HTTPException(status_code=400, detail="User already has a company profile")
            
        result = hasura_service.insert_company_profile(profile)
        return {"status": "success", "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create company profile: {e}")

@router.put("/update", tags=["Company Profile"])
async def update_company(profile: CompanyProfileUpdate):
    """
    Updates an existing company profile.
    """
    try:
        result = hasura_service.update_company_profile(profile)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update company profile: {e}")

@router.get("/user/{user_id}", tags=["Company Profile"])
async def get_user_company(user_id: str):
    """
    Retrieves a company profile for a specific user.
    """
    try:
        company = hasura_service.get_company_by_user_id(user_id)
        if not company:
            return {"status": "success", "data": None}
        return {"status": "success", "data": company}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve company profile: {e}")
