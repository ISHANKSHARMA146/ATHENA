# routes/company.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from services import hasura_service

router = APIRouter()

# Company Profile Input Model
class CompanyProfile(BaseModel):
    # Required fields
    user_id: str
    name: str
    
    # Company Identity - optional fields
    overview: Optional[str] = None
    industry: Optional[str] = None
    year_founded: Optional[int] = None
    headquarters_location: Optional[str] = None
    global_presence: Optional[str] = None
    company_size: Optional[str] = None
    ownership_type: Optional[str] = None
    company_type: Optional[str] = None
    products_services: Optional[str] = None
    specialties: Optional[str] = None
    growth_stage: Optional[str] = None
    key_markets: Optional[str] = None
    
    # Leadership & Team
    founders: Optional[str] = None
    leadership_team: Optional[str] = None
    board_members: Optional[str] = None
    team_composition: Optional[str] = None
    
    # Culture & Brand
    work_culture: Optional[str] = None
    dei_statement: Optional[str] = None
    sustainability_initiatives: Optional[str] = None
    awards: Optional[str] = None
    milestones: Optional[str] = None
    media_mentions: Optional[str] = None
    success_stories: Optional[str] = None
    unique_differentiators: Optional[str] = None
    brand_voice: Optional[str] = None
    employer_brand_sentiment: Optional[str] = None
    
    # Hiring & Operations
    hiring_volumes: Optional[str] = None
    company_languages: Optional[str] = None
    workplace_model: Optional[str] = None
    hiring_regions: Optional[str] = None
    
    # Web Presence & Links
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    careers_page_url: Optional[str] = None
    social_media_links: Optional[str] = None
    employer_review_links: Optional[str] = None

class CompanyProfileUpdate(CompanyProfile):
    id: int
    user_id: Optional[str] = None  # Make user_id optional for updates

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
