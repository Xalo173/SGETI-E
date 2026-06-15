from __future__ import annotations

import json

from langchain_core.prompts import PromptTemplate

from app.services.knowledge_base import knowledge_base
from app.services.llm_service import llm_service


PLAN_PROMPT = PromptTemplate.from_template(
    """
Eres un asistente experto en auditorías de software.
Debes proponer un plan de evaluación usando exclusivamente los estándares recuperados.

Contexto del software:
{context}

Fragmentos de normas recuperados:
{context_documents}

Responde en JSON estricto con estas claves:
- title
- summary
- methodology
- standards_used: lista de objetos con norm, section y rationale
- steps: lista de objetos con step, description, deliverables, owner
- criteria: lista de objetos con criterion, metric, evidence

Incluye referencias explícitas a ISO 25010 e IEEE 1028 cuando correspondan.
"""
)


class RagService:
    def generate_plan(self, context: str) -> tuple[dict, list[dict]]:
        retriever = knowledge_base.get_retriever()
        documents = retriever.invoke(context)
        joined_documents = "\n\n".join(document.page_content for document in documents)

        prompt = PLAN_PROMPT.format(context=context, context_documents=joined_documents)
        try:
            raw_text = llm_service.generate_text(prompt)
            plan = self._parse_plan(raw_text)
        except RuntimeError:
            # Keep the demo usable when Anthropic is not configured yet.
            plan = self._fallback_plan(context)

        citations = [
            {
                "source": document.metadata.get("source", "knowledge-base"),
                "title": document.metadata.get("title", document.metadata.get("source", "standard")),
                "excerpt": document.page_content[:220],
            }
            for document in documents
        ]
        return plan, citations

    def _parse_plan(self, raw_text: str) -> dict:
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return self._fallback_plan(raw_text)

    def _fallback_plan(self, context: str) -> dict:
        return {
            "title": "Plan de auditoría generado por IA",
            "summary": f"Plan diseñado para el contexto: {context[:280]}",
            "methodology": "RAG con estándares ISO 25010 e IEEE 1028",
            "standards_used": [
                {"norm": "ISO/IEC 25010", "section": "Quality Model", "rationale": "Define product quality characteristics."},
                {"norm": "IEEE 1028", "section": "Review process", "rationale": "Provides review and audit techniques."},
            ],
            "steps": [
                {"step": "1", "description": "Revisar contexto y alcance", "deliverables": ["Context matrix"], "owner": "Lead auditor"},
                {"step": "2", "description": "Ejecutar análisis guiado por normas", "deliverables": ["Findings log"], "owner": "Audit team"},
                {"step": "3", "description": "Consolidar reporte final", "deliverables": ["PDF report"], "owner": "Lead auditor"},
            ],
            "criteria": [
                {"criterion": "Functional suitability", "metric": "Coverage of critical flows", "evidence": "Test cases and observations"},
                {"criterion": "Review completeness", "metric": "Issues traced to standards", "evidence": "Standards citations"},
            ],
        }


rag_service = RagService()
