from __future__ import annotations

from uuid import UUID

from app.services.knowledge_base import knowledge_base
from app.services.report_service import ReportService
from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.report_tasks.generate_report_task")
def generate_report_task(audit_id: str) -> dict[str, str]:
    service = ReportService()
    report_path = service.build_report_now(UUID(audit_id))
    return {"audit_id": audit_id, "report_path": report_path}


@celery_app.task(name="app.tasks.report_tasks.reindex_knowledge_task")
def reindex_knowledge_task() -> dict[str, str]:
    knowledge_base.ensure_seeded()
    return {"status": "reindexed"}
