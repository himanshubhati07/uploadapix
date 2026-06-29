# Analytics and history routes.
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Project, ProjectAnalytics, ProjectHistory
from app.schemas import ProjectAnalyticsRead, ProjectHistoryRead, ProjectOverviewResponse, ProjectRead
from app.core.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["analytics"])


@router.get("/{project_id}/analytics", response_model=ProjectAnalyticsRead)
async def get_project_analytics(project_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(ProjectAnalytics).where(ProjectAnalytics.project_id == project_id))
    analytics = result.scalar_one_or_none()
    if analytics is None:
        raise HTTPException(status_code=404, detail="Analytics not found")
    return analytics


@router.get("/{project_id}/history", response_model=list[ProjectHistoryRead])
async def get_project_history(project_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(ProjectHistory).where(ProjectHistory.project_id == project_id).order_by(ProjectHistory.date.desc()))
    return result.scalars().all()


@router.get("/overview", response_model=ProjectOverviewResponse)
async def get_project_overview(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    total = await db.scalar(select(func.count(Project.id)))
    in_progress = await db.scalar(select(func.count(Project.id)).where(Project.status == "in_progress"))
    completed = await db.scalar(select(func.count(Project.id)).where(Project.status == "completed"))
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month = await db.scalar(select(func.count(Project.id)).where(Project.created_at >= month_start))
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return ProjectOverviewResponse(
        total_projects=total or 0,
        in_progress=in_progress or 0,
        completed=completed or 0,
        this_month=this_month or 0,
        projects=projects,
    )


@router.get("/history", response_model=list[ProjectHistoryRead])
async def list_project_history(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(ProjectHistory).order_by(ProjectHistory.date.desc()))
    return result.scalars().all()
