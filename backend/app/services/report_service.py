from __future__ import annotations

from pathlib import Path
from uuid import UUID

from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.audit import Audit
from app.services.pdf_service import pdf_service


class ReportService:
    def enqueue_report_generation(self, audit_id: UUID) -> str:
        # Delegate PDF generation to Celery so the API request returns immediately.
        from app.tasks.report_tasks import generate_report_task

        task = generate_report_task.delay(str(audit_id))
        return task.id

    def sync_refresh_report_status(self, audit_id: UUID) -> None:
        with SessionLocal() as session:
            audit = session.get(Audit, audit_id)
            if audit and audit.report_status == "not_requested":
                audit.report_status = "processing"
                session.commit()

    def get_report_file(self, audit_id: UUID):
        with SessionLocal() as session:
            audit = session.get(Audit, audit_id)
            if not audit or not audit.report_file_path:
                return None
            report_path = Path(audit.report_file_path)
            if not report_path.exists():
                return None
            return FileResponse(path=str(report_path), media_type="application/pdf", filename=report_path.name)

    def build_report_now(self, audit_id: UUID) -> str:
        with SessionLocal() as session:
            audit = session.get(Audit, audit_id)
            if not audit:
                raise ValueError("Audit not found")

            findings = [
                {
                    "severity": finding.severity,
                    "title": finding.title,
                    "description": finding.description,
                }
                for finding in audit.findings
            ]
            plan = audit.plan
            report_dir = Path(settings.report_storage_dir)
            report_dir.mkdir(parents=True, exist_ok=True)
            output_path = report_dir / f"audit-report-{audit_id}.pdf"
            pdf_service.build_report(
                output_path=str(output_path),
                audit={
                    "software_name": audit.software_name,
                    "scope": audit.scope,
                    "objective": audit.objective,
                },
                plan=None if not plan else {
                    "summary": plan.summary,
                    "standards_used": plan.standards_used,
                },
                findings=findings,
            )
            audit.report_status = "ready"
            audit.report_file_path = str(output_path)
            session.commit()
            return str(output_path)
