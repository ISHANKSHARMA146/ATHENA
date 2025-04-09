from openai import OpenAI
from utils.logger import Logger
from config.settings import Config
from typing import Dict, Any, List
import json
import re

# Initialize Logger
logger = Logger(__name__).get_logger()

class GPTService:
    """
    Service for interacting with OpenAI's API to process job descriptions.
    """
    def __init__(self):
        """
        Initializes the GPT service with the OpenAI API key.
        """
        try:
            config = Config()
            self.openai_client = OpenAI(api_key=config.get_openai_key())
            self.model = config.get_openai_model()
            self.embedding_model = config.get_openai_embedding_model()
            logger.info("GPT service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize GPT service: {str(e)}", exc_info=True)
            raise

    def camel_to_snake(self, camel_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert dictionary keys from camelCase to snake_case.
        
        Args:
            camel_dict (Dict[str, Any]): Dictionary with camelCase keys
            
        Returns:
            Dict[str, Any]: Dictionary with snake_case keys
        """
        snake_dict = {}
        for key, value in camel_dict.items():
            # Convert camelCase to snake_case
            snake_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            
            # If value is a dict, recursively convert its keys too
            if isinstance(value, dict):
                value = self.camel_to_snake(value)
            # If value is a list of dicts, convert each dict
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                value = [self.camel_to_snake(item) if isinstance(item, dict) else item for item in value]
                
            snake_dict[snake_key] = value
            
        return snake_dict

    async def extract_with_prompts(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Any
    ) -> Dict[str, Any]:
        """
        Extract structured information using GPT with custom prompts and schema.
        
        Args:
            system_prompt (str): System-level instructions for GPT.
            user_prompt (str): User-specific query for GPT processing.
            response_schema (Any): Expected schema for the response.

        Returns:
            Dict containing extracted structured information.
        """
        try:
            # Get the expected field names from the schema
            expected_fields = list(response_schema.__annotations__.keys())
            logger.info(f"Expected fields from schema: {expected_fields}")
            
            # Add specific schema examples and instructions
            schema_info = f"""
            IMPORTANT: Use snake_case for all field names in your JSON response.
            For example, use 'job_title' not 'jobTitle', 'role_summary' not 'roleSummary'.
            
            Your JSON response MUST include these exact field names:
            {', '.join(expected_fields)}
            
            For list fields such as 'required_skills', use array format like:
            "required_skills": ["Python", "JavaScript", "SQL"]
            
            For string fields, use simple strings, not arrays.
            """
            
            # Construct the messages - ensure "json" is mentioned to comply with OpenAI requirements
            messages = [
                {"role": "system", "content": f"{system_prompt}\n\n{schema_info}\n\nEnsure response follows the schema and is formatted as JSON."},
                {"role": "user", "content": f"{user_prompt}\n\nPlease return your response as JSON with snake_case field names (using underscores, not camelCase)."}
            ]
            
            logger.info(f"Sending request to GPT with model: {self.model}")
            
            # Make GPT API call
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=4000
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            parsed_response = json.loads(content)
            
            # Log raw response for debugging
            logger.info(f"Raw response keys: {list(parsed_response.keys())}")
            
            # Convert camelCase keys to snake_case
            normalized_response = self.camel_to_snake(parsed_response)
            
            # Fix key mappings: map known alternative fields to expected fields
            field_mappings = {
                "industry": "industry_name",
                "qualifications": "required_qualifications",
                "key_stakeholders": "stakeholder_interactions",
                "decision_making_authority": "decision_making",
                "certifications": "mandatory_certifications",
                "kpis": "performance_indicators",
                "key_metrics": "performance_indicators",
                "work_environment": "work_model",
                "career_development": "growth_opportunities",
                "compensation_framework": "base_salary"
            }
            
            # Apply field mappings
            for alt_key, expected_key in field_mappings.items():
                if alt_key in normalized_response and expected_key not in normalized_response:
                    normalized_response[expected_key] = normalized_response[alt_key]
            
            # Handle list-to-string conversions for specific fields
            list_to_string_fields = [
                "required_qualifications", "preferred_qualifications", 
                "mandatory_certifications", "legal_eligibility"
            ]
            
            for field in list_to_string_fields:
                if field in normalized_response and isinstance(normalized_response[field], list):
                    # Convert list to string with items separated by newlines
                    normalized_response[field] = "\n".join(normalized_response[field])
                    
            # Ensure skills_priority is a list
            if "skills_priority" in normalized_response and isinstance(normalized_response["skills_priority"], str):
                # If it's a string, try to split it into a list
                normalized_response["skills_priority"] = [s.strip() for s in normalized_response["skills_priority"].split(',')]
            
            # Extract required skills from the expanded skills sections if needed
            if "required_skills" not in normalized_response and "hard_skills" in normalized_response:
                # Combine hard skills and soft skills if available
                hard_skills = normalized_response.get("hard_skills", [])
                soft_skills = normalized_response.get("soft_skills", [])
                
                if isinstance(hard_skills, list) and isinstance(soft_skills, list):
                    normalized_response["required_skills"] = hard_skills + soft_skills
                elif isinstance(hard_skills, list):
                    normalized_response["required_skills"] = hard_skills
                elif isinstance(soft_skills, list):
                    normalized_response["required_skills"] = soft_skills
                else:
                    # Default to empty list
                    normalized_response["required_skills"] = []
            
            # Log the transformed response for debugging
            logger.info(f"Normalized response keys: {list(normalized_response.keys())}")
            
            # Validate against the schema
            try:
                validated_data = response_schema(**normalized_response)
                return validated_data.dict()
            except Exception as validation_error:
                # Log details about the validation error
                logger.error(f"Validation error: {str(validation_error)}")
                logger.error(f"Received fields: {list(normalized_response.keys())}")
                logger.error(f"Expected fields: {expected_fields}")
                
                # Add missing required fields with default values as a last resort
                for field in expected_fields:
                    if field not in normalized_response:
                        field_type = response_schema.__annotations__[field]
                        if "Optional" not in str(field_type):
                            # This is a required field
                            if "List" in str(field_type):
                                normalized_response[field] = []
                            elif "str" in str(field_type):
                                normalized_response[field] = "Not specified"
                            elif "int" in str(field_type):
                                normalized_response[field] = 0
                
                # Try validation again with fixed fields
                validated_data = response_schema(**normalized_response)
                return validated_data.dict()

        except Exception as e:
            logger.error(f"GPT extraction failed: {str(e)}", exc_info=True)
            raise Exception(f"GPT extraction failed: {str(e)}")