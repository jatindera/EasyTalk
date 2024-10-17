import React, { useState, useEffect, useContext, useRef } from 'react';
import { FaPlus, FaPaperPlane, FaCopy, FaCheck } from 'react-icons/fa';
import { AppContext } from '../../services/context/appContext';
import styles from './Chat.module.css';
import { sendMessage, fetchChatHistoryTitles, fetchChatHistory } from '../../services/chat/clientChatService'; // Removed fetchChatHistory as we'll define it here
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark.css'; // Import a CSS style for highlighting (you can choose different themes)
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';





const ChatSection = () => {

  // NEW: Track which message has been copied
  const [copiedMessageIndex, setCopiedMessageIndex] = useState(null);



  // Function to handle copying text
  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text)
      .then(() => {
        setCopiedMessageIndex(index); // NEW: Set copied message index
        setTimeout(() => setCopiedMessageIndex(null), 2000); // NEW: Reset after 2 seconds
      })
      .catch((error) => {
        console.error('Error copying text:', error); // NEW: Error handling
      });
  };


  const { accessToken } = useContext(AppContext);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatSessionId, setChatSessionId] = useState(null); // Chat session ID state
  const [showSidebar, setShowSidebar] = useState(true);
  const [chatList, setChatList] = useState([]); // For sidebar chat list
  const [isTokenReady, setIsTokenReady] = useState(false); // To control when the token is ready
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const formatMessage = (text) => {
    // Convert block math \[ ... \] to $$ ... $$
    text = text.replace(/\\\[(.*?)\\\]/gs, '$$ $1 $$');
  
    // Convert inline math \( ... \) to $ ... $
    text = text.replace(/\\\((.*?)\\\)/g, '$ $1 $');
  
    return text;
  };
  

  const containsLatex = (text) => {
    const latexPattern = /\$.*?\$|\$\$.*?\$\$|\\\(|\\\)|\\\[|\\\]/s;
    return latexPattern.test(text);
  };




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
    console.log("useEffect triggered with chatSessionId:", chatSessionId);
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
  }, [isTokenReady, accessToken, chatSessionId]);

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

      // Add user's message to the chat
      setMessages(prevMessages => [
        ...prevMessages,
        { sender: 'human', text: input }
      ]);

      let aiMessageIndex;

      // Handle incoming chunks with the onChunkReceived callback
      sendMessage(accessToken, input, chatSessionId, (chunk) => {
        // Ensure the UI updates immediately for each chunk received
        setMessages((prevMessages) => {
          // If this is the first chunk, add a new AI message
          if (aiMessageIndex === undefined) {
            aiMessageIndex = prevMessages.length; // Store index for the new AI message
            return [
              ...prevMessages,
              { sender: 'ai', text: chunk }
            ];
          }

          // For subsequent chunks, append to the existing AI message
          const updatedMessages = [...prevMessages];
          updatedMessages[aiMessageIndex].text += chunk;

          return updatedMessages;
        });

        // Scroll to the bottom after each update
        if (chatWindowRef.current) {
          chatWindowRef.current.scrollTo({
            top: chatWindowRef.current.scrollHeight,
            behavior: 'smooth',
          });
        }
      })
        .then(({ newChatSessionId }) => {
          // If a new session ID is returned, update it
          if (newChatSessionId && newChatSessionId !== chatSessionId) {
            setChatSessionId(newChatSessionId);
            console.log("Updated chatSessionId to:", newChatSessionId);
          }
        })
        .catch((error) => {
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
      chatWindowRef.current.scrollTo({
        top: chatWindowRef.current.scrollHeight,
        behavior: 'smooth', // Adds smooth scrolling effect
      });
    }
  }, [messages, isLoading]);



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
          ref={chatWindowRef}
          className={styles.chatWindow}
          style={{ backgroundColor: '#2c2c2c', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)', position: 'relative' }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`alert ${msg.sender === 'human' ? 'alert-primary' : 'alert-secondary'}`}
              style={{
                backgroundColor: msg.sender === 'human' ? '#454545' : '#363636',
                color: '#ffffff',
                position: 'relative', // UPDATED: Added position for placing the copy icon
                paddingRight: '70px',  // NEW: Add padding to ensure copy button doesn’t overlap content
              }}
            >
              <strong>{msg.sender === 'human' ? 'You: ' : 'AI: '}</strong>

              {containsLatex(msg.text) ? (
                <ReactMarkdown
                  remarkPlugins={[remarkMath]}
                  rehypePlugins={[rehypeHighlight, rehypeKatex]}
                >
                  {formatMessage(msg.text)}
                </ReactMarkdown>
              ) : (
                <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
                  {msg.text}
                </ReactMarkdown>
              )}
              {/* <ReactMarkdown
                remarkPlugins={[remarkMath]}
                rehypePlugins={[rehypeHighlight, rehypeKatex]}>
                {msg.text}
             
              </ReactMarkdown> */}
              {msg.sender === 'ai' && ( // NEW: Only add the copy button for AI responses
                <button
                  onClick={() => handleCopy(msg.text, index)} // UPDATED: Call handleCopy with message text and index
                  style={{
                    position: 'absolute',
                    top: '10px',
                    right: '10px',
                    background: 'none',
                    border: 'none',
                    color: '#ffffff',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                  }}
                  title="Copy to clipboard" // NEW: Tooltip for better user experience
                >
                  {copiedMessageIndex === index ? ( // NEW: Toggle between copy and check icon
                    <>
                      <FaCheck />
                      <span style={{ marginLeft: '5px' }}>Copied!</span> {/* NEW: Show "Copied!" text */}
                    </>
                  ) : (
                    <>
                      <FaCopy />
                      <span style={{ marginLeft: '5px' }}>Copy</span> {/* NEW: Show "Copy code" text */}
                    </>
                  )}
                </button>
              )}
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