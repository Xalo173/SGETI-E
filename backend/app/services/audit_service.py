from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import SessionLocal
from app.models.audit import Audit, AuditFinding, AuditPhaseHistory, AuditPlan
from app.schemas.audit import AuditCreate, AuditFindingCreate, AuditFindingRead, AuditListItem, AuditPlanRead, AuditPlanResponse, AuditRead
from app.services.rag_service import rag_service


class AuditService:
    def create_audit(self, payload: AuditCreate) -> AuditRead:
        with SessionLocal() as session:
            audit = Audit(
                title=payload.title,
                software_name=payload.software_name,
                software_type=payload.software_type,
                scope=payload.scope,
                objective=payload.objective,
                context=payload.context.model_dump(),
                current_phase="requirements",
                report_status="not_requested",
            )
            session.add(audit)
            session.add(AuditPhaseHistory(audit=audit, phase="requirements", note="Audit created"))
            session.commit()
            return self.get_audit(audit.id)  # type: ignore[return-value]

    def list_audits(self) -> list[AuditListItem]:
        with SessionLocal() as session:
            audits = session.scalars(select(Audit).order_by(Audit.created_at.desc())).all()
            return [
                AuditListItem(
                    id=audit.id,
                    title=audit.title,
                    software_name=audit.software_name,
                    current_phase=audit.current_phase,
                    report_status=audit.report_status,
                    created_at=audit.created_at,
                )
                for audit in audits
            ]

    def get_audit(self, audit_id: UUID) -> AuditRead | None:
        with SessionLocal() as session:
            audit = session.scalars(
                select(Audit)
                .where(Audit.id == audit_id)
                .options(
                    selectinload(Audit.plan),
                    selectinload(Audit.findings),
                )
            ).first()
            if not audit:
                return None

            plan = None
            if audit.plan:
                plan = AuditPlanRead(
                    title=audit.plan.title,
                    summary=audit.plan.summary,
                    methodology=audit.plan.methodology,
                    standards_used=audit.plan.standards_used,
                    steps=audit.plan.steps,
                    criteria=audit.plan.criteria,
                )

            findings = [
                AuditFindingRead(
                    id=finding.id,
                    severity=finding.severity,
                    title=finding.title,
                    description=finding.description,
                    evidence=finding.evidence,
                    recommendation=finding.recommendation,
                    created_at=finding.created_at,
                )
                for finding in audit.findings
            ]

            return AuditRead(
                id=audit.id,
                title=audit.title,
                software_name=audit.software_name,
                software_type=audit.software_type,
                scope=audit.scope,
                objective=audit.objective,
                context=audit.context,
                current_phase=audit.current_phase,
                plan_summary=audit.plan_summary,
                plan_citations=audit.plan_citations,
                report_status=audit.report_status,
                report_file_path=audit.report_file_path,
                created_at=audit.created_at,
                updated_at=audit.updated_at,
                plan=plan,
                findings=findings,
            )

    def generate_plan(self, audit_id: UUID) -> AuditPlanResponse | None:
        with SessionLocal() as session:
            audit = session.get(Audit, audit_id)
            if not audit:
                return None

            context_text = f"""
Título: {audit.title}
Software: {audit.software_name}
Tipo: {audit.software_type}
Alcance: {audit.scope}
Objetivo: {audit.objective}
Contexto JSON: {audit.context}
""".strip()

            plan_payload, citations = rag_service.generate_plan(context_text)
            plan = AuditPlan(
                audit=audit,
                title=plan_payload["title"],
                summary=plan_payload["summary"],
                methodology=plan_payload["methodology"],
                standards_used=plan_payload.get("standards_used", []),
                steps=plan_payload.get("steps", []),
                criteria=plan_payload.get("criteria", []),
            )
            audit.plan_summary = plan.summary
            audit.plan_citations = citations
            audit.current_phase = "design"
            session.add(plan)
            session.add(AuditPhaseHistory(audit=audit, phase="design", note="Plan generated with RAG"))
            session.commit()
            return AuditPlanResponse(
                audit_id=audit.id,
                plan=AuditPlanRead(
                    title=plan.title,
                    summary=plan.summary,
                    methodology=plan.methodology,
                    standards_used=plan.standards_used,
                    steps=plan.steps,
                    criteria=plan.criteria,
                ),
            )

    def update_phase(self, audit_id: UUID, phase: str) -> AuditRead | None:
        with SessionLocal() as session:
            audit = session.get(Audit, audit_id)
            if not audit:
                return None
            audit.current_phase = phase
            session.add(AuditPhaseHistory(audit=audit, phase=phase, note=f"Phase updated to {phase}"))
            session.commit()
        return self.get_audit(audit_id)

    def add_finding(self, audit_id: UUID, payload: AuditFindingCreate) -> AuditRead | None:
        with SessionLocal() as session:
            audit = session.get(Audit, audit_id)
            if not audit:
                return None
            finding = AuditFinding(audit=audit, **payload.model_dump())
            session.add(finding)
            audit.current_phase = "execution"
            session.add(AuditPhaseHistory(audit=audit, phase="execution", note="Finding registered"))
            session.commit()
        return self.get_audit(audit_id)
