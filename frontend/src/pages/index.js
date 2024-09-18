"use client"
import Head from 'next/head';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FaUser, FaInstagram, FaFacebook, FaPlus, } from 'react-icons/fa';
import React, { useState } from 'react';
import styles from '../styles/Chat.module.css'
import { FaPaperPlane } from 'react-icons/fa';
import { loginRequest } from '../services/auth/authConfig';

import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
  useMsal,
} from '@azure/msal-react';


export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const [showSidebar, setShowSidebar] = useState(true); // State to toggle sidebar

  const { instance } = useMsal();

  const handleLogin = () => {
    instance.loginPopup(loginRequest)
      .then(response => {
        // Set the active account after a successful login
        const account = response.account;
        instance.setActiveAccount(account);

        // Acquire the access token after setting the active account
        instance.acquireTokenSilent({
          ...loginRequest,
          account: account // Pass the account object
        })
          .then(response => {
            console.log("Access Token:", response.accessToken);
          })
          .catch(error => {
            console.error("Failed to acquire access token silently:", error);
            // Fallback to acquire token via popup if silent acquisition fails
            instance.acquireTokenPopup({
              ...loginRequest,
              account: account // Pass the account object
            })
              .then(response => {
                console.log("Access Token:", response.accessToken);
              })
              .catch(error => {
                console.error("Failed to acquire access token:", error);
              });
          });
      })
      .catch(e => {
        console.error("Login failed:", e);
      });
  };


  const handleNewChat = () => {
    // Implement the functionality for creating a new chat
    alert('New chat created!'); // Placeholder for functionality
  };

  // const toggleSidebar = () => {
  //   setShowSidebar(!showSidebar); // Toggle the sidebar visibility
  // };

  const handleSendMessage = () => {
    if (input.trim() !== '') {
      setMessages([...messages, { sender: 'user', text: input }]);
      setInput('');
      // Simulate AI response
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'ai', text: 'This is a simulated AI response.' },
        ]);
      }, 1000);
    }
  };

  return (
    <div className="d-flex flex-column vh-100" style={{ backgroundColor: '#1c1c1c' }}>
      <Head>
        <title>Easy Talk</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Header Section */}
      <header className="navbar navbar-expand-lg" style={{ backgroundColor: '#343a40', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)' }}>
        <a className="navbar-brand text-white" href="#">Easy Talk</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <a className="nav-link text-white" href="#">Home</a>
            </li>
            <li className="nav-item">
              <a className="nav-link text-white" href="#">Features</a>
            </li>
            <UnauthenticatedTemplate>
              <li className="nav-item">
                <button className="btn btn-primary" onClick={handleLogin}>Login</button>
              </li>
            </UnauthenticatedTemplate>
            <AuthenticatedTemplate>
            <li className="nav-item">
              <a className="nav-link text-white" href="#">
                <FaUser size={20} className="ms-2" />
              </a>
            </li>
            </AuthenticatedTemplate>
          </ul>
        </div>
      </header>

      {/* Main Content Section */}
      <div className="d-flex flex-grow-1" style={{ overflow: 'hidden' }}>
        {/* Sidebar */}
        {showSidebar && (
          <aside className="bg-dark text-white p-3" style={{ width: '250px', overflowY: 'auto' }}>
            <div className="d-flex justify-content-between align-items-center mb-3">
              {/* New Chat Icon */}
              <button className="btn btn-sm btn-outline-light" onClick={handleNewChat}>
                <FaPlus className="me-2" /> New Chat
              </button>
              {/* Close Sidebar Icon */}
              {/* <button className="btn btn-sm btn-outline-light" onClick={toggleSidebar}>
                <FaTimes />
              </button> */}
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
              className="form-control custom-input" // Add the custom class
              placeholder="Type a message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              style={{ backgroundColor: '#4a4a4a', color: '#ffffff', borderColor: '#5a5a5a', borderRadius: '20px 0 0 20px' }} // Rounded input box
            />
            <div className="input-group-append">
              <button className="btn btn-success" onClick={handleSendMessage} style={{ borderRadius: '0 20px 20px 0' }}>
                <FaPaperPlane /> {/* Up arrow icon */}
              </button>
            </div>
          </div>
        </main>

      </div>

      {/* Footer Section */}
      <footer className="bg-dark py-3">
        <div className="container">
          <div className="d-flex justify-content-between">
            <div>
              <a href="#" className="text-white">Privacy Policy</a> | <a href="#" className="text-white">Terms of Service</a>
            </div>
            <div>
              <a href="#" className="text-white">Contact</a> |
              <a href="#" className="text-white">Feedback</a> |
              <a href="#" className="text-white">Follow Us</a> |
              <a href="#" className="text-white">Subscribe</a> |
            </div>
            <div>
              <span className="text-white">Follow us:</span>
              <a href="#" className="ms-2 text-white"><FaInstagram /></a>
              <a href="#" className="ms-2 text-white"><FaFacebook /></a>
            </div>
          </div>
        </div>
      </footer>

    </div>
  );
}
