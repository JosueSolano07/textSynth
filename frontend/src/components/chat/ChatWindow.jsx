import { useState, useRef, useEffect } from "react";
import ChatInput from "./ChatInput";
import { sendQuestion } from "../../services/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const bottomRef = useRef(null);

  // 🔥 enviar mensaje al backend
  const handleSend = async (text) => {

    // 1. agregar mensaje usuario
    const newMessages = [
      ...messages,
      { role: "user", text }
    ];

    setMessages(newMessages);

    try {

      // 2. construir history para backend
      const history = newMessages.map(m => ({
        role: m.role,
        content: m.text
      }));

      // 3. llamar backend
      const res = await sendQuestion({
        question: text,
        history
      });

      // 4. agregar respuesta IA
      setMessages(prev => [
        ...prev,
        { role: "assistant", text: res.answer }
      ]);

    } catch (err) {
      console.error(err);

      setMessages(prev => [
        ...prev,
        { role: "assistant", text: "Error conectando con el backend." }
      ]);
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div style={styles.container}>

      {/* MESSAGES */}
      <div style={styles.chatArea}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: m.role === "user" ? "flex-end" : "flex-start",
              background: m.role === "user" ? "#2b6cff" : "#2a2a2a",
            }}
          >
            {m.text}
          </div>
        ))}

        <div ref={bottomRef} />
      </div>

      {/* INPUT */}
      <ChatInput onSend={handleSend} />
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    background: "#111",
    color: "white",
  },
  chatArea: {
    flex: 1,
    padding: "20px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  message: {
    padding: "10px 14px",
    borderRadius: "12px",
    maxWidth: "60%",
    color: "white",
    fontSize: "14px",
    whiteSpace: "pre-wrap"
  },
};