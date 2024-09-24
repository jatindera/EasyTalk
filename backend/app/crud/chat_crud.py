from sqlalchemy.orm import Session
from app.models.chat_models import ChatSession, ChatHistory
from datetime import datetime
from sqlalchemy import text

# Create a new chat session
def create_new_chat_session(db: Session, user_id: str, session_name: str = None ):
    chat_session = ChatSession(user_id=user_id, session_name=session_name)
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    return chat_session

def get_chat_history_titles(db: Session, user_id: str):
    # Wrinting query because mappings, which returns dictionary, is not supported by ORM
    query = text("SELECT session_id, session_name FROM chat_sessions WHERE user_id = :user_id")
    chat_history_titles = db.execute(query,{"user_id": user_id}).mappings().all()
    return chat_history_titles


# Store a new message in the chat history
def create_chat_history(db: Session, session_id: int, user_id: int, query: str, answer: str):
    history_row = ChatHistory(
        session_id=session_id,
        user_id=user_id,
        query=query,
        answer=answer,
        timestamp=datetime.now()
    )
    db.add(history_row)
    db.commit()
    db.refresh(history_row)
    return history_row


# Fetch all chat history by session ID
def fetch_chat_history_for_session(db: Session, chat_session_id: int, user_id: str):
    return db.query(ChatHistory).filter(
        ChatHistory.session_id == chat_session_id,
        ChatHistory.user_id == user_id
    ).all()
