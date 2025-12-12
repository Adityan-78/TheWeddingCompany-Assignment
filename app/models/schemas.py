from pydantic import BaseModel, EmailStr
from typing import Optional

class OrgCreateIn(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrgCreateOut(BaseModel):
    org_id: str
    organization_name: str
    org_collection_name: str
    admin_id: str

class OrgGetOut(BaseModel):
    org_id: str
    organization_name: str
    org_collection_name: str
    connection_details: Optional[dict]
    admin_user_id: Optional[str]

class OrgUpdateIn(BaseModel):
    organization_name: str
    new_organization_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class OrgDeleteIn(BaseModel):
    organization_name: str

class AdminLoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
