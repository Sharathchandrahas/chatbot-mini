import React, { useState } from "react";
import axios from "axios";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSendMessage = async () => {
    if (!message && !file) return;
    setLoading(true);
    const formData = new FormData();
    if (message) formData.append("message", message);
    if (file) formData.append("file", file);
    formData.append("conversation", JSON.stringify(conversation));

    try {
      const res = await axios.post(
        "http://localhost:8000/api/chat/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setConversation(res.data.conversation);
    } catch (error) {
      console.error("Error sending message:", error);
    }

    setLoading(false);
    setMessage("");
    setFile(null);
  };

  return (
    <div className="chat-container">
      <p>Sharath's ChatGPT</p>
      <div className="chat-box">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`message ${
              msg.role === "user" ? "user-message" : "ai-message"
            }`}
          >
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
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
        />
        <button onClick={handleSendMessage} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chat;
