import { useState } from "react";
import ChatInput from "./ChatInput";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);

  const handleMessage = (msg) => {
    setMessages((prev) => [...prev, msg]);
  };

  return (
    <div>
      {messages.map((m, i) => (
        <div key={i}>{m.text}</div>
      ))}

      <ChatInput onMessage={handleMessage} />
    </div>
  );
}