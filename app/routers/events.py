from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from datetime import datetime
from typing import List
from bson import ObjectId
import os
from ..database import get_db
from ..auth import get_current_user
from ..models import EventCreate
from ..schemas import event_schema

router = APIRouter()

@router.post("/", response_model=dict)
async def create_event(event: EventCreate, current_user = Depends(get_current_user)):
    db = get_db()
    event_dict = event.model_dump()
    event_dict["user_name"] = current_user["username"]
    event_dict["created_at"] = datetime.utcnow()
    
    result = await db.events.insert_one(event_dict)
    created_event = await db.events.find_one({"_id": result.inserted_id})
    return event_schema(created_event)

@router.post("/image/{favorite_member}/{event_id}", response_model=dict)
async def upload_image(event_id: str, favorite_member: str, file: UploadFile = File(...)):
    db = get_db()
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    # Create directory if it doesn't exist
    directory = f"static/{favorite_member}/events"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the file
    file_location = f"{directory}/{event_id}.jpg"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    # Update the event with the photo URL
    photo_url = f"static/{favorite_member}/events/{event_id}.jpg"
    await db.events.update_one({"_id": ObjectId(event_id)}, {"$set": {"photo_url": photo_url}})

    updated_event = await db.events.find_one({"_id": ObjectId(event_id)})
    return event_schema(updated_event)

@router.get("/image/{favorite_member}/{event_id}", response_class=FileResponse)
async def get_image(favorite_member: str, event_id: str):
    file_path = f"static/{favorite_member}/events/{event_id}.jpg"
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@router.get("/", response_model=List[dict])
async def read_events(skip: int = 0, limit: int = 10):
    db = get_db()
    events = []
    cursor = db.events.find().skip(skip).limit(limit)
    async for event in cursor:
        events.append(event_schema(event))
    return events

@router.get("/favorite/{favorite_member}", response_model=List[dict])
async def read_events_by_favorite_member(favorite_member: str, skip: int = 0, limit: int = 10):
    db = get_db()
    events = []
    cursor = db.events.find({"favorite_member": favorite_member}).skip(skip).limit(limit)
    async for event in cursor:
        events.append(event_schema(event))
    return events

@router.get("/{event_id}", response_model=dict)
async def read_event(event_id: str):
    db = get_db()
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event_schema(event)

@router.delete("/{event_id}")
async def delete_event(event_id: str, current_user = Depends(get_current_user)):
    db = get_db()
    existing_event = await db.events.find_one({"_id": ObjectId(event_id)})
    if existing_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if existing_event["user_name"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    
    await db.events.delete_one({"_id": ObjectId(event_id)})
    return {"message": "Event deleted successfully"}