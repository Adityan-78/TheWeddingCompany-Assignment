# tests/test_orgs.py
import pytest
from app.services.org_service import OrgService
from app.db.client import get_master_db
import asyncio


@pytest.mark.anyio
async def test_create_get_delete_org():
    svc = OrgService()
    name = "testtenantdemo"
    email = "admin_test@example.com"
    password = "StrongPass123!"

    # clean up if exists
    db = get_master_db()
    existing = await db["organizations"].find_one({"organization_name": name})
    if existing:
        await db["organizations"].delete_one({"_id": existing["_id"]})
        await db["admins"].delete_many({"org_id": existing["_id"]})
        # drop collection if exists
        db_client = svc.client[db.name]
        coll_name = f"org_{name}"
        if coll_name in await db_client.list_collection_names():
            await db_client[coll_name].drop()

    created = await svc.create_organization(name, email, password)
    assert created["organization_name"] == name

    fetched = await svc.get_org_by_name(name)
    assert fetched is not None
    assert fetched["organization_name"] == name

    # delete using admin id
    await svc.delete_organization(name, created["admin_id"])
    still = await svc.get_org_by_name(name)
    assert still is None
