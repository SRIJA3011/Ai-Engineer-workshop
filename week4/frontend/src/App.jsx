
import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  const API_URL =
    import.meta.env.VITE_API_URL || "http://localhost:8000";

  const messagesEndRef = useRef(null);

  // Automatically scroll when messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // Send message
  async function sendMessage(e) {
    e.preventDefault();

    if (!input.trim() || loading) return;

    const userMessage = {
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          session_id: sessionId,
        }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);

      setSessionId(data.session_id);

    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Error connecting to server. Please try again.",
        },
      ]);

    } finally {
      setLoading(false);
    }
  }

  // Start a new chat
  async function startNewChat() {
    if (loading) return;

    try {
      const res = await fetch(`${API_URL}/new-chat`, {
        method: "POST",
      });

      if (!res.ok) {
        throw new Error("Unable to start a new chat");
      }

      const data = await res.json();

      setSessionId(data.session_id);
      setMessages([]);

    } catch (error) {
      console.error("New chat error:", error);
      alert("Error starting new chat. Please try again.");
    }
  }

  return (
    <div className="app-container">

      {/* Header */}
      <header className="header">

        <div>
          <h2>Enterprise Ingestion Firewall</h2>

          <p className="session-text">
            Session: {sessionId || "New Connection"}
          </p>
        </div>

        <button
          className="new-chat-btn"
          onClick={startNewChat}
          disabled={loading}
        >
          + New Chat
        </button>

      </header>

      {/* Chat Area */}
      <main className="chat-window">

        {messages.length === 0 && (
          <div className="empty-state">
            <h3>How can I help you today?</h3>

            <p>
              Ask about billing, technical issues, or general inquiries.
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message-wrapper ${msg.role}`}
          >
            <div className="message-bubble">
              <ReactMarkdown>
                {msg.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {loading && (
          <div className="message-wrapper assistant">
            <div
              className="message-bubble typing-indicator"
              style={{ padding: "16px 18px" }}
            >
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />

      </main>

      {/* Input Area */}
      <footer className="input-area">

        <form
          onSubmit={sendMessage}
          className="input-form"
        >

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            disabled={loading}
          />

          <button
            type="submit"
            disabled={loading || !input.trim()}
          >
            {loading ? "..." : "Send"}
          </button>

        </form>

      </footer>

    </div>
  );
}
