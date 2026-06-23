import type { Audit } from '../types'

export function ReportPanel({ audit, onRequestReport, busy }: { audit: Audit | null; onRequestReport: () => Promise<void>; busy: boolean }) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Report panel">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold">Reporte PDF</h2>
          <p className="mt-1 text-sm text-slate-600">Generación en background con Celery y Redis.</p>
        </div>
        <button type="button" onClick={onRequestReport} disabled={!audit || busy} className="rounded-xl bg-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60">
          Generar reporte
        </button>
      </div>

      <div className="mt-4 rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">
        <p><strong>Estado:</strong> {audit?.report_status ?? 'n/a'}</p>
        <p className="mt-2"><strong>Archivo:</strong> {audit?.report_file_path ?? 'No disponible'}</p>
      </div>

      {audit?.report_file_path && (
        <a href={`${import.meta.env.VITE_API_URL ?? 'http://localhost:8000'}/api/v1/audits/${audit.id}/report`} className="mt-4 inline-flex rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50">
          Descargar PDF
        </a>
      )}
    </section>
  )
}
