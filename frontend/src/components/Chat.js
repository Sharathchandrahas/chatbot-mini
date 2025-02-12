import React, { useState } from "react";
import axios from "axios";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSendMessage = async () => {
    if (!message) return;
    setLoading(true);

    const updatedConversation = [
      ...conversation,
      { role: "user", content: message },
    ];

    try {
      const res = await axios.post("http://localhost:8000/api/chat/", {
        message: message,
        conversation: updatedConversation,
      });

      setConversation([
        ...updatedConversation,
        { role: "assistant", content: res.data.response },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    }

    setLoading(false);
    setMessage("");
  };

  return (
    <div className="chat-container">
      <h2>Chat with AI</h2>
      <div className="chat-box">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`message ${
              msg.role === "user" ? "user-message" : "ai-message"
            }`}
          >
            <strong>{msg.role === "user" ? "You: " : "AI: "}</strong>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={handleInputChange}
          placeholder="Type your message..."
        />
        <button onClick={handleSendMessage} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chat;
