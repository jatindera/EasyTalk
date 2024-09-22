from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.chat_utils import getSessionName
from app.services.user_service import get_current_user, get_user_by_email, create_new_user
from app.db.database import get_db
from app.schemas.chat_schemas import ChatRequest
from app.schemas.user_schemas import UserCreate
from app.services import chat_service
from app.services.langchain_service import general_chat


router = APIRouter(
    prefix="/api",
    tags=["Chat API"],
)

@router.post("/llm-chat")
def llm_chat(request: ChatRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    query = request.query
    chat_session_id = request.chatSessionId
    email = user["email"]
    # Retrieve or create the user in the database
    user_record = get_user_by_email(email, db)
    if not user_record:
        userCreateObj = UserCreate(
            email=email,
            first_name=user["first_name"],
            last_name=user["last_name"],
            provider_name=user["provider_name"],
            provider_id=user["provider_id"],
            role=user["role"]
        )
        user_record = create_new_user(db, userCreateObj)
        print(user_record.user_id)
        print("*************")
        
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

@router.get("/chat-history/{session_id}")
def fetch_chat_history_for_session(session_id: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    print("*"*100)
    print("Inside fetch_chat_history_for_session")
    print(session_id)
    print(user)
    print("*"*100)

    # Fetch all the messages corresponding to the session ID from the database
    # messages = chat_service.fetch_chat_history_for_session(db, session_id, user.user_id)

    #  # Transform the query result into a list of dictionaries with query, answer, and timestamp
    # chat_history = [
    #     {"query": msg.query, "answer": msg.answer, "timestamp": msg.timestamp}
    #     for msg in messages
    # ]

    # return {"session_id": session_id, "messages": chat_history}
