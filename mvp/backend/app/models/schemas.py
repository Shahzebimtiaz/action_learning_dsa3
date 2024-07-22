from pydantic import BaseModel
from typing import Optional, List
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

class FeedbackRequest(BaseModel):
    original_text: str
    feedback: List[dict]

class FeedbackResponse(BaseModel):
    id: int
    original_text: str
    feedback: List[dict]


# class ActivityLogCreate(BaseModel):
#     user_id: int
#     action: str
#     details: Optional[str]

# class ActivityLogResponse(BaseModel):
#     id: int
#     user_id: int
#     action: str
#     details: Optional[str]
#     timestamp: str

#     class Config:
#         orm_mode = True
