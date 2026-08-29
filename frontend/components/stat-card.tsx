export function StatCard({ label, value, trend }: { label: string; value: string; trend: string }) {
  return <article className="card stat-card"><div className="label">{label}</div><div className="value">{value}</div><div className="trend">↗ {trend}</div></article>;
}
