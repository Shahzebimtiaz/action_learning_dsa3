from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String, index=True)
    feedback = Column(JSON)
