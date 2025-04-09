from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

# Basic JD schema for extraction
class JobDescriptionSchema(BaseModel):
    job_title: str = Field(..., description="Job title for the position")
    job_description: str = Field(..., description="Full job description text without any contextual loss")
    industry_name: str = Field(..., description="Job industry of the job finances, technological, civil, healthcare, etc.")
    required_skills: Optional[List[str]] = Field(None, description="List of required skills for the job")
    min_work_experience: Optional[int] = Field(None, description="Minimum work experience required for the job in years")

# Enhanced JD schema aligned with our form structure
class EnhancedJobDescriptionSchema(BaseModel):
    # Basic Information
    job_title: str = Field(..., description="Enhanced job title for better clarity")
    job_code: Optional[str] = Field(None, description="Job code or requisition ID")
    job_level: Optional[str] = Field(None, description="Job level or internal grading")
    department: Optional[str] = Field(None, description="Department or business unit")
    job_function: Optional[str] = Field(None, description="Function or job category")
    
    # Industry Information
    industry_name: str = Field(..., description="Job industry e.g. Technology, Healthcare, Finance", alias="industry")
    
    # Job Posting Metadata
    contract_duration: Optional[str] = Field(None, description="Duration of contract if applicable")
    time_commitment: Optional[str] = Field(None, description="Time commitment e.g. Full-time, Part-time")
    
    # Detailed Role Description
    role_summary: str = Field(..., description="Expanded overview of the role including purpose and impact", alias="summary")
    responsibilities: List[str] = Field(..., description="List of at least 10 responsibilities for the job", alias="duties")
    performance_indicators: List[str] = Field(..., description="List of KPIs or performance measurement criteria", 
                                            alias="key_metrics")
    decision_making: Optional[str] = Field(None, description="Decision-making authority in the role", 
                                        alias="decision_making_authority")
    stakeholder_interactions: Optional[str] = Field(None, description="Key stakeholders the role interacts with", 
                                                  alias="key_stakeholders")
    
    # Requirements Breakdown
    required_skills: List[str] = Field(..., description="List of required skills for the job", alias="skills")
    required_qualifications: Optional[str] = Field(None, description="Required qualifications for the role", 
                                                 alias="qualifications")
    preferred_qualifications: Optional[str] = Field(None, description="Preferred qualifications for the role", 
                                                  alias="preferred")
    mandatory_certifications: Optional[str] = Field(None, description="Mandatory certifications required", 
                                                  alias="certifications")
    legal_eligibility: Optional[str] = Field(None, description="Legal requirements for eligibility")
    background_checks: Optional[str] = Field(None, description="Required background checks")
    clearance_level: Optional[str] = Field(None, description="Required security clearance level")
    
    # Skills Classification
    hard_skills: Optional[List[str]] = Field(None, description="Technical skills required", 
                                           alias="technical_skills")
    soft_skills: Optional[List[str]] = Field(None, description="Interpersonal skills required", 
                                           alias="interpersonal_skills")
    domain_expertise: Optional[List[str]] = Field(None, description="Domain knowledge required", 
                                                alias="domain_knowledge")
    methodologies: Optional[List[str]] = Field(None, description="Methodologies the candidate should know")
    languages: Optional[List[str]] = Field(None, description="Programming or spoken languages required")
    skills_priority: Optional[List[str]] = Field(None, description="Priority ranking of required skills")
    
    # Experience Information
    min_work_experience: Optional[int] = Field(None, description="Minimum work experience required in years", 
                                             alias="experience")
    
    # Compensation Details
    base_salary: Optional[str] = Field(None, description="Base salary range", 
                                     alias="compensation")
    bonus_structure: Optional[str] = Field(None, description="Bonus or commission details", 
                                         alias="bonuses")
    equity_options: Optional[str] = Field(None, description="Equity or stock options")
    benefits: Optional[str] = Field(None, description="Benefits package details")
    relocation_assistance: Optional[str] = Field(None, description="Relocation assistance available", 
                                               alias="relocation")
    visa_sponsorship: Optional[str] = Field(None, description="Visa sponsorship availability", 
                                          alias="visa")
    
    # Work Environment
    work_model: Optional[str] = Field(None, description="Work model e.g. Remote, Hybrid, On-site", 
                                    alias="work_environment")
    work_locations: Optional[str] = Field(None, description="Potential work locations", 
                                        alias="locations")
    travel_requirements: Optional[str] = Field(None, description="Required travel percentage", 
                                             alias="travel")
    shift_type: Optional[str] = Field(None, description="Type of shift e.g. Regular, Night shift", 
                                    alias="shifts")
    
    # Career Path Info
    growth_opportunities: Optional[str] = Field(None, description="Career growth possibilities", 
                                              alias="career_development")
    training_development: Optional[str] = Field(None, description="Training and development programs", 
                                              alias="training")
    mentorship: Optional[str] = Field(None, description="Mentorship opportunities")
    succession_planning: Optional[str] = Field(None, description="Succession planning details")
    culture_page_link: Optional[str] = Field(None, description="Link to company culture page")
    careers_page_link: Optional[str] = Field(None, description="Link to company careers page")
    
    class Config:
        populate_by_name = True  # Allow population from aliases

# Mapped JD Form Data (matches exactly with our JDInput class in routes/jd.py)
class JDFormData(BaseModel):
    # Required fields
    company_id: Optional[int] = Field(None, description="Company ID")
    title: str = Field(..., description="Job title")
    
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
    skills_priority: Optional[Union[str, List[str]]] = None
    
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

# Enhancement Result
class EnhancementResult(BaseModel):
    enhanced_jd: EnhancedJobDescriptionSchema
    job_form_data: JDFormData 