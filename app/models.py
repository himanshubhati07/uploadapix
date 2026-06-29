# SQLAlchemy models for the application.
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import DateTime, String, Boolean, ForeignKey, Enum as SAEnum, Text, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class ProviderName(str, Enum):
    google = "google"


class ProjectStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class EnvironmentType(str, Enum):
    prod = "prod"
    dev = "dev"
    test = "test"


class IntegrationStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"
    stopped = "stopped"
    incomplete = "incomplete"
    complete = "complete"


class RepositoryType(str, Enum):
    frontend = "frontend"
    backend = "backend"


class UploadStatus(str, Enum):
    uploaded = "uploaded"
    analyzing = "analyzing"
    completed = "completed"


class AnalysisStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"


class IntegrationAnalysisStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class DataPackageStatus(str, Enum):
    uploaded = "uploaded"
    analyzed = "analyzed"
    pre_flight_checked = "pre_flight_checked"
    integrated = "integrated"


class ServiceStatus(str, Enum):
    running = "running"
    stopped = "stopped"


class ServiceType(str, Enum):
    frontend = "frontend"
    backend = "backend"


class DeploymentStatus(str, Enum):
    success = "success"
    pending = "pending"
    failed = "failed"


class DeploymentActionType(str, Enum):
    copy = "copy"
    open_tunnel = "open_tunnel"


class IntegrationIssueType(str, Enum):
    critical = "critical"
    warning = "warning"


class IntegrationIssueStatus(str, Enum):
    open = "open"
    resolved = "resolved"


class IssueActionType(str, Enum):
    resolve = "resolve"
    ignore = "ignore"
    retry = "retry"


class IntegrationProcessStatus(str, Enum):
    ongoing = "ongoing"
    completed = "completed"
    stopped = "stopped"


class CodeStackStatus(str, Enum):
    ready = "ready"
    not_ready = "not_ready"


