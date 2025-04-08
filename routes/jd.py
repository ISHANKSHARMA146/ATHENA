# routes/jd.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services import hasura_service

router = APIRouter()

class JDInput(BaseModel):
    # Required fields
    company_id: int
    title: str
    
    # Basic Job Info - optional fields
    job_code: Optional[str] = None
    job_level: Optional[str] = None
    department: Optional[str] = None
    job_function: Optional[str] = None
    
    # Job Posting Metadata
    contract_duration: Optional[str] = None
    time_commitment: Optional[str] = None
    
    # Detailed Role Description
    job_summary: Optional[str] = None
    day_to_day_tasks: Optional[str] = None
    performance_indicators: Optional[str] = None
    decision_making: Optional[str] = None
    stakeholder_interactions: Optional[str] = None
    
    # Requirements Breakdown
    required_qualifications: Optional[str] = None
    preferred_qualifications: Optional[str] = None
    mandatory_certifications: Optional[str] = None
    legal_eligibility: Optional[str] = None
    background_checks: Optional[str] = None
    clearance_level: Optional[str] = None
    
    # Skills Classification
    hard_skills: Optional[str] = None
    soft_skills: Optional[str] = None
    domain_expertise: Optional[str] = None
    methodologies: Optional[str] = None
    languages: Optional[str] = None
    skills_priority: Optional[str] = None
    
    # Compensation Details
    base_salary: Optional[str] = None
    bonus_structure: Optional[str] = None
    equity_options: Optional[str] = None
    benefits: Optional[str] = None
    relocation_assistance: Optional[str] = None
    visa_sponsorship: Optional[str] = None
    
    # Work Environment
    work_model: Optional[str] = None
    work_locations: Optional[str] = None
    travel_requirements: Optional[str] = None
    shift_type: Optional[str] = None
    
    # Career Path Info
    growth_opportunities: Optional[str] = None
    training_development: Optional[str] = None
    mentorship: Optional[str] = None
    succession_planning: Optional[str] = None
    culture_page_link: Optional[str] = None
    careers_page_link: Optional[str] = None

@router.post("/submit", tags=["Job Description"])
async def submit_jd(jd: JDInput):
    """
    Submits a job description for a specific company.
    """
    try:
        result = hasura_service.insert_job_description(jd)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit job description: {e}")

@router.get("/company/{company_id}", tags=["Job Description"])
async def get_company_jobs(company_id: int):
    """
    Retrieves all job descriptions for a specific company.
    """
    try:
        jobs = hasura_service.get_company_jobs(company_id)
        return {"status": "success", "data": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve job descriptions: {e}")
