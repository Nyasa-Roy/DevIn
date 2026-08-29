"use client";

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) { return <div className="content"><div className="error-state"><strong>We couldn&apos;t load this repository.</strong><p>Please try again or check the backend connection.</p><button className="button secondary" onClick={() => reset()}>Try again</button></div></div>; }
