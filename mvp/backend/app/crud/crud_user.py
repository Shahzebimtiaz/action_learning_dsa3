from app.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from app.models.user import User 
import app.models.database as database
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(db:Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, firstname: str, lastname: str, email: str, password: str, date_of_birth: str, gender: str):
    db_user = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password,
        date_of_birth=date_of_birth,
        gender=gender,
        isadmin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user