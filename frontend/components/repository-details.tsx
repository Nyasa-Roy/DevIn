"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getRepositoryActivity, getRepositoryOverview, RepositoryActivity, RepositoryOverview } from "../lib/api";
import { SyncButton } from "./sync-button";

export function RepositoryDetails({ repositoryId }: { repositoryId: number }) {
  const [overview, setOverview] = useState<RepositoryOverview | null>(null);
  const [activity, setActivity] = useState<RepositoryActivity | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getRepositoryOverview(repositoryId), getRepositoryActivity(repositoryId)])
      .then(([nextOverview, nextActivity]) => { setOverview(nextOverview); setActivity(nextActivity); })
      .catch((reason: Error) => setError(reason.message));
  }, [repositoryId]);

  const value = (field: keyof RepositoryOverview) => overview ? overview[field] : "—";
  return <div className="content"><div className="page-heading"><div><Link className="eyebrow" href="/repositories">← All repositories</Link><h1>Repository overview</h1><p className="subtle">Live data from the connected GitHub repository.</p></div><SyncButton repositoryId={repositoryId} /></div>{error && <div className="error-state" style={{ marginBottom: 18 }}>{error}</div>}<section className="grid stat-grid"><article className="card stat-card"><div className="label">Health score</div><div className="value">{value("health_score")} / 100</div><div className="trend">Based on the last {value("period_days")} days</div></article><article className="card stat-card"><div className="label">Open pull requests</div><div className="value">{value("open_pull_requests")}</div><div className="trend">{value("pull_requests")} total pull requests</div></article><article className="card stat-card"><div className="label">Open issues</div><div className="value">{value("open_issues")}</div><div className="trend">{value("issues")} total issues</div></article><article className="card stat-card"><div className="label">Contributors</div><div className="value">{value("contributors")}</div><div className="trend">Across recent commits</div></article></section><section className="grid two-col"><article className="card"><div className="card-heading"><h2>Repository activity</h2><span className="subtle">{activity ? `${activity.commits.length} commits loaded` : "Loading…"}</span></div>{activity?.commits.length ? <div className="activity-list">{activity.commits.slice(0, 8).map((commit) => <div className="activity-item" key={commit.sha}><div className="activity-icon">↗</div><div><strong>{commit.message || "Commit without a message"}</strong><span>{commit.author ?? "Unknown author"} · {commit.committed_at ? new Date(commit.committed_at).toLocaleString() : "Date unavailable"}</span></div></div>)}</div> : <div className="empty-state"><p className="subtle">No commits are stored yet. Start a repository sync to load GitHub activity.</p></div>}</article><article className="card"><div className="card-heading"><h2>Repository totals</h2><span className="badge">Live</span></div><div className="legend"><div><b>{value("commits")}</b><span>Commits</span></div><div><b>{value("merged_pull_requests")}</b><span>Merged PRs</span></div><div><b>{value("average_pr_size")}</b><span>Avg. PR size</span></div></div></article></section></div>;
}
