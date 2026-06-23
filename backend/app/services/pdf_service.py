from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class PdfService:
    def build_report(self, output_path: str, audit: dict, plan: dict | None, findings: list[dict]) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="AuditTitle", parent=styles["Title"], fontSize=20, leading=24, textColor=colors.HexColor("#0f172a")))
        styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontSize=14, leading=18, spaceBefore=10))

        doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=1.8 * cm, leftMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm)
        story = []

        story.append(Paragraph("AuditAI - Reporte de Auditoría", styles["AuditTitle"]))
        story.append(Spacer(1, 0.4 * cm))
        story.append(Paragraph(f"<b>Software:</b> {audit['software_name']}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Alcance:</b> {audit['scope']}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Objetivo:</b> {audit['objective']}", styles["BodyText"]))

        story.append(Paragraph("Plan generado", styles["Section"]))
        if plan:
            story.append(Paragraph(plan.get("summary", "Sin resumen"), styles["BodyText"]))
            standards = [["Norma", "Rationale"]]
            for item in plan.get("standards_used", []):
                standards.append([item.get("norm", ""), item.get("rationale", "")])
            story.append(Spacer(1, 0.2 * cm))
            story.append(Table(standards, colWidths=[5 * cm, 10 * cm], style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#f8fafc")]),
            ])))

        story.append(Paragraph("Hallazgos", styles["Section"]))
        if findings:
            findings_table = [["Severidad", "Título", "Descripción"]]
            for finding in findings:
                findings_table.append([finding["severity"], finding["title"], finding["description"]])
            story.append(Table(findings_table, colWidths=[2.5 * cm, 4.5 * cm, 8.0 * cm], style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])))
        else:
            story.append(Paragraph("No se registraron hallazgos todavía.", styles["BodyText"]))

        doc.build(story)
        return str(path)


pdf_service = PdfService()
