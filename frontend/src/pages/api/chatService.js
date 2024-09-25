// pages/api/llm-chat.js
import axios from 'axios';

export default async function handler(req, res) {
  const { query, chatSessionId } = req.body; // Extract data from the client request
  console.log(query, chatSessionId)
  const accessToken = req.headers.authorization?.split(' ')[1]; // Get the access token from the Authorization header

  if (!query || !accessToken) {
    return res.status(400).json({ error: 'Query and access token are required.' });
  }

  try {
    // Make a request to the FastAPI server
    const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, { 
      query,
      chatSessionId,
    }, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    // Send back the response data to the client
    res.status(200).json(response.data);
  } catch (error) {
    console.error('Error while calling FastAPI:', error);
    res.status(error.response?.status || 500).json({ error: 'Internal Server Error' });
  }
}
