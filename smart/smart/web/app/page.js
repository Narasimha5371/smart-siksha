import Link from "next/link";

export default function HomePage() {
  return (
    <main className="shell" style={{ display: "grid", gap: 24 }}>
      <section className="panel" style={{ padding: 24 }}>
        <p style={{ margin: 0, color: "var(--amber)", fontWeight: 800 }}>Smart Shiksha</p>
        <h1 className="headline" style={{ fontSize: "clamp(2rem, 8vw, 4rem)", marginBottom: 8 }}>
          Curriculum-Locked AI Tutor for Every Student
        </h1>
        <p style={{ color: "var(--ink-muted)", maxWidth: 740 }}>
          Cross-platform learning with retrieval-grounded tutoring from NCERT and State Board content.
          Built for reliable classroom and home learning.
        </p>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 18 }}>
          <Link href="/student" className="btn btn-primary">Open Student Portal</Link>
          <Link href="/teacher" className="btn btn-outline">Open Teacher Dashboard</Link>
        </div>
      </section>

      <section className="kpi-grid">
        <article className="panel" style={{ padding: 18 }}>
          <h3 className="headline" style={{ marginTop: 0 }}>RAG Tutor</h3>
          <p style={{ color: "var(--ink-muted)", marginBottom: 0 }}>Answers only from indexed syllabus chunks.</p>
        </article>
        <article className="panel" style={{ padding: 18 }}>
          <h3 className="headline" style={{ marginTop: 0 }}>Teacher Controls</h3>
          <p style={{ color: "var(--ink-muted)", marginBottom: 0 }}>Upload PDFs and retrain index on demand.</p>
        </article>
        <article className="panel" style={{ padding: 18 }}>
          <h3 className="headline" style={{ marginTop: 0 }}>Student Experience</h3>
          <p style={{ color: "var(--ink-muted)", marginBottom: 0 }}>Desktop split view: chat + textbook references.</p>
        </article>
      </section>
    </main>
  );
}
