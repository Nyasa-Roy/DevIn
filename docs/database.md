# Database design

The planned relational model is centred on `users` and `repositories`.

Core entities: users, repositories, repository_members, commits, contributors, pull_requests, pull_request_files, pull_request_reviews, issues, files, file_metrics, repository_metrics, pr_features, ml_predictions, anomalies, and embeddings.

Phase 1 establishes the connection layer and migration-ready SQLAlchemy base. Models are introduced alongside the GitHub integration in Phase 4 so that imported data contracts are defined from the API responses rather than guessed in isolation.

PostgreSQL is the production database. SQLite remains supported through `DATABASE_URL` for local tests and smoke checks.
