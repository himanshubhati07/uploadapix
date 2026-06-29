# Service monitoring routes.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Service, ServiceLog, ServiceStatus, UserActionHistory
from app.schemas import ServiceCreate, ServiceRead, ServiceLogRead, MessageResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/services", tags=["services"])
log_router = APIRouter(prefix="/logs", tags=["services"])
action_router = APIRouter(prefix="/actions", tags=["services"])


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
async def create_service(payload: ServiceCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    service = Service(**payload.model_dump())
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


@router.get("", response_model=list[ServiceRead])
async def list_services(db: AsyncSession = Depends(get_db), _=Depends(get_current_user), offset: int = 0, limit: int = 20):
    result = await db.execute(select(Service).offset(offset).limit(limit))
    return result.scalars().all()


@router.post("/{service_id}/start", response_model=ServiceRead)
async def start_service(service_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.status == ServiceStatus.running:
        raise HTTPException(status_code=409, detail="Service already running")
    service.status = ServiceStatus.running
    db.add(UserActionHistory(user_id=_.id, action=f"start_service:{service_id}"))
    await db.commit()
    await db.refresh(service)
    return service


@router.post("/{service_id}/stop", response_model=ServiceRead)
async def stop_service(service_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.status == ServiceStatus.stopped:
        raise HTTPException(status_code=409, detail="Service already stopped")
    service.status = ServiceStatus.stopped
    db.add(UserActionHistory(user_id=_.id, action=f"stop_service:{service_id}"))
    await db.commit()
    await db.refresh(service)
    return service


@log_router.get("/{service_id}", response_model=list[ServiceLogRead])
async def get_service_logs(service_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(ServiceLog).where(ServiceLog.service_id == service_id).order_by(ServiceLog.timestamp.asc()))
    return result.scalars().all()


@action_router.get("/history", response_model=list[MessageResponse])
async def get_action_history(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(UserActionHistory).where(UserActionHistory.user_id == current_user.id))
    history = result.scalars().all()
    return [MessageResponse(message=item.action) for item in history]
