# Repository and analysis routes.
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Repository, IntegrationAnalysis, IntegrationAnalysisStatus
from app.schemas import RepositoryCreate, RepositoryRead, RepositoryUpdate, IntegrationAnalysisRead, IntegrationAnalysisCreate, MessageResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/repositories", tags=["repositories"])
analysis_router = APIRouter(prefix="/analysis", tags=["repositories"])


@router.post("", response_model=RepositoryRead, status_code=status.HTTP_201_CREATED)
async def create_repository(payload: RepositoryCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    repository = Repository(**payload.model_dump())
    db.add(repository)
    await db.commit()
    await db.refresh(repository)
    return repository


@router.post("/upload", response_model=RepositoryRead, status_code=status.HTTP_201_CREATED)
async def upload_repository(payload: RepositoryCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    repository = Repository(**payload.model_dump())
    db.add(repository)
    await db.commit()
    await db.refresh(repository)
    return repository


@router.get("/{repository_id}", response_model=RepositoryRead)
async def get_repository(repository_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Repository).where(Repository.id == repository_id))
    repository = result.scalar_one_or_none()
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repository


@router.put("/{repository_id}", response_model=RepositoryRead)
async def update_repository(repository_id: str, payload: RepositoryUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Repository).where(Repository.id == repository_id))
    repository = result.scalar_one_or_none()
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(repository, key, value)
    repository.last_analyzed_at = datetime.utcnow()
    await db.commit()
    await db.refresh(repository)
    return repository


@router.post("/{repository_id}/compatibility_check", response_model=IntegrationAnalysisRead, status_code=status.HTTP_201_CREATED)
async def compatibility_check(repository_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Repository).where(Repository.id == repository_id))
    repository = result.scalar_one_or_none()
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    if repository.upload_status != repository.upload_status.__class__.completed:
        raise HTTPException(status_code=409, detail="Repository upload must be completed")
    analysis = IntegrationAnalysis(repository_id=repository.id, status=IntegrationAnalysisStatus.in_progress)
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


@router.post("/{repository_id}/dependency_analysis", response_model=IntegrationAnalysisRead, status_code=status.HTTP_201_CREATED)
async def dependency_analysis(repository_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    return await compatibility_check(repository_id, db, _)


@router.get("/{repository_id}/logs", response_model=list[IntegrationAnalysisRead])
async def get_repository_logs(repository_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(IntegrationAnalysis).where(IntegrationAnalysis.repository_id == repository_id))
    return result.scalars().all()


@analysis_router.post("/start", response_model=IntegrationAnalysisRead, status_code=status.HTTP_201_CREATED)
async def start_analysis(payload: IntegrationAnalysisCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    analysis = IntegrationAnalysis(
        integration_id=payload.integration_id,
        repository_id=payload.repository_id,
        status=IntegrationAnalysisStatus.in_progress,
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


@analysis_router.get("/{analysis_id}", response_model=IntegrationAnalysisRead)
async def get_analysis(analysis_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(IntegrationAnalysis).where(IntegrationAnalysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
