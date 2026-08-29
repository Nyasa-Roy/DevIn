import Link from "next/link";

export default function LoginPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  return <main className="login-page"><div className="login-card card"><div className="brand login-brand"><span className="brand-mark">D</span><span className="brand-name" style={{ color: "var(--ink)" }}>DevInsight</span></div><div className="eyebrow">Engineering intelligence</div><h1>See how your team builds.</h1><p className="subtle">Connect GitHub to turn repository activity into clear, actionable insight.</p><a className="button github-button" href={`${apiUrl}/auth/github`}>Continue with GitHub</a><p className="login-note">You&apos;ll be redirected to GitHub to authorize access. DevInsight never exposes your access token to the browser.</p><Link className="back-link" href="/">← Back to home</Link></div></main>;
}
