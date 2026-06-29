# Seed initial data into the database.
import asyncio
from dotenv import load_dotenv
from sqlalchemy import select
from app.database import engine, Base, async_session
from app.models import (
    User,
    Project,
    Integration,
    Repository,
    Service,
    Deployment,
    IntegrationIssue,
    IntegrationProcess,
    CodeStack,
    Environment,
    ProjectAnalytics,
    ProjectHistory,
    DataPackage,
    IntegrationAnalysis,
    AnalysisReport,
    GitHubIntegration,
    ServiceType,
    ServiceStatus,
    RepositoryType,
    ProjectStatus,
    IntegrationStatus,
    IntegrationIssueType,
)
from app.core.security import get_password_hash

load_dotenv('.env_c880a487-d8cf-4cb1-82c9-3bfd459673d3', override=True)


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        result = await session.execute(select(User))
        if result.scalars().first():
            return

        users = [
            User(full_name="Alice Doe", email="alice@example.com", password_hash=get_password_hash("Password1")),
            User(full_name="Bob Smith", email="bob@example.com", password_hash=get_password_hash("Password1")),
        ]
        session.add_all(users)
        await session.flush()

        session.add(GitHubIntegration(user_id=users[0].id, access_token="ghp_sampletoken"))

        projects = [
            Project(name="Project Alpha", status=ProjectStatus.in_progress),
            Project(name="Project Beta", status=ProjectStatus.completed),
        ]
        session.add_all(projects)
        await session.flush()

        integrations = [
            Integration(
                name="Integration Alpha",
                status=IntegrationStatus.completed,
                frontend_repo_url="https://github.com/example/frontend",
                backend_repo_url="https://github.com/example/backend",
                project_id=projects[0].id,
            ),
            Integration(
                name="Integration Beta",
                status=IntegrationStatus.in_progress,
                frontend_repo_url="https://github.com/example/frontend2",
                backend_repo_url="https://github.com/example/backend2",
                project_id=projects[1].id,
            ),
        ]
        session.add_all(integrations)
        await session.flush()

        repositories = [
            Repository(
                name="Frontend Repo",
                url="https://github.com/example/frontend",
                repo_type=RepositoryType.frontend,
                user_id=users[0].id,
                integration_id=integrations[0].id,
            ),
            Repository(
                name="Backend Repo",
                url="https://github.com/example/backend",
                repo_type=RepositoryType.backend,
                user_id=users[0].id,
                integration_id=integrations[0].id,
            ),
        ]
        session.add_all(repositories)
        await session.flush()

        services = [
            Service(
                name="Frontend Service",
                service_type=ServiceType.frontend,
                url="https://frontend.example.com",
                status=ServiceStatus.running,
                project_id=projects[0].id,
                integration_id=integrations[0].id,
            ),
            Service(
                name="Backend Service",
                service_type=ServiceType.backend,
                url="https://backend.example.com",
                status=ServiceStatus.stopped,
                project_id=projects[0].id,
                integration_id=integrations[0].id,
            ),
        ]
        session.add_all(services)

        deployments = [
            Deployment(id="dep-001", name="Deployment 1"),
            Deployment(id="dep-002", name="Deployment 2"),
        ]
        session.add_all(deployments)

        issues = [
            IntegrationIssue(
                title="API mismatch",
                description="Backend API mismatch",
                issue_type=IntegrationIssueType.critical,
                affected_component="backend",
            ),
            IntegrationIssue(
                title="CSS warning",
                description="Minor styling issue",
                issue_type=IntegrationIssueType.warning,
                affected_component="frontend",
            ),
        ]
        session.add_all(issues)

        processes = [
            IntegrationProcess(progress=0.5),
            IntegrationProcess(progress=0.8),
        ]
        session.add_all(processes)

        codestacks = [
            CodeStack(name="Stack A", description="Frontend+Backend", status="ready"),
            CodeStack(name="Stack B", description="Legacy stack", status="not_ready"),
        ]
        session.add_all(codestacks)

        environments = [
            Environment(name="Production"),
            Environment(name="Staging"),
        ]
        session.add_all(environments)

        analytics = ProjectAnalytics(project_id=projects[0].id, forward_generated=5, backward_generated=3, syntax_updates=2)
        session.add(analytics)
        histories = [
            ProjectHistory(project_id=projects[0].id, description="Initial setup", status="completed", version="v1.0.0"),
            ProjectHistory(project_id=projects[1].id, description="Integration ongoing", status="in_progress", version="v1.1.0"),
        ]
        session.add_all(histories)

        data_package = DataPackage(integration_id=integrations[0].id, file_path="/tmp/package.zip", size=12.5)
        session.add(data_package)
        await session.flush()

        analysis = IntegrationAnalysis(integration_id=integrations[0].id, repository_id=repositories[0].id, status="completed")
        session.add(analysis)
        await session.flush()
        session.add(AnalysisReport(analysis_id=analysis.id, result="All good"))

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
