from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from bson import ObjectId
from app.config import settings
from app.db.client import get_master_db

oauth2 = OAuth2PasswordBearer(tokenUrl="/admin/login")

async def get_current_user(token: str = Depends(oauth2)):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except:
        raise HTTPException(401, "Invalid or expired token")

async def get_current_admin(token=Depends(get_current_user)):
    admin_id = token.get("admin_id")
    if not admin_id:
        raise HTTPException(401, "Invalid token")

    db = get_master_db()
    admin = await db["admins"].find_one({"_id": ObjectId(admin_id)})
    if not admin:
        raise HTTPException(401, "Admin not found")

    admin["_id"] = str(admin["_id"])
    return admin
