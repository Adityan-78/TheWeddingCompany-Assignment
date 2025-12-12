from fastapi import APIRouter, HTTPException
from app.models.schemas import AdminLoginIn, TokenOut
from app.services.org_service import OrgService
from app.core.auth import create_access_token

router = APIRouter(prefix="/admin", tags=["admin"])
service = OrgService()

@router.post("/login", response_model=TokenOut)
async def admin_login(payload: AdminLoginIn):
    admin = await service.authenticate_admin(payload.email, payload.password)
    if not admin:
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"admin_id": admin["_id"], "org_id": admin["org_id"]})
    return {"access_token": token, "token_type": "bearer"}
