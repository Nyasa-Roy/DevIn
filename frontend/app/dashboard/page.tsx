"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getRepositories, getRepositoryActivity, getRepositoryOverview, GithubRepository, RepositoryActivity, RepositoryOverview } from "../../lib/api";
import { StatCard } from "../../components/stat-card";

type ConnectedRepository = { repository: GithubRepository; overview: RepositoryOverview; activity: RepositoryActivity };

export default function DashboardPage() {
  const [repositories, setRepositories] = useState<ConnectedRepository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getRepositories().then(async (items) => {
      const connected = items.filter((item) => item.connected && item.repository_id);
      const details = await Promise.all(connected.map(async (repository) => {
        const repositoryId = repository.repository_id as number;
        const [overview, activity] = await Promise.all([getRepositoryOverview(repositoryId), getRepositoryActivity(repositoryId)]);
        return { repository, overview, activity };
      }));
      setRepositories(details);
    }).catch((reason: Error) => setError(reason.message)).finally(() => setLoading(false));
  }, []);

  const totals = useMemo(() => ({
    openPullRequests: repositories.reduce((sum, item) => sum + item.overview.open_pull_requests, 0),
    openIssues: repositories.reduce((sum, item) => sum + item.overview.open_issues, 0),
    commits: repositories.reduce((sum, item) => sum + item.overview.commits, 0),
    health: repositories.length ? Math.round(repositories.reduce((sum, item) => sum + item.overview.health_score, 0) / repositories.length) : 0,
  }), [repositories]);
  const recent = repositories.flatMap((item) => item.activity.commits.map((commit) => ({ ...commit, repository: item.repository.full_name }))).sort((left, right) => (right.committed_at ?? "").localeCompare(left.committed_at ?? "")).slice(0, 6);

  return <div className="content"><div className="page-heading"><div><div className="eyebrow">Workspace overview</div><h1>DevInsight workspace</h1><p className="subtle">Live information from repositories connected to your GitHub account.</p></div><Link className="button" href="/repositories">+ Connect repository</Link></div>{error && <div className="error-state" style={{ marginBottom: 18 }}>{error}</div>}<section className="grid stat-grid" aria-label="Workspace statistics"><StatCard label="Connected repositories" value={loading ? "—" : String(repositories.length)} trend="GitHub repositories" /><StatCard label="Open pull requests" value={loading ? "—" : String(totals.openPullRequests)} trend="Across connected repositories" /><StatCard label="Recent commits" value={loading ? "—" : String(totals.commits)} trend="Current analytics window" /><StatCard label="Average health score" value={loading ? "—" : String(totals.health)} trend="Out of 100" /></section><section className="grid two-col"><article className="card"><div className="card-heading"><h2>Recent activity</h2><Link href="/activity">View all</Link></div>{loading ? <div className="empty-state"><p className="subtle">Loading activity…</p></div> : recent.length === 0 ? <div className="empty-state"><p className="subtle">Sync a connected repository to load activity.</p></div> : <div className="activity-list">{recent.map((commit) => <div className="activity-item" key={`${commit.repository}-${commit.sha}`}><div className="activity-icon">↗</div><div><strong>{commit.message || "Commit without a message"}</strong><span>{commit.repository} · {commit.author ?? "Unknown author"}</span></div></div>)}</div>}</article><article className="card"><div className="card-heading"><h2>Workspace totals</h2><span className="badge">Live</span></div><div className="legend"><div><b>{totals.openPullRequests}</b><span>Open PRs</span></div><div><b>{totals.openIssues}</b><span>Open issues</span></div><div><b>{totals.commits}</b><span>Commits</span></div></div></article></section><section className="card" style={{ marginTop: 18 }}><div className="card-heading"><h2>Connected repositories</h2><Link href="/repositories">Manage repositories</Link></div>{loading ? <div className="empty-state"><p className="subtle">Loading repositories…</p></div> : repositories.length === 0 ? <div className="empty-state"><p className="subtle">No connected repositories yet.</p></div> : <div className="repo-list">{repositories.map(({ repository, overview }) => <Link className="repo-row" href={`/repositories/${repository.repository_id}`} key={repository.id}><div><strong>{repository.full_name}</strong><span>{overview.commits} commits · {overview.open_pull_requests} open pull requests</span></div><span className="badge">Health · {overview.health_score}</span></Link>)}</div>}</section></div>;
}
