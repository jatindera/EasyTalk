import axios from 'axios';

export default async function handler(req, res) {
  const { sessionId } = req.body; // Extract sessionId from the request body
  const accessToken = req.headers.authorization?.split(' ')[1]; // Get access token from Authorization header

  if (!sessionId || !accessToken) {
    return res.status(400).json({ error: 'Session ID and access token are required.' });
  }

  try {
    // Make a request to the FastAPI server to fetch chat history for the session
    const result = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/chat-history/${sessionId}`, {}, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    // Send back the fetched chat history to the client
    res.status(200).json(result.data);
  } catch (error) {
    console.error('Error while fetching chat history from FastAPI:', error);
    res.status(error.response?.status || 500).json({ error: 'Internal Server Error' });
  }
}
