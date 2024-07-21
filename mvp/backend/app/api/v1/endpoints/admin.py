# app/api/v1/endpoints/admin.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.user import User as DBUser, ActivityLog as DBActivityLog
from app.models.schemas import UserCreate, UserResponse #, ActivityLogResponse
from pydantic import BaseModel
from datetime import datetime
from app.models import user as models
from typing import Optional

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = DBUser(email=user.email, password=user.password, isadmin=user.isadmin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db_user.password = user.password
    db_user.isadmin = user.isadmin
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

# @router.get("/activity_logs/", response_model=list[ActivityLogResponse])
# def read_activity_logs(db: Session = Depends(get_db)):
#     logs = db.query(DBActivityLog).all()
#     return logs

class LogActivityRequest(BaseModel):
    user_id: int
    activity_type: str
    detail: str
    source_language: Optional[str]

class ActivityLogResponse(BaseModel):
    action: str
    details: str
    timestamp: str
    source_language: Optional[str]

    class Config:
        orm_mode = True

@router.post("/log_user_activity/")
def log_user_activity(request: LogActivityRequest, db: Session = Depends(get_db)):
    db_log = DBActivityLog(user_id=request.user_id, 
                           activity_type=request.activity_type, 
                           detail=request.detail,
                           source_language=request.source_language)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return {"message": "Activity logged successfully"}

# @router.get("/activity_logs/", response_model=list[ActivityLogResponse])
# def read_activity_logs(db: Session = Depends(get_db)):
#     logs = db.query(models.ActivityLog).all()
#     return [ActivityLogResponse(action=log.activity_type, details=log.detail, timestamp=log.timestamp.isoformat()) for log in logs]

@router.get("/activity_logs/", response_model=list[ActivityLogResponse])
def read_activity_logs(db: Session = Depends(get_db)):
    logs = db.query(DBActivityLog).all()
    return [ActivityLogResponse(action=log.activity_type, 
                                details=log.detail, 
                                source_language=log.source_language,
                                timestamp=log.timestamp.isoformat()) for log in logs]