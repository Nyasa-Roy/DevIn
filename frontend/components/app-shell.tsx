"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getCurrentUser, logout } from "../lib/api";

export function AppShell({ children }: Readonly<{ children: React.ReactNode }>) {
  const [signedIn, setSignedIn] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);

  useEffect(() => { getCurrentUser().then(() => setSignedIn(true)).catch(() => setSignedIn(false)); }, []);

  async function signOut() {
    setLoggingOut(true);
    try { await logout(); window.location.assign("/login"); }
    catch { setLoggingOut(false); }
  }

  return <div className="shell"><aside className="sidebar"><Link className="brand" href="/dashboard"><span className="brand-mark">D</span><span className="brand-name">DevInsight</span></Link><p className="nav-label">Workspace</p><nav className="nav" aria-label="Main navigation"><Link className="nav-link active" href="/dashboard"><span>◈ &nbsp; Overview</span></Link><Link className="nav-link" href="/repositories"><span>▣ &nbsp; Repositories</span></Link><Link className="nav-link" href="/dashboard"><span>⌁ &nbsp; Activity</span></Link><Link className="nav-link" href="/dashboard"><span>⚙ &nbsp; Settings</span></Link></nav><div className="sidebar-footer"><div className="profile"><span className="avatar">NR</span><div><strong>Nyasa Roy</strong><small>Engineering team</small></div></div></div></aside><main className="main"><header className="topbar"><span className="topbar-title">Engineering intelligence / Workspace</span><div className="topbar-actions"><span className="status-dot">● All systems operational</span>{signedIn && <button className="button secondary" onClick={signOut} disabled={loggingOut}>{loggingOut ? "Logging out…" : "Log out"}</button>}<span className="avatar">NR</span></div></header>{children}</main></div>;
}
