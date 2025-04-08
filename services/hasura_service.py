# services/hasura_service.py
import requests
from config.settings import settings
from pydantic import BaseModel
from typing import Optional

class CompanyProfileModel(BaseModel):
    id: Optional[int] = None
    user_id: str
    
    # Company Identity
    name: str
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

class JobDescriptionModel(BaseModel):
    id: Optional[int] = None
    company_id: int
    
    # Basic Job Info
    title: str
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

def execute_graphql(query: str, variables: dict = None):
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": settings.hasura_admin_secret
    }
    
    # Add better error handling
    try:
        response = requests.post(
            settings.hasura_graphql_endpoint,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=10  # Add timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Hasura GraphQL request failed: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid JSON response from Hasura: {str(e)}")
    except Exception as e:
        raise Exception(f"Error executing GraphQL query: {str(e)}")

def insert_company_profile(profile):
    # Build the dynamic fields for the query
    fields = []
    variables = {}
    
    # Process all fields from the profile model
    for key, value in profile.dict().items():
        if key != "id" and value is not None:  # Skip id and None values
            fields.append(f"{key}: ${key}")
            variables[key] = value
    
    # Build the GraphQL mutation
    query = f"""
    mutation ({', '.join(f"${key}: {get_gql_type(key, value)}" for key, value in variables.items())}) {{
      insert_company_profiles(objects: {{{', '.join(fields)}}}) {{
        returning {{
          id
          user_id
          name
          # Include other fields as needed
        }}
      }}
    }}
    """
    
    result = execute_graphql(query, variables)
    try:
        data = result["data"]["insert_company_profiles"]["returning"][0]
        return CompanyProfileModel(**data)
    except (KeyError, IndexError) as e:
        raise Exception("Error parsing response from Hasura") from e

def update_company_profile(profile):
    # Extract the id for pk_columns
    profile_id = profile.id
    
    # Build the dynamic fields for _set
    set_fields = {}
    
    # Process all fields from the profile model
    for key, value in profile.dict().items():
        if key != "id" and value is not None:  # Skip id and None values
            set_fields[key] = value
    
    # Build the GraphQL mutation
    query = """
    mutation ($id: Int!, $set_fields: company_profiles_set_input!) {
      update_company_profiles_by_pk(
        pk_columns: {id: $id}, 
        _set: $set_fields
      ) {
        id
        user_id
        name
        # Include other fields as needed
      }
    }
    """
    
    variables = {
        "id": profile_id,
        "set_fields": set_fields
    }
    
    result = execute_graphql(query, variables)
    try:
        data = result["data"]["update_company_profiles_by_pk"]
        return CompanyProfileModel(**data)
    except (KeyError, IndexError) as e:
        raise Exception("Error parsing response from Hasura") from e

def get_company_by_user_id(user_id: str):
    query = """
    query ($user_id: String!) {
      company_profiles(where: {user_id: {_eq: $user_id}}) {
        id
        user_id
        name
        # Include other fields you want to retrieve
      }
    }
    """
    variables = {
        "user_id": user_id
    }
    result = execute_graphql(query, variables)
    try:
        companies = result["data"]["company_profiles"]
        if not companies:
            return None
        return CompanyProfileModel(**companies[0])
    except (KeyError, IndexError) as e:
        raise Exception("Error parsing response from Hasura") from e

def insert_job_description(jd):
    # Build the dynamic fields for the query
    fields = []
    variables = {}
    
    # Process all fields from the jd model
    for key, value in jd.dict().items():
        if key != "id" and value is not None:  # Skip id and None values
            fields.append(f"{key}: ${key}")
            variables[key] = value
    
    # Build the GraphQL mutation
    query = f"""
    mutation ({', '.join(f"${key}: {get_gql_type(key, value)}" for key, value in variables.items())}) {{
      insert_job_descriptions(objects: {{{', '.join(fields)}}}) {{
        returning {{
          id
          company_id
          title
          # Include other fields as needed
        }}
      }}
    }}
    """
    
    result = execute_graphql(query, variables)
    try:
        data = result["data"]["insert_job_descriptions"]["returning"][0]
        return JobDescriptionModel(**data)
    except (KeyError, IndexError) as e:
        raise Exception("Error parsing response from Hasura") from e

def get_company_jobs(company_id: int):
    query = """
    query ($company_id: Int!) {
      job_descriptions(where: {company_id: {_eq: $company_id}}) {
        id
        company_id
        title
        # Include other fields you want to retrieve
      }
    }
    """
    variables = {
        "company_id": company_id
    }
    result = execute_graphql(query, variables)
    try:
        jobs = result["data"]["job_descriptions"]
        return [JobDescriptionModel(**job) for job in jobs]
    except (KeyError, IndexError) as e:
        raise Exception("Error parsing response from Hasura") from e

# Helper function to determine GraphQL type from Python type
def get_gql_type(key, value):
    if key == "company_id" or key == "id" or key == "year_founded":
        return "Int!"
    if isinstance(value, bool):
        return "Boolean!"
    return "String!"
