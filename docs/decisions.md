# Architecture decisions

## ADR-001: PostgreSQL is the system of record

PostgreSQL provides transactions, mature relational querying, and a straightforward path to pgvector for semantic search. SQLite is supported only as a local test adapter.

## ADR-002: FastAPI is the backend boundary

FastAPI provides typed request/response contracts, async-friendly endpoints, and generated OpenAPI documentation while keeping Python close to the data and ML layers.

## ADR-003: Celery handles repository synchronisation

GitHub API work can be slow and rate-limited, so sync requests enqueue durable jobs in Redis and return a job identifier immediately.

## ADR-004: Logistic Regression is the first risk baseline

It is fast, reproducible, and interpretable. More complex models can be compared only after a reliable historical dataset and evaluation split exist.

## ADR-005: Search begins with a lexical baseline

A deterministic lexical retriever keeps the API useful before embedding infrastructure is available. It can later be replaced or augmented by sentence-transformer embeddings stored in pgvector.
