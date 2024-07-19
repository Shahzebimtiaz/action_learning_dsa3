# from sqlalchemy.orm import Session
# from app.models.user import User
# from app.schemas.user import UserCreate
# from app.core.security import get_password_hash, verify_password

# def create(db: Session, *, obj_in: UserCreate) -> User:
#     db_obj = User(
#         email=obj_in.email,
#         hashed_password=get_password_hash(obj_in.password),
#     )
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj

# def authenticate(db: Session, *, email: str, password: str) -> User:
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         return None
#     if not verify_password(password, user.hashed_password):
#         return None
#     return user
