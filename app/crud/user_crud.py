# app/crud/user_crud.py

from sqlalchemy.orm import Session
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate

def get_user_by_email(email: str, db: Session ):
    """
    Retrieve user details by email from the database.

    Parameters:
    db (Session): The database session.
    email (str): The email of the user.

    Returns:
    User: The user object or None if not found.
    """
    return db.query(User).filter(User.email == email).first()

def create_new_user(userCreate: UserCreate, db: Session):
     # Add the new user to the database session
    db_user = User(
        email=userCreate.email,
        first_name=userCreate.first_name,
        last_name=userCreate.last_name,
        provider_name=userCreate.provide_name,
        provider_id=userCreate.provider_id,
        role=userCreate.role,
        )
    db.add(db_user)
    
    # Commit the session to persist the new user in the database
    db.commit()
    
    # Refresh the new_user object to reflect the changes in the database
    db.refresh(db_user)
    
    # Return the newly created user
    return db_user