from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    isadmin: bool

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ActivityLogBase(BaseModel):
    user_id: int
    activity_type: str
    description: Optional[str] = None

class ActivityLogResponse(ActivityLogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
