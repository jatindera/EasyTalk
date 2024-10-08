# app/crud/user_crud.py

from sqlalchemy.orm import Session
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate


def get_user_by_userid(db: Session, user_id: str, )->UserCreate:
    return db.query(User).filter(User.user_id == user_id).first()


def create_new_user(db: Session, user_create: UserCreate)->str:
    # Add the new user to the database session
    print("xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy")
    print(user_create)
    db_user = User(
        user_id=user_create.user_id,
        email=user_create.email,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        ip_address=user_create.ip_address,
        provider_name=user_create.provider_name,
        role=user_create.role,
    )
    db.add(db_user)

    # Commit the session to persist the new user in the database
    db.commit()

    # Refresh the new_user object to reflect the changes in the database
    db.refresh(db_user)

    # Return the newly created user
    return db_user.user_id
