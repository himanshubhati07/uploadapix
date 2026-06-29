# GitHub integration routes.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import GitHubIntegration
from app.schemas import GitHubIntegrationCreate, GitHubIntegrationRead, MessageResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/integrations/github", tags=["github"])
user_router = APIRouter(prefix="/user", tags=["github"])


@router.post("", response_model=GitHubIntegrationRead, status_code=status.HTTP_201_CREATED)
async def create_github_integration(payload: GitHubIntegrationCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    existing = await db.execute(select(GitHubIntegration).where(GitHubIntegration.user_id == current_user.id))
    integration = existing.scalar_one_or_none()
    if integration:
        integration.access_token = payload.access_token
    else:
        integration = GitHubIntegration(user_id=current_user.id, access_token=payload.access_token)
        db.add(integration)
    await db.commit()
    await db.refresh(integration)
    return integration


@router.get("/status", response_model=MessageResponse)
async def get_github_status(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(GitHubIntegration).where(GitHubIntegration.user_id == current_user.id))
    integration = result.scalar_one_or_none()
    if integration is None:
        return MessageResponse(message="GitHub integration not configured")
    return MessageResponse(message="GitHub integration active")


@router.delete("", response_model=MessageResponse)
async def delete_github_integration(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(GitHubIntegration).where(GitHubIntegration.user_id == current_user.id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="GitHub integration not found")
    await db.delete(integration)
    await db.commit()
    return MessageResponse(message="GitHub integration removed")


@user_router.post("/github-access", response_model=GitHubIntegrationRead, status_code=status.HTTP_201_CREATED)
async def upsert_github_access(payload: GitHubIntegrationCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await create_github_integration(payload, db, current_user)
