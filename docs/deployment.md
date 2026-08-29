# Deployment

The supported production shape is container-based: deploy the Next.js image to a managed container service, the FastAPI and Celery images to separate services, and use managed PostgreSQL (with pgvector) and Redis. AWS ECS/Fargate, RDS, and ElastiCache are suitable targets without requiring Kubernetes.

Required production settings are `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `GITHUB_CLIENT_ID`, and `GITHUB_CLIENT_SECRET`. Secrets belong in the cloud secret manager, never in the image or repository.

The first deployment gate is the CI workflow: backend and ML tests, frontend build, and `docker compose config` should pass before publishing images.
