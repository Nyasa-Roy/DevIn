"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { CurrentUser, getCurrentUser, logout } from "../lib/api";

const navigation = [
  { href: "/dashboard", label: "Overview", icon: "◈" },
  { href: "/repositories", label: "Repositories", icon: "▣" },
  { href: "/activity", label: "Activity", icon: "⌁" },
  { href: "/settings", label: "Settings", icon: "⚙" },
];

export function AppShell({ children }: Readonly<{ children: React.ReactNode }>) {
  const pathname = usePathname();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loggingOut, setLoggingOut] = useState(false);
  const [logoutError, setLogoutError] = useState<string | null>(null);

  useEffect(() => { getCurrentUser().then(setUser).catch(() => setUser(null)); }, [pathname]);

  async function signOut() {
    setLoggingOut(true);
    setLogoutError(null);
    try {
      await logout();
      window.location.assign("/login");
    } catch (reason) {
      setLogoutError(reason instanceof Error ? reason.message : "Logout failed");
      setLoggingOut(false);
    }
  }

  if (pathname === "/login") return <>{children}</>;
  const initials = user?.login.slice(0, 2).toUpperCase() ?? "NR";
  return <div className="shell"><aside className="sidebar"><Link className="brand" href="/dashboard"><span className="brand-mark">D</span><span className="brand-name">DevInsight</span></Link><p className="nav-label">Workspace</p><nav className="nav" aria-label="Main navigation">{navigation.map((item) => <Link className={`nav-link${pathname.startsWith(item.href) ? " active" : ""}`} href={item.href} key={item.href}><span>{item.icon} &nbsp; {item.label}</span></Link>)}</nav><div className="sidebar-footer"><div className="profile"><span className="avatar">{initials}</span><div><strong>{user?.login ?? "GitHub user"}</strong><small>{user ? "Connected account" : "Session unavailable"}</small></div></div></div></aside><main className="main"><header className="topbar"><span className="topbar-title">Engineering intelligence / Workspace</span><div className="topbar-actions"><span className="status-dot">● Local demo</span>{logoutError && <span className="error-text">{logoutError}</span>}<button className="button secondary" data-testid="logout-button" onClick={signOut} disabled={loggingOut}>{loggingOut ? "Logging out…" : "Log out"}</button><span className="avatar">{initials}</span></div></header>{children}</main></div>;
}
