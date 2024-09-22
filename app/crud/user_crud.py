# app/crud/user_crud.py

from sqlalchemy.orm import Session
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate

def get_user_by_email(email: str, db: Session ):
    return db.query(User).filter(User.email == email).first()

def create_new_user(db: Session, user_create: UserCreate):
     # Add the new user to the database session
    db_user = User(
        email=user_create.email,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        provider_name=user_create.provider_name,
        provider_id=user_create.provider_id,
        role=user_create.role,
        )
    db.add(db_user)
    
    # Commit the session to persist the new user in the database
    db.commit()
    
    # Refresh the new_user object to reflect the changes in the database
    db.refresh(db_user)
    
    # Return the newly created user
    return db_user