import secrets
from datetime import datetime, timedelta, time
from typing import Optional
from fastapi import Request
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

engine = create_engine("sqlite://")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(...)
    password: str = Field(...)


def auth_db_init():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(User(username="admin", password=pwd_context.hash("password")))
        session.commit()


class V3Message(BaseModel):
    message: str = Field(...)
    token: str | None = Field(None)


def v3_message(m: str, code: int = None, r: Request = None, t: str = None) -> V3Message:
    if r and code:
        return V3Message(message=f"[v3] -> {code} {r.method} {m}", token=t)
    else:
        return V3Message(message=f"[v3] -> {m}", token=t)


class S3c5t(BaseModel):
    s3cr5t: str = Field(default=SECRET_KEY)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token():
    to_encode = {}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

