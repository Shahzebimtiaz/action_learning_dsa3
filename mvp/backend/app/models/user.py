from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    isadmin = Column(Boolean, default=False)  # New column to indicate admin status

class ActivityLog(Base):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Reference to User ID
    activity_type = Column(String, nullable=False)  # e.g., 'login', 'image ocr'
    description = Column(Text, nullable=True)  # Additional info about the activity
    timestamp = Column(DateTime, server_default=func.now())
