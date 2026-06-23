import { useEffect, useState } from 'react'
import type { Audit } from '../types'

export function FindingsPanel({
  audit,
  onRefresh,
  onSaveFinding,
}: {
  audit: Audit | null
  onRefresh?: () => void
  onSaveFinding: (finding: { severity: string; title: string; description: string }) => Promise<void>
}) {
  const [description, setDescription] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!audit) {
      setDescription('')
    }
  }, [audit])

  const handleSave = async () => {
    const trimmedDescription = description.trim()
    if (!trimmedDescription) {
      return
    }

    setSaving(true)
    try {
      await onSaveFinding({
        severity: 'medium',
        title: trimmedDescription.slice(0, 60),
        description: trimmedDescription,
      })
      setDescription('')
      onRefresh?.()
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Findings panel">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold">Ejecución y hallazgos</h2>
          <p className="mt-1 text-sm text-slate-600">Los hallazgos se registran en la fase de ejecución y alimentan el reporte PDF.</p>
        </div>
        <button
          type="button"
          onClick={handleSave}
          className="rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {saving ? 'Guardando...' : 'Actualizar'}
        </button>
      </div>

      <div className="mt-4 space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
        <label className="block text-sm font-medium text-slate-700">
          Nuevo hallazgo
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            rows={4}
            className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20"
            placeholder="Describe el hallazgo, evidencia o riesgo detectado..."
            aria-label="Nuevo hallazgo"
          />
        </label>
        <p className="text-xs text-slate-500">El botón permanece habilitado. Si el texto está vacío, no se guardará nada.</p>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-2">
        {audit?.findings?.length ? (
          audit.findings.map((finding) => (
            <article key={finding.id} className="rounded-2xl border border-slate-200 p-4" aria-label={`Finding ${finding.title}`}>
              <div className="flex items-center justify-between gap-3">
                <h3 className="font-semibold text-slate-900">{finding.title}</h3>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-[11px] font-bold uppercase text-slate-700">{finding.severity}</span>
              </div>
              <p className="mt-2 text-sm leading-6 text-slate-700">{finding.description}</p>
            </article>
          ))
        ) : (
          <p className="text-sm text-slate-500">Todavía no hay hallazgos registrados.</p>
        )}
      </div>
    </section>
  )
}
