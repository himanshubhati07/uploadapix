# Authentication dependencies and helpers.
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, TokenBlacklist
from app.core.security import decode_access_token

load_dotenv('.env_c880a487-d8cf-4cb1-82c9-3bfd459673d3', override=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

INVALID_TOKEN_MESSAGE = "Your session has expired or the authentication token is invalid. Please log in again."


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=INVALID_TOKEN_MESSAGE,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        jti: str = payload.get("jti")
        if user_id is None or jti is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    result = await db.execute(select(TokenBlacklist).where(TokenBlacklist.token_jti == jti))
    if result.scalar_one_or_none() is not None:
        raise credentials_exception

    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
