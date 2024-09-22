from sqlalchemy.orm import Session
from app.models.chat_models import ChatSession
from app.crud import chat_crud
from typing import List
from app.models.chat_models import ChatHistory

def create_new_chat_session(db: Session, user_id: int, session_name:str) -> ChatSession:
    
    # Call the CRUD function to create a new user
    chat_session_row = chat_crud.create_new_chat_session(db, user_id, session_name)
    return chat_session_row

def create_chat_history(db: Session, session_id: int, user_id: int, query: str, answer: str):
    history_row = chat_crud.create_chat_history(db, session_id, user_id, query, answer)
    return history_row

def fetch_chat_history_for_session(db: Session, chat_session_id: int, user_id: int) -> List[ChatHistory]:
    # Fetch chat history for the given chat session ID and user ID
    chat_history = chat_crud.fetch_chat_history_for_session(db, chat_session_id, user_id)

    if not chat_history:
        raise ValueError(f"No chat history found for chat_session_id {chat_session_id} and user_id {user_id}")

    return chat_history