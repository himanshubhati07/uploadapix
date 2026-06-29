# Authentication routes.
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User, OAuthProvider, ProviderName, TokenBlacklist
from app.schemas import (
    UserCreate,
    UserRead,
    UserLogin,
    TokenResponse,
    MessageResponse,
    GoogleAuthRequest,
)
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    validate_password_complexity,
    decode_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.core.auth import get_current_user, INVALID_TOKEN_MESSAGE

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    complexity_error = validate_password_complexity(payload.password)
    if complexity_error:
        raise HTTPException(status_code=422, detail=complexity_error)

    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered.")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        remember_me=payload.remember_me,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user.last_login = datetime.utcnow()
    token, expires_at, _ = create_access_token(subject=str(user.id), role=user.role.value)
    await db.commit()
    return TokenResponse(access_token=token, expires_in=int((expires_at - datetime.utcnow()).total_seconds()))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    except Exception as exc:
        raise HTTPException(status_code=401, detail=INVALID_TOKEN_MESSAGE) from exc

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail=INVALID_TOKEN_MESSAGE)

    access_token, expires_at, _ = create_access_token(subject=str(user.id), role=user.role.value)
    return TokenResponse(access_token=access_token, expires_in=int((expires_at - datetime.utcnow()).total_seconds()))


@router.post("/logout", response_model=MessageResponse)
async def logout(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        jti = payload.get("jti")
        user_id = payload.get("sub")
        exp = payload.get("exp")
    except Exception as exc:
        raise HTTPException(status_code=401, detail=INVALID_TOKEN_MESSAGE) from exc

    if not jti or not user_id or not exp:
        raise HTTPException(status_code=401, detail=INVALID_TOKEN_MESSAGE)

    blacklist = TokenBlacklist(token_jti=jti, user_id=user_id, expires_at=datetime.utcfromtimestamp(exp))
    db.add(blacklist)
    await db.commit()
    return MessageResponse(message="Logged out successfully")


@router.get("/profile", response_model=UserRead)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/validate-token", response_model=MessageResponse)
async def validate_token(_: User = Depends(get_current_user)):
    return MessageResponse(message="Token is valid")


@router.post("/google", response_model=TokenResponse)
async def google_auth(payload: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=get_password_hash(payload.provider_user_id),
        )
        db.add(user)
        await db.flush()
        oauth = OAuthProvider(
            provider_name=ProviderName.google,
            provider_user_id=payload.provider_user_id,
            user_id=user.id,
        )
        db.add(oauth)
        await db.commit()
        await db.refresh(user)
    else:
        oauth_result = await db.execute(
            select(OAuthProvider).where(
                OAuthProvider.user_id == user.id,
                OAuthProvider.provider_name == ProviderName.google,
            )
        )
        if oauth_result.scalar_one_or_none() is None:
            db.add(
                OAuthProvider(
                    provider_name=ProviderName.google,
                    provider_user_id=payload.provider_user_id,
                    user_id=user.id,
                )
            )
            await db.commit()

    token, expires_at, _ = create_access_token(subject=str(user.id), role=user.role.value)
    return TokenResponse(access_token=token, expires_in=int((expires_at - datetime.utcnow()).total_seconds()))
