# EasyTalk

EasyTalk is a chat application that allows users to communicate effortlessly. The project leverages the Langchain framework for integrating Large Language Models (LLMs) into the chat experience. The project is built with a FastAPI-based backend and a React-based frontend. The application integrates various technologies to provide secure, scalable, and user-friendly chat experiences.

## Features
- **User Authentication**: Secure user authentication with OAuth2 and role-based access control (RBAC).
- **Real-Time Chat**: Real-time messaging using FastAPI and EventSource, powered by LLM models like OpenAI, Google Gemini, and others, with the flexibility to use any preferred model.
- **Session Management**: Maintains chat session history with unique session IDs.
- **Scalable Frontend**: Built using Next.js, providing server-side rendering, extra security, and optimized performance.
- **Backend API**: Developed with FastAPI to manage chat sessions, user authentication, and message handling.

## Project Structure
### Backend
- **Framework**: FastAPI, Langchain
- **Directory**: `backend/app`
- **Dependencies**: Listed in `requirements.txt`
- **Environment Variables**: Example in `.env.template`

The backend handles authentication, chat logic, and integrates with Azure AD for secure access. Key features include:
- Secure authentication with tokens.
- Chat history management using SQLAlchemy.
- RESTful APIs for interacting with the frontend.

### Frontend
- **Framework**: React (Next.js)
- **Directory**: `frontend/src`
- **Dependencies**: Listed in `package.json`
- **Environment Variables**: Configured in `.env`

The frontend provides an intuitive user interface for chatting. Features include:
- Role-based protected routes.
- Integration with backend APIs to fetch chat data.
- Responsive design for mobile and desktop.

## Installation
### Prerequisites
- **Node.js** (for the frontend)
- **Python 3.10+** (for the backend)
- **Virtual Environment** for Python dependencies

### Backend Setup
1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables by copying `.env.template` to `.env` and configuring values.
5. Run the FastAPI server:
   ```sh
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Set up environment variables by copying `.env` and configuring values.
4. Run the development server:
   ```sh
   npm run dev
   ```

## Usage
- After setting up both the backend and frontend, open your browser and navigate to `http://localhost:3000` to access the EasyTalk application.
- Sign in using your credentials, and start chatting in real-time.

## Technologies Used
- **LLM Framework**: Langchain
- **Frontend**: React, Next.js
- **Backend**: FastAPI, SQLAlchemy
- **Authentication**: OAuth2, Azure AD
- **Database**: MySQL
- **Other**: Docker (for containerization), EventSource (for streaming)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

## License
This project is licensed under the MIT License.

## Contact
For questions or suggestions, feel free to open an issue or contact the project maintainers.