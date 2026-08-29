from app.models import PullRequest
from app.services.risk import predict_risk


def test_risk_prediction_includes_explainable_factors() -> None:
    result = predict_risk(PullRequest(id=7, repository_id=1, github_number=42, title="Large refactor", state="open", additions=500, deletions=100, changed_files=14, reviews=1))
    assert result["risk_level"] == "HIGH"
    assert result["risk_percent"] > 50
    assert len(result["explanations"]) >= 2
