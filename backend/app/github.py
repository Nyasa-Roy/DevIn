import httpx


class GitHubClient:
    base_url = "https://api.github.com"

    def __init__(self, token: str):
        self._client = httpx.AsyncClient(timeout=15, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, **params):
        response = await self._client.get(f"{self.base_url}{path}", params=params or None)
        response.raise_for_status()
        return response.json()

    async def repositories(self) -> list[dict]:
        return await self._get("/user/repos", per_page=100, sort="updated")

    async def repository(self, full_name: str) -> dict:
        return await self._get(f"/repos/{full_name}")

    async def repository_snapshot(self, full_name: str, default_branch: str) -> dict:
        branches, commits, pulls, issues = await self._get(f"/repos/{full_name}/branches", per_page=100), await self._get(f"/repos/{full_name}/commits", per_page=100), await self._get(f"/repos/{full_name}/pulls", state="all", per_page=100), await self._get(f"/repos/{full_name}/issues", state="all", per_page=100)
        return {"default_branch": default_branch, "branches": branches, "commits": commits, "pull_requests": pulls, "issues": [issue for issue in issues if "pull_request" not in issue]}
