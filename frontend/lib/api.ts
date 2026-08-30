const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type GithubRepository = { id: number; name: string; full_name: string; html_url: string; private: boolean; connected: boolean };

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...options, credentials: "include", headers: { "Content-Type": "application/json", ...options?.headers } });
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? `Request failed (${response.status})`);
  return response.status === 204 ? (undefined as T) : response.json();
}

export const getRepositories = () => request<GithubRepository[]>("/repositories");
export const connectRepository = (id: number) => request<{ id: number; full_name: string; connected: boolean }>(`/repositories/${id}/connect`, { method: "POST" });
