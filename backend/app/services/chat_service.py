from sqlalchemy.orm import Session
from app.crud import chat_crud
from typing import List
from app.services import user_service, langchain_service
from app.models.user_models import User
from app.schemas import user_schemas
from app.schemas.user_schemas import UserCreate


def getSessionName(name: str) -> str:
    return name[:60] if len(name) > 60 else name


def create_new_chat_session(
    db: Session, user_id: int, question: str
) -> str:
    print("==============Going to create new Chat Session Id==============")
    session_name = getSessionName(question)
    # Clear existing Chat Memory from Langchain. We only need to create Chat Memory per Chat Session
    langchain_service.clear_store()
    #Create new Chat Session ID
    chat_session_id = chat_crud.create_new_chat_session(db, user_id, session_name)
    return chat_session_id


def create_chat_history(
    db: Session, session_id: int, user_id: str, query: str, answer: str
) -> dict:
    history_row = chat_crud.create_chat_history(db, session_id, user_id, query, answer)
    return history_row


def get_chat_history_titles(db: Session, user_id: str):
    chat_history_titles = chat_crud.get_chat_history_titles(db, user_id)
    return chat_history_titles


def get_chat_history_for_session(db: Session, session_id: str, user_id: str):
    chat_history = chat_crud.get_chat_history_for_session(db, session_id, user_id)
    return chat_history


def fetch_chat_history_for_session(
    db: Session, chat_session_id: int, user_id: int
) -> List:
    # Fetch chat history for the given chat session ID and user ID
    chat_history = chat_crud.fetch_chat_history_for_session(
        db, chat_session_id, user_id
    )

    if not chat_history:
        raise ValueError(
            f"No chat history found for chat_session_id {chat_session_id} and user_id {user_id}"
        )

    return []

def get_user_for_chat(db: Session, user_id: str) -> UserCreate:
    user_record = user_service.get_user_by_userid(db,user_id)
    return user_record

def create_new_user_for_chat(db: Session, userCreate:user_schemas.UserCreate)->str:
    user_id = user_service.create_new_user(db,userCreate)
    return user_id


def create_chat_response(db: Session, question: str, chat_session_id: str, user_id: str):
    answer = langchain_service.generate_response(db, question, chat_session_id, user_id)
    return answer