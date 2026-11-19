"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getRepositories, getRepositoryActivity, getRepositoryOverview } from "../../lib/api";

type ActivityItem = { repositoryId: number; name: string; commits: Awaited<ReturnType<typeof getRepositoryActivity>>["commits"]; commitCount: number; error?: string };

export default function ActivityPage() {
  const [items, setItems] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const repositories = (await getRepositories()).filter((repository) => repository.connected && repository.repository_id);
        const loaded = await Promise.all(repositories.map(async (repository) => {
          const repositoryId = repository.repository_id as number;
          try {
            const [activity, overview] = await Promise.all([getRepositoryActivity(repositoryId), getRepositoryOverview(repositoryId)]);
            return { repositoryId, name: repository.full_name, commits: activity.commits.slice(0, 5), commitCount: overview.commits };
          } catch (reason) {
            return { repositoryId, name: repository.full_name, commits: [], commitCount: 0, error: reason instanceof Error ? reason.message : "Could not load activity" };
          }
        }));
        setItems(loaded);
      } catch (reason) {
        setError(reason instanceof Error ? reason.message : "Could not load repositories");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return <div className="content"><div className="page-heading"><div><div className="eyebrow">GitHub activity</div><h1>Activity</h1><p className="subtle">Recent commits stored by DevInsight after repository synchronisation.</p></div><Link className="button" href="/repositories">Manage repositories</Link></div>{error && <div className="error-state">{error}</div>}{loading ? <div className="card empty-state"><p className="subtle">Loading repository activity…</p></div> : items.length === 0 ? <div className="card empty-state"><p className="subtle">Connect and sync a repository to see activity here.</p></div> : <div className="grid two-col">{items.map((item) => <article className="card" key={item.repositoryId}><div className="card-heading"><div><h2>{item.name}</h2><span className="subtle">{item.commitCount} commits in the current analytics window</span></div><Link className="badge" href={`/repositories/${item.repositoryId}`}>Open repository</Link></div>{item.error ? <div className="error-state">{item.error}</div> : item.commits.length === 0 ? <div className="empty-state"><p className="subtle">No activity stored yet. Open the repository and run a sync.</p></div> : <div className="activity-list">{item.commits.map((commit) => <div className="activity-item" key={commit.sha}><div className="activity-icon">↗</div><div><strong>{commit.message || "Commit without a message"}</strong><span>{commit.author ?? "Unknown author"} · {commit.committed_at ? new Date(commit.committed_at).toLocaleString() : "Date unavailable"}</span></div></div>)}</div>}</article>)}</div>}</div>;
}
