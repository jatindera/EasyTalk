from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# from app.utils.chat_utils import getSessionName
from app.services.user_service import get_authenticated_user
from app.db.database import get_db
from app.schemas.chat_schemas import ChatRequest
from app.schemas.user_schemas import UserCreate
from app.services import chat_service
from fastapi.responses import StreamingResponse


router = APIRouter(
    prefix="/api",
    tags=["Chat API"],
)

from fastapi.responses import StreamingResponse
import re


@router.post("/chat")
async def chat(
    request: ChatRequest,
    user: dict = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    question = request.query
    chat_session_id = request.chatSessionId
    user_id = user["user_id"]

    # Retrieve or create the user in the database
    user_record = chat_service.get_user_for_chat(db, user_id)
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
        user_id = chat_service.create_new_user_for_chat(db, userCreateObj)

    # Check or create the chat session ID
    if not chat_session_id:
        chat_session_id = chat_service.create_new_chat_session(db, user_id, question)
        # print("xxxxxxxxxxxxxxxx", chat_session_id)

    # Save the human message before streaming starts

    chat_service.save_message(db, chat_session_id, user_id, "human", question)

    # Streaming the response
    async def response_stream():
        ai_response = ""
        buffer = ""
        async for chunk in chat_service.create_chat_response_astream(
            db, question, chat_session_id, user_id
        ):
            # ai_response is to be saved in database. It is partial stream so we need to make it complete using reg.
            buffer += chunk
            # Try to yield a complete sentence by checking for punctuation
            if re.search(r"[.!?]\s$", buffer):
                ai_response += buffer
                buffer = ""

            # Yield chunk without any change to display on frontend. On Frontend, It will
            # magically be parsed as complete stream.
            yield chunk

        # Add the last incomplete chunk if any remaining

        # Add any remaining buffer content
        if buffer:
            ai_response += buffer
        # Save the complete AI response after streaming ends
        chat_service.save_message(db, chat_session_id, user_id, "ai", ai_response)

    if chat_session_id:
        headers = {"newChatSessionId": chat_session_id}
    else:
        headers = {}

    return StreamingResponse(
        response_stream(), media_type="text/plain", headers=headers
    )


@router.post("/chat-history")
def get_chat_history_titles(
    user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)
):
    user_id = user["user_id"]
    # Fetch chat history for the current user
    chat_history_titles = chat_service.get_chat_history_titles(db, user_id)
    # print(chat_history_titles)
    if not chat_history_titles:
        return {"chat_history_titles": ""}
    return {"chat_history_titles": chat_history_titles}


@router.post("/chat-history/{session_id}")
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
