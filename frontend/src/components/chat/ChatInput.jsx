import { useState } from "react";
import { askQuestion } from "../../services/api";

export default function ChatInput({ onMessage }) {
  const [text, setText] = useState("");

  const send = async () => {
    if (!text) return;

    const res = await askQuestion(text);

    onMessage({
      role: "assistant",
      text: res.answer,
    });

    setText("");
  };

  return (
    <div>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={send}>Enviar</button>
    </div>
  );
}