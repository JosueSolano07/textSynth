import { useEffect, useRef, useState } from "react";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg.content }),
      });

      const data = await res.json();

      const botMsg = {
        role: "assistant",
        content: data.answer || data.error || "Error",
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error de conexión con el backend" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={styles.app}>
      {/* HEADER */}
      <div style={styles.header}>
        <div style={styles.title}>🧠 TextSynth Chat</div>
        <div style={styles.subtitle}>Pregúntale a tus documentos</div>
      </div>

      {/* CHAT */}
      <div ref={chatRef} style={styles.chat}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: m.role === "user" ? "flex-end" : "flex-start",
              background:
                m.role === "user" ? "#4f46e5" : "#1f1f1f",
            }}
          >
            {m.content}
          </div>
        ))}

        {loading && (
          <div style={styles.typing}>Pensando...</div>
        )}
      </div>

      {/* INPUT */}
      <div style={styles.inputBox}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Pregunta tu documento..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button style={styles.button} onClick={sendMessage}>
          Enviar
        </button>
      </div>
    </div>
  );
}

const styles = {
  app: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    backgroundColor: "#0d0d0d",
    color: "white",
    fontFamily: "Arial",
  },

  header: {
    padding: 15,
    borderBottom: "1px solid #222",
    textAlign: "center",
  },

  title: {
    fontSize: 18,
    fontWeight: "bold",
  },

  subtitle: {
    fontSize: 12,
    opacity: 0.6,
  },

  chat: {
    flex: 1,
    overflowY: "auto",
    padding: 15,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },

  message: {
    padding: 12,
    borderRadius: 12,
    maxWidth: "70%",
    whiteSpace: "pre-wrap",
    lineHeight: 1.4,
  },

  typing: {
    opacity: 0.6,
    fontStyle: "italic",
  },

  inputBox: {
    display: "flex",
    padding: 10,
    borderTop: "1px solid #222",
    gap: 10,
  },

  input: {
    flex: 1,
    padding: 12,
    borderRadius: 10,
    border: "none",
    outline: "none",
    background: "#1a1a1a",
    color: "white",
  },

  button: {
    padding: "10px 15px",
    borderRadius: 10,
    border: "none",
    background: "#4f46e5",
    color: "white",
    cursor: "pointer",
  },
};