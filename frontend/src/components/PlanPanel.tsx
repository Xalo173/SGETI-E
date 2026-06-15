import type { Audit, AuditPlan } from '../types'

export function PlanPanel({ audit, plan, onGeneratePlan, busy }: { audit: Audit | null; plan: AuditPlan | null; onGeneratePlan: () => Promise<void>; busy: boolean }) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Plan panel">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold">Diseño de evaluación</h2>
          <p className="mt-1 text-sm text-slate-600">RAG con cita de normas usadas para el plan.</p>
        </div>
        <button type="button" onClick={onGeneratePlan} disabled={!audit || busy} className="rounded-xl bg-warm px-4 py-2 text-sm font-semibold text-white transition hover:bg-amber-700 disabled:cursor-not-allowed disabled:opacity-60">
          Generar plan
        </button>
      </div>

      {!plan && <p className="mt-4 text-sm text-slate-500">Genera el plan para ver metodología, criterios y citas de normas.</p>}

      {plan && (
        <div className="mt-4 space-y-4">
          <div>
            <h3 className="text-lg font-semibold">{plan.title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-700">{plan.summary}</p>
          </div>

          <Block title="Metodología" value={plan.methodology} />

          <ListBlock title="Normas usadas" items={plan.standards_used.map((item) => `${item.norm}: ${item.rationale}`)} />
          <ListBlock title="Pasos" items={plan.steps.map((item) => `${item.step}. ${item.description}`)} />
          <ListBlock title="Criterios" items={plan.criteria.map((item) => `${item.criterion}: ${item.metric}`)} />
        </div>
      )}
    </section>
  )
}

function Block({ title, value }: { title: string; value: string }) {
  return (
    <div>
      <h4 className="text-sm font-semibold uppercase tracking-wide text-slate-500">{title}</h4>
      <p className="mt-2 rounded-2xl bg-slate-50 p-4 text-sm leading-6 text-slate-700">{value}</p>
    </div>
  )
}

function ListBlock({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <h4 className="text-sm font-semibold uppercase tracking-wide text-slate-500">{title}</h4>
      <ul className="mt-2 space-y-2">
        {items.map((item) => (
          <li key={item} className="rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-700">
            {item}
          </li>
        ))}
      </ul>
    </div>
  )
}
