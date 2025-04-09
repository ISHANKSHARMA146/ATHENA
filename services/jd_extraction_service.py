from utils.file_parser import parse_pdf_or_docx
from services.gpt_service import GPTService
from config.settings import Config
from io import BytesIO
from utils.logger import Logger
from models.schemas import JobDescriptionSchema
from datetime import datetime

logger = Logger(__name__).get_logger()

class JobDescriptionExtractor:
    """
    Service for extracting structured information from job descriptions.
    """
    def __init__(self):
        """
        Initializes the Job Description Extractor with GPT integration.
        """
        logger.info("JobDescriptionExtractor initialized successfully.")
        self.gpt_service = GPTService()

    async def extract_job_description(self, file_buffer: BytesIO, filename: str):
        """
        Extracts structured information from a job description file.
        Args:
            file_buffer (BytesIO): The job description file buffer.
            filename (str): Name of the uploaded job description file.
        
        Returns:
            Dict containing structured job description data.
        """
        try:
            text = parse_pdf_or_docx(file_buffer, filename)
            today_date = datetime.now().strftime("%Y-%m-%d")

            # System Prompt
            system_prompt = f"""
            You are an AI model specialized in extracting structured job descriptions from documents. 
            Ensure accurate data extraction and return structured JSON output. 
            Today's date is {today_date}. Follow these rules:

            1. **Extract Fields**:
               - job_title: Extract the most relevant job title.
               - job_description: Provide a comprehensive summary of the full job description text, preserving key details.
               - industry_name: Extract the industry of the job (e.g., "Technology", "Healthcare", "Finance").
               - required_skills: Identify all explicitly mentioned skills and infer essential skills based on context.
               - min_work_experience: Extract minimum experience requirement in years (as a number).

            2. **Skill Extraction**:
               - Extract both technical and soft skills.
               - Include tools, technologies, programming languages, platforms and methodologies mentioned.
               - Structure as a list of specific skills, not general categories.

            3. **Work Experience Calculation**:
               - Ensure the experience field is formatted as a numeric value in years.
               - If a range is given, use the minimum value.
               - Infer experience if not explicitly stated using context clues (e.g., "senior" typically means 5+ years).
               - If no experience requirement is mentioned or implied, use 0.

            4. **Industry Identification**:
               - Be specific about the industry (e.g., "Healthcare Software" rather than just "Technology").
               - Look for context clues about the company's sector if not explicitly stated.

            5. **Formatting**:
               - Ensure structured JSON output with no missing fields.
               - Use clear, concise language.
            """

            # User Prompt
            user_prompt = f"""
            Extract structured job description details from the following text:

            {text}

            Ensure structured formatting, extract all key details, and infer missing information where applicable.
            """

            # Call GPT Service
            structured_data = await self.gpt_service.extract_with_prompts(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_schema=JobDescriptionSchema
            )

            return structured_data  

        except Exception as e:
            logger.error(f"Error extracting job description from file '{filename}': {str(e)}", exc_info=True)
            raise

    async def upload_job_description(self, file_buffer: BytesIO, filename: str):
        """
        Uploads and processes a job description file.
        Args:
            file_buffer (BytesIO): The job description file buffer.
            filename (str): Name of the uploaded job description file.
        
        Returns:
            Dict containing structured job description data.
        """
        try:
            extracted_data = await self.extract_job_description(file_buffer, filename)
            return {
                "status": "success",
                "data": extracted_data
            }
        except Exception as e:
            logger.error(f"Error uploading job description file '{filename}': {str(e)}", exc_info=True)
            raise 