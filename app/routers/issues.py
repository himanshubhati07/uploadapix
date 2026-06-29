# Integration issue tracking routes.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import IntegrationIssue, IntegrationIssueStatus, IntegrationIssueType, IssueAction, IssueActionType
from app.schemas import IntegrationIssueRead, MessageResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/integration", tags=["issues"])


@router.get("/issues", response_model=list[IntegrationIssueRead])
async def list_issues(db: AsyncSession = Depends(get_db), _=Depends(get_current_user), offset: int = 0, limit: int = 20):
    result = await db.execute(select(IntegrationIssue).offset(offset).limit(limit))
    return result.scalars().all()


@router.post("/issues/{issue_id}/resolve", response_model=MessageResponse)
async def resolve_issue(issue_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(IntegrationIssue).where(IntegrationIssue.id == issue_id))
    issue = result.scalar_one_or_none()
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue.status = IntegrationIssueStatus.resolved
    db.add(IssueAction(issue_id=issue.id, label="Resolve", action_type=IssueActionType.resolve))
    await db.commit()
    return MessageResponse(message="Issue resolved")


@router.post("/issues/{issue_id}/ignore", response_model=MessageResponse)
async def ignore_issue(issue_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(IntegrationIssue).where(IntegrationIssue.id == issue_id))
    issue = result.scalar_one_or_none()
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    db.add(IssueAction(issue_id=issue.id, label="Ignore", action_type=IssueActionType.ignore))
    await db.commit()
    return MessageResponse(message="Issue ignored")


@router.post("/retry", response_model=MessageResponse)
async def retry_integration(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(IntegrationIssue).where(IntegrationIssue.issue_type == IntegrationIssueType.critical, IntegrationIssue.status == IntegrationIssueStatus.open))
    critical_open = result.scalars().first()
    if critical_open:
        raise HTTPException(status_code=409, detail="Resolve all critical issues before retry")
    return MessageResponse(message="Integration retry initiated")
