from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user_models import User
from app.db.database import get_db
from app.crud.user_crud import get_user_by_oid


router = APIRouter(
    prefix="/api",
    tags=["Users API"],
)

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# @router.post("/first-visit")
# async def handle_first_visit(email: str, db: Session = Depends(get_db)):
#     """
#     Endpoint to handle the first visit of a user by retrieving user details from the database.

#     Parameters:
#     email (str): The email of the user.
#     db (Session): The database session.

#     Returns:
#     dict: A dictionary containing the user's session information.
#     """
    
#     # Retrieve user details from the database
#     user = get_user_by_email(db, email)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Initialize the user session data
#     user_session_data = {
#         'user_name': user.name,
#         'user_email': user.email,
#         'session_history': [],
#         'current_session_id': None  # No active session initially
#     }
    
#     # Return the initialized session data
#     return user_session_data
