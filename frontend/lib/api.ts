const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
let csrfTokenValue: string | null = null;

export type GithubRepository = { id: number; repository_id: number | null; name: string; full_name: string; html_url: string; private: boolean; connected: boolean };
export type RepositoryOverview = { repository_id: number; period_days: number; health_score: number; commits: number; pull_requests: number; open_pull_requests: number; merged_pull_requests: number; issues: number; open_issues: number; contributors: number; average_pr_size: number };
export type RepositoryActivity = { commits: Array<{ sha: string; author: string | null; message: string; committed_at: string | null }> };

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const method = options?.method?.toUpperCase() ?? "GET";
  if (method !== "GET" && method !== "HEAD") {
    if (!csrfTokenValue) csrfTokenValue = (await fetch(`${API_URL}/auth/csrf`, { credentials: "include" }).then((response) => response.json())).csrf_token;
  }
  const response = await fetch(`${API_URL}${path}`, { ...options, credentials: "include", headers: { "Content-Type": "application/json", ...(csrfTokenValue ? { "X-CSRF-Token": csrfTokenValue } : {}), ...options?.headers } });
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? `Request failed (${response.status})`);
  return response.status === 204 ? (undefined as T) : response.json();
}

export const getRepositories = () => request<GithubRepository[]>("/repositories");
export const connectRepository = (id: number) => request<{ id: number; github_id: number; full_name: string; connected: boolean }>(`/repositories/${id}/connect`, { method: "POST" });
export const getRepositoryOverview = (id: number) => request<RepositoryOverview>(`/repositories/${id}/overview`);
export const getRepositoryActivity = (id: number) => request<RepositoryActivity>(`/repositories/${id}/activity`);
export const syncRepository = (id: number) => request<{ job_id: string; repository_id: number; status: string }>(`/repositories/${id}/sync`, { method: "POST" });
export const getSyncStatus = (repositoryId: number, jobId: string) => request<{ status: string; error: string | null }>(`/repositories/${repositoryId}/sync/${jobId}`);
