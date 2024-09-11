from fastapi import APIRouter
from app.services.langchain_service import general_chat  # Import the general_chat function from the service
from app.utils.chat_utils import generate_session_id  # Import the generate_session_id function

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat API v1.0"],
)

@router.post("/chat")
def chat_endpoint(query: str, new_chat: bool = False):
    # If it's a new chat, generate a new session ID
    if new_chat:
        session_id = generate_session_id()
    else:
        # Assume session_id is passed from the client (for an existing session)
        # In a real application, handle session retrieval from DB or in-memory store
        session_id = "3a0102fc-c9dc-4ded-bc38-b1c27696a26f"  # This should be replaced with actual session retrieval logic

    # Call the general_chat function in langchain_service.py with the session_id
    result = general_chat(query, session_id)
    return {"result": result, "session_id": session_id}


