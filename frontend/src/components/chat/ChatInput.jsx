import { useState } from "react";
import { sendQuestion } from "../../services/api";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!text.trim()) return;

    onSend(text); // SOLO texto

    setText("");
  };

  return (
    <div style={styles.container}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Escribe tu mensaje..."
        style={styles.input}
        onKeyDown={(e) => e.key === "Enter" && send()}
      />

      <button onClick={send} style={styles.button}>
        {loading ? "..." : "Enviar"}
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    padding: "10px",
    borderTop: "1px solid #333",
    background: "#1a1a1a",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "8px",
    border: "none",
    outline: "none",
    marginRight: "10px",
  },
  button: {
    padding: "10px 16px",
    borderRadius: "8px",
    background: "#2b6cff",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
};