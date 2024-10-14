import axios from 'axios';
import Cookies from 'js-cookie';

export const sendMessage = async (accessToken, message, chatSessionId = null, onStream) => {
  // Create EventSource connection with accessToken as query parameter
  const eventSource = new EventSource(`/api/chatService?query=${encodeURIComponent(message)}&chatSessionId=${chatSessionId || ''}&accessToken=${encodeURIComponent(accessToken)}`);

  eventSource.onmessage = (event) => {
    const data = event.data;
    if (data) {
      onStream(data); // Send the data to the frontend handler
    }
  };

  eventSource.onerror = (error) => {
    console.error('EventSource error:', error);
    eventSource.close();
  };
};



export const fetchChatHistoryTitles = async (accessToken) => {
  const requestBody = {
  };
  try {
    // Make a request to the Next.js API route to fetch chat history
    const response = await axios.post('/api/chatHistoryTitles', requestBody, {
      headers: {
        'Authorization': `Bearer ${accessToken}`, // Pass the access token
        'Content-Type': 'application/json',
      },
    });

    // Return the chat history data
    return response;
  } catch (error) {
    console.error('Error fetching chat history:', error);
    throw error;
  }
};

export const fetchChatHistory = async (accessToken, sessionId) => {
  const requestBody = {
    sessionId,
  };

  try {
    // Make a request to the Next.js API route to fetch chat history for the session
    const response = await axios.post('/api/fetchChatHistory', requestBody, {
      headers: {
        'Authorization': `Bearer ${accessToken}`, // Pass the access token
        'Content-Type': 'application/json',
      },
    });

    // Return the chat history data
    return response;
  } catch (error) {
    console.error('Error fetching chat history:', error);
    throw error;
  }
};


