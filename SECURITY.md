# Security policy

## Local development

Keep `backend/.env` outside Git. Never paste `GITHUB_CLIENT_SECRET`, access tokens, database passwords, or production `SECRET_KEY` into issues or chat. The repository ignores `.env` files and local databases.

## Production requirements

- Set a random `SECRET_KEY` of at least 32 characters.
- Use HTTPS for the frontend and OAuth callback.
- Store secrets in a managed secret store, not in images or Compose files.
- Use the minimum GitHub permissions required; prefer a GitHub App for production.
- Keep PostgreSQL and Redis on private networks.
- Enable dependency, secret, and container scanning in CI.
- Rotate the GitHub client secret and encryption key according to an incident-response plan.

## Reporting

Do not disclose a suspected token or credential publicly. Revoke the credential first, then report the issue privately to the repository owner.
