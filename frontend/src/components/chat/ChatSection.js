import React, { useState, useEffect, useContext, useRef, memo } from 'react';
import { FaPlus, FaPaperPlane } from 'react-icons/fa';
import { AppContext } from '../../services/context/appContext';
import styles from './Chat.module.css';
import { sendMessage, fetchChatHistoryTitles, fetchChatHistory } from '../../services/chat/clientChatService';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css'; // Import KaTeX CSS for LaTeX rendering
import remarkGfm from 'remark-gfm'; // Import GitHub Flavored Markdown plugin

const ChatSection = () => {
  const { accessToken } = useContext(AppContext);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatSessionId, setChatSessionId] = useState(null); // Chat session ID state
  const [showSidebar, setShowSidebar] = useState(true);
  const [chatList, setChatList] = useState([]); // For sidebar chat list
  const [isTokenReady, setIsTokenReady] = useState(false); // To control when the token is ready
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const chatWindowRef = useRef(null);

  useEffect(() => {
    if (accessToken) {
      setIsTokenReady(true);
    }
  }, [accessToken]);

  useEffect(() => {
    if (isTokenReady) {
      fetchChatHistoryTitles(accessToken)
        .then((history) => {
          setChatList(history.data.chat_history_titles || []);
        })
        .catch((error) => {
          console.error('Error fetching chat history:', error);
        });
    }
  }, [isTokenReady, accessToken, chatSessionId]);

  const loadChatHistory = (sessionId) => {
    if (accessToken && sessionId) {
      fetchChatHistory(accessToken, sessionId)
        .then((history) => {
          const chatMessages = history.data.chat_history.map((item) => ({
            sender: item.role,
            text: item.content,
          }));

          setMessages(chatMessages);
          setChatSessionId(sessionId);
        })
        .catch((error) => {
          console.error('Error fetching chat history:', error);
        });
    }
  };

  const handleSendMessage = () => {
    setInput(''); // Clear the input field immediately
    if (input.trim() !== '' && accessToken) {
      setIsLoading(true);

      // Add the user's message to the messages state
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'human', text: input }, // User's message
      ]);

      // Start streaming the response from server
      sendMessage(accessToken, input, chatSessionId, (chunk, newChatSessionId) => {
        if (newChatSessionId && newChatSessionId !== chatSessionId) {
          setChatSessionId(newChatSessionId);
        }

        setMessages((prevMessages) => {
          // Find the last AI message to append the new chunk to
          const lastMessage = prevMessages[prevMessages.length - 1];
          if (lastMessage && lastMessage.sender === 'ai') {
            // Append the new chunk to the existing AI message
            return [
              ...prevMessages.slice(0, -1),
              { sender: 'ai', text: lastMessage.text + chunk },
            ];
          } else {
            // Add a new AI message if one doesn't exist yet
            return [...prevMessages, { sender: 'ai', text: chunk }];
          }        

        });


      }).catch(error => {
        console.error('Error while calling FastAPI:', error);
      })
        .finally(() => {
          setIsLoading(false); // Stop loading
        });

    }
  };



  const handleNewChat = () => {
    setMessages([]);
    setChatSessionId(null);
    setInput('');
  };

  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTo({
        top: chatWindowRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages, isLoading]);

  return (
    <div className="d-flex flex-grow-1" style={{ overflow: 'hidden' }}>
      {showSidebar && (
        <aside className={`${styles.sidebar}`}>
          <div className="d-flex justify-content-between align-items-center mb-3">
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

      <main className={`${styles.mainContent}`} style={{ position: 'relative' }}>
        <div
          ref={chatWindowRef}
          className={styles.chatWindow}
          style={{ backgroundColor: '#2c2c2c', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)', position: 'relative' }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`alert ${msg.sender === 'human' ? 'alert-primary' : 'alert-secondary'}`}
              style={{ backgroundColor: msg.sender === 'human' ? '#454545' : '#363636', color: '#ffffff' }}
            >
              <strong>{msg.sender === 'human' ? 'You: ' : 'AI: '}</strong>
              <ReactMarkdown
                remarkPlugins={[remarkMath, remarkGfm]}
                rehypePlugins={[rehypeKatex]}
              >
                {msg.text}
              </ReactMarkdown>
            </div>
          ))}

          {isLoading && (
            <div className={styles.typingIndicator}>
              <span></span>
              <span></span>
              <span></span>
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
