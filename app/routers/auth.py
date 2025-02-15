from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from ..database import get_db
from ..auth import verify_password, get_password_hash, create_access_token
from ..models import UserCreate, Token, LoginRequest
from ..schemas import user_schema

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    db = get_db()
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["created_at"] = datetime.utcnow()
    
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return user_schema(created_user)

@router.post("/token", response_model=Token)
async def login(login_request: LoginRequest):
    db = get_db()
    user = await db.users.find_one({"username": login_request.username})
    if not user or not verify_password(login_request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}