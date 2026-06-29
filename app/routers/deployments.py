# Deployment history routes.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Deployment, DeploymentAction, DeploymentActionType
from app.schemas import DeploymentCreate, DeploymentRead, DeploymentActionRead, MessageResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.post("", response_model=DeploymentRead, status_code=status.HTTP_201_CREATED)
async def create_deployment(payload: DeploymentCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    deployment = Deployment(id=payload.deployment_id, name=payload.name, status=payload.status)
    db.add(deployment)
    await db.commit()
    await db.refresh(deployment)
    return deployment


@router.get("", response_model=list[DeploymentRead])
async def list_deployments(db: AsyncSession = Depends(get_db), _=Depends(get_current_user), offset: int = 0, limit: int = 20):
    result = await db.execute(select(Deployment).offset(offset).limit(limit))
    return result.scalars().all()


@router.get("/{deployment_id}", response_model=DeploymentRead)
async def get_deployment(deployment_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Deployment).where(Deployment.id == deployment_id))
    deployment = result.scalar_one_or_none()
    if deployment is None:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment


@router.post("/{deployment_id}/copy", response_model=DeploymentActionRead)
async def copy_deployment_id(deployment_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Deployment).where(Deployment.id == deployment_id))
    deployment = result.scalar_one_or_none()
    if deployment is None:
        raise HTTPException(status_code=404, detail="Deployment not found")
    action = DeploymentAction(deployment_id=deployment_id, action_type=DeploymentActionType.copy)
    db.add(action)
    await db.commit()
    await db.refresh(action)
    return action


@router.post("/{deployment_id}/tunnel", response_model=DeploymentActionRead)
async def open_deployment_tunnel(deployment_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Deployment).where(Deployment.id == deployment_id))
    deployment = result.scalar_one_or_none()
    if deployment is None:
        raise HTTPException(status_code=404, detail="Deployment not found")
    action = DeploymentAction(deployment_id=deployment_id, action_type=DeploymentActionType.open_tunnel)
    db.add(action)
    await db.commit()
    await db.refresh(action)
    return action
