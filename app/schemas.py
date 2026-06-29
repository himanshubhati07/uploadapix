# Pydantic schemas for request/response validation.
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .models import (
    UserRole,
    ProviderName,
    ProjectStatus,
    EnvironmentType,
    IntegrationStatus,
    RepositoryType,
    UploadStatus,
    AnalysisStatus,
    IntegrationAnalysisStatus,
    DataPackageStatus,
    ServiceStatus,
    ServiceType,
    DeploymentStatus,
    DeploymentActionType,
    IntegrationIssueType,
    IntegrationIssueStatus,
    IssueActionType,
    IntegrationProcessStatus,
    CodeStackStatus,
    HistoryStatus,
)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class MessageResponse(BaseModel):
    message: str


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    remember_me: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: UUID
    role: UserRole
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    email: EmailStr
    full_name: str
    provider_user_id: str


class OAuthProviderRead(BaseModel):
    id: UUID
    provider_name: ProviderName
    provider_user_id: str

    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    name: str
    status: ProjectStatus = ProjectStatus.not_started
    environment: Optional[EnvironmentType] = None
    url: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[ProjectStatus] = None
    environment: Optional[EnvironmentType] = None
    url: Optional[str] = None


class ProjectRead(ProjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IntegrationBase(BaseModel):
    name: str
    status: IntegrationStatus = IntegrationStatus.pending
    frontend_repo_url: Optional[str] = None
    backend_repo_url: Optional[str] = None
    access_token: Optional[str] = None
    project_id: Optional[UUID] = None


class IntegrationCreate(IntegrationBase):
    pass


class IntegrationUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[IntegrationStatus] = None
    frontend_repo_url: Optional[str] = None
    backend_repo_url: Optional[str] = None
    access_token: Optional[str] = None


class IntegrationRead(IntegrationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RepositoryBase(BaseModel):
    name: str
    url: str
    repo_type: RepositoryType
    integration_id: Optional[UUID] = None
    upload_status: UploadStatus = UploadStatus.uploaded
    analysis_status: AnalysisStatus = AnalysisStatus.pending
    file_path: Optional[str] = None


class RepositoryCreate(RepositoryBase):
    user_id: Optional[UUID] = None


class RepositoryUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    repo_type: Optional[RepositoryType] = None
    upload_status: Optional[UploadStatus] = None
    analysis_status: Optional[AnalysisStatus] = None
    file_path: Optional[str] = None


class RepositoryRead(RepositoryBase):
    id: UUID
    user_id: Optional[UUID] = None
    last_analyzed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IntegrationAnalysisBase(BaseModel):
    integration_id: Optional[UUID] = None
    repository_id: Optional[UUID] = None
    status: IntegrationAnalysisStatus = IntegrationAnalysisStatus.pending
    errors: Optional[str] = None


class IntegrationAnalysisCreate(IntegrationAnalysisBase):
    pass


class IntegrationAnalysisRead(IntegrationAnalysisBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisReportRead(BaseModel):
    id: UUID
    analysis_id: UUID
    result: str
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DataPackageCreate(BaseModel):
    file_path: str
    size: float


class DataPackageRead(BaseModel):
    id: UUID
    integration_id: UUID
    file_path: str
    status: DataPackageStatus
    size: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisResultRead(BaseModel):
    id: UUID
    data_package_id: UUID
    issues: str
    recommendations: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GitHubIntegrationCreate(BaseModel):
    access_token: str


class GitHubIntegrationRead(BaseModel):
    id: UUID
    user_id: UUID
    access_token: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceBase(BaseModel):
    name: str
    service_type: ServiceType
    url: str
    status: ServiceStatus = ServiceStatus.stopped
    integration_id: Optional[UUID] = None
    project_id: Optional[UUID] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceLogRead(BaseModel):
    id: UUID
    service_id: UUID
    timestamp: datetime
    message: str

    model_config = ConfigDict(from_attributes=True)


class LogEntryRead(BaseModel):
    id: UUID
    project_id: UUID
    timestamp: datetime
    message: str

    model_config = ConfigDict(from_attributes=True)


class DeploymentBase(BaseModel):
    name: str
    status: DeploymentStatus = DeploymentStatus.pending


class DeploymentCreate(DeploymentBase):
    deployment_id: str


class DeploymentRead(DeploymentBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeploymentActionRead(BaseModel):
    id: UUID
    deployment_id: str
    action_type: DeploymentActionType
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class IntegrationIssueBase(BaseModel):
    title: str
    description: str
    issue_type: IntegrationIssueType
    affected_component: str
    status: IntegrationIssueStatus = IntegrationIssueStatus.open


class IntegrationIssueCreate(IntegrationIssueBase):
    pass


class IntegrationIssueRead(IntegrationIssueBase):
    id: UUID
    date_reported: datetime

    model_config = ConfigDict(from_attributes=True)


class IssueActionRead(BaseModel):
    id: UUID
    issue_id: UUID
    label: str
    action_type: IssueActionType

    model_config = ConfigDict(from_attributes=True)


class IntegrationProcessRead(BaseModel):
    id: UUID
    status: IntegrationProcessStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    progress: float

    model_config = ConfigDict(from_attributes=True)


class IntegrationProcessStopRequest(BaseModel):
    integration_process_id: UUID


class CodeStackRead(BaseModel):
    id: UUID
    name: str
    description: str
    status: CodeStackStatus

    model_config = ConfigDict(from_attributes=True)


class EnvironmentRead(BaseModel):
    id: UUID
    name: str
    launch_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProjectAnalyticsRead(BaseModel):
    id: UUID
    project_id: UUID
    forward_generated: int
    backward_generated: int
    syntax_updates: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectHistoryRead(BaseModel):
    id: UUID
    project_id: UUID
    description: str
    date: datetime
    status: HistoryStatus
    version: str

    model_config = ConfigDict(from_attributes=True)


class ProjectOverviewResponse(BaseModel):
    total_projects: int
    in_progress: int
    completed: int
    this_month: int
    projects: List[ProjectRead]
