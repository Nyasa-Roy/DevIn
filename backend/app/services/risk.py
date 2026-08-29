from app.models import PullRequest


def predict_risk(pr: PullRequest) -> dict:
    changed = pr.additions + pr.deletions
    score = min(0.97, max(0.05, 0.12 + min(changed / 2500, 0.55) + min(pr.changed_files / 30, 0.22) - min(pr.reviews / 10, 0.12)))
    factors = []
    if pr.changed_files >= 10:
        factors.append(f"{pr.changed_files} files changed")
    if changed >= 400:
        factors.append(f"Large change surface ({changed} lines)")
    if pr.reviews < 2:
        factors.append("Limited review coverage")
    if not factors:
        factors.append("Small change surface with normal review coverage")
    level = "HIGH" if score >= 0.65 else "MEDIUM" if score >= 0.35 else "LOW"
    return {"pull_request_id": pr.id, "github_number": pr.github_number, "risk_score": round(score, 4), "risk_percent": round(score * 100, 1), "risk_level": level, "explanations": factors, "model": "baseline-heuristic"}
