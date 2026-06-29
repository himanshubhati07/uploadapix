# Pytest fixtures for async database and client.
import os
import pytest
import asyncpg
from uuid import uuid4
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine.url import make_url
from dotenv import load_dotenv

load_dotenv('.env_c880a487-d8cf-4cb1-82c9-3bfd459673d3', override=True)

from app.main import app
from app.database import Base, get_db
from app.models import User, Project, Integration, Repository, Deployment, Service, IntegrationIssue
from app.core.security import get_password_hash
from app.models import RepositoryType, ProjectStatus, IntegrationStatus, ServiceType, ServiceStatus, IntegrationIssueType

MAIN_DB_URL = os.getenv("DATABASE_URL", "")
_parts = MAIN_DB_URL.rsplit("/", 1)
TEST_DB_URL = (_parts[0] + "/" + _parts[1] + "_test") if len(_parts) == 2 else MAIN_DB_URL


@pytest.fixture(scope="session")
async def db_engine():
    from sqlalchemy.pool import NullPool

    main_engine = create_async_engine(MAIN_DB_URL, poolclass=NullPool)
    async with main_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await main_engine.dispose()

    test_url = make_url(TEST_DB_URL)
    admin_url = test_url.set(database="postgres", drivername="postgresql")
    conn = await asyncpg.connect(admin_url.render_as_string(hide_password=False))
    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", test_url.database)
        if not exists:
            await conn.execute(f'CREATE DATABASE "{test_url.database}"')
    finally:
        await conn.close()

    engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session
        try:
            await session.rollback()
        except Exception:
            pass


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def seed_data(db_session):
    unique = uuid4().hex[:8]
    user = User(full_name="Seed User", email=f"seed-{unique}@example.com", password_hash=get_password_hash("Password1"))
    project = Project(name=f"Seed Project {unique}", status=ProjectStatus.in_progress)
    integration = Integration(
        name=f"Seed Integration {unique}",
        status=IntegrationStatus.pending,
        frontend_repo_url="https://github.com/example/frontend",
        backend_repo_url="https://github.com/example/backend",
    )
    repository = Repository(
        name=f"Seed Repo {unique}",
        url=f"https://github.com/example/repo-{unique}",
        repo_type=RepositoryType.frontend,
    )
    deployment = Deployment(id=f"dep-{unique}", name="Seed Deployment")
    service = Service(name=f"Seed Service {unique}", service_type=ServiceType.frontend, url=f"https://seed-{unique}.service", status=ServiceStatus.stopped)
    issue = IntegrationIssue(title="Seed Issue", description="Seed", issue_type=IntegrationIssueType.warning, affected_component="backend")
    db_session.add_all([user, project, integration, repository, deployment, service, issue])
    await db_session.commit()
    return {
        "user": user,
        "project": project,
        "integration": integration,
        "repository": repository,
        "deployment": deployment,
        "service": service,
        "issue": issue,
    }
