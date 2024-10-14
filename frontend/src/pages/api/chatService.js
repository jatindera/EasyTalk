import axios from 'axios';

export default async function handler(req, res) {
  const { query, chatSessionId, accessToken } = req.query;

  if (!query || !accessToken) {
    return res.status(400).json({ error: 'Query and access token are required.' });
  }

  try {
    // Make a request to the FastAPI server
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_API_URL}/api/chat`,
      {
        query,
        chatSessionId,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        responseType: 'stream', // Set response type to stream
      }
    );

    // Set proper headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // Handle the stream from FastAPI
    response.data.on('data', (chunk) => {
      res.write(chunk);
      res.flush();
    });

    response.data.on('end', () => {
      res.end();
    });

    response.data.on('error', (error) => {
      console.error('Stream error from FastAPI:', error);
      res.end();
    });
  } catch (error) {
    console.error('Error while calling FastAPI:', error);
    res.status(error.response?.status || 500).json({ error: 'Internal Server Error' });
  }
}
