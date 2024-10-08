import React, { useState, useEffect, useContext, useRef } from 'react';
import { FaPlus, FaPaperPlane, FaSpinner } from 'react-icons/fa';
import { AppContext } from '../../services/context/appContext';
import styles from './Chat.module.css';
import { sendMessage, fetchChatHistoryTitles, fetchChatHistory } from '../../services/chat/clientChatService'; // Removed fetchChatHistory as we'll define it here
import Link from 'next/link';



const ChatSection = () => {
  const { accessToken } = useContext(AppContext);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatSessionId, setChatSessionId] = useState(null); // Chat session ID state
  const [showSidebar, setShowSidebar] = useState(true);
  const [chatList, setChatList] = useState([]); // For sidebar chat list
  const [isTokenReady, setIsTokenReady] = useState(false); // To control when the token is ready
  const [isLoading, setIsLoading] = useState(false); // Loading state

  // Create a reference for the chat window
  const chatWindowRef = useRef(null);

  // Watch the accessToken and set the isTokenReady flag when it's available
  useEffect(() => {
    if (accessToken) {
      setIsTokenReady(true);
    }
  }, [accessToken]);

  // Fetch chat history titles when accessToken is ready
  useEffect(() => {
    if (isTokenReady) {
      // Fetch previous chat history title and session id
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
  }, [isTokenReady, accessToken, chatSessionId]); // Run this effect only when the token is ready

  const loadChatHistory = (sessionId) => {
    if (accessToken && sessionId) {
      fetchChatHistory(accessToken, sessionId)
        .then(history => {
          const chatMessages = history.data.chat_history.map((item) => ({
            sender: item.role, // This will be 'human' or 'ai' as per the FastAPI response
            text: item.content,
          }));

          // Update state with the fetched chat messages
          setMessages(chatMessages);
          setChatSessionId(sessionId);
        })
        .catch(error => {
          console.error('Error fetching chat history:', error);
        });
    }
  };


  const handleSendMessage = () => {
    setInput(''); // Clear the input field immediately
    if (input.trim() !== '' && accessToken) {
      setIsLoading(true); // Start loading
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
            { sender: 'human', text: input },    // User's message
            { sender: 'ai', text: response }    // AI's response
          ]);

          setInput(''); // Clear the input field
        })
        .catch(error => {
          console.error('Error while calling FastAPI:', error);
        })
        .finally(() => {
          setIsLoading(false); // Stop loading
        });
    }
  };

  const handleNewChat = () => {
    // Reset the chat messages and chatSessionId for a new chat
    setMessages([]); // Clear all previous messages
    setChatSessionId(null); // Reset the chat session ID
    setInput(''); // Clear the input field
  };

  // Scroll to bottom whenever messages change
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="d-flex flex-grow-1" style={{ overflow: 'hidden' }}>
      {/* Sidebar */}
      {showSidebar && (
        <aside className={`${styles.sidebar}`}>
          <div className="d-flex justify-content-between align-items-center mb-3">
            {/* New Chat Icon */}
            <button className="btn btn-sm btn-outline-light" onClick={handleNewChat}>
              <FaPlus className="me-2" /> New Chat
            </button>
          </div>
          <ul className="list-unstyled">
            {chatList.map((chat, index) => (
              <li key={index} className="mb-3 chat-label">
                <Link href="#" onClick={() => loadChatHistory(chat.session_id)}>
                  {chat.session_name || `Chat ${index + 1}`}
                </Link>
              </li>
            ))}
          </ul>
        </aside>
      )}


      {/* Main Chat Interface */}
      <main className={`${styles.mainContent}`} style={{ position: 'relative' }}>
        <div
          ref={chatWindowRef} // Attach reference to chat window
          className={styles.chatWindow} style={{ backgroundColor: '#2c2c2c', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)', position: 'relative' }}>
          {messages.map((msg, index) => (
            <div key={index} className={`alert ${msg.sender === 'human' ? 'alert-primary' : 'alert-secondary'}`} style={{ backgroundColor: msg.sender === 'human' ? '#454545' : '#363636', color: '#ffffff' }}>
              <strong>{msg.sender === 'human' ? 'You: ' : 'AI: '}</strong> {msg.text}
            </div>
          ))}
          {isLoading && (
            <div className={styles.fullScreenOverlay}>
              <FaSpinner className={styles.fullScreenSpinner} /> Loading...
            </div>
          )}

        </div>
        <div className={styles.inputContainer}>
          <input
            type="text"
            className="form-control"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button onClick={handleSendMessage}>
            <FaPaperPlane /> Send
          </button>
        </div>
      </main>

    </div>

  );
};

export default ChatSection;
