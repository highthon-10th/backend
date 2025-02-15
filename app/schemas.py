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
    
def event_schema(event: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(event["_id"]),
        "favorite_member": event["favorite_member"],
        "latitude": event["latitude"],
        "longitude": event["longitude"],
        "photo_url": event.get("photo_url"),
        "event_name": event["event_name"],
        "event_time": event["event_time"],
        "event_link": event["event_link"],
        "user_name": event["user_name"],
        "description": event["description"],
        "created_at": event["created_at"]
    }
    
def visit_schema(visit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(visit["_id"]),
        "name": visit["name"],
        "favorite_member": visit["favorite_member"],
        "photo_url": visit.get("photo_url"),
        "latitude": visit["latitude"],
        "longitude": visit["longitude"],
        "description": visit["description"],
        "place_type": visit["place_type"],
        "directions_link": visit["directions_link"],
        "created_at": visit["created_at"]
    }