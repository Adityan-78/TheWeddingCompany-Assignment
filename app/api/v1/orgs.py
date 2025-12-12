from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import OrgCreateIn, OrgCreateOut, OrgGetOut, OrgUpdateIn, OrgDeleteIn
from app.services.org_service import OrgService
from app.deps import get_current_admin

router = APIRouter(prefix="/org", tags=["org"])
service = OrgService()

@router.post("/create", response_model=OrgCreateOut, status_code=201)
async def create_org(payload: OrgCreateIn):
    try:
        data = await service.create_organization(payload.organization_name, payload.email, payload.password)
        return data
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/get", response_model=OrgGetOut)
async def get_org(organization_name: str):
    data = await service.get_org_by_name(organization_name)
    if not data:
        raise HTTPException(404, "Organization not found")
    return data

@router.put("/update", response_model=OrgGetOut)
async def update_org(payload: OrgUpdateIn, current_admin=Depends(get_current_admin)):
    try:
        data = await service.update_organization(payload.organization_name, payload.new_organization_name, payload.email, payload.password, current_admin)
        return data
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/delete")
async def delete_org(payload: OrgDeleteIn, current_admin=Depends(get_current_admin)):
    try:
        await service.delete_organization(payload.organization_name, current_admin)
        return {"status": "deleted"}
    except ValueError as e:
        raise HTTPException(404, str(e))
    except PermissionError as e:
        raise HTTPException(403, str(e))
