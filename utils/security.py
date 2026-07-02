import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from bd import get_db
from models.users import Users

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

if not SECRET_KEY:
    raise ValueError("Не обнаружен SECREY_KEY")


def create_token(data: dict):
    to_encode = data.copy()  # потому что словарь это ссылка
    time_token = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"user_id": data["user_id"], "exp": time_token})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return None  # просрочен
    except JWTError:
        return None  # поврежден


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Неверный токен")
    user_id = payload.get("user_id")
    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user
