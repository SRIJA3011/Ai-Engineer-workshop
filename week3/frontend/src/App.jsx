import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null); // NEW: Track Session ID

  // Send Message
  async function send() {
    if (!text) return;
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, session_id: sessionId }), // Pass session_id
      });
      const data = await res.json();
      setResponse(data.reply);
      setSessionId(data.session_id); // Save the session_id returned by backend
      setText(""); // Clear input
    } catch (e) {
      setResponse("⚠️ Error: " + e.message);
    } finally {
      setLoading(false);
    }
  }

  // Start New Chat
  async function newChat() {
    try {
      const res = await fetch("http://localhost:8000/new-chat", { method: "POST" });
      const data = await res.json();
      setSessionId(data.session_id);
      setResponse(""); // Clear chat window
      setText("");
    } catch (e) {
      alert("Error starting new chat");
    }
  }

  return (
    <div style={{ padding: 20, maxWidth: "600px", margin: "auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>AI Support Chat</h2>
        <button onClick={newChat} style={{ padding: "8px", background: "#ff4d4d", color: "white", border: "none", borderRadius: "4px" }}>
          + New Chat
        </button>
      </div>
      
      <p style={{ fontSize: "12px", color: "gray" }}>Session ID: {sessionId || "None yet"}</p>

      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input 
          style={{ flex: 1, padding: "8px" }}
          value={text} 
          onChange={(e) => setText(e.target.value)} 
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder="Type a message..."
        />
        <button onClick={send} disabled={loading} style={{ padding: "8px 16px" }}>
          {loading ? "Thinking…" : "Send"}
        </button>
      </div>

      <div style={{ padding: "15px", border: "1px solid #ccc", borderRadius: "5px", minHeight: "100px" }}>
        <ReactMarkdown>{response}</ReactMarkdown>
      </div>
    </div>
  );
}