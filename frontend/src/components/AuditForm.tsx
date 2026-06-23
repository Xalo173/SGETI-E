import { useState } from 'react'
import type { ReactNode, FormEvent } from 'react'

export function AuditForm({ onSubmit, busy }: { onSubmit: (payload: any) => Promise<void>; busy: boolean }) {
  const [form, setForm] = useState({
    title: 'Auditoría inicial',
    software_name: 'Plataforma de pagos',
    software_type: 'Web app',
    scope: 'Módulos de autenticación, pagos y reporting',
    objective: 'Evaluar calidad, trazabilidad y riesgos del software.',
    stakeholders: 'CIO, Product Owner, Equipo de QA',
    systems: 'Frontend, API, Base de datos',
    risks: 'Fallas de seguridad, inconsistencias funcionales, baja mantenibilidad',
    compliance_goals: 'ISO 25010, IEEE 1028',
    notes: 'Priorizar áreas críticas del negocio.',
  })

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    await onSubmit({
      ...form,
      context: {
        stakeholders: form.stakeholders.split(',').map((value) => value.trim()).filter(Boolean),
        systems: form.systems.split(',').map((value) => value.trim()).filter(Boolean),
        risks: form.risks.split(',').map((value) => value.trim()).filter(Boolean),
        compliance_goals: form.compliance_goals.split(',').map((value) => value.trim()).filter(Boolean),
        notes: form.notes,
      },
    })
  }

  const inputClass = 'mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20'

  return (
    <form onSubmit={submit} className="mt-4 space-y-4" aria-label="Audit creation form">
      <Field label="Título"><input className={inputClass} value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} /></Field>
      <Field label="Software"><input className={inputClass} value={form.software_name} onChange={(event) => setForm({ ...form, software_name: event.target.value })} /></Field>
      <Field label="Tipo"><input className={inputClass} value={form.software_type} onChange={(event) => setForm({ ...form, software_type: event.target.value })} /></Field>
      <Field label="Alcance"><textarea className={inputClass} rows={3} value={form.scope} onChange={(event) => setForm({ ...form, scope: event.target.value })} /></Field>
      <Field label="Objetivo"><textarea className={inputClass} rows={3} value={form.objective} onChange={(event) => setForm({ ...form, objective: event.target.value })} /></Field>
      <Field label="Stakeholders"><input className={inputClass} value={form.stakeholders} onChange={(event) => setForm({ ...form, stakeholders: event.target.value })} /></Field>
      <Field label="Sistemas"><input className={inputClass} value={form.systems} onChange={(event) => setForm({ ...form, systems: event.target.value })} /></Field>
      <Field label="Riesgos"><input className={inputClass} value={form.risks} onChange={(event) => setForm({ ...form, risks: event.target.value })} /></Field>
      <Field label="Metas de cumplimiento"><input className={inputClass} value={form.compliance_goals} onChange={(event) => setForm({ ...form, compliance_goals: event.target.value })} /></Field>
      <Field label="Notas"><textarea className={inputClass} rows={2} value={form.notes} onChange={(event) => setForm({ ...form, notes: event.target.value })} /></Field>
      <button type="submit" disabled={busy} className="w-full rounded-xl bg-ink px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60">
        {busy ? 'Procesando...' : 'Crear auditoría'}
      </button>
    </form>
  )
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="block text-sm font-medium text-slate-700">
      {label}
      {children}
    </label>
  )
}
