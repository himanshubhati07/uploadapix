# Integration-related routes.
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import (
    Integration,
    IntegrationAnalysis,
    IntegrationAnalysisStatus,
    IntegrationStatus,
    AnalysisReport,
    DataPackage,
    DataPackageStatus,
    AnalysisResult,
    IntegrationProcess,
    IntegrationProcessStatus,
    Service,
    ServiceStatus,
)
from app.schemas import (
    IntegrationCreate,
    IntegrationRead,
    IntegrationUpdate,
    IntegrationAnalysisCreate,
    IntegrationAnalysisRead,
    AnalysisReportRead,
    DataPackageCreate,
    DataPackageRead,
    MessageResponse,
    ServiceRead,
    IntegrationProcessStopRequest,
)
from app.core.auth import get_current_user

router = APIRouter(prefix="/integrations", tags=["integrations"])
aux_router = APIRouter(prefix="/integration", tags=["integrations"])


@router.post("", response_model=IntegrationRead, status_code=status.HTTP_201_CREATED)
async def create_integration(payload: IntegrationCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    if payload.frontend_repo_url is None or payload.backend_repo_url is None:
        raise HTTPException(status_code=422, detail="Both frontend and backend repository URLs are required")
    integration = Integration(**payload.model_dump())
    db.add(integration)
    await db.commit()
    await db.refresh(integration)
    return integration


@router.get("", response_model=list[IntegrationRead])
async def list_integrations(db: AsyncSession = Depends(get_db), _=Depends(get_current_user), offset: int = 0, limit: int = 20):
    result = await db.execute(select(Integration).offset(offset).limit(limit))
    return result.scalars().all()


@router.get("/{integration_id}", response_model=IntegrationRead)
async def get_integration(integration_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Integration).where(Integration.id == integration_id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integration


@router.patch("/{integration_id}/status", response_model=IntegrationRead)
async def update_integration_status(integration_id: str, payload: IntegrationUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Integration).where(Integration.id == integration_id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    if payload.status is None:
        raise HTTPException(status_code=422, detail="Status is required")
    integration.status = payload.status
    await db.commit()
    await db.refresh(integration)
    return integration


@router.put("/{integration_id}", response_model=IntegrationRead)
async def update_integration(integration_id: str, payload: IntegrationUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Integration).where(Integration.id == integration_id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(integration, key, value)
    await db.commit()
    await db.refresh(integration)
    return integration


@router.post("/{integration_id}/analyze", response_model=IntegrationAnalysisRead, status_code=status.HTTP_201_CREATED)
async def analyze_integration(integration_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Integration).where(Integration.id == integration_id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")

    analysis = IntegrationAnalysis(integration_id=integration.id, status=IntegrationAnalysisStatus.in_progress)
    db.add(analysis)
    await db.flush()

    data_package_result = await db.execute(
        select(DataPackage).where(DataPackage.integration_id == integration_id).order_by(DataPackage.created_at.desc())
    )
    data_package = data_package_result.scalars().first()
    if data_package:
        data_package.status = DataPackageStatus.analyzed
        db.add(AnalysisResult(data_package_id=data_package.id, issues="", recommendations=""))

    report = AnalysisReport(analysis_id=analysis.id, result="Analysis completed successfully")
    analysis.status = IntegrationAnalysisStatus.completed
    db.add(report)
    await db.commit()
    await db.refresh(analysis)
    return analysis


@router.get("/{integration_id}/reports/{report_id}", response_model=AnalysisReportRead)
async def get_integration_report(integration_id: str, report_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    report_result = await db.execute(
        select(AnalysisReport).join(IntegrationAnalysis).where(
            AnalysisReport.id == report_id,
            IntegrationAnalysis.integration_id == integration_id,
        )
    )
    report = report_result.scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/{integration_id}/upload", response_model=DataPackageRead, status_code=status.HTTP_201_CREATED)
async def upload_data_package(integration_id: str, payload: DataPackageCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Integration).where(Integration.id == integration_id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    data_package = DataPackage(integration_id=integration.id, file_path=payload.file_path, size=payload.size)
    db.add(data_package)
    await db.commit()
    await db.refresh(data_package)
    return data_package


@router.get("/{integration_id}/status", response_model=IntegrationRead)
async def get_integration_status(integration_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    return await get_integration(integration_id, db, _)


@router.post("/{integration_id}/pre-flight", response_model=DataPackageRead)
async def pre_flight_check(integration_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(DataPackage).where(DataPackage.integration_id == integration_id).order_by(DataPackage.created_at.desc()))
    data_package = result.scalars().first()
    if data_package is None:
        raise HTTPException(status_code=404, detail="Data package not found")
    if data_package.status != DataPackageStatus.analyzed:
        raise HTTPException(status_code=409, detail="Data package must be analyzed before pre-flight")
    data_package.status = DataPackageStatus.pre_flight_checked
    await db.commit()
    await db.refresh(data_package)
    return data_package


@router.post("/{integration_id}/integrate", response_model=IntegrationRead)
async def integrate(integration_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Integration).where(Integration.id == integration_id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    integration.status = IntegrationStatus.completed
    await db.commit()
    await db.refresh(integration)
    return integration


@router.post("/{integration_id}/launch", response_model=MessageResponse)
async def launch_integration(integration_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Integration).where(Integration.id == integration_id))
    integration = result.scalar_one_or_none()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    if integration.status not in {IntegrationStatus.completed, IntegrationStatus.complete}:
        raise HTTPException(status_code=409, detail="Integration must be complete before launch")
    return MessageResponse(message="Integration launch initiated")


@router.put("/{integration_id}/services/{service_id}/start", response_model=ServiceRead)
async def start_service(integration_id: str, service_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.id == service_id, Service.integration_id == integration_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.status == ServiceStatus.running:
        raise HTTPException(status_code=409, detail="Service already running")
    service.status = ServiceStatus.running
    await db.commit()
    await db.refresh(service)
    return service


@router.put("/{integration_id}/services/{service_id}/stop", response_model=ServiceRead)
async def stop_service(integration_id: str, service_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.id == service_id, Service.integration_id == integration_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.status == ServiceStatus.stopped:
        raise HTTPException(status_code=409, detail="Service already stopped")
    service.status = ServiceStatus.stopped
    await db.commit()
    await db.refresh(service)
    return service


@router.get("/{integration_id}/services", response_model=list[ServiceRead])
async def list_services(integration_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Service).where(Service.integration_id == integration_id))
    return result.scalars().all()


@aux_router.post("", response_model=IntegrationAnalysisRead, status_code=status.HTTP_201_CREATED)
async def create_integration_analysis(payload: IntegrationAnalysisCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    analysis = IntegrationAnalysis(**payload.model_dump())
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


@aux_router.get("/status/{analysis_id}", response_model=IntegrationAnalysisRead)
async def get_integration_analysis_status(analysis_id: str, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(IntegrationAnalysis).where(IntegrationAnalysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@aux_router.post("/stop", response_model=MessageResponse)
async def stop_integration_process(payload: IntegrationProcessStopRequest, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(IntegrationProcess).where(IntegrationProcess.id == payload.integration_process_id))
    process = result.scalar_one_or_none()
    if process is None:
        raise HTTPException(status_code=404, detail="Integration process not found")
    if process.status != IntegrationProcessStatus.ongoing:
        raise HTTPException(status_code=409, detail="Integration process not ongoing")
    process.status = IntegrationProcessStatus.stopped
    process.progress = 0.0
    process.end_time = datetime.utcnow()
    await db.commit()
    return MessageResponse(message="Integration process stopped")
