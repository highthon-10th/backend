from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from typing import List
from ..database import get_db
from ..auth import get_current_user
from ..models import ItemCreate
from ..schemas import item_schema

router = APIRouter()

@router.post("/", response_model=dict)
async def create_item(item: ItemCreate, current_user = Depends(get_current_user)):
    db = get_db()
    item_dict = item.model_dump()
    item_dict["owner_id"] = current_user["_id"]
    item_dict["created_at"] = datetime.utcnow()
    
    result = await db.items.insert_one(item_dict)
    created_item = await db.items.find_one({"_id": result.inserted_id})
    return item_schema(created_item)

@router.get("/", response_model=List[dict])
async def read_items(skip: int = 0, limit: int = 10, current_user = Depends(get_current_user)):
    db = get_db()
    items = []
    cursor = db.items.find({"owner_id": current_user["_id"]}).skip(skip).limit(limit)
    async for item in cursor:
        items.append(item_schema(item))
    return items

@router.get("/{item_id}", response_model=dict)
async def read_item(item_id: str, current_user = Depends(get_current_user)):
    db = get_db()
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item["owner_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this item")
    return item_schema(item)

@router.put("/{item_id}", response_model=dict)
async def update_item(item_id: str, item: ItemCreate, current_user = Depends(get_current_user)):
    db = get_db()
    existing_item = await db.items.find_one({"_id": ObjectId(item_id)})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if existing_item["owner_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to modify this item")
    
    update_data = item.model_dump(exclude_unset=True)
    await db.items.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_data}
    )
    
    updated_item = await db.items.find_one({"_id": ObjectId(item_id)})
    return item_schema(updated_item)

@router.delete("/{item_id}")
async def delete_item(item_id: str, current_user = Depends(get_current_user)):
    db = get_db()
    existing_item = await db.items.find_one({"_id": ObjectId(item_id)})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if existing_item["owner_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
    
    await db.items.delete_one({"_id": ObjectId(item_id)})
    return {"message": "Item deleted successfully"}