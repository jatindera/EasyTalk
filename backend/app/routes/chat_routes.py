from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# from app.utils.chat_utils import getSessionName
from app.services.user_service import get_authenticated_user
from app.db.database import get_db
from app.schemas.chat_schemas import ChatRequest
from app.schemas.user_schemas import UserCreate
from app.services import chat_service


router = APIRouter(
    prefix="/api",
    tags=["Chat API"],
)


@router.post("/chat")
def chat(
    request: ChatRequest,
    user: dict = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    question = request.query
    chat_session_id = request.chatSessionId
    user_id = user["user_id"]
    # Retrieve or create the user in the database
    user_record = chat_service.get_user_for_chat(db,user_id)
    print("-"*100)
    print(user_record)
    print("-"*100)
    if not user_record:
        userCreateObj = UserCreate(
            user_id=user_id,
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            ip_address=user["ip_address"],
            provider_name=user["provider_name"],
            role=user["role"],
        )
        user_id = chat_service.create_new_user_for_chat(db,userCreateObj)

    # session_name = getSessionName(question)
    # Check or create the chat session ID
    if not chat_session_id:
        chat_session_id = chat_service.create_new_chat_session(
            db, user_id, question
        )

    # Call the AI model to get the response
    ai_response = chat_service.create_chat_response(db, question, chat_session_id, user_id)

    return {"response": ai_response, "newChatSessionId": chat_session_id}


@router.post("/chat-history")
def get_chat_history_titles(
    user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)
):
    user_id = user["user_id"]
    # Fetch chat history for the current user
    chat_history_titles = chat_service.get_chat_history_titles(db, user_id)
    if not chat_history_titles:
        return {"chat_history_titles": ""}
    return {"chat_history_titles": chat_history_titles}


@router.get("/chat-history/{session_id}")
def get_chat_history_for_session(
    session_id: str,
    user: dict = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    user_id = user["user_id"]
    # Fetch chat history for the current user and the given session id
    chat_history = chat_service.get_chat_history_for_session(db, session_id, user_id)
    if not chat_history:
        return {"chat_history": ""}
    return {"chat_history": chat_history}
