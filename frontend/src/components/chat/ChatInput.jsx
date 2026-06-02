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
    padding: "16px 24px",
    background: "#212121",
  },

  input: {
    flex: 1,
    background: "#303030",
    color: "#ececec",
    border: "1px solid #404040",
    borderRadius: "24px",
    padding: "14px 18px",
    outline: "none",
    fontSize: "15px",
    marginRight: "10px",
  },

  button: {
    background: "#10a37f",
    color: "white",
    border: "none",
    borderRadius: "12px",
    padding: "0 18px",
    cursor: "pointer",
    fontWeight: "600",
  },
};