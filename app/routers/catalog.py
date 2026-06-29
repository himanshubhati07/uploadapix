# Catalog routes for codestacks and environments.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import CodeStack, Environment
from app.schemas import CodeStackRead, EnvironmentRead
from app.core.auth import get_current_user

router = APIRouter(tags=["catalog"])


@router.get("/codestacks/{codestack_id}", response_model=CodeStackRead)
async def get_codestack(codestack_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(CodeStack).where(CodeStack.id == codestack_id))
    codestack = result.scalar_one_or_none()
    if codestack is None:
        raise HTTPException(status_code=404, detail="Code stack not found")
    return codestack


@router.get("/environments/{environment_id}", response_model=EnvironmentRead)
async def get_environment(environment_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Environment).where(Environment.id == environment_id))
    environment = result.scalar_one_or_none()
    if environment is None:
        raise HTTPException(status_code=404, detail="Environment not found")
    return environment
