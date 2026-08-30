"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { connectRepository, getRepositories, GithubRepository } from "../../lib/api";

export default function RepositoriesPage() {
  const [repositories, setRepositories] = useState<GithubRepository[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [connecting, setConnecting] = useState<number | null>(null);

  useEffect(() => { getRepositories().then(setRepositories).catch((reason: Error) => setError(reason.message)).finally(() => setLoading(false)); }, []);

  async function connect(id: number) {
    setConnecting(id); setError(null);
    try { await connectRepository(id); setRepositories((current) => current.map((repository) => repository.id === id ? { ...repository, connected: true } : repository)); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Could not connect repository"); }
    finally { setConnecting(null); }
  }

  const filtered = repositories.filter((repository) => repository.full_name.toLowerCase().includes(query.toLowerCase()));
  return <div className="content"><div className="page-heading"><div><div className="eyebrow">GitHub workspace</div><h1>Repositories</h1><p className="subtle">Choose a repository to bring its engineering data into DevInsight.</p></div></div>{error && <div className="error-state" style={{ marginBottom: 18 }}>{error}</div>}<div className="card"><div className="card-heading"><h2>Accessible repositories <span style={{ color: "var(--muted)", fontWeight: 400 }}>({loading ? "…" : filtered.length})</span></h2><input className="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search repositories" aria-label="Search repositories" /></div>{loading ? <div className="empty-state"><p className="subtle">Loading your GitHub repositories…</p></div> : filtered.length === 0 ? <div className="empty-state"><p className="subtle">No repositories matched your search.</p></div> : <div className="repo-list">{filtered.map((repository) => <div className="repo-row" key={repository.id}><div><strong>{repository.full_name}</strong><span>{repository.private ? "Private" : "Public"} · <a href={repository.html_url} target="_blank" rel="noreferrer">View on GitHub</a></span></div>{repository.connected ? <Link className="badge" href={`/repositories/${repository.name}`}>Connected · Open</Link> : <button className="button" disabled={connecting === repository.id} onClick={() => connect(repository.id)}>{connecting === repository.id ? "Connecting…" : "Connect"}</button>}</div>)}</div>}</div></div>;
}
