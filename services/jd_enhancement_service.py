from services.gpt_service import GPTService
from utils.logger import Logger
from models.schemas import JobDescriptionSchema, EnhancedJobDescriptionSchema, JDFormData, EnhancementResult
from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

logger = Logger(__name__).get_logger()

class JDEnhancementInput(BaseModel):
    """Schema for the input to the JD enhancement service."""
    job_title: str
    job_description: str
    industry_name: str
    required_skills: List[str] = []
    min_work_experience: int = 0

class JobDescriptionEnhancer:
    """
    Service for enhancing job descriptions and mapping them to the job form fields.
    """
    def __init__(self):
        """
        Initializes the Job Description Enhancer with GPT integration.
        """
        logger.info("JobDescriptionEnhancer initialized successfully.")
        self.gpt_service = GPTService()

    async def enhance_job_description(self, jd_data: Dict[str, Any]):
        """
        Enhances a job description with more structured and detailed information.
        
        Args:
            jd_data (Dict[str, Any]): The extracted job description data.
            
        Returns:
            Dict containing enhanced job description data.
        """
        try:
            # Convert input to expected format if needed
            if not isinstance(jd_data, JDEnhancementInput):
                jd_data = JDEnhancementInput(
                    job_title=jd_data.get("job_title", ""),
                    job_description=jd_data.get("job_description", ""),
                    industry_name=jd_data.get("industry_name", ""),
                    required_skills=jd_data.get("required_skills", []),
                    min_work_experience=jd_data.get("min_work_experience", 0)
                )

            today_date = datetime.now().strftime("%Y-%m-%d")

            # System Prompt
            system_prompt = f"""
            You are an AI expert specializing in job description enhancement for the recruiting industry.
            Your task is to transform basic job descriptions into comprehensive, well-structured descriptions
            that align with industry standards and best practices. Today's date is {today_date}.
            
            **Required Output Fields**:
            - job_title: The enhanced job title (string)
            - industry_name: The industry of the job (string, EXACTLY as provided in input)
            - role_summary: Detailed description of the role (string)
            - responsibilities: List of job responsibilities (array of strings)
            - required_skills: List of required skills (array of strings)
            - performance_indicators: Measurable KPIs for the role (array of strings)
            - min_work_experience: Minimum years of experience required (number)
            
            **Enhancement Guidelines**:
            
            1. **Job Details Expansion**:
               - Create a detailed role_summary (250-300 words) that explains the position's purpose and impact
               - Expand responsibilities to at least 10 clear, specific duties
               - Define at least 10 measurable performance_indicators for the role
               - Identify decision_making authority and stakeholder_interactions
            
            2. **Skills Classification**:
               - Preserve ALL required_skills from the input and expand the list
               - Additionally categorize skills into:
                 * hard_skills (technical abilities)
                 * soft_skills (interpersonal abilities)
                 * domain_expertise (industry knowledge)
                 * methodologies (frameworks, approaches)
                 * languages (programming or spoken)
            
            3. **Qualification Details**:
               - Specify required_qualifications and preferred_qualifications as detailed strings
               - Note any mandatory_certifications, clearances, or legal requirements
            
            4. **Work Environment**:
               - Specify work_model (remote, hybrid, on-site)
               - Include work_locations, travel_requirements if applicable
            
            IMPORTANT: Always preserve the exact industry_name provided in the input.
            """

            # User Prompt
            user_prompt = f"""
            Please enhance this job description with comprehensive details while maintaining accuracy.
            Your response MUST include all required fields in the exact format specified.

            Job Title: {jd_data.job_title}
            Industry Name: {jd_data.industry_name}
            Minimum Experience: {jd_data.min_work_experience} years
            
            Job Description:
            {jd_data.job_description}
            
            Required Skills:
            {', '.join(jd_data.required_skills) if jd_data.required_skills else "Not specified"}
            
            Transform this into a comprehensive, well-structured job description following the guidelines.
            Include all required fields in your JSON response.
            """

            # Call GPT Service
            enhanced_data = await self.gpt_service.extract_with_prompts(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_schema=EnhancedJobDescriptionSchema
            )

            return enhanced_data

        except Exception as e:
            logger.error(f"Error enhancing job description: {str(e)}", exc_info=True)
            raise

    def map_to_job_form(self, enhanced_jd: Dict[str, Any]) -> JDFormData:
        """
        Maps the enhanced job description to the job form fields.
        
        Args:
            enhanced_jd (Dict[str, Any]): The enhanced job description data.
            
        Returns:
            JDFormData: Job form data ready for submission to Hasura.
        """
        try:
            # Initialize the job form data with the title
            job_form_data = {
                "title": enhanced_jd.get("job_title", ""),
                "job_code": enhanced_jd.get("job_code", ""),
                "job_level": enhanced_jd.get("job_level", ""),
                "department": enhanced_jd.get("department", ""),
                "job_function": enhanced_jd.get("job_function", ""),
                
                # Job Posting Metadata
                "contract_duration": enhanced_jd.get("contract_duration", ""),
                "time_commitment": enhanced_jd.get("time_commitment", ""),
                
                # Detailed Role Description
                "job_summary": enhanced_jd.get("role_summary", ""),
                "day_to_day_tasks": "\n".join(enhanced_jd.get("responsibilities", [])),
                "performance_indicators": "\n".join(enhanced_jd.get("performance_indicators", [])),
                "decision_making": enhanced_jd.get("decision_making", ""),
                "stakeholder_interactions": enhanced_jd.get("stakeholder_interactions", ""),
                
                # Requirements Breakdown
                "required_qualifications": enhanced_jd.get("required_qualifications", ""),
                "preferred_qualifications": enhanced_jd.get("preferred_qualifications", ""),
                "mandatory_certifications": enhanced_jd.get("mandatory_certifications", ""),
                "legal_eligibility": enhanced_jd.get("legal_eligibility", ""),
                "background_checks": enhanced_jd.get("background_checks", ""),
                "clearance_level": enhanced_jd.get("clearance_level", ""),
                
                # Skills Classification - convert lists to newline-separated strings if needed
                "hard_skills": "\n".join(enhanced_jd.get("hard_skills", [])) if isinstance(enhanced_jd.get("hard_skills"), list) else enhanced_jd.get("hard_skills", ""),
                "soft_skills": "\n".join(enhanced_jd.get("soft_skills", [])) if isinstance(enhanced_jd.get("soft_skills"), list) else enhanced_jd.get("soft_skills", ""),
                "domain_expertise": "\n".join(enhanced_jd.get("domain_expertise", [])) if isinstance(enhanced_jd.get("domain_expertise"), list) else enhanced_jd.get("domain_expertise", ""),
                "methodologies": "\n".join(enhanced_jd.get("methodologies", [])) if isinstance(enhanced_jd.get("methodologies"), list) else enhanced_jd.get("methodologies", ""),
                "languages": "\n".join(enhanced_jd.get("languages", [])) if isinstance(enhanced_jd.get("languages"), list) else enhanced_jd.get("languages", ""),
                "skills_priority": enhanced_jd.get("skills_priority", ""),
                
                # Compensation Details
                "base_salary": enhanced_jd.get("base_salary", ""),
                "bonus_structure": enhanced_jd.get("bonus_structure", ""),
                "equity_options": enhanced_jd.get("equity_options", ""),
                "benefits": enhanced_jd.get("benefits", ""),
                "relocation_assistance": enhanced_jd.get("relocation_assistance", ""),
                "visa_sponsorship": enhanced_jd.get("visa_sponsorship", ""),
                
                # Work Environment
                "work_model": enhanced_jd.get("work_model", ""),
                "work_locations": enhanced_jd.get("work_locations", ""),
                "travel_requirements": enhanced_jd.get("travel_requirements", ""),
                "shift_type": enhanced_jd.get("shift_type", ""),
                
                # Career Path Info
                "growth_opportunities": enhanced_jd.get("growth_opportunities", ""),
                "training_development": enhanced_jd.get("training_development", ""),
                "mentorship": enhanced_jd.get("mentorship", ""),
                "succession_planning": enhanced_jd.get("succession_planning", ""),
                "culture_page_link": enhanced_jd.get("culture_page_link", ""),
                "careers_page_link": enhanced_jd.get("careers_page_link", "")
            }
            
            # Additional processing for work experience if available
            min_experience = enhanced_jd.get("min_work_experience", 0)
            if min_experience > 0 and not job_form_data["required_qualifications"]:
                job_form_data["required_qualifications"] = f"Minimum {min_experience} years of relevant experience"

            # If job title is not set but we have it from the enhanced JD
            if not job_form_data["title"] and enhanced_jd.get("job_title"):
                job_form_data["title"] = enhanced_jd["job_title"]
                
            # Create validated JDFormData object
            validated_form_data = JDFormData(**job_form_data)
            return validated_form_data

        except Exception as e:
            logger.error(f"Error mapping to job form: {str(e)}", exc_info=True)
            raise

    async def process_job_description(self, jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete process to enhance a job description and map it to the job form.
        
        Args:
            jd_data (Dict[str, Any]): The extracted job description data.
            
        Returns:
            Dict containing job form data ready for Hasura submission.
        """
        try:
            # Enhance the job description
            enhanced_jd = await self.enhance_job_description(jd_data)
            
            # Map to job form fields
            job_form_data = self.map_to_job_form(enhanced_jd)
            
            # Create enhancement result
            result = EnhancementResult(
                enhanced_jd=enhanced_jd,
                job_form_data=job_form_data
            )
            
            return {
                "status": "success",
                "data": result.dict()
            }
        except Exception as e:
            logger.error(f"Error processing job description: {str(e)}", exc_info=True)
            raise 