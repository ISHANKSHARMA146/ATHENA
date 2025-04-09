# routes/jd.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from services import hasura_service
from services.jd_extraction_service import JobDescriptionExtractor
from services.jd_enhancement_service import JobDescriptionEnhancer
from io import BytesIO
import logging

logger = logging.getLogger(__name__)
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

# New models for JD extraction and enhancement
class ExtractedJD(BaseModel):
    job_title: str
    job_description: str
    industry_name: str
    required_skills: Optional[List[str]] = None
    min_work_experience: Optional[int] = None

class EnhancedJD(BaseModel):
    job_title: str
    industry_name: str
    role_summary: str
    responsibilities: List[str]
    required_skills: List[str]
    min_work_experience: Optional[int] = None
    key_metrics: List[str]

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

# JD Extraction and Enhancement Routes
@router.post("/extract", tags=["Job Description"])
async def extract_jd(file: UploadFile = File(...)):
    """
    Extract structured information from a job description file (PDF, DOCX, etc.).
    """
    try:
        # Read file content
        file_content = await file.read()
        file_buffer = BytesIO(file_content)
        
        # Extract job description
        extractor = JobDescriptionExtractor()
        result = await extractor.upload_job_description(file_buffer, file.filename)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract job description: {e}")

@router.post("/enhance", tags=["Job Description"])
async def enhance_jd(jd_data: ExtractedJD):
    """
    Enhance a job description with more structured and detailed information.
    """
    try:
        # Enhance job description
        enhancer = JobDescriptionEnhancer()
        result = await enhancer.process_job_description(jd_data.dict())
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enhance job description: {e}")

@router.post("/extract-and-enhance", tags=["Job Description"])
async def extract_and_enhance_jd(file: UploadFile = File(...)):
    """
    Extract and enhance a job description from a file in one step.
    """
    try:
        # Read file content
        file_content = await file.read()
        file_buffer = BytesIO(file_content)
        
        # Extract job description
        extractor = JobDescriptionExtractor()
        extraction_result = await extractor.extract_job_description(file_buffer, file.filename)
        
        # Enhance job description
        enhancer = JobDescriptionEnhancer()
        enhancement_result = await enhancer.process_job_description(extraction_result)
        
        return enhancement_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process job description: {e}")

@router.post("/submit-from-enhancement", tags=["Job Description"])
async def submit_enhanced_jd(enhanced_data: Dict[str, Any], company_id: int = Form(...)):
    """
    Submit a job description to Hasura from enhanced data.
    """
    try:
        # Get the job form data from the enhanced data
        job_form_data = enhanced_data.get("data", {}).get("job_form_data", {})
        
        # Add company_id to the data
        job_form_data["company_id"] = company_id
        
        # Create JDInput object
        jd_input = JDInput(**job_form_data)
        
        # Submit to Hasura
        result = hasura_service.insert_job_description(jd_input)
        
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit enhanced job description: {e}")
