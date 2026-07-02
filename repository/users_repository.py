from sqlalchemy.orm import Session

from models.users import Users
from schemas.users_schema import UserCreateSchema


def create_user(
    db: Session, user_create: UserCreateSchema, hash_password: str
) -> Users:
    db_user = Users(name=user_create.name, password_hash=hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def found_user_by_id(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id).first()
    return user


def found_user_by_login(db: Session, name: str):
    user = db.query(Users).filter(Users.name == name).first()
    return user
