import React, { useState, useEffect, useContext } from 'react';
import { FaPlus, FaPaperPlane } from 'react-icons/fa';
import { AppContext } from '../../services/context/appContext';
import styles from './Chat.module.css';
import { sendMessage, fetchChatHistoryTitles } from '../../services/chat/clientChatService'; // Removed fetchChatHistory as we'll define it here

const ChatSection = () => {
  const { accessToken } = useContext(AppContext);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatSessionId, setChatSessionId] = useState(null); // Chat session ID state
  const [showSidebar, setShowSidebar] = useState(true);
  const [chatList, setChatList] = useState([]); // For sidebar chat list
  const [isTokenReady, setIsTokenReady] = useState(false); // To control when the token is ready

  // Watch the accessToken and set the isTokenReady flag when it's available
  useEffect(() => {
    if (accessToken) {
      setIsTokenReady(true);
    }
  }, [accessToken]);

  // Fetch chat history when accessToken is ready
  useEffect(() => {
    if (isTokenReady) {
      // Fetch previous chat history
      fetchChatHistoryTitles(accessToken)
        .then(history => {
          console.log("*****************")
          console.log(history.data.chat_history_titles)
          console.log("*****************")
          setChatList(history.data.chat_history_titles || []); // Assuming response contains a `chatSessions` list for sidebar
        })
        .catch(error => {
          console.error('Error fetching chat history:', error);
        });
    }
  }, [isTokenReady, accessToken]); // Run this effect only when the token is ready

  const handleSendMessage = () => {
    if (input.trim() !== '' && accessToken) {
      sendMessage(accessToken, input, chatSessionId)
        .then(data => {
          const { response, newChatSessionId } = data;

          // If a new session ID is returned, update both local storage and state
          if (newChatSessionId && newChatSessionId !== chatSessionId) {
            setChatSessionId(newChatSessionId);
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
            {chatList.map((chat, index) => (
              <li key={index} className="mb-3 chat-label">
                {chat.session_name || `Chat ${index + 1}`}  {/* Assuming each chat session has a 'name' */}
              </li>
            ))}
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
