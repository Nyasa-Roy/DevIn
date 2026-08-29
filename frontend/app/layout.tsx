import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "../components/app-shell";

export const metadata: Metadata = {
  title: "DevInsight | Engineering intelligence",
  description: "Understand repository health, activity, and pull-request risk.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
