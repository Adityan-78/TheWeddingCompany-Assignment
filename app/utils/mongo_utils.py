# app/utils/mongo_utils.py
import re
from typing import Any, Dict
from bson import ObjectId


def safe_collection_name(org_name: str) -> str:
    # Lowercase, replace non-alphanumeric with underscore, trim.
    s = org_name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return f"org_{s}"


def oid_to_str(d: Dict[str, Any]) -> Dict[str, Any]:
    # shallow conversion helpful for responses
    out = {}
    for k, v in d.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        else:
            out[k] = v
    return out
