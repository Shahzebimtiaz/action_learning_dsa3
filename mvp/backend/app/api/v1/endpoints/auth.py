# implement authentication endpoint here, user db table users




# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app import crud, models, schemas
# from app.deps import get_db

# router = APIRouter()

# @router.post("/register")
# def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
#     user = crud.user.create(db, obj_in=user_in)
#     return user

# @router.post("/login")
# def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
#     user = crud.user.authenticate(db, email=user_in.email, password=user_in.password)
#     return user
