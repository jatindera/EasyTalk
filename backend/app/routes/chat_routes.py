from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.chat_utils import getSessionName
from app.services.user_service import get_current_user, get_user_by_oid, create_new_user
from app.db.database import get_db
from app.schemas.chat_schemas import ChatRequest
from app.schemas.user_schemas import UserCreate
from app.services import chat_service
from app.services.langchain_service import general_chat


router = APIRouter(
    prefix="/api",
    tags=["Chat API"],
)

@router.post("/chat")
def llm_chat(request: ChatRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    query = request.query
    chat_session_id = request.chatSessionId
    user_id = user["user_id"]
    # Retrieve or create the user in the database
    user_record = get_user_by_oid(user_id, db)
    if not user_record:
        userCreateObj = UserCreate(
            user_id=user_id,
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            ip_address=user["ip_address"],
            provider_name=user["provider_name"],
            role=user["role"]
        )
        user_record = create_new_user(db, userCreateObj)
        
    session_name = getSessionName(query)
    # Check or create the chat session ID
    if not chat_session_id:
        new_chat_session = chat_service.create_new_chat_session(db, user_record.user_id,session_name)
        chat_session_id = new_chat_session.session_id
        db.add(new_chat_session)
        db.commit()
     
    # Call the AI model to get the response
    ai_response = general_chat(query, chat_session_id)
    answer = ai_response

    # Store the user's query and AI's answer in the chat history
    new_chat_history = chat_service.create_chat_history(
        db,
        chat_session_id,
        user_record.user_id,
        query,
        answer
    )
    db.add(new_chat_history)
    db.commit()

    return {"response": ai_response, "newChatSessionId": chat_session_id}
    

@router.post("/chat-history")
def get_chat_history_titles(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user["user_id"]
    # Fetch chat history for the current user
    chat_history_titles = chat_service.get_chat_history_titles(db, user_id)
    if not chat_history_titles:
        return {"chat_history_titles": ""}
    return {"chat_history_titles": chat_history_titles}



@router.get("/chat-history/{session_id}")
def get_chat_history_for_session(session_id: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user["user_id"]
    # Fetch chat history for the current user and the given session id
    chat_history = chat_service.get_chat_history_for_session(db, session_id, user_id)
    if not chat_history:
        return {"chat_history": ""}
    return {"chat_history": chat_history}


