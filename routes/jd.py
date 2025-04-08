# routes/jd.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import hasura_service

router = APIRouter()

class JDInput(BaseModel):
    company_id: int
    title: str
    description: str

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
