import axios from 'axios';

//Axios.post ang .get is async by default. Same is with fetch by the way.
export default async function handler(req, res) {
  const accessToken = req.headers.authorization?.split(' ')[1]; // Get access token from Authorization header
  try {
    // Make a request to the FastAPI server to fetch chat history
    console.log("NextJS -> Going to fetch all titles")
    const result = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/chat-history`,{}, {
      headers: {
        'Authorization': `Bearer ${accessToken}`, // Pass the access token for authentication
        'Content-Type': 'application/json',
      },
    });
    // console.log(result.data)
    // Send back the fetched chat history to the client
    res.status(200).json(result.data);
  } catch (error) {
    console.error('Error while fetching chat history from FastAPI:', error);
    res.status(error.response?.status || 500).json({ error: 'Internal Server Error' });
  }
}
