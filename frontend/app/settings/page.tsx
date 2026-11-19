"use client";

import { useEffect, useState } from "react";
import { CurrentUser, getCurrentUser, logout } from "../../lib/api";

export default function SettingsPage() {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loggingOut, setLoggingOut] = useState(false);

  useEffect(() => { getCurrentUser().then(setUser).catch((reason: Error) => setError(reason.message)); }, []);

  async function signOut() {
    setLoggingOut(true);
    setError(null);
    try { await logout(); window.location.assign("/login"); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Logout failed"); setLoggingOut(false); }
  }

  return <div className="content"><div className="page-heading"><div><div className="eyebrow">Account</div><h1>Settings</h1><p className="subtle">Review the GitHub account connected to this local DevInsight session.</p></div></div>{error && <div className="error-state" style={{ marginBottom: 18 }}>{error}</div>}<section className="grid two-col"><article className="card"><div className="card-heading"><h2>GitHub connection</h2><span className="badge">{user ? "Connected" : "Unavailable"}</span></div><div className="settings-list"><div><span className="subtle">Account</span><strong>{user?.login ?? "No active GitHub session"}</strong></div><div><span className="subtle">GitHub user ID</span><strong>{user?.github_id ?? "—"}</strong></div><div><span className="subtle">Token storage</span><strong>Encrypted on the backend</strong></div></div></article><article className="card"><div className="card-heading"><h2>Session</h2></div><p className="subtle">Logging out clears the DevInsight browser session. It does not revoke the OAuth application from your GitHub account.</p><button className="button secondary" onClick={signOut} disabled={loggingOut}>{loggingOut ? "Logging out…" : "Log out of DevInsight"}</button></article></section></div>;
}
