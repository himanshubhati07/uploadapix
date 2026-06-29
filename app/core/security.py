# Security utilities for password hashing and JWT handling.
import os
import re
import uuid
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext

load_dotenv('.env_c880a487-d8cf-4cb1-82c9-3bfd459673d3', override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> tuple[str, datetime, str]:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = uuid.uuid4().hex
    to_encode = {"sub": subject, "role": role, "exp": expire, "jti": jti}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire, jti


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def validate_password_complexity(password: str) -> Optional[str]:
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must include an uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must include a lowercase letter."
    if not re.search(r"\d", password):
        return "Password must include a number."
    return None
