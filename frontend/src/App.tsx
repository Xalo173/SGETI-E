import { useEffect, useMemo, useState } from 'react'
import { api } from './lib/api'
import { AuditCard } from './components/AuditCard'
import { AuditForm } from './components/AuditForm'
import { FindingsPanel } from './components/FindingsPanel'
import { PlanPanel } from './components/PlanPanel'
import { PhaseStepper } from './components/PhaseStepper'
import { ReportPanel } from './components/ReportPanel'
import type { Audit, AuditPlan, AuditSummary } from './types'

export default function App() {
  const [audits, setAudits] = useState<AuditSummary[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [selectedAudit, setSelectedAudit] = useState<Audit | null>(null)
  const [plan, setPlan] = useState<AuditPlan | null>(null)
  const [busy, setBusy] = useState(false)
  const selectedSummary = useMemo(() => audits.find((item) => item.id === selectedId) ?? null, [audits, selectedId])

  const loadAudits = async () => {
    const response = await api.get<AuditSummary[]>('/api/v1/audits')
    setAudits(response.data)
    if (!selectedId && response.data.length > 0) {
      setSelectedId(response.data[0].id)
    }
  }

  const loadAudit = async (auditId: string) => {
    const response = await api.get<Audit>(`/api/v1/audits/${auditId}`)
    setSelectedAudit(response.data)
    setPlan(response.data.plan ?? null)
  }

  useEffect(() => {
    void loadAudits()
  }, [])

  useEffect(() => {
    if (selectedId) {
      void loadAudit(selectedId)
    }
  }, [selectedId])

  useEffect(() => {
    if (!selectedId) return

    const interval = setInterval(() => {
      void loadAudit(selectedId)
    }, 3000)

    return () => clearInterval(interval)
  }, [selectedId])

  const createAudit = async (payload: unknown) => {
    setBusy(true)
    try {
      await api.post('/api/v1/audits', payload)
      await loadAudits()
    } finally {
      setBusy(false)
    }
  }

  const generatePlan = async () => {
    if (!selectedId) return
    setBusy(true)
    try {
      const response = await api.post<{ plan: AuditPlan }>(`/api/v1/audits/${selectedId}/plan`)
      setPlan(response.data.plan)
      await loadAudit(selectedId)
      await loadAudits()
    } finally {
      setBusy(false)
    }
  }

  const changePhase = async (phase: string) => {
    if (!selectedId) return
    setBusy(true)
    try {
      await api.put(`/api/v1/audits/${selectedId}/phase`, { phase })
      await loadAudit(selectedId)
      await loadAudits()
    } finally {
      setBusy(false)
    }
  }

  const requestReport = async () => {
    if (!selectedId) return
    setBusy(true)
    try {
      await api.post(`/api/v1/audits/${selectedId}/report`)
      await loadAudit(selectedId)
      await loadAudits()
    } finally {
      setBusy(false)
    }
  }

  const saveFinding = async (finding: { severity: string; title: string; description: string }) => {
    if (!selectedId) return
    await api.post(`/api/v1/audits/${selectedId}/findings`, finding)
    await loadAudit(selectedId)
    await loadAudits()
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(15,118,110,0.18),_transparent_34%),linear-gradient(180deg,#f8fafc_0%,#eef2ff_100%)] text-ink">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col gap-8 px-4 py-6 sm:px-6 lg:px-8">
        <header className="rounded-3xl border border-slate-200/80 bg-white/85 p-6 shadow-glow backdrop-blur" aria-label="AuditAI header">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-accent">AuditAI</p>
              <h1 className="mt-2 text-3xl font-black tracking-tight sm:text-4xl">Planificación de auditorías de software asistida por IA</h1>
              <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
                Flujo completo en tres fases con RAG demostrable, trazabilidad de normas y generación de reportes en background.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
              <Stat label="Auditorías" value={String(audits.length)} />
              <Stat label="Fase" value={selectedAudit?.current_phase ?? 'n/a'} />
              <Stat label="Reporte" value={selectedAudit?.report_status ?? 'n/a'} />
              <Stat label="Standards" value={plan ? 'RAG' : 'pending'} />
            </div>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-[380px_1fr]">
          <aside className="space-y-6">
            <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Create audit">
              <h2 className="text-xl font-bold">Nueva auditoría</h2>
              <p className="mt-1 text-sm text-slate-600">Captura el contexto del software a auditar.</p>
              <AuditForm onSubmit={createAudit} busy={busy} />
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Audit list">
              <h2 className="text-xl font-bold">Auditorías</h2>
              <div className="mt-4 space-y-3" role="list" aria-label="Audit list items">
                {audits.map((audit) => (
                  <AuditCard
                    key={audit.id}
                    audit={audit}
                    active={audit.id === selectedId}
                    onSelect={setSelectedId}
                  />
                ))}
                {audits.length === 0 && <p className="text-sm text-slate-500">Aún no hay auditorías creadas.</p>}
              </div>
            </section>
          </aside>

          <section className="space-y-6">
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <PhaseStepper
                currentPhase={selectedAudit?.current_phase ?? 'requirements'}
                onChangePhase={changePhase}
                busy={busy}
              />
            </div>

            <div className="grid gap-6 xl:grid-cols-2">
              <PlanPanel audit={selectedAudit} plan={plan} onGeneratePlan={generatePlan} busy={busy} />
              <ReportPanel audit={selectedAudit} onRequestReport={requestReport} busy={busy} />
            </div>

            <FindingsPanel
              audit={selectedAudit}
              onRefresh={selectedId ? () => loadAudit(selectedId) : undefined}
              onSaveFinding={saveFinding}
            />

            {selectedSummary && (
              <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <h2 className="text-xl font-bold">Resumen activo</h2>
                <p className="mt-2 text-sm text-slate-600">{selectedSummary.title}</p>
              </section>
            )}
          </section>
        </section>
      </div>
    </main>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 px-3 py-3">
      <dt className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">{label}</dt>
      <dd className="mt-1 text-sm font-bold text-slate-900">{value}</dd>
    </div>
  )
}
