import axios from 'axios';

export const sendMessage = async (accessToken, message, chatSessionId = null) => {
  const requestBody = {
    query: message,
    chatSessionId: chatSessionId || "", // Send the chatSessionId or empty string for the first request
  };

  try {
    const response = await axios.post('/api/chatService', requestBody, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Error while calling Next.js API route:', error);
    throw error;
  }
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

