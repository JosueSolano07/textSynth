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

              background:
                m.role === "user"
                  ? "#303030"
                  : "#2a2a2a",

              alignSelf:
                m.role === "user"
                  ? "flex-end"
                  : "flex-start",

              marginRight:
                m.role === "user"
                  ? "24px"
                  : "auto",

              marginLeft:
                m.role === "assistant"
                  ? "24px"
                  : "auto",
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
    background: "#212121",
  },

  chatArea: {
    flex: 1,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "20px",
    padding: "24px 0",
    minHeight: 0,
  },

  message: {
    padding: "14px 18px",
    borderRadius: "18px",
    maxWidth: "780px",
    width: "fit-content",
    fontSize: "15px",
    lineHeight: "1.7",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    color: "#ececec",
    marginLeft: "auto",
    marginRight: "auto",
  },
};