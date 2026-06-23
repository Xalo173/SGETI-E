const phases = [
  { id: 'requirements', label: '1. Requerimiento' },
  { id: 'design', label: '2. Diseño' },
  { id: 'execution', label: '3. Ejecución' },
  { id: 'closed', label: 'Cierre' },
]

export function PhaseStepper({ currentPhase, onChangePhase, busy }: { currentPhase: string; onChangePhase: (phase: string) => void; busy: boolean }) {
  return (
    <section aria-label="Audit phases">
      <div className="flex flex-wrap gap-3">
        {phases.map((phase) => {
          const active = currentPhase === phase.id
          return (
            <button
              key={phase.id}
              type="button"
              onClick={() => onChangePhase(phase.id)}
              disabled={busy}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition focus:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
                active ? 'bg-accent text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
              aria-pressed={active}
            >
              {phase.label}
            </button>
          )
        })}
      </div>
      <p className="mt-3 text-sm text-slate-600">La navegación del flujo está pensada para teclado y lectores de pantalla.</p>
    </section>
  )
}
