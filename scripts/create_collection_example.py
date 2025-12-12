# scripts/create_collection_example.py
import asyncio
from app.db.client import get_client, get_master_db
from app.utils.mongo_utils import safe_collection_name

async def main():
    client = get_client()
    master_db = get_master_db()
    org_name = "example_org"
    coll_name = safe_collection_name(org_name)
    db = client[master_db.name]
    if coll_name in await db.list_collection_names():
        print(f"Collection {coll_name} already exists.")
    else:
        await db.create_collection(coll_name)
        print(f"Created collection {coll_name} in DB {db.name}.")

if __name__ == "__main__":
    asyncio.run(main())
