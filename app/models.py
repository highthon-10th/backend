from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str
    favorite_member: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(UserBase):
    id: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str
    owner_id: str
    created_at: datetime


# 여기서 부터 하이톤 프로젝트에 맞게 수정 - GOOD
class EventBase(BaseModel):
    favorite_member: str
    latitude: float
    longitude: float
    photo_url: str
    event_name: str
    event_time: str
    event_link: str
    description: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: str
    user_name: str
    created_at: datetime
    
    
class VisitBase(BaseModel):
    name: str
    favorite_member: str
    photo_url: Optional[str] = None
    latitude: float
    longitude: float
    description: str
    place_type: str  # 식당, 공원, 카페, 기타
    directions_link: str

class VisitCreate(VisitBase):
    pass

class Visit(VisitBase):
    id: str
    created_at: datetime