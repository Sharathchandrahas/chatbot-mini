import React, { useState } from "react";
import axios from "axios";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSendMessage = async () => {
    if (!message) return;
    setLoading(true);
    setResponse("");

    try {
      const res = await axios.post("http://localhost:8000/api/chat/", {
        message: message,
      });
      setResponse(res.data.response);
    } catch (error) {
      console.error("Error sending message:", error);
      setResponse("Sorry, there was an error. Please try again.");
    }

    setLoading(false);
    setMessage("");
  };

  return (
    <div className="chat-container">
      <h2>Do you have any queries?</h2>
      <input
        type="text"
        value={message}
        onChange={handleInputChange}
        placeholder="Type your query here..."
      />
      <button onClick={handleSendMessage} disabled={loading}>
        {loading ? "Sending..." : "Submit"}
      </button>

      {loading && <p>Waiting for response...</p>}

      {!loading && response && (
        <div className="response">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default Chat;
