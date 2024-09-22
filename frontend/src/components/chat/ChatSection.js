import React, { useState, useEffect, useContext } from 'react';
import { FaPlus, FaPaperPlane } from 'react-icons/fa';
import { AuthContext } from '../../services/auth/authContext';
import styles from './Chat.module.css';
import { sendMessage, fetchChatHistory } from '../../services/chat/clientChatService';

const ChatSection = () => {
  const { accessToken } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatSessionId, setChatSessionId] = useState(null); // Chat session ID state
  const [showSidebar, setShowSidebar] = useState(true); 

 // Fetch chat history on component load or when the session ID changes
 useEffect(() => {
  if (chatSessionId && accessToken) {
    // Fetch previous chat history if a session ID is available
    fetchChatHistory(accessToken, chatSessionId)
      .then(history => {
        setMessages(history); // Populate chat history
      })
      .catch(error => {
        console.error('Error fetching chat history:', error);
      });
  }
}, [chatSessionId, accessToken]);

const handleSendMessage = () => {
  if (input.trim() !== '' && accessToken) {
    sendMessage(accessToken, input, chatSessionId)
      .then(data => {
        const { response, newChatSessionId } = data;

        // If a new session ID is returned, update both local storage and state
        if (newChatSessionId && newChatSessionId !== chatSessionId) {
          setChatSessionId(newChatSessionId);
          localStorage.setItem('chatSessionId', newChatSessionId); // Save new session ID in local storage
        }

        // Update the message state with the new message and response
        setMessages(prevMessages => [
          ...prevMessages,
          { sender: 'user', text: input },    // User's message
          { sender: 'ai', text: response }    // AI's response
        ]);

        setInput(''); // Clear the input field
      })
      .catch(error => {
        console.error('Error while calling FastAPI:', error);
      });
  }
};

  const handleNewChat = () => {
  // Reset the chat messages and chatSessionId for a new chat
  setMessages([]); // Clear all previous messages
  setChatSessionId(null); // Reset the chat session ID
  setInput(''); // Clear the input field
};

  return (
    <div className="d-flex flex-grow-1" style={{ overflow: 'hidden' }}>
      {/* Sidebar */}
      {showSidebar && (
        <aside className="bg-dark text-white p-3" style={{ width: '250px', overflowY: 'auto' }}>
          <div className="d-flex justify-content-between align-items-center mb-3">
            {/* New Chat Icon */}
            <button className="btn btn-sm btn-outline-light" onClick={handleNewChat}>
              <FaPlus className="me-2" /> New Chat
            </button>
          </div>
          <ul className="list-unstyled">
            <li className="mb-3 chat-label">Chat1</li>
            <li className="mb-3 chat-label">Chat2</li>
          </ul>
        </aside>
      )}

      {/* Main Chat Interface */}
      <main className="d-flex flex-column flex-grow-1 p-4" style={{ maxHeight: '100%' }}>
        <div className="flex-grow-1 overflow-auto p-3 mb-3" style={{ backgroundColor: '#2c2c2c', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)' }}>
          <div className={styles.chatWindow}>
            {messages.map((msg, index) => (
              <div key={index} className={`alert ${msg.sender === 'user' ? 'alert-primary' : 'alert-secondary'}`} style={{ backgroundColor: msg.sender === 'user' ? '#454545' : '#363636', color: '#ffffff' }}>
                <strong>{msg.sender === 'user' ? 'You: ' : 'AI: '}</strong> {msg.text}
              </div>
            ))}
          </div>
        </div>
        <div className="input-group p-3" style={{ backgroundColor: '#3a3a3a', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)' }}>
          <input
            type="text"
            className="form-control custom-input"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            style={{ backgroundColor: '#4a4a4a', color: '#ffffff', borderColor: '#5a5a5a', borderRadius: '20px 0 0 20px' }}
          />
          <div className="input-group-append">
            <button className="btn btn-success" onClick={handleSendMessage} style={{ borderRadius: '0 20px 20px 0' }}>
              <FaPaperPlane />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ChatSection;
