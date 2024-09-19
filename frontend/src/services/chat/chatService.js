import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;
console.log("111111111111")
console.log(API_URL)
console.log("111111111111")

export const sendMessage = (accessToken, message) => {
  // Prepare the request body
  const requestBody = {
    "query":message, // Send the query parameter
    "chatSessionId": ""

  };
    return axios.post(`${API_URL}/api/llm-chat`, requestBody, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  };

  export const getChatHistory = (accessToken, sessionId) => {
    return axios.get(`${API_URL}/api/llm-chat/history/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  };