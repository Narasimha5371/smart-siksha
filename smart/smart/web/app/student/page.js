"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export default function StudentPortalPage() {
  const [text, setText] = useState("");
  const [messages, setMessages] = useState([
    { from: "ai", text: "Welcome. Ask a question from your textbook chapter." },
  ]);
  const [contextChunks, setContextChunks] = useState([
    "Ask a curriculum question to view retrieved textbook references here.",
  ]);
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (!text.trim() || loading) return;
    const input = text.trim();
    setText("");
    setMessages((prev) => [...prev, { from: "user", text: input }]);
    setLoading(true);

    try {
      const resp = await fetch(`${API_BASE}/chat/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "demo-student",
          session_id: "student-web-session",
          message: input,
          language: "en",
        }),
      });

      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      setMessages((prev) => [...prev, { from: "ai", text: data.text }]);
      if (Array.isArray(data.context_chunks) && data.context_chunks.length) {
        setContextChunks(data.context_chunks);
      } else {
        setContextChunks(["No textbook context was returned for this question."]);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { from: "ai", text: `Request failed: ${err.message}` }]);
      setContextChunks(["Unable to load references due to a request error."]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell" style={{ display: "grid", gap: 16 }}>
      <header className="panel" style={{ padding: 16 }}>
        <h1 className="headline" style={{ margin: 0 }}>Student Portal</h1>
        <p style={{ margin: "6px 0 0", color: "var(--ink-muted)" }}>
          Left: chat tutor. Right: textbook references.
        </p>
      </header>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "1.2fr 1fr",
          gap: 14,
        }}
      >
        <article className="panel" style={{ display: "grid", gridTemplateRows: "1fr auto", minHeight: "68vh" }}>
          <div style={{ padding: 16, overflowY: "auto", display: "grid", gap: 10 }}>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                style={{
                  justifySelf: msg.from === "user" ? "end" : "start",
                  maxWidth: "75%",
                  padding: "10px 12px",
                  borderRadius: 12,
                  background: msg.from === "user" ? "rgba(91,181,255,.20)" : "rgba(54,223,179,.17)",
                  border: "1px solid var(--line)",
                }}
              >
                {msg.text}
              </div>
            ))}
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 8, padding: 12, borderTop: "1px solid var(--line)" }}>
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Ask about this chapter..."
              style={{
                borderRadius: 10,
                border: "1px solid var(--line)",
                background: "rgba(7,20,33,.8)",
                color: "var(--ink)",
                padding: "10px 12px",
              }}
            />
            <button className="btn btn-primary" onClick={sendMessage} disabled={loading}>
              {loading ? "..." : "Send"}
            </button>
          </div>
        </article>

        <aside className="panel" style={{ padding: 16 }}>
          <h2 className="headline" style={{ marginTop: 0 }}>Textbook Reference</h2>
          <div style={{ display: "grid", gap: 10 }}>
            {contextChunks.map((chunk, idx) => (
              <p key={idx} style={{ margin: 0, color: "var(--ink-muted)", lineHeight: 1.5 }}>
                {chunk}
              </p>
            ))}
          </div>
        </aside>
      </section>

      <style jsx>{`
        @media (max-width: 980px) {
          section {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </main>
  );
}
