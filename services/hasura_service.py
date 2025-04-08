# services/hasura_service.py
import requests
from config.settings import settings
from pydantic import BaseModel

class CompanyProfileModel(BaseModel):
    id: int = None
    user_id: str
    name: str
    address: str
    description: str = None

class JobDescriptionModel(BaseModel):
    id: int = None
    company_id: int
    title: str
    description: str

def execute_graphql(query: str, variables: dict = None):
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": settings.hasura_admin_secret
    }
    response = requests.post(
        settings.hasura_graphql_endpoint,
        json={"query": query, "variables": variables},
        headers=headers
    )
    response.raise_for_status()
    return response.json()

def insert_company_profile(profile):
    query = """
    mutation ($user_id: String!, $name: String!, $address: String!, $description: String) {
      insert_company_profiles(objects: {user_id: $user_id, name: $name, address: $address, description: $description}) {
        returning {
          id
          user_id
          name
          address
          description
        }
      }
    }
    """
    variables = {
        "user_id": profile.user_id,
        "name": profile.name,
        "address": profile.address,
        "description": profile.description
    }
    result = execute_graphql(query, variables)
    try:
        data = result["data"]["insert_company_profiles"]["returning"][0]
        return CompanyProfileModel(**data)
    except (KeyError, IndexError) as e:
        raise Exception("Error parsing response from Hasura") from e

def update_company_profile(profile):
    query = """
    mutation ($id: Int!, $name: String!, $address: String!, $description: String) {
      update_company_profiles_by_pk(
        pk_columns: {id: $id}, 
        _set: {name: $name, address: $address, description: $description}
      ) {
        id
        user_id
        name
        address
        description
      }
    }
    """
    variables = {
        "id": profile.id,
        "name": profile.name,
        "address": profile.address,
        "description": profile.description
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
        address
        description
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
    query = """
    mutation ($company_id: Int!, $title: String!, $description: String!) {
      insert_job_descriptions(objects: {company_id: $company_id, title: $title, description: $description}) {
        returning {
          id
          company_id
          title
          description
        }
      }
    }
    """
    variables = {
        "company_id": jd.company_id,
        "title": jd.title,
        "description": jd.description
    }
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
        description
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
