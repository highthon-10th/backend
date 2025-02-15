from datetime import datetime
from typing import Dict, Any

def user_schema(user: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "favorite_member": user["favorite_member"],
        "created_at": user["created_at"]
    }

def item_schema(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "description": item["description"],
        "owner_id": str(item["owner_id"]),
        "created_at": item["created_at"]
    }