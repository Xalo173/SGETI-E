from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.audit import AuditCreate, AuditFindingCreate, AuditListItem, AuditPlanResponse, AuditRead, AuditUpdatePhase
from app.services.audit_service import AuditService
from app.services.report_service import ReportService

router = APIRouter(prefix="/audits")
audit_service = AuditService()
report_service = ReportService()


@router.post("", response_model=AuditRead, status_code=status.HTTP_201_CREATED)
def create_audit(payload: AuditCreate) -> AuditRead:
    return audit_service.create_audit(payload)


@router.get("", response_model=list[AuditListItem])
def list_audits() -> list[AuditListItem]:
    return audit_service.list_audits()


@router.get("/{audit_id}", response_model=AuditRead)
def get_audit(audit_id: UUID) -> AuditRead:
    audit = audit_service.get_audit(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit


@router.post("/{audit_id}/plan", response_model=AuditPlanResponse)
def generate_plan(audit_id: UUID) -> AuditPlanResponse:
    try:
        response = audit_service.generate_plan(audit_id)
        if not response:
            raise HTTPException(status_code=404, detail="Audit not found")
        return response
    except Exception:
        audit = audit_service.get_audit(audit_id)
        if not audit:
            raise HTTPException(status_code=404, detail="Audit not found")

        return AuditPlanResponse(
            audit_id=audit.id,
            plan={
                "title": "Plan de auditoría demo",
                "summary": "Plan de respaldo generado localmente para demostrar el flujo sin clave de Anthropic.",
                "methodology": "RAG local con normas ISO/IEC 25010 e IEEE 1028",
                "standards_used": [
                    {
                        "norm": "ISO/IEC 25010",
                        "section": "Quality model",
                        "rationale": "Define the product quality characteristics to evaluate.",
                    },
                    {
                        "norm": "IEEE 1028",
                        "section": "Software reviews and audits",
                        "rationale": "Provides the audit and review structure used in the evaluation.",
                    },
                ],
                "steps": [
                    {
                        "step": "1",
                        "description": "Revisar contexto, alcance y objetivos del software.",
                        "deliverables": ["Matriz de contexto"],
                        "owner": "Lead auditor",
                    },
                    {
                        "step": "2",
                        "description": "Evaluar el software contra criterios de calidad y auditoría.",
                        "deliverables": ["Lista de hallazgos"],
                        "owner": "Equipo de auditoría",
                    },
                    {
                        "step": "3",
                        "description": "Consolidar evidencias y redactar el reporte final.",
                        "deliverables": ["Reporte PDF"],
                        "owner": "Lead auditor",
                    },
                ],
                "criteria": [
                    {
                        "criterion": "Functional suitability",
                        "metric": "Cobertura de flujos críticos",
                        "evidence": "Casos de prueba y observaciones",
                    },
                    {
                        "criterion": "Review completeness",
                        "metric": "Trazabilidad a normas",
                        "evidence": "Citas de ISO 25010 e IEEE 1028",
                    },
                ],
            },
        )


@router.put("/{audit_id}/phase", response_model=AuditRead)
def update_phase(audit_id: UUID, payload: AuditUpdatePhase) -> AuditRead:
    audit = audit_service.update_phase(audit_id, payload.phase)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit


@router.post("/{audit_id}/findings", response_model=AuditRead, status_code=status.HTTP_201_CREATED)
def create_finding(audit_id: UUID, payload: AuditFindingCreate) -> AuditRead:
    audit = audit_service.add_finding(audit_id, payload)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit


@router.post("/{audit_id}/report", status_code=status.HTTP_202_ACCEPTED)
def request_report(audit_id: UUID) -> dict[str, str]:
    task_id = report_service.enqueue_report_generation(audit_id)
    report_service.sync_refresh_report_status(audit_id)
    return {"message": "Report generation queued", "task_id": task_id}


@router.get("/{audit_id}/report")
def download_report(audit_id: UUID):
    response = report_service.get_report_file(audit_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Report not ready")
    return response
