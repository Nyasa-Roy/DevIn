"use client";

import { useState } from "react";
import { getSyncStatus, syncRepository } from "../lib/api";

export function SyncButton({ repositoryId }: { repositoryId: number }) {
  const [status, setStatus] = useState<"idle" | "queued" | "running" | "completed" | "failed">("idle");
  const [error, setError] = useState<string | null>(null);

  async function sync() {
    setError(null); setStatus("queued");
    try {
      const job = await syncRepository(repositoryId);
      const poll = async () => {
        const result = await getSyncStatus(repositoryId, job.job_id);
        setStatus(result.status as typeof status);
        if (result.status === "queued" || result.status === "running") window.setTimeout(poll, 1500);
        if (result.status === "failed") setError(result.error ?? "Sync failed");
      };
      await poll();
    } catch (reason) { setStatus("failed"); setError(reason instanceof Error ? reason.message : "Could not start sync"); }
  }

  return <div><button className="button secondary" onClick={sync} disabled={status === "queued" || status === "running"}>{status === "queued" ? "Queued…" : status === "running" ? "Syncing…" : status === "completed" ? "Sync completed" : "Sync repository"}</button>{error && <div className="sync-error">{error}</div>}</div>;
}