class HistoryStatus(str, Enum):
    completed = "completed"
    in_progress = "in_progress"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.user)
    remember_me: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    oauth_providers: Mapped[list["OAuthProvider"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    repositories: Mapped[list["Repository"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    github_integration: Mapped[Optional["GitHubIntegration"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    action_history: Mapped[list["UserActionHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    provider_name: Mapped[ProviderName] = mapped_column(SAEnum(ProviderName))
    provider_user_id: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(back_populates="oauth_providers")


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    token_jti: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[ProjectStatus] = mapped_column(SAEnum(ProjectStatus), default=ProjectStatus.not_started)
    environment: Mapped[EnvironmentType | None] = mapped_column(SAEnum(EnvironmentType), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    services: Mapped[list["Service"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    logs: Mapped[list["LogEntry"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    analytics: Mapped[Optional["ProjectAnalytics"]] = relationship(back_populates="project", uselist=False, cascade="all, delete-orphan")
    histories: Mapped[list["ProjectHistory"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Integration(Base):
    __tablename__ = "integrations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[IntegrationStatus] = mapped_column(SAEnum(IntegrationStatus), default=IntegrationStatus.pending)
    frontend_repo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    backend_repo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    access_token: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("projects.id"), nullable=True)

    repositories: Mapped[list["Repository"]] = relationship(back_populates="integration", cascade="all, delete-orphan")
    analyses: Mapped[list["IntegrationAnalysis"]] = relationship(back_populates="integration", cascade="all, delete-orphan")
    services: Mapped[list["Service"]] = relationship(back_populates="integration", cascade="all, delete-orphan")
    data_packages: Mapped[list["DataPackage"]] = relationship(back_populates="integration", cascade="all, delete-orphan")


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(500))
    repo_type: Mapped[RepositoryType] = mapped_column(SAEnum(RepositoryType))
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    integration_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("integrations.id"), nullable=True)
    upload_status: Mapped[UploadStatus] = mapped_column(SAEnum(UploadStatus), default=UploadStatus.uploaded)
    analysis_status: Mapped[AnalysisStatus] = mapped_column(SAEnum(AnalysisStatus), default=AnalysisStatus.pending)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_analyzed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User | None] = relationship(back_populates="repositories")
    integration: Mapped[Integration | None] = relationship(back_populates="repositories")
    analyses: Mapped[list["IntegrationAnalysis"]] = relationship(back_populates="repository", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("user_id", "url", name="uq_repo_user_url"),)


class IntegrationAnalysis(Base):
    __tablename__ = "integration_analyses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("integrations.id"), nullable=True)
    repository_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("repositories.id"), nullable=True)
    status: Mapped[IntegrationAnalysisStatus] = mapped_column(SAEnum(IntegrationAnalysisStatus), default=IntegrationAnalysisStatus.pending)
    errors: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    integration: Mapped[Integration | None] = relationship(back_populates="analyses")
    repository: Mapped[Repository | None] = relationship(back_populates="analyses")
    report: Mapped[Optional["AnalysisReport"]] = relationship(back_populates="analysis", uselist=False, cascade="all, delete-orphan")


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    analysis_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("integration_analyses.id"))
    result: Mapped[str] = mapped_column(Text)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    analysis: Mapped[IntegrationAnalysis] = relationship(back_populates="report")


class DataPackage(Base):
    __tablename__ = "data_packages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("integrations.id"))
    file_path: Mapped[str] = mapped_column(String(500))
    status: Mapped[DataPackageStatus] = mapped_column(SAEnum(DataPackageStatus), default=DataPackageStatus.uploaded)
    size: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    integration: Mapped[Integration] = relationship(back_populates="data_packages")
    analysis_result: Mapped[Optional["AnalysisResult"]] = relationship(back_populates="data_package", uselist=False, cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    data_package_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("data_packages.id"))
    issues: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    data_package: Mapped[DataPackage] = relationship(back_populates="analysis_result")


class GitHubIntegration(Base):
    __tablename__ = "github_integrations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    access_token: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="github_integration")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    integration_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("integrations.id"), nullable=True)
    project_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(200))
    service_type: Mapped[ServiceType] = mapped_column(SAEnum(ServiceType))
    url: Mapped[str] = mapped_column(String(500))
    status: Mapped[ServiceStatus] = mapped_column(SAEnum(ServiceStatus), default=ServiceStatus.stopped)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    integration: Mapped[Integration | None] = relationship(back_populates="services")
    project: Mapped[Project | None] = relationship(back_populates="services")
    logs: Mapped[list["ServiceLog"]] = relationship(back_populates="service", cascade="all, delete-orphan")


class ServiceLog(Base):
    __tablename__ = "service_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("services.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    message: Mapped[str] = mapped_column(Text)

    service: Mapped[Service] = relationship(back_populates="logs")


class LogEntry(Base):
    __tablename__ = "project_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    message: Mapped[str] = mapped_column(Text)

    project: Mapped[Project] = relationship(back_populates="logs")


class UserActionHistory(Base):
    __tablename__ = "user_action_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="action_history")


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[DeploymentStatus] = mapped_column(SAEnum(DeploymentStatus), default=DeploymentStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    actions: Mapped[list["DeploymentAction"]] = relationship(back_populates="deployment", cascade="all, delete-orphan")


class DeploymentAction(Base):
    __tablename__ = "deployment_actions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    deployment_id: Mapped[str] = mapped_column(ForeignKey("deployments.id"))
    action_type: Mapped[DeploymentActionType] = mapped_column(SAEnum(DeploymentActionType))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    deployment: Mapped[Deployment] = relationship(back_populates="actions")


class IntegrationIssue(Base):
    __tablename__ = "integration_issues"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    issue_type: Mapped[IntegrationIssueType] = mapped_column(SAEnum(IntegrationIssueType))
    affected_component: Mapped[str] = mapped_column(String(200))
    status: Mapped[IntegrationIssueStatus] = mapped_column(SAEnum(IntegrationIssueStatus), default=IntegrationIssueStatus.open)
    date_reported: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    actions: Mapped[list["IssueAction"]] = relationship(back_populates="issue", cascade="all, delete-orphan")


class IssueAction(Base):
    __tablename__ = "issue_actions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    issue_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("integration_issues.id"))
    label: Mapped[str] = mapped_column(String(200))
    action_type: Mapped[IssueActionType] = mapped_column(SAEnum(IssueActionType))

    issue: Mapped[IntegrationIssue] = relationship(back_populates="actions")


class IntegrationProcess(Base):
    __tablename__ = "integration_processes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status: Mapped[IntegrationProcessStatus] = mapped_column(SAEnum(IntegrationProcessStatus), default=IntegrationProcessStatus.ongoing)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    progress: Mapped[float] = mapped_column(Float, default=0.0)


class CodeStack(Base):
    __tablename__ = "code_stacks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[CodeStackStatus] = mapped_column(SAEnum(CodeStackStatus), default=CodeStackStatus.not_ready)


class Environment(Base):
    __tablename__ = "environments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    launch_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ProjectAnalytics(Base):
    __tablename__ = "project_analytics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    forward_generated: Mapped[int] = mapped_column(default=0)
    backward_generated: Mapped[int] = mapped_column(default=0)
    syntax_updates: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project: Mapped[Project] = relationship(back_populates="analytics")


class ProjectHistory(Base):
    __tablename__ = "project_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[HistoryStatus] = mapped_column(SAEnum(HistoryStatus), default=HistoryStatus.in_progress)
    version: Mapped[str] = mapped_column(String(50))

    project: Mapped[Project] = relationship(back_populates="histories")
