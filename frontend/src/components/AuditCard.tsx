import type { AuditSummary } from '../types'

export function AuditCard({ audit, active, onSelect }: { audit: AuditSummary; active: boolean; onSelect: (id: string) => void }) {
  return (
    <button
      type="button"
      onClick={() => onSelect(audit.id)}
      className={`w-full rounded-2xl border p-4 text-left transition focus:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
        active ? 'border-accent bg-accent/5 shadow-sm' : 'border-slate-200 bg-white hover:border-slate-300'
      }`}
      aria-pressed={active}
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-bold text-slate-900">{audit.title}</p>
          <p className="mt-1 text-xs text-slate-600">{audit.software_name}</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-slate-700">
          {audit.current_phase}
        </span>
      </div>
    </button>
  )
}
