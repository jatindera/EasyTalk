from sqlalchemy.orm import Session
from app.models.chat_models import ChatSession, ChatHistory
from datetime import datetime
from sqlalchemy import text

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from typing import List
from sqlalchemy.exc import SQLAlchemyError


# Create a new chat session
def create_new_chat_session(db: Session, user_id: str, session_name: str = None)->str:
    chat_session = ChatSession(user_id=user_id, session_name=session_name)
    db.add(chat_session)  # Add the new chat session to the database session
    db.commit()           # Commit the transaction to insert the new row into the database
    db.refresh(chat_session)  # Refresh the chat_session to get the generated values from the database
    return chat_session.session_id  # Return the newly generated session_id


def get_chat_history_titles(db: Session, user_id: str):
    # Writing query because mappings, which returns dictionary, is not supported by ORM
    # query = text(
    #     "SELECT session_id, session_name FROM EasyTalk.chat_sessions WHERE user_id = :user_id order by created_at desc"
    # )
    # chat_history_titles = db.execute(query, {"user_id": user_id}).mappings().all()
    # return chat_history_titles
    return []


def get_chat_history_for_session(db: Session, session_id, user_id: str) -> dict:
    # Writing query because mappings, which returns dictionary, is not supported by ORM
    query = text(
        "SELECT query, answer FROM EasyTalk.chat_history WHERE session_id = :session_id and user_id = :user_id"
    )
    chat_history = (
        db.execute(query, {"session_id": session_id, "user_id": user_id})
        .mappings()
        .all()
    )
    return chat_history


def save_message(db: Session, session_id: str, role: str, content: str, user_id: str):
    db.add(
        ChatHistory(session_id=session_id, role=role, content=content, user_id=user_id)
    )
    db.commit()
