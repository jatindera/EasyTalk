export default async function handler(req, res) {
  const { query, chatSessionId } = req.body; // Extract data from the client request
  const accessToken = req.headers.authorization?.split(' ')[1]; // Get the access token from the Authorization header

  if (!query || !accessToken) {
    return res.status(400).json({ error: 'Query and access token are required.' });
  }

  try {
    // Use the Fetch API for handling the streaming response from FastAPI
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        chatSessionId,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch from FastAPI');
    }

    // Extract newChatSessionId from the headers (use .get() method and lowercase header name)
    // Fetch works like following.
    const newChatSessionId = response.headers.get('newchatsessionid');
    console.log("******************", newChatSessionId)


    // Set the newChatSessionId in the response header to the client, only if it exists
    if (newChatSessionId) {
      res.setHeader('newChatSessionId', newChatSessionId);
    }

    res.setHeader('Content-Type', 'text/plain');
    res.setHeader('Transfer-Encoding', 'chunked');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Cache-Control', 'no-cache');
    res.flushHeaders();


    // Stream the response data to the client
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      res.write(chunk);
      res.flush(); // Flush data to client immediately
    }

    res.end();
  } catch (error) {
    console.error('Error while calling FastAPI:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
