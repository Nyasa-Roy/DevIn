# Machine learning

Phase 8 defines deterministic PR features and the historical risk label: reverted PRs, bug-related issues, or at least two significant follow-up fixes are labelled risky. Phase 9 provides a Logistic Regression baseline with precision, recall, F1, ROC-AUC, and PR-AUC evaluation and joblib serialization. Phase 10 exposes explainable risk scores through the backend. Phase 11 adds an Isolation Forest detector; semantic retrieval currently uses a lexical baseline until source chunk embeddings and pgvector are introduced.

Risk predictions are assessments for review prioritisation, not guarantees of defects.
