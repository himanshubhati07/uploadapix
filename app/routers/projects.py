# Project management routes.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Project, Service, LogEntry
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate, ServiceRead, LogEntryRead
from app.core.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    project = Project(**payload.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(db: AsyncSession = Depends(get_db), _=Depends(get_current_user), offset: int = 0, limit: int = 20):
    result = await db.execute(select(Project).offset(offset).limit(limit))
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: str, payload: ProjectUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/{project_id}/services", response_model=list[ServiceRead])
async def list_project_services(project_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.project_id == project_id))
    return result.scalars().all()


@router.get("/{project_id}/logs", response_model=list[LogEntryRead])
async def list_project_logs(project_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(LogEntry).where(LogEntry.project_id == project_id).order_by(LogEntry.timestamp.asc()))
    return result.scalars().all()


@router.post("/{project_id}/services/{service_id}/start", response_model=ServiceRead)
async def start_project_service(project_id: str, service_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.id == service_id, Service.project_id == project_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.status.value == "running":
        raise HTTPException(status_code=409, detail="Service already running")
    service.status = service.status.__class__.running
    await db.commit()
    await db.refresh(service)
    return service


@router.post("/{project_id}/services/{service_id}/stop", response_model=ServiceRead)
async def stop_project_service(project_id: str, service_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.id == service_id, Service.project_id == project_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.status.value == "stopped":
        raise HTTPException(status_code=409, detail="Service already stopped")
    service.status = service.status.__class__.stopped
    await db.commit()
    await db.refresh(service)
    return service
