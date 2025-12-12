from bson import ObjectId
from typing import Optional, Dict, Any, List
from app.db.client import get_master_db, get_client
from app.utils.mongo_utils import safe_collection_name, oid_to_str
from app.core.security import hash_password, verify_password
import datetime

MASTER_ORG = "organizations"
MASTER_ADMIN = "admins"


class OrgService:
    def __init__(self):
        self.master = get_master_db()
        self.client = get_client()

    async def org_exists(self, name: str) -> bool:
        return await self.master[MASTER_ORG].find_one({"organization_name": name}) is not None

    async def get_org_by_name(self, name: str):
        org = await self.master[MASTER_ORG].find_one({"organization_name": name})
        if not org:
            return None
        org = oid_to_str(org)
        return {
            "org_id": org["_id"],
            "organization_name": org["organization_name"],
            "org_collection_name": org["org_collection_name"],
            "connection_details": org.get("connection_details"),
            "admin_user_id": str(org.get("admin_user_id")) if org.get("admin_user_id") else None
        }

    async def create_organization(self, name: str, email: str, password: str):
        if await self.org_exists(name):
            raise ValueError("Organization already exists")

        coll = safe_collection_name(name)
        created = datetime.datetime.utcnow()

        org_doc = {
            "organization_name": name,
            "org_collection_name": coll,
            "connection_details": {"type": "mongodb", "database": self.master.name},
            "created_at": created
        }

        org_res = await self.master[MASTER_ORG].insert_one(org_doc)
        org_id = org_res.inserted_id

        admin_doc = {
            "email": email,
            "password": hash_password(password),
            "org_id": org_id,
            "created_at": created
        }

        admin_res = await self.master[MASTER_ADMIN].insert_one(admin_doc)
        admin_id = admin_res.inserted_id

        await self.master[MASTER_ORG].update_one({"_id": org_id}, {"$set": {"admin_user_id": admin_id}})

        db = self.client[self.master.name]
        try:
            await db.create_collection(coll)
        except:
            pass

        return {
            "org_id": str(org_id),
            "organization_name": name,
            "org_collection_name": coll,
            "admin_id": str(admin_id)
        }

    async def authenticate_admin(self, email: str, password: str):
        admin = await self.master[MASTER_ADMIN].find_one({"email": email})
        if not admin:
            return None
        if not verify_password(password, admin["password"]):
            return None
        return {"_id": str(admin["_id"]), "org_id": str(admin["org_id"])}

    async def delete_organization(self, name: str, admin: dict):
        org = await self.master[MASTER_ORG].find_one({"organization_name": name})
        if not org:
            raise ValueError("Organization not found")

        if str(org["admin_user_id"]) != str(admin["_id"]):
            raise PermissionError("Not authorized")

        coll = org["org_collection_name"]
        db = self.client[self.master.name]

        if coll in await db.list_collection_names():
            await db[coll].drop()

        await self.master[MASTER_ADMIN].delete_many({"org_id": org["_id"]})
        await self.master[MASTER_ORG].delete_one({"_id": org["_id"]})

    async def update_organization(self, old_name: str, new_name: Optional[str], email: Optional[str], password: Optional[str], admin: dict):
        org = await self.master[MASTER_ORG].find_one({"organization_name": old_name})
        if not org:
            raise ValueError("Organization not found")

        if str(org["admin_user_id"]) != admin["_id"]:
            raise PermissionError("Not authorized")

        update = {}

        if email or password:
            admin_update = {}
            if email:
                admin_update["email"] = email
            if password:
                admin_update["password"] = hash_password(password)
            await self.master[MASTER_ADMIN].update_one({"_id": org["admin_user_id"]}, {"$set": admin_update})

        if new_name and new_name != old_name:
            if await self.org_exists(new_name):
                raise ValueError("New organization name already exists")

            old_coll = org["org_collection_name"]
            new_coll = safe_collection_name(new_name)
            db = self.client[self.master.name]

            try:
                await db.create_collection(new_coll)
            except:
                pass

            if old_coll in await db.list_collection_names():
                cursor = db[old_coll].find({})
                docs = []
                async for d in cursor:
                    docs.append(d)
                    if len(docs) >= 500:
                        await db[new_coll].insert_many(docs)
                        docs = []
                if docs:
                    await db[new_coll].insert_many(docs)
                await db[old_coll].drop()

            update["organization_name"] = new_name
            update["org_collection_name"] = new_coll

        if update:
            await self.master[MASTER_ORG].update_one({"_id": org["_id"]}, {"$set": update})

        new_org = await self.master[MASTER_ORG].find_one({"_id": org["_id"]})
        new_org = oid_to_str(new_org)
        return {
            "org_id": new_org["_id"],
            "organization_name": new_org["organization_name"],
            "org_collection_name": new_org["org_collection_name"],
            "connection_details": new_org.get("connection_details"),
            "admin_user_id": str(new_org.get("admin_user_id")) if new_org.get("admin_user_id") else None
        }
