from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AuditContext(BaseModel):
    stakeholders: list[str] = Field(default_factory=list)
    systems: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    compliance_goals: list[str] = Field(default_factory=list)
    notes: str | None = None


class AuditCreate(BaseModel):
    title: str
    software_name: str
    software_type: str
    scope: str
    objective: str
    context: AuditContext


class AuditUpdatePhase(BaseModel):
    phase: str = Field(pattern="^(requirements|design|execution|closed)$")


class AuditFindingCreate(BaseModel):
    severity: str = Field(pattern="^(low|medium|high|critical)$")
    title: str
    description: str
    evidence: str | None = None
    recommendation: str | None = None


class AuditFindingRead(AuditFindingCreate):
    id: UUID
    created_at: datetime


class AuditPlanRead(BaseModel):
    title: str
    summary: str
    methodology: str
    standards_used: list[dict]
    steps: list[dict]
    criteria: list[dict]


class AuditRead(BaseModel):
    id: UUID
    title: str
    software_name: str
    software_type: str
    scope: str
    objective: str
    context: dict
    current_phase: str
    plan_summary: str | None
    plan_citations: list[dict] | None
    report_status: str
    report_file_path: str | None
    created_at: datetime
    updated_at: datetime
    plan: AuditPlanRead | None = None
    findings: list[AuditFindingRead] = Field(default_factory=list)


class AuditListItem(BaseModel):
    id: UUID
    title: str
    software_name: str
    current_phase: str
    report_status: str
    created_at: datetime


class AuditPlanResponse(BaseModel):
    audit_id: UUID
    plan: AuditPlanRead
