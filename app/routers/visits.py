from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from datetime import datetime
from typing import List
from bson import ObjectId
import os
from ..database import get_db
from ..auth import get_current_user
from ..models import VisitCreate
from ..schemas import visit_schema

router = APIRouter()

@router.post("/", response_model=dict)
async def create_visit(visit: VisitCreate, current_user = Depends(get_current_user)):
    db = get_db()
    visit_dict = visit.model_dump()
    visit_dict["created_at"] = datetime.utcnow()
    
    result = await db.visits.insert_one(visit_dict)
    created_visit = await db.visits.find_one({"_id": result.inserted_id})
    return visit_schema(created_visit)

@router.post("/image/{favorite_member}/{visit_id}", response_model=dict)
async def upload_image(favorite_member: str, visit_id: str, file: UploadFile = File(...)):
    db = get_db()
    visit = await db.visits.find_one({"_id": ObjectId(visit_id)})
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")

    # Create directory if it doesn't exist
    directory = f"static/{favorite_member}/visits"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the file
    file_location = f"{directory}/{visit_id}.jpg"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    # Update the visit with the photo URL
    photo_url = f"static/{favorite_member}/visits/{visit_id}.jpg"
    await db.visits.update_one({"_id": ObjectId(visit_id)}, {"$set": {"photo_url": photo_url}})

    updated_visit = await db.visits.find_one({"_id": ObjectId(visit_id)})
    return visit_schema(updated_visit)

@router.get("/image/{favorite_member}/{visit_id}", response_class=FileResponse)
async def get_image(favorite_member: str, visit_id: str):
    file_path = f"static/{favorite_member}/visits/{visit_id}.jpg"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@router.get("/", response_model=List[dict])
async def read_visits(skip: int = 0, limit: int = 10):
    db = get_db()
    visits = []
    cursor = db.visits.find().skip(skip).limit(limit)
    async for visit in cursor:
        visits.append(visit_schema(visit))
    return visits

@router.get("/{visit_id}", response_model=dict)
async def read_visit(visit_id: str):
    db = get_db()
    visit = await db.visits.find_one({"_id": ObjectId(visit_id)})
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit_schema(visit)

@router.delete("/{visit_id}")
async def delete_visit(visit_id: str, current_user = Depends(get_current_user)):
    db = get_db()
    existing_visit = await db.visits.find_one({"_id": ObjectId(visit_id)})
    if existing_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    await db.visits.delete_one({"_id": ObjectId(visit_id)})
    return {"message": "Visit deleted successfully"}