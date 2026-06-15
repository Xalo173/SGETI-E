export type AuditSummary = {
  id: string
  title: string
  software_name: string
  current_phase: string
  report_status: string
  created_at: string
}

export type AuditPlan = {
  title: string
  summary: string
  methodology: string
  standards_used: Array<{ norm: string; section?: string; rationale: string }>
  steps: Array<{ step: string; description: string; deliverables?: string[]; owner?: string }>
  criteria: Array<{ criterion: string; metric: string; evidence?: string }>
}

export type Audit = {
  id: string
  title: string
  software_name: string
  software_type: string
  scope: string
  objective: string
  context: Record<string, unknown>
  current_phase: string
  plan_summary: string | null
  plan_citations: Array<{ source: string; title: string; excerpt: string }> | null
  report_status: string
  report_file_path: string | null
  created_at: string
  updated_at: string
  plan: AuditPlan | null
  findings: Array<{ id: string; severity: string; title: string; description: string; evidence?: string | null; recommendation?: string | null; created_at: string }>
}
