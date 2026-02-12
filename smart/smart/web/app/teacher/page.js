"use client";

import { useEffect, useMemo, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export default function TeacherDashboardPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("Choose a PDF, then upload to curriculum ingestion queue.");
  const [stats, setStats] = useState(null);
  const [statsError, setStatsError] = useState("");

  useEffect(() => {
    async function loadStats() {
      try {
        setStatsError("");
        const resp = await fetch(`${API_BASE}/dashboard/stats?user_id=teacher-web`);
        const data = await resp.json();
        if (!resp.ok) throw new Error(data?.detail || `HTTP ${resp.status}`);
        setStats(data);
      } catch (err) {
        setStatsError(`Stats error: ${err.message}`);
      }
    }

    loadStats();
  }, []);

  const avgScore = useMemo(() => {
    if (!stats?.progress_vs_time?.length) return "--";
    const total = stats.progress_vs_time.reduce((sum, row) => sum + Number(row.score || 0), 0);
    return `${Math.round(total / stats.progress_vs_time.length)}%`;
  }, [stats]);

  const weakTopicsLabel = useMemo(() => {
    if (!stats?.weak_topics?.length) return "None";
    return stats.weak_topics.join(", ");
  }, [stats]);

  const streakLabel = useMemo(() => {
    if (typeof stats?.daily_streak !== "number") return "--";
    return `${stats.daily_streak} days`;
  }, [stats]);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading...");
    try {
      const resp = await fetch(`${API_BASE}/teacher/upload-curriculum`, {
        method: "POST",
        body: formData,
      });
      const data = await resp.json();
      if (!resp.ok) throw new Error(data?.detail || "Upload failed");
      setStatus(`${data.message} Saved at: ${data.file}`);
    } catch (err) {
      setStatus(`Upload error: ${err.message}`);
    }
  }

  return (
    <main className="shell" style={{ display: "grid", gap: 14 }}>
      <header className="panel" style={{ padding: 16 }}>
        <h1 className="headline" style={{ margin: 0 }}>Teacher Dashboard</h1>
        <p style={{ margin: "6px 0 0", color: "var(--ink-muted)" }}>
          Upload PDFs and monitor class-level learning signals.
        </p>
      </header>

      <section className="kpi-grid">
        <article className="panel" style={{ padding: 16 }}>
          <h3 className="headline" style={{ margin: 0 }}>Average Score</h3>
          <p style={{ fontSize: 34, margin: "8px 0 0" }}>{avgScore}</p>
        </article>
        <article className="panel" style={{ padding: 16 }}>
          <h3 className="headline" style={{ margin: 0 }}>Daily Streak</h3>
          <p style={{ fontSize: 34, margin: "8px 0 0" }}>{streakLabel}</p>
        </article>
        <article className="panel" style={{ padding: 16 }}>
          <h3 className="headline" style={{ margin: 0 }}>Weak Topic Cluster</h3>
          <p style={{ margin: "8px 0 0", color: "var(--ink-muted)" }}>{weakTopicsLabel}</p>
        </article>
      </section>
      {statsError ? (
        <section className="panel" style={{ padding: 16, borderColor: "rgba(255,130,130,.55)" }}>
          <p style={{ margin: 0, color: "#ffb4b4" }}>{statsError}</p>
        </section>
      ) : null}

      <section className="panel" style={{ padding: 16 }}>
        <h2 className="headline" style={{ marginTop: 0 }}>Upload Curriculum PDF</h2>
        <form onSubmit={handleUpload} style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
          <input
            type="file"
            accept=".pdf,.txt,.md"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            style={{ color: "var(--ink-muted)" }}
          />
          <button className="btn btn-primary" type="submit">Upload</button>
        </form>
        <p style={{ color: "var(--ink-muted)", marginBottom: 0 }}>{status}</p>
      </section>

      <section className="panel" style={{ padding: 16 }}>
        <h2 className="headline" style={{ marginTop: 0 }}>Training Pipeline</h2>
        <ol style={{ color: "var(--ink-muted)", marginBottom: 0 }}>
          <li>Upload textbook files from this page.</li>
          <li>Run `python backend/train_ai.py` on the server.</li>
          <li>New chunks become available for `/chat/message` retrieval.</li>
        </ol>
      </section>
    </main>
  );
}
