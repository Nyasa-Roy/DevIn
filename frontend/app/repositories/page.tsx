import Link from "next/link";

const repositories = ["devinsight-api", "frontend-platform", "data-pipeline", "mobile-app"];

export default function RepositoriesPage() {
  return <div className="content"><div className="page-heading"><div><div className="eyebrow">Workspace</div><h1>Repositories</h1><p className="subtle">Connect and monitor the repositories your team cares about.</p></div><button className="button">+ Connect repository</button></div><div className="card"><div className="card-heading"><h2>Connected repositories <span style={{ color: "var(--muted)", fontWeight: 400 }}>({repositories.length})</span></h2><input className="search" placeholder="Search repositories" aria-label="Search repositories" /></div><div className="repo-list">{repositories.map((repo, index) => <Link className="repo-row" href={`/repositories/${repo}`} key={repo}><div><strong>{repo}</strong><span>github.com/devinsight/{repo} · Last synced {index + 1} hour{index ? "s" : ""} ago</span></div><span className="badge">Connected</span></Link>)}</div></div></div>;
}
