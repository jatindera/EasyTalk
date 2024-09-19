from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.langchain_service import general_chat  # Import the general_chat function from the service
from app.utils.chat_utils import generate_session_id  # Import the generate_session_id function
from app.services.user_service import get_current_user, get_user_by_email, create_new_user
from app.db.database import get_db
from app.schemas.user_schemas import UserCreate
from app.schemas.chat_schemas import ChatRequest
from app.services.langchain_service import general_chat


router = APIRouter(
    prefix="/api",
    tags=["Chat API"],
)


@router.post("/llm-chat")
def llm_chat(request: ChatRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    query = request.query
    chatSessionId = request.chatSessionId
    # Step 1: Get the user's email from the authenticated `user` object
    email = user["email"]
    
    # # Step 2: Retrieve user from the database using the service function
    user_record = get_user_by_email(email, db)

    if not user_record:
        # If the user is not found, handle it as a first-time interaction and creaet new user
        userCreateObj = UserCreate(
            email=email,
            first_name=user["first_name"],
            last_name=user["last_name"],
            provide_name=user["provider_name"],
            provider_id=user["provider_id"],
            role=user["role"]
        )

        user_record = create_new_user(userCreateObj, db)
       
    new_chat = False
    if chatSessionId is None or chatSessionId == "":
        new_chat = True
    # Step 3: Determine the chat session ID
    if new_chat:
        # Step 4: If it's a new chat, generate a new session ID
        chatSessionId = generate_session_id()
        # Optionally, create a new chat session in the database
        # create_new_chat_session(db, user_record.id, session_id)
    # else:
    #     # Step 5: If not a new chat, retrieve the latest session ID for the user
    #     session_id = get_latest_session_id_for_user(db, user_record.id)
    #     if not session_id:
    #         # If no previous session found, create a new session ID
    #         session_id = generate_session_id()
    #         create_new_chat_session(db, user_record.id, session_id)

    # # Step 6: Call the generate_llm_response function with the session ID
    result = general_chat(query, chatSessionId)
    print(result)
    return result
    
    # # Step 7: Save the query and result to the chat history (database or other storage)
    # save_chat_to_database(db, session_id, query, result)
    
    # # Step 8: Return the result and session ID
    # return {"result": result, "session_id": session_id}


