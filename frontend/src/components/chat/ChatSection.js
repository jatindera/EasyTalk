// components/ChatSection.js
import React, { useState, useContext } from 'react';
import { FaPlus, FaPaperPlane } from 'react-icons/fa';
import { AuthContext } from '../../services/auth/authContext';
import styles from './Chat.module.css';
import { sendMessage } from '../../services/chat/chatService';

const ChatSection = () => {
  // Access the context for the access token
  const { accessToken } = useContext(AuthContext);

  // Local state for the chat
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [showSidebar, setShowSidebar] = useState(true);

  // Function to handle sending messages
  const handleSendMessage = () => {
    if (input.trim() !== '' && accessToken) {
      // Call the FastAPI endpoint to send a message
      sendMessage(accessToken, input)
        .then(data => {
          console.log(data)
          // Update the message state with the response from FastAPI
          setMessages([...messages, { sender: 'user', text: input }, { sender: 'ai', text: data.data }]);
          setInput('');
        })
        .catch(error => {
          console.error('Error while calling FastAPI:', error);
        });
    }
  };

  // Function to handle new chat creation
  const handleNewChat = () => {
    alert('New chat created!'); // Placeholder for functionality
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
            <li className="mb-3 chat-label">Chat3</li>
            <li className="mb-3 chat-label">Chat4</li>
            <li className="mb-3 chat-label">Chat5</li>
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
