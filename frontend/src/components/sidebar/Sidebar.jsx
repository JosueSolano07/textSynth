import ChatList from "./ChatList";
import DocumentList from "./DocumentList";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <button className="new-chat">+ New Chat</button>

      <ChatList />

      <div className="divider" />

      <DocumentList />
    </div>
  );
}